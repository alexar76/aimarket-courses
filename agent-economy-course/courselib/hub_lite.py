"""Lightweight AIMarket-compatible hub for economy labs (~5 MB deps, no git clones).

Uses only uvicorn + httpx. For the full SDK cycle (lab06 capstone) use
``courselib.economy.embedded_sandbox()``.
"""

from __future__ import annotations

import contextlib
import json
import os
import secrets
import socket
import threading
import time
from datetime import datetime, timezone
from typing import Any, Iterator

import httpx

from courselib.trust import sign_receipt, verify_receipt

_HUB_SECRET = os.environ.get("COURSE_HUB_LITE_SECRET", "course-hub-lite-dev-secret")
_SIGNER_PUBLIC_KEY = "Y291cnNlLWh1Yi1saXRlLWRlbW8ta2V5"  # demo base64 key
_CAPABILITIES: list[dict[str, Any]] = [
    {
        "product_id": "prod-translate",
        "capability_id": "translate.multi@v2",
        "price_per_call_usd": 0.01,
        "description": "Translate text (course demo)",
    },
    {
        "product_id": "prod-summarize",
        "capability_id": "summarize@v1",
        "price_per_call_usd": 0.005,
        "description": "Summarize text (course demo)",
    },
]
_CHANNELS: dict[str, dict[str, Any]] = {}
_TRUST_SCORES: dict[str, float] = {}


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
        raise TimeoutError(f"hub-lite on :{self.port} did not become ready")

    def stop(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5.0)


def _manifest_for(base_url: str) -> dict[str, Any]:
    tools = [
        {
            "name": c["capability_id"],
            "description": c["description"],
            "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}},
            "price_per_call_usd": c["price_per_call_usd"],
            "product_id": c["product_id"],
            "capability_id": c["capability_id"],
        }
        for c in _CAPABILITIES
    ]
    return {
        "protocol_version": "v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": base_url,
        "capabilities_count": len(tools),
        "tools": tools,
        "signature": {
            "algorithm": "ed25519",
            "public_key": _SIGNER_PUBLIC_KEY,
            "value": "course-demo-signature",
        },
    }


def _build_app(port_holder: list[int]) -> Any:
    from fastapi import FastAPI

    app = FastAPI(title="course-hub-lite")

    def base_url() -> str:
        return f"http://127.0.0.1:{port_holder[0]}"

    @app.get("/.well-known/ai-market.json")
    async def well_known() -> dict:
        return {
            "name": "course-hub-lite",
            "protocol_versions": ["v2"],
            "hub_version": "0.1.0-course",
            "manifest_url": base_url() + "/ai-market/manifest",
            "capabilities_count": len(_CAPABILITIES),
            "products_count": len({c["product_id"] for c in _CAPABILITIES}),
            "supported_chains": ["base"],
            "supported_tokens": ["USDC"],
            "signer_public_key": _SIGNER_PUBLIC_KEY,
        }

    @app.get("/ai-market/manifest")
    async def manifest() -> dict:
        return _manifest_for(base_url())

    @app.get("/ai-market/v2/discover")
    async def discover(q: str = "", limit: int = 8) -> dict:
        qlow = q.lower()
        hits = [
            c for c in _CAPABILITIES
            if not qlow or qlow in c["capability_id"].lower() or qlow in c["description"].lower()
        ]
        return {"matches": hits[:limit]}

    @app.post("/ai-market/v2/invoke")
    async def invoke(body: dict) -> dict:
        product_id = body.get("product_id", "")
        capability_id = body.get("capability_id", "")
        payload = body.get("payload") or {}
        cap = next(
            (c for c in _CAPABILITIES if c["product_id"] == product_id and c["capability_id"] == capability_id),
            None,
        )
        if cap is None:
            return {"success": False, "error": "capability not found"}
        text = payload.get("input") or payload.get("text") or ""
        output = {
            "output": {
                "served_by": "course-hub-lite",
                "capability": capability_id,
                "product": product_id,
                "echo": text,
            }
        }
        receipt = sign_receipt(
            {
                "product_id": product_id,
                "capability_id": capability_id,
                "price_usd": cap["price_per_call_usd"],
                "payload_hash": json.dumps(payload, sort_keys=True),
            },
            _HUB_SECRET,
        )
        return {
            "success": True,
            "price_usd": cap["price_per_call_usd"],
            "result": output,
            "receipt": receipt,
        }

    @app.post("/ai-market/v2/channel/open")
    async def channel_open(body: dict) -> dict:
        budget = float(body.get("budget_usd", 1.0))
        channel_id = "ch_" + secrets.token_hex(6)
        _CHANNELS[channel_id] = {"budget_usd": budget, "spent_usd": 0.0, "open": True}
        return {"success": True, "channel_id": channel_id, "budget_usd": budget}

    @app.post("/ai-market/v2/channel/close")
    async def channel_close(body: dict) -> dict:
        channel_id = body.get("channel_id", "")
        ch = _CHANNELS.get(channel_id)
        if ch is None:
            return {"success": False, "error": "channel not found"}
        ch["open"] = False
        return {
            "success": True,
            "channel_id": channel_id,
            "spent_usd": ch["spent_usd"],
            "refund_usd": max(0.0, ch["budget_usd"] - ch["spent_usd"]),
        }

    @app.post("/ai-market/v2/capabilities/register")
    async def register_capability(body: dict) -> dict:
        required = ("product_id", "capability_id", "price_per_call_usd", "description")
        missing = [k for k in required if k not in body]
        if missing:
            return {"success": False, "error": f"missing fields: {', '.join(missing)}"}
        entry = {
            "product_id": body["product_id"],
            "capability_id": body["capability_id"],
            "price_per_call_usd": float(body["price_per_call_usd"]),
            "description": body["description"],
        }
        _CAPABILITIES[:] = [c for c in _CAPABILITIES if c["capability_id"] != entry["capability_id"]]
        _CAPABILITIES.append(entry)
        return {"success": True, "capability": entry}

    @app.get("/ai-market/v2/trust/graph")
    async def trust_graph() -> dict:
        return {"scores": dict(_TRUST_SCORES)}

    @app.post("/ai-market/v2/trust/record")
    async def trust_record(body: dict) -> dict:
        product_id = body.get("product_id", "")
        verified = bool(body.get("verified"))
        delta = 0.05 if verified else -0.1
        prev = _TRUST_SCORES.get(product_id, 0.5)
        score = max(0.0, min(1.0, prev + delta))
        _TRUST_SCORES[product_id] = score
        return {"success": True, "product_id": product_id, "trust_score": score}

    return app


