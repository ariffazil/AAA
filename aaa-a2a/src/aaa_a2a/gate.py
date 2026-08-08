"""AAA Gate Runtime — ART · AUTH · ACT · FQ · arifFLOW.

The Gate Runtime wraps the Wisdom Runtime (333→555→888).
Every A2A task passes through these gates before dispatch.

Gates operate at three scales:
  ART  = Call Scale   — "May this call enter?"
  AUTH = Task Scale   — "Was the process followed?"
  ACT  = Mutation Scale — "May reality now change?"

Plus two cross-cutting metabolic checks:
  FQ Gate       — "Is the federation healthy enough to act?"
  flow_ingest   — "Record this action in the metabolic ledger."

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import httpx

logger = logging.getLogger("aaa.gate")

# ═══════════════════════════════════════════════════════════════════════════════
# Action Classification
# ═══════════════════════════════════════════════════════════════════════════════


class ActionClass(str, Enum):
    """What kind of action is this? Escalating risk."""

    OBSERVE = "observe"  # Read-only, no side effects
    REASON = "reason"  # Think, plan, analyze
    DRAFT = "draft"  # Generate code/text, no execution
    MUTATE = "mutate"  # Edit files, restart services
    DEPLOY = "deploy"  # Production deployment
    IRREVERSIBLE = "irreversible"  # rm -rf, DROP, force push


def classify_action(text: str, target_organ: str = "") -> ActionClass:
    """Classify intent text into action class.

    Quick heuristic — ART in kernel does full power-class analysis.
    """
    lower = text.lower()

    # Irreversible patterns
    irreversible = ["rm -rf", "drop table", "force push", "delete vault", "chattr -a"]
    if any(p in lower for p in irreversible):
        return ActionClass.IRREVERSIBLE

    # Deploy patterns
    deploy = ["deploy", "production", "caddy reload", "docker push", "systemctl restart"]
    if any(p in lower for p in deploy):
        return ActionClass.DEPLOY

    # Mutate patterns
    mutate = [
        "edit",
        "write",
        "commit",
        "push",
        "restart",
        "build",
        "forge",
        "create file",
        "update",
        "modify",
        "patch",
        "install",
        "unlink",
    ]
    if any(p in lower for p in mutate):
        return ActionClass.MUTATE

    # Draft patterns
    draft = ["generate", "draft", "scaffold", "plan", "propose", "design"]
    if any(p in lower for p in draft):
        return ActionClass.DRAFT

    # Reason patterns
    reason = ["analyze", "evaluate", "simulate", "compare", "audit", "review"]
    if any(p in lower for p in reason):
        return ActionClass.REASON

    return ActionClass.OBSERVE


# ═══════════════════════════════════════════════════════════════════════════════
# Gate Results
# ═══════════════════════════════════════════════════════════════════════════════


class GateVerdict(str, Enum):
    PROCEED = "PROCEED"
    SABAR = "SABAR"  # Pause, downgrade, but may continue
    HOLD = "HOLD"  # Stop until resolved
    VOID = "VOID"  # Constitutional block


@dataclass
class GateResult:
    verdict: GateVerdict
    gate: str
    reason: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.verdict == GateVerdict.PROCEED

    @property
    def blocked(self) -> bool:
        return self.verdict in (GateVerdict.HOLD, GateVerdict.VOID)


# ═══════════════════════════════════════════════════════════════════════════════
# FQ Gate — "Is the federation healthy enough to act?"
# ═══════════════════════════════════════════════════════════════════════════════

FQ_GATE_THRESHOLD = 0.50


async def check_fq_gate(
    arifflow_url: str = "http://localhost:7073",
    timeout: float = 3.0,
) -> GateResult:
    """Probe arifFlow for FQ. HOLD if FQ < 0.50.

    Fails closed: if arifFlow unreachable, returns SABAR (degraded, not blocked).
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{arifflow_url}/health", timeout=timeout)
            resp.raise_for_status()
            data = resp.json()

        fq = data.get("fq", {})
        quotient = fq.get("quotient", 0.0)
        verdict = fq.get("verdict", "UNKNOWN")

        if quotient < FQ_GATE_THRESHOLD:
            return GateResult(
                verdict=GateVerdict.HOLD,
                gate="FQ",
                reason=f"FQ={quotient:.2f} below threshold {FQ_GATE_THRESHOLD}. Verdict: {verdict}",
                details={"fq": quotient, "verdict": verdict},
            )

        if verdict in ("OVERHEAT", "BURNING"):
            return GateResult(
                verdict=GateVerdict.SABAR,
                gate="FQ",
                reason=f"FQ verdict={verdict}. Proceeding with caution.",
                details={"fq": quotient, "verdict": verdict},
            )

        return GateResult(
            verdict=GateVerdict.PROCEED,
            gate="FQ",
            details={"fq": quotient, "verdict": verdict},
        )

    except Exception as e:
        logger.warning(f"FQ gate: arifFlow unreachable ({e}) — degraded, not blocked")
        return GateResult(
            verdict=GateVerdict.SABAR,
            gate="FQ",
            reason=f"arifFlow unreachable: {e}",
            details={"error": str(e)},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ART Gate — "May this call enter?"
# ═══════════════════════════════════════════════════════════════════════════════


async def check_art_gate(
    action_class: ActionClass,
    agent_id: str,
    tool_name: str = "",
    arifos_url: str = "http://localhost:8088",
    timeout: float = 5.0,
) -> GateResult:
    """Lightweight ART admission check.

    For MUTATE+ actions, delegates to kernel arif_judge for full constitutional review.
    For OBSERVE/REASON, applies local heuristic checks.
    """
    # OBSERVE and REASON always pass ART
    if action_class in (ActionClass.OBSERVE, ActionClass.REASON):
        return GateResult(verdict=GateVerdict.PROCEED, gate="ART")

    # DRAFT gets local heuristic check
    if action_class == ActionClass.DRAFT:
        return GateResult(
            verdict=GateVerdict.PROCEED,
            gate="ART",
            details={"note": "DRAFT — local heuristic pass, full ART deferred"},
        )

    # MUTATE, DEPLOY, IRREVERSIBLE → call kernel for constitutional review
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{arifos_url}/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "arif_judge",
                        "arguments": {
                            "mode": "judge",
                            "candidate": tool_name or action_class.value,
                            "action_tier": (
                                "irreversible"
                                if action_class == ActionClass.IRREVERSIBLE
                                else "deploy"
                                if action_class == ActionClass.DEPLOY
                                else "mutate"
                            ),
                            "actor_id": agent_id,
                        },
                    },
                },
                timeout=timeout,
            )
            resp.raise_for_status()
            data = resp.json()

        result = _extract_mcp_result(data)
        verdict_str = str(result.get("verdict", "UNMEASURED")).upper()

        if verdict_str in ("VOID",):
            return GateResult(
                verdict=GateVerdict.VOID,
                gate="ART",
                reason=f"Kernel ART: {result.get('reasons', ['constitutional block'])}",
                details=result,
            )
        if verdict_str in ("HOLD",):
            return GateResult(
                verdict=GateVerdict.HOLD,
                gate="ART",
                reason=f"Kernel ART HOLD: {result.get('reasons', ['requires review'])}",
                details=result,
            )
        if verdict_str in ("SABAR",):
            return GateResult(
                verdict=GateVerdict.SABAR,
                gate="ART",
                reason=f"Kernel ART SABAR: {result.get('reasons', ['caution'])}",
                details=result,
            )
        # SEAL or OK → proceed
        return GateResult(verdict=GateVerdict.PROCEED, gate="ART", details=result)

    except Exception as e:
        logger.warning(f"ART gate: kernel unreachable ({e}) — fail-closed SABAR")
        # For MUTATE: SABAR (degraded but not blocked — see FQ fallback pattern)
        # For DEPLOY/IRREVERSIBLE: HOLD (fail-closed on high-risk)
        if action_class in (ActionClass.DEPLOY, ActionClass.IRREVERSIBLE):
            return GateResult(
                verdict=GateVerdict.HOLD,
                gate="ART",
                reason=f"Kernel unreachable for {action_class.value}: {e}",
            )
        return GateResult(
            verdict=GateVerdict.SABAR,
            gate="ART",
            reason=f"Kernel unreachable: {e}",
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ACT Gate — "May reality now change?"
# ═══════════════════════════════════════════════════════════════════════════════


async def check_act_gate(
    action_class: ActionClass,
    session_token: str | None,
    agent_id: str,
) -> GateResult:
    """Pre-execution ACT gate.

    Validates session token presence, action class authorization,
    and checks for required ceremony markers.
    """
    # OBSERVE/REASON/DRAFT don't need ACT
    if action_class in (ActionClass.OBSERVE, ActionClass.REASON, ActionClass.DRAFT):
        return GateResult(
            verdict=GateVerdict.PROCEED,
            gate="ACT",
            details={"note": f"{action_class.value} exempt from ACT"},
        )

    # MUTATE+ requires session token
    if not session_token:
        return GateResult(
            verdict=GateVerdict.HOLD,
            gate="ACT",
            reason=f"{action_class.value} requires session_token (call arif_init first)",
            details={"missing": "session_token"},
        )

    # Validate token format
    if not _is_valid_token(session_token):
        return GateResult(
            verdict=GateVerdict.HOLD,
            gate="ACT",
            reason="Invalid session_token format",
            details={"token_prefix": session_token[:20] if session_token else "None"},
        )

    # IRREVERSIBLE requires explicit ack
    if action_class == ActionClass.IRREVERSIBLE:
        return GateResult(
            verdict=GateVerdict.HOLD,
            gate="ACT",
            reason="IRREVERSIBLE actions require explicit sovereign acknowledgment",
            details={"required": "ack_irreversible or F13 approval"},
        )

    return GateResult(verdict=GateVerdict.PROCEED, gate="ACT")


def _is_valid_token(token: str) -> bool:
    """Validate token format — act_v1.* or sct_v1.*"""
    if not token:
        return False
    return token.startswith("act_v1.") or token.startswith("sct_v1.")


# ═══════════════════════════════════════════════════════════════════════════════
# arifFLOW Ingest — "Record this action in the metabolic ledger"
# ═══════════════════════════════════════════════════════════════════════════════


async def ingest_flow(
    actor_id: str,
    session_id: str,
    step_type: str = "Execute",
    epistemic_label: str = "Derivation",
    floor_verdict: str = "Pass",
    payload: dict[str, Any] | None = None,
    arifflow_url: str = "http://localhost:7073",
    timeout: float = 3.0,
) -> dict[str, Any]:
    """Mint a flow receipt in arifFlow's metabolic ledger.

    Returns the flow receipt or error info. Non-blocking — failure is logged, not fatal.
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{arifflow_url}/ingest",
                json={
                    "actor_id": actor_id,
                    "session_id": session_id,
                    "step_type": step_type,
                    "epistemic_label": epistemic_label,
                    "floor_verdict": floor_verdict,
                    "payload": payload or {},
                },
                timeout=timeout,
            )
            resp.raise_for_status()
            return {"ok": True, "result": resp.json()}
    except Exception as e:
        logger.debug(f"flow_ingest: arifFlow unreachable ({e}) — non-fatal")
        return {"ok": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════════════════════════
# Composite Gate Runner
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class GateChainResult:
    """Result of running the full gate chain."""

    passed: bool
    art: GateResult | None = None
    fq: GateResult | None = None
    act: GateResult | None = None
    blocked_by: str = ""
    final_verdict: GateVerdict = GateVerdict.PROCEED

    @property
    def blocked(self) -> bool:
        return not self.passed


async def run_gate_chain(
    intent_text: str,
    agent_id: str,
    target_organ: str = "",
    session_token: str | None = None,
    tool_name: str = "",
) -> GateChainResult:
    """Run the full ART → FQ → ACT gate chain.

    Returns GateChainResult with per-gate results and overall pass/fail.
    Blocking on HOLD/VOID from any gate.

    Order: FQ first (cheapest), then ART, then ACT.
    """
    action_class = classify_action(intent_text, target_organ)
    result = GateChainResult(passed=True)

    # 1. FQ Gate (always — even OBSERVE watches metabolism)
    result.fq = await check_fq_gate()
    if result.fq.blocked:
        result.passed = False
        result.blocked_by = "FQ"
        result.final_verdict = result.fq.verdict
        return result

    # 2. ART Gate
    result.art = await check_art_gate(
        action_class=action_class,
        agent_id=agent_id,
        tool_name=tool_name,
    )
    if result.art.blocked:
        result.passed = False
        result.blocked_by = "ART"
        result.final_verdict = result.art.verdict
        return result

    # 3. ACT Gate
    result.act = await check_act_gate(
        action_class=action_class,
        session_token=session_token,
        agent_id=agent_id,
    )
    if result.act.blocked:
        result.passed = False
        result.blocked_by = "ACT"
        result.final_verdict = result.act.verdict
        return result

    return result


def _extract_mcp_result(data: dict) -> dict:
    """Extract result from MCP JSON-RPC response (handles SSE wrapping)."""
    if "result" in data:
        inner = data["result"]
        if isinstance(inner, dict):
            content = inner.get("content", [])
            if isinstance(content, list) and content:
                for item in content:
                    if isinstance(item, dict) and "text" in item:
                        import json

                        try:
                            return json.loads(item["text"])
                        except (json.JSONDecodeError, TypeError):
                            pass
            return inner
    return data
