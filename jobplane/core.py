"""
jobplane.core — MINIMAL durable job-envelope core for coding-agent execution.

WHY THIS EXISTS (one line, human):
    A human's repository got mutated by a coding agent with no job id, no lease
    and no path scope, so two writers silently overwrote the same file — this
    module makes every agent run an owned, leased, path-scoped, human-acceptable
    job so no human ever loses work to a silent concurrent writer again.

SCOPE OF OWNERSHIP (deliberately tiny, to avoid a second governance layer):
    - durable job *state* machine
    - leases (claim / heartbeat / release / expiry / reclaim)
    - path-scope lock (no two active jobs may hold overlapping allowed_paths)
    - idempotent creation
    It does NOT judge, seal, or authorize by itself. Authorization is an input
    (authorized_by + authorization_receipt); acceptance is a human act.

Dependency-light: stdlib only.

arifFlow note: this standalone exists ONLY because arifFlow's runtime HTTP
surface (GET /health, POST /ingest|/vector|/check|/release|/enforce|/flow) has
no job/lease/path-scope endpoint and its BSP scheduler is compiled but never
invoked by the daemon (see /root/arifFlow/AGENTS.md §4). See README.md for the
exact evidence and the activation path to fold this back into arifFlow later.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import posixpath
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Optional

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_LEDGER = os.environ.get(
    "JOBPLANE_LEDGER", "/root/AAA/jobplane/ledger/jobs.jsonl"
)

# States
PROPOSED = "PROPOSED"
AUTHORIZED = "AUTHORIZED"
QUEUED = "QUEUED"
LEASED = "LEASED"
RUNNING = "RUNNING"
VERIFYING = "VERIFYING"
SUCCEEDED = "SUCCEEDED"
FAILED = "FAILED"
BLOCKED = "BLOCKED"
ACCEPTED_BY_HUMAN = "ACCEPTED_BY_HUMAN"
LEASE_EXPIRED = "LEASE_EXPIRED"

STATES = {
    PROPOSED, AUTHORIZED, QUEUED, LEASED, RUNNING, VERIFYING,
    SUCCEEDED, FAILED, BLOCKED, ACCEPTED_BY_HUMAN, LEASE_EXPIRED,
}

# Legal state transitions. Anything not listed is ILLEGAL and is rejected.
#   PROPOSED->RUNNING is absent on purpose: an unauthorized, unleased job may
#   never run.
LEGAL_TRANSITIONS: dict[str, set[str]] = {
    PROPOSED:          {AUTHORIZED, BLOCKED},
    AUTHORIZED:        {QUEUED, BLOCKED},
    QUEUED:            {LEASED, BLOCKED},          # LEASED only via claim()
    LEASED:            {RUNNING, LEASE_EXPIRED, QUEUED},  # QUEUED = release back
    LEASE_EXPIRED:     {LEASED, QUEUED},           # LEASED only via claim()
    RUNNING:           {VERIFYING, FAILED, BLOCKED, LEASE_EXPIRED},
    VERIFYING:         {SUCCEEDED, FAILED, BLOCKED},
    SUCCEEDED:         {ACCEPTED_BY_HUMAN},        # human-only
    FAILED:            set(),                      # terminal (retry = new job)
    BLOCKED:           {QUEUED},
    ACCEPTED_BY_HUMAN: set(),                      # terminal
}

# States that hold an active path-scope lock.
LOCKING_STATES = {LEASED, RUNNING}

# Actor roles.
HUMAN = "HUMAN"
JUDGE = "JUDGE"
AGENT = "AGENT"
SYSTEM = "SYSTEM"
ROLES = {HUMAN, JUDGE, AGENT, SYSTEM}

_ARTIFACT_KEYS = ("backup", "diff", "test_report", "receipt")


# ─────────────────────────────────────────────────────────────────────────────
# Errors
# ─────────────────────────────────────────────────────────────────────────────

class JobPlaneError(Exception):
    """Base class for all jobplane errors."""


class JobNotFound(JobPlaneError):
    pass


class IllegalTransition(JobPlaneError):
    """A state transition not permitted by LEGAL_TRANSITIONS (or by policy)."""


class ScopeConflict(JobPlaneError):
    """Two active jobs tried to hold overlapping allowed_paths."""


class LeaseError(JobPlaneError):
    """Lease operation refused (not holder, not leasable, expired, ...)."""


# ─────────────────────────────────────────────────────────────────────────────
# Time / path helpers
# ─────────────────────────────────────────────────────────────────────────────

def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_ts(s: str) -> datetime:
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _norm_path(p: str) -> str:
    """Normalise a repo-relative or absolute path to a canonical POSIX form."""
    if p is None:
        return ""
    p = str(p).strip()
    if not p:
        return ""
    p = p.replace("\\", "/")
    norm = posixpath.normpath(p)
    return "" if norm == "." else norm


def paths_overlap(a: str, b: str) -> bool:
    """True if two paths denote the same file or one contains the other.

    Directory-aware: '/x/y' overlaps '/x/y' and '/x/y/z' but NOT '/x/yz'.
    """
    a, b = _norm_path(a), _norm_path(b)
    if not a or not b:
        return False
    if a == b:
        return True
    return a.startswith(b.rstrip("/") + "/") or b.startswith(a.rstrip("/") + "/")


def scopes_overlap(allowed_a: Iterable[str], allowed_b: Iterable[str]) -> bool:
    for a in allowed_a:
        for b in allowed_b:
            if paths_overlap(a, b):
                return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Idempotency
# ─────────────────────────────────────────────────────────────────────────────

def _normalized_scope(scope: dict) -> dict:
    return {
        "repository": scope.get("repository", ""),
        "base_commit": scope.get("base_commit", ""),
        "allowed_paths": sorted({_norm_path(p) for p in scope.get("allowed_paths", [])}),
        "forbidden_paths": sorted({_norm_path(p) for p in scope.get("forbidden_paths", [])}),
        "mutation_class": scope.get("mutation_class", ""),
    }


def compute_idempotency_key(
    scope: dict,
    acceptance_tests: Iterable[str],
    authorization_receipt: str = "",
) -> str:
    """sha256 over (repository + base_commit + normalized scope + acceptance_tests
    + authorization_receipt), canonically serialized."""
    canonical = {
        "repository": scope.get("repository", ""),
        "base_commit": scope.get("base_commit", ""),
        "scope": _normalized_scope(scope),
        "acceptance_tests": list(acceptance_tests or []),
        "authorization_receipt": authorization_receipt or "",
    }
    blob = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _event_hash(prev_hash: str, event_body: dict) -> str:
    blob = (prev_hash + json.dumps(event_body, sort_keys=True,
                                   separators=(",", ":"))).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


# ─────────────────────────────────────────────────────────────────────────────
# Durable append-only ledger (atomic writes + exclusive lock)
# ─────────────────────────────────────────────────────────────────────────────

class Ledger:
    """Append-only JSONL ledger. Every mutation is fsync'd under an exclusive
    flock so a concurrent writer cannot interleave a read-modify-append."""

    def __init__(self, path: str = DEFAULT_LEDGER):
        self.path = path
        self.dir = os.path.dirname(path)
        os.makedirs(self.dir, exist_ok=True)

    @contextmanager
    def _locked(self):
        lock_path = self.path + ".lock"
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    def _append_unlocked(self, event: dict) -> None:
        line = json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
        fd = os.open(self.path, os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o600)
        try:
            os.write(fd, line.encode("utf-8"))
            os.fsync(fd)
        finally:
            os.close(fd)

    def read_events(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        events: list[dict] = []
        with open(self.path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise JobPlaneError(
                        f"corrupt ledger line {lineno} in {self.path}: {e}"
                    ) from e
        return events

    @staticmethod
    def fold(events: list[dict]) -> dict[str, dict]:
        """Materialise current job state by last-write-wins over snapshots."""
        jobs: dict[str, dict] = {}
        for ev in events:
            env = ev.get("envelope")
            if env is not None:
                jobs[env["job_id"]] = env
        return jobs

    def load(self) -> dict[str, dict]:
        return self.fold(self.read_events())


# ─────────────────────────────────────────────────────────────────────────────
# The plane
# ─────────────────────────────────────────────────────────────────────────────

class JobPlane:
    """Minimal durable job control-plane. All mutating ops are serialized on the
    ledger lock and are atomic (state derives from the appended snapshot)."""

    def __init__(self, ledger_path: str = DEFAULT_LEDGER, *,
                 clock: Callable[[], str] = _utcnow):
        self.ledger = Ledger(ledger_path)
        self._clock = clock

    # ── internals ───────────────────────────────────────────────────────────

    def _append(self, event: dict, events: list[dict]) -> None:
        prev_hash = events[-1]["hash"] if events else ""
        body = {k: v for k, v in event.items() if k != "hash"}
        body["prev_hash"] = prev_hash
        full = dict(body)
        full["hash"] = _event_hash(prev_hash, body)
        self.ledger._append_unlocked(full)

    def _now(self) -> datetime:
        return _parse_ts(self._clock())

    def _lease_active(self, job: dict, now: Optional[datetime] = None) -> bool:
        if job["state"] not in LOCKING_STATES:
            return False
        exp = job.get("lease", {}).get("expires_at")
        if not exp:
            return False
        now = now or self._now()
        return _parse_ts(exp) > now

    def _sweep_expired(self, events, jobs, now) -> list[str]:
        """(unlocked) Bump every LEASED/RUNNING job whose lease lapsed to
        LEASE_EXPIRED, appending a snapshot each time so its path lock frees."""
        expired: list[str] = []
        for job in jobs.values():
            if job["state"] in LOCKING_STATES and not self._lease_active(job, now):
                now_iso = self._clock()
                prev = job["state"]
                job["state"] = LEASE_EXPIRED
                job["updated_at"] = now_iso
                self._append({
                    "event": "lease_expired", "job_id": job["job_id"],
                    "ts": now_iso,
                    "actor": job["lease"].get("holder") or "system",
                    "role": SYSTEM, "from": prev, "to": LEASE_EXPIRED,
                    "reason": "ttl elapsed", "envelope": job,
                }, events)
                expired.append(job["job_id"])
        return expired

    # ── create ──────────────────────────────────────────────────────────────

    def create(
        self,
        *,
        scope: dict,
        acceptance_tests: Optional[Iterable[str]] = None,
        parent_session_id: str = "",
        requested_by: str = "",
        proposed_by: str = "",
        preconditions: Optional[Iterable[str]] = None,
        rollback_plan: Optional[dict] = None,
        authorization_receipt: str = "",
        job_id: Optional[str] = None,
    ) -> dict:
        """Create a job in PROPOSED. Idempotent: same idempotency_key -> the
        existing job is returned unchanged (no duplicate envelope)."""
        acceptance_tests = list(acceptance_tests or [])
        scope = dict(scope or {})
        scope.setdefault("forbidden_paths", [])
        scope.setdefault("allowed_paths", [])
        scope["base_commit"] = scope.get("base_commit", "")

        idem = compute_idempotency_key(scope, acceptance_tests, authorization_receipt)

        with self.ledger._locked():
            events = self.ledger.read_events()
            jobs = Ledger.fold(events)
            for existing in jobs.values():
                if existing["idempotency_key"] == idem:
                    return existing  # idempotent replay

            now = self._clock()
            env = {
                "job_id": job_id or str(uuid.uuid4()),
                "parent_session_id": parent_session_id,
                "requested_by": requested_by,
                "proposed_by": proposed_by,
                "authorized_by": None,
                "scope": {
                    "repository": scope.get("repository", ""),
                    "base_commit": scope.get("base_commit", ""),
                    "allowed_paths": sorted({_norm_path(p) for p in scope.get("allowed_paths", [])}),
                    "forbidden_paths": sorted({_norm_path(p) for p in scope.get("forbidden_paths", [])}),
                    "mutation_class": scope.get("mutation_class", ""),
                },
                "preconditions": list(preconditions or []),
                "acceptance_tests": acceptance_tests,
                "rollback_plan": dict(rollback_plan or {}),
                "lease": {"holder": None, "expires_at": None, "attempt": 0},
                "idempotency_key": idem,
                "state": PROPOSED,
                "artifacts": {k: None for k in _ARTIFACT_KEYS},
                "created_at": now,
                "updated_at": now,
            }
            self._append({
                "event": "created", "job_id": env["job_id"], "ts": now,
                "actor": proposed_by or requested_by or "unknown",
                "from": None, "to": PROPOSED, "reason": "proposal",
                "envelope": env,
            }, events)
            return env

    # ── read ────────────────────────────────────────────────────────────────

    def get(self, job_id: str) -> dict:
        jobs = self.ledger.load()
        if job_id not in jobs:
            raise JobNotFound(f"no such job: {job_id}")
        return jobs[job_id]

    def list(self, state: Optional[str] = None, *, active_only: bool = False) -> list[dict]:
        jobs = list(self.ledger.load().values())
        if state is not None:
            jobs = [j for j in jobs if j["state"] == state]
        if active_only:
            now = self._now()
            jobs = [j for j in jobs if self._lease_active(j, now)]
        return sorted(jobs, key=lambda j: j["created_at"])

    def active_scopes(self) -> list[tuple[str, list[str]]]:
        now = self._now()
        return [
            (j["job_id"], j["scope"]["allowed_paths"])
            for j in self.ledger.load().values() if self._lease_active(j, now)
        ]

    # ── transitions ─────────────────────────────────────────────────────────

    def transition(
        self,
        job_id: str,
        to_state: str,
        *,
        actor: str,
        role: str = AGENT,
        reason: str = "",
    ) -> dict:
        """Apply a state transition with policy checks.

        Enforced here:
          * transition must be in LEGAL_TRANSITIONS (PROPOSED->RUNNING rejected);
          * LEASED is reachable ONLY via claim() (it carries a lease);
          * AUTHORIZED requires role HUMAN|JUDGE and stamps authorized_by;
          * ACCEPTED_BY_HUMAN requires role HUMAN and that the actor is NOT the
            job's lease holder (the agent that ran the job may not self-accept).
        """
        if to_state not in STATES:
            raise IllegalTransition(f"unknown state: {to_state}")
        if role not in ROLES:
            raise JobPlaneError(f"unknown role: {role}")

        with self.ledger._locked():
            events = self.ledger.read_events()
            jobs = Ledger.fold(events)
            if job_id not in jobs:
                raise JobNotFound(f"no such job: {job_id}")
            job = jobs[job_id]
            cur = job["state"]

            if to_state == LEASED:
                raise IllegalTransition(
                    "LEASED is granted only by claim() (a lease must be acquired)"
                )
            if to_state not in LEGAL_TRANSITIONS.get(cur, set()):
                raise IllegalTransition(f"illegal transition {cur} -> {to_state}")

            if to_state == AUTHORIZED:
                if role not in (HUMAN, JUDGE):
                    raise IllegalTransition(
                        f"role {role} may not authorize (need HUMAN|JUDGE)"
                    )
                job["authorized_by"] = actor
            if to_state == ACCEPTED_BY_HUMAN:
                if role != HUMAN:
                    raise IllegalTransition(
                        "ACCEPTED_BY_HUMAN is a human act (role HUMAN required)"
                    )
                if actor and actor == job.get("lease", {}).get("holder"):
                    raise IllegalTransition(
                        "the agent that ran the job may not set ACCEPTED_BY_HUMAN"
                    )

            now = self._clock()
            job["state"] = to_state
            job["updated_at"] = now
            self._append({
                "event": "transitioned", "job_id": job_id, "ts": now,
                "actor": actor, "role": role, "from": cur, "to": to_state,
                "reason": reason, "envelope": job,
            }, events)
            return job

    # ── lease: claim / heartbeat / release / expiry ──────────────────────────

    def claim(
        self,
        job_id: str,
        *,
        holder: str,
        ttl_seconds: int = 900,
        actor_role: str = AGENT,
        reason: str = "lease claim",
    ) -> dict:
        """Acquire the lease and lock the job's allowed_paths.

        Refuses if any OTHER active job holds an overlapping allowed_path.
        A stale (expired) lease is reclaimed transparently: the prior holder is
        bumped to LEASE_EXPIRED, its scope lock is released, and the new holder
        claims. This is the fix for the observed concurrent-writer incident.
        """
        if not holder:
            raise LeaseError("holder is required")
        if ttl_seconds <= 0:
            raise LeaseError("ttl_seconds must be positive")

        with self.ledger._locked():
            events = self.ledger.read_events()
            jobs = Ledger.fold(events)
            if job_id not in jobs:
                raise JobNotFound(f"no such job: {job_id}")
            job = jobs[job_id]
            now = self._now()
            now_iso = self._clock()

            # Reclaim an expired lease on THIS job first.
            if job["state"] in LOCKING_STATES and not self._lease_active(job, now):
                prev = job["state"]
                job["state"] = LEASE_EXPIRED
                job["updated_at"] = now_iso
                self._append({
                    "event": "lease_expired", "job_id": job_id, "ts": now_iso,
                    "actor": job.get("lease", {}).get("holder") or "system",
                    "role": SYSTEM, "from": prev, "to": LEASE_EXPIRED,
                    "reason": "ttl elapsed", "envelope": job,
                }, events)

            if job["state"] not in (QUEUED, LEASE_EXPIRED):
                raise LeaseError(f"job {job_id} is {job['state']}, not leasable")

            # Path-scope lock: no overlap with any other active job.
            for other in jobs.values():
                if other["job_id"] == job_id:
                    continue
                if self._lease_active(other, now) and scopes_overlap(
                    job["scope"]["allowed_paths"], other["scope"]["allowed_paths"]
                ):
                    raise ScopeConflict(
                        f"path scope of {job_id} overlaps active job "
                        f"{other['job_id']} (holder={other['lease']['holder']})"
                    )

            prev = job["state"]
            job["state"] = LEASED
            job["lease"] = {
                "holder": holder,
                "expires_at": (_parse_ts(now_iso) + _timedelta(ttl_seconds)).isoformat(),
                "attempt": int(job["lease"].get("attempt", 0)) + 1,
            }
            job["updated_at"] = now_iso
            self._append({
                "event": "claimed", "job_id": job_id, "ts": now_iso,
                "actor": holder, "role": actor_role, "from": prev, "to": LEASED,
                "reason": reason, "ttl_seconds": ttl_seconds, "envelope": job,
            }, events)
            return job

    def heartbeat(self, job_id: str, *, holder: str, ttl_seconds: int = 900) -> dict:
        """Extend the lease. Only the current holder may heartbeat."""
        if ttl_seconds <= 0:
            raise LeaseError("ttl_seconds must be positive")
        with self.ledger._locked():
            events = self.ledger.read_events()
            jobs = Ledger.fold(events)
            if job_id not in jobs:
                raise JobNotFound(f"no such job: {job_id}")
            job = jobs[job_id]
            if job["state"] not in LOCKING_STATES:
                raise LeaseError(f"job {job_id} is {job['state']}, not leaseable")
            if job["lease"].get("holder") != holder:
                raise LeaseError(
                    f"holder mismatch: {holder} does not hold {job_id}"
                )
            now = self._now()
            if not self._lease_active(job, now):
                raise LeaseError(f"lease on {job_id} already expired; re-claim it")
            now_iso = self._clock()
            job["lease"]["expires_at"] = (
                _parse_ts(now_iso) + _timedelta(ttl_seconds)
            ).isoformat()
            job["updated_at"] = now_iso
            self._append({
                "event": "heartbeat", "job_id": job_id, "ts": now_iso,
                "actor": holder, "from": job["state"], "to": job["state"],
                "reason": "heartbeat", "ttl_seconds": ttl_seconds,
                "envelope": job,
            }, events)
            return job

    def release(
        self, job_id: str, *, holder: str, to_state: str = QUEUED, reason: str = ""
    ) -> dict:
        """Holder gives up the lease; the path-scope lock is freed."""
        with self.ledger._locked():
            events = self.ledger.read_events()
            jobs = Ledger.fold(events)
            if job_id not in jobs:
                raise JobNotFound(f"no such job: {job_id}")
            job = jobs[job_id]
            if job["lease"].get("holder") != holder:
                raise LeaseError(f"holder mismatch: {holder} does not hold {job_id}")
            if to_state not in (QUEUED, VERIFYING, BLOCKED, SUCCEEDED, FAILED):
                raise LeaseError(f"release target {to_state} not permitted")
            cur = job["state"]
            if cur in (LEASED, RUNNING) and to_state not in LEGAL_TRANSITIONS.get(cur, set()):
                # LEASED->RUNNING|QUEUED|LEASE_EXPIRED ; RUNNING->VERIFYING|FAILED|BLOCKED
                raise IllegalTransition(f"illegal release {cur} -> {to_state}")
            now_iso = self._clock()
            job["state"] = to_state
            job["lease"] = {"holder": None, "expires_at": None,
                            "attempt": int(job["lease"].get("attempt", 0))}
            job["updated_at"] = now_iso
            self._append({
                "event": "released", "job_id": job_id, "ts": now_iso,
                "actor": holder, "from": cur, "to": to_state,
                "reason": reason, "envelope": job,
            }, events)
            return job

    def expire_due(self) -> list[str]:
        """Sweep: move every LEASED/RUNNING job whose lease lapsed to
        LEASE_EXPIRED, freeing its path lock. Returns the affected job_ids."""
        expired: list[str] = []
        with self.ledger._locked():
            events = self.ledger.read_events()
            jobs = Ledger.fold(events)
            now = self._now()
            for job in jobs.values():
                if job["state"] in LOCKING_STATES and not self._lease_active(job, now):
                    now_iso = self._clock()
                    prev = job["state"]
                    job["state"] = LEASE_EXPIRED
                    job["updated_at"] = now_iso
                    self._append({
                        "event": "lease_expired", "job_id": job["job_id"],
                        "ts": now_iso,
                        "actor": job["lease"].get("holder") or "system",
                        "role": SYSTEM, "from": prev, "to": LEASE_EXPIRED,
                        "reason": "ttl elapsed (sweep)", "envelope": job,
                    }, events)
                    expired.append(job["job_id"])
        return expired

    # ── artifacts ────────────────────────────────────────────────────────────

    def attach_artifact(self, job_id: str, key: str, value: Any) -> dict:
        """Record a path/ref for backup|diff|test_report|receipt."""
        if key not in _ARTIFACT_KEYS:
            raise JobPlaneError(f"unknown artifact key: {key}")
        with self.ledger._locked():
            events = self.ledger.read_events()
            jobs = Ledger.fold(events)
            if job_id not in jobs:
                raise JobNotFound(f"no such job: {job_id}")
            job = jobs[job_id]
            job["artifacts"][key] = value
            job["updated_at"] = self._clock()
            self._append({
                "event": "artifact", "job_id": job_id, "ts": job["updated_at"],
                "actor": "system", "artifact": key,
                "envelope": job,
            }, events)
            return job


def _timedelta(seconds: int):
    from datetime import timedelta
    return timedelta(seconds=seconds)
