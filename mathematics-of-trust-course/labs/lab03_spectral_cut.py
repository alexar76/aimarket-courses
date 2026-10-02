"""Lab 03 — Spectral connectivity & Fiedler cut (Module 3).

Measure how close a trust graph is to splitting using FOURIER.

Run:  python labs/lab03_spectral_cut.py
Exercise: python labs/run_exercises.py --module m3
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.trust import analyze_spectral, demo_trust_graph


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    out = analyze_spectral(demo_trust_graph())
    cut = out["spectral_cut"]
    trace.log("spectral", fiedler=out["fiedler_value"], verified=out["verified"])

    print(f"\n{t('labs.lab03.fiedler')}: λ₂={out['fiedler_value']:.6f}")
    print(f"{t('labs.lab03.cut')}: |A|={len(cut['set_a'])} |B|={len(cut['set_b'])}")
    print(f"  A: {', '.join(cut['set_a'][:5])}")
    print(f"  B: {', '.join(cut['set_b'][:5])}")
    print(f"  conductance={cut['conductance']:.4f}")
    print(f"{t('ui.verify')}: {out['verified']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
