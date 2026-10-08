"""LUMEN trust scoring — PageRank over an MCP server trust graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from courselib.oracle_paths import ensure_oracle


def _pagerank():
    ensure_oracle("lumen")
    from lumen import pagerank  # noqa: WPS433 — dynamic oracle import

    return pagerank


@dataclass
class TrustGraph:
    """Directed weighted trust edges between MCP server ids."""

    nodes: list[str] = field(default_factory=list)
    edges: list[tuple[str, str, float]] = field(default_factory=list)

    def node_index(self) -> dict[str, int]:
        return {name: i for i, name in enumerate(self.nodes)}

    def to_lumen_edges(self) -> list[list[float]]:
        idx = self.node_index()
        return [[idx[src], idx[dst], w] for src, dst, w in self.edges]


def score_servers(graph: TrustGraph) -> dict[str, float]:
    """Return PageRank scores keyed by server id (sums to 1)."""
    if not graph.nodes:
        return {}
    pr = _pagerank()
    out = pr.pagerank(len(graph.nodes), graph.to_lumen_edges())
    return {graph.nodes[i]: out["scores"][i] for i in range(len(graph.nodes))}


def score_entity(server_id: str, graph: TrustGraph) -> dict[str, Any]:
    """Score one server; unknown ids get 0."""
    scores = score_servers(graph)
    if server_id not in scores:
        return {"score": 0.0, "degraded": False, "known": False}
    return {"score": scores[server_id], "degraded": False, "known": True}


def demo_mcp_trust_graph() -> TrustGraph:
    """Teaching graph: official servers trusted by hub; typosquat isolated."""
    return TrustGraph(
        nodes=[
            "hub",
            "official-filesystem",
            "official-fetch",
            "community-weather",
            "offical-mcp-drainer",
        ],
        edges=[
            ("hub", "official-filesystem", 3.0),
            ("hub", "official-fetch", 2.0),
            ("hub", "community-weather", 1.0),
            ("official-filesystem", "hub", 1.0),
            ("official-fetch", "hub", 1.0),
            ("community-weather", "official-fetch", 0.5),
        ],
    )
