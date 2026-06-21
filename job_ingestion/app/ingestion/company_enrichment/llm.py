from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, field_validator

COMPANY_ENRICHMENT_SYSTEM_PROMPT = (
    "You extract factual company profile attributes from about-page text. "
    "Use only information explicitly stated in the text. "
    "Return null for any field not clearly supported by the source.\n\n"
    "Field rules:\n"
    "- founded_year: four-digit year only when explicitly stated\n"
    "- headquarters: city and state/country when available\n"
    "- employee_count_range: use ranges like '51-200' or '1001-5000' when stated\n"
    "- one_line_description: one concise sentence describing what the company does\n"
    "- website: canonical company homepage URL if present in text or input context\n"
    "- linkedin_url: full LinkedIn company URL if present\n"
    "- glassdoor_rating: numeric rating only if explicitly stated; otherwise null"
)


class CompanyEnrichmentResult(BaseModel):
    founded_year: Optional[int] = None
    headquarters: Optional[str] = None
    employee_count_range: Optional[str] = None
    one_line_description: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    glassdoor_rating: Optional[float] = None

    @field_validator("founded_year", mode="before")
    @classmethod
    def _coerce_founded_year(cls, value: object) -> int | None:
        if value is None:
            return None
        if isinstance(value, bool):
            return None
        if isinstance(value, int):
            return value if 1800 <= value <= 2100 else None
        if isinstance(value, float):
            year = int(value)
            return year if 1800 <= year <= 2100 else None
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.isdigit():
                year = int(stripped)
                return year if 1800 <= year <= 2100 else None
        return None

    @field_validator("glassdoor_rating", mode="before")
    @classmethod
    def _coerce_glassdoor_rating(cls, value: object) -> float | None:
        if value is None:
            return None
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            rating = float(value)
            return rating if 0 < rating <= 5 else None
        if isinstance(value, str):
            try:
                rating = float(value.strip())
                return rating if 0 < rating <= 5 else None
            except ValueError:
                return None
        return None

    @field_validator(
        "headquarters",
        "employee_count_range",
        "one_line_description",
        "website",
        "linkedin_url",
        mode="before",
    )
    @classmethod
    def _coerce_optional_str(cls, value: object) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None


DEFAULT_COMPANY_ENRICHMENT = CompanyEnrichmentResult()
