from __future__ import annotations

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.greenhouse import (
    GreenhouseConnector,
    _board_token,
    _careers_urls,
    _job_passes_domain_check,
    _merge_jobs,
    _should_validate_domain,
    discover_job_ids_from_html,
)
from app.models.company import Company


def _greenhouse_company(**overrides: object) -> Company:
    defaults: dict[str, object] = {
        "name": "Example Corp",
        "platform": "greenhouse",
        "board_token": "examplecorp",
        "platform_config": None,
        "is_active": True,
    }
    defaults.update(overrides)
    return Company(**defaults)  # type: ignore[arg-type]


CAREERS_HTML = """
<html>
<body>
  <a href="https://careers.example.com/openings?gh_jid=1001">Engineer</a>
  <a href="https://job-boards.greenhouse.io/examplecorp/jobs/1002">PM</a>
  <a href="/jobs/1003/designer">Designer</a>
  <script src="https://boards-api.greenhouse.io/v1/boards/examplecorp/embed?for=examplecorp"></script>
</body>
</html>
"""

LIST_JOB_1 = {
    "id": 1,
    "title": "Listed Role",
    "content": "<p>Listed</p>",
    "absolute_url": "https://boards.greenhouse.io/examplecorp/jobs/1",
    "location": {"name": "Remote"},
    "departments": [],
    "updated_at": "2026-01-01T00:00:00Z",
    "metadata": [],
}

LIST_JOB_2 = {
    "id": 2,
    "title": "Another Listed",
    "content": "<p>Another</p>",
    "absolute_url": "https://boards.greenhouse.io/examplecorp/jobs/2",
    "location": {"name": "NYC"},
    "departments": [],
    "updated_at": "2026-01-02T00:00:00Z",
    "metadata": [],
}

DETAIL_JOB_3 = {
    "id": 3,
    "title": "Careers Only",
    "content": "<p>From careers page</p>",
    "absolute_url": "https://careers.example.com/jobs?gh_jid=3",
    "location": {"name": "SF"},
    "departments": [{"name": "Engineering"}],
    "updated_at": "2026-01-03T00:00:00Z",
    "metadata": [],
}


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def test_discover_job_ids_from_html_gh_jid_and_paths() -> None:
    ids = discover_job_ids_from_html(
        CAREERS_HTML,
        "https://careers.example.com/jobs",
    )
    assert ids == {"1001", "1002", "1003"}


def test_discover_job_ids_ignores_jobs_path_without_greenhouse_signal() -> None:
    html = '<a href="/jobs/9999/example">No GH signal</a>'
    ids = discover_job_ids_from_html(html, "https://careers.example.com/jobs")
    assert ids == set()


def test_discover_job_ids_board_links_without_careers_path() -> None:
    html = '<a href="https://boards.greenhouse.io/acme/jobs/42">Role</a>'
    ids = discover_job_ids_from_html(html, "https://careers.acme.com/")
    assert ids == {"42"}


def test_merge_jobs_list_wins_on_conflict() -> None:
    list_job = {**LIST_JOB_1, "title": "From List"}
    extra_job = {**LIST_JOB_1, "title": "From Detail"}
    merged = _merge_jobs([list_job], [extra_job])
    assert len(merged) == 1
    assert merged[0]["title"] == "From List"


def test_merge_jobs_adds_careers_only() -> None:
    merged = _merge_jobs([LIST_JOB_1], [DETAIL_JOB_3])
    assert {str(j["id"]) for j in merged} == {"1", "3"}


def test_careers_urls_primary_and_extras() -> None:
    company = _greenhouse_company(
        platform_config={
            "careers_url": "https://careers.example.com/jobs",
            "careers_urls": [
                "https://careers.example.com/search",
                "https://careers.example.com/jobs",
            ],
        },
    )
    assert _careers_urls(company) == [
        "https://careers.example.com/jobs",
        "https://careers.example.com/search",
    ]


