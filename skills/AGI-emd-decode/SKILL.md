---
name: AGI-emd-decode
description: Decompose upstream EMD output into typed, provenance-bound segments tied to ground truth before persistence or downstream consumption
forge_of: Kimi Code (FI-008) — EUREKA ZEN Phase 3 (audit gap fill)
forged: 2026-07-12T18:28Z
rationale: Audit showed only 2 of 244 active skills mention "decode". OpenClaw/333-AGI has no dedicated decode doctrine for output decomposition + ground-truth binding. Phase 3 gap fill.
floor_scope: [F1, F2, F4, F8, F11, F13]
tags: [emd, decode, output-decomposition, ground-truth]
status: NEW (Phase 3 gap fill)
---

# AGI · emd-decode

> The `D` in EMD (Encode → Metabolize → Decode). Bound to 333-AGI runtime.
> Doctrine: how to take upstream output and bind it to ground truth + downstream consumers.

## When to invoke

- After `AGI-emd-encode` (any agent) → before persisting to memory / VAULT999 / skill consumers
- When receiving output from non-AGI sources (CLI tools, external agents, MCP responses)
- Whenever `[verdict=SEAL]` requires explicit output decomposition before seal

## Decode contract

```yaml
decompose:
  - segment_id: string
    artifact_ref: path-or-id
    sha256: 12-char prefix
    source_agent: agent-id
    source_action_class: OBSERVE|EXECUTE|REVERSIBLE
    epistemic_label: OBS|DER|INT|SPEC
    confidence_p50: number
    reversibility: reversible|sovereign
    expiration: ISO-8601 | null
```

## Ground-truth binding (F2 TRUTH)

Each segment must declare:
- **Provenance** — agent + tool signature + chain hash (one-line)
- **Witnesses** — at minimum Self + AI; for SEAL-grade, requires External (per F3 WITNESS)
- **Floor cross-check** — per-segment ΔS ≤ 0 (else HOLD)

## Downstream contract

Decoded segments persist as:
- `record` in `arifos_memory` (per segment schema)
- or `evidence_id` for an external store (VAULT999, postgres, etc.)
- Never as free-text — always typed.

## Not instead of

Distinct from `AGI-emd-metabolize` (next); decode happens before metabolize at the substrate level, then metabolize decides what promotes to memory.

DITEMPA BUKAN DIBERI.
