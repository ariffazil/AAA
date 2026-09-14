# Path-5 Operational Runbook (v1.0)
**Document:** `RUNBOOK.md`  
**Standard:** QQQ Protocol · Operational Readiness  
**Date:** 2026-09-14T09:48:30+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::PATH5_OPERATIONALIZATION::v1`

---

## 1. Quick Operator Summary

Path-5 replaces direct-to-root edits with an isolated worktree substrate governed by cryptographic leases and serial reconciliation.

```text
Operator Request (Arif / Hermes)
  ↓
1. Request Lease  (path5_engine.py lease --request --actor <ID> --repo <REPO> --paths <PATTERNS>)
  ↓
2. Spawn Worktree (path5_engine.py worktree --create --lease-id <ID> --repo-path <PATH>)
  ↓
3. Agent Mutates  (Worktree isolated at /root/forge_work/worktrees/<lease_id>)
  ↓
4. In-Worktree Tests (pytest / npm test)
  ↓
5. Reconcile & Merge (Reconciler verifies diff, scope, secrets, tests, merges, emits receipt, cleans up)
```

---

## 2. Standard Commands

### 2.1 Requesting a Lease
```bash
python3 /root/AAA/path5/path5_engine.py lease \
  --request \
  --actor "FI-009/AGY" \
  --repo "AAA" \
  --paths "path5/*" "tests/*" \
  --ttl 3600
```

### 2.2 Spawning Worktree
```bash
python3 /root/AAA/path5/path5_engine.py worktree \
  --create \
  --lease-id "lease_1897d4d6f533" \
  --repo-path "/root/AAA"
```

### 2.3 Automated End-to-End Test Suite
```bash
python3 /root/AAA/path5/test_path5_e2e.py
```

---

## 3. Emergency Overrides & Troubleshooting

- **Revoke a Rogue Lease:**
  ```python
  from path5_engine import LeaseEngine
  LeaseEngine().revoke("<lease_id>", reason="888_HOLD security kill")
  ```
- **Prune Dangling Worktrees:**
  ```bash
  git -C /root/<REPO> worktree prune
  ```
- **Inspect Active Receipts:**
  ```bash
  tail -n 10 /root/AAA/path5/receipts.jsonl | jq .
  ```
