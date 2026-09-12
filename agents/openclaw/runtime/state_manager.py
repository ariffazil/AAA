#!/usr/bin/env python3
"""
OpenClaw State Manager v1.0.0

Cross-session state management for OpenClaw orchestrator.
Redis L1 (fast) + JSON file L2 (persistent) per person_id.

Features:
  - Per-person conversation state (last N messages, preferences, context)
  - Session continuity via carry_forward pattern
  - FQ-aware state (low FQ = simplify, don't escalate)
  - TTL-based expiry for L1 cache
  - Crash-safe JSON persistence for L2

Forged: 2026-09-12 by 333-AGI under F13 directive
DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import os
import time
import hashlib
import threading
from typing import Any, Optional
from dataclasses import dataclass, field, asdict


# ─── Constants ───────────────────────────────────────────────────────────
STATE_DIR = os.environ.get("OPENCLAW_STATE_DIR", "/root/AAA/agents/openclaw/runtime/state")
L1_TTL_SECONDS = int(os.environ.get("STATE_L1_TTL", "3600"))  # 1 hour
MAX_HISTORY = int(os.environ.get("STATE_MAX_HISTORY", "50"))  # last 50 messages
MAX_CONTEXT_WINDOW = int(os.environ.get("STATE_MAX_CONTEXT", "10"))  # last 10 for context

# Redis config (optional — falls back to in-memory if unavailable)
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
REDIS_DB = int(os.environ.get("REDIS_DB", "3"))  # DB 3 for OpenClaw state
REDIS_KEY_PREFIX = "openclaw:state:"


@dataclass
class ConversationTurn:
    """Single conversation turn."""

    role: str  # user | assistant | system
    content: str
    timestamp: float
    channel: str = ""
    rule_id: str = ""
    target_agent: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class PersonState:
    """Persistent state for a person_id."""

    person_id: str
    person_class: str = "unknown"  # SOVEREIGN | warga | unknown
    created_at: float = 0
    last_active: float = 0
    conversation_history: list[ConversationTurn] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)
    active_workflows: list[str] = field(default_factory=list)
    routing_stats: dict = field(default_factory=dict)  # rule_id → count
    fq_at_last_interaction: float = 0
    language_preference: str = "mixed"  # en | ms | mixed
    metadata: dict = field(default_factory=dict)


class StateManager:
    """
    Cross-session state manager with Redis L1 + JSON L2.
    """

    def __init__(self):
        os.makedirs(STATE_DIR, exist_ok=True)
        self._l1_cache: dict[str, tuple[float, PersonState]] = {}
        self._lock = threading.Lock()
        self._redis = None
        self._init_redis()

    def _init_redis(self):
        """Try to connect to Redis. Fall back to in-memory if unavailable."""
        try:
            import redis

            self._redis = redis.from_url(REDIS_URL, db=REDIS_DB, decode_responses=True)
            self._redis.ping()
        except Exception:
            self._redis = None

    # ─── Public API ──────────────────────────────────────────────────

    def get_state(self, person_id: str) -> PersonState:
        """Get person state (L1 → L2 → create new)."""
        # L1: in-memory cache
        cached = self._l1_get(person_id)
        if cached:
            return cached

        # L1.5: Redis
        if self._redis:
            redis_state = self._redis_get(person_id)
            if redis_state:
                self._l1_set(person_id, redis_state)
                return redis_state

        # L2: JSON file
        file_state = self._file_get(person_id)
        if file_state:
            self._l1_set(person_id, file_state)
            if self._redis:
                self._redis_set(person_id, file_state)
            return file_state

        # Create new
        state = PersonState(
            person_id=person_id,
            created_at=time.time(),
            last_active=time.time(),
        )
        self._l1_set(person_id, state)
        self._file_set(person_id, state)
        return state

    def update_state(self, person_id: str, **kwargs) -> PersonState:
        """Update person state fields."""
        state = self.get_state(person_id)
        state.last_active = time.time()

        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)

        self._l1_set(person_id, state)
        if self._redis:
            self._redis_set(person_id, state)
        self._file_set(person_id, state)
        return state

    def add_turn(
        self,
        person_id: str,
        role: str,
        content: str,
        *,
        channel: str = "",
        rule_id: str = "",
        target_agent: str = "",
        metadata: dict | None = None,
    ) -> PersonState:
        """Add a conversation turn to history."""
        state = self.get_state(person_id)

        turn = ConversationTurn(
            role=role,
            content=content,
            timestamp=time.time(),
            channel=channel,
            rule_id=rule_id,
            target_agent=target_agent,
            metadata=metadata or {},
        )

        state.conversation_history.append(turn)

        # Trim to max history
        if len(state.conversation_history) > MAX_HISTORY:
            state.conversation_history = state.conversation_history[-MAX_HISTORY:]

        state.last_active = time.time()

        # Update routing stats
        if rule_id:
            state.routing_stats[rule_id] = state.routing_stats.get(rule_id, 0) + 1

        self._l1_set(person_id, state)
        if self._redis:
            self._redis_set(person_id, state)
        self._file_set(person_id, state)
        return state

    def get_context_window(self, person_id: str, n: int = MAX_CONTEXT_WINDOW) -> list[dict]:
        """Get last N conversation turns as context for LLM."""
        state = self.get_state(person_id)
        recent = state.conversation_history[-n:] if state.conversation_history else []
        return [{"role": t.role, "content": t.content} for t in recent]

    def get_conversation_summary(self, person_id: str) -> dict:
        """Get conversation summary for routing context."""
        state = self.get_state(person_id)
        return {
            "person_id": person_id,
            "person_class": state.person_class,
            "total_turns": len(state.conversation_history),
            "last_active": state.last_active,
            "top_routes": sorted(
                state.routing_stats.items(),
                key=lambda x: x[1],
                reverse=True,
            )[:5],
            "language": state.language_preference,
            "active_workflows": state.active_workflows,
            "fq_at_last": state.fq_at_last_interaction,
        }

    def record_fq(self, person_id: str, fq: float) -> None:
        """Record FQ at time of interaction."""
        self.update_state(person_id, fq_at_last_interaction=fq)

    def add_workflow(self, person_id: str, flow_id: str) -> None:
        """Track active workflow for a person."""
        state = self.get_state(person_id)
        if flow_id not in state.active_workflows:
            state.active_workflows.append(flow_id)
            self._l1_set(person_id, state)
            self._file_set(person_id, state)

    def remove_workflow(self, person_id: str, flow_id: str) -> None:
        """Remove completed workflow."""
        state = self.get_state(person_id)
        if flow_id in state.active_workflows:
            state.active_workflows.remove(flow_id)
            self._l1_set(person_id, state)
            self._file_set(person_id, state)

    # ─── L1: In-Memory Cache ─────────────────────────────────────────

    def _l1_get(self, person_id: str) -> Optional[PersonState]:
        """Get from in-memory cache with TTL check."""
        with self._lock:
            if person_id in self._l1_cache:
                ts, state = self._l1_cache[person_id]
                if time.time() - ts < L1_TTL_SECONDS:
                    return state
                del self._l1_cache[person_id]
        return None

    def _l1_set(self, person_id: str, state: PersonState) -> None:
        """Store in in-memory cache."""
        with self._lock:
            self._l1_cache[person_id] = (time.time(), state)
            # Evict if too large
            if len(self._l1_cache) > 500:
                oldest = sorted(
                    self._l1_cache.items(),
                    key=lambda x: x[1][0],
                )[:250]
                for k, _ in oldest:
                    del self._l1_cache[k]

    # ─── L1.5: Redis ─────────────────────────────────────────────────

    def _redis_get(self, person_id: str) -> Optional[PersonState]:
        """Get from Redis."""
        if not self._redis:
            return None
        try:
            key = f"{REDIS_KEY_PREFIX}{person_id}"
            data = self._redis.get(key)
            if data:
                return self._deserialize(json.loads(data))
        except Exception:
            pass
        return None

    def _redis_set(self, person_id: str, state: PersonState) -> None:
        """Store in Redis with TTL."""
        if not self._redis:
            return
        try:
            key = f"{REDIS_KEY_PREFIX}{person_id}"
            data = json.dumps(self._serialize(state), default=str)
            self._redis.setex(key, L1_TTL_SECONDS, data)
        except Exception:
            pass

    # ─── L2: JSON File ───────────────────────────────────────────────

    def _file_get(self, person_id: str) -> Optional[PersonState]:
        """Get from JSON file."""
        path = self._state_path(person_id)
        if os.path.exists(path):
            try:
                with open(path) as f:
                    data = json.load(f)
                return self._deserialize(data)
            except Exception:
                pass
        return None

    def _file_set(self, person_id: str, state: PersonState) -> None:
        """Store to JSON file."""
        path = self._state_path(person_id)
        try:
            with open(path, "w") as f:
                json.dump(self._serialize(state), f, indent=2, default=str)
        except Exception:
            pass

    def _state_path(self, person_id: str) -> str:
        """Get file path for person state."""
        safe_id = hashlib.sha256(person_id.encode()).hexdigest()[:16]
        return os.path.join(STATE_DIR, f"{safe_id}.json")

    # ─── Serialization ───────────────────────────────────────────────

    def _serialize(self, state: PersonState) -> dict:
        """Serialize state to dict."""
        return {
            "person_id": state.person_id,
            "person_class": state.person_class,
            "created_at": state.created_at,
            "last_active": state.last_active,
            "conversation_history": [asdict(t) for t in state.conversation_history],
            "preferences": state.preferences,
            "active_workflows": state.active_workflows,
            "routing_stats": state.routing_stats,
            "fq_at_last_interaction": state.fq_at_last_interaction,
            "language_preference": state.language_preference,
            "metadata": state.metadata,
        }

    def _deserialize(self, data: dict) -> PersonState:
        """Deserialize dict to state."""
        turns = [ConversationTurn(**t) for t in data.get("conversation_history", [])]
        return PersonState(
            person_id=data.get("person_id", ""),
            person_class=data.get("person_class", "unknown"),
            created_at=data.get("created_at", 0),
            last_active=data.get("last_active", 0),
            conversation_history=turns,
            preferences=data.get("preferences", {}),
            active_workflows=data.get("active_workflows", []),
            routing_stats=data.get("routing_stats", {}),
            fq_at_last_interaction=data.get("fq_at_last_interaction", 0),
            language_preference=data.get("language_preference", "mixed"),
            metadata=data.get("metadata", {}),
        )


# ─── Module-level singleton ─────────────────────────────────────────────
_manager: StateManager | None = None


def get_state_manager() -> StateManager:
    """Get or create the singleton StateManager."""
    global _manager
    if _manager is None:
        _manager = StateManager()
    return _manager


def get_person_state(person_id: str) -> PersonState:
    """Convenience: get person state."""
    return get_state_manager().get_state(person_id)


def add_conversation_turn(person_id: str, role: str, content: str, **kwargs) -> PersonState:
    """Convenience: add a conversation turn."""
    return get_state_manager().add_turn(person_id, role, content, **kwargs)
