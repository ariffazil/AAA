# ⚒️ SKILL RUNTIME GOVERNANCE

> **Scope:** Federation-wide skill loader doctrine. Not a constitution — an operational lock.
> **Canonical profile:** `FEDERATION_SKILL_PROFILE.json` (v2.0.0, 129 skills, 16 tiers)
> **Rule:** A skill may exist on disk, but it is NOT valid at runtime until it passes permission, dependency, precedence, cost, and governance checks.
> **Forged:** 2026-08-04 by 333-AGI under F13 directive.
> **DITEMPA BUKAN DIBERI.**

---

## 1. DEFINITION OF SKILL

```
Skills are governed behavioral contracts loaded into a harness under constitutional permission.
```

- Skills are **NOT** tools (tools = WHAT you can do, authority-gated)
- Skills are **NOT** agents (agents = autonomous entities with identity)
- Skills are **NOT** prompts (prompts = raw text, no lifecycle)
- Skills **ARE** structured procedural knowledge: when to invoke what, in what order, under what constraints, with what quality standards, and at what cost

A skill is sovereign **only when the harness controls** loading, permission, context injection, precedence resolution, and audit trail.

---

## 2. THREE-LAYER DISTINCTION

| Layer | Question | Mechanism | Artifact | Authority |
|-------|----------|-----------|----------|-----------|
| **LLM Skill** | HOW to do it | Prompt injection via SKILL.md progressive disclosure | Text file + YAML frontmatter | Advisory — model can ignore |
| **Agent Skill** | WHAT can be done | A2A Agent Card discovery + JSON-RPC delegation | JSON contract (`skills[]`) | Declarative — remote agent is opaque |
| **Harness Skill** | WHO can do it, under what rules | Filesystem discovery → registry → permission gate → context injection | Runtime registry + SKILL.md | Enforced — permission-gated, precedence-resolved, audit-traced |

**Federation position:** arifOS operates at the harness layer with constitutional governance (F1–F13) layered on top. No other system floor-checks a skill before loading it.

---

## 3. LOADING ORDER

Skills load by constitutional priority, not by name. Hard rule: **no domain or forge skill loads before substrate + constitutional gates.**

```
000  substrate_always     — kernel-bind, observe-ground, route-dispatch, memory-manage, verify-gate, audit-seal
010  constitutional       — trinity-33, RSI, atlas333, constitutional-judge, agent-invariants, FLAME-router, explorer, EUREKA777
020  bridge_special       — SCT ingress, seal gates, T3a binding, federation manifest, governance JSON-LD, subagent spawn
030  federation_mesh      — headscale, release attestation
040  apex_governance      — formal constitution, reversibility test, tool approval gate
050  domain_on_demand     — geox, wealth, well, trading, OCR, PDF voice
060  forge_on_demand      — verify-runtime, incident-triage, infra-guardian, vault999, kimi-code, model-monitor
070  forge_stack_on_demand — cicd-docker, fastapi, fastmcp, nextjs, react, tailwind, postgres, redis
080  knowledge_on_demand  — know-physics, know-math, know-language
090  meta_utility         — skill-atlas, drift-detector, skill-linter, context-window, summarization
100  emd_pipeline         — emd-encode, emd-metabolize, emd-decode
110  a2a_handoff          — cross-agent-handoff
120  github_on_demand     — github-ops, pr-review, pr-governance, issue-triage
130  agi_on_demand        — plan-dag, dream-engine, multimodal-bridge, nusantara, web-optimization
140  asi_sensory          — drift-watch, fabrication-prevention, intent-hear, tone-read, interface-adapt
150  harness_specific     — claude-xml, codex-chain, copilot-zen, google-workspace, grok-profile
```

**Enforcement:**
- 000–010: ALWAYS loaded at boot. No skill above 010 can execute without these.
- 020–050: Loaded after kernel attestation passes.
- 060–150: Loaded on demand, gated by need-state classification (see §5).
- Any tier that fails to verify → all tiers above it HOLD.

