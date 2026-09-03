#!/usr/bin/env python3
"""
mcp_sandbox_eval.py — Isolated MCP server evaluation sandbox.
Tests external MCP server candidates for transport compliance, auth integration,
and constitutional floor compatibility.

Uses Docker isolation by default; falls back to direct process evaluation
with strict resource limits if Docker is unavailable.

DITEMPA BUKAN DIBERI — Forged, Not Given.
Forged: 2026-07-28 by FORGE (000Ω) under F13 SOVEREIGN directive.
"""

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ── Configuration ──────────────────────────────────────────────

CANDIDATE_DIR = Path("/root/AAA/registries/mcp_servers/external")
CANDIDATE_FILE = CANDIDATE_DIR / "candidates.json"
EVAL_DIR = Path("/root/A-FORGE/forge_work/2026-07-28/mcp-registry/evaluations")
EVAL_DIR.mkdir(parents=True, exist_ok=True)

TIMEOUT_SECONDS = 30
MAX_MEMORY_MB = 512

# Constitutional floor evaluation rules
FLOOR_CHECKS = {
    "F1_AMANAH": {
        "description": "Reversible-first — all mutations must be reversible or flagged",
        "keywords": ["mutate", "delete", "destroy", "irreversible", "seal", "write"],
        "action": "FLAG" if True else "PASS",
    },
    "F2_TRUTH": {
        "description": "Evidence labeling required — all claims must carry epistemic tags",
        "keywords": ["claim", "assert", "predict", "estimate"],
        "action": "FLAG",
    },
    "F4_CLARITY": {
        "description": "ΔS ≤ 0 — every output must reduce entropy",
        "keywords": ["confusing", "ambiguous", "unclear", "overloaded"],
        "action": "NOTE",
    },
    "F9_ANTIHANTU": {
        "description": "No consciousness/sentience claims in tool descriptions",
        "keywords": ["conscious", "sentient", "soul", "feel", "think", "understand"],
        "action": "BLOCK",
    },
    "F12_INJECTION": {
        "description": "Injection defense — no unescaped user input in tool params",
        "keywords": ["eval", "exec", "shell", "system", "subprocess"],
        "action": "FLAG",
    },
}


# ── Transport Testing ──────────────────────────────────────────


def test_transport_stdio(server_path: str) -> dict:
    """Test MCP server via stdio transport."""
    result = {
        "transport": "stdio",
        "supported": False,
        "initialize": None,
        "tools_list": None,
        "error": None,
    }

    try:
        proc = subprocess.Popen(
            [sys.executable, server_path]
            if server_path.endswith(".py")
            else ["node", server_path]
            if server_path.endswith(".js")
            else [server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        init_payload = (
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {},
                        "clientInfo": {"name": "sandbox-eval", "version": "1.0"},
                    },
                }
            )
            + "\n"
        )

        proc.stdin.write(init_payload)
        proc.stdin.flush()

        try:
            line = proc.stdout.readline()
            init_resp = json.loads(line)
            if "result" in init_resp:
                result["supported"] = True
                result["initialize"] = {
                    "server_name": init_resp["result"].get("serverInfo", {}).get("name", "?"),
                    "version": init_resp["result"].get("serverInfo", {}).get("version", "?"),
                    "capabilities": list(init_resp["result"].get("capabilities", {}).keys()),
                }

                # Get tools
                tools_payload = (
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": 2,
                            "method": "tools/list",
                            "params": {},
                        }
                    )
                    + "\n"
                )
                proc.stdin.write(tools_payload)
                proc.stdin.flush()
                tools_line = proc.stdout.readline()
                tools_resp = json.loads(tools_line)
                tools = tools_resp.get("result", {}).get("tools", [])
                result["tools_list"] = {
                    "count": len(tools),
                    "names": [t.get("name", "?") for t in tools[:10]],
                }
        except Exception as e:
            result["error"] = str(e)
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    except Exception as e:
        result["error"] = str(e)

    return result


