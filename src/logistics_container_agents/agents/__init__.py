from logistics_container_agents.agents.carrier_selection import CarrierSelectionAgent
from logistics_container_agents.agents.compliance import ComplianceAgent
from logistics_container_agents.agents.documentation import DocumentationAgent
from logistics_container_agents.agents.orchestrator import BookingOrchestratorAgent
from logistics_container_agents.agents.rate_quoting import RateQuotingAgent
from logistics_container_agents.agents.route_planning import RoutePlanningAgent
from logistics_container_agents.agents.shipper_intake import ShipperIntakeAgent

AGENT_ROSTER = [
    ShipperIntakeAgent,
    RoutePlanningAgent,
    RateQuotingAgent,
    CarrierSelectionAgent,
    ComplianceAgent,
    DocumentationAgent,
    BookingOrchestratorAgent,
]

__all__ = [
    "AGENT_ROSTER",
    "BookingOrchestratorAgent",
    "CarrierSelectionAgent",
    "ComplianceAgent",
    "DocumentationAgent",
    "RateQuotingAgent",
    "RoutePlanningAgent",
    "ShipperIntakeAgent",
]
