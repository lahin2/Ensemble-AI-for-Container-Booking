# Logistics Container Agents

Open-source **ensemble of AI agents** for maritime **FCL container booking** — a Flexport-style workflow where specialized agents handle intake, routing, quoting, carrier selection, compliance, documentation, and confirmation.

**You bring your own AI.** Configure a cloud API (OpenAI, Anthropic) or a local OpenAI-compatible server (Ollama, LM Studio, vLLM). There is no bundled demo runtime and no mock provider in the CLI.

## Agent fleet

| Agent | Output |
|-------|--------|
| ShipperIntakeAgent | `BookingRequest` |
| RoutePlanningAgent | `RoutePlan` |
| RateQuotingAgent | `RateQuote` |
| CarrierSelectionAgent | `CarrierOffer` |
| ComplianceAgent | `ComplianceResult` |
| DocumentationAgent | `BookingDocuments` |
| BookingOrchestrator | `ConfirmedBooking` |

See [docs/agents.md](docs/agents.md) and [docs/architecture.md](docs/architecture.md).

## Prerequisites

1. Python 3.11+
2. `LLM_PROVIDER` and matching credentials — see [docs/configuration.md](docs/configuration.md)

## Setup

```bash
cd LogisticsContainerAgents
cp .env.example .env
# Edit .env: set LLM_PROVIDER and API keys or LLM_BASE_URL

pip install -e .
```

## Run a booking

Prepare a `BookingRequest` JSON file (see [scenarios/sample_shanghai_la.json](scenarios/sample_shanghai_la.json) as a template only).

```bash
python -m logistics_container_agents.cli book --request scenarios/sample_shanghai_la.json
```

List agents:

```bash
python -m logistics_container_agents.cli agents list
```

## TypeScript CLI

```bash
cd typescript/cli
npm install
npm run book -- --request ../../scenarios/sample_shanghai_la.json
```

Requires the same `.env` in the project root and Python on `PATH`.

## Development

```bash
pip install -e ".[dev]"
pytest
```

Tests use a **dev-only** mock LLM under `tests/support/` (not exposed to end users).

## Roadmap

- Live carrier / forwarder APIs
- TrackingAgent milestones
- Multi-container splits and RAG on tariffs

## License

MIT — see [LICENSE](LICENSE).
