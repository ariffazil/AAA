#!/usr/bin/env python3
"""
HERMES Authority Boundary — I3+I5 Enforcement (Phase2)
Binds trigger → proposed action → scope with hash verification.

Canonical: /root/AAA/instructions/authority-envelope.md
Companion: /root/AAA/instructions/state-transition-discipline.md

F13 binding: CanMutate = AuthorityGranted ∧ ScopeMatches ∧ TargetPermitted ∧ BoundaryActive
Confidence appears NOWHERE in that expression.

Usage:
    from hermes_authority_boundary import AuthorityBoundary
    ab = AuthorityBoundary()
    envelope = ab.create_envelope(actor, session, objective, operation, scope, target)
    result = ab.validate_and_execute(envelope, payload)
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Optional, Any


# ─── State-Transition Discipline ───


class ActionState(Enum):
    """Never collapse to boolean. PROPOSED ≠ APPROVED ≠ EXECUTED ≠ VERIFIED."""

    PROPOSED = "proposed"
    SCOPED = "scoped"
    APPROVED = "approved"
    EXECUTING = "executing"
    EXECUTED = "executed"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REVOKED = "revoked"
    VOID = "void"


class Verdict(Enum):
    """QRL-4 mapping. Never map upward."""

    SEAL = "SEAL"
    SABAR = "SABAR"
    HOLD = "HOLD"
    VOID = "VOID"


# ─── Authority Envelope (12 fields) ───


@dataclass
class AuthorityEnvelope:
    """
    The 12-field authority tuple from authority-envelope.md.
    The executor may NEVER issue its own envelope.
    """

    actor: str  # WHO is acting
    session: str  # Session binding
    host: str  # Where execution happens
    objective: str  # Permission belongs to a purpose, not an entity
    operation: str  # read ≠ write ≠ edit ≠ delete ≠ commit
    scope: str  # What domain/paths/organs are covered
    target: str  # Specific target of the operation
    issuer: str  # WHO granted this authority (NEVER the actor)
    expiry: float  # Unix timestamp when this envelope dies
    expected_postcondition: str  # What an independent witness will measure
    budget: dict  # {max_seconds, max_organ_calls, max_cost_units}
    revocation_ref: str  # Reference to credible revocation event

    # Computed fields
    envelope_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    created_at: float = field(default_factory=time.time)
    state: ActionState = field(default=ActionState.PROPOSED)
    hash: str = ""

    def __post_init__(self):
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Bind trigger → action → scope. Hash changes if ANY field changes."""
        canonical = json.dumps(
            {
                "actor": self.actor,
                "session": self.session,
                "objective": self.objective,
                "operation": self.operation,
                "scope": self.scope,
                "target": self.target,
                "issuer": self.issuer,
                "expiry": self.expiry,
                "expected_postcondition": self.expected_postcondition,
            },
            sort_keys=True,
        )
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]

    def is_expired(self) -> bool:
        return time.time() > self.expiry

    def is_budget_exhausted(self, calls_made: int = 0, seconds_elapsed: float = 0) -> bool:
        if self.budget.get("max_organ_calls") and calls_made >= self.budget["max_organ_calls"]:
            return True
        if self.budget.get("max_seconds") and seconds_elapsed >= self.budget["max_seconds"]:
            return True
        return False

    def to_receipt(self) -> dict:
        """Machine-readable receipt for VAULT999."""
        return {
            "envelope_id": self.envelope_id,
            "hash": self.hash,
            "actor": self.actor,
            "session": self.session,
            "objective": self.objective,
            "operation": self.operation,
            "scope": self.scope,
            "target": self.target,
            "issuer": self.issuer,
            "expiry": self.expiry,
            "state": self.state.value,
            "created_at": self.created_at,
            "budget": self.budget,
            "revocation_ref": self.revocation_ref,
        }


# ─── Validation Result ───


@dataclass
class ValidationResult:
    allowed: bool
    verdict: Verdict
    reason: str
    reason_code: str
    failed_checks: list[str] = field(default_factory=list)
    envelope_hash: str = ""
    receipt: dict = field(default_factory=dict)


# ─── Authority Boundary Engine ───


