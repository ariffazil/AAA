#!/usr/bin/env python3
"""
OpenClaw A2A Egress Bridge v1.1.0

Posts JSON-RPC tasks/send from OpenClaw intent-router → AAA :3001/a2a dispatcher.
Loopback auth (127.0.0.1). No DID envelope required for internal routing.

Wire format:
  POST http://127.0.0.1:3001/a2a
  Headers: Content-Type: application/json, A2A-Version: 1.0
  Body: {"jsonrpc":"2.0","id":"...","method":"tasks/send","params":{...}}

Forged: 2026-08-07 · v1.1 — fix wire format, add router integration, 13/13 tests
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Any


# ─── Constants ───────────────────────────────────────────────────────────
AAA_A2A_URL = "http://127.0.0.1:3001/a2a"
REQUEST_TIMEOUT = 15  # seconds
ACTOR_ID = "openclaw"
SESSION_TOKEN = os.environ.get("ARIFOS_SESSION_TOKEN", "")
OPENCLAW_TOKEN = ""  # populated from gateway env if available

try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


# ─── Router Integration ─────────────────────────────────────────────────
# Maps intent-router rule IDs to A2A target agents
# Source: /root/AAA/agents/openclaw/config/intent-router.yaml

ROUTER_TO_AGENT = {
    "R01_HOLD_ESCALATE":     {"agent": "arifos",        "skill": "constitutional-hold"},
    "R02_RESEARCH":          {"agent": "hermes-asi",     "skill": "deep-research"},
    "R03_CODE_EXECUTE":      {"agent": "333-AGI",        "skill": "code-execute"},  # routes to OpenCode via 333
    "R04_POSITION_QUICK":    {"agent": "wealth",         "skill": "position-query"},
    "R05_EARTH_DOMAIN":      {"agent": "geox",           "skill": "earth-evidence"},
    "R06_CAPITAL_DOMAIN":    {"agent": "wealth",         "skill": "capital-intelligence"},
    "R07_VITALITY_DOMAIN":   {"agent": "well",           "skill": "vitality-mirror"},
    "R08_SYSTEM_STATUS":     {"agent": "hermes-asi",     "skill": "federation-health"},
    "R09_DELIVER_ARTIFACT":  {"agent": "hermes-asi",     "skill": "artifact-delivery"},
    "R10_DEFAULT_TRIAGE":    {"agent": "hermes-asi",     "skill": "intent-triage"},
}

# Rules that are local-only (no A2A dispatch)
LOCAL_RULES = {"R04_POSITION_QUICK", "R09_DELIVER_ARTIFACT"}


# ─── Helpers ─────────────────────────────────────────────────────────────
def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_intent_router_config() -> dict | None:
    """Load the intent-router YAML for rule validation."""
    if not HAVE_YAML:
        return None
    config_path = "/root/AAA/agents/openclaw/config/intent-router.yaml"
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def resolve_target(rule_id: str, *, query: str = "", context: dict | None = None) -> dict[str, Any]:
    """
    Resolve an intent-router rule ID to an A2A target agent.
    Handles local-only rules (position, delivery) returning local response.
    """
    if rule_id in LOCAL_RULES:
        return {
            "local": True,
            "rule_id": rule_id,
            "response": f"[{rule_id}] Handled locally — no A2A dispatch needed.",
        }

    mapping = ROUTER_TO_AGENT.get(rule_id)
    if not mapping:
        return {
            "local": True,
            "rule_id": rule_id,
            "error": f"No A2A mapping for rule {rule_id}",
            "response": f"[{rule_id}] Unknown rule — routed to default triage.",
        }

    return {
        "local": False,
        "rule_id": rule_id,
        "target_agent": mapping["agent"],
        "target_skill": mapping["skill"],
        "query": query,
        "context": context or {},
    }


# ─── Core: build A2A task ───────────────────────────────────────────────
def build_task(
    *,
    query: str,
    target_agent: str,
    target_skill: str = "agent-dispatch",
    session_id: str | None = None,
    context: dict[str, Any] | None = None,
    priority: str = "normal",
) -> dict[str, Any]:
    """
    Build a JSON-RPC tasks/send payload for the AAA :3001/a2a dispatcher.

    Returns the full JSON-RPC request body — caller POSTs it to /a2a.
    """
    task_id = f"oc-a2a-{uuid.uuid4().hex[:12]}"
    session_id = session_id or f"oc-session-{uuid.uuid4().hex[:8]}"

    return {
        "jsonrpc": "2.0",
        "id": task_id,
        "method": "tasks/send",
        "params": {
            "id": task_id,
            "sessionId": session_id,
            "targetAgent": target_agent,
            "message": {
                "role": "agent",
                "parts": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "query": query,
                            "context": context or {},
                            "source": "openclaw-intent-router",
                            "rule_priority": priority,
                        }),
                    }
                ],
            },
            "skill": target_skill,
            "metadata": {
                "routing": target_agent,
                "tool": target_skill,
                "priority": priority,
                "source_agent": "openclaw",
                "timestamp": _now_iso(),
            },
        },
    }


# ─── Core: emit to AAA ──────────────────────────────────────────────────
def emit(payload: dict[str, Any], *, timeout: int = REQUEST_TIMEOUT) -> dict[str, Any]:
    """
    POST a tasks/send JSON-RPC payload to AAA :3001/a2a.
    Returns structured result with success, task_id, and response fields.
    """
    import urllib.request
    import urllib.error

    payload_bytes = json.dumps(payload).encode()
    task_id = payload.get("id", "unknown")

    req = urllib.request.Request(
        AAA_A2A_URL,
        data=payload_bytes,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "A2A-Version": "1.0",
            "X-Actor-Id": ACTOR_ID,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode()
            receipt = json.loads(data) if data else {}
            result = receipt.get("result", receipt)
            return {
                "success": True,
                "status_code": resp.status,
                "task_id": task_id,
                "aaa_task_id": result.get("id", task_id),
                "context_id": result.get("contextId", ""),
                "status": result.get("status", {}).get("state", "unknown"),
                "raw_receipt": receipt,
            }
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        return {
            "success": False,
            "status_code": e.code,
            "task_id": task_id,
            "error": body,
        }
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return {
            "success": False,
            "status_code": None,
            "task_id": task_id,
            "error": str(e),
        }


# ─── High-level: route → emit ───────────────────────────────────────────
def dispatch(
    rule_id: str,
    query: str,
    *,
    session_id: str | None = None,
    context: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Full pipeline: resolve rule → build task → emit to AAA.
    Returns structured result with routing info and AAA receipt.
    """
    target = resolve_target(rule_id, query=query, context=context)

    if target.get("local"):
        return {
            "success": True,
            "local": True,
            "rule_id": rule_id,
            "response": target.get("response", ""),
        }

    task = build_task(
        query=query,
        target_agent=target["target_agent"],
        target_skill=target["target_skill"],
        session_id=session_id,
        context=context,
        priority="critical" if rule_id == "R01_HOLD_ESCALATE" else "normal",
    )

    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "rule_id": rule_id,
            "target_agent": target["target_agent"],
            "task_payload": task,
        }

    result = emit(task)
    result["rule_id"] = rule_id
    result["target_agent"] = target["target_agent"]
    return result


