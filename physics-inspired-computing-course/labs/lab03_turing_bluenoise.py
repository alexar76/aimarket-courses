"""Lab 03 — Turing blue-noise sampling (Module 3).

Mitchell best-candidate points with maximal minimum distance.

Run:  python labs/lab03_turing_bluenoise.py
Exercise: python labs/run_exercises.py --module m3
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.physics import turing_bluenoise
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    out = turing_bluenoise(count=64, candidates=12, seed=2026)
    print(f"\n{t('ui.result')}:")
    print(f"  count:         {out['count']}")
    print(f"  min_distance:  {out['min_distance']:.6f}")
    print(f"  seed:          {out['seed']} ({out['seed_source']})")
    print(f"  sample:        {out['points'][:3]} …")
    trace.log("bluenoise", count=out["count"], min_distance=out["min_distance"])

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