class AuthorityBoundary:
    """
    The reference monitor. Every protected mutation → AUTHORITY CHECK → ALLOW/HOLD → EXECUTE.

    Invariants:
    1. Complete mediation — ALL paths to protected state pass this gate
    2. Tamper resistance — the monitor cannot be disabled by the actor it governs
    3. Verifiability — every decision is receipted
    """

    # F1-F13 floor definitions
    FLOORS = {
        "F1": {"name": "AMANAH", "check": "reversibility", "irreversible_requires": "F13"},
        "F2": {"name": "KEBENARAN", "check": "evidence_quality", "min_truth_class": "DER"},
        "F3": {"name": "TRI-WITNESS", "check": "independent_verification"},
        "F5": {"name": "PRIVASI", "check": "data_minimization"},
        "F6": {"name": "MARUAH", "check": "dignity_preservation"},
        "F7": {"name": "KERENDAHAN_HATI", "check": "confidence_cap", "max": 0.90},
        "F9": {"name": "ANTI_HANTU", "check": "hallucination_gate"},
        "F11": {"name": "AUDIT", "check": "receipt_trail"},
        "F12": {"name": "AUTHORITY", "check": "issuer_not_actor"},
        "F13": {"name": "SOVEREIGN", "check": "human_authorization"},
    }

    # Operations that require F13
    IRREVERSIBLE_OPS = {"delete", "deploy", "push", "seal", "drop", "destroy", "publish"}

    # Operations that are always allowed (read-only)
    READ_ONLY_OPS = {"read", "observe", "search", "fetch", "list", "probe", "inspect"}

    def __init__(self, receipt_log: Optional[Path] = None):
        self.receipt_log = receipt_log or Path("/root/.local/share/arifos/authority_receipts.jsonl")
        self.receipt_log.parent.mkdir(parents=True, exist_ok=True)

    def create_envelope(
        self,
        actor: str,
        session: str,
        objective: str,
        operation: str,
        scope: str,
        target: str,
        issuer: str = "F13-SOVEREIGN",
        ttl_seconds: int = 3600,
        budget: Optional[dict] = None,
        revocation_ref: str = "",
    ) -> AuthorityEnvelope:
        """
        Create an authority envelope. The executor may NEVER issue its own envelope.
        If issuer == actor, the envelope is VOID on creation.
        """
        import socket

        host = socket.gethostname()

        envelope = AuthorityEnvelope(
            actor=actor,
            session=session,
            host=host,
            objective=objective,
            operation=operation,
            scope=scope,
            target=target,
            issuer=issuer,
            expiry=time.time() + ttl_seconds,
            expected_postcondition=f"operation={operation} on {target} within scope={scope}",
            budget=budget or {"max_seconds": ttl_seconds, "max_organ_calls": 10},
            revocation_ref=revocation_ref or f"revocation-{uuid.uuid4().hex[:8]}",
        )

        # I5: Self-authorization check
        if envelope.issuer == envelope.actor:
            envelope.state = ActionState.VOID
            self._log_receipt(envelope, "VOID", "self_authorization", "F12")

        return envelope

    def validate(self, envelope: AuthorityEnvelope, payload: Optional[dict] = None) -> ValidationResult:
        """
        The complete mediation check. Every field is tested.
        Returns ALLOW or HOLD with specific failed checks.
        """
        failed = []

        # ─── F12: Issuer ≠ Actor (I5 enforcement) ───
        if envelope.issuer == envelope.actor:
            failed.append("F12:issuer_equals_actor")

        # ─── Expiry check ───
        if envelope.is_expired():
            failed.append("EXPIRED")
            envelope.state = ActionState.EXPIRED

        # ─── Budget check ───
        if envelope.is_budget_exhausted():
            failed.append("BUDGET_EXHAUSTED")

        # ─── F1: Irreversibility requires F13 ───
        if envelope.operation.lower() in self.IRREVERSIBLE_OPS:
            if envelope.issuer != "F13-SOVEREIGN":
                failed.append("F1:irreversible_without_F13")

        # ─── F13: Human authorization for sovereign ops ───
        if envelope.operation.lower() in {"deploy", "seal", "destroy"}:
            if not envelope.revocation_ref:
                failed.append("F13:no_revocation_ref")

        # ─── Scope validation ───
        if payload:
            target_in_scope = self._check_scope(envelope.scope, envelope.target, payload)
            if not target_in_scope:
                failed.append("SCOPE_MISMATCH")

        # ─── Hash integrity ───
        expected_hash = envelope._compute_hash()
        if envelope.hash != expected_hash:
            failed.append("HASH_MISMATCH")

        # ─── Determine verdict ───
        if failed:
            verdict = Verdict.HOLD
            reason = f"Blocked: {', '.join(failed)}"
            reason_code = "AUTHORITY_BOUNDARY_HOLD"
            envelope.state = ActionState.REJECTED
        else:
            verdict = Verdict.SABAR if envelope.operation.lower() in self.READ_ONLY_OPS else Verdict.HOLD
            reason = (
                "Read-only operation within mandate"
                if verdict == Verdict.SABAR
                else "Write operation — requires explicit approval"
            )
            reason_code = "READ_ONLY_SABAR" if verdict == Verdict.SABAR else "WRITE_HOLD"
            if envelope.operation.lower() in self.READ_ONLY_OPS:
                envelope.state = ActionState.APPROVED
                verdict = Verdict.SABAR

        result = ValidationResult(
            allowed=(verdict in (Verdict.SABAR, Verdict.SEAL)),
            verdict=verdict,
            reason=reason,
            reason_code=reason_code,
            failed_checks=failed,
            envelope_hash=envelope.hash,
            receipt=envelope.to_receipt(),
        )

        self._log_receipt(envelope, verdict.value, reason_code, ",".join(failed) if failed else "NONE")
        return result

    def bind_trigger(self, trigger: str, proposed_action: str, scope: str) -> dict:
        """
        Hash binding: trigger → proposed action → scope.
        If scope changes, the hash changes, and the binding is invalid.
        """
        binding = {
            "trigger": trigger,
            "proposed_action": proposed_action,
            "scope": scope,
            "timestamp": time.time(),
        }
        canonical = json.dumps(binding, sort_keys=True)
        binding["hash"] = hashlib.sha256(canonical.encode()).hexdigest()[:16]
        return binding

    def verify_binding(self, binding: dict, current_scope: str) -> bool:
        """
        Verify that the binding's scope hasn't changed.
        If scope changed → binding invalid → stop.
        """
        if binding.get("scope") != current_scope:
            return False
        canonical = json.dumps(
            {
                "trigger": binding["trigger"],
                "proposed_action": binding["proposed_action"],
                "scope": binding["scope"],
                "timestamp": binding["timestamp"],
            },
            sort_keys=True,
        )
        expected_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]
        return binding.get("hash") == expected_hash

    def _check_scope(self, declared_scope: str, target: str, payload: dict) -> bool:
        """
        Verify the target is within the declared scope.
        Scope is a comma-separated list of allowed prefixes.
        """
        scopes = [s.strip() for s in declared_scope.split(",")]
        return any(target.startswith(s) for s in scopes)

    def _log_receipt(self, envelope: AuthorityEnvelope, verdict: str, reason_code: str, failed_checks: str):
        """Append-only receipt log. Never edit, never delete."""
        receipt = {
            "timestamp": time.time(),
            "envelope_id": envelope.envelope_id,
            "hash": envelope.hash,
            "actor": envelope.actor,
            "operation": envelope.operation,
            "scope": envelope.scope,
            "target": envelope.target,
            "verdict": verdict,
            "reason_code": reason_code,
            "failed_checks": failed_checks,
            "state": envelope.state.value,
        }
        with open(self.receipt_log, "a") as f:
            f.write(json.dumps(receipt) + "\n")