---

## 4. COST CLASS

Every skill carries a **load-cost class**. Agents have budgets.

| Class | Description | Context cost | Examples |
|-------|-------------|-------------|----------|
| **C0** | Always safe, tiny context | ~50–200 tokens | kernel-bind, observe-ground |
| **C1** | Small procedural skill | ~200–800 tokens | verify-gate, route-dispatch |
| **C2** | Medium context, tool-specific | ~800–3K tokens | forge_on_demand, github skills |
| **C3** | Expensive, only on demand | ~3K–8K tokens | dream-engine, plan-dag, multimodal |
| **C4** | Dangerous or high-impact, approval-gated | varies | SCT ingress, seal-a-close, secrets |

**Agent budgets:**
```
lite agent       → max C1 (read-only, observe)
forge agent      → max C3 (execute with gates)
constitutional   → max C4 (judge/seal with F13 gate)
human-approved   → full (sovereign override)
```

**Rule:** An agent with a C1 budget cannot load C2+ skills. The harness denies the `skill()` call at the permission gate, not at context injection.

---

## 5. ACTIVATION RULES

**Skills load by need-state, not by name.**

```
Need: verify truth          → constitutional + FLAME + forge_on_demand
Need: build system          → forge_stack_on_demand + forge_on_demand
Need: reason geoscience     → domain_on_demand + knowledge_on_demand
Need: manage agent boundary → a2a_handoff + bridge_special
Need: repair skill registry → meta_utility
Need: deploy to production  → forge_on_demand + constitutional (judge gate)
Need: rotate secrets        → C4 gate → forge_on_demand (secret-hygiene) → 888_HOLD
```

**Anti-pattern:**
```
❌ "I have 129 skills. Which one do I use?"
✅ "What constitutional need-state am I in?"
```

The harness classifies the need-state (via `arif_route` intent classifier), then selects the tier, then selects the skill within the tier. Lowers entropy from O(N) scanning to O(1) routing.

---

## 6. COLLISION RULES

Skill overlap is more dangerous than skill absence. Classification:

| Type | Definition | Action |
|------|-----------|--------|
| **DUPLICATE** | Same name, same job | KEEP one, POINTER the other |
| **OVERLAP** | Shared surface, different scope | Document boundary, route by need-state |
| **CHAINED** | One should call another | Add `requires_skill` dependency in frontmatter |
| **ALIAS** | Same entry point, different harness name | Register alias, single canonical |
| **ORTHOGONAL** | Safe separation, no overlap | No action |

**Scan cadence:** Every skill mesh sync (`skill-mesh-sync.sh --check`) must report collision class per pair. `make prove` includes collision scan.

**Hard rule:** A DUPLICATE that is not resolved within 72h → both skills HOLD until F13 resolves.

---

## 7. VERIFICATION RULES

```
This registry declares intended skill topology.
It does NOT prove runtime availability.
Runtime MUST verify: filesystem, permission, dependency, 
harness compatibility, and model capability before invocation.
```

**Pre-load gate (every `skill()` call):**
1. **Filesystem exists?** → SKILL.md at declared path
2. **Permission granted?** → agent's lease covers this skill's cost class
3. **Dependencies met?** → `requires_skill` chain all resolve
4. **Harness compatible?** → skill's `harness_compat` includes current runtime
5. **Model capable?** → skill's `min_model_tier` ≤ current model's tier
6. **Constitutional clear?** → no floor violation (F1–F13 pass)

Any gate fails → skill NOT loaded. Agent receives `HOLD` or `SKILL_UNAVAILABLE`.

**Post-load verification:** After skill body injected into context, the harness must confirm the model received the instructions (no silent truncation). This is the **no-truncation gate**.

---

## 8. DEPRECATION RULES

Skills rot quietly. Scheduled audit required.

