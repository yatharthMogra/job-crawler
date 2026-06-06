import sys
import types as stdtypes

import pytest
from pydantic import BaseModel

from app.config import Settings
from app.exceptions import LLMProviderError
from app.llm.gemini import GeminiProvider


class _ResponseModel(BaseModel):
    ok: bool


def _install_fake_genai(monkeypatch, *, models: object, captured: dict[str, str] | None = None) -> None:
    class _FakeClient:
        def __init__(self, api_key: str) -> None:
            if captured is not None:
                captured["api_key"] = api_key
            self.aio = stdtypes.SimpleNamespace(models=models)

    genai_types_module = stdtypes.ModuleType("google.genai.types")

    class GenerateContentConfig:
        def __init__(self, **kwargs: object) -> None:
            pass

    genai_types_module.GenerateContentConfig = GenerateContentConfig

    google_module = stdtypes.ModuleType("google")
    genai_module = stdtypes.ModuleType("google.genai")
    genai_module.Client = _FakeClient
    genai_module.types = genai_types_module
    google_module.genai = genai_module

    monkeypatch.setitem(sys.modules, "google", google_module)
    monkeypatch.setitem(sys.modules, "google.genai", genai_module)
    monkeypatch.setitem(sys.modules, "google.genai.types", genai_types_module)


@pytest.mark.asyncio
async def test_gemini_provider_parses_json_response(monkeypatch) -> None:
    captured: dict[str, str] = {}

    class _FakeResponse:
        text = '{"ok": true}'

    class _FakeModels:
        async def generate_content(self, *, model: str, contents: str, config=None):  # noqa: ANN003
            captured["model"] = model
            captured["contents"] = contents
            return _FakeResponse()

    _install_fake_genai(monkeypatch, models=_FakeModels(), captured=captured)

    settings = Settings(gemini_api_key="test-key", gemini_model="gemini-test-model")
    provider = GeminiProvider(settings)
    result = await provider.complete("system", "user", _ResponseModel)

    assert result.output.ok is True
    assert result.input_tokens == 0
    assert result.output_tokens == 0
    assert captured["api_key"] == "test-key"
    assert captured["model"] == "gemini-test-model"
    assert "Return JSON only." in captured["contents"]


@pytest.mark.asyncio
async def test_gemini_provider_wraps_client_errors(monkeypatch) -> None:
    class _FakeModels:
        async def generate_content(self, *, model: str, contents: str, config=None):  # noqa: ANN003
            raise RuntimeError("network issue")

    _install_fake_genai(monkeypatch, models=_FakeModels())

    settings = Settings(gemini_api_key="test-key", gemini_model="gemini-test-model")
    provider = GeminiProvider(settings)

    with pytest.raises(LLMProviderError, match="Gemini completion failed"):
        await provider.complete("system", "user", _ResponseModel)


@pytest.mark.asyncio
async def test_gemini_provider_parses_fenced_json_response(monkeypatch) -> None:
    class _FakeResponse:
        text = '```json\n{"ok": true}\n```'

    class _FakeModels:
        async def generate_content(self, *, model: str, contents: str, config=None):  # noqa: ANN003
            return _FakeResponse()

    _install_fake_genai(monkeypatch, models=_FakeModels())

    settings = Settings(gemini_api_key="test-key", gemini_model="gemini-test-model")
    provider = GeminiProvider(settings)
    result = await provider.complete("system", "user", _ResponseModel)

    assert result.output.ok is True


@pytest.mark.asyncio
async def test_gemini_provider_pdf_fallback_not_supported() -> None:
    settings = Settings(gemini_api_key="test-key", gemini_model="gemini-3.1-flash-lite")
    provider = GeminiProvider(settings)

    with pytest.raises(LLMProviderError, match="PDF multimodal fallback is not supported"):
        await provider.extract_text_from_pdf(b"%PDF-1.4")
