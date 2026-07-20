---
type: Documentation
title: The 5 Layers + 6 Realities — Architectural Analysis
description: External analysis of the arifOS 33-skill Copilot architecture, identifying the 5-layer decision model and 6-reality coverage as the key architectural insight
tags: [architecture, analysis, layers, realities, decision-framework]
timestamp: 2026-07-20T08:00:00Z
links:
  - index.md
  - ../atlas333.md
  - ../federation-map.md
---
# The 5 Layers + 6 Realities

*This analysis was generated from an external evaluation of Arif's system architecture, then validated against the live federation.*

## The 5-Layer Decision Model

| Layer | Question | Organ | Failure Mode |
|-------|----------|-------|-------------|
| Memory | What is true about history? | VAULT999 | Context loss, repeating past mistakes |
| Earth | What is true about the Earth? | GEOX | Geological assumptions unchallenged |
| Capital | What is true about value? | WEALTH | Technical correctness ≠ economic viability |
| Human | What is true about the human? | WELL | Tired human makes bad decisions regardless of data |
| Operations | What is true about the work state? | AAA | Coordination failures, blocked workflows |

## The 6 Realities

Every major decision failure originates from one of these six domains:

1. **Evidence** — Claims must be grounded in observation (F2 TRUTH)
2. **Memory** — Context must survive across sessions (F1 AMANAH)
3. **Earth** — Physical reality cannot be assumed (GEOX)
4. **Economic** — Value constraints are real (WEALTH)
5. **Human** — Cognitive state affects decision quality (WELL)
6. **Operational** — Coordination must be explicit (AAA)

## What This Architecture Does That Normal Copilot Cannot

### 1. Build Continuity
Most AI sessions forget. This system explicitly preserves: What do we already know? What was already decided? Has this been done before? What remains unresolved?

### 2. Distinguish Facts from Assumptions
Evidence, interpretation, opinion, and speculation are separated by epistemic class (OBS/DER/INT/SPEC), not lumped together.

### 3. Cover the Major Sources of Decision Failure
Most organizations focus only on information or execution. This stack covers evidence, memory, earth reality, economic reality, human reality, and operational reality — six different realities.

## The Elevator Pitch

> "It acts like a disciplined chief-of-staff for knowledge work. It helps gather evidence, preserve institutional memory, understand subsurface uncertainty, evaluate trade-offs, monitor human readiness, coordinate work across tasks, and maintain decision traceability. Its purpose is not to make decisions for people. Its purpose is to help people make better decisions with less context loss and less avoidable error."
