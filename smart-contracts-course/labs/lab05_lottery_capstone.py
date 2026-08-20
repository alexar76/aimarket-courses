"""Lab 05 — Capstone: fair lottery round (Module 5).

Full round simulation with VRF + optional on-chain VDF path.
Run:  python labs/lab05_lottery_capstone.py
Exercise: python labs/run_exercises.py --module m5
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.contracts import simulate_fair_round
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    out = simulate_fair_round(onchain_vdf=True, client_seed=t("labs.lab05.client_seed"))
    trace.log("capstone", ticket=out["ticket"], vdf_path=out["vdf_path"], vector_ok=out["chronos_vector_valid"])

    print(f"{t('ui.result')}: ticket={out['ticket']} path={out['vdf_path']}")
    print(f"{t('ui.verify')}: chronos_vector={out['chronos_vector_valid']}")
    print(f"{t('labs.lab05.docs')}: {out['docs']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
