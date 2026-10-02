"""Lab 05 — Landauer thermodynamic audit (Module 5).

Bit-erasure energy floor kT·ln2 over an operation DAG.

Run:  python labs/lab05_landauer_audit.py
Exercise: python labs/run_exercises.py --module m5
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.physics import demo_circuit_ops, landauer_audit
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    ops = demo_circuit_ops()
    print(f"\n{t('labs.lab05.ops')}: {len(ops)}")
    out = landauer_audit(ops, temperature_k=300.0)
    print(f"\n{t('ui.result')}:")
    print(f"  irreversible_bits: {out['irreversible_bits']}")
    print(f"  energy_floor_j:    {out['energy_floor_j']:.3e} J")
    print(f"  efficiency:        {out['efficiency']:.2%}")
    print(f"  commitment:        {out['circuit_commitment'][:16]}…")
    trace.log("landauer", bits=out["irreversible_bits"], floor_j=out["energy_floor_j"])

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
