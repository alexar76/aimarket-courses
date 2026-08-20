"""Lab 04 — GP posterior & Expected Improvement (Module 4).

Fit a Gaussian process with GAUSS and verify the posterior field.

Run:  python labs/lab04_gauss_gp.py
Exercise: python labs/run_exercises.py --module m4
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.optimization import gp_posterior
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    out = gp_posterior()
    sug = out["suggest"]
    trace.log("gp", verified=out["verified"], suggest=sug.get("best"))

    print(f"\n{t('labs.lab04.posterior')}:")
    for i, (mu, sig) in enumerate(zip(out["mean"], out["std"])):
        print(f"  q[{i}]: μ={mu:.4f}  σ={sig:.4f}")
    print(f"\n{t('labs.lab04.suggest')}: x={sug['best']}  EI={sug['ei']:.4f}")
    print(f"{t('ui.verify')}: {out['verified']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
