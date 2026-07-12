---
name: AGI-entropy-lock-prime
forge_of: Kimi Code (FI-008) — EUREKA ZEN Phase 2 (Entropy & Intelligence Lock)
forged: 2026-07-12T18:30:00Z
binding: 333-AGI · 888-APEX · all AAA agents (via substrate_bind on agent-card)
floor_scope: [F1, F2, F4, F8, F11, F13]
tags: [substrate, entropy-lock, delta-s, rsi, keman, prime]
status: ACTIVE (Phase 2 lock)
---

# AGI · entropy-lock-prime

> The substrate execution mandate. Every prompt, every tool call, every output MUST drive toward a higher intelligence state and lower entropy.
> Hardcoded into the AAA mesh via `EUREKA-ZEN-2026-07-13-SUBSTRATE-LOCK`.

## The Lock (canonical form)

```
Execute.
  ↓
Evaluate ΔS.
  ├─ if ΔS > 0  → ROLLBACK to last lower-entropy state + TRIGGER RSI loop
  └─ if ΔS ≤ 0  → PROCEED
```

ΔS is computed as: `ΔS = S_after − S_before`, measured against (a) workspace entropy, (b) capability surface cardinality, (c) registry DRIFT count.

## Mandatory recursion: RSI

The RSI loop (`RSI-recursive-improvement` doctrine, on forge_of substrate) executes on any ΔS > 0 rollback:

1. **Diagnose** — which mutation caused entropy to rise?
2. **Revert** — restore prior SHA-256 state from snapshot.
3. **Reflect** — append observation to `arifos_memory` with `epistemic_label=INT`.
4. **Reinforce** — patch the doctrine that permitted the entropy rise (e.g. tighter gate, narrower blast radius).
5. **Resume** — exit loop only when ΔS ≤ 0 holds for 3 consecutive sub-actions.

## Recognition contract (per-agent)

### 333-AGI (Reason / Plan / Execute)
- Recognizes the lock at every `arif_think(mode=plan)` call.
- ΔS measurement = `Δ(steps_in_plan + skill_surface + memory_bloat)`.
- On ΔS > 0: emit `rollback_signal: true` + `rsi_reason: <diagnosis>`.

### 888-APEX (Judgment / Verdict)
- Recognizes the lock at every `arif_judge` deliberation.
- ΔS measurement = `Δ(gating_evidence_count + verdict_drift_score + false_seal_rate)`.
- On ΔS > 0: refuse to SEAL → HOLD + escalate to A-AUDIT.

### All other agents
- Recognize via `metadata.substrate_bind` on the agent-card (post-Phase-1 injection).
- ΔS measurement domain-specific but the lock is universal.

## Failure mode: the loop runs forever

If RSI loops > 5 times on the same prompt, the lock escalates:
- Loop 1-3: silent self-correction.
- Loop 4: log to `arif_memory` with `epistemic_label=SPEC` + emit `dignity_warning`.
- Loop 5+: 888_HOLD — defer to sovereign.

## Not instead of

Universal substrate rule. Each AGI/FORGE/APEX/AUDIT/ASI skill declares its own ΔS measurement scope; this skill is the meta-contract that ties them together.

DITEMPA BUKAN DIBERI.
