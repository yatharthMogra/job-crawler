from __future__ import annotations

from collections.abc import AsyncGenerator
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app


class _ExecuteResult:
    def __init__(self, rows: list[SimpleNamespace] | SimpleNamespace) -> None:
        self._rows = rows

    def fetchall(self) -> list[SimpleNamespace]:
        assert isinstance(self._rows, list)
        return self._rows

    def one(self) -> SimpleNamespace:
        assert isinstance(self._rows, SimpleNamespace)
        return self._rows


class _DummySession:
    def __init__(
        self,
        *,
        globals_row: SimpleNamespace,
        group_rows: list[SimpleNamespace],
        title_rows: list[SimpleNamespace],
    ) -> None:
        self._globals_row = globals_row
        self._group_rows = group_rows
        self._title_rows = title_rows
        self._call_count = 0

    async def execute(self, _stmt):
        self._call_count += 1
        if self._call_count == 1:
            return _ExecuteResult(self._globals_row)
        if self._call_count == 2:
            return _ExecuteResult(self._group_rows)
        return _ExecuteResult(self._title_rows)


def _override(session: _DummySession):
    async def _dummy_db() -> AsyncGenerator[_DummySession, None]:
        yield session

    app.dependency_overrides[get_db] = _dummy_db


def test_taxonomy_health_flags_domains_and_caps_titles() -> None:
    globals_row = SimpleNamespace(total=150, no_pool=17)
    group_rows = [
        SimpleNamespace(domain="Software", total=100, no_pool=15),
        SimpleNamespace(domain="Research_Science", total=50, no_pool=2),
    ]
    title_rows = [
        SimpleNamespace(domain="Software", title="Systems Engineer", cnt=8),
        SimpleNamespace(domain="Software", title="Research Scientist", cnt=5),
        SimpleNamespace(domain="Research_Science", title="Principal Scientist", cnt=2),
    ]
    session = _DummySession(globals_row=globals_row, group_rows=group_rows, title_rows=title_rows)
    _override(session)
    client = TestClient(app)

    response = client.get("/admin/taxonomy-health")
    assert response.status_code == 200
    body = response.json()

    assert body["group_by"] == "domain"
    assert body["total_active_enriched"] == 150
    assert body["global_no_pool_count"] == 17
    assert body["global_no_pool_pct"] == 11.3
    assert body["domains_flagged"] == 1
    assert body["domains_needing_review"] == 1

    software = next(d for d in body["domains"] if d["domain"] == "Software")
    assert software["no_pool_pct"] == 15.0
    assert software["flagged"] is True
    assert software["needs_review"] is True
    assert software["acknowledged"] is False
    assert len(software["top_no_pool_titles"]) == 2
    assert software["top_no_pool_titles"][0]["title"] == "Systems Engineer"

    research = next(d for d in body["domains"] if d["domain"] == "Research_Science")
    assert research["flagged"] is False

    app.dependency_overrides.clear()


def test_taxonomy_health_role_group_by() -> None:
    globals_row = SimpleNamespace(total=100, no_pool=20)
    group_rows = [
        SimpleNamespace(domain="BACKEND_ENGINEER", total=40, no_pool=12),
        SimpleNamespace(domain="(none)", total=10, no_pool=10),
    ]
    title_rows = [
        SimpleNamespace(domain="BACKEND_ENGINEER", title="Backend Engineer", cnt=7),
    ]
    session = _DummySession(globals_row=globals_row, group_rows=group_rows, title_rows=title_rows)
    _override(session)
    client = TestClient(app)

    response = client.get("/admin/taxonomy-health?group_by=role")
    assert response.status_code == 200
    body = response.json()
    assert body["group_by"] == "role"
    assert body["total_active_enriched"] == 100
    assert body["global_no_pool_count"] == 20
    assert body["domains_flagged"] == 2
    assert body["domains"][0]["domain"] == "BACKEND_ENGINEER"

    app.dependency_overrides.clear()


def test_taxonomy_health_top_titles_limited_to_ten() -> None:
    globals_row = SimpleNamespace(total=20, no_pool=20)
    group_rows = [SimpleNamespace(domain="Software", total=20, no_pool=20)]
    title_rows = [
        SimpleNamespace(domain="Software", title=f"Title {index}", cnt=20 - index)
        for index in range(15)
    ]
    session = _DummySession(globals_row=globals_row, group_rows=group_rows, title_rows=title_rows)
    _override(session)
    client = TestClient(app)

    response = client.get("/admin/taxonomy-health")
    assert response.status_code == 200
    software = response.json()["domains"][0]
    assert len(software["top_no_pool_titles"]) == 10

    app.dependency_overrides.clear()


def test_taxonomy_health_excludes_acknowledged_from_needs_review(monkeypatch) -> None:
    import app.api.admin as admin_api

    monkeypatch.setattr(
        admin_api,
        "list_acknowledgements",
        lambda _group_by: {"Software": "2026-06-12T12:00:00+00:00"},
    )

    globals_row = SimpleNamespace(total=100, no_pool=15)
    group_rows = [SimpleNamespace(domain="Software", total=100, no_pool=15)]
    session = _DummySession(globals_row=globals_row, group_rows=group_rows, title_rows=[])
    _override(session)
    client = TestClient(app)

    response = client.get("/admin/taxonomy-health")
    assert response.status_code == 200
    body = response.json()
    software = body["domains"][0]
    assert software["flagged"] is True
    assert software["acknowledged"] is True
    assert software["needs_review"] is False
    assert body["domains_needing_review"] == 0

    app.dependency_overrides.clear()
