"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py.

Reference solutions (CI / instructors): courselib/exercise_solutions.py
"""

from __future__ import annotations

from courselib.sensors import (
    LIVE_WEATHER_DEVICE,
    SIM_WEATHER_DEVICE,
    add_sensor_checklist,
    classify_mode,
    honesty_claims,
    licence_gate,
)

MODULES = ("m1", "m2", "m3", "m4", "m5")


def exercise_m1_live_vs_sim() -> None:
    """Classify LIVE om-wx-01 vs SIM ws-01 from fleet-shaped dicts."""
    # YOUR CODE HERE — build two device dicts and assert classify_mode:
    #   {"device_id": "om-wx-01", "source": "https://open-meteo.com"} → "LIVE"
    #   {"device_id": "ws-01", "source": None} → "SIM"
    raise NotImplementedError("exercise_m1_live_vs_sim: implement this exercise")


def exercise_m2_licence_gate() -> None:
    """Commercial rail: OpenAQ passes; AirNow / BY-NC fail."""
    # YOUR CODE HERE — assert licence_gate("openaq")["verdict"] == "pass"
    #   and licence_gate("airnow")["verdict"] == "fail"
    #   and licence_gate("CC BY-NC")["verdict"] == "fail"
    raise NotImplementedError("exercise_m2_licence_gate: implement this exercise")


def exercise_m3_honesty_claims() -> None:
    """Open-Meteo-as-station is dishonest; fail-loud policy is honest."""
    # YOUR CODE HERE — assert honesty_claims("om-as-station")["verdict"] == "dishonest"
    #   and honesty_claims("fail-loud")["verdict"] == "honest"
    raise NotImplementedError("exercise_m3_honesty_claims: implement this exercise")


def exercise_m4_atlas_nearest_shape() -> None:
    """Offline shape check: nearest payload must expose distance_km + nearest.id."""
    # YOUR CODE HERE — given a sample ATLAS-shaped dict, assert required keys exist
    #   sample = {"ok": True, "distance_km": 12.5, "nearest": {"id": "om-wx-01", "mode": "LIVE"}}
    raise NotImplementedError("exercise_m4_atlas_nearest_shape: implement this exercise")


def exercise_m5_add_sensor_checklist() -> None:
    """Capstone checklist must include licence + redeploy + honesty steps."""
    # YOUR CODE HERE — titles = {s["title"].lower() for s in add_sensor_checklist()}
    #   assert any("licence" in t for t in titles)
    #   assert any("redeploy" in t for t in titles)
    #   assert any("honesty" in t for t in titles)
    raise NotImplementedError("exercise_m5_add_sensor_checklist: implement this exercise")


EXERCISES = {
    "m1": exercise_m1_live_vs_sim,
    "m2": exercise_m2_licence_gate,
    "m3": exercise_m3_honesty_claims,
    "m4": exercise_m4_atlas_nearest_shape,
    "m5": exercise_m5_add_sensor_checklist,
}


def run_all() -> dict[str, str]:
    out: dict[str, str] = {}
    for mod, fn in EXERCISES.items():
        try:
            fn()
            out[mod] = "ok"
        except Exception as exc:
            out[mod] = f"fail: {exc}"
    return out


def all_passed(results: dict[str, str] | None = None) -> bool:
    results = results if results is not None else run_all()
    return all(v == "ok" for v in results.values())


# Re-export helpers so student notebooks can `from courselib.exercises import …`
__all__ = [
    "MODULES",
    "EXERCISES",
    "run_all",
    "all_passed",
    "LIVE_WEATHER_DEVICE",
    "SIM_WEATHER_DEVICE",
    "classify_mode",
    "licence_gate",
    "honesty_claims",
    "add_sensor_checklist",
]
