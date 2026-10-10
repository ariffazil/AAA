"""pytest suite for jobplane — illegal-transition + overlapping-scope cases.

Run:  /usr/bin/python3 -m pytest /root/AAA/jobplane/test_jobplane.py -v
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobplane.core import (  # noqa: E402
    ACCEPTED_BY_HUMAN, AUTHORIZED, BLOCKED, LEASE_EXPIRED, LEASED, PROPOSED,
    QUEUED, RUNNING, SUCCEEDED, VERIFYING,
    IllegalTransition, JobPlane, JobNotFound, LeaseError, ScopeConflict,
    compute_idempotency_key, paths_overlap,
)


# ── fixtures / helpers ───────────────────────────────────────────────────────

class FakeClock:
    def __init__(self, start="2026-10-10T00:00:00+00:00"):
        self.dt = datetime.fromisoformat(start)

    def __call__(self) -> str:
        return self.dt.isoformat()

    def advance(self, seconds: int) -> None:
        self.dt += timedelta(seconds=seconds)


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def jp(tmp_path, clock):
    return JobPlane(str(tmp_path / "jobs.jsonl"), clock=clock)


def make_job(jp, allowed, **kw):
    return jp.create(
        scope={
            "repository": kw.pop("repository", "/root/repo"),
            "base_commit": kw.pop("base_commit", "deadbeef"),
            "allowed_paths": allowed,
            "forbidden_paths": kw.pop("forbidden", []),
            "mutation_class": kw.pop("mutation_class", "code_edit"),
        },
        acceptance_tests=kw.pop("acceptance", ["pytest -q"]),
        requested_by="arif",
        proposed_by="555-ASI",
        authorization_receipt=kw.pop("authorization_receipt", "REC-1"),
        **kw,
    )


def authorize_queue_claim(jp, job, holder="555-ASI", ttl=900):
    jid = job["job_id"]
    jp.transition(jid, AUTHORIZED, actor="arif", role="HUMAN")
    jp.transition(jid, QUEUED, actor="555-ASI")
    jp.claim(jid, holder=holder, ttl_seconds=ttl)
    return jid


# ── required: illegal transitions ────────────────────────────────────────────

def test_proposed_to_running_is_rejected(jp):
    job = make_job(jp, ["/root/repo/src"])
    with pytest.raises(IllegalTransition):
        jp.transition(job["job_id"], RUNNING, actor="555-ASI")
    # state unchanged, no snapshot appended beyond 'created'
    assert jp.get(job["job_id"])["state"] == PROPOSED


def test_proposed_cannot_skip_to_verifying_or_leased(jp):
    job = make_job(jp, ["/root/repo/src"])
    for bad in (VERIFYING, SUCCEEDED, LEASED):
        with pytest.raises(IllegalTransition):
            jp.transition(job["job_id"], bad, actor="x")
    # direct LEASED via transition is never allowed (must go through claim())
    with pytest.raises(IllegalTransition):
        jp.transition(job["job_id"], LEASED, actor="x")


def test_cannot_run_before_leased(jp):
    job = make_job(jp, ["/root/repo/src"])
    jp.transition(job["job_id"], AUTHORIZED, actor="arif", role="HUMAN")
    jp.transition(job["job_id"], QUEUED, actor="555-ASI")
    with pytest.raises(IllegalTransition):
        jp.transition(job["job_id"], RUNNING, actor="555-ASI")  # QUEUED->RUNNING illegal


def test_authorize_requires_human_or_judge(jp):
    job = make_job(jp, ["/root/repo/src"])
    with pytest.raises(IllegalTransition):
        jp.transition(job["job_id"], AUTHORIZED, actor="555-ASI", role="AGENT")
    jp.transition(job["job_id"], AUTHORIZED, actor="arif", role="HUMAN")
    assert jp.get(job["job_id"])["authorized_by"] == "arif"


# ── required: ACCEPTED_BY_HUMAN is a human act ───────────────────────────────

def test_agent_cannot_accept(jp):
    job = make_job(jp, ["/root/repo/src"])
    jid = authorize_queue_claim(jp, job)
    jp.transition(jid, RUNNING, actor="555-ASI")
    jp.transition(jid, VERIFYING, actor="555-ASI")
    jp.transition(jid, SUCCEEDED, actor="555-ASI")
    with pytest.raises(IllegalTransition):
        jp.transition(jid, ACCEPTED_BY_HUMAN, actor="555-ASI", role="AGENT")
    assert jp.get(jid)["state"] == SUCCEEDED


def test_runner_cannot_accept_even_claiming_human(jp):
    job = make_job(jp, ["/root/repo/src"])
    jid = authorize_queue_claim(jp, job, holder="bot")
    jp.transition(jid, RUNNING, actor="bot")
    jp.transition(jid, VERIFYING, actor="bot")
    jp.transition(jid, SUCCEEDED, actor="bot")
    # the lease holder (the runner) may NOT self-accept...
    with pytest.raises(IllegalTransition):
        jp.transition(jid, ACCEPTED_BY_HUMAN, actor="bot", role="HUMAN")
    # ...but a human who is not the runner may.
    jp.transition(jid, ACCEPTED_BY_HUMAN, actor="arif", role="HUMAN")
    assert jp.get(jid)["state"] == ACCEPTED_BY_HUMAN


# ── required: overlapping path scope ─────────────────────────────────────────

def test_overlapping_scope_claim_is_rejected(jp):
    a = make_job(jp, ["/root/repo/src/a"])
    b = jp.create(
        scope={"repository": "/root/repo", "base_commit": "cafe",
               "allowed_paths": ["/root/repo/src/a"], "forbidden_paths": [],
               "mutation_class": "code_edit"},
        acceptance_tests=["x"], authorization_receipt="REC-2",
    )
    aid = authorize_queue_claim(jp, a, holder="A")
    jp.transition(b["job_id"], AUTHORIZED, actor="arif", role="HUMAN")
    jp.transition(b["job_id"], QUEUED, actor="B")
    with pytest.raises(ScopeConflict):
        jp.claim(b["job_id"], holder="B")
    assert jp.get(b["job_id"])["state"] == QUEUED
    assert jp.get(aid)["state"] == LEASED


def test_nested_path_overlap_is_rejected(jp):
    a = make_job(jp, ["/root/repo/src/a"])
    b = jp.create(
        scope={"repository": "/root/repo", "base_commit": "cafe",
               "allowed_paths": ["/root/repo/src"], "forbidden_paths": [],
               "mutation_class": "code_edit"},
        acceptance_tests=["x"], authorization_receipt="REC-2",
    )
    authorize_queue_claim(jp, a, holder="A")
    jp.transition(b["job_id"], AUTHORIZED, actor="arif", role="HUMAN")
    jp.transition(b["job_id"], QUEUED, actor="B")
    with pytest.raises(ScopeConflict):
        jp.claim(b["job_id"], holder="B")


def test_non_overlapping_scope_claims_coexist(jp):
    a = make_job(jp, ["/root/repo/src/a"])
    b = jp.create(
        scope={"repository": "/root/repo", "base_commit": "cafe",
               "allowed_paths": ["/root/repo/docs"], "forbidden_paths": [],
               "mutation_class": "code_edit"},
        acceptance_tests=["x"], authorization_receipt="REC-2",
    )
    authorize_queue_claim(jp, a, holder="A")
    jp.transition(b["job_id"], AUTHORIZED, actor="arif", role="HUMAN")
    jp.transition(b["job_id"], QUEUED, actor="B")
    jp.claim(b["job_id"], holder="B")
    assert jp.get(b["job_id"])["state"] == LEASED
    assert len(jp.active_scopes()) == 2


def test_paths_overlap_semantics():
    assert paths_overlap("/x/y", "/x/y")
    assert paths_overlap("/x/y", "/x/y/z")
    assert not paths_overlap("/x/y", "/x/yz")   # boundary-aware
    assert not paths_overlap("/x/y", "/a/b")


# ── lease expiry / reclaim / heartbeat ───────────────────────────────────────

def test_expired_lease_is_reclaimed_and_scope_freed(jp, clock):
    a = make_job(jp, ["/root/repo/src"])
    jid = authorize_queue_claim(jp, a, holder="A", ttl=60)
    b = jp.create(
        scope={"repository": "/root/repo", "base_commit": "cafe",
               "allowed_paths": ["/root/repo/src"], "forbidden_paths": [],
               "mutation_class": "code_edit"},
        acceptance_tests=["x"], authorization_receipt="REC-2",
    )
    jp.transition(b["job_id"], AUTHORIZED, actor="arif", role="HUMAN")
    jp.transition(b["job_id"], QUEUED, actor="B")
    with pytest.raises(ScopeConflict):
        jp.claim(b["job_id"], holder="B")  # A still active

    clock.advance(120)  # A's lease lapses
    job_b = jp.claim(b["job_id"], holder="B")     # auto-reclaims A
    assert job_b["state"] == LEASED
    assert jp.get(jid)["state"] == LEASE_EXPIRED
    assert job_b["lease"]["holder"] == "B"


def test_expire_due_sweep(jp, clock):
    a = make_job(jp, ["/root/repo/src"])
    jid = authorize_queue_claim(jp, a, holder="A", ttl=30)
    assert jp.expire_due() == []           # not yet
    clock.advance(31)
    assert jp.expire_due() == [jid]
    assert jp.get(jid)["state"] == LEASE_EXPIRED


def test_heartbeat_extends_and_is_holder_only(jp, clock):
    a = make_job(jp, ["/root/repo/src"])
    jid = authorize_queue_claim(jp, a, holder="A", ttl=100)
    first_exp = jp.get(jid)["lease"]["expires_at"]
    clock.advance(50)
    jp.heartbeat(jid, holder="A", ttl_seconds=100)
    assert jp.get(jid)["lease"]["expires_at"] > first_exp
    with pytest.raises(LeaseError):
        jp.heartbeat(jid, holder="intruder")


def test_release_frees_scope(jp):
    a = make_job(jp, ["/root/repo/src"])
    jid = authorize_queue_claim(jp, a, holder="A")
    jp.release(jid, holder="A", to_state=QUEUED)
    assert jp.get(jid)["state"] == QUEUED
    assert jp.get(jid)["lease"]["holder"] is None
    assert jp.active_scopes() == []
    with pytest.raises(LeaseError):
        jp.release(jid, holder="A")  # no longer holder


# ── idempotency ──────────────────────────────────────────────────────────────

def test_create_is_idempotent(jp):
    a = make_job(jp, ["/root/repo/src"], base_commit="abc")
    b = make_job(jp, ["/root/repo/src"], base_commit="abc")
    assert a["job_id"] == b["job_id"]
    created = [e for e in jp.ledger.read_events() if e["event"] == "created"]
    assert len(created) == 1


def test_idempotency_key_is_order_insensitive_for_paths(jp):
    k1 = compute_idempotency_key(
        {"repository": "/r", "base_commit": "c", "allowed_paths": ["/a", "/b"],
         "forbidden_paths": [], "mutation_class": "code_edit"},
        ["t1"], "REC")
    k2 = compute_idempotency_key(
        {"repository": "/r", "base_commit": "c", "allowed_paths": ["/b", "/a"],
         "forbidden_paths": [], "mutation_class": "code_edit"},
        ["t1"], "REC")
    assert k1 == k2


def test_idempotency_key_changes_with_authorization_receipt(jp):
    base = {"repository": "/r", "base_commit": "c", "allowed_paths": ["/a"],
            "forbidden_paths": [], "mutation_class": "code_edit"}
    assert compute_idempotency_key(base, ["t"], "R1") != \
        compute_idempotency_key(base, ["t"], "R2")


# ── ledger durability / integrity ────────────────────────────────────────────

def test_ledger_is_append_only_and_hash_chained(jp):
    a = make_job(jp, ["/root/repo/src"])
    jid = authorize_queue_claim(jp, a, holder="A")
    jp.transition(jid, RUNNING, actor="A")
    events = jp.ledger.read_events()
    assert len(events) == 5  # created, authorized, queued, claimed, running
    prev = ""
    for ev in events:
        body = {k: v for k, v in ev.items() if k != "hash"}
        assert ev["prev_hash"] == prev
        expected = hashlib.sha256(
            (prev + json.dumps(body, sort_keys=True, separators=(",", ":"))).encode()
        ).hexdigest()
        assert ev["hash"] == expected
        prev = ev["hash"]


def test_get_missing_job_raises(jp):
    with pytest.raises(JobNotFound):
        jp.get("nope")


# ── envelope shape ───────────────────────────────────────────────────────────

def test_envelope_matches_contract_shape(jp):
    job = make_job(jp, ["/root/repo/src"])
    assert set(job.keys()) == {
        "job_id", "parent_session_id", "requested_by", "proposed_by",
        "authorized_by", "scope", "preconditions", "acceptance_tests",
        "rollback_plan", "lease", "idempotency_key", "state", "artifacts",
        "created_at", "updated_at",
    }
    assert set(job["scope"].keys()) == {
        "repository", "base_commit", "allowed_paths", "forbidden_paths",
        "mutation_class",
    }
    assert set(job["lease"].keys()) == {"holder", "expires_at", "attempt"}
    assert set(job["artifacts"].keys()) == {"backup", "diff", "test_report", "receipt"}
    assert job["state"] == PROPOSED
