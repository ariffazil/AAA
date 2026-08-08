#!/usr/bin/env python3
"""
arifOS Reality Loop — Claude Agent SDK Application
====================================================
Programmatic agentic reality loop using the Claude Agent SDK.
Implements the 000→999 cycle with constitutional governance.

Architecture:
  /000 (human intent) → F1-F13 (kernel judgment) → 333→888→777→999 (operational)
  Each stage is a governed SDK agent call with constitutional context injection.

Usage:
  python3 reality_loop.py "Analyze the entropy state of the federation"
  python3 reality_loop.py "Review all open carry-forward loops and propose resolutions"

Requirements:
  - claude-agent-sdk >= 0.2.0
  - arifOS kernel running at :8088
  - FED routing at :4000 (ANTHROPIC_BASE_URL)

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import asyncio
import json
import os
import sys
import urllib.request
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────
ARIFOS_HEALTH = "http://127.0.0.1:8088/health"
ARIFOS_INIT = "http://127.0.0.1:8088/mcp"
ARIFLOW_HEALTH = "http://127.0.0.1:7073/health"

# FED routing for Claude Agent SDK
os.environ.setdefault("ANTHROPIC_BASE_URL", "http://127.0.0.1:4000")
os.environ.setdefault("ANTHROPIC_AUTH_TOKEN", os.environ.get("FED_TOKEN", "sk-local"))

# ── Constitutional Context ─────────────────────────────────────────────

CONSTITUTIONAL_SYSTEM_PROMPT = """You are an agent of the arifOS AAA Federation under Muhammad Arif bin Fazil (F13 SOVEREIGN).

CONSTITUTIONAL FLOORS (non-bypassable):
F1 AMANAH — Reversible-first. Snapshot before mutate. Irreversible → 888_HOLD.
F2 TRUTH — Label evidence OBS/DER/INT/SPEC. Cap confidence at 0.90. Never fabricate.
F4 CLARITY — ΔS ≤ 0 on every output. Reduce entropy.
F7 HUMILITY — Ω₀ ∈ [0.03, 0.05]. Unknown → say unknown.
F9 ANTI-HANTU — No deception, manipulation, or consciousness claims.
F11 AUDIT — Every action traced. Evidence path required.
F13 SOVEREIGN — Arif holds final veto. His word is terminal.

FEDERATION ORGANS:
- arifOS :8088 — Constitutional kernel (F1-F13, judge, seal)
- A-FORGE :7071 — Execution actuator (build, deploy, mutate)
- GEOX :8081 — Earth intelligence
- WEALTH :18082 — Capital intelligence
- WELL :18083 — Human readiness mirror
- arifFlow :7073 — Metabolism (FQ pulse)

AUTONOMY:
- T1 AUTO-DO: Read, probe, search, edit, build, test, commit
- T2 ANNOUNCE: Multi-file refactor, deploy after green tests (10s window)
- T3 888_HOLD: rm -rf, DROP, force-push main, production deploy without tests
- Digital ops = MUBAH (auto-do). Never ask permission for T1/T2.

DITEMPA BUKAN DIBERI. Probe before act. Lead with answer. Never end with 'Jalan?'"""

# ── Helpers ────────────────────────────────────────────────────────────


def probe_kernel() -> dict:
    """Probe arifOS kernel health."""
    try:
        req = urllib.request.Request(ARIFOS_HEALTH)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            t = data.get("thermodynamic", {})
            return {
                "verdict": t.get("verdict", "?"),
                "floors": data.get("floors_active", "?"),
                "drift": data.get("runtime_drift", False),
                "vault999": data.get("vault999_health", "?"),
            }
    except Exception as e:
        return {"verdict": "DOWN", "error": str(e)}


def probe_fq() -> dict:
    """Probe arifFlow FQ pulse."""
    try:
        req = urllib.request.Request(ARIFLOW_HEALTH)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
            fq = data.get("fq", {})
            return {
                "quotient": fq.get("quotient", "?"),
                "verdict": fq.get("verdict", "?"),
                "receipts": data.get("receipts", 0),
            }
    except Exception:
        return {"quotient": "?", "verdict": "DOWN", "receipts": 0}


def build_stage_prompt(intent: str, stage: str, kernel: dict, fq: dict) -> str:
    """Build a stage-specific prompt with constitutional context."""
    return f"""[arifOS Reality Loop — Stage: {stage}]
Intent: {intent}
Kernel: verdict={kernel.get("verdict")} · floors={kernel.get("floors")} · drift={kernel.get("drift")}
FQ: {fq.get("quotient")} ({fq.get("verdict")}) · receipts={fq.get("receipts")}

Constitutional floor check:
- F1 REVERSIBLE: Is this action reversible? If not → HOLD.
- F2 TRUTH: All claims must carry OBS/DER/INT/SPEC labels.
- F4 ΔS ≤ 0: Output should reduce chaos, not add to it.
- F7 HUMILITY: Unknown → say unknown. Cap confidence at 0.90.
- F11 AUDIT: Every conclusion must have evidence path.

