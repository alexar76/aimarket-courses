"""Lab 08 - The economics of orchestration (Module 8, advanced track).

Full autonomous cycle via the real aimarket-agent SDK: discover → channel →
invoke → escrow → receipt → settle. Heavier deps than hub-lite labs — install
once per Colab session and reuse for lab04/07 if already installed.

Run:  python labs/lab08_metered_economy.py   (COURSE_LANG=ru|es to localize)
Needs: pip install -e ".[sandbox]"   (~50 MB, git clones — run once)
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.economy import embedded_sandbox
from courselib.i18n import get_translator
from courselib.orchestration import Trace


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m8.title')} ==")

    with embedded_sandbox(budget=3.0) as econ:
        # The discovery *intent* stays in English so it matches the demo hub's
        # (English) capability catalog; only display text is localized. Searching
        # a real federated hub in any language is itself a later lab.
        res = econ.hire("translate text to multiple languages")
        bom = res.get("bill_of_materials")
        if not bom:
            print(res.get("note") or res.get("error") or "no capabilities matched")
            return

        trace = Trace()
        trace.emit("hire", task=res["task"], ok=res["ok"],
                   channel=bom["channel_id"] or None, spent_usd=res["total_spent_usd"])

        print(f"{t('ui.task')}        :", res["task"])
        print(f"{t('ui.success')}     :", res["ok"])
        print(f"{t('ui.channel')}     :", bom["channel_id"] or t("ui.none"))
        print(f"{t('ui.total_spent')} :", f"${res['total_spent_usd']}")
        print(f"{t('ui.protocol')}    :", bom["protocol_version"])

        print(f"\n{t('ui.steps')}:")
        for step in bom["results"]:
            # capability_id lives in the signed receipt; the sandbox factory
            # nests it under result.output.capability. Try both before falling back.
            cid = (
                (step.get("receipt") or {}).get("capability_id")
                or step.get("capability_id")
                or step.get("result", {}).get("output", {}).get("capability")
                or t("ui.none")
            )
            trace.emit("step", capability=cid, success=step.get("success"),
                       price_usd=step.get("price_usd"))
            print(f"  {t('ui.success')}={step.get('success')}  "
                  f"{t('ui.price')}=${step.get('price_usd')}  {cid}")

        cap = econ.capital_listings()
        listings = cap.get("listings", [])
        trace.emit("capital", listings=len(listings))
        print(f"\n{t('ui.acex_listings')}: {len(listings)}")

        # M9 observability: the full economic cycle is inspectable.
        print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
        for e in trace.events:
            print(" ", e["kind"], {k: v for k, v in e.items() if k not in ("t", "kind")})


if __name__ == "__main__":
    main()
