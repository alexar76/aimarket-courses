"""Live federation helpers for the peer-hubs course.

Prefer public GETs against a real hub (default ``https://modelmarket.dev``).
Nothing here invents peer catalogues or marks SIM traffic as LIVE.

Optional offline fixtures power unit tests without a network.
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

DEFAULT_HUB = (os.environ.get("COURSE_HUB_URL") or "https://modelmarket.dev").rstrip("/")
WELL_KNOWN_PATH = "/.well-known/ai-market.json"
PEERS_PATH = "/ai-market/v2/federation/peers"
PREVIEW_PATH = "/ai-market/v2/federation/preview"

# Teaching pipeline — matches aimarket-hub/docs/federation-admission.md
ANNOUNCE_PIPELINE: tuple[str, ...] = (
    "announce",  # knock — observation only
    "pending",  # quarantine row; nothing indexed
    "preview",  # signed manifest → preview table (search/invoke never read it)
    "approve",  # operator Approve or assay auto-admit
    "crawl",  # trusted peer indexed into the live catalogue
)


class FederationError(RuntimeError):
    """Raised when a live hub call fails or returns unexpected shape."""


def hub_base(url: str | None = None) -> str:
    return (url or DEFAULT_HUB).rstrip("/")


def fetch_json(url: str, *, timeout: float = 20.0) -> dict[str, Any]:
    """GET JSON from an absolute URL. Fail loudly — never invent a body."""
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "federation-peer-hubs-course/1.0"},
        method="GET",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read()
            status = getattr(resp, "status", None) or resp.getcode()
    except urllib.error.HTTPError as exc:
        raise FederationError(f"HTTP {exc.code} for {url}") from exc
    except urllib.error.URLError as exc:
        raise FederationError(f"network error for {url}: {exc.reason}") from exc
    if status and int(status) >= 400:
        raise FederationError(f"HTTP {status} for {url}")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FederationError(f"invalid JSON from {url}") from exc
    if not isinstance(data, dict):
        raise FederationError(f"expected JSON object from {url}, got {type(data).__name__}")
    return data


def well_known(hub_url: str | None = None, *, timeout: float = 20.0) -> dict[str, Any]:
    """``GET /.well-known/ai-market.json`` — name, counts, signer, hybrid signature."""
    base = hub_base(hub_url)
    return fetch_json(f"{base}{WELL_KNOWN_PATH}", timeout=timeout)


def list_peers(hub_url: str | None = None, *, timeout: float = 20.0) -> dict[str, Any]:
    """``GET /ai-market/v2/federation/peers`` — trusted peers + pending + door flags."""
    base = hub_base(hub_url)
    return fetch_json(f"{base}{PEERS_PATH}", timeout=timeout)


def preview_capabilities(
    peer_url: str,
    hub_url: str | None = None,
    *,
    limit: int = 50,
    timeout: float = 20.0,
) -> dict[str, Any]:
    """``GET /ai-market/v2/federation/preview?url=…`` — quarantined catalogue only."""
    base = hub_base(hub_url)
    q = urllib.parse.urlencode({"url": peer_url, "limit": str(limit)})
    return fetch_json(f"{base}{PREVIEW_PATH}?{q}", timeout=timeout)


def hybrid_signature_info(wk: dict[str, Any]) -> dict[str, Any]:
    """Summarise classical + PQ fields on a well-known document (no crypto verify)."""
    sig = wk.get("signature") if isinstance(wk.get("signature"), dict) else {}
    return {
        "signer_public_key": (wk.get("signer_public_key") or sig.get("public_key") or "")[:48],
        "algorithm": sig.get("algorithm") or "ed25519",
        "pq_algorithm": sig.get("pq_algorithm") or "",
        "has_pq": bool(sig.get("pq_algorithm") and sig.get("pq_public_key") and sig.get("pq_value")),
        "has_classical": bool(sig.get("value") or sig.get("signature")),
        "hybrid": bool(
            (sig.get("algorithm") or "ed25519")
            and sig.get("pq_algorithm")
            and (sig.get("value") or sig.get("signature"))
            and sig.get("pq_value")
        ),
    }


def peer_summary(peer: dict[str, Any], *, role: str = "trusted") -> dict[str, Any]:
    """Compare declared claims vs what this hub has observed/read.

    Trusted peers: ``capabilities_count`` is the indexed (read) count.
    Pending peers: ``declared_capabilities`` is the knock claim;
    ``preview_capabilities`` is what the quarantine table actually holds.
    """
    declared_meta = peer.get("declared") if isinstance(peer.get("declared"), dict) else {}
    pending_like = (
        role == "pending"
        or peer.get("status") == "pending"
        or peer.get("trusted") is False
    )
    if pending_like:
        declared = int(peer.get("declared_capabilities") or peer.get("capabilities_count") or 0)
        observed = int(peer.get("preview_capabilities") or 0)
        source_observed = "preview_table"
    else:
        if peer.get("declared_capabilities") is not None:
            declared = int(peer["declared_capabilities"])
        else:
            # Trusted row: indexed count is evidence; knock claim may be absent.
            declared = int(peer.get("capabilities_count") or 0)
        observed = int(peer.get("capabilities_count") or 0)
        source_observed = "indexed_catalogue"
    return {
        "url": peer.get("url") or "",
        "name": peer.get("name") or "",
        "trusted": bool(peer.get("trusted")),
        "status": peer.get("status") or "",
        "trust_score": peer.get("trust_score"),
        "declared_capabilities": declared,
        "observed_capabilities": observed,
        "observed_source": source_observed,
        "gap": declared - observed,
        "declared_id": declared_meta.get("id") or "",
        "canonical_id": peer.get("canonical_id") or "",
        "honesty_note": (
            "declared ≠ observed is normal until crawl/approve finishes; "
            "UI must show both, never only the knock claim"
        ),
    }


def open_vs_closed(peers_payload: dict[str, Any]) -> dict[str, Any]:
    """Teaching model: open door vs closed door; preview is a separate switch.

    An open door lets strangers announce into ``pending``. A closed door still
    keeps pending rows (seeds, crawler observations) — it does not erase
    quarantine. Preview/admission is independent of the door flag.
    """
    open_door = bool(peers_payload.get("open_federation"))
    pending = list(peers_payload.get("pending") or [])
    trusted = list(peers_payload.get("peers") or [])
    return {
        "door": "open" if open_door else "closed",
        "open_federation": open_door,
        "pending_count": int(peers_payload.get("pending_count") or len(pending)),
        "trusted_count": int(peers_payload.get("count") or len(trusted)),
        "observation_gossip": bool(peers_payload.get("observation_gossip", True)),
        "preview_independent_of_door": True,
        "teaching": {
            "open": "Strangers may POST /federation/announce → pending (not indexed).",
            "closed": "Announce may be refused, but pending peers can still exist from seeds/crawls.",
            "preview": "Preview quarantine is its own switch — search/invoke never read that table.",
            "approve": "Only Approve / assay auto-admit promotes pending → trusted + crawl.",
        },
    }


def preview_quarantine(
    hub_url: str | None = None,
    *,
    peers_payload: dict[str, Any] | None = None,
    timeout: float = 20.0,
) -> dict[str, Any]:
    """Explain preview quarantine and attach a live pending snapshot when present."""
    payload = peers_payload if peers_payload is not None else list_peers(hub_url, timeout=timeout)
    pending = list(payload.get("pending") or [])
    sample_preview: dict[str, Any] | None = None
    if pending:
        first = pending[0]
        url = str(first.get("url") or "")
        if url:
            try:
                sample_preview = preview_capabilities(url, hub_url, timeout=timeout)
            except FederationError:
                sample_preview = {
                    "error": "preview_endpoint_unreachable",
                    "url": url,
                    "quarantined": True,
                }
    return {
        "quarantined": True,
        "search_reads_preview_table": False,
        "invoke_reads_preview_table": False,
        "manifest_reads_preview_table": False,
        "rule": (
            "Signed manifests for pending peers land in peer_preview_capabilities. "
            "Search, routing, invoke, and the published manifest never read that table."
        ),
        "pending_count": int(payload.get("pending_count") or len(pending)),
        "pending_snapshot": [
            {
                "url": p.get("url"),
                "name": p.get("name"),
                "declared_capabilities": p.get("declared_capabilities"),
                "preview_capabilities": p.get("preview_capabilities"),
                "assay_verdict": p.get("assay_verdict"),
                "status": p.get("status") or "pending",
            }
            for p in pending[:5]
        ],
        "sample_preview": sample_preview,
        "empty_pending_note": (
            None
            if pending
            else "No pending peers right now — quarantine rule still holds; lab uses the live empty queue as evidence."
        ),
    }


def announce_checklist() -> list[dict[str, str]]:
    """Capstone checklist: announce → preview → approve → crawl."""
    labels = {
        "announce": "Knock (POST /federation/announce or inbound crawler) — observation only",
        "pending": "Peer sits in pending — capabilities_count stays 0 for indexing",
        "preview": "Optional preview: signed rows in quarantine table (never searchable)",
        "approve": "Operator Approve or assay pass + AUTO_ADMIT — trusted=true",
        "crawl": "Next crawl indexes the peer into the live catalogue",
    }
    return [{"step": s, "detail": labels[s]} for s in ANNOUNCE_PIPELINE]


def live_probe(hub_url: str | None = None, *, timeout: float = 20.0) -> dict[str, Any]:
    """One-shot live probe: well-known + peers summary for labs / capstone."""
    base = hub_base(hub_url)
    wk = well_known(base, timeout=timeout)
    peers = list_peers(base, timeout=timeout)
    door = open_vs_closed(peers)
    trusted = [peer_summary(p, role="trusted") for p in (peers.get("peers") or [])[:8]]
    pending = [peer_summary(p, role="pending") for p in (peers.get("pending") or [])[:8]]
    return {
        "hub": base,
        "live": True,
        "name": wk.get("name"),
        "hub_version": wk.get("hub_version"),
        "federated_capabilities_count": wk.get("federated_capabilities_count"),
        "signature": hybrid_signature_info(wk),
        "door": door,
        "trusted_peers": trusted,
        "pending_peers": pending,
        "checklist": announce_checklist(),
    }


# --- Offline teaching fixtures (unit tests / no-network demos) -----------------

FIXTURE_WELL_KNOWN: dict[str, Any] = {
    "name": "fixture.hub.example",
    "hub_version": "3.2.0",
    "federated_capabilities_count": 12,
    "signer_public_key": "fixture-ed25519-pubkey",
    "signature": {
        "algorithm": "ed25519",
        "public_key": "fixture-ed25519-pubkey",
        "value": "fixture-sig",
        "pq_algorithm": "ml-dsa-65",
        "pq_public_key": "fixture-pq-pubkey",
        "pq_value": "fixture-pq-sig",
    },
}

FIXTURE_PEERS: dict[str, Any] = {
    "open_federation": True,
    "observation_gossip": True,
    "count": 2,
    "pending_count": 1,
    "peers": [
        {
            "url": "https://atlas.example",
            "name": "ATLAS fixture",
            "capabilities_count": 11,
            "trust_score": 0.48,
            "trusted": True,
            "status": "active",
            "canonical_id": "atlas",
            "declared": {"id": "atlas.map", "hub_version": "0.1.0"},
        },
        {
            "url": "https://gaia.example",
            "name": "GAIA fixture",
            "capabilities_count": 40,
            "trust_score": 0.45,
            "trusted": True,
            "status": "active",
            "canonical_id": "gaia",
            "declared": {"id": "gaia.gateway", "hub_version": "0.1.0"},
        },
    ],
    "pending": [
        {
            "url": "https://stranger.example",
            "name": "Stranger hub",
            "status": "pending",
            "trusted": False,
            "declared_capabilities": 7,
            "preview_capabilities": 3,
            "assay_verdict": None,
            "declared": {"id": "stranger.hub"},
        }
    ],
}


def fixture_probe() -> dict[str, Any]:
    """Deterministic offline probe — labelled fixture, never presented as LIVE."""
    door = open_vs_closed(FIXTURE_PEERS)
    return {
        "hub": "fixture://offline",
        "live": False,
        "name": FIXTURE_WELL_KNOWN["name"],
        "hub_version": FIXTURE_WELL_KNOWN["hub_version"],
        "federated_capabilities_count": FIXTURE_WELL_KNOWN["federated_capabilities_count"],
        "signature": hybrid_signature_info(FIXTURE_WELL_KNOWN),
        "door": door,
        "trusted_peers": [peer_summary(p, role="trusted") for p in FIXTURE_PEERS["peers"]],
        "pending_peers": [peer_summary(p, role="pending") for p in FIXTURE_PEERS["pending"]],
        "quarantine": preview_quarantine(peers_payload=FIXTURE_PEERS),
        "checklist": announce_checklist(),
    }
