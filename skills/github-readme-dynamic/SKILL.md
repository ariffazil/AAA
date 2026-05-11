# GitHub README Dynamic SOT — Skill

## Purpose

Generate and maintain README.md files that are always aligned with actual repo architecture.
No drift between what the README claims and what the code contains.

## Core Principle

**README = compiled artifact, not authored prose.**
Static narrative is written by hand. Dynamic facts are extracted from code and injected into the README on every significant change.

## What This Skill Does

1. **Scans** a repo directory and extracts dynamic facts:
   - Tool count and list (from `tool_registry.json`, `constitutional_map.py`, `megaTools/`)
   - File tree for key directories
   - Version, build_epoch, build_timestamp from registry files
   - Endpoint list from server entrypoints
   - Package metadata from `pyproject.toml`

2. **Compares** extracted facts against README claims

3. **Patches** README at designated `<!-- SOT:section_name -->` markers with fresh content

4. **Validates** that critical claims match — fails with a report if drift detected

## Dynamic Sections (markers in README)

```
<!-- SOT:tool_surface -->
<!-- SOT:file_structure -->
<!-- SOT:version_info -->
<!-- SOT:endpoints -->
```

## Usage

```bash
# Full audit — compare README claims vs actual
python3 skills/github-readme-dynamic/audit.py /root/arifOS

# Generate updated README (dry-run first)
python3 skills/github-readme-dynamic/generate.py /root/arifOS --dry-run

# Apply and commit
python3 skills/github-readme-dynamic/generate.py /root/arifOS --apply
```

## Per-Repo Approach

### arifOS (Python/MCP)
- Source of truth: `arifosmcp/tool_registry.json` (11 tools, v2.0.0-canonical-kanon, 2026.04.25)
- Scan: `arifosmcp/tools/`, `arifosmcp/megaTools/`, `arifosmcp/runtime/`
- Markers needed: `tool_surface`, `file_structure`, `version_info`, `endpoints`
- Key drift: README says 13 tools, registry says 11. README says arifos_fetch(222)/arifos_reply(444r) but those are MISSING from registry.

### AAA (OpenClaw workspace)
- Source of truth: `openclaw.json`, workspace root files
- Scan: root `.md` and `.yaml` files, `skills/` dir
- Markers needed: `workspace_structure`, `skills_inventory`

### WEALTH (Python/FastMCP)
- Source of truth: `internal/monolith.py`, `server.py`, `mcp/server.py`
- Scan: `internal/`, `tools/`
- Markers needed: `tool_surface`, `capital_scales`

### GEOX (Python + visualization)
- Source of truth: `geox/geox_mcp/`, `geox/core/`, `skills/`, `geox-gui/`
- Markers needed: `tool_surface`, `apps_inventory`, `skill_domains`

### A-FORGE (TypeScript/Node)
- Source of truth: `package.json`, `src/` structure
- Scan: `src/`, `dist/`
- Markers: `file_structure`, `npm_surface`

### arif-sites (Static + Docusaurus)
- Source of truth: `sites/`, `apps/`, `services/`, `infra/`
- Markers: `site_inventory`, `deployment_targets`

## Validation Rules

| Claim in README | Must Match | Tolerance |
|---|---|---|
| Tool count | Actual tool_registry.json count | Exact |
| Version | build_epoch from registry | Exact |
| Tool names | Names from registry | Exact |
| File count | Actual non-__pycache__ Python files | ±5% |

## Output Format

```
=== README SOT AUDIT: arifOS ===

[DELTA] tool_count: README claims 13, registry has 11
[DELTA] tool_names: README includes arifos_fetch(222), arifos_reply(444r) — NOT in registry
[DELTA] version: README says 2026.04.24-KANON, registry build_epoch is 2026.04.25
[OK] endpoints: /health, /metadata, /humans.txt — all found in server.py
[OK] floors: F1-F13 present in constitutional_map.py

SEAL: 2 blockers, 2 ok
```

## Arif's Protocol

1. Run `audit.py` on a repo → see DELTA report
2. Discuss with Arif which DELTAs need fixing
3. `generate.py --apply` patches the README at SOT markers
4. Commit + push

## GitHub Actions CI (optional future step)

```yaml
# .github/workflows/readme-sync.yml
on: [push]
jobs:
  readme-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: python3 skills/github-readme-dynamic/generate.py . --apply
      - uses: peter-evans/create-pull-request@v5
```

This keeps README updated on every push without manual intervention.
