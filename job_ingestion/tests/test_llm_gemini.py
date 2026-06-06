import sys
import types

import pytest
from pydantic import BaseModel

from app.config import Settings
from app.exceptions import LLMProviderError
from app.llm.gemini import GeminiProvider


class _ResponseModel(BaseModel):
    ok: bool


@pytest.mark.asyncio
async def test_gemini_provider_parses_json_response(monkeypatch) -> None:
    captured: dict[str, str] = {}

    class _FakeResponse:
        text = '{"ok": true}'

    class _FakeModels:
        async def generate_content(self, *, model: str, contents: str):  # noqa: ANN003
            captured["model"] = model
            captured["contents"] = contents
            return _FakeResponse()

    class _FakeClient:
        def __init__(self, api_key: str) -> None:
            captured["api_key"] = api_key
            self.aio = types.SimpleNamespace(models=_FakeModels())

    google_module = types.ModuleType("google")
    genai_module = types.ModuleType("google.genai")
    genai_module.Client = _FakeClient
    google_module.genai = genai_module

    monkeypatch.setitem(sys.modules, "google", google_module)
    monkeypatch.setitem(sys.modules, "google.genai", genai_module)

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
        async def generate_content(self, *, model: str, contents: str):  # noqa: ANN003
            raise RuntimeError("network issue")

    class _FakeClient:
        def __init__(self, api_key: str) -> None:
            self.aio = types.SimpleNamespace(models=_FakeModels())

    google_module = types.ModuleType("google")
    genai_module = types.ModuleType("google.genai")
    genai_module.Client = _FakeClient
    google_module.genai = genai_module

    monkeypatch.setitem(sys.modules, "google", google_module)
    monkeypatch.setitem(sys.modules, "google.genai", genai_module)

    settings = Settings(gemini_api_key="test-key", gemini_model="gemini-test-model")
    provider = GeminiProvider(settings)

    with pytest.raises(LLMProviderError, match="Gemini completion failed"):
        await provider.complete("system", "user", _ResponseModel)


@pytest.mark.asyncio
async def test_gemini_provider_parses_fenced_json_response(monkeypatch) -> None:
    class _FakeResponse:
        text = '```json\n{"ok": true}\n```'

    class _FakeModels:
        async def generate_content(self, *, model: str, contents: str):  # noqa: ANN003
            return _FakeResponse()

    class _FakeClient:
        def __init__(self, api_key: str) -> None:
            self.aio = types.SimpleNamespace(models=_FakeModels())

    google_module = types.ModuleType("google")
    genai_module = types.ModuleType("google.genai")
    genai_module.Client = _FakeClient
    google_module.genai = genai_module

    monkeypatch.setitem(sys.modules, "google", google_module)
    monkeypatch.setitem(sys.modules, "google.genai", genai_module)

    settings = Settings(gemini_api_key="test-key", gemini_model="gemini-test-model")
    provider = GeminiProvider(settings)
    result = await provider.complete("system", "user", _ResponseModel)

    assert result.output.ok is True
