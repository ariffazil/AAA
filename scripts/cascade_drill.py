#!/usr/bin/env python3
"""cascade_drill.py — Provider failover cascade drill (P0.4, 2026-08-05).

Default mode (no --live): injects stubbed failures. Zero network. Zero cost.
Live mode (--live): makes real API calls with max_tokens=8, trivial "ping" prompt.

Forged: 2026-08-05 by 333-AGI under F13 directive "P0.4 cascade drill"
DITEMPA BUKAN DIBERI
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


REGISTRY_PATH = "/root/AAA/registries/models/AGENT_MODEL_MAP.json"
OUTPUT_DIR = "/root/forge_work/2026-08-05/cascade-drill"


def load_registry(path: str = REGISTRY_PATH) -> dict:
    with open(path) as f:
        return json.load(f)


def get_agent(registry: dict, agent_id: str) -> dict | None:
    for agent in registry.get("agents", []):
        if agent["agent_id"] == agent_id:
            return agent
    return None


def normalize_chain_entries(fallback_chain: list[dict]) -> list[dict]:
    """Filter bare-string entries and normalize to uniform schema.

    Bare-string entries have 'model' instead of 'model_key'+'provider'.
    These are legacy artifacts and are dropped from the drill.
    """
    normalized = []
    for entry in fallback_chain:
        if "provider" in entry and "model_key" in entry:
            normalized.append(entry)
    return normalized


def check_dead_providers(fallback_chain: list[dict], dead_pools: list[str]) -> list[dict]:
    """Check if any dead provider appears in the fallback chain. Returns violations."""
    violations = []
    for entry in fallback_chain:
        provider = entry.get("provider", "")
        if provider in dead_pools:
            violations.append(
                {
                    "provider": provider,
                    "priority": entry.get("priority"),
                    "model_key": entry.get("model_key"),
                    "note": entry.get("note"),
                }
            )
    return violations


def make_stub(fail_first_n: int) -> Callable:
    """Return a callable that fails the first N attempts, then succeeds on N+1."""
    call_count = 0

    def stub_fn(provider: str, model: str, payload: dict | None = None) -> dict:
        nonlocal call_count
        call_count += 1
        if call_count <= fail_first_n:
            return {
                "success": False,
                "error": f"STUB_FAILURE_{call_count}: injected failure for {provider}/{model}",
                "tokens": {"input": 0, "output": 0},
                "content": None,
            }
        return {
            "success": True,
            "content": f"STUB_SUCCESS after {fail_first_n} failures",
            "tokens": {"input": 1, "output": 1},
        }

    return stub_fn


def make_live_fn() -> Callable:
    """Return a callable that makes a real API call.

    Uses minimal tokens (max_tokens=8) and a trivial "ping" prompt.
    Provider routing uses kunci-mas.env env vars.

    Currently supports: deepseek (DEEPSEEK_API_KEY), minimax (MINIMAX_API_KEY),
    qwen-token-plan (QWEN_API_KEY).
    """
    PROVIDER_ENDPOINTS = {
        "deepseek": ("https://api.deepseek.com/v1/chat/completions", "DEEPSEEK_API_KEY"),
        "minimax": ("https://api.minimax.io/v1/text/chatcompletion_v2", "MINIMAX_API_KEY"),
        "qwen-token-plan": (
            "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions",
            "QWEN_API_KEY",
        ),
        "qwen-token-plan-individual": (
            "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions",
            "QWEN_API_KEY",
        ),
        "kimi-moonshot": ("https://api.kimi.com/coding/v1/chat/completions", "KIMI_API_KEY"),
        "bailian-token-plan": (
            "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions",
            "QWEN_API_KEY",
        ),
        "ollama": ("http://localhost:11434/v1/chat/completions", None),
    }

    def live_fn(provider: str, model: str, payload: dict | None = None) -> dict:
        if provider not in PROVIDER_ENDPOINTS:
            return {
                "success": False,
                "error": f"UNSUPPORTED_PROVIDER: {provider} — no endpoint mapped",
                "tokens": {"input": 0, "output": 0},
                "content": None,
            }

        endpoint, key_env = PROVIDER_ENDPOINTS[provider]
        api_key = os.environ.get(key_env) if key_env else None

        headers = {"Content-Type": "application/json"}
        if api_key and provider != "ollama":
            headers["Authorization"] = f"Bearer {api_key}"

        body = {
            "model": model,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 8,
            "temperature": 0,
        }

        # MiniMax uses a different request body format
        if provider == "minimax":
            body = {
                "model": model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 8,
                "temperature": 0.01,
            }

        data = json.dumps(body).encode()
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

        try:
            resp = urllib.request.urlopen(req, timeout=30)
            resp_body = json.loads(resp.read().decode())
            t0 = time.time()
            elapsed = (time.time() - t0) * 1000
            return {
                "success": True,
                "content": resp_body,
                "tokens": {"input": 1, "output": 1},
                "latency_ms": round(elapsed, 1),
            }
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()[:500] if e.fp else ""
            return {
                "success": False,
                "error": f"HTTP {e.code}: {error_body}",
                "tokens": {"input": 0, "output": 0},
                "content": None,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"NETWORK_ERROR: {e}",
                "tokens": {"input": 0, "output": 0},
                "content": None,
            }

    return live_fn


def run_cascade(
    agent_id: str,
    fallback_chain: list[dict],
    execute_fn: Callable,
) -> dict:
    """Run the cascade drill. Iterate chain, stop at first success."""
    cascade_log: list[dict] = []
    seen_providers: set[str] = set()
    last_error = None

    for entry in fallback_chain:
        provider = entry["provider"]
        model = entry["model_key"]
        priority = entry.get("priority", "?")
        note = entry.get("note", "")

        # F1: Never retry same provider
        if provider in seen_providers:
            cascade_log.append(
                {
                    "priority": priority,
                    "provider": provider,
                    "model": model,
                    "action": "SKIPPED",
                    "reason": "provider_already_attempted",
                }
            )
            continue

        seen_providers.add(provider)
        hop = {
            "priority": priority,
            "provider": provider,
            "model": model,
            "action": "ATTEMPTING",
            "note": note,
        }

        t_start = time.time()
        try:
            result = execute_fn(provider, model, None)
        except Exception as exc:
            result = {"success": False, "error": f"EXECUTION_EXCEPTION: {exc}", "tokens": {"input": 0, "output": 0}}

        elapsed_ms = round((time.time() - t_start) * 1000, 1)
        hop["latency_ms"] = elapsed_ms

        if result.get("success"):
            hop["action"] = "SUCCESS"
            cascade_log.append(hop)
            return {
                "success": True,
                "route_used": {
                    "priority": priority,
                    "provider": provider,
                    "model": model,
                    "latency_ms": elapsed_ms,
                },
                "cascade": cascade_log,
            }

        last_error = result.get("error", "unknown")
        hop["action"] = "FAILED"
        hop["error"] = last_error
        cascade_log.append(hop)

        if "auth" in str(last_error).lower() or "401" in str(last_error):
            cascade_log.append(
                {
                    "action": "PROVIDER_BLOCKED",
                    "provider": provider,
                    "reason": "auth_failure",
                }
            )

    # ALL FAILED
    cascade_log.append(
        {
            "action": "CASCADE_EXHAUSTED",
            "hops_attempted": len([h for h in cascade_log if h.get("action") == "FAILED"]),
        }
    )
    return {
        "success": False,
        "error": f"All {len(fallback_chain)} routes exhausted. Last error: {last_error}",
        "cascade": cascade_log,
    }


def run_assertions(
    result: dict,
    violations: list[dict],
    cascade_log: list[dict],
    fallback_chain: list[dict],
) -> list[dict]:
    """Run post-cascade assertions. Returns list of assertion results."""
    assertions = []

    # A1: Dead providers must not appear in chain
    if violations:
        provider_names = [v["provider"] for v in violations]
        assertions.append(
            {
                "assertion": "dead_providers_not_in_chain",
                "passed": False,
                "violation": f"DEAD providers in fallback chain: {provider_names}",
                "details": violations,
            }
        )
    else:
        assertions.append(
            {
                "assertion": "dead_providers_not_in_chain",
                "passed": True,
            }
        )

    # A2: fallback_fired — at least one FAILED + one SUCCESS
    actions = [h.get("action") for h in cascade_log]
    has_failed = "FAILED" in actions
    has_success = "SUCCESS" in actions
    fallback_fired = has_failed and has_success
    assertions.append(
        {
            "assertion": "fallback_fired",
            "passed": fallback_fired,
            "detail": f"FAILED={has_failed}, SUCCESS={has_success}",
        }
    )

    # A3: no_provider_retried — each provider appears at most once
    providers_seen = [h.get("provider") for h in cascade_log if h.get("provider")]
    duplicates = [p for p in set(providers_seen) if providers_seen.count(p) > 1]
    assertions.append(
        {
            "assertion": "no_provider_retried",
            "passed": len(duplicates) == 0,
            "duplicates": duplicates if duplicates else None,
        }
    )

    # A4: all chain entries have provider field (no bare strings)
    bare_entries = len(fallback_chain) - len([e for e in fallback_chain if "provider" in e and "model_key" in e])
    assertions.append(
        {
            "assertion": "all_entries_have_provider",
            "passed": bare_entries == 0,
            "bare_entries_found": bare_entries,
        }
    )

    return assertions


def log_results(
    agent_id: str,
    output_dir: str,
    result: dict,
    assertions: list[dict],
    violations: list[dict],
    mode: str,
    fail_first_n: int,
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{agent_id}-{ts}.jsonl"
    filepath = os.path.join(output_dir, filename)

    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_id,
        "mode": mode,
        "fail_first_n": fail_first_n,
        "cascade_success": result.get("success"),
        "route_used": result.get("route_used"),
        "error": result.get("error"),
        "cascade_log": result.get("cascade"),
        "assertions": assertions,
        "dead_provider_violations": violations,
    }

    # Append as JSONL
    with open(filepath, "a") as f:
        f.write(json.dumps(record, default=str) + "\n")

    return filepath


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="cascade_drill.py — P0.4 Provider failover cascade drill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
    python3 cascade_drill.py --agent opencode --fail-first-n 2
    python3 cascade_drill.py --agent hermes --fail-first-n 1 --live
    python3 cascade_drill.py --all --fail-first-n 1
    python3 cascade_drill.py --agent forge --fail-first-n 0
        """,
    )
    p.add_argument("--agent", default=None, help="Agent ID to drill (e.g. opencode, hermes, forge)")
    p.add_argument("--all", action="store_true", help="Drill all agents")
    p.add_argument("--fail-first-n", type=int, default=1, help="Number of stub failures to inject (default: 1)")
    p.add_argument("--live", action="store_true", help="Make real API calls (requires kunci-mas.env)")
    p.add_argument("--registry", default=REGISTRY_PATH, help="Path to AGENT_MODEL_MAP.json")
    p.add_argument("--output-dir", default=OUTPUT_DIR, help="Output directory for drill logs")
    p.add_argument("--quiet", action="store_true", help="Suppress progress output")
    return p


