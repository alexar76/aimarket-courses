"""Lab 02 — Licence gate / commercial rail (M2).

Only CC0 / CC BY / OGL / NLOD / U.S. PD / Copernicus CC BY clear the rail.
AirNow waits on Data Exchange Guidelines assent; OpenAQ ships.

Run:  python labs/lab02_licence_gate.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.sensors import (
    LICENCE_TABLE,
    gaia_health,
    licence_fail_ids,
    licence_gate,
    licence_pass_ids,
    try_live,
)


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))
    print()

    print("Commercial licence table (embedded teaching data):")
    for row in LICENCE_TABLE:
        mark = "✓" if row["verdict"] == "pass" else "✗"
        print(f"  {mark} {row['name']:28} {row['licence']:28} {row['verdict']}")
        print(f"      {row['note']}")

    print()
    assert licence_gate("openaq")["verdict"] == "pass"
    assert licence_gate("airnow")["verdict"] == "fail"
    assert licence_gate("CC BY-NC")["verdict"] == "fail"
    assert licence_gate("U.S. PD")["verdict"] == "pass"
    print(f"{t('ui.verify')}: licence_gate pass/fail asserts — ok")
    print(f"  pass ids: {', '.join(licence_pass_ids())}")
    print(f"  fail ids: {', '.join(licence_fail_ids())}")

    health = try_live(gaia_health, label="GAIA /health")
    if health is not None:
        print(f"\nLive GAIA still reachable (devices={health.get('devices')}) — "
              "licence gate is independent of reachability.")

    print(f"\n--- {t('exercises.heading')} ---")
    print("Run: python labs/run_exercises.py --module m2")


if __name__ == "__main__":
    main()
