"""Lab 05 — Sandpile cascade risk (Module 5).

Measure avalanche tail risk on an exposure graph with ABLATION.

Run:  python labs/lab05_sandpile_cascade.py
Exercise: python labs/run_exercises.py --module m5
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.trust import analyze_cascade, demo_exposure_graph


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    out = analyze_cascade(demo_exposure_graph(), grains=600, nonce="lab05")
    cascade = out["cascade"]
    trace.log("cascade", tau=out["tau"], max_av=out["max_avalanche"], verified=out["verified"])

    print(f"\n{t('labs.lab05.stats')}:")
    print(f"  τ (power-law):   {out['tau']:.4f}")
    print(f"  max avalanche: {out['max_avalanche']}")
    print(f"  CVaR 99%:      {out['cvar99']:.2f}")
    if out["triggers"]:
        top = out["triggers"][0]
        print(f"  top trigger:   {top['node']} ({top['big_cascades']} big cascades)")
    print(f"{t('ui.verify')}: {out['verified']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
