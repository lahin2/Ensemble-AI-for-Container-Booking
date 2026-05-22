from __future__ import annotations

import json
from typing import TypeVar

import httpx
from pydantic import BaseModel

from logistics_container_agents.llm.config import LLMSettings

T = TypeVar("T", bound=BaseModel)


class OpenAIProvider:
    def __init__(self, settings: LLMSettings) -> None:
        self._api_key = settings.openai_api_key or ""
        self._model = settings.openai_model
        base = settings.openai_base_url or "https://api.openai.com/v1"
        self._base_url = base.rstrip("/")

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
            "messages": [
                {
                    "role": "system",
                    "content": (
                        f"{system}\n\nRespond with JSON only matching this schema:\n"
                        f"{schema_json}"
                    ),
                },
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{self._base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return schema.model_validate(parsed)
