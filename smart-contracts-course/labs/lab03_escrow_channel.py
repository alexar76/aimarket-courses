"""Lab 03 — Escrow & payment channels (Module 3).

Receipt-gated debit modelled on AIMarketEscrow.
Run:  python labs/lab03_escrow_channel.py
Exercise: python labs/run_exercises.py --module m3
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.contracts import EscrowChannel
from courselib.i18n import get_translator
from courselib.trace import Trace


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    ch = EscrowChannel("ch-lab03", t("labs.lab03.depositor"))
    ch.open(1000)
    trace.log("open", balance=ch.balance)

    ch.debit(250, "rcpt-001", "hub-course", signature_valid=True)
    trace.log("debit", amount=250, balance=ch.balance, nonce=ch.nonce)

    try:
        ch.debit(250, "rcpt-001", "hub-course", signature_valid=True)
        replay_ok = True
    except ValueError as exc:
        replay_ok = False
        trace.log("replay_blocked", error=str(exc))
    print(f"{t('labs.lab03.replay')}: blocked={not replay_ok}")

    settled = ch.settle()
    trace.log("settle", **settled)
    print(f"{t('ui.result')}: hub={settled['to_hub']} refund={settled['refund']}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event)

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
