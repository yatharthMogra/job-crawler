from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import stripe
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models.billing_event import BillingEvent
from app.models.candidate import Candidate

log = structlog.get_logger(__name__)

PlanKey = Literal["plus", "pro"]
PAID_STATUSES = frozenset({"active", "past_due", "trialing"})


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def configure_stripe(settings: Settings) -> None:
    stripe.api_key = settings.stripe_secret_key


def price_id_for_plan(settings: Settings, plan: PlanKey) -> str:
    if plan == "plus":
        return settings.stripe_price_plus.strip()
    return settings.stripe_price_pro.strip()


def plan_tier_from_price_id(settings: Settings, price_id: str | None) -> str:
    if not price_id:
        return "free"
    if price_id == settings.stripe_price_plus.strip():
        return "plus"
    if price_id == settings.stripe_price_pro.strip():
        return "pro"
    return "free"


def effective_plan_tier(
    plan_tier: str | None,
    subscription_status: str | None,
    plan_expires_at: datetime | None,
    *,
    past_due_grace_days: int = 3,
    now: datetime | None = None,
) -> str:
    """Resolve access tier from stored billing fields."""
    raw = (plan_tier or "free").strip().lower()
    if raw not in ("plus", "pro"):
        return "free"

    status = (subscription_status or "none").strip().lower()
    now = now or _utcnow()
    expires = plan_expires_at
    if expires is not None and expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    if status == "past_due":
        if expires is None:
            return raw
        grace_end = expires + timedelta(days=past_due_grace_days)
        return raw if now <= grace_end else "free"

    if status in PAID_STATUSES:
        if expires is not None and now > expires:
            return "free"
        return raw

    # canceled / incomplete / none — honor period end if still set
    if expires is not None and now <= expires and status == "canceled":
        return raw

    # Manual comps / legacy rows may set plan_tier without Stripe status.
    if status in ("none", "") and expires is None:
        return raw
    if status in ("none", "") and expires is not None and now <= expires:
        return raw

    return "free"


async def get_candidate_or_raise(db: AsyncSession, candidate_id: uuid.UUID) -> Candidate:
    candidate = await db.get(Candidate, candidate_id)
    if candidate is None:
        raise ValueError("Candidate not found")
    return candidate


async def ensure_stripe_customer(
    db: AsyncSession,
    candidate: Candidate,
    settings: Settings,
) -> str:
    configure_stripe(settings)
    if candidate.stripe_customer_id:
        return candidate.stripe_customer_id

    customer = stripe.Customer.create(
        email=candidate.email,
        name=candidate.name,
        metadata={"candidate_id": str(candidate.id)},
    )
    candidate.stripe_customer_id = customer["id"]
    await db.commit()
    await db.refresh(candidate)
    return candidate.stripe_customer_id


async def create_checkout_session(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    plan: PlanKey,
    settings: Settings,
) -> str:
    if not settings.stripe_configured:
        raise RuntimeError("Stripe is not configured")

    configure_stripe(settings)
    candidate = await get_candidate_or_raise(db, candidate_id)
    customer_id = await ensure_stripe_customer(db, candidate, settings)
    price_id = price_id_for_plan(settings, plan)
    if not price_id:
        raise RuntimeError(f"Missing Stripe price for plan={plan}")

    session = stripe.checkout.Session.create(
        mode="subscription",
        customer=customer_id,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=settings.billing_success_url,
        cancel_url=settings.billing_cancel_url,
        client_reference_id=str(candidate.id),
        metadata={"candidate_id": str(candidate.id), "plan_tier": plan},
        subscription_data={"metadata": {"candidate_id": str(candidate.id), "plan_tier": plan}},
        allow_promotion_codes=True,
    )
    url = session.get("url")
    if not url:
        raise RuntimeError("Stripe Checkout Session missing url")
    return url


async def create_portal_session(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    settings: Settings,
) -> str:
    if not settings.stripe_configured:
        raise RuntimeError("Stripe is not configured")

    configure_stripe(settings)
    candidate = await get_candidate_or_raise(db, candidate_id)
    if not candidate.stripe_customer_id:
        raise RuntimeError("No Stripe customer for this candidate")

    session = stripe.billing_portal.Session.create(
        customer=candidate.stripe_customer_id,
        return_url=settings.billing_success_url.split("?")[0],
    )
    url = session.get("url")
    if not url:
        raise RuntimeError("Stripe Portal Session missing url")
    return url


