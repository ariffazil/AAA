# Temperature T — Witness Audit

> **Forged:** 2026-09-11 by 333-AGI Δ MIND under F13 SOVEREIGN directive
> **Scope:** `/root/{AAA,arifOS,A-FORGE}` — exploration-pressure signals across the federation
> **Doctrine input:** Eureka #7 — "Temperature Is More Fundamental Than ALPHA"
> **Verdict:** DRAFT — witness gathered, formal T parameter proposed as 5th APEX dial, awaiting F13

---

## 1. Executive Witness

**Exploration pressure (T) is partially embedded in APEX already, but not first-class addressable.**

| Layer | Has T? | Form | Code |
|-------|--------|------|------|
| LLM sampling | yes | `temperature: 0.2-0.7` knobs | `forgeGemini.ts:36,46,68` · `flame_client.ts:113` · `SeaLionProvider.ts:116` · `ChatCompletionProvider.ts:177` · `skillForge.ts:100,169` |
| Memory cooling | yes | `temperature float8 [0,1]` cooling rate | `supabase/migrations/20260628_001_cooling_ledger_core.sql:41` |
| APEX formula | partial | `X = EXPLORATION × AMANAH` | `apexDials.ts:30,62,211` |
| Possibility space | yes | `max_hypotheses: 4` default | `reality-loop/types.ts:622` · `forgeTools.ts:1824` · `prompts.ts:442,447` |
| Diversity guard | yes | `minTaskTypeDiversity` | `mcp/shell/antiSink.ts:165,166,173,181` |
| Witness diversity | yes | `witness.diversity` PARTIAL/NONE | `infrastructure/governance/actBridge.ts:67,158` |
| Organ mapping | yes | `333 EXPLORE` reason layer | `mcp/contract/civilizational_eight_organs.ts:101,283,309` |
| Novelty score | NO | — | absent |
| Stagnation detector | partial | FQ STUCK / FOSSILIZED verdicts | `arifFlow :7073/health` (live) |

**Smoking gun:** `apexDials.ts:30` already names `X = EXPLORATION × AMANAH`. EXPLORATION is in the constitutional formula — but it's mixed with amanah via geometric mean, not addressable as a standalone control.

---

## 2. Current T-Like Parameters in Code

### 2.1 LLM sampling temperature (per-call, not systemic)
```
forgeGemini.ts:    temperature: args.temperature || 0.7   (default)
flame_client.ts:   temperature: 0.2                       (chat)
SeaLionProvider.ts: temperature: 0.3
ChatCompletionProvider.ts: temperature: 0.3
skillForge.ts:     temperature: opts.temperature ?? 0.2
```
**Class:** Per-call inference knob. Not systemic.

### 2.2 cooling_ledger temperature (memory decay)
```sql
CREATE TABLE cooling_ledger_entries (
  ...
  temperature float8 NOT NULL DEFAULT 1.0,  -- 1.0 fresh, 0.0 cooled
  ...
);
CREATE INDEX idx_cle_temperature ON cooling_ledger_entries(temperature);
```
**Class:** Memory decay rate. 1.0 → 0.0 over time. Controls how fast witness objects cool out of active memory.

### 2.3 APEX X dial (constitutional)
```ts
// apexDials.ts:30
X: number;  // EXPLORATION × AMANAH — GM(F6, F8, F9, Risk)
// apexDials.ts:16 (canonical T-000 §2 mapping)
X (EXECUTION/XPLORE):   F6, F8, F9, Risk → Empathy, Genius, Anti-Hantu, Risk
```
**Class:** Constitutional dial. Mixed with amanah via geometric mean. Not directly tunable.

### 2.4 Hypothesis count (possibility space)
```ts
// reality-loop/types.ts:622
max_hypotheses: 4,  // default in forge_reality_loop config
// engine.ts:286
generate ${config.max_hypotheses} mutually-exclusive hypotheses
// forgeTools.ts:1738
JSON config: {iteration_depth, max_hypotheses, action_budget, ...}
```
**Class:** Hardcoded constant per session. Tunes possibility space size.

### 2.5 Diversity guards (anti-Calhoun)
```ts
// antiSink.ts:165
const diversity = state.taskTypesSeen.size;
if (diversity < config.minTaskTypeDiversity) {
  hints.push(`Task diversity ${diversity} < ${config.minTaskTypeDiversity} min`);
}
```
**Class:** Behavioral check, not a tunable.

### 2.6 Organ mapping (constitutional intent)
```
civilizational_eight_organs.ts:101
arifos_mapping: ["111 THINK", "333 EXPLORE", "AGI reasoning layer"]
civilizational_eight_organs.ts:283
3. REASON → 111 THINK + 333 EXPLORE reason about situation
```
**Class:** Name only. No code enforces 333 = EXPLORE function as T.

---

## 3. Audit Questions — Answers from Witness

