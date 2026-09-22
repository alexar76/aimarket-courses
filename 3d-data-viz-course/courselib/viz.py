"""Graph data structures matching alien-monitor REST API responses + R3F scene mapping."""

from __future__ import annotations

import json
import os
import socket
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

DEFAULT_MONITOR_URL = os.getenv("ALIEN_MONITOR_URL", "http://127.0.0.1:9100").rstrip("/")

# Mirrored from alien-monitor/frontend/src/oracleScenes/meta.ts
ORACLE_SCENE_META: dict[str, dict[str, Any]] = {
    "platon": {
        "camera": [0, 1.5, 11],
        "accent": "#6ee7ff",
        "primitive": "Coupled Stuart-Landau / Kuramoto oscillators on a Fibonacci sphere",
    },
    "chronos": {
        "camera": [0, 3, 16],
        "accent": "#c084fc",
        "primitive": "Wesolowski VDF — sequential squaring over an RSA-2048 modulus",
    },
    "lattice": {
        "camera": [0, 2, 13],
        "accent": "#7dd3fc",
        "primitive": "Halton low-discrepancy sequence · van der Corput radical inverse",
    },
    "murmuration": {
        "camera": [0, 4, 16],
        "accent": "#f472b6",
        "primitive": "DeGroot consensus dynamics · Tukey-biweight robust aggregation",
    },
    "lumen": {
        "camera": [0, 2, 14],
        "accent": "#fbbf24",
        "primitive": "EigenTrust / PageRank power iteration over the trust graph",
    },
    "colony": {
        "camera": [0, 8, 14],
        "accent": "#34d399",
        "primitive": "Nearest-neighbour + 2-opt TSP tour with an optimality-gap bound",
    },
    "turing": {
        "camera": [0, 2, 13],
        "accent": "#a78bfa",
        "primitive": "Mitchell best-candidate blue-noise — maximal minimum distance",
    },
    "percola": {
        "camera": [0, 2, 14],
        "accent": "#22d3ee",
        "ambient": True,
        "primitive": "Bond percolation · giant-component collapse at f_c",
    },
    "ablation": {
        "camera": [0, 2, 14],
        "accent": "#ef4444",
        "ambient": True,
        "primitive": "Abelian sandpile · self-organized criticality · avalanche τ",
    },
    "landauer": {
        "camera": [0, 2, 14],
        "accent": "#fb7185",
        "ambient": True,
        "primitive": "Landauer's principle · kT·ln2 erasure-energy floor",
    },
}


@dataclass
class Vec3:
    x: float
    y: float
    z: float

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> Vec3:
        d = d or {}
        return cls(float(d.get("x", 0)), float(d.get("y", 0)), float(d.get("z", 0)))


@dataclass
class MonitorNode:
    id: str
    label: str
    group: str
    status: str
    metrics: dict[str, Any] = field(default_factory=dict)
    position: Vec3 = field(default_factory=Vec3)
    icon: str = ""
    url: str | None = None
    description: str = ""

    @classmethod
    def from_api(cls, raw: dict[str, Any]) -> MonitorNode:
        return cls(
            id=str(raw.get("id", "")),
            label=str(raw.get("label", raw.get("id", ""))),
            group=str(raw.get("group", "unknown")),
            status=str(raw.get("status", "unknown")),
            metrics=dict(raw.get("metrics") or {}),
            position=Vec3.from_dict(raw.get("position")),
            icon=str(raw.get("icon", "")),
            url=raw.get("url"),
            description=str(raw.get("description", "")),
        )


@dataclass
class MonitorLink:
    source: str
    target: str
    kind: str = "default"
    weight: float = 1.0

    @classmethod
    def from_api(cls, raw: dict[str, Any]) -> MonitorLink:
        return cls(
            source=str(raw.get("source", "")),
            target=str(raw.get("target", "")),
            kind=str(raw.get("kind", raw.get("type", "default"))),
            weight=float(raw.get("weight", 1.0)),
        )


