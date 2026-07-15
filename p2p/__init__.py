"""AAA P2P inner-loop socket layer (Phase 3a).

Unix domain socket mesh between 333-AGI, 555-ASI, and 888-APEX.
Stdlib-only asyncio implementation. F11 audit hash-chained.

Public surface:
    audit.AuditLog        — append-only hash-chained ledger
    audit.verify_chain    — verify hash chain integrity
    socket_server.P2PServer — asyncio Unix-socket server
    socket_client.P2PClient — asyncio client
    protocol.Message       — typed message dataclass
    protocol.MESSAGE_SCHEMA — JSON schema for validation
"""

from .protocol import (
    Message,
    MESSAGE_SCHEMA,
    ALLOWED_AGENTS,
    ALLOWED_VERBS,
    ALLOWED_BLAST,
    validate_message,
    canonical_json,
    new_message,
)

__all__ = [
    "Message",
    "MESSAGE_SCHEMA",
    "ALLOWED_AGENTS",
    "ALLOWED_VERBS",
    "ALLOWED_BLAST",
    "validate_message",
    "canonical_json",
    "new_message",
]

__version__ = "1.0.0"