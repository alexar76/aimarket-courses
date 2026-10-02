"""GAIA / ATLAS HTTP helpers and teaching tables for the sensors course.

Live endpoints (override with env):
  COURSE_GAIA_URL / GAIA_PUBLIC_URL  → https://iot.modelmarket.dev
  COURSE_ATLAS_URL / ATLAS_PUBLIC_URL → https://atlas.modelmarket.dev

No mocks on LIVE paths — network failures raise SensorsError loudly.
Licence / honesty tables are embedded teaching data (offline-safe).
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request
from typing import Any

DEFAULT_GAIA_URL = "https://iot.modelmarket.dev"
DEFAULT_ATLAS_URL = "https://atlas.modelmarket.dev"
DEFAULT_TIMEOUT = 12.0

# Teaching defaults — LIVE Open-Meteo relay vs SIM campus pin
LIVE_WEATHER_DEVICE = "om-wx-01"
SIM_WEATHER_DEVICE = "ws-01"
WEATHER_CAP = "gaia.weather.read@v1"
FLEET_CAP = "gaia.fleet.status@v1"
ATLAS_NEAREST_CAP = "atlas.nearest.read@v1"
ATLAS_POINT_CAP = "atlas.point.read@v1"


class SensorsError(RuntimeError):
    """Raised when a live GAIA/ATLAS call fails or returns a non-ok payload."""


def gaia_base_url() -> str:
    return (
        os.environ.get("COURSE_GAIA_URL")
        or os.environ.get("GAIA_PUBLIC_URL")
        or DEFAULT_GAIA_URL
    ).rstrip("/")


def atlas_base_url() -> str:
    return (
        os.environ.get("COURSE_ATLAS_URL")
        or os.environ.get("ATLAS_PUBLIC_URL")
        or DEFAULT_ATLAS_URL
    ).rstrip("/")


def _request_json(
    method: str,
    url: str,
    *,
    body: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Accept": "application/json", "User-Agent": "gaia-atlas-sensors-course/0.1"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode("utf-8")
            if not raw.strip():
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        raise SensorsError(f"HTTP {exc.code} for {url}: {detail or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise SensorsError(f"offline or unreachable: {url} ({exc.reason})") from exc
    except TimeoutError as exc:
        raise SensorsError(f"timeout after {timeout}s: {url}") from exc
    except json.JSONDecodeError as exc:
        raise SensorsError(f"invalid JSON from {url}: {exc}") from exc


def get_json(url: str, *, timeout: float = DEFAULT_TIMEOUT) -> Any:
    return _request_json("GET", url, timeout=timeout)


def post_json(url: str, body: dict[str, Any], *, timeout: float = DEFAULT_TIMEOUT) -> Any:
    return _request_json("POST", url, body=body, timeout=timeout)


def health(base_url: str | None = None, *, timeout: float = 8.0) -> dict[str, Any]:
    """GET /health — GAIA returns devices count; ATLAS returns stations count."""
    base = (base_url or gaia_base_url()).rstrip("/")
    payload = get_json(f"{base}/health", timeout=timeout)
    if not isinstance(payload, dict):
        raise SensorsError(f"unexpected health payload from {base}")
    return payload


def gaia_health(*, timeout: float = 8.0) -> dict[str, Any]:
    return health(gaia_base_url(), timeout=timeout)


def atlas_health(*, timeout: float = 8.0) -> dict[str, Any]:
    return health(atlas_base_url(), timeout=timeout)


def invoke(
    capability_id: str,
    input_payload: dict[str, Any] | None = None,
    *,
    base_url: str | None = None,
    product_id: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """POST /ai-market/v2/invoke — fail loudly on transport or ok:false."""
    base = (base_url or gaia_base_url()).rstrip("/")
    body: dict[str, Any] = {
        "capability_id": capability_id,
        "input": input_payload or {},
    }
    if product_id:
        body["product_id"] = product_id
    payload = post_json(f"{base}/ai-market/v2/invoke", body, timeout=timeout)
    if not isinstance(payload, dict):
        raise SensorsError(f"unexpected invoke payload for {capability_id}")
    if payload.get("ok") is False:
        raise SensorsError(f"invoke failed for {capability_id}: {payload.get('error') or payload}")
    return payload


def gaia_fleet_status(*, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Invoke gaia.fleet.status@v1 — returns full response including output.devices."""
    return invoke(FLEET_CAP, {}, timeout=timeout)


def fleet_devices(*, timeout: float = DEFAULT_TIMEOUT) -> list[dict[str, Any]]:
    payload = gaia_fleet_status(timeout=timeout)
    out = payload.get("output") or {}
    devices = out.get("devices") if isinstance(out, dict) else None
    if not isinstance(devices, list):
        raise SensorsError("fleet.status missing output.devices list")
    return devices