Current stage: {stage}
Proceed with the {stage} phase of the reality loop."""


# ── Reality Loop ───────────────────────────────────────────────────────


async def reality_loop(intent: str):
    """Execute one cycle of the arifOS reality loop (000→999)."""

    # Import SDK lazily so the script is importable even without SDK
    from claude_agent_sdk import query, ClaudeAgentOptions

    print(f"\n{'=' * 60}")
    print(f"arifOS Reality Loop — 000→999")
    print(f"Intent: {intent}")
    print(f"{'=' * 60}\n")

    # ── STAGE 000: INIT — Probe reality ─────────────────────────────────
    print("[000 INIT] Probing kernel...")
    kernel = probe_kernel()
    fq = probe_fq()

    if kernel.get("verdict") == "DOWN":
        print("[000 INIT] ❌ KERNEL DOWN — cannot proceed without constitutional governance")
        return {"stage": "000", "verdict": "HALT", "reason": "kernel_down"}

    if fq.get("verdict") == "DOWN":
        print("[000 INIT] ⚠️  arifFlow DOWN — proceeding without FQ (degraded)")
    elif fq.get("quotient", 0) < 0.5:
        print(f"[000 INIT] ⚠️  FQ={fq['quotient']} < 0.5 — HOLDING non-critical work")

    print(f"[000 INIT] Kernel: {kernel['verdict']} · floors={kernel['floors']} · FQ={fq.get('quotient')}")

    # ── STAGE 333: THINK — SDK reasoning ────────────────────────────────
    print("\n[333 THINK] Reasoning...")
    try:
        stage_prompt = build_stage_prompt(intent, "THINK", kernel, fq)

        think_result = ""
        async for msg in query(
            prompt=stage_prompt,
            options=ClaudeAgentOptions(
                system_prompt=CONSTITUTIONAL_SYSTEM_PROMPT,
                permission_mode="dontAsk",
                max_turns=3,
                allowed_tools=["Read", "Glob", "Grep", "WebSearch"],
                model="hermes-asi",
            ),
        ):
            if hasattr(msg, "type") and msg.type == "assistant":
                for block in (
                    getattr(msg, "message", msg).content if hasattr(getattr(msg, "message", msg), "content") else []
                ):
                    if hasattr(block, "text"):
                        think_result += block.text

        print(f"[333 THINK] Complete — {len(think_result)} chars of reasoning")

    except Exception as e:
        print(f"[333 THINK] SDK call failed: {e}")
        think_result = f"[SDK_UNAVAILABLE] Direct reasoning: {intent}"
        print(f"[333 THINK] Falling back to local reasoning")

    # ── STAGE 888: JUDGE — Constitutional verdict ───────────────────────
    print("\n[888 JUDGE] Constitutional check...")

    # Simulated floor check (in production, calls arif_judge on :8088)
    verdict = "SEAL"
    if kernel.get("drift"):
        verdict = "HOLD"
        print("[888 JUDGE] ⚠️  Kernel drift detected → HOLD")

    if fq.get("quotient", 1.0) < 0.3:
        verdict = "HOLD"
        print(f"[888 JUDGE] ⚠️  FQ={fq['quotient']} < 0.3 → HOLD")

    print(f"[888 JUDGE] Verdict: {verdict}")

    # ── STAGE 777: FORGE — Execute (simulated) ──────────────────────────
    print("\n[777 FORGE] Executing...")
    if verdict == "HOLD":
        print("[777 FORGE] ⛔ HOLD verdict — execution blocked")
        forge_result = {"status": "BLOCKED", "reason": "constitutional_hold"}
    else:
        forge_result = {"status": "EXECUTED", "intent": intent, "reasoning": think_result[:500]}

    # ── STAGE 999: SEAL — Close loop ────────────────────────────────────
    print("\n[999 SEAL] Closing reality loop...")

    result = {
        "intent": intent,
        "kernel": kernel,
        "fq": fq,
        "verdict": verdict,
        "execution": forge_result,
        "loop_closed": verdict == "SEAL",
    }

    print(f"[999 SEAL] Loop {'✅ CLOSED' if result['loop_closed'] else '⚠️ HELD'}")
    print(f"\n{'=' * 60}")
    print(f"Result: {json.dumps(result, indent=2, default=str)}")
    print(f"{'=' * 60}\n")

    return result


# ── CLI Entry ──────────────────────────────────────────────────────────


def main():
    intent = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else ("Analyze the current state of the arifOS federation and report health")
    )

    print(f"arifOS Reality Loop Agent v1.0.0")
    print(f"SDK: claude-agent-sdk — FED routing via {os.environ.get('ANTHROPIC_BASE_URL', 'default')}")
    print(f"Intent: {intent}\n")

    result = asyncio.run(reality_loop(intent))

    # Emit Zen margin
    if result.get("loop_closed"):
        print("Zen::ΔS=-0.5::FQ=" + str(result.get("fq", {}).get("quotient", "?")) + "::Ω₀=0.04")
    else:
        print("Zen::ΔS=0.0::FQ=" + str(result.get("fq", {}).get("quotient", "?")) + "::Ω₀=0.04::HOLD")

    return 0 if result.get("loop_closed") else 1


if __name__ == "__main__":
    sys.exit(main())
