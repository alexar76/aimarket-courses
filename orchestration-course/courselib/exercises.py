"""Hands-on exercises — student stubs (# YOUR CODE HERE).

Fill each stub, then:

  python labs/run_exercises.py
  pytest tests/test_exercises.py -q

Reference solutions (for maintainers / CI): courselib/exercise_solutions.py
"""

from __future__ import annotations

from courselib.orchestration import (
    Agent,
    Context,
    Handoff,
    Router,
    StatefulPipeline,
    Tool,
    Trace,
    guarded_tool,
    injection_guardrail,
    keyword_policy,
)
from courselib.trust import sign_receipt, tamper_receipt, verify_receipt

MODULES = ("m1", "m2", "m3", "m5", "m6", "m7")


def exercise_m1_add_tool_route() -> None:
    """Add a route so 'count' uses a word-count tool."""
    trace = Trace()
    # YOUR CODE HERE — build an Agent with keyword_policy({"count": "count_words"})
    # and Tool("count_words", lambda s: len(s.split())), then assert:
    #   agent.run("please count words in this line") == 6
    #   and trace.of_kind("tool_call")
    raise NotImplementedError("exercise_m1: implement the count_words route")


def exercise_m2_build_router() -> None:
    """Route Spanish vs English greetings."""
    # YOUR CODE HERE — Router with es/en Agents; assert "hola"→"ES", "hello"→"EN"
    raise NotImplementedError("exercise_m2: implement the language router")


def exercise_m3_handoff_once() -> None:
    """Front desk must hand off legal tasks."""
    # YOUR CODE HERE — front Agent returns Handoff(to=legal, ...) on "nda"
    raise NotImplementedError("exercise_m3: implement the legal handoff")


def exercise_m5_context_bom() -> None:
    """Build a 3-stage BOM: spec -> draft -> published flag."""
    # YOUR CODE HERE — StatefulPipeline of ingest/review/publish stages
    raise NotImplementedError("exercise_m5: implement the 3-stage BOM pipeline")


def exercise_m6_block_injection() -> None:
    """Guardrail must block prompt injection."""
    # YOUR CODE HERE — guarded_tool(echo, [injection_guardrail()])
    raise NotImplementedError("exercise_m6: wrap echo with injection_guardrail")


def exercise_m7_verify_and_tamper() -> None:
    """Signed receipt verifies; tampered receipt fails."""
    # YOUR CODE HERE — sign_receipt / verify_receipt / tamper_receipt
    raise NotImplementedError("exercise_m7: verify signed + reject tampered receipt")


EXERCISES: dict[str, callable] = {
    "m1": exercise_m1_add_tool_route,
    "m2": exercise_m2_build_router,
    "m3": exercise_m3_handoff_once,
    "m5": exercise_m5_context_bom,
    "m6": exercise_m6_block_injection,
    "m7": exercise_m7_verify_and_tamper,
}


def run_all() -> dict[str, str]:
    """Run every exercise; return {module: 'ok'|'fail: ...'}."""
    out: dict[str, str] = {}
    for mod, fn in EXERCISES.items():
        try:
            fn()
            out[mod] = "ok"
        except Exception as exc:
            out[mod] = f"fail: {exc}"
    return out


def all_passed(results: dict[str, str] | None = None) -> bool:
    results = results if results is not None else run_all()
    return all(v == "ok" for v in results.values())
