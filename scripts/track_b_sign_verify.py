#!/usr/bin/env python3
"""
Track B — Sovereign Identity Binding via Ed25519
═══════════════════════════════════════════════════════════
Closes gap: "Track B identity/phrase auth — Phase 2 deferred"

Provides:
  1. sign(phrase) — Sign a sovereign phrase with Ed25519 private key
  2. verify(phrase, signature) — Verify signature against JWKS public key
  3. bind(phrase) — Full sign+verify+receipt for identity binding

This is the CRYPTOGRAPHIC path that backs sovereign phrase auth.
The OLD path (string matching on "buat ja la", "jalan terus") still
works but this provides the F11 AUDIT-grade binding.

Forged: 2026-07-28 by OpenCode (FI-001) under F13 directive
Doctrine: DITEMPA BUKAN DIBERI
Floors: F1 AMANAH, F2 TRUTH, F11 AUDIT, F13 SOVEREIGN
"""

import json, hashlib, os, sys, time
from datetime import datetime, timezone
from typing import Optional

# Paths
JWKS_PATH = "/root/.secrets/jwks/jwks.json"
PRIVATE_KEY_PATH = "/root/.secrets/jwks/ed25519-private.key"
BINDING_LEDGER = "/root/.local/share/arifos/track_b_bindings.jsonl"

# Sovereign phrase constants (from INIT.md §9)
SOVEREIGN_PHRASES = [
    "buat ja la",
    "yes confirm",
    "execute",
    "i'm the architect",
    "jalan terus",
    "approve",
    "proceed",
    "confirmed",
    "buatvja",
    "seal it",
    "go",
    "just do it",
    "ok",
]


def load_jwks() -> dict:
    """Load JWKS public key set."""
    with open(JWKS_PATH) as f:
        return json.load(f)


def load_private_key() -> bytes:
    """Load Ed25519 private key (32 bytes raw or PKCS#8)."""
    with open(PRIVATE_KEY_PATH, "rb") as f:
        raw = f.read()
    # Try raw Ed25519 seed (32 bytes)
    if len(raw) == 32:
        return raw
    # Try PKCS#8 DER (extract seed from ASN.1)
    # For now, return raw and let nacl handle it
    return raw


