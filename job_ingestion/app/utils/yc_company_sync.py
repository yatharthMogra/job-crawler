from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.ingestion.connectors.yc_directory import DirectoryCrawlResult, WorkdayDiscovery
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

DEFAULT_COMPANIES_PATH = Path("data/companies.json")


@dataclass
class YCCompanySyncResult:
    inserted: int = 0
    skipped_existing: int = 0
    workday_flagged: int = 0


def _load_companies_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def _append_companies_json(path: Path, entries: list[dict[str, Any]]) -> None:
    if not entries:
        return
    existing = _load_companies_json(path)
    existing_tokens = {str(item.get("board_token")) for item in existing if item.get("board_token")}
    for entry in entries:
        token = str(entry.get("board_token"))
        if token in existing_tokens:
            continue
        existing.append(entry)
        existing_tokens.add(token)
    path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")


def _workday_entry(discovery: WorkdayDiscovery, company_name: str) -> dict[str, Any]:
    return {
        "company": company_name,
        "platform": "workday",
        "board_token": discovery.board_token,
        "platform_config": {
            "tenant": discovery.tenant,
            "instance": discovery.instance,
        },
        "is_active": False,
        "requires_review": True,
    }


async def upsert_discovered_companies(
    db: AsyncSession,
    result: DirectoryCrawlResult,
    *,
    companies_path: Path | str = DEFAULT_COMPANIES_PATH,
    workday_company_names: dict[str, str] | None = None,
) -> YCCompanySyncResult:
    path = Path(companies_path)
    sync_result = YCCompanySyncResult(skipped_existing=result.skipped_existing)
    existing_rows = (await db.scalars(select(Company))).all()
    existing_tokens = {row.board_token for row in existing_rows}
    json_entries: list[dict[str, Any]] = []
    workday_names = workday_company_names or {}

    async def _insert(name: str, platform: str, board_token: str, **extra: Any) -> None:
        if board_token in existing_tokens:
            sync_result.skipped_existing += 1
            return
        company = Company(
            name=name,
            platform=platform,
            board_token=board_token,
            is_active=extra.get("is_active", True),
            requires_review=extra.get("requires_review", False),
            platform_config=extra.get("platform_config"),
        )
        db.add(company)
        existing_tokens.add(board_token)
        sync_result.inserted += 1
        json_entries.append(
            {
                "company": name,
                "platform": platform,
                "board_token": board_token,
                "is_active": company.is_active,
                **(
                    {"platform_config": company.platform_config}
                    if company.platform_config
                    else {}
                ),
                **({"requires_review": True} if company.requires_review else {}),
            }
        )

    for token in result.greenhouse_tokens:
        await _insert(name=token.replace("-", " ").title(), platform="greenhouse", board_token=token)
    for slug in result.lever_slugs:
        await _insert(name=slug.replace("-", " ").title(), platform="lever", board_token=slug)
    for slug in result.ashby_slugs:
        await _insert(name=slug.replace("-", " ").title(), platform="ashby", board_token=slug)
    for discovery in result.workday_discoveries:
        name = workday_names.get(discovery.board_token, discovery.tenant.replace("-", " ").title())
        if discovery.board_token in existing_tokens:
            sync_result.skipped_existing += 1
            continue
        company = Company(
            name=name,
            platform="workday",
            board_token=discovery.board_token,
            is_active=False,
            requires_review=True,
            platform_config={
                "tenant": discovery.tenant,
                "instance": discovery.instance,
            },
        )
        db.add(company)
        existing_tokens.add(discovery.board_token)
        sync_result.inserted += 1
        sync_result.workday_flagged += 1
        json_entries.append(_workday_entry(discovery, name))

    _append_companies_json(path, json_entries)
    await db.commit()
    return sync_result
