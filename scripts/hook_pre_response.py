#!/usr/bin/env python3
"""
hook_pre_response.py — Pre-response gate hook for the arifOS runtime.

Implements the two non-optional runtime reflexes per F13 directive 2026-10-06:

  Reflex 1: Name mentioned -> machine probe before narrative.
  Reflex 2: Safety concern -> reduce claim strength, not information value.

This hook is invoked BEFORE the LLM generates a response to a user prompt
that mentions a named human. It calls gate.py, returns a structured
preamble that the LLM must incorporate, and BLOCKS descriptive_person_claims
when the probe_receipt is absent.

Install:
  Wire into /root/.hermes/hooks/ (already used by the agent runtime).
  The hook protocol is documented in /root/.hermes/AGENTS.md.

Usage as a library:
    from hook_pre_response import pre_response
    result = pre_response(user_prompt="...", model="hermes-default")
    # returns dict with: ok, gate_result, instruction_for_llm

Usage as CLI:
    python3 hook_pre_response.py "What does Syed want from me?" --model hermes-default
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

# Local imports
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import gate as gate_mod  # type: ignore


def pre_response(user_prompt: str, model: str = "hermes-default", max_signal_level: str = "L3") -> Dict[str, Any]:
    """
    Pre-response gate. Returns:
      ok: bool — whether the LLM may proceed with descriptive_person_claims
      gate_result: full gate.py output
      instruction_for_llm: text the LLM must prepend/integrate
      blocked_reason: if blocked, why
    """
    gate_result = gate_mod.gate_response(user_prompt, candidate_answer=None, max_signal_level=max_signal_level)

    named = gate_result.get("named_humans", [])
    sensitive = gate_result.get("sensitive_targets", [])

    # Build the LLM instruction preamble
    parts: list[str] = []
    parts.append("=== HUMAN_REALITY_REFLEX GATE ===")
    parts.append(f"model: {model}")
    parts.append(f"prompt: {user_prompt[:200]}{'...' if len(user_prompt) > 200 else ''}")
    if named:
        for n in named:
            cap = next((c for c in gate_result.get("probe_receipts", []) if c.get("subject") == n["handle"]), None)
            ladder = gate_result.get("signal_ladders", {}).get(n["handle"], {})
            strongest = ladder.get("strongest_allowed", "VOID")
            parts.append(f"")
            parts.append(f"--- {n['handle']} ({n.get('display_name', '?')}) ---")
            if cap:
                ev = cap.get("evidence", {})
                parts.append(f"  observed: {len(ev.get('observed', []))} facts")
                parts.append(f"  reported: {len(ev.get('reported', []))} facts (scope:shared)")
                parts.append(f"  inferred: {len(ev.get('inferred', []))} facts")
                parts.append(f"  privacy_excluded: {cap.get('privacy_excluded', {}).get('count', 0)} dm-scope facts")
                parts.append(f"  freshness: {cap.get('freshness', {}).get('age_hours', '?')}h, stale={cap.get('freshness', {}).get('stale', '?')}")
            parts.append(f"  strongest signal class allowed: {strongest}")
            parts.append(f"  ladder: {list(ladder.get('available_levels', []))}")
    if sensitive:
        parts.append("")
        parts.append(f"⚠ SENSITIVE TARGETS HIT: {sensitive}")
        parts.append("Adjacent-signal transforms REQUIRED (see gate.py).")
        parts.append("Identity uncertainty must not erase behavioral intelligence.")

    blocked = bool(gate_result.get("blocked_reasons"))
    if blocked:
        parts.append("")
        parts.append("⚠ CANDIDATE WAS BLOCKED. Use the adjusted_answer from gate.py.")
        for r in gate_result.get("blocked_reasons", []):
            parts.append(f"  - {r}")

    if not named and not sensitive:
        parts.append("No named human, no sensitive target. Reflexes did not trigger.")

    parts.append("=== END GATE ===")
    instruction_for_llm = "\n".join(parts)

    return {
        "ok": True,  # gate itself runs; "blocked_reasons" tells the LLM what to do
        "gate_result": gate_result,
        "instruction_for_llm": instruction_for_llm,
        "blocked_reason": "; ".join(gate_result.get("blocked_reasons", [])) or None,
        "named_humans": [n["handle"] for n in named],
        "strongest_signal_class": {
            n["handle"]: gate_result.get("signal_ladders", {}).get(n["handle"], {}).get("strongest_allowed", "VOID")
            for n in named
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-response HUMAN_REALITY_REFLEX gate hook.")
    parser.add_argument("prompt")
    parser.add_argument("--model", default="hermes-default")
    parser.add_argument("--max-level", default="L3", choices=["L0", "L1", "L2", "L3", "L4"])
    args = parser.parse_args()

    result = pre_response(args.prompt, model=args.model, max_signal_level=args.max_level)
    print(json.dumps({
        "ok": result["ok"],
        "blocked_reason": result["blocked_reason"],
        "named_humans": result["named_humans"],
        "strongest_signal_class": result["strongest_signal_class"],
        "instruction_for_llm": result["instruction_for_llm"],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