@dataclass
class TopologyGraph:
    nodes: list[MonitorNode]
    links: list[MonitorLink]

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> TopologyGraph:
        nodes = [MonitorNode.from_api(n) for n in payload.get("nodes") or []]
        links = [MonitorLink.from_api(lk) for lk in payload.get("links") or []]
        return cls(nodes=nodes, links=links)

    def node_ids(self) -> list[str]:
        return [n.id for n in self.nodes]

    def oracle_slugs(self) -> list[str]:
        out: list[str] = []
        for n in self.nodes:
            if n.id.startswith("oracle-"):
                out.append(n.id.removeprefix("oracle-"))
            elif n.group == "oracle":
                out.append(n.id)
        return out

    def adjacency(self) -> list[tuple[int, int, float]]:
        index = {nid: i for i, nid in enumerate(self.node_ids())}
        edges: list[tuple[int, int, float]] = []
        seen: set[tuple[int, int]] = set()
        for link in self.links:
            i, j = index.get(link.source), index.get(link.target)
            if i is None or j is None or i == j:
                continue
            key = (i, j)
            if key in seen:
                continue
            seen.add(key)
            edges.append((i, j, link.weight))
        return edges


@dataclass
class HealthStatus:
    status: str
    mode: str
    raw: dict[str, Any]

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> HealthStatus:
        return cls(
            status=str(payload.get("status", "unknown")),
            mode=str(payload.get("mode", "unknown")),
            raw=dict(payload),
        )


@dataclass
class ReputationPeer:
    url: str
    name: str
    trust_score: float | None
    categories: list[str] = field(default_factory=list)

    @classmethod
    def from_api(cls, raw: dict[str, Any]) -> ReputationPeer:
        score = raw.get("trust_score")
        return cls(
            url=str(raw.get("url", "")),
            name=str(raw.get("name", "")),
            trust_score=float(score) if score is not None else None,
            categories=list(raw.get("categories") or []),
        )


@dataclass
class ReputationPeers:
    peers: list[ReputationPeer]
    count: int
    mode: str
    source: str

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> ReputationPeers:
        peers = [ReputationPeer.from_api(p) for p in payload.get("peers") or []]
        return cls(
            peers=peers,
            count=int(payload.get("count", len(peers))),
            mode=str(payload.get("mode", "")),
            source=str(payload.get("source", "")),
        )


@dataclass
class LumenScores:
    ok: bool
    scores: list[float]
    ids: list[str]
    source: str = ""
    error: str = ""
    converged: bool | None = None
    iterations: int | None = None

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> LumenScores:
        return cls(
            ok=bool(payload.get("ok")),
            scores=[float(s) for s in payload.get("scores") or []],
            ids=[str(i) for i in payload.get("ids") or []],
            source=str(payload.get("source", "")),
            error=str(payload.get("error", "")),
            converged=payload.get("converged"),
            iterations=payload.get("iterations"),
        )

    def by_id(self) -> dict[str, float]:
        return dict(zip(self.ids, self.scores))


@dataclass
class R3FSceneSpec:
    slug: str
    camera: tuple[float, float, float]
    accent: str
    primitive: str
    ambient: bool = False
    node_id: str = ""

    @classmethod
    def for_oracle(cls, slug: str, node_id: str | None = None) -> R3FSceneSpec:
        meta = ORACLE_SCENE_META.get(slug, {})
        cam = meta.get("camera", [0, 2, 14])
        return cls(
            slug=slug,
            camera=(float(cam[0]), float(cam[1]), float(cam[2])),
            accent=str(meta.get("accent", "#ffffff")),
            primitive=str(meta.get("primitive", slug)),
            ambient=bool(meta.get("ambient", False)),
            node_id=node_id or f"oracle-{slug}",
        )


def map_graph_to_r3f_scenes(graph: TopologyGraph) -> list[R3FSceneSpec]:
    """Bind monitor oracle nodes to R3F scene metadata."""
    specs: list[R3FSceneSpec] = []
    for slug in graph.oracle_slugs():
        specs.append(R3FSceneSpec.for_oracle(slug))
    return specs


def _get_json(path: str, base_url: str = DEFAULT_MONITOR_URL, timeout: float = 3.0) -> dict[str, Any]:
    url = f"{base_url}{path}"
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def probe_health(base_url: str = DEFAULT_MONITOR_URL) -> HealthStatus:
    return HealthStatus.from_api(_get_json("/api/health", base_url))


def probe_topology(base_url: str = DEFAULT_MONITOR_URL) -> TopologyGraph:
    return TopologyGraph.from_api(_get_json("/api/topology", base_url))


def probe_reputation_peers(base_url: str = DEFAULT_MONITOR_URL) -> ReputationPeers:
    return ReputationPeers.from_api(_get_json("/api/reputation/peers", base_url))


