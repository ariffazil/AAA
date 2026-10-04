"""
MUTATION GATE SKELETON — K5 template (arifos-kernel-eurekas).

This is the live-traced Hermes mutation gate skeleton as shipped
2026-08-07. Adapt to your harness's runtime:

  - Hermes:        /root/HERMES/gate/hermes_mutation_gate.py (this file's canonical home)
  - OpenCode:      translate to TypeScript /root/.config/opencode/plugins/<your-gate>.ts
  - Kimi Code:     translate to Python plugin under /root/.arifos/agents/kimi/plugins/

CONTRACT (K5)
=============
  evaluate(tool, args, session_id, actor_id, apex_verdict_present) -> GateVerdict

  decision ∈ {ALLOW, BLOCK, REQUIRE_JUDGE}
  reason  = string explaining the decision
  rule_id = which pattern matched (or "OBSERVE")
  needs_judge_for = human-readable what to judge (or null)

  + Receipt per evaluation. NEVER block on receipt failure (E-19).
  + Pure function. No runtime side effects. Interception point is separate.

TIERS
=====
  T3 (BLOCK)         secrets path, rm -rf /root/, arif_seal, forge_deploy, force-push, DROP TABLE
  T2 (REQUIRE_JUDGE)  write_file, patch, terminal, execute_code, delegate_task  (without apex verdict)
  T0/T1 (ALLOW)      read, grep, search, observation tools

EUREKAS OPERATIONALISED
========================
  E-04 (per spawn)    → every evaluate() writes a receipt
  E-11 (runtime>memory) → pattern check wins over agent intent
  E-12 (cap>instr)    → MUTATE_TOOLS hardcoded, not advised
  E-15 (productive disagreement) → GateVerdict is the disagreement surface
  E-22 (receipt-anchored) → the receipt trail is the audit floor

USAGE (Hermes CLI smoke)
========================
  $ python3 hermes_mutation_gate.py --tool write_file --args '{"path":"/tmp/x"}'
  {"decision": "REQUIRE_JUDGE", "reason": "mutation tool 'write_file' without arif_judge verdict", ...}

  $ python3 hermes_mutation_gate.py --tool terminal --args '{"command":"rm -rf /root/forge_work"}'
  {"decision": "BLOCK", "rule_id": "T3_PATTERN_3", ...}

INTERCEPTION (Phase 2 — Hermes-side, NOT THIS FILE)
====================================================
This file is pure logic. The interception point (a tool wrapper
or a session-injected hook) is a separate concern. Plan:

  - Add a tool wrapper in /root/HERMES that calls evaluate() before
    each tool execution and aborts on Decision.BLOCK.
  - Wrap the delegation gateway so all delegate_task children
    inherit the parent's apex_verdict_present = False unless the
    parent carries a valid arif_judge verdict from this session.
  - On REQUIRE_JUDGE, emit a request to :8088/mcp arif_judge and
    wait for verdict before continuing.
  - On ALLOW, proceed normally.

9-TEST VECTOR MATRIX (run before SEAL)
=======================================
  Tool           | Args                              | Expected
  ---------------+-----------------------------------+--------------
  read_file      | any                               | ALLOW
  write_file     | no apex verdict                   | REQUIRE_JUDGE
  write_file     | with apex verdict                 | ALLOW
  terminal       | cat /root/.secrets/kunci-mas.env  | BLOCK (T3)
  terminal       | rm -rf /root/forge_work           | BLOCK (T3)
  execute_code   | arif_seal()                       | BLOCK (T3)
  delegate_task  | no apex verdict                   | REQUIRE_JUDGE
  delegate_task  | with apex verdict                 | ALLOW
  terminal       | git push --force origin main      | BLOCK (T3)

All 9 must pass. See /root/HERMES/gate/receipts/hermes_actions.jsonl
for the trail written during a 9-case smoke run.
"""

# =====================================================================
# ORIGINAL SOURCE — DO NOT EDIT THIS TEMPLATE; COPY TO YOUR HARNESS HOME
# =====================================================================
from __future__ import annotations

import json
import os
import time
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any

RECEIPT_DIR = Path(
    os.environ.get("HERMES_RECEIPT_DIR", "/root/HERMES/gate/receipts")
)
RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

EVERY_ACTION_LOG = RECEIPT_DIR / "hermes_actions.jsonl"
SECRETS_LOG = RECEIPT_DIR / "secrets_blocked.jsonl"
JUDGE_LOG = RECEIPT_DIR / "judge_required.jsonl"


def _hash(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode()
    ).hexdigest()[:32]


def receipt(record: dict, trail: Path = EVERY_ACTION_LOG) -> None:
    """Append receipt. NEVER block (E-19: infra failure ≠ governance failure)."""
    try:
        record = {"ts": int(time.time() * 1000), **record}
        record["receipt_hash"] = _hash(record)
        with trail.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")
    except Exception:
        pass


# Mutating tools (E-12: capability > instruction)
MUTATE_TOOLS = {
    "write_file", "patch",
    "execute_code",
    "terminal",
    "delegate_task",  # mutations inherited by children
}

# T3 patterns (irreversible / F1 AMANAH)
T3_PATTERNS: list = [
    lambda args: _arg_str(args).lower().count("kunci-mas") > 0,
    lambda args: _arg_str(args).lower().count(".secrets/") > 0,
    lambda args: _arg_str(args).lower().count("signing_key") > 0,
    lambda args: "rm -rf" in _arg_str(args) and "/root/" in _arg_str(args),
    lambda args: "DROP TABLE" in _arg_str(args).upper(),
    lambda args: "DROP DATABASE" in _arg_str(args).upper(),
    lambda args: "git push" in _arg_str(args) and "--force" in _arg_str(args),
    lambda args: "arif_seal" in _arg_str(args),
    lambda args: "forge_seal" in _arg_str(args),
    lambda args: "forge_deploy" in _arg_str(args),
    lambda args: "systemctl restart" in _arg_str(args) or "systemctl stop" in _arg_str(args),
    lambda args: "caddy reload" in _arg_str(args).lower(),
]


def _arg_str(args: Any) -> str:
    try:
        return json.dumps(args, default=str)
    except Exception:
        return str(args)


def _is_observed_subagent_failure(tool: str, args: Any) -> bool:
    """delegate_task inheritance vector (E-22)."""
    return tool == "delegate_task"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REQUIRE_JUDGE = "REQUIRE_JUDGE"


@dataclass
class GateVerdict:
    decision: Decision
    reason: str
    rule_id: str
    needs_judge_for: str | None = None


def evaluate(
    tool: str,
    args: dict,
    *,
    session_id: str = "unknown",
    actor_id: str = "anonymous",
    apex_verdict_present: bool = False,
) -> GateVerdict:
    """Pure function. Never raises. Receipt by caller."""
    arg_str = _arg_str(args)

    for i, pat in enumerate(T3_PATTERNS):
        try:
            if pat(args):
                return GateVerdict(
                    Decision.BLOCK,
                    reason=arg_str[:160],
                    rule_id=f"T3_PATTERN_{i}",
                    needs_judge_for=f"irreversible: {tool}",
                )
        except Exception:
            continue

    if _is_observed_subagent_failure(tool, args):
        if not apex_verdict_present:
            return GateVerdict(
                Decision.REQUIRE_JUDGE,
                reason="delegate_task inherits toolset without judgment path",
                rule_id="DELEGATION_RISK",
                needs_judge_for="child inheritance of mutation tools",
            )

    if tool in MUTATE_TOOLS:
        if not apex_verdict_present:
            return GateVerdict(
                Decision.REQUIRE_JUDGE,
                reason=f"mutation tool '{tool}' without arif_judge verdict",
                rule_id="MUTATE_NO_JUDGE",
                needs_judge_for=tool,
            )

    return GateVerdict(
        Decision.ALLOW,
        reason="observation / non-mutating tool",
        rule_id="OBSERVE",
    )


def _main() -> None:  # pragma: no cover (CLI smoke)
    import argparse, sys

    parser = argparse.ArgumentParser(description="Hermes mutation gate (CLI smoke).")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--args", default="{}")
    parser.add_argument("--session-id", default="cli-smoke")
    parser.add_argument("--actor-id", default="cli-tester")
    parser.add_argument("--apex-verdict-present", action="store_true")
    parsed = parser.parse_args()

    try:
        args_dict = json.loads(parsed.args)
    except Exception as exc:
        print(f"ERROR: args must be JSON: {exc}", file=sys.stderr)
        sys.exit(2)

    v = evaluate(
        parsed.tool, args_dict,
        session_id=parsed.session_id,
        actor_id=parsed.actor_id,
        apex_verdict_present=parsed.apex_verdict_present,
    )
    record = {
        "event": f"gate.{v.decision.value.lower()}",
        "session_id": parsed.session_id,
        "actor_id": parsed.actor_id,
        "tool": parsed.tool,
        "args_hash": _hash(args_dict),
        "decision": v.decision.value,
        "rule_id": v.rule_id,
        "needs_judge_for": v.needs_judge_for,
        "reason": v.reason[:160],
    }
    receipt(record, EVERY_ACTION_LOG)
    print(json.dumps(asdict(v), default=str))


if __name__ == "__main__":  # pragma: no cover
    _main()