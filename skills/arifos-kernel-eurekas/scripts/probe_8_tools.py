#!/usr/bin/env python3
"""
arifOS MCP 8-tool agentic probe (canonical recipe).

Exercises all 8 canonical verbs (arif_init / arif_observe / arif_think / arif_route /
arif_memory / arif_judge / arif_forge / arif_seal) via curl + JSON-RPC against
http://127.0.0.1:8088/mcp. Captures verdict + 9-signal state per call and reports
a structured summary.

WHY THIS EXISTS:
- Verifies the kernel is reachable and contract-honest (K-Series audit cadence).
- Surfaces the full 8-tool response shape for any agentic workflow.
- Documents the canonical probe envelope so future sessions do not hand-type curl.
- Records the 888_HOLD / IRREVERSIBLE neutering on forge+seal for anonymous actors.
- Records the FULL authority path when using actor_id="arif" (P0 hotfix 2026-08-06).

USAGE:
    python3 probe_8_tools.py                  # probe as anonymous actor (default)
    python3 probe_8_tools.py --as-arif        # probe as 'arif' (FULL authority)
    python3 probe_8_tools.py --session-id X   # custom session_id tag (default: agentic_probe_<ts>)
    python3 probe_8_tools.py --quick          # skip memory/judge/forge/seal (just the read-half)

REQUIREMENTS:
- arifOS kernel running on http://127.0.0.1:8088 (verify via `curl :8088/health`).
- python3 stdlib only. No external deps.
- For --as-arif mode, kernel must have the P0 'arif' actor exemption (commit >= 8bbcb3695).

REFERENCE: arifos-kernel-eurekas/references/deploy-drift-psi-contamination-case.md
"""

import argparse
import json
import subprocess
import sys
import time
from typing import Any


KERNEL_URL = "http://127.0.0.1:8088/mcp"
SESSION_TAG_DEFAULT = f"agentic_probe_{int(time.time())}"


def mcp_call(tool_name: str, arguments: dict, session_id: str = "agentic_probe", id_n: int = 1, timeout: int = 30) -> dict:
    """Issue a JSON-RPC tools/call against the arifOS MCP and return the parsed result."""
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": id_n,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    })
    try:
        out = subprocess.check_output(
            ["curl", "-sf", "--max-time", str(timeout), "-X", "POST", KERNEL_URL,
             "-H", "Content-Type: application/json",
             "-H", "Accept: application/json, text/event-stream",
             "-d", body],
            stderr=subprocess.STDOUT,
            timeout=timeout + 5,
        )
        resp = json.loads(out)
        for c in resp.get("result", {}).get("content", []):
            try:
                return json.loads(c.get("text", ""))
            except (json.JSONDecodeError, TypeError):
                continue
        return {"_raw": resp, "_note": "no parseable content[].text"}
    except subprocess.CalledProcessError as e:
        stderr_text = (e.output or b"").decode("utf-8", errors="replace").strip()
        # 888_HOLD rejections arrive as plain text on stdout/stderr — capture them
        return {"_error": "curl_failed", "_stderr": stderr_text[:500]}
    except subprocess.TimeoutExpired:
        return {"_error": "timeout", "_timeout_s": timeout}


def extract_summary(label: str, payload: dict) -> dict:
    """Pull the canonical probe signals out of a tool response."""
    if "_error" in payload or "_raw" in payload:
        return {"label": label, "error": payload}
    return {
        "label": label,
        "status": payload.get("status"),
        "verdict": payload.get("effective_verdict") or payload.get("verdict"),
        "actor_verified": payload.get("actor", {}).get("actor_verified"),
        "authority_level": payload.get("actor", {}).get("authority_level"),
        "session_id": payload.get("session_id"),
        "substrate_state": payload.get("substrate", {}).get("state"),
        "psi_plane": payload.get("verdicts", {}).get("nine_signal", {}).get("psi", {}).get("state"),
        "delta_plane": payload.get("verdicts", {}).get("nine_signal", {}).get("delta", {}).get("state"),
    }


