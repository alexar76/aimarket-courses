"""Lab 06 — On-chain verification & lottery consumer (Module 6).

Concept: VDF vector for Base testnet; lottery word from Sortes ECVRF.
Run:  python labs/lab06_onchain_consumer.py
Exercise: python labs/run_exercises.py --module m6
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.randomness import lottery_word_from_vrf, onchain_vdf_vector
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m6.title')} ==")

    vec = onchain_vdf_vector()
    trace.log("onchain_vdf", valid=vec["valid"])

    round_seed = t("labs.lab06.round")
    word = lottery_word_from_vrf(round_seed)
    trace.log("lottery_word", hex=word.hex()[:32])

    print(f"{t('ui.protocol')}: {vec['scheme']}")
    print(f"{t('ui.verify')}: {vec['valid']}")
    print(f"{t('labs.lab06.word')}: 0x{word.hex()[:32]}…")
    print(t("labs.lab06.deploy_note"))

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab06_hint"))


if __name__ == "__main__":
    main()
