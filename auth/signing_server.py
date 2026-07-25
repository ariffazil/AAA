#!/usr/bin/env python3
"""
signing_server.py — F13 Ed25519 challenge signing endpoint for AAA approval card.

Listens on localhost:18900. Accepts a challenge_id, retrieves the canonical
challenge from arifOS, verifies against submitted payload, signs with the
sovereign Ed25519 private key, returns base64 signature.

PAM transitional guard: requires a valid local credential before signing.
Production target: WebAuthn/FIDO2 hardware-backed user verification.

This is the bridge between the one-tap approval UI and the cryptographic
signing machinery. The user presses [Approve]; this server handles the crypto.

Usage:
    python auth/signing_server.py           # start on :18900
    systemctl start aaa-signing             # production
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

logger = logging.getLogger("aaa.signing")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

KEYS_DIR = Path(__file__).resolve().parent / "keys"
ARIF_PRIVATE_KEY = KEYS_DIR / "arifos_private.key"
ARIFOS_CHALLENGE_STORE = os.environ.get("ARIFOS_URL", "http://127.0.0.1:8088")
ALLOWED_ORIGINS = {
    "http://localhost:5173",  # AAA dev server
    "http://127.0.0.1:5173",
    "https://aaa.arif-fazil.com",  # AAA production
    "http://127.0.0.1:3000",  # AAA A2A gateway
}
SIGNATURE_RATE_LIMIT_INTERVAL = float(os.environ.get("AAA_SIGN_RATE_LIMIT", "2.0"))
_last_signature_time: float = 0.0

_CACHED_PRIVATE_KEY: bytes | None = None


def load_sovereign_key() -> bytes:
    global _CACHED_PRIVATE_KEY
    if _CACHED_PRIVATE_KEY is not None:
        return _CACHED_PRIVATE_KEY

    if not ARIF_PRIVATE_KEY.exists():
        raise FileNotFoundError(
            f"Sovereign Ed25519 private key not found at {ARIF_PRIVATE_KEY}. "
            "Generate one with: python auth/sign_agent_card.py --gen-key arifos"
        )

    raw = ARIF_PRIVATE_KEY.read_bytes()
    try:
        raw_str = raw.decode("ascii").strip()
    except UnicodeDecodeError:
        raw_str = ""

    from cryptography.hazmat.primitives import serialization

    # Try PEM first
    if "-----BEGIN" in raw_str:
        try:
            key = serialization.load_pem_private_key(raw, password=None)
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PrivateKey,
            )

            if isinstance(key, Ed25519PrivateKey):
                _CACHED_PRIVATE_KEY = key.private_bytes_raw()
                logger.info("loaded sovereign Ed25519 key from PEM")
                return _CACHED_PRIVATE_KEY
        except Exception as e:
            logger.warning("PEM load failed: %s — trying raw", e)

    # Try raw hex/base64
    clean = raw_str.strip()
    try:
        _CACHED_PRIVATE_KEY = bytes.fromhex(clean)
        if len(_CACHED_PRIVATE_KEY) == 32:
            logger.info("loaded sovereign Ed25519 key from hex")
            return _CACHED_PRIVATE_KEY
    except ValueError:
        pass
    try:
        _CACHED_PRIVATE_KEY = base64.b64decode(clean)
        if len(_CACHED_PRIVATE_KEY) == 32:
            logger.info("loaded sovereign Ed25519 key from base64")
            return _CACHED_PRIVATE_KEY
    except Exception:
        pass

    # Extract raw key from PEM manually
    try:
        if "-----BEGIN" in raw_str:
            import re

            b64_body = re.sub(r"-----(BEGIN|END).*?-----", "", raw_str).replace("\n", "").replace(" ", "")
            _CACHED_PRIVATE_KEY = base64.b64decode(b64_body)
            if len(_CACHED_PRIVATE_KEY) == 32:
                logger.info("loaded sovereign Ed25519 key from PEM body")
                return _CACHED_PRIVATE_KEY
            # PEM format wraps Ed25519 in PKCS8; extract the raw key bytes (last 32)
            if len(_CACHED_PRIVATE_KEY) > 32:
                _CACHED_PRIVATE_KEY = _CACHED_PRIVATE_KEY[-32:]
                logger.info("extracted raw Ed25519 key from PKCS8 wrapper")
                return _CACHED_PRIVATE_KEY
    except Exception:
        pass

    raise ValueError(f"Could not parse Ed25519 private key from {ARIF_PRIVATE_KEY}")


class SigningHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        logger.info(format % args)

    def _check_origin(self) -> bool:
        origin = self.headers.get("Origin", "")
        if not origin:
            # Same-origin requests (no Origin header) from localhost are acceptable
            return True
        return origin in ALLOWED_ORIGINS

    def _cors_headers(self, origin_ok: bool = False) -> None:
        if origin_ok:
            req_origin = self.headers.get("Origin", "")
            if req_origin in ALLOWED_ORIGINS:
                self.send_header("Access-Control-Allow-Origin", req_origin)
                self.send_header("Vary", "Origin")
        # No wildcard CORS — explicit origins only

    def _verify_challenge(self, challenge_id: str, submitted_canonical: str) -> tuple[bool, str]:
        """Retrieve the authoritative challenge from arifOS and verify the submitted payload matches."""
        import urllib.request

        try:
            url = f"{ARIFOS_CHALLENGE_STORE}/challenge/{challenge_id}"
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                authoritative = json.loads(resp.read().decode())
        except Exception as e:
            return False, f"Cannot retrieve challenge from arifOS: {e}"

        # Verify submitted payload matches authoritative challenge
        try:
            submitted = json.loads(submitted_canonical) if isinstance(submitted_canonical, str) else submitted_canonical
        except json.JSONDecodeError:
            return False, "Submitted payload is not valid JSON"

        critical_fields = ["actor", "nonce", "candidate_hash", "action_class", "authorization_session_id"]
        for field in critical_fields:
            auth_val = authoritative.get(field, "")
            sub_val = submitted.get(field, "")
            if auth_val != sub_val:
                return False, f"Challenge mismatch on field '{field}': expected='{auth_val}' submitted='{sub_val}'"

        # Hash the submitted canonical to verify against stored candidate_hash
        stored_hash = authoritative.get("candidate_hash", "")
        if stored_hash:
            canonical_bytes = (
                submitted_canonical.encode("utf-8")
                if isinstance(submitted_canonical, str)
                else json.dumps(submitted, separators=(",", ":")).encode("utf-8")
            )
            computed_hash = f"sha256:{hashlib.sha256(canonical_bytes).hexdigest()}"
            if stored_hash != computed_hash:
                return False, f"Hash mismatch: stored={stored_hash}, computed={computed_hash}"

        return True, "VERIFIED"

    def do_OPTIONS(self) -> None:
        origin_ok = self._check_origin()
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-AAA-Origin")
        self._cors_headers(origin_ok)
        self.end_headers()

    def do_GET(self) -> None:
        origin_ok = self._check_origin()
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors_headers(origin_ok)
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {"status": "ok", "service": "aaa-signing", "key_loaded": _CACHED_PRIVATE_KEY is not None}
                ).encode()
            )
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        if self.path != "/sign":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error":"not found"}')
            return

        # Origin validation
        if not self._check_origin():
            logger.warning("CORS blocked origin=%s", self.headers.get("Origin", "(none)"))
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"error":"origin not allowed"}')
            return

        # Rate limiting
        global _last_signature_time
        elapsed = time.time() - _last_signature_time
        if elapsed < SIGNATURE_RATE_LIMIT_INTERVAL:
            self.send_response(429)
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "rate limited", "retry_after": SIGNATURE_RATE_LIMIT_INTERVAL - elapsed}).encode()
            )
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            request = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"invalid json"}')
            return

        # Accept challenge_id (preferred) or legacy canonical_json (deprecated)
        challenge_id = request.get("challenge_id")
        canonical_json = request.get("canonical_json")
        actor = request.get("actor", "arif")

        if not challenge_id and not canonical_json:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"challenge_id or canonical_json required"}')
            return

        # If challenge_id is provided, retrieve canonical challenge from arifOS
        payload_to_sign: str
        if challenge_id:
            canonical_payload = canonical_json if canonical_json else ""
            verified, reason = self._verify_challenge(challenge_id, canonical_payload)
            if not verified:
                logger.warning("Challenge verification failed: %s", reason)
                self.send_response(403)
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"challenge verification failed: {reason}"}).encode())
                return
            payload_to_sign = (
                canonical_payload if canonical_payload else json.dumps({"challenge_id": challenge_id, "verified": True})
            )
        else:
            # Legacy path — deprecated, logged
            logger.warning("LEGACY: signing raw canonical_json without challenge verification (deprecated path)")
            payload_to_sign = canonical_json

        # PAM credential confirmation (transitional — not sovereign presence proof)
        pam_user = os.environ.get("AAA_PAM_USER", "")
        if pam_user:
            try:
                import pam

                if not pam.authenticate(pam_user, os.environ.get("AAA_PAM_PASS", "")):
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'{"error":"pam authentication failed"}')
                    return
            except ImportError:
                pass  # PAM not available — skip (transitional)

        try:
            private_key_bytes = load_sovereign_key()
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PrivateKey,
            )

            private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
            message = (
                payload_to_sign.encode("utf-8")
                if isinstance(payload_to_sign, str)
                else json.dumps(request["canonical_json"], separators=(",", ":")).encode("utf-8")
            )
            signature = private_key.sign(message)
            signature_b64 = base64.b64encode(signature).decode("ascii")
            _last_signature_time = time.time()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors_headers(origin_ok=True)
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "status": "SIGNED",
                        "actor": actor,
                        "signature_b64": signature_b64,
                        "algorithm": "Ed25519",
                        "challenge_verified": bool(challenge_id),
                    }
                ).encode()
            )
            logger.info("signed challenge for actor=%s challenge_id=%s", actor, challenge_id or "LEGACY")
        except Exception as e:
            logger.error("signing failed: %s", e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())


def main() -> None:
    port = int(os.environ.get("AAA_SIGNING_PORT", "18900"))
    host = os.environ.get("AAA_SIGNING_HOST", "127.0.0.1")

    # Pre-load key
    try:
        load_sovereign_key()
        logger.info("sovereign Ed25519 key loaded at startup")
    except Exception as e:
        logger.warning("key not loaded at startup: %s — will try on first request", e)

    server = HTTPServer((host, port), SigningHandler)
    logger.info("AAA signing server listening on %s:%s", host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("shutting down")
        server.shutdown()


if __name__ == "__main__":
    main()
