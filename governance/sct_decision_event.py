"""
SCT Decision Event — PR 3 observability foundation.

Every ALLOW/REJECT at organ ingress produces one structured decision event:
  - shared trace_id (black-box incident number)
  - organ, tool, action_class (registry-owned)
  - SCT fingerprint only (never raw token)
  - decision + reason
  - timestamp

Events are append-only JSONL for local observability. VAULT999 gets a
rollup later (PR7) — not every line.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("federation.sct.decision")

SCHEMA_VERSION = "sct_decision_event.v1"
SCHEMA_ID = "https://arif-fazil.com/schema/sct_decision_event/v1"

# Where detailed events land (observability plane — not VAULT999)
_DEFAULT_EVENT_DIR = Path(
    os.environ.get(
        "SCT_DECISION_EVENT_DIR",
        "/root/A-FORGE/forge_work/2026-07-17/sct_decision_events",
    )
)


@dataclass
class SctDecisionEvent:
    """One ingress decision. Secret tokens NEVER stored."""

    schema: str = SCHEMA_VERSION
    schema_id: str = SCHEMA_ID
    event_id: str = ""
    trace_id: str = ""
    ts: str = ""
    organ: str = "unknown"
    tool: str = ""
    action_class: str = ""
    required_authority: str = ""
    require_sct: bool = False
    decision: str = ""  # ALLOW | REJECT
    reason_code: str = ""  # SCT_REQUIRED | SCT_AMBIGUOUS | SCT_INVALID | OK | …
    actor_id: str = ""
    sct_fingerprint: str = ""  # sha256:… or empty if absent
    sct_source_count: int = 0
    sct_unique_tokens: int = 0
    registry_source: str = ""  # tools.yaml | organ_default | …
    registry_known: bool = False
    extraction_locations: list[str] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_jsonl(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))


def new_trace_id() -> str:
    """Mint a federation-wide trace id for one request chain."""
    return f"trc-{uuid.uuid4().hex[:16]}"


def extract_trace_id(
    arguments: dict[str, Any] | None = None,
    *,
    headers: dict[str, str] | None = None,
    meta: dict[str, Any] | None = None,
) -> str:
    """Resolve trace_id from args / _meta / headers; mint if absent.

    Propagation order (first non-empty wins — trace ids are not secrets;
    multi-source conflict is rare and we prefer continuity of an existing id):
      1. arguments.trace_id
      2. arguments._meta.trace_id
      3. meta.trace_id
      4. headers X-Trace-Id / X-ArifOS-Trace / traceparent (W3C: version-traceid-…)
    """
    args = arguments if isinstance(arguments, dict) else {}

    for key in ("trace_id", "traceId"):
        v = args.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()

    nested = args.get("_meta") if isinstance(args.get("_meta"), dict) else None
    if nested:
        for key in ("trace_id", "traceId"):
            v = nested.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()

    if meta and isinstance(meta, dict):
        for key in ("trace_id", "traceId"):
            v = meta.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()

    if headers:
        lower = {str(k).lower(): v for k, v in headers.items()}
        for key in ("x-trace-id", "x-arifos-trace", "x-request-id"):
            v = lower.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
        # W3C traceparent: 00-<trace-id>-<span-id>-<flags>
        tp = lower.get("traceparent") or ""
        if isinstance(tp, str) and tp.count("-") >= 2:
            parts = tp.split("-")
            if len(parts) >= 2 and len(parts[1]) >= 8:
                return f"trc-w3c-{parts[1][:16]}"

    return new_trace_id()


def build_decision_event(
    *,
    tool: str,
    organ: str,
    decision: str,
    reason_code: str,
    trace_id: str | None = None,
    actor_id: str = "",
    action_class: str = "",
    required_authority: str = "",
    require_sct: bool = False,
    sct_fingerprint: str = "",
    sct_source_count: int = 0,
    sct_unique_tokens: int = 0,
    registry_source: str = "",
    registry_known: bool = False,
    extraction_locations: list[str] | None = None,
    meta: dict[str, Any] | None = None,
) -> SctDecisionEvent:
    """Construct a decision event (does not persist)."""
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return SctDecisionEvent(
        event_id=f"sde-{uuid.uuid4().hex[:12]}",
        trace_id=trace_id or new_trace_id(),
        ts=now,
        organ=organ,
        tool=tool,
        action_class=action_class,
        required_authority=required_authority,
        require_sct=require_sct,
        decision=decision,
        reason_code=reason_code,
        actor_id=actor_id or "",
        sct_fingerprint=sct_fingerprint or "",
        sct_source_count=int(sct_source_count or 0),
        sct_unique_tokens=int(sct_unique_tokens or 0),
        registry_source=registry_source or "",
        registry_known=bool(registry_known),
        extraction_locations=list(extraction_locations or []),
        meta=dict(meta or {}),
    )


def append_decision_event(
    event: SctDecisionEvent,
    *,
    directory: Path | None = None,
) -> Path | None:
    """Append event as JSONL. Returns path written, or None on failure.

    Fail-open for observability I/O: never block the gate if disk is full.
    """
    d = directory or _DEFAULT_EVENT_DIR
    try:
        d.mkdir(parents=True, exist_ok=True)
        day = time.strftime("%Y-%m-%d", time.gmtime())
        path = d / f"sct_decisions_{day}.jsonl"
        with path.open("a", encoding="utf-8") as fh:
            fh.write(event.to_jsonl() + "\n")
        return path
    except OSError as exc:
        logger.warning("sct_decision_event: append failed: %s", exc)
        return None


def emit_decision(
    *,
    tool: str,
    organ: str,
    decision: str,
    reason_code: str,
    arguments: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    meta: dict[str, Any] | None = None,
    actor_id: str = "",
    action_class: str = "",
    required_authority: str = "",
    require_sct: bool = False,
    sct_fingerprint: str = "",
    sct_source_count: int = 0,
    sct_unique_tokens: int = 0,
    registry_source: str = "",
    registry_known: bool = False,
    extraction_locations: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> SctDecisionEvent:
    """Build + append one decision event. Returns the event."""
    tid = extract_trace_id(arguments, headers=headers, meta=meta)
    event = build_decision_event(
        tool=tool,
        organ=organ,
        decision=decision,
        reason_code=reason_code,
        trace_id=tid,
        actor_id=actor_id,
        action_class=action_class,
        required_authority=required_authority,
        require_sct=require_sct,
        sct_fingerprint=sct_fingerprint,
        sct_source_count=sct_source_count,
        sct_unique_tokens=sct_unique_tokens,
        registry_source=registry_source,
        registry_known=registry_known,
        extraction_locations=extraction_locations,
        meta=extra,
    )
    path = append_decision_event(event)
    if path:
        logger.info(
            "sct_decision %s organ=%s tool=%s decision=%s reason=%s trace=%s fp=%s file=%s",
            event.event_id,
            organ,
            tool,
            decision,
            reason_code,
            event.trace_id,
            sct_fingerprint or "-",
            path.name,
        )
    return event


# JSON Schema (for PR5 cockpit / validators)
DECISION_EVENT_JSON_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": SCHEMA_ID,
    "title": "SCT Decision Event",
    "type": "object",
    "required": [
        "schema",
        "event_id",
        "trace_id",
        "ts",
        "organ",
        "tool",
        "decision",
        "reason_code",
    ],
    "properties": {
        "schema": {"const": SCHEMA_VERSION},
        "schema_id": {"type": "string"},
        "event_id": {"type": "string"},
        "trace_id": {"type": "string"},
        "ts": {"type": "string"},
        "organ": {"type": "string"},
        "tool": {"type": "string"},
        "action_class": {"type": "string"},
        "required_authority": {"type": "string"},
        "require_sct": {"type": "boolean"},
        "decision": {"enum": ["ALLOW", "REJECT"]},
        "reason_code": {"type": "string"},
        "actor_id": {"type": "string"},
        "sct_fingerprint": {
            "type": "string",
            "description": "sha256:… prefix only — never raw SCT",
        },
        "sct_source_count": {"type": "integer", "minimum": 0},
        "sct_unique_tokens": {"type": "integer", "minimum": 0},
        "registry_source": {"type": "string"},
        "registry_known": {"type": "boolean"},
        "extraction_locations": {"type": "array", "items": {"type": "string"}},
        "meta": {"type": "object"},
    },
    "additionalProperties": False,
}


__all__ = [
    "SCHEMA_VERSION",
    "SCHEMA_ID",
    "SctDecisionEvent",
    "DECISION_EVENT_JSON_SCHEMA",
    "new_trace_id",
    "extract_trace_id",
    "build_decision_event",
    "append_decision_event",
    "emit_decision",
]
