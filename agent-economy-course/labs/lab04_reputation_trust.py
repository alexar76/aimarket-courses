"""Lab 04 - Reputation & trust (Module 4).

Signed receipts make paid agent calls verifiable. Verify receipts, tamper
demos, and feed a trust graph hook — same pattern as LUMEN-style reputation.

Run:  python labs/lab04_reputation_trust.py   (COURSE_LANG=ru|es to localize)
Needs: pip install -e ".[hub-lite]"
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.hub_lite import embedded_hub_lite
from courselib.i18n import get_translator
from courselib.orchestration import Trace
from courselib.trust import TrustGraph, tamper_receipt


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m4.title')} ==")

    trace = Trace()
    graph = TrustGraph()

    with embedded_hub_lite() as hub:
        print(f"{t('ui.hub')}:", hub.well_known().get("name"))

        out = hub.invoke("prod-translate", "translate.multi@v2", {"text": t("labs.lab04.sample")})
        receipt = out.get("receipt") or {}
        product_id = receipt.get("product_id", "prod-translate")
        trace.emit("invoke", capability="translate.multi@v2", price_usd=out.get("price_usd"))
        print(f"{t('ui.success')}   :", out.get("success"))
        print(f"{t('ui.receipt')}   : nonce={receipt.get('nonce', 'n/a')[:8]}…")

        ok = hub.verify_receipt(receipt)
        score = graph.record(product_id, out.get("price_usd", 0), verified=ok)
        hub.record_trust(product_id, verified=ok)
        trace.emit("verify", tampered=False, valid=ok, trust_score=score)
        print(f"{t('labs.lab04.verify_ok')} :", ok)
        print(f"{t('ui.score')}       : {score:.2f}")

        bad = tamper_receipt(receipt, price_usd=0.0)
        bad_ok = hub.verify_receipt(bad)
        bad_score = graph.record(product_id, 0.0, verified=bad_ok)
        hub.record_trust(product_id, verified=bad_ok)
        trace.emit("verify", tampered=True, valid=bad_ok, trust_score=bad_score)
        print(f"{t('labs.lab04.verify_bad')}:", bad_ok)
        print(f"{t('labs.lab04.trust_graph')}:", hub.trust_graph())

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e["kind"], {k: v for k, v in e.items() if k not in ("t", "kind")})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
