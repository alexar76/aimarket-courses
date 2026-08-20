"""Lab 03 — Least-time routing with eikonal dual (Module 3).

Find the fastest agent composition path with FERMAT and verify potentials.

Run:  python labs/lab03_fermat_route.py
Exercise: python labs/run_exercises.py --module m3
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.optimization import route_least_time
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    out = route_least_time()
    trace.log("route", total=out["total"], verified=out["verified"])

    print(f"\n{t('labs.lab03.path')}: {' → '.join(out['path'] or [])}")
    print(f"  total cost: {out['total']}")
    print(f"{t('ui.verify')}: {out['verified']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
