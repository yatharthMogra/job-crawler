from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse

from app.models.company import Company

_ATS_HOSTS = frozenset(
    {
        "jobs.lever.co",
        "boards.greenhouse.io",
        "jobs.ashbyhq.com",
        "apply.workable.com",
        "careers.smartrecruiters.com",
        "jobs.jobvite.com",
    }
)


def resolve_company_website(company: Company, posting_url: str | None = None) -> str | None:
    config = company.platform_config or {}
    configured = config.get("company_website")
    if isinstance(configured, str) and configured.strip():
        return _normalize_url(configured.strip())

    for candidate in (posting_url, config.get("careers_url"), config.get("website")):
        if not isinstance(candidate, str) or not candidate.strip():
            continue
        normalized = _normalize_url(candidate.strip())
        if normalized and not _is_ats_host(normalized):
            return normalized

    if isinstance(posting_url, str) and posting_url.strip():
        parsed = urlparse(posting_url.strip())
        if parsed.scheme and parsed.netloc and not _is_ats_host(posting_url):
            return f"{parsed.scheme}://{parsed.netloc}"

    token = company.board_token.strip()
    if token and "." in token and not token.startswith("http"):
        return _normalize_url(token)
    return None


def about_page_candidates(website: str) -> list[str]:
    base = website.rstrip("/")
    return [
        f"{base}/about",
        f"{base}/about-us",
        f"{base}/company",
        f"{base}/careers",
        base,
    ]


def _normalize_url(value: str) -> str | None:
    trimmed = value.strip()
    if not trimmed:
        return None
    if not trimmed.startswith(("http://", "https://")):
        trimmed = f"https://{trimmed}"
    parsed = urlparse(trimmed)
    if not parsed.scheme or not parsed.netloc:
        return None
    return f"{parsed.scheme}://{parsed.netloc}"


def _is_ats_host(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(host == ats or host.endswith(f".{ats}") for ats in _ATS_HOSTS)
