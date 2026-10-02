"""Lab 01 — TSP with quality gap (Module 1).

Solve a small TSP with COLONY and inspect the optimality certificate.

Run:  python labs/lab01_colony_tsp.py
Exercise: python labs/run_exercises.py --module m1
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.optimization import solve_tsp
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    out = solve_tsp()
    trace.log("tsp", length=out["length"], gap=out["gap"], verified=out["certificate_valid"])

    print(f"\n{t('labs.lab01.tour')}: {out['tour']}")
    print(f"  length:       {out['length']:.4f}")
    print(f"  lower bound:  {out['lower_bound']:.4f}")
    print(f"  gap:          {out['gap']*100:.2f}%")
    print(f"  nn baseline:  {out['nn_length']:.4f}")
    print(f"{t('ui.verify')}: certificate_valid={out['certificate_valid']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
