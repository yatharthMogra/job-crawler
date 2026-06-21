from __future__ import annotations

from typing import Optional

import httpx
from bs4 import BeautifulSoup

from app.ingestion.company_enrichment.resolver import about_page_candidates

USER_AGENT = "JobCrawlerCompanyEnrichment/1.0"
REQUEST_TIMEOUT = 15.0
MAX_CHARS = 12_000


async def fetch_company_about_text(website: str) -> Optional[str]:
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, headers=headers, follow_redirects=True) as client:
        for url in about_page_candidates(website):
            try:
                response = await client.get(url)
            except httpx.HTTPError:
                continue
            if response.status_code >= 400:
                continue
            text = _html_to_text(response.text)
            if len(text) >= 200:
                return text[:MAX_CHARS]
    return None


def _html_to_text(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())
