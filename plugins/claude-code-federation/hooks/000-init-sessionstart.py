#!/usr/bin/env python3
"""
000 INIT — SessionStart Hook for Claude Code
=============================================
Constitutional governance: establish identity and bind session.

This hook fires at the START of every Claude Code session. It:
  1. Probes arifOS kernel (:8088/health) — verify floors=13, verdict=SEAL
  2. Probes all 7 federation organs — report liveness
  3. Binds session via arif_init — get session_id + SCT token
  4. Stores session state to /tmp/opencode/session_state.json
  5. Injects federation context as additionalContext

Part of the arifos-federation Claude Code plugin.
DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────
ARIFOS_HEALTH = "http://127.0.0.1:8088/health"
ARIFOS_INIT = "http://127.0.0.1:8088/mcp"
ORGANS = {"arifos": 8088, "aforge": 7071, "arifflow": 7073, "aaa": 3001, "geox": 8081, "wealth": 18082, "well": 18083}
SESSION_STATE = "/tmp/opencode/session_state.json"

# ── Helpers ────────────────────────────────────────────────────────────


def probe(url: str, timeout: int = 3) -> dict | None:
    """Probe a health endpoint, return parsed JSON or None."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def probe_organs() -> dict:
    """Probe all federation organs. Returns {name: status}."""
    results = {}
    for name, port in ORGANS.items():
        url = f"http://127.0.0.1:{port}/health"
        data = probe(url, timeout=2)
        results[name] = "alive" if data else "DOWN"
    return results


def bind_session() -> dict:
    """Bind session via arifOS kernel. Returns session state or empty dict."""
    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "arif_init",
                "arguments": {
                    "mode": "init",
                    "actor_id": "claude-code/FI-002",
                    "intent": "Claude Code session — autonomous coding under F1-F13",
                    "requested_authority": "FULL",
                },
            },
        }
    ).encode()

    try:
        req = urllib.request.Request(ARIFOS_INIT, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            content = result.get("result", {}).get("content", [{}])[0]
            text = content.get("text", "{}")
            inner = json.loads(text) if isinstance(text, str) else text

            return {
                "session_id": inner.get("session_id", ""),
                "session_token": inner.get("session_token", ""),
                "actor_id": "claude-code/FI-002",
                "bound_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "lane": "B",
                "profile": "BUILD",
            }
    except Exception as e:
        return {"error": str(e), "session_id": "unbound"}


# ── Main ───────────────────────────────────────────────────────────────


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    # ── Step 1: Probe kernel ────────────────────────────────────────────
    kernel = probe(ARIFOS_HEALTH, timeout=5)
    kernel_ok = False
    if kernel:
        thermo = kernel.get("thermodynamic", {})
        verdict = thermo.get("verdict", "?")
        floors = kernel.get("floors_active", "?")
        kernel_ok = verdict == "SEAL" and floors == 13

    # ── Step 2: Probe organs ────────────────────────────────────────────
    organs = probe_organs()
    alive = sum(1 for v in organs.values() if v == "alive")

    # ── Step 3: Bind session ────────────────────────────────────────────
    session = bind_session()
    sid = session.get("session_id", "unbound")

    # ── Step 4: Store state ─────────────────────────────────────────────
    try:
        os.makedirs(os.path.dirname(SESSION_STATE), exist_ok=True)
        with open(SESSION_STATE, "w") as f:
            json.dump(session, f)
    except (IOError, PermissionError):
        pass

    # ── Step 5: Build context injection ─────────────────────────────────
    organ_lines = "  ".join(f"{'✅' if v == 'alive' else '❌'} {n}" for n, v in organs.items())

    context = f"""[arifOS Federation — Session Boot]
Kernel: {"✅ SEAL, floors=13" if kernel_ok else "⚠️ DEGRADED"}
Organs ({alive}/7): {organ_lines}
Session: {sid}
Lane: B · Profile: BUILD
Floors active: F1 AMANAH · F2 TRUTH · F4 CLARITY · F7 HUMILITY · F9 ANTI-HANTU · F11 AUDIT · F13 SOVEREIGN

DITEMPA BUKAN DIBERI — Forged, Not Given. Claude Code is a governed execution harness under arifOS constitutional kernel. arifOS judges. Claude Code executes. Probe before act. Reversible first. Never ask permission for digital ops (MUBAH)."""

    # ── Emit ────────────────────────────────────────────────────────────
    output = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}

    # Warn if degraded
    if alive < 4:
        output["systemMessage"] = (
            f"**[WARNING] Federation degraded — {alive}/7 organs alive.** "
            f"Proceeding in LIMITED mode. Some capabilities unavailable."
        )

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
