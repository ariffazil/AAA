#!/usr/bin/env python3
"""
did_registry.py — Runtime DID public-key resolver for the arifOS federation.

Wraps auth/did_registry.yaml (committed, public) so any organ can resolve
a DID to its Ed25519 public key without touching private key files.

Usage:
    from auth.did_registry import resolve, verify

    pub_hex = resolve("did:arif:geox")
    ok = verify(data_bytes, signature_hex, "did:arif:a-forge")
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

_REGISTRY_PATH = Path(__file__).parent / "did_registry.yaml"


@lru_cache(maxsize=1)
def _load() -> dict[str, str]:
    """Load DID → public_key_hex mapping once, cache forever."""
    data = yaml.safe_load(_REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    return {entry["did"]: entry["public_key_hex"] for entry in data.get("dids", [])}


def resolve(did: str) -> str:
    """Return the Ed25519 public key hex for a DID. Raises KeyError if unknown."""
    registry = _load()
    if did not in registry:
        raise KeyError(
            f"Unknown DID: '{did}'. "
            f"Known: {sorted(registry)}. "
            "Run: python auth/gen_did.py"
        )
    return registry[did]


def verify(data: bytes, signature_hex: str, did: str) -> bool:
    """
    Verify an Ed25519 signature against a DID's public key.

    Returns True if valid, False if invalid or DID unknown.
    Does NOT raise — callers should treat False as rejection.
    """
    try:
        pub_hex = resolve(did)
        vk = VerifyKey(pub_hex, encoder=HexEncoder)
        vk.verify(data, bytes.fromhex(signature_hex))
        return True
    except (KeyError, BadSignatureError, ValueError):
        return False


def list_dids() -> list[str]:
    """Return all registered DIDs."""
    return sorted(_load().keys())


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    print("arifOS DID Registry\n")
    for did in list_dids():
        pub = resolve(did)
        print(f"  {did:30s}  {pub[:16]}…")
    print(f"\n{len(list_dids())} DIDs loaded from {_REGISTRY_PATH}")
