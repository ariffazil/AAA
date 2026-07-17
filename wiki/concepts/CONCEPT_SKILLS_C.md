---
title: "Skills vs Workflows vs Knowledge — Operational Definitions"
created: 2026-05-17
updated: 2026-05-17
type: concept
tags: [skills, workflows, knowledge, operational-definition, AAA, arifOS]
sources: [
  "arifOS/arifosmcp/providers/meta_skills.py",
  "arifOS/arifosmcp/providers/skills.py",
  "research/EMBODIMENT_SKILLS_KNOWLEDGE_DEEP_RESEARCH.md"
]
confidence: high
---

# Skills vs Workflows vs Knowledge

> **Part of:** [[intelligence-tree]] — Skills layer + Knowledge layer + Workflows layer
> **Extends:** [[agent-skills-architecture]]

---

## The Core Distinction

| Term | Definition | arifOS Form | Example |
|------|-----------|-------------|---------|
| **SKILL** | Behavioral capacity — "I can do X" | Pre-tool-call gate + void conditions | `epistemic-integrity` meta-skill |
| **WORKFLOW** | Multi-step procedure with state | Directed graph of steps | Hermes pagi brief pipeline |
| **KNOWLEDGE** | Validated, entropy-reducing truth | Sealed verdicts, zkPC receipts | VAULT999 SEAL entries |

---

## Skill = Behavioral Capacity

**"I can do X" — capability assertion with preconditions.**

A skill encodes when and how to use tools safely. It does NOT create new capabilities — it arranges existing tools into a repeatable pattern.

**In arifOS:** Two layers:

### Domain Skills (`SkillsDirectoryProvider`)
From `skills/geox/`, `skills/wealth/`, `skills/well/`. Callable Python functions, NOT MCP tools.

```python
# invoke("geox", "seismic.analysis", data) — called inside arif_mind_reason
class SkillsDirectoryProvider:
    def get(self, domain: str, name: str) -> Callable[..., Any] | None:
        return self._skills.get(domain, {}).get(name)
```

### Meta-Skills (`MetaSkillsProvider`)
5 canonical pre-invocation hooks:

| Meta-Skill | Fires When | Void Conditions |
|------------|-----------|----------------|
| `RSI-recursive-improvement` | AGI→ASI transition | Self-model divergence >5%, circular dependency |
| `orthogonal-abstraction` | Cross-domain reasoning | Surface similarity without structural invariant |
| `epistemic-integrity` | Consequential output | Hallucination, overconfidence, missing uncertainty band |
| `constitutional-governance` | All tool invocations | Self-authorization, floor breach, irreversible without verdict |
| `entropy-optimization` | Resource allocation | Action without EVOI calculation |

**Rule of thumb:** If you keep re-typing steps → it's a Skill.

---

## Workflow = Multi-Step Procedure

**"Do X then Y then Z, remembering state between steps."**

A workflow chains multiple skills and/or tools, handles branching, errors, and state persistence. A workflow invokes skills; skills invoke tools.

**In arifOS:** `.antigravity/workflows/` contains macro-level task templates:
- `start_feature_branch.md` — Git branching workflow
- `precommit_sentinel.md` — Pre-commit constitutional check
- `sync_with_main.md` — Branch synchronization

**Example — Hermes Pagi Brief Workflow:**
```
1. SENSE (arif_sense_observe) → scan news sources
2. REASON (arif_mind_reason) → apply World Model primer, filter for relevance
3. CRITIQUE (arif_heart_critique) → F5 peace check, F9 anti-hallucination
4. COMPOSE (arif_reply_compose) → Bahasa Melayu executive brief
5. DELIVER (arif_gateway_connect) → send to Telegram DM
6. SEAL (arif_vault_seal) → log to VAULT999 outcomes
```

**Rule of thumb:** If you keep doing the same multi-stage pipeline → it's a Workflow.

---

## Knowledge = Validated Truth

**"What I know to be true" — compressed representation that reduces uncertainty.**

Knowledge is the output of reasoning that has been sealed. It is entropy-reducing (F4: ΔS ≤ 0).

**In arifOS:** VAULT999 sealed verdicts:

```json
{
  "verdict": "SEAL",
  "knowing": {
    "P_truth": 0.96,
    "ΔS": -1.8,
    "TW": 0.97,
    "evidence": [...]
  },
  "not_knowing": {
    "Ω₀": 0.04,
    "acknowledged_limits": [...]
  },
  "zkpc_proof": "zero_knowledge_proof_all_checks_executed",
  "arif_signature": "ed25519_signature_888_judge"
}
```

**Rule of thumb:** If you keep re-typing background context → it's Knowledge.

---

## How They Connect

```
KNOWLEDGE (what is)
    ↓ (compressed from memory)
SKILL (how to act)
    ↓ (chained sequences)
WORKFLOW (orchestrated chains)
    ↓ (calls)
TOOLS (atomic capabilities)
    ↓ (produces)
NEW MEMORY (what happened)
    ↓ (loop back)
```

Skills consume Knowledge (void conditions, pre-checks are built on validated facts).
Workflows invoke Skills (multi-step orchestration uses skill procedures).
Tools implement Skills (the actual execution is a tool call).

---

## The Stability/Governance Rule

**No upgrade from Scar to Skill without explicit 888 decision.**

- A scar is a single incident record (memory)
- A skill is a repeatable policy (knowledge crystallized)
- Not every scar produces a skill — only deliberate constitutional judgment

This prevents:
- Skill inflation (every event becomes a skill → brittle, over-constrained)
- Skill drought (no skills update → system ignores evidence)

---

## In AAA Wiki

```
AAA/wiki/
├── concepts/         → KNOWLEDGE (governance patterns, definitions)
├── skills/           → SKILLS (reusable procedures, canonical spec)
├── workflows/        → WORKFLOWS (orchestrated chains) [pending]
├── raw/              → KNOWLEDGE (immutable source evidence)
├── scar-*.md        → MEMORY (failure incidents)
└── LOG_MD.md           → MEMORY (append-only action history)
```

---

## Quick Reference

| If you keep... | It's a... | AAA location |
|----------------|-----------|-------------|
| Re-typing steps for a task | **Skill** | `wiki/skills/` |
| Re-typing background context | **Knowledge** | `wiki/concepts/` |
| Doing the same multi-stage pipeline | **Workflow** | `wiki/workflows/` (pending) |
| Recording what happened | **Memory** | `wiki/scar-*/`, `LOG_MD.md`, `VAULT999` |

---

## Related Pages

- [[intelligence-tree]] — 7-layer tree (skills + knowledge + workflows layers)
- [[concept-tools-and-embodiment]] — tools, embodiment, bridge mechanism
- [[concept-memory-knowledge-loop]] — stability/permeability paradox
- [[agent-skills-architecture]] — cross-platform skills landscape

---

*Source: `/root/arifOS/arifosmcp/providers/meta_skills.py` + `/root/arifOS/arifosmcp/providers/skills.py`*
*DITEMPA BUKAN DIBERI — Skills are forged from scars, not given by fiat.*