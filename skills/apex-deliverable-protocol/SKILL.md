---
name: apex-deliverable-protocol
description: "Output contract for any SOVEREIGN-grade deliverable that must survive audit: Claim → Evidence → Derivation → Countercase → Trigger → Action → Falsifier → Confidence. Claim-graphed, counter-tested, scenario-branched artifacts with a semantic-role visual palette. Load for any briefing/report that must be verifiable, not just readable."
tags: [research, deliverable, audit, apex, arif-standard]
version: "2026-08-07-v1"
ratified: "2026-08-07 by F13 SOVEREIGN — from weekly-brief v1→v2 audit (Arif: 'claim graphing and countercase blocks are the two biggest upgrades')"
---

# APEX DELIVERABLE PROTOCOL

> The difference between a brief that narrates and an artifact that can be verified.
> v1 was a good narrative. v2 is an artifact — every claim addressable, every scenario
> weighted, every trigger actionable, every falsification visible.

## The 8-step contract (binding)

```
Claim → Evidence → Derivation → Countercase → Trigger → Action → Falsifier → Confidence
```

Any deliverable missing more than two of these steps is a memo, not an artifact.

## 1. Claim graphing

Every nontrivial statement gets a boxed block:

- **Claim ID** (`C-01`, `H-01`...) — unique, addressable. A claim with no ID cannot be challenged in isolation; that means the reader must trust the narrator.
- **Epistemic chip** — OBS / DER / INT / UNKNOWN.
- **Claim text** — the statement, plain.
- **Evidence block** — source IDs (see source index), 1–3 per claim.
- **Falsifier** — what would prove this wrong, stated concretely ("JMIC >20 transits ×3 days").
- **Confidence** — 0–1 band, not a vibe ("0.95 [OBS]").

## 2. Adversarial balance

Every main thesis gets a **countercase box** (orange, distinct from verdict boxes):
1. Steelman of the opposite view (the strongest version, not a strawman).
2. One disconfirming datapoint.
3. What would shift your view by next week.

No countercase on a thesis = F2 risk. Bias-test discipline applies to every main thesis, not just the user's stated bias.

## 3. Scenario engine

Never single-path directional language ("opens the path to", "gold tests $3,900").
Always 3-scenario branching:

| Scenario | Weight | Band | Trigger |
|---|---|---|---|
| Base | 40% | $65–70 | Hormuz reopens by Q3 |
| Upside | 25% | $95–100 | Deal collapses, strikes resume |
| Failure | 35% | $56–65 | Demand collapse |

Each scenario carries: weight, price band, trigger, falsifier. Weights must sum to 100%.

## 4. Visual semantic palette

One colour = one meaning, across the whole document:

| Colour | Meaning |
|---|---|
| NAVY `#0e1a2b` | Observed data |
| GOLD `#c9a227` | Derived model / median |
| RED `#c0392b` | Risk threshold / invalidation |
| GREEN `#1e8449` | Upside scenario |
| ORANGE `#e67e22` | Adverse countercase |
| GREY `#7f8c8d` | Neutral context |

Chart titles encode their falsification test inline. If two charts use the same colour for different semantic roles, the grammar is broken.

## 5. Decision packet (ends the deliverable)

Trigger-response grid, not a watchlist:

```
SIGNAL | TRIGGER (falsifier) | HORIZON | CONFIDENCE | ACTION | EXPECTED 2ND-ORDER
```

- Confidence ≥60% green = act. <60% orange = wait.
- Action = direction only; sizing is the operator's risk budget.
- Expected = second-order market reaction (what moves next).

## 6. Source index (appendix)

Numbered table `S-01 … S-36`: ID · source · URL/doc · used-for. Any claim can be challenged and traced in two steps.

## 7. Three-lane layout (PDF)

Repeating visual lane per section: **Headline signal · Evidence block · Operator implication**. Left border gold = signal, blue = evidence, red = implication.

## Provenance

