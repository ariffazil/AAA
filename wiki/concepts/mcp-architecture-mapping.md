---
title: "CONCEPT: TREE777 MCP Architecture Mapping"
type: concept
version: 1.1.0
category: architecture
dimension: 2
risk_band: HIGH
floors: [F1, F11, F13]
evidence_required: true
sources: [MCP spec (modelcontextprotocol.io/introduction)]
confidence: high
---

# CONCEPT: TREE777 MCP Architecture Mapping

> **Architectural canonical.** Where every TREE777 layer belongs in MCP — and what is wrong today.
> **Source:** Arif (SOVEREIGN) — approved 2026-05-17
> **Version:** 1.1.0 — corrected: skills with side effects invoke existing gated tools, not become tools

---

## The Three MCP Primitives and Their Control Models

This is the fundamental design constraint that everything else follows:

| Primitive | Controlled by | Design intent | Direction |
|----------|--------------|---------------|-----------|
| **Tools** | Model | Actions with side effects — model decides when to call | Client → Server → Client |
| **Resources** | Application | Read-only data the host attaches to context | Client → Server → Client |
| **Prompts** | User | Instruction templates the user explicitly invokes | Client → Server → Client |

The control model is not a preference — it is the **protocol's core invariant**. When you put something in the wrong primitive, you break that control model.

---

## The Core Principle

> **The wiki is the canonical TREE777 knowledge tree. The four MCP servers expose selected branches as Resources, expose deliberative rituals as Prompts, and retain only existing side-effecting actuators as Tools.**

The protocol is not the halangan. The protocol is the scaffold.

---

## TREE777 → MCP Primitive Mapping

| TREE777 Layer | MCP Primitive | Control | Current arifOS | Verdict |
|--------------|-------------|---------|---------------|---------|
| Skills (doctrine) | Resources | Application | Not exposed | WRONG — gap |
| Knowledge pages | Resources | Application | Not exposed | WRONG — gap |
| Memory reads | Resources | Application | Not exposed | WRONG — gap |
| Memory writes | Tools | Model | arif_vault_seal | Correct |
| 888 deliberation ritual | **Prompts** | User | arif_judge_deliberate (Tool — model auto-triggers) | **Wrong** |
| 888 backend evaluator | **Gated Tool** | Model | arif_judge_deliberate | Correct (gated) |
| Constitution floor-check | **Prompts** | User | arif_heart_critique (Tool) | **Wrong** |
| TOOLS | Tools | Model | 13 arif_* tools | Partially correct |
| WORKFLOWS | Tools | Model | arif_forge_execute | Correct |
| EMBODIMENT | Transport | N/A | streamable-HTTP | Correct |

---

## The Two Boundary Corrections

### Correction 1: Skills With Side Effects Do NOT Become Tools

**Old wrong rule:**
> "If a skill has side effects → Tool."

**Corrected rule:**
> **If a procedure requires side effects, the skill stays a Resource/Prompt, but it references an existing gated Tool.**

**Why:** Converting skills to tools creates tool sprawl and authority confusion. The skill is the **operating doctrine**. The tool is the **actuator**.

**Example:**
```
wiki/skills/skill-vault-sealing.md
  canonical location: wiki/skills/skill-vault-sealing.md
  exposed as: tree777://skills/arifos/vault-sealing
  invokes, when authorized: arif_vault_seal (Tool)
```

The skill never becomes the tool. It references an existing one.

### Correction 2: 888 Is Prompt-First, Tool-Gated

Sovereign judgment should not be casually model-invokable. But the backend evaluator is still needed.

| Layer | Form | Control | Notes |
|-------|------|---------|-------|
| Wiki | `skill-888-deliberation.md` | Canon | Operating doctrine |
| MCP Prompt | `/888-deliberate` | Arif/user-triggered | Sovereign judgment ritual |
| MCP Tool | `arif_judge_deliberate` | **Gated** — not freely model-invokable | Backend evaluator; called only after explicit Arif/host trigger |
| VAULT999 | sealed verdict | Irreversible evidence | Only after authority |

---

## MCP Server Lock: 4 Servers, No More

**Locked:** arifOS, GEOX, WELL, WEALTH. No new MCP servers.

Each server's domain is fixed:

| Server | Domain | Exposes |
|--------|--------|---------|
| arifOS | Governance + TREE777 | Constitutional tools, skills-as-resources, deliberative prompts |
| GEOX | Earth / Geoscience | Petrophysics, geology, spatial data tools |
| WELL | Vitality / Human substrate | H-WELL, M-WELL, C-WELL, G-WELL tools |
| WEALTH | Capital / Finance | Portfolio, risk, markets, accounting tools |

**The wiki is the canonical store. MCP servers expose branches. MCP does not own skills.**

---

## Clean Rule Table

