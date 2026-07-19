"""Lab 02 — Optimal transport with dual certificate (Module 2).

Move mass between distributions with KANTOR and verify the dual.

Run:  python labs/lab02_kantor_transport.py
Exercise: python labs/run_exercises.py --module m2
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.optimization import solve_transport
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))

    out = solve_transport()
    tr = out["transport"]
    trace.log("transport", cost=out["cost"], w=out.get("wasserstein"), verified=out["verified"])

    print(f"\n{t('labs.lab02.cost')}: {out['cost']:.6f}")
    if out.get("wasserstein") is not None:
        print(f"  W₂ distance: {out['wasserstein']:.6f}")
    print(f"  dual obj:    {tr['dual_objective']:.6f}")
    print(f"  method:      {tr['method']}")
    print(f"{t('ui.verify')}: {out['verified']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
