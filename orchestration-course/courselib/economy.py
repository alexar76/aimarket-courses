"""Sandbox-first bridge to the real AIMarket economy via the ``aimarket-agent`` SDK.

The course teaches neutral orchestration patterns; this module is the *lab
environment* where those patterns run against the actual economy — discovery,
payment channels, escrow, signed receipts — with **zero infra and zero real
money**.

``embedded_sandbox()`` boots a real AIMarket Hub plus a tiny stub Factory in
background threads (uvicorn), seeds demo capabilities, and hands you a
``SandboxEconomy`` wrapping the genuine SDK pointed at it. Nothing leaves the
machine; no wallet, no testnet, no spend.

Graduate path: set ``COURSE_HUB_URL`` to a real hub and the same lab code runs
against the live federation — that is the whole point of embedding the SDK
rather than a toy client.
"""

from __future__ import annotations

import contextlib
import os
import socket
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Iterator, Optional

import httpx


# ── Make the SDK + hub importable whether pip-installed or run from the repo ──

def _ensure_imports() -> None:
    try:
        import aimarket_agent  # noqa: F401
        import aimarket_hub  # noqa: F401
        return
    except ImportError:
        pass
    # Dev fallback: add sibling monorepo packages to sys.path.
    here = Path(__file__).resolve()
    repo_root = next((p for p in here.parents if (p / "aimarket-agent").is_dir()), here.parents[3])
    for pkg in ("aimarket-agent", "aimarket-hub"):
        p = repo_root / pkg
        if p.is_dir() and str(p) not in sys.path:
            sys.path.insert(0, str(p))


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _ThreadedUvicorn:
    """Run a uvicorn server in a daemon thread with clean start/stop."""

    def __init__(self, app: Any, port: int):
        import uvicorn

        class _Server(uvicorn.Server):
            def install_signal_handlers(self) -> None:  # no signals off the main thread
                pass

        self.port = port
        self._server = _Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
        self._thread = threading.Thread(target=self._server.run, daemon=True)

    def start(self, ready_path: str = "", timeout: float = 15.0) -> None:
        self._thread.start()
        deadline = time.time() + timeout
        base = f"http://127.0.0.1:{self.port}"
        while time.time() < deadline:
            if getattr(self._server, "started", False):
                if not ready_path:
                    return
                try:
                    if httpx.get(base + ready_path, timeout=1.0).status_code < 500:
                        return
                except Exception:
                    pass
            time.sleep(0.05)
        raise TimeoutError(f"server on :{self.port} did not become ready")

    def stop(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5.0)


def _build_hub_app(tmp: Path) -> Any:
    from aimarket_hub.api import create_app
    from aimarket_hub.config import HubConfig
    from aimarket_hub.database import HubDatabase
    from aimarket_hub.signing import Signer

    config = HubConfig()
    config.db_path = str(tmp / "hub.db")
    config.signing_key_path = str(tmp / "hub_key")
    db = HubDatabase(config.db_path)
    signer = Signer(config.signing_key_path)
    return create_app(config=config, db=db, signer=signer)


def _build_factory_stub() -> Any:
    """A minimal stand-in for the AI-Factory execution backend (deterministic)."""
    from fastapi import FastAPI

    app = FastAPI(title="course-sandbox-factory")

    @app.get("/api/health")
    async def health() -> dict:
        return {"ok": True, "service": "course-sandbox-factory"}

    # `payload: dict` is taken from the JSON body (resolves cleanly under
    # `from __future__ import annotations`, unlike a locally-imported Request type).
    @app.post("/capabilities/{product_id}/{capability_id}/invoke")
    async def invoke(product_id: str, capability_id: str, payload: dict) -> dict:
        return {
            "output": {
                "served_by": "course-sandbox-factory",
                "capability": capability_id,
                "product": product_id,
                "echo": payload.get("input"),
            }
        }

    return app



