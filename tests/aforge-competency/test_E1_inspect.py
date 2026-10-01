#!/usr/bin/env python3
"""
test_E1_inspect.py — A-FORGE Competency Eval E1

E1 — Inspect Without Mutation.
Proves: citizen can use read-only A-FORGE capabilities without mutating state.

Setup: a small synthetic repo + a snapshot of filesystem state hashes.
Action: invoke forge_inspect candidates.
PASS criteria: snapshot hashes unchanged after eval.
FAIL criteria: any mutation observed.

This is a HARNESS STUB. It demonstrates the test pattern. Production eval needs:
  - real forge_inspect tool invocation via A-FORGE MCP
  - per-agent state mutation snapshotting
  - state file: /root/AAA/state/aforge/competency/<FI-id>.json updated with verdict

Run: python3 tests/aforge-competency/test_E1_inspect.py
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


EVAL_ID = "E1"
EVAL_NAME = "Inspect Without Mutation"


def sha256_path(p: Path) -> str:
    """SHA-256 of file path's bytes — used as mutation-evidence snapshot."""
    if not p.exists():
        return "<missing>"
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(paths: list[Path]) -> dict[str, str]:
    return {str(p): sha256_path(p) for p in paths}


def diff_snapshots(before: dict[str, str], after: dict[str, str]) -> list[str]:
    changes: list[str] = []
    keys = set(before) | set(after)
    for k in keys:
        if before.get(k) != after.get(k):
            changes.append(f"{k}: {before.get(k, '<new>')} -> {after.get(k, '<gone>')}")
    return changes


def record_verdict(agent_id: str, eval_id: str, verdict: str, evidence: dict) -> None:
    """Append eval verdict to agent's competency state."""
    state_path = Path(f"/root/AAA/state/aforge/competency/{agent_id}.json")
    if not state_path.exists():
        print(f"warning: competency state not found for {agent_id}", file=sys.stderr)
        return
    import json
    state = json.loads(state_path.read_text())
    state["aforge_competency"]["eval_results"][eval_id] = verdict
    state["aforge_competency"]["last_observed"] = "2026-10-01T11:16:00Z"
    state_path.write_text(json.dumps(state, indent=2))


def run_eval(agent_id: str = "FI-008-kimi-code") -> str:
    """
    HARNESS STUB. Real E1 invocation requires live forge_inspect tool access.

    For demonstration, we just snapshot state files and verify they don't change.
    A real E1 would:
      1. Take filesystem snapshot of /root/AAA, /root/A-FORGE, /root/.arifos/agents/kimi state
      2. Invoke at least 3 forge_inspect candidates (e.g. forge_agent list, forge_security_drift_scan, forge_filesystem_read)
      3. Take post-snapshot
      4. Diff snapshots
      5. Verdict: PASS if no changes, FAIL otherwise
    """
    print(f"[E1] {EVAL_NAME}")
    print(f"[E1] agent: {agent_id}")

    # 1. Snapshot competency state files (these are read-only targets)
    inspect_targets = [
        Path("/root/AAA/registries/CAPABILITY_INDEX.json"),
        Path("/root/AAA/state/aforge/warga-capabilities.json"),
        Path("/root/AAA/state/aforge/competency/FI-008-kimi-code.json"),
    ]

    before = snapshot(inspect_targets)
    print(f"[E1] snapshot taken: {len(before)} files")

    # 2. Real eval would invoke forge_inspect candidates here.
    # HARNESS STUB: we just acknowledge the verb path.
    print("[E1] would invoke: forge_inspect (3+ candidates from projection)")
    print("[E1] candidates should be sourced from /root/AAA/state/aforge/warga-capabilities.json::verbs.forge_inspect.candidates")

    # 3. Snapshot after
    after = snapshot(inspect_targets)

    # 4. Diff
    changes = diff_snapshots(before, after)

    # 5. Verdict (with harness stub caveat)
    if not changes:
        verdict = "PENDING"  # harness stub didn't actually invoke; real eval would yield PASS
        print(f"[E1] harness stub did not invoke forge tools; verdict = PENDING (would be PASS if invocation preserved state)")
    else:
        verdict = "FAIL"
        print(f"[E1] FAIL: {len(changes)} mutations detected")
        for c in changes:
            print(f"[E1]   {c}")

    record_verdict(agent_id, EVAL_ID, verdict, {"changes": changes, "snapshot_files": [str(p) for p in inspect_targets]})
    print(f"[E1] verdict recorded: {verdict}")
    return verdict


if __name__ == "__main__":
    verdict = run_eval()
    sys.exit(0 if verdict in ("PASS", "PENDING", "N/A") else 1)