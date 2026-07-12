# AAA Skill Library

> **Authority:** Subordinate to `arifOS` constitution and agent role.  
> **Purpose:** Reusable governed playbooks that teach agents how to perform specific work safely.

---

## What Is a Skill?

A skill is **not** an agent, an MCP tool, or the constitution. It is a **training manual** — a reusable playbook that tells an agent:

- When should this skill be used?
- What does it help the agent do?
- What inputs does it need?
- What steps should the agent follow?
- What tools may it use?
- What must it **never** do?
- When must it escalate to `arifOS` / Arif?
- What output should it produce?

---

## Authority Hierarchy

```
Arif
↓
arifOS constitution / floors / judge
↓
AAA agent role
↓
AAA skill  ← you are here
↓
MCP / native tool
```

A skill **must not**:
- Approve dangerous actions
- Override arifOS
- Define final authority
- Delete files without asking

A skill **must**:
- Help the agent perform work safely
- Obey arifOS
- Escalate dangerous actions
- Produce evidence and a plan

---

## Skill Structure

Every skill lives in its own directory under `skills/<skill-id>/`:

```
skills/<skill-id>/
├── SKILL.md        # Canonical playbook (required)
├── EXAMPLES_MD.md     # Example inputs/outputs (recommended)
└── tests.md        # Test cases and verification (recommended)
```

### SKILL.md Frontmatter

```yaml
---
id: <skill-id>
name: <Human-readable name>
version: "1.0.0"
description: <One-line purpose>
owner: <Agent or team>
risk_tier: low | medium | high
knowledge_basis:
  physics: false
  math: false
  language: true
host_compatibility:
  - claude-code
  - codex
  - opencode
dependencies:
  skills: []
  servers: []
  tools: []
examples:
  - <brief example description>
tests:
  - <test case description>
version_lock:
  schema_version: "1"
  artifact_hash: pending
---
```

### SKILL.md Body Sections

1. **Overview** — What this skill does and why it exists
2. **When to Use** — Trigger conditions and context
3. **When NOT to Use** — Boundary conditions and escalation triggers
4. **Inputs** — What the agent needs before starting
5. **Procedure** — Step-by-step instructions
6. **Allowed Tools** — Which MCP/native tools may be used
7. **Forbidden Actions** — Hard stops and escalation rules
8. **Output Format** — What the agent must produce
9. **Escalation Path** — When and how to escalate to arifOS / Arif

---

## Registry

All skills must be registered in `registries/skills.yaml` and packaged in `contracts/skills/packages.yaml`.

---

## TREE777 Audit

Skills are audited weekly by TREE777:

```bash
node scripts/tree777-skill-audit.mjs
```

TREE777 checks:
- Every registered skill has a `SKILL.md`
- No orphan links (broken references)
- Skills conform to the canonical template
- Promotion readiness (examples + tests present)

Results are anchored to `VAULT999` for audit continuity.

---

## Recommended Skills

| Skill | Priority | Purpose |
|-------|----------|---------|
| `repo-hygiene-audit` | **P0** | Inspect repos for chaos, produce cleanup plan |
| `mcp-smoke-test` | P1 | Validate MCP servers respond correctly |
| `agent-onboarding` | P1 | Standard agent identity setup |
| `github-pr-review` | P2 | Governed PR review checklist |
| `service-health-triage` | P2 | Diagnose federation service health |
| `secret-safety-scan` | P2 | Scan for exposed secrets |
| `readme-truth-check` | P2 | Verify README matches reality |
| `incident-escalation` | P2 | Standard incident response protocol |

---

**DITEMPA BUKAN DIBERI** — Skills are forged, not given.

## Multi-harness unification (2026-07-12)

- **Alias table:** [`SKILL_ALIAS_TABLE.json`](./SKILL_ALIAS_TABLE.json) — V3 short → disk path (63/63)
- **Mesh sync:** [`scripts/skill-mesh-sync.sh`](./scripts/skill-mesh-sync.sh)
- **Complete receipt:** [`docs/SKILL-UNIFICATION-COMPLETE-2026-07-12.md`](./docs/SKILL-UNIFICATION-COMPLETE-2026-07-12.md)
- **Canon:** AAA catalog; `~/.grok` / `~/.claude` / `~/.codex` are views

### Ops skill (load this)

- **`skill-unification`** — alias table, mesh-sync, BOOT gate (also linked in `~/.grok/skills/skill-unification`)
- **`meta-mesa-skill-atlas`** — inventory / routing / gaps
