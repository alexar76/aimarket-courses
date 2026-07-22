"""Hands-on exercises — DIY checks for each module."""

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
    url, mock = resolve_monitor_url()
    try:
        h = probe_health(url)
        assert h.status == "ok"
        assert h.mode in ("test", "real", "universe")
    finally:
        if mock:
            mock.stop()


def exercise_m2_topology_parses() -> None:
    url, mock = resolve_monitor_url()
    try:
        g = probe_topology(url)
        assert isinstance(g, TopologyGraph)
        assert all(isinstance(n, MonitorNode) for n in g.nodes)
        assert len(g.adjacency()) >= 1
    finally:
        if mock:
            mock.stop()


def exercise_m3_peers_list() -> None:
    url, mock = resolve_monitor_url()
    try:
        p = probe_reputation_peers(url)
        assert p.count == len(p.peers)
    finally:
        if mock:
            mock.stop()


def exercise_m4_lumen_scores() -> None:
    url, mock = resolve_monitor_url()
    try:
        l = probe_lumen_scores(url)
        assert isinstance(l, LumenScores)
        assert l.ok and len(l.scores) == len(l.ids)
        assert abs(sum(l.scores) - 1.0) < 0.05 or sum(l.scores) > 0
    finally:
        if mock:
            mock.stop()


def exercise_m5_r3f_mapping() -> None:
    url, mock = resolve_monitor_url()
    try:
        g = probe_topology(url)
        scenes = map_graph_to_r3f_scenes(g)
        assert scenes
        assert all(isinstance(s, R3FSceneSpec) for s in scenes)
        assert all(len(s.camera) == 3 for s in scenes)
    finally:
        if mock:
            mock.stop()


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


def all_passed() -> bool:
    return all(v == "ok" for v in run_all().values())
