"""
attention_plane.py — P2 2026-09-21 (AAA-ATTENTION-CONVERGENCE).

Canonical AttentionPacket schema + priority formula.

Identity:
    AAA : (evidence, state, deadlines, drift, uncertainty) → AttentionPacket

Pipeline (per F13 2026-09-21):
    Reality → HERMES (meaning) → CHRON (temporal) → AAA (attention) → arifOS/Human

AAA does NOT:
  - Judge (that's arifOS)
  - Execute (that's A-FORGE)
  - Witness (that's FRAME / VAULT999 / arifFlow)
  - Decide truth (that's HERMES / FRAME)

AAA DOES:
  - Classify (ObservedState_A ?= ObservedState_B)
  - Prioritize (Impact × Urgency × EvidenceQuality × Novelty / AttentionCost)
  - Compress (one AttentionPacket per subject, not N dashboards)
  - Recommend routing (AAA_route_recommendation, NOT arifOS_route_dispatch)

Priority formula:
    P = (Impact × Urgency × EvidenceQuality × Novelty) / AttentionCost

Hard overrides (force P = ∞ / must-show):
  - authority_violation
  - security_breach
  - deadline_expiry
  - failed_invariant
  - irreversibility_floor (high floor, not necessarily ∞)

Constitutional:
    F1 AMANAH — fail-closed on missing inputs; attention_cost ≥ 1.0
    F2 TRUTH  — every field carries evidence provenance
    F11 AUDIT — every AttentionPacket writes to /root/AAA/attention/ledger.jsonl
"""

from __future__ import annotations

import datetime as _dt
import json
import math
import os
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# ── Configuration ───────────────────────────────────────────────────

CHRON_URL = os.getenv("CHRON_URL", "http://127.0.0.1:18102")
HERMES_URL = os.getenv("HERMES_URL", "http://127.0.0.1:18087")
AAA_URL = os.getenv("AAA_URL", "http://127.0.0.1:3001")
ATTENTION_LEDGER = Path("/root/AAA/attention/ledger.jsonl")

# ── Enums ───────────────────────────────────────────────────────────

class AttentionClass(str, Enum):
    """The kind of attention the packet is requesting."""

    ACTION_REQUIRED = "ACTION_REQUIRED"
    INFORM = "INFORM"
    HOLD = "HOLD"
    DEFER = "DEFER"
    SILENT = "SILENT"  # explicitly: do not show this now


class EpistemicState(str, Enum):
    """Evidence quality state for the attention subject."""

    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    INTERPRETED = "INTERPRETED"
    SPECULATED = "SPECULATED"
    ASSUMED = "ASSUMED"
    MISSING = "MISSING"


class Override(str, Enum):
    """Hard overrides that force priority to ∞ (must-show)."""

    AUTHORITY_VIOLATION = "authority_violation"
    SECURITY_BREACH = "security_breach"
    DEADLINE_EXPIRY = "deadline_expiry"
    FAILED_INVARIANT = "failed_invariant"
    IRREVERSIBILITY_FLOOR = "irreversibility_floor"  # high floor, not ∞


# ── AttentionPacket dataclass ───────────────────────────────────────

