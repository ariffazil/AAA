# AUDITOR Falsification Matrix — Reference Run 2026-08-30

**Source session:** `fallback-zen-20260830/` — Hermes gpt-oss-120b last-rung replacement dispute.
**Voice:** 555-ASI AUDITOR (musyawawah sibling).
**Lesson extracted:** 2026-08-30 21:57 MYT.

## When to use this reference

Load when AUDITOR is tasked to attack an ARCHITECT position (or any
sibling position) in a musyawawah and needs a concrete attack
template. The four-lens matrix below is the minimum-falsification
shape that survived a real run; if your attack has fewer lenses, it
is rhetoric, not evidence.

## The four-lens matrix (binding)

For EACH proposal being attacked:

### Lens 1 — Hidden failure mode

Name the second-order effect nobody wrote down. Pattern: take the
proposal at face value, then ask "what does this do that the
proposer didn't say it does?"

Examples from the 2026-08-30 run:
- ARCHITECT A moved Sonnet to rung 9 *while it stayed at rung 7* →
  correlated billing relationship across two rungs (Anthropic
  single point of failure dressed as redundancy).
- ARCHITECT B claimed summariser dependency on `auxiliary.compression`
  (MiniMax-M3) which is *weekly-exhausted today* → the "free"
  headline routed through paid Anthropic Haiku anyway.
- ARCHITECT C proposed three free-tier providers as a "lattice" →
  all three reset on vendor schedules; Arif's traffic pattern
  (long sessions, large context) is exactly the pattern free
  tiers punish.

If you cannot name a hidden failure mode, the proposal is
genuinely boring and AUDITOR may pass — but only with the
"passes falsification" verdict in writing.

### Lens 2 — Cost-vs-cascade-blast-radius mismatch

Two columns:
- **Cost** as the proposer stated it (cheapest framing).
- **Blast radius** as the worst-credible 30-day event.

Compute `blast_radius / cost`. If the ratio is bad (high blast,
low cost), the proposal is theatre. If the ratio is good (low
blast, high cost), the proposal is honest about its trade.

Examples:
- ARCHITECT A: cost $1.50/mo, blast radius = Anthropic outage
  takes 2 rungs. Ratio: bad (paid, still correlated).
- ARCHITECT B: cost ~$0 (with MiniMax), blast radius = summariser
  chain dies, raw 70k+ lands on rung 9, 413 returns. Ratio: bad
  (cheap, no real safety added).
- ARCHITECT C: cost $0 (within daily caps), blast radius = free
  tier cap at 10-15 calls/day, chain goes silent. Ratio: bad
  (cheap, cap is the binding constraint).
- AUDITOR counter: cost cents/day, blast radius = OR outage
  (rare, paid). Ratio: good.

### Lens 3 — F1 / F3 / F11 / F12 violations

For each floor, ask: "Does this proposal make reversibility,
evidence, graceful degradation, or scar-honesty WORSE?"

Cite the floor by name. Do NOT bundle into "constitutional
concerns" — the parent convergence needs to know which floor
tripped.

If you cannot cite a specific violation, the proposal passed this
lens. Most proposals pass F1, F3, F11, F12 individually; what
you are looking for is the proposal that violates 2+ in the same
move.

Patterns that consistently violate:
- "Move X to two positions" → F11 (correlated failure).
- "Summarise it before sending" → F3 (unbenchmarked lossy seam) + F1 (contract change without consent).
- "Add a free-tier mirror" → F11 + F12 (no scar recorded for the failure mode that is coming).
- "Pay for a bigger model" → F1 (single billing concentration) + F3 (uncached price assumption).

### Lens 4 — 30-day kill clock

Name three plausible production events that break the proposal in
the next month. NOT hypotheticals — events that already happened
in `errors.log` and WILL happen again.

Pattern: `grep -E "(429|413|529|ReadError|timeout)" errors.log`
shows the failure modes already in production. Any proposal that
ignores these is making an unsupported assumption.

Example killers from the 2026-08-30 run:
- For ARCHITECT A: "Anthropic has 4 partial degradations in 90
  days; both Sonnet rungs die together; DeepSeek also degraded
  twice this month (errors.log line 4956)."
- For ARCHITECT B: "MiniMax weekly reset cliff hits while summary
  in flight; summariser 429; rung 9 receives raw 70k+; 413."
