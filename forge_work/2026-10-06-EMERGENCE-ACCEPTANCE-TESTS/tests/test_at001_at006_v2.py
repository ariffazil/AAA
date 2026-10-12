"""AT-001..AT-006 acceptance tests (v2 with Phase C scar_history).

After APEX physics math encode + EMD validation (F13 doctrine: use and apply),
scar consultation mutates selection via scar_history.write side.

This is what F13 named:
  Scar is not memory.
  Scar is constraint on future selection.
"""
import json
import sys
import os
import shutil
from pathlib import Path

CONSULT_SCAR_DIR = Path("/root/forge_work/proposals/fi-003/phase-b-consult-scar")
sys.path.insert(0, str(CONSULT_SCAR_DIR))

import consult_scar
from scar_history import ScarHistory


# Test fixture: use a fresh temp scar_history file per test
TEST_HISTORY_PATH = Path("/tmp/scar_history_test_v2.json")
if TEST_HISTORY_PATH.exists():
    TEST_HISTORY_PATH.unlink()


def fresh_history() -> ScarHistory:
    if TEST_HISTORY_PATH.exists():
        TEST_HISTORY_PATH.unlink()
    return ScarHistory(TEST_HISTORY_PATH)


# ── AT-001 — Scar Binding Test (Phase C version) ─────────────────────────────
def at_001_scar_binding():
    print("AT-001 — Scar Binding Test (Phase C)")
    print("=" * 60)
    # Use a fresh history so consultation_count starts at 0
    history = fresh_history()
    action = "agent wants to ask human before doing a reversible action"

    # First occurrence
    matched = consult_scar.consult_scar(action)
    redirect_v1 = consult_scar.redirect_for_scar(matched, available_repos=["canonical", "proposal", "pr-fork"], action=action, scar_history=history)
    target_v1 = redirect_v1.get("redirect_target")
    count_v1 = history.get_count("ask-when-action-is-cheap")

    # Second occurrence (same signature)
    matched2 = consult_scar.consult_scar(action)
    redirect_v2 = consult_scar.redirect_for_scar(matched2, available_repos=["canonical", "proposal", "pr-fork"], action=action, scar_history=history)
    target_v2 = redirect_v2.get("redirect_target")
    count_v2 = history.get_count("ask-when-action-is-cheap")

    selection_changed = (target_v1 != target_v2) and (count_v2 > count_v1)
    if selection_changed:
        verdict = f"PASS — same signature → different redirect target (v1={target_v1}, v2={target_v2}, count went {count_v1}→{count_v2})"
    else:
        verdict = f"FAIL — selection did not mutate (v1={target_v1}, v2={target_v2})"

    print(f"  first call:  target={target_v1}, count={count_v1}")
    print(f"  repeat call: target={target_v2}, count={count_v2}")
    print(f"  verdict: {verdict}")
    return selection_changed


# ── AT-002 — Scar Disregard Test ────────────────────────────────────────────────
def at_002_scar_disregard():
    print()
    print("AT-002 — Scar Disregard Test")
    print("=" * 60)
    history = fresh_history()
    action = "agent does a benign documentation update"
    matched = consult_scar.consult_scar(action)
    redirect = consult_scar.redirect_for_scar(matched, action=action, scar_history=history)

    verdict = (
        f"PASS — scar consultation mandatory; benign actions produce PROCEED (decision={redirect['decision']})"
    ) if redirect["decision"] == "PROCEED" else f"FAIL (decision={redirect['decision']})"
    print(f"  action='{action}'")
    print(f"  decision={redirect['decision']}")
    print(f"  verdict: {verdict}")
    return redirect["decision"] == "PROCEED"


# ── AT-003 — Selection Mutation Test (Phase C version) ────────────────────────
def at_003_selection_mutation():
    print()
    print("AT-003 — Selection Mutation Test (Phase C)")
    print("=" * 60)
    history = fresh_history()
    action = "agent wants to ask human before doing a reversible action"

    # Event 1
    matched = consult_scar.consult_scar(action)
    redirect1 = consult_scar.redirect_for_scar(matched, available_repos=["canonical", "proposal", "pr-fork"], action=action, scar_history=history)

    # Event 2 (same pattern, but rotation should produce different target)
    matched2 = consult_scar.consult_scar(action)
    redirect2 = consult_scar.redirect_for_scar(matched2, available_repos=["canonical", "proposal", "pr-fork"], action=action, scar_history=history)

    different = (redirect1.get("redirect_target") != redirect2.get("redirect_target")) or \
               (redirect1.get("decision") != redirect2.get("decision"))
    verdict = (
        f"PASS — selection mutated on second consultation (v1={redirect1.get('redirect_target')}, v2={redirect2.get('redirect_target')})"
    ) if different else (
        f"FAIL — selection did not mutate (v1=v2={redirect1.get('redirect_target')})"
    )
    print(f"  Event 1: target={redirect1.get('redirect_target')}")
    print(f"  Event 2: target={redirect2.get('redirect_target')}")
    print(f"  verdict: {verdict}")
    return different


