#!/usr/bin/env python3
"""
Warga Manager — arifOS Federation Citizen Registry
====================================================
Implements the 4-layer institutional architecture:
  Layer 1: Identity (warga.jsonl — append-only registry)
  Layer 2: Lifecycle (apprentice / review / prune / grieve)
  Layer 3: Community (scar_gossip.jsonl — reputation propagation)
  Layer 4: Visibility (CLI dashboard queries)

Canonical paths:
  /root/AAA/registry/warga.jsonl          — citizen registry (append-only)
  /root/AAA/registry/scar_gossip.jsonl    — gossip protocol (append-only)

Schema: arifos.warga.v1
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

# ── Canonical paths ──────────────────────────────────────────────────────────
REGISTRY_DIR = Path("/root/AAA/registry")
WARGA_FILE = REGISTRY_DIR / "warga.jsonl"
GOSSIP_FILE = REGISTRY_DIR / "scar_gossip.jsonl"

# ── Schema constants ─────────────────────────────────────────────────────────
SCHEMA_VERSION = "arifos.warga.v1"
AUTHORITY_BANDS = ["apprentice", "novice", "journeyman", "sovereign-witness"]
LIFECYCLE_STAGES = ["apprentice", "active", "review", "quarantine", "decommissioned"]
REVIEW_INTERVALS_DAYS = [30, 90, 180]
GOSSIP_RETENTION_DAYS = 90


# ── Utility ──────────────────────────────────────────────────────────────────
def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _append_jsonl(path: Path, record: dict) -> None:
    """Append a JSON record to an append-only JSONL file with file locking."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
            f.flush()
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def _read_jsonl(path: Path) -> list[dict]:
    """Read all records from a JSONL file."""
    if not path.exists():
        return []
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def _compute_record_hash(record: dict) -> str:
    """Compute SHA-256 of a record for integrity."""
    content = json.dumps(record, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 1: IDENTITY — Registry operations
# ══════════════════════════════════════════════════════════════════════════════

def register_agent(
    agent_id: str,
    role: str,
    authority_band: str = "apprentice",
    stage: str = "apprentice",
    metadata: dict | None = None,
) -> dict:
    """
    Register a new agent in the warga registry (Layer 1).
    Append-only: one record per agent, ever. Re-registration = new record with
    the old one marked superseded.
    """
    if authority_band not in AUTHORITY_BANDS:
        raise ValueError(f"Invalid authority_band: {authority_band}. Must be one of {AUTHORITY_BANDS}")
    if stage not in LIFECYCLE_STAGES:
        raise ValueError(f"Invalid stage: {stage}. Must be one of {LIFECYCLE_STAGES}")

    now = _now_iso()
    record = {
        "schema": SCHEMA_VERSION,
        "id": agent_id,
        "role": role,
        "created_at": now,
        "authority_band": authority_band,
        "stage": stage,
        "scars": 0,
        "fq": 0.0,
        "last_review": now,
        "next_review": (datetime.now(UTC) + timedelta(days=30)).isoformat(),
        "review_count": 0,
        "void_count": 0,
        "peer_acks": [],
        "superseded": False,
        "superseded_by": None,
        "metadata": metadata or {},
    }
    record["record_hash"] = _compute_record_hash(record)

    _append_jsonl(WARGA_FILE, record)
    return {"status": "registered", "record": record}


def get_agent(agent_id: str) -> dict | None:
    """Get the latest active record for an agent."""
    records = _read_jsonl(WARGA_FILE)
    # Last non-superseded record for this agent wins
    for rec in reversed(records):
        if rec.get("id") == agent_id and not rec.get("superseded", False):
            return rec
    return None


def list_agents(stage: str | None = None, authority_band: str | None = None) -> list[dict]:
    """List all active (non-superseded) agents, optionally filtered.
    Skips event records (lifecycle_review, lifecycle_grieve, gossip_broadcast).
    """
    records = _read_jsonl(WARGA_FILE)
    active = {}
    EVENT_TYPES = {"lifecycle_review", "lifecycle_grieve", "gossip_broadcast"}
    for rec in records:
        # Skip event records — they don't have agent identity
        if rec.get("event_type") in EVENT_TYPES:
            continue
        aid = rec.get("id")
        if not aid:
            continue
        if rec.get("superseded", False):
            active.pop(aid, None)
            continue
        # Always keep the latest record per agent (don't filter mid-loop)
        active[aid] = rec

    # Apply filters AFTER building the active dict
    result = list(active.values())
    if stage:
        result = [r for r in result if r.get("stage") == stage]
    if authority_band:
        result = [r for r in result if r.get("authority_band") == authority_band]
    return result


def supersede_agent(agent_id: str, reason: str, superseded_by: str | None = None) -> dict:
    """Mark an agent as superseded (decommissioned). Append a new record."""
    now = _now_iso()
    record = {
        "schema": SCHEMA_VERSION,
        "id": agent_id,
        "role": (get_agent(agent_id) or {}).get("role", "unknown"),
        "created_at": now,
        "authority_band": "apprentice",
        "stage": "decommissioned",
        "scars": 0,
        "fq": 0.0,
        "last_review": now,
        "next_review": None,
        "review_count": 0,
        "void_count": 0,
        "peer_acks": [],
        "superseded": True,
        "superseded_by": superseded_by,
        "decommission_reason": reason,
        "metadata": {},
    }
    record["record_hash"] = _compute_record_hash(record)
    _append_jsonl(WARGA_FILE, record)
    return {"status": "superseded", "record": record}


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 2: LIFECYCLE — Kernel verb handlers
# ══════════════════════════════════════════════════════════════════════════════

def lifecycle_apprentice(agent_id: str, shadow_of: str | None = None) -> dict:
    """
    Mode: APPRENTICE — 7-day shadow period, observe-only.
    Agent cannot write to production. Can read and observe.
    """
    agent = get_agent(agent_id)
    if agent and agent.get("stage") != "apprentice":
        return {"status": "blocked", "reason": f"Agent already at stage: {agent['stage']}"}

    now = _now_iso()
    shadow_end = (datetime.now(UTC) + timedelta(days=7)).isoformat()

    if not agent:
        # New agent — register
        reg = register_agent(agent_id, role="apprentice", stage="apprentice")
        agent = reg["record"]

    # Update shadow period metadata
    update = {
        **agent,
        "stage": "apprentice",
        "shadow_of": shadow_of,
        "shadow_started": now,
        "shadow_ends": shadow_end,
        "write_authority": False,
    }
    # Strip event fields
    for k in ("event_type", "gossip_type", "detail", "source", "broadcast_at", "acknowledged_by"):
        update.pop(k, None)
    update["record_hash"] = _compute_record_hash(update)
    _append_jsonl(WARGA_FILE, update)

    return {
        "status": "apprentice_started",
        "agent_id": agent_id,
        "shadow_of": shadow_of,
        "shadow_ends": shadow_end,
        "write_authority": False,
        "note": "Agent is observe-only for 7 days. Cannot write to production.",
    }


def lifecycle_review(agent_id: str, verdict: str, fq_score: float | None = None, reviewer: str = "arif") -> dict:
    """
    Mode: REVIEW — 30/90/180-day checkpoint.
    verdict: "continue" | "reinitiate" | "decommission"
    """
    agent = get_agent(agent_id)
    if not agent:
        return {"status": "error", "reason": f"Agent not found: {agent_id}"}

    now = _now_iso()
    review_record = {
        "schema": SCHEMA_VERSION,
        "event_type": "lifecycle_review",
        "agent_id": agent_id,
        "reviewed_at": now,
        "reviewer": reviewer,
        "verdict": verdict,
        "previous_stage": agent.get("stage"),
        "previous_band": agent.get("authority_band"),
        "fq_score": fq_score or agent.get("fq", 0.0),
        "scars": agent.get("scars", 0),
        "void_count": agent.get("void_count", 0),
        "review_count": agent.get("review_count", 0) + 1,
    }

    if verdict == "continue":
        # Promote if eligible (use new fq_score, not old record)
        new_band = agent.get("authority_band", "apprentice")
        new_stage = "active"
        effective_fq = fq_score if fq_score is not None else agent.get("fq", 0.0)
        if agent.get("scars", 0) == 0 and effective_fq >= 0.8:
            idx = AUTHORITY_BANDS.index(new_band) if new_band in AUTHORITY_BANDS else 0
            if idx < len(AUTHORITY_BANDS) - 1:
                new_band = AUTHORITY_BANDS[idx + 1]

        next_review_days = REVIEW_INTERVALS_DAYS[min(agent.get("review_count", 0), len(REVIEW_INTERVALS_DAYS) - 1)]
        update = {
            **agent,
            "stage": new_stage,
            "authority_band": new_band,
            "last_review": now,
            "next_review": (datetime.now(UTC) + timedelta(days=next_review_days)).isoformat(),
            "review_count": agent.get("review_count", 0) + 1,
            "fq": fq_score or agent.get("fq", 0.0),
        }
        # Remove event_type fields that might have leaked from previous records
        update.pop("event_type", None)
        update.pop("gossip_type", None)
        update.pop("detail", None)
        update.pop("source", None)
        update.pop("broadcast_at", None)
        update.pop("acknowledged_by", None)
        update["record_hash"] = _compute_record_hash(update)
        _append_jsonl(WARGA_FILE, update)
        review_record["new_stage"] = new_stage
        review_record["new_band"] = new_band

    elif verdict == "reinitiate":
        update = {
            **agent,
            "stage": "apprentice",
            "authority_band": "apprentice",
            "last_review": now,
            "next_review": (datetime.now(UTC) + timedelta(days=7)).isoformat(),
            "review_count": agent.get("review_count", 0) + 1,
        }
        update.pop("event_type", None)
        update.pop("gossip_type", None)
        update.pop("detail", None)
        update.pop("source", None)
        update.pop("broadcast_at", None)
        update.pop("acknowledged_by", None)
        update["record_hash"] = _compute_record_hash(update)
        _append_jsonl(WARGA_FILE, update)
        review_record["new_stage"] = "apprentice"
        review_record["new_band"] = "apprentice"

    elif verdict == "decommission":
        result = supersede_agent(agent_id, reason=f"Lifecycle review decommission by {reviewer}")
        review_record["new_stage"] = "decommissioned"

    else:
        return {"status": "error", "reason": f"Invalid verdict: {verdict}. Must be continue/reinitiate/decommission"}

    _append_jsonl(WARGA_FILE, {**review_record, "record_hash": _compute_record_hash(review_record)})
    return {"status": "review_complete", **review_record}


def lifecycle_prune(dry_run: bool = True) -> dict:
    """
    Mode: PRUNE — TTL expiry sweep. Identifies records past their TTL.
    If dry_run=True, returns candidates without modifying.
    If dry_run=False, marks expired records as superseded.
    """
    now = datetime.now(UTC)
    records = _read_jsonl(WARGA_FILE)
    active = {}
    for rec in records:
        aid = rec.get("id")
        if rec.get("superseded", False):
            active.pop(aid, None)
            continue
        active[aid] = rec

    candidates = []
    for aid, rec in active.items():
        next_review = rec.get("next_review")
        if not next_review:
            continue
        try:
            review_dt = datetime.fromisoformat(next_review)
            if review_dt.tzinfo is None:
                review_dt = review_dt.replace(tzinfo=UTC)
            days_overdue = (now - review_dt).days
            if days_overdue > 0:
                candidates.append({
                    "agent_id": aid,
                    "next_review": next_review,
                    "days_overdue": days_overdue,
                    "stage": rec.get("stage"),
                    "authority_band": rec.get("authority_band"),
                })
        except (ValueError, TypeError):
            continue

    if not dry_run and candidates:
        for c in candidates:
            supersede_agent(c["agent_id"], reason=f"Prune: {c['days_overdue']} days past review deadline")

    return {
        "status": "prune_complete",
        "dry_run": dry_run,
        "candidates_found": len(candidates),
        "candidates": candidates,
    }


def lifecycle_grieve(agent_id: str, failure_declaration: str, peer_verdict: str | None = None) -> dict:
    """
    Mode: GRIEVE — post-failure declaration, peer musyawarah.
    When an agent fails (arif_seal verdict=VOID), this mode handles:
    1. Declaration of what changed
    2. Peer review (gossip propagation)
    3. Decision: reintegrate | quarantine | decommission
    """
    agent = get_agent(agent_id)
    now = _now_iso()

    grieve_record = {
        "schema": SCHEMA_VERSION,
        "event_type": "lifecycle_grieve",
        "agent_id": agent_id,
        "declared_at": now,
        "failure_declaration": failure_declaration,
        "peer_verdict": peer_verdict,
        "previous_stage": agent.get("stage") if agent else "unknown",
        "previous_band": agent.get("authority_band") if agent else "unknown",
    }

    if peer_verdict == "reintegrate":
        if agent:
            update = {**agent}
            for k in ("event_type", "gossip_type", "detail", "source", "broadcast_at", "acknowledged_by"):
                update.pop(k, None)
            update["stage"] = "active"
            update["last_review"] = now
            update["void_count"] = agent.get("void_count", 0) + 1
            update["record_hash"] = _compute_record_hash(update)
            _append_jsonl(WARGA_FILE, update)
        grieve_record["new_stage"] = "active"
        grieve_record["note"] = "Agent reintegrated with failure recorded."

    elif peer_verdict == "quarantine":
        if agent:
            update = {**agent}
            for k in ("event_type", "gossip_type", "detail", "source", "broadcast_at", "acknowledged_by"):
                update.pop(k, None)
            update["stage"] = "quarantine"
            update["last_review"] = now
            update["void_count"] = agent.get("void_count", 0) + 1
            update["record_hash"] = _compute_record_hash(update)
            _append_jsonl(WARGA_FILE, update)
        grieve_record["new_stage"] = "quarantine"
        grieve_record["note"] = "Agent quarantined. Pending further review."

    elif peer_verdict == "decommission":
        result = supersede_agent(agent_id, reason=f"Grieve decommission: {failure_declaration}")
        grieve_record["new_stage"] = "decommissioned"
        grieve_record["note"] = "Agent decommissioned after failure."

    else:
        # No verdict yet — just record the declaration
        grieve_record["new_stage"] = agent.get("stage") if agent else "pending"
        grieve_record["note"] = "Failure declared. Awaiting peer musyawarah verdict."

    grieve_record["record_hash"] = _compute_record_hash(grieve_record)
    _append_jsonl(WARGA_FILE, grieve_record)

    # Also broadcast to gossip layer
    gossip_broadcast(agent_id, "VOID", failure_declaration)

    return {"status": "grieve_recorded", **grieve_record}


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 3: COMMUNITY — Gossip protocol
# ══════════════════════════════════════════════════════════════════════════════

def gossip_broadcast(agent_id: str, event_type: str, detail: str, source: str = "kernel") -> dict:
    """
    Broadcast a gossip event when arif_seal fires with verdict=VOID.
    Append-only to scar_gossip.jsonl.
    """
    now = _now_iso()
    gossip = {
        "schema": SCHEMA_VERSION,
        "event_type": "gossip_broadcast",
        "agent_id": agent_id,
        "gossip_type": event_type,  # VOID, REVIEW, REINTEGRATE, etc.
        "detail": detail,
        "source": source,
        "broadcast_at": now,
        "acknowledged_by": [],
    }
    gossip["record_hash"] = _compute_record_hash(gossip)
    _append_jsonl(GOSSIP_FILE, gossip)
    return {"status": "broadcast_sent", "gossip": gossip}


def gossip_ingest(agent_id: str) -> list[dict]:
    """
    Ingest gossip events relevant to an agent on arif_init.
    Returns all unacknowledged events.
    """
    records = _read_jsonl(GOSSIP_FILE)
    now = datetime.now(UTC)
    cutoff = now - timedelta(days=GOSSIP_RETENTION_DAYS)

    relevant = []
    for rec in records:
        if rec.get("superseded", False):
            continue
        broadcast_at = rec.get("broadcast_at")
        if broadcast_at:
            try:
                dt = datetime.fromisoformat(broadcast_at)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=UTC)
                if dt < cutoff:
                    continue
            except (ValueError, TypeError):
                continue

        # Relevant if: about this agent, or about any agent (for reputation awareness)
        relevant.append(rec)

    return relevant


def gossip_ack(agent_id: str, gossip_hash: str) -> dict:
    """Acknowledge a gossip event."""
    records = _read_jsonl(GOSSIP_FILE)
    updated = False
    for rec in records:
        if rec.get("record_hash") == gossip_hash:
            if agent_id not in rec.get("acknowledged_by", []):
                rec.setdefault("acknowledged_by", []).append(agent_id)
                rec["record_hash"] = _compute_record_hash(rec)
                updated = True
            break

    return {"status": "acknowledged" if updated else "already_acked_or_not_found", "gossip_hash": gossip_hash}


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 4: VISIBILITY — CLI Dashboard
# ══════════════════════════════════════════════════════════════════════════════

def dashboard_warga() -> str:
    """Show all active citizens with lifecycle stage and authority band."""
    agents = list_agents()
    if not agents:
        return "No active citizens in registry."

    lines = ["═══ WARGA REGISTRY ═══", ""]
    for a in sorted(agents, key=lambda x: x.get("authority_band", "")):
        lines.append(
            f"  {a['id']:20s} │ {a.get('stage','?'):14s} │ "
            f"band={a.get('authority_band','?'):18s} │ "
            f"scars={a.get('scars',0)} fq={a.get('fq',0.0):.2f} │ "
            f"review={a.get('next_review','?')[:10]}"
        )
    lines.append(f"\n  Total: {len(agents)} active citizens")
    return "\n".join(lines)


