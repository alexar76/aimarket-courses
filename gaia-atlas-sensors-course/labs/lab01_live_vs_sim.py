"""Lab 01 — LIVE vs SIM (M1).

A LIVE pin has fleet provenance ``source`` set (HTTPS allowlisted upstream).
A SIM pin (ws-01) has ``source=null`` — never badge it LIVE.

Where the readings come from: ``gaia.fleet.status@v1`` is free, so it is read from
GAIA directly. ``gaia.weather.read@v1`` costs $0.001 a call, and GAIA sells it only
through the hub (https://modelmarket.dev): with its price gate on, a direct call gets
402 and the hub's name. This lab buys it on the hub's free sandbox trial instead: no
wallet, no account, 5 calls per visitor id per hour. Each run reads two devices, so
it spends 2 of the 5; a sixth call in the hour gets 429 ``trial_quota_exhausted`` and
costs nothing, and the allowance comes back the next hour. Your visitor id is a
random one kept in ``~/.config/gaia-atlas-sensors-course/sandbox-visitor``. Point
``COURSE_HUB_URL`` at another hub if you use one.

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
    hub_base_url,
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
    print(
        f"Weather reads are priced, so they go through the hub's free trial at {hub_base_url()} "
        "(5 calls an hour; this lab spends 2)."
    )
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
        trial = payload.get("sandbox") or {}
        if isinstance(trial, dict) and "remaining" in trial:
            print(f"  hub trial: {trial['remaining']} of {trial.get('max_trials')} calls left this hour")
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
