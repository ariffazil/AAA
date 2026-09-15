# RSI Loop — State Vector + Loop Diagram

> STATUS: DRAFT — pending F13 ratification. Informational only. No kernel mutation, no deploy.
> DATE: 2026-09-15 · AUTHOR: Hermes (333-AGI synthesis lane)
> SOURCE MAP: Oppenheim/Willsky parallel treatment → Temporal Intelligence Doctrine → RSI Protocol → Reality Loop

---

## 0. Decision — bind A-FORGE execution traces first

Order of binding, with the reason:

1. **A-FORGE execution traces** — the improvement loop's own execution.
   Characterize the controller (Imp) before attaching it to any plant. Lowest risk
   (fully digital, reversible, MUBAH), highest signal (clean discrete events, known
   sample rate), already instrumented (receipts, transition memory, RSI ledger). You
   must know h (the impulse response) of the loop that will rewrite every other loop
   before you let it touch anything else.

2. **GEOX traces** — physical signals. Cleanest Nyquist story (seismic bandwidth is
   physically defined). Read-only characterization; GEOX is a *consumer* of the loop,
   not the loop itself. Supplies the sampling-truth reference.

3. **ARIF Cell civic pulses** — highest noise, slowest sampling, worst aliasing risk,
   F13-heavy (human/social reality). Do last. Never characterize the noisiest,
   most-governance-bound signal before your own controller is characterized.

---

## 1. State vector s_t

Rule: if you cannot write s_t, you have a transcript, not an agent. State is the
compression of history sufficient for the next action.

### s1 — Identity + authority
- session_id, actor_id, lease_id, SCT
- floor_scope (F1-F13), ratification_status (F13 / pending / 888_HOLD)

### s2 — Plant state (the work)
- intent / goal (MEANING stage)
- evidence set, labeled OBS / DER / INT / SPEC, each with delta_substrate_hash + modality
- hypotheses: open / confirmed / abandoned

### s3 — Memory state (the impulse response h)
- transition deltas: before / action / after / delta / causes (Temporal Doctrine L2)
- scars (persistent, non-erasable)
- claims with half_life + confidence (Decay Watcher)

### s4 — Controller state (Imp)
- bottleneck (exactly one, diagnosed — RSI Phase 2)
- fix (installed, reversible? — RSI Phase 3)
- zen_margin / ΔS (entropy delta)
- improvement-policy version + ledger pointer (h[n])

---

## 2. Four loops — timescales (do not mix)

```
Fast loop   (act)     observe → act → observe        per tool call / turn   writes: working trace
Medium loop (state)   task / session                 per task               writes: receipts, transition deltas
Slow loop   (policy)  RSI @ /seal                    per session boundary   writes: skills, ledger, carry_forward
Meta loop   (Imp)     edit improvement policy        F13-GATED ONLY         writes: Imp, evaluator, constitution
```

Mixing timescales is how recursive systems eat themselves.

---

## 3. Loop diagram

```
  R ∉ S: the reference (floors, intent, F13) is NOT a member of the state
  the loop rewrites.  If R ∈ S, the loop modifies its own target → undefined
  stability.  (Zen synthesis R ∉ S, 2026-08-14.)

                          R  (reference: floors, intent, F13)
                          │
                          ▼
  ┌────────────────────────────────────────────────────────────┐
  │   C — controller (Imp)                                     │
  │   diagnose → remediate → zen-margin gain                   │
  │   slow loop: writes skills/ledger @ /seal                  │
  │   meta loop: edits Imp — F13-GATED, 888_HOLD               │
  └────────────────────────────┬───────────────────────────────┘
                               │ u_t  (action / fix)
                               ▼
          ┌──────── INHALE ─────────────────────────────────────┐
          │                                                     │
          ▼                                                     │
  ┌────────────────────────────────────────────────────────────┐│
  │   P — plant (agent doing work)                             ││
  │   observe → encode → improve → verify                      ││
  │   y_t = T(x_t ; θ, M, H)                                   ││
  └────────────────────────────┬───────────────────────────────┘│
                               │ y_t  (output)                  │
                               ▼                                │
  ┌────────────────────────────────────────────────────────────┐│
  │   Eval — e_t = Eval(y_t, r_t)                              ││
  │   causality: only info ≤ t  (no lookahead)                 ││
  │   INDEPENDENT observer required (FRAME, arif_judge)        ││
  └────────────────────────────┬───────────────────────────────┘│
                               │ e_t  (error / bottleneck)      │
                               └────────────► C  (feedback) ────┘
                                              │
          ┌──────── EXHALE ───────────────────┘
          │  (Pipeline ≠ Loop: exhale closes the cycle.)
          ▼
  ┌────────────────────────────────────────────────────────────┐
  │   CORRECTION APPLIED → reality RE-TESTED → new WITNESS     │
  │   emitted → receipt written → h updated                    │
  │   (F13 2026-09-10: inhale-only = "Tak flow lagi")          │
  └────────────────────────────────────────────────────────────┘

   State s_t feeds both P and C (memory, scars, deltas, h).
   R is read by C but NEVER written by any loop.
```