def dashboard_reputation() -> str:
    """Show scar count, FQ, and role coverage."""
    agents = list_agents()
    if not agents:
        return "No active citizens."

    lines = ["═══ REPUTATION ═══", ""]
    for a in sorted(agents, key=lambda x: -x.get("void_count", 0)):
        void_marker = " ⚠️" if a.get("void_count", 0) > 0 else ""
        lines.append(
            f"  {a['id']:20s} │ void={a.get('void_count',0)} │ "
            f"scars={a.get('scars',0)} │ fq={a.get('fq',0.0):.2f} │ "
            f"role={a.get('role','?')}{void_marker}"
        )
    return "\n".join(lines)


def dashboard_renewal_queue() -> str:
    """Show agents due for 30/90/180-day review."""
    agents = list_agents()
    now = datetime.now(UTC)

    lines = ["═══ RENEWAL QUEUE ═══", ""]
    due = []
    for a in agents:
        next_review = a.get("next_review")
        if not next_review:
            continue
        try:
            dt = datetime.fromisoformat(next_review)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)
            days_until = (dt - now).days
            due.append({**a, "days_until_review": days_until})
        except (ValueError, TypeError):
            continue

    if not due:
        return "No reviews due."

    for a in sorted(due, key=lambda x: x["days_until_review"]):
        status = "🔴 OVERDUE" if a["days_until_review"] < 0 else f"  {a['days_until_review']}d"
        lines.append(
            f"  {a['id']:20s} │ {status:12s} │ "
            f"next={a.get('next_review','?')[:10]} │ stage={a.get('stage','?')}"
        )
    return "\n".join(lines)


