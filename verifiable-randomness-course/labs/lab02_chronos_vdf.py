"""Lab 02 — VDF time with Chronos (Module 2).

Concept: Wesolowski VDF proves sequential work; verify without redoing it.
Run:  python labs/lab02_chronos_vdf.py
Exercise: python labs/run_exercises.py --module m2
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.randomness import vdf_eval
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")

    seed = t("labs.lab02.seed")
    out = vdf_eval(seed, difficulty=700)
    trace.log("vdf_eval", difficulty=out["difficulty"], valid=out["valid"])

    print(f"{t('ui.proof')}: pi={str(out['proof']['pi'])[:24]}… l={out['proof']['l']}")
    print(f"{t('ui.verify')}: {out['valid']}")

    # Tamper demo
    ensure = __import__("courselib.oracle_paths", fromlist=["ensure_oracle"]).ensure_oracle
    ensure("chronos")
    from chronos import vdf

    tampered = vdf.verify(out["g"], out["y"] + 1, out["difficulty"], out["proof"]["pi"], out["proof"]["l"])
    trace.log("tamper_check", valid=tampered)
    print(f"{t('labs.lab02.tampered')}: {tampered}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
