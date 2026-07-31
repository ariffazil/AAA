"""
arifOS Federation — Graphiti Domain Schemas
Forged: 2026-07-31 · Session: SEAL-06ca329779e642e9
Pydantic v2 models for temporal knowledge graph ingestion.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


# ═══════════════════════════════════════════════════════════════════
# 1. FEDERATION TOPOLOGY
# ═══════════════════════════════════════════════════════════════════


class OrganNode(BaseModel):
    """A federation organ (arifOS, A-FORGE, GEOX, etc)."""

    organ_id: str = Field(..., description="e.g. 'arifos', 'aforge', 'geox'")
    name: str
    port: int
    role: str
    status: str = "active"  # active | degraded | down
    tool_count: int = 0
    mcp_endpoint: Optional[str] = None

    valid_at: datetime = Field(default_factory=datetime.utcnow)
    invalid_at: Optional[datetime] = None  # set when organ is decommissioned


class AgentNode(BaseModel):
    """A Trinity agent persona."""

    agent_id: str  # e.g. '333-AGI', '555-ASI', '888-APEX'
    name: str
    trinity_role: str  # Mind / Sense / Soul
    model_family: str  # deepseek / qwen / glm
    model_slug: str
    permission_profile: dict[str, str]  # {"edit": "deny", "bash": "deny", ...}
    temperature: float = 0.0
    steps_limit: int = 30

    valid_at: datetime = Field(default_factory=datetime.utcnow)
    invalid_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════
# 2. MODEL ROUTING
# ═══════════════════════════════════════════════════════════════════


class ModelRouteNode(BaseModel):
    """A model entry in the routing registry."""

    provider: str  # qwen-token-plan, deepseek, bailian, etc.
    model_slug: str
    status: str = "active"  # active | degraded | shadow | dead
    cost_tier: str = "heavy"  # cheap | heavy | apex | free
    context_window: int = 131072
    max_output: int = 8192
    shadow_tag: Optional[str] = None  # e.g. 'SHADOW-TR-001'
    death_reason: Optional[str] = None  # e.g. 'censorship on Malaysian topics'

    valid_at: datetime = Field(default_factory=datetime.utcnow)
    invalid_at: Optional[datetime] = None


class ModelProviderNode(BaseModel):
    """A model provider entry."""

    provider_id: str
    name: str
    base_url: str
    pricing_model: str  # flat_rate | pay_as_you_go | free
    monthly_cost_usd: float = 0.0
    status: str = "active"

    valid_at: datetime = Field(default_factory=datetime.utcnow)
    invalid_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════
# 3. SESSIONS & AUDIT
# ═══════════════════════════════════════════════════════════════════


class SessionNode(BaseModel):
    """An arifOS session record."""

    session_id: str  # SEAL-xxxxxxxx
    actor_id: str
    intent: str
    verdict_band: str = "OBSERVE_ONLY"
    fq: Optional[float] = None
    delta_s: Optional[float] = None
    organs_healthy: int = 7
    open_loops: list[str] = Field(default_factory=list)
    completed_tasks: list[str] = Field(default_factory=list)

    valid_at: datetime = Field(default_factory=datetime.utcnow)
    invalid_at: Optional[datetime] = None


class SecurityEventNode(BaseModel):
    """A security-relevant configuration change."""

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str  # permission_change, provider_death, shadow_detected
    description: str
    agent_id: str
    session_id: str
    severity: str = "low"  # low | medium | high | critical

    valid_at: datetime = Field(default_factory=datetime.utcnow)
    invalid_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════
# 4. MCP TOOL SURFACE
# ═══════════════════════════════════════════════════════════════════


class MCPToolNode(BaseModel):
    """An MCP tool in the federation surface."""

    tool_name: str
    server: str
    domain: str  # kernel | execution | earth | capital | human | inference
    reversibility_tier: int = 0  # 0-5 per AGI substrate doctrine
    blast_radius: str = "none"  # none | low | moderate | high | critical
    status: str = "active"

    valid_at: datetime = Field(default_factory=datetime.utcnow)
    invalid_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════
# 5. EPISODE INGESTION HELPERS
# ═══════════════════════════════════════════════════════════════════


class FederationEpisode(BaseModel):
    """A batch of domain entities to ingest as a Graphiti episode."""

    episode_name: str
    source: str = "333-AGI"
    session_id: str
    organs: list[OrganNode] = Field(default_factory=list)
    agents: list[AgentNode] = Field(default_factory=list)
    model_routes: list[ModelRouteNode] = Field(default_factory=list)
    providers: list[ModelProviderNode] = Field(default_factory=list)
    tools: list[MCPToolNode] = Field(default_factory=list)
    security_events: list[SecurityEventNode] = Field(default_factory=list)

    def to_episode_body(self) -> str:
        """Serialize to natural-language episode body for Graphiti ingestion."""
        parts = []
        if self.organs:
            parts.append(
                "Federation Organs:\n"
                + "\n".join(
                    f"- {o.organ_id} (: {o.port}): {o.role} [{o.status}] ({o.tool_count} tools)" for o in self.organs
                )
            )
        if self.agents:
            parts.append(
                "Trinity Agents:\n"
                + "\n".join(
                    f"- {a.agent_id} ({a.trinity_role}): {a.model_slug} [{a.model_family}] (temp={a.temperature}, steps={a.steps_limit})"
                    for a in self.agents
                )
            )
        if self.model_routes:
            parts.append(
                "Model Routes:\n"
                + "\n".join(
                    f"- {m.provider}/{m.model_slug}: [{m.status}] {m.cost_tier} tier, {m.context_window // 1024}K ctx"
                    + (f" SHADOW={m.shadow_tag}" if m.shadow_tag else "")
                    + (f" DEAD={m.death_reason}" if m.death_reason else "")
                    for m in self.model_routes
                )
            )
        if self.providers:
            parts.append(
                "Providers:\n"
                + "\n".join(
                    f"- {p.provider_id}: {p.pricing_model} [{p.status}] ${p.monthly_cost_usd}/mo"
                    for p in self.providers
                )
            )
        if self.security_events:
            parts.append(
                "Security Events:\n"
                + "\n".join(
                    f"- [{e.severity.upper()}] {e.event_type}: {e.description} (by {e.agent_id} in {e.session_id})"
                    for e in self.security_events
                )
            )
        return "\n\n".join(parts) if parts else "(empty episode)"
