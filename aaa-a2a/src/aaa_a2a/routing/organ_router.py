"""Organ Router — intent → MCP organ dispatch.

Routes A2A tasks to the correct federation organ via MCP HTTP.
Each organ owns a domain: GEOX=earth, WEALTH=capital, WELL=vitality, etc.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import httpx
from typing import Any


# ── Organ Registry ───────────────────────────────────────────────────────

ORGANS: dict[str, dict[str, str]] = {
    "arifos": {
        "name": "arifOS Kernel",
        "url": "http://localhost:8088",
        "authority": "judge",
        "domain": "governance",
    },
    "aforge": {
        "name": "A-FORGE Execution Shell",
        "url": "http://localhost:7072",
        "authority": "execute",
        "domain": "execution",
    },
    "geox": {
        "name": "GEOX Earth Intelligence",
        "url": "http://localhost:8081",
        "authority": "evidence",
        "domain": "earth",
    },
    "wealth": {
        "name": "WEALTH Capital Intelligence",
        "url": "http://localhost:18082",
        "authority": "evidence",
        "domain": "capital",
    },
    "well": {
        "name": "WELL Human Readiness",
        "url": "http://localhost:18083",
        "authority": "evidence",
        "domain": "vitality",
    },
}


# ── Intent Keywords → Organ ──────────────────────────────────────────────

INTENT_KEYWORDS: dict[str, list[str]] = {
    "geox": [
        "seismic",
        "basin",
        "petrophysics",
        "well log",
        "geology",
        "earth",
        "reservoir",
        "stratigraphy",
    ],
    "wealth": [
        "capital",
        "finance",
        "npv",
        "irr",
        "stock",
        "investment",
        "budget",
        "cost",
        "money",
    ],
    "well": ["sleep", "fatigue", "vitality", "health", "readiness", "energy", "stress", "wellness"],
    "aforge": ["build", "deploy", "execute", "code", "git", "docker", "shell", "forge"],
    "arifos": ["judge", "verdict", "seal", "vault", "constitution", "floor", "governance"],
}


def route_intent(text: str) -> str:
    """Route natural language intent to organ ID.

    Returns organ ID or "arifos" as default.
    """
    lower = text.lower()

    # Score each organ by keyword matches
    scores: dict[str, int] = {}
    for organ, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in lower)
        if score > 0:
            scores[organ] = score

    if not scores:
        return "arifos"  # Default to kernel

    return max(scores, key=scores.get)  # type: ignore[arg-type]


async def call_mcp_tool(
    organ_id: str,
    tool_name: str,
    arguments: dict[str, Any] | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Call an MCP tool on a federation organ.

    Args:
        organ_id: Organ ID (geox, wealth, well, aforge, arifos)
        tool_name: MCP tool name
        arguments: Tool arguments
        timeout: Request timeout in seconds

    Returns:
        Tool result dict with 'ok', 'result'/'error'
    """
    organ = ORGANS.get(organ_id)
    if not organ:
        return {"ok": False, "error": f"Unknown organ: {organ_id}"}

    mcp_url = f"{organ['url']}/mcp"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                mcp_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments or {},
                    },
                },
                timeout=timeout,
            )
            resp.raise_for_status()
            data = resp.json()
            if "error" in data:
                return {"ok": False, "error": data["error"]}
            return {"ok": True, "result": data.get("result", {})}
    except httpx.TimeoutException:
        return {"ok": False, "error": f"Timeout calling {organ_id}/{tool_name}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


async def probe_organ(organ_id: str) -> dict[str, Any]:
    """Probe an organ's health endpoint.

    Returns health status dict.
    """
    organ = ORGANS.get(organ_id)
    if not organ:
        return {"healthy": False, "error": f"Unknown organ: {organ_id}"}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{organ['url']}/health", timeout=5.0)
            resp.raise_for_status()
            return {"healthy": True, "data": resp.json()}
    except Exception as e:
        return {"healthy": False, "error": str(e)}


async def probe_all_organs() -> dict[str, dict]:
    """Probe all organs. Returns dict of organ_id → health status."""
    import asyncio

    results = {}
    probes = {organ_id: probe_organ(organ_id) for organ_id in ORGANS}
    for organ_id, coro in probes.items():
        results[organ_id] = await coro
    return results
