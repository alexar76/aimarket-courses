"""Tests for viz graph models and monitor API client."""

from courselib.viz import (
    HealthStatus,
    LumenScores,
    MockMonitorServer,
    MonitorLink,
    MonitorNode,
    R3FSceneSpec,
    TopologyGraph,
    map_graph_to_r3f_scenes,
    probe_health,
    probe_lumen_scores,
    probe_reputation_peers,
    probe_topology,
)


def test_health_from_api():
    h = HealthStatus.from_api({"status": "ok", "mode": "test"})
    assert h.status == "ok"
    assert h.mode == "test"


def test_topology_graph_parsing():
    payload = {
        "nodes": [{"id": "hub", "label": "Hub", "group": "core", "status": "healthy"}],
        "links": [{"source": "hub", "target": "oracle-lumen"}],
    }
    g = TopologyGraph.from_api(payload)
    assert len(g.nodes) == 1
    assert isinstance(g.nodes[0], MonitorNode)
    assert isinstance(g.links[0], MonitorLink)


def test_lumen_scores_by_id():
    l = LumenScores.from_api({"ok": True, "scores": [0.6, 0.4], "ids": ["a", "b"]})
    assert l.by_id() == {"a": 0.6, "b": 0.4}


def test_r3f_scene_meta():
    spec = R3FSceneSpec.for_oracle("murmuration")
    assert spec.slug == "murmuration"
    assert len(spec.camera) == 3
    assert spec.accent.startswith("#")


def test_mock_server_endpoints():
    mock = MockMonitorServer()
    url = mock.start()
    try:
        h = probe_health(url)
        g = probe_topology(url)
        p = probe_reputation_peers(url)
        l = probe_lumen_scores(url)
        assert h.status == "ok"
        assert len(g.nodes) >= 3
        assert p.count >= 1
        assert l.ok and len(l.scores) == len(l.ids)
        scenes = map_graph_to_r3f_scenes(g)
        assert any(s.slug == "lumen" for s in scenes)
    finally:
        mock.stop()


def test_oracle_slug_extraction():
    g = TopologyGraph.from_api(
        {
            "nodes": [
                {"id": "oracle-turing", "label": "T", "group": "oracle", "status": "ok"},
                {"id": "hub", "label": "H", "group": "core", "status": "ok"},
            ],
            "links": [],
        }
    )
    assert g.oracle_slugs() == ["turing"]