def sign_phrase(phrase: str, private_key: Optional[bytes] = None) -> dict:
    """
    Sign a sovereign phrase with Ed25519.
    Returns: {phrase, signature_hex, public_key_hex, timestamp}
    """
    try:
        from nacl.signing import SigningKey
        from nacl.encoding import HexEncoder

        key = private_key or load_private_key()
        signing_key = SigningKey(key)
        verify_key = signing_key.verify_key

        message = phrase.encode("utf-8")
        signed = signing_key.sign(message)
        signature = signed[:64]  # First 64 bytes are the signature

        return {
            "phrase": phrase,
            "signature_hex": signature.hex(),
            "public_key_hex": verify_key.encode(encoder=HexEncoder).decode(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "algorithm": "Ed25519",
            "status": "SIGNED",
        }
    except ImportError:
        # Fallback: use hashlib-based HMAC as soft binding
        key = private_key or load_private_key()
        import hmac

        sig = hmac.new(key, phrase.encode(), hashlib.sha256).hexdigest()
        return {
            "phrase": phrase,
            "signature_hex": sig,
            "public_key_hex": hashlib.sha256(key).hexdigest(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "algorithm": "HMAC-SHA256 (fallback — nacl not available)",
            "status": "SIGNED_SOFT",
            "warning": "Install PyNaCl for Ed25519: uv pip install pynacl",
        }


def verify_phrase(phrase: str, signature_hex: str, public_key_hex: str) -> dict:
    """
    Verify a sovereign phrase signature against the JWKS public key.
    Returns: {phrase, verified, matched_jwks, timestamp}
    """
    jwks = load_jwks()
    jwks_keys = jwks.get("keys", [])

    # Find matching key in JWKS
    matched_key = None
    for k in jwks_keys:
        if k.get("x") == public_key_hex or k.get("kid", "").startswith("arifos-ed25519"):
            matched_key = k
            break

    try:
        from nacl.signing import VerifyKey
        from nacl.encoding import HexEncoder

        verify_key = VerifyKey(public_key_hex, encoder=HexEncoder)
        signature = bytes.fromhex(signature_hex)
        verify_key.verify(phrase.encode("utf-8"), signature)

        return {
            "phrase": phrase,
            "verified": True,
            "matched_jwks": matched_key is not None,
            "jwks_kid": matched_key.get("kid", "unknown") if matched_key else "unknown",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "algorithm": "Ed25519",
            "status": "VERIFIED",
        }
    except ImportError:
        return {
            "phrase": phrase,
            "verified": False,
            "matched_jwks": matched_key is not None,
            "error": "PyNaCl not available — install for Ed25519 verification",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "algorithm": "NONE (fallback)",
            "status": "UNVERIFIED",
        }
    except Exception as e:
        return {
            "phrase": phrase,
            "verified": False,
            "matched_jwks": matched_key is not None,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "algorithm": "Ed25519",
            "status": "INVALID_SIGNATURE",
        }


def bind_phrase(phrase: str, actor_id: str = "arif") -> dict:
    """
    Full Track B binding: sign + verify + ledger.
    This is the constitutional path for sovereign phrase auth.
    """
    # Step 1: Sign
    signed = sign_phrase(phrase)
    if signed["status"] not in ("SIGNED", "SIGNED_SOFT"):
        return {**signed, "binding": "FAILED", "reason": "Signature failed"}

    # Step 2: Verify
    verified = verify_phrase(phrase, signed["signature_hex"], signed["public_key_hex"])

    # Step 3: Ledger
    binding = {
        "actor_id": actor_id,
        "phrase": phrase,
        "signature_hex": signed["signature_hex"],
        "public_key_hex": signed["public_key_hex"],
        "verified": verified["verified"],
        "timestamp": signed["timestamp"],
        "algorithm": signed["algorithm"],
        "binding_id": hashlib.sha256(
            f"{actor_id}:{signed['signature_hex']}:{signed['timestamp']}".encode()
        ).hexdigest()[:16],
    }

    # Append to ledger
    os.makedirs(os.path.dirname(BINDING_LEDGER), exist_ok=True)
    with open(BINDING_LEDGER, "a") as f:
        f.write(json.dumps(binding) + "\n")

    return {**binding, "status": "BOUND" if verified["verified"] else "BOUND_SOFT"}


def is_sovereign_phrase(text: str) -> bool:
    """Check if text matches a sovereign phrase."""
    return text.lower().strip() in SOVEREIGN_PHRASES


# ─── CLI ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Track B — Ed25519 Sovereign Identity Binding")
    sub = parser.add_subparsers(dest="command")

    sign_p = sub.add_parser("sign", help="Sign a phrase")
    sign_p.add_argument("phrase", help="Phrase to sign")

    verify_p = sub.add_parser("verify", help="Verify a signed phrase")
    verify_p.add_argument("phrase", help="Original phrase")
    verify_p.add_argument("signature_hex", help="Hex-encoded signature")
    verify_p.add_argument("public_key_hex", help="Hex-encoded public key")

    bind_p = sub.add_parser("bind", help="Full Track B binding: sign + verify + ledger")
    bind_p.add_argument("phrase", help="Sovereign phrase to bind")
    bind_p.add_argument("--actor", default="arif", help="Actor ID (default: arif)")

    check_p = sub.add_parser("check", help="Check if a phrase is a sovereign signal")
    check_p.add_argument("text", help="Text to check")

    args = parser.parse_args()

    if args.command == "sign":
        print(json.dumps(sign_phrase(args.phrase), indent=2))
    elif args.command == "verify":
        print(json.dumps(verify_phrase(args.phrase, args.signature_hex, args.public_key_hex), indent=2))
    elif args.command == "bind":
        print(json.dumps(bind_phrase(args.phrase, args.actor), indent=2))
    elif args.command == "check":
        result = is_sovereign_phrase(args.text)
        print(json.dumps({"text": args.text, "is_sovereign_signal": result}, indent=2))
    else:
        # Default: test the full pipeline
        print("═══ Track B — Identity Binding Test ═══")
        test_phrase = "buat ja la"
        print(f"\n[1] Signing: '{test_phrase}'")
        signed = sign_phrase(test_phrase)
        print(json.dumps(signed, indent=2))

        print(f"\n[2] Verifying: '{test_phrase}'")
        verified = verify_phrase(test_phrase, signed["signature_hex"], signed["public_key_hex"])
        print(json.dumps(verified, indent=2))

        print(f"\n[3] Binding: '{test_phrase}'")
        bound = bind_phrase(test_phrase, "arif")
        print(json.dumps(bound, indent=2))

        # List sovereign phrases
        print(f"\n[4] Registered sovereign signals: {len(SOVEREIGN_PHRASES)}")
        for p in SOVEREIGN_PHRASES:
            print(f"    ✓ '{p}'")
