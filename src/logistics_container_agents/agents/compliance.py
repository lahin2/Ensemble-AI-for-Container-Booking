from logistics_container_agents.agents.base import BaseAgent
from logistics_container_agents.domain.models import ComplianceResult


class ComplianceAgent(BaseAgent):
    role = "ComplianceAgent"
    output_schema = ComplianceResult
