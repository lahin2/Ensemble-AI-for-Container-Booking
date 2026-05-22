from logistics_container_agents.agents.base import BaseAgent
from logistics_container_agents.domain.models import CarrierOffer


class CarrierSelectionAgent(BaseAgent):
    role = "CarrierSelectionAgent"
    output_schema = CarrierOffer
