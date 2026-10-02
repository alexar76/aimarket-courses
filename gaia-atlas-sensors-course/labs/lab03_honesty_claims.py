"""Lab 03 — Fleet & pin honesty (M3).

Open-Meteo ≠ in-situ station; public AIS ≠ own-edge; warning ≠ in-situ.
SIM devices must never be claimed LIVE.

Run:  python labs/lab03_honesty_claims.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.sensors import (
    HONESTY_TABLE,
    LIVE_WEATHER_DEVICE,
    SIM_WEATHER_DEVICE,
    classify_mode,
    fleet_devices,
    honesty_claims,
    try_live,
)


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))
    print()

    print("Honesty claims (teaching table):")
    for row in HONESTY_TABLE:
        mark = "✓" if row["verdict"] == "honest" else "✗"
        print(f"  {mark} [{row['verdict']}] {row['claim']}")
        if row["correction"]:
            print(f"      → {row['correction']}")

    assert honesty_claims("om-as-station")["verdict"] == "dishonest"
    assert honesty_claims("fail-loud")["verdict"] == "honest"
    assert honesty_claims("public-ais-as-edge")["verdict"] == "dishonest"
    print(f"\n{t('ui.verify')}: honesty_claims classifier — ok")

    devices = try_live(fleet_devices, label="gaia.fleet.status@v1")
    if devices is not None:
        by_id = {d.get("device_id"): d for d in devices}
        for device_id in (LIVE_WEATHER_DEVICE, SIM_WEATHER_DEVICE):
            d = by_id.get(device_id)
            if not d:
                print(f"  (fleet missing {device_id})")
                continue
            mode = classify_mode(d)
            print(f"  {device_id}: mode={mode} source={d.get('source')!r}")
            if device_id == SIM_WEATHER_DEVICE:
                assert mode == "SIM"
            if device_id == LIVE_WEATHER_DEVICE:
                assert mode == "LIVE"

    print(f"\n--- {t('exercises.heading')} ---")
    print("Run: python labs/run_exercises.py --module m3")


if __name__ == "__main__":
    main()
