from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.models.company import Company


class BaseConnector(ABC):
    @abstractmethod
    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        raise NotImplementedError
