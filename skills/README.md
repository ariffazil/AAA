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

---

## Skill Mirror Topology (2026-07-16, QQQ-envelope P7)

The federation's skill canon lives at **`/root/.agents/skills/`** (user-scope canonical,
ATLAS333-aligned). AAA's `skills/` is a **mixed bundle**: most entries are mirror-canonical
symlinks into that location; a minority are project-scope real files that live only in this
repo. The split is intentional and explicitly declared here so future agents (and future Arif)
don't have to archeology.

### Layout

| Class | Count | Form | Source of truth | When to edit here |
|-------|-------|------|-----------------|-------------------|
| **Mirror-canonical** | 71 | Symlinks → `/root/.agents/skills/<name>/` | `/root/.agents/skills/` | NEVER — edit the canonical instead |
| **Project-scope real** | 144 | Real directories tracked in git | This repo (`AAA/skills/`) | When the skill is AAA-specific |
| **`ARCHIVE-*`** markers | 30 | Real directories (intentional) | This repo | Move to `_archive/` if retiring |
| **Root-file leakage** | 3 | `AAA_SKILL.md`, `AAA_ZEN.md`, `APPROVE_HANDLER.md` at `skills/` root | This repo (legacy) | Move to repo root in follow-up commit |

Total entries: 248 (symlinks + real dirs + leakage).

### Verification (post-zen, all green)

- All 71 mirror-canonical symlinks resolve to existing targets (broken = 0).
- All 138 originally-shared skills byte-identical between AAA and `/root/.agents/skills/`.
- All 2 AAA-only-then-added-from-`.agents/` skills (apex-formal-constitution, causal555-pywhy)
  present as real dirs.
- Working tree clean after `a3fc813 feat(skills): zen AAA skill catalog, align with A2A + ATLAS333 canonical`
  on branch `feat/aaa-skill-catalog-zen`.

### Why mirror-canonical symlinks (QQQ verdict: P7)

Q1 enumerated 7 paths. Q2 metrics: P7 (mirror + docs) dominated P1 on Conf (0.90 vs 0.85) at
+10min cost; P2 (real files) wins on portability but loses on federation alignment; P5
(INVERSE — never align) failed on PA-NONE; P6 (submodule) dominated on Time/Conf.
Q3 quantum: choosing P7 canonizes "federation is canonical-first; project repos mirror
user-scope; explicit doctrine over implicit archaeology."

### Operational notes

- **Adding a new skill:** if it's general federation doctrine, add it to `/root/.agents/skills/<name>/`
  and create a symlink here. If it's AAA-specific, add it as a real dir in this repo.
- **Editing a mirror-canonical skill:** do NOT edit through the symlink. Edit
  `/root/.agents/skills/<name>/SKILL.md` directly. The change is immediately visible
  via the symlink.
- **Audit / drift detection:** future agents can `diff -r skills/<mirror-name>/ /root/.agents/skills/<mirror-name>/`
  to confirm mirrors haven't been locally overridden. Any divergence indicates either
  a manual `cp` over a symlink (drift) or a deliberate `_archive/` snapshot (intentional).

### Receipts

- `/root/forge_work/2026-07-16/AAA_SKILL_CATALOG_ZEN.md` — full method, metrics, hazard
- `_archive/skill-canonical-sync-2026-07-16/` — gitignored, local-only backups of
  10 divergent AAA-side SKILL.md files that were overwritten by canonical

DITEMPA BUKAN DIBERI.
