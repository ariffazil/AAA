"""
receipt_signer.py — Canonical RFC 8785 JSON Canonicalization and Ed25519 Signer module.
Authority: F13 Sovereign (Muhammad Arif bin Fazil)
Doctrine: DITEMPA BUKAN DIBERI
"""
from __future__ import annotations
import json
import jsonschema
import nacl.signing
import rfc8785
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent / "schemas" / "receipt.v1.schema.json"

class ReceiptSigner:
    """Signs causally linked receipts after strict schema validation and JCS canonicalization."""
    def __init__(self, signing_key: nacl.signing.SigningKey, key_id: str):
        self._signing_key = signing_key
        self.key_id = key_id
        self._verify_key = signing_key.verify_key
        self.public_key_hex = self._verify_key.encode().hex()
        with open(SCHEMA_PATH) as f:
            self._schema = json.load(f)

    def validate_schema(self, receipt: dict) -> None:
        """Validates that receipt strictly conforms to receipt.v1 JSON Schema."""
        jsonschema.validate(instance=receipt, schema=self._schema)

    def canonicalize(self, receipt: dict) -> bytes:
        """Serializes dictionary to deterministic bytes using RFC 8785 JSON Canonicalization Scheme."""
        return rfc8785.dumps(receipt)

    def sign(self, receipt: dict) -> tuple[dict, str]:
        """
        Validates schema, canonicalizes using RFC 8785, and signs using Ed25519.
        Returns (canonical_dict, ed25519_signature_hex).
        """
        self.validate_schema(receipt)
        if receipt.get("key_id") != self.key_id:
            raise ValueError(f"Receipt key_id '{receipt.get('key_id')}' does not match signer '{self.key_id}'")
        canonical_bytes = self.canonicalize(receipt)
        signed = self._signing_key.sign(canonical_bytes)
        return receipt, signed.signature.hex()
