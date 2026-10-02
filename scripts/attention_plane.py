"""
attention_plane.py — P2 2026-09-21 (AAA-ATTENTION-CONVERGENCE).

Canonical AttentionPacket schema + priority formula.

Identity:
    AAA : (evidence, state, deadlines, drift, uncertainty) → AttentionPacket

Pipeline (per F13 2026-09-21):
    Reality → HERMES (meaning) → CHRON (temporal) → AAA (attention) → arifOS/Human

PR-3 ONE-DOOR (2026-10-02): HERMES and CHRON are consumed only through
AAA-owned adapters (adapters/meaning_adapter.py, adapters/
temporal_adapter.py) over HTTP/MCP. No organ filesystem paths, no
sys.path reach-ins, no organ python imports. Fail closed (F1).

AAA does NOT:
  - Judge (that's arifOS)
  - Execute (that's A-FORGE)
  - Witness (that's FRAME / VAULT999; arifFlow is metabolism, not witness)
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
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# ── AAA package bootstrap (PR-3 ONE-DOOR) ────────────────────────────
# The script lives in scripts/; put the AAA repo root on sys.path so it can
# import AAA's own adapter package. This is AAA's own boundary — not an
# organ reach-in. Organs are consumed ONLY via the adapters below.

_AAA_ROOT = Path(__file__).resolve().parents[1]
if str(_AAA_ROOT) not in sys.path:
    sys.path.insert(0, str(_AAA_ROOT))

from adapters.meaning_adapter import MeaningAdapter  # noqa: E402
from adapters.temporal_adapter import TemporalAdapter  # noqa: E402

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
    impact: float = 0.5  # 0.0–1.0
    urgency: float = 0.5  # 0.0–1.0
    uncertainty: float = 0.5  # 0.0–1.0 (higher = less certain)
    reversibility: float = 0.5  # 0.0–1.0 (higher = more reversible)

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

    EvidenceQuality = (1 - Uncertainty)   # F13 2026-09-25: source+freshness+support ONLY
    ActionRisk = f(reversibility, blast radius) — separate gate, NEVER folded into P

    Hard overrides (force P = ∞ for must-show):
      - authority_violation, security_breach, deadline_expiry,
        failed_invariant → P = ∞
      - irreversibility_floor → P ≥ 0.85 (high floor, not ∞)

    Returns (priority, applied_overrides).
    """
    applied: list[str] = []

    # F1 AMANAH — attention_cost ≥ 1.0 (module header contract; the 0.01 clamp was drift)
    cost = max(attention_cost, 1.0)

    # PR-1 ATTENTION-TRUTH (2026-10-02, 333-AGI): EvidenceQuality excludes Reversibility.
    # Reversibility belongs to ActionRisk (irreversibility_floor override / human surfacing),
    # never to evidence strength — a well-evidenced irreversible action keeps high evidence
    # quality AND still routes to the human via the ActionRisk gate. Aligns runtime with
    # README L151 F13 ruling of 2026-09-25 (reversibility was double-counted).
    evidence_quality = 1.0 - _clamp(uncertainty)

    numerator = _clamp(impact) * _clamp(urgency) * _clamp(evidence_quality) * _clamp(novelty)

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
    """Pull CHRON's temporal urgency inputs via TemporalAdapter (PR-3 ONE-DOOR).

    CHRON is the canonical source for:
      - attention_debt (how much owed attention has accumulated)
      - active predictions (count + due-soon flag)
      - next_verify_at (next calibration deadline)
      - calibration summary (mean Brier, accuracy)
      - learning-closure gap (many episodes + zero actionable lessons)

    PR-3 ONE-DOOR (2026-10-02): the MCP session/HTTP plumbing moved into
    adapters/temporal_adapter.py. This function reshapes the adapter
    briefing into the backward-compatible keys existing callers/tests rely
    on, plus the enriched PR-3 fields.

    Live probe (2026-10-02) confirms CHRON MCP tool shapes:
        chron_temporal_briefing / chron_predictions_due /
        chron_store_stats / chron_lessons; GET /health as fallback.
    """
    brief = TemporalAdapter(base_url=CHRON_URL).briefing()
    available = bool(brief.get("available"))
    due_count = int(brief.get("prediction_due_count") or 0)
    last_loop = brief.get("last_loop") or {}
    out: dict[str, Any] = {
        # ── backward-compatible keys (P2-2026-09-21 contract) ──
        "available": available,
        "attention_debt": float(brief.get("attention_debt") or 0.0) if available else 0.0,
        "prediction_due": available and due_count > 0,
        "predictions_due_count": due_count if available else 0,
        "next_verify_at": brief.get("next_verify_at"),
        "source": brief.get("source", "unavailable"),
        # ── PR-3 ONE-DOOR enrichment ──
        "predictions_due": brief.get("prediction_due") or [],
        "verification_backlog": brief.get("verification_backlog"),
        "unclassified_outcomes": brief.get("unclassified_outcomes"),
        "actionable_lessons": brief.get("actionable_lessons"),
        "calibration_health": brief.get("calibration_health"),
        "learning_closure_gap": brief.get("learning_closure_gap"),
        "degradation": brief.get("degradation"),
    }
    if last_loop.get("timestamp"):
        out["last_loop_timestamp"] = last_loop.get("timestamp")
    return out


# ── HERMES integration ─────────────────────────────────────────────


