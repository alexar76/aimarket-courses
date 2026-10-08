"""Lab 04 — ATLAS operator map read (M4).

Call atlas.nearest.read@v1 near Berlin (default Open-Meteo anchor).
Inspect distance_km, nearest pin mode/source, and station counts from /health.

Run:  python labs/lab04_atlas_map_read.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.sensors import (
    atlas_health,
    atlas_nearest,
    classify_mode,
    try_live,
)


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))
    print()

    # Offline shape contract students will implement in m4 exercise
    sample = {
        "ok": True,
        "distance_km": 0.0,
        "nearest": {"id": "om-wx-01", "mode": "LIVE", "source": "https://open-meteo.com"},
    }
    assert sample["ok"] and "id" in sample["nearest"]
    print(f"{t('ui.verify')}: offline ATLAS payload shape — ok")

    health = try_live(atlas_health, label="ATLAS /health")
    if health is not None:
        print(
            f"ATLAS health: status={health.get('status')} "
            f"stations={health.get('stations')} cached={health.get('cached_readings')}"
        )

    lat, lon = 52.52, 13.41
    print(f"\nInvoking atlas.nearest.read@v1 at lat={lat} lon={lon} …")
    payload = try_live(lambda: atlas_nearest(lat, lon, layers=["weather"]), label="atlas.nearest")
    if payload is not None:
        nearest = payload.get("nearest") or {}
        print(f"{t('ui.result')}:")
        print(f"  distance_km={payload.get('distance_km')}")
        print(f"  layer={payload.get('layer')}")
        print(f"  nearest.id={nearest.get('id')} place={nearest.get('place')}")
        print(f"  nearest.mode={nearest.get('mode')} live={nearest.get('live')}")
        print(f"  nearest.source={nearest.get('source')!r}")
        if nearest:
            print(f"  classify_mode → {classify_mode(nearest)}")
        values = payload.get("values") or {}
        if values:
            print(f"  values.temperature_c={values.get('temperature_c')}")

    print(f"\n--- {t('exercises.heading')} ---")
    print("Run: python labs/run_exercises.py --module m4")


if __name__ == "__main__":
    main()