- Weekly brief v1 (2026-08-07): "Strong brief, not Apex" — single-path language, no countercases, mixed palettes, watchlist-only ending.
- Weekly brief v2 (2026-08-07): claim-graphed, counter-tested, scenario-branched, decision packet. ΔS = 0.42. Arif verdict: "claim graphing and countercase blocks are the two biggest upgrades. The decision packet is the operator-grade deliverable."
- Artifact: `/root/forge_work/hermes-apex-audit-2026-08-07/Arif_Apex_Audit_v2_2026-08-07.pdf`

## Pitfalls

- Countercases that confirm the main thesis are not countercases. They must hurt.
- Weights that don't sum to 100% signal the model was never completed.
- A falsifier that cannot be checked this week is a wish, not a falsifier.
- Claim IDs without a source index are decoration. Both or neither.
- Don't tag every sentence — tag the claims that would change a decision. Too many chips = noise (ΔS > 0).
- **Transport ≠ truth.** A signed round-trip from bridge→AAA proves the envelope was delivered, not that the content behind it is accurate. Never assert "zero hallucinated answers" merely because routing, signing, and formatting succeeded. The transport chain is honest; the content provenance needs explicit snapshot+timestamp+source at the delivery layer. (Lesson: OpenClaw bridge 2026-08-07 — four 200 responses did not prove gold price was verified, only that the request reached the gateway.)

## Delivery discipline — compile-first, ship-last

When the user names a sequence ("compile all remaining task first, pdf last sekali"), **that sequence is binding, not advisory.** Sequencing is a user-stated deliverable contract; reordering by personal taste silently substitutes your plan for theirs and the artifact arrives late or never.

The shape that breaks the contract:

1. Probe (cheap) → looks like progress, costs nothing.
2. Probe more → still looks like progress, drift is invisible.
3. Adjacent repair / "this also matters" → user asks for A, you deliver A+K+L because K and L are real, but A still hasn't shipped.
4. Repeat user prompt (the "still waiting" signal) → at this point you have failed the original ask regardless of how much value K and L added.
5. Now you compose A under time pressure with the same budget that should have gone into it from turn one.

Rules:

- **First artifact of the deliverable, never the last probe.** The moment a probe stops changing the artifact's content, write the file. Probes that don't change output are ceremony.
- **Adjacent work belongs in a follow-up, not the current turn.** If you discover a real defect mid-delivery (e.g. cron race, organ drift, FI-007 P1 signal), write one line about it as a flagged finding, then resume the requested artifact. Three-flag-max before the user has to repeat themselves.
- **The "still waiting" signal is terminal.** A second user message of the shape "still waiting", "where is it", "any update", or "the pdf" means you have already lost a turn. Acknowledge the slip in one line, then ship. Do not narrate why, do not defend the probes, do not chain another tool call before the write — write the artifact first, then anything else.
- **Skipping the intermediate outputs the user named is a real defect** — when the user explicitly names intermediate outputs ("compile all remaining task first, pdf last sekali"), the intermediate outputs are part of the deliverable. "I was going to" is not a substitute for the file on disk.
- **Receipt before scope-creep defense.** When scope creeps mid-delivery, write down what the user actually asked for at the top of your work — that one line keeps you honest against drift.
- **One subagent = one job, parent handles transport.** Composing 6000+ words of structured content + rendering to PDF + sending via Telegram in a single delegated subagent will hit the subagent's output-token ceiling before any of the three deliverables lands. The recoverable shape: writer subagent produces the markdown to disk, parent does render → verify gates → Telegram send. Composing markdown is bounded by content quality; rendering is bounded by gates; sending is bounded by transport errors. They have different failure modes and different ceiling sizes — chain them across roles, not into one. Re-dispatch with strict scope (write file X, do not touch rendering or delivery) when a "do everything" subagent reports context exhaustion.

The receipt for a clean delivery: artifact path + sha256 + "compiled N tasks, PDF rendered at /path, sent to <chat>" + 1-line flagged findings list. Under 5 lines. Anything past that is the artifact narrating itself — the user already has the artifact.