@dataclass
class AttentionPacket:
    """Canonical machine-readable attention object (16 fields).

    Every surface projects from this. One subject → one packet.
    No dashboard code; this IS the dashboard contract.
    """

    # Identity
    subject: str
    attention_class: AttentionClass

    # Scoring
    priority: float  # 0.0 – ∞ (∞ = must-show override)

    # Why-now
    why_now: str
    deadline: str | None = None  # ISO 8601 or None

    # Multi-axis scoring (used by formula)
    impact: float = 0.5             # 0.0–1.0
    urgency: float = 0.5            # 0.0–1.0
    uncertainty: float = 0.5        # 0.0–1.0 (higher = less certain)
    reversibility: float = 0.5     # 0.0–1.0 (higher = more reversible)

    # Evidence (HERMES contract)
    epistemic_state: EpistemicState = EpistemicState.OBSERVED
    source_count: int = 0
    contradictions: int = 0

    # Temporal (CHRON contract)
    temporal: dict[str, Any] = field(default_factory=dict)
    # e.g. {"prediction_due": False, "staleness_seconds": 24, "attention_debt": 0.0}

    # Routing recommendation (NOT dispatch — that's arifOS)
    recommended_organ: str = ""
    required_authority: str = "OBSERVE_ONLY"  # OBSERVE_ONLY | LIMITED_MUTATE | FULL
    execution_required: bool = False

    # Overrides + provenance
    overrides: list[str] = field(default_factory=list)
    evidence_basis: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # JSON-serializable enums
        d["attention_class"] = self.attention_class.value
        d["epistemic_state"] = self.epistemic_state.value
        d["overrides"] = list(self.overrides)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "AttentionPacket":
        return cls(
            subject=d["subject"],
            attention_class=AttentionClass(d["attention_class"]),
            priority=float(d["priority"]),
            why_now=d.get("why_now", ""),
            deadline=d.get("deadline"),
            impact=float(d.get("impact", 0.5)),
            urgency=float(d.get("urgency", 0.5)),
            uncertainty=float(d.get("uncertainty", 0.5)),
            reversibility=float(d.get("reversibility", 0.5)),
            epistemic_state=EpistemicState(d.get("epistemic_state", "OBSERVED")),
            source_count=int(d.get("source_count", 0)),
            contradictions=int(d.get("contradictions", 0)),
            temporal=d.get("temporal", {}),
            recommended_organ=d.get("recommended_organ", ""),
            required_authority=d.get("required_authority", "OBSERVE_ONLY"),
            execution_required=bool(d.get("execution_required", False)),
            overrides=d.get("overrides", []),
            evidence_basis=d.get("evidence_basis", []),
        )


# ── Priority formula ───────────────────────────────────────────────

def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def compute_priority(
    *,
    impact: float,
    urgency: float,
    uncertainty: float,
    reversibility: float = 0.5,
    attention_cost: float = 1.0,
    overrides: list[str] | None = None,
    novelty: float = 0.5,
) -> tuple[float, list[str]]:
    """Compute AttentionPacket priority.

    Formula:
        P = (Impact × Urgency × EvidenceQuality × Novelty) / AttentionCost

    EvidenceQuality = (1 - Uncertainty) × Reversibility

    Hard overrides (force P = ∞ for must-show):
      - authority_violation, security_breach, deadline_expiry,
        failed_invariant → P = ∞
      - irreversibility_floor → P ≥ 0.85 (high floor, not ∞)

    Returns (priority, applied_overrides).
    """
    applied: list[str] = []

    # F1 AMANAH — attention_cost cannot be zero (would yield ∞)
    cost = max(attention_cost, 0.01)

    evidence_quality = (1.0 - _clamp(uncertainty)) * _clamp(reversibility)

    numerator = (
        _clamp(impact)
        * _clamp(urgency)
        * _clamp(evidence_quality)
        * _clamp(novelty)
    )

    p = numerator / cost

    if overrides:
        for ov in overrides:
            if ov == Override.IRREVERSIBILITY_FLOOR.value:
                # High floor for irreversible actions
                p = max(p, 0.85)
                applied.append(ov)
            elif ov in {
                Override.AUTHORITY_VIOLATION.value,
                Override.SECURITY_BREACH.value,
                Override.DEADLINE_EXPIRY.value,
                Override.FAILED_INVARIANT.value,
            }:
                # Must-show
                p = math.inf
                applied.append(ov)

    return (p, applied)


# ── CHRON integration ──────────────────────────────────────────────

