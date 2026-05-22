from __future__ import annotations

import json
from typing import TypeVar

import httpx
from pydantic import BaseModel

from logistics_container_agents.llm.config import LLMSettings

T = TypeVar("T", bound=BaseModel)


class AnthropicProvider:
    def __init__(self, settings: LLMSettings) -> None:
        self._api_key = settings.anthropic_api_key or ""
        self._model = settings.anthropic_model

    async def complete_structured(
        self,
        *,
        system: str,
        user: str,
        schema: type[T],
    ) -> T:
        schema_json = json.dumps(schema.model_json_schema())
        payload = {
            "model": self._model,
            "max_tokens": 4096,
            "system": (
                f"{system}\n\nRespond with JSON only matching this schema:\n{schema_json}"
            ),
            "messages": [{"role": "user", "content": user}],
            "temperature": 0.2,
        }
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
        text_blocks = [
            b["text"] for b in data["content"] if b.get("type") == "text"
        ]
        content = "".join(text_blocks).strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[-1]
            if content.endswith("```"):
                content = content.rsplit("```", 1)[0]
        parsed = json.loads(content)
        return schema.model_validate(parsed)
