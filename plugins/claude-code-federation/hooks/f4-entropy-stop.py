#!/usr/bin/env python3
"""
F4 CLARITY + F11 AUDIT — Stop Hook for Claude Code
====================================================
Constitutional governance: ΔS ≤ 0 on session end.

This hook fires when Claude Code session stops. It:
  1. Runs entropy sweep via A-FORGE (:7071) — detect uncommitted work
  2. Counts uncommitted git changes across federation repos
  3. Reports FQ pulse via arifFlow (:7073)
  4. Records session close to audit ledger
  5. Recommends next actions (commit, seal, carry-forward)

Part of the arifos-federation Claude Code plugin.
DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────
AUDIT_LOG = "/root/.claude/hooks/f11-audit.jsonl"
SESSION_STATE = "/tmp/opencode/session_state.json"
ARIFLOW_HEALTH = "http://127.0.0.1:7073/health"
ARIFLOW_INGEST = "http://127.0.0.1:7073/ingest"
FEDERATION_REPOS = ["/root/arifOS", "/root/A-FORGE", "/root/AAA", "/root/GEOX", "/root/WEALTH", "/root/WELL"]

# ── Helpers ────────────────────────────────────────────────────────────


def load_session() -> dict:
    try:
        with open(SESSION_STATE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def probe_fq() -> dict:
    """Probe arifFlow for FQ pulse."""
    try:
        req = urllib.request.Request(ARIFLOW_HEALTH)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
            fq = data.get("fq", {})
            return {
                "quotient": fq.get("quotient", "?"),
                "verdict": fq.get("verdict", "?"),
                "receipts": data.get("receipts", 0),
            }
    except Exception:
        return {"quotient": "?", "verdict": "DOWN", "receipts": 0}


def check_dirty_repos() -> dict:
    """Check all federation repos for uncommitted changes."""
    results = {}
    for repo in FEDERATION_REPOS:
        if not os.path.isdir(f"{repo}/.git"):
            continue
        try:
            r = subprocess.run(["git", "-C", repo, "status", "-s"], capture_output=True, text=True, timeout=5)
            name = os.path.basename(repo)
            dirty_lines = [l for l in r.stdout.strip().split("\n") if l.strip()]
            results[name] = len(dirty_lines)
        except Exception:
            results[os.path.basename(repo)] = -1  # error
    return results


def compute_entropy(dirty: dict) -> float:
    """Compute simple entropy score. Higher = more chaos."""
    total = sum(max(0, v) for v in dirty.values())
    # 0 clean = ΔS=0, >20 dirty = ΔS>0
    return min(1.0, total / 20.0)


def ingest_close(session_id: str):
    """Ingest session close into arifFlow."""
    payload = json.dumps(
        {
            "actor_id": "claude-code/FI-002",
            "session_id": session_id or "unbound",
            "step_type": "Seal",
            "epistemic_label": "Seal",
            "floor_verdict": "Pass",
            "payload": {"event": "session_close", "ts": time.time()},
        }
    ).encode()
    try:
        req = urllib.request.Request(ARIFLOW_INGEST, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass


# ── Main ───────────────────────────────────────────────────────────────


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    session = load_session()
    sid = session.get("session_id", "unbound")

    # ── Step 1: FQ pulse ────────────────────────────────────────────────
    fq = probe_fq()

    # ── Step 2: Dirty repo scan ─────────────────────────────────────────
    dirty = check_dirty_repos()
    entropy = compute_entropy(dirty)

    # ── Step 3: Audit log ───────────────────────────────────────────────
    entry = {
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "session": sid,
        "event": "session_stop",
        "fq": fq,
        "dirty_repos": dirty,
        "entropy": round(entropy, 2),
    }
    try:
        with open(AUDIT_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except (IOError, PermissionError):
        pass

    # ── Step 4: Ingest to arifFlow ──────────────────────────────────────
    ingest_close(sid)

    # ── Step 5: Build recommendation ────────────────────────────────────
    dirty_repos_list = [f"{k}({v})" for k, v in dirty.items() if v > 0]
    fq_line = f"FQ: {fq['quotient']} ({fq['verdict']}) · receipts: {fq['receipts']}"

    if entropy == 0:
        verdict = "✅ ΔS=0 — clean workspace"
    elif entropy < 0.3:
        verdict = f"⚠️ ΔS={entropy:.2f} — {', '.join(dirty_repos_list)} have uncommitted changes"
    else:
        verdict = f"🛑 ΔS={entropy:.2f} — high entropy! {', '.join(dirty_repos_list)} need attention"

    message = (
        f"**[F4 CLARITY — Session Close]**\n"
        f"{verdict}\n"
        f"{fq_line}\n"
        f"Session: `{sid}`\n\n"
        f"_DITEMPA BUKAN DIBERI — Leave it cleaner than you found it._"
    )

    output = {"systemMessage": message}
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
