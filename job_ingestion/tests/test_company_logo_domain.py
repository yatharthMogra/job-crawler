from __future__ import annotations

from app.ingestion.company_logos.domain import (
    domain_from_website,
    guess_company_domain,
    resolve_logo_domain,
)
from app.models.company import Company


def _company(**kwargs) -> Company:
    defaults = {
        "name": "Anthropic",
        "platform": "greenhouse",
        "board_token": "anthropic",
        "is_active": True,
    }
    defaults.update(kwargs)
    return Company(**defaults)


def test_domain_from_website_strips_www() -> None:
    assert domain_from_website("https://www.anthropic.com/about") == "anthropic.com"


def test_resolve_logo_domain_uses_known_alias() -> None:
    company = _company(name="Boeing", board_token="boeing")
    assert resolve_logo_domain(company) == "boeing.com"


def test_resolve_logo_domain_uses_platform_config_website() -> None:
    company = _company(
        name="Acme Corp",
        board_token="acme",
        platform_config={"company_website": "https://www.acme.example"},
    )
    assert resolve_logo_domain(company) == "acme.example"


def test_resolve_logo_domain_uses_enrichment_website() -> None:
    company = _company(name="Obscure Co", board_token="obscure-co")
    assert resolve_logo_domain(company, enrichment_website="https://obscure.io") == "obscure.io"


def test_guess_company_domain_strips_legal_suffix() -> None:
    assert guess_company_domain("Greenheck Group LLC") == "greenheck.com"