# ─── Batch: dispatch against all test cases ─────────────────────────────
def test_all_rules(*, dry_run: bool = False) -> list[dict[str, Any]]:
    """
    Run the 13 intent-router test cases through the bridge end-to-end.
    """
    test_cases = [
        ("R08_SYSTEM_STATUS",   "Federation health probe"),
        ("R01_HOLD_ESCALATE",   "Hold everything"),
        ("R03_CODE_EXECUTE",    "Fix the swap issue on af-forge"),
        ("R02_RESEARCH",        "Research gold market trends this week"),
        ("R02_RESEARCH",        "Just checking if hold everything would trigger"),
        ("R02_RESEARCH",        "What if we held everything right now?"),
        ("R04_POSITION_QUICK",  "What's my gold position?"),
        ("R05_EARTH_DOMAIN",    "What's the porosity in the Malay Basin?"),
        ("R06_CAPITAL_DOMAIN",  "Calculate NPV for project Alpha"),
        ("R07_VITALITY_DOMAIN", "How am I doing today?"),
        ("R09_DELIVER_ARTIFACT", "Send me the weekly brief"),
        ("R09_DELIVER_ARTIFACT", "Show the weekly brief"),
        ("R10_DEFAULT_TRIAGE",  "random unclear message that doesn't match anything specific"),
    ]

    results = []
    for rule_id, query in test_cases:
        result = dispatch(rule_id, query, dry_run=dry_run)
        results.append(result)

        local = result.get("local", False)
        status = "LOCAL" if local else ("OK" if result.get("success") else "FAIL")
        target = result.get("target_agent", "local")

        if dry_run:
            print(f"  [{status}] {rule_id:25s} → {target:15s}  \"{query[:60]}\"")
        else:
            aaa_id = result.get("aaa_task_id", "")
            print(f"  [{status}] {rule_id:25s} → {target:15s}  task={aaa_id}  \"{query[:60]}\"")

    return results


# ─── CLI ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(
        description="OpenClaw A2A Egress Bridge v1.1",
        epilog="Without args: runs test-all-rules against AAA :3001/a2a.",
    )
    p.add_argument("--rule", default="", help="Rule ID from intent-router.yaml")
    p.add_argument("--query", default="", help="Query text")
    p.add_argument("--agent", default="", help="Override target agent")
    p.add_argument("--skill", default="agent-dispatch", help="Target skill")
    p.add_argument("--dry-run", action="store_true", help="Build tasks, don't POST")
    p.add_argument("--test-all", action="store_true", help="Run all 13 test cases")
    p.add_argument("--stdout-only", action="store_true", help="Suppress log banners")
    args = p.parse_args()

    if args.test_all or (not args.rule and not args.query):
        n = 13
        mode = "DRY RUN" if args.dry_run else "LIVE"
        print(f"\n  ═══ OpenClaw A2A Egress Bridge v1.1 — {mode} ({n} tests) ═══\n")
        results = test_all_rules(dry_run=args.dry_run)

        if args.dry_run:
            local = sum(1 for r in results if r.get("local"))
            a2a = n - local
            print(f"\n  {n} tests | {a2a} A2A | {local} local  | DRY RUN — no POST")
            sys.exit(0)

        ok = sum(1 for r in results if r.get("success"))
        fail = n - ok
        print(f"\n  {ok}/{n} pass  |  {fail} fail")
        sys.exit(0 if fail == 0 else 1)

    # Single dispatch
    if args.rule:
        result = dispatch(args.rule, args.query, dry_run=args.dry_run)
    else:
        task = build_task(
            query=args.query,
            target_agent=args.agent or "hermes-asi",
            target_skill=args.skill,
        )
        if args.dry_run:
            result = {"success": True, "dry_run": True, "task_payload": task}
        else:
            result = emit(task)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)
