"""Lab 02 — Colony TSP certificate (Module 2).

Nearest-neighbour + 2-opt with admissible optimality gap.

Run:  python labs/lab02_colony_tsp.py
Exercise: python labs/run_exercises.py --module m2
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.physics import colony_tsp
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))

    cities = [[0, 0], [3, 1], [4, 4], [1, 5], [0, 3], [2, 2]]
    print(f"\n{t('labs.lab02.cities')}: {len(cities)}")
    out = colony_tsp(cities)
    print(f"\n{t('ui.result')}:")
    print(f"  tour:         {out['tour']}")
    print(f"  length:       {out['length']:.4f}")
    print(f"  lower_bound:  {out['lower_bound']:.4f}")
    print(f"  gap:          {out['gap']:.2%}")
    trace.log("tsp", length=out["length"], gap=round(out["gap"], 4))

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
