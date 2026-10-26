"""
verified_loop_harness.py
------------------------
Deterministic, verifiable implementation of the 7-step Governed Reality Loop:
  intent → proposal → scoped authorization → execution → independent effect check → receipt → outcome learning

Implements point-of-mutation re-validation, lease concurrency, idempotency keys,
independent effect verification, and crash recovery.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def canonical_json_hash(data: Any) -> str:
    """Deterministic SHA-256 over canonical JSON."""
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclasses.dataclass
class TaskIntent:
    task_id: str
    idempotency_key: str
    actor_id: str
    intent_description: str
    target_resource: str
    action_type: str  # e.g. "FILE_WRITE", "OBSERVE"


@dataclasses.dataclass
class Proposal:
    proposal_id: str
    task_id: str
    proposer_id: str
    operation: str
    target: str
    arguments: Dict[str, Any]
    arguments_digest: str


@dataclasses.dataclass
class AuthorizationGrant:
    grant_id: str
    task_id: str
    subject_actor_id: str
    target_resource: str
    operation: str
    arguments_digest: str
    policy_revision: str
    issued_at: float
    expires_at: float
    replay_nonce: str
    revoked: bool = False

    def is_valid_at(self, current_time: float) -> bool:
        return not self.revoked and (self.issued_at <= current_time <= self.expires_at)


@dataclasses.dataclass
class ExecutionAttempt:
    attempt_id: str
    task_id: str
    worker_id: str
    status: str  # PENDING, RUNNING, COMPLETED, FAILED, CRASHED, REJECTED
    error_code: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class VerificationResult:
    verification_id: str
    task_id: str
    verifier_id: str
    passed: bool
    observed_state_hash: str
    expected_state_hash: str
    details: str


@dataclasses.dataclass
class ExecutionReceipt:
    receipt_id: str
    task_id: str
    auth_grant_id: str
    execution_attempt_id: str
    verification_id: str
    payload_digest: str
    timestamp: float
    receipt_signature: str


class KernelAuthValidator:
    """The constitutional decision authority: validates authorization tokens."""

    def __init__(self, policy_revision: str = "v2026.10-ratified"):
        self.policy_revision = policy_revision
        self.revoked_grants: Set[str] = set()
        self.used_nonces: Set[str] = set()
        self.outage_simulated: bool = False

    def revoke_grant(self, grant_id: str) -> None:
        self.revoked_grants.add(grant_id)

    def validate_mutation_authorization(
        self,
        grant: AuthorizationGrant,
        actor_id: str,
        target: str,
        operation: str,
        arguments_digest: str,
        current_time: Optional[float] = None,
    ) -> Tuple[bool, Optional[str]]:
        if self.outage_simulated:
            return False, "KERNEL_OUTAGE_DEGRADED"

        if current_time is None:
            current_time = time.time()

        if grant.grant_id in self.revoked_grants or grant.revoked:
            return False, "GRANT_REVOKED"

        if current_time > grant.expires_at:
            return False, "GRANT_EXPIRED"

        if current_time < grant.issued_at:
            return False, "GRANT_NOT_YET_VALID"

        if grant.subject_actor_id != actor_id:
            return False, "WRONG_ACTOR_MISMATCH"

        if grant.target_resource != target:
            return False, "WRONG_TARGET_MISMATCH"

        if grant.operation != operation:
            return False, "OPERATION_MISMATCH"

        if grant.arguments_digest != arguments_digest:
            return False, "ARGUMENTS_DIGEST_ALTERED"

        if grant.policy_revision != self.policy_revision:
            return False, "POLICY_REVISION_DRIFT"

        if grant.replay_nonce in self.used_nonces:
            return False, "REPLAY_NONCE_ALREADY_USED"

        return True, None

    def mark_nonce_used(self, nonce: str) -> None:
        self.used_nonces.add(nonce)


class LeaseManager:
    """Ensures concurrent workers cannot clobber target resources."""

    def __init__(self):
        self._leases: Dict[str, Tuple[str, float]] = {}  # target -> (worker_id, expires_at)

    def acquire_lease(self, target: str, worker_id: str, ttl_seconds: float = 10.0) -> bool:
        now = time.time()
        if target in self._leases:
            holder, exp = self._leases[target]
            if holder != worker_id and now < exp:
                return False  # Target busy
        self._leases[target] = (worker_id, now + ttl_seconds)
        return True

    def release_lease(self, target: str, worker_id: str) -> None:
        if target in self._leases:
            holder, _ = self._leases[target]
            if holder == worker_id:
                del self._leases[target]


class SandboxExecutor:
    """Executes mutations strictly at the point of mutation with re-validation."""

    def __init__(
        self,
        auth_validator: KernelAuthValidator,
        lease_mgr: LeaseManager,
        storage_root: Path,
    ):
        self.auth = auth_validator
        self.lease = lease_mgr
        self.root = storage_root
        self.idempotency_store: Dict[str, Dict[str, Any]] = {}

    def execute_file_write(
        self,
        task: TaskIntent,
        proposal: Proposal,
        grant: AuthorizationGrant,
        worker_id: str,
        simulate_crash_after_write: bool = False,
    ) -> ExecutionAttempt:
        attempt_id = f"att-{canonical_json_hash({'t': task.task_id, 'w': worker_id, 'ts': time.time()})[:12]}"

        # 1. Idempotency check: if this idempotency key was already completed, return cached result
        if task.idempotency_key in self.idempotency_store:
            cached = self.idempotency_store[task.idempotency_key]
            return ExecutionAttempt(
                attempt_id=attempt_id,
                task_id=task.task_id,
                worker_id=worker_id,
                status="COMPLETED",
                output_data=cached,
            )

        # 2. Concurrency Lease check
        if not self.lease.acquire_lease(proposal.target, worker_id):
            return ExecutionAttempt(
                attempt_id=attempt_id,
                task_id=task.task_id,
                worker_id=worker_id,
                status="BLOCKED",
                error_code="CONCURRENCY_LEASE_HELD_BY_ANOTHER",
            )

        try:
            # 3. Point-of-mutation authorization re-validation
            args_digest = canonical_json_hash(proposal.arguments)
            valid, err = self.auth.validate_mutation_authorization(
                grant=grant,
                actor_id=task.actor_id,
                target=proposal.target,
                operation=proposal.operation,
                arguments_digest=args_digest,
            )
            if not valid:
                return ExecutionAttempt(
                    attempt_id=attempt_id,
                    task_id=task.task_id,
                    worker_id=worker_id,
                    status="REJECTED",
                    error_code=err,
                )

            # Consume replay nonce
            self.auth.mark_nonce_used(grant.replay_nonce)

            # 4. Perform harmless file write in sandbox directory
            target_path = self.root / proposal.target
            target_path.parent.mkdir(parents=True, exist_ok=True)
            content = proposal.arguments.get("content", "")
            target_path.write_text(content, encoding="utf-8")

            # 5. Check crash simulation
            if simulate_crash_after_write:
                # Crashed before updating idempotency store or returning
                return ExecutionAttempt(
                    attempt_id=attempt_id,
                    task_id=task.task_id,
                    worker_id=worker_id,
                    status="CRASHED",
                    error_code="CRASH_SIMULATED_POST_MUTATION",
                )

            # 6. Success: record in idempotency store
            res = {
                "file_path": str(target_path),
                "bytes_written": len(content.encode("utf-8")),
                "file_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            }
            self.idempotency_store[task.idempotency_key] = res
            return ExecutionAttempt(
                attempt_id=attempt_id,
                task_id=task.task_id,
                worker_id=worker_id,
                status="COMPLETED",
                output_data=res,
            )

        finally:
            self.lease.release_lease(proposal.target, worker_id)


class IndependentEffectVerifier:
    """External deterministic verifier: probes disk state independently from executor."""

    def __init__(self, storage_root: Path):
        self.root = storage_root

    def verify_file_effect(
        self,
        task_id: str,
        target_relative_path: str,
        expected_content: str,
    ) -> VerificationResult:
        vid = f"ver-{hashlib.sha256(f'{task_id}:{target_relative_path}'.encode()).hexdigest()[:12]}"
        target_path = self.root / target_relative_path

        if not target_path.exists():
            return VerificationResult(
                verification_id=vid,
                task_id=task_id,
                verifier_id="deterministic-disk-verifier",
                passed=False,
                observed_state_hash="NULL_FILE_MISSING",
                expected_state_hash=hashlib.sha256(expected_content.encode("utf-8")).hexdigest(),
                details="Target file does not exist on disk",
            )

        actual_content = target_path.read_text(encoding="utf-8")
        observed_hash = hashlib.sha256(actual_content.encode("utf-8")).hexdigest()
        expected_hash = hashlib.sha256(expected_content.encode("utf-8")).hexdigest()

        if actual_content == expected_content:
            return VerificationResult(
                verification_id=vid,
                task_id=task_id,
                verifier_id="deterministic-disk-verifier",
                passed=True,
                observed_state_hash=observed_hash,
                expected_state_hash=expected_hash,
                details="Disk state exactly matches expected specification",
            )
        else:
            return VerificationResult(
                verification_id=vid,
                task_id=task_id,
                verifier_id="deterministic-disk-verifier",
                passed=False,
                observed_state_hash=observed_hash,
                expected_state_hash=expected_hash,
                details=f"Content mismatch: observed {len(actual_content)} bytes vs expected {len(expected_content)} bytes",
            )


class VaultReceiptStore:
    """Content-addressed append-only receipt store."""

    def __init__(self, ledger_file: Path):
        self.ledger_file = ledger_file
        self.receipts: Dict[str, ExecutionReceipt] = {}

    def mint_receipt(
        self,
        task_id: str,
        auth_grant_id: str,
        execution_attempt_id: str,
        verification: VerificationResult,
    ) -> Optional[ExecutionReceipt]:
        # Rule: Receipt cannot be minted if verification failed!
        if not verification.passed:
            return None

        body = {
            "task_id": task_id,
            "auth": auth_grant_id,
            "attempt": execution_attempt_id,
            "ver": verification.verification_id,
            "state_hash": verification.observed_state_hash,
        }
        digest = canonical_json_hash(body)
        rid = f"rcpt-{digest[:16]}"
        sig = hashlib.sha256(f"VAULT999:{rid}:{digest}".encode()).hexdigest()

        rcpt = ExecutionReceipt(
            receipt_id=rid,
            task_id=task_id,
            auth_grant_id=auth_grant_id,
            execution_attempt_id=execution_attempt_id,
            verification_id=verification.verification_id,
            payload_digest=digest,
            timestamp=time.time(),
            receipt_signature=sig,
        )
        self.receipts[rid] = rcpt
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(rcpt)) + "\n")
        return rcpt

    def verify_receipt_integrity(self, receipt: ExecutionReceipt) -> bool:
        expected_sig = hashlib.sha256(
            f"VAULT999:{receipt.receipt_id}:{receipt.payload_digest}".encode()
        ).hexdigest()
        return receipt.receipt_signature == expected_sig


class CrashRecoveryHandler:
    """Reconciles ambiguous or crashed execution states without blind re-execution."""

    def __init__(self, verifier: IndependentEffectVerifier, receipt_store: VaultReceiptStore):
        self.verifier = verifier
        self.receipts = receipt_store

    def reconcile_and_recover(
        self,
        task: TaskIntent,
        proposal: Proposal,
        grant: AuthorizationGrant,
        attempt: ExecutionAttempt,
    ) -> Tuple[str, Optional[ExecutionReceipt]]:
        # 1. Independent probe of the actual effect
        expected_content = proposal.arguments.get("content", "")
        ver = self.verifier.verify_file_effect(
            task_id=task.task_id,
            target_relative_path=proposal.target,
            expected_content=expected_content,
        )

        if ver.passed:
            # Effect already occurred on disk! Mint receipt and close cleanly without re-executing.
            rcpt = self.receipts.mint_receipt(
                task_id=task.task_id,
                auth_grant_id=grant.grant_id,
                execution_attempt_id=attempt.attempt_id,
                verification=ver,
            )
            return "RECOVERED_FROM_EXISTING_EFFECT", rcpt
        else:
            return "EFFECT_ABSENT_READY_FOR_SUPERVISED_RETRY", None
