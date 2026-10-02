"""Student stubs — fill # YOUR CODE HERE, then run labs/run_exercises.py."""

from __future__ import annotations

from courselib.viz import (
    HealthStatus,
    LumenScores,
    MonitorNode,
    R3FSceneSpec,
    TopologyGraph,
    exercise_check,
    map_graph_to_r3f_scenes,
    probe_health,
    probe_lumen_scores,
    probe_reputation_peers,
    probe_topology,
    resolve_monitor_url,
)

MODULES = ("m1", "m2", "m3", "m4", "m5")


def exercise_m1_health_ok() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m1_health_ok: implement this exercise")

def exercise_m2_topology_parses() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m2_topology_parses: implement this exercise")

def exercise_m3_peers_list() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m3_peers_list: implement this exercise")

def exercise_m4_lumen_scores() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m4_lumen_scores: implement this exercise")

def exercise_m5_r3f_mapping() -> None:
    # YOUR CODE HERE
    raise NotImplementedError("exercise_m5_r3f_mapping: implement this exercise")

EXERCISES = {
    "m1": exercise_m1_health_ok,
    "m2": exercise_m2_topology_parses,
    "m3": exercise_m3_peers_list,
    "m4": exercise_m4_lumen_scores,
    "m5": exercise_m5_r3f_mapping,
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
