from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class AgentEvent:
    stage: str
    agent: str
    payload: dict[str, Any]


class MessageBus:
    def __init__(self) -> None:
        self.events: list[AgentEvent] = []

    def publish(self, stage: str, agent: str, payload: dict[str, Any]) -> None:
        self.events.append(
            AgentEvent(stage=stage, agent=agent, payload=payload)
        )
