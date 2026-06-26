"""
sovereign_auth.py — Ed25519 sovereign signer for arifOS MCP challenge-response.
Owner: arif

The private key file at ARIFOS_SOVEREIGN_KEY_FILE is 39 bytes:
  7 bytes malformed-DER header (30 2a 02 01 01 04 20) + 32-byte Ed25519 seed.
This module tries multiple formats and caches the key.
"""

from __future__ import annotations

import base64
import logging
import os
from pathlib import Path
from typing import Any, Optional

log = logging.getLogger("opencode-bot.sovereign")

SOVEREIGN_KEY_PATH = os.environ.get(
    "ARIFOS_SOVEREIGN_KEY_FILE", "/root/compose/sekrits/arifos_sovereign.key"
)
_SOVEREIGN_KEY_CACHE: Any = None


def load_sovereign_private_key() -> Any:
    """Load the Ed25519 sovereign private key. Cached."""
    global _SOVEREIGN_KEY_CACHE
    if _SOVEREIGN_KEY_CACHE is not None:
        return _SOVEREIGN_KEY_CACHE
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PrivateKey,
        )
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        log.warning("SOVEREIGN_KEY: cryptography library not installed")
        return None

    key_path = Path(SOVEREIGN_KEY_PATH)
    if not key_path.exists():
        log.warning(f"SOVEREIGN_KEY: file not found at {key_path}")
        return None
    try:
        raw = key_path.read_bytes()
    except Exception as exc:
        log.warning(f"SOVEREIGN_KEY: cannot read {key_path}: {exc}")
        return None

    # Format 1: 39-byte broken DER header + 32-byte seed at offset 7
    if (
        len(raw) == 39
        and raw[:2] == b"\x30\x2a"
        and raw[2:7] == b"\x02\x01\x01\x04\x20"
    ):
        try:
            _SOVEREIGN_KEY_CACHE = Ed25519PrivateKey.from_private_bytes(raw[7:39])
            log.info(f"SOVEREIGN_KEY: loaded (39-byte broken-DER format)")
            return _SOVEREIGN_KEY_CACHE
        except Exception as exc:
            log.warning(f"SOVEREIGN_KEY: 39-byte parse failed: {exc}")

    # Format 2: raw 32-byte seed
    if len(raw) == 32:
        try:
            _SOVEREIGN_KEY_CACHE = Ed25519PrivateKey.from_private_bytes(raw)
            log.info(f"SOVEREIGN_KEY: loaded (32-byte raw seed)")
            return _SOVEREIGN_KEY_CACHE
        except Exception as exc:
            log.warning(f"SOVEREIGN_KEY: 32-byte parse failed: {exc}")

    # Format 3: PEM
    if raw.startswith(b"-----BEGIN"):
        try:
            _SOVEREIGN_KEY_CACHE = serialization.load_pem_private_key(raw, password=None)
            log.info(f"SOVEREIGN_KEY: loaded (PEM)")
            return _SOVEREIGN_KEY_CACHE
        except Exception as exc:
            log.warning(f"SOVEREIGN_KEY: PEM parse failed: {exc}")

    # Format 4: DER
    try:
        _SOVEREIGN_KEY_CACHE = serialization.load_der_private_key(raw, password=None)
        log.info(f"SOVEREIGN_KEY: loaded (DER)")
        return _SOVEREIGN_KEY_CACHE
    except Exception as exc:
        log.warning(f"SOVEREIGN_KEY: DER parse failed: {exc}")

    log.warning(f"SOVEREIGN_KEY: no format matched for {key_path} ({len(raw)} bytes)")
    return None


def sign_actor_challenge(actor_id: str, nonce: str) -> Optional[str]:
    """Sign f'{actor_id}:{nonce}' with Ed25519. Return base64 signature or None."""
    privkey = load_sovereign_private_key()
    if privkey is None:
        return None
    try:
        payload = f"{actor_id}:{nonce}".encode("utf-8")
        sig_bytes = privkey.sign(payload)
        return base64.b64encode(sig_bytes).decode("ascii")
    except Exception as exc:
        log.warning(f"SOVEREIGN_SIGN: signing failed: {exc}")
        return None
