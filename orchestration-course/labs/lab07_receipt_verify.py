"""Lab 07 - Trust, verification & provenance (Module 7).

Signed receipts make paid agent calls verifiable. This lab uses hub-lite
(fast Colab install) and stdlib HMAC verification — same pattern as production.

Run:  python labs/lab07_receipt_verify.py   (COURSE_LANG=ru|es to localize)
Needs: pip install -e ".[hub-lite]"   (~5 MB, no git clones)
Exercise: python labs/run_exercises.py --module m7
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.hub_lite import embedded_hub_lite
from courselib.i18n import get_translator
from courselib.orchestration import Trace
from courselib.trust import tamper_receipt


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m7.title')} ==")

    trace = Trace()

    with embedded_hub_lite() as hub:
        print(f"{t('ui.hub')}:", hub.well_known().get("name"))

        out = hub.invoke("prod-translate", "translate.multi@v2", {"text": t("labs.lab07.sample")})
        receipt = out.get("receipt") or {}
        trace.emit("invoke", capability="translate.multi@v2", price_usd=out.get("price_usd"))
        print(f"{t('ui.success')}   :", out.get("success"))
        print(f"{t('ui.price')}     :", out.get("price_usd"))
        print(f"{t('ui.receipt')}   : nonce={receipt.get('nonce', 'n/a')[:8]}…")

        ok = hub.verify_receipt(receipt)
        trace.emit("verify", tampered=False, valid=ok)
        print(f"{t('labs.lab07.verify_ok')} :", ok)

        bad = tamper_receipt(receipt, price_usd=0.0)
        bad_ok = hub.verify_receipt(bad)
        trace.emit("verify", tampered=True, valid=bad_ok)
        print(f"{t('labs.lab07.verify_bad')}:", bad_ok)

    # M9 observability: every verification decision is logged, not hidden.
    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e["kind"], {k: v for k, v in e.items() if k not in ("t", "kind")})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab07_hint"))


if __name__ == "__main__":
    main()
