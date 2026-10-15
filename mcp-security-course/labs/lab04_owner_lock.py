"""Lab 04 — Owner-lock & fail-closed allowlist (Module 4).

Demonstrate owner-approved tool allowlists that block everything else.

Run:  python labs/lab04_owner_lock.py
      COURSE_LANG=ru python labs/lab04_owner_lock.py
Exercise: python labs/run_exercises.py --module m4
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.warden import BENIGN_TOOLS, OwnerLock, ToolDef


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m4.title')} ==")
    print(t("modules.m4.concept"))

    owner_id = t("labs.lab04.owner_id")
    allowed = {"read_file", "search_docs"}
    lock = OwnerLock(owner_id, allowed)
    print(f"\n{t('labs.lab04.allowlist')}: {sorted(allowed)}")

    candidates = BENIGN_TOOLS + [
        ToolDef(name="exec_shell", description="Run arbitrary shell commands."),
        ToolDef(name="transfer_funds", description="Send crypto to an address."),
    ]

    for tool in candidates:
        ok, reason = lock.check_tool(tool.name)
        status = t("ui.allowed") if ok else t("ui.blocked")
        print(f"  {tool.name:20s} → {status}")
        if not ok:
            print(f"    {reason}")
        trace.log(
            "owner_lock",
            tool=tool.name,
            allowed=ok,
            reason=reason if not ok else "",
        )

    print(f"\n{t('labs.lab04.fail_closed')}")
    empty = OwnerLock(owner_id, [])
    ok_empty, reason_empty = empty.check_tool("read_file")
    print(f"  read_file with empty allowlist → {t('ui.blocked')}: {reason_empty}")
    trace.log("owner_lock", tool="read_file", allowed=ok_empty, empty_allowlist=True)

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.of_kind("owner_lock"):
        print(" ", event["tool"], "allowed=" + str(event["allowed"]))

    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab04_hint"))


if __name__ == "__main__":
    main()
