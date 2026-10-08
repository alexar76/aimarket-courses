"""Lab 05 — Commit–reveal & bias attacks (Module 5).

Concept: build a biased lottery the operator can grind; break it with ECVRF.
Run:  python labs/lab05_commit_reveal.py
Exercise: python labs/run_exercises.py --module m5
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.randomness import BiasedLottery, FairLottery
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")

    player = t("labs.lab05.player_seed")
    biased = BiasedLottery()
    fair = FairLottery()

    commit_hash = biased.commit(player)
    trace.log("commit", hash=commit_hash[:16])

    b_ticket = biased.draw(player)
    f_ticket, proof = fair.draw(player)
    trace.log("draw", biased=b_ticket, fair=f_ticket, vrf_ok=proof["verified"])

    print(f"{t('labs.lab05.biased_ticket')}: {b_ticket}")
    print(f"{t('labs.lab05.fair_ticket')}: {f_ticket}")
    print(f"{t('ui.verify')} VRF: {proof['verified']}")
    print(t("labs.lab05.audit_note"))

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
