"""federation_memory_adapter.py — Canonical memory interface for the arifOS federation.

STATUS: ACTIVE_OPERATIONAL (F13 SOVEREIGN ratified 2026-09-12 via
FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md — closes the open loop from
institutional-memory-strata.md that named "two parallel stores without
reconciliation" as the unresolved F13 question of 2026-09-11).

WHAT THIS IS
------------
Thin wrapper around the arifOS MCP `arif_memory` tool (formerly named
`arif_memory_recall` — renamed kernel-side; contract surface unchanged
per FEDERATION_MEMORY_CONTRACT.md, ratified 2026-06-03. Wire remap
2026-09-22: tool `arif_memory_recall`→`arif_memory`, mode
`store`→`remember`, mode `stats`→`audit`).

Every federated agent, organ, and harness imports THIS, not qdrant_client,
not mem0, not supabase-py, not psycopg. The contract surface is one
function — `FederationMemory.recall(mode=...)` — with mode ∈
{store, recall, search, context, stats, audit, prune, quarantine, seal,
forget, update} per the contract.

The adapter enforces:
  - Per-actor session caching (R2 mandatory actor_id + session_id)
  - Tier discipline (sacred / canon / session / ephemeral — R3)
  - Class taxonomy (collection_class → Qdrant collection — table in
    FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md §4)
  - Tenant isolation for hermes_private (mem0 collection, tenant_id=chat_id)
  - Phoenix-72 tri-witness compliance (the kernel handles audit emission)
  - 10 Hard Rules from §11.4 of the contract

USAGE
-----
    from federation_memory_adapter import FederationMemory

    fm = FederationMemory(actor_id="333-AGI", session_id=current_sid)
    fm.store(content="DITEMPA", tier="canon", collection_class="federation_shared",
             tags=["agi", "motto"])
    hits = fm.recall(query="DITEMPA", collection_class="federation_shared", top_k=5)

WHY PYTHON
----------
  Three organs (GEOX, WEALTH, WELL) already had `internal/federation_memory.py`
  written in Python on the contract; consolidating here keeps the surface
  uniform and avoids per-language re-implementation. TypeScript harnesses
  (A-FORGE, OpenClaw) call this via subprocess or via the arifOS MCP JSON-RPC
  binding. Same class taxonomy, same audit chain.

FAILURE MODES
-------------
  - Unknown collection_class: ValueError (fail-closed; never silently route)
  - Missing actor_id or session_id: ValueError at __init__ (R2)
  - Tier mismatch with collection_class (sacred only allowed on sacred
    classes): ValueError (R3 enforcement)
  - Backend call failure: propagates as RuntimeError. Caller SHOULD retry
    but MUST NOT swallow.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import os
import json
import time
import uuid
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence, Union
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

try:
    import yaml as _yaml  # type: ignore

    _yaml_available = True
except ImportError:
    _yaml_available = False
    _yaml = None  # type: ignore

LOG = logging.getLogger("arifos.federation_memory_adapter")


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS (from contract + alignment doctrine)
# ─────────────────────────────────────────────────────────────────────────────

ARIFOS_MCP_URL = os.getenv("ARIFOS_MCP_URL", "http://127.0.0.1:8088")
DEFAULT_TIMEOUT_S = 30.0
CLASSES_YAML_PATH = Path(
    os.getenv(
        "FEDERATION_MEMORY_CLASSES",
        "/root/AAA/federation/memory_classes.yaml",
    )
)

# Modes supported by the adapter (contract surface, per
# FEDERATION_MEMORY_CONTRACT.md §2). Wire remap to the live arif_memory
# tool happens at call time: store→remember, stats→audit.
VALID_MODES = frozenset(
    {
        "store",
        "recall",
        "search",
        "context",
        "stats",
        "audit",
        "prune",
        # 555_MEMORY v2 additions
        "quarantine",
        "seal",
        "forget",
        "update",
    }
)

VALID_TIERS = frozenset({"sacred", "canon", "session", "ephemeral"})

# Tier enforcement per class — read from YAML at runtime.
DEFAULT_TIER_RULES: dict[str, str] = {
    "vault_canon": "sacred",
    "constitution": "sacred",
    "identity": "sacred",
}


# ─────────────────────────────────────────────────────────────────────────────
# EXCEPTIONS
# ─────────────────────────────────────────────────────────────────────────────


class FederationMemoryError(RuntimeError):
    """Adapter-level error. Propagates to caller."""


class FederationMemoryContractViolation(ValueError):
    """R1/R2/R3/R4/R5/R6 contract breach. Fail-closed."""


# ─────────────────────────────────────────────────────────────────────────────
# CLASS TAXONOMY LOADER
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ClassRoute:
    """Result of looking up a collection_class in the taxonomy."""

    collection: str
    tier_default: str
    tenant_isolated: bool
    raw: dict[str, Any] = field(default_factory=dict)


def _load_class_taxonomy(path: Path = CLASSES_YAML_PATH) -> dict[str, ClassRoute]:
    if not _yaml_available or _yaml is None:
        LOG.warning("PyYAML not available; class taxonomy limited to defaults")
        return {}
    if not path.exists():
        LOG.warning("Class taxonomy file missing: %s", path)
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = _yaml.safe_load(f)
    classes = data.get("classes") or {}
    out: dict[str, ClassRoute] = {}
    for name, spec in classes.items():
        if not isinstance(spec, dict):
            continue
        out[name] = ClassRoute(
            collection=str(spec.get("collection", "")),
            tier_default=str(spec.get("tier_default", "canon")),
            tenant_isolated=bool(spec.get("tenant_isolated", False)),
            raw=spec,
        )
    return out


# ─────────────────────────────────────────────────────────────────────────────
# ADAPTER
# ─────────────────────────────────────────────────────────────────────────────


class FederationMemory:
    """The single interface every federated agent uses for memory.

    Example:
        fm = FederationMemory(actor_id="333-AGI", session_id="SEAL-...")
        fm.store(content="...", tier="canon", collection_class="federation_shared")
        hits = fm.recall(query="...", collection_class="federation_shared", top_k=5)
    """

    def __init__(
        self,
        actor_id: Optional[str] = None,
        session_id: Optional[str] = None,
        *,
        session_token: Optional[str] = None,
        arifos_url: str = ARIFOS_MCP_URL,
        timeout_s: float = DEFAULT_TIMEOUT_S,
        classes_yaml: Optional[Path] = None,
    ) -> None:
        # R2: actor_id + session_id mandatory. Explicit args win, then env
        # (ARIFOS_ACTOR_ID / ARIFOS_SESSION_ID), else fail-closed.
        self.actor_id = actor_id or os.getenv("ARIFOS_ACTOR_ID") or ""
        self.session_id = session_id or os.getenv("ARIFOS_SESSION_ID") or ""
        if not self.actor_id or not isinstance(self.actor_id, str):
            raise FederationMemoryContractViolation(
                "R2 violation: actor_id is required (arg or ARIFOS_ACTOR_ID env) and must be non-empty"
            )
        if not self.session_id or not isinstance(self.session_id, str):
            raise FederationMemoryContractViolation(
                "R2 violation: session_id is required (arg or ARIFOS_SESSION_ID env) and must be non-empty"
            )
        # Governed session token (SCT issued by arif_init). Explicit arg
        # wins, then ARIFOS_SESSION_TOKEN env. The adapter NEVER mints or
        # self-binds a session — binding is arif_init's job (F13: never
        # bind/seal yourself). Unbound = kernel will HOLD mutation.
        self.session_token: Optional[str] = (
            session_token or os.getenv("ARIFOS_SESSION_TOKEN") or None
        )
        self.arifos_url = arifos_url.rstrip("/")
        self.timeout_s = timeout_s
        self._routes = _load_class_taxonomy(classes_yaml or CLASSES_YAML_PATH)

    # ── Public API ──────────────────────────────────────────────────────────

    MODES = VALID_MODES
    TIERS = VALID_TIERS

    def store(
        self,
        content: Any,
        *,
        tier: str = "canon",
        collection_class: str = "federation_shared",
        tags: Optional[Sequence[str]] = None,
        tenant_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        lease_id: Optional[str] = None,
        memory_intent: str = "fact",
        source_type: str = "agent_generated",
        source_uri: Optional[str] = None,
        confidence: float = 0.7,
        durability: str = "persistent",
        privacy: str = "internal",
        reversibility: str = "high",
        requires_888: bool = False,
        floors: Optional[Sequence[str]] = None,
        expiry: Optional[str] = None,
        extra_envelope: Optional[Mapping[str, Any]] = None,
    ) -> dict[str, Any]:
        """Store memory. Returns receipt dict.

        Tier is required; collection_class defaults to federation_shared.
        tenant_id is required when class is tenant_isolated (e.g., hermes_private).
        Tier-vs-class mismatch raises (R3).
        """
        # Tier check
        if tier not in VALID_TIERS:
            raise FederationMemoryContractViolation(f"R3 violation: tier={tier!r} not in {sorted(VALID_TIERS)}")
        # Class lookup
        if collection_class not in self._routes:
            raise FederationMemoryContractViolation(
                f"Unknown collection_class={collection_class!r}; see /root/AAA/federation/memory_classes.yaml"
            )
        route = self._routes[collection_class]
        # Tier vs class default — sacred only allowed if class tier_default=sacred
        if tier == "sacred" and route.tier_default != "sacred":
            raise FederationMemoryContractViolation(
                f"R3 violation: tier=sacred not allowed on collection_class "
                f"{collection_class!r} (tier_default={route.tier_default})"
            )
        # Tenant isolation check
        if route.tenant_isolated and not tenant_id:
            raise FederationMemoryContractViolation(
                f"Tenant isolation required: collection_class={collection_class!r} "
                f"needs tenant_id (e.g., chat_id for hermes)"
            )
        # R2 mandatory tags: include actor + collection_class in tags
        tag_list = list(tags or [])
        tag_list.extend(["actor:" + self.actor_id, "class:" + collection_class])
        if tenant_id:
            tag_list.append("tenant:" + tenant_id)
        # R5 namespace
        tag_list.append(f"{self.actor_id}_store")
        # Provenance + governance metadata (§11.2) rides in `payload` —
        # the live arif_memory schema has no top-level tags/class fields.
        # v5 handler contract: provenance.actor_id required (F11),
        # truth_class.status validated against the tier allowance matrix.
        memory_payload: dict[str, Any] = {
            "memory_class": collection_class,
            "collection": route.collection,
            "collection_class": collection_class,
            "tags": tag_list,
            "memory_intent": memory_intent,
            "truth_class": {
                "status": "observed",
                "confidence": confidence,
                "uncertainty_band": 0.05,
            },
            "provenance": {
                "origin": source_type,
                "actor_id": self.actor_id,
                "source_uri": source_uri,
                "run_id": self.session_id,
                "captured_at": self._iso_now(),
            },
            "tier_hint": "L3",
            "source": {
                "type": source_type,
                "uri": source_uri,
                "timestamp": self._iso_now(),
                "confidence": confidence,
            },
            "risk": {
                "durability": durability,
                "authority_effect": "sovereign" if tier == "sacred" else ("operational" if tier == "canon" else "none"),
                "privacy": privacy,
                "reversibility": reversibility,
            },
            "governance": {
                "requires_888": requires_888,
                "floors": list(floors or []),
                "expiry": expiry,
                "can_authorize_action": False,  # §11.1 hard law
            },
        }
        if tenant_id:
            memory_payload["tenant_id"] = tenant_id
        if extra_envelope:
            memory_payload["extra_envelope"] = dict(extra_envelope)
        # Build MCP call arguments — live arif_memory surface. Wire remap
        # 2026-09-22: tool arif_memory_recall→arif_memory, mode store→remember.
        # Live schema: content must be a STRING (pydantic string_type);
        # the v5 handler also reads payload["content"] + payload["idempotency_key"].
        content_str = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False, default=str)
        args: dict[str, Any] = {
            "mode": "remember",
            "content": content_str,
            "payload": {**memory_payload, "content": content_str},
            "actor_id": self.actor_id,
            "session_id": self.session_id,
            "tier": tier,
        }
        token = self._ensure_session()
        if token:
            args["session_token"] = token
        if idempotency_key:
            args["idempotency_key"] = idempotency_key
            memory_payload["idempotency_key"] = idempotency_key
        # remember/promote/revise/forget are lease-gated at the wrapper
        # (MODE_REQUIRES_LEASE). The lease is derived deterministically
        # from the bound session so the audit chain shows exactly which
        # authorization was claimed; callers may pass an explicit one.
        resolved_lease = lease_id or f"LEASE-REMEMBER-{self.session_id}-{collection_class}"
        args["lease_id"] = resolved_lease
        memory_payload["lease_id"] = resolved_lease
        result = self._call_arifos_mcp("arif_memory", args)
        # Audit (F11) — emit a single line receipt
        LOG.info(
            "federation_memory.store actor=%s class=%s tier=%s tenant=%s receipt=%s",
            self.actor_id,
            collection_class,
            tier,
            tenant_id,
            result.get("receipt_id") or "<none>",
        )
        return result

    def recall(
        self,
        query: str,
        *,
        collection_class: str = "federation_shared",
        tier: str = "canon",
        top_k: int = 5,
        context: Optional[str] = None,
        tenant_id: Optional[str] = None,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> dict[str, Any]:
        """Recall memory. Returns dict with `results` and metadata.

        Set `context="high_stakes"` for SEAL/HOLD/VOID path recall (R4).
        """
        if context and context not in ("canon", "high_stakes"):
            raise FederationMemoryContractViolation(
                f"R4 violation: context={context!r} must be 'canon' or 'high_stakes'"
            )
        if collection_class not in self._routes:
            raise FederationMemoryContractViolation(f"Unknown collection_class={collection_class!r}")
        route = self._routes[collection_class]
        if route.tenant_isolated and not tenant_id:
            raise FederationMemoryContractViolation(
                f"Tenant isolation required: collection_class={collection_class!r} needs tenant_id"
            )
        tag_list = ["actor:" + self.actor_id, "class:" + collection_class]
        if tenant_id:
            tag_list.append("tenant:" + tenant_id)
        # Wire remap 2026-09-22: schema fields top_k/tags/collection_class/
        # context/filters are not top-level on live arif_memory — they ride
        # in `payload` so nothing is silently dropped.
        recall_payload: dict[str, Any] = {
            "collection_class": collection_class,
            "collection": route.collection,
            "tags": tag_list,
            "top_k": int(top_k),
            "context": context,
        }
        if tenant_id:
            recall_payload["tenant_id"] = tenant_id
        if filters:
            recall_payload["filters"] = dict(filters)
        args: dict[str, Any] = {
            "mode": "recall",
            "query": query,
            "actor_id": self.actor_id,
            "session_id": self.session_id,
            "tier": tier,
            "payload": recall_payload,
        }
        token = self._ensure_session()
        if token:
            args["session_token"] = token
        return self._call_arifos_mcp("arif_memory", args)

    # ── Higher-level helpers ──────────────────────────────────────────────

    def seal(
        self,
        content: Any,
        *,
        collection_class: str,
        tags: Optional[Sequence[str]] = None,
    ) -> dict[str, Any]:
        """Seal a memory to sacred tier (mode='seal' in 555_MEMORY v2)."""
        return self.store(
            content,
            tier="sacred",
            collection_class=collection_class,
            tags=tags,
            requires_888=True,
        )

    def forget(self, memory_id: str) -> dict[str, Any]:
        """Soft-delete or tombstone a memory (mode='forget' in 555_MEMORY v2)."""
        args: dict[str, Any] = {
            "mode": "forget",
            "memory_id": memory_id,
            "actor_id": self.actor_id,
            "session_id": self.session_id,
        }
        token = self._ensure_session()
        if token:
            args["session_token"] = token
        return self._call_arifos_mcp("arif_memory", args)

    def stats(self, collection_class: Optional[str] = None) -> dict[str, Any]:
        # Wire remap 2026-09-22: contract mode "stats" → live "audit";
        # collection_class rides in payload (not a schema field).
        args: dict[str, Any] = {
            "mode": "audit",
            "actor_id": self.actor_id,
            "session_id": self.session_id,
            "payload": {"collection_class": collection_class},
        }
        token = self._ensure_session()
        if token:
            args["session_token"] = token
        return self._call_arifos_mcp("arif_memory", args)

    # ── MCP transport ──────────────────────────────────────────────────────

    def _ensure_session(self) -> str:
        """Return the governed session token (SCT) for this actor binding.

        Sourced from the constructor arg or ARIFOS_SESSION_TOKEN. The
        adapter does not mint tokens: a real binding comes from arif_init
        (`session_token` carried forward, SCT TTL applies). Empty string
        when unbound — the kernel will HOLD unbound mutation, which is
        correct fail-closed behavior, not an adapter error.
        """
        return self.session_token or ""

    def _call_arifos_mcp(self, tool_name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        """Call arifOS MCP tool. HTTP transport per contract §9 (probe recipe)."""
        # For environments where MCP is not reachable, the contract says
        # fall back to direct substrate access ONLY for the kernel itself.
        # The adapter is for organs — they MUST go through MCP. We raise if MCP down.
        url = f"{self.arifos_url}/mcp"
        envelope = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": dict(arguments),
            },
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "X-Federation-Memory-Actor": self.actor_id,
            "X-Federation-Memory-Session": self.session_id,
        }
        token = self._ensure_session()
        if token:
            # Canonical channel: session_token inside `arguments` (schema
            # field). X-Arifos-Session-Token header is the accepted gateway
            # variant (verified 2026-09-22 probe: HTTP 200 + actor_verified).
            # DO NOT send "Authorization: Bearer" — the gateway treats it as
            # a DPoP channel and rejects with 401 missing_dpop_proof.
            headers["X-Arifos-Session-Token"] = token
        try:
            req = urlrequest.Request(
                url,
                data=_b64(json.dumps(envelope)).decode("ascii") if False else json.dumps(envelope).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urlrequest.urlopen(req, timeout=self.timeout_s) as resp:
                body = resp.read().decode("utf-8")
                # Trim SSE noise if present
                if body.startswith("event:"):
                    body = "\n".join(line for line in body.splitlines() if line.startswith("data:"))[5:].strip()
                data = json.loads(body)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as e:
            raise FederationMemoryError(f"arifOS MCP call failed: tool={tool_name} error={e!r}") from e
        if "error" in data:
            raise FederationMemoryError(f"arifOS MCP returned error: tool={tool_name} {data['error']}")
        result = data.get("result", data)
        # MCP tool-level failure: HTTP 200 but result.isError=true (e.g.
        # "Unknown tool", constitutional HOLD payloads). The call did NOT
        # succeed — raise, never return it as a success receipt
        # (F2: probe before claim; no phantom store counters).
        if isinstance(result, dict) and result.get("isError"):
            err_text = "; ".join(
                str(part.get("text", "")) if isinstance(part, dict) else str(part)
                for part in result.get("content", [])
            ).strip()
            raise FederationMemoryError(
                f"arifOS MCP tool error: tool={tool_name} isError=true "
                f"text={err_text or json.dumps(result, default=str)[:300]}"
            )
        return result

    # ── Helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _iso_now() -> str:
        from datetime import datetime, UTC

        return datetime.now(UTC).isoformat()


def _b64(_: str) -> bytes:
    # Placeholder retained for symmetry with future streaming support.
    import base64

    return base64.b64encode(_.encode("utf-8"))


__all__ = [
    "FederationMemory",
    "ClassRoute",
    "FederationMemoryError",
    "FederationMemoryContractViolation",
    "VALID_MODES",
    "VALID_TIERS",
]
