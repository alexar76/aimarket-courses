"""Lab 01 — LIVE vs SIM (M1).

A LIVE pin has fleet provenance ``source`` set (HTTPS allowlisted upstream).
A SIM pin (ws-01) has ``source=null`` — never badge it LIVE.

Run:  python labs/lab01_live_vs_sim.py
      COURSE_LANG=ru python labs/lab01_live_vs_sim.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.sensors import (
    LIVE_WEATHER_DEVICE,
    SIM_WEATHER_DEVICE,
    classify_mode,
    fleet_devices,
    gaia_health,
    gaia_weather_read,
    reading_from_invoke,
    try_live,
)


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))
    print()
    print("Rule: LIVE iff source is set. Offline upstream → fail loud, never invent.")
    print(f"Teaching pair: LIVE={LIVE_WEATHER_DEVICE}  SIM={SIM_WEATHER_DEVICE}")
    print()

    # Offline teaching assert
    assert classify_mode({"device_id": LIVE_WEATHER_DEVICE, "source": "https://open-meteo.com"}) == "LIVE"
    assert classify_mode({"device_id": SIM_WEATHER_DEVICE, "source": None}) == "SIM"
    print(f"{t('ui.verify')}: offline classify_mode LIVE/SIM — ok")

    health = try_live(gaia_health, label="GAIA /health")
    if health is not None:
        print(f"GAIA health: status={health.get('status')} devices={health.get('devices')}")

    for device_id, expect in ((LIVE_WEATHER_DEVICE, "LIVE"), (SIM_WEATHER_DEVICE, "SIM")):
        payload = try_live(lambda d=device_id: gaia_weather_read(d), label=f"weather {device_id}")
        if payload is None:
            continue
        reading = reading_from_invoke(payload)
        values = reading.get("values") or {}
        print(
            f"{t('ui.result')}: {device_id} temp_c={values.get('temperature_c')} "
            f"model={reading.get('model')}"
        )
        # Prefer fleet source when available
        devices = try_live(fleet_devices, label="fleet.status")
        mode = expect
        if devices:
            match = next((d for d in devices if d.get("device_id") == device_id), None)
            if match:
                mode = classify_mode(match)
                print(f"  fleet.source={match.get('source')!r} → mode={mode}")
        assert mode == expect, (device_id, mode, expect)
        print(f"  {t('ui.success')}: badge {mode}")

    print(f"\n--- {t('exercises.heading')} ---")
    print("Run: python labs/run_exercises.py --module m1")


if __name__ == "__main__":
    main()