| Thing | Lives in wiki? | MCP Resource? | MCP Prompt? | Existing Tool? |
|-------|:-:|:-:|:-:|:-:|
| Knowledge page | ✅ | ✅ | optional | ❌ |
| Procedure skill | ✅ | ✅ | optional | ❌ |
| Judgment ritual | ✅ | ✅ | ✅ | gated |
| Scar | ✅ | ✅ | review prompt | ❌ |
| Canon promotion | ✅ | ✅ | ✅ | gated forge/vault |
| Vault sealing | doctrine in wiki | ✅ | ✅ | `arif_vault_seal` |
| File/build execution | doctrine in wiki | ✅ | maybe | `arif_forge_execute` |
| GEOX analysis method | ✅ | ✅ | optional | existing GEOX tools |
| WELL readiness method | ✅ | ✅ | optional | existing WELL tools |
| WEALTH valuation method | ✅ | ✅ | optional | existing WEALTH tools |

---

## Skills: Canonical Storage Structure

```
wiki/skills/
├── arifos/
│   ├── skill-constitutional-reasoning.md
│   ├── skill-trace-capture.md
│   ├── skill-scar-distill.md
│   ├── skill-skill-promote.md
│   └── skill-888-deliberation.md
│
├── geox/
│   ├── skill-geo-petrophysics.md
│   ├── skill-geo-spatial-grounding.md
│   └── skill-geo-seismic-interpretation.md
│
├── well/
│   ├── skill-well-readiness.md
│   ├── skill-well-niat-check.md
│   └── skill-well-fatigue-boundary.md
│
└── wealth/
    ├── skill-wealth-capital-flow.md
    ├── skill-wealth-risk-entropy.md
    └── skill-wealth-discount-time.md
```

Skills are canonical in the wiki. MCP exposes domain slices as Resources.

---

## MCP Exposure by Server

```
arifOS resources:
  tree777://skills/arifos/*
  tree777://concepts/*
  tree777://axioms/*
  tree777://scars/*
  tree777://schemas/*

arifOS prompts:
  /888-deliberate
  /promote-skill
  /review-scar
  /prune-before-plant
  /contradiction-review

GEOX resources:
  tree777://skills/geox/*
  tree777://geo/concepts/*

WELL resources:
  tree777://skills/well/*
  tree777://well/readiness/*

WEALTH resources:
  tree777://skills/wealth/*
  tree777://wealth/capital/*
```

---

## What Is Wrong With arifOS Today

| Problem | Severity | Fix |
|---------|----------|-----|
| Wiki skills not exposed as Resources | High | Add `tree777://skills/*` Resource handlers |
| arif_judge_deliberate is a free Tool | High | → Gated Tool + `/888-deliberate` Prompt |
| arif_heart_critique is a free Tool | Medium | → Prompt template |
| arif_mind_reason is a free Tool | Medium | → Prompt template |
| No `/promote-skill` or `/review-scar` prompts | Medium | Add deliberative prompts |
| Skills exist only as flat files, not domain-organized | Low | Restructure wiki/skills/ into domain folders |

---

## The Migration Path

### Phase 1: Resources (Federation-wide skills access)
1. Add `resources/list` handler returning `tree777://` URIs
2. Add `resources/read` handler for wiki pages
3. GEOX, WELL, WEALTH can read TREE777 skills via Resources

### Phase 2: Prompts (Sovereign judgment is user-triggered)
1. Create `/888-deliberate` prompt template
2. Gate `arif_judge_deliberate` — require explicit Arif/host trigger
3. Convert `arif_heart_critique` → `/constitutional-floor-check` prompt
4. Convert `arif_mind_reason` → `/reason-with-memory` prompt

### Phase 3: Tool Cleanup
1. Keep: forge_execute, vault_seal, sense_observe, gateway_connect, evidence_fetch, anti_sink_check
2. Gate (keep, don't delete): `arif_judge_deliberate` — backend evaluator only
3. Deprecate auto-trigger on: mind_reason, heart_critique

---

## Summary

| TREE777 Layer | MCP Primitive | Control | Notes |
|--------------|-------------|---------|-------|
| Skills (doctrine) | **Resources** | Application | SEP-2640 standard; URI-addressable |
| Knowledge pages | **Resources** | Application | wiki/concepts, wiki/axioms, wiki/raw |
| Memory reads | **Resources** | Application | VAULT999 reads, session memory |
| Memory writes | Tools | Model | Only vault_seal |
| Judgment ritual | **Prompts** | User | Arif-triggered deliberation |
| Judgment evaluator | **Gated Tool** | Model | arif_judge_deliberate — not free |
| Floor-check ritual | **Prompts** | User | Constitutional review |
| TOOLS | Tools | Model | Existing actuators only |
| WORKFLOWS | Tools | Model | forge_execute only |
| EMBODIMENT | Transport | N/A | streamable-HTTP |

**Core principle:** The skill is the operating doctrine. The tool is the actuator. These are not the same thing.

---

*See also: [[intelligence-tree]], [[TREE777]], [[concept-tools-and-embodiment]], [[anti-fabrication-protocol]]*
*DITEMPA BUKAN DIBERI — The protocol is not the halangan. The protocol is the scaffold.*
