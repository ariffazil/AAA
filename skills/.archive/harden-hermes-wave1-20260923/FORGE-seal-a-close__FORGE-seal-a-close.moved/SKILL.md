---
name: FORGE-seal-a-close
description: >
  Close remaining Seal-A gates after P0 proof/identity/SCT/T3a work.
  Use when: Seal-A, stage 000, SE stage engine, SOT v2, BOOT, T3a binding,
  free_nonce, constitutional_grade, remaining seal tasks.
version: 2026.07.17b
floors: [F1, F2, F3, F7, F11, F13]
---

# FORGE — Seal-A Close Path

> **Do not claim Seal-A closed until T3a matrix 13/13 + R1–R4 live-green.**  
> **Never manual-bump stage to leave 000.**  
> **SE advance blocked until T3a CLOSED (sovereign ruling 2026-07-17).**

## Already CLOSED (do not re-do)

| Item | Evidence |
|------|----------|
| T6 SKIPPED≠PASS | spine honesty |
| Identity dual-kill + vault_replay | standing sole |
| R1 SE stage engine | proof-only advance |
| R2 SOT v2 operational | hash active + supersession |
| R3 BOOT >OBSERVE refuse | live demotion |
| SCT PR1 + PR2 | AAA sealed CI GREEN |
| A-FORGE SCT AMBIGUOUS + prod lockout | health bypass_profile:none |
| T3a POSITIVE Ed25519→SOVEREIGN | matrix 4/4 |

Receipts: `/root/A-FORGE/forge_work/2026-07-17/`.

## Remaining order (strict)

### Block 0 — T3a — **CLOSED 2026-07-17**

Skill: `FORGE-t3a-binding-matrix` (regression only)

- Matrix **13/13** · receipt `T3A-CLOSE-RECEIPT.md` · commit `196cb5ef2`

### Block 1 — R4 canary — **GREEN 2026-07-17**

```bash
cd /root/arifOS && PYTHONPATH=/opt/arifos/app python3 -c \
  "from arifosmcp.transport.conformance_spine import run_spine; import json; r=run_spine(fast=False); print(r['score'], r['all_green'], r['skipped'], r['substrate_gate'])"
```

Last: **9/9** · all_green · skipped=0 · constitutional_grade true · `R4-SPINE-FULL-T3A-CLOSE.json`  
Stabilize :8088 first if Recv-Q backlog / timeouts.

### Block 2 — SE stage advance — **NEXT**

Use `se_stage_engine.try_advance(proof_bundle)` — never hand-edit.

### Block 3 — SCT PR4–7 (parked until SE or parallel if SE blocked)

trace_id × 5 organs → 65 matrix → VAULT rollup. Skill: `FORGE-sct-federation-ingress`.

## Verification contract

1. Code committed + deployed  
2. Live probe in forge_work  
3. No dual authority fields  
4. Fast-mode never GREEN  
5. Matrix 13/13 for T3a — **met**

## Epistemic

```yaml
seal_a: OPEN until SE proof path exercised
t3a: CLOSED   # 13/13 2026-07-17
r4: GREEN     # 9/9 full spine
se_stage: "000" ADMISSIBLE via try_advance only
K_apex_runtime: measure after verified SOVEREIGN session
```
