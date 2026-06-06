from app.config import Settings
from app.exceptions import LLMProviderError
from app.llm.base import LLMProvider
from app.llm.gemini import GeminiProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    provider = settings.llm_provider.lower().strip()
    if provider == "gemini":
        return GeminiProvider(settings)
    raise LLMProviderError(f"Unsupported LLM provider: {settings.llm_provider}")
