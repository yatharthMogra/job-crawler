from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class LLMResult(Generic[T]):
    output: T
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0


class LLMProvider(ABC):
    @abstractmethod
    async def complete(
        self, system_prompt: str, user_prompt: str, response_model: type[T]
    ) -> LLMResult[T]:
        raise NotImplementedError

    async def generate_text(self, system_prompt: str, user_prompt: str) -> LLMResult[str]:
        raise NotImplementedError

    async def count_tokens(self, contents: str) -> int:
        return 0
