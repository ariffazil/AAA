#!/usr/bin/env python3
"""
signing_server.py — F13 Ed25519 challenge signing endpoint for AAA approval card.

Listens on localhost:18900. Accepts canonical challenge payloads,
signs with the sovereign Ed25519 private key, returns base64 signature.

This is the bridge between the one-tap approval UI and the cryptographic
signing machinery. The user presses [Approve]; this server handles the crypto.

Usage:
    python auth/signing_server.py           # start on :18900
    systemctl start aaa-signing             # production
"""

from __future__ import annotations

import base64
import json
import logging
import os
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

logger = logging.getLogger("aaa.signing")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

KEYS_DIR = Path(__file__).resolve().parent / "keys"
ARIF_PRIVATE_KEY = KEYS_DIR / "arifos_private.key"

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

    def _cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
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
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error":"not found"}')
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            request = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error":"invalid json"}')
            return

        canonical_json = request.get("canonical_json")
        actor = request.get("actor", "arif")

        if not canonical_json:
            self.send_response(400)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error":"canonical_json required"}')
            return

        try:
            private_key_bytes = load_sovereign_key()
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PrivateKey,
            )

            private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
            message = (
                canonical_json.encode("utf-8")
                if isinstance(canonical_json, str)
                else json.dumps(request["canonical_json"], separators=(",", ":")).encode("utf-8")
            )
            signature = private_key.sign(message)
            signature_b64 = base64.b64encode(signature).decode("ascii")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "status": "SIGNED",
                        "actor": actor,
                        "signature_b64": signature_b64,
                        "algorithm": "Ed25519",
                    }
                ).encode()
            )
            logger.info("signed challenge for actor=%s", actor)
        except Exception as e:
            logger.error("signing failed: %s", e)
            self.send_response(500)
            self._cors_headers()
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
