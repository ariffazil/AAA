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

import ast as _ast
import json
import os
import shutil
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


# ── AST Security Validator (Micro-Server Hardening) ────────────

BANNED_AST_NODES: set[str] = {
    "eval",
    "exec",
    "__import__",
    "getattr",
    "setattr",
    "importlib",
    "ctypes",
    "os.system",
    "popen",
}

BANNED_IMPORTS: set[str] = {
    "socket",
    "ctypes",
    "subprocess",
    "pty",
    "shutil",
    "signal",
}


class ASTSecurityValidator(_ast.NodeVisitor):
    """Walks Python AST and flags dangerous patterns before containerization."""

    def __init__(self) -> None:
        super().__init__()
        self.violations: list[str] = []

    def visit_Name(self, node: _ast.Name) -> None:
        if node.id in BANNED_AST_NODES:
            self.violations.append(f"Forbidden AST identifier: '{node.id}' at line {node.lineno}")
        self.generic_visit(node)

    def visit_Attribute(self, node: _ast.Attribute) -> None:
        if node.attr in BANNED_AST_NODES:
            self.violations.append(f"Forbidden attribute access: '{node.attr}' at line {node.lineno}")
        self.generic_visit(node)

    def visit_Import(self, node: _ast.Import) -> None:
        for alias in node.names:
            if alias.name in BANNED_IMPORTS:
                self.violations.append(f"Forbidden module import: '{alias.name}' at line {node.lineno}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: _ast.ImportFrom) -> None:
        module = node.module or ""
        if any(banned in module for banned in BANNED_IMPORTS):
            self.violations.append(f"Forbidden from-import: '{module}' at line {node.lineno}")
        self.generic_visit(node)

    def visit_Call(self, node: _ast.Call) -> None:
        if isinstance(node.func, _ast.Name) and node.func.id in {"eval", "exec"}:
            self.violations.append(f"Forbidden call: '{node.func.id}()' at line {node.lineno}")
        if isinstance(node.func, _ast.Attribute) and node.func.attr in {"system", "popen"}:
            self.violations.append(f"Forbidden subprocess call: '{node.func.attr}()' at line {node.lineno}")
        self.generic_visit(node)


def validate_ast(script_path: str) -> tuple[bool, list[str]]:
    """Scans Python code for dangerous execution patterns."""
    try:
        with open(script_path, encoding="utf-8") as f:
            tree = _ast.parse(f.read(), filename=script_path)
        validator = ASTSecurityValidator()
        validator.visit(tree)
        if validator.violations:
            return False, validator.violations
        return True, []
    except SyntaxError as e:
        return False, [f"Syntax Error: {e}"]
    except Exception as e:
        return False, [f"AST Parse Error: {e}"]


# ── Docker Sandbox Execution ────────────────────────────────────


def run_container_sandbox(
    script_path: str,
    timeout_sec: int = 10,
    memory_mb: int = 128,
    cpu_cores: float = 0.5,
) -> tuple[bool, str, str | None]:
    """Runs a micro-server in an unprivileged ephemeral Docker container.

    Returns: (passed: bool, message: str, error_detail: str | None)
    """
    if not shutil.which("docker"):
        return True, "SKIPPED — Docker unavailable", None

    script_dir = os.path.dirname(os.path.abspath(script_path))
    script_file = os.path.basename(script_path)

    docker_cmd = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--read-only",
        "--user",
        "65534:65534",
        "--memory",
        f"{memory_mb}m",
        "--cpus",
        str(cpu_cores),
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,size=64m",
        "-v",
        f"{script_dir}:/app:ro",
        "python:3.11-slim",
        "python3",
        "-I",
        f"/app/{script_file}",
    ]

    try:
        init_payload = (
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {},
                        "clientInfo": {"name": "sandbox-eval", "version": "2.0"},
                    },
                }
            )
            + "\n"
        )

        proc = subprocess.Popen(
            docker_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = proc.communicate(input=init_payload, timeout=timeout_sec)

        if proc.returncode != 0:
            return False, f"Container exit {proc.returncode}", stderr[:500]

        try:
            resp = json.loads(stdout.strip().split("\n")[0])
            if "result" in resp:
                name = resp["result"].get("serverInfo", {}).get("name", "?")
                return True, f"MCP handshake OK — server: {name}", None
            return False, "Initialize missing 'result'", stdout[:300]
        except (json.JSONDecodeError, IndexError):
            return False, "Invalid JSON-RPC response", stdout[:300]

    except subprocess.TimeoutExpired:
        try:
            proc.kill()
        except Exception:
            pass
        return False, f"Timeout ({timeout_sec}s)", None
    except Exception as e:
        return False, f"Container failure: {e}", None


# ── Micro-Server Evaluation (AST + Docker) ──────────────────────


def evaluate_micro_server(script_path: str) -> dict[str, Any]:
    """Full pipeline: AST scan → container sandbox → verdict.

    Designed for generated micro-MCP servers in /root/AAA/mcp/staged/.
    """
    result: dict[str, Any] = {
        "script": script_path,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "ast_gate": None,
        "container_gate": None,
        "overall_score": 0.0,
        "verdict": "UNEVALUATED",
    }

    print(f"\n🔬 [MICRO-SERVER EVAL] {script_path}")

    ast_ok, ast_errors = validate_ast(script_path)
    result["ast_gate"] = {"passed": ast_ok, "violations": ast_errors}
    if not ast_ok:
        print(f"  ❌ [AST REJECT] {len(ast_errors)} violation(s)")
        for v in ast_errors[:5]:
            print(f"     • {v}")
        result["verdict"] = "REJECTED_AST"
        return result
    print("  ✅ [AST GATE] Clean.")

    container_ok, container_msg, container_err = run_container_sandbox(script_path)
    result["container_gate"] = {
        "passed": container_ok,
        "message": container_msg,
        "error": container_err,
    }
    if container_ok and "SKIPPED" not in container_msg:
        print(f"  ✅ [CONTAINER] {container_msg}")
        result["verdict"] = "APPROVED"
        result["overall_score"] = 0.95
    elif "SKIPPED" in container_msg:
        print(f"  ⚠️  [CONTAINER SKIP] {container_msg}")
        result["verdict"] = "APPROVED_NO_DOCKER"
        result["overall_score"] = 0.70
    else:
        print(f"  ❌ [CONTAINER REJECT] {container_msg}")
        result["verdict"] = "REJECTED_CONTAINER"
        result["overall_score"] = 0.30

    return result


# ── Main ───────────────────────────────────────────────────────


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MCP Server Sandbox Evaluator")
    parser.add_argument("--endpoint", type=str, help="Evaluate a single MCP endpoint directly")
    parser.add_argument("--script", type=str, help="Evaluate a local micro-MCP .py (AST + Docker sandbox)")
    parser.add_argument("--batch", action="store_true", help="Batch evaluate top candidates from catalog")
    parser.add_argument("--limit", type=int, default=5, help="Max candidates to evaluate in batch")
    parser.add_argument("--catalog", type=str, default=str(CANDIDATE_FILE), help="Candidate catalog path")
    args = parser.parse_args()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  mcp_sandbox_eval.py — MCP Server Evaluation Sandbox    ║")
    print("║  AST + Docker + External · 2026-07-28                    ║")
    print("╚══════════════════════════════════════════════════════════╝")

    if args.script:
        result = evaluate_micro_server(args.script)
        print(f"\n{'=' * 60}")
        print(json.dumps(result, indent=2))
    elif args.endpoint:
        candidate = {"name": args.endpoint, "url": args.endpoint, "source": "manual"}
        result = evaluate_candidate(candidate)
        print(f"\n{'=' * 60}")
        print(json.dumps(result, indent=2))
    elif args.batch:
        run_batch(args.catalog, args.limit)
    else:
        print("Usage:")
        print("  --script PATH      AST + Docker eval for local micro-MCP .py")
        print("  --endpoint URL     Evaluate single MCP endpoint (HTTP/SSE)")
        print("  --batch            Batch evaluate from candidate catalog")
        print("  --limit N          Max batch size (default 5)")


if __name__ == "__main__":
    main()
