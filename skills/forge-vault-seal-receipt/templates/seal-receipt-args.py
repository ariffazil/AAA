#!/usr/bin/env python3
"""
seal-receipt-args.py — Template for crafting forge_vault(mode="receipt") arguments.

Use this when sealing a session that produced:
  - A code patch (branch + commit + files)
  - A probe or audit result
  - A fix or refactor
  - An openclaw/opencode/codex session

The script builds a canonical args dict, validates required fields,
and prints the JSON-RPC call. Drop the dict into the MCP call.

NOTE: forge_vault is F13-gated — non-SOVEREIGN actors get -32042.
This template is for SOVEREIGN actors (Arif, actor_id="ARIF").
"""

import json

def build_seal_args(
    session_label: str,
    actor_id: str,
    intent: str,
    summary: str,
    domain: str,
    delta_s: str = "<= 0",
    patch_ref: dict | None = None,
    test_result: str | None = None,
    live_status: str | None = None,
    evidence: str | None = None,
    open_loops: list[str] | None = None,
    out_of_scope: list[str] | None = None,
) -> dict:
    """Build canonical forge_vault(mode='receipt') arguments.

    Required: session_label, actor_id, intent, summary, domain.
    """

    if not session_label or not actor_id or not intent or not summary or not domain:
        raise ValueError("session_label, actor_id, intent, summary, domain are required")

    args = {
        "mode": "receipt",
        "session_label": session_label,
        "actor_id": actor_id,
        "intent": intent,
        "summary": summary,
        "domain": domain,
        "delta_s": delta_s,
    }

    if patch_ref:
        args["patch_ref"] = patch_ref
    if test_result:
        args["test_result"] = test_result
    if live_status:
        args["live_status"] = live_status
    if evidence:
        args["evidence"] = evidence
    if open_loops:
        args["open_loops"] = open_loops
    if out_of_scope:
        args["out_of_scope"] = out_of_scope

    return args


def build_jsonrpc_call(tool: str, args: dict, request_id: int = 99) -> dict:
    """Wrap args in a JSON-RPC tools/call envelope."""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": tool,
            "arguments": args
        }
    }


# === USAGE EXAMPLE (WEALTH patch 2026-08-08) ===

if __name__ == "__main__":
    args = build_seal_args(
        session_label="wea-seal-2026-08-08",
        actor_id="ARIF",
        intent="SEAL session close — WEALTH capital_entropy 4-bug fix (F1/F2/F3/F4) complete",
        summary=(
            "WEALTH capital_entropy 4-bug fix sealed. "
            "F1: CoercedDictListStrict applied to 7 CoercedDictList fields. "
            "F2: shadow=True now suppresses vault writes via arguments.shadow check at _emit_receipt. "
            "F3: kappa_r derived from evidence_quality enum (was hardcoded 0.93). "
            "F4: metric_purpose_audit routes through _wrap_entropy. "
            "Tests: 14/14 PASS. OpenClaw peer audit caught 3 architectural bugs in initial Kimi patch — all fixed."
        ),
        domain="wealth",
        delta_s="<= 0 (4 bugs fixed, 0 surface added)",
        patch_ref={
            "branch": "fix/differential-power-consequence-map",
            "commit": "317651e",
            "worktree": "/tmp/wealth-fix-85LHzT",
            "live": "/root/WEALTH unchanged",
            "files": [
                "wealth_mcp/tools/canonical.py (+27 lines)",
                "wealth_mcp/server.py (+25 lines)",
                "wealth_contracts/envelope.py (+17 lines)",
                "tests/test_capital_entropy_bugfixes.py (+146 lines, 14/14 PASS)"
            ]
        },
        test_result="14/14 PASS",
        live_status="worktree-only, awaiting F13 SEAL to deploy",
        evidence=(
            "Live WEALTH :18082 healthy (8 tools, session handshake confirmed). "
            "Worktree pytest 14/14 PASS in /tmp/wealth-fix-85LHzT/. "
            "OpenClaw peer audit via gateway :18789."
        ),
        open_loops=[
            "F5/F6 (A-FORGE hardcoded path /root/A-FORGE/forge_work/2026-07-17/, ~200 PermissionError warnings/day) — not in scope"
        ],
        out_of_scope=[
            "Investbrain integration (Path A vs B) — pending Arif decision",
            "Receipt pollution cleanup (88 probe receipts marked with PROBE_MARKER)"
        ]
    )

    call = build_jsonrpc_call("forge_vault", args)

    print(json.dumps(call, indent=2)[:2000])
    print(f"\n... (truncated, total {len(json.dumps(call))} chars)")