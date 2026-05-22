import pytest

from logistics_container_agents.domain.models import (
    BookingRequest,
    CargoDetails,
    ContainerSpec,
    ContainerType,
    Incoterm,
    Port,
    ShipperParty,
)
from logistics_container_agents.ensemble.runner import EnsembleRunner
from tests.support.mock_llm import MockLLMProvider


@pytest.mark.asyncio
async def test_golden_path_booking(
    sample_request: BookingRequest, mock_llm: MockLLMProvider
) -> None:
    runner = EnsembleRunner(mock_llm)
    result = await runner.run(sample_request)
    assert result.success is True
    assert result.booking is not None
    assert result.booking.booking_reference.startswith("TEST-")


@pytest.mark.asyncio
async def test_compliance_blocks_denied_party() -> None:
    request = BookingRequest(
        shipper=ShipperParty(name="Blocked Shipping LLC"),
        origin=Port(unlocode="CNSHA", name="Shanghai", country="CN"),
        destination=Port(unlocode="USLAX", name="Los Angeles", country="US"),
        cargo=CargoDetails(
            commodity="Goods", weight_kg=1000, volume_cbm=10, hazmat=False
        ),
        containers=[ContainerSpec(type=ContainerType.GP20, quantity=1)],
        incoterm=Incoterm.FOB,
    )
    llm = MockLLMProvider(request)
    runner = EnsembleRunner(llm)
    result = await runner.run(request)
    assert result.success is False
    assert result.blocked_reasons


@pytest.mark.asyncio
async def test_hazmat_flags_but_not_auto_blocked(sample_request: BookingRequest) -> None:
    sample_request.cargo.hazmat = True
    llm = MockLLMProvider(sample_request)
    runner = EnsembleRunner(llm)
    result = await runner.run(sample_request)
    assert result.success is True
    assert "hazmat_review" in (result.artifacts.get("compliance", {}).get("flags") or [])