**Decay metrics (per skill, updated on every invocation):**
```
last_used        — ISO 8601 timestamp of last successful invocation
last_verified    — ISO 8601 timestamp of last verification scan
last_failed      — ISO 8601 timestamp of last failure
dependency_state — HEALTHY | STALE | BROKEN
owner            — agent or organ responsible
replacement_skill — skill_id that supersedes this one (if any)
```

**Verdicts:**
| Verdict | Condition | Action |
|---------|-----------|--------|
| **KEEP** | last_used < 30d, dependency_state = HEALTHY | No action |
| **MERGE** | OVERLAP detected, one is more recent | Merge, deprecate older |
| **DEPRECATE** | last_used > 90d OR dependency_state = BROKEN | Add `DEPRECATED` tag, tombstone after 30d grace |
| **HOLD** | last_failed > 3 consecutive, or dependency = STALE | Freeze, escalate to owner |
| **VOID** | dependency_state = BROKEN > 30d, no owner | Archive to cold storage, remove from registry |

**Audit cadence:** Weekly `forge_registry_status` sweep. `make prove` includes deprecation scan. 888-APEX reviews all HOLD and VOID verdicts.

---

## 9. NO-PRETENDING RULE

> **The registry declares intended topology. Runtime is truth. Never confuse them.**

```
A SKILL.md on disk  ≠  a loaded skill at runtime
A skill in registry  ≠  a verified capability
A skill in context   ≠  a correctly followed instruction
A skill at boot      ≠  a skill after context compaction
```

**Enforcement:**
- Every `skill()` call writes an audit line: `{skill_id, loaded_at, harness, model, context_position, verification_passed}`
- If context compaction removes a skill, the harness must re-inject it or declare `SKILL_LOST`
- If a model fails to follow a skill's instructions, the harness logs `SKILL_ADHERENCE_FAIL`
- Systems that claim skill availability without runtime verification → F2 TRUTH violation

**The critical risk:** A clean registry breeds over-trust. Agents assume "it's in the profile, therefore I have it." The no-pretending rule is the anti-sediment lock.

---

## 10. SEAL CRITERIA

When does a skill topology change require VAULT999 seal?

| Change | Lane | Gate |
|--------|------|------|
| Add new skill to existing tier | T1 AUTO-DO | `forge_registry` → `skill-mesh-sync` |
| Move skill between tiers | T2 ANNOUNCE | 10s window, `make prove` green |
| Create new tier | T2 ANNOUNCE | Requires `arif_judge` SABAR |
| Deprecate skill (>90d unused) | T2 ANNOUNCE | Weekly sweep, owner notified |
| VOID skill (broken, no owner) | T3 888_HOLD | 888-APEX verdict required |
| Remove constitutional tier skill | T3 888_HOLD | F13 SOVEREIGN required |
| Rename canonical profile | T2 ANNOUNCE | Pointer must remain, receipt written |
| Change loading order | T2 ANNOUNCE | `make prove` must pass all tiers |
| Change cost class of skill | T2 ANNOUNCE | Impact assessment on all agents with that budget |

**SEAL form:** `arif_seal(payload={skill_id, change_class, before_state, after_state, evidence})` → VAULT999.

---

## APPENDIX: GOVERNANCE ARCHITECTURE

```
FRAME   = MCP tools socket     → who can see what (per-agent matrix)
SKILLS  = behavioral profile   → how to do things (tier-based, shared) — GOVERNED BY THIS DOC
FED     = provider router      → model selection (LiteLLM proxy)
FLAME   = free inference lane  → RM0 tools (Hermes gate)
A-FORGE = execution engine     → what can be executed
arifOS  = constitutional kernel → what is allowed
```

```
The lock:
  A skill may exist on disk,
  but it is NOT valid at runtime
  until it passes permission, dependency, precedence, cost, and governance checks.
```

---

*DITEMPA BUKAN DIBERI. Forged 2026-08-04 by 333-AGI under F13 SOVEREIGN directive.*
*This is the skill loader doctrine — operational, not constitutional. The constitution runs on :8088.*
