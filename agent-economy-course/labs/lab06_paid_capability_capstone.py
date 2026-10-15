"""Lab 06 - Capstone: paid agent loop (Module 6, advanced track).

Full autonomous cycle via the real aimarket-agent SDK: discover → channel →
invoke → escrow → receipt → settle. Heavier deps than hub-lite labs.

Run:  python labs/lab06_paid_capability_capstone.py   (COURSE_LANG=ru|es to localize)
Needs: pip install -e ".[sandbox]"   (~50 MB, git clones — run once)
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.economy import embedded_sandbox, sdk_available
from courselib.i18n import get_translator
from courselib.orchestration import Trace


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m6.title')} ==")
    print(t("modules.m6.concept"))

    # The capstone is the only lab that needs the full aimarket-agent SDK
    # (the [sandbox] extra). Everything else runs on hub-lite. If the SDK is
    # absent, skip cleanly with a clear hint instead of crashing.
    if not sdk_available():
        print()
        print(t("labs.lab06.sdk_missing"))
        print(f"\n--- {t('exercises.heading')} ---")
        print(t("exercises.lab06_hint"))
        return

    with embedded_sandbox(budget=3.0) as econ:
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

        print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
        for e in trace.events:
            print(" ", e["kind"], {k: v for k, v in e.items() if k not in ("t", "kind")})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab06_hint"))


if __name__ == "__main__":
    main()
