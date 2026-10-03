---
id: forge-musyawarah-gotong
name: FORGE-musyawarah-gotong
version: 1.0.0
description: >
  Runtime for musyawarah (independent 333 ARCHITECT + 555 AUDITOR) then
  gotong-royong (sequential execute hop). Authority star, evidence as
  position files. Not a chatboard. Grok: workflow musyawarah-gotong.
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F3, F4, F7, F9, F11, F13]
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
tags: [musyawarah, gotong-royong, deliberation, handoff, F3, F13]
---

# FORGE-musyawarah-gotong

Make musyawarah and gotong royong fire. Do not role-play both voices in one process.

## What is real

```
MUSYAWARAH  333-agi ARCHITECT ∥ 555-asi AUDITOR   (read-only, independent)
CONVERGE    parent synthesizes; 888-apex only on residual disagreement
GOTONG      sequential hop: previous output = next STATE_IN
```

A sibling may share what it saw. It may not tell you what to be.
(`inter-agent-protocol.md` §11)

## What is fake (do not cite as musyawarah)

`aaa_capability_loader._musyawawah_phase` is an in-process heuristic. Same function speaks ARCHITECT, AUDITOR, and SOVEREIGN, then stamps `SEALED_MUSYAWARAH_CONSENSUS`. That is not F3. Field `musyawarah_kind: in_process_heuristic`.

Hermes skill `forge-musyawawah-deliberation` is the Hermes adapter (7-phase, `delegate_task`). Use it on Hermes. Do not copy it onto Grok.

## When it MUST fire

| Class | Musyawarah | Gotong |
|---|---|---|
| T0/T1 reads, grep, local reversible edit | No. Auto-do. | No. |
| T2/T3, deploy, capital, SEAL, F13-adjacent dispute | Yes. Two independent voices before mutate. | After dual GO only. |
| Sembang / angan-angan | VOID. | VOID. |

## How it fires

**Grok:** workflow `musyawarah-gotong` at `/root/.grok/workflows/musyawarah-gotong.rhai`

```
args.dispute  = one question, two defensible positions   (required)
args.files    = paths to read                             (optional)
args.execute  = true only after you want the gotong hop   (default false)
```

**Hermes:** `forge-musyawawah-deliberation` (existing). Same physics: parent drafts first, sibling does not see parent draft, Lane A ≠ Lane B.

**Any harness without the workflow:** spawn 333-agi + 555-asi in parallel with `FORGE-subagent-spawn`, capability read-only, then parent converges. Do not let them write `guidance`.

## Artifacts

Position files / structured `output_schema`, not a chatboard.

```
forge_work/<id>/ARCHITECT_POSITION.md
forge_work/<id>/AUDITOR_POSITION.md
forge_work/<id>/SYNTHESIS.md     (agree / residual / surprises)
```

Workflow scratch: `SYNTHESIS.md` on the run.

## Rules

1. Voices do not see each other during musyawarah. Contamination = invalid run.
2. Parent never voices SOVEREIGN. 888 recommends; kernel `effective_verdict` / F13 seals.
3. Dual GO + `execute=false` → packet only. Gotong does not silently mutate.
4. Gotong hop is isolation worktree, reversible, `inclusive_delta` required, no unilateral extras.
5. Missing/failed voice → HOLD (fail closed). A silent auditor is not consent.
6. Loader `SEALED_MUSYAWARAH_CONSENSUS` is not a musyawarah receipt.

## Anti-patterns

- One model playing ARCHITECT + AUDITOR + SOVEREIGN
- Sibling chatboard as the deliberation surface
- `kind=guidance` from a specialist
- Claiming SEAL after Lane B / heuristic stamp
- Running musyawarah on T1 grep
---
DITEMPA BUKAN DIBERI