- For ARCHITECT C: "Cerebras 1M tok/day cap hit in one afternoon;
  OR `:free` swaps to upstream model that hallucinates function
  calls; tool executor crashes; misclassified failure."

## Counter-position shape

After attacking all proposals, AUDITOR files ONE counter-position.
Not three. The shape:

1. **One model swap, not a stack.** Same model identifier or
   directly comparable, different channel/tier. Reuses what is
   already wired.
2. **One line of system fix, not a new rung.** (e.g. add 413 to
   retry triggers; record F12 scar.) The system fix is what
   would have prevented today's incident even if the model had
   stayed.
3. **F12 scar record.** Mandatory. Without it, the next AUDITOR
   re-litigates the same dispute from scratch.
4. **One-line summary at the end.** E.g. "Same model, paid
   channel, 128K ceiling, recorded scar, +1 retry trigger. That's
   the entire move."

Three counter-proposals is collaboration, not falsification. If
the parent synthesis sees three counter-proposals from AUDITOR,
AUDITOR has failed.

## Verification ritual before writing the audit

Run these BEFORE drafting the attack table:

```
# 1. Confirm the cited features exist (or don't) in config
grep -n "<feature>" /root/HERMES/config.yaml
grep -n "<feature>" /root/HERMES/*.yaml

# 2. Pull the actual incident evidence
grep -n "<error_code>" /root/.hermes/logs/errors.log | tail -20

# 3. Confirm the cost assumptions in the proposal
grep -n "circuit_breaker\|cache_control\|prompt_cache" /root/HERMES/config.yaml
```

If `circuit_breaker` returns nothing, ARCHITECT's claim about cost
caps is unfounded. Quote the grep result in the attack. "ARCHITECT
claims X; grep shows X is not in config; therefore ARCHITECT's cost
model is unfounded." This is the difference between AUDITOR-as-
rhetoric and AUDITOR-as-evidence.

## Edge case: ARCHITECT file not on disk at audit start

Parallel musyawawah often spawns AUDITOR before ARCHITECT finishes
writing. The task prompt may say "audit the proposals in
ARCHITECT_POSITION.md" but the file is missing.

Valid responses:
1. **Wait + attack later** — usually impossible; AUDITOR's window
   is bounded.
2. **Attack the obvious proposals** — any reasonable ARCHITECT
   would write the same three proposals given the inventory. State
   the assumption in the preamble. Re-verify when the file lands.

If the file arrives mid-audit, REWRITE the audit to attack the
actual proposals. Do not append a "correction" footnote that the
parent will miss.

## Worked example (excerpt from 2026-08-30)

```
A — "Big Floor" (Sonnet 4.5 paid @ 200k ctx as rung 9)
  Hidden failure mode: Anthropic appears at rung 7 AND rung 9.
  Cost vs blast: $1.50/mo, but blast radius = Anthropic outage
                 kills 2 rungs.
  Floor violations: F1 (correlated billing), F3 (prompt caching
                    not in relay_llm.py), F11 (no graceful mode).
  30-day killers: (a) Anthropic partial degradation → 2 rungs die,
                  (b) no circuit_breaker in config → cost cap is
                      narrative, (c) Anthropic key unmonitored → no
                      budget alarm.

  Verdict: REJECT.
```

Four sentences. Each one citable. Each one survives a parent
challenge. That is the AUDITOR shape.

## Anti-patterns (NEVER)

- ❌ Three counter-proposals (collaboration, not falsification).
- ❌ "Constitutional concerns" without naming the floor.
- ❌ Attacking a proposal without grep-verifying the cited features.
- ❌ "Could potentially fail in some scenarios" — name the scenario.
- ❌ Mirroring ARCHITECT's constructive framing in AUDITOR's counter.
- ❌ Long preamble before the attack table. AUDITOR opens with the
  attack, not with the methodology.
- ❌ Decorative epistemic tags without content. Tags are evidence
  hooks, not decoration — see pitfall #7 in the parent skill.

## Cross-references

- Parent skill: `forge-musyawawah-deliberation` SKILL.md (pitfalls #7–10
  for AUDITOR-specific patterns; this file is the worked example).
- Position template: `templates/position-file.md` — adapt section
  (4) "Constitutional risk on the OTHER position" to include the
  four-lens matrix.
- 2026-08-30 reference run: `/root/forge_work/fallback-zen-20260830/`
  — full AUDITOR_POSITION.md + ARCHITECT_POSITION.md + SYNTHESIS.md.
