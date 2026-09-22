"""Lab 04 — Time-lock RSW with Aestus (Module 4).

Concept: seal a bid now; anyone can open after provable sequential work.
Run:  python labs/lab04_aestus_timelock.py
Exercise: python labs/run_exercises.py --module m4
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.randomness import timelock_seal
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")

    secret = t("labs.lab04.secret")
    out = timelock_seal(secret, T=350)
    trace.log("timelock", T=out["puzzle"]["T"], opened=out["message_match"])

    print(f"{t('ui.proof')}: T={out['puzzle']['T']} squarings")
    print(f"{t('ui.result')}: {out['opened'].get('data', '')[:40]}")
    print(f"{t('ui.verify')}: {out['message_match']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
