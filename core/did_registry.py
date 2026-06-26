#!/usr/bin/env python3
"""
did_registry.py — Canonical DID→public_key resolver for the arifOS federation.

Mount point: /root/secrets/did/registry.json → /root/AAA/secrets/did/registry.json
Importable by every organ. No key generation — just resolution and verification.

Usage:
    from core.did_registry import resolve_did, verify_signature, load_registry

    pubkey = resolve_did("did:arif:geox")
    ok     = verify_signature(data, signature_hex, "did:arif:a-forge")
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from nacl.exceptions import BadSignatureError
from nacl.encoding import HexEncoder
from nacl.signing import VerifyKey

# Canonical registry path — symlinked to /root/secrets/did/registry.json
REGISTRY_PATH = Path("/root/secrets/did/registry.json")
FALLBACK_PATH = Path(__file__).parent.parent / "secrets" / "did" / "registry.json"


def _find_registry() -> Path:
    if REGISTRY_PATH.exists():
        return REGISTRY_PATH
    if FALLBACK_PATH.exists():
        return FALLBACK_PATH
    raise FileNotFoundError(
        "DID registry not found at /root/secrets/did/registry.json. "
        "Run: python auth/gen_did.py"
    )


def load_registry() -> dict:
    """Return the full DID registry dict."""
    return json.loads(_find_registry().read_text())


def resolve_did(did: str) -> str:
    """
    Resolve a DID to its Ed25519 public key (hex).
    Raises KeyError if DID not in registry.
    """
    registry = load_registry()
    entry = registry.get("dids", {}).get(did)
    if not entry:
        raise KeyError(f"DID '{did}' not found in registry")
    return entry["public_key_hex"]


def get_verify_key(did: str) -> VerifyKey:
    """Get a nacl VerifyKey for a DID."""
    return VerifyKey(resolve_did(did), encoder=HexEncoder)


def resolve_organ_id(did: str) -> str:
    """Resolve a DID to its organ_id (e.g. 'did:arif:geox' → 'geox')."""
    registry = load_registry()
    entry = registry.get("dids", {}).get(did)
    if not entry:
        raise KeyError(f"DID '{did}' not found in registry")
    return entry["organ_id"]


def verify_signature(data: bytes, signature_hex: str, did: str) -> bool:
    """
    Verify an Ed25519 signature against a DID's public key.
    Returns True if valid, False if invalid or DID not found.
    Constant-time where possible via nacl.
    """
    try:
        vk = get_verify_key(did)
        vk.verify(data, bytes.fromhex(signature_hex))
        return True
    except (BadSignatureError, KeyError, ValueError):
        return False


def list_dids() -> list[str]:
    """Return all registered DIDs."""
    registry = load_registry()
    return list(registry.get("dids", {}).keys())


# ── Smoke test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    reg = load_registry()
    print(f"DID Registry v{reg['version']} — {len(reg['dids'])} organs\n")
    for did, entry in reg["dids"].items():
        pub = entry["public_key_hex"][:16] + "…"
        print(f"  {did:28s} {pub}  [{entry['algorithm']}]  {entry['organ_id']}")

    # Verify a self-signature smoke test
    print("\nSmoke test: sign+verify with did:arif:aaa")
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from auth.gen_did import sign as gen_sign

    test_data = b"arifOS federation -- DITEMPA BUKAN DIBERI"
    sig = gen_sign(test_data, organ_id="aaa")
    ok = verify_signature(test_data, sig, "did:arif:aaa")
    print(f"  sig_valid: {ok} (expected: True)")

    # Negative test
    ok_bad = verify_signature(b"wrong data", sig, "did:arif:aaa")
    print(f"  bad_data:  {ok_bad} (expected: False)")
