from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CheckoutSessionCreate(BaseModel):
    candidate_id: uuid.UUID
    plan: Literal["plus", "pro"]


class CheckoutSessionOut(BaseModel):
    url: str


class PortalSessionCreate(BaseModel):
    candidate_id: uuid.UUID


class PortalSessionOut(BaseModel):
    url: str


class BillingStatusOut(BaseModel):
    candidate_id: uuid.UUID
    plan_tier: str
    subscription_status: str
    plan_expires_at: datetime | None = None
    can_upgrade: bool
    can_manage: bool
    stripe_configured: bool = False
    effective_plan_tier: str = Field(
        description="Plan tier after expiry / past_due grace rules"
    )
