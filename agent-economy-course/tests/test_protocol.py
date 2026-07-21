"""Tests for Protocol v2 JSON shape validation."""

from courselib.protocol import (
    is_valid_manifest,
    is_valid_well_known,
    validate_manifest,
    validate_well_known,
)


def test_valid_well_known_sample():
    data = {
        "name": "demo-hub",
        "protocol_versions": ["v2"],
        "manifest_url": "https://example.com/ai-market/manifest",
        "signer_public_key": "Y291cnNlLWh1Yi1saXRlLWRlbW8ta2V5",
    }
    assert is_valid_well_known(data)
    assert not validate_well_known(data)


def test_well_known_missing_required():
    assert validate_well_known({})
    assert "name" in " ".join(validate_well_known({}))


def test_valid_manifest_sample():
    data = {
        "protocol_version": "v2",
        "generated_at": "2026-01-01T00:00:00+00:00",
        "tools": [
            {
                "name": "translate@v1",
                "description": "translate",
                "input_schema": {"type": "object"},
                "price_per_call_usd": 0.01,
            }
        ],
        "signature": {"algorithm": "ed25519", "public_key": "pk", "value": "sig"},
    }
    assert is_valid_manifest(data)


def test_manifest_rejects_bad_protocol_version():
    data = {
        "protocol_version": "v9",
        "generated_at": "2026-01-01T00:00:00+00:00",
        "tools": [],
        "signature": {"algorithm": "ed25519", "public_key": "pk", "value": "sig"},
    }
    assert validate_manifest(data)
