# Focused Skill Audit Report

Generated: 2026-06-12T17:16:47.759763+00:00
Trigger: propagation of `arifos-memory, arifos-mcp-federation` to agent config locations.

## 1. Propagation Verification

### arifos-memory

| Scope | Path | Exists | Symlink | Resolves |
|-------|------|--------|---------|----------|
| agents | `/root/.agents/skills/arifos-memory/SKILL.md` | True | False | True |
| claude | `/root/.claude/skills/arifos-MEMORY_MD.md` | True | True | True |
| codex | `/root/.codex/skills/arifos-MEMORY_MD.md` | True | True | True |
| kimi | `/root/.arifos/agents/kimi/skills/arifos-memory/SKILL.md` | True | False | True |

### arifos-mcp-federation

| Scope | Path | Exists | Symlink | Resolves |
|-------|------|--------|---------|----------|
| agents | `/root/.agents/skills/arifos-mcp-federation/SKILL.md` | True | False | True |
| claude | `/root/.claude/skills/arifos-mcp-federation.md` | True | True | True |
| codex | `/root/.codex/skills/arifos-mcp-federation.md` | True | True | True |
| kimi | `/root/.arifos/agents/kimi/skills/arifos-mcp-federation/SKILL.md` | True | False | True |


## 2. Target Skill Health

| Skill | Scopes | Version | Lines | Age (d) | Issues |
|-------|--------|---------|-------|---------|--------|
| arifos-mcp-federation | agents, claude, codex, kimi | 1.1.0 | 108 | 0.0 | - |
| arifos-memory | agents, claude, codex, kimi | 1.1.0 | 96 | 0.0 | - |

## 3. Trigger Overlap (Jaccard ≥0.35)

No significant description overlap detected.

## 4. All Active Skills Snapshot

| Skill | Scopes | Version | Lines | Age (d) | Issues |
|-------|--------|---------|-------|---------|--------|
| agents-sdk | agents | unknown | 221 | 43.1 | stale |
| arifos-evals | agents | unknown | 107 | 17.5 | - |
| arifos-governance | agents | unknown | 90 | 17.5 | - |
| arifos-observability | agents | unknown | 72 | 17.5 | doc-rot |
| arifos-plan-dag | agents | unknown | 73 | 17.5 | - |
| arifos-recursive-audit | agents | 1.1.0 | 83 | 0.0 | - |
| arifos-untrusted-sandbox | agents | 1.0.0 | 84 | 5.9 | - |
| cloudflare | agents | unknown | 245 | 43.1 | stale |
| cloudflare-email-service | agents | unknown | 103 | 43.1 | stale |
| durable-objects | agents | unknown | 186 | 43.1 | stale |
| frontend-design | agents | unknown | 42 | 43.1 | stale |
| geox-basin-interpreter | agents | unknown | 89 | 17.5 | - |
| replicate-models | agents | unknown | 74 | 8.9 | - |
| replicate-prompting | agents | unknown | 202 | 8.9 | - |
| sandbox-sdk | agents | unknown | 177 | 43.1 | stale |
| skill-creator | agents | unknown | 66 | 17.5 | - |
| skill-trigger-linter | agents | unknown | 81 | 17.5 | - |
| web-perf | agents | unknown | 201 | 43.1 | stale |
| workers-best-practices | agents | unknown | 127 | 43.1 | stale |
| wrangler | agents | unknown | 922 | 43.1 | stale, bloat |
| arifos-mcp-federation | agents, claude, codex, kimi | 1.1.0 | 108 | 0.0 | - |
| arifos-memory | agents, claude, codex, kimi | 1.1.0 | 96 | 0.0 | - |
| godel-humility-lock | agents, claude, codex, kimi | 1.0.0 | 91 | 5.9 | - |
| vps-health-ops | agents, claude, codex, kimi | 1.0.0 | 90 | 0.0 | - |
| constitutional-reasoning | claude | unknown | 168 | 26.4 | - |
| docker-thermodynamics | claude | unknown | 73 | 28.4 | - |
| drift-watch | claude | unknown | 45 | 10.2 | - |
| f1-gate | claude | unknown | 36 | 10.2 | doc-rot |
| github-ops | claude | unknown | 85 | 28.4 | - |
| incident-triage | claude | unknown | 35 | 10.2 | doc-rot |
| mcp-ops | claude | unknown | 182 | 16.2 | - |
| multi-discipline-critique | claude | unknown | 44 | 10.2 | - |
| precommit-review | claude | unknown | 34 | 10.2 | - |
| secret-hygiene | claude | unknown | 76 | 28.4 | - |
| vault-integrity | claude | unknown | 71 | 28.4 | - |
| verify-runtime | claude | unknown | 40 | 10.2 | - |
| vps-docker-ops | claude | unknown | 104 | 28.4 | - |
| code-wiki | codex | unknown | 328 | 16.2 | - |
| fastmcp | codex | 1.0.0 | 152 | 16.2 | - |
| mcporter | codex | 1.0.0 | 162 | 16.2 | - |
| mcp-unified | kimi | 2.1.0 | 281 | 16.2 | doc-rot |
| site-architecture | kimi | 2.1.0 | 208 | 26.1 | - |

## 5. Recommendations

1. If propagation table shows `exists=false` or `resolves=false`, recreate the symlink.
2. Resolve broken absolute paths in flagged skills (likely stale example paths).
3. For any high-overlap pair, sharpen `Use When` / `Do Not Use When` boundaries.
4. Review target skill references (e.g. `references/GRAPHITI_MD.md`) for freshness.