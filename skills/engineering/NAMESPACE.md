# NAMESPACE: engineering

> **Marker file** (added 2026-09-19, Fasa 1 skill hygiene).
> This directory is a *namespace*, not a skill.
> Skills live in the subdirectories listed below.

## Purpose
This namespace groups related skills under one roof for discovery and routing.
Each subdirectory is an independent skill with its own SKILL.md.

## Contained skills (15 entries · 14 skills + 1 alias)
- `cicd-deploy`
- `code-review`
- `drift-watch`
- `federation-health`
- `incident-response`
- `mcp-ops` — **owner of the MCP cluster** (absorbed 19 MCP names, 2026-09-20)
- `mcp-testing` — **ALIAS → `mcp-ops`** (merged 2026-09-20; the name still resolves, it is not a separate skill)
- `pr-governance`
- `security-audit`
- `skill-creator`
- `skill-drift`
- `skill-inventory`
- `telemetry-watchdog`
- `verify-work`
- `vps-ops`

## Owner

**Owner:** `AAA/engineering`

_Single-writer policy (Fasa 2): owner has write authority; other layers can read but not edit._

## Conventions
- Do not edit skill SKILL.md files from this namespace layer.
- To add a new skill: create subdirectory with SKILL.md, then add to FEDERATED_SKILLS_REGISTRY_V3.yaml.
- To deprecate: rename subdir to `<name>.DEPRECATED-<date>`, do not delete.
