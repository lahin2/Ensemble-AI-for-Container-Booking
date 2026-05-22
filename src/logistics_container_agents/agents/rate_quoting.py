from logistics_container_agents.agents.base import BaseAgent
from logistics_container_agents.domain.models import RateQuote


class RateQuotingAgent(BaseAgent):
    role = "RateQuotingAgent"
    output_schema = RateQuote