def probe_lumen_scores(base_url: str = DEFAULT_MONITOR_URL) -> LumenScores:
    return LumenScores.from_api(_get_json("/api/reputation/lumen", base_url))


def monitor_reachable(base_url: str = DEFAULT_MONITOR_URL, timeout: float = 1.0) -> bool:
    try:
        probe_health(base_url)
        return True
    except (URLError, OSError, TimeoutError, ValueError):
        return False


_MOCK_PAYLOADS: dict[str, dict[str, Any]] = {
    "/api/health": {"status": "ok", "mode": "test"},
    "/api/topology": {
        "nodes": [
            {
                "id": "hub",
                "label": "AIMarket Hub",
                "group": "core",
                "status": "healthy",
                "metrics": {"capabilities": 12},
                "position": {"x": 0, "y": 0, "z": 0},
            },
            {
                "id": "oracle-lumen",
                "label": "LUMEN",
                "group": "oracle",
                "status": "healthy",
                "metrics": {},
                "position": {"x": 3, "y": 1, "z": -2},
            },
            {
                "id": "oracle-murmuration",
                "label": "Murmuration",
                "group": "oracle",
                "status": "healthy",
                "metrics": {},
                "position": {"x": -3, "y": 2, "z": 1},
            },
            {
                "id": "oracle-turing",
                "label": "Turing",
                "group": "oracle",
                "status": "healthy",
                "metrics": {},
                "position": {"x": 1, "y": -2, "z": 3},
            },
        ],
        "links": [
            {"source": "hub", "target": "oracle-lumen", "kind": "invoke"},
            {"source": "hub", "target": "oracle-murmuration", "kind": "invoke"},
            {"source": "oracle-lumen", "target": "oracle-turing", "kind": "trust"},
        ],
    },
    "/api/reputation/peers": {
        "peers": [
            {"url": "https://hub-a.example", "name": "Hub Alpha", "trust_score": 0.82},
            {"url": "https://hub-b.example", "name": "Hub Beta", "trust_score": 0.61},
        ],
        "count": 2,
        "mode": "test",
        "source": "mock",
    },
    "/api/reputation/lumen": {
        "ok": True,
        "scores": [0.45, 0.30, 0.15, 0.10],
        "ids": ["hub", "oracle-lumen", "oracle-murmuration", "oracle-turing"],
        "source": "mock · lumen.reputation@v1",
        "converged": True,
        "iterations": 18,
    },
}


class MockMonitorServer:
    """Lightweight stdlib HTTP mock matching alien-monitor REST shape."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0) -> None:
        self.host = host
        self.port = port
        self._httpd: HTTPServer | None = None
        self._thread: threading.Thread | None = None
        payloads = _MOCK_PAYLOADS

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args: Any) -> None:
                return

            def do_GET(self) -> None:
                path = self.path.split("?", 1)[0]
                body = payloads.get(path)
                if body is None:
                    self.send_response(404)
                    self.end_headers()
                    return
                data = json.dumps(body).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self._handler = Handler

    def start(self) -> str:
        sock = socket.socket()
        sock.bind((self.host, self.port))
        self.port = sock.getsockname()[1]
        sock.close()
        self._httpd = HTTPServer((self.host, self.port), self._handler)
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        return f"http://{self.host}:{self.port}"

    def stop(self) -> None:
        if self._httpd:
            self._httpd.shutdown()
            self._httpd.server_close()


def resolve_monitor_url() -> tuple[str, MockMonitorServer | None]:
    """Return live monitor URL or start an in-process mock server."""
    if monitor_reachable():
        return DEFAULT_MONITOR_URL, None
    mock = MockMonitorServer()
    url = mock.start()
    return url, mock


def exercise_check(module: str) -> None:
    """Minimal DIY check students extend in each module."""
    assert module.startswith("m"), module
    url, mock = resolve_monitor_url()
    try:
        if module == "m1":
            h = probe_health(url)
            assert h.status == "ok"
        elif module == "m2":
            g = probe_topology(url)
            assert len(g.nodes) >= 2
        elif module == "m3":
            p = probe_reputation_peers(url)
            assert p.count >= 0
        elif module == "m4":
            l = probe_lumen_scores(url)
            assert l.ok and len(l.scores) == len(l.ids)
        elif module == "m5":
            g = probe_topology(url)
            scenes = map_graph_to_r3f_scenes(g)
            assert all(s.slug for s in scenes)
        else:
            raise AssertionError(f"unknown module {module}")
    finally:
        if mock:
            mock.stop()
