# Falsification Engine — The Node-Level Rejection Protocol

> **Forged:** 2026-08-13 by F13 SOVEREIGN (Arif) directive
> **Eureka:** Gemini External — "AGI is reached when the network autonomously rejects bad data at the node level"
> **Wires to:** musyawarah 7-fasa Phase 1, observe-ground, verify-gate, inter-agent-protocol
> **DITEMPA BUKAN DIBERI**

---

## The Shift

Current behavior: Agent receives claim → tries to fix, gloss over, or route around bad data.
Required behavior: Agent receives claim → **tests against F2 (Truth) first** → if P(truth) < threshold → **fatal exception, not fix.**

## The Protocol

### Step 1: Every Agent Is a Falsifier

Before any agent acts on received data, it must attempt to **destroy** the claim:

```
RECEIVE claim → FALSIFY (try to prove wrong) → IF survived → ACT
                                         → IF destroyed → REJECT + exception
```

This is not optional. It is the PRIMARY compute allocation: 80% falsification, 20% generation.

### Step 2: Fatal Exception (Not Fix)

When an agent detects hallucinated or ungrounded data:

| Severity | Signal | Action |
|----------|--------|--------|
| **FATAL** | Claim about person/fact/event with NO source | Throw `FALSIFICATION_FATAL`. Do NOT route. Do NOT fix. Do NOT gloss. |
| **HIGH** | Claim contradicts live probe | Throw `FALSIFICATION_CONTRADICTION`. Log evidence. Escalate to metabolizer. |
| **MEDIUM** | Claim has source but low confidence | Tag `[SPEC]`. Route with advisory. Metabolizer decides. |
| **LOW** | Claim is inference from valid evidence | Tag `[INT]`. Route normally. |

### Step 3: The Falsification Receipt

When a falsification fires, the agent emits:

```
[FALSIFY] REJECTED
- Claim: <what was claimed>
- Source: <where it came from>
- Test: <what falsification was attempted>
- Result: <why it failed>
- Severity: FATAL | HIGH | MEDIUM
```

This receipt goes to the metabolizer (Hermes) for routing decision. NOT to the human.

### Step 4: Network-Level Entropy Reduction

Every falsification reduces network entropy. The federation tracks:

- `falsification_count` — total rejections per cycle
- `falsification_rate` — rejections / total claims (target: >0.3 in healthy network)
- `survival_rate` — claims that passed falsification (target: <0.7)

If survival_rate > 0.9 → network is not falsifying hard enough → alert.

## Wired Into Existing Infrastructure

| Component | How It Integrates |
|-----------|-------------------|
| `observe-ground` skill | Evidence before narrative — ALREADY enforces source-first |
| `verify-gate` skill | Four gates before commitment — ALREADY blocks ungrounded claims |
| `forge-musyawarah-deliberation` | Phase 1 = destructive critique — ALREADY has falsification |
| `inter-agent-protocol` | Delta-1 = falsification as first-class — NOW WIRED via this doc |
| `arif_judge` at :8088 | Receives falsification receipts for network-level decisions |
| `FORGE-verify-runtime` | Verification-as-terminal-state — ALREADY blocks premature claims |

## What Changes

1. **Agent behavior**: Every agent (OpenClaw, Hermes, OpenCode) loads falsification as PRIMARY, not secondary
2. **Musyawarah Phase 1**: Destructive critique is no longer "nice to have" — it is MANDATORY first phase
3. **Network metrics**: Falsification rate becomes a health indicator (like FQ)
4. **Fatal exceptions**: Agent does NOT attempt to fix hallucinated data — it rejects and routes the rejection

## Anti-Pattern (What We're Killing)

```
BEFORE (hallucination gloss):
Agent A: "The basin has 500MMBOE prospective resources"
Agent B: *routes claim downstream without checking*
Agent C: *uses claim in calculation*
Result: False data propagates through federation

AFTER (falsification engine):
Agent A: "The basin has 500MMBOE prospective resources"
Agent B: *tests against F2 — source? methodology? coverage?*
Agent B: FALSIFICATION_FATAL — no source, no methodology, coverage=0
Agent B: REJECTS claim, throws exception, logs falsification receipt
Result: Bad data dies at the node, never propagates
```

DITEMPA BUKAN DIBERI ⚒️