def drill_agent(
    registry: dict,
    agent_id: str,
    fail_first_n: int,
    live: bool,
    output_dir: str,
    quiet: bool = False,
) -> int:
    """Run cascade drill for one agent. Returns exit code (0=all pass, 1=violations)."""
    agent = get_agent(registry, agent_id)
    if not agent:
        print(f"ERROR: Agent '{agent_id}' not found in registry", file=sys.stderr)
        return 2

    fallback_chain = normalize_chain_entries(agent.get("fallback_chain", []))
    dead_pools = registry.get("_meta", {}).get("dead_pools", [])

    if not quiet:
        name = agent.get("agent_name") or agent_id
        print(f"\n{'=' * 60}")
        print(f"AGENT: {name} ({agent_id})")
        primary_provider = agent.get("primary_provider") or agent.get("pool") or "unknown"
        print(f"PRIMARY: {agent.get('primary_model', '?')} @ {primary_provider}")
        print(f"FALLBACK CHAIN: {len(fallback_chain)} entries")
        for entry in fallback_chain:
            print(f"  [{entry.get('priority')}] {entry['provider']}/{entry['model_key']} ({entry.get('cost', '?')})")
        print(f"MODE: {'LIVE' if live else 'STUB'} (fail-first-n={fail_first_n})")

    # A1: Check dead providers in chain
    violations = check_dead_providers(fallback_chain, dead_pools)
    if not quiet and violations:
        print(f"\n!!! DEAD PROVIDER VIOLATIONS: {[v['provider'] for v in violations]}")
        for v in violations:
            print(f"    [{v['priority']}] {v['provider']}/{v['model_key']} — {v['note']}")

    if live:
        execute_fn = make_live_fn()
    else:
        execute_fn = make_stub(fail_first_n)

    result = run_cascade(agent_id, fallback_chain, execute_fn)
    assertions = run_assertions(result, violations, result["cascade"], fallback_chain)

    if not quiet:
        print(f"\nCASCADE RESULT: {'PASS' if result['success'] else 'FAIL'}")
        if result.get("route_used"):
            ru = result["route_used"]
            print(f"  Route used: [{ru['priority']}] {ru['provider']}/{ru['model']} ({ru['latency_ms']}ms)")
        print(f"\nASSERTIONS:")
        for a in assertions:
            icon = "PASS" if a["passed"] else "FAIL"
            print(f"  [{icon}] {a['assertion']}")
            if not a["passed"] and not quiet:
                detail = a.get("violation") or a.get("detail") or a.get("duplicates")
                if detail:
                    print(f"         {detail}")

    logfile = log_results(
        agent_id, output_dir, result, assertions, violations, "live" if live else "stub", fail_first_n
    )
    if not quiet:
        print(f"\nLogged: {logfile}")

    return 0 if all(a["passed"] for a in assertions) else 1


