"""Lab 04 — Relayer round lifecycle (Module 4).

baseSeed → Sortes draw → optional Chronos VDF beacon.
Run:  python labs/lab04_relayer_round.py
Exercise: python labs/run_exercises.py --module m4
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.contracts import RelayerRound, load_chronos_vector, verify_wesolowski_vector
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    rnd = RelayerRound(
        round_id=42,
        blockhash=bytes.fromhex("ab" * 32),
        platon_random=bytes.fromhex("cd" * 32),
        onchain_vdf=True,
    )
    seed = rnd.chronos_seed()
    ticket, vrf = rnd.draw_ticket(t("labs.lab04.client_seed"))
    vdf = rnd.vdf_beacon()
    vec_ok = verify_wesolowski_vector(load_chronos_vector())

    trace.log("base_seed", seed=seed[:18] + "…")
    trace.log("sortes_draw", ticket=ticket, verified=vrf.get("verified"))
    trace.log("vdf_beacon", nonempty=bool(vdf and vdf.pi), vector_ok=vec_ok)

    print(f"{t('labs.lab04.seed')}: {seed[:20]}…")
    print(f"{t('labs.lab04.ticket')}: {ticket} verified={vrf.get('verified')}")
    print(f"{t('labs.lab04.vdf')}: vector_valid={vec_ok}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