def test_board_token_override() -> None:
    company = _greenhouse_company(
        board_token="c3ai",
        platform_config={"board_token_override": "c3iot"},
    )
    assert _board_token(company) == "c3iot"


def test_should_validate_domain_defaults_true_with_careers_url() -> None:
    company = _greenhouse_company(
        platform_config={"careers_url": "https://careers.example.com/jobs"},
    )
    assert _should_validate_domain(company) is True


def test_should_validate_domain_respects_explicit_false() -> None:
    company = _greenhouse_company(
        platform_config={
            "careers_url": "https://careers.example.com/jobs",
            "validate_absolute_url_domain": False,
        },
    )
    assert _should_validate_domain(company) is False


def test_job_passes_domain_check_accepts_careers_and_greenhouse() -> None:
    careers = ["https://careers.example.com/jobs"]
    assert _job_passes_domain_check(
        {"absolute_url": "https://careers.example.com/jobs?gh_jid=1"},
        careers,
    )
    assert _job_passes_domain_check(
        {"absolute_url": "https://boards.greenhouse.io/examplecorp/jobs/1"},
        careers,
    )
    assert not _job_passes_domain_check(
        {"absolute_url": "https://other-company.com/jobs/1"},
        careers,
    )


@pytest.mark.asyncio
async def test_greenhouse_list_only(monkeypatch) -> None:
    captured: list[str] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object], status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, str] | None = None):  # noqa: ARG002
            captured.append(url)
            return _FakeResponse({"jobs": [LIST_JOB_1, LIST_JOB_2]})

    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.httpx.AsyncClient",
        _FakeClient,
    )

    connector = GreenhouseConnector()
    company = _greenhouse_company()
    jobs = await connector.fetch_jobs(company)

    assert len(jobs) == 2
    assert captured == ["https://boards-api.greenhouse.io/v1/boards/examplecorp/jobs"]


@pytest.mark.asyncio
async def test_greenhouse_supplement_merge(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(
            self,
            payload: dict[str, object] | None = None,
            status_code: int = 200,
            text: str = "",
        ) -> None:
            self._payload = payload
            self.status_code = status_code
            self.text = text

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise ConnectorFetchError(f"HTTP {self.status_code}")

        def json(self) -> dict[str, object]:
            assert self._payload is not None
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, str] | None = None):  # noqa: ARG002
            if url.endswith("/jobs") and "/jobs/" not in url.replace("/jobs", "", 1):
                return _FakeResponse({"jobs": [LIST_JOB_1, LIST_JOB_2]})
            if url.endswith("/jobs/3"):
                return _FakeResponse(DETAIL_JOB_3)
            return _FakeResponse(None, status_code=404)

    async def _fake_careers_html(_self, _url: str) -> str:
        return '<a href="?gh_jid=3">Careers only</a><span>greenhouse</span>'

    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr(
        GreenhouseConnector,
        "_fetch_careers_html",
        _fake_careers_html,
    )
    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.asyncio.sleep",
        _noop_sleep,
    )

    connector = GreenhouseConnector()
    company = _greenhouse_company(
        platform_config={"careers_url": "https://careers.example.com/jobs"},
    )
    jobs = await connector.fetch_jobs(company)

    assert {str(j["id"]) for j in jobs} == {"1", "2", "3"}


@pytest.mark.asyncio
async def test_greenhouse_dedup_list_wins(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            assert self._payload is not None
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, str] | None = None):  # noqa: ARG002
            if url.endswith("/jobs/1"):
                return _FakeResponse({**LIST_JOB_1, "title": "From Detail"})
            return _FakeResponse({"jobs": [LIST_JOB_1]})

    async def _fake_careers_html(_self, _url: str) -> str:
        return '<a href="?gh_jid=1">Dup</a><script>greenhouse</script>'

    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr(
        GreenhouseConnector,
        "_fetch_careers_html",
        _fake_careers_html,
    )
    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.asyncio.sleep",
        _noop_sleep,
    )

    connector = GreenhouseConnector()
    company = _greenhouse_company(
        platform_config={"careers_url": "https://careers.example.com/jobs"},
    )
    jobs = await connector.fetch_jobs(company)

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Listed Role"


