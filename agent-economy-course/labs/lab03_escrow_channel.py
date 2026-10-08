"""Lab 03 - Escrow & payment channels (Module 3).

Open a pre-funded payment channel, invoke through hub-lite, then close and
inspect the refund — the micropayment pattern behind Protocol v2 escrow.

Run:  python labs/lab03_escrow_channel.py   (COURSE_LANG=ru|es to localize)
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
    print(f"== {t('modules.m3.title')} ==")
    print(t("modules.m3.concept"))

    trace = Trace()

    with embedded_hub_lite() as hub:
        opened = hub.open_channel(budget_usd=0.25)
        channel_id = opened.get("channel_id", "")
        trace.emit("channel_open", channel_id=channel_id, budget=opened.get("budget_usd"))
        print(f"{t('ui.channel')}     :", channel_id or t("ui.none"))
        print(f"{t('labs.lab03.budget')}   : ${opened.get('budget_usd')}")

        out = hub.invoke("prod-summarize", "summarize@v1", {"text": t("labs.lab03.sample")})
        trace.emit("invoke", capability="summarize@v1", price_usd=out.get("price_usd"))
        print(f"\n{t('ui.invoke')} summarize@v1  {t('ui.price')}=${out.get('price_usd')}")

        closed = hub.close_channel(channel_id)
        trace.emit("channel_close", spent=closed.get("spent_usd"), refund=closed.get("refund_usd"))
        print(f"\n{t('labs.lab03.spent')}    : ${closed.get('spent_usd', 0)}")
        print(f"{t('labs.lab03.refund')}   : ${closed.get('refund_usd', 0)}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for e in trace.events:
        print(" ", e["kind"], {k: v for k, v in e.items() if k not in ("t", "kind")})

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab03_hint"))


if __name__ == "__main__":
    main()
