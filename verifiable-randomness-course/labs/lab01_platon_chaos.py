"""Lab 01 — Chaos VRF with Platon (Module 1).

Concept: verifiable randomness from a signed chaos-oracle draw.
Run:  python labs/lab01_platon_chaos.py
Exercise: python labs/run_exercises.py --module m1
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.randomness import chaos_draw
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    seed = t("labs.lab01.client_seed")
    out = chaos_draw(seed)
    trace.log("chaos_draw", verified=out["verified"], bytes=len(out["draw"]["random_hex"]) // 2)

    print(f"{t('ui.proof')}: scheme={out['draw']['proof']['scheme']}")
    print(f"{t('ui.result')}: {out['draw']['random_hex'][:32]}…")
    print(f"{t('ui.verify')}: {out['verified']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
