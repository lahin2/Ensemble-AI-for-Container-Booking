from __future__ import annotations

import os
from dataclasses import dataclass


class LLMConfigError(Exception):
    """Raised when LLM_PROVIDER or required credentials are missing."""


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    openai_api_key: str | None
    openai_model: str
    openai_base_url: str | None
    anthropic_api_key: str | None
    anthropic_model: str
    local_base_url: str | None
    local_model: str
    local_api_key: str | None


def load_llm_settings() -> LLMSettings:
    provider = (os.getenv("LLM_PROVIDER") or "").strip().lower()
    if not provider:
        raise LLMConfigError(
            "LLM_PROVIDER is not set. Copy .env.example to .env and set "
            "LLM_PROVIDER to one of: openai, anthropic, local. "
            "See docs/configuration.md."
        )
    if provider not in {"openai", "anthropic", "local"}:
        raise LLMConfigError(
            f"Unknown LLM_PROVIDER={provider!r}. "
            "Use: openai, anthropic, or local."
        )

    settings = LLMSettings(
        provider=provider,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_base_url=os.getenv("OPENAI_BASE_URL"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest"),
        local_base_url=os.getenv("LLM_BASE_URL"),
        local_model=os.getenv("LLM_MODEL", ""),
        local_api_key=os.getenv("LLM_API_KEY"),
    )
    _validate_provider(settings)
    return settings


def _validate_provider(settings: LLMSettings) -> None:
    if settings.provider == "openai":
        if not settings.openai_api_key:
            raise LLMConfigError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai. "
                "See docs/configuration.md."
            )
    elif settings.provider == "anthropic":
        if not settings.anthropic_api_key:
            raise LLMConfigError(
                "ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic. "
                "See docs/configuration.md."
            )
    elif settings.provider == "local":
        if not settings.local_base_url:
            raise LLMConfigError(
                "LLM_BASE_URL is required when LLM_PROVIDER=local "
                "(e.g. http://localhost:11434/v1). See docs/configuration.md."
            )
        if not settings.local_model:
            raise LLMConfigError(
                "LLM_MODEL is required when LLM_PROVIDER=local. "
                "See docs/configuration.md."
            )
