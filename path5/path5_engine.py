#!/usr/bin/env python3
"""
path5_engine.py — Path-5 Constitutional Swarm Substrate Engine.
Implements the living substrate:
  Agent → Lease → Worktree → Mutation → Validation → Reconciliation → Merge → Receipt

Standard: QQQ Protocol · F1 Truth · Fail Closed · DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PATH5_DIR = Path("/root/AAA/path5")
WORKTREES_DIR = Path("/root/forge_work/worktrees")
LEASE_STORE = PATH5_DIR / "leases.jsonl"
RECEIPT_LOG = PATH5_DIR / "receipts.jsonl"
RECONCILE_LOCK = WORKTREES_DIR / ".reconcile.lock"
ARIFFLOW_INGEST = "http://127.0.0.1:7073/ingest"

# Hard limits (Merge Flood Governance)
MAX_ACTIVE_WORKTREES = 4
DEFAULT_TTL_SEC = 3600
MAX_TTL_SEC = 14400


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _emit_flow_receipt(receipt: Dict[str, Any]) -> None:
    """Fail-soft arifFlow / witness event emission."""
    try:
        import urllib.request
        req = urllib.request.Request(
            ARIFFLOW_INGEST,
            data=json.dumps(receipt).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            pass
    except Exception:
        # Fail-soft: witness local file log remains primary truth
        pass


class LeaseEngine:
    def __init__(self, store_path: Path = LEASE_STORE):
        self.store_path = store_path
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.store_path.exists():
            self.store_path.touch()

    def _read_all(self) -> Dict[str, Dict[str, Any]]:
        leases = {}
        if not self.store_path.exists():
            return leases
        with open(self.store_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    leases[obj["lease_id"]] = obj
                except Exception:
                    pass
        return leases

    def _write_all(self, leases: Dict[str, Dict[str, Any]]) -> None:
        with open(self.store_path, "w", encoding="utf-8") as f:
            for lease in leases.values():
                f.write(json.dumps(lease) + "\n")

    def request_lease(
        self,
        actor_id: str,
        repository: str,
        allowed_paths: List[str],
        ttl_seconds: int = DEFAULT_TTL_SEC,
        capability: str = "code_mutation"
    ) -> Dict[str, Any]:
        """Issue an active capability lease."""
        leases = self._read_all()
        # Enforce max active worktrees
        active_count = sum(1 for l in leases.values() if l.get("status") == "ACTIVE" and time.time() <= l.get("expires_at", 0))
        if active_count >= MAX_ACTIVE_WORKTREES:
            raise RuntimeError(f"CONCURRENCY_LIMIT_REACHED: {active_count} active leases currently open (max: {MAX_ACTIVE_WORKTREES})")

        now_ts = time.time()
        ttl = min(ttl_seconds, MAX_TTL_SEC)
        lease_id = f"lease_{uuid.uuid4().hex[:12]}"
        
        lease = {
            "lease_id": lease_id,
            "actor_id": actor_id,
            "capability": capability,
            "scope": {
                "repository": repository,
                "allowed_paths": allowed_paths,
                "forbidden_paths": ["/root/.secrets/*", "*.env"]
            },
            "ttl_seconds": ttl,
            "issued_at": _utc(),
            "expires_at": now_ts + ttl,
            "last_heartbeat": now_ts,
            "status": "ACTIVE",
            "revoked": False,
            "revocation_reason": None,
        }
        leases[lease_id] = lease
        self._write_all(leases)

        receipt = {
            "event_type": "path5.lease.issued",
            "timestamp": _utc(),
            "lease_id": lease_id,
            "actor_id": actor_id,
            "repository": repository,
            "ttl_seconds": ttl,
        }
        self.record_receipt(receipt)
        _emit_flow_receipt(receipt)
        return lease

    def heartbeat(self, lease_id: str) -> Dict[str, Any]:
        leases = self._read_all()
        lease = leases.get(lease_id)
        if not lease:
            return {"valid": False, "reason": "LEASE_NOT_FOUND"}
        if lease.get("revoked"):
            return {"valid": False, "reason": "LEASE_REVOKED"}
        if time.time() > lease.get("expires_at", 0):
            lease["status"] = "EXPIRED"
            self._write_all(leases)
            return {"valid": False, "reason": "LEASE_EXPIRED"}

        lease["last_heartbeat"] = time.time()
        self._write_all(leases)
        return {"valid": True, "lease_id": lease_id, "last_heartbeat": lease["last_heartbeat"]}

    def validate(self, lease_id: str, relative_path: Optional[str] = None) -> Dict[str, Any]:
        leases = self._read_all()
        lease = leases.get(lease_id)
        if not lease:
            return {"valid": False, "reason": "LEASE_NOT_FOUND"}
        if lease.get("revoked"):
            return {"valid": False, "reason": "LEASE_REVOKED"}
        if time.time() > lease.get("expires_at", 0):
            lease["status"] = "EXPIRED"
            self._write_all(leases)
            return {"valid": False, "reason": "LEASE_EXPIRED"}
        if lease.get("status") != "ACTIVE":
            return {"valid": False, "reason": f"LEASE_{lease.get('status')}"}

        # Scope validation if path provided
        if relative_path:
            import fnmatch
            allowed = lease.get("scope", {}).get("allowed_paths", [])
            matches = any(fnmatch.fnmatch(relative_path, pat) for pat in allowed)
            if not matches:
                return {
                    "valid": False,
                    "reason": f"SCOPE_VIOLATION: '{relative_path}' not in allowed {allowed}"
                }
        return {"valid": True, "lease": lease}

    def revoke(self, lease_id: str, reason: str = "Sovereign revocation") -> Dict[str, Any]:
        leases = self._read_all()
        lease = leases.get(lease_id)
        if not lease:
            return {"revoked": False, "reason": "LEASE_NOT_FOUND"}
        lease["revoked"] = True
        lease["status"] = "REVOKED"
        lease["revocation_reason"] = reason
        self._write_all(leases)

        receipt = {
            "event_type": "path5.lease.revoked",
            "timestamp": _utc(),
            "lease_id": lease_id,
            "reason": reason
        }
        self.record_receipt(receipt)
        _emit_flow_receipt(receipt)
        return {"revoked": True, "lease_id": lease_id}

    def record_receipt(self, receipt_data: Dict[str, Any]) -> str:
        RECEIPT_LOG.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(receipt_data, sort_keys=True)
        r_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        receipt_data["receipt_hash"] = f"sha256:{r_hash}"
        receipt_data["recorded_at"] = _utc()
        with open(RECEIPT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(receipt_data) + "\n")
        return receipt_data["receipt_hash"]


class WorktreeManager:
    def __init__(self, worktrees_dir: Path = WORKTREES_DIR):
        self.worktrees_dir = worktrees_dir
        self.worktrees_dir.mkdir(parents=True, exist_ok=True)

    def get_worktree_path(self, lease_id: str) -> Path:
        return self.worktrees_dir / lease_id

    def create(self, lease_id: str, repo_path: Path, base_ref: str = "HEAD") -> Path:
        """Create an isolated worktree bound to lease_id."""
        wt_path = self.get_worktree_path(lease_id)
        branch_name = f"swarm/{lease_id}"

        # Clean existing if dirty
        if wt_path.exists():
            self.destroy(lease_id, repo_path)

        cmd = ["git", "-C", str(repo_path), "worktree", "add", "-b", branch_name, str(wt_path), base_ref]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Failed to create worktree: {res.stderr.strip()}")

        return wt_path

    def destroy(self, lease_id: str, repo_path: Path) -> None:
        """Safely prune and remove worktree and branch."""
        wt_path = self.get_worktree_path(lease_id)
        branch_name = f"swarm/{lease_id}"

        if wt_path.exists():
            subprocess.run(["git", "-C", str(repo_path), "worktree", "remove", "--force", str(wt_path)], capture_output=True)
        subprocess.run(["git", "-C", str(repo_path), "branch", "-D", branch_name], capture_output=True)
        subprocess.run(["git", "-C", str(repo_path), "worktree", "prune"], capture_output=True)


class Reconciler:
    def __init__(self, lease_engine: LeaseEngine, worktree_mgr: WorktreeManager):
        self.lease_engine = lease_engine
        self.worktree_mgr = worktree_mgr

    def reconcile(
        self,
        lease_id: str,
        repo_path: Path,
        target_branch: str = "main",
        test_command: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute the 6-stage A-FORGE Reconciler Pipeline:
          1. Scope & Diff
          2. Policy & Lease check
          3. Drift guard
          4. In-worktree tests
          5. Serialized merge
          6. Receipt & cleanup
        """
        wt_path = self.worktree_mgr.get_worktree_path(lease_id)
        if not wt_path.exists():
            return {"success": False, "stage": "PRECHECK", "error": "WORKTREE_NOT_FOUND"}

        # 1 & 2. Lease & Policy Check
        val = self.lease_engine.validate(lease_id)
        if not val.get("valid"):
            return {"success": False, "stage": "LEASE_VALIDATION", "error": val.get("reason")}
        lease = val["lease"]

        # Diff inspection
        cmd_diff = ["git", "-C", str(wt_path), "diff", "--name-only", f"{target_branch}...HEAD"]
        res_diff = subprocess.run(cmd_diff, capture_output=True, text=True)
        if res_diff.returncode != 0:
            # Fallback for comparing with origin/target
            cmd_diff = ["git", "-C", str(wt_path), "diff", "--name-only", "HEAD~1...HEAD"]
            res_diff = subprocess.run(cmd_diff, capture_output=True, text=True)

        changed_files = [f.strip() for f in res_diff.stdout.splitlines() if f.strip()]
        if not changed_files:
            return {"success": False, "stage": "DIFF_CHECK", "error": "NO_COMMITTED_CHANGES"}

        # Scope validation against lease
        for cf in changed_files:
            path_val = self.lease_engine.validate(lease_id, relative_path=cf)
            if not path_val.get("valid"):
                return {"success": False, "stage": "SCOPE_CHECK", "error": path_val.get("reason"), "file": cf}

        # 3. Drift & Secret Guard
        for cf in changed_files:
            if ".secrets" in cf or cf.endswith(".env"):
                return {"success": False, "stage": "DRIFT_GUARD", "error": f"SENSITIVE_FILE_PROHIBITED: {cf}"}

        # 4. In-Worktree Tests
        if test_command:
            res_test = subprocess.run(test_command, cwd=str(wt_path), capture_output=True, text=True)
            if res_test.returncode != 0:
                return {
                    "success": False,
                    "stage": "TEST_EXECUTION",
                    "error": "TESTS_FAILED",
                    "stderr": res_test.stderr[-500:],
                    "stdout": res_test.stdout[-500:]
                }

        # 5. Serialized Merge with File Lock
        RECONCILE_LOCK.parent.mkdir(parents=True, exist_ok=True)
        with open(RECONCILE_LOCK, "w") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                # Merge swarm branch into target
                branch_name = f"swarm/{lease_id}"
                # Checkout target repo
                subprocess.run(["git", "-C", str(repo_path), "checkout", target_branch], capture_output=True, check=True)
                merge_msg = f"reconcile(swarm): merge {lease_id} by {lease['actor_id']}"
                cmd_merge = ["git", "-C", str(repo_path), "merge", "--no-ff", branch_name, "-m", merge_msg]
                res_merge = subprocess.run(cmd_merge, capture_output=True, text=True)
                if res_merge.returncode != 0:
                    subprocess.run(["git", "-C", str(repo_path), "merge", "--abort"], capture_output=True)
                    return {"success": False, "stage": "GIT_MERGE", "error": res_merge.stderr.strip()}

                # Get resulting commit hash
                res_sha = subprocess.run(["git", "-C", str(repo_path), "rev-parse", "HEAD"], capture_output=True, text=True)
                commit_sha = res_sha.stdout.strip()
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

        # 6. Receipt & Cleanup
        receipt_data = {
            "event_type": "path5.merge.approved",
            "timestamp": _utc(),
            "lease_id": lease_id,
            "actor_id": lease["actor_id"],
            "repository": str(repo_path.name),
            "merged_commit_sha": commit_sha,
            "changed_files": changed_files,
            "reconciler": "A-FORGE-RECONCILER-V1",
        }
        receipt_hash = self.lease_engine.record_receipt(receipt_data)
        _emit_flow_receipt(receipt_data)

        # Mark lease completed
        leases = self.lease_engine._read_all()
        if lease_id in leases:
            leases[lease_id]["status"] = "COMPLETED"
            self.lease_engine._write_all(leases)

        # Destroy worktree substrate
        self.worktree_mgr.destroy(lease_id, repo_path)

        return {
            "success": True,
            "lease_id": lease_id,
            "commit_sha": commit_sha,
            "receipt_hash": receipt_hash,
            "changed_files": changed_files
        }


def main():
    parser = argparse.ArgumentParser(description="Path-5 Constitutional Swarm Engine")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Lease commands
    p_lease = subparsers.add_parser("lease")
    p_lease.add_argument("--request", action="store_true")
    p_lease.add_argument("--actor", required=True)
    p_lease.add_argument("--repo", required=True)
    p_lease.add_argument("--paths", nargs="+", required=True)
    p_lease.add_argument("--ttl", type=int, default=DEFAULT_TTL_SEC)

    # Worktree commands
    p_wt = subparsers.add_parser("worktree")
    p_wt.add_argument("--create", action="store_true")
    p_wt.add_argument("--lease-id", required=True)
    p_wt.add_argument("--repo-path", required=True)

    args = parser.parse_args()
    lease_eng = LeaseEngine()
    wt_mgr = WorktreeManager()

    if args.subcommand == "lease" and args.request:
        lease = lease_eng.request_lease(args.actor, args.repo, args.paths, args.ttl)
        print(json.dumps(lease, indent=2))
    elif args.subcommand == "worktree" and args.create:
        wt_path = wt_mgr.create(args.lease_id, Path(args.repo_path))
        print(f"WORKTREE_CREATED: {wt_path}")


if __name__ == "__main__":
    main()
