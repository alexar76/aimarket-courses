"""Unit tests for courselib.sensors — offline by default; live optional."""

from __future__ import annotations

import os

import pytest

from courselib.sensors import (
    HONESTY_TABLE,
    LICENCE_TABLE,
    LIVE_WEATHER_DEVICE,
    SIM_WEATHER_DEVICE,
    SensorsError,
    add_sensor_checklist,
    atlas_health,
    atlas_nearest,
    classify_mode,
    fleet_devices,
    gaia_health,
    gaia_weather_read,
    honesty_claims,
    licence_fail_ids,
    licence_gate,
    licence_pass_ids,
    reading_from_invoke,
)


def test_licence_table_has_pass_and_fail():
    assert licence_pass_ids()
    assert licence_fail_ids()
    assert "openaq" in licence_pass_ids()
    assert "airnow" in licence_fail_ids()


@pytest.mark.parametrize(
    "token,expect",
    [
        ("CC0", "pass"),
        ("CC BY 4.0", "pass"),
        ("OGL", "pass"),
        ("U.S. PD", "pass"),
        ("CC BY-NC", "fail"),
        ("airnow", "fail"),
        ("OpenSky", "fail"),
        ("", "fail"),
    ],
)
def test_licence_gate(token, expect):
    assert licence_gate(token)["verdict"] == expect


def test_honesty_table_covers_core_claims():
    ids = {r["id"] for r in HONESTY_TABLE}
    assert {"om-as-station", "fail-loud", "sim-as-live", "public-ais-as-edge"} <= ids


@pytest.mark.parametrize(
    "claim,expect",
    [
        ("om-as-station", "dishonest"),
        ("fail-loud", "honest"),
        ("sim-as-live", "dishonest"),
        ("Open-Meteo relay reading is an in-situ weather station", "dishonest"),
        ("Upstream fail → offline status, no debit, no fake success", "honest"),
    ],
)
def test_honesty_claims(claim, expect):
    assert honesty_claims(claim)["verdict"] == expect


def test_classify_mode_live_vs_sim():
    assert classify_mode({"device_id": LIVE_WEATHER_DEVICE, "source": "https://open-meteo.com"}) == "LIVE"
    assert classify_mode({"device_id": SIM_WEATHER_DEVICE, "source": None}) == "SIM"
    assert classify_mode({"device_id": "x", "mode": "LIVE", "source": None}) == "LIVE"


def test_add_sensor_checklist_shape():
    steps = add_sensor_checklist()
    assert len(steps) >= 6
    assert all({"step", "title", "detail"} <= set(s) for s in steps)


def test_licence_table_rows_well_formed():
    for row in LICENCE_TABLE:
        assert row["verdict"] in ("pass", "fail")
        assert row["id"] and row["name"] and row["licence"]


def _online() -> bool:
    if os.environ.get("COURSE_SKIP_NETWORK", "").strip().lower() in ("1", "true", "yes", "on"):
        return False
    try:
        gaia_health(timeout=3.0)
        return True
    except SensorsError:
        return False


@pytest.mark.network
def test_live_gaia_weather_and_fleet():
    if not _online():
        pytest.skip("GAIA unreachable / COURSE_SKIP_NETWORK")
    health = gaia_health()
    assert health.get("devices", 0) > 0
    payload = gaia_weather_read(LIVE_WEATHER_DEVICE)
    reading = reading_from_invoke(payload)
    assert reading.get("device_id") == LIVE_WEATHER_DEVICE
    assert "temperature_c" in (reading.get("values") or {})
    devices = fleet_devices()
    assert len(devices) >= max(1, int(health.get("devices", 0)) - 5)
    om = next(d for d in devices if d["device_id"] == LIVE_WEATHER_DEVICE)
    assert classify_mode(om) == "LIVE"


@pytest.mark.network
def test_live_atlas_nearest():
    if not _online():
        pytest.skip("GAIA unreachable / COURSE_SKIP_NETWORK")
    try:
        ath = atlas_health(timeout=3.0)
    except SensorsError:
        pytest.skip("ATLAS unreachable")
    assert ath.get("stations", 0) > 0
    payload = atlas_nearest(52.52, 13.41)
    assert payload.get("ok") is True
    assert "distance_km" in payload
    assert isinstance(payload.get("nearest"), dict)
