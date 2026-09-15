#!/usr/bin/env python3
"""connectors.py — arrows to the organs that ALREADY exist.

F13 directive 2026-09-15: "Learning layers → organ yang DAH wujud (connect
arrows, bukan komponen baru)."

| Layer | Existing organ | This module's arrow |
|---|---|---|
| 1 Skill | live skills + weekly sweep (compression exists) | `skill_queue()` → skill-learn-ingest drain |
| 2 Pattern | `forge_experience_trace` · `forge_wm_gaps` · `forge_cool_pattern` | `experience_trace()` |
| 3 Governance | SCAR DB (`forge_scar` seal → `forge_scar_scan` consult) | `scar_consult()` |
| 4 Judgment | i-ARIF · musyawarah 333/555 · FED latency feedback | `proposals` (F13 queue) + `fq()` |

And the measurement Arif set as the condition for B to be real:

  "Setiap promotion event mesti feed forge_rsi_impulse_response (h(t)) +
   dual-rate FQ yang kau ratify Q1–Q6 … tanpa ini, B adalah teater."

So every promotion emits: a flow receipt (Verify + Execute) and an experience
trace. Then the loop READS BACK h(t) and governance FQ — the loop measured by an
independent observer (FRAME / A-FORGE), never by itself.

No new organ. No new store of truth. Arrows only.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone

AFORGE_MCP = "http://127.0.0.1:7072/mcp"
ARIFLOW = "http://127.0.0.1:7073"
FRAME = "http://127.0.0.1:18085/health"

ACTOR = "hermes-rsi-loop"
HTTP_TIMEOUT = 90


# ── MCP transport (A-FORGE) ──────────────────────────────────────────────────

def _mcp(method: str, params: dict | None = None, rid: int = 1, timeout: int = HTTP_TIMEOUT,
         attempts: int = 3):
    """MCP call with bounded backoff.

    A-FORGE's transport rate-limits bursts (HTTP 429). The loop's own verification
    traffic can throttle the loop's own measurement, which then reports None and
    looks like a dead instrument. Retry before believing the gap.
    """
    import time as _t
    last = None
    for n in range(attempts):
        try:
            body = json.dumps({"jsonrpc": "2.0", "id": rid, "method": method,
                               "params": params or {}}).encode()
            req = urllib.request.Request(AFORGE_MCP, data=body, headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read().decode()
            for line in raw.splitlines():
                if line.startswith("data: "):
                    raw = line[6:]
            return json.loads(raw)
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code not in (429, 503, 502):
                raise
            _t.sleep(2.0 * (n + 1))
        except Exception as exc:
            last = exc
            _t.sleep(1.0 * (n + 1))
    raise last if last else RuntimeError("mcp failed")


def _mcp_call(tool: str, args: dict) -> dict:
    """Returns {'ok': bool, 'data': ..., 'error': ...} — never raises."""
    try:
        _mcp("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                            "clientInfo": {"name": ACTOR, "version": "1.0"}}, 1)
        res = _mcp("tools/call", {"name": tool, "arguments": args}, 2)
        content = res.get("result", {}).get("content", [])
        text = content[0].get("text", "") if content else json.dumps(res)[:400]
        try:
            return {"ok": True, "data": json.loads(text)}
        except Exception:
            return {"ok": True, "data": text}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}", "tool": tool}


# ── arifFlow receipts (feeds dual-rate FQ) ───────────────────────────────────

def flow_receipt(step_type: str, step_number: int = 1, cost_ns: int = 0,
                 session_id: str = "hermes-rsi-loop",
                 epistemic_label: str = "Observation",
                 floor_verdict: str = "Pass",
                 intent_reason: str | None = None) -> dict:
    """POST /ingest — the ONLY way a receipt enters the live ledger.

    step_type must be 'Verify' or 'Execute': FQ = verify/execute is computed from
    exactly these two values, so writing anything else would silently not count.
    `cooling_decision` is required by the writer and must be one of
    None | Hold | Clamp | Bypass.
    """
    payload = {
        "receipt_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "actor_id": ACTOR,
        "session_id": session_id,
        "step_type": step_type,
        "step_number": step_number,
        "cost_ns": cost_ns,
        "risk_class": "T0Observe",
        "epistemic_label": epistemic_label,
        "floor_verdict": floor_verdict,
        "cooling_decision": "None",
        "previous_receipt_hash": None,
        "jcs_body_hash": None,
        "topology_id": None,
        "lane_id": None,
        "session_token": None,
        "preceding_verify_cost_ns": None,
        "intent_reason": intent_reason,
    }
    req = urllib.request.Request(f"{ARIFLOW}/ingest", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return {"ok": True, "data": json.loads(r.read().decode())}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "error": f"HTTP {exc.code}: {exc.read().decode()[:200]}"}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


def fq() -> dict:
    """The loop's own flow quotient, as arifFlow sees it."""
    try:
        with urllib.request.urlopen(f"{ARIFLOW}/health", timeout=10) as r:
            d = json.loads(r.read().decode())
        return {"ok": True, "fq": d.get("fq", d)}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


# ── experience traces (feeds h(t)) ───────────────────────────────────────────

def experience_trace(atom: dict, receipt: dict, outcome: dict) -> dict:
    """Layer 2 arrow: record the promotion as an experience trace.

    `new_skill` is what makes the trace detectable as an impulse event — h(t)
    cannot measure a fix it cannot see.
    """
    applied = bool(outcome.get("applied"))
    return _mcp_call("forge_experience_trace", {
        "agent_id": ACTOR,
        "tool": "forge_rsi_promotion",
        "input_summary": f"{atom['pattern_type']} atom {atom['atom_id']} "
                         f"(layer={atom['layer']}, freq={atom['frequency']})",
        "output_summary": outcome.get("action", "?") + (
            f" → {outcome.get('target')}" if outcome.get("target") else
            f" ({outcome.get('reason', '')})"),
        "success": bool(receipt.get("passed")),
        "feedback_self": atom.get("claim", "")[:300],
        "feedback_environmental": f"verifier checks: {receipt.get('failed_checks') or 'all passed'}",
        "feedback_constitutional": "PASS" if applied else "HOLD",
        "capability_change": 0.05 if applied else 0.0,
        "confidence_change": 0.02 if receipt.get("passed") else -0.05,
        "new_skill": (atom.get("target") or atom["pattern_type"]).lower() if applied else None,
        "new_scar": None,
    })


# ── measurement (the condition for B to be real) ─────────────────────────────

def measurement(window_days: int = 30) -> dict:
    """Read h(t) + dual-rate FQ from A-FORGE. Independent, never self-computed.

    A failed read is reported as an ERROR, never as None: a measurement that
    silently returns nothing is indistinguishable from a measurement that says
    zero, and that is exactly the failure mode this loop exists to catch.
    """
    h = _mcp_call("forge_rsi_impulse_response", {"window_days": window_days})
    f = _mcp_call("forge_rsi_dual_rate_fq", {"min_governance_samples": 10})
    out = {"read_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")}
    if h.get("ok") and isinstance(h.get("data"), dict):
        d = h["data"]
        out["h_t"] = {
            "impulse_events": d.get("total_impulse_events"),
            "samples_with_influence": d.get("samples_with_influence"),
            "median_half_life_sessions": d.get("median_half_life_sessions"),
            "h_characterized": d.get("h_characterized"),
            "by_event_type": d.get("by_event_type"),
        }
    else:
        out["h_t"] = {"STATUS": "UNREADABLE", "error": h.get("error")}
    if f.get("ok") and isinstance(f.get("data"), dict):
        d = f["data"]
        out["fq"] = {
            "daily": d.get("daily_fq"),
            "governance_7d": d.get("governance_fq"),
            "window_count": d.get("governance_window_count"),
            "sufficient": d.get("governance_window_sufficient"),
        }
    else:
        out["fq"] = {"STATUS": "UNREADABLE", "error": f.get("error")}
    out["readable"] = (out["h_t"].get("STATUS") != "UNREADABLE"
                       and out["fq"].get("STATUS") != "UNREADABLE")
    return out


def scar_consult(patterns: list[str]) -> dict:
    """Layer 3 arrow: consult the SCAR DB before promoting (existing organ)."""
    return _mcp_call("forge_scar_scan", {"patterns": patterns, "mode": "consult"})


def wm_gaps(limit: int = 20) -> dict:
    """Layer 2 arrow: surprise scoring — what the world model did NOT predict."""
    return _mcp_call("forge_wm_gaps", {"limit": limit})


def cool_pattern(recurrence: int = 3) -> dict:
    """Layer 2/3 arrow: existing recurrence → cooling receipt machinery."""
    return _mcp_call("forge_cool_pattern", {"recurrence_count": recurrence,
                                            "window_days": 90})


def frame_health() -> dict:
    try:
        with urllib.request.urlopen(FRAME, timeout=8) as r:
            return {"ok": True, "data": json.loads(r.read().decode())}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


if __name__ == "__main__":
    print("=== frame ===");      print(json.dumps(frame_health(), indent=1)[:300])
    print("=== flow fq ===");    print(json.dumps(fq(), indent=1)[:400])
    print("=== measurement ==="); print(json.dumps(measurement(), indent=1))
    print("=== wm_gaps ===");    print(json.dumps(wm_gaps(5), indent=1)[:500])
