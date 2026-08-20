"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

from __future__ import annotations

from courselib.lumen import TrustGraph, demo_mcp_trust_graph, score_servers
from courselib.warden import (
    BENIGN_TOOLS,
    MALICIOUS_TOOLS,
    McpServerRef,
    OwnerLock,
    StaticScanGate,
    ThreatFeed,
    ToolDef,
    Warden,
    WardenGateInput,
    WardenPolicy,
    GraphTrustOracle,
    MemoryStore,
)

MODULES = ('m1', 'm2', 'm3', 'm4', 'm5')

def exercise_m1_injection_detected() -> None:
    """Poisoned tool description must trigger TOOL_DEF_INJECTION."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_injection_detected: implement this exercise")

def exercise_m2_benign_clean() -> None:
    """Benign tools should produce no critical findings."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_benign_clean: implement this exercise")

def exercise_m3_lumen_ranks_hub() -> None:
    """Hub node should outrank an isolated typosquat server."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_lumen_ranks_hub: implement this exercise")

def exercise_m4_owner_lock_fail_closed() -> None:
    """Unknown tool must be blocked when allowlist is enforced."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_owner_lock_fail_closed: implement this exercise")

def exercise_m5_warden_blocks_malicious() -> None:
    """Full WARDEN pipeline must block the poisoned capstone server."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_warden_blocks_malicious: implement this exercise")

EXERCISES = {
    "m1": exercise_m1_injection_detected,
    "m2": exercise_m2_benign_clean,
    "m3": exercise_m3_lumen_ranks_hub,
    "m4": exercise_m4_owner_lock_fail_closed,
    "m5": exercise_m5_warden_blocks_malicious,
}

def run_all() -> dict[str, str]:
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
