"""Validate AIMarket v2 well-known and capability manifest JSON shapes.

Conceptually aligned with ``aimarket-protocol/schemas/*.json``. Uses structural
checks only — no jsonschema dependency — so labs run in minimal environments.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urlparse

_PROTOCOL_VERSIONS = frozenset({"v1", "v2", "mcp"})


def validate_well_known(data: dict[str, Any]) -> list[str]:
    """Validate ``/.well-known/ai-market.json``. Empty list means valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["well-known must be a JSON object"]

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("name is required (non-empty string)")

    versions = data.get("protocol_versions")
    if not isinstance(versions, list) or not versions:
        errors.append("protocol_versions is required (non-empty array)")
    elif not all(isinstance(v, str) and v in _PROTOCOL_VERSIONS for v in versions):
        errors.append("protocol_versions must contain v1, v2, and/or mcp")

    manifest_url = data.get("manifest_url")
    if not isinstance(manifest_url, str) or not _looks_like_url(manifest_url):
        errors.append("manifest_url is required (valid URI string)")

    signer = data.get("signer_public_key")
    if not isinstance(signer, str) or len(signer) < 8:
        errors.append("signer_public_key is required (base64 public key string)")

    for key in ("products_count", "capabilities_count", "federated_capabilities_count"):
        val = data.get(key)
        if val is not None and (not isinstance(val, int) or val < 0):
            errors.append(f"{key} must be a non-negative integer")

    federation = data.get("federation")
    if federation is not None:
        if not isinstance(federation, dict):
            errors.append("federation must be an object")
        else:
            fee = federation.get("routing_fee_bps")
            if fee is not None and (not isinstance(fee, int) or fee < 0 or fee > 10000):
                errors.append("federation.routing_fee_bps must be 0..10000")

    return errors


def validate_manifest(data: dict[str, Any]) -> list[str]:
    """Validate ``GET /ai-market/manifest`` response. Empty list means valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest must be a JSON object"]

    pv = data.get("protocol_version")
    if pv not in ("v1", "v2"):
        errors.append("protocol_version is required (v1 or v2)")

    generated = data.get("generated_at")
    if not isinstance(generated, str):
        errors.append("generated_at is required (ISO-8601 string)")
    else:
        try:
            datetime.fromisoformat(generated.replace("Z", "+00:00"))
        except ValueError:
            errors.append("generated_at must be ISO-8601")

    tools = data.get("tools")
    if not isinstance(tools, list):
        errors.append("tools array is required")
    else:
        for i, tool in enumerate(tools):
            if not isinstance(tool, dict):
                errors.append(f"tools[{i}] must be an object")
                continue
            for req in ("name", "description", "input_schema"):
                if req not in tool:
                    errors.append(f"tools[{i}].{req} is required")
            price = tool.get("price_per_call_usd")
            if price is not None and (not isinstance(price, (int, float)) or price < 0):
                errors.append(f"tools[{i}].price_per_call_usd must be >= 0")

    signature = data.get("signature")
    if not isinstance(signature, dict):
        errors.append("signature object is required")
    else:
        for req in ("algorithm", "public_key", "value"):
            if req not in signature:
                errors.append(f"signature.{req} is required")
        if signature.get("algorithm") not in (None, "ed25519"):
            errors.append("signature.algorithm must be ed25519")

    return errors


def is_valid_well_known(data: dict[str, Any]) -> bool:
    return not validate_well_known(data)


def is_valid_manifest(data: dict[str, Any]) -> bool:
    return not validate_manifest(data)


def _looks_like_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)
