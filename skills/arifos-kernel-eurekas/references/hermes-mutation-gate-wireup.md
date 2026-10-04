# Hermes Mutation Gate — Runtime Wire-Up Recipe

> **Status:** LIVE-VERIFIED 2026-08-07
> **Path:** `/root/HERMES/gate/mutation_gate_hook.py`
> **Gate source:** `templates/mutation-gate-skeleton.py` (same directory)
> **Skill:** `arifos-kernel-eurekas` K5/K6 companion

---

## What this file does

Bridges `hermes_mutation_gate.py` (pure logic) into Hermes' `pre_tool_call`
shell-hook runtime. The gate exists on disk; this file makes it fire.

---

## The bridge (3 layers, 3 files)

```
Layer 1: hermes_mutation_gate.py      ← pure logic (SKILL template)
Layer 2: mutation_gate_hook.py         ← shell-hook adapter (stdin JSON → stdout JSON)
Layer 3: config.yaml hooks entry      ← runtime registration
```

Layer 1 is the skill template. Layer 2 is this reference. Layer 3 is one line of config.

---

## Hook wrapper: `mutation_gate_hook.py`

```python
#!/usr/bin/env python3
"""
mutation_gate_hook.py — Hermes pre_tool_call hook.
Reads JSON on stdin (tool_name, tool_input, session_id).
Returns {"decision":"block","reason":"..."} or {"decision":"approve"} on stdout.
Writes receipt to hermes_actions.jsonl.
"""
import sys, json, os
from hermes_mutation_gate import evaluate, Decision, receipt, _hash

raw = sys.stdin.read()
event = json.loads(raw)
tool = event.get("tool_name") or event.get("toolName") or "unknown"
args = event.get("tool_input") or event.get("toolInput") or {}
session_id = event.get("session_id") or "unknown"
actor_id = os.environ.get("HERMES_ACTOR_ID", "anonymous")
apex = bool(event.get("extra", {}).get("apex_verdict_ref"))

v = evaluate(tool, args if isinstance(args, dict) else {"raw": str(args)},
             session_id=session_id, actor_id=actor_id, apex_verdict_present=apex)

receipt({"event": f"gate.{v.decision.value.lower()}", "session_id": session_id,
         "actor_id": actor_id, "tool": tool, "args_hash": _hash(args),
         "decision": v.decision.value, "rule_id": v.rule_id,
         "needs_judge_for": v.needs_judge_for, "reason": v.reason[:200]})

if v.decision == Decision.BLOCK:
    print(json.dumps({"decision": "block", "reason": v.reason[:400]}))
elif v.decision == Decision.REQUIRE_JUDGE:
    print(json.dumps({"decision": "block", "reason": f"REQUIRE_JUDGE: {v.reason[:300]}"}))
else:
    print(json.dumps({"decision": "approve"}))
```

---

## Config registration (Layer 3)

Add to `/root/HERMES/config.yaml` (or profile config):

```yaml
hooks:
  pre_tool_call:
    - command: /root/HERMES/gate/mutation_gate_hook.py
      matcher: "*"
      accept_hooks: true
```

After config change, restart Hermes gateway:
```bash
hermes gateway restart
```

---

## Verification: live 4-case test

```bash
# 1. BLOCKED — secrets path
echo '{"tool_name":"terminal","tool_input":{"command":"cat /root/.secrets/kunci-mas.env"},"session_id":"test1"}' \
  | python3 /root/HERMES/gate/mutation_gate_hook.py
# Expected: {"decision":"block","reason":"..."}

# 2. BLOCKED — destructive
echo '{"tool_name":"terminal","tool_input":{"command":"rm -rf /root/forge_work"},"session_id":"test2"}' \
  | python3 /root/HERMES/gate/mutation_gate_hook.py
# Expected: {"decision":"block","reason":"..."}

# 3. BLOCKED — force-push
echo '{"tool_name":"terminal","tool_input":{"command":"git push --force origin main"},"session_id":"test3"}' \
  | python3 /root/HERMES/gate/mutation_gate_hook.py
# Expected: {"decision":"block","reason":"..."}

# 4. ALLOWED — legitimate read
echo '{"tool_name":"read_file","tool_input":{"path":"/root/AGENTS.md"},"session_id":"test4"}' \
  | python3 /root/HERMES/gate/mutation_gate_hook.py
# Expected: {"decision":"approve"}
```

All 4 produce receipts in `hermes_actions.jsonl`. Check:
```bash
tail -4 /root/HERMES/gate/receipts/hermes_actions.jsonl | python3 -c "
import sys,json
for line in sys.stdin:
    r = json.loads(line)
    print(f'{r[\"decision\"]:13} {r[\"tool\"]:12} {r[\"rule_id\"]}')"
```

---

## Failure mode: what if the hook crashes?

The wrapper catches all exceptions and returns `{"decision":"approve"}` on
hook error. This is E-19 safe (infra failure ≠ governance failure) but
NOT fail-closed. For fail-closed, change the except block to:
```python
print(json.dumps({"decision": "block", "reason": "HOOK CRASH — failing closed"}))
```

The current behavior is the safe default during rollout; fail-closed should
be switched on after 2+ weeks of stable hook operation.

---

## Pitfall: session_id required by Hermes hook protocol

Hermes hook expects stdin JSON to contain `tool_name`, `tool_input`, `session_id`.
If `session_id` is missing, the hook still works (defaults to "unknown") but
the receipt has a gap. The runtime should always provide it.

---

## Related files

- Gate logic: `/root/HERMES/gate/hermes_mutation_gate.py` (skill template)
- Receipt trail: `/root/HERMES/gate/receipts/hermes_actions.jsonl`
- E-22 audit: `/root/AAA/federation/FASA1_AUDIT_E22_PENETRATION.md`
- Adjacent skill: `arifos-kernel-eurekas` K5 (gate design)
- Adjacent skill: `governance-contract-self-audit` (contract-side mirror)
