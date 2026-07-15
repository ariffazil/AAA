"""P2P message schema and validation (F12 INJECTION guard).

Stdlib only. Python 3.12+ syntax.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


# ── Schema constants ────────────────────────────────────────────────────────

ALLOWED_AGENTS: frozenset[str] = frozenset({"333-AGI", "555-ASI", "888-APEX"})
ALLOWED_VERBS: frozenset[str] = frozenset({"propose", "translate", "judge", "ack", "reject"})
ALLOWED_BLAST: frozenset[str] = frozenset({"LOW", "MEDIUM", "HIGH", "IRREVERSIBLE"})

# Schema as a dict; validate_message() walks it. We do not depend on jsonschema
# to stay stdlib-only. Keys are required field names; "types" maps each field
# to its expected python type. Payload is intentionally untyped (verb-specific).
MESSAGE_SCHEMA: dict[str, Any] = {
    "required": [
        "from", "to", "verb", "payload", "timestamp",
        "requires_judgment", "blast_radius",
    ],
    "types": {
        "from": str,
        "to": str,
        "verb": str,
        "payload": dict,
        "timestamp": str,
        "requires_judgment": bool,
        "blast_radius": str,
    },
    "optional": {
        "session_id": str,
        "signature": (str, type(None)),
    },
    "enums": {
        "from": ALLOWED_AGENTS,
        "to": ALLOWED_AGENTS | {"all"},
        "verb": ALLOWED_VERBS,
        "blast_radius": ALLOWED_BLAST,
    },
}


# ── Validation ─────────────────────────────────────────────────────────────


class SchemaError(ValueError):
    """Raised when an inbound message fails schema validation (F12 INJECTION)."""


def validate_message(msg: Any) -> None:
    """Validate a parsed JSON message against MESSAGE_SCHEMA.

    Raises SchemaError with a precise code if anything is wrong. F12
    INJECTION guard: never trust the wire — check every field.
    """
    if not isinstance(msg, dict):
        raise SchemaError(f"F12_SCHEMA:not_a_dict:got_{type(msg).__name__}")

    for key in MESSAGE_SCHEMA["required"]:
        if key not in msg:
            raise SchemaError(f"F12_SCHEMA:missing_field:{key}")

    types = MESSAGE_SCHEMA["types"]
    for key, expected in types.items():
        if not isinstance(msg[key], expected):
            raise SchemaError(
                f"F12_SCHEMA:bad_type:{key}:expected_{expected.__name__}_got_{type(msg[key]).__name__}"
            )

    enums = MESSAGE_SCHEMA["enums"]
    for key, allowed in enums.items():
        if msg[key] not in allowed:
            raise SchemaError(
                f"F12_SCHEMA:bad_enum:{key}:{msg[key]!r}_not_in_{sorted(allowed)}"
            )

    # F1 AMANAH: signature is required for IRREVERSIBLE blast radius.
    if msg["blast_radius"] == "IRREVERSIBLE" and not msg.get("signature"):
        raise SchemaError("F1_ED25519_REQUIRED:irreversible_must_sign")

    # Optional fields: only accept known keys with correct types.
    for key, expected in MESSAGE_SCHEMA["optional"].items():
        if key in msg and not isinstance(msg[key], expected):
            raise SchemaError(
                f"F12_SCHEMA:bad_optional_type:{key}:got_{type(msg[key]).__name__}"
            )

    # Reject unknown top-level keys to keep wire format tight.
    allowed_keys = set(types) | set(MESSAGE_SCHEMA["optional"])
    unknown = set(msg) - allowed_keys
    if unknown:
        raise SchemaError(f"F12_SCHEMA:unknown_fields:{sorted(unknown)}")


# ── Canonical JSON (for hashing) ────────────────────────────────────────────


def canonical_json(obj: Any) -> str:
    """RFC-8785-ish canonical JSON: sorted keys, no whitespace, UTF-8.

    Used both for hashing (audit chain) and Ed25519 signing (when added).
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


# ── Typed message ───────────────────────────────────────────────────────────


@dataclass(slots=True)
class Message:
    """Typed P2P message. Wire format = asdict() + JSON."""

    sender: str  # "from" on the wire
    recipient: str  # "to" on the wire — agent id or "all"
    verb: str
    payload: dict[str, Any]
    blast_radius: str = "LOW"
    requires_judgment: bool = False
    session_id: str | None = None
    signature: str | None = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_wire(self) -> dict[str, Any]:
        """Serialise to wire dict (matches schema 1:1)."""
        d: dict[str, Any] = {
            "from": self.sender,
            "to": self.recipient,
            "verb": self.verb,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "requires_judgment": self.requires_judgment,
            "blast_radius": self.blast_radius,
        }
        if self.session_id is not None:
            d["session_id"] = self.session_id
        if self.signature is not None:
            d["signature"] = self.signature
        return d

    @classmethod
    def from_wire(cls, d: dict[str, Any]) -> "Message":
        """Parse a wire dict into a Message. Assumes validate_message() ran."""
        return cls(
            sender=d["from"],
            recipient=d["to"],
            verb=d["verb"],
            payload=d["payload"],
            timestamp=d["timestamp"],
            requires_judgment=d["requires_judgment"],
            blast_radius=d["blast_radius"],
            session_id=d.get("session_id"),
            signature=d.get("signature"),
        )


def new_message(
    sender: str,
    recipient: str,
    verb: str,
    payload: dict[str, Any],
    *,
    blast_radius: str = "LOW",
    requires_judgment: bool = False,
    session_id: str | None = None,
    signature: str | None = None,
) -> dict[str, Any]:
    """Build a fresh wire-format message with the current timestamp."""
    msg = Message(
        sender=sender,
        recipient=recipient,
        verb=verb,
        payload=payload,
        blast_radius=blast_radius,
        requires_judgment=requires_judgment,
        session_id=session_id,
        signature=signature,
    )
    return msg.to_wire()