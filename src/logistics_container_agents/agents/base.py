from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from logistics_container_agents.llm.base import LLMProvider

_DOCS = Path(__file__).resolve().parents[3] / "docs" / "agents.md"
_AGENT_GUIDE = _DOCS.read_text(encoding="utf-8") if _DOCS.exists() else ""


class BaseAgent:
    role: str = "agent"
    output_schema: type[BaseModel]

    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    def _system_prompt(self) -> str:
        return (
            f"You are the {self.role} in a maritime FCL container booking ensemble.\n"
            f"{_AGENT_GUIDE}\n"
            "Return only valid JSON for the requested schema. No markdown."
        )

    async def run(self, user_prompt: str) -> BaseModel:
        return await self._llm.complete_structured(
            system=self._system_prompt(),
            user=user_prompt,
            schema=self.output_schema,
        )
