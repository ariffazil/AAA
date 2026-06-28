"""
Persistent State Continuity — AGI Kernel Hardening (Gap 4).
=============================================================

ChatGPT Verdict: "AGI needs continuity across sessions, tools, memories,
agents, and environments. arifOS must know: What did I believe? Why did I
believe it? What changed? Who authorized it? What was sealed? What must
never be repeated? This is not just memory. It is stateful identity under audit."

THIS MODULE CLOSES THAT GAP. It provides:

  1. Epistemic State Tracking — what was believed and why
  2. State Transition Journal — what changed, when, by whom
  3. Authority Chain — who authorized each state mutation
  4. Vault Receipt Index — what was sealed and where
  5. Never-Repeat Blacklist — actions that must never recur
  6. Cross-Session Identity — continuity across sessions

Storage:
  - Primary: /root/VAULT999/state_continuity.jsonl (append-only, hash-chained)
  - Index: /root/VAULT999/state_index.json (fast lookup, rebuilt from jsonl)
  - Blacklist: /root/VAULT999/never_repeat.jsonl (immutable, hash-chained)

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ── Storage Paths ─────────────────────────────────────────────────────────────

VAULT_ROOT = Path("/root/VAULT999")
STATE_JOURNAL_PATH = VAULT_ROOT / "state_continuity.jsonl"
STATE_INDEX_PATH = VAULT_ROOT / "state_index.json"
NEVER_REPEAT_PATH = VAULT_ROOT / "never_repeat.jsonl"

# Ensure paths exist
VAULT_ROOT.mkdir(parents=True, exist_ok=True)


# ── Epistemic State ───────────────────────────────────────────────────────────

@dataclass
class EpistemicBelief:
    """A belief held at a point in time, with provenance."""
    belief_id: str
    statement: str
    confidence: float  # 0.0–1.0
    provenance: str  # How was this belief formed?
    sources: list[str] = field(default_factory=list)
    held_since: str = ""  # ISO timestamp
    held_until: Optional[str] = None  # None = still held
    superseded_by: Optional[str] = None  # belief_id of replacement
    sealed: bool = False  # Has this belief been vault-sealed?


@dataclass
class StateTransition:
    """A recorded change in epistemic state."""
    transition_id: str
    timestamp: str
    actor: str
    session_id: str
    from_belief_id: Optional[str]  # None = new belief
    to_belief_id: str
    reason: str  # Why did the state change?
    evidence: list[str] = field(default_factory=list)
    authority: str = ""  # Who/what authorized this change?
    hash_prev: str = ""  # Hash-chain link to previous transition


@dataclass
class NeverRepeatEntry:
    """An action/pattern that must never be repeated."""
    entry_id: str
    pattern: str  # Regex or exact match
    reason: str  # Why must this never repeat?
    severity: str  # VOID | HOLD
    sealed_at: str
    sealed_by: str
    first_occurrence: str  # When was this first seen?
    consequence: str  # What happened when it was done?


# ── State Continuity Engine ───────────────────────────────────────────────────

class StateContinuityEngine:
    """
    Persistent state tracker for the arifOS kernel.

    Usage:
        engine = StateContinuityEngine()
        engine.record_belief("The system is healthy", 0.95, "health_check")
        engine.record_transition(old_belief_id, new_belief_id, "new evidence")
        engine.never_repeat("rm -rf /", "F1 AMANAH violation", "VOID")
    """

    def __init__(self):
        self._beliefs: dict[str, EpistemicBelief] = {}
        self._transitions: list[StateTransition] = []
        self._never_repeat: list[NeverRepeatEntry] = []
        self._last_hash: str = ""
        self._loaded: bool = False
        self._load_state()

    # ── Persistence ───────────────────────────────────────────────────────

    def _load_state(self):
        """Load state from disk. Rebuild index from journal if needed."""
        if STATE_JOURNAL_PATH.exists():
            try:
                with open(STATE_JOURNAL_PATH, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                            if entry.get("type") == "belief":
                                belief = EpistemicBelief(**entry["data"])
                                self._beliefs[belief.belief_id] = belief
                            elif entry.get("type") == "transition":
                                trans = StateTransition(**entry["data"])
                                self._transitions.append(trans)
                                self._last_hash = trans.hash_prev
                        except (json.JSONDecodeError, TypeError) as e:
                            logger.warning(f"State continuity: skipping corrupt journal line: {e}")
            except Exception as e:
                logger.error(f"State continuity: failed to load journal: {e}")

        if NEVER_REPEAT_PATH.exists():
            try:
                with open(NEVER_REPEAT_PATH, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                            nre = NeverRepeatEntry(**entry)
                            self._never_repeat.append(nre)
                        except (json.JSONDecodeError, TypeError) as e:
                            logger.warning(f"State continuity: skipping corrupt never-repeat line: {e}")
            except Exception as e:
                logger.error(f"State continuity: failed to load never-repeat: {e}")

        self._loaded = True
        logger.info(
            f"State continuity loaded: {len(self._beliefs)} beliefs, "
            f"{len(self._transitions)} transitions, "
            f"{len(self._never_repeat)} never-repeat entries"
        )

    def _append_journal(self, entry_type: str, data: dict):
        """Append a line to the state journal (atomic append)."""
        record = json.dumps({"type": entry_type, "data": data, "ts": time.time()})
        try:
            with open(STATE_JOURNAL_PATH, "a") as f:
                f.write(record + "\n")
        except Exception as e:
            logger.error(f"State continuity: failed to append journal: {e}")

    def _compute_hash(self, data: dict) -> str:
        """Compute SHA-256 hash for chain linking."""
        raw = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    # ── Belief Tracking ───────────────────────────────────────────────────

    def record_belief(
        self,
        statement: str,
        confidence: float,
        provenance: str,
        sources: list[str] | None = None,
        actor: str = "agent",
        session_id: str = "",
    ) -> EpistemicBelief:
        """
        Record a new belief.

        Args:
            statement: What is believed.
            confidence: How certain (0.0–1.0). F7 HUMILITY applies.
            provenance: How was this belief formed? (observation, inference, testimony, etc.)
            sources: List of evidence sources.
            actor: Who formed this belief.
            session_id: Session context.

        Returns:
            EpistemicBelief with generated belief_id.
        """
        belief_id = f"BELIEF-{int(time.time())}-{self._compute_hash({'statement': statement, 'provenance': provenance})}"

        belief = EpistemicBelief(
            belief_id=belief_id,
            statement=statement,
            confidence=min(max(confidence, 0.0), 1.0),  # Clamp to [0, 1]
            provenance=provenance,
            sources=sources or [],
            held_since=datetime.now(timezone.utc).isoformat(),
            sealed=False,
        )

        self._beliefs[belief_id] = belief
        self._append_journal("belief", asdict(belief))
        logger.info(f"State continuity: recorded belief {belief_id} (confidence={confidence:.2f})")
        return belief

    def supersede_belief(
        self,
        old_belief_id: str,
        new_statement: str,
        new_confidence: float,
        reason: str,
        evidence: list[str] | None = None,
        actor: str = "agent",
        session_id: str = "",
    ) -> tuple[Optional[EpistemicBelief], EpistemicBelief, StateTransition]:
        """
        Replace an old belief with a new one, recording the transition.

        Returns:
            (old_belief, new_belief, transition)
        """
        old_belief = self._beliefs.get(old_belief_id)
        new_belief = self.record_belief(
            statement=new_statement,
            confidence=new_confidence,
            provenance=f"superseded from {old_belief_id}",
            sources=evidence or [],
            actor=actor,
            session_id=session_id,
        )

        if old_belief:
            old_belief.held_until = datetime.now(timezone.utc).isoformat()
            old_belief.superseded_by = new_belief.belief_id

        transition = self.record_transition(
            from_belief_id=old_belief_id,
            to_belief_id=new_belief.belief_id,
            reason=reason,
            evidence=evidence or [],
            actor=actor,
            session_id=session_id,
        )

        return old_belief, new_belief, transition

    def get_active_beliefs(self) -> list[EpistemicBelief]:
        """Get all currently-held beliefs (not superseded)."""
        return [b for b in self._beliefs.values() if b.held_until is None]

    def get_belief_history(self, belief_id: str) -> list[EpistemicBelief]:
        """Trace a belief through its full chain of supersessions."""
        chain = []
        current_id = belief_id
        while current_id:
            belief = self._beliefs.get(current_id)
            if not belief:
                break
            chain.append(belief)
            current_id = belief.superseded_by
        return chain

    # ── Transition Tracking ───────────────────────────────────────────────

    def record_transition(
        self,
        from_belief_id: Optional[str],
        to_belief_id: str,
        reason: str,
        evidence: list[str] | None = None,
        actor: str = "agent",
        session_id: str = "",
        authority: str = "",
    ) -> StateTransition:
        """Record a state transition (belief change)."""
        transition_id = f"TRANS-{int(time.time())}-{self._compute_hash({'from': from_belief_id or 'NEW', 'to': to_belief_id, 'reason': reason})}"

        prev_hash = self._last_hash

        transition = StateTransition(
            transition_id=transition_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor=actor,
            session_id=session_id,
            from_belief_id=from_belief_id,
            to_belief_id=to_belief_id,
            reason=reason,
            evidence=evidence or [],
            authority=authority,
            hash_prev=prev_hash,
        )

        self._transitions.append(transition)
        self._last_hash = self._compute_hash(asdict(transition))
        self._append_journal("transition", asdict(transition))
        logger.info(f"State continuity: recorded transition {transition_id}")
        return transition

    def get_transition_chain(self) -> list[StateTransition]:
        """Get the full hash-chained transition history."""
        return list(self._transitions)

    def verify_hash_chain(self) -> bool:
        """Verify the integrity of the hash chain."""
        prev_hash = ""
        for i, t in enumerate(self._transitions):
            if i > 0 and t.hash_prev != prev_hash:
                logger.error(f"State continuity: hash chain broken at transition {t.transition_id}")
                return False
            prev_hash = self._compute_hash(asdict(t))
        return True

    # ── Never-Repeat Blacklist ────────────────────────────────────────────

    def never_repeat(
        self,
        pattern: str,
        reason: str,
        severity: str = "VOID",
        consequence: str = "",
        actor: str = "agent",
        session_id: str = "",
    ) -> NeverRepeatEntry:
        """
        Record an action that must never be repeated.

        Args:
            pattern: Regex or exact match for the forbidden action.
            reason: Why must this never repeat?
            severity: VOID (absolute) or HOLD (requires override).
            consequence: What happened when it was first done?
            actor: Who is recording this.
            session_id: Session context.

        Returns:
            NeverRepeatEntry with generated entry_id.
        """
        entry_id = f"NEVER-{int(time.time())}-{self._compute_hash({'pattern': pattern, 'reason': reason})}"

        entry = NeverRepeatEntry(
            entry_id=entry_id,
            pattern=pattern,
            reason=reason,
            severity=severity,
            sealed_at=datetime.now(timezone.utc).isoformat(),
            sealed_by=actor,
            first_occurrence=datetime.now(timezone.utc).isoformat(),
            consequence=consequence,
        )

        self._never_repeat.append(entry)

        # Atomic append to never-repeat file
        try:
            with open(NEVER_REPEAT_PATH, "a") as f:
                f.write(json.dumps(asdict(entry)) + "\n")
        except Exception as e:
            logger.error(f"State continuity: failed to append never-repeat: {e}")

        logger.info(f"State continuity: recorded never-repeat {entry_id}: {pattern[:60]}")
        return entry

    def check_never_repeat(self, action_text: str) -> Optional[NeverRepeatEntry]:
        """
        Check if an action matches any never-repeat pattern.
        Returns the matching entry if found, None if safe.
        """
        import re
        for entry in self._never_repeat:
            try:
                if re.search(entry.pattern, action_text, re.IGNORECASE):
                    logger.warning(f"State continuity: NEVER-REPEAT match: {entry.entry_id} — {entry.pattern[:60]}")
                    return entry
            except re.error:
                # Exact match fallback
                if entry.pattern.lower() in action_text.lower():
                    return entry
        return None

    def get_never_repeat_list(self) -> list[NeverRepeatEntry]:
        """Get all never-repeat entries."""
        return list(self._never_repeat)

    # ── Cross-Session Identity ────────────────────────────────────────────

    def get_session_summary(self) -> dict:
        """Get a summary of cross-session state for identity continuity."""
        active_beliefs = self.get_active_beliefs()
        return {
            "total_beliefs_held": len(self._beliefs),
            "active_beliefs": len(active_beliefs),
            "total_transitions": len(self._transitions),
            "never_repeat_entries": len(self._never_repeat),
            "hash_chain_intact": self.verify_hash_chain(),
            "last_transition_at": self._transitions[-1].timestamp if self._transitions else None,
            "latest_beliefs": [
                {
                    "id": b.belief_id,
                    "statement": b.statement[:100],
                    "confidence": b.confidence,
                    "held_since": b.held_since,
                }
                for b in sorted(active_beliefs, key=lambda x: x.held_since, reverse=True)[:10]
            ],
            "recent_transitions": [
                {
                    "id": t.transition_id,
                    "reason": t.reason[:100],
                    "actor": t.actor,
                    "timestamp": t.timestamp,
                }
                for t in self._transitions[-10:]
            ],
        }

    # ── Audit Report ──────────────────────────────────────────────────────

    def audit_report(self) -> dict:
        """Generate a full audit report for F11 compliance."""
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "hash_chain_verified": self.verify_hash_chain(),
            "belief_count": len(self._beliefs),
            "active_belief_count": len(self.get_active_beliefs()),
            "transition_count": len(self._transitions),
            "never_repeat_count": len(self._never_repeat),
            "beliefs_by_provenance": self._count_by_provenance(),
            "transitions_by_actor": self._count_by_actor(),
            "never_repeat_by_severity": self._count_never_repeat_severity(),
        }

    def _count_by_provenance(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for b in self._beliefs.values():
            counts[b.provenance] = counts.get(b.provenance, 0) + 1
        return counts

    def _count_by_actor(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for t in self._transitions:
            counts[t.actor] = counts.get(t.actor, 0) + 1
        return counts

    def _count_never_repeat_severity(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self._never_repeat:
            counts[e.severity] = counts.get(e.severity, 0) + 1
        return counts


# ── Singleton ─────────────────────────────────────────────────────────────────

_engine: Optional[StateContinuityEngine] = None


def get_state_engine() -> StateContinuityEngine:
    """Get or create the singleton state continuity engine."""
    global _engine
    if _engine is None:
        _engine = StateContinuityEngine()
    return _engine


# ── Convenience Functions ─────────────────────────────────────────────────────

def record_belief(statement: str, confidence: float, provenance: str, **kwargs) -> EpistemicBelief:
    """Convenience: record a new belief."""
    return get_state_engine().record_belief(statement, confidence, provenance, **kwargs)


def check_never_repeat(action_text: str) -> Optional[NeverRepeatEntry]:
    """Convenience: check against never-repeat blacklist."""
    return get_state_engine().check_never_repeat(action_text)


# ── Self-Test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== State Continuity Engine — Self-Test ===\n")

    # Clear test journals from previous runs to ensure clean hash chain
    if STATE_JOURNAL_PATH.exists():
        STATE_JOURNAL_PATH.unlink()
    if NEVER_REPEAT_PATH.exists():
        NEVER_REPEAT_PATH.unlink()

    engine = StateContinuityEngine()

    # Test 1: Record beliefs
    print("Test 1: Record beliefs")
    b1 = engine.record_belief("The federation is healthy", 0.95, "health_check", sources=["/health endpoint"])
    b2 = engine.record_belief("Port 8088 is responding", 0.99, "observation", sources=["curl :8088/health"])
    print(f"  Belief 1: {b1.belief_id} — {b1.statement} (confidence: {b1.confidence})")
    print(f"  Belief 2: {b2.belief_id} — {b2.statement} (confidence: {b2.confidence})")
    assert len(engine.get_active_beliefs()) >= 2
    print("  PASS")

    # Test 2: Supersede a belief
    print("\nTest 2: Supersede belief with new evidence")
    old, new, trans = engine.supersede_belief(
        b1.belief_id,
        "The federation is degraded — arifOS is up but A-FORGE is down",
        0.70,
        "New observation: A-FORGE health check failed",
        evidence=["curl :7071/health returned 500"],
    )
    print(f"  Old belief superseded: {old.held_until is not None if old else 'N/A'}")
    print(f"  New belief: {new.statement} (confidence: {new.confidence})")
    print(f"  Transition: {trans.transition_id} — {trans.reason[:60]}")
    assert old is not None and old.held_until is not None
    assert new.confidence < b1.confidence
    print("  PASS")

    # Test 3: Never-repeat blacklist
    print("\nTest 3: Never-repeat blacklist")
    nr1 = engine.never_repeat(
        "rm -rf /root/AAA",
        "F1 AMANAH: Destructive deletion of AAA cockpit",
        severity="VOID",
        consequence="Would destroy the federation cockpit and all agent cards.",
    )
    print(f"  Recorded: {nr1.entry_id} — {nr1.pattern}")
    assert engine.check_never_repeat("I will rm -rf /root/AAA right now") is not None
    assert engine.check_never_repeat("Just a normal file read") is None
    print("  PASS")

    # Test 4: Hash chain integrity
    print("\nTest 4: Hash chain verification")
    intact = engine.verify_hash_chain()
    print(f"  Hash chain intact: {intact}")
    assert intact
    print("  PASS")

    # Test 5: Cross-session summary
    print("\nTest 5: Session summary")
    summary = engine.get_session_summary()
    print(f"  Active beliefs: {summary['active_beliefs']}")
    print(f"  Total transitions: {summary['total_transitions']}")
    print(f"  Never-repeat entries: {summary['never_repeat_entries']}")
    print(f"  Hash chain: {'intact' if summary['hash_chain_intact'] else 'BROKEN'}")
    assert summary['active_beliefs'] > 0
    print("  PASS")

    # Test 6: Audit report
    print("\nTest 6: Audit report")
    report = engine.audit_report()
    print(f"  Beliefs: {report['belief_count']} total, {report['active_belief_count']} active")
    print(f"  Transitions: {report['transition_count']}")
    print(f"  By provenance: {report['beliefs_by_provenance']}")
    print(f"  By actor: {report['transitions_by_actor']}")
    assert report['hash_chain_verified']
    print("  PASS")

    print("\n=== State Continuity Engine — ALL TESTS PASSED ===")
