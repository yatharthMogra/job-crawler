from __future__ import annotations

import json

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.workatastartup import WorkAtAStartupConnector
from app.models.company import Company


def _inertia_html(props: dict) -> str:
    payload = json.dumps({"component": "TestPage", "props": props, "url": "/", "version": "1"})
    return f'<div id="app" data-page="{payload.replace(chr(34), "&quot;")}"></div>'


@pytest.mark.asyncio
async def test_workatastartup_connector_parses_company_jobs(monkeypatch) -> None:
    company_html = _inertia_html(
        {
            "rawCompany": {
                "name": "Firecrawl",
                "slug": "firecrawl",
                "batch": "S22",
                "team_size": 12,
                "one_liner": "Web data API",
                "jobs": [
                    {
                        "id": 123,
                        "title": "Backend Engineer",
                        "description": "<p>Build crawlers</p>",
                        "job_type": "fulltime",
                        "eng_type": ["be"],
                        "visa": "yes",
                        "remote": "no",
                        "pretty_location_or_remote": "San Francisco, CA",
                    }
                ],
            }
        }
    )

    class _FakeResponse:
        def __init__(self, *, status_code: int = 200, text: str = "", payload=None):
            self.status_code = status_code
            self.text = text
            self._payload = payload

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise RuntimeError(f"HTTP {self.status_code}")

        def json(self):
            return self._payload

    class _FakeClient:
        async def get(self, url: str, **kwargs):  # noqa: ARG002
            if "account.ycombinator.com/?continue" in url:
                return _FakeResponse(
                    text='<meta name="csrf-token" content="csrf123"/>',
                )
            if url.endswith("/sign_in"):
                return _FakeResponse(payload={"redirectTo": "https://sso-auth.workatastartup.com/set_auth?key=abc"})
            if "set_auth" in url:
                return _FakeResponse(text="ok")
            if "/companies/firecrawl" in url:
                return _FakeResponse(text=company_html)
            if "/jobs?role=eng" in url:
                return _FakeResponse(text=_inertia_html({"jobs": []}))
            if "/jobs?role=ds" in url:
                return _FakeResponse(text=_inertia_html({"jobs": []}))
            raise RuntimeError(f"unexpected url {url}")

        async def post(self, url: str, **kwargs):  # noqa: ARG002
            if url.endswith("/sign_in"):
                return _FakeResponse(payload={"redirectTo": "https://sso-auth.workatastartup.com/set_auth?key=abc"})
            raise RuntimeError(f"unexpected post url {url}")

    class _FakeSession:
        def __init__(self, **kwargs):  # noqa: ARG002
            self._client = _FakeClient()

        async def __aenter__(self):
            return self._client

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

    monkeypatch.setattr("app.ingestion.connectors.workatastartup.AsyncSession", _FakeSession)
    monkeypatch.setattr("app.ingestion.connectors.workatastartup.asyncio.sleep", _noop_sleep)

    class _Settings:
        yc_crawler_email = "crawler@example.com"
        yc_crawler_password = "secret"
        yc_waas_roles_list = ["eng"]

    connector = WorkAtAStartupConnector(_Settings())
    company = Company(
        name="Work at a Startup (YC)",
        platform="workatastartup",
        board_token="yc-global",
        is_active=True,
        platform_config={"company_slugs": ["firecrawl"]},
    )
    jobs = await connector.fetch_jobs(company)

    assert len(jobs) == 1
    assert jobs[0]["id"] == "yc_123"
    assert jobs[0]["company"]["name"] == "Firecrawl"
    assert jobs[0]["description"] == "<p>Build crawlers</p>"
    assert jobs[0]["visa_sponsorship"] is True


async def _noop_sleep(*_args, **_kwargs):
    return None


@pytest.mark.asyncio
async def test_workatastartup_connector_missing_credentials() -> None:
    class _Settings:
        yc_crawler_email = ""
        yc_crawler_password = ""
        yc_waas_roles_list = ["eng"]

    connector = WorkAtAStartupConnector(_Settings())
    company = Company(name="WaaS", platform="workatastartup", board_token="yc-global", is_active=True)
    with pytest.raises(ConnectorFetchError, match="credentials missing"):
        await connector.fetch_jobs(company)


@pytest.mark.asyncio
async def test_workatastartup_connector_parse_error_on_missing_csrf(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200
        text = "<html></html>"

    class _FakeClient:
        async def get(self, url: str, **kwargs):  # noqa: ARG002
            return _FakeResponse()

    class _FakeSession:
        def __init__(self, **kwargs):  # noqa: ARG002
            self._client = _FakeClient()

        async def __aenter__(self):
            return self._client

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

    monkeypatch.setattr("app.ingestion.connectors.workatastartup.AsyncSession", _FakeSession)

    class _Settings:
        yc_crawler_email = "crawler@example.com"
        yc_crawler_password = "secret"
        yc_waas_roles_list = ["eng"]

    connector = WorkAtAStartupConnector(_Settings())
    company = Company(name="WaaS", platform="workatastartup", board_token="yc-global", is_active=True)
    with pytest.raises(ParseError, match="CSRF"):
        await connector.fetch_jobs(company)
