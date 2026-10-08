"""Trust, verification & provenance helpers (M4).

Stdlib-only signed receipts for teaching verification without heavy SDK deps.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from typing import Any


def sign_receipt(payload: dict[str, Any], secret: str) -> dict[str, Any]:
    """Attach ``nonce`` and HMAC-SHA256 ``signature`` to a receipt payload."""
    body = dict(payload)
    body["nonce"] = secrets.token_hex(8)
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    sig = hmac.new(secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()
    body["signature"] = sig
    return body


def verify_receipt(receipt: dict[str, Any], secret: str) -> bool:
    """Return True when the receipt signature matches the payload."""
    if "signature" not in receipt or "nonce" not in receipt:
        return False
    sig = receipt["signature"]
    body = {k: v for k, v in receipt.items() if k != "signature"}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    expected = hmac.new(secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)


def tamper_receipt(receipt: dict[str, Any], **changes: Any) -> dict[str, Any]:
    """Demo helper: mutate fields without re-signing (should fail verification)."""
    bad = dict(receipt)
    bad.update(changes)
    return bad


class TrustGraph:
    """Minimal in-memory trust graph fed by verified receipts (LUMEN-style demo)."""

    def __init__(self) -> None:
        self._scores: dict[str, float] = {}
        self._events: list[dict[str, Any]] = []

    def record(self, product_id: str, price_usd: float, verified: bool) -> float:
        """Bump trust on verified paid calls; decay on failed verification."""
        delta = 0.05 if verified else -0.1
        prev = self._scores.get(product_id, 0.5)
        score = max(0.0, min(1.0, prev + delta))
        self._scores[product_id] = score
        self._events.append(
            {"product_id": product_id, "price_usd": price_usd, "verified": verified, "score": score}
        )
        return score

    def score(self, product_id: str) -> float:
        return self._scores.get(product_id, 0.5)

    def graph(self) -> dict[str, float]:
        return dict(self._scores)

    def events(self) -> list[dict[str, Any]]:
        return list(self._events)
