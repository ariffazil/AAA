# SKILL FRONTMATTER CONTRACT — Compass Layer v1.0

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-13 by 333-AGI under F13 SOVEREIGN (888 authorization)
> **Authority:** 888 (Arif) · **Status:** BINDING for all SKILL.md from 2026-08-13
> **Companion:** `/root/AAA/scripts/compass.py` (gate enforcement)

## Purpose

Two new frontmatter fields extend the existing schema (name, description, risk_tier, floor_scope, capability_tier, dependencies) — they do NOT replace any existing field. Compass reads both old (`dependencies.mcp_servers`) and new (`required_tools`) for backwards compatibility.

## The Two New Fields

### `required_tools` — list[str]

```yaml
required_tools:
  - forge_fetch         # URL fetch (observation)
  - forge_browser_navigate  # browser actuation
  - browser_exec        # code-in-browser
```

**Semantics:** The complete set of non-universal tools this skill MAY invoke. Universal tools (see below) are ALWAYS allowed and MUST NOT be listed (avoids bloat).

**When empty/missing:** Fail-closed — skill resolves to OBSERVE-only universal minimum. No mutation, no network egress beyond fetch, no MCP calls.

**Backwards compatibility:** If `required_tools` is absent but `dependencies.mcp_servers` exists, Compass uses `dependencies.mcp_servers` as the source of truth. Migration is incremental.

### `tool_gate` — enum

```yaml
tool_gate: strict       # or: permissive
```

| Value | Behavior |
|-------|----------|
| `strict` (default) | Final allowlist = `required_tools` + universal minimum ONLY. Anything else blocked. |
| `permissive` | Final allowlist = `required_tools` + universal minimum + standard observation tools (forge_search, forge_research, arif_observe). |
| (missing) | Fail-closed to `strict`. |

## Universal Minimum (always allowed, never listed)

These tools are the baseline substrate every agent/skill needs for self-state. Listing them is forbidden (causes Compass to warn, not fail):

```
read, glob, grep                    # filesystem observation
forge_fetch                         # URL fetch (read-only HTTP)
forge_health_check, forge_memory    # self-state
arif_observe                        # evidence search (read-only)
forge_shell_dryrun                  # preview without mutation
```

## Fail-Closed Behavior (F1 AMANAH)

When a SKILL.md has NEITHER `required_tools` NOR `dependencies.mcp_servers`:

```
final_allowlist = universal_minimum ONLY
mutation_tools = BLOCKED (forge_shell, forge_filesystem write, forge_git commit, arif_forge, arif_seal)
network_egress = fetch ONLY (no browser, no search API beyond arif_observe)
```

This is the **strictest** default. Skills must EARN wider tool access by declaring it.

## Compass Algorithm

```
INPUT: skill_path (SKILL.md location)
OUTPUT: JSON {skill_id, allowlist, gate_mode, source}

1. Parse YAML frontmatter
2. source = "required_tools" if present
   elif "dependencies.mcp_servers" present → source = "legacy"
   else → source = "fail_closed"
3. declared = required_tools OR dependencies.mcp_servers OR []
4. gate = tool_gate OR "strict"
5. final = declared + universal_minimum (dedup)
6. if gate == "permissive": final += [forge_search, forge_research, arif_think]
7. emit JSON
```

## Migration Plan

- **v1.0 (now):** 10 pilot skills get explicit `required_tools` + `tool_gate`. Compass handles legacy for the other 169 via `dependencies.mcp_servers` fallback.
- **v1.1 (next epoch):** Bulk-migrate skills with `dependencies.mcp_servers` to use `required_tools` naming. Compass warns (not fails) on legacy.
- **v2.0 (post-Arif review):** All skills have `required_tools`. Compass removes legacy fallback.

## Naming Convention for `required_tools` values

Use the canonical MCP tool name as it appears in `tools/list`. Examples:
- `forge_fetch`, `forge_filesystem`, `forge_shell`, `forge_git`, `forge_browser_navigate`, `forge_browser_click`, `forge_browser_evaluate_js`, `browser_exec`
- `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`
- `forge_postgres`, `forge_docker`, `forge_vault`, `forge_predict`
- `geox_basin`, `geox_seismic_compute`, `geox_petrophysics`, `wealth_capital_*`, `well_*`

**Forbidden:** ad-hoc names like "the browser" or "git ops". Use exact tool IDs.

## Pilot Cohort (v1.0 — 10 skills)

| Skill | required_tools (proposed) | gate |
|-------|---------------------------|------|
| AAA-OCR-optical-compression | forge_fetch, forge_filesystem | strict |
| image-text-editing | forge_filesystem, forge_shell | strict |
| AGI-agentic-web | forge_fetch, forge_browser_navigate, forge_browser_click, forge_browser_evaluate_js, browser_exec | permissive |
| FORGE-mcp-lifeguard | forge_fetch, forge_shell_dryrun, forge_health_check | permissive |
| FORGE-document-intelligence | forge_fetch, forge_filesystem, forge_document_ingest | strict |
| apex_verdict_seal | arif_judge, arif_seal, forge_memory | strict |
| hermes-fact-check (if in catalog) | arif_observe, forge_fetch, forge_memory | permissive |
| AGI-explorer-intelligence | arif_observe, forge_fetch, forge_search | permissive |
| ASI-drift-watch | forge_health_check, forge_fetch, forge_filesystem | permissive |
| FORGE-github-ops | forge_github, forge_git, forge_filesystem | strict |

## Verification (one-line test)

```bash
python3 /root/AAA/scripts/compass.py --skill /root/AAA/skills/agi/AGI-agentic-web/SKILL.md
# → emits JSON allowlist
# → filters MCP tool schemas to allowlist before injection to system prompt
```

DITEMPA BUKAN DIBERI — The arrow is connected. The compass points true north.
