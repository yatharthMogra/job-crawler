from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

DEFAULT_FETCH_SCHEDULE: dict[str, Any] = {
    "tick_minutes": 10,
    "batch_cap": 200,
    "default_fetch_tier": 2,
    "waas": {"dedicated_job": True, "interval_minutes": 30},
    "intervals": {
        "workatastartup": {"1": 30},
        "greenhouse": {"1": 45, "2": 180, "3": 720},
        "lever": {"1": 45, "2": 180, "3": 720},
        "ashby": {"1": 120, "2": 480, "3": 1440},
        "workday": {"1": 240, "2": 720, "3": 2880},
        "oracle_hcm": {"1": 360, "2": 1440, "3": 2880},
        "icims": {"1": 360, "2": 1440, "3": 2880},
        "successfactors": {"1": 360, "2": 1440, "3": 2880},
        "workable": {"1": 180, "2": 720, "3": 1440},
        "smartrecruiters": {"1": 45, "2": 180, "3": 720},
        "bamboohr": {"1": 45, "2": 180, "3": 720},
        "google_careers": {"1": 360, "2": 720, "3": 1440},
        "amazon_jobs": {"1": 360, "2": 720, "3": 1440},
        "uber_careers": {"1": 360, "2": 720, "3": 1440},
        "eightfold": {"1": 45, "2": 180, "3": 720},
    },
    "throttles": {
        "default_concurrency": 8,
        "platforms": {
            "ashby": {"concurrency": 1, "inter_company_seconds": 3},
            "workday": {"concurrency": 3, "inter_company_seconds": 1},
            "oracle_hcm": {"concurrency": 2},
            "icims": {"concurrency": 1},
            "successfactors": {"concurrency": 1},
            "smartrecruiters": {"concurrency": 3},
            "bamboohr": {"concurrency": 3},
            "google_careers": {"concurrency": 1},
            "amazon_jobs": {"concurrency": 1},
            "uber_careers": {"concurrency": 1},
            "eightfold": {"concurrency": 3},
        },
    },
}

DEFAULT_INTERVAL_MINUTES = 720
VALID_TIERS = frozenset({1, 2, 3})


class WaasConfig(BaseModel):
    dedicated_job: bool = True
    interval_minutes: int = Field(default=30, ge=1)


class PlatformThrottle(BaseModel):
    concurrency: int = Field(default=8, ge=1)
    inter_company_seconds: float = Field(default=0, ge=0)


class ThrottleConfig(BaseModel):
    default_concurrency: int = Field(default=8, ge=1)
    platforms: dict[str, PlatformThrottle] = Field(default_factory=dict)

    def for_platform(self, platform: str) -> PlatformThrottle:
        override = self.platforms.get(platform)
        if override is None:
            return PlatformThrottle(concurrency=self.default_concurrency)
        return PlatformThrottle(
            concurrency=override.concurrency,
            inter_company_seconds=override.inter_company_seconds,
        )


class FetchScheduleConfig(BaseModel):
    tick_minutes: int = Field(default=10, ge=1)
    batch_cap: int = Field(default=200, ge=1)
    default_fetch_tier: int = Field(default=2, ge=1, le=3)
    waas: WaasConfig = Field(default_factory=WaasConfig)
    intervals: dict[str, dict[str, int]] = Field(default_factory=dict)
    throttles: ThrottleConfig = Field(default_factory=ThrottleConfig)

    @field_validator("default_fetch_tier")
    @classmethod
    def validate_default_tier(cls, value: int) -> int:
        if value not in VALID_TIERS:
            raise ValueError("default_fetch_tier must be 1, 2, or 3")
        return value

    def interval_minutes(self, platform: str, tier: int) -> int:
        tier_key = str(tier)
        platform_intervals = self.intervals.get(platform, {})
        if tier_key in platform_intervals:
            return max(1, int(platform_intervals[tier_key]))
        if "2" in platform_intervals:
            return max(1, int(platform_intervals["2"]))
        for fallback_platform in ("greenhouse", "workday"):
            fallback = self.intervals.get(fallback_platform, {})
            if tier_key in fallback:
                return max(1, int(fallback[tier_key]))
        return DEFAULT_INTERVAL_MINUTES

    def num_shards(self, platform: str, tier: int) -> int:
        interval = self.interval_minutes(platform, tier)
        return max(1, (interval + self.tick_minutes - 1) // self.tick_minutes)


def parse_fetch_schedule_json(raw: Optional[str]) -> FetchScheduleConfig:
    if not raw or not raw.strip():
        return FetchScheduleConfig.model_validate(DEFAULT_FETCH_SCHEDULE)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"FETCH_SCHEDULE_JSON is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("FETCH_SCHEDULE_JSON must be a JSON object")
    merged = {**DEFAULT_FETCH_SCHEDULE, **payload}
    merged_intervals: dict[str, dict[str, int]] = {}
    for platform, tiers in DEFAULT_FETCH_SCHEDULE["intervals"].items():
        merged_intervals[platform] = dict(tiers)
    for platform, tiers in (payload.get("intervals") or {}).items():
        platform_tiers = dict(merged_intervals.get(platform, {}))
        platform_tiers.update({str(k): int(v) for k, v in tiers.items()})
        merged_intervals[platform] = platform_tiers
    merged["intervals"] = merged_intervals
    default_throttles = DEFAULT_FETCH_SCHEDULE["throttles"]
    payload_throttles = payload.get("throttles") or {}
    merged["throttles"] = {
        "default_concurrency": payload_throttles.get(
            "default_concurrency", default_throttles["default_concurrency"]
        ),
        "platforms": {
            **default_throttles["platforms"],
            **(payload_throttles.get("platforms") or {}),
        },
    }
    default_waas = DEFAULT_FETCH_SCHEDULE["waas"]
    payload_waas = payload.get("waas") or {}
    merged["waas"] = {**default_waas, **payload_waas}
    return FetchScheduleConfig.model_validate(merged)


@lru_cache(maxsize=8)
def get_fetch_schedule(fetch_schedule_json: str = "") -> FetchScheduleConfig:
    return parse_fetch_schedule_json(fetch_schedule_json or None)
