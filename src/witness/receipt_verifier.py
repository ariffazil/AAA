"""
receipt_verifier.py — Independent RFC 8785 JSON Canonicalization and Ed25519 Verifier module.
Authority: F13 Sovereign (Muhammad Arif bin Fazil)
Doctrine: DITEMPA BUKAN DIBERI
"""
from __future__ import annotations
import json
import jsonschema
import nacl.signing
import nacl.exceptions
import rfc8785
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent / "schemas" / "receipt.v1.schema.json"

class ReceiptVerifier:
    """Verifies that receipts are structurally valid and cryptographically authentic."""
    def __init__(self, public_key_hex: str):
        self.public_key_hex = public_key_hex
        self._verify_key = nacl.signing.VerifyKey(bytes.fromhex(public_key_hex))
        with open(SCHEMA_PATH) as f:
            self._schema = json.load(f)

    def validate_schema(self, receipt: dict) -> None:
        """Validates that receipt strictly conforms to receipt.v1 JSON Schema."""
        jsonschema.validate(instance=receipt, schema=self._schema)

    def canonicalize(self, receipt: dict) -> bytes:
        """Serializes dictionary to deterministic bytes using RFC 8785 JSON Canonicalization Scheme."""
        return rfc8785.dumps(receipt)

    def verify(self, receipt: dict, signature_hex: str) -> bool:
        """
        Validates schema, canonicalizes bytes, and checks Ed25519 signature against public key.
        Returns True if authentic. Raises BadSignatureError or ValidationError if invalid.
        """
        self.validate_schema(receipt)
        canonical_bytes = self.canonicalize(receipt)
        self._verify_key.verify(canonical_bytes, bytes.fromhex(signature_hex))
        return True
