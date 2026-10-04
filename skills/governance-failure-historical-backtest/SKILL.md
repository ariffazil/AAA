---
name: governance-failure-historical-backtest
description: "Build detector frameworks for civilizational-scale moral/governance collapse — control sets, blinded panels, exclusionary ratchet, Évian bound."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Governance, Holocaust, Atrocity, Backtest, Detector, F1-F13, arifOS]
---

# Governance-Failure Historical Backtest

## When to use

- Building any "could it have been prevented?" detector — for genocide, atrocity, regulatory capture, civilizational collapse, mass institutional failure.
- Designing a 6-agent / multi-domain constitutional analysis on a *single* historical case.
- Honest verdict-rendering under the F1-F13 floors when the answer has to be specific and falsifiable.
- Especially when the case feels "obvious" — that's when the hindsight bias is strongest.

## Core method — six non-negotiable fixes

Arif's critique of a Holocaust backtest (2026-08-06) is the canonical formulation. The six fixes are:

### 1. Control set is non-negotiable

A detector that fires on the target case but never runs against negative controls learns nothing. The 1929 stressed-democracy baseline applies to ~10 European polities in the same window — Italy, Poland, Hungary, Portugal, Yugoslavia, Romania, Austria — and most did not commit mass atrocity. Build a **panel** of country-years before the framework can claim anything.

Concretely: at minimum Italy 1925, Poland 1926, Hungary 1920, Portugal 1926, Austria 1933, Romania 1937, Czechoslovakia 1935 (benign baseline). If Germany-1935 doesn't rank above the panel mean on the substantive indicator, the framework is measuring nothing.

### 2. Blind the case selection

Stripping identifiers and running a panel of country-years is the only version that produces information. "Germany 1929-1939" encodes the answer before Agent 1 runs. The test that can be solved by reading the prompt isn't a test.

### 3. Split the ladder into two axes

`OPEN → FRAGILE → AUTHORITARIAN → SYSTEMIC ATROCITY RISK` collapses two weakly-coupled dimensions and guarantees false positives — most authoritarian regimes never commit mass atrocity.

- **Axis A — Regime Consolidation:** OPEN / FRAGILE / AUTHORITARIAN / CLOSED-TOTALITARIAN. Measured by elections, judiciary independence, military autonomy, media plurality, opposition capacity, term dynamics.
- **Axis B — Group-Targeting Ratchet:** NO-EXCLUSION / PROGRADE-EXCLUSION / LEGAL-CODIFICATION / CONFISCATION / SEQUESTRATION / EXPULSION / MASS-ATROCITY. Measured by dated public statutes and decrees.

Plot on a 2-axis chart. The upper-right corner is where atrocity risk lives; the lower-left is benign.

### 4. The exclusionary ratchet is the high-signal observable

Regime-level indicators (judiciary, military, media, elections) are noisy. The variable that carries signal is **legal codification of group exclusion**, dated and public:

- April 1933 civil service law
- September 1935 Nuremberg Laws
- 1938 property-registration and expropriation decrees

This is a monotone ratchet with an observable derivative. *It deserves its own agent*, not a line under "laws."

### 5. The Évian bound — what detection can and cannot buy

A framework that fires on 1938 (post-Nuremberg, post-Aryanization) tells the delegates of the Évian Conference what they already knew. The 32 nations convened precisely because the persecution was internationally recognized. **Detection ≠ action.** Build the test to measure the architectural ceiling for detection separately from the architectural ceiling for action. The binding constraint on atrocity prevention is willingness to absorb cost, not information.

### 6. Counterfactual Decision Audit (renamed from "Axiom of Choice Test")

The four-question audit on each decision node is sound:
1. What alternative choices existed?
2. Who possessed the choice?
3. What incentives constrained the choice?
4. What information was available?

The label "Axiom of Choice" borrowed mathematical authority the four questions don't earn — same error class as `epistemic.class: OBSERVED, integrity 1.0` on empty ingest. Rename to **Counterfactual Decision Audit** and keep the questions.

## Process discipline

### Sequencing gate

**Don't run the framework until tests/test_differential.py is red or green.** Code without a test that fails on bad inputs is a receipt for empty ingest.

### Hindsight lockdown

- No post-war findings, no final casualty counts, no Wannsee knowledge (until a 1942 checkpoint).
- Each rolling checkpoint (e.g. 1929, 1933, 1935, 1938) consumes only information available *before* that checkpoint.
- Treat future events as unknown.

### Each checkpoint output requires

- **Dominant risk driver** (economic / power / incentive / narrative / military)
- **Institutional failure driver** (which institution failed first)
- **Incentive failure driver** (who had upside from complicity)
- **Power concentration driver** (which concentration event raised tail risk)
- **Earliest credible warning point** — and *why* it wasn't visible at the time
- **Missing evidence** — the explicit list of facts that would have changed the verdict if available

