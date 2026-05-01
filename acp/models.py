"""
ACP data models — compatible with agentcommunicationprotocol.dev spec.
"""

from __future__ import annotations
import uuid
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


# ─── Agent Card ──────────────────────────────────────────────────────────────

class ACPProvider(BaseModel):
    organization: str = "arifOS"
    system: str = "AAA"
    runtime: str = "ollama"


class ACPCapabilities(BaseModel):
    streaming: bool = True
    push_notifications: bool = False
    authenticated_extended_card: bool = False
    input_modes: list[str] = ["text/plain", "application/json"]
    output_modes: list[str] = ["text/plain", "application/json"]


class ACPSkill(BaseModel):
    id: str
    name: str
    description: str
    tags: list[str] = []
    examples: list[str] = []


class AgentCard(BaseModel):
    """A2A Agent Card — discoverable identity for an ACP agent."""
    id: str
    name: str
    description: str
    url: str = ""
    preferred_transport: Literal["jsonrpc-http", "jsonrpc-sse", "rest-sse"] = "jsonrpc-sse"
    provider: ACPProvider = Field(default_factory=ACPProvider)
    version: str = "1.0.0"
    capabilities: ACPCapabilities = Field(default_factory=ACPCapabilities)
    skills: list[ACPSkill] = []
    supports_authenticated_extended_card: bool = False

    def skill_by_id(self, skill_id: str) -> Optional[ACPSkill]:
        for s in self.skills:
            if s.id == skill_id:
                return s
        return None


# ─── ACP Messages ─────────────────────────────────────────────────────────────

class ACPMessage(BaseModel):
    """A2A message between agents."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: Literal["user", "agent", "system"] = "agent"
    content: str
    metadata: dict = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ACPTask(BaseModel):
    """ACP task / run representation."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    agent_id: str
    message: ACPMessage
    skill_id: Optional[str] = None
    status: Literal["pending", "in_progress", "completed", "failed", "cancelled"] = "pending"
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
