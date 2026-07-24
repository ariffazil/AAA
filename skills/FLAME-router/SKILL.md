---
id: FLAME-router
name: FLAME-router
version: "2026.07.24"
description: >
  Classify inference work into the stateless FLAME tool lane or the governed
  constitutional agent lane, with Arif-ratified division of labor (2026-07-24).
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope:
  - F2
  - F4
  - F9
  - F13
---
# 🔥 FLAME-router — Tool Lane vs Agent Lane Routing

> **Skill ID:** FLAME-router · **Version:** 2026.07.24 · **Axis:** routing
> **Ratified:** 2026-07-24 by Arif (F13 SOVEREIGN)
> **Load when:** Any agent needs to decide between FLAME (tool lane) and constitutional cascade (agent lane).
> **Do NOT load for:** Constitutional judgment, SEAL/HOLD decisions, human-facing responses.

## The Clean Division of Labor (Arif-ratified 2026-07-24)

| Layer | Role | Model Tier |
|---|---|---|
| **FLAME** | Tools, workers, fallback throughput | Free/cheap, tiered by availability, disposable |
| **Hermes** | Epistemic/human-life reasoning | Premium, high-effort, reasoning-preserved |
| **OpenCode** | Execution/coding actuation | Budget-to-premium depending on task complexity |
| **arifOS** | Judgment, audit, sealing | Policy logic — not a model tier at all |

## What FLAME Answers

```
"Can something respond right now, cheaply, without breaking rate limits?"
```

FLAME **never** answers: "Is this answer true or authorized?"

## The Two-Lane Rule

```
TOOL LANE (FLAME):     Tools, workers, batch jobs, classifiers, embedders.
                       Cascading availability ladder — 12 tiers.
                       RM0. Hit-rate adaptive. ADVISORY output only.
                       Zero constitutional authority.

AGENT LANE (cascade):  Agents, reasoning, judgment, governance.
                       TokenRouter→MiniMax→MiMo→Groq→Gemini→Cerebras→SEA-LION→Ollama→HOLD.
                       F1-F13 gated. Constitutional.
```

## FLAME Tier Structure (2026-07-24)

Tiers are a cascading **availability ladder**, not a reasoning hierarchy. Higher tiers are more trusted/available — not "smarter." The chain exists so *something* always responds.

```
T1-T5:  Core — Groq (2 tiers) + SEA-LION (3 tiers) = fastest + BM-native
T6-T7:  Core — Gemini flash + Cerebras gemma = general + volume
T8-T10: Experimental — gpt-oss-120b variants (low-weight)
T11:    OpenRouter :free — gap-fill bridge (Cohere, InclusionAI, Poolside, NVIDIA)
T12:    Ollama qwen2.5-coder:3b — local survival knife
```

## Decision Matrix

| Task | Lane | Why |
|---|---|---|
| Summarize a log file | **FLAME** | No judgment needed |
| Classify 1000 documents | **FLAME** | Pure throughput |
| Generate embeddings | **FLAME** | Stateless transform |
| Non-binding fact check | **FLAME** | Advisory only |
| Plan safety review | **FLAME** | Advisory only |
| Geoscience evidence synthesis (non-seal) | **FLAME** | Compute, not judgment |
| Market signal interpretation | **FLAME** | Interpretation, never allocates |
| Reason about architecture | **Agent** | Needs constitutional grounding |
| Judge a constitutional question | **Agent** | arifOS 666_JUDGE domain |
| Respond to Arif | **Agent** | Human-facing, governed |
| Execute a forge mutation | **Agent** | Lease + judge required |
| Epistemic/human-life reasoning | **Agent** | Hermes premium reasoning domain |
| Seal to VAULT999 | **Agent** | arifOS 999_SEAL domain |

## Task-Class Chains (reorder tiers by task type)

```bash
flame --task-class coding "Write a function to..."
flame --task-class bm_malay "Terangkan maksud..."  
flame --task-class gap_fill "Query needing unique free model"
```

| Task Class | Preferred Tiers | Why |
|---|---|---|
| `coding` | Groq 70B → OR → Cerebras | Deep reasoning first |
| `epistemic` | Groq 70B → Gemini | Reasoning + context |
| `bm_malay` | SEA-LION Qwen → SEA-LION Llama | BM-native priority |
| `classification` | Groq 8B → Gemini Lite | Fast, cheap |
| `summarization` | Groq 8B → Gemini | Speed + accuracy |
| `gap_fill` | OpenRouter only | Models FLAME can't reach directly |
| `destructive` | **NEVER FLAME** | Governed cascade only |

## Constitutional Boundary

**FLAME NEVER:**
- Judges (arifOS only — `GOVERNED_USE["constitutional_judgment"]`)
- Seals (VAULT999 only — `GOVERNED_USE["constitutional_seal"]`)
- Primary epistemic reasoning (Hermes domain)
- Human-life/substrate reasoning (WELL domain)
- Sovereign data (PII, myKad, PETRONAS — SENSITIVITY hard gate)
- Execution authorization (A-FORGE lease domain)
- Uses paid models (RM0 hard gate)
- Uses OpenRouter auto/auto-beta router (F11 AUDITABILITY violation)
- Routes agent work (use agent cascade)

**FLAME ONLY:**
- Advisory, classification, extraction, summarization, embedding
- Stateless text → transform → output
- ADVISORY authority — consumers MUST validate
- Emergency fallback when governed cascade exhausted

## FLAME Commands

```bash
free-llm "prompt"                          # Single inference
free-llm --mode probe                      # Health check all 12 tiers
free-llm --mode stats                      # Hit-rate dashboard
free-llm --mode snapshot-checksum          # Integrity hash
free-llm --batch file.txt                  # Batch processing
free-llm --task-class coding "prompt"      # Task-class chain reorder
free-llm --sensitivity PUBLIC "prompt"     # Declare data sensitivity
free-llm --caller hermes_fact_check "..."  # Caller identity for audit
```

## ATLAS333 Context

FLAME activates 8 ATLAS333 paradoxes (Memory: M6,M7,M8 · Mind: R1,R4,R7 · Contour: C1,C2). Key tensions: speed vs. quality (R1), stability vs. reordering (M6), free access vs. constitutional boundary (C1).

## When FLAME returns HOLD

1. Try agent lane cascade (may have different model availability)
2. Check FLAME health: `free-llm --mode probe`
3. Check hit-rates: `free-llm --mode stats`
4. If all tiers exhausted: escalate to agent lane with degraded flag
