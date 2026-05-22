from logistics_container_agents.agents.base import BaseAgent
from logistics_container_agents.domain.models import BookingDocuments


class DocumentationAgent(BaseAgent):
    role = "DocumentationAgent"
    output_schema = BookingDocuments
