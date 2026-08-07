#!/usr/bin/env python3
"""
OpenClaw A2A Egress Bridge
--------------------------

Maps intent-router rule output → A2A v1.0.0 POST /tasks on :3001.

Contract (from /root/.openclaw/workspace/a2a-server/server.js + handoff-protocol.yaml):
  - HTTP method: POST
  - URL:        http://127.0.0.1:3001/tasks
  - Header:     A2A-Version: 1.0 (REQUIRED)
  - Header:     Authorization: Bearer <token> (AAA gateway)
  - Header:     X-A2A-Key: <api-key> (AAA gateway)
  - Body:       JSON-RPC 2.0 envelope with method=message/send (or tasks/send)
  - Body top-level: session_id, actor_id (DID)
  - Signed envelope: Ed25519 over canonical-JSON of body, base64 payload
  - DID registry:    /opt/arifos/.secrets/did/registry.json (runtime)
                     /root/AAA/secrets/did/registry.json (source)

Forged: 2026-08-07  ·  Part of OpenClaw AA completion  ·  F11/F13 compliant
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

# ──────────────────────────── paths & constants ────────────────────────────

ROUTER_YAML = Path("/root/AAA/agents/openclaw/config/intent-router.yaml")
HANDOFF_YAML = Path("/root/AAA/agents/openclaw/config/handoff-protocol.yaml")

# A2A gateway targets (local first; public via env override)
A2A_BASE = os.environ.get("A2A_BASE_URL", "http://127.0.0.1:3001")
A2A_TOKEN = os.environ.get("A2A_TOKEN", "aaa-a2a-token-dev")
A2A_API_KEY = os.environ.get("A2A_API_KEY", "aaa-a2a-apikey-dev")

# DID source — runtime beats source
DID_REGISTRY = Path(
    os.environ.get(
        "DID_REGISTRY_PATH",
        "/opt/arifos/.secrets/did/registry.json",
    )
)
if not DID_REGISTRY.exists():
    DID_REGISTRY = Path("/root/AAA/secrets/did/registry.json")

# OpenClaw actor identity
OPENCLAW_KEY_PATH = Path(
    os.environ.get("OPENCLAW_KEY_PATH", "/root/AAA/auth/keys/openclaw_private.key")
)
OPENCLAW_DID = "did:key:ed25519:openclaw"  # look up in registry

A2A_VERSION = "1.0"
SIG_ALGO = "ed25519"


# ──────────────────────────── crypto helpers ────────────────────────────

def _load_ed25519():
    """Lazy import — cryptography is the canonical lib (not PyNaCl)."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        return Ed25519PrivateKey
    except ImportError:
        raise RuntimeError(
            "Missing 'cryptography' lib. Install: pip install cryptography"
        )


