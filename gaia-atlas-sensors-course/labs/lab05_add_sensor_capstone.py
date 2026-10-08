"""Lab 05 — Capstone: add a sensor checklist (M5).

Walk Recipe A conceptually (licence → kind → YAML → redeploy → honesty),
then read the live fleet device count from GAIA.

Docs: docs/add-gaia-atlas-sensor.md · gaia/docs/LIVE-RELAYS.md

Run:  python labs/lab05_add_sensor_capstone.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.sensors import (
    add_sensor_checklist,
    fleet_devices,
    gaia_health,
    licence_gate,
    try_live,
)


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))
    print()

    print("Recipe A — add-sensor checklist:")
    for step in add_sensor_checklist():
        print(f"  {step['step']}. {step['title']}")
        print(f"     {step['detail']}")

    titles = {s["title"].lower() for s in add_sensor_checklist()}
    assert any("licence" in x for x in titles)
    assert any("redeploy" in x for x in titles)
    assert any("honesty" in x for x in titles)
    # Capstone also re-checks the rail gate students must not skip
    assert licence_gate("openaq")["verdict"] == "pass"
    assert licence_gate("opensky")["verdict"] == "fail"
    print(f"\n{t('ui.verify')}: checklist + licence gate — ok")

    health = try_live(gaia_health, label="GAIA /health")
    devices = try_live(fleet_devices, label="gaia.fleet.status@v1")
    if health is not None:
        print(f"\nLive fleet (health.devices) = {health.get('devices')}")
    if devices is not None:
        live_n = sum(1 for d in devices if d.get("source"))
        sim_n = len(devices) - live_n
        print(f"Fleet status count = {len(devices)} (source-set LIVE≈{live_n}, SIM≈{sim_n})")
        print("After adding a sensor: expect health.devices and fleet count to increase by 1.")

    print(f"\n--- {t('exercises.heading')} ---")
    print("Run: python labs/run_exercises.py --module m5")


if __name__ == "__main__":
    main()
