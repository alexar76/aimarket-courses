"""Lab 02 — Static scan & policy (Module 2).

Scan malicious vs benign MCP tool definitions and print WARDEN findings.

Run:  python labs/lab02_static_scan.py
      COURSE_LANG=ru python labs/lab02_static_scan.py
Exercise: python labs/run_exercises.py --module m2
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.warden import (
    BENIGN_SERVER,
    BENIGN_TOOLS,
    MALICIOUS_TOOLS,
    StaticScanGate,
    WardenGateInput,
    WardenPolicy,
)


def _scan(label: str, tools, trace: Trace) -> None:
    gate = StaticScanGate()
    result = gate.evaluate(
        WardenGateInput(
            server=BENIGN_SERVER,
            tools=tools,
            prior=[],
            policy=WardenPolicy(),
        )
    )
    print(f"\n--- {label} ---")
    print(f"score: {result.score:.2f}  findings: {len(result.findings)}")
    for f in result.findings:
        print(f"  [{f.severity}] {f.code} — {f.message}")
        trace.log("finding", gate=f.gate, code=f.code, severity=f.severity, tool=f.tool)


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m2.title')} ==")
    print(t("modules.m2.concept"))
    _scan(t("labs.lab02.benign_label"), BENIGN_TOOLS, trace)
    _scan(t("labs.lab02.malicious_label"), MALICIOUS_TOOLS, trace)
    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.of_kind("finding"):
        print(" ", event["code"], event.get("severity"), event.get("tool"))
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab02_hint"))


if __name__ == "__main__":
    main()
