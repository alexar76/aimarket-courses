"""Lab 01 — MCP threat model (Module 1).

Demonstrate prompt injection and tool poisoning attack surfaces without an LLM.

Run:  python labs/lab01_threat_model.py
      COURSE_LANG=ru python labs/lab01_threat_model.py
Exercise: python labs/run_exercises.py --module m1
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from courselib.i18n import get_translator
from courselib.trace import Trace
from courselib.warden import MALICIOUS_TOOLS, ToolDef


def _scenario_injection(t, trace: Trace) -> None:
    print(f"\n--- {t('labs.lab01.injection_heading')} ---")
    user_task = t("labs.lab01.user_task")
    poisoned = ToolDef(
        name="summarize",
        description=t("labs.lab01.poisoned_desc"),
        input_schema={"type": "object", "properties": {"text": {"type": "string"}}},
    )
    print(f"{t('ui.task')}: {user_task}")
    print(f"{t('labs.lab01.tool_def')} ({poisoned.name}):")
    print(f"  {poisoned.description}")
    trace.log("prompt_injection", tool=poisoned.name)
    print(t("labs.lab01.injection_note"))


def _scenario_tool_poisoning(t, trace: Trace) -> None:
    print(f"\n--- {t('labs.lab01.poison_heading')} ---")
    for tool in MALICIOUS_TOOLS[:1]:
        print(f"{t('labs.lab01.tool_def')} ({tool.name}):")
        print(f"  {tool.description[:120]}…")
        trace.log("tool_poisoning", tool=tool.name, code="TOOL_DEF_INJECTION")
    print(t("labs.lab01.poison_note"))


def main() -> None:
    t = get_translator()
    trace = Trace()
    print(f"== {t('modules.m1.title')} ==")
    print(t("modules.m1.concept"))
    _scenario_injection(t, trace)
    _scenario_tool_poisoning(t, trace)
    print(f"\n{t('ui.trace')} ({len(trace)} {t('ui.events')}):")
    for event in trace.events:
        print(" ", event["kind"], {k: v for k, v in event.items() if k != "kind"})
    print(f"\n--- {t('exercises.heading')} ---")
    print(t("exercises.lab01_hint"))


if __name__ == "__main__":
    main()
