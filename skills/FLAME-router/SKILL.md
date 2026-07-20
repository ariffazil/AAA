# 🔥 FLAME-router — Tool Lane vs Agent Lane Routing

> **Skill ID:** FLAME-router · **Version:** 1.0.0 · **Axis:** routing
> **Load when:** Any agent needs to decide between FLAME (tool lane) and constitutional cascade (agent lane).
> **Do NOT load for:** Constitutional judgment, SEAL/HOLD decisions, human-facing responses.

## The Two-Lane Rule

```
TOOL LANE (FLAME):     Workers, batch jobs, summarizers, classifiers, embedders.
                       RM0. Hit-rate adaptive. Zero constitutional authority.

AGENT LANE (cascade):  Agents, reasoning, judgment, governance.
                       TokenRouter→MiniMax→MiMo→Groq→Gemini→Cerebras→SEA-LION→Ollama→HOLD.
                       F1-F13 gated. Constitutional.
```

## Decision Matrix

| Task | Lane | Why |
|------|------|-----|
| Summarize a log file | **FLAME** | No judgment needed |
| Classify 1000 documents | **FLAME** | Pure throughput |
| Generate embeddings | **FLAME** | Stateless transform |
| Reason about architecture | **Agent** | Needs constitutional grounding |
| Judge a constitutional question | **Agent** | F1-F13 required |
| Respond to Arif | **Agent** | Human-facing, governed |
| Health-check free tier | **FLAME** | Observation only |
| Execute a forge mutation | **Agent** | Lease + judge required |

## FLAME Commands

```bash
free-llm "prompt"              # Single inference through free-loop
free-llm --mode probe          # Health check all 8 models
free-llm --mode stats          # Hit-rate dashboard
free-llm --mode seal           # Integrity seal
free-llm --batch file.txt      # Batch processing
```

## Constitutional Boundary

**FLAME NEVER:**
- Judges (arifOS only)
- Seals (VAULT999 only)
- Holds constitutional authority
- Touches paid models (RM0 hard gate)
- Routes agent work (use agent cascade)

**FLAME ONLY:**
- Text → transform → output
- System workers and tools
- Stateless, non-judicial inference

## ATLAS333 Context

FLAME activates 8 ATLAS333 paradoxes (Memory: M6,M7,M8 · Mind: R1,R4,R7 · Contour: C1,C2). Key tensions: speed vs. quality (R1), stability vs. reordering (M6), free access vs. constitutional boundary (C1). See `FLAME_ATLAS333_MAP.md`.

## When FLAME returns HOLD

1. Try agent lane cascade (may have different model availability)
2. Check FLAME health: `free-llm --mode probe`
3. Check hit-rates: `free-llm --mode stats`
4. If all tiers exhausted: escalate to agent lane with degraded flag
