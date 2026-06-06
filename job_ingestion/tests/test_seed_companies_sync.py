from __future__ import annotations

import json

import pytest

from app.models.company import Company
from app.utils.seed import seed_companies


class _ScalarResult:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows


class _FakeSession:
    def __init__(self, companies: list[Company]):
        self.companies = companies
        self.committed = False

    async def scalars(self, stmt):  # noqa: ARG002
        return _ScalarResult(self.companies)

    def add(self, company: Company) -> None:
        self.companies.append(company)

    async def delete(self, company: Company) -> None:
        self.companies.remove(company)

    async def commit(self) -> None:
        self.committed = True


@pytest.mark.asyncio
async def test_seed_companies_hard_deletes_rows_missing_from_source(tmp_path) -> None:
    existing_keep = Company(name="Anthropic", platform="greenhouse", board_token="anthropic", is_active=True)
    existing_stale = Company(name="ScaleAI", platform="lever", board_token="scale-ai", is_active=True)
    session = _FakeSession(companies=[existing_keep, existing_stale])

    source = tmp_path / "companies.json"
    source.write_text(
        json.dumps(
            [
                {"company": "Anthropic", "platform": "greenhouse", "board_token": "anthropic", "is_active": True},
                {"company": "OpenAI", "platform": "ashby", "board_token": "openai", "is_active": True},
            ]
        ),
        encoding="utf-8",
    )

    result = await seed_companies(session, source_file=str(source))

    assert result == {"inserted": 1, "updated": 1, "deleted": 1}
    assert session.committed is True
    tokens = sorted(company.board_token for company in session.companies)
    assert tokens == ["anthropic", "openai"]
