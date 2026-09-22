"""Reference solutions (CI / instructors)."""

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
    live = {"device_id": LIVE_WEATHER_DEVICE, "source": "https://open-meteo.com (CC BY 4.0)"}
    sim = {"device_id": SIM_WEATHER_DEVICE, "source": None}
    assert classify_mode(live) == "LIVE"
    assert classify_mode(sim) == "SIM"


def exercise_m2_licence_gate() -> None:
    assert licence_gate("openaq")["verdict"] == "pass"
    assert licence_gate("airnow")["verdict"] == "fail"
    assert licence_gate("CC BY-NC")["verdict"] == "fail"
    assert licence_gate("U.S. PD")["verdict"] == "pass"


def exercise_m3_honesty_claims() -> None:
    assert honesty_claims("om-as-station")["verdict"] == "dishonest"
    assert honesty_claims("fail-loud")["verdict"] == "honest"
    assert honesty_claims("sim-as-live")["verdict"] == "dishonest"


def exercise_m4_atlas_nearest_shape() -> None:
    sample = {
        "ok": True,
        "distance_km": 12.5,
        "nearest": {"id": "om-wx-01", "mode": "LIVE", "source": "https://open-meteo.com"},
    }
    assert sample["ok"] is True
    assert isinstance(sample["distance_km"], (int, float))
    assert "id" in sample["nearest"]
    assert classify_mode(sample["nearest"]) == "LIVE"


def exercise_m5_add_sensor_checklist() -> None:
    steps = add_sensor_checklist()
    assert len(steps) >= 5
    titles = {s["title"].lower() for s in steps}
    assert any("licence" in t for t in titles)
    assert any("redeploy" in t for t in titles)
    assert any("honesty" in t for t in titles)


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
