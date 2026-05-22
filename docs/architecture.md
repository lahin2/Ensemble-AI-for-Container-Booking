# Architecture

## Overview

Logistics Container Agents is an **ensemble** of role-specific LLM agents that collaborate on a single **FCL container booking** workflow. Each agent reads prior artifacts from `WorkflowState`, calls deterministic maritime tools where needed, and returns a **Pydantic-validated** structured object.

## Pipeline

1. **ShipperIntakeAgent** — normalize `BookingRequest`
2. **RoutePlanningAgent** — `RoutePlan` from schedule data
3. **RateQuotingAgent** — `RateQuote` from rate tables
4. **CarrierSelectionAgent** — `CarrierOffer`
5. **ComplianceAgent** — `ComplianceResult` (may block)
6. **DocumentationAgent** — `BookingDocuments`
7. **BookingOrchestrator** — `ConfirmedBooking`

`EnsembleRunner` runs stages sequentially. If compliance blocks, the pipeline stops and returns a failure payload with reasons.

## Components

| Layer | Responsibility |
|-------|----------------|
| `domain/` | Shared types and JSON schema for agent I/O |
| `tools/` | In-repo schedules, rates, sanctions (no external APIs) |
| `llm/` | User-configured providers (OpenAI, Anthropic, local) |
| `agents/` | Role prompts + structured completion |
| `ensemble/` | Orchestration, message bus, workflow state |

## LLM configuration

Users must set `LLM_PROVIDER` and the matching credentials. See [configuration.md](configuration.md). There is no bundled mock runtime for end users.

## Extension points

- Add agents by subclassing `BaseAgent` and registering in `EnsembleRunner`
- Swap tool backends for live carrier APIs
- Add `TrackingAgent` milestones without changing the pipeline contract
