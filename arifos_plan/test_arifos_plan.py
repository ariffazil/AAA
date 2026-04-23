"""
Test arifos_plan — Planning Organ MVP
Run: python test_arifos_plan.py
"""
import sys
sys.path.insert(0, __file__)
from arifos_plan import propose_plan, get_plan, list_pending, update_status, abort_plan

# ─── Test 1: Low-risk plan (auto-approves) ───────────────────────────────────
print("\n=== TEST 1: Low-risk plan (auto-approves) ===")
result = propose_plan(
    description="Git pull latest main",
    tasks=[{
        "description": "git pull origin main",
        "tool": "mcpgit",
        "mutates_external_state": True,
        "target_surface": "git_repo",
        "reversible": True,
        "risk_band": "LOW",
    }],
    risk_band="LOW",
    irreversible=False,
    created_by="test-agent",
)
print(f"verdict: {result['verdict']}")
print(f"status: {result['plan']['status']}")
print(f"hold_reason: {result.get('hold_reason')}")
assert result['verdict'] == 'SEAL', f"Expected SEAL, got {result['verdict']}"
plan_id_low = result['plan']['plan_id']
print(f"✅ PASS — plan {plan_id_low} auto-approved")

# ─── Test 2: High-risk plan (triggers 888_HOLD) ──────────────────────────────
print("\n=== TEST 2: High-risk plan (triggers 888_HOLD) ===")
result = propose_plan(
    description="Drop staging DB and re-migrate",
    tasks=[{
        "description": "DROP DATABASE staging",
        "tool": "mcpsql",
        "mutates_external_state": True,
        "target_surface": "staging_postgres",
        "reversible": False,
        "risk_band": "HIGH",
    }],
    risk_band="HIGH",
    irreversible=True,
    created_by="test-agent",
)
print(f"verdict: {result['verdict']}")
print(f"status: {result['plan']['status']}")
print(f"hold_reason: {result.get('hold_reason')}")
assert result['verdict'] == 'HOLD', f"Expected HOLD, got {result['verdict']}"
plan_id_high = result['plan']['plan_id']
print(f"✅ PASS — plan {plan_id_high} triggers 888_HOLD")

# ─── Test 3: Get plan ─────────────────────────────────────────────────────────
print("\n=== TEST 3: get_plan ===")
result = get_plan(plan_id_low)
assert result['verdict'] == 'SEAL', f"Expected SEAL, got {result['verdict']}"
assert result['plan']['plan_id'] == plan_id_low
print(f"✅ PASS — fetched plan {plan_id_low}")

# ─── Test 4: list_pending ────────────────────────────────────────────────────
print("\n=== TEST 4: list_pending ===")
result = list_pending()
assert result['count'] >= 1, f"Expected >=1 pending, got {result['count']}"
print(f"✅ PASS — {result['count']} pending plan(s)")

# ─── Test 5: Sovereign approves high-risk plan ──────────────────────────────
print("\n=== TEST 5: Approve high-risk plan (sovereign) ===")
result = update_status(
    plan_id=plan_id_high,
    decision="APPROVED",
    decided_by="arif-human",
    notes="Approved — staging is safe to reset",
    floor_signatures=["F0", "F1", "F13"],
)
print(f"verdict: {result['verdict']}")
print(f"status: {result['plan']['status']}")
assert result['verdict'] == 'SEAL', f"Expected SEAL, got {result['verdict']}"
assert result['plan']['status'] == 'APPROVED', f"Expected APPROVED, got {result['plan']['status']}"
print(f"✅ PASS — plan {plan_id_high} APPROVED by sovereign")

# ─── Test 6: Reject plan ─────────────────────────────────────────────────────
print("\n=== TEST 6: Reject plan ===")
result = update_status(
    plan_id=plan_id_high,
    decision="REJECTED",
    decided_by="arif-human",
    notes="Not yet — need backup first",
)
print(f"verdict: {result['verdict']}")
print(f"status: {result['plan']['status']}")
assert result['verdict'] == 'VOID', f"Expected VOID, got {result['verdict']}"
assert result['plan']['status'] == 'ABORTED', f"Expected ABORTED, got {result['plan']['status']}"
print(f"✅ PASS — plan {plan_id_high} ABORTED")

# ─── Test 7: abort_plan shortcut ─────────────────────────────────────────────
print("\n=== TEST 7: abort_plan shortcut ===")
result2 = propose_plan(description="Test abort", tasks=[], risk_band="LOW", irreversible=False)
pid = result2['plan']['plan_id']
abort = abort_plan(pid, reason="Changed mind", aborted_by="arif-human")
assert abort['plan']['status'] == 'ABORTED'
print(f"✅ PASS — plan {pid} aborted via shortcut")

print("\n" + "="*50)
print("ALL TESTS PASSED — arifos_plan MVP ✅")
print("="*50)
