"""Lab 02 — VDF verify on-chain (Module 2).

Verify Foundry vector from lottery/contracts/test/vectors/chronos_vector.json.
Run:  python labs/lab02_vdf_verify.py
Exercise: python labs/run_exercises.py --module m2
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.contracts import load_chronos_vector, verify_wesolowski_vector
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))

    vec = load_chronos_vector()
    ok = verify_wesolowski_vector(vec)
    trace.log("vdf_verify", seed=vec["seed"], T=vec["T"], valid=ok)
    print(f"{t('ui.proof')}: scheme=wesolowski-vdf seed={vec['seed']!r}")
    print(f"{t('ui.verify')}: {ok} (AB_equals_y={vec.get('AB_equals_y')})")
    print(t("labs.lab02.foundry_note"))

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
