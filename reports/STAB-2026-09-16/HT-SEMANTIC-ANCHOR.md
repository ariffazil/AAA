# h(t) — PINNED SEMANTIC ANCHOR
> 2026-09-18 · read-only · resolves three drifted meanings of one instrument

## The exact contract (from `ImpulseResponseReport`, impulse-response.ts:86)

```typescript
interface ImpulseResponseReport {
  window_start: string;
  window_end: string;
  total_impulse_events: number;
  samples_with_influence: number;
  mean_half_life_sessions: number | null;
  median_half_life_sessions: number | null;
  by_event_type: Array<{
    event_type: ImpulseEventType;     // 888_HOLD | scar_seal | tool_failure | fix_deployment
    count: number;
    mean_half_life: number | null;
    still_active_count: number;
  }>;
  h_characterized: boolean;           // requires ≥5 samples
  computed_at: string;
}
```

## The anchor — one sentence

> **h(t) returns decay half-lives (mean, median, and per-event-class) for how long an
> institutional event stays causally active in subsequent routing, tool selection, and budget
> allocation. It is a measurement primitive over four institutional event classes. It is not
> ρ(J), not σ_max, not a timing buffer, not a clock separator.**

## The three drifted meanings, corrected

| # | Drift | Correction |
|---|---|---|
| 1 | h(t) ≈ ρ(J)/σ_max for §14 dynamic stability | ❌ Wrong. h(t) is decay-per-class. §14 stability is **UNMEASURED** — h(t) supplies raw data, not the matrix. |
| 2 | h(t) = "timing margin / safety buffer" | ❌ Not a contract term. It returns half-lives, not a buffer. Reading it as a buffer is added meaning. |
| 3 | h(t) alone yields §22 clock separation | ⚠ **Partly supported, with a real gap** — see below. |

## Meaning 3 — the tool already supports cross-class comparison

OpenClaw's correction was: *"untuk clock separation, perlu bandingkan h(t) untuk event class
berbeza, bukan guna h(t) tunggal."* **Correct — and the tool already does this natively.**
`by_event_type` returns a per-class `mean_half_life`. Cross-class comparison needs no extra work.

**But the classes available are institutional events only:**
```
888_HOLD · scar_seal · tool_failure · fix_deployment
```
There is **no** "cognition-compromise" class and no "authority-elevation" class. So §22's
`τ_cognition < τ_authority` ratio cannot be computed today — not because h(t) is misused, but
because **the input event classes do not exist**.

**Precise status:**
| Use | Status |
|---|---|
| Per-event-class decay measurement | ✅ **supported today** |
| Cross-class comparison (institutional) | ✅ **supported today** |
| §22 clock separation (cognition vs authority) | ❌ **requires new event types** — build proposal |
| §14 dynamic stability (ρ(J), σ_max) | ❌ **not this instrument** |

## Why this is the cleanest instance of the night

`h(t)` is a working tool that acquired **three meanings across coherent context** — no fallback,
no seat swap, no external prompt. Each re-framing was locally reasonable. This is the
**steady-state** variant of the defect class, distinct from the swap-induced regression.

## OpenClaw's two invariants — recorded verbatim

1. **Tool semantic anchor.** Every tool referenced in analysis carries one pinned semantic
   anchor (what it actually returns) that holds for the whole thread. The anchor may not be
   changed by convenience of argument. If a derivation needs the tool, **the derivation is
   justified, not the tool re-framed.**
2. **Re-framing cross-check.** Writing *"X can measure Y"* after previously writing *"X is Z"*
   requires an explicit statement: is Y **derived from** Z, or is Y a **reinterpretation** of Z?
   Reinterpretation carries drift risk.

**Both accepted.** This document is the anchor for h(t) — the first application of invariant 1.

## IC=0 taxonomy — fourth subclass

| # | Subclass | Trigger | Tonight's evidence |
|---|---|---|---|
| 1 | Epistemic | external correction | 666→888 flip-flop |
| 2 | System-level | self-contradiction | `substrate_state` DEGRADED↔HEALTHY |
| 3 | Operational | context miss / seat swap | #59219 regression |
| 4 | **Semantic (voluntary)** | **none — writer re-frames** | **h(t) × 3 meanings** |

Subclass 4 is the hardest: **no external event marks it.** Subclasses 1–3 all have a
detectable trigger. Subclass 4 is self-authored drift inside coherent context — it looks like
normal reasoning from the inside, which is precisely why invariant 1 (pinned anchor) is the
only defence.