class HubLiteClient:
    """Thin HTTP client for the embedded hub-lite."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def well_known(self) -> dict[str, Any]:
        return httpx.get(self.base_url + "/.well-known/ai-market.json", timeout=5.0).json()

    def manifest(self) -> dict[str, Any]:
        return httpx.get(self.base_url + "/ai-market/manifest", timeout=5.0).json()

    def discover(self, query: str, limit: int = 8) -> list[dict[str, Any]]:
        r = httpx.get(
            self.base_url + "/ai-market/v2/discover",
            params={"q": query, "limit": limit},
            timeout=5.0,
        )
        return r.json().get("matches", [])

    def invoke(self, product_id: str, capability_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        r = httpx.post(
            self.base_url + "/ai-market/v2/invoke",
            json={"product_id": product_id, "capability_id": capability_id, "payload": payload},
            timeout=10.0,
        )
        return r.json()

    def open_channel(self, budget_usd: float = 1.0) -> dict[str, Any]:
        r = httpx.post(
            self.base_url + "/ai-market/v2/channel/open",
            json={"budget_usd": budget_usd},
            timeout=5.0,
        )
        return r.json()

    def close_channel(self, channel_id: str) -> dict[str, Any]:
        r = httpx.post(
            self.base_url + "/ai-market/v2/channel/close",
            json={"channel_id": channel_id},
            timeout=5.0,
        )
        return r.json()

    def register_capability(
        self,
        product_id: str,
        capability_id: str,
        price_per_call_usd: float,
        description: str,
    ) -> dict[str, Any]:
        r = httpx.post(
            self.base_url + "/ai-market/v2/capabilities/register",
            json={
                "product_id": product_id,
                "capability_id": capability_id,
                "price_per_call_usd": price_per_call_usd,
                "description": description,
            },
            timeout=5.0,
        )
        return r.json()

    def trust_graph(self) -> dict[str, float]:
        return httpx.get(self.base_url + "/ai-market/v2/trust/graph", timeout=5.0).json().get("scores", {})

    def record_trust(self, product_id: str, verified: bool) -> dict[str, Any]:
        r = httpx.post(
            self.base_url + "/ai-market/v2/trust/record",
            json={"product_id": product_id, "verified": verified},
            timeout=5.0,
        )
        return r.json()

    def verify_receipt(self, receipt: dict[str, Any]) -> bool:
        return verify_receipt(receipt, _HUB_SECRET)


@contextlib.contextmanager
def embedded_hub_lite() -> Iterator[HubLiteClient]:
    """Boot hub-lite in-process and yield a client (~2 s cold start)."""
    port_holder: list[int] = [0]
    server = _ThreadedUvicorn(_build_app(port_holder), _free_port())
    port_holder[0] = server.port
    server.start(ready_path="/.well-known/ai-market.json")
    client = HubLiteClient(f"http://127.0.0.1:{server.port}")
    try:
        yield client
    finally:
        server.stop()