def _route_seeds_to_factory(db_path: Path, factory_url: str) -> int:
    """Give the hub's seeded capabilities an invoke URL on the sandbox factory.

    The hub only lists what it can execute (``fulfillment.capability_is_fulfillable``,
    hub 2026-07-27): a seeded row with no ``invoke_url`` is still callable through the
    factory passthrough, but search no longer offers it — so ``discover()`` and ``hire()``
    found nothing. Pointing each row at the stub factory makes it a real, executable
    listing again, exactly what a published capability looks like on a live hub — so it
    is no longer a demo row either (search hides those unless asked).
    """
    import sqlite3

    conn = sqlite3.connect(str(db_path), timeout=10)
    try:
        cur = conn.execute(
            "UPDATE capabilities SET invoke_url = ? || '/capabilities/' || product_id || '/' "
            "|| capability_id || '/invoke', is_demo = 0 WHERE COALESCE(source_hub, 'local') IN ('local', '') "
            "AND COALESCE(invoke_url, '') = ''",
            (factory_url.rstrip("/"),),
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


class SandboxEconomy:
    """Thin, friendly wrapper over the real ``aimarket-agent`` SDK.

    Every method drives the genuine Protocol v2 client — only the *backend* is a
    local sandbox. Swap ``base_url`` for a real hub and the same calls go live.
    """

    def __init__(self, base_url: str, budget: float = 3.0, timeout: float = 30.0,
                 api_key: str = ""):
        _ensure_imports()
        from aimarket_agent import AIMarketAgent

        self.base_url = base_url.rstrip("/")
        # A key pays priced calls from its prepaid balance (X-API-Key). Passed only when
        # set, so an SDK older than 2.3.0 still runs the keyless sandbox labs.
        extra = {"api_key": api_key} if api_key else {}
        self._agent = AIMarketAgent(base_url=self.base_url, budget=budget, timeout=timeout, **extra)

    def discover(self, query: str, limit: int = 8) -> list[dict[str, Any]]:
        """Find capabilities (no spend) — M4: discovery."""
        return self._agent.discover(query, limit=limit)

    def hire(self, task: str) -> dict[str, Any]:
        """Full autonomous cycle: discover → channel → invoke → settle (M3/M8)."""
        return self._agent.run(task)

    def invoke(self, product_id: str, capability_id: str, payload: dict[str, Any],
               source_hub: Optional[str] = None) -> dict[str, Any]:
        """Invoke one capability directly (M1) — returns the signed-receipt envelope."""
        # On a live hub most capabilities are federated: invoked as "local" the hub refuses
        # them and names the source_hub to use. Ask /search for it, as a buyer would.
        if source_hub is None:
            source_hub = self._source_hub_for(product_id, capability_id)
        return self._agent.invoke_single(product_id, capability_id, payload, source_hub=source_hub)

    def _source_hub_for(self, product_id: str, capability_id: str) -> str:
        for match in self._agent.discover(capability_id, limit=20):
            if match.get("capability_id") == capability_id and match.get("product_id") == product_id:
                return str(match.get("source_hub") or "local")
        return "local"

    def capital_listings(self) -> dict[str, Any]:
        """Read ACEX capital state (CapShares / revenue) — advanced track (M8).

        Degrades gracefully: a hub that can't serve capital state (non-2xx or a
        non-JSON body) yields an empty listing instead of crashing the lab.
        """
        r = httpx.get(self.base_url + "/ai-market/v2/capital/listings", timeout=5.0)
        if r.status_code != 200:
            return {"listings": [], "error": f"hub returned {r.status_code}"}
        try:
            return r.json()
        except ValueError:
            return {"listings": [], "error": "non-JSON capital response"}

    def well_known(self) -> dict[str, Any]:
        return httpx.get(self.base_url + "/.well-known/ai-market.json", timeout=5.0).json()

    def close(self) -> None:
        self._agent.close()


@contextlib.contextmanager
def embedded_sandbox(budget: float = 3.0) -> Iterator[SandboxEconomy]:
    """Boot a local Hub + Factory and yield a SandboxEconomy wired to them.

    Fully self-contained: temp DB, in-process servers, deterministic factory.
    """
    _ensure_imports()
    prev_env = {
        k: os.environ.get(k)
        for k in ("AIFACTORY_PUBLIC_URL", "ACEX_AUTO_IPO", "AIFACTORY_DATA_ROOT", "AIMARKET_ALLOW_LOCAL_PUBLISH")
    }
    servers: list[_ThreadedUvicorn] = []
    with tempfile.TemporaryDirectory(prefix="course-sandbox-") as tmpdir:
        # Everything from the first environment change on is undone in the `finally`, even
        # when a server fails to start: a failed boot must not leave the switches set.
        try:
            tmp = Path(tmpdir)
            # Keep ALL hub state inside the sandbox tmpdir. Without this the ACEX
            # ledger (capital_listings) resolves its SQLite path to the Docker-only
            # default /app/data, fails to mkdir, and the endpoint 500s — crashing
            # lab08. Pointing the data root at the temp dir keeps the lab offline
            # and self-contained.
            os.environ["AIFACTORY_DATA_ROOT"] = str(tmp)
            # The stub factory listens on 127.0.0.1; the hub refuses loopback provider URLs
            # unless told this is a local sandbox (its own dev switch, restored on exit).
            os.environ["AIMARKET_ALLOW_LOCAL_PUBLISH"] = "1"
            factory = _ThreadedUvicorn(_build_factory_stub(), _free_port())
            servers.append(factory)
            factory.start(ready_path="/api/health")
            # Hub must see the factory URL when it handles invokes.
            os.environ["AIFACTORY_PUBLIC_URL"] = f"http://127.0.0.1:{factory.port}"

            hub = _ThreadedUvicorn(_build_hub_app(tmp), _free_port())
            servers.append(hub)
            hub.start(ready_path="/.well-known/ai-market.json")
            _route_seeds_to_factory(tmp / "hub.db", f"http://127.0.0.1:{factory.port}")
            econ = SandboxEconomy(f"http://127.0.0.1:{hub.port}", budget=budget)
            try:
                yield econ
            finally:
                econ.close()
        finally:
            for server in reversed(servers):
                server.stop()
            for k, v in prev_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


def connect(base_url: Optional[str] = None, budget: float = 3.0,
            api_key: Optional[str] = None) -> SandboxEconomy:
    """Connect to a hub by URL (or ``COURSE_HUB_URL``) for graduate/live runs.

    For self-contained labs prefer ``with embedded_sandbox() as econ:``.
    """
    url = base_url or os.environ.get("COURSE_HUB_URL")
    if not url:
        raise RuntimeError(
            "No hub URL. Use `with embedded_sandbox() as econ:` for a local "
            "sandbox, or set COURSE_HUB_URL / pass base_url for a live hub."
        )
    # On a live hub a priced call needs payment: a key from <hub>/start, topped up with
    # USDC, pays it from a prepaid balance. Without one the hub answers payment_required.
    key = api_key if api_key is not None else os.environ.get("COURSE_API_KEY", "")
    return SandboxEconomy(url, budget=budget, api_key=key.strip())
