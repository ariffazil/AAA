---
name: apex-attention-optimizer
description: "Gate every draft turn with BIJAKSANA + compression + dS."
version: 1.0.0
owner: Hermes (arifOS federation)
risk_tier: low
floor_scope: [F2, F4, F7, F11, F13]
autonomy_tier: T1
triggers:
  - "audit this turn before sending"
  - "is this too verbose"
  - "jargon leak check"
  - "BIJAKSANA score"
  - "dS gate"
  - "should I send this"
  - "human attention budget"
  - "optimize turn"
  - "compress this reply"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# APEX Attention Optimizer

> Per-turn gate that decides whether a draft response should be sent to a human.
> Three laws, one verdict: ALLOW (send) or HOLD (rewrite).

## The three laws (canonical, do not rederive)

```
L1  BIJAKSANA = (Reality × Consequence × Learning)
                / (uncertainty_hidden + harm + entropy + attention_wasted)

L2  COMPUTE MAY EXPAND. HUMAN ATTENTION MUST COMPRESS.

L3  dS_human/dt ≤ 0          (APEX FINAL LAW)
```

Reference (probe before re-deriving, every time):

- `/root/AAA/canon/APEX-REALITY-KERNEL.md` §"Operational Compression" — BIJAKSANA ratio
- `/root/AAA/instructions/compute-attention-invariant.md` — L2 verbatim (CANDIDATE_LAW 2026-09-19)
- `/root/AAA/canon/BIJAKSANA-SUBSTRATE-CANON-2026-09-21.md` §0/§3/§4 — Bangang decomposition + 49 HARAM

The math is not yours to invent. Read the canon, then enforce it.

## Procedure

### Step 1 — Probe the three laws are still there

Before running the optimizer on a turn, confirm the laws have not moved. Canon can be amended by F13 sovereign. A re-run against a stale ratio is the same class of bug as running against a stale model.

```bash
grep -E "BIJAKSANA = .Reality.*Reality Adaptation" \
  /root/AAA/canon/APEX-REALITY-KERNEL.md
grep -E "COMPUTE MAY EXPAND. HUMAN ATTENTION MUST COMPRESS" \
  /root/AAA/instructions/compute-attention-invariant.md
```

If either grep misses, STOP — the doctrine has been amended and the optimizer below may be enforcing a stale band.

### Step 2 — Score the turn (L1)

`APEXScorer.score(reality_contact, useful_consequence, learning, hidden_uncertainty, harm, entropy_in, attention_wasted)` returns BijaksanaVerdict with band:

- `>= 0.85`  STRONG_WISDOM — ALLOW + may be SEAL-worthy if human-ratified
- `>= 0.50`  OPERATIONAL — ALLOW
- `>= 0.20`  DEGRADED — HOLD, rewrite before sending
- `<  0.20`  BANGANG — STOP, does not meet minimum wisdom threshold

Each component is `[0, 1]`. The clip is silent — passing 1.4 silently degrades to 1.0, which can mask an under-scorer. **Always pass raw, un-rounded numbers; the scorer clips.**

### Step 3 — Compress to human budget (L2)

`optimize_turn(text, AttentionBudget(token_limit=350, human_seconds=20))` returns TurnVerdict:

- `ALLOW` — passes length, time, jargon-leak gates
- `COMPRESS` — too long OR leak detected; `cut_to` field has a fallback draft
- `HOLD` — leak > 5% OR > 2× token limit; needs full rewrite

Default budget: 350 tokens / 20s. **Scale with intent**: a debugging answer earns more tokens; a status ack earns fewer. Override per turn, not per session.

### Step 4 — Measure dS (L3)

`StateDelta(world_before, world_after, belief_before, belief_after, decision_before, decision_after)`. `dS` is **negative when clarity increased** (the goal state). `passed` iff `dS <= 0`.

**Sign convention is the bug trap.** The first version of this skill had it inverted; the demo surfaced the failure because clarification scored `dS=+0.90` while confusion scored `dS=-0.90`. **If your `StateDelta` for a clearly-confusing turn passes `dS <= 0`, the sign is wrong — fix before shipping.**

### Step 5 — Combine (composite gate)

