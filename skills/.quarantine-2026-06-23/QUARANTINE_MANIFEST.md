# Skill Quarantine Manifest — 2026-06-23

**Authority:** ARIF directive `ARIFOS::AAA_FEDERATED_SKILL_ALIGNMENT::v1`  
**Executor:** Kimi Code CLI governed agent  
**Skill applied:** `auditor-validator-kutip-sampah` + `aforge-execution-governor`  
**Action class:** GUARDED_WRITE (reversible quarantine)  
**Blast radius:** AAA-scope skill directory (`/root/AAA/skills/`)

## Quarantined duplicates

These AAA-scope skills overlapped with canonical project-scope versions. The project-scope copies are retained as canonical because they are the upstream/third-party source or the domain-owning organ's version.

| Skill | Original path | Canonical path | Reason |
|---|---|---|---|
| `geox-basin-interpreter` | `/root/AAA/skills/geox-basin-interpreter/` | `/root/.agents/skills/geox-basin-interpreter/` | GEOX domain skill; project-scope is the domain-owning source. |
| `skill-creator` | `/root/AAA/skills/skill-creator/` | `/root/.agents/skills/skill-creator/` | Project-scope is the upstream Pydantic skill-creator package with full assets (LICENSE, agents/, assets/, eval-viewer/, references/, scripts/). |
| `mcp-smoke-test` | `/root/AAA/skills/mcp-smoke-test/` | `/root/.agents/skills/mcp-smoke-test/` | Identical content to project-scope copy; project-scope retained as canonical location. |

## Rollback

All moves are reversible. To restore a quarantined skill:

```bash
mv .quarantine-2026-06-23/<skill> ./<skill>
```
