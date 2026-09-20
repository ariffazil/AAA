# NAMESPACE: knowledge

> **Marker file** (added 2026-09-19, Fasa 1 skill hygiene).
> This directory is a *namespace*, not a skill.
> Skills live in the subdirectories listed below.

## Purpose
This namespace groups related skills under one roof for discovery and routing.
Each subdirectory is an independent skill with its own SKILL.md.

## Contained skills (3)
- `know-language`
- `know-math`
- `know-physics`

> **2026-09-20 — case/path-duplicate collapse (BRIEF-v2 wave 2).** These three names were
> stored twice: a real directory here *and* a real directory at the skills root, so the
> loader resolved to one while the other rotted. The skills-root directories are now the
> single canonical owners; the subdirectories below are **alias symlinks** to them
> (`knowledge/know-language -> ../know-language`). The names still resolve from the loader.
> Pre-collapse bodies are preserved at
> `know-<name>/references/absorbed-know-<name>.md` and
> `.frozen/2026-09-20-case-dupes/know-<name>/`.

## Owner

**Owner:** `AAA/knowledge`

_Single-writer policy (Fasa 2): owner has write authority; other layers can read but not edit._

## Conventions
- Do not edit skill SKILL.md files from this namespace layer.
- To add a new skill: create subdirectory with SKILL.md, then add to FEDERATED_SKILLS_REGISTRY_V3.yaml.
- To deprecate: rename subdir to `<name>.DEPRECATED-<date>`, do not delete.
