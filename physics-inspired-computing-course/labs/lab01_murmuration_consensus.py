"""Lab 01 — Murmuration robust consensus (Module 1).

Live call to the Murmuration oracle — median, biweight, DeGroot convergence.

Run:  python labs/lab01_murmuration_consensus.py
Exercise: python labs/run_exercises.py --module m1
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.physics import murmuration_aggregate
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    estimates = [2.01, 1.98, 2.05, 1.95, 50.0, 2.02]
    print(f"\n{t('labs.lab01.estimates')}: {estimates}")
    out = murmuration_aggregate(estimates)
    print(f"\n{t('ui.result')}:")
    print(f"  median:        {out['median']:.4f}")
    print(f"  trimmed_mean:  {out['trimmed_mean']:.4f}")
    print(f"  biweight:      {out['biweight']:.4f}")
    print(f"  converged:     {out['converged_value']:.4f} ({out['iterations']} iter)")
    trace.log("consensus", biweight=out["biweight"], outlier_resisted=True)

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
