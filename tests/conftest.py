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
from tests.support.mock_llm import MockLLMProvider


@pytest.fixture
def sample_request() -> BookingRequest:
    return BookingRequest(
        shipper=ShipperParty(name="Acme Electronics Ltd", contact_email="ops@acme.example"),
        origin=Port(unlocode="CNSHA", name="Shanghai", country="CN"),
        destination=Port(unlocode="USLAX", name="Los Angeles", country="US"),
        cargo=CargoDetails(
            commodity="Consumer electronics",
            weight_kg=12000,
            volume_cbm=58,
            hazmat=False,
        ),
        containers=[ContainerSpec(type=ContainerType.HC40, quantity=1)],
        incoterm=Incoterm.FOB,
    )


@pytest.fixture
def mock_llm(sample_request: BookingRequest) -> MockLLMProvider:
    llm = MockLLMProvider(sample_request)
    return llm
