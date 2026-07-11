from __future__ import annotations

import uuid

import stripe
import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_api_key
from app.config import Settings, get_settings
from app.database import get_db
from app.schemas.billing import (
    BillingStatusOut,
    CheckoutSessionCreate,
    CheckoutSessionOut,
    PortalSessionCreate,
    PortalSessionOut,
)
from app.services import stripe_billing

log = structlog.get_logger(__name__)

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post(
    "/checkout-session",
    response_model=CheckoutSessionOut,
    dependencies=[Depends(require_api_key)],
)
async def create_checkout_session(
    payload: CheckoutSessionCreate,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> CheckoutSessionOut:
    if not settings.stripe_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Billing is not configured",
        )
    try:
        url = await stripe_billing.create_checkout_session(
            db,
            candidate_id=payload.candidate_id,
            plan=payload.plan,
            settings=settings,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    except stripe.StripeError as exc:
        log.exception("billing.checkout_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to start checkout",
        ) from exc
    return CheckoutSessionOut(url=url)


@router.post(
    "/portal-session",
    response_model=PortalSessionOut,
    dependencies=[Depends(require_api_key)],
)
async def create_portal_session(
    payload: PortalSessionCreate,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> PortalSessionOut:
    if not settings.stripe_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Billing is not configured",
        )
    try:
        url = await stripe_billing.create_portal_session(
            db,
            candidate_id=payload.candidate_id,
            settings=settings,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except stripe.StripeError as exc:
        log.exception("billing.portal_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to open billing portal",
        ) from exc
    return PortalSessionOut(url=url)


@router.get(
    "/status",
    response_model=BillingStatusOut,
    dependencies=[Depends(require_api_key)],
)
async def billing_status(
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> BillingStatusOut:
    try:
        candidate = await stripe_billing.get_candidate_or_raise(db, candidate_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    effective = stripe_billing.effective_plan_tier(
        candidate.plan_tier,
        candidate.subscription_status,
        candidate.plan_expires_at,
        past_due_grace_days=settings.billing_past_due_grace_days,
    )
    can_manage = bool(candidate.stripe_customer_id) and settings.stripe_configured
    can_upgrade = effective == "free" or (
        effective == "plus" and settings.stripe_configured
    )
    return BillingStatusOut(
        candidate_id=candidate.id,
        plan_tier=candidate.plan_tier,
        subscription_status=candidate.subscription_status,
        plan_expires_at=candidate.plan_expires_at,
        can_upgrade=can_upgrade,
        can_manage=can_manage,
        stripe_configured=settings.stripe_configured,
        effective_plan_tier=effective,
    )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    if not settings.stripe_webhook_secret.strip():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Webhook secret not configured",
        )
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.stripe_webhook_secret,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload") from exc
    except stripe.SignatureVerificationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature") from exc

    # stripe returns StripeObject; convert for JSON-safe storage / handling
    event_dict = event.to_dict() if hasattr(event, "to_dict") else dict(event)
    try:
        await stripe_billing.handle_stripe_event(db, event_dict, settings)
    except Exception:
        log.exception(
            "billing.webhook_handler_failed",
            event_type=event_dict.get("type"),
            event_id=event_dict.get("id"),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook handler failed",
        )
    return {"received": True}
