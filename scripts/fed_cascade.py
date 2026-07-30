#!/usr/bin/env python3
"""
fed_cascade.py — AAA Agent Execution Cascade Wrapper (BUILD 5)
═══════════════════════════════════════════════════════════════
Template wrapper that AAA agents use to execute FED-ranked routes.

Flow:
  1. Agent calls fed_route() → receives 3 ranked routes
  2. For each route (rank 1 → 2 → 3):
     a. Execute call
     b. If success → return result
     c. If timeout/auth error → emit telemetry, cascade to next
  3. All 3 failed → escalate to recovery (Ollama local)

Rules (F1 Amanah):
  • Never retry the same provider twice in one cascade
  • Never swallow failures silently — always emit to arifFlow
  • Auth failure on one provider → skip ALL routes for that provider

Usage:
  from fed_cascade import cascade_execute
  result = cascade_execute(
      agent_id="opencode",
      task="code review",
      payload={"messages": [...]},
      constitutional_tier=333,
  )

Forged: 2026-07-30  ·  DITEMPA BUKAN DIBERI
"""

import json
import time
from datetime import datetime, timezone
from typing import Any, Callable, Optional

# Import FED route engine (same process for now; can be MCP-remote later)
from fed_router import fed_route_engine


def emit_telemetry(
    agent_id: str,
    provider: str,
    model: str,
    duration_ms: float,
    status: str,
    tokens_in: int = 0,
    tokens_out: int = 0,
    error: Optional[str] = None,
):
    """Emit telemetry to arifFlow (:7073) after every call attempt."""
    import urllib.request

    payload = {
        "actor_id": agent_id,
        "step_type": "Execute",
        "cost_ns": int(duration_ms * 1_000_000),
        "epistemic_label": "Observation",
        "floor_verdict": "Pass" if status == "success" else "Caution",
        "payload": {
            "provider": provider,
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "status": status,
            "error": error,
            "cascade_step": True,
        },
    }

    try:
        req = urllib.request.Request(
            "http://127.0.0.1:7073/ingest",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # Telemetry is best-effort; never block execution


def cascade_execute(
    agent_id: str,
    task: str = "",
    model: str = "deepseek-v4-pro",
    modality: str = "text",
    constitutional_tier: int = 333,
    payload: Optional[dict] = None,
    execute_fn: Optional[Callable] = None,
) -> dict:
    """
    Execute a task through FED-ranked routes with automatic cascade.

    Args:
        agent_id: "opencode", "hermes", "asi-555", "apex-888"
        task: Natural language task description
        model: Target model
        modality: text, vision, video, audio, omni
        constitutional_tier: 0, 333, 555, 666, 999
        payload: The actual call payload (messages, etc.)
        execute_fn: Callable(provider, model, payload) → result dict.
                    Must return {"success": bool, "content": ..., "tokens": {...}, "error": str}

    Returns:
        {"success": bool, "route_used": {...}, "content": ..., "cascade": [...]}
    """
    # Step 1: Query FED
    routes = fed_route_engine(
        task=task,
        model=model,
        modality=modality,
        agent_id=agent_id,
        constitutional_tier=constitutional_tier,
    )

    if not routes:
        return {"success": False, "error": "FED returned no routes", "cascade": []}

    cascade_log = []
    seen_providers = set()
    last_error = None

    # Step 2: Try each route
    for route in routes:
        provider = route["provider"]
        rank = route["rank"]

        # F1: Never retry same provider
        if provider in seen_providers:
            cascade_log.append(
                {"rank": rank, "provider": provider, "action": "SKIPPED", "reason": "provider_already_attempted"}
            )
            continue

        seen_providers.add(provider)
        cascade_log.append(
            {"rank": rank, "provider": provider, "model": model, "router": route["router"], "action": "ATTEMPTING"}
        )

        # Execute
        t0 = time.time()
        try:
            if execute_fn:
                result = execute_fn(provider, model, payload)
            else:
                # No execute_fn provided — return routes only (dry-run mode)
                return {
                    "success": False,
                    "error": "No execute_fn provided. Routes returned for inspection.",
                    "routes": routes,
                    "cascade": cascade_log,
                }

            elapsed_ms = (time.time() - t0) * 1000

            if result.get("success"):
                # Success!
                tokens = result.get("tokens", {})
                emit_telemetry(
                    agent_id, provider, model, elapsed_ms, "success", tokens.get("input", 0), tokens.get("output", 0)
                )

                cascade_log[-1]["action"] = "SUCCESS"
                cascade_log[-1]["latency_ms"] = round(elapsed_ms, 1)

                return {
                    "success": True,
                    "route_used": {
                        "rank": rank,
                        "provider": provider,
                        "model": model,
                        "router": route["router"],
                        "latency_ms": round(elapsed_ms, 1),
                    },
                    "content": result.get("content"),
                    "cascade": cascade_log,
                }
            else:
                # Provider returned error
                last_error = result.get("error", "unknown")
                emit_telemetry(agent_id, provider, model, elapsed_ms, "failed", error=last_error)
                cascade_log[-1]["action"] = "FAILED"
                cascade_log[-1]["error"] = last_error
                cascade_log[-1]["latency_ms"] = round(elapsed_ms, 1)

                # Auth failure → skip all routes for this provider
                if "auth" in str(last_error).lower() or "401" in str(last_error):
                    cascade_log.append({"action": "PROVIDER_BLOCKED", "provider": provider, "reason": "auth_failure"})
                    continue

        except TimeoutError:
            elapsed_ms = (time.time() - t0) * 1000
            last_error = "timeout"
            emit_telemetry(agent_id, provider, model, elapsed_ms, "timeout")
            cascade_log[-1]["action"] = "TIMEOUT"
            cascade_log[-1]["latency_ms"] = round(elapsed_ms, 1)

        except Exception as e:
            elapsed_ms = (time.time() - t0) * 1000
            last_error = str(e)
            emit_telemetry(agent_id, provider, model, elapsed_ms, "error", error=last_error)
            cascade_log[-1]["action"] = "ERROR"
            cascade_log[-1]["error"] = last_error

    # Step 3: All routes exhausted → recovery
    cascade_log.append(
        {"action": "RECOVERY", "provider": "ollama", "model": "qwen3:8b", "reason": "all_routes_exhausted"}
    )

    return {
        "success": False,
        "error": f"All routes exhausted. Last error: {last_error}",
        "cascade": cascade_log,
        "recovery_route": {"provider": "ollama", "model": "qwen3:8b"},
    }


# ── Dry-run mode (test routing without execution) ───────────────────────
def dry_run(agent_id="opencode", task="test", model="deepseek-v4-pro", modality="text", constitutional_tier=333):
    """Test FED routing without executing any calls."""
    return cascade_execute(
        agent_id=agent_id,
        task=task,
        model=model,
        modality=modality,
        constitutional_tier=constitutional_tier,
        execute_fn=None,  # triggers dry-run mode
    )


if __name__ == "__main__":
    # Quick self-test
    result = dry_run(agent_id="opencode", task="code review", model="deepseek-v4-pro", constitutional_tier=333)
    print(json.dumps(result, indent=2, default=str))