@pytest.mark.asyncio
async def test_greenhouse_detail_404_skipped(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise ConnectorFetchError(f"HTTP {self.status_code}")

        def json(self) -> dict[str, object]:
            assert self._payload is not None
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, str] | None = None):  # noqa: ARG002
            if "/jobs/" in url and not url.endswith("/jobs"):
                return _FakeResponse(None, status_code=404)
            return _FakeResponse({"jobs": [LIST_JOB_1]})

    async def _fake_careers_html(_self, _url: str) -> str:
        return '<a href="?gh_jid=9999">Missing</a><span>greenhouse</span>'

    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr(
        GreenhouseConnector,
        "_fetch_careers_html",
        _fake_careers_html,
    )
    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.asyncio.sleep",
        _noop_sleep,
    )

    connector = GreenhouseConnector()
    company = _greenhouse_company(
        platform_config={"careers_url": "https://careers.example.com/jobs"},
    )
    jobs = await connector.fetch_jobs(company)

    assert len(jobs) == 1
    assert jobs[0]["id"] == 1


@pytest.mark.asyncio
async def test_greenhouse_domain_mismatch_rejected(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            assert self._payload is not None
            return self._payload

    wrong_domain_job = {
        **DETAIL_JOB_3,
        "id": 55,
        "absolute_url": "https://totally-other.com/jobs/55",
    }

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, str] | None = None):  # noqa: ARG002
            if url.endswith("/jobs/55"):
                return _FakeResponse(wrong_domain_job)
            return _FakeResponse({"jobs": []})

    async def _fake_careers_html(_self, _url: str) -> str:
        return '<a href="?gh_jid=55">Bad domain</a><span>greenhouse</span>'

    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr(
        GreenhouseConnector,
        "_fetch_careers_html",
        _fake_careers_html,
    )
    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.asyncio.sleep",
        _noop_sleep,
    )

    connector = GreenhouseConnector()
    company = _greenhouse_company(
        platform_config={"careers_url": "https://careers.example.com/jobs"},
    )
    jobs = await connector.fetch_jobs(company)

    assert jobs == []


@pytest.mark.asyncio
async def test_greenhouse_list_malformed_raises(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"not_jobs": []}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, str] | None = None):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.httpx.AsyncClient",
        _FakeClient,
    )

    connector = GreenhouseConnector()
    with pytest.raises(ParseError):
        await connector.fetch_jobs(_greenhouse_company())


@pytest.mark.asyncio
async def test_greenhouse_board_token_override_in_detail_url(monkeypatch) -> None:
    detail_urls: list[str] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            assert self._payload is not None
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, str] | None = None):  # noqa: ARG002
            if "/jobs/" in url and not url.endswith("/jobs"):
                detail_urls.append(url)
                return _FakeResponse(DETAIL_JOB_3)
            return _FakeResponse({"jobs": []})

    async def _fake_careers_html(_self, _url: str) -> str:
        return CAREERS_HTML

    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr(
        GreenhouseConnector,
        "_fetch_careers_html",
        _fake_careers_html,
    )
    monkeypatch.setattr(
        "app.ingestion.connectors.greenhouse.asyncio.sleep",
        _noop_sleep,
    )

    connector = GreenhouseConnector()
    company = _greenhouse_company(
        board_token="c3ai",
        platform_config={
            "careers_url": "https://careers.example.com/jobs",
            "board_token_override": "c3iot",
        },
    )
    await connector.fetch_jobs(company)

    assert any("/boards/c3iot/jobs/" in url for url in detail_urls)
