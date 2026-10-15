"""AI-Factory pipeline client — live factory or embedded mock.

Probes:
  GET /api/public/pipeline-status
  GET /ai-market/products
"""

from __future__ import annotations

import json
import os
import socket
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import httpx

# Simplified teaching map: research → design → build → test → ship
PIPELINE_PHASES: tuple[tuple[str, str, str], ...] = (
    ("research", "analyst", "MARKET_RESEARCHED"),
    ("design", "architect", "ARCH_DESIGNED"),
    ("build", "developer", "CODE_COMMITTED"),
    ("test", "qa", "QA_TESTING"),
    ("ship", "devops", "COMPLETED"),
)

MOCK_STATUS = {"products_in_pipeline": 4, "products_shipped": 2}

MOCK_PRODUCTS: list[dict[str, Any]] = [
    {
        "id": "demo-analytics",
        "name": "Pipeline Analytics Dashboard",
        "description": "Mock shipped product from embedded factory.",
        "category": "analytics",
        "tags": ["factory", "course"],
        "capabilities": [{"id": "metrics.summary", "price_per_call_usd": 0.01}],
    },
    {
        "id": "demo-orchestrator",
        "name": "Orchestrator Health Probe",
        "description": "Teaches GET /api/public/pipeline-status.",
        "category": "devtools",
        "tags": ["orchestrator"],
        "capabilities": [{"id": "pipeline.status", "price_per_call_usd": 0.0}],
    },
]


def _load_monorepo_flow() -> dict[str, Any]:
    here = Path(__file__).resolve()
    for root in here.parents:
        flow = root / "config" / "pipeline_flow.json"
        if flow.is_file():
            return json.loads(flow.read_text(encoding="utf-8"))
    return {
        "agent_flow": {
            "IDEA_RECEIVED": ["analyst", "MARKET_RESEARCHED"],
            "MARKET_RESEARCHED": ["pm", "SPEC_WRITTEN"],
            "SPEC_WRITTEN": ["architect", "ARCH_DESIGNED"],
            "ARCH_DESIGNED": ["developer", "CODE_COMMITTED"],
            "CODE_COMMITTED": ["qa", "QA_TESTING"],
            "QA_TESTING": ["devops", "COMPLETED"],
        },
        "stage_agents": [p[1] for p in PIPELINE_PHASES],
    }


def pipeline_flow_document() -> dict[str, Any]:
    return _load_monorepo_flow()


def next_state(current: str) -> tuple[str, str] | None:
    """Return (agent, next_state) for orchestrator stage transitions."""
    flow = pipeline_flow_document().get("agent_flow") or {}
    pair = flow.get(current)
    if not isinstance(pair, list) or len(pair) != 2:
        return None
    return str(pair[0]), str(pair[1])


def walk_to_ship(start: str = "IDEA_RECEIVED", *, max_steps: int = 32) -> list[dict[str, str]]:
    """Trace orchestrator path until COMPLETED or cap."""
    path: list[dict[str, str]] = [{"state": start, "agent": ""}]
    state = start
    for _ in range(max_steps):
        nxt = next_state(state)
        if nxt is None:
            break
        agent, new_state = nxt
        path.append({"state": new_state, "agent": agent})
        state = new_state
        if state in {"COMPLETED", "DEPLOYED_PRODUCTION"}:
            break
    return path


def resolve_factory_base_url() -> str | None:
    for key in ("COURSE_FACTORY_URL", "AIFACTORY_URL", "FACTORY_PUBLIC_URL"):
        val = (os.environ.get(key) or "").strip().rstrip("/")
        if val:
            return val
    return None


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _build_mock_app():
    from fastapi import FastAPI

    app = FastAPI(title="course-mock-factory")

    @app.get("/api/public/pipeline-status")
    async def pipeline_status() -> dict[str, int]:
        return dict(MOCK_STATUS)

    @app.get("/ai-market/products")
    async def products() -> dict[str, Any]:
        return {"products": MOCK_PRODUCTS, "count": len(MOCK_PRODUCTS), "protocol_version": "v0"}

    @app.get("/api/health")
    async def health() -> dict[str, Any]:
        return {"ok": True, "service": "course-mock-factory"}

    return app


class _ThreadedUvicorn:
    def __init__(self, app: Any, port: int) -> None:
        import uvicorn

        class _Server(uvicorn.Server):
            def install_signal_handlers(self) -> None:
                pass

        self.port = port
        self._server = _Server(
            uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
        )
        self._thread = threading.Thread(target=self._server.run, daemon=True)

    def start(self, timeout: float = 12.0) -> None:
        self._thread.start()
        base = f"http://127.0.0.1:{self.port}"
        deadline = time.time() + timeout
        while time.time() < deadline:
            if getattr(self._server, "started", False):
                try:
                    if httpx.get(base + "/api/health", timeout=1.0).status_code < 500:
                        return
                except Exception:
                    pass
            time.sleep(0.05)
        raise TimeoutError(f"mock factory on :{self.port} did not become ready")

    def stop(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5.0)


@dataclass
class FactoryClient:
    base_url: str
    timeout: float = 10.0
    source: str = "live"

    def get_pipeline_status(self) -> dict[str, Any]:
        with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
            r = client.get("/api/public/pipeline-status")
            r.raise_for_status()
            data = r.json()
        return {
            "products_in_pipeline": int(data.get("products_in_pipeline", 0)),
            "products_shipped": int(data.get("products_shipped", 0)),
            "source": self.source,
        }

    def list_products(self) -> dict[str, Any]:
        with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
            r = client.get("/ai-market/products")
            r.raise_for_status()
            data = r.json()
        products = data.get("products") or []
        return {
            "products": products,
            "count": int(data.get("count", len(products))),
            "source": self.source,
        }


@contextmanager
def factory_client(*, prefer_live: bool = True) -> Iterator[FactoryClient]:
    """Use live factory when reachable; otherwise start embedded mock."""
    live = resolve_factory_base_url() if prefer_live else None
    if live:
        try:
            httpx.get(live + "/api/public/pipeline-status", timeout=2.0).raise_for_status()
            yield FactoryClient(live, source="live")
            return
        except Exception:
            pass

    port = _free_port()
    server = _ThreadedUvicorn(_build_mock_app(), port)
    server.start()
    try:
        yield FactoryClient(f"http://127.0.0.1:{port}", source="mock")
    finally:
        server.stop()


def probe_factory() -> dict[str, Any]:
    """Capstone: pipeline heartbeat + shipped products in one call."""
    with factory_client() as client:
        status = client.get_pipeline_status()
        catalog = client.list_products()
    return {
        "status": status,
        "catalog": catalog,
        "phases": [p[0] for p in PIPELINE_PHASES],
    }


def exercise_check(module: str) -> None:
    if module == "m1":
        assert len(PIPELINE_PHASES) == 5
    elif module == "m2":
        with factory_client(prefer_live=False) as client:
            st = client.get_pipeline_status()
        assert "products_in_pipeline" in st
    elif module == "m3":
        with factory_client(prefer_live=False) as client:
            cat = client.list_products()
        assert cat["count"] >= 1
    elif module == "m4":
        path = walk_to_ship()
        states = [p["state"] for p in path]
        assert "IDEA_RECEIVED" in states
    elif module == "m5":
        out = probe_factory()
        assert out["status"]["source"] in {"live", "mock"}
        assert out["catalog"]["count"] >= 1
    else:
        raise ValueError(f"unknown module {module}")
