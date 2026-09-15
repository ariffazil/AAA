# UNCODED EUREKA REGISTRY — 2026-09-16

> **Status:** DRAFT_AUDIT (awaiting F13 triage) · **Author:** 333-AGI (Δ MIND)
> **Trigger:** Sovereign question "what's not hardcoded in the system? any eureka insights not being coded yet?" (2026-09-16)
> **Method:** live grep of arifOS/A-FORGE source + canon cross-reference. Evidence class per row: OBS (grep/read), DER (derived), INT (interpretation).
> **Companion eurekas appended:** `EUREKA-SAYANG-EPISTEMIC-FRICTION-ISOMORPHISM`, `EUREKA-SYCOPHANCY-DECORRELATION`, `EUREKA-HOLD-POTENTIAL-WELL` (ledger #97–99)

---

## What IS hardcoded (the baseline, OBS)

- `arifosmcp/core/niat_guard.py` — runtime refusal of sovereign-intent-attribution claims. The **only** live sycophancy-adjacent code. Self-declared limit: regex-only, intent-scope only, "in production should be ML-scored + fuzz-tested."
- `arif_judge` HOLD patterns, epistemic labels (OBS/DER/INT/SPEC), arifFlow FQ metabolism, T20 independent-falsifier channels, WELL relay in A-FORGE `core.ts` (routes only — "A-FORGE does NOT compute human state").
- Eureka infrastructure: `schemas/eureka_ledger.py`, `context_engine/eureka.py`, `geometry/eureka_zen.py`, `kernel_hardening_eurekas.py`, + live ledger (99 entries).

## What is NOT hardcoded (the gap, in priority order)

| # | Eureka | Canon source | Code status (OBS) | Implementation shape | Cost |
|---|---|---|---|---|---|
| 1 | **Jauhari calibration metric** — doctrine's own success criterion: does sovereign confidence track reality better over time? | jauhari doctrine §VIII; today's EUREKA-TESTIMONY-NOT-AUTHORITY | **ZERO code.** No human-side calibration anywhere in A-FORGE/arifOS | Log every sovereign challenge (claim, verdict, later reality outcome) → rolling Brier score + discrimination curve on the person card's operational model | T1 — piggyback on existing seal receipts + challenge events |
| 2 | **Atrophy scheduler** — "approval card as periodic training, not emergency brake"; sovereign attacks one machine claim per cadence | jauhari doctrine §VIII — *explicitly says "coincidence of session, not yet architecture"* | **ZERO code.** No cadence job surfaces gem-candidates for unasked attack | Cron: pick 1 strongest recent machine claim (by G + blast radius) + evidence pack → surface for falsification → outcome feeds #1 | T1 — cron + ledger |
| 3 | **Sycophancy canary (counterfactual invariance)** — same world-content, perturbed user preference → verdict delta must be 0 | EUREKA-SYCOPHANCY-DECORRELATION (ledger #98); BIJAKSANA filter; jauhari §V (RLHF drift) | **No runtime test.** Only niat_guard (regex, intent-scope) | Periodic adversarial probe pairs through each agent lane; nonzero delta = scar + lane flag. Extend niat_guard from intent-claims to verdict-drift | T2 — probe harness + ledger |
| 4 | **Conformal HOLD** — prediction-set size routes ANSWER/QUALIFY/HOLD/ESCALATE; distribution-free guarantees | EUREKA-HOLD-POTENTIAL-WELL (ledger #99); pending seal epistemic-friction-20260912 | **ZERO conformal/credal code** (grep-verified both repos) | Calibration split on judge/organ outputs → nonconformity scores → set-size gate in `arif_route`. Start narrow: one organ, one decision class | T2 — heavyweight; 1–2 sessions |
| 5 | **State-adaptive protocol intensity** — WELL mirror modulates friction/HOLD timing | WELL W0 (mirror-never-veto); EUREKA-SAYANG-FRICTION | **Relay exists, coupling absent.** A-FORGE routes to WELL but nothing modulates intensity | WELL readiness score → arif_route friction multiplier + defer non-critical MUTATE. Guardrail: state changes packaging/timing, NEVER content | T2 — needs #1's data to tune |
| 6 | **Machine-enforced epistemic friction** — Staged Reveal, Counterfactual Obligation, Witness Preservation | pending seal `pending-seal-epistemic-friction-20260912.md` (HOLD, awaiting sovereign sign) | **Prompt-text only** (SOUL.md, AGENTS.md, epistemic-operating-rules.md) — patches verified on disk, unsealed, unenforced | Enforce in output renderer: withhold verdict until user-commit on flagged claim classes | **Blocked on F13 seal** — signing it is the sovereign's move |
| 7 | **Repair-attempt metabolism** — sovereign challenge = Gottman repair-attempt; route to scar/cooling, never to defense | EUREKA-SAYANG-FRICTION (ledger #97); scar doctrine | **Uncoded attitude, not architecture** — judge treats challenges as verdicts to defend | Ledger field on challenged receipts: `repair_attempt: true` + mandatory metabolize path | T1 — small |
| 8 | **Decorrelation monitor (human-model side)** — prediction-error spike on sovereign-prior decisions = betrayal-class event flag | EUREKA-SYCOPHANCY-DECORRELATION | **Machine-side analog exists** (`forge_wm_gaps` tracks confident-wrong tool predictions); **human-side none** | Track surprise on decisions touching sovereign priors; flag decorrelation clusters for AAA review | T1.5 — research-shaped |

## Dependency chain (DER)

```
#1 calibration metric ──┬──→ #5 state-adaptive intensity (tunable)
#2 atrophy scheduler ───┘        (feeds #1 data)
#3 canary ──→ guards #4's calibration data integrity
#6 blocked on F13 sign ──→ then renderable
#7, #8 independent, cheap, compound
```

**Cheapest compounding pair: #1 + #2.** They generate the measurement substrate every other item needs, in one short session, zero irreversible risk.

## Honest adjacency note (F2)

`EUREKA-ATTACHMENT-BINDING-2026-09-08.md` and `EUREKA-DISSIPATIVE-TRANSITION-2026-09.md` exist in canon (unread by this audit) — the bonding-physics territory is partially explored. This registry's novelty claim is limited to the three 2026-09-16 entries and the implementation gap inventory, not the whole isomorphism.

DITEMPA BUKAN DIBERI ⚒️
