from __future__ import annotations

from logistics_container_agents.llm.anthropic_provider import AnthropicProvider
from logistics_container_agents.llm.base import LLMProvider
from logistics_container_agents.llm.config import load_llm_settings
from logistics_container_agents.llm.local_provider import LocalProvider
from logistics_container_agents.llm.openai_provider import OpenAIProvider


def create_llm_provider() -> LLMProvider:
    settings = load_llm_settings()
    if settings.provider == "openai":
        return OpenAIProvider(settings)
    if settings.provider == "anthropic":
        return AnthropicProvider(settings)
    return LocalProvider(settings)
