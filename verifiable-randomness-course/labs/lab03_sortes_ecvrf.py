"""Lab 03 — ECVRF offline verify with Sortes (Module 3).

Concept: 80-byte RFC 9381 proof; verify beta without calling the oracle again.
Run:  python labs/lab03_sortes_ecvrf.py
Exercise: python labs/run_exercises.py --module m3
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.randomness import ecvrf_draw
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")

    alpha = t("labs.lab03.alpha").encode()
    out = ecvrf_draw(alpha)
    trace.log("ecvrf", proof_len=out["proof_len"], verified=out["verified"])

    print(f"{t('ui.proof')}: {out['proof_len']} bytes = {out['proof_hex'][:40]}…")
    print(f"{t('ui.result')}: beta={out['beta_hex'][:32]}…")
    print(f"{t('ui.verify')}: {out['verified']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