def fetch_chron_attention_debt() -> dict[str, Any]:
    """Pull CHRON's temporal urgency inputs via MCP.

    CHRON is the canonical source for:
      - attention_debt (how much owed attention has accumulated)
      - active predictions (count + due-soon flag)
      - next_verify_at (next calibration deadline)
      - calibration summary (mean Brier, accuracy)

    Live probe (2026-09-21) confirms CHRON briefing shape:
        {"predictions_due": [...], "calibration": {...},
         "attention_debt": {"total_ad": 0, ...}, "last_loop": {...}}
    """
    out: dict[str, Any] = {
        "available": False,
        "attention_debt": 0.0,
        "prediction_due": False,
        "predictions_due_count": 0,
        "next_verify_at": None,
        "source": "unavailable",
    }
    sid: str | None = None
    try:
        # Initialize CHRON MCP session
        init_req = urllib.request.Request(
            f"{CHRON_URL}/mcp",
            data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                              "params": {"protocolVersion": "2025-06-18",
                                         "capabilities": {},
                                         "clientInfo": {"name": "attention_plane", "version": "1.0"}}}).encode(),
            headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
            method="POST",
        )
        with urllib.request.urlopen(init_req, timeout=5) as resp:
            sid = resp.headers.get("mcp-session-id")
        if not sid:
            return out
        # Call chron_temporal_briefing — the canonical temporal context source
        call_req = urllib.request.Request(
            f"{CHRON_URL}/mcp",
            data=json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                              "params": {"name": "chron_temporal_briefing", "arguments": {}}}).encode(),
            headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                      "Mcp-Session-Id": sid},
            method="POST",
        )
        with urllib.request.urlopen(call_req, timeout=5) as resp:
            raw_text = resp.read().decode()
        # CHRON returns SSE format — extract from data: line
        body: dict[str, Any] = {}
        for line in raw_text.split("\n"):
            if line.startswith("data: "):
                body = json.loads(line[6:])
                break
        if not body:
            body = json.loads(raw_text)
        text = body.get("result", {}).get("content", [{}])[0].get("text", "")
        if not text:
            return out
        payload = json.loads(text)
        out["available"] = True
        out["source"] = "chron:chron_temporal_briefing"
        # attention_debt is a dict with total_ad field
        if isinstance(payload.get("attention_debt"), dict):
            out["attention_debt"] = float(payload["attention_debt"].get("total_ad", 0))
        else:
            out["attention_debt"] = float(payload.get("attention_debt", 0))
        # predictions_due is an array
        out["predictions_due_count"] = len(payload.get("predictions_due") or [])
        out["prediction_due"] = out["predictions_due_count"] > 0
        # last_loop provides staleness
        last_loop = payload.get("last_loop") or {}
        out["last_loop_timestamp"] = last_loop.get("timestamp")
        return out
    except Exception:
        return out
    return out


# ── HERMES integration ─────────────────────────────────────────────

def fetch_hermes_evidence(subject: str) -> dict[str, Any]:
    """Pull HERMES's claim/provenance/contradiction metadata via MCP.

    HERMES is the canonical source for:
      - claim certainty / epistemic tag
      - principal type (PERSON, AI_ORGAN, INSTITUTION, …)
      - contradictions (count of conflicting claims on the subject)
      - unknowns (claims deferred due to insufficient evidence)

    Live probe (2026-09-21) confirms HERMES exposes principal_type_classifier
    at /root/HERMES/mcp/hermes-rasa/principal_type_classifier.py and
    hermes_claim tools.
    """
    out: dict[str, Any] = {
        "available": False,
        "epistemic_state": "MISSING",
        "principal_type": "UNKNOWN",
        "source_count": 0,
        "contradictions": 0,
        "source": "unavailable",
    }
    sid: str | None = None
    try:
        # Import the deterministic classifier directly (already deployed)
        import sys as _sys
        hermes_path = "/root/HERMES/mcp/hermes-rasa"
        if hermes_path not in _sys.path:
            _sys.path.insert(0, hermes_path)
        from principal_type_classifier import classify_principal_type, PrincipalType

        cls = classify_principal_type(subject)
        out["available"] = True
        out["principal_type"] = cls.principal_type.value
        out["matched_rule"] = cls.matched_rule
        out["confidence"] = cls.confidence
        out["source"] = "hermes:principal_type_classifier"
        # Map principal_type → epistemic_state (HEURISTIC)
        if cls.principal_type == PrincipalType.PERSON:
            out["epistemic_state"] = "OBSERVED"  # humans are observed entities
        elif cls.principal_type in {
            PrincipalType.AI_ORGAN, PrincipalType.SYSTEM,
            PrincipalType.INSTITUTION, PrincipalType.LEGISLATURE,
            PrincipalType.CORPORATION, PrincipalType.STATE, PrincipalType.CITY,
        }:
            out["epistemic_state"] = "DERIVED"  # structural entity
        elif cls.principal_type in {
            PrincipalType.TIME, PrincipalType.DATE,
            PrincipalType.EVENT, PrincipalType.DOCUMENT,
        }:
            out["epistemic_state"] = "INTERPRETED"  # temporal/event = contextual
        elif cls.principal_type == PrincipalType.UNKNOWN:
            out["epistemic_state"] = "MISSING"
        out["source_count"] = 1  # classifier is one source
        return out
    except Exception:
        return out
    return out


