"""Lab 04 — Ablation cascade risk (Module 4).

Abelian sandpile SOC — power-law avalanche exponent tau and tail risk.

Run:  python labs/lab04_ablation_cascade.py
Exercise: python labs/run_exercises.py --module m4
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.physics import ablation_cascade, demo_exposure_graph
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    edges = demo_exposure_graph()
    print(f"\n{t('labs.lab04.edges')}: {len(edges)}")
    out = ablation_cascade(edges, grains=1200, nonce="lab04")
    print(f"\n{t('ui.result')}:")
    print(f"  tau:            {out['tau']:.4f}")
    print(f"  max_avalanche:  {out['max_avalanche']}")
    print(f"  cvar95:         {out['cvar95']:.2f}")
    print(f"  topple_total:   {out['topple_total']}")
    trace.log("cascade", tau=out["tau"], max_avalanche=out["max_avalanche"])

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
