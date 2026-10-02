"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

from __future__ import annotations

from courselib.hub_lite import embedded_hub_lite
from courselib.protocol import is_valid_manifest, is_valid_well_known, validate_well_known
from courselib.trust import TrustGraph, sign_receipt, tamper_receipt, verify_receipt

MODULES = ('m1', 'm2', 'm3', 'm4', 'm5', 'm6')

def exercise_m1_validate_well_known() -> None:
    """Parse and validate a Protocol v2 well-known document."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_validate_well_known: implement this exercise")

def exercise_m2_discover_capability() -> None:
    """Discover a translate capability on hub-lite."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_discover_capability: implement this exercise")

def exercise_m3_open_close_channel() -> None:
    """Open a payment channel, then close it with a refund."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_open_close_channel: implement this exercise")

def exercise_m4_verify_receipt_and_trust() -> None:
    """Verify a signed receipt and feed the trust graph."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_verify_receipt_and_trust: implement this exercise")

def exercise_m5_publish_capability() -> None:
    """Register a metered capability and discover it."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_publish_capability: implement this exercise")

def exercise_m6_paid_invoke_flow() -> None:
    """Invoke a paid capability and verify the receipt."""
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m6_paid_invoke_flow: implement this exercise")

EXERCISES = {
    "m1": exercise_m1_validate_well_known,
    "m2": exercise_m2_discover_capability,
    "m3": exercise_m3_open_close_channel,
    "m4": exercise_m4_verify_receipt_and_trust,
    "m5": exercise_m5_publish_capability,
    "m6": exercise_m6_paid_invoke_flow,
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