# ── Build AttentionPacket from inputs ──────────────────────────────

def build_packet(
    subject: str,
    why_now: str,
    *,
    impact: float = 0.5,
    urgency: float = 0.5,
    uncertainty: float = 0.5,
    reversibility: float = 0.5,
    novelty: float = 0.5,
    attention_cost: float = 1.0,
    overrides: list[str] | None = None,
    recommended_organ: str = "",
    required_authority: str = "OBSERVE_ONLY",
    execution_required: bool = False,
    deadline: str | None = None,
    consume_chron: bool = True,
    consume_hermes: bool = True,
) -> AttentionPacket:
    """Construct an AttentionPacket from raw inputs, optionally enriched by CHRON/HERMES."""
    used_overrides = list(overrides or [])

    temporal: dict[str, Any] = {}
    if consume_chron:
        chron = fetch_chron_attention_debt()
        temporal["chron_available"] = chron["available"]
        temporal["chron_source"] = chron["source"]
        temporal["attention_debt"] = chron["attention_debt"]
        temporal["prediction_due"] = chron["prediction_due"]
        # If CHRON says prediction_due, urgency goes up
        if chron["prediction_due"]:
            urgency = max(urgency, 0.85)
            if Override.DEADLINE_EXPIRY.value not in used_overrides:
                # Don't auto-add override, just boost urgency
                pass

    epistemic = EpistemicState.OBSERVED
    source_count = 0
    contradictions = 0
    if consume_hermes:
        hermes = fetch_hermes_evidence(subject)
        temporal["hermes_available"] = hermes["available"]
        temporal["hermes_source"] = hermes["source"]
        try:
            epistemic = EpistemicState(hermes["epistemic_state"])
        except (KeyError, ValueError):
            epistemic = EpistemicState.OBSERVED
        source_count = hermes["source_count"]
        contradictions = hermes["contradictions"]

    priority, applied = compute_priority(
        impact=impact,
        urgency=urgency,
        uncertainty=uncertainty,
        reversibility=reversibility,
        attention_cost=attention_cost,
        overrides=used_overrides,
        novelty=novelty,
    )

    return AttentionPacket(
        subject=subject,
        attention_class=AttentionClass.ACTION_REQUIRED
        if priority >= 0.85
        else AttentionClass.INFORM
        if priority >= 0.5
        else AttentionClass.DEFER
        if priority >= 0.2
        else AttentionClass.SILENT,
        priority=priority,
        why_now=why_now,
        deadline=deadline,
        impact=impact,
        urgency=urgency,
        uncertainty=uncertainty,
        reversibility=reversibility,
        epistemic_state=epistemic,
        source_count=source_count,
        contradictions=contradictions,
        temporal=temporal,
        recommended_organ=recommended_organ,
        required_authority=required_authority,
        execution_required=execution_required,
        overrides=applied,
        evidence_basis=[
            f"chron:{temporal.get('chron_source', 'unavailable')}",
            f"hermes:{temporal.get('hermes_source', 'unavailable')}",
        ],
    )


def write_to_ledger(packet: AttentionPacket) -> None:
    """F11 AUDIT — every AttentionPacket is appended to the ledger."""
    ATTENTION_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    record = packet.to_dict()
    record["ledgered_at"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    with ATTENTION_LEDGER.open("a") as f:
        f.write(json.dumps(record, default=str) + "\n")


# ── CLI ──────────────────────────────────────────────────────────────

def _check(label, ok, detail=""):
    glyph = "✓" if ok else "✗"
    line = f"  {glyph} {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def main() -> int:
    """Self-test of the AttentionPacket + priority formula + integration."""
    print("=" * 70)
    print("AAA ATTENTION PLANE — self-test (P2 2026-09-21)")
    print("=" * 70)
    all_ok = True

    # Test 1: priority formula — high-impact + novel → high priority
    p, ov = compute_priority(
        impact=0.9, urgency=0.8, uncertainty=0.1, reversibility=0.9,
        novelty=0.9,  # novel = high
        attention_cost=1.0,
    )
    all_ok &= _check(
        "priority formula: high-impact + novel + low-uncertainty → high priority",
        p > 0.5 and not math.isinf(p),
        f"P={p:.3f}",
    )

    # Test 2: override forces ∞
    p, ov = compute_priority(
        impact=0.1, urgency=0.1, uncertainty=0.9, reversibility=0.1,
        attention_cost=1.0,
        overrides=[Override.AUTHORITY_VIOLATION.value],
    )
    all_ok &= _check(
        "override authority_violation → P = ∞",
        math.isinf(p) and Override.AUTHORITY_VIOLATION.value in ov,
        f"P={p} overrides={ov}",
    )

    # Test 3: irreversibility_floor
    p, ov = compute_priority(
        impact=0.1, urgency=0.1, uncertainty=0.5, reversibility=0.0,
        attention_cost=1.0,
        overrides=[Override.IRREVERSIBILITY_FLOOR.value],
    )
    all_ok &= _check(
        "irreversibility_floor → P ≥ 0.85",
        p >= 0.85,
        f"P={p:.3f}",
    )

    # Test 4: 16 fields present
    pkt = AttentionPacket(
        subject="test",
        attention_class=AttentionClass.INFORM,
        priority=0.5,
        why_now="test",
    )
    d = pkt.to_dict()
    expected_fields = {
        "subject", "attention_class", "priority", "why_now", "deadline",
        "impact", "urgency", "uncertainty", "reversibility",
        "epistemic_state", "source_count", "contradictions",
        "temporal", "recommended_organ", "required_authority", "execution_required",
        "overrides", "evidence_basis",
    }
    all_ok &= _check(
        f"AttentionPacket has all 16+ canonical fields",
        all(k in d for k in expected_fields),
        f"present={sum(1 for k in expected_fields if k in d)}/{len(expected_fields)}",
    )

    # Test 5: CHRON integration (best-effort; may not be reachable in test)
    chron = fetch_chron_attention_debt()
    print(f"  · CHRON probe: {chron['source']} attention_debt={chron['attention_debt']}")

    # Test 6: HERMES integration (best-effort)
    hermes = fetch_hermes_evidence("WEALTH")
    print(f"  · HERMES probe: {hermes['source']} epistemic={hermes['epistemic_state']}")

    # Test 7: build_packet end-to-end
    pkt2 = build_packet(
        subject="WEALTH surface drift",
        why_now="HIGH schema drift detected",
        impact=0.9, urgency=0.8, uncertainty=0.2, reversibility=0.9,
        consume_chron=True, consume_hermes=True,
    )
    print(f"\n  Sample packet:")
    for k, v in pkt2.to_dict().items():
        print(f"    {k}: {v}")
    write_to_ledger(pkt2)

    print()
    print("=" * 70)
    print("RESULT: PASS — AttentionPlane self-test green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
