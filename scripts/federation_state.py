#!/usr/bin/env python3
"""Federation State Plane — canonical single-source-of-truth object.

Probes all federation sources, computes bottleneck, writes federation_state.json.
Read-only. No mutation. No new database. No orchestration changes.

Surfaces:
  1. /root/AAA/state/federation_state.json  (file)
  2. CRF augmentation (stdout text block)
  3. API: /api/state (via AAA backend)

Inputs:
  - cockpit_probe status.json (organ health, memory tiers, vault chain)
  - flow_health :7073 (FQ per-actor, verdict, diagnosis)
  - decision_ledger.jsonl (authority decisions)
  - forge_lease / forge_lock (execution leases)
  - direct health probes (fallback if status.json stale)

DITEMPA BUKAN DIBERI.
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ── Paths ──────────────────────────────────────────────────────────────

STATUS_JSON = Path("/root/AAA/state/status.json")
DECISION_LEDGER = Path("/root/AAA/state/decision_ledger.jsonl")
OUTPUT_JSON = Path("/root/AAA/state/federation_state.json")

# ── Config ─────────────────────────────────────────────────────────────

PROBE_TIMEOUT = 8  # seconds per endpoint (cold-start safe)
ORGAN_ENDPOINTS = [
    {"id": "arifos",   "port": 8088,  "role": "Kernel"},
    {"id": "a-forge",  "port": 7071,  "role": "Execution"},
    {"id": "aaa",      "port": 3001,  "role": "Control Plane"},
    {"id": "geox",     "port": 8081,  "role": "Earth Intelligence"},
    {"id": "wealth",   "port": 18082, "role": "Capital Intelligence"},
    {"id": "well",     "port": 18083, "role": "Vitality Mirror"},
    {"id": "arifflow", "port": 7073,  "role": "Metabolism"},
    {"id": "fed",      "port": 7074,  "role": "Model Router"},
]

# ── Probes ─────────────────────────────────────────────────────────────

def probe_health(port: int) -> dict:
    """Probe a single organ. Returns {healthy, latency_ms, data, failure_reason}."""
    url = f"http://127.0.0.1:{port}/health"
    t0 = time.monotonic()
    try:
        req = Request(url, headers={"User-Agent": "federation-state/1.0"})
        with urlopen(req, timeout=PROBE_TIMEOUT) as resp:
            ms = round((time.monotonic() - t0) * 1000, 1)
            body = json.loads(resp.read().decode())
            return {"healthy": resp.status == 200, "latency_ms": ms, "data": body, "failure_reason": None}
    except HTTPError as e:
        return {"healthy": False, "latency_ms": round((time.monotonic() - t0) * 1000, 1), "data": {}, "failure_reason": f"HTTP {e.code}"}
    except URLError as e:
        reason = str(e.reason) if hasattr(e, 'reason') else str(e)
        if "Connection refused" in reason or "ECONNREFUSED" in reason:
            return {"healthy": False, "latency_ms": round((time.monotonic() - t0) * 1000, 1), "data": {}, "failure_reason": "service_down"}
        elif "timed out" in reason.lower() or "timeout" in reason.lower():
            return {"healthy": False, "latency_ms": round((time.monotonic() - t0) * 1000, 1), "data": {}, "failure_reason": "timeout"}
        return {"healthy": False, "latency_ms": round((time.monotonic() - t0) * 1000, 1), "data": {}, "failure_reason": reason[:80]}
    except Exception as e:
        return {"healthy": False, "latency_ms": round((time.monotonic() - t0) * 1000, 1), "data": {}, "failure_reason": str(e)[:80]}


def probe_all_organs() -> list[dict]:
    """Probe all organs and return list of organ states."""
    results = []
    for organ in ORGAN_ENDPOINTS:
        p = probe_health(organ["port"])
        results.append({
            "id": organ["id"],
            "role": organ["role"],
            "port": organ["port"],
            "healthy": p["healthy"],
            "latency_ms": p["latency_ms"],
            "failure_reason": p["failure_reason"],
        })
    return results


def probe_flow_health() -> dict:
    """Get FQ state from arifFlow."""
    p = probe_health(7073)
    if not p["healthy"]:
        return {"verdict": "UNKNOWN", "quotient": None, "per_actor": {}}

    data = p["data"]
    fq = data.get("fq", {})

    # Extract per-actor summary (top-level fields only)
    per_actor = {}
    for actor_id, actor_data in fq.get("per_actor", {}).items():
        per_actor[actor_id] = {
            "verdict": actor_data.get("verdict", "UNKNOWN"),
            "quotient": actor_data.get("quotient"),
            "held": actor_data.get("held", False),
            "throttled": actor_data.get("throttled", False),
            "execute": actor_data.get("execute", 0),
            "verify": actor_data.get("verify", 0),
            "diagnosis": actor_data.get("diagnosis", ""),
        }

    # Count holds and throttles
    held_count = sum(1 for a in per_actor.values() if a["held"])
    throttled_count = sum(1 for a in per_actor.values() if a["throttled"])

    # Identify stuck actors
    stuck_actors = [aid for aid, a in per_actor.items() if a["verdict"] == "STUCK"]

    return {
        "verdict": fq.get("verdict", "UNKNOWN"),
        "quotient": fq.get("quotient"),
        "diagnosis": fq.get("diagnosis", ""),
        "execute_count": fq.get("execute_count", 0),
        "verify_count": fq.get("verify_count", 0),
        "held_count": held_count,
        "throttled_count": throttled_count,
        "stuck_actors": stuck_actors,
        "per_actor": per_actor,
    }


def probe_authority_state() -> dict:
    """Read decision_ledger for unresolved obligations. Returns None for unavailable sources (fail-closed)."""
    holds = None
    sabars = None
    seals = None
    ledger_available = False
    oldest_hold_ts = None
    oldest_hold_intent = None

    if DECISION_LEDGER.exists():
        try:
            holds = 0
            sabars = 0
            seals = 0
            with open(DECISION_LEDGER) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        verdict = d.get("verdict", "").upper()
                        ts = d.get("timestamp", "")
                        if verdict == "HOLD":
                            holds += 1
                            if oldest_hold_ts is None or ts < oldest_hold_ts:
                                oldest_hold_ts = ts
                                oldest_hold_intent = d.get("intent", "unknown")
                        elif verdict == "SABAR":
                            sabars += 1
                        elif verdict == "SEAL":
                            seals += 1
                    except json.JSONDecodeError:
                        pass
            ledger_available = True
        except Exception:
            pass  # holds/sabars/seals stay None = UNKNOWN

    # Compute age of oldest hold
    oldest_hold_hours = None
    if oldest_hold_ts:
        try:
            dt = datetime.fromisoformat(oldest_hold_ts.replace("Z", "+00:00"))
            age = datetime.now(timezone.utc) - dt
            oldest_hold_hours = round(age.total_seconds() / 3600, 1)
        except Exception:
            pass

    # Count held actors from flow (supplementary)
    flow = probe_health(7073)
    held_actors = []
    if flow["healthy"]:
        fq = flow["data"].get("fq", {})
        for aid, adata in fq.get("per_actor", {}).items():
            if adata.get("held"):
                held_actors.append(aid)

    return {
        "decision_ledger": {
            "holds": holds,
            "sabars": sabars,
            "seals": seals,
            "total": (holds or 0) + (sabars or 0) + (seals or 0) if holds is not None else None,
            "available": ledger_available,
        },
        "oldest_hold": {
            "age_hours": oldest_hold_hours,
            "intent": oldest_hold_intent,
        } if holds and holds > 0 else None,
        "flow_holds": {
            "count": len(held_actors),
            "actors": held_actors,
            "available": flow["healthy"],
        },
    }


def compute_bottleneck(organs: list[dict], authority: dict, fq: dict) -> dict:
    """Determine current federation bottleneck from available signals."""
    alive = sum(1 for o in organs if o["healthy"])
    total = len(organs)

    # Check for infrastructure failure first
    dead = [o["id"] for o in organs if not o["healthy"]]
    if dead:
        return {
            "type": "INFRASTRUCTURE",
            "severity": "CRITICAL" if len(dead) > 2 else "WARNING",
            "reason": f"{len(dead)} organs down: {', '.join(dead)}",
            "impact_flows": len(dead),
        }

    # Check authority debt — fail-closed: if source unavailable, report UNKNOWN not 0
    ledger = authority.get("decision_ledger", {})
    flow_holds = authority.get("flow_holds", {})
    ledger_holds = ledger.get("holds")
    flow_held_count = flow_holds.get("count", 0)
    flow_available = flow_holds.get("available", False)

    if ledger_holds is None and not flow_available:
        # Both authority sources unavailable — cannot determine bottleneck
        return {
            "type": "UNKNOWN",
            "severity": "WARNING",
            "reason": "Authority sources unavailable (ledger + arifFlow)",
            "impact_flows": 0,
        }

    holds = (ledger_holds or 0) + (flow_held_count or 0)
    if holds > 0:
        oldest = authority.get("oldest_hold", {})
        return {
            "type": "AUTHORITY",
            "severity": "WARNING" if holds > 5 else "INFO",
            "reason": f"{holds} unresolved holds",
            "oldest_hours": oldest.get("age_hours") if oldest else None,
            "oldest_intent": oldest.get("intent") if oldest else None,
            "impact_flows": holds,
        }

    # Check FQ state
    stuck = fq.get("stuck_actors", [])
    if stuck:
        return {
            "type": "METABOLISM",
            "severity": "WARNING",
            "reason": f"{len(stuck)} actors STUCK: {', '.join(stuck)}",
            "impact_flows": len(stuck),
        }

    # All clear
    return {
        "type": "NONE",
        "severity": "OK",
        "reason": "Federation flowing",
        "impact_flows": 0,
    }


def derive_health_verdict(organs: list[dict]) -> str:
    """Derive overall federation health from organ states."""
    alive = sum(1 for o in organs if o["healthy"])
    total = len(organs)
    if alive == total:
        return "SEAL"
    elif alive >= total - 1:
        return "DEGRADED"
    else:
        return "CRITICAL"


# ── Main ───────────────────────────────────────────────────────────────

def federation_state() -> dict:
    """Build the canonical federation state object."""
    t0 = time.monotonic()
    now = datetime.now(timezone.utc).isoformat()

    # Probe all sources
    organs = probe_all_organs()
    fq = probe_flow_health()
    authority = probe_authority_state()
    bottleneck = compute_bottleneck(organs, authority, fq)

    # Organ summary
    alive = sum(1 for o in organs if o["healthy"])
    total = len(organs)

    # Health verdict
    health = derive_health_verdict(organs)

    # Organ detail (compact)
    organ_detail = []
    for o in organs:
        detail = {
            "id": o["id"],
            "status": "UP" if o["healthy"] else "DOWN",
            "latency_ms": o["latency_ms"],
        }
        if not o["healthy"] and o.get("failure_reason"):
            detail["failure"] = o["failure_reason"]
        organ_detail.append(detail)

    state = {
        "version": 1,
        "generated_at": now,
        "probe_ms": round((time.monotonic() - t0) * 1000, 1),

        "federation": {
            "status": health,
            "organs_alive": alive,
            "organs_total": total,
            "organs": organ_detail,
        },

        "metabolism": {
            "verdict": fq.get("verdict", "UNKNOWN"),
            "quotient": fq.get("quotient"),
            "diagnosis": fq.get("diagnosis", ""),
            "execute_count": fq.get("execute_count", 0),
            "verify_count": fq.get("verify_count", 0),
            "held_count": fq.get("held_count", 0),
            "throttled_count": fq.get("throttled_count", 0),
            "stuck_actors": fq.get("stuck_actors", []),
        },

        "authority": {
            "holds": _safe_add(authority.get("decision_ledger", {}).get("holds"), authority.get("flow_holds", {}).get("count")),
            "seals": authority.get("decision_ledger", {}).get("seals"),  # None = UNKNOWN if ledger unavailable
            "oldest_hold": authority.get("oldest_hold"),
            "held_actors": authority.get("flow_holds", {}).get("actors", []),
        },

        "bottleneck": bottleneck,

        "_source": "federation_state.py v1.0",
    }

    return state


def render_crf_block(state: dict) -> str:
    """Render a CRF-compatible text block for terminal display."""
    fed = state["federation"]
    meta = state["metabolism"]
    auth = state["authority"]
    bn = state["bottleneck"]

    # Organ status line
    organ_parts = []
    for o in fed["organs"]:
        icon = "●" if o["status"] == "UP" else "○"
        organ_parts.append(f"{icon}{o['id']}")

    lines = [
        "═" * 72,
        f" FEDERATION STATE: {fed['status']}  |  Organs: {fed['organs_alive']}/{fed['organs_total']}  |  FQ: {meta.get('quotient', '?')} ({meta.get('verdict', '?')})",
        f" {' '.join(organ_parts)}",
    ]

    # Authority line (only if something is blocked)
    if auth["holds"] > 0:
        oldest = auth.get("oldest_hold")
        oldest_str = ""
        if oldest and oldest.get("age_hours"):
            oldest_str = f"  oldest: {oldest['age_hours']}h"
            if oldest.get("intent"):
                oldest_str += f" — {oldest['intent'][:40]}"
        lines.append(f" HOLDS: {auth['holds']}{oldest_str}")

    # Bottleneck line (only if not NONE)
    if bn["type"] != "NONE":
        lines.append(f" BOTTLENECK: {bn['type']} — {bn['reason']}")

    # Stuck actors (only if any)
    if meta.get("stuck_actors"):
        lines.append(f" STUCK: {', '.join(meta['stuck_actors'])}")

    lines.append("═" * 72)

    return "\n".join(lines)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "json"

    state = federation_state()

    if mode == "crf":
        # Terminal mode: print CRF block
        print(render_crf_block(state))
    elif mode == "write":
        # Write to file only (for cron)
        tmp = OUTPUT_JSON.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2))
        tmp.rename(OUTPUT_JSON)
        print(f"Written to {OUTPUT_JSON} ({state['probe_ms']}ms)")
    else:
        # JSON mode: print to stdout
        print(json.dumps(state, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
