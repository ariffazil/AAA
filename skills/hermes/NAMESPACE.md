# NAMESPACE: hermes

**owner:** AAA  <!-- SK7: derived from dir_name=hermes, default=AAA, added 2026-09-26T23:53:33Z -->

> **Marker file** (added 2026-09-19, Fasa 1 skill hygiene).
> This directory is a *namespace*, not a skill.
> Skills live in the subdirectories listed below.

## Purpose
This namespace groups related skills under one roof for discovery and routing.
Each subdirectory is an independent skill with its own SKILL.md.

## Contained skills (0 — migrated 2026-09-25 mesh repair)

Former children, now merged into umbrellas (see `SKILL_ALIAS_TABLE.json`):
- `web-scrape` → folded into `web-ops` (`hermes-research-substrate` → `web-ops`)
- `web-search` → alias `web-search` → `web-ops`

This namespace is retained as a routing marker only. Do not add children here;
new hermes-capability skills live at top level (`hermes-*`) per the 2026-10-06
alignment (`/root/AAA/reports/skills-alignment-2026-10-06.md`).

## Owner

**Owner:** `AAA/hermes`

_Single-writer policy (Fasa 2): owner has write authority; other layers can read but not edit._

## Conventions
- Do not edit skill SKILL.md files from this namespace layer.
- To add a new skill: create subdirectory with SKILL.md, then add to FEDERATED_SKILLS_REGISTRY_V3.yaml.
- To deprecate: rename subdir to `<name>.DEPRECATED-<date>`, do not delete.