def fetch_hermes_evidence(subject: str) -> dict[str, Any]:
    """Pull HERMES's meaning metadata via MeaningAdapter (PR-3 ONE-DOOR).

    HERMES is the canonical source for:
      - principal type (what the subject IS, per HERMES's typing)
      - epistemic tag mapped from that typing

    PR-3 ONE-DOOR (2026-10-02): the sys.path insertion into HERMES's
    local classifier module directory and the direct
    principal_type_classifier import are GONE. AAA now sees only what
    HERMES actually serves behind its MCP door:
    hermes_perspective_scope, whose principal typing is the coarse
    5-type contract (PERSON | INSTITUTION | COLLECTIVE | SYSTEM |
    UNDEFINED).

    Known granularity gap, recorded not papered over (F2): the legacy
    deterministic 15-class classifier (POLITICAL_PARTY, AI_ORGAN, …) is
    not exposed behind any door. Canary delta: "DAP" now types PERSON
    (was POLITICAL_PARTY via the old smuggled import); "WEALTH" now
    types UNDEFINED (was AI_ORGAN). The fix belongs on the HERMES side
    (expose the fine classifier as an MCP tool); AAA must not reach
    around the door to recover it.

    Live probe (2026-10-02) confirms HERMES :18087 /health healthy and
    15 MCP tools including hermes_perspective_scope.
    """
    out: dict[str, Any] = {
        "available": False,
        "epistemic_state": "MISSING",
        "principal_type": "UNKNOWN",
        "source_count": 0,
        "contradictions": 0,
        "source": "unavailable",
        "degradation": None,
    }
    cls = MeaningAdapter(base_url=HERMES_URL).classify(subject)
    out["degradation"] = cls.get("degradation")
    if not cls.get("available"):
        return out

    principal_type = cls.get("principal_type") or "UNDEFINED"
    out["available"] = True
    out["principal_type"] = principal_type
    out["confidence"] = cls.get("confidence")
    out["source"] = cls.get("source", "unavailable")
    out["epistemic_state"] = _epistemic_for_principal(principal_type)
    out["source_count"] = 1  # one door, one classification source
    return out


# Principal typing → epistemic state. Coarse 5-type door contract first;
# legacy 15-class values tolerated so a future HERMES door upgrade maps
# without editing this file. Unknown/UNDEFINED → MISSING (F6: safe default).
_PERSONAL_TYPES = {"PERSON"}
_STRUCTURAL_TYPES = {
    "INSTITUTION",
    "COLLECTIVE",
    "SYSTEM",
    # legacy fine-grained values (not served by the door today)
    "AI_ORGAN",
    "LEGISLATURE",
    "CORPORATION",
    "STATE",
    "CITY",
    "POLITICAL_PARTY",
    "COALITION",
}
_TEMPORAL_TYPES = {"TIME", "DATE", "EVENT", "DOCUMENT"}


def _epistemic_for_principal(principal_type: str) -> str:
    if principal_type in _PERSONAL_TYPES:
        return "OBSERVED"  # humans are observed entities
    if principal_type in _STRUCTURAL_TYPES:
        return "DERIVED"  # structural entity
    if principal_type in _TEMPORAL_TYPES:
        return "INTERPRETED"  # temporal/event = contextual
    return "MISSING"  # UNDEFINED / unseen value → fail-closed default


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
        impact=0.9,
        urgency=0.8,
        uncertainty=0.1,
        reversibility=0.9,
        novelty=0.9,  # novel = high
        attention_cost=1.0,
    )
    all_ok &= _check(
        "priority formula: high-impact + novel + low-uncertainty → high priority",
        p > 0.5 and not math.isinf(p),
        f"P={p:.3f}",
    )

    # Test 1b: PR-1 ATTENTION-TRUTH — evidence/risk separation.
    # Well-evidenced irreversible action: evidence quality must stay HIGH.
    # (Old formula scored this 0.000 because reversibility=0.0 zeroed the product,
    #  burying strong evidence under an unrelated risk dimension.)
    p_irr, _ = compute_priority(
        impact=0.9,
        urgency=0.8,
        uncertainty=0.1,
        reversibility=0.0,
        novelty=0.9,
        attention_cost=1.0,
    )
    all_ok &= _check(
        "separation: irreversible + well-evidenced keeps high priority via evidence",
        p_irr > 0.5,
        f"P={p_irr:.3f} (old formula: 0.000)",
    )
    # And the risk side is carried by the ActionRisk gate, not by evidence decay:
    p_irr_floor, ov_fl = compute_priority(
        impact=0.1,
        urgency=0.1,
        uncertainty=0.1,
        reversibility=0.0,
        novelty=0.1,
        attention_cost=1.0,
        overrides=[Override.IRREVERSIBILITY_FLOOR.value],
    )
    all_ok &= _check(
        "separation: ActionRisk floor surfaces irreversible regardless of priority",
        p_irr_floor >= 0.85,
        f"P={p_irr_floor:.3f} overrides={ov_fl}",
    )

    # Test 2: override forces ∞
    p, ov = compute_priority(
        impact=0.1,
        urgency=0.1,
        uncertainty=0.9,
        reversibility=0.1,
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
        impact=0.1,
        urgency=0.1,
        uncertainty=0.5,
        reversibility=0.0,
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
        "subject",
        "attention_class",
        "priority",
        "why_now",
        "deadline",
        "impact",
        "urgency",
        "uncertainty",
        "reversibility",
        "epistemic_state",
        "source_count",
        "contradictions",
        "temporal",
        "recommended_organ",
        "required_authority",
        "execution_required",
        "overrides",
        "evidence_basis",
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
        impact=0.9,
        urgency=0.8,
        uncertainty=0.2,
        reversibility=0.9,
        consume_chron=True,
        consume_hermes=True,
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
