"""Lab 05 — Proof portfolio capstone (Module 5).

Chain COLONY, KANTOR, FERMAT, and GAUSS certificates in one audit.

Run:  python labs/lab05_proof_capstone.py
Exercise: python labs/run_exercises.py --module m5
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.optimization import proof_portfolio
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    out = proof_portfolio()
    for name, ok in out["flags"].items():
        trace.log("certificate", name=name, ok=ok)
        status = t("ui.success") if ok else t("ui.blocked")
        print(f"  {name}: {status}")

    print(f"\n{t('labs.lab05.summary')}: all_verified={out['all_verified']}")
    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