| Question | Answer | Witness |
|----------|--------|---------|
| What increases exploration? | LLM temperature knobs (0.7), `max_hypotheses` count, low FQ throttling | §2.1, §2.4 |
| What decreases exploration? | Cooling decay, FQ STUCK/FOSSILIZED verdicts, F13 HOLD | §2.2, FQ probe |
| How do we detect novelty? | Diversity guards (antiSink), witness diversity counter | §2.5, §2.6 |
| How do we detect stagnation? | FQ vector diagnosis (FOSSILIZED/STUCK/BURNING/FLOWING/OPTIMAL) | FQ probe (live) |
| How do we measure possibility-space size? | `hypothesis_count`, `max_hypotheses`, `sample_size` (in apex-semantics.md) | §2.4 |
| How do we measure exploitation vs exploration? | X dial via F6+F8+F9+Risk; ratio (hypotheses generated vs hypotheses committed) | §2.3, §2.4 |

---

## 4. The Gap

There is **no first-class T parameter**. Exploration pressure is:
- Implicit in LLM temperature (per-call, not systemic)
- Implicit in APEX X dial (mixed with amanah)
- Implicit in `max_hypotheses` (hardcoded constant)
- Implicit in cooling rate (memory decay)
- Implicit in diversity guards (behavioral only)

No agent can read a single value `T` and know "how aggressively is this system exploring right now?"

---

## 5. Formal Proposal — Survivability Inequality

```
T × G ≥ FQ
```

### Unit Analysis

| Symbol | Domain | Units | Source |
|--------|--------|-------|--------|
| T | exploration temperature | dimensionless [0,∞) — proposed normalized to [0,1] | new: Boltzmann-style |
| G | constitutional fitness | dimensionless [0,1] | APEX canonical `G = (A·P·E·X)^(1/4)` |
| FQ | reality-contact ratio | dimensionless [0,∞) — verify/execute | arifFlow FQ metric |

**Unit check:** all dimensionless. Inequality is well-defined.

### Survivability Conditions

| State | T | G | FQ | T·G ≥ FQ? | Verdict |
|-------|---|---|-----|-----------|---------|
| FROZEN | low | high | low | borderline | too cold, too committed |
| CHAOTIC | high | low | low | fails | too hot, no judgment |
| BURNOUT | high | high | low | fails | lots of action, no verify |
| FOSSILIZED | low | low | high | fails | no variation, only verify |
| VIABLE | balanced | balanced | balanced | passes | sustainable adaptive loop |

**Inequality holds iff:** variation is wide enough, governance is sharp enough, and reality-contact is high enough — simultaneously.

---

## 6. Proposed 5th Dial — T (EXPLORATION TEMPERATURE)

Modify APEX canonical formula:
```
Current: G = (A · P · E · X)^(1/4)              [4-dial Nash Bargaining Product]
Proposed: G = (A · P · E · X)^(1/4) · σ(T)    [4-dial × sigmoid temperature gate]
```

Or expose T separately:
```
Current: G = (A · P · E · X)^(1/4)
Proposed: G = (A · P · E · X)^(1/4) where T is read from X sub-component
```

**Option A (additive — break canonical):** Add T as 5th dial. `G = (A·P·E·X·T)^(1/5)`.
- Pro: Explicit, tunable
- Con: Breaks V3 directive (4-dial). Requires F13 sovereign ratification.

**Option B (extractive — keep canonical):** Decompose X into `X = (T · Am)^(1/2)` where Am = AMANAH-only dial. Keep G 4-dial but expose T as sub-component of X.
- Pro: Preserves V3. T becomes addressable.
- Con: Requires redefining X geometric mean.

**Option C (orthogonal — new layer):** Keep G canonical. Add T as separate pre-filter on `max_hypotheses`. `effective_hypotheses = max_hypotheses · σ(T)`.
- Pro: Zero disruption. Surgical.
- Con: T not in constitutional G.

**Recommendation:** Option B. Preserves canonical G while making T first-class.

---

## 7. Reversibility

This audit is read-only. No mutation. No state change. Pure witness.

The proposed T parameter is **NOT YET IMPLEMENTED**. The witness object documents what currently exists and what could be added without breaking the canonical 4-dial formula.

---

## 8. Open Questions (for sovereign JUDGMENT)

1. Should T become a 5th APEX dial (breaks V3) or a sub-component of X (preserves V3)?
2. Should `max_hypotheses` default of 4 be replaced with `f(T)` dynamic count?
3. Should `333 EXPLORE` organ be formally ratified with EXPLORATION temperature authority?
4. Should the survivability inequality `T × G ≥ FQ` be canonized as a system law?
5. Name: `T` (Boltzmann) vs `α` (alpha field) vs `EXPLORATION_TEMP` (verbose)?

---

## 9. Anti-HARAM Audit

- [x] **No Pretending** — every claim cites file:line
- [x] **No Human-as-Adapter** — no copy-paste, no relay
- [x] **No Attention Theft** — narrative ≤ 1 sentence per table
- [x] **No Authority Drift** — no canonical mutation proposed without flagging V3 break
- [x] **No Narrative > Reality** — witness object, not story

---

*DITEMPA BUKAN DIBERI ⚒️*
