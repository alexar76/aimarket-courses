"""Lab 01 — Unbiasable lottery draw (Module 1).

Compare biased operator grinding vs fair ECVRF draw.
Run:  python labs/lab01_unbiasable_draw.py
Exercise: python labs/run_exercises.py --module m1
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.contracts import BiasedLottery, FairLottery
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))

    player = t("labs.lab01.player_seed")
    biased = BiasedLottery()
    grind = biased.operator_can_grind(player)
    trace.log("biased_draw", grindable=grind, ticket=biased.draw(player))
    print(f"{t('labs.lab01.biased_label')}: grindable={grind}, ticket={biased.draw(player)}")

    fair = FairLottery()
    commit = fair.commit(player)
    ticket, proof = fair.draw(player)
    trace.log("fair_draw", commit=commit[:16], ticket=ticket, verified=proof.get("verified"))
    print(f"{t('labs.lab01.fair_label')}: ticket={ticket}, verified={proof.get('verified')}")
    print(t("labs.lab01.docs_note"))

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
