import re
import time
from typing import TypeVar

from pydantic import BaseModel

from app.config import Settings
from app.exceptions import LLMProviderError
from app.llm.base import LLMProvider, LLMResult

T = TypeVar("T", bound=BaseModel)


class GeminiProvider(LLMProvider):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def complete(
        self, system_prompt: str, user_prompt: str, response_model: type[T]
    ) -> LLMResult[T]:
        if not self._settings.gemini_api_key:
            raise LLMProviderError("GEMINI_API_KEY is not configured.")

        try:
            from google import genai
        except ImportError as exc:
            raise LLMProviderError("google-genai is not installed.") from exc

        client = genai.Client(api_key=self._settings.gemini_api_key)
        prompt = f"{system_prompt}\n\n{user_prompt}\n\nReturn JSON only."
        started = time.monotonic()
        try:
            from google.genai import types

            response = await client.aio.models.generate_content(
                model=self._settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_model,
                ),
            )
            text = self._response_text(response) or "{}"
            parsed = self._parse_response_json(response_model=response_model, text=text)
            usage = getattr(response, "usage_metadata", None)
            input_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
            output_tokens = int(getattr(usage, "candidates_token_count", 0) or 0)
            return LLMResult(
                output=parsed,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=int((time.monotonic() - started) * 1000),
            )
        except Exception as exc:  # pragma: no cover - external API behavior
            raise LLMProviderError(f"Gemini completion failed: {exc}") from exc

    async def extract_text_from_pdf(self, _pdf_bytes: bytes) -> str:
        raise LLMProviderError(
            "PDF multimodal fallback is not supported with Gemini. "
            "PyMuPDF extraction failed; try a text-based PDF."
        )

    async def count_tokens(self, contents: str) -> int:
        if not self._settings.gemini_api_key:
            return 0
        try:
            from google import genai
        except ImportError:
            return 0

        try:
            client = genai.Client(api_key=self._settings.gemini_api_key)
            response = await client.aio.models.count_tokens(
                model=self._settings.gemini_model,
                contents=contents,
            )
            return int(getattr(response, "total_tokens", 0) or 0)
        except Exception:
            return 0

    @staticmethod
    def _response_text(response: object) -> str:
        text = getattr(response, "text", None)
        if isinstance(text, str):
            return text

        candidates = getattr(response, "candidates", None)
        if not isinstance(candidates, list):
            return ""
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None)
            if not isinstance(parts, list):
                continue
            for part in parts:
                part_text = getattr(part, "text", None)
                if isinstance(part_text, str):
                    return part_text
        return ""

    @classmethod
    def _parse_response_json(cls, response_model: type[T], text: str) -> T:
        candidates: list[str] = [text]
        sanitized = cls._strip_json_fences(text)
        if sanitized and sanitized != text:
            candidates.append(sanitized)
        last_error: Exception | None = None
        for candidate in candidates:
            try:
                return response_model.model_validate_json(candidate)
            except Exception as exc:  # pragma: no cover - guarded by follow-up candidate
                last_error = exc
        if last_error is None:
            return response_model.model_validate_json(text)
        raise last_error

    @staticmethod
    def _strip_json_fences(text: str) -> str:
        value = text.strip()
        if not value:
            return value
        fenced_match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", value, flags=re.IGNORECASE | re.DOTALL)
        if fenced_match:
            return fenced_match.group(1).strip()
        inline_match = re.search(r"```(?:json)?\s*(.*?)\s*```", value, flags=re.IGNORECASE | re.DOTALL)
        if inline_match:
            return inline_match.group(1).strip()
        return value
