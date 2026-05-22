"""TrackingAgent stub — not wired into v1 pipeline."""

from pydantic import BaseModel, Field


class TrackingMilestone(BaseModel):
    code: str
    description: str
    at: str | None = None


class TrackingSnapshot(BaseModel):
    booking_reference: str
    milestones: list[TrackingMilestone] = Field(default_factory=list)


class TrackingAgent:
    """Placeholder for future milestone/ETA tracking."""

    async def fetch(self, booking_reference: str) -> TrackingSnapshot:
        return TrackingSnapshot(booking_reference=booking_reference, milestones=[])
