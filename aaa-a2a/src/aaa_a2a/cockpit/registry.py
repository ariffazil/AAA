"""AAA Cockpit — Live Agent Registry with TTL Tombstoning.

Maintains an in-memory registry of agent states, updated via:
  1. Heartbeats POSTed by organs themselves (push)
  2. Background health probes by AAA itself (pull)

Agents missing 3 consecutive probes are tombstoned (TTL = 45s at 15s interval).
Static agent cards at /root/AAA/agent-cards/ serve as fallback definitions.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("aaa.cockpit.registry")

# ── Constants ──────────────────────────────────────────────────────────────

PROBE_INTERVAL_SECONDS = 15
MAX_MISSED_PROBES = 3  # = TTL of 45 seconds
STATUS_JSON_PATH = Path("/root/AAA/state/status.json")
ORGANS_YAML_PATH = Path("/root/AAA/federation/organs.yaml")
AGENT_CARDS_PATH = Path("/root/AAA/agent-cards")

# Organs that we actively probe (must expose /health)
PROBED_ORGANS: list[dict[str, Any]] = [
    {"id": "arifos", "port": 8088, "role": "Kernel", "ceiling": "JUDGE_ONLY"},
    {"id": "a-forge", "port": 7071, "role": "Execution", "ceiling": "EXECUTE_AFTER_SEAL"},
    {"id": "aaa", "port": 3001, "role": "Control Plane", "ceiling": "DISPLAY_ONLY"},
    {"id": "geox", "port": 8081, "role": "Earth Intelligence", "ceiling": "COMPUTE_ONLY"},
    {"id": "wealth", "port": 18082, "role": "Capital Intelligence", "ceiling": "COMPUTE_ONLY"},
    {"id": "well", "port": 18083, "role": "Vitality Mirror", "ceiling": "REFLECT_ONLY"},
    {"id": "arifflow", "port": 7073, "role": "Metabolism", "ceiling": "METABOLIZE_ONLY"},
]

# Additional services probed for completeness
PROBED_SERVICES: list[dict[str, Any]] = [
    {"id": "flame", "port": 18901, "role": "Free Inference", "ceiling": "ADVISORY_WORKER"},
    {"id": "fed", "port": 7074, "role": "Model Router", "ceiling": "ADVISORY_ONLY"},
    {"id": "hermes", "port": 18086, "role": "Telegram Bridge", "ceiling": "RELAY_ONLY"},
]


# ── Models ─────────────────────────────────────────────────────────────────


@dataclass
class HeartbeatPayload:
    """What an organ sends to register its liveness."""

    agent_id: str
    status: str = "healthy"  # healthy | degraded | dead
    load: float = 0.0  # CPU load or capacity
    capabilities: list[str] = field(default_factory=list)
    tools_count: int = 0
    latency_ms: float = 0.0
    sct: str | None = None
    apex_scalars: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentState:
    """Live state of one agent in the cockpit registry."""

    agent_id: str
    name: str = ""
    role: str = ""
    authority_ceiling: str = ""
    port: int = 0
    status: str = "unknown"  # healthy | degraded | dead | unknown
    last_seen: float = 0.0  # Unix timestamp
    missed_probes: int = 0
    latency_ms: float = 0.0
    load: float = 0.0
    capabilities: list[str] = field(default_factory=list)
    tools_count: int = 0
    apex_scalars: dict[str, Any] = field(default_factory=dict)
    source: str = "static"  # static | heartbeat | probe
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_alive(self) -> bool:
        return self.status in ("healthy", "degraded")

    @property
    def is_dead(self) -> bool:
        return self.status == "dead"

    @property
    def age_seconds(self) -> float:
        if self.last_seen == 0:
            return float("inf")
        return time.time() - self.last_seen

    @property
    def ttl_status(self) -> str:
        """Human-readable TTL status."""
        if self.is_dead:
            return "🪦 DEAD"
        age = self.age_seconds
        if age < 30:
            return "🟢 LIVE"
        elif age < 60:
            return "🟡 STALE"
        elif age < 120:
            return "🟠 GHOST"
        return "🔴 LOST"


# ── Registry ───────────────────────────────────────────────────────────────


class AgentRegistry:
    """In-memory registry of all agents with live state tracking.

    Not thread-safe — assumes single-threaded asyncio usage."""

    def __init__(self):
        self._agents: dict[str, AgentState] = {}
        self._boot_time: float = time.time()
        self._probe_count: int = 0
        self._last_probe: float = 0.0
        self._heartbeats_received: int = 0

    # ── Registration ───────────────────────────────────────────────────

    def register_static(self, agent_id: str, **kwargs: Any) -> AgentState:
        """Register an agent from static definition (agent cards, organs.yaml)."""
        state = AgentState(agent_id=agent_id, source="static", **kwargs)
        self._agents[agent_id] = state
        return state

    def receive_heartbeat(self, payload: HeartbeatPayload) -> AgentState:
        """Process a heartbeat from a live organ."""
        current = self._agents.get(payload.agent_id)
        if current is None:
            current = AgentState(
                agent_id=payload.agent_id,
                source="heartbeat",
                name=payload.agent_id,
            )
            self._agents[payload.agent_id] = current

        current.status = payload.status
        current.last_seen = time.time()
        current.missed_probes = 0
        current.latency_ms = payload.latency_ms
        current.load = payload.load
        current.capabilities = payload.capabilities
        current.tools_count = payload.tools_count
        current.apex_scalars = payload.apex_scalars
        current.metadata = payload.metadata
        current.source = "heartbeat"

        self._heartbeats_received += 1
        logger.debug(f"Heartbeat from {payload.agent_id}: {payload.status}")
        return current

    def update_from_probe(
        self,
        agent_id: str,
        healthy: bool,
        latency_ms: float = 0.0,
        apex_scalars: dict[str, Any] | None = None,
        tools_count: int = 0,
    ) -> AgentState:
        """Update agent state from an active health probe."""
        current = self._agents.get(agent_id)
        if current is None:
            current = AgentState(
                agent_id=agent_id,
                source="probe",
                name=agent_id,
            )
            self._agents[agent_id] = current

        if healthy:
            current.status = "healthy"
            current.missed_probes = 0
        else:
            current.missed_probes += 1
            if current.missed_probes >= MAX_MISSED_PROBES:
                current.status = "dead"
            elif current.missed_probes >= 2:
                current.status = "degraded"

        current.last_seen = time.time()
        current.latency_ms = latency_ms
        current.source = "probe"
        if apex_scalars:
            current.apex_scalars = apex_scalars
        if tools_count:
            current.tools_count = tools_count
        return current

    def mark_unreachable(self, agent_id: str, reason: str = "") -> AgentState:
        """Mark an agent as unreachable (missed probe)."""
        current = self._agents.get(agent_id)
        if current is None:
            current = AgentState(agent_id=agent_id, source="probe", name=agent_id)
            self._agents[agent_id] = current

        current.missed_probes += 1
        if current.missed_probes >= MAX_MISSED_PROBES:
            current.status = "dead"
        elif current.missed_probes >= 2:
            current.status = "degraded"
        current.last_seen = time.time()
        current.metadata["last_reason"] = reason
        return current

    # ── Query ──────────────────────────────────────────────────────────

    def get(self, agent_id: str) -> AgentState | None:
        return self._agents.get(agent_id)

    def list_all(self) -> list[AgentState]:
        return sorted(self._agents.values(), key=lambda a: a.agent_id)

    def list_alive(self) -> list[AgentState]:
        return [a for a in self._agents.values() if a.is_alive]

    def list_dead(self) -> list[AgentState]:
        return [a for a in self._agents.values() if a.is_dead]

    def summary(self) -> dict[str, Any]:
        """Return a summary of the registry for status.json."""
        alive = self.list_alive()
        dead = self.list_dead()
        all_agents = self.list_all()

        return {
            "cockpit_version": "2.0.0-live",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": round(time.time() - self._boot_time, 1),
            "probe_count": self._probe_count,
            "last_probe_at": datetime.fromtimestamp(self._last_probe, tz=timezone.utc).isoformat()
            if self._last_probe
            else None,
            "heartbeats_received": self._heartbeats_received,
            "agents": {
                "total": len(all_agents),
                "alive": len(alive),
                "dead": len(dead),
            },
            "agent_list": [
                {
                    "agent_id": a.agent_id,
                    "name": a.name,
                    "role": a.role,
                    "authority_ceiling": a.authority_ceiling,
                    "port": a.port,
                    "status": a.status,
                    "ttl": a.ttl_status,
                    "age_seconds": round(a.age_seconds, 1) if a.last_seen > 0 else None,
                    "latency_ms": round(a.latency_ms, 1),
                    "load": round(a.load, 3),
                    "tools_count": a.tools_count,
                    "capabilities": a.capabilities[:8],
                    "apex_scalars": {
                        k: v for k, v in a.apex_scalars.items() if k in ("G", "C_dark", "W3")
                    },
                    "source": a.source,
                    "missed_probes": a.missed_probes,
                }
                for a in all_agents
            ],
        }

    # ── Persistence ────────────────────────────────────────────────────

    def write_status_json(self, path: Path | None = None) -> Path:
        """Write status.json to disk. Atomic write via temp file."""
        target = path or STATUS_JSON_PATH
        data = self.summary()
        data["_note"] = (
            "This file is auto-generated by AAA Cockpit Live Polling. Do not edit manually."
        )

        # Atomic write: temp → rename
        tmp = target.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, default=str))
        tmp.rename(target)
        logger.info(f"Status written: {target} ({len(data['agent_list'])} agents)")
        return target


# ── Singleton ──────────────────────────────────────────────────────────────

_registry: AgentRegistry | None = None


def get_registry() -> AgentRegistry:
    """Get or create the singleton registry."""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
        _init_static_agents(_registry)
    return _registry


def _init_static_agents(registry: AgentRegistry) -> None:
    """Pre-register all known organs from the probe list."""
    for organ in PROBED_ORGANS:
        registry.register_static(
            agent_id=organ["id"],
            name=organ["id"].replace("-", " ").title(),
            role=organ["role"],
            authority_ceiling=organ["ceiling"],
            port=organ["port"],
        )
    for svc in PROBED_SERVICES:
        registry.register_static(
            agent_id=svc["id"],
            name=svc["id"].title(),
            role=svc["role"],
            authority_ceiling=svc["ceiling"],
            port=svc["port"],
        )
    logger.info(f"Static agents registered: {len(PROBED_ORGANS) + len(PROBED_SERVICES)}")
