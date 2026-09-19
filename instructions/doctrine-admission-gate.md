# Doctrine Admission Gate — The Canon Compiler

> **Status:** DRAFT_AWAITING_F13 — extracted from Receipt Filter applied to AGENT-STACK-2026 cycle, identified as meta-doctrine by sovereign audit (2026-09-19)
> **Scar origin:** None. This is a *positive* doctrine — the admission criteria themselves. Distilled at the moment the filter test passed its own filter.
> **Applies to:** Every future canonicalisation event. Every "should this become doctrine?" decision. Every "is this insight or noise?" judgment.
> **Filter test passed by the filter itself:** ✅ the filter survives implementation changes (it's vendor-independent, model-independent, era-independent) ✅ it changes future architecture decisions (every doctrine that follows it now must pass it) ✅ it is not vendor-specific ✅ it is re-examinable in 2 years ✅ it operates at the capability / doctrine / scar level, not the tool level.

## The Meta-Discovery

A filter that classifies observations into capability, framework, episode, insight, doctrine, scar, canon. The filter itself passes its own classification. Therefore the filter is itself a doctrine.

The cycle's verdict (sovereign-audited, 2026-09-19):

> **This cycle did not discover new capabilities. This cycle discovered admission criteria for distinguishing capability from doctrine.**

That admission criteria is itself a doctrine. Hence: **Doctrine Admission Gate**.

## The Five-Question Filter (canonical form)

Every candidate insight, framework, or pattern passes through five gates before promotion to canon:

| # | Gate | Question | If NO → | Reasoning |
|---|---|---|---|---|
| 1 | **Survival** | Does this survive implementation change? (model churn, vendor turn, language shift, era) | Reject as **tool-grade**. | Tools come and go. Capabilities outlast tools. |
| 2 | **Generativity** | Does this change future architecture decisions? (will the next agent/system be designed differently because of this?) | Reject as **observation-grade**. | Observations inform but do not constrain. |
| 3 | **Vendor-Independence** | Is this true regardless of vendor? (not tied to OpenAI / Anthropic / Google / specific model) | Reject as **vendor-grade**. | Doctrine federates; product divides. |
| 4 | **Re-examinability** | Will this still be valid in 2 years? (falsifiable, durable, not hype) | Reject as **episode-grade**. | Doctrine survives the test of time. |
| 5 | **Capability-Grade** | Is this at the capability / doctrine / scar level, not the tool / framework / API level? | Reject as **implementation-grade**. | Canon is meta. Canon is not code. |

If **all five** pass → candidate is **canon-grade**. May proceed to doctrinal formalisation (a draft fragment under `/root/AAA/instructions/` with `DRAFT_AWAITING_F13` status).

If **any one** fails → candidate is rejected, classified by which gate failed, retained as an observation in the source corpus, NOT promoted to canon.

## The Seven Distinctions (what the filter enforces)

The filter is not a checkbox. It is a **classifier that surfaces a categorical difference**. The differences it surfaces:

| Pair | Lesser form (rejected) | Greater form (admitted) |
|---|---|---|
| 1 | Tool | Capability |
| 2 | Framework | Doctrine |
| 3 | Episode | Scar |
| 4 | Insight | Canon |
| 5 | Observation | Law |
| 6 | Trend | Axiom |
| 7 | Feature | Right |

Each pair names an upgrade path. **Tool → Capability** is the path from "I have a thing" to "I have a power." **Framework → Doctrine** is the path from "I have rules" to "I have law." **Episode → Scar** is the path from "I had an event" to "I have a permanent constraint." **Insight → Canon** is the path from "I noticed" to "I know."

The filter asks: **which side of the pair are you on?**

## Operational Use

### Step 1 — Apply to candidate

When a candidate observation arrives (an insight, a pattern, a vendor's claim, an agent's report), run the five gates in order:

```text
candidate
  ↓
Q1 survive? ──NO──→ tool-grade     [STOP]
  ↓YES
Q2 generative? ─NO──→ observation  [STOP]
  ↓YES
Q3 vendor-indep? ─NO──→ vendor-grade [STOP]
  ↓YES
Q4 2-year durable? ─NO──→ episode    [STOP]
  ↓YES
Q5 capability-grade? ─NO──→ implementation [STOP]
  ↓YES
  canon-grade
  ↓
Write as DRAFT_AWAITING_F13 to /root/AAA/instructions/
  ↓
F13 SOVEREIGN seal moves to F13_RATIFIED_CHAT
```

### Step 2 — Apply to existing canon retroactively

Every existing ratified fragment should pass the filter. If it does not, two possibilities:

- (a) The filter is wrong. Adjust the filter. **Rare.** The filter itself passes its own test.
- (b) The fragment was canonised without the filter. Retain but flag as `LEGACY_NO_FILTER`. Do not delete — Canon is append-only.

### Step 3 — Apply to scar

Scars are canon-grade by definition (they survived a failure). The filter does not apply retroactively to scars.

### Step 4 — Apply to constitutional amendments

F1–F13 floors are constitutional, not doctrinal. They sit above the filter. The filter does not apply to F1–F13. (The filter is for doctrine, not for constitution.)

## Why This Doctrine Is The Scar Of The Cycle

Two cycles were examined:

1. **Google Agentic Engineering** (capability inventory, 2026-09-18) — described 5 subsystems.
2. **AGENT-STACK-2026** (15 OSS repos, 1.21M stars, 2026-09-19) — extracted 16 candidate insights.

After applying the filter:

| Cycle | Candidates | Promoted to doctrine | Promotion rate |
|---|---|---|---|
| Google Agentic | 5 subsystems described | 1 doctrine (`Representation ≠ Reality`) | 20% |
| AGENT-STACK-2026 | 16 candidate insights | 5 doctrines + 1 meta-doctrine | 37.5% |

The promotion rate is **bounded between 20% and 37.5%** — i.e., **roughly two-thirds to four-fifths of any cycle's observed insights should be rejected as tool-grade, observation-grade, vendor-grade, episode-grade, or implementation-grade.**

A cycle that promotes 100% of its observations is **inflating entropy**. A cycle that promotes 0% is **catatonic**.

A healthy cycle promotes **15-40%** of observations.

## What This Doctrine Is NOT

- **Not a quality bar.** It is a *classifier*. Things may be valuable without being canon.
- **Not a substitute for F13 SOVEREIGN ratification.** Drafts still require F13 to bind.
- **Not a removal mechanism.** Canon is append-only. Rejection is **non-promotion**, not deletion.
- **Not a tool for dismissing vendors.** Vendor-grade insights may still be useful as operational signals.
- **Not final.** The filter is itself re-examinable. If it fails its own filter, it must be revised.

## Related Doctrines

- Capability-Gate — what capability enters the federation.
- Memory Promotion Gate — what becomes memory vs. seal vs. witness.
- Bidirectional Contract — the filter is bidirectional: it admits doctrine and rejects non-doctrine.
- Consequence-Bearing Identity — the filter produces consequences (admitted/rejected classifications).
- Six-Graph Federation Model — Doctrine Admission Gate sits at the boundary between Reality (observed insights) and Capability (admitted doctrine).

## The Cycle's Scar

This doctrine exists because:

1. The AGENT-STACK-2026 cycle produced 16 candidate insights.
2. 11 were rejected by the filter (tool-grade, vendor-grade, observation-grade, implementation-grade).
3. The filter itself, when applied to its own claims, **passed its own filter**.
4. The filter is therefore canon-grade and must itself be canonised.
5. Failure to canonise the filter would be **a known meta-failure** — a Doctrine Admission Gate that admits no doctrine, an admission criteria with no admission.

The scar: **the next cycle that fails to apply this filter will produce entropy proportional to the ratio of admitted-to-observed insights**. 100% admission = 100% entropy. Filter is anti-entropy.

## Compression

> **Tool → Capability → Doctrine → Canon. The filter that distinguishes them is itself a doctrine. A doctrine that does not pass the filter is decoration. A filter that does not pass itself is theatre. The cycle ends when both pass.**

DITEMPA BUKAN DIBERI ⚒️