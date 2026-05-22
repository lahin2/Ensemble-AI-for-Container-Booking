# Configuration

## Required

Set `LLM_PROVIDER` to one of: `openai`, `anthropic`, `local`.

Copy `.env.example` to `.env` in the project root (or export variables in your shell).

## OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

For an OpenAI-compatible local server, also set:

```env
OPENAI_BASE_URL=http://localhost:11434/v1
```

## Anthropic

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-haiku-latest
```

## Local (Ollama, LM Studio, vLLM)

```env
LLM_PROVIDER=local
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.2
LLM_API_KEY=          # optional; Ollama often needs no key
```

Ensure the server exposes **chat completions** compatible with the OpenAI API (`/v1/chat/completions`).

## Verify setup

```bash
pip install -e .
python -m logistics_container_agents.cli agents list
python -m logistics_container_agents.cli book --request scenarios/sample_shanghai_la.json
```

If configuration is missing, the CLI exits with an actionable error message.
