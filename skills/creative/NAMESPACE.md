# NAMESPACE: creative

> **Marker file** (added 2026-09-19, Fasa 1 skill hygiene).
> This directory is a *namespace*, not a skill.
> Skills live in the subdirectories listed below.

## Purpose
This namespace groups related skills under one roof for discovery and routing.
Each subdirectory is an independent skill with its own SKILL.md.

## Contained skills (10)
- `ascii-art`
- `chart-artifact-render-qa`
- `comfyui`
- `excalidraw`
- `image-restyle-and-edit`
- `image-text-editing`
- `pretext`
- `reference-image-rendering`
- `sketch`
- `touchdesigner-mcp`

## Owner

**Owner:** `AAA/creative`

_Single-writer policy (Fasa 2): owner has write authority; other layers can read but not edit._

## Conventions
- Do not edit skill SKILL.md files from this namespace layer.
- To add a new skill: create subdirectory with SKILL.md, then add to FEDERATED_SKILLS_REGISTRY_V3.yaml.
- To deprecate: rename subdir to `<name>.DEPRECATED-<date>`, do not delete.
