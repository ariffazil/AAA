#!/usr/bin/env python3
"""
OpenClaw Orchestrator CLI v0.1.0

Subprocess-callable entry point for Node.js adapter.
Reads JSON from stdin, writes JSON to stdout.
Zero network calls. Local-only. Deterministic.

Capability contract:
  capability_id: openclaw.orchestrator.classify | openclaw.orchestrator.dag
  Input: JSON on stdin
  Output: JSON on stdout
  Exit code: 0=success, 1=error, 2=validation failure

Usage:
  echo '{"capability_id":"openclaw.orchestrator.classify","query":"research gold"}' | python3 orchestrator_cli.py
  echo '{"capability_id":"openclaw.orchestrator.dag","flow":{...}}' | python3 orchestrator_cli.py

Forged: 2026-09-12 by 333-AGI under F13 directive
DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import os
import sys
import time
import traceback

# Ensure runtime is importable (parent of runtime/ directory)
_script_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_script_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# ─── Allowed capabilities ───────────────────────────────────────────────
ALLOWED_CAPABILITIES = {
    "openclaw.orchestrator.classify",
    "openclaw.orchestrator.classify_multi",
    "openclaw.orchestrator.dag_define",
    "openclaw.orchestrator.dag_execute",
    "openclaw.orchestrator.dag_template",
    "openclaw.orchestrator.state_get",
    "openclaw.orchestrator.health",
}

MAX_QUERY_LENGTH = 10000
MAX_FLOW_TASKS = 20


def validate_input(data: dict) -> tuple[bool, str]:
    """Validate input against capability contract."""
    cap_id = data.get("capability_id", "")
    if cap_id not in ALLOWED_CAPABILITIES:
        return False, f"CAPABILITY_DENIED: {cap_id} not in {sorted(ALLOWED_CAPABILITIES)}"

    if cap_id in ("openclaw.orchestrator.classify", "openclaw.orchestrator.classify_multi"):
        query = data.get("query", "")
        if not query:
            return False, "MISSING_FIELD: query is required"
        if len(query) > MAX_QUERY_LENGTH:
            return False, f"QUERY_TOO_LONG: {len(query)} > {MAX_QUERY_LENGTH}"
        # Reject shell metacharacters in query (defense in depth)
        dangerous = set(";|&$`\x0a\x0d")
        if dangerous.intersection(query):
            return False, "DANGEROUS_CHARACTERS: query contains shell metacharacters"

        # Reject URLs in query (defense in depth)
        if "http://" in query.lower() or "https://" in query.lower():
            return False, "URL_NOT_ALLOWED: query contains URL"

    if cap_id in ("openclaw.orchestrator.dag_define",):
        flow = data.get("flow", {})
        if not flow:
            return False, "MISSING_FIELD: flow is required"
        if not flow.get("tasks"):
            return False, "MISSING_FIELD: flow.tasks is required"
        if len(flow.get("tasks", [])) > MAX_FLOW_TASKS:
            return False, f"TOO_MANY_TASKS: {len(flow['tasks'])} > {MAX_FLOW_TASKS}"
        # Validate each task has required fields
        for i, task in enumerate(flow["tasks"]):
            if not task.get("id"):
                return False, f"MISSING_FIELD: flow.tasks[{i}].id is required"
            if not task.get("agent"):
                return False, f"MISSING_FIELD: flow.tasks[{i}].agent is required"

    if cap_id in ("openclaw.orchestrator.dag_execute",):
        flow_id = data.get("flow_id", "")
        if not flow_id:
            return False, "MISSING_FIELD: flow_id is required"
        # Reject path traversal in flow_id
        if ".." in flow_id or "/" in flow_id:
            return False, "INVALID_FIELD: flow_id contains path traversal"

    return True, "ok"


def execute_capability(data: dict) -> dict:
    """Execute the requested capability."""
    cap_id = data["capability_id"]
    start_ms = int(time.time() * 1000)

    if cap_id == "openclaw.orchestrator.classify":
        from runtime.semantic_router import classify_intent
        from dataclasses import asdict

        result = classify_intent(
            data["query"],
            person_id=data.get("person_id", "cli"),
            context=data.get("context"),
        )
        return {
            "status": "success",
            "capability_id": cap_id,
            "result": asdict(result),
            "latency_ms": int(time.time() * 1000) - start_ms,
        }

    elif cap_id == "openclaw.orchestrator.classify_multi":
        from runtime.semantic_router import classify_multi_intents
        from dataclasses import asdict

        results = classify_multi_intents(data["query"], person_id=data.get("person_id", "cli"))
        return {
            "status": "success",
            "capability_id": cap_id,
            "intents": [asdict(r) for r in results],
            "latency_ms": int(time.time() * 1000) - start_ms,
        }

    elif cap_id == "openclaw.orchestrator.dag_define":
        from runtime.dag_engine import define_workflow

        result = define_workflow(data["flow"])
        return {
            "status": "success",
            "capability_id": cap_id,
            "result": result,
            "latency_ms": int(time.time() * 1000) - start_ms,
        }

    elif cap_id == "openclaw.orchestrator.dag_execute":
        from runtime.dag_engine import execute_workflow

        result = execute_workflow(data["flow_id"], dry_run=data.get("dry_run", False))
        return {
            "status": "success",
            "capability_id": cap_id,
            "result": result,
            "latency_ms": int(time.time() * 1000) - start_ms,
        }

    elif cap_id == "openclaw.orchestrator.dag_template":
        from runtime.dag_engine import create_from_template

        result = create_from_template(data.get("template", ""), data.get("variables", {}))
        return {
            "status": "success",
            "capability_id": cap_id,
            "result": result,
            "latency_ms": int(time.time() * 1000) - start_ms,
        }

    elif cap_id == "openclaw.orchestrator.state_get":
        from runtime.state_manager import get_state_manager

        sm = get_state_manager()
        state = sm.get_state(data.get("person_id", "unknown"))
        return {
            "status": "success",
            "capability_id": cap_id,
            "result": sm._serialize(state),
            "latency_ms": int(time.time() * 1000) - start_ms,
        }

    elif cap_id == "openclaw.orchestrator.health":
        return {
            "status": "success",
            "capability_id": cap_id,
            "result": {
                "status": "healthy",
                "capabilities": sorted(ALLOWED_CAPABILITIES),
                "components": ["semantic_router", "dag_engine", "state_manager", "observability"],
            },
            "latency_ms": int(time.time() * 1000) - start_ms,
        }

    return {"status": "failed", "error": f"Unknown capability: {cap_id}"}


def main():
    """Main entry point — read JSON from stdin, write JSON to stdout."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            print(json.dumps({"status": "failed", "error": "EMPTY_INPUT"}))
            sys.exit(2)

        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "failed", "error": f"INVALID_JSON: {e}"}))
        sys.exit(2)

    # Validate
    valid, reason = validate_input(data)
    if not valid:
        print(json.dumps({"status": "failed", "error": reason}))
        sys.exit(2)

    # Execute
    try:
        result = execute_capability(data)
        print(json.dumps(result, default=str))
        sys.exit(0)
    except Exception as e:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "error": str(e),
                    "error_class": type(e).__name__,
                    "safe_message": "Internal orchestrator error. See logs.",
                }
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
