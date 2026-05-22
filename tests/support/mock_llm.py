"""Dev/test-only mock LLM — not part of the public package API."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import TypeVar

from pydantic import BaseModel

from logistics_container_agents.domain.models import (
    BookingDocuments,
    BookingRequest,
    CarrierOffer,
    ComplianceResult,
    ConfirmedBooking,
    ContainerType,
    Incoterm,
    Port,
    RateLineItem,
    RateQuote,
    RouteLeg,
    RoutePlan,
    ShipperParty,
)

T = TypeVar("T", bound=BaseModel)

_BLOCKED = "blocked shipping llc"


class MockLLMProvider:
    """Deterministic structured outputs for pytest (not for end users)."""

    def __init__(self, request: BookingRequest | None = None) -> None:
        self._request = request

    def bind_request(self, request: BookingRequest) -> None:
        self._request = request

    async def complete_structured(
        self,
        *,
        system: str,
        user: str,
        schema: type[T],
    ) -> T:
        req = self._request
        if schema is BookingRequest and req:
            return schema.model_validate(req.model_dump())  # type: ignore[return-value]

        if schema is RoutePlan:
            origin = req.origin.unlocode if req else "CNSHA"
            dest = req.destination.unlocode if req else "USLAX"
            return RoutePlan(
                legs=[
                    RouteLeg(
                        from_port=origin,
                        to_port=dest,
                        mode="ocean",
                        carrier_line="Pacific Star Line",
                        etd=date(2026, 6, 10),
                        eta=date(2026, 6, 28),
                    )
                ],
                transshipment_ports=[],
                transit_days=18,
            )  # type: ignore[return-value]

        if schema is RateQuote:
            return RateQuote(
                ocean_freight_usd=2850.0,
                surcharges=[
                    RateLineItem(code="BAF", description="Bunker", amount_usd=320.0)
                ],
                total_usd=3650.0,
                valid_until=date.today() + timedelta(days=14),
            )  # type: ignore[return-value]

        if schema is CarrierOffer:
            return CarrierOffer(
                carrier_line="Pacific Star Line",
                service_string="PSL-TP1",
                voyage="PSL401E",
                vessel_name="MV Horizon Star",
                space_allocation="1x40HC confirmed (simulated)",
                reliability_score=0.92,
            )  # type: ignore[return-value]

        if schema is ComplianceResult:
            name = (req.shipper.name if req else "").lower()
            blocked = _BLOCKED in name
            flags: list[str] = []
            reasons: list[str] = []
            if blocked:
                reasons.append("Party on sanctions deny-list")
            if req and req.cargo.hazmat:
                flags.append("hazmat_review")
                reasons.append("Hazmat requires manual review")
            return ComplianceResult(blocked=blocked, flags=flags, reasons=reasons)  # type: ignore[return-value]

        if schema is BookingDocuments:
            return BookingDocuments(
                shipping_instruction_draft="SI draft (test)",
                bl_instructions="B/L instructions (test)",
            )  # type: ignore[return-value]

        if schema is ConfirmedBooking:
            return ConfirmedBooking(
                booking_reference="TEST-BKG-001",
                carrier_line="Pacific Star Line",
                voyage="PSL401E",
                origin=req.origin.unlocode if req else "CNSHA",
                destination=req.destination.unlocode if req else "USLAX",
                container_summary="1x40HC",
                documentation_cutoff=datetime(2026, 6, 8, 12, 0, 0),
                vgm_cutoff=datetime(2026, 6, 9, 12, 0, 0),
                summary="Test confirmed booking",
            )  # type: ignore[return-value]

        raise NotImplementedError(f"MockLLMProvider has no fixture for {schema.__name__}")
