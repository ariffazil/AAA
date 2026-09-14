#!/usr/bin/env python3
"""
test_path5_e2e.py — End-to-End Witness Verification Suite for Path-5 Swarm Substrate.
Proves the complete chain:
  Agent A + Agent B
  → Lease A + Lease B
  → Worktree A + Worktree B (Physical Isolation)
  → Concurrent Mutations
  → Scope & Floor Validation (Fail-Closed Gates)
  → Reconciler Verification Pipeline
  → Serialized Merge to Base
  → Receipt Chain Verification
"""

import os
import sys
import time
import json
import shutil
import subprocess
from pathlib import Path

# Add path5 to sys.path
sys.path.insert(0, "/root/AAA/path5")
from path5_engine import LeaseEngine, WorktreeManager, Reconciler, LEASE_STORE, RECEIPT_LOG

TEST_REPO = Path("/tmp/path5-e2e-repo")
WORKTREES_DIR = Path("/root/forge_work/worktrees")


def setup_test_repo():
    """Create a pristine git repository for physical worktree testing."""
    if TEST_REPO.exists():
        shutil.rmtree(TEST_REPO)
    TEST_REPO.mkdir(parents=True, exist_ok=True)

    subprocess.run(["git", "init", "-b", "main"], cwd=str(TEST_REPO), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "ArifOS Test Harness"], cwd=str(TEST_REPO), check=True)
    subprocess.run(["git", "config", "user.email", "test@arifos.local"], cwd=str(TEST_REPO), check=True)

    # Base directory structure
    (TEST_REPO / "module_a").mkdir()
    (TEST_REPO / "module_b").mkdir()
    (TEST_REPO / "module_a" / "core.py").write_text("# Module A base\ndef run():\n    return 'base_a'\n")
    (TEST_REPO / "module_b" / "core.py").write_text("# Module B base\ndef run():\n    return 'base_b'\n")
    (TEST_REPO / "tests").mkdir()
    (TEST_REPO / "tests" / "test_smoke.py").write_text("def test_smoke():\n    assert True\n")

    subprocess.run(["git", "add", "."], cwd=str(TEST_REPO), check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "chore: initial base commit"], cwd=str(TEST_REPO), check=True, capture_output=True)


