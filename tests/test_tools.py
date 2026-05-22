from logistics_container_agents.tools.maritime import (
    get_lane_rates,
    lookup_schedules,
    screen_party,
)


def test_lookup_schedules() -> None:
    rows = lookup_schedules("CNSHA", "USLAX")
    assert len(rows) >= 1
    assert rows[0]["origin"] == "CNSHA"


def test_get_lane_rates() -> None:
    rate = get_lane_rates("CNSHA", "USLAX", "40HC")
    assert rate is not None
    assert rate["base_ocean_usd"] > 0


def test_screen_party_denied() -> None:
    result = screen_party("Blocked Shipping LLC")
    assert result["denied"] is True


def test_screen_party_ok() -> None:
    result = screen_party("Acme Electronics Ltd")
    assert result["denied"] is False
