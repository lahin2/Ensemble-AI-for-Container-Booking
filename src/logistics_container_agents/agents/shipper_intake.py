from logistics_container_agents.agents.base import BaseAgent
from logistics_container_agents.domain.models import BookingRequest


class ShipperIntakeAgent(BaseAgent):
    role = "ShipperIntakeAgent"
    output_schema = BookingRequest
