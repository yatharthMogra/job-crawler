from __future__ import annotations

from app.config import Settings
from app.exceptions import ExtractionError
from app.llm.base import LLMProvider
from app.utils.text_utils import is_garbage_text


def extract_text_pymupdf(pdf_bytes: bytes) -> str:
    try:
        import fitz
    except ImportError as exc:
        raise ExtractionError("PyMuPDF is not installed.") from exc

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    parts: list[str] = []
    for page in doc:
        parts.append(page.get_text())
    doc.close()
    return "\n".join(parts).strip()


async def extract_text(
    pdf_bytes: bytes,
    *,
    settings: Settings,
    llm_provider: LLMProvider,
) -> tuple[str, str, str]:
    """
    Returns (extracted_text, method_used, extraction_status).
    method_used: pymupdf | multimodal
    extraction_status: success | fallback_used | failed
    """
    text = extract_text_pymupdf(pdf_bytes)
    threshold = settings.pymupdf_min_char_threshold

    if len(text.strip()) >= threshold and not is_garbage_text(text):
        return text, "pymupdf", "success"

    try:
        fallback_text = await llm_provider.extract_text_from_pdf(pdf_bytes)
    except Exception as exc:
        raise ExtractionError(f"PDF extraction failed: {exc}") from exc

    if len(fallback_text.strip()) < threshold:
        return fallback_text, "multimodal", "failed"

    return fallback_text, "multimodal", "fallback_used"
