# Linux Foundation AI Catalog — Pin

> **Pinned:** 2026-06-22
> **Source:** https://github.com/Agent-Card/ai-catalog
> **Spec site:** https://agent-card.github.io/ai-catalog/
> **License:** MIT
> **Status:** Draft v0.1 (Linux Foundation temporary working repo)

## What is it

A typed, nestable JSON container for discovering heterogeneous AI artifacts
across protocols (MCP, A2A, Claude Code plugins, datasets, model cards, nested
catalogs). Optional **Trust Manifest** extension for DID/SPIFFE identity,
attestations, provenance. Static discovery at `/.well-known/ai-catalog.json`.

## Adoption path (upstream)

> "When the specification is finalized, A2A and MCP steering committees will
> vote on adoption of the AI Catalog standard, potentially replacing existing
> protocol-specific standards or proposals."
> — Agent-Card/ai-catalog README

## Our local artifact

`AAA/registries/discovery/ai-catalog.json` — schema `$schema` field references
the upstream v0.1 spec. 7 catalog entries: arifOS, A-FORGE, GEOX, WEALTH,
WELL, AAA Cockpit, arifOS Skills Bundle.

## Decision points (awaits 888)

1. Serve `ai-catalog.json` at `https://aaa.arif-fazil.com/.well-known/ai-catalog.json`?
2. Submit PR to upstream with federation extension feedback?
3. Adopt Trust Manifest as our standard identity binding?
4. Track upstream spec change cadence (currently working-group pace)?

## Build (local mirror, optional)

```bash
# uv-run spec builder (matches upstream)
uv run --locked python tools/build_spec.py specification/ai-catalog.md dist/index.html
```

This is for mirroring upstream's published spec site; not needed for our
local catalog generation.