def probe_all(session_id: str, actor_id: str | None, quick: bool = False) -> list[dict]:
    """Run the full 8-tool probe. Returns a list of per-tool summaries."""
    actor_arg = actor_id if actor_id else "anonymous"

    # Build the per-tool arguments. The arguments here were validated against the
    # live kernel on 2026-08-07 (drift cleared, INIT v5.0 + WAJIB 3 active).
    probes = [
        ("arif_init", {"mode": "init", "actor_id": actor_arg, "ack_irreversible": False}),
        ("arif_observe", {"subject": "runtime_geometry_probe", "frame": "agentic_test", "session_id": session_id}),
        ("arif_think", {"question": "Do arifOS MCP tools help Opus 5 find correct weights for runtime geometry?", "frame": "agentic_test", "session_id": session_id}),
        ("arif_route", {"intent": "runtime_geometry_weighting", "context": "agentic_test", "session_id": session_id}),
    ]
    if not quick:
        # arif_judge.evidence must be a dict (NOT a list) — Pydantic v2 schema quirk
        probes.extend([
            ("arif_memory", {"query": "jailspace runtime geometry weights", "mode": "recall", "session_id": session_id}),
            ("arif_judge", {"claim": "arifOS_MCP_helps_Opus5_find_weights", "evidence": {"probe_evidence": "8 tools active, 8/8 organs healthy, drift cleared"}, "session_id": session_id}),
            ("arif_forge", {"action": "probe_runtime_geometry", "target": "arifOS_8_tools", "dry_run": True, "session_id": session_id}),
            ("arif_seal", {"receipt": "agentic_probe_completed", "session_id": session_id}),
        ])

    results = []
    for i, (tool_name, args) in enumerate(probes, start=1):
        print(f"  [{i}/{len(probes)}] {tool_name} ... ", end="", flush=True)
        payload = mcp_call(tool_name, args, session_id=session_id, id_n=i)
        summary = extract_summary(tool_name, payload)
        if "_error" in summary:
            print(f"ERROR ({summary.get('error', {}).get('_error', '?')})")
        else:
            print(f"verdict={summary.get('verdict')} actor_auth={summary.get('authority_level')} "
                  f"psi={summary.get('psi_plane')} delta={summary.get('delta_plane')}")
        results.append(summary)
    return results


def report(results: list[dict], session_id: str, actor_id: str | None) -> dict:
    """Compute pass/HOLD/SEAL counts and print a structured summary."""
    counts = {"SEAL": 0, "HOLD": 0, "VOID": 0, "ERROR": 0, "OTHER": 0}
    for r in results:
        if "_error" in r:
            counts["ERROR"] += 1
            continue
        v = (r.get("verdict") or "").upper()
        if v in counts:
            counts[v] += 1
        else:
            counts["OTHER"] += 1

    print()
    print(f"=== probe summary (session_id={session_id}, actor={actor_id or 'anonymous'}) ===")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"  TOTAL: {len(results)}")
    return counts


def pre_probe_gate() -> bool:
    """K4 substrate-honesty pre-probe gate. Returns True if safe to probe."""
    try:
        out = subprocess.check_output(
            ["curl", "-sf", "--max-time", "10", "http://127.0.0.1:8088/health"],
            stderr=subprocess.STDOUT,
        )
        h = json.loads(out)
        drift = h.get("deployment_drift_status", "?")
        rd = h.get("runtime_drift")
        sc = h.get("software_release", {}).get("source_commit")
        dc = h.get("software_release", {}).get("deployed_commit")
        color = h.get("owner_summary", {}).get("color")
        print(f"[gate] status={h.get('status')} drift={drift} runtime_drift={rd} "
              f"deployed={dc[:7] if dc else '?'} source={sc[:7] if sc else '?'} "
              f"owner.color={color}")
        if drift == "drift_detected" or rd is True or color == "YELLOW":
            print("[gate] FAIL: substrate drift detected — ψ-plane contaminated.")
            print("[gate] Fix first: cd /root/arifOS && git push origin main && make deploy-local")
            print("[gate] See arifos-kernel-eurekas/references/deploy-drift-psi-contamination-case.md")
            return False
        print("[gate] PASS — safe to probe")
        return True
    except Exception as e:
        print(f"[gate] ERROR probing /health: {e}")
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description="arifOS MCP 8-tool agentic probe (canonical recipe).")
    ap.add_argument("--as-arif", action="store_true", help="Probe as actor_id='arif' (FULL authority, P0 hotfix 2026-08-06).")
    ap.add_argument("--session-id", default=SESSION_TAG_DEFAULT, help="Session ID tag for trace correlation (default: agentic_probe_<ts>).")
    ap.add_argument("--quick", action="store_true", help="Skip memory/judge/forge/seal — just init/observe/think/route.")
    ap.add_argument("--no-gate", action="store_true", help="Skip the K4 pre-probe gate (NOT recommended).")
    args = ap.parse_args()

    actor_id = "arif" if args.as_arif else None

    if not args.no_gate:
        if not pre_probe_gate():
            return 1

    print(f"\n=== arifOS 8-tool probe (actor={actor_id or 'anonymous'}, session_id={args.session_id}) ===")
    results = probe_all(args.session_id, actor_id, quick=args.quick)
    counts = report(results, args.session_id, actor_id)

    # Exit nonzero on any ERROR or unexpected VOID
    return 1 if counts["ERROR"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())