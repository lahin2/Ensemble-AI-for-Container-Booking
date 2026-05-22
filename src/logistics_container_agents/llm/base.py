from __future__ import annotations

from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMProvider(Protocol):
    async def complete_structured(
        self,
        *,
        system: str,
        user: str,
        schema: type[T],
    ) -> T: ...