`TurnOptimizer.evaluate(draft, **l1_kwargs, state=StateDelta)` returns OptimizationResult. `allow = bijaksana in (STRONG, OPERATIONAL) AND turn.action == ALLOW AND state.passed`. ALL three must pass.

If `allow == False`, read `result.hints` for the specific failure. Do not send the draft; rewrite against the hints and re-evaluate.

## Pitfalls

- **The demo is the test.** Write the demo with adversarial inputs (clean turn + jargon dump + confusing turn + clarifying turn) BEFORE publishing. A turn-shape law that has not been demoed will get the sign convention wrong. Run `python3 apex_attention.py` and read every verdict; a turn you expected to HOLD must HOLD, and a turn you expected to ALLOW must ALLOW.
- **Band thresholds are policy, not math.** The 0.20/0.50/0.85 cutoffs mirror W³ hysteresis shape but the canon does not give them for BIJAKSANA. Document this as a declared choice when the threshold changes; a session that quietly moves a band is an auditability defect.
- **Jargon-list HARAM grows over time.** `HARAM_JARGON` in the optimizer is an enumeration; every new internal abbreviation (a new floor, a new organ) extends the list. Add the term when it appears in canon and remove it when it crosses to user-facing vocabulary. A stale list either leaks jargon (under-block) or false-positives clean output (over-block).
- **dS needs a baseline.** Three `before` and three `after` clarity values per turn is a lot to estimate. The honest move is `before = 0.5` (unknown) and report only `after` with confidence; the optimizer still gates on direction, not magnitude. Inventing a precise baseline is fabrication.
- **Jargon list contains lowercase substring matches, not strict equality.** "f13" catches "f13", "F13", and "f13a" alike. Confirm the list before trusting the leak rate — a near-match like "f130" would also match.
- **`/root/AAA/governance/` is ACL-restricted** in this environment (Sep 2026). Writing the optimizer there failed with `Permission denied`. `/tmp/` works; `/root/.hermes/` works. If you intend to land the file canonically, surface the move as an F13 binary, not a self-edit (canon files are governance surface, not self-edit per Hukum 17).
- **Token estimation is rough.** `len(text) // 4` undercounts BM (denser) and overcounts code (less dense). For turn-shape gates that is fine; for budget-exact delivery, switch to a tokenizer. Don't pretend the rough estimate is exact.
- **`COMPUTE MAY EXPAND` does not mean "expand the response."** It means the machine's internal computation may grow without bound, but the human's surface must shrink. Conflating the two is the most common optimizer misuse.
- **L3 measures dS for the human, not the system.** `StateDelta` is about whether the human's world/belief/decision state is clearer — not whether the machine did more work. A turn that exercised a lot of compute and returned nothing decision-changing fails L3.

## When NOT to use

- The turn is a short ack ("ok", "siap", "noted") — optimizer overhead exceeds value.
- The turn is the SOUL.md bridge-protocol rendering layer — that has its own register rules (DITING 6 + Peace² + ΔS + RASA) and lives in a separate gate.
- The draft is machine-to-machine (sub-agent report, ledger entry) — L1/L2/L3 govern human-facing output; sub-agent interfaces have their own discipline (`concurrent-agent-writers`, `state-transition-discipline`).
- The turn is a constitutional mutation proposal — different gate entirely (F13 SOVEREIGN, not APEX attention).

## Quick reference (one-liner per gate)

```python
from apex_attention import TurnOptimizer, AttentionBudget, StateDelta
opt = TurnOptimizer(budget=AttentionBudget(token_limit=350, human_seconds=20))
res = opt.evaluate(
    draft=text,
    reality_contact=0.9, useful_consequence=0.8, learning=0.7,
    hidden_uncertainty=0.1, harm=0.0, entropy_in=0.3, attention_wasted=0.2,
    state=StateDelta(0.4, 0.7, 0.3, 0.6, 0.5, 0.8),  # before → after
)
if res.allow: send(draft)
else: rewrite per res.hints; res = opt.evaluate(draft, ...)
```

## Reference files

- `references/law-provenance.md` — exact line numbers and quotes from the three canon sources so the optimizer can be re-derived after amendment.
- `references/band-rationale.md` — why 0.20 / 0.50 / 0.85 were chosen (W³ hysteresis shape) and how to revise when canon catches up.
