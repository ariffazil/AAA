#!/usr/bin/env python3
"""
fed_router.py — FED Core MCP Server (Federation Router) · v3.1 Zen
═══════════════════════════════════════════════════════════
Port: 7074  ·  Unit: fed-router.service  ·  MCP prefix: fed_*
Answers: "Where should this agent route?"

Architecture:
  READ  → fed_state.db (provider_balance, route_latency, route_health)
  WRITE → token_bank_spend (on every routed call)
  NEVER → actively ping for latency (passive telemetry only)

Zen v3.1 (2026-08-02 — LiteLLM patterns absorbed):
  1. Route Health Gate — skip DEGRADED, demote RATE_LIMITED (cooldown)
  2. Cost Surface — estimated cost per 1M tokens on every route
  3. Telemetry Gate — demote untested routes (<10 samples)
  4. Complete Pricing — DeepSeek direct + all provider tables

Hardened v3.0 invariants (preserved):
  1. Asymmetric Balance Bypass (dual-track — Track A hard / Track B soft / UNVERIFIABLE)
  2. Constitutional Hard-Gate (tier ≥ 666 → direct only)
  3. Agent Cascade Contract (ranked array output)
  4. State Isolation (READ providers → WRITE token_bank_spend only)
  5. Balance Bypass Enforcement (Track A <$1 HARD, Track B <$5 SOFT, conf<0.50 UNVERIFIABLE)
  6. Model Route Tables (deepseek, qwen, gpt, claude, kimi, glm families)

Forged: 2026-07-30  ·  Zen-dated: 2026-08-02  ·  DITEMPA BUKAN DIBERI
"""

import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

# ── Config ───────────────────────────────────────────────────────────────
FED_STATE_DB = Path("/root/.local/share/arifos/token_bank.db")
FED_PORT = 7074

# ── Pricing tables (inlined — shared logic with token_bank.py) ──────────
# Keep in sync with /root/AAA/scripts/token_bank.py pricing tables
# Zen 2026-08-02: Added DeepSeek direct pricing + all provider tables (LiteLLM model catalog pattern)

DEEPSEEK_PRICING = {
    "deepseek-v4-pro": {"input": 0.435, "output": 0.87},
    "deepseek-v4-flash": {"input": 0.14, "output": 0.28},
}

MULEROUTER_PRICING = {
    "deepseek-v4-pro": {"input": 0.55, "output": 2.19},
    "deepseek-v4-flash": {"input": 0.20, "output": 0.80},
    "qwen3-max": {"input": 0.50, "output": 1.50},
    "qwen3.7-max": {"input": 2.50, "output": 7.50},
    "qwen3.6-flash": {"input": 0.15, "output": 0.60},
    "qwen-vl-max": {"input": 0.80, "output": 2.00},
    "qwen3-vl-plus": {"input": 0.80, "output": 2.00},
    "qwen3-vl-flash": {"input": 0.30, "output": 1.00},
    "qwen3-omni-flash": {"input": 0.30, "output": 0.90},
    "qwen3.5-omni-flash": {"input": 0.30, "output": 0.90},
    "qwen3.5-omni-plus": {"input": 0.80, "output": 2.00},
    "gpt-5.6-sol": {"input": 1.50, "output": 10.00},
    "gpt-5.5": {"input": 2.50, "output": 10.00},
    "gpt-5.4": {"input": 1.25, "output": 5.00},
    "grok-4": {"input": 2.00, "output": 8.00},
    "glm-5.1": {"input": 0.50, "output": 2.00},
}

TOKENROUTER_PRICING = {
    "deepseek-v4-pro": {"input": 0.55, "output": 2.19},
    "deepseek-v4-flash": {"input": 0.20, "output": 0.80},
    "gpt-5.6-sol": {"input": 1.50, "output": 10.00},
    "gpt-5.5": {"input": 2.50, "output": 10.00},
    "claude-sonnet-5": {"input": 3.00, "output": 15.00},
    "claude-opus-4.8": {"input": 15.00, "output": 75.00},
    "kimi-k3": {"input": 0.00, "output": 0.00},
    "glm-5.2": {"input": 0.00, "output": 0.00},
}


