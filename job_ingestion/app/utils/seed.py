import json
import asyncio
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.company import Company


async def seed_companies(db: AsyncSession, source_file: str = "data/companies.json") -> dict[str, int]:
    path = Path(source_file)
    if not path.exists():
        return {"inserted": 0, "updated": 0, "deleted": 0}

    payload = json.loads(path.read_text(encoding="utf-8"))
    companies = (await db.scalars(select(Company))).all()
    existing_by_token = {row.board_token: row for row in companies}
    inserted = 0
    updated = 0
    deleted = 0
    desired_tokens: set[str] = set()

    for item in payload:
        name = item.get("company") or item.get("name")
        platform = item.get("platform", "greenhouse")
        board_token = item.get("board_token")
        is_active = bool(item.get("is_active", True))
        platform_config = item.get("platform_config")
        if not name or not board_token:
            continue
        token = str(board_token)
        desired_tokens.add(token)

        existing = existing_by_token.get(token)
        if existing:
            existing.name = str(name)
            existing.platform = str(platform)
            existing.is_active = is_active
            existing.platform_config = platform_config if isinstance(platform_config, dict) else None
            updated += 1
            continue

        company = Company(
            name=str(name),
            platform=str(platform),
            board_token=token,
            is_active=is_active,
            platform_config=platform_config if isinstance(platform_config, dict) else None,
        )
        db.add(company)
        existing_by_token[token] = company
        inserted += 1

    for token, row in existing_by_token.items():
        if token in desired_tokens:
            continue
        await db.delete(row)
        deleted += 1

    await db.commit()
    return {"inserted": inserted, "updated": updated, "deleted": deleted}


async def _seed_from_cli() -> None:
    async with AsyncSessionLocal() as db:
        result = await seed_companies(db)
        print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    asyncio.run(_seed_from_cli())
