from logistics_container_agents.agents.base import BaseAgent
from logistics_container_agents.domain.models import RoutePlan


class RoutePlanningAgent(BaseAgent):
    role = "RoutePlanningAgent"
    output_schema = RoutePlan
