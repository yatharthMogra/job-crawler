from __future__ import annotations

from html import unescape
from typing import Optional

from bs4 import BeautifulSoup


def clean_job_description(raw_html: Optional[str]) -> str:
    if not raw_html:
        return ""
    normalized = raw_html
    for _ in range(3):
        decoded = unescape(normalized)
        if decoded == normalized:
            break
        normalized = decoded
    soup = BeautifulSoup(normalized, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())


def build_description_preview(text: Optional[str], max_chars: int = 400) -> Optional[str]:
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return None
    if len(cleaned) <= max_chars:
        return cleaned
    preview = cleaned[:max_chars].rstrip()
    split_idx = preview.rfind(" ")
    if split_idx >= max_chars // 2:
        preview = preview[:split_idx].rstrip()
    return f"{preview}..."
