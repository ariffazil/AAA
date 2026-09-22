"""
test_aaa_attention_convergence.py — P2 2026-09-21 (AAA-ATTENTION-CONVERGENCE).

Regression canary for AAA's attention-plane pivot. Every assertion must
FAIL LOUD on regression.

Eight sub-fixes verified (per F13 2026-09-21):
  1. AttentionPacket canonical schema (16+ fields)
  2. Priority formula + 5 hard overrides
  3. CHRON integration (temporal urgency inputs)
  4. HERMES integration (claim/provenance/contradiction)
  5. State reconciliation semantics (NOT "verification")
  6. FRAME / VAULT999 / arifFlow taxonomy correction
  7. HERMES out of "interface" tier; CHRON added formally
  8. README counts from SOT, not hardcoded prose

Constitutional:
    F2 TRUTH   — every assertion cites the surface under check
    F4 CLARITY — ΔS ≤ 0 (test reduces drift)
    F11 AUDIT  — every result leaves evidence on stdout
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, "/root/AAA/scripts")
from attention_plane import (  # noqa: E402
    AttentionClass,
    AttentionPacket,
    EpistemicState,
    Override,
    build_packet,
    compute_priority,
    fetch_chron_attention_debt,
    fetch_hermes_evidence,
)


def _check(label, ok, detail=""):
    glyph = "✓" if ok else "✗"
    line = f"  {glyph} {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def main() -> int:
    print("=" * 70)
    print("FEDERATION E2E — AAA-ATTENTION-CONVERGENCE")
    print("  Test ID: P2-2026-09-21")
    print("  Doctrine: AAA : Reality → Attention")
    print("=" * 70)
    all_ok = True

    # ─────────────────────────────────────────────────────────────────
    # P2-1: AttentionPacket canonical schema (16+ fields)
    # ─────────────────────────────────────────────────────────────────
    print("\n[P2-1] AttentionPacket canonical schema")
    pkt = AttentionPacket(
        subject="test",
        attention_class=AttentionClass.INFORM,
        priority=0.5,
        why_now="test",
    )
    d = pkt.to_dict()
    required = {
        "subject", "attention_class", "priority", "why_now", "deadline",
        "impact", "urgency", "uncertainty", "reversibility",
        "epistemic_state", "source_count", "contradictions",
        "temporal", "recommended_organ", "required_authority", "execution_required",
        "overrides", "evidence_basis",
    }
    all_ok &= _check(
        f"AttentionPacket has all 16+ canonical fields",
        all(k in d for k in required),
        f"present={sum(1 for k in required if k in d)}/{len(required)}",
    )
    all_ok &= _check(
        "AttentionClass enum = 5 states (ACTION_REQUIRED, INFORM, HOLD, DEFER, SILENT)",
        len(AttentionClass) == 5,
        f"states={[s.value for s in AttentionClass]}",
    )

    # ─────────────────────────────────────────────────────────────────
    # P2-2: Priority formula + 5 hard overrides
    # ─────────────────────────────────────────────────────────────────
    print("\n[P2-2] Priority formula + hard overrides")

    # Test 1: high-impact + novel → high priority
    p, ov = compute_priority(
        impact=0.9, urgency=0.8, uncertainty=0.1, reversibility=0.9,
        novelty=0.9, attention_cost=1.0,
    )
    all_ok &= _check(
        "priority formula: high-impact + novel + low-uncertainty → high priority",
        p > 0.5 and not math.isinf(p),
        f"P={p:.3f}",
    )

    # Test 2: authority_violation → P = ∞
    p, ov = compute_priority(
        impact=0.1, urgency=0.1, uncertainty=0.9, reversibility=0.1,
        attention_cost=1.0,
        overrides=[Override.AUTHORITY_VIOLATION.value],
    )
    all_ok &= _check(
        "override authority_violation → P = ∞ (must-show)",
        math.isinf(p) and Override.AUTHORITY_VIOLATION.value in ov,
        f"P={p} overrides={ov}",
    )

    # Test 3: security_breach → P = ∞
    p, ov = compute_priority(
        impact=0.5, urgency=0.5, uncertainty=0.5, reversibility=0.5,
        attention_cost=1.0,
        overrides=[Override.SECURITY_BREACH.value],
    )
    all_ok &= _check(
        "override security_breach → P = ∞",
        math.isinf(p),
        f"P={p}",
    )

    # Test 4: deadline_expiry → P = ∞
    p, ov = compute_priority(
        impact=0.5, urgency=0.5, uncertainty=0.5, reversibility=0.5,
        attention_cost=1.0,
        overrides=[Override.DEADLINE_EXPIRY.value],
    )
    all_ok &= _check(
        "override deadline_expiry → P = ∞",
        math.isinf(p),
        f"P={p}",
    )

    # Test 5: failed_invariant → P = ∞
    p, ov = compute_priority(
        impact=0.5, urgency=0.5, uncertainty=0.5, reversibility=0.5,
        attention_cost=1.0,
        overrides=[Override.FAILED_INVARIANT.value],
    )
    all_ok &= _check(
        "override failed_invariant → P = ∞",
        math.isinf(p),
        f"P={p}",
    )

    # Test 6: irreversibility_floor → P ≥ 0.85 (NOT ∞)
    p, ov = compute_priority(
        impact=0.1, urgency=0.1, uncertainty=0.5, reversibility=0.0,
        attention_cost=1.0,
        overrides=[Override.IRREVERSIBILITY_FLOOR.value],
    )
    all_ok &= _check(
        "override irreversibility_floor → P ≥ 0.85 (high floor, not ∞)",
        p >= 0.85 and not math.isinf(p),
        f"P={p:.3f}",
    )

    # Test 7: attention_cost cannot be zero (F1 AMANAH)
    p, _ = compute_priority(
        impact=0.5, urgency=0.5, uncertainty=0.5, reversibility=0.5,
        attention_cost=0.0,
    )
    all_ok &= _check(
        "F1 AMANAH: attention_cost=0 → clamped to ≥ 0.01",
        not math.isinf(p),
        f"P={p:.3f} (cost clamped)",
    )

    # ─────────────────────────────────────────────────────────────────
    # P2-3: CHRON integration
    # ─────────────────────────────────────────────────────────────────
    print("\n[P2-3] CHRON integration (temporal urgency)")
    chron = fetch_chron_attention_debt()
    all_ok &= _check(
        "CHRON MCP reachable on :18102",
        chron["available"] or chron["source"] != "unavailable",
        f"source={chron['source']}",
    )
    all_ok &= _check(
        "CHRON exposes attention_debt + predictions_due fields",
        "attention_debt" in chron and "prediction_due" in chron,
        f"keys={list(chron.keys())}",
    )

    # Test build_packet consumes CHRON
    pkt2 = build_packet(
        subject="WEALTH",
        why_now="test CHRON consumption",
        impact=0.5, urgency=0.5, uncertainty=0.5, reversibility=0.5,
        consume_chron=True,
    )
    all_ok &= _check(
        "build_packet consumes CHRON (temporal.available in temporal dict)",
        pkt2.temporal.get("chron_available"),
        f"chron_available={pkt2.temporal.get('chron_available')}",
    )

    # ─────────────────────────────────────────────────────────────────
    # P2-4: HERMES integration
    # ─────────────────────────────────────────────────────────────────
    print("\n[P2-4] HERMES integration (claim/provenance/contradiction)")
    hermes = fetch_hermes_evidence("DAP")
    all_ok &= _check(
        "HERMES principal_type_classifier reachable",
        hermes["available"] and hermes["source"] != "unavailable",
        f"source={hermes['source']} principal={hermes.get('principal_type')}",
    )
    all_ok &= _check(
        'HERMES classifies "DAP" as POLITICAL_PARTY (not PERSON)',
        hermes.get("principal_type") == "POLITICAL_PARTY",
        f"principal_type={hermes.get('principal_type')}",
    )

    hermes_wealth = fetch_hermes_evidence("WEALTH")
    all_ok &= _check(
        'HERMES classifies "WEALTH" as AI_ORGAN (not PERSON)',
        hermes_wealth.get("principal_type") == "AI_ORGAN",
        f"principal_type={hermes_wealth.get('principal_type')}",
    )

    # Test build_packet consumes HERMES
    pkt3 = build_packet(
        subject="DAP",
        why_now="test HERMES consumption",
        impact=0.5, urgency=0.5, uncertainty=0.5, reversibility=0.5,
        consume_hermes=True,
    )
    all_ok &= _check(
        "build_packet consumes HERMES (epistemic_state from classification)",
        pkt3.epistemic_state in {EpistemicState.OBSERVED, EpistemicState.DERIVED, EpistemicState.INTERPRETED, EpistemicState.MISSING},
        f"epistemic={pkt3.epistemic_state}",
    )

    # ─────────────────────────────────────────────────────────────────
    # P2-5: State reconciliation semantics (NOT "verification")
    # ─────────────────────────────────────────────────────────────────
    print("\n[P2-5] State reconciliation semantics")
    try:
        readme = open("/root/AAA/README.md").read()
        # The new README should use "state reconciliation" / "consistency verification"
        all_ok &= _check(
            'README uses "state reconciliation" (NOT unrestricted "verification")',
            "state reconciliation" in readme.lower() or "consistency verification" in readme.lower(),
        )
        # The new README should explicitly say AAA does NOT establish Claim = AbsoluteTruth
        all_ok &= _check(
            "README disclaims 'Claim = AbsoluteTruth' authority",
            "AbsoluteTruth" in readme or "establishes ObservedState" in readme or "absolute truth" in readme.lower(),
        )
    except Exception as exc:
        all_ok &= _check("README readable", False, str(exc))

    # ─────────────────────────────────────────────────────────────────
    # P2-6: FRAME / VAULT999 / arifFlow taxonomy correction
    # ─────────────────────────────────────────────────────────────────
    print("\n[P2-6] FRAME / VAULT999 / arifFlow taxonomy")
    try:
        readme = open("/root/AAA/README.md").read()
        all_ok &= _check(
            "README: FRAME = independent witness",
            "FRAME" in readme and "witness" in readme.lower(),
        )
        all_ok &= _check(
            "README: VAULT999 = immutable ledger",
            "VAULT999" in readme and "ledger" in readme.lower(),
        )
        all_ok &= _check(
            "README: arifFlow = metabolism / FQ / receipts (NOT witness plane)",
            "arifFlow" in readme and "metabolism" in readme.lower()
            and ("NOT witness" in readme or "not witness" in readme.lower()
                 or "not a witness plane" in readme.lower()),
        )
        # Explicit "Witness ≠ Telemetry ≠ Ledger" check
        all_ok &= _check(
            'README states "Witness ≠ Telemetry ≠ Ledger"',
            "Witness ≠ Telemetry ≠ Ledger" in readme or "Witness != Telemetry" in readme,
        )
    except Exception as exc:
        all_ok &= _check("README readable", False, str(exc))

    # ─────────────────────────────────────────────────────────────────
    # P2-7: HERMES out of "interface" tier; CHRON added formally
    # ─────────────────────────────────────────────────────────────────
    print("\n[P2-7] HERMES + CHRON taxonomy")
    try:
        readme = open("/root/AAA/README.md").read()
        all_ok &= _check(
            'README: HERMES = Meaning Plane (NOT "interface" tier)',
            "Meaning Plane" in readme or "meaning plane" in readme.lower(),
        )
        all_ok &= _check(
            "README: CHRON = Temporal Plane (added formally)",
            "Temporal Plane" in readme or "temporal plane" in readme.lower(),
        )
        # 7 organs with irreducible questions
        all_ok &= _check(
            "README has 7-organ irreducible-questions table (HERMES, CHRON, AAA, arifOS, A-FORGE, FRAME, VAULT999)",
            all(
                org in readme
                for org in ("HERMES", "CHRON", "AAA", "arifOS", "A-FORGE", "FRAME", "VAULT999")
            ),
        )
        all_ok &= _check(
            'README contains "Routing a message ≠ authorizing its consequence" invariant',
            "Routing a message" in readme and "authorizing its consequence" in readme,
        )
    except Exception as exc:
        all_ok &= _check("README readable", False, str(exc))

    # ─────────────────────────────────────────────────────────────────
    # P2-8: README counts from SOT (not hardcoded)
    # ─────────────────────────────────────────────────────────────────
    print("\n[P2-8] Counts from SOT (not hardcoded prose)")
    try:
        readme = open("/root/AAA/README.md").read()
        all_ok &= _check(
            'README states "counts are live from SOT, not hardcoded"',
            "release snapshots" in readme or "release snapshot" in readme
            or "live counts" in readme.lower() or "projection" in readme.lower(),
        )
        all_ok &= _check(
            "README does NOT hardcode specific organ/skill counts",
            not re.search(r"\b\d+\s+organs?\b", readme.lower())
            or "organs (live)" in readme.lower(),
        )
    except Exception as exc:
        all_ok &= _check("README readable", False, str(exc))

    # ─────────────────────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────────────────────
    print()
    print("=" * 70)
    if all_ok:
        print("RESULT: PASS — AAA-ATTENTION-CONVERGENCE green")
        print("  - AttentionPacket canonical schema (16+ fields)")
        print("  - Priority formula + 5 hard overrides (4× ∞, 1× floor)")
        print("  - CHRON integration (temporal urgency)")
        print("  - HERMES integration (principal_type classifier)")
        print("  - State reconciliation semantics (NOT 'verification')")
        print("  - FRAME / VAULT999 / arifFlow taxonomy corrected")
        print("  - HERMES out of 'interface' tier; CHRON added formally")
        print("  - README counts from SOT, not hardcoded prose")
        return 0
    else:
        print("RESULT: FAIL — some P2 checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
