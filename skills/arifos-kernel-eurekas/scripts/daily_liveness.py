#!/usr/bin/env python3
"""STAB-2026-08-07 Rule #4 — daily liveness probe for all 8 canonical arifOS tools.

Differs from probe_8_tools.py (interactive, agentic). This script is the cron-bound
detector: minimal payloads (no human prompts), JSON output to stdout, exit code
signals HOLD if any tool is dead or returning unexpected error.

USAGE:
    python3 daily_liveness.py                  # one-shot probe
    python3 daily_liveness.py --out /var/log/arifos_liveness.json
    # cron line: 0 6 * * * /usr/bin/python3 /root/arifOS/scripts/daily_liveness.py

EXIT CODES:
    0 = all 8 tools responded (forged + seal may return EXPECTED_HOLD on anonymous — that's not dead)
    1 = at least one tool returned DEAD (curl error / timeout / unexpected error verdict)
    2 = substrate /health gate failed (kernel unreachable or drift_detected) — abort

PAIRING:
    - systemd timer: /etc/systemd/system/arifos-liveness.timer → daily_liveness.service
    - journal: journalctl -u arifos-liveness
    - VAULT999: append summary to /root/arifOS/VAULT999/outcomes.jsonl via git_to_vault.py

RATIONALE (Rule #4):
    Tools that no caller exercises stay dead quietly. arif_think was reported
    "crashed 2/2" by Opus 5 — actually a Claude-app tool-permission block, but
    the *class* of bug (silent tool death) only surfaces via automated probe.
    This script is the audit floor for "every canonical tool actually responds."

REFERENCE: arifos-kernel-eurekas/SKILL.md, payload-text-consistency reference
(Rule #4 row). Adjacent script: scripts/probe_8_tools.py (interactive agentic probe).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE = "http://127.0.0.1:8088/mcp"
TIMEOUT_S = 20

# (tool_name, arguments) — minimal payloads per tool. arif_forge + arif_seal
# use dry_run / anonymous to capture the EXPECTED_HOLD pattern (anonymous cannot
# forge/seal — that's correct, not dead).
PROBES = [
    ("arif_init", {"mode": "init", "actor_id": "liveness_probe", "ack_irreversible": False}),
    ("arif_observe", {"subject": "liveness_check", "frame": "ok", "session_id": "liveness_probe"}),
    ("arif_think", {"question": "liveness ping", "session_id": "liveness_probe"}),
    ("arif_route", {"intent": "liveness_check", "session_id": "liveness_probe"}),
    ("arif_memory", {"query": "liveness", "mode": "recall", "session_id": "liveness_probe"}),
    ("arif_judge", {"candidate": "liveness_check", "evidence": {"in_band": True}, "session_id": "liveness_probe"}),
    ("arif_forge", {"action": "liveness_ping", "dry_run": True, "session_id": "liveness_probe"}),
    ("arif_seal", {"receipt": "liveness_check", "session_id": "liveness_probe"}),
]


def call_mcp(tool_name: str, args: dict) -> dict:
    """Issue a JSON-RPC tools/call. Returns parsed result dict or {'_error': ...}."""
    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": args},
        }
    ).encode()
    req = urllib.request.Request(
        BASE,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            raw = r.read().decode()
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return {"_error": f"{type(e).__name__}: {e}"}

    # Streamable-HTTP may return SSE; try plain JSON first then strip SSE lines.
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        for line in raw.splitlines():
            if line.startswith("data:"):
                try:
                    return json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    continue
        return {"_error": "no_json_payload", "_raw_head": raw[:200]}


def extract_verdict(out: dict) -> tuple[str, str]:
    """Return (verdict_str, classification). Classification ∈ {ALIVE, EXPECTED_HOLD, DEAD}."""
    if "_error" in out:
        return f"DEAD: {out['_error'][:80]}", "DEAD"
    try:
        text = out.get("result", {}).get("content", [{}])[0].get("text", "")
        parsed = json.loads(text)
    except (json.JSONDecodeError, IndexError, AttributeError):
        return "DEAD: unparseable response", "DEAD"

    verdict = (
        parsed.get("effective_verdict")
        or parsed.get("verdict")
        or parsed.get("_wrapper_degradation", ["UNKNOWN"])[0]
    )

    # forge/seal expected to 888_HOLD for anonymous — correct, not dead
    if "HOLD" in str(verdict).upper() or "888_HOLD" in str(verdict).upper():
        # distinguish expected from real HOLD
        reasons = parsed.get("reasons", []) or parsed.get("_reasons", [])
        if any("anonymous" in str(r).lower() or "non-anonymous" in str(r).lower() for r in reasons):
            return f"{verdict} (anonymous, expected)", "EXPECTED_HOLD"

    # VOID is suspicious for read-class tools; HOLD for read-class is also suspicious
    if verdict in ("VOID", "HOLD", "888_HOLD"):
        return f"{verdict} (suspicious for read-class)", "SUSPICIOUS"
    return str(verdict), "ALIVE"


def substrate_gate() -> tuple[bool, dict]:
    """K4 pre-probe: /health must be healthy + aligned. Returns (passed, health_dict)."""
    try:
        with urllib.request.urlopen("http://127.0.0.1:8088/health", timeout=10) as r:
            h = json.loads(r.read().decode())
    except Exception as e:
        return False, {"_error": str(e)}

    if h.get("status") != "healthy":
        return False, h
    if h.get("deployment_drift_status") == "drift_detected":
        return False, h
    if h.get("runtime_drift") is True:
        return False, h
    return True, h


def main() -> int:
    ap = argparse.ArgumentParser(description="arifOS daily liveness probe (Rule #4).")
    ap.add_argument("--out", help="Write JSON report to this path (default: stdout).")
    ap.add_argument("--skip-gate", action="store_true", help="Skip K4 substrate gate (NOT recommended for cron).")
    args = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    report: dict = {
        "ts": now,
        "kernel": BASE,
        "tool_count": len(PROBES),
        "results": [],
        "dead": [],
        "suspicious": [],
        "healthy": True,
    }

    # K4 substrate gate
    if not args.skip_gate:
        ok, h = substrate_gate()
        report["substrate_gate"] = "PASS" if ok else "FAIL"
        report["substrate"] = h
        if not ok:
            report["healthy"] = False
            report["dead"].append("__substrate__")
            out = json.dumps(report, indent=1)
            (open(args.out, "w") if args.out else sys.stdout).write(out + "\n")
            return 2

    # Probe every tool
    for tool_name, args_dict in PROBES:
        t0 = time.monotonic()
        out = call_mcp(tool_name, args_dict)
        elapsed_ms = round((time.monotonic() - t0) * 1000, 1)
        verdict, classification = extract_verdict(out)
        result = {
            "tool": tool_name,
            "verdict": verdict,
            "classification": classification,
            "latency_ms": elapsed_ms,
        }
        report["results"].append(result)
        if classification == "DEAD":
            report["dead"].append(tool_name)
        elif classification == "SUSPICIOUS":
            report["suspicious"].append(tool_name)

    report["healthy"] = not report["dead"]
    report["exit_reason"] = (
        "all 8 tools responded" if report["healthy"]
        else f"dead tools: {report['dead']}"
    )

    out_str = json.dumps(report, indent=1)
    if args.out:
        with open(args.out, "w") as f:
            f.write(out_str + "\n")
    else:
        print(out_str)

    return 0 if report["healthy"] else 1


if __name__ == "__main__":
    sys.exit(main())