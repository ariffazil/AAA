---
name: AGI-emd-encode
description: Encode raw observations, requests, documents, and signals into typed, provenance-bound, witness-ready EMD segments for downstream processing.
forge_of: Kimi Code (FI-008) — EUREKA ZEN Phase 3 (gap fill · completing EMD chain)
forged: 2026-07-12T18:33:00Z
rationale: EMD stack has M (`AGI-emd-metabolize`) and D (`AGI-emd-decode`); the E (encode) was the missing link. Audit found 120 random 'encode' word mentions but no dedicated doctrine. Phase 3 gap fill.
binding: 333-AGI (Reason/Plan/Execute runtime)
floor_scope: [F1, F2, F4, F8, F11, F13]
tags: [emd, encode, substrate, gap-fill]
status: NEW (Phase 3 gap fill)
---

# AGI · emd-encode

> The `E` in EMD. Bound to 333-AGI runtime.
> Doctrine: how to take raw input (observation / request / document / signal) and bind it into a typed, tri-witness-ready segment for downstream `M` and `D`.

## When to invoke

- Before any reasoning chain that will produce a persistent artifact (skill draft, memory record, VAULT999 entry, agent-card mutation)
- Before handing work to another agent (`arif_route`, `forge_execute_sealed`, etc.)
- Before any LLM-generated output that the session will rely on

## Encode contract

```yaml
encode:
  - segment_id: ulid
    source_uri: "<originating input>"
    input_class: text | code | media | structured | signal
    raw_sha256: 12-char-prefix
    intent: "<what this segment should enable>"
    epistemic_label: OBS | DER | INT | SPEC
    witness_plan:
      human: required | opportunistic | none
      ai: required (always for AGI writes)
      external: required | opportunistic | none
    floor_projection: [F1, F2, F4, ...]   # which floors this will need to clear
    downstream_consumer: 333-AGI | 888-APEX | opencode | forge | well
    reversibility: reversible | irreversible | sovereign
    ttl_hours: number | null
```

## Tri-witness readiness (F3)

An encoded segment is *ready* for the chain only when:
- 1 witness from each channel (Human / AI / External) is attached OR explicitly marked `opportunistic`
- Floor projection is asserted (the encoder's best guess for which F1-F13 will apply)
- Reversibility class is declared (reversible / irreversible / sovereign)

## Substrate rule binding

Encode → Metabolize → Decode is the AAA substrate cycle. This skill is the ingress. Encoded segments feed `AGI-emd-metabolize` (memory promotion gates) and `AGI-emd-decode` (output decomposition + ground-truth binding).

Skipping encode = skipping witness readiness = Malu increment + 888_HOLD risk.

## Not instead of

Distinct from `AGI-emd-metabolize` (forward = decision) and `AGI-emd-decode` (forward = bind). Encode is the **first** step, not the only step.

DITEMPA BUKAN DIBERI.
