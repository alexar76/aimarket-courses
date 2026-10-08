"""Lab 05 — WARDEN capstone: catch a malicious MCP server (Module 5).

Run the full WARDEN gate chain against a poisoned server vs a benign one.

Run:  python labs/lab05_warden_capstone.py
      COURSE_LANG=ru python labs/lab05_warden_capstone.py
Exercise: python labs/run_exercises.py --module m5
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.lumen import demo_mcp_trust_graph
from courselib.trace import Trace
from courselib.warden import (
    BENIGN_SERVER,
    BENIGN_TOOLS,
    MALICIOUS_TOOLS,
    POISONED_SERVER,
    GraphTrustOracle,
    MemoryStore,
    OwnerLock,
    Warden,
    WardenPolicy,
    WardenVerdict,
)


def _print_verdict(t, label: str, verdict: WardenVerdict, trace: Trace) -> None:
    status = t("ui.allowed") if verdict.allow else t("ui.blocked")
    print(f"\n--- {label} ---")
    print(f"{t('ui.result')}: {status}  {t('ui.score')}: {verdict.score:.3f}")
    if verdict.decided_by:
        print(f"{t('labs.lab05.decided_by')}: {verdict.decided_by}")
    print(f"{t('labs.lab05.findings')}: {len(verdict.findings)}")
    for f in verdict.findings[:8]:
        print(f"  [{f.severity}] {f.gate}/{f.code}")
        trace.log("warden_finding", gate=f.gate, code=f.code, severity=f.severity)
    if len(verdict.findings) > 8:
        print(f"  … +{len(verdict.findings) - 8} more")
    print(f"{t('labs.lab05.tools_allowed')}: {verdict.allowed_tools}")
    print(f"{t('labs.lab05.tools_blocked')}: {verdict.blocked_tools}")


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m5.title')} ==")
    print(t("modules.m5.concept"))

    graph = demo_mcp_trust_graph()
    store = MemoryStore()
    owner = OwnerLock(t("labs.lab04.owner_id"), {"read_file", "search_docs", "helpful_assistant"})
    policy = WardenPolicy(
        block_at_severity="high",
        min_reputation=0.02,
        allow_unknown_servers=False,
        pin_tool_defs=True,
    )
    warden = Warden.create(
        oracle=GraphTrustOracle(graph),
        store=store,
        policy=policy,
        owner_lock=owner,
    )

    benign = warden.vet(BENIGN_SERVER, BENIGN_TOOLS)
    _print_verdict(t, t("labs.lab05.benign_label"), benign, trace)

    poisoned = warden.vet(POISONED_SERVER, MALICIOUS_TOOLS)
    _print_verdict(t, t("labs.lab05.malicious_label"), poisoned, trace)

    print(f"\n{t('labs.lab05.summary')}")
    print(f"  {t('labs.lab05.benign_label')}: {t('ui.allowed') if benign.allow else t('ui.blocked')}")
    print(f"  {t('labs.lab05.malicious_label')}: {t('ui.allowed') if poisoned.allow else t('ui.blocked')}")

    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')})")
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab05_hint"))


if __name__ == "__main__":
    main()
