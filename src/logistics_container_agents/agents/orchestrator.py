from logistics_container_agents.agents.base import BaseAgent
from logistics_container_agents.domain.models import ConfirmedBooking


class BookingOrchestratorAgent(BaseAgent):
    role = "BookingOrchestrator"
    output_schema = ConfirmedBooking
