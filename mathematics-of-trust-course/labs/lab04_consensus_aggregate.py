"""Lab 04 — Robust consensus aggregation (Module 4).

Aggregate agent estimates with MURMURATION — median beats outliers.

Run:  python labs/lab04_consensus_aggregate.py
Exercise: python labs/run_exercises.py --module m4
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.trust import aggregate_consensus, demo_agent_estimates


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    values = demo_agent_estimates()
    out = aggregate_consensus(values)
    trace.log("consensus", median=out["median"], biweight=out["biweight"])

    print(f"\n{t('labs.lab04.values')}: {values}")
    print(f"  mean (naive):     {sum(values)/len(values):.2f}")
    print(f"  median:           {out['median']:.2f}")
    print(f"  trimmed mean:     {out['trimmed_mean']:.2f}")
    print(f"  biweight:         {out['biweight']:.2f}")
    print(f"  DeGroot converge: {out['converged_value']:.2f} ({out['iterations']} iters)")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
