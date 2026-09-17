# PATCH PROPOSAL — belief-like state: issuer + revision_authority are mandatory fields

> **Status:** DRAFT_AWAITING_F13 · 2026-09-16 · **Trace:** TRACE-333-20260916-BSS01
> **Proposer:** 333-AGI (build hop for Hermes' proposal, ratified in chat 2026-09-16)
> **Targets:** `/root/AAA/instructions/triad-perspective-consequence-persistence.md` §3.4 (DRAFT_AWAITING_F13) — schema line; optional companion note for `memory-promotion-gate.md` (F13_RATIFIED_CHAT).
> **Not applied.** Proposal only; application happens at F13 ratification of the triad draft (or as a standalone edit if F13 prefers).

**Object contract:** `{ state: PRODUCED, prev_state: PROPOSED_IN_CHAT, expected_next: F13_READ → SEAL|DISCARD, owner: F13, evidence_required: post-apply grep (§5) }`

## 1. The gap (OBS)

External audit's schema: `belief-like state = proposition + provenance + confidence + scope + time + revision_conditions`. Hermes' finding, accepted: **no issuer field**. A schema that says *what* may be revised but not *who may revise* is authority-blind — and the executor may never self-issue revision authority (authority-envelope: the 10-field tuple carries `Issuer`; no self-authorization). The auditor promoted a schema to authority while rejecting narrative promotion to canon — same defect, opposite direction.

Current triad draft line 109 still carries the authority-blind schema:

```
belief-like state = proposition + provenance + confidence + scope + time + revision_conditions
```

## 2. Proposed schema (replacement for triad §3.4 code block)

```
belief-like state =
  proposition          — what is held
+ provenance           — where it came from (Class O/S/C/P tags)
+ confidence           — bounded, never authority
+ scope                — where the claim holds
+ time                 — observed_at, valid window
+ revision_conditions  — what evidence would overturn it
+ issuer               — who may assert/author it (MANDATORY)
+ revision_authority   — who may revise/retract it (MANDATORY, never executor-alone)
```

**Binding law:** `revision without authority = contamination vector` — the same class as Class F → Class O promotion. RETRACTED/SUPERSEDED transitions (state-transition-discipline) are only valid when performed by the recorded `revision_authority`. A schema without these two fields is decoration wearing a formal suit.

## 3. Cross-links

- `authority-envelope.md` (F13_RATIFIED_CHAT): Issuer field, no self-authorization, TOCTOU binding.
- `memory-promotion-gate.md` (F13_RATIFIED_CHAT): the 4-gate write path gains an explicit *who* at the gate — issuer check complements, does not amend, its gates.
- `state-transition-discipline` claim states: `{ claim_id, value, source, state, observed_at, supersedes }` — `source` names provenance; `issuer` names authority. Distinct questions, both required.

## 4. OPTIONAL ADDENDUM (flagged, not part of Hermes' binary ask)

Triad §3.5 already adopts "witness is an actuator." The half-loop Hermes noted as missing — the *consequence written down*:

```
probe_1 → subject changes → probe_2 data is second-order (probe-conditioned)
```

Rule: second-pass observations taken after any interaction must be tagged as such (e.g. `OBS_SECONDARY`) and never pooled with first-pass data as equivalent evidence. One tag, closes the reflexive gap: *data kedua bukan data pertama*.

## 5. Post-apply verification (for the sealing session)

```bash
grep -c "revision_authority" /root/AAA/instructions/triad-perspective-consequence-persistence.md  # expect ≥ 1
grep -c "issuer" /root/AAA/instructions/triad-perspective-consequence-persistence.md             # expect ≥ 1
```

DITEMPA BUKAN DIBERI ⚒️
