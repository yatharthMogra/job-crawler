import fitz
import pytest

from app.utils.text_utils import is_garbage_text


def _make_text_pdf(path) -> None:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Jane Doe\nSoftware Engineer\nPython, FastAPI, PostgreSQL, AWS")
    doc.save(path)
    doc.close()


@pytest.mark.asyncio
async def test_pymupdf_extraction_success(tmp_path, monkeypatch) -> None:
    from app.config import Settings
    from app.pipeline.extractor import extract_text

    pdf_path = tmp_path / "resume.pdf"
    _make_text_pdf(pdf_path)

    class DummyLLM:
        async def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
            return "fallback"

    settings = Settings(pymupdf_min_char_threshold=10)
    text, method, status = await extract_text(str(pdf_path), settings=settings, llm_provider=DummyLLM())
    assert method == "pymupdf"
    assert status == "success"
    assert "Python" in text
    assert not is_garbage_text(text)


@pytest.mark.asyncio
async def test_multimodal_fallback_on_short_text(tmp_path) -> None:
    from app.config import Settings
    from app.pipeline.extractor import extract_text

    doc = fitz.open()
    doc.new_page()
    pdf_path = tmp_path / "empty.pdf"
    doc.save(pdf_path)
    doc.close()

    class DummyLLM:
        async def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
            return (
                "Recovered resume text with enough characters for successful extraction. "
                "Jane Doe Software Engineer Python FastAPI PostgreSQL AWS Docker Kubernetes."
            )

    settings = Settings(pymupdf_min_char_threshold=100)
    text, method, status = await extract_text(str(pdf_path), settings=settings, llm_provider=DummyLLM())
    assert method == "multimodal"
    assert status == "fallback_used"
    assert "Recovered resume" in text