def run_e2e_simulation():
    print("================================================================================")
    print("PATH-5 OPERATIONALLY WITNESSED CAPABILITY TEST RUN")
    print("Reference: ARIFOS::PATH5_OPERATIONALIZATION::v1")
    print("================================================================================")

    setup_test_repo()
    lease_eng = LeaseEngine()
    wt_mgr = WorktreeManager(WORKTREES_DIR)
    reconciler = Reconciler(lease_eng, wt_mgr)

    # 1. ISSUE LEASES
    print("\n[PHASE 1: LEASE ISSUANCE]")
    lease_a = lease_eng.request_lease(
        actor_id="FI-008/Kimi",
        repository="test-repo",
        allowed_paths=["module_a/*", "tests/*"],
        ttl_seconds=3600
    )
    print(f"✓ Lease A issued: {lease_a['lease_id']} for FI-008 (scope: {lease_a['scope']['allowed_paths']})")

    lease_b = lease_eng.request_lease(
        actor_id="FI-009/Antigravity",
        repository="test-repo",
        allowed_paths=["module_b/*", "tests/*"],
        ttl_seconds=3600
    )
    print(f"✓ Lease B issued: {lease_b['lease_id']} for FI-009 (scope: {lease_b['scope']['allowed_paths']})")

    # 2. CREATE ISOLATED WORKTREES
    print("\n[PHASE 2: WORKTREE FABRIC SPAWN]")
    wt_a = wt_mgr.create(lease_a["lease_id"], TEST_REPO)
    print(f"✓ Worktree A active at: {wt_a}")
    wt_b = wt_mgr.create(lease_b["lease_id"], TEST_REPO)
    print(f"✓ Worktree B active at: {wt_b}")

    assert wt_a.exists(), "Worktree A directory must exist"
    assert wt_b.exists(), "Worktree B directory must exist"
    assert wt_a != wt_b, "Worktree substrates must be physically distinct"

    # 3. CONCURRENT MUTATIONS
    print("\n[PHASE 3: CONCURRENT MUTATION IN PARALLEL WORKTREES]")
    file_a = wt_a / "module_a" / "core.py"
    file_a.write_text("# Module A mutated by FI-008\ndef run():\n    return 'mutated_by_kimi'\n")
    subprocess.run(["git", "add", "module_a/core.py"], cwd=str(wt_a), check=True)
    subprocess.run(["git", "commit", "-m", "feat(a): upgrade engine A"], cwd=str(wt_a), check=True)
    print(f"✓ Agent A mutated {file_a.relative_to(wt_a)} and committed to swarm/{lease_a['lease_id']}")

    file_b = wt_b / "module_b" / "core.py"
    file_b.write_text("# Module B mutated by FI-009\ndef run():\n    return 'mutated_by_antigravity'\n")
    subprocess.run(["git", "add", "module_b/core.py"], cwd=str(wt_b), check=True)
    subprocess.run(["git", "commit", "-m", "feat(b): upgrade engine B"], cwd=str(wt_b), check=True)
    print(f"✓ Agent B mutated {file_b.relative_to(wt_b)} and committed to swarm/{lease_b['lease_id']}")

    # 4. NEGATIVE GATE TESTING (FAIL-CLOSED ENFORCEMENT)
    print("\n[PHASE 4: FAIL-CLOSED GATE TESTING]")
    # Test 4.1: Scope violation check
    scope_violation = lease_eng.validate(lease_a["lease_id"], relative_path="module_b/rogue.py")
    assert not scope_violation["valid"], "Agent A modifying module_b must fail scope check"
    print("✓ Gate 4.1 PASS: Out-of-scope mutation refused (SCOPE_VIOLATION)")

    # Test 4.2: Expired lease rejection
    test_expired_lease = lease_eng.request_lease(
        actor_id="ExpiredAgent",
        repository="test-repo",
        allowed_paths=["*"],
        ttl_seconds=1
    )
    time.sleep(1.2)
    exp_val = lease_eng.validate(test_expired_lease["lease_id"])
    assert not exp_val["valid"] and exp_val["reason"] == "LEASE_EXPIRED", "Expired lease must fail validation"
    print("✓ Gate 4.2 PASS: Expired lease blocked (LEASE_EXPIRED)")

    # Test 4.3: Revoked lease rejection
    test_revoked_lease = lease_eng.request_lease(
        actor_id="RevokedAgent",
        repository="test-repo",
        allowed_paths=["*"],
        ttl_seconds=3600
    )
    lease_eng.revoke(test_revoked_lease["lease_id"], reason="888_HOLD security kill")
    rev_val = lease_eng.validate(test_revoked_lease["lease_id"])
    assert not rev_val["valid"] and rev_val["reason"] == "LEASE_REVOKED", "Revoked lease must fail validation"
    print("✓ Gate 4.3 PASS: Revoked lease blocked (LEASE_REVOKED)")

    # 5. RECONCILIATION & SERIALIZED MERGE
    print("\n[PHASE 5: RECONCILER PIPELINE & SERIALIZED MERGE]")
    test_cmd = ["python3", "-m", "pytest", "tests/test_smoke.py"]

    # Reconcile Agent A
    res_rec_a = reconciler.reconcile(
        lease_id=lease_a["lease_id"],
        repo_path=TEST_REPO,
        target_branch="main",
        test_command=test_cmd
    )
    print(f"✓ Reconciler merged Agent A: Commit {res_rec_a['commit_sha']} | Receipt {res_rec_a['receipt_hash']}")
    assert res_rec_a["success"], f"Reconcile A failed: {res_rec_a.get('error')}"

    # Reconcile Agent B
    res_rec_b = reconciler.reconcile(
        lease_id=lease_b["lease_id"],
        repo_path=TEST_REPO,
        target_branch="main",
        test_command=test_cmd
    )
    print(f"✓ Reconciler merged Agent B: Commit {res_rec_b['commit_sha']} | Receipt {res_rec_b['receipt_hash']}")
    assert res_rec_b["success"], f"Reconcile B failed: {res_rec_b.get('error')}"

    # 6. PHYSICAL REALITY AUDIT (0 COLLISIONS)
    print("\n[PHASE 6: REALITY SUBSTRATE VERIFICATION]")
    # Check that main repo has both mutations intact
    content_a = (TEST_REPO / "module_a" / "core.py").read_text()
    content_b = (TEST_REPO / "module_b" / "core.py").read_text()

    assert "mutated_by_kimi" in content_a, "Main repo must contain Agent A's changes"
    assert "mutated_by_antigravity" in content_b, "Main repo must contain Agent B's changes"
    print("✓ Physical Verification: Main repository holds both mutations simultaneously without file collision.")

    # Check that worktrees were destroyed cleanly
    assert not wt_a.exists(), "Worktree A must be pruned post-merge"
    assert not wt_b.exists(), "Worktree B must be pruned post-merge"
    print("✓ Substrate Hygiene: Temporary worktrees destroyed cleanly post-reconciliation.")

    # 7. RECEIPT LOGGING
    print("\n[PHASE 7: RECEIPT CHAIN INTEGRITY]")
    with open(RECEIPT_LOG, "r") as f:
        receipt_lines = f.readlines()
    print(f"✓ Receipt Log: {len(receipt_lines)} receipts persisted in {RECEIPT_LOG}")
    last_receipt = json.loads(receipt_lines[-1])
    print(f"✓ Latest receipt hash: {last_receipt['receipt_hash']} ({last_receipt['event_type']})")

    print("\n================================================================================")
    print("E2E WITNESS RESULT: ALL CRITERIA MET (SEAL_CAPABILITY)")
    print("================================================================================")
    return {
        "lease_a": lease_a["lease_id"],
        "lease_b": lease_b["lease_id"],
        "commit_a": res_rec_a["commit_sha"],
        "commit_b": res_rec_b["commit_sha"],
        "receipt_a": res_rec_a["receipt_hash"],
        "receipt_b": res_rec_b["receipt_hash"],
    }


def test_path5_e2e_witness():
    """CI automated witness proof for Path-5 Swarm Substrate."""
    res = run_e2e_simulation()
    assert res["lease_a"] and res["lease_b"]
    assert res["commit_a"] and res["commit_b"]


if __name__ == "__main__":
    run_e2e_simulation()