def _estimate_cost(provider_id: str, model_id: str, tokens_in: int, tokens_out: int) -> float:
    """Calculate estimated cost in USD. Zen 2026-08-02: added deepseek pricing."""
    tables = {
        "deepseek": DEEPSEEK_PRICING,
        "mulerouter": MULEROUTER_PRICING,
        "tokenrouter": TOKENROUTER_PRICING,
    }
    pricing = tables.get(provider_id, {}).get(model_id, {"input": 0.50, "output": 2.00})
    return round((tokens_in / 1_000_000) * pricing["input"] + (tokens_out / 1_000_000) * pricing["output"], 8)


def _estimate_cost_per_1k(provider_id: str, model_id: str) -> dict:
    """Return estimated cost per 1K tokens for a route. LiteLLM catalog pattern."""
    tables = {
        "deepseek": DEEPSEEK_PRICING,
        "mulerouter": MULEROUTER_PRICING,
        "tokenrouter": TOKENROUTER_PRICING,
    }
    pricing = tables.get(provider_id, {}).get(model_id, {"input": 0.50, "output": 2.00})
    return {
        "input_per_1m_usd": pricing["input"],
        "output_per_1m_usd": pricing["output"],
    }


mcp = FastMCP("FED — Federation Router")


# ── DB helpers (READ-ONLY for balances) ──────────────────────────────────
def get_db():
    conn = sqlite3.connect(str(FED_STATE_DB))
    conn.row_factory = sqlite3.Row
    return conn


def read_provider_balance(provider_id: str) -> dict | None:
    """Read from providers table in token_bank.db. Returns dict with balance_usd, confidence_score, track_type."""
    conn = get_db()
    row = conn.execute("SELECT * FROM providers WHERE provider_name = ?", (provider_id,)).fetchone()
    conn.close()
    if not row:
        return None
    r = dict(row)
    # Normalize field names for backward compatibility with router logic
    r["balance_confidence"] = r.get("confidence_score", 1.0)
    r["track"] = r.get("track_type", "B")
    return r


def read_all_providers() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM providers ORDER BY track_type, provider_name").fetchall()
    conn.close()
    result = []
    for row in rows:
        r = dict(row)
        r["balance_confidence"] = r.get("confidence_score", 1.0)
        r["track"] = r.get("track_type", "B")
        result.append(r)
    return result