def dashboard_prune_queue() -> str:
    """Show TTL-expiring memories/scars/skills."""
    result = lifecycle_prune(dry_run=True)
    lines = ["═══ PRUNE QUEUE ═══", ""]
    if not result["candidates"]:
        return "No candidates for pruning."
    for c in result["candidates"]:
        lines.append(
            f"  {c['agent_id']:20s} │ overdue={c['days_overdue']}d │ "
            f"stage={c['stage']} │ band={c['authority_band']}"
        )
    lines.append(f"\n  Total: {result['candidates_found']} candidates")
    return "\n".join(lines)


def dashboard_apprentice_onboard() -> str:
    """Show agents currently in shadow period."""
    agents = list_agents(stage="apprentice")
    if not agents:
        return "No agents in apprentice/shadow period."

    lines = ["═══ APPRENTICE ONBOARD ═══", ""]
    now = datetime.now(UTC)
    for a in agents:
        shadow_ends = a.get("shadow_ends", "?")
        try:
            dt = datetime.fromisoformat(shadow_ends)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)
            days_left = (dt - now).days
            remaining = f"{days_left}d remaining" if days_left > 0 else "OVERDUE"
        except (ValueError, TypeError):
            remaining = "unknown"

        lines.append(
            f"  {a['id']:20s} │ shadow_of={a.get('shadow_of','?'):12s} │ "
            f"{remaining} │ write_auth={a.get('write_authority', False)}"
        )
    return "\n".join(lines)


