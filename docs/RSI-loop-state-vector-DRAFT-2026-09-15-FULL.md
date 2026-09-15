# RSI Loop — State Vector + Loop Diagram (FULL DRAFT, grounded)

> STATUS: DRAFT — pending F13 ratification. Informational only. No kernel mutation, no deploy.
> DATE: 2026-09-15 · AUTHOR: Hermes (333-AGI synthesis lane)
> BASIS: live probe of RSI ledger, VAULT999, crontab, systemd timers (2026-09-15 02:38 +08)
> SELECTION: A-FORGE execution traces = first binding target (design recommendation, NOT a ratification — ratification is F13's act).

---

## 0. Decision — A-FORGE first (confirmed for the draft)

A-FORGE is the only organ that mutates production state, so its loop is the one that
most needs stability constraints. GEOX aliasing produces wrong geology; A-FORGE aliasing
produces wrong policy. GEOX is COMPUTE_ONLY and second; Cell civic pulses have no stable
signal source yet and go last.

Crucial finding from the probe: the infrastructure for the signal IS already there
(forge_experience_trace exists; traces are metabolized every 15 min). The missing pieces
are exactly two: (1) the state-vector formalization, and (2) the sampling-rate question
for the improvement controller. Both are addressed below.

---

## 1. Signal inventory — what actually flows in (OBSERVED)

| Stream | Source / writer | Store (path) | Rate |
|---|---|---|---|
| Experience traces | forge_experience_trace → metabolize | /root/VAULT999/experience/ + p0_metabolize_traces.py | 15 min |
| Receipts | forge_receipt_draft / seal | arifflow_receipts.jsonl (10.9 MB), opencode_receipts.jsonl (33 MB), seal_receipts.jsonl | continuous |
| Scars | scar events | /root/.local/share/arifos/scars/ + scar_events.jsonl | event-driven |
| RSI ledger | rsi-cycle.py @ /seal | rsi-ledger.jsonl (961 entries) + VAULT999/rsi_ledger.jsonl (3.5 MB) | session boundary |
| Reality loop | reality-pulse.py | /root/.local/share/arifos/reality_loop/ + VAULT999/reality-loop/ | 15 min |
| Contradictions | contradiction ledger | contradiction_ledger.jsonl (39 KB) | event-driven |
| Cooldowns / cooling | cooling ledger | cooling_ledger.jsonl (39 KB) | event-driven |
| Fed events / sync | fed sentinel + sync | fed_events.jsonl (418 KB), fed_sync_log.jsonl (873 KB) | hourly |
| Telemetry (fast) | systemd timers | federation-state (30 s), triadic-snapshot (1 min), arifos-reality (1 min) | 30 s – 1 min |
| Capability fitness | fitness probe | capability_fitness_history.jsonl (129 KB) | daily |
| World model | metabolism | /root/.local/share/arifos/world-model/ + metabolize_state.json | 30 min |

Observation: the signal inventory is rich. The federation already observes at 30 s to
15 min across ten-plus streams. What it does NOT yet do is close the improvement loop on
those streams at a rate matched to the failure modes it governs (see §3).

---

## 2. State stores — persist / decay / forget

### PERSIST (immutable, non-erasable)
- VAULT999 sealed events (SEALED_EVENTS.jsonl), rsi_ledger.jsonl, arifflow_sealed.jsonl
- scars/ (Scar Law — persistent)
- SEAL receipts, chain tombstones

### DECAY (TTL-bounded, binary)
- cooling_ledger.jsonl — cooldowns decay to re-arm
- SRO / SCT — TTL 1 h, renew every 30 min (sct-renew.timer)
- forge_work GC — 7-day TTL, 30-day quarantine, 90-day archive
- state-snapshot purge — 3-day retention (cron 05:00)

### FORGOTTEN (binary purge)
- session context window (context rot), snapshots, caches

### MISSING — the aliasing-relevant decay is NOT built
- The Decay Watcher (Temporal Doctrine P1) — confidence(t) = c₀·e^(-λt) with half_life.
  Continuous half-life decay on claims. Status: 🔨 declared, not implemented.
  Consequence: forgetting is currently BINARY (TTL purge), not CONTINUOUS. A claim is
  either "present" or "gone," never "stale at 0.4." That binary switch is what lets an
  aliased (under-sampled) claim masquerade as fresh right up until purge.

### MISSING — the transition primitive (L2)
- /root/VAULT999/transitions/ is EMPTY. /root/VAULT999/chronus/ exists (dir, Sep 9) but
  holds no populated transition store.
- Confirms the doctrine's own diagnosis: State A → Action → State B → Delta → Why is the
  missing primitive. Receipts and scars exist; the DELTA between before/after states is
  not being recorded as a first-class signal. Without it, "recursive improvement" has no
  difference signal to improve on — only events.

---

## 3. Sample rates vs phenomenon bandwidth — the Nyquist gap

| Loop | Writer | Actual rate | Governs | Status |
|---|---|---|---|---|
| Fast (observe) | systemd timers | 30 s – 1 min | liveness/telemetry | fine |
| Medium (state) | p0_metabolize / metabolize_cron / reality-pulse / reexamine | 5 – 30 min | experience → state | fine |
| Slow (policy) | cron digests + RSI @ /seal | hourly–daily + session boundary | skills / ledger / carry-forward | fine for daily cycles |
| Meta (Imp) | RSI @ /seal (only) | session boundary, irregular (hours–days) | bottleneck / drift / recurrence | UNDER-SAMPLED |

The gap: the controller Imp fires ONCE per session, but the failure modes it is supposed
to correct (REPETITION — same approach 3+ times; TOOL_DRIFT; SCOPE_CREEP; recurrence)
manifest WITHIN a session, on minute-to-hour timescales.

This is a textbook aliasing risk. A within-session repetition is recorded as a single
event at session end; its true frequency is lost. The RSI skill itself flags this —
"RSI only at session end" is listed as an anti-pattern, and mid-session bottleneck
detection (stuck > 5 min) is currently OPTIONAL, not mandatory.

Nyquist implication: if a failure mode has bandwidth B (events per session), the Imp loop
must sample at ≥ 2B. Session-boundary sampling is at 1× the session rate — marginal for
once-per-session failures, below Nyquist for anything faster. The fix is not "more crons"
— it is making mid-session RSI triggers mandatory for the REPETITION class, and recording
the transition delta at the moment of detection, not at close.

---

## 4. Loop topology — which loop writes which layer

```
Fast loop    (act)      systemd timers → telemetry state.        Writes: OBSERVATION only.
Medium loop  (state)    p0_metabolize / metabolize_cron /         Writes: experience, receipts,
                        reality-pulse / reexamine                 metabolize_state, world-model.
Slow loop    (policy)   RSI @ /seal (rsi-cycle.py) + digests.     Writes: skills, ledger, carry_forward.
Meta loop    (Imp)      F13-gated ONLY.                           Writes: Imp, evaluator, constitution, floors.
                                                                  (No automated meta writer exists — correct.)
```

Rule (from control): inner loops fast, outer loops slow. The federation already gets this
right for observation (fast inner) vs policy (slow outer). What is missing is a MIDDLE
band — a within-session improvement trigger — between "observe every 30 s" and "improve
once per session." That missing band is where the aliasing lives.

Write separation is clean: no loop currently writes a layer above its own band. The danger
is not cross-layer writes today; it is the absence of the middle band.

---

## 5. 888_HOLD position in the feedback path

Three concrete gate sites (OBSERVED):

1. VERIFY → SEAL: apex-zen-run-loop.sh (5 min) holds SEAL on abort state
   (apex-zen-abort-state.json); seal-pending/ buffers; unsealed-counter.sh (30 min) alerts
   if unsealed work accumulates past threshold.
2. slow → meta: any write to Imp / evaluator / constitution / floors is F13-gated.
   There is no automated meta writer. This is the anti-windup / saturation device.
3. circuit-breakers/ dir — JITU-style breaker state for runaway loops.

Removing HOLD from any of these three = unbounded integrator (context rot / ledger
windup) → predicted divergence, not emergence.

---

## 6. Stability questions that need empirical answers

These are the questions the diagram raises but cannot answer from first principles.
Each needs a measurement, not a vote.

1. Bottleneck inter-arrival distribution. For each RSI bottleneck type (REPETITION,
   EVIDENCE_GAP, TOOL_DRIFT, SCOPE_CREEP, OVERCONFIDENCE, RECURRENCE), what is the
   inter-arrival time? This IS the bandwidth of the failure phenomenon. Without it the
   Imp sampling rate is a guess.

2. Is the ledger read, or written-only? A write-only ledger is an OPEN loop, not a
   feedback loop. The 961-entry rsi-ledger.jsonl — does session start actually load the
   last N entries (recurrence check), or does it only append? Measure: correlation between
   prior-session bottleneck and next-session fix.

3. Impulse-response decay of a fix/scar. How many sessions does one installed fix remain
   causally active? This determines whether h[n] has finite or infinite memory. If
   infinite (never forgets), context rot is the integrator-windup signature and needs a
   saturation bound.

4. Anti-windup on the ledger. institutional_ledger.jsonl (18 MB), opencode_receipts.jsonl
   (33 MB), ariflow_receipts.jsonl (10.9 MB) all grow unbounded. Where is the saturation
   limit on "lessons accumulated"? No bound = windup.

5. Causal eval. Do RSI traces ever include post-decision information (lookahead,
   contaminated benches)? Audit the trace schema for info ≤ t only.

6. Closed-loop pole location. From the 961-entry ledger: do the SAME bottlenecks recur
   (pole near unit circle → thrashtrend) or do fixes decay the error (pole inside →
   stable learning)? Recurrence rate is the direct readout.

7. Gain of Imp. Is each fix "one bottleneck, one reversible fix" (bounded gain) or does a
   single session rewrite multiple layers (high gain, oscillation risk)? Measure fixes
   per cycle vs RSI's "singular fix" rule.

The first measurement to run — cheapest and highest leverage — is #2 (is the ledger
read?) and #6 (recurrence rate), because together they answer whether the improvement
loop is even CLOSED, before anyone worries about its stability margin.

---

## Boundary

Draft only. No kernel mutation, no deploy, no purchase. Before any live RSI loop writes
persistent policy, evaluator, or constitution, F13 ratification is required. The selection
of A-FORGE as first binding target is a design recommendation, not a ratification.
