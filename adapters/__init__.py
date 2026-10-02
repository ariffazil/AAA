"""AAA organ adapters (PR-3 ONE-DOOR, 2026-10-02).

Stable AAA-owned contracts in front of federation organs. AAA consumes
organ *capabilities* over HTTP/MCP through these adapters — never organ
filesystems, never sys.path reach-ins, never organ python imports.

    MeaningAdapter  — HERMES meaning capability (:18087)
    TemporalAdapter — CHRON temporal capability (:18102)

Shared transport: adapters._mcp_http (streamable-HTTP MCP, stdlib only).
F1 AMANAH: every adapter fails closed with typed degradation, never
substitutes a guess for an unreachable organ.
"""

from .meaning_adapter import ADAPTER_VERSION as MEANING_ADAPTER_VERSION
from .meaning_adapter import MeaningAdapter
from .temporal_adapter import ADAPTER_VERSION as TEMPORAL_ADAPTER_VERSION
from .temporal_adapter import TemporalAdapter

__all__ = [
    "MeaningAdapter",
    "MEANING_ADAPTER_VERSION",
    "TemporalAdapter",
    "TEMPORAL_ADAPTER_VERSION",
]