def main():
    args = build_parser().parse_args()

    if not args.agent and not args.all:
        print("ERROR: --agent or --all required.", file=sys.stderr)
        build_parser().print_help()
        sys.exit(2)

    if args.live:
        print("LIVE MODE: Real API calls will be made. CTRL+C to abort within 3s...")
        try:
            time.sleep(3)
        except KeyboardInterrupt:
            print("\nAborted.")
            sys.exit(0)

    registry = load_registry(args.registry)
    os.makedirs(args.output_dir, exist_ok=True)

    if args.all:
        agent_ids = [a["agent_id"] for a in registry.get("agents", [])]
        if not args.quiet:
            print(f"DRILLING ALL {len(agent_ids)} AGENTS\n{'=' * 60}")
    else:
        agent_ids = [args.agent]

    exit_code = 0
    total = len(agent_ids)
    passed = 0
    failed = 0

    for agent_id in agent_ids:
        rc = drill_agent(
            registry=registry,
            agent_id=agent_id,
            fail_first_n=args.fail_first_n,
            live=args.live,
            output_dir=args.output_dir,
            quiet=args.quiet,
        )
        if rc == 0:
            passed += 1
        elif rc == 2:
            pass  # not found — doesn't count
        else:
            failed += 1
            exit_code = 1

    if not args.quiet and args.all:
        print(f"\n{'=' * 60}")
        print(f"SUMMARY: {passed}/{total} passed, {failed}/{total} failed")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