def _canon(obj: Any) -> str:
    """Canonical JSON for signing equality (RFC 8785 subset — sorted keys, no whitespace)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _load_private_key(path: Path) -> "Ed25519PrivateKey":
    """Load an Ed25519 private key.

    Supports two formats:
      1. Raw 32-byte Ed25519 seed (arifOS convention at /root/AAA/auth/keys/)
      2. PEM-encoded PKCS8 Ed25519 (standard)
    """
    Ed25519PrivateKey = _load_ed25519()
    raw = path.read_bytes()
    # Try PEM first (heuristic: PEM starts with b'-----BEGIN')
    if raw.lstrip().startswith(b"-----BEGIN"):
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        key = load_pem_private_key(raw, password=None)
        if not isinstance(key, Ed25519PrivateKey):
            raise TypeError(f"PEM key is not Ed25519: {type(key).__name__}")
        return key
    # Else: raw 32-byte seed
    if len(raw) != 32:
        raise ValueError(
            f"Expected 32-byte Ed25519 seed, got {len(raw)} bytes from {path}"
        )
    return Ed25519PrivateKey.from_private_bytes(raw)


def _sign_payload(private_key, payload: bytes) -> bytes:
    return private_key.sign(payload)


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _resolve_did(did: str) -> dict:
    """Resolve DID → public_key + metadata from registry."""
    if not DID_REGISTRY.exists():
        return {"did": did, "resolved": False, "reason": "registry_missing"}
    try:
        reg = json.loads(DID_REGISTRY.read_text())
    except Exception as e:
        return {"did": did, "resolved": False, "reason": f"registry_parse_error: {e}"}
    entry = reg.get(did) or reg.get(did.replace("did:key:ed25519:", "ed25519:"))
    if not entry:
        # Fallback: search by short key id
        for k, v in reg.items():
            if did.endswith(k) or k.endswith(did.split(":")[-1]):
                return {"did": k, "resolved": True, "public_key": v}
        return {"did": did, "resolved": False, "reason": "did_not_found"}
    pub = entry.get("publicKeyMultibase") or entry.get("public_key") or entry.get("pub")
    return {"did": did, "resolved": True, "public_key": pub, "meta": entry}


# ──────────────────────────── routing ────────────────────────────

@dataclass
class RouteResult:
    rule_id: str
    organ: str
    tool: str
    intent_class: str
    priority_flag: str
    require_seal: bool = False
    fallback: Optional[str] = None
    human_visible: str = ""
    raw: dict = field(default_factory=dict)


def _load_router_rules() -> list[dict]:
    """Load rules from intent-router.yaml — minimal YAML parse to avoid dep."""
    import yaml
    if not ROUTER_YAML.exists():
        raise FileNotFoundError(f"router config missing: {ROUTER_YAML}")
    cfg = yaml.safe_load(ROUTER_YAML.read_text())
    return cfg.get("rules", [])


def _rule_matches(rule: dict, text: str) -> bool:
    import re
    text_lower = text.lower()
    pats = rule.get("match", {}).get("patterns", [])
    excl = rule.get("match", {}).get("exclude_when", [])
    for p in pats:
        if re.search(p, text_lower, re.IGNORECASE):
            # Exclusion check
            for x in excl:
                if re.search(x, text_lower, re.IGNORECASE):
                    return False
            return True
    return False


def route(text: str) -> RouteResult:
    """Apply the ten-rule router. First match wins."""
    rules = _load_router_rules()
    # Sort by priority desc (R01=10 → R10=1)
    rules_sorted = sorted(rules, key=lambda r: -(r.get("priority", 0)))
    for rule in rules_sorted:
        if _rule_matches(rule, text):
            r = rule.get("route", {})
            return RouteResult(
                rule_id=rule["id"],
                organ=r.get("organ", "hermes-asi"),
                tool=r.get("tool", "a2a_dispatch"),
                intent_class=r.get("intent_class", "triage"),
                priority_flag=r.get("priority_flag", "low"),
                require_seal=bool(r.get("require_seal", False)),
                fallback=r.get("fallback"),
                human_visible=rule.get("human_visible", ""),
                raw=rule,
            )
    # Default fallback if R10 missing
    return RouteResult(
        rule_id="R10_DEFAULT_TRIAGE",
        organ="hermes-asi",
        tool="a2a_dispatch",
        intent_class="triage",
        priority_flag="low",
        human_visible="Let me route this to Hermes for you.",
    )


# ──────────────────────────── A2A envelope ────────────────────────────

def build_envelope(
    text: str,
    route_result: RouteResult,
    *,
    session_id: Optional[str] = None,
    actor_id: Optional[str] = None,
    extras: Optional[dict] = None,
) -> dict:
    """
    Build the JSON-RPC 2.0 envelope with A2A v1.0.0 semantics.

    Top-level (per arifOS A2A-Version contract):
      session_id, actor_id (DID), message, metadata
    """
    if session_id is None:
        session_id = f"oc-{uuid.uuid4().hex[:12]}"
    if actor_id is None:
        actor_id = OPENCLAW_DID

    message = {
        "role": "user",
        "parts": [
            {"kind": "text", "text": text},
        ],
    }

    envelope = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "session_id": session_id,
            "actor_id": actor_id,
            "message": message,
            "metadata": {
                "routing": {
                    "rule_id": route_result.rule_id,
                    "organ": route_result.organ,
                    "tool": route_result.tool,
                    "intent_class": route_result.intent_class,
                    "priority_flag": route_result.priority_flag,
                    "require_seal": route_result.require_seal,
                    "fallback": route_result.fallback,
                },
                "openclaw": {
                    "version": "1.0.0",
                    "router": "intent-router.yaml",
                    "bridge": "a2a_bridge.py",
                },
            },
        },
    }
    if extras:
        envelope["params"]["metadata"].update(extras)
    return envelope


def sign_envelope(envelope: dict) -> dict:
    """Sign the canonical-JSON of the envelope and append a signature block."""
    if not OPENCLAW_KEY_PATH.exists():
        return {
            "envelope": envelope,
            "signature": None,
            "skipped": "key_missing",
            "reason": f"OpenClaw private key not found at {OPENCLAW_KEY_PATH}",
        }
    try:
        key_pem = OPENCLAW_KEY_PATH.read_bytes()
        canonical = _canon(envelope).encode("utf-8")
        sig_bytes = _sign_payload(key_pem, canonical)
        sig_b64 = _b64url(sig_bytes)
        digest = _sha256_hex(canonical)
        return {
            "envelope": envelope,
            "signature": {
                "algo": SIG_ALGO,
                "value": sig_b64,
                "canonical_hash": digest,
                "signed_fields": list(envelope.keys()),
            },
        }
    except Exception as e:
        return {
            "envelope": envelope,
            "signature": None,
            "skipped": "sign_error",
            "reason": f"{type(e).__name__}: {e}",
        }


# ──────────────────────────── dispatch ────────────────────────────

def _http_send(envelope: dict, *, timeout: float = 60.0) -> dict:
    """HTTP POST envelope to A2A gateway. Lazy import of httpx."""
    import httpx
    headers = {
        "Content-Type": "application/json",
        "A2A-Version": A2A_VERSION,
        "Authorization": f"Bearer {A2A_TOKEN}",
        "X-A2A-Key": A2A_API_KEY,
    }
    try:
        with httpx.Client(timeout=timeout) as c:
            r = c.post(f"{A2A_BASE}/tasks", json=envelope, headers=headers)
        return {
            "ok": r.status_code < 400,
            "status": r.status_code,
            "body": r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text,
            "task_id": (r.json().get("result", {}) or {}).get("id") if r.status_code < 400 else None,
        }
    except Exception as e:
        return {
            "ok": False,
            "status": 0,
            "body": f"{type(e).__name__}: {e}",
            "task_id": None,
        }


def dispatch(
    text: str,
    *,
    sign: bool = True,
    send: bool = True,
    session_id: Optional[str] = None,
    actor_id: Optional[str] = None,
    extras: Optional[dict] = None,
    timeout: float = 60.0,
) -> dict:
    """End-to-end: route → build envelope → sign → optional HTTP send."""
    result = {"ts": int(time.time() * 1000), "input": text}
    rr = route(text)
    result["routing"] = {
        "rule_id": rr.rule_id,
        "organ": rr.organ,
        "tool": rr.tool,
        "intent_class": rr.intent_class,
        "priority_flag": rr.priority_flag,
        "require_seal": rr.require_seal,
        "fallback": rr.fallback,
        "human_visible": rr.human_visible,
    }
    envelope = build_envelope(
        text, rr, session_id=session_id, actor_id=actor_id, extras=extras
    )
    result["envelope"] = envelope
    if sign:
        signed = sign_envelope(envelope)
        result["signature"] = signed.get("signature")
        if signed.get("skipped"):
            result["signature_skipped"] = signed["skipped"]
            result["signature_reason"] = signed.get("reason")
    if send:
        resp = _http_send(envelope, timeout=timeout)
        result["a2a_response"] = resp
    return result


# ──────────────────────────── CLI ────────────────────────────

def _print_json(d: dict) -> None:
    print(json.dumps(d, indent=2, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser(
        description="OpenClaw A2A Bridge — route → POST /tasks"
    )
    p.add_argument("text", help="intent text to route and dispatch")
    p.add_argument("--no-sign", action="store_true", help="skip Ed25519 signing")
    p.add_argument("--no-send", action="store_true", help="build envelope only, don't HTTP POST")
    p.add_argument("--session-id", help="explicit session_id (default: generated)")
    p.add_argument("--actor-id", help="DID (default: openclaw)")
    p.add_argument("--timeout", type=float, default=60.0, help="HTTP timeout seconds")
    p.add_argument("--resolve-did", action="store_true", help="print DID resolution for the actor")
    p.add_argument("--dry-run", action="store_true", help="treat as 'no-send' (env override-friendly)")
    args = p.parse_args()

    if args.resolve_did:
        _print_json(_resolve_did(args.actor_id or OPENCLAW_DID))
        return 0

    send = not (args.no_send or args.dry_run)
    sign = not args.no_sign
    out = dispatch(
        args.text,
        sign=sign,
        send=send,
        session_id=args.session_id,
        actor_id=args.actor_id,
        timeout=args.timeout,
    )
    _print_json(out)
    return 0 if (not send or out.get("a2a_response", {}).get("ok", False)) else 1


if __name__ == "__main__":
    sys.exit(main())
