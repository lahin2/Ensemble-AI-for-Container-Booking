from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).parent / "data"


def _load_json(name: str) -> Any:
    with (_DATA_DIR / name).open(encoding="utf-8") as f:
        return json.load(f)


def lookup_schedules(origin: str, destination: str) -> list[dict[str, Any]]:
    schedules = _load_json("schedules.json")
    return [
        s
        for s in schedules
        if s["origin"] == origin and s["destination"] == destination
    ]


def get_lane_rates(
    origin: str, destination: str, container_type: str
) -> dict[str, Any] | None:
    rates = _load_json("rates.json")
    for row in rates:
        if (
            row["origin"] == origin
            and row["destination"] == destination
            and row["container_type"] == container_type
        ):
            return row
    return None


def screen_party(party_name: str) -> dict[str, Any]:
    sanctions = _load_json("sanctions.json")
    denied = party_name.strip().lower() in {
        p.lower() for p in sanctions["denied_parties"]
    }
    return {
        "denied": denied,
        "hazmat_requires_review": sanctions.get("hazmat_requires_review", True),
    }


def allocate_space(carrier_line: str, voyage: str) -> dict[str, str]:
    return {
        "carrier_line": carrier_line,
        "voyage": voyage,
        "space_allocation": "1x40HC confirmed (simulated)",
        "status": "allocated",
    }


def build_tool_context(
    origin: str,
    destination: str,
    container_type: str,
    party_name: str,
) -> str:
    schedules = lookup_schedules(origin, destination)
    rates = get_lane_rates(origin, destination, container_type)
    screening = screen_party(party_name)
    return json.dumps(
        {
            "schedules": schedules,
            "rates": rates,
            "compliance_screening": screening,
        },
        indent=2,
    )