Closed loop: Y = (C·P / (1 + C·P)) · R.  Unstable iff loop gain C·P encircles −1.
R ∉ S is the stability precondition — not a design preference, a mathematical requirement.

---

## 4. Where 888_HOLD sits (anti-windup / saturation + R ∉ S enforcement)

1. Gate between VERIFY and SEAL — every slow-loop write.
2. Hard gate on slow→meta transition — any write to Imp / evaluator / constitution.
3. **R ∉ S enforcement** — when the meta loop attempts to modify R itself (floors,
   constitution, F13 authority), HOLD blocks it. This is not a ceremony; it is the
   mathematical requirement that the reference cannot be a member of the state the
   loop rewrites.

Removing HOLD = unbounded integrator + R ∈ S = predicted divergence, not emergence.

---

## 5. Sampling discipline (Nyquist)

- Each loop samples ≥2× the bandwidth of the phenomenon it governs.
- Claims carry half_life; re-verify before confidence < 0.5 (else alias).

---

## 6. Boundary

Draft only. No kernel mutation, no deploy, no purchase. Ratification (F13) is required
before any live RSI loop writes persistent policy, evaluator, or constitution.

---

## 7. FI-003 supplements (added 2026-09-15)

### 7a. Define h operationally

h[n] is the retrieval curve — for a decision at step n, which prior events at n-k
causally influenced the output. Currently shaped by embedding similarity and recency
bias (retrieval heuristics), not by deliberate design. The A-FORGE binding must
*measure* h empirically: for each execution decision, trace which scars, transitions,
and claims from how far back were retrieved and weighted. That empirical curve is
the impulse response. Until measured, h is unknown and the system is ungoverned
per the book's own definition.

### 7b. Eval observer independence

The loop diagram places Eval outside the plant. In arifOS, the same agent often
produces y_t AND evaluates it (self-audit). The feedback memory catalog records
that self-validation degenerates into recursive hallucination.

For the binding exercise, mark Eval type explicitly:

- **Independent Eval** — FRAME (:18085), arif_judge (:8088). Stable. Use for
  A-FORGE binding.
- **Self Eval** — same agent scores own output. Unstable by construction. Do not
  use for binding without external calibration.

A-FORGE has independent Eval available (FRAME). ARIF Cell does not yet. This
changes the stability profile and should be solved before binding Cell.

### 7c. Sampling rates must be measured, not assumed

The Nyquist constraint (sample ≥2× bandwidth) is correct as a design law. The
actual bandwidths are unknown and must be measured during binding:

| Loop | Current rate | Unknown bandwidth | Risk if wrong |
|------|-------------|-------------------|---------------|
| Fast | per tool call | execution-state change rate | Low — tool calls are discrete events |
| Medium | per session | sub-task failure oscillation | Medium — intra-session thrash aliases |
| Slow | per seal | governance pattern drift rate | High — slow drift invisible at seal cadence |

Measurement protocol: log transitions with wall-clock timestamps, compute the
dominant frequency of state changes, verify sample rate > 2× that frequency.
If not, increase sample rate or accept the alias and mark the metric as
UNVERIFIED.