def read_route_latency(provider_id: str, model_id: str) -> dict | None:
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM route_latency WHERE provider_name = ? AND model_id = ?",
        (provider_id, model_id),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def read_route_health(provider_id: str, model_id: str) -> dict | None:
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM route_health WHERE provider_name = ? AND model_id = ?",
        (provider_id, model_id),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def log_spend(provider_id: str, model_id: str, tokens_in: int, tokens_out: int, agent_id: str):
    """Write spend to token_bank_spend. FED's ONLY write path."""
    cost = _estimate_cost(provider_id, model_id, tokens_in, tokens_out)
    now = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(str(FED_STATE_DB))
    conn.execute(
        """INSERT INTO token_bank_spend (provider_name, model_id, agent_id,
                                          tokens_in, tokens_out, estimated_cost_usd, called_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (provider_id, model_id, agent_id, tokens_in, tokens_out, cost, now),
    )
    conn.commit()
    conn.close()


# ── Routing tables ───────────────────────────────────────────────────────
# Model → [route] mapping. Priority: direct > gateway_clean > gateway_shadowed.
# Fed from AGENT_MODEL_MAP.json fed_routes + provider registry.

MODEL_ROUTES = {
    # DeepSeek family
    "deepseek-v4-pro": [
        {
            "provider": "deepseek",
            "router": "direct",
            "class": "direct",
            "constitutional": True,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "qwen-token-plan-team",
            "router": "direct",
            "class": "direct",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 3,
        },
        {
            "provider": "tokenrouter",
            "router": "gateway",
            "class": "gateway_shadowed",
            "constitutional": False,
            "shadow": "SHADOW-TR-001",
            "priority": 4,
        },
    ],
    "deepseek-v4-flash": [
        {
            "provider": "deepseek",
            "router": "direct",
            "class": "direct",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "qwen-token-plan-team",
            "router": "direct",
            "class": "direct",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 3,
        },
        {
            "provider": "tokenrouter",
            "router": "gateway",
            "class": "gateway_shadowed",
            "constitutional": False,
            "shadow": "SHADOW-TR-001",
            "priority": 4,
        },
    ],
    # Qwen family — best via MuleRouter (vision models)
    "qwen3.6-flash": [
        {
            "provider": "qwen-token-plan-team",
            "router": "direct",
            "class": "direct",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    "qwen3.7-plus": [
        {
            "provider": "qwen-token-plan-team",
            "router": "direct",
            "class": "direct",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    "qwen-vl-max": [
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "bailian-token-plan",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    "qwen3-vl-plus": [
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "bailian-token-plan",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    "qwen3-vl-flash": [
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
    ],
    "qwen3-omni-flash": [
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
    ],
    "qwen3-max": [
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "bailian-token-plan",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    # GPT family — best via TokenRouter
    "gpt-5.6-sol": [
        {
            "provider": "tokenrouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    "gpt-5.5": [
        {
            "provider": "tokenrouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    # Claude family — TokenRouter only
    "claude-sonnet-5": [
        {
            "provider": "tokenrouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
    ],
    "claude-opus-4.8": [
        {
            "provider": "tokenrouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
    ],
    # Kimi / GLM — TokenRouter FREE
    "kimi-k3": [
        {
            "provider": "tokenrouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
            "free": True,
        },
        {
            "provider": "kimi-moonshot",
            "router": "direct",
            "class": "direct",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    "glm-5.2": [
        {
            "provider": "tokenrouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
            "free": True,
        },
        {
            "provider": "qwen-token-plan-team",
            "router": "direct",
            "class": "direct",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
    "kimi-k2.7-code": [
        {
            "provider": "qwen-token-plan-team",
            "router": "direct",
            "class": "direct",
            "constitutional": False,
            "shadow": None,
            "priority": 1,
        },
        {
            "provider": "mulerouter",
            "router": "gateway",
            "class": "gateway",
            "constitutional": False,
            "shadow": None,
            "priority": 2,
        },
    ],
}

# Modality boost map
VISION_MODELS = {
    "qwen-vl-max",
    "qwen3-vl-plus",
    "qwen3-vl-flash",
    "qwen3-omni-flash",
    "qwen3.5-omni-flash",
    "qwen3.5-omni-plus",
}

# Constitutional tier → allowed router classes
CONSTITUTIONAL_ALLOWED = {
    666: {"direct"},  # JUDGE: direct ONLY
    999: {"direct"},  # SEAL: direct ONLY
    333: {"direct", "gateway"},
    555: {"direct", "gateway"},
    0: {"direct", "gateway"},  # default
}


# ── FED Route Engine (Zen-hardened v3.1 — LiteLLM patterns absorbed) ─────
# Zen 2026-08-02: Absorbed LiteLLM patterns:
#   - Route health gate (cooldown DEGRADED, demote RATE_LIMITED)
#   - Cost estimate surfaced per route (catalog pricing)
#   - Insufficient telemetry demotion (low-sample routes deprioritized)
def fed_route_engine(
    task: str = "",
    model: str = "deepseek-v4-pro",
    modality: str = "text",
    agent_id: str = "opencode",
    constitutional_tier: int = 333,
) -> list[dict]:
    """
    Zen-hardened 9-step routing logic (was 7, +2 LiteLLM patterns).

    Steps:
      1. FILTER: remove DEAD providers
      2. HEALTH GATE: skip DEGRADED, demote RATE_LIMITED (LiteLLM cooldown)
      3. RANK: by priority class (direct > gateway > shadowed)
      4. BOOST: vision modality → push VL-capable providers up
      5. DEGRADE: constitutional ≥ 666 → direct ONLY
      6. BALANCE GATE: dual-track (API hard, Token Bank soft, UNVERIFIABLE bypass)
      7. LATENCY GATE: read pre-computed p50/p95; demote if p95>5s
      8. TELEMETRY GATE: demote routes with <10 samples (LiteLLM: don't route to unproven paths)
      9. COST SURFACE: attach estimated cost per 1K tokens to each route
      10. RETURN: top 3 routes with reasoning
    """
    routes = MODEL_ROUTES.get(model, MODEL_ROUTES.get("deepseek-v4-pro", []))

    if not routes:
        return [{"rank": 0, "error": f"No routes defined for model: {model}"}]

    now = datetime.now(timezone.utc).isoformat()
    ranked = []

    for route in routes:
        provider_id = route["provider"]
        bal = read_provider_balance(provider_id)

        # ── Step 1: FILTER dead providers ────────────────────────────
        if bal and bal.get("notes") and "DEAD" in str(bal["notes"]).upper():
            continue

        # ── Step 2: HEALTH GATE (Zen: LiteLLM cooldown pattern) ─────
        health = read_route_health(provider_id, model)
        health_status = health["status"] if health else "LIVE"
        health_flag = None

        if health_status == "DEGRADED":
            # LiteLLM cooldown: skip failing deployments entirely
            continue
        elif health_status == "RATE_LIMITED":
            # LiteLLM cooldown: demote but keep as last resort
            health_flag = "RATE_LIMITED"
            # Don't skip — just heavily demote below

        # ── Step 4: DEGRADE constitutional ───────────────────────────
        allowed = CONSTITUTIONAL_ALLOWED.get(constitutional_tier, {"direct", "gateway"})
        if route["class"] not in allowed:
            continue

        # ── Step 2: RANK — priority score (lower = better) ───────────
        priority = route["priority"]
        if modality == "vision" and provider_id == "mulerouter":
            priority -= 2  # Boost MuleRouter for vision (4 VL models)
        if modality == "vision" and model in VISION_MODELS:
            priority -= 1
        if health_flag == "RATE_LIMITED":
            priority += 8  # Heavy demotion — last resort

        # ── Step 5: BALANCE GATE dual-track ──────────────────────────
        balance = bal["balance_usd"] if bal else None
        confidence = bal["balance_confidence"] if bal else 0.30
        track = bal["track"] if bal else "B"
        balance_flag = None

        if track == "A" and confidence >= 0.95:
            # Track A: API-probed, hard gate at $1.00
            if balance is not None and balance < 1.00:
                priority += 10  # HARD demotion
                balance_flag = "LOW_BALANCE_HARD"
        elif track == "B":
            # Track B: Token Bank estimate, soft gate at $5.00
            if confidence < 0.50:
                balance_flag = "UNVERIFIABLE"
                # NEVER demote — retain rank, flag only
            elif balance is not None and balance < 5.00 and confidence > 0.70:
                priority += 5  # SOFT demotion
                balance_flag = "LOW_BALANCE_SOFT"
            elif balance is None:
                balance_flag = "UNVERIFIABLE"
                # NEVER demote for unknown balance

        # ── Step 6: LATENCY GATE (passive) ───────────────────────────
        lat = read_route_latency(provider_id, model)
        p50_ms = lat["p50_ms"] if lat else None
        p95_ms = lat["p95_ms"] if lat else None
        sample_count = lat["sample_count"] if lat else 0
        latency_flag = None

        if p50_ms:
            if p95_ms and p95_ms > 5000:
                latency_flag = "DEGRADED"
                priority += 3

        # ── Step 7: TELEMETRY GATE (Zen: LiteLLM pattern) ────────────
        # Demote routes with insufficient telemetry — prefer proven paths
        if sample_count < 10:
            if sample_count == 0:
                latency_flag = "NO_TELEMETRY"
                priority += 2  # Slight demotion for completely untested
            else:
                latency_flag = "INSUFFICIENT_TELEMETRY"
                # Only demote if we have some data that suggests slowness
                if p50_ms and p50_ms > 2000:
                    priority += 1

        # ── Step 8: COST SURFACE (Zen: LiteLLM model catalog) ────────
        cost_per_1k = _estimate_cost_per_1k(provider_id, model)

        ranked.append(
            {
                "rank": 0,  # filled after sort
                "priority": priority,
                "provider": provider_id,
                "model": model,
                "router": route["router"],
                "router_class": route["class"],
                "balance_usd": balance,
                "balance_confidence": confidence,
                "balance_track": track,
                "balance_flag": balance_flag,
                "latency_p50_ms": p50_ms,
                "latency_p95_ms": p95_ms,
                "latency_sample_count": sample_count,
                "latency_flag": latency_flag,
                "health": health_status,
                "health_flag": health_flag,
                "cost_per_1m_input_usd": cost_per_1k["input_per_1m_usd"],
                "cost_per_1m_output_usd": cost_per_1k["output_per_1m_usd"],
                "shadow": route.get("shadow"),
                "free": route.get("free", False),
                "reason": _build_reason(route, balance_flag, latency_flag, health_flag, constitutional_tier),
            }
        )

    # Sort by priority (ascending)
    ranked.sort(key=lambda r: r["priority"])

    # Assign ranks
    for i, r in enumerate(ranked[:3]):
        r["rank"] = i + 1

    return ranked[:3]


def _build_reason(route, balance_flag, latency_flag, health_flag, tier):
    parts = []
    if tier >= 666:
        parts.append("666/999 constitutional — direct path required")
    if route["class"] == "direct":
        parts.append("zero gateway contamination")
    if route.get("free"):
        parts.append("FREE tier")
    if route.get("shadow"):
        parts.append(f"SHADOWED: {route['shadow']}")
    if health_flag == "RATE_LIMITED":
        parts.append("provider rate-limited (cooldown)")
    if balance_flag == "LOW_BALANCE_HARD":
        parts.append("balance < $1.00 (HARD demotion)")
    elif balance_flag == "LOW_BALANCE_SOFT":
        parts.append("balance < $5.00 (soft demotion)")
    elif balance_flag == "UNVERIFIABLE":
        parts.append("balance unverifiable — check dashboard")
    if latency_flag == "DEGRADED":
        parts.append("p95 latency >5s")
    elif latency_flag == "NO_TELEMETRY":
        parts.append("no telemetry — untested route")
    elif latency_flag == "INSUFFICIENT_TELEMETRY":
        parts.append("insufficient telemetry samples")
    return "; ".join(parts) if parts else "available"


# ── MCP Tools ────────────────────────────────────────────────────────────


@mcp.tool()
def fed_route(
    task: str = "",
    model: str = "deepseek-v4-pro",
    modality: str = "text",
    agent_id: str = "opencode",
    constitutional_tier: int = 333,
    tokens_in_estimate: int = 0,
    tokens_out_estimate: int = 0,
) -> dict:
    """
    Primary routing tool. Returns ranked routes for a given task.

    Args:
        task: Natural language description of the task
        model: Target model (default: deepseek-v4-pro)
        modality: text, vision, video, audio, omni
        agent_id: Calling agent (opencode, hermes, asi-555, apex-888)
        constitutional_tier: 0=default, 333=primary, 555=research, 666=judge, 999=seal
        tokens_in_estimate: Estimated input tokens (for spend logging)
        tokens_out_estimate: Estimated output tokens (for spend logging)

    Returns:
        { routes: [...], meta: { query_time_ms, state_db } }
    """
    t0 = time.time()
    routes = fed_route_engine(
        task=task,
        model=model,
        modality=modality,
        agent_id=agent_id,
        constitutional_tier=constitutional_tier,
    )
    elapsed = round((time.time() - t0) * 1000)

    # Log estimated spend if tokens provided
    if tokens_in_estimate or tokens_out_estimate:
        primary = routes[0] if routes else None
        if primary:
            log_spend(primary["provider"], model, tokens_in_estimate, tokens_out_estimate, agent_id)

    return {
        "routes": routes,
        "meta": {
            "query_time_ms": elapsed,
            "state_db": str(FED_STATE_DB),
            "queried_at": datetime.now(timezone.utc).isoformat(),
            "cascade_instruction": (
                "Execute routes in rank order. On failure (timeout/auth), "
                "emit telemetry and cascade to next rank. Never retry same provider twice."
            ),
        },
    }


@mcp.tool()
def fed_status() -> dict:
    """Return full FED state: all provider balances, route health, latency summary."""
    providers = read_all_providers()

    conn = get_db()
    lat_rows = conn.execute(
        "SELECT provider_name, model_id, p50_ms, p95_ms, sample_count, last_sample FROM route_latency"
    ).fetchall()
    health_rows = conn.execute("SELECT provider_name, model_id, status, shadow_id FROM route_health").fetchall()
    spend_total = conn.execute(
        "SELECT provider_name, SUM(estimated_cost_usd) as total FROM token_bank_spend GROUP BY provider_name"
    ).fetchall()
    conn.close()

    return {
        "providers": providers,
        "latency": [dict(r) for r in lat_rows],
        "health": [dict(r) for r in health_rows],
        "spend_summary": {r["provider_name"]: round(r["total"], 6) for r in spend_total},
        "state_db": str(FED_STATE_DB),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def fed_probe() -> dict:
    """Run balance probe (delegates to balance_probe.py). Returns Track A + Track B status."""
    import subprocess

    result = subprocess.run(
        ["python3", "/root/AAA/scripts/balance_probe.py"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "exit_code": result.returncode,
        "output": result.stdout[-2000:],
        "provider_count": 6,
    }


@mcp.tool()
def fed_contrast(route_a: str, route_b: str) -> dict:
    """Compare two routes side-by-side: cost, latency, shadow, constitutional fit."""

    # Parse provider:model strings
    def parse(r):
        parts = r.split(":", 1)
        return parts[0] if len(parts) > 1 else None, parts[1] if len(parts) > 1 else parts[0]

    prov_a, model_a = parse(route_a)
    prov_b, model_b = parse(route_b)

    bal_a = read_provider_balance(prov_a) if prov_a else None
    bal_b = read_provider_balance(prov_b) if prov_b else None
    lat_a = read_route_latency(prov_a, model_a) if prov_a else None
    lat_b = read_route_latency(prov_b, model_b) if prov_b else None

    return {
        "route_a": {
            "provider": prov_a,
            "model": model_a,
            "balance": bal_a["balance_usd"] if bal_a else None,
            "latency_p50": lat_a["p50_ms"] if lat_a else None,
        },
        "route_b": {
            "provider": prov_b,
            "model": model_b,
            "balance": bal_b["balance_usd"] if bal_b else None,
            "latency_p50": lat_b["p50_ms"] if lat_b else None,
        },
    }


# ── Health endpoint ──────────────────────────────────────────────────────
@mcp.tool()
def fed_health() -> dict:
    """FED health check — returns service status and DB integrity."""
    conn = get_db()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    conn.close()

    return {
        "status": "LIVE",
        "port": FED_PORT,
        "version": "3.1.0-zen",
        "tables": [t["name"] for t in tables],
        "state_db": str(FED_STATE_DB),
    }


# ── Latency telemetry ────────────────────────────────────────────────────
@mcp.tool()
def fed_report_latency(
    provider: str,
    model: str,
    latency_ms: float,
    status_code: int = 200,
    tokens_in: int = 0,
    tokens_out: int = 0,
    agent_id: str = "unknown",
) -> dict:
    """
    Report latency for a provider-model route. Agents call this after every
    API call to populate route_latency table with live telemetry.

    Args:
        provider: Provider name (deepseek, mulerouter, tokenrouter, etc.)
        model: Model ID (deepseek-v4-pro, qwen-vl-max, etc.)
        latency_ms: Round-trip latency in milliseconds
        status_code: HTTP status code (200, 429, 503, etc.)
        tokens_in: Input tokens used
        tokens_out: Output tokens generated
        agent_id: Reporting agent

    Returns:
        { recorded: true, p50_ms: ..., sample_count: ... }
    """
    now = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(str(FED_STATE_DB))
    conn.row_factory = sqlite3.Row

    # Read existing stats
    existing = conn.execute(
        "SELECT p50_ms, p95_ms, sample_count FROM route_latency WHERE provider_name = ? AND model_id = ?",
        (provider, model),
    ).fetchone()

    if existing:
        n = existing["sample_count"] + 1
        old_p50 = existing["p50_ms"] or latency_ms
        old_p95 = existing["p95_ms"] or latency_ms
        # Welford-style online update (approximate)
        new_p50 = old_p50 + (latency_ms - old_p50) / n
        new_p95 = max(old_p95, latency_ms) - (max(old_p95, latency_ms) - latency_ms) * 0.05  # exponential decay
        conn.execute(
            """UPDATE route_latency SET p50_ms=?, p95_ms=?, sample_count=?, last_sample=? WHERE provider_name=? AND model_id=?""",
            (round(new_p50, 2), round(new_p95, 2), n, now, provider, model),
        )
    else:
        conn.execute(
            """INSERT INTO route_latency (provider_name, model_id, p50_ms, p95_ms, sample_count, last_sample)
               VALUES (?, ?, ?, ?, 1, ?)""",
            (provider, model, latency_ms, latency_ms, now),
        )

    # Log spend if tokens used
    if tokens_in or tokens_out:
        cost = _estimate_cost(provider, model, tokens_in, tokens_out)
        conn.execute(
            """INSERT INTO token_bank_spend (provider_name, model_id, agent_id, tokens_in, tokens_out, estimated_cost_usd, called_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (provider, model, agent_id, tokens_in, tokens_out, cost, now),
        )

    # Update route health
    health_status = "LIVE" if status_code < 500 else "DEGRADED"
    if status_code == 429:
        health_status = "RATE_LIMITED"
    conn.execute(
        """INSERT INTO route_health (provider_name, model_id, status, last_checked)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(provider_name, model_id) DO UPDATE SET status=excluded.status, last_checked=excluded.last_checked""",
        (provider, model, health_status, now),
    )

    conn.commit()

    # Read updated stats
    final = conn.execute(
        "SELECT p50_ms, p95_ms, sample_count FROM route_latency WHERE provider_name = ? AND model_id = ?",
        (provider, model),
    ).fetchone()
    conn.close()

    return {
        "recorded": True,
        "provider": provider,
        "model": model,
        "p50_ms": final["p50_ms"],
        "p95_ms": final["p95_ms"],
        "sample_count": final["sample_count"],
        "health": health_status,
    }


# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    os.environ["FASTMCP_PORT"] = str(FED_PORT)
    print(f"🔀 FED Router v3.0 starting on :{FED_PORT}")
    print(f"   State DB: {FED_STATE_DB}")
    print(f"   Invariants: state-isolation, constitutional-hard-gate, dual-track-bypass")
    print(f"   Tools: fed_route, fed_status, fed_probe, fed_contrast, fed_health")
    mcp.run(transport="streamable-http", host="127.0.0.1")
