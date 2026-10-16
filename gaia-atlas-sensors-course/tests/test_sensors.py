"""Unit tests for courselib.sensors — offline by default; live optional."""

from __future__ import annotations

import io
import json
import os
import re
import urllib.error

import pytest

import courselib.sensors as sensors
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


# ── Where each read goes: priced via the hub's sandbox trial, free direct ─────


class _Recorder:
    """Stands in for urlopen: records each request and answers like GAIA via the hub."""

    def __init__(self, status: int = 200, body: dict | None = None) -> None:
        self.requests: list = []
        self.status = status
        self.body = body

    def __call__(self, req, timeout=None, context=None):
        self.requests.append(req)
        if self.status != 200:
            raise urllib.error.HTTPError(
                req.full_url, self.status, "refused", {}, io.BytesIO(json.dumps(self.body).encode())
            )
        body = self.body or {
            "ok": True,
            "success": True,
            "output": {"reading": {"device_id": "ws-01", "values": {"temperature_c": 11.5}}},
            "sandbox": {"sandbox": True, "remaining": 4, "used": 1, "max_trials": 5},
        }
        return io.BytesIO(json.dumps(body).encode())


@pytest.fixture
def offline_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    for name in ("COURSE_SANDBOX_VISITOR", "COURSE_HUB_URL", "COURSE_GAIA_URL", "GAIA_PUBLIC_URL"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(sensors, "_session_visitor", None)
    return tmp_path


def test_priced_weather_read_goes_through_the_hub_trial(offline_home, monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(sensors.urllib.request, "urlopen", rec)
    payload = gaia_weather_read(SIM_WEATHER_DEVICE)
    assert reading_from_invoke(payload)["device_id"] == "ws-01"

    (req,) = rec.requests
    assert req.full_url == "https://modelmarket.dev/ai-market/v2/invoke"
    assert json.loads(req.data) == {
        "product_id": "gaia.gateway",
        "capability_id": "gaia.weather.read@v1",
        "input": {"device_id": "ws-01"},
        "source_hub": "https://iot.modelmarket.dev",
    }
    visitor = req.get_header("X-aimarket-sandbox-visitor")
    assert re.fullmatch(r"[A-Za-z0-9_-]{8,64}", visitor)
    assert not req.get_header("X-payment-channel")


def test_hub_url_is_configurable(offline_home, monkeypatch):
    monkeypatch.setenv("COURSE_HUB_URL", "https://hub.example/")
    rec = _Recorder()
    monkeypatch.setattr(sensors.urllib.request, "urlopen", rec)
    gaia_weather_read(LIVE_WEATHER_DEVICE)
    assert rec.requests[0].full_url == "https://hub.example/ai-market/v2/invoke"


def test_free_fleet_status_stays_direct_to_gaia(offline_home, monkeypatch):
    rec = _Recorder(body={"ok": True, "output": {"devices": [{"device_id": "ws-01", "source": None}]}})
    monkeypatch.setattr(sensors.urllib.request, "urlopen", rec)
    assert fleet_devices()[0]["device_id"] == "ws-01"
    (req,) = rec.requests
    assert req.full_url == "https://iot.modelmarket.dev/ai-market/v2/invoke"
    assert json.loads(req.data) == {"capability_id": "gaia.fleet.status@v1", "input": {}}
    assert not req.get_header("X-aimarket-sandbox-visitor")


def test_visitor_id_is_random_once_then_stable(offline_home):
    first = sensors.sandbox_visitor_id()
    assert re.fullmatch(r"course-[0-9a-f]{24}", first)
    saved = offline_home / "gaia-atlas-sensors-course" / "sandbox-visitor"
    assert saved.read_text().strip() == first
    sensors._session_visitor = None  # a new process reads the same file
    assert sensors.sandbox_visitor_id() == first


def test_visitor_id_override_is_checked(offline_home, monkeypatch):
    monkeypatch.setenv("COURSE_SANDBOX_VISITOR", "my-lab-seat-07")
    assert sensors.sandbox_visitor_id() == "my-lab-seat-07"
    monkeypatch.setenv("COURSE_SANDBOX_VISITOR", "short")
    with pytest.raises(SensorsError, match="8-64"):
        sensors.sandbox_visitor_id()


def test_a_spent_trial_says_so(offline_home, monkeypatch):
    rec = _Recorder(429, {"success": False, "error": "trial_quota_exhausted"})
    monkeypatch.setattr(sensors.urllib.request, "urlopen", rec)
    with pytest.raises(SensorsError, match="free trial is spent") as info:
        gaia_weather_read(SIM_WEATHER_DEVICE)
    assert info.value.status == 429 and "trial_quota_exhausted" in str(info.value)


def test_a_network_rate_limit_is_not_called_a_spent_trial(offline_home, monkeypatch):
    rec = _Recorder(429, {"success": False, "error": "rate_limit_exceeded"})
    monkeypatch.setattr(sensors.urllib.request, "urlopen", rec)
    with pytest.raises(SensorsError) as info:
        gaia_weather_read(SIM_WEATHER_DEVICE)
    assert info.value.status == 429 and "free trial" not in str(info.value)


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
