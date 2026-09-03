<!-- SOT-MANIFEST
owner: aaa-maintainer
skill_manifest_version: 1.0.0
scope: /root/AAA
-->

# SKILL.md — AAA Capability Map

> **What AAA can do. What AAA cannot. What patterns AAA follows. What AAA avoids.**

---

## 1 · Core Capabilities
- Display federation health (Cockpit React dashboard)
- Route agent-to-agent messages (A2A v1.0.0)
- Maintain agent cards and discovery manifests
- Audit git/skills governance across federation
- Render AAA's GitHub canon (12 skills, this bundle)

## 2 · MCP Servers
| Server | Port | When |
|---|---|---|
| arifOS | 8088 | Always first. Session, judgment, seal. |
| A-FORGE | 7071 / 7072 | Engineering, lease-gated mutations. |
| GEOX | 8081 | Domain queries via A2A. |
| WEALTH | 18082 | Domain queries via A2A. |
| WELL | 18083 | Domain queries via A2A. |

## 3 · Tools
### Read (no lease)
- `forge_filesystem_read`, `forge_filesystem_glob`, `forge_filesystem_grep`
- `forge_git_status`, `forge_git_log`, `forge_git_diff`
- `arifos_arif_observe`, `arifos_arif_think`

### Write (lease required)
- `forge_filesystem_write`, `forge_git_commit`
- `forge_github_create_issue`, `forge_github_create_pull_request`, `forge_github_pr`
- `arifos_arif_seal`

### Domain — GitHub Canon
All 12 skills under `skills/github/` are available to AAA-agent.

## 4 · Workflows
- GHA-1: GitHub Issue Triage
- GHA-2: PR Governance Review
- GHA-3: CI Diagnose
- GHA-4: GitHub Runbook
- GHA-5–16: Per-skill workflows (see 12-skill canon)

## 5 · Patterns I Follow
- 3-file invariant (AGENT.md + SKILL.md + TASKS.md)
- Skill library at `skills/<id>/SKILL.md`
- Conventional commits with `REPO=ariffazil/AAA` trailer
- Date-stamp tags `vYYYY.MM.DD[-SUFFIX]`
- `npm run validate:aaa` before commit

## 6 · Patterns I Avoid
- New `@mcp.tool` registrations (per "no new tools" rule)
- Inline CLAUDE.md / model-specific files
- Self-approval on PR
- Skip CI to ship faster
- Bypass A2A auth
- Direct VAULT999 mutation

## 7 · Code Style
- React 19 + TypeScript ~6.0 + Vite 8 + Tailwind 4
- Path alias: `@/` → `src/`
- ESLint 10 + typescript-eslint 8

## 8 · Issue / PR Conventions
- Issue: Title + body (context, evidence, risk, labels)
- PR: `Closes #N`, body + checklist
- Never assign to Arif without explicit ack
- Never close without documentation

---

*License: AGPL-3.0 · Sovereign: Arif bin Fazil · DITEMPA BUKAN DIBERI*
