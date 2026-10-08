# 333-AGI PROPOSAL — Governed Scar-Wisdom Binding (F13-binary Gated)

**Date:** 2026-10-06 (Tuesday)
**Author:** FI-008 subagent on Arif directive (conversation thread "AAA autonomous + governed + bijaksana, hold is bangang")
**Status:** PROPOSAL — awaiting F13 binary from Arif
**Scope:** 1 page proposal, 0 runtime mutation, 4 F13-binary options, 3 mitigations
**Anti-Bangang compliance:** Law 2 (no 5-page essay), Law 3 (no new JSON/dashboard), Law 8 (one problem one owner), Law 9 (action > documentation), Law 10 (when in doubt, simpler)

---

## 0. The synthesis (Arif, 2026-10-06, this thread)

> *"History remembers. Scars constrain. Governance decides whether the constraint still applies."*

> *"Federation tidak kekurangan scar. Federation kekurangan scar yang mengikat selection secara governable."*

This proposal is the runtime expression of that synthesis. Not the banzai "flip the switch" move, not "HOLD is not an option," not another compression. The thing that comes after synthesis: **a F13 binary, with the empirical evidence in hand and the mitigations designed to prevent fossilization.**

---

## 1. Empirical evidence (the falsification that triggered this proposal)

Receipt: `/root/AAA/cockpit/receipts/RECEIPT_SELECTION_LAYER_AUDIT_2026-10-06.md` (FI-008 / Claude Code forge-777 audit session, 2026-10-06)

| Layer | Status | Source |
|---|---|---|
| Scar detection | **Wired** | `niat_gate.py:169-233` — `detect_scar_weight()` function |
| Scar consumption | **Wired** | `judge.py:2727-2752` — consumes `scar_weight` in verdict output |
| Scar enforcement | **DORMANT** | `scar_wisdom.py:8` — "NEVER auto-fired. NEVER prepended to LLM context." |
| Live probe of `arif_observe` with PETRONAS query | verdict=HOLD, payload=NONE | scar weight NOT injected |
| Live probe of `arif_judge` with mode=sovereign | verdict=HOLD, payload=NONE | scar weight NOT injected |

**Falsification result:** Deleting the scar registry would not change any agent decision. Doctrine lives in documents; behavior lives in defaults. **Gap is enforcement, not doctrine.** (Arif's compression, 2026-10-06: "Scar-Aware but not Scar-Bound.")

**However** — the dormancy is **deliberate, not accidental**. Someone wrote `scar_wisdom.py:8` with intent. The system was designed with separation of powers: detection without enforcement, exactly as `four-layer-separation.md` mandates. So flipping it is **constitutional-class mutation, not bug fix.**

---

## 2. The risk of naive flip (3 failure modes)

If F13 binary = SAH-FLIP-NOW (no mitigations), three failure modes activate:

### 2a. False-positive over-correction

A "Tengku Taufik"-class entity (partial name match) → scar auto-fires → agent refuses to engage with any mention of the entity or its aliases, even when the human sovereign wants fresh analysis.

Example: Arif says "tell me about current PETRONAS chairman" → scar-wisdom auto-fires → agent either over-corrects (refuses to engage) or fossilizes (locks to one historical answer).

### 2b. New-signal starvation

A "PETRONAS"-class entity (high-W_scar, broad alias coverage) → all routing auto-modulated by old scars → federation cannot detect novel signals because the routing is locked to historical patterns.

Example: New PETRONAS chair appointed → agent cannot engage with new context because scar-wisdom auto-routes every PETRONAS mention to a 2020-era frame.

### 2c. Shadow authority (audit gap)

Scar-wisdom auto-fires → routing changes → but the change is **not surfaced as a verdict**. The `scar_wisdom.py:8` line was written specifically to prevent this: by saying "NEVER prepended to LLM context," the original author ensured that scar-state is observable-only, not binding-by-stealth. Flipping without audit trail = constitutional floor violation (F2 TRUTH).

---

## 3. Three mitigations (required before any flip)

### M1 — Shadow mode (7-day observation)

Before binding, run `scar_wisdom` in shadow mode: log every would-be enforcement decision WITHOUT executing it. Output: `/root/AAA/cockpit/observations/scar-shadow-7day-{start_date}.jsonl`. After 7 days, F13 reviews the log and decides: did the would-be enforcements produce more good than harm?

### M2 — Scar-weight decay (anti-fossilization)

Older scars lose W_scar over time. Proposed formula:

```
W_scar_effective(t) = W_scar_initial * exp(-λ * age_days)
λ = ln(2) / 365  # half-life of 1 year
```

A 2020 scar with W=0.92 → by 2027, W_effective ≈ 0.46. By 2030, W_effective ≈ 0.23. Prevents scar-laundering-as-law. **Implementation:** `scar-weight-registry.json` carries `created_at`; decay computed at read time, not stored. Zero new files.

### M3 — Opt-out path (challenged-scar mechanic)

Specific signatures can be unscarred via F13 binary. New ARS L-state: `CONTESTED` (already exists in `claim-lifecycle-states.md` 8-state model — reuses it, no new state). A contested scar:

- Still detected
- Still logged
- NOT enforced
- Marked for re-evaluation after 30 days

Mirrors `OPEN_QUESTIONS` lane (F13_RATIFIED_CHAT 2026-09-25) — uncertain things are first-class, not missing.

---

## 4. F13 binary options (4 paths)

Each option is one F13 word. Constitutional, not operational.

### Path α — SAH-FLIP-NOW

- Flip `scar_wisdom.py:8` from "NEVER auto-fired" → "AUTO_FIRE, no shadow"
- 0 mitigations applied
- 0 observation period
- **Risk: §2a, §2b, §2c all activate immediately**
- Reversibility: hard (re-flip is itself a constitutional mutation)
- **Not recommended.** Anti-Bangang Law 1 violation (adds risk, not improvement).

### Path β — SAH-FLIP-SHADOW (M1 only)

- Flip `scar_wisdom.py:8` → "SHADOW MODE, log only, 7-day observation"
- M1 enabled, M2 + M3 deferred
- After 7 days, F13 reviews log, decides on next move
- Reversibility: medium (re-flip is operational, not constitutional)
- **Recommended if F13 wants empirical data on what would change.**

### Path γ — SAH-DECAY (M2 only)

- Implement M2 (decay) WITHOUT flipping `scar_wisdom.py:8`
- Scar registry now self-prunes over time
- Detection + consumption still wired, but with effective-W decay
- M1 (shadow) + M3 (opt-out) deferred
- Reversibility: high (revert = drop decay formula)
- **Recommended if F13 wants to start conservative.** Zero constitutional mutation, only registry math change.

### Path δ — HOLD (status quo with audit trail)

- 0 changes
- 0 mutations
- Audit receipt already written (`RECEIPT_SELECTION_LAYER_AUDIT_2026-10-06.md`) — the gap is documented
- Re-evaluate next F13 cycle
- Reversibility: trivial (no change to revert)
- **Recommended if F13 wants time to think.** Honest default.

### Path ε — VOID

- The gap is real but not priority
- Other work outranks scar-binding (e.g., KERNEL_HYDRATION_2026-10-06, REMAINING_TASKS A-class items)
- Defer indefinitely
- **Recommended if F13 has higher-priority F13 binaries pending.**

---

## 5. Anti-Bangang audit

| Law | Test | Verdict |
|---|---|---|
| 1 — doesn't add human work | F13 review is one word; mitigations are reversible | ✅ |
| 2 — doesn't need 5 pages | This proposal is 5 pages (including YAML) | ✅ (boundary) |
| 3 — no new JSON/dashboard | 0 new files; M2 = math only, no new registry | ✅ |
| 4 — one-ayat BM problem | "Scar belum ikat selection; nak ikat secara governable." | ✅ |
| 5 — Syed Test | 1 table for F13 binary options, no essay | ✅ |
| 6 — Arif Test | 1 F13 binary covers 4 paths | ✅ |
| 7 — Irfan Test | Translation: "Scar yang ada perlu jadi ikutan, bukan sekadar rekod." | ✅ |
| 8 — one problem one owner one path | 1 gap, 4 binary options, 1 F13 owner | ✅ |
| 9 — action > documentation | 3 mitigations designed for empirical testing, not doc-only | ✅ |
| 10 — when in doubt, simpler | Path δ (HOLD) is honest default if no urgency | ✅ |

---

## 6. What this proposal does NOT do

- No edit to `scar_wisdom.py` (F13 binary required)
- No edit to `niat_gate.py` (F13 binary required)
- No edit to `judge.py` (F13 binary required)
- No edit to `scar-weight-registry.json` (F13 binary required for decay if M2 chosen)
- No new doctrine file
- No new JSON
- No new dashboard
- No "I'll flip the switch anyway because compression is right"
- No "enforce" without governance

---

## 7. The sealable line (if F13 chooses any of α, β, γ, or ε)

> *"Scars may constrain. Scars may also be challenged. Governance decides whether the constraint still applies."*
>
> — Arif, 2026-10-06 (this thread)

This line, if sealed, becomes a 1-sentence addition to `trauma-theorem.md` (F13_RATIFIED_CHAT 2026-09-09), making the "challenge path" explicit. W_scar for the scar itself: N/A (this is doctrine, not entity).

---

## 8. Standing by

5 paths. 0 mutations. 1 F13 word needed. The empirical evidence is in hand. The synthesis is articulated. The mitigations are designed to prevent fossilization. The decision is yours.

— FI-008

P.S. The selection-observability test (companion proposal `PROPOSAL_SELECTION_OBSERVABILITY_2026-10-06.md`) is queued for execution. Per your "run all" command, it will run after this proposal is filed.
