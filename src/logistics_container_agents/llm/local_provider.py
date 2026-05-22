from __future__ import annotations

from logistics_container_agents.llm.config import LLMSettings
from logistics_container_agents.llm.openai_provider import OpenAIProvider


class LocalProvider(OpenAIProvider):
    """OpenAI-compatible chat completions against a local server."""

    def __init__(self, settings: LLMSettings) -> None:
        local_settings = LLMSettings(
            provider="openai",
            openai_api_key=settings.local_api_key or "local",
            openai_model=settings.local_model,
            openai_base_url=settings.local_base_url,
            anthropic_api_key=None,
            anthropic_model=settings.anthropic_model,
            local_base_url=settings.local_base_url,
            local_model=settings.local_model,
            local_api_key=settings.local_api_key,
        )
        super().__init__(local_settings)
