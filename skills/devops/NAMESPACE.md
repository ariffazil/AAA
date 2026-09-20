# NAMESPACE: devops

> **Marker file** (added 2026-09-19, Fasa 1 skill hygiene).
> This directory is a *namespace*, not a skill.
> Skills live in the subdirectories listed below.

## Purpose
This namespace groups related skills under one roof for discovery and routing.
Each subdirectory is an independent skill with its own SKILL.md.

## Contained skills (1 entry · 1 alias)
- `mcp-transport-fix` — **ALIAS → `/root/AAA/skills/engineering/mcp-ops`** (merged 2026-09-20)
- `mcp-edit-activation` — **ALIAS → `/root/AAA/skills/engineering/mcp-ops`** (merged 2026-09-20)

> This namespace now holds **no standalone skill**: both entries are aliases pointing at the MCP
> owner. They are kept so no old name stops resolving (2026-09-20 MCP cluster merge).

## Owner

**Owner:** `AAA/devops`

_Single-writer policy (Fasa 2): owner has write authority; other layers can read but not edit._

## Conventions
- Do not edit skill SKILL.md files from this namespace layer.
- To add a new skill: create subdirectory with SKILL.md, then add to FEDERATED_SKILLS_REGISTRY_V3.yaml.
- To deprecate: rename subdir to `<name>.DEPRECATED-<date>`, do not delete.
