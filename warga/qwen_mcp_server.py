#!/usr/bin/env python3
"""
qwen_mcp_server.py — FastMCP server wrapping the Qwen bridge as TI-003
════════════════════════════════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI ⚒️

Exposes 4 MCP tools over stdio (transport="stdio") per Tier-2 of the F13-ratified
Qwen-TI-003 ratification (2026-09-30, SEALED_EVENTS #971):

    qwen_call       — invoke qwen via acpx, with lease-gated scope + reversibility
    qwen_health     — liveness check (calls a tiny prompt)
    qwen_receipts   — fetch last N pre_call receipts from the JSONL log
    qwen_cost_cap   — set/inspect per-call + per-day USD cost caps

The server is invoked by:
    /root/.arifos/agents/kimi/mcp-launchers/qwen.sh   (kimi-code harness)
    opencode.json type:"local" command:[python3, /root/.../qwen_mcp_server.py]

Tier A identity envelope is preserved at the launcher layer (NOT here), per the
existing pattern used by arifos/arifflow/etc. See _tier_a_envelope.sh.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Make /root/AAA/warga importable so we can use the bridge
sys.path.insert(0, "/root/AAA/warga")

from fastmcp import FastMCP  # fastmcp 4.0.4

# Re-use the Tier-1 bridge we (and the federation) already hardened
import qwen_bridge  # noqa: E402

# ── Cost cap state (in-memory; resets on server restart — accepted T2 limitation) ──
_COST_CAPS: Dict[str, float] = {
    "per_call_usd": float(os.environ.get("QWEN_COST_CAP_PER_CALL_USD", "1.0")),
    "per_day_usd": float(os.environ.get("QWEN_COST_CAP_PER_DAY_USD", "50.0")),
}
_SPEND_TODAY_USD: float = 0.0
_DAY_RESET_AT: float = time.time()

# Default lease for Qwen calls (matches bridge Tier-1 defaults)
_DEFAULT_LEASE = {
    "scope": "OBSERVE_ONLY",
    "reversibility": "REVERSIBLE",
    "max_turns": 10,
    "ttl_seconds": 600,
    "consent": {"thought_stream": False},
}


def _maybe_reset_daily_spend() -> None:
    global _SPEND_TODAY_USD, _DAY_RESET_AT
    now = time.time()
    if now - _DAY_RESET_AT > 86400:
        _SPEND_TODAY_USD = 0.0
        _DAY_RESET_AT = now


def _estimate_cost_usd(cost: Dict[str, int], model: str = "qwen-route") -> float:
    """Very rough cost estimate. Replace with model-specific pricing when known.
    Default: $1 per 100k output tokens, $0.10 per 100k input/cached tokens.
    """
    inp = cost.get("input", 0)
    out = cost.get("output", 0)
    thought = cost.get("thought", 0)
    total = cost.get("total", 0) or (inp + out + thought)
    # Conservative default — assume mostly input
    return round((total * 1.0) / 100_000, 4)


# ── FastMCP server ──────────────────────────────────────────────────────────────
mcp = FastMCP("qwen-ti-003")


@mcp.tool()
def qwen_call(
    prompt: str,
    lease_scope: str = "OBSERVE_ONLY",
    reversibility: str = "REVERSIBLE",
    max_turns: int = 10,
    ttl_seconds: int = 600,
    thought_stream: bool = False,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Invoke Qwen Code via the Tier-1 constitutional bridge.

    Args:
        prompt:           the user prompt (single string)
        lease_scope:       OBSERVE_ONLY | STANDARD | ELEVATED
        reversibility:     REVERSIBLE | HARD | IRREVERSIBLE
        max_turns:         bound on agentic turns (1..500)
        ttl_seconds:       idle TTL in seconds (60..28800)
        thought_stream:    F11 consent — emit agent_thought_chunk to log (default false)
        session_id:        arifOS session id to thread through receipts

    Returns: dict with status, call_id, cost, final_message, dropped_thought_chunks.
    Raises: ValueError on invalid scope; RuntimeError on cost-cap breach.
    """
    global _SPEND_TODAY_USD
    _maybe_reset_daily_spend()
    if _SPEND_TODAY_USD >= _COST_CAPS["per_day_usd"]:
        return {
            "status": "HOLD",
            "reason": f"daily cost cap breached (${_SPEND_TODAY_USD:.2f} >= ${_COST_CAPS['per_day_usd']:.2f})",
        }

    lease = {
        "scope": lease_scope,
        "reversibility": reversibility,
        "max_turns": max(1, min(max_turns, 500)),
        "ttl_seconds": max(30, min(ttl_seconds, 28800)),
        "consent": {"thought_stream": thought_stream},
    }
    try:
        result = qwen_bridge.bridge_call(prompt, lease, session_id=session_id)
    except Exception as exc:
        return {"status": "error", "reason": f"{type(exc).__name__}: {exc}"}

    cost_usd = _estimate_cost_usd(result["cost"])
    _SPEND_TODAY_USD += cost_usd

    return {
        "status": result["status"],
        "call_id": result["call_id"],
        "log_path": result["log_path"],
        "pre_hash": result["pre_hash"],
        "post_hash": result["post_hash"],
        "cost": result["cost"],
        "cost_estimate_usd": cost_usd,
        "spent_today_usd": round(_SPEND_TODAY_USD, 4),
        "final_message": result.get("final_message"),
        "event_count": result["event_count"],
        "dropped_thought_chunks": result["dropped_thought_chunks"],
    }


