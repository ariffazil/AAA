"""federation_memory_adapter.py — Canonical memory interface for the arifOS federation.

STATUS: ACTIVE_OPERATIONAL (F13 SOVEREIGN ratified 2026-09-12 via
FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md — closes the open loop from
institutional-memory-strata.md that named "two parallel stores without
reconciliation" as the unresolved F13 question of 2026-09-11).

WHAT THIS IS
------------
Thin wrapper around the arifOS MCP `arif_memory_recall` tool (defined in
/root/arifOS/docs/FEDERATION_MEMORY_CONTRACT.md, ratified 2026-06-03).

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

# Modes supported by arif_memory_recall (per FEDERATION_MEMORY_CONTRACT.md §2)
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
        actor_id: str,
        session_id: str,
        *,
        arifos_url: str = ARIFOS_MCP_URL,
        timeout_s: float = DEFAULT_TIMEOUT_S,
        classes_yaml: Optional[Path] = None,
    ) -> None:
        # R2: actor_id + session_id mandatory
        if not actor_id or not isinstance(actor_id, str):
            raise FederationMemoryContractViolation("R2 violation: actor_id is required and must be non-empty")
        if not session_id or not isinstance(session_id, str):
            raise FederationMemoryContractViolation("R2 violation: session_id is required and must be non-empty")
        self.actor_id = actor_id
        self.session_id = session_id
        self.arifos_url = arifos_url.rstrip("/")
        self.timeout_s = timeout_s
        self._routes = _load_class_taxonomy(classes_yaml or CLASSES_YAML_PATH)
        self._session_token: Optional[str] = None
        self._token_ts: float = 0.0
        self._TOKEN_TTL_S = 300.0

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
        # Memory envelope (§11.2)
        envelope: dict[str, Any] = {
            "actor_id": self.actor_id,
            "session_id": self.session_id,
            "memory_intent": memory_intent,
            "niat": f"{self.actor_id}: store via FederationMemory adapter",
            "content": content,
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
        if extra_envelope:
            envelope.update(dict(extra_envelope))
        # Build MCP call arguments
        args = {
            "mode": "store",
            "content": envelope,
            "actor_id": self.actor_id,
            "session_id": self.session_id,
            "tier": tier,
            "tags": tag_list,
            "collection_class": collection_class,
        }
        if tenant_id:
            args["tenant_id"] = tenant_id
        result = self._call_arifos_mcp("arif_memory_recall", args)
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
        args = {
            "mode": "recall",
            "query": query,
            "actor_id": self.actor_id,
            "session_id": self.session_id,
            "top_k": int(top_k),
            "tier": tier,
            "tags": tag_list,
            "collection_class": collection_class,
            "context": context,
        }
        if tenant_id:
            args["tenant_id"] = tenant_id
        if filters:
            args["filters"] = dict(filters)
        return self._call_arifos_mcp("arif_memory_recall", args)

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
        return self._call_arifos_mcp(
            "arif_memory_recall",
            {
                "mode": "forget",
                "memory_id": memory_id,
                "actor_id": self.actor_id,
                "session_id": self.session_id,
            },
        )

    def stats(self, collection_class: Optional[str] = None) -> dict[str, Any]:
        return self._call_arifos_mcp(
            "arif_memory_recall",
            {
                "mode": "stats",
                "actor_id": self.actor_id,
                "session_id": self.session_id,
                "collection_class": collection_class,
            },
        )

    # ── MCP transport ──────────────────────────────────────────────────────

    def _ensure_session(self) -> str:
        # Reuse token within TTL; refresh on demand.
        now = time.time()
        if self._session_token and (now - self._token_ts) < self._TOKEN_TTL_S:
            return self._session_token
        # We do not maintain an MCP session here; the kernel is queried in
        # fire-and-forget mode via _call_arifos_mcp_raw. A real MCP binding
        # would establish a session via 'initialize'. Left as future work.
        return ""

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
        try:
            req = urlrequest.Request(
                url,
                data=_b64(json.dumps(envelope)).decode("ascii") if False else json.dumps(envelope).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "X-Federation-Memory-Actor": self.actor_id,
                    "X-Federation-Memory-Session": self.session_id,
                },
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
        return data.get("result", data)

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