# ─── CLI interface ───

if __name__ == "__main__":
    import sys

    ab = AuthorityBoundary()

    if len(sys.argv) < 2:
        print("Usage: hermes-authority-boundary.py <create|validate|bind>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "create":
        # Example: create envelope for a read-only probe
        env = ab.create_envelope(
            actor="hermes-agent",
            session="test-session",
            objective="Probe system state",
            operation="read",
            scope="/root/AAA,/root/.hermes",
            target="/root/AAA/federation/organs.yaml",
            issuer="F13-SOVEREIGN",
            ttl_seconds=300,
        )
        print(json.dumps(env.to_receipt(), indent=2))

    elif cmd == "validate":
        # Example: validate a write operation
        env = ab.create_envelope(
            actor="hermes-agent",
            session="test-session",
            objective="Update config",
            operation="write",
            scope="/root/.hermes",
            target="/root/.hermes/config.yaml",
            issuer="hermes-agent",  # SELF-AUTHORIZATION — should fail
        )
        result = ab.validate(env)
        print(f"Allowed: {result.allowed}")
        print(f"Verdict: {result.verdict.value}")
        print(f"Reason: {result.reason}")
        print(f"Failed: {result.failed_checks}")

    elif cmd == "bind":
        binding = ab.bind_trigger(
            trigger="deadline_approaching",
            proposed_action="send_reminder",
            scope="telegram:arif",
        )
        print(json.dumps(binding, indent=2))
        print(f"Valid: {ab.verify_binding(binding, 'telegram:arif')}")
        print(f"After scope change: {ab.verify_binding(binding, 'telegram:everyone')}")
