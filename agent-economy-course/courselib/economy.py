"""Sandbox-first bridge to the real AIMarket economy via the ``aimarket-agent`` SDK.

Boots a local Hub + stub Factory for labs that need payment channels, escrow,
and the full autonomous ``hire()`` cycle — zero infra and zero real money.

Graduate path: set ``COURSE_HUB_URL`` to a real hub and the same lab code runs live.
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


class SandboxUnavailable(RuntimeError):
    """Raised when the optional ``aimarket-agent`` SDK is not installed.

    The capstone (M6) is the only part of the course that needs the full SDK.
    Labs and exercises that rely on ``hub-lite`` keep working without it, so
    callers can catch this and degrade gracefully (skip + clear message) rather
    than crashing with a deep ``ModuleNotFoundError``.
    """


_INSTALL_HINT = (
    "The capstone needs the aimarket-agent SDK. Install it with:\n"
    "    pip install -e \".[sandbox]\"   (~50 MB, git clones — run once)"
)


def _try_path_bootstrap() -> None:
    """Dev fallback: add sibling monorepo packages to sys.path if present."""
    here = Path(__file__).resolve()
    repo_root = next((p for p in here.parents if (p / "aimarket-agent").is_dir()), here.parents[3])
    for pkg in ("aimarket-agent", "aimarket-hub"):
        p = repo_root / pkg
        if p.is_dir() and str(p) not in sys.path:
            sys.path.insert(0, str(p))


def sdk_available() -> bool:
    """True if the full ``aimarket-agent``/``aimarket-hub`` SDK can be imported.

    Tries a normal import first, then the in-repo path bootstrap. Lets the
    capstone check up front and skip cleanly when the SDK is absent.
    """
    import importlib.util

    def _present() -> bool:
        return all(importlib.util.find_spec(m) for m in ("aimarket_agent", "aimarket_hub"))

    if _present():
        return True
    _try_path_bootstrap()
    importlib.invalidate_caches()
    return _present()


def _ensure_imports() -> None:
    try:
        import aimarket_agent  # noqa: F401
        import aimarket_hub  # noqa: F401
        return
    except ImportError:
        pass
    _try_path_bootstrap()
    try:
        import aimarket_agent  # noqa: F401
        import aimarket_hub  # noqa: F401
    except ImportError as exc:  # SDK genuinely absent — fail with a clear message
        raise SandboxUnavailable(_INSTALL_HINT) from exc


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _ThreadedUvicorn:
    def __init__(self, app: Any, port: int):
        import uvicorn

        class _Server(uvicorn.Server):
            def install_signal_handlers(self) -> None:
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
    from fastapi import FastAPI

    app = FastAPI(title="course-sandbox-factory")

    @app.get("/api/health")
    async def health() -> dict:
        return {"ok": True, "service": "course-sandbox-factory"}

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


class SandboxEconomy:
    """Thin wrapper over the real ``aimarket-agent`` SDK."""

    def __init__(self, base_url: str, budget: float = 3.0, timeout: float = 30.0):
        _ensure_imports()
        from aimarket_agent import AIMarketAgent

        self.base_url = base_url.rstrip("/")
        self._agent = AIMarketAgent(base_url=self.base_url, budget=budget, timeout=timeout)

    def discover(self, query: str, limit: int = 8) -> list[dict[str, Any]]:
        return self._agent.discover(query, limit=limit)

    def hire(self, task: str) -> dict[str, Any]:
        return self._agent.run(task)

    def invoke(self, product_id: str, capability_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._agent.invoke_single(product_id, capability_id, payload)

    def capital_listings(self) -> dict[str, Any]:
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
    _ensure_imports()
    prev_env = {
        k: os.environ.get(k)
        for k in ("AIFACTORY_PUBLIC_URL", "ACEX_AUTO_IPO", "AIFACTORY_DATA_ROOT")
    }
    with tempfile.TemporaryDirectory(prefix="course-sandbox-") as tmpdir:
        tmp = Path(tmpdir)
        os.environ["AIFACTORY_DATA_ROOT"] = str(tmp)
        factory = _ThreadedUvicorn(_build_factory_stub(), _free_port())
        factory.start(ready_path="/api/health")
        os.environ["AIFACTORY_PUBLIC_URL"] = f"http://127.0.0.1:{factory.port}"

        hub = _ThreadedUvicorn(_build_hub_app(tmp), _free_port())
        hub.start(ready_path="/.well-known/ai-market.json")

        econ = SandboxEconomy(f"http://127.0.0.1:{hub.port}", budget=budget)
        try:
            yield econ
        finally:
            econ.close()
            hub.stop()
            factory.stop()
            for k, v in prev_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


def connect(base_url: Optional[str] = None, budget: float = 3.0) -> SandboxEconomy:
    url = base_url or os.environ.get("COURSE_HUB_URL")
    if not url:
        raise RuntimeError(
            "No hub URL. Use `with embedded_sandbox() as econ:` for a local "
            "sandbox, or set COURSE_HUB_URL / pass base_url for a live hub."
        )
    return SandboxEconomy(url, budget=budget)