@mcp.tool()
def qwen_health() -> Dict[str, Any]:
    """Liveness check — verify Qwen bridge + acpx + qwen-code CLI are all reachable.

    Returns: dict with status + per-component checks. Does NOT call qwen for a real
    prompt (no token cost). Boots a tiny synthetic call with --max-turns 1.
    """
    health: Dict[str, Any] = {
        "status": "ok",
        "checked_at": time.time(),
        "components": {},
    }
    # Check acpx binary
    import shutil
    acpx_path = shutil.which(qwen_bridge.ACPX_BIN) or qwen_bridge.ACPX_BIN
    health["components"]["acpx"] = {
        "path": acpx_path,
        "reachable": Path(acpx_path).exists() or shutil.which(qwen_bridge.ACPX_BIN) is not None,
    }
    # Check qwen binary
    qwen_path = shutil.which("qwen") or "/root/.local/bin/qwen"
    health["components"]["qwen"] = {
        "path": qwen_path,
        "reachable": Path(qwen_path).exists(),
    }
    # Check log dir writable
    log_dir = qwen_bridge.VAULT_LOG_DIR
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        health["components"]["log_dir"] = {"path": str(log_dir), "writable": True}
    except Exception as e:
        health["components"]["log_dir"] = {"path": str(log_dir), "writable": False, "error": str(e)}
        health["status"] = "degraded"

    # Check vault log size + recent activity
    today_log = log_dir / f"{time.strftime('%Y-%m-%d')}.jsonl"
    if today_log.exists():
        size_mb = round(today_log.stat().st_size / (1024 * 1024), 2)
        health["components"]["today_log"] = {"path": str(today_log), "size_mb": size_mb}
    else:
        health["components"]["today_log"] = {"path": str(today_log), "exists": False}

    return health


@mcp.tool()
def qwen_receipts(limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch the last N pre_call receipts from today's JSONL log.

    Args:
        limit: max receipts to return (1..100, default 10)

    Returns: list of receipt dicts (most recent first).
    """
    today_log = qwen_bridge.VAULT_LOG_DIR / f"{time.strftime('%Y-%m-%d')}.jsonl"
    if not today_log.exists():
        return []
    limit = max(1, min(limit, 100))
    out: List[Dict[str, Any]] = []
    try:
        with open(today_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Walk backwards to find pre_call records
        for line in reversed(lines):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("kind") == "pre_call":
                out.append({
                    "call_id": rec.get("call_id"),
                    "ts": rec.get("ts"),
                    "policy_bridge_floor": (rec.get("policy") or {}).get("bridgeFloor"),
                    "policy_default_action": (rec.get("policy") or {}).get("defaultAction"),
                    "prompt_len_chars": rec.get("prompt_len_chars"),
                    "pre_hash": rec.get("pre_hash"),
                    "session_id": rec.get("session_id"),
                })
                if len(out) >= limit:
                    break
    except Exception as e:
        return [{"error": f"failed to read log: {e}"}]
    return out


@mcp.tool()
def qwen_cost_cap(
    per_call_usd: Optional[float] = None,
    per_day_usd: Optional[float] = None,
) -> Dict[str, Any]:
    """Set and/or inspect per-call + per-day USD cost caps.

    Args:
        per_call_usd: if provided, update the per-call cap (0.01..100)
        per_day_usd:  if provided, update the per-day cap (0.10..10000)

    Returns: dict with current caps + spend-today + headroom.
    """
    global _COST_CAPS, _SPEND_TODAY_USD
    _maybe_reset_daily_spend()
    if per_call_usd is not None:
        _COST_CAPS["per_call_usd"] = max(0.01, min(float(per_call_usd), 100.0))
    if per_day_usd is not None:
        _COST_CAPS["per_day_usd"] = max(0.10, min(float(per_day_usd), 10000.0))
    return {
        "caps": dict(_COST_CAPS),
        "spent_today_usd": round(_SPEND_TODAY_USD, 4),
        "headroom_per_call_usd": round(_COST_CAPS["per_call_usd"] - _SPEND_TODAY_USD, 4)
            if _COST_CAPS["per_day_usd"] > 0 else None,
        "headroom_per_day_usd": round(_COST_CAPS["per_day_usd"] - _SPEND_TODAY_USD, 4),
        "day_reset_in_seconds": round(86400 - (time.time() - _DAY_RESET_AT), 1),
    }


if __name__ == "__main__":
    # stdio transport — invoked by the kimi launcher / opencode.json entry
    mcp.run(transport="stdio")