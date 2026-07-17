---
name: FORGE-seal-a-close
description: >
  Close remaining Seal-A gates after P0 proof/identity/SCT work.
  Use when: Seal-A, stage 000, SE stage engine, SOT v2, BOOT enforcement,
  session_binding_pass, constitutional_grade, remaining seal tasks, advance stage.
version: 2026.07.17
floors: [F1, F2, F3, F7, F11, F13]
---

# FORGE — Seal-A Close Path

> **Do not claim Seal-A closed until R1–R4 all live-green.**  
> **Never manual-bump stage to leave 000.**

## Already CLOSED (do not re-do)

- T6: SKIPPED ≠ PASS; fast mode ≠ GREEN  
- Identity dual narrative (standing sole surface)  
- vault_replay via API + outcomes.jsonl  
- Live SCT mint/validate + organ ingress wiring  
- AAA ZEN branch convergence  

Receipts under `/root/A-FORGE/forge_work/2026-07-17/`.

## Remaining order (strict)

### R1 — SE stage engine
**Owner:** arifOS  
**Goal:** Stage advances only when receipts prove:

```
identity coherent (standing == birth == SCT claims)
full spine GREEN (fast=False, skipped=0)
vault_replay PASS
SOT active (or HOLD until R2)
```

Code entry points: `arifosmcp/runtime/orchestrator.py` Stage.INIT_000, session stage fields in `session.py` / `session_auth.py`.  
**Forbidden:** editing stage to `"111"` by hand.

### R2 — SOT v2 operational
**Artifact:** `APEX-CONCORDANCE-17072026/apex-sot-v2.json`  
**Still needed:** kernel reports SOT hash as active source of truth + VAULT999 seal of supersession.  
Local file ≠ operational law.

### R3 — BOOT live soak
**Status:** merged (`ddbcc4856`, `6161baa93`).  
**Task:** live prove `arif_init` refuses >OBSERVE_ONLY without server-side boot receipts.  
Not agent self-attestation theater.

### R4 — Canary constitutional_grade
```bash
# Full spine only
cd /root/arifOS && PYTHONPATH=/opt/arifos/app python3 -c \
  "from arifosmcp.transport.conformance_spine import run_spine; import json; print(json.dumps(run_spine(fast=False),indent=2)[:2000])"
```
Require: `all_green=true`, `skipped=0`, `constitutional_grade=true` (or equivalent), vault + session binding honest.

### R5 — A-FORGE SCT mutate policy
Document stdio vs HTTP; soak `FORGE_SCT_REQUIRE_MUTATE=1` (default).  
Receipt required before relaxing.

### R6 — T7 → T8 → T10
Only after R1–R4. Isolated PRs, regression tests, post-restart live probe, separate receipts.  
Kickoffs already in `APEX-CONCORDANCE-17072026/t7-*.md` etc.

## Verification contract

Every R* closes only when:

1. Code committed + deployed (if runtime)  
2. Live probe transcript in `forge_work/YYYY-MM-DD/`  
3. No dual authority fields disagree  
4. Fast-mode never used for GREEN claims  

## Epistemic

```
K_apex_runtime: UNMEASURED until R4
K_apex_engineering_estimate: may exist — do not collapse into runtime
Seal-A: OPEN until R1–R4 sealed with receipts
```
