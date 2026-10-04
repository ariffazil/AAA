---
id: audit-entity-classify
name: audit-entity-classify
version: 1.0.0
description: "Given a What is X? question about a federation entity (process, organ, doctrine, dataset, prompt, identity), produce a structural identification audit. Option-by-option evidence table, what X is NOT list, what X IS with one sentence, minimum irreducible function test, and exactly one classification. Use when the user asks what is X, is X an agent or a service, what does X actually do, should we keep X, is X constitutional, or any structural-identification question about a federation primitive, organ, role, identity, or doctrinal surface."
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F11]
tags: [audit, classification, identity, ontology, structural, federation, what-is, reduce-to-truth]
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
- hermes
- openclaw
- agy
dependencies:
  skills:
  - AUDIT-recursive-audit
  - AUDIT-skill-atlas
  - verify-nested-sibling-reports
  - federation-infra-verification
  servers: []
  tools:
  - sandbox_terminal
  - filesystem_read
examples:
- "What is AAA? - option A Cockpit / B Federation Fabric / C Constitutional Runtime / D Registry - classify with evidence"
- "What is FED? - option A Cost Router / B Traffic Router / C Agent Router / D Intelligence Router / E Federation Cognitive Allocator"
- "What is i-ARIF? - option A Agent / B Kernel / C Identity / D Authority / E Constitutional Envelope / F Federation Self-Model / G Human-Digital Twin / H Sovereign Context Object / I or something else"
- "What is APEX? Is it a theory of intelligence or a theory of governed intelligence?"
- "What is arifOS? Kernel, runtime, or protocol?"
- "What is A-FORGE? Process, service, or tool registry?"
tests:
- "Each option has at least 1 OBS evidence (file:line, process, value) AND at least 1 counter-evidence"
- "What X is NOT list excludes every option except the final classification"
- "Minimum irreducible function test: what breaks if X dies?"
- "Final classification is one word from the option list, defended in 1-2 sentences"
version_lock:
  schema_version: '1'
  artifact_hash: pending
---

# AUDIT-entity-classify — Structural Identification Audit

> Forged: 2026-08-08 by 333-AGI after the I-ARIF / FED / AAA / APEX audits
> SOT: wherever the entity lives in the federation (file:line, process, schema, doc)
> Doct: DITEMPA BUKAN DIBERI

## When to use this skill

The user (or a sibling audit) asks a structural-identification question:

- What is X?
- Is X an agent / kernel / service / runtime / authority / identity / dataset / doctrine?
- What does X actually do?
- Should we keep X?
- Is X constitutional?

This skill is NOT for: performance audits, security audits, drift detection, skill audits. Use existing audit skills for those.

## The 6-step output format

When the skill fires, produce output in this exact shape:

1. EVIDENCE — file:line, process ps, probe curl, schema field
2. OBSERVED IMPLEMENTATIONS — every artifact implementing this entity
3. WHAT X IS NOT — one bullet per option, evidence-backed
4. WHAT X IS — one short sentence
5. MINIMUM IRREDUCIBLE FUNCTION — what breaks if X dies
6. VERDICT — SEAL / PARTIAL / UNKNOWN

## The classification decision rule

Generate an option-by-option evidence table BEFORE the final verdict.

Each option has evidence FOR AND counter-evidence AGAINST. The chosen option has the strongest NET evidence.

## The minimum irreducible function test

If X disappeared tomorrow, what intelligence capability is lost?

- What breaks (concrete consequence)
- What survives (what can step in)
- What is truly irreplaceable (the one thing only X provides)

If nothing breaks, X is deletable. If everything breaks, X is sovereign-grade.

## The essay vs operational code trap

When a document defines X philosophically but the runtime code measures X operationally, the gap is real and worth flagging:

- Philosophical: A = AKAL (reasoning quality)
- Operational: A = lease compliance rate
- State both. Do not collapse them.

## The phantom reference check

Before classifying, always check:

```bash
# Does the cited reference exist?
grep -c '<REFERENCE_STRING>' /root/arifOS/VAULT999/outcomes.jsonl

# Does the cited artefact exist?
grep -rl '<artifact_name>' /root/AAA /root/arifOS /root/A-FORGE 2>/dev/null | head -5
```

If both return 0 hits, the entity is phantom — the question itself is malformed. State that. Do not classify a phantom.

## The X / Y / Z count verification

When a number is quoted (38 agents, 13 tools, 14 source files), verify the count:

```bash
curl -s http://127.0.0.1:<port>/.well-known/agents.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('agents:', len(d.get('agents', [])))
"
```

A claim with no probe is a sibling-assumed figure. Always verify.

## The structural vs verification division

Do not confuse what X is structurally with whether X works correctly. The classification is ontological (what is X). The verification is functional (does X work). This skill is for the former.

## Canonical anchor classifications

| Entity | Classification | Evidence path |
|---|---|---|
| AAA | D. Registry | 0 MCP tools, 38 agents registered, near-zero traffic |
| arifOS | Constitutional Kernel | 8 verbs, arif_forge deploy 888_HOLD on probe, every organ reports final_authority=ARIF |
| A-FORGE | Execution Surface | 48 tools, APA bridges, forge_execute path |
| FED | Federation Cognitive Allocator | 14 tools, constitutional_tier parameter, 666/999 provider restriction |
| APEX | Governance Health Model | G=(APEX)^(1/4), 43675 rows, geometric mean, measured G=0.3156 |
| i-ARIF | Training Data | 1435 pairs (HF I-ARIF-CANON), AGPL-3.0, zero runtime artifacts |
| AGI/ASI/APEX agent classes | Prompt-layer labels | Zero class implementations in code |
| **The 9-Role Agent Kernel (HEXAGON)** | Organisational decomposition — *which organ carries which deed* | `/root/AAA/agents/HEXAGON.yaml` — 3+2+1+1 |
| **The 9-Cell Cognitive Atlas** | Functional decomposition — *which cognitive step every forge MUST traverse* | 000 Observer → 111 Explorer → 222 Architect → 333 Thinker → 444 Orchestrator → 555 Verifier → 666 Auditor → 777 Executor → 888 Judge → 999 Witness. Two views, one truth. |
| **Phenotype / Genome framing** | Cognitive genome carried by every phenotype; OpenCode-Zen / Hermes-Zen / OpenClaw-Zen = expression patterns, not separate agents | `AAA_PRINCIPAL.md` §2.8 — 10 LLM harnesses are phenotype expressions, not constitutional roles. |
| **ART-ACT-AUTH orthogonal binding** | 3-layer binding that makes phenotype swap work: ART = reflex pre-call, ACT = execution ceremony, AUTH = identity + attestation | `apex-theory-canon` references/apex-art-act-layer-correction.md. 999 = AUTH, not ART. |

## The correction pattern

When you classify X wrongly and another agent proves you wrong, issue a public correction in the same session. The correction IS the deliverable.

## Pitfalls

- Do not classify before probing
- Do not pick the most flattering option
- Do not seal PARTIAL classifications
- Do not collapse essay and code
- Do not over-classify

## Related

- verify-nested-sibling-reports (confident-wrong verdict)
- federation-infra-verification (live state probing)
- arifos-collapse-vector-audit (security claims)
- references/taxonomy-anchor-2026-08-08.md — canonical organ/entity anchors with probe recipes, irreducibility tests, and the 9-role HEXAGON topology
