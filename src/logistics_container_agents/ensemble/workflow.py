from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from logistics_container_agents.domain.models import (
    BookingDocuments,
    BookingRequest,
    CarrierOffer,
    ComplianceResult,
    ConfirmedBooking,
    RateQuote,
    RoutePlan,
)
from logistics_container_agents.ensemble.bus import MessageBus


class WorkflowState:
    def __init__(self, request: BookingRequest, bus: MessageBus | None = None) -> None:
        self.bus = bus or MessageBus()
        self.request: BookingRequest | None = request
        self.route: RoutePlan | None = None
        self.quote: RateQuote | None = None
        self.carrier: CarrierOffer | None = None
        self.compliance: ComplianceResult | None = None
        self.documents: BookingDocuments | None = None
        self.booking: ConfirmedBooking | None = None
        self.transcripts: list[dict[str, str]] = []

    def _record(self, agent: str, artifact: BaseModel) -> None:
        self.transcripts.append({agent: artifact.model_dump_json()})

    def set_request(self, req: BookingRequest) -> None:
        self.request = req
        self.bus.publish("intake", "ShipperIntakeAgent", req.model_dump(mode="json"))

    def set_route(self, route: RoutePlan) -> None:
        self.route = route
        self.bus.publish("routing", "RoutePlanningAgent", route.model_dump(mode="json"))

    def set_quote(self, quote: RateQuote) -> None:
        self.quote = quote
        self.bus.publish("quoting", "RateQuotingAgent", quote.model_dump(mode="json"))

    def set_carrier(self, carrier: CarrierOffer) -> None:
        self.carrier = carrier
        self.bus.publish(
            "carrier", "CarrierSelectionAgent", carrier.model_dump(mode="json")
        )

    def set_compliance(self, result: ComplianceResult) -> None:
        self.compliance = result
        self.bus.publish(
            "compliance", "ComplianceAgent", result.model_dump(mode="json")
        )

    def set_documents(self, docs: BookingDocuments) -> None:
        self.documents = docs
        self.bus.publish(
            "documentation", "DocumentationAgent", docs.model_dump(mode="json")
        )

    def set_booking(self, booking: ConfirmedBooking) -> None:
        self.booking = booking
        self.bus.publish(
            "confirm", "BookingOrchestrator", booking.model_dump(mode="json")
        )

    def artifacts(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        if self.request:
            out["request"] = self.request.model_dump(mode="json")
        if self.route:
            out["route"] = self.route.model_dump(mode="json")
        if self.quote:
            out["quote"] = self.quote.model_dump(mode="json")
        if self.carrier:
            out["carrier"] = self.carrier.model_dump(mode="json")
        if self.compliance:
            out["compliance"] = self.compliance.model_dump(mode="json")
        if self.documents:
            out["documents"] = self.documents.model_dump(mode="json")
        if self.booking:
            out["booking"] = self.booking.model_dump(mode="json")
        return out