def gaia_weather_read(
    device_id: str = LIVE_WEATHER_DEVICE,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Invoke gaia.weather.read@v1 for a device (LIVE om-wx-01 or SIM ws-01)."""
    return invoke(WEATHER_CAP, {"device_id": device_id}, timeout=timeout)


def atlas_nearest(
    lat: float = 52.52,
    lon: float = 13.41,
    *,
    layers: list[str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Invoke atlas.nearest.read@v1 against the live ATLAS hub."""
    body: dict[str, Any] = {"lat": lat, "lon": lon}
    if layers:
        body["layers"] = layers
    return invoke(ATLAS_NEAREST_CAP, body, base_url=atlas_base_url(), timeout=timeout)


def atlas_point_read(
    lat: float,
    lon: float,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    return invoke(
        ATLAS_POINT_CAP,
        {"lat": lat, "lon": lon},
        base_url=atlas_base_url(),
        timeout=timeout,
    )


# ---------------------------------------------------------------------------
# LIVE vs SIM classification (offline-safe helpers)
# ---------------------------------------------------------------------------


def is_live_device(device: dict[str, Any]) -> bool:
    """LIVE iff provenance source is set; SIM otherwise (ATLAS/GAIA honesty rule)."""
    source = device.get("source")
    if source is None or source == "" or source is False:
        # ATLAS pins may use mode/live flags
        mode = str(device.get("mode") or "").upper()
        if mode == "LIVE" or device.get("live") is True:
            return True
        return False
    return True


def classify_mode(device_or_reading: dict[str, Any]) -> str:
    """Return 'LIVE' or 'SIM' for a fleet device, ATLAS pin, or weather output."""
    if "reading" in device_or_reading and isinstance(device_or_reading.get("reading"), dict):
        # full invoke output — prefer nested reading device_id + outer attestation
        reading = device_or_reading["reading"]
        device_id = str(reading.get("device_id") or "")
        if device_id == LIVE_WEATHER_DEVICE:
            return "LIVE"
        if device_id == SIM_WEATHER_DEVICE:
            return "SIM"
    if is_live_device(device_or_reading):
        return "LIVE"
    device_id = str(device_or_reading.get("device_id") or "")
    if device_id.startswith("om-") or device_id.startswith("nws-") or device_id.startswith("usgs-"):
        # known live-kind prefixes when source omitted from reading blob
        if device_or_reading.get("model") and "Open-Meteo" in str(device_or_reading.get("model")):
            return "LIVE"
    if device_id in (SIM_WEATHER_DEVICE, "aq-01", "en-01") or device_id.startswith("ws-"):
        if not device_or_reading.get("source"):
            return "SIM"
    return "LIVE" if is_live_device(device_or_reading) else "SIM"


def reading_from_invoke(payload: dict[str, Any]) -> dict[str, Any]:
    out = payload.get("output") or {}
    if isinstance(out, dict) and isinstance(out.get("reading"), dict):
        return out["reading"]
    raise SensorsError("weather invoke missing output.reading")


# ---------------------------------------------------------------------------
# Licence gate — commercial rail teaching table (offline)
# ---------------------------------------------------------------------------

# Pass bar: CC0 / CC BY / OGL / NLOD / U.S. PD / Copernicus CC BY
_PASS_TOKENS = (
    "CC0",
    "CC BY",
    "CC-BY",
    "OGL",
    "NLOD",
    "U.S. PD",
    "US PD",
    "PUBLIC DOMAIN",
    "PD",
    "COPERNICUS",
)

_FAIL_TOKENS = (
    "BY-NC",
    "CC BY-NC",
    "NON-COMMERCIAL",
    "NC ",
    " INDICATIVE",
    "HELPDESK-ONLY",
)

# Named candidates from the commercial shortlist
LICENCE_TABLE: list[dict[str, str]] = [
    {
        "id": "openaq",
        "name": "OpenAQ",
        "licence": "CC BY 4.0",
        "verdict": "pass",
        "note": "Ships on prod key — free explore.openaq.org key.",
    },
    {
        "id": "open-meteo-data",
        "name": "Open-Meteo data (CC BY)",
        "licence": "CC BY 4.0",
        "verdict": "pass",
        "note": "Data licence OK; hosted free endpoint ToS is separate.",
    },
    {
        "id": "usgs",
        "name": "USGS earthquake / river",
        "licence": "U.S. PD",
        "verdict": "pass",
        "note": "US Government public domain.",
    },
    {
        "id": "nws",
        "name": "NWS / NOAA",
        "licence": "U.S. PD",
        "verdict": "pass",
        "note": "US Government public domain.",
    },
    {
        "id": "safecast",
        "name": "Safecast",
        "licence": "CC0",
        "verdict": "pass",
        "note": "CC0 — commercial OK.",
    },
    {
        "id": "firms",
        "name": "NASA FIRMS",
        "licence": "CC0 / PD-ish (NASA citation)",
        "verdict": "pass",
        "note": "Cite NASA; commercial rail OK.",
    },
    {
        "id": "uk-ogl",
        "name": "UK Carbon Intensity",
        "licence": "OGL",
        "verdict": "pass",
        "note": "Open Government Licence.",
    },
    {
        "id": "airnow",
        "name": "EPA AirNow",
        "licence": "Data Exchange Guidelines",
        "verdict": "fail",
        "note": "Hold until recorded operator assent — not shipped.",
    },
    {
        "id": "opensky",
        "name": "OpenSky",
        "licence": "non-commercial research",
        "verdict": "fail",
        "note": "Hard no for paid Hub SKUs.",
    },
    {
        "id": "adsbx",
        "name": "ADS-B Exchange",
        "licence": "restrictive ToS",
        "verdict": "fail",
        "note": "Hard no as commercial relay.",
    },
    {
        "id": "purpleair",
        "name": "PurpleAir",
        "licence": "commercial SaaS ToS",
        "verdict": "fail",
        "note": "Not on commercial rail.",
    },
    {
        "id": "stanford-nc",
        "name": "Stanford CC BY-NC dump",
        "licence": "CC BY-NC",
        "verdict": "fail",
        "note": "NC blocks Hub SKUs.",
    },
]


def licence_gate(licence_or_id: str) -> dict[str, Any]:
    """Classify a licence string or table id as pass/fail for the commercial rail.

    Returns ``{"verdict": "pass"|"fail", "reason": str, "licence": str}``.
    """
    raw = (licence_or_id or "").strip()
    if not raw:
        return {"verdict": "fail", "reason": "empty licence", "licence": raw}

    lower = raw.lower()
    for row in LICENCE_TABLE:
        if lower in (row["id"], row["name"].lower()):
            return {
                "verdict": row["verdict"],
                "reason": row["note"],
                "licence": row["licence"],
                "id": row["id"],
            }

    upper = raw.upper()
    for tok in _FAIL_TOKENS:
        if tok.strip().upper() in upper or tok.lower() in lower:
            return {
                "verdict": "fail",
                "reason": f"blocked token matched: {tok.strip()}",
                "licence": raw,
            }

    # AirNow / Data Exchange Guidelines without assent
    if "airnow" in lower or "data exchange guidelines" in lower:
        return {
            "verdict": "fail",
            "reason": "AirNow requires Data Exchange Guidelines assent",
            "licence": raw,
        }

    for tok in _PASS_TOKENS:
        if tok.upper() in upper:
            # bare "NC" already handled; bare "PD" ok
            if tok.upper() == "PD" and "BY-NC" in upper:
                continue
            return {
                "verdict": "pass",
                "reason": f"allowed licence family: {tok}",
                "licence": raw,
            }

    return {
        "verdict": "fail",
        "reason": "unknown / not on commercial allowlist",
        "licence": raw,
    }


def licence_pass_ids() -> list[str]:
    return [r["id"] for r in LICENCE_TABLE if r["verdict"] == "pass"]


def licence_fail_ids() -> list[str]:
    return [r["id"] for r in LICENCE_TABLE if r["verdict"] == "fail"]


# ---------------------------------------------------------------------------
# Honesty claims classifier (offline)
# ---------------------------------------------------------------------------

HONESTY_TABLE: list[dict[str, str]] = [
    {
        "id": "om-as-station",
        "claim": "Open-Meteo relay reading is an in-situ weather station",
        "verdict": "dishonest",
        "correction": "Open-Meteo is a forecast/model relay — not a physical station.",
    },
    {
        "id": "om-as-relay",
        "claim": "Open-Meteo pin is a LIVE public-API relay with CC BY attribution",
        "verdict": "honest",
        "correction": "",
    },
    {
        "id": "sim-as-live",
        "claim": "ws-01 SIM campus pin is a LIVE attested field sensor",
        "verdict": "dishonest",
        "correction": "ws-01 has source=null — badge must stay SIM.",
    },
    {
        "id": "live-om",
        "claim": "om-wx-01 is LIVE because fleet.source is set",
        "verdict": "honest",
        "correction": "",
    },
    {
        "id": "public-ais-as-edge",
        "claim": "Public AIS aggregator equals own-edge feeder AIS",
        "verdict": "dishonest",
        "correction": "Public AIS ≠ feeder-ais — different custody and honesty class.",
    },
    {
        "id": "warning-as-insitu",
        "claim": "A weather warning polygon is an in-situ measurement",
        "verdict": "dishonest",
        "correction": "Warnings are alerts, not station readings.",
    },
    {
        "id": "offline-no-invent",
        "claim": "When upstream is offline, invent the last good reading",
        "verdict": "dishonest",
        "correction": "Fail offline — never invent; Hub must not debit.",
    },
    {
        "id": "fail-loud",
        "claim": "Upstream fail → offline status, no debit, no fake success",
        "verdict": "honest",
        "correction": "",
    },
]


def honesty_claims(claim_or_id: str) -> dict[str, Any]:
    """Classify an honesty claim or table id.

    Returns ``{"verdict": "honest"|"dishonest", "correction": str, "claim": str}``.
    """
    raw = (claim_or_id or "").strip()
    if not raw:
        return {
            "verdict": "dishonest",
            "correction": "empty claim",
            "claim": raw,
        }

    lower = raw.lower()
    for row in HONESTY_TABLE:
        if lower == row["id"] or lower == row["claim"].lower():
            return {
                "verdict": row["verdict"],
                "correction": row["correction"],
                "claim": row["claim"],
                "id": row["id"],
            }

    # Heuristic classifier for free-form student strings
    dishonest = (
        "in-situ station" in lower
        or "is an in-situ" in lower
        or "equals own-edge" in lower
        or "invent" in lower
        or "fake success" in lower
        or ("ws-01" in lower and "live" in lower)
        or ("warning" in lower and "in-situ" in lower)
        or ("open-meteo" in lower and "station" in lower and "not" not in lower)
    )
    if dishonest:
        return {
            "verdict": "dishonest",
            "correction": "Matches a known honesty violation pattern.",
            "claim": raw,
        }

    honest_markers = (
        "relay",
        "fail offline",
        "no debit",
        "source is set",
        "attribution",
        "sim",
    )
    if any(m in lower for m in honest_markers) and "invent" not in lower:
        return {"verdict": "honest", "correction": "", "claim": raw}

    return {
        "verdict": "dishonest",
        "correction": "Unrecognized claim — treat as fail-closed until reviewed.",
        "claim": raw,
    }


# ---------------------------------------------------------------------------
# Capstone checklist (Recipe A mental model)
# ---------------------------------------------------------------------------

ADD_SENSOR_CHECKLIST: list[dict[str, str]] = [
    {
        "step": "1",
        "title": "Licence clear",
        "detail": "Upstream must be CC0 / CC BY / OGL / NLOD / U.S. PD / Copernicus CC BY.",
    },
    {
        "step": "2",
        "title": "Kind exists",
        "detail": "Recipe A only if --kind already exists (open-meteo-weather, nws, openaq, …).",
    },
    {
        "step": "3",
        "title": "device_id + anchor",
        "detail": "Pick device_id, lat/lon place aliases — buyers never pass coordinates on invoke.",
    },
    {
        "step": "4",
        "title": "Append YAML",
        "detail": "scripts/add_gaia_atlas_sensor.py → gaia/config/extra_sensors.yaml + ATLAS mirror.",
    },
    {
        "step": "5",
        "title": "Redeploy order",
        "detail": "Redeploy GAIA → ATLAS; LIVE needs GAIA_ENABLE_LIVE=1.",
    },
    {
        "step": "6",
        "title": "Honesty badge",
        "detail": "LIVE only when fleet.source is set; SIM otherwise — never invent readings.",
    },
    {
        "step": "7",
        "title": "Verify live",
        "detail": "gaia.fleet.status@v1 count ↑; weather/nearest invoke returns attested output.",
    },
]


def add_sensor_checklist() -> list[dict[str, str]]:
    return list(ADD_SENSOR_CHECKLIST)


def network_allowed() -> bool:
    return os.environ.get("COURSE_SKIP_NETWORK", "").strip().lower() not in (
        "1",
        "true",
        "yes",
        "on",
    )


def try_live(fn, *, label: str = "live call"):
    """Run ``fn``; on SensorsError return None and print a clear offline line.

    Labs use this so CI smoke stays green offline while LIVE paths never stub success.
    Set ``COURSE_SKIP_NETWORK=1`` to skip live calls without attempting HTTP.
    """
    if not network_allowed():
        print(f"[offline] {label}: COURSE_SKIP_NETWORK=1")
        return None
    try:
        return fn()
    except SensorsError as exc:
        print(f"[offline] {label}: {exc}")
        return None
