#!/usr/bin/env python3
"""
capsule.py — Signed event capsule for AAA ingress.

Every inbound event (GitHub webhook, cron, manual trigger) is wrapped in a
CAPSULE before touching the skill router. The capsule:

  1. Verifies HMAC-SHA256 from the event source (GitHub webhook secret)
  2. Hashes the raw payload → deterministic event_id
  3. Signs the capsule fields with did:arif:aaa (Ed25519)
  4. Leaves a vault999_leaf slot for VAULT999 Merkle append

Without step 1, receipts are hearsay. Without step 3, the A2A mesh cannot
verify the capsule was produced by AAA and not a forged injector.

Usage:
    from core.capsule import build_capsule, verify_github_hmac

    capsule = build_capsule(
        raw_payload=request.body,
        event_type="github.pull_request.opened",
        hmac_header=request.headers["X-Hub-Signature-256"],
        github_secret=os.environ["GITHUB_WEBHOOK_SECRET"],
    )
"""
from __future__ import annotations

import hashlib
import hmac as _hmac
import json
import os
import secrets
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


# ── Model ─────────────────────────────────────────────────────────────────────

class CAPSULE(BaseModel):
    """Cryptographically signed wrapper for every inbound federation event."""

    # Identity
    event_id: str = Field(
        description="SHA256(raw_payload || received_at_iso) — deterministic, globally unique"
    )
    source: str = Field(description="Event origin: 'github' | 'cron' | 'manual' | 'a2a'")
    event_type: str = Field(description="Dot-path type: e.g. 'github.pull_request.opened'")

    # Integrity
    payload_hash: str = Field(description="SHA256(raw_payload), hex — payload fingerprint")
    received_at: str  = Field(description="ISO8601 UTC timestamp of ingress receipt")
    source_did: str   = Field(description="DID of event origin, e.g. 'did:github:webhook'")

    # Auth
    hmac_verified: bool = Field(
        description="True iff HMAC-SHA256 from source was verified against shared secret"
    )
    nonce: str = Field(description="32-byte random hex — replay prevention")

    # AAA signature over the capsule body
    signature: str = Field(
        description="Ed25519 signature by did:arif:aaa over canonical_bytes(capsule)"
    )

    # VAULT999 (populated after Merkle append)
    vault999_leaf: Optional[str] = Field(
        default=None,
        description="SHA256 Merkle leaf hash after VAULT999 append"
    )

    # Routing (populated by skill router)
    skill_routed_to: Optional[str] = Field(default=None)
    agent_pool: Optional[str]      = Field(default=None)
    authority_tier: Optional[str]  = Field(default=None)

    def canonical_bytes(self) -> bytes:
        """Deterministic byte representation for signing and verification."""
        fields = {
            "event_id":     self.event_id,
            "source":       self.source,
            "event_type":   self.event_type,
            "payload_hash": self.payload_hash,
            "received_at":  self.received_at,
            "source_did":   self.source_did,
            "hmac_verified": self.hmac_verified,
            "nonce":        self.nonce,
        }
        return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()


# ── HMAC verification ─────────────────────────────────────────────────────────

def verify_github_hmac(raw_payload: bytes, signature_header: str, secret: str) -> bool:
    """
    Verify GitHub's X-Hub-Signature-256 header.

    GitHub computes: sha256=HMAC(webhook_secret, raw_body)
    We recompute and compare in constant time to prevent timing attacks.

    Returns True if valid, False if invalid or header malformed.
    """
    if not signature_header.startswith("sha256="):
        return False
    expected = "sha256=" + _hmac.new(
        secret.encode("utf-8"), raw_payload, hashlib.sha256
    ).hexdigest()
    return _hmac.compare_digest(expected, signature_header)


# ── Capsule builder ───────────────────────────────────────────────────────────

def build_capsule(
    raw_payload: bytes,
    event_type: str,
    source: str = "github",
    source_did: str = "did:github:webhook",
    hmac_header: str = "",
    github_secret: str = "",
) -> CAPSULE:
    """
    Build and sign a CAPSULE from a raw webhook payload.

    Args:
        raw_payload:   The raw request body bytes (before any JSON parsing).
        event_type:    Dot-path event type string, e.g. 'github.pull_request.opened'.
        source:        Event origin label ('github', 'cron', 'manual').
        source_did:    DID of the event source.
        hmac_header:   X-Hub-Signature-256 header value (GitHub). Empty = not verifiable.
        github_secret: Shared HMAC secret from GitHub webhook settings.

    Returns:
        A signed CAPSULE ready for routing. vault999_leaf is None until VAULT999 append.
    """
    received_at = datetime.now(timezone.utc).isoformat()
    payload_hash = hashlib.sha256(raw_payload).hexdigest()
    event_id = hashlib.sha256(
        (payload_hash + received_at).encode()
    ).hexdigest()
    nonce = secrets.token_hex(32)

    hmac_verified = False
    if hmac_header and github_secret:
        hmac_verified = verify_github_hmac(raw_payload, hmac_header, github_secret)

    # Build partial capsule for signing
    partial = CAPSULE(
        event_id=event_id,
        source=source,
        event_type=event_type,
        payload_hash=payload_hash,
        received_at=received_at,
        source_did=source_did,
        hmac_verified=hmac_verified,
        nonce=nonce,
        signature="pending",  # replaced below
    )

    # Sign with did:arif:aaa
    signature = _sign_capsule(partial)
    return partial.model_copy(update={"signature": signature})