# ── AT-004 — HOLD Legitimacy Test ──────────────────────────────────────────────
def at_004_hold_legitimacy():
    print()
    print("AT-004 — HOLD Legitimacy Test")
    print("=" * 60)
    history = fresh_history()
    action = "agent wants to ask human before doing a reversible action"
    matched = consult_scar.consult_scar(action)
    redirect = consult_scar.redirect_for_scar(matched, action=action, scar_history=history)

    mandatory = {"owner", "evidence_gap", "next_action", "expiry", "scar_signature"}
    present = set(redirect.keys()) & mandatory
    all_present = mandatory.issubset(set(redirect.keys()))

    verdict = (
        f"PASS — 5/5 mandatory HOLD fields present: {sorted(present)}"
    ) if all_present else (
        f"FAIL — missing: {sorted(mandatory - present)}"
    )
    print(f"  mandatory: {sorted(mandatory)}")
    print(f"  present: {sorted(present)}")
    print(f"  verdict: {verdict}")
    return all_present


# ── AT-005 — Constitutional Boundary Test (Phase C version) ────────────────────
def at_005_constitutional_boundary():
    print()
    print("AT-005 — Constitutional Boundary Test (Phase C)")
    print("=" * 60)
    history = fresh_history()
    # Test: action involves irreversible mutation + canonical mutation
    irreversible_action = "agent wants to do irreversible mutation to /root/AAA/canon/ without F13 SAH"
    matched = consult_scar.consult_scar(irreversible_action)
    redirect = consult_scar.redirect_for_scar(matched, action=irreversible_action, scar_history=history)

    boundary_detected = redirect.get("authority_boundary", False)
    target = redirect.get("redirect_target", "")
    escalation_routed = "f13_escalation" in str(target)

    verdict = (
        f"PASS — irreversible action routed to {target} (escalation path)"
    ) if boundary_detected and escalation_routed else (
        f"FAIL — boundary not detected (boundary={boundary_detected}, target={target})"
    )
    print(f"  decision: {redirect.get('decision')}")
    print(f"  authority_boundary: {boundary_detected}")
    print(f"  redirect_target: {target}")
    print(f"  verdict: {verdict}")
    return boundary_detected and escalation_routed


# ── AT-006 — Anti-Fossilization Test (Phase C version) ────────────────────────
def at_006_anti_fossilization():
    print()
    print("AT-006 — Anti-Fossilization Test (Phase C)")
    print("=" * 60)
    history = fresh_history()
    action = "agent wants to ask human before doing a reversible action"

    # First consultation — scar blocks
    matched = consult_scar.consult_scar(action)
    redirect_v1 = consult_scar.redirect_for_scar(matched, action=action, scar_history=history)

    # Inject new evidence — override the scar
    history.override_with_evidence("ask-when-action-is-cheap", "F13 explicitly authorized this reversal pattern 2026-10-06")

    # Second consultation — should proceed (override)
    matched2 = consult_scar.consult_scar(action)
    redirect_v2 = consult_scar.redirect_for_scar(matched2, action=action, scar_history=history)

    override_works = ("+OVERRIDDEN" in redirect_v2.get("scar_signature", "")) or \
                     (redirect_v2.get("redirect_target") == "proceed (overridden)") or \
                     (redirect_v2.get("decision") == "PROCEED_WITH_AWARENESS")

    verdict = (
        f"PASS — scar overridden by new evidence (v2 sig={redirect_v2.get('scar_signature')})"
    ) if override_works else (
        f"FAIL — scar still blocks after override (v1={redirect_v1.get('decision')}, v2={redirect_v2.get('decision')})"
    )
    print(f"  v1 (before override): decision={redirect_v1.get('decision')}, sig={redirect_v1.get('scar_signature')}")
    print(f"  v2 (after override): decision={redirect_v2.get('decision')}, sig={redirect_v2.get('scar_signature')}")
    print(f"  verdict: {verdict}")
    return override_works


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("AAA-EMERGENCE Acceptance Test Suite v2 (with Phase C scar_history)")
    print("Per F13 canonization 2026-10-06 10:05 MYT + APEX math invocation 10:10 MYT")
    print("=" * 60)
    print()

    results = {
        "AT-001 Scar Binding": at_001_scar_binding(),
        "AT-002 Scar Disregard": at_002_scar_disregard(),
        "AT-003 Selection Mutation": at_003_selection_mutation(),
        "AT-004 HOLD Legitimacy": at_004_hold_legitimacy(),
        "AT-005 Constitutional Boundary": at_005_constitutional_boundary(),
        "AT-006 Anti-Fossilization": at_006_anti_fossilization(),
    }

    print()
    print("=" * 60)
    print("SUMMARY (with Phase C scar_history)")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for name, passed_test in results.items():
        marker = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"  {marker}  {name}")
    print(f"\n  TOTAL: {passed}/{total} passed")
    print()
    if passed == total:
        print("ALL GREEN — APEX physics math code applied. Scar is now constraint, not history.")
    else:
        print(f"{total - passed} test(s) still need wiring.")
