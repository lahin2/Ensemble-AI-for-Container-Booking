import os

import pytest

from logistics_container_agents.llm.config import LLMConfigError, load_llm_settings


def test_missing_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    with pytest.raises(LLMConfigError, match="LLM_PROVIDER"):
        load_llm_settings()


def test_openai_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(LLMConfigError, match="OPENAI_API_KEY"):
        load_llm_settings()


def test_local_requires_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "local")
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.setenv("LLM_MODEL", "llama3.2")
    with pytest.raises(LLMConfigError, match="LLM_BASE_URL"):
        load_llm_settings()
