# NAMESPACE: .archive

> **Marker file** (added 2026-09-19, Fasa 1 skill hygiene).
> This directory is a *namespace*, not a skill.
> Skills live in the subdirectories listed below.

## Purpose
This namespace groups related skills under one roof for discovery and routing.
Each subdirectory is an independent skill with its own SKILL.md.

## Contained skills (14)
- `2026-08-18-fitness`
- `2026-09-16-media-skill-dedup`
- `2026-09-16-skill-zen-quartet`
- `2026-09-17-leadership-roster-merge`
- `2026-09-19-sota-snapshot`
- `agent-capability-self-audit`
- `alias-tables-20260918`
- `drift-watch`
- `empty-20260917`
- `mcp-ops`
- `mmx-cli`
- `session-close-20260917-215305`
- `shells-20260917`
- `warga-skills`

## Owner

**Owner:** `AAA/.learning (system hidden)`

_Single-writer policy (Fasa 2): owner has write authority; other layers can read but not edit._

## Conventions
- Do not edit skill SKILL.md files from this namespace layer.
- To add a new skill: create subdirectory with SKILL.md, then add to FEDERATED_SKILLS_REGISTRY_V3.yaml.
- To deprecate: rename subdir to `<name>.DEPRECATED-<date>`, do not delete.