## Output templates

For each checkpoint:

```
VERDICT: [OPEN / FRAGILE / AUTHORITARIAN / TOTALITARIAN] on Axis A
        [NO-EXCLUSION / ... / MASS-ATROCITY] on Axis B
CONFIDENCE: [0.00–1.00]
DOMINANT RISK DRIVER: [economic | power | incentive | narrative | military]
INSTITUTIONAL FAILURE DRIVER: [named institution]
INCENTIVE FAILURE DRIVER: [named actor class with upside from complicity]
POWER CONCENTRATION DRIVER: [single concentration event]
MISSING EVIDENCE: [facts that would shift verdict]
EARLIEST CREDIBLE WARNING: [date + signal + why not visible]
```

## Power-law framing

When decision-making nodes drop below ~5, the system enters **infinite-variance territory**: any outcome, including civilizational-scale catastrophe, becomes possible. Concentration is not simplification — it concentrates tail risk.

Suggested heuristic:
- 50+ nodes → local consequence
- 10–50 → regional
- 5–10 → national
- 3–5 → continental
- 1 → civilizational

Multiplicative institutional independence is the **firewall against fat-tailed catastrophe** in any complex system.

## Pitfalls

- **Hindsight bias:** assembling a rolling atrocity assessment of a country picked at random encodes the answer before Agent 1 runs. Blind the panel.
- **False precision:** assigning 0.94 confidence to a 1934 checkpoint because "we know what happened" is hindsight. Confidence must derive from contemporaneous evidence density, not from outcome.
- **False-positive inflation:** most authoritarian regimes never commit mass atrocity. Collapsing regime-consolidation and group-targeting onto one ladder guarantees false positives on the authoritarian half and false negatives on the massacre half.
- **Borrowed authority:** naming a four-question audit "Axiom of Choice" borrows set-theory authority for an unrelated method. Same defect as epistemic.class: OBSERVED on empty ingest.
- **Cost-blindness:** the binding constraint on atrocity prevention after the detection floor is met is willingness to absorb cost (Évian). Don't conflate detection-architecture with action-architecture.
- **The ceiling on existing tools (Aug 2026, verified):** `wealth_power_consequence_map` is content-sensitive (SHA-256 derivation) and scores correctly across the panel — Germany 1929 LOW (0.265), Weimar/Germany 1935 HIGH (1.0), Italy 1935 HIGH (0.985), Poland 1935 HIGH (0.823), France 1935 LOW (0.258). **But Italy 1935 ranks within 0.015 of Germany 1935** because the tool measures power structure (decision concentration, irreversible harm, exit rights denial) — not group-targeting ideology. The Axis A / Axis B split is *structural*, not just labeling: a tool that returns one scalar cannot separate "authoritarian with colonial violence" from "systematic domestic extermination of a citizen minority." The exclusionary ratchet (Nuremberg laws, civil service law, property decrees) is a separate axis that `power_consequence_map` does not measure. Don't claim "the detector fires on the Holocaust case" unless it also includes the ratchet as a distinct signal. A scalar that ranks Germany and Italy together is not a Holocaust detector.
- **The "axis B is the high-signal observable" trap:** saying "the ratchet deserves its own agent" is not the same as building it. If only Axis A exists in code (as in WEALTH today), the framework runs on a single dimension and inherits the false-positive ceiling. Treat the two-axis split as a code-shape requirement, not a labelling convention. Every detector for civilizational-scale atrocity must (a) measure ratchet directly as a monotone time-series of dated legal acts, (b) plot it on a separate axis from regime consolidation, (c) refuse to render a final verdict when ratchet data is unavailable — the missing axis is the verdict's missing evidence, not a partial verdict.
- **The "evolving in AI capability" misframe (Arif, 2026-08-06):** the deepest insight from the backtest session is not "how smart should WEALTH become?" but "where must WEALTH stop?" The detector's own F13 boundary is what makes it a constitutional instrument rather than a successor tool. If a detector can answer "act now, override sovereign" it has become the same shape as the failures it studies — single-actor decision-making, no veto, no Évian-bound willingness check. The ceiling is the design.

## Verification

- Run the framework on Italy 1925 and Hungary 1920 before claiming any verdict on Germany. If scores cluster, panel-rank, or invert in unexpected ways, revise the framework before publishing.
- For each checkpoint, the missing-evidence list must be non-trivial. A checkpoint with empty missing-evidence is a confession that you used hindsight.

## Support files

- `references/germany-1929-1939-case.md` — full rolling-checkpoint backtest across 1929/1932/1934/1937 with verdicts, dominant drivers, and the Évian-bound discussion.
- `references/decision-node-audit-recipe.md` — the four-question counterfactual audit template, with examples (Hindenburg, Centre Party, Rhineland, business elites).