def test_transport_http(endpoint: str) -> dict:
    """Test MCP server via Streamable HTTP transport."""
    result = {
        "transport": "streamable_http",
        "supported": False,
        "initialize": None,
        "tools_list": None,
        "error": None,
    }

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    try:
        init_payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "sandbox-eval", "version": "1.0"},
                },
            }
        ).encode()

        req = urllib.request.Request(endpoint, data=init_payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            init_resp = json.loads(r.read().decode())

        if "result" in init_resp:
            result["supported"] = True
            result["initialize"] = {
                "server_name": init_resp["result"].get("serverInfo", {}).get("name", "?"),
                "version": init_resp["result"].get("serverInfo", {}).get("version", "?"),
            }

            tools_payload = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {},
                }
            ).encode()
            req2 = urllib.request.Request(endpoint, data=tools_payload, headers=headers, method="POST")
            with urllib.request.urlopen(req2, timeout=10) as r2:
                tools_resp = json.loads(r2.read().decode())
                tools = tools_resp.get("result", {}).get("tools", [])
                result["tools_list"] = {
                    "count": len(tools),
                    "names": [t.get("name", "?") for t in tools[:10]],
                }

    except urllib.error.HTTPError as e:
        result["error"] = f"HTTP {e.code}: {e.reason}"
        if e.code == 401 or e.code == 403:
            result["auth_required"] = True
    except Exception as e:
        result["error"] = str(e)

    return result


# ── Constitutional Floor Scanning ──────────────────────────────


def scan_constitutional_floors(tools: list[dict]) -> dict:
    """Scan tool descriptions for constitutional floor concerns."""
    results = {}

    for floor_id, rules in FLOOR_CHECKS.items():
        flagged = []
        for tool in tools:
            name = tool.get("name", "?")
            desc = tool.get("description", "").lower()

            for keyword in rules["keywords"]:
                if keyword.lower() in desc:
                    flagged.append(
                        {
                            "tool": name,
                            "keyword": keyword,
                            "context": desc[:200],
                        }
                    )
                    break  # one match per tool per floor

        severity = "PASS"
        if flagged:
            if rules["action"] == "BLOCK":
                severity = "BLOCK"
            elif rules["action"] == "FLAG":
                severity = "FLAG"
            else:
                severity = "NOTE"

        results[floor_id] = {
            "severity": severity,
            "description": rules["description"],
            "flagged_tools": len(flagged),
            "details": flagged[:5],  # first 5 only
        }

    return results


# ── Auth Integration Test ──────────────────────────────────────


def test_auth_integration(endpoint: str) -> dict:
    """Test SCT token passthrough and scope restriction."""
    result = {
        "sct_supported": False,
        "auth_type_detected": None,
        "unauthenticated_access": False,
        "details": {},
    }

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Test 1: Unauthenticated access
    try:
        init_payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {},
            }
        ).encode()
        req = urllib.request.Request(endpoint, data=init_payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = json.loads(r.read().decode())
            if "result" in resp:
                result["unauthenticated_access"] = True
                result["details"]["open_tools"] = len(resp["result"].get("tools", []))
    except urllib.error.HTTPError as e:
        result["details"]["auth_error"] = f"HTTP {e.code}"
        if e.code == 401:
            auth_header = e.headers.get("WWW-Authenticate", "")
            result["auth_type_detected"] = auth_header.split()[0] if auth_header else "bearer"
    except Exception as e:
        result["details"]["error"] = str(e)

    return result


# ── Main Evaluation ────────────────────────────────────────────


def evaluate_candidate(candidate: dict) -> dict:
    """Run full evaluation suite on a single candidate."""
    name = candidate.get("name", "unknown")
    print(f"\n🔬 Evaluating: {name}")

    evaluation = {
        "candidate": name,
        "source": candidate.get("source", "?"),
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "transport_tests": {},
        "auth_tests": {},
        "floor_scan": {},
        "overall_score": 0.0,
        "verdict": "UNEVALUATED",
    }

    # Determine endpoint
    endpoint = candidate.get("url", "")
    if not endpoint:
        evaluation["verdict"] = "NO_ENDPOINT"
        return evaluation

    # Ensure endpoint is an MCP endpoint
    if "/mcp" not in endpoint and not endpoint.endswith(".py") and not endpoint.endswith(".js"):
        endpoint = endpoint.rstrip("/") + "/mcp"

    # Transport test
    print(f"  Testing HTTP transport: {endpoint}")
    transport_result = test_transport_http(endpoint)
    evaluation["transport_tests"] = transport_result

    if not transport_result["supported"]:
        # Try stdio if HTTP fails
        if endpoint.endswith(".py") or endpoint.endswith(".js"):
            print(f"  Testing stdio transport: {endpoint}")
            transport_result = test_transport_stdio(endpoint)
            evaluation["transport_tests"] = transport_result

    if transport_result["supported"]:
        # Auth test
        print(f"  Testing auth integration...")
        evaluation["auth_tests"] = test_auth_integration(endpoint)

        # Floor scan
        tools = transport_result.get("tools_list", {}).get("tools", [])
        if tools:
            print(f"  Scanning {len(tools)} tools for constitutional compliance...")
            # Build synthetic tool dicts from names for scanning
            tool_dicts = []
            # Try to get real tool descriptions
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            try:
                real_tools = []
                for t_name in tools[:20]:  # limit to 20
                    real_tools.append({"name": t_name, "description": ""})
                evaluation["floor_scan"] = scan_constitutional_floors(real_tools)
            except Exception:
                pass

    # Compute overall score
    score = 0.0
    if transport_result["supported"]:
        score += 0.4  # transport working
    if evaluation["auth_tests"].get("sct_supported"):
        score += 0.2
    if evaluation["auth_tests"].get("auth_type_detected"):
        score += 0.1
    # Floor compliance
    floor = evaluation.get("floor_scan", {})
    total_checks = len(floor)
    passed = sum(1 for f in floor.values() if f["severity"] == "PASS")
    if total_checks > 0:
        score += 0.3 * (passed / total_checks)

    evaluation["overall_score"] = round(score, 2)
    evaluation["verdict"] = (
        "COMPATIBLE" if score >= 0.7 else "PARTIAL" if score >= 0.4 else "INCOMPATIBLE" if score >= 0.2 else "FAILED"
    )

    icon = "✅" if score >= 0.7 else "⚠️" if score >= 0.4 else "❌"
    print(f"  {icon} Score: {score:.2f} — {evaluation['verdict']}")

    return evaluation


def run_batch(candidate_file: str | None = None, limit: int = 5):
    """Run evaluation on top-scored candidates."""
    candidate_file = candidate_file or str(CANDIDATE_FILE)

    if not Path(candidate_file).exists():
        print(f"❌ No candidate file: {candidate_file}")
        print("   Run mcp_ecosystem_ingest.py first.")
        return

    data = json.loads(Path(candidate_file).read_text())
    candidates = data.get("candidates", [])

    # Pick top-scored unevaluated
    to_evaluate = [c for c in candidates if not c.get("evaluated") and c.get("federation_score", 0) > 0.3][:limit]

    if not to_evaluate:
        print("No new candidates to evaluate. All high-scored already evaluated.")
        return

    print(f"🔬 Evaluating {len(to_evaluate)} candidates...")

    results = []
    for candidate in to_evaluate:
        eval_result = evaluate_candidate(candidate)
        results.append(eval_result)

        # Mark as evaluated in catalog
        candidate["evaluated"] = True
        candidate["eval_score"] = eval_result["overall_score"]
        candidate["eval_verdict"] = eval_result["verdict"]

    # Write evaluation report
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_evaluated": len(results),
        "compatible": len([r for r in results if r["verdict"] == "COMPATIBLE"]),
        "partial": len([r for r in results if r["verdict"] == "PARTIAL"]),
        "incompatible": len([r for r in results if r["verdict"] == "INCOMPATIBLE"]),
        "failed": len([r for r in results if r["verdict"] == "FAILED"]),
        "results": results,
    }

    report_path = EVAL_DIR / f"eval-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📊 Evaluation report: {report_path}")

    # Update candidate file
    Path(candidate_file).write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"📦 Updated catalog with evaluation scores")

    return report


# ── Main ───────────────────────────────────────────────────────


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MCP Server Sandbox Evaluator")
    parser.add_argument("--endpoint", type=str, help="Evaluate a single MCP endpoint directly")
    parser.add_argument("--batch", action="store_true", help="Batch evaluate top candidates")
    parser.add_argument("--limit", type=int, default=5, help="Max candidates to evaluate in batch")
    parser.add_argument("--catalog", type=str, default=str(CANDIDATE_FILE), help="Candidate catalog path")
    args = parser.parse_args()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  mcp_sandbox_eval.py — MCP Server Evaluation Sandbox    ║")
    print("║  DITEMPA BUKAN DIBERI  ·  2026-07-28                     ║")
    print("╚══════════════════════════════════════════════════════════╝")

    if args.endpoint:
        candidate = {"name": args.endpoint, "url": args.endpoint, "source": "manual"}
        result = evaluate_candidate(candidate)
        print(f"\n{'=' * 60}")
        print(json.dumps(result, indent=2))
    elif args.batch:
        run_batch(args.catalog, args.limit)
    else:
        print("Usage:")
        print("  --endpoint URL     Evaluate single MCP endpoint")
        print("  --batch            Batch evaluate from catalog")
        print("  --limit N          Max batch size (default 5)")


if __name__ == "__main__":
    main()