def _ts_to_dt(value: int | float | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromtimestamp(int(value), tz=timezone.utc)


def _subscription_price_id(subscription: dict[str, Any]) -> str | None:
    items = (subscription.get("items") or {}).get("data") or []
    if not items:
        return None
    price = items[0].get("price") or {}
    if isinstance(price, str):
        return price
    return price.get("id")


async def _find_candidate_for_subscription(
    db: AsyncSession,
    subscription: dict[str, Any],
) -> Candidate | None:
    meta = subscription.get("metadata") or {}
    candidate_id_raw = meta.get("candidate_id")
    if candidate_id_raw:
        try:
            candidate = await db.get(Candidate, uuid.UUID(str(candidate_id_raw)))
            if candidate is not None:
                return candidate
        except ValueError:
            pass

    customer_id = subscription.get("customer")
    if isinstance(customer_id, dict):
        customer_id = customer_id.get("id")
    if customer_id:
        result = await db.execute(
            select(Candidate).where(Candidate.stripe_customer_id == str(customer_id))
        )
        candidate = result.scalar_one_or_none()
        if candidate is not None:
            return candidate

    sub_id = subscription.get("id")
    if sub_id:
        result = await db.execute(
            select(Candidate).where(Candidate.stripe_subscription_id == str(sub_id))
        )
        return result.scalar_one_or_none()
    return None


async def apply_subscription_to_candidate(
    db: AsyncSession,
    candidate: Candidate,
    subscription: dict[str, Any],
    settings: Settings,
) -> None:
    status = str(subscription.get("status") or "none")
    price_id = _subscription_price_id(subscription)
    tier = plan_tier_from_price_id(settings, price_id)
    meta_tier = (subscription.get("metadata") or {}).get("plan_tier")
    if meta_tier in ("plus", "pro"):
        tier = meta_tier

    candidate.stripe_subscription_id = subscription.get("id") or candidate.stripe_subscription_id
    customer_id = subscription.get("customer")
    if isinstance(customer_id, dict):
        customer_id = customer_id.get("id")
    if customer_id and not candidate.stripe_customer_id:
        candidate.stripe_customer_id = str(customer_id)

    candidate.subscription_status = status
    candidate.plan_expires_at = _ts_to_dt(subscription.get("current_period_end"))

    if status in ("active", "trialing", "past_due"):
        candidate.plan_tier = tier if tier in ("plus", "pro") else candidate.plan_tier
        if candidate.plan_tier not in ("plus", "pro"):
            candidate.plan_tier = "plus"
    elif status in ("canceled", "unpaid", "incomplete_expired"):
        expires = candidate.plan_expires_at
        if expires is not None and expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if expires is None or _utcnow() > expires:
            candidate.plan_tier = "free"
            candidate.stripe_subscription_id = None
    else:
        # incomplete etc. — leave tier until paid
        pass

    log.info(
        "billing.subscription_applied",
        candidate_id=str(candidate.id),
        plan_tier=candidate.plan_tier,
        subscription_status=candidate.subscription_status,
        subscription_id=candidate.stripe_subscription_id,
    )


async def handle_stripe_event(
    db: AsyncSession,
    event: dict[str, Any],
    settings: Settings,
) -> None:
    event_id = str(event.get("id") or "")
    event_type = str(event.get("type") or "")
    data_object = (event.get("data") or {}).get("object") or {}

    if not event_id:
        raise ValueError("Stripe event missing id")

    existing = await db.scalar(
        select(BillingEvent.id).where(BillingEvent.stripe_event_id == event_id)
    )
    if existing is not None:
        log.info("billing.webhook_duplicate", stripe_event_id=event_id, event_type=event_type)
        return

    candidate: Candidate | None = None

    if event_type == "checkout.session.completed":
        ref = data_object.get("client_reference_id") or (data_object.get("metadata") or {}).get(
            "candidate_id"
        )
        if ref:
            try:
                candidate = await db.get(Candidate, uuid.UUID(str(ref)))
            except ValueError:
                candidate = None
        sub_id = data_object.get("subscription")
        if candidate and sub_id:
            configure_stripe(settings)
            subscription = stripe.Subscription.retrieve(str(sub_id))
            await apply_subscription_to_candidate(db, candidate, dict(subscription), settings)

    elif event_type in (
        "customer.subscription.updated",
        "customer.subscription.deleted",
        "customer.subscription.created",
    ):
        candidate = await _find_candidate_for_subscription(db, data_object)
        if candidate is not None:
            await apply_subscription_to_candidate(db, candidate, data_object, settings)
            if event_type == "customer.subscription.deleted":
                candidate.plan_tier = "free"
                candidate.subscription_status = "canceled"
                candidate.stripe_subscription_id = None

    elif event_type in ("invoice.paid", "invoice.payment_failed"):
        sub_id = data_object.get("subscription")
        customer_id = data_object.get("customer")
        if sub_id:
            configure_stripe(settings)
            subscription = stripe.Subscription.retrieve(str(sub_id))
            candidate = await _find_candidate_for_subscription(db, dict(subscription))
            if candidate is not None:
                await apply_subscription_to_candidate(db, candidate, dict(subscription), settings)
        elif customer_id:
            result = await db.execute(
                select(Candidate).where(Candidate.stripe_customer_id == str(customer_id))
            )
            candidate = result.scalar_one_or_none()
            if candidate is not None and event_type == "invoice.payment_failed":
                candidate.subscription_status = "past_due"

    db.add(
        BillingEvent(
            stripe_event_id=event_id,
            event_type=event_type,
            payload=event,
            candidate_id=candidate.id if candidate else None,
        )
    )
    await db.commit()
