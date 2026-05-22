from __future__ import annotations

import json
from logistics_container_agents.agents import (
    BookingOrchestratorAgent,
    CarrierSelectionAgent,
    ComplianceAgent,
    DocumentationAgent,
    RateQuotingAgent,
    RoutePlanningAgent,
    ShipperIntakeAgent,
)
from logistics_container_agents.domain.models import BookingRequest, WorkflowResult
from logistics_container_agents.ensemble.workflow import WorkflowState
from logistics_container_agents.llm.base import LLMProvider
from logistics_container_agents.tools.maritime import build_tool_context, screen_party


class EnsembleRunner:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm
        self._intake = ShipperIntakeAgent(llm)
        self._route = RoutePlanningAgent(llm)
        self._rate = RateQuotingAgent(llm)
        self._carrier = CarrierSelectionAgent(llm)
        self._compliance = ComplianceAgent(llm)
        self._docs = DocumentationAgent(llm)
        self._orchestrator = BookingOrchestratorAgent(llm)

    async def run(self, request: BookingRequest) -> WorkflowResult:
        state = WorkflowState(request)

        container_type = request.containers[0].type.value
        tool_ctx = build_tool_context(
            request.origin.unlocode,
            request.destination.unlocode,
            container_type,
            request.shipper.name,
        )
        screening = screen_party(request.shipper.name)

        intake_out = await self._intake.run(
            f"Normalize this booking request:\n{request.model_dump_json(indent=2)}"
        )
        state.set_request(intake_out)  # type: ignore[arg-type]
        req = state.request
        assert req is not None

        route_out = await self._route.run(
            f"Booking:\n{req.model_dump_json()}\n\nSchedule data:\n{tool_ctx}"
        )
        state.set_route(route_out)  # type: ignore[arg-type]

        quote_out = await self._rate.run(
            f"Booking:\n{req.model_dump_json()}\n\nRoute:\n"
            f"{state.route.model_dump_json()}\n\nRates:\n{tool_ctx}"
        )
        state.set_quote(quote_out)  # type: ignore[arg-type]

        carrier_out = await self._carrier.run(
            f"Route:\n{state.route.model_dump_json()}\n\nQuote:\n"
            f"{state.quote.model_dump_json()}\n\nOptions:\n{tool_ctx}"
        )
        state.set_carrier(carrier_out)  # type: ignore[arg-type]

        compliance_prompt = json.dumps(
            {
                "shipper": req.shipper.model_dump(),
                "cargo": req.cargo.model_dump(),
                "tool_screening": screening,
            },
            indent=2,
        )
        compliance_out = await self._compliance.run(
            f"Assess compliance:\n{compliance_prompt}"
        )
        state.set_compliance(compliance_out)  # type: ignore[arg-type]

        if compliance_out.blocked:
            return WorkflowResult(
                success=False,
                blocked_reasons=compliance_out.reasons,
                artifacts=state.artifacts(),
                events=[e.__dict__ for e in state.bus.events],
            )

        docs_out = await self._docs.run(
            f"Draft documents for:\n{json.dumps(state.artifacts(), indent=2)}"
        )
        state.set_documents(docs_out)  # type: ignore[arg-type]

        booking_out = await self._orchestrator.run(
            f"Confirm booking from artifacts:\n{json.dumps(state.artifacts(), indent=2)}"
        )
        state.set_booking(booking_out)  # type: ignore[arg-type]

        return WorkflowResult(
            success=True,
            booking=state.booking,
            artifacts=state.artifacts(),
            events=[e.__dict__ for e in state.bus.events],
        )
