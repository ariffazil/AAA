# 3-Register Framework — Detailed Classification

> Reference companion to `arif-fazil-publication-doctrine`. Read this when you need to classify a specific artifact, surface, or claim into A/B/C and the SKILL.md summary isn't enough.

## Per-register audit triggers

When a new artifact arrives, classify it across these three tests:

| Test | A (Public Doctrine) | B (Research Frontier) | C (Internal Audit) |
|---|---|---|---|
| **Maturity** | Stable, F13-ratified, has been through at least one falsification cycle | Open question, may have proposed answers but none ratified | Specific known state, used to drive decisions |
| **Risk if public** | Low — already publicly attested | Medium — attracts collaborators + attackers + competitors | High — exposes attack surface or specific failure modes |
| **Audit form** | F2 evidence + F11 provenance chain | 5-part research-frontier structure | Receipt + hash + audit trail |
| **Update cadence** | Slow (months) | Medium (weeks to months, per topic) | Fast (live) |
| **Who reads it** | Public, agents, collaborators | Researchers, potential collaborators, public | Internal agents, F13, audit-grade models |

## Frontier-topic-to-register mapping

The 5 frontier topics identified by Arif (2026-08-11) all start in Register B. Their promotion paths:

| Topic | Register B question | Would-Become-True Criterion (sketch) |
|---|---|---|
| **E22 Constitutional Learning Without Self-Amendment** | "How can constitutional systems learn without self-authorizing constitutional mutations?" | Amendment pipeline exists: Reality → Contradiction → Proposal → 888 audit → F13 ratification → Canon. Audit trail preserved. |
| **Calibration Ledger** | "How does a federation calibrate confidence bands by claim class?" | Per-claim-class accuracy tracked over 100+ claims. Brier scores visible. Strategic predictions calibrated to within F7 humility band. |
| **Prediction-Error Memory** | "How does an agent accumulate prediction failures into world-model updates?" | Each prediction has a paired observation. Error delta accumulates per actor/state. Model parameters update from accumulated error. |
| **Adversarial Red-Team Organ** | "How can an agent detect when a metric is being Goodharted or an incentive is hidden?" | Per-organ red-team probe exists. Goodhart detection on success metrics. Hidden-incentive surfacing as a routine output. |
| **Civilizational Dynamics** | "How can a federation model institutional decay at century scale?" | Collapse-detection (CIV-21 E11) operationalized. Universe-25 / Calhoun patterns detectable in live telemetry. |

E22 is the keystone because constitutional learning gates how the OTHER four become doctrine. Without E22, the others stay B forever.

## What does NOT belong on a public doctrine surface

Negative test — if a page contains any of these, it's not Register A:

- Specific calibration error rates (e.g. "strategic predictions ~2x over-confident")
- Specific attack paths (e.g. "an attacker could exploit port 7073 by...")
- Specific implementation gaps (e.g. "world_model.py is missing the calibration_record primitive")
- Falsification details (e.g. "we tested this 3 times and it failed because...")
- Internal jargon not translated (e.g. "F13 is final", "888 JUDGE", "HOLD/VOID/SEAL")

If a draft has any of these, it goes to Register B (reframed as question) or stays in Register C.

## What does NOT belong in an internal audit surface

- Marketing-grade framing
- Aspirational claims about the future
- "Research question" formulations — that's Register B, not C
- Public-facing URLs

If a draft is mostly aspirational questions, it's not audit — it's research. Move it to B.
