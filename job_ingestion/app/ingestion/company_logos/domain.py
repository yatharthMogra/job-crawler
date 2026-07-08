from __future__ import annotations

import re
from typing import Optional
from urllib.parse import urlparse

from app.ingestion.company_enrichment.resolver import resolve_company_website
from app.models.company import Company

LEGAL_SUFFIXES = re.compile(
    r"\b(inc|incorporated|llc|l\.l\.c|ltd|limited|corp|corporation|co|company|plc|gmbh|ag|sa|nv|bv|"
    r"technologies|technology|tech|software|systems|group|holdings|holding|partners|ventures|labs|lab|ai|pbc|pc)\b\.?",
    re.IGNORECASE,
)

COMPANY_DOMAINS: dict[str, str] = {
    "scaleai": "scale.com",
    "scale ai": "scale.com",
    "scale": "scale.com",
    "ramp": "ramp.com",
    "vercel": "vercel.com",
    "stripe": "stripe.com",
    "notion": "notion.so",
    "linear": "linear.app",
    "databricks": "databricks.com",
    "anthropic": "anthropic.com",
    "figma": "figma.com",
    "retool": "retool.com",
    "plaid": "plaid.com",
    "brex": "brex.com",
    "mercury": "mercury.com",
    "airtable": "airtable.com",
    "cohere": "cohere.com",
    "snowflake": "snowflake.com",
    "datadog": "datadoghq.com",
    "coinbase": "coinbase.com",
    "robinhood": "robinhood.com",
    "instacart": "instacart.com",
    "doordash": "doordash.com",
    "rippling": "rippling.com",
    "deel": "deel.com",
    "google": "google.com",
    "alphabet": "abc.xyz",
    "meta": "meta.com",
    "facebook": "meta.com",
    "amazon": "amazon.com",
    "aws": "aws.amazon.com",
    "apple": "apple.com",
    "microsoft": "microsoft.com",
    "netflix": "netflix.com",
    "uber": "uber.com",
    "airbnb": "airbnb.com",
    "openai": "openai.com",
    "nvidia": "nvidia.com",
    "intel": "intel.com",
    "amd": "amd.com",
    "oracle": "oracle.com",
    "salesforce": "salesforce.com",
    "adobe": "adobe.com",
    "ibm": "ibm.com",
    "cisco": "cisco.com",
    "walmart": "walmart.com",
    "bloomberg": "bloomberg.com",
    "goldman sachs": "goldmansachs.com",
    "jpmorgan chase": "jpmorganchase.com",
    "morgan stanley": "morganstanley.com",
    "citadel": "citadel.com",
    "jane street": "janestreet.com",
    "two sigma": "twosigma.com",
    "blackrock": "blackrock.com",
    "capital one": "capitalone.com",
    "linkedin": "linkedin.com",
    "twitter": "x.com",
    "x": "x.com",
    "snap": "snap.com",
    "snapchat": "snap.com",
    "tiktok": "tiktok.com",
    "bytedance": "bytedance.com",
    "shopify": "shopify.com",
    "paypal": "paypal.com",
    "tesla": "tesla.com",
    "spacex": "spacex.com",
    "anduril": "anduril.com",
    "palantir": "palantir.com",
    "cloudflare": "cloudflare.com",
    "mongodb": "mongodb.com",
    "atlassian": "atlassian.com",
    "asana": "asana.com",
    "slack": "slack.com",
    "zoom": "zoom.us",
    "dropbox": "dropbox.com",
    "reddit": "reddit.com",
    "pinterest": "pinterest.com",
    "spotify": "spotify.com",
    "lyft": "lyft.com",
    "wayfair": "wayfair.com",
    "target": "target.com",
    "nike": "nike.com",
    "disney": "disney.com",
    "comcast": "comcast.com",
    "verizon": "verizon.com",
    "at&t": "att.com",
    "att": "att.com",
    "lockheed martin": "lockheedmartin.com",
    "northrop grumman": "northropgrumman.com",
    "raytheon": "rtx.com",
    "boeing": "boeing.com",
    "general electric": "ge.com",
    "ge": "ge.com",
    "general motors": "gm.com",
    "ford": "ford.com",
    "pfizer": "pfizer.com",
    "moderna": "modernatx.com",
    "accenture": "accenture.com",
    "deloitte": "deloitte.com",
    "mckinsey": "mckinsey.com",
    "bcg": "bcg.com",
    "bain": "bain.com",
    "medtronic": "medtronic.com",
}


def _normalize_key(name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9\s]", " ", name.strip().lower().replace("&", " and "))
    return re.sub(r"\s+", " ", cleaned).strip()


def _strip_legal_suffixes(name: str) -> str:
    return re.sub(r"\s+", " ", LEGAL_SUFFIXES.sub(" ", _normalize_key(name))).strip()


def _resolve_map_entry(name: str) -> str | None:
    key = _normalize_key(name)
    if not key:
        return None
    if key in COMPANY_DOMAINS:
        return COMPANY_DOMAINS[key]

    stripped = _strip_legal_suffixes(name)
    if stripped in COMPANY_DOMAINS:
        return COMPANY_DOMAINS[stripped]

    aliases = sorted(COMPANY_DOMAINS, key=len, reverse=True)
    for alias in aliases:
        if len(alias) < 3:
            tokens = stripped.split()
            if alias in tokens or key == alias:
                return COMPANY_DOMAINS[alias]
            continue
        if key == alias or stripped == alias:
            return COMPANY_DOMAINS[alias]
        if (
            key.startswith(f"{alias} ")
            or key.endswith(f" {alias}")
            or f" {alias} " in key
            or stripped.startswith(f"{alias} ")
            or stripped.endswith(f" {alias}")
            or f" {alias} " in stripped
        ):
            return COMPANY_DOMAINS[alias]
        if " " in alias and (alias in key or alias in stripped):
            return COMPANY_DOMAINS[alias]
    return None


def domain_from_website(website: str | None) -> str | None:
    if not website or not website.strip():
        return None
    try:
        url = website if "://" in website else f"https://{website}"
        host = urlparse(url).hostname or ""
        return host.removeprefix("www.") or None
    except Exception:
        return None


def guess_company_domain(name: str) -> str:
    cleaned = _strip_legal_suffixes(name).replace(" ", "")
    return f"{cleaned}.com" if cleaned else "example.com"


def resolve_logo_domain(
    company: Company,
    *,
    enrichment_website: str | None = None,
) -> str:
    config = company.platform_config or {}

    for candidate in (
        config.get("company_website"),
        config.get("website"),
        config.get("careers_url"),
        enrichment_website,
    ):
        domain = domain_from_website(candidate if isinstance(candidate, str) else None)
        if domain:
            return domain

    domain_config = config.get("domain")
    if isinstance(domain_config, str) and domain_config.strip():
        return domain_config.strip().removeprefix("www.")

    website = resolve_company_website(company)
    domain = domain_from_website(website)
    if domain:
        return domain

    token = company.board_token.strip()
    if token and "." in token and not token.startswith("http"):
        return token.removeprefix("www.")

    mapped = _resolve_map_entry(company.name)
    if mapped:
        return mapped

    return guess_company_domain(company.name)


def logo_source_urls(domain: str) -> list[str]:
    encoded = domain
    return [
        f"https://www.google.com/s2/favicons?domain={encoded}&sz=128",
        f"https://icons.duckduckgo.com/ip3/{domain}.ico",
        f"https://unavatar.io/{encoded}?fallback=false",
        f"https://logo.clearbit.com/{domain}",
    ]