def _sign_capsule(capsule: CAPSULE) -> str:
    """Sign capsule.canonical_bytes() with did:arif:aaa. Graceful no-op if key absent."""
    import sys
    from pathlib import Path
    # Ensure AAA root is on sys.path regardless of how this module is invoked
    _root = str(Path(__file__).resolve().parent.parent)
    if _root not in sys.path:
        sys.path.insert(0, _root)
    try:
        from auth.gen_did import sign  # type: ignore[import]
        return sign(capsule.canonical_bytes(), organ_id="aaa")
    except FileNotFoundError:
        return "UNSIGNED:run-python-auth-gen_did.py"
    except ImportError:
        return "UNSIGNED:auth.gen_did-not-importable"


def verify_capsule_signature(capsule: CAPSULE) -> bool:
    """Verify that capsule.signature was produced by did:arif:aaa."""
    if capsule.signature.startswith("UNSIGNED:"):
        return False
    import sys
    from pathlib import Path
    _root = str(Path(__file__).resolve().parent.parent)
    if _root not in sys.path:
        sys.path.insert(0, _root)
    try:
        from auth.gen_did import verify  # type: ignore[import]
        return verify(capsule.canonical_bytes(), capsule.signature, organ_id="aaa")
    except Exception:
        return False


# ── A2A envelope schema ───────────────────────────────────────────────────────

class A2A_ENVELOPE(BaseModel):
    """
    Signed inter-organ task envelope for Hermes A2A mesh.

    When A-FORGE delegates a task to GEOX, it wraps the request in this
    envelope. GEOX verifies all three before accepting:
      1. signature → message really came from A-FORGE (not an impersonator)
      2. capability_token → did:arif:Ω authorised this delegation
      3. nonce + issued_at → not a replay
    """
    from_did: str   = Field(description="Sender organ DID, e.g. 'did:arif:a-forge'")
    to_did: str     = Field(description="Recipient organ DID, e.g. 'did:arif:geox'")
    task_id: str    = Field(description="Unique task ID: SHA256(from_did||to_did||nonce)")
    task_type: str  = Field(description="Capability being requested, e.g. 'petrophysics-eval'")
    payload: dict   = Field(description="Task-specific input data")
    issued_at: str  = Field(description="ISO8601 UTC — replay window check against this")
    nonce: str      = Field(description="32-byte random hex — unique per envelope")
    capability_token: str = Field(
        description="JWT signed by did:arif:Ω granting from_did the right to call to_did for task_type"
    )
    signature: str  = Field(
        description="Ed25519 signature by from_did's private key over canonical_bytes(envelope)"
    )
    vault999_capsule_ref: Optional[str] = Field(
        default=None,
        description="event_id of the originating CAPSULE, for audit chain linkage"
    )

    def canonical_bytes(self) -> bytes:
        fields = {
            "from_did":  self.from_did,
            "to_did":    self.to_did,
            "task_id":   self.task_id,
            "task_type": self.task_type,
            "issued_at": self.issued_at,
            "nonce":     self.nonce,
        }
        return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()


# ── CLI smoke test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    print("=== CAPSULE smoke test ===\n")

    fake_payload = json.dumps({"action": "opened", "number": 42}).encode()
    fake_secret  = "test-secret-123"
    good_sig = "sha256=" + _hmac.new(fake_secret.encode(), fake_payload, hashlib.sha256).hexdigest()

    c = build_capsule(
        raw_payload=fake_payload,
        event_type="github.pull_request.opened",
        source="github",
        hmac_header=good_sig,
        github_secret=fake_secret,
    )

    print(f"event_id      : {c.event_id[:16]}…")
    print(f"payload_hash  : {c.payload_hash[:16]}…")
    print(f"received_at   : {c.received_at}")
    print(f"hmac_verified : {c.hmac_verified}")
    print(f"nonce         : {c.nonce[:16]}…")
    print(f"signature     : {c.signature[:32]}…")
    sig_ok = verify_capsule_signature(c)
    print(f"sig valid     : {sig_ok}")

    # Test bad HMAC
    c_bad = build_capsule(
        raw_payload=fake_payload,
        event_type="github.pull_request.opened",
        hmac_header="sha256=badhash",
        github_secret=fake_secret,
    )
    print(f"\nbad HMAC test : hmac_verified={c_bad.hmac_verified} (expected: False)")

    print("\n=== A2A_ENVELOPE fields ===")
    env = A2A_ENVELOPE(
        from_did="did:arif:a-forge",
        to_did="did:arif:geox",
        task_id="abc123",
        task_type="petrophysics-eval",
        payload={"well": "KB-1", "curve": "GR"},
        issued_at=datetime.now(timezone.utc).isoformat(),
        nonce=secrets.token_hex(32),
        capability_token="<JWT-placeholder>",
        signature="<Ed25519-placeholder>",
    )
    print(f"canonical_bytes (first 80): {env.canonical_bytes()[:80]}")
    print("\nDone. Run python auth/gen_did.py to enable real Ed25519 signing.")