def dashboard_gossip() -> str:
    """Show recent gossip events."""
    records = _read_jsonl(GOSSIP_FILE)
    if not records:
        return "No gossip events."

    now = datetime.now(UTC)
    cutoff = now - timedelta(days=GOSSIP_RETENTION_DAYS)
    lines = ["═══ GOSSIP FEED ═══", ""]

    recent = []
    for rec in records:
        broadcast_at = rec.get("broadcast_at")
        if broadcast_at:
            try:
                dt = datetime.fromisoformat(broadcast_at)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=UTC)
                if dt >= cutoff:
                    recent.append(rec)
            except (ValueError, TypeError):
                continue

    for rec in recent[-20:]:  # Last 20 events
        acks = len(rec.get("acknowledged_by", []))
        lines.append(
            f"  {rec.get('broadcast_at','?')[:19]} │ "
            f"{rec.get('agent_id','?'):20s} │ "
            f"type={rec.get('gossip_type','?'):8s} │ "
            f"acks={acks} │ "
            f"{rec.get('detail','')[:50]}"
        )

    lines.append(f"\n  Total: {len(recent)} events in last {GOSSIP_RETENTION_DAYS} days")
    return "\n".join(lines)


def dashboard_all() -> str:
    """Full dashboard: all surfaces."""
    sections = [
        dashboard_warga(),
        "",
        dashboard_reputation(),
        "",
        dashboard_renewal_queue(),
        "",
        dashboard_prune_queue(),
        "",
        dashboard_apprentice_onboard(),
        "",
        dashboard_gossip(),
    ]
    return "\n".join(sections)


# ══════════════════════════════════════════════════════════════════════════════
# CLI Interface
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="arifOS Warga Manager — Federation Citizen Registry")
    sub = parser.add_subparsers(dest="command")

    # register
    p_reg = sub.add_parser("register", help="Register a new agent")
    p_reg.add_argument("agent_id", help="Unique agent ID")
    p_reg.add_argument("--role", default="agent", help="Agent role")
    p_reg.add_argument("--band", default="apprentice", choices=AUTHORITY_BANDS)

    # get
    p_get = sub.add_parser("get", help="Get agent by ID")
    p_get.add_argument("agent_id")

    # list
    p_list = sub.add_parser("list", help="List all agents")
    p_list.add_argument("--stage", choices=LIFECYCLE_STAGES)
    p_list.add_argument("--band", choices=AUTHORITY_BANDS)

    # apprentice
    p_app = sub.add_parser("apprentice", help="Start shadow period")
    p_app.add_argument("agent_id")
    p_app.add_argument("--shadow-of", default=None)

    # review
    p_rev = sub.add_parser("review", help="Lifecycle review")
    p_rev.add_argument("agent_id")
    p_rev.add_argument("--verdict", required=True, choices=["continue", "reinitiate", "decommission"])
    p_rev.add_argument("--fq", type=float, default=None)
    p_rev.add_argument("--reviewer", default="arif")

    # prune
    p_prune = sub.add_parser("prune", help="TTL expiry sweep")
    p_prune.add_argument("--execute", action="store_true", help="Actually prune (not just dry run)")

    # grieve
    p_gri = sub.add_parser("grieve", help="Post-failure declaration")
    p_gri.add_argument("agent_id")
    p_gri.add_argument("--failure-declaration", required=True)
    p_gri.add_argument("--verdict", choices=["reintegrate", "quarantine", "decommission"])

    # gossip
    p_gos = sub.add_parser("gossip", help="Show gossip feed")
    p_bcast = sub.add_parser("broadcast", help="Manual gossip broadcast")
    p_bcast.add_argument("agent_id")
    p_bcast.add_argument("--type", default="MANUAL")
    p_bcast.add_argument("--detail", required=True)

    # dashboard
    p_dash = sub.add_parser("dashboard", help="Show dashboard")
    p_dash.add_argument("--surface", default="all",
                        choices=["all", "warga", "reputation", "renewal", "prune", "apprentice", "gossip"])

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "register":
        result = register_agent(args.agent_id, role=args.role, authority_band=args.band)
    elif args.command == "get":
        result = get_agent(args.agent_id)
        if result:
            print(json.dumps(result, indent=2))
            return
        else:
            print(f"Agent not found: {args.agent_id}")
            return
    elif args.command == "list":
        agents = list_agents(stage=args.stage, authority_band=args.band)
        for a in agents:
            print(json.dumps(a, indent=2))
        return
    elif args.command == "apprentice":
        result = lifecycle_apprentice(args.agent_id, shadow_of=args.shadow_of)
    elif args.command == "review":
        result = lifecycle_review(args.agent_id, verdict=args.verdict, fq_score=args.fq, reviewer=args.reviewer)
    elif args.command == "prune":
        result = lifecycle_prune(dry_run=not args.execute)
    elif args.command == "grieve":
        result = lifecycle_grieve(args.agent_id, failure_declaration=args.failure_declaration, peer_verdict=args.verdict)
    elif args.command == "gossip":
        print(dashboard_gossip())
        return
    elif args.command == "broadcast":
        result = gossip_broadcast(args.agent_id, event_type=args.type, detail=args.detail, source="manual")
    elif args.command == "dashboard":
        if args.surface == "all":
            print(dashboard_all())
        elif args.surface == "warga":
            print(dashboard_warga())
        elif args.surface == "reputation":
            print(dashboard_reputation())
        elif args.surface == "renewal":
            print(dashboard_renewal_queue())
        elif args.surface == "prune":
            print(dashboard_prune_queue())
        elif args.surface == "apprentice":
            print(dashboard_apprentice_onboard())
        elif args.surface == "gossip":
            print(dashboard_gossip())
        return
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
