from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ContainerType(str, Enum):
    GP20 = "20GP"
    HC40 = "40HC"
    GP40 = "40GP"


class Incoterm(str, Enum):
    EXW = "EXW"
    FOB = "FOB"
    CIF = "CIF"
    DDP = "DDP"


class Port(BaseModel):
    unlocode: str = Field(..., description="UN/LOCODE, e.g. CNSHA")
    name: str
    country: str


class ShipperParty(BaseModel):
    name: str
    contact_email: str | None = None


class CargoDetails(BaseModel):
    commodity: str
    weight_kg: float
    volume_cbm: float
    hazmat: bool = False


class ContainerSpec(BaseModel):
    type: ContainerType
    quantity: int = Field(ge=1, le=50)
    soc: bool = False


class BookingRequest(BaseModel):
    shipper: ShipperParty
    origin: Port
    destination: Port
    cargo: CargoDetails
    containers: list[ContainerSpec]
    incoterm: Incoterm
    ready_date: date | None = None
    notes: str | None = None


class RouteLeg(BaseModel):
    from_port: str
    to_port: str
    mode: str = "ocean"
    carrier_line: str | None = None
    etd: date | None = None
    eta: date | None = None


class RoutePlan(BaseModel):
    legs: list[RouteLeg]
    transshipment_ports: list[str] = Field(default_factory=list)
    transit_days: int = Field(ge=1)


class RateLineItem(BaseModel):
    code: str
    description: str
    amount_usd: float


class RateQuote(BaseModel):
    currency: str = "USD"
    ocean_freight_usd: float
    surcharges: list[RateLineItem] = Field(default_factory=list)
    total_usd: float
    valid_until: date


class CarrierOffer(BaseModel):
    carrier_line: str
    service_string: str
    voyage: str
    vessel_name: str
    space_allocation: str
    reliability_score: float = Field(ge=0.0, le=1.0)


class ComplianceResult(BaseModel):
    blocked: bool
    flags: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class BookingDocuments(BaseModel):
    shipping_instruction_draft: str
    bl_instructions: str


class ConfirmedBooking(BaseModel):
    booking_reference: str
    carrier_line: str
    voyage: str
    origin: str
    destination: str
    container_summary: str
    documentation_cutoff: datetime
    vgm_cutoff: datetime
    summary: str


class WorkflowResult(BaseModel):
    success: bool
    booking: ConfirmedBooking | None = None
    blocked_reasons: list[str] = Field(default_factory=list)
    artifacts: dict[str, Any] = Field(default_factory=dict)
    events: list[dict[str, Any]] = Field(default_factory=list)
