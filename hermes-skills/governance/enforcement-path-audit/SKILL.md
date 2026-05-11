---
name: enforcement-path-audit
description: "Verify governance features (floors, gates, contracts) are actually wired and enforcing vs. committed but not integrated. Uses 5-layer ground-truth protocol: file existence, import tracing, live runtime probe, config mismatch check, cross-repo transport audit."
triggers: ["wired but not enforcing", "contract not active", "architecture line broken", "F14 not working", "budget contract not enforcing", "enforcement path audit"]
tags: ["arifOS", "governance", "audit", "enforcement", "debug"]
category: governance
---

# arifOS Enforcement Path Audit

## When to Use

Verify whether a governance feature (floor, gate, contract, policy) is actually wired and live vs. committed but not integrated. Trigger when:
- A commit claims a feature is "wired" or "enforcing"
- A contract/policy file exists but enforcement is unclear
- Architecture lines ("AAA defines → A-FORGE enforces → arifOS judges") need ground-truth verification

## 5-Layer Ground Truth Protocol

### L1: File Existence
```bash
find /root -name "*.json" -path "*/budget/*" | head
find /root -name "*semantic_gate*" | head
```

### L2: Import Chain Tracing
```bash
grep -r "budget_contract\|classify_intent\|semantic_gate" \
  /root/arifOS/arifosmcp/ --include="*.py" | grep -v ".pyc\|.archive\|__pycache__\|test_"

grep -n "get_budget_contract\|classify_intent(" \
  /root/arifOS/arifosmcp/runtime/floor.py
```

### L3: Runtime Live Probe
```bash
curl -s http://localhost:8080/health
curl -s http://localhost:8080/tools/list
curl -s http://localhost:8080/governance/risk-classify \
  -X POST -H "Content-Type: application/json" -d '{"script":"print(1)"}'
```

### L4: Config vs. Contract Mismatch
```bash
cat ~/.hermes/config.yaml | grep max_turn
cat /root/AAA/contracts/budget/AAA-GOV-BUDGET-v1.json
```

### L5: Cross-Repo Transport
```bash
grep -n "fetch\|http" /root/A-FORGE/src/governance/GovernanceBridge.ts | head
grep -n "budget\|Budget" /root/A-FORGE/src/engine/AgentEngine.ts
```

## Defined vs. Wired

| State | Meaning |
|-------|---------|
| Defined | File exists, code written, committed |
| Imported | In import tree, not necessarily called |
| Called | Actual call sites in execution path |
| Wired | Live runtime probe confirms active |

**Key lesson:** import ≠ call. `get_budget_contract()` existed in isolation — never called in any tool handler despite being "defined and imported."

## Key Findings From This Audit

- `budget_contract.py`: defined in `100c4eb4`, imported by `floor.py`, but `get_budget_contract()` never called in any tool handler — **NOT ENFORCING**
- F14 `semantic_gate.py`: `classify_intent()` called in `floor.py`'s `check_floors()` at line 231 — **WIRED**
- Hermes `config.yaml`: `max_turns: 90` vs contract `max_turns: 8` — **CONFIG DRIFT**
- A-FORGE `GovernanceBridge.ts`: HTTP calls only for `risk-classify`, not budget

## DITEMPA BUKAN DIBERI

Ground truth, not derived claims. Curl it. Trace imports. Verify call sites.
