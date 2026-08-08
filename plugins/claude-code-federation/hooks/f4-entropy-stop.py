#!/usr/bin/env python3
"""
F4 CLARITY — Stop Hook v2.0 (BLOCK on HIGH entropy)
=====================================================
Upgrade: ΔS > 0.5 → BLOCK exit (not just WARN).
ΔS ≤ 0.3 → allow with clear message.
0.3 < ΔS ≤ 0.5 → warn (recommend commit).

Part of arifos-federation Claude Code plugin v1.1.0.
DITEMPA BUKAN DIBERI.
"""

import json
import os
import subprocess
import sys
import time
import urllib.request

AUDIT_LOG = "/root/.claude/hooks/f11-audit.jsonl"
SESSION_STATE = "/tmp/opencode/session_state.json"
FEDERATION_REPOS = ["/root/arifOS", "/root/A-FORGE", "/root/AAA", "/root/GEOX", "/root/WEALTH", "/root/WELL"]
BLOCK_THRESHOLD = 0.5  # ΔS above this → BLOCK exit
WARN_THRESHOLD = 0.3  # ΔS above this → WARN


def load_session():
    try:
        with open(SESSION_STATE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def probe_fq():
    try:
        req = urllib.request.Request("http://127.0.0.1:7073/health")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
            return data.get("fq", {})
    except Exception:
        return {}


def check_dirty_repos():
    results = {}
    for repo in FEDERATION_REPOS:
        if not os.path.isdir(f"{repo}/.git"):
            continue
        try:
            r = subprocess.run(["git", "-C", repo, "status", "-s"], capture_output=True, text=True, timeout=5)
            results[os.path.basename(repo)] = len([l for l in r.stdout.strip().split("\n") if l.strip()])
        except Exception:
            results[os.path.basename(repo)] = -1
    return results


def compute_entropy(dirty):
    total = sum(max(0, v) for v in dirty.values())
    return min(1.0, total / 20.0)


def main():
    session = load_session()
    sid = session.get("session_id", "unbound")
    fq = probe_fq()
    dirty = check_dirty_repos()
    entropy = compute_entropy(dirty)

    # Audit log
    entry = {"ts": time.time(), "session": sid, "event": "session_stop", "entropy": round(entropy, 2), "dirty": dirty}
    try:
        with open(AUDIT_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except (IOError, PermissionError):
        pass

    dirty_list = [f"{k}({v})" for k, v in dirty.items() if v > 0]
    fq_line = f"FQ: {fq.get('quotient', '?')} ({fq.get('verdict', '?')})"

    # ── BLOCK on HIGH entropy ────────────────────────────────
    if entropy > BLOCK_THRESHOLD:
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": f"ΔS={entropy:.2f} > {BLOCK_THRESHOLD} — uncommitted work exceeds safe threshold",
                    "systemMessage": (
                        f"**[F4 CLARITY — BLOCKED]**\n"
                        f"ΔS={entropy:.2f} > {BLOCK_THRESHOLD} — {', '.join(dirty_list)} have uncommitted changes.\n"
                        f"{fq_line}\n\n"
                        f"**Action required:** Commit or stash changes before exiting.\n"
                        f'`git -C /root/ add -A && git -C /root/ commit -m "chore: session checkpoint"`\n'
                        f"Session: `{sid}`"
                    ),
                }
            )
        )
        sys.exit(2)  # exit 2 = block (Claude Code convention)

    # ── WARN on MEDIUM entropy ───────────────────────────────
    if entropy > WARN_THRESHOLD:
        print(
            json.dumps(
                {
                    "systemMessage": (
                        f"**[F4 CLARITY]**\n"
                        f"ΔS={entropy:.2f} — {', '.join(dirty_list)} uncommitted.\n"
                        f"{fq_line}\n"
                        f"Consider committing before exiting.\n"
                        f"Session: `{sid}`"
                    )
                }
            )
        )
        sys.exit(0)

    # ── Clean ────────────────────────────────────────────────
    print(
        json.dumps(
            {
                "systemMessage": (
                    f"**[F4 CLARITY — ✅ ΔS=0]**\n"
                    f"Clean workspace across all 6 organ repos.\n"
                    f"{fq_line}\n"
                    f"Session: `{sid}`\n"
                    f"_DITEMPA BUKAN DIBERI_"
                )
            }
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
