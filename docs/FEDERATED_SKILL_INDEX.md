# Federated Skill Index

> **SOT:** 2026-07-24 | **seal_seq:** fed-phase-5
> **Zen 99 Cap:** 33 skills per agent (333-AGI, 555-ASI, 888-APEX) = 99 total

## Skill Distribution

| Catalog | Count | Owner | Status |
|---------|-------|-------|--------|
| AAA/skills/ | 213 | AAA | ⚠️ Over cap (62 FORGE skills alone) |
| HERMES/skills/ | 219 | HERMES | ⚠️ Unprefixed, needs audit |
| arifOS/skills/ | 35 | arifOS | ⚠️ Near cap |
| A-FORGE/skills/ | 1 | A-FORGE | ✅ Under cap |

## Namespace Discipline

| Prefix | Owner | Cap | Current | Status |
|--------|-------|-----|---------|--------|
| `agi_*` | 333-AGI | 33 | 14 | ✅ Under |
| `asi_*` | 555-ASI | 33 | 12 | ✅ Under |
| `apex_*` | 888-APEX | 33 | 3 | ✅ Under |
| `forge_*` | A-FORGE | — | 62 | ⚠️ AAA hosts 62 FORGE skills |
| `arif_*` | arifOS | 9 (fixed) | 9 | ✅ Locked |
| `geox_*` | GEOX | — | 32 | ✅ |
| `capital_*` | WEALTH | — | 12 | ✅ |
| `well_*` | WELL | — | 8 | ✅ |

## Key Catalogs

| Catalog | Path | Description |
|---------|------|-------------|
| AAA Master | `/root/AAA/skills/AAA_SKILL.md` | Canonical AAA skill index |
| AAA Zen | `/root/AAA/skills/AAA_ZEN.md` | Zen-aligned skill philosophy |
| HERMES Master | `/root/HERMES/skills/` | 219 skills in flat directory |
| arifOS Master | `/root/arifOS/skills/` | 35 kernel skills |

## Known Issues

1. **FORGE skill bloat (62 skills in AAA):** 29 over the Zen 33 cap for 888-APEX. Many FORGE skills are operational (FORGE-cicd-docker-deploy, FORGE-github-ops, FORGE-vps-docker) — candidates for consolidation or A-FORGE migration.

2. **HERMES skills unfederated (219 skills):** No namespace prefix convention. Skills like `capital`, `geology`, `governance` should route to their respective organs rather than duplicating logic in HERMES.

3. **Cross-organ duplicates:** Skills like `dream-engine` exist in both AAA and HERMES. `federation-orchestrator` and `FORGE-federation-orchestrator` may overlap.

## Remediation Path

1. Audit FORGE skills — consolidate/collapse where possible
2. Move execution skills from AAA → A-FORGE
3. Add namespace prefixes to HERMES skills
4. Deduplicate cross-organ skills
5. Enforce Zen 99 cap at registration time
