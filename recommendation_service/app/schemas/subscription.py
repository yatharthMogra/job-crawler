from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class SubscriptionCreateIn(BaseModel):
    candidate_id: uuid.UUID
    pool_names: list[str] = Field(min_length=1)


class SubscriptionOut(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    pool_name: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SubscriptionListOut(BaseModel):
    candidate_id: uuid.UUID
    subscriptions: list[SubscriptionOut]


class SubscriptionUpdateIn(BaseModel):
    pool_names: list[str] = Field(min_length=1)
    is_active: bool = True
