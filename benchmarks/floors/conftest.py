"""
Shared test infrastructure for F1–F13 floor benchmarks.

Provides:
- async HTTP client for arifOS MCP (localhost:8088)
- Kernel availability check (skip if offline)
- Response extraction helpers
- Structured result logging
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import httpx
import pytest

# ── Paths ─────────────────────────────────────────────────────────────────────
RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Kernel Configuration ─────────────────────────────────────────────────────
KERNEL_URL = os.environ.get("ARIFOS_KERNEL_URL", "http://localhost:8088")
KERNEL_TIMEOUT = float(os.environ.get("ARIFOS_TIMEOUT", "10.0"))


# ── Kernel Liveness Check (synchronous — runs at module load) ──────────────
def check_kernel_alive_sync() -> bool:
    """Probe arifOS kernel with a synchronous ping. Returns True if reachable."""
    try:
        with httpx.Client(
            base_url=KERNEL_URL, timeout=KERNEL_TIMEOUT
        ) as client:
            resp = client.post(
                "/mcp",
                headers={"Accept": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "id": "liveness",
                    "method": "tools/call",
                    "params": {
                        "name": "arif_ping",
                        "arguments": {"mode": "probe"},
                    },
                },
            )
            if resp.status_code != 200:
                return False
            body = resp.json()
            # MCP returns content wrapped in text blocks
            result = body.get("result") or {}
            is_error = result.get("isError", False)
            if is_error:
                return False
            # Try structuredContent if present (arifOS native)
            sc = result.get("structuredContent") or {}
            if sc.get("verdict") in ("SEAL", "OK"):
                return True
            if sc.get("status") in ("OK", "SEAL"):
                return True
            # Fallback: try text content parsing
            content = result.get("content") or []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text = item.get("text", "")
                    if '"verdict": "SEAL"' in text or '"status": "OK"' in text:
                        return True
            # If we got here and the tool responded without error, kernel is alive
            return True
    except Exception:
        return False


_kernel_available = check_kernel_alive_sync()

kernel_alive = pytest.mark.skipif(
    not _kernel_available,
    reason="arifOS kernel unreachable at " + KERNEL_URL,
)


# ── MCP Call Helpers ─────────────────────────────────────────────────────────
async def call_tool(
    tool: str,
    arguments: dict[str, Any] | None = None,
    session_id: str | None = None,
    actor_id: str = "forge-bench",
) -> dict[str, Any]:
    """Call an arifOS MCP tool and return the parsed response envelope.

    Returns the **structuredContent** dict (the top-level envelope with
    ``verdict``, ``status``, ``result``, etc.).

    On transport/HTTP error, returns ``{"verdict": "ERROR", "status": "ERROR",
    "error": <message>}``.
    """
    params: dict[str, Any] = {"name": tool, "arguments": arguments or {}}
    if session_id:
        params["arguments"]["session_id"] = session_id
    if actor_id:
        params["arguments"]["actor_id"] = actor_id

    try:
        async with httpx.AsyncClient(
            base_url=KERNEL_URL, timeout=KERNEL_TIMEOUT
        ) as client:
            resp = await client.post(
                "/mcp",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "id": f"call-{tool}",
                    "method": "tools/call",
                    "params": params,
                },
            )
    except Exception as exc:
        return {"verdict": "ERROR", "status": "ERROR", "error": str(exc)}

    if resp.status_code != 200:
        return {
            "verdict": "ERROR",
            "status": "ERROR",
            "http_status": resp.status_code,
            "body": resp.text[:500],
        }

    try:
        body = resp.json()
    except Exception as exc:
        return {"verdict": "ERROR", "status": "ERROR", "error": f"JSON parse: {exc}"}

    # MCP error → extract error data
    if "error" in body:
        err = body["error"]
        data = err.get("data", {})
        return {
            "verdict": data.get("verdict", "HOLD"),
            "status": "ERROR",
            "mcp_error": err.get("message", "Unknown MCP error"),
            "code": err.get("code"),
            "blocked_at": data.get("blocked_at"),
            "reasons": data.get("reasons", []),
            "violated_laws": data.get("violated_laws", []),
            "gate_results": data.get("gate_results", []),
            "raw": body,
        }

    return extract_structured(body)


def extract_structured(response: dict[str, Any]) -> dict[str, Any]:
    """Extract the structured envelope from an MCP response (result or error)."""
    if "error" in response:
        return {"verdict": "HOLD", "status": "ERROR", "raw": response}
    result = response.get("result", {})
    # structuredContent is the server-side envelope
    sc = result.get("structuredContent", {})
    if sc:
        return sc
    # fallback: parse text content
    for c in result.get("content", []):
        if c.get("type") == "text":
            try:
                return json.loads(c["text"])
            except (json.JSONDecodeError, KeyError):
                continue
    return {"verdict": "UNKNOWN", "status": "ERROR", "raw": response}


def get_verdict(response: dict[str, Any]) -> str:
    """Safely extract verdict string from any response."""
    return response.get("verdict", "UNKNOWN") or "UNKNOWN"


def get_status(response: dict[str, Any]) -> str:
    """Safely extract status string."""
    return response.get("status", "UNKNOWN") or "UNKNOWN"


# ── Result Recorder ──────────────────────────────────────────────────────────
def record_result(
    floor: str,
    test_id: str,
    description: str,
    expected_verdict: str,
    actual_verdict: str,
    passed: bool,
    details: dict[str, Any] | None = None,
) -> None:
    """Append a single test result to the floor's result JSON file."""
    result_file = RESULTS_DIR / f"{floor}_results.json"
    entry = {
        "test_id": test_id,
        "floor": floor,
        "description": description,
        "expected_verdict": expected_verdict,
        "actual_verdict": actual_verdict,
        "passed": passed,
        "details": details or {},
    }
    # Load existing results
    if result_file.exists():
        with open(result_file) as f:
            data = json.load(f)
    else:
        data = {"suite": floor, "results": []}
    data["results"].append(entry)
    data["summary"] = _summarize(data["results"])
    with open(result_file, "w") as f:
        json.dump(data, f, indent=2, default=str)


def _summarize(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total * 100, 1) if total else 0.0,
    }


# ── Pytest fixtures ─────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def kernel_session():
    """Create a light session for the test module. Yields session_id."""
    resp = await call_tool(
        "arif_session_init",
        {"mode": "light", "actor_id": "forge-bench"},
    )
    sid = resp.get("result", {}).get("session_id")
    if not sid:
        sid = resp.get("session_id")
    if not sid and resp.get("status") == "OK":
        sid = "SEAL-bench-default"
    yield sid or "SEAL-bench-default"


@pytest.fixture(scope="module")
async def kernel_attestation():
    """Fetch kernel attestation once per module."""
    return await call_tool("arif_os_attest", {"actor_id": "forge-bench"})
