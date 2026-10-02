"""Lab 02 - Hub discovery & invocation (Module 2).

Embedded hub-lite discover → invoke → receipt. Same pattern as production
AIMarket federation without cloning aimarket-hub.

Run:  python labs/lab02_hub_discover.py   (COURSE_LANG=ru|es to localize)
Needs: pip install -e ".[hub-lite]"
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.hub_lite import embedded_hub_lite
from courselib.i18n import get_translator
from courselib.orchestration import Trace


def main() -> None:
    t = get_translator()
    print(f"== {t('modules.m2.title')} ==")

    trace = Trace()

    with embedded_hub_lite() as hub:
        print(f"{t('ui.hub')}:", hub.well_known().get("name"))

        print(f"\n{t('ui.discover')}('translate'):")
        matches = hub.discover("translate")[:5]
        trace.emit("discover", query="translate", matches=len(matches))
        for m in matches:
            print(f"  {m.get('product_id')}/{m.get('capability_id')}"
                  f"  ${m.get('price_per_call_usd')}")

        print(f"\n{t('labs.lab02.invoking')}:")
        out = hub.invoke("prod-translate", "translate.multi@v2", {"text": "hello world"})
        trace.emit("invoke", capability="translate.multi@v2",
                   success=out.get("success"), price_usd=out.get("price_usd"))
        print(f"  {t('ui.success')}     :", out.get("success"))
        print(f"  {t('ui.price')}       :", out.get("price_usd"))
        print(f"  {t('ui.served_by')}   :", out.get("result", {}).get("output", {}).get("served_by"))
        print(f"  {t('ui.receipt')}     :", (out.get("receipt") or {}).get("nonce", "n/a"))

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e["kind"], {k: v for k, v in e.items() if k not in ("t", "kind")})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
