# absorbed-INDEX — what `mcp-ops` absorbed, and where the content went

> Created 2026-09-20 by the Wave-1 MCP cluster merge (F13 directive).
> **Nothing was deleted.** Every absorbed skill body is on disk twice: verbatim in `references/`,
> and as the untouched original directory under
> `/root/AAA/skills/.frozen/2026-09-20-mcp-consolidation/`.
> Every absorbed **name** still resolves — as a symlink to `mcp-ops`, not as a separate skill.

## Stage 1 — DISCOVER

| Absorbed name | Original location | Body preserved at | Frozen copy |
|---|---|---|---|
| `mcp-ecosystem-indexing` | `AAA/skills/domains/general/forge/mcp-ops/mcp-ecosystem-indexing` | `references/absorbed-mcp-ecosystem-indexing.md` | `.frozen/2026-09-20-mcp-consolidation/aaa/domains/general/forge/mcp-ops/mcp-ecosystem-indexing` |
| `forge-mcp-registry-publish` | `AAA/skills/domains/general/aaa/catalog-ops/forge-mcp-registry-publish` | `references/absorbed-forge-mcp-registry-publish.md` | `.frozen/…/aaa/domains/general/aaa/catalog-ops/forge-mcp-registry-publish` |

## Stage 2 — PROBE

| Absorbed name | Original location | Body preserved at | Frozen copy |
|---|---|---|---|
| `mcp-organ-probe` | `AAA/skills/governance/mcp-organ-probe` | `references/absorbed-mcp-organ-probe.md` + `references/absorbed-mcp-organ-probe/references/layer-drop-diagnosis.md` | `.frozen/…/aaa/governance/mcp-organ-probe` |
| `mcp-edit-activation` | `AAA/skills/devops/mcp-edit-activation` | `references/absorbed-mcp-edit-activation.md` | `.frozen/…/aaa/devops/mcp-edit-activation` |
| `mcp-transport-fix` | `AAA/skills/devops/mcp-transport-fix` | `references/absorbed-mcp-transport-fix.md` | `.frozen/…/aaa/devops/mcp-transport-fix` |
| `FORGE-mcp-lifeguard` | `.hermes/skills/FORGE-mcp-lifeguard` | `references/absorbed-FORGE-mcp-lifeguard.md` (+ `_meta.json`, `probe.sh`, `liveness.json`) | `.frozen/…/hermes-view/FORGE-mcp-lifeguard` |

## Stage 3 — INTEGRATE

| Absorbed name | Original location | Body preserved at | Frozen copy |
|---|---|---|---|
| `forge-fastmcp` | `AAA/skills/forge-fastmcp` | `references/absorbed-forge-fastmcp.md` | `.frozen/…/aaa/forge-fastmcp` |
| `FORGE-fastmcp` (case-variant) | `.hermes/skills/FORGE-fastmcp` | `references/absorbed-FORGE-fastmcp.md` | `.frozen/…/hermes-view/FORGE-fastmcp` |
| `forge-mcp-gui` | `AAA/skills/forge-mcp-gui` | `references/absorbed-forge-mcp-gui.md` | `.frozen/…/aaa/forge-mcp-gui` |
| `FORGE-mcp-gui` (case-variant) | `.hermes/skills/FORGE-mcp-gui` | `references/absorbed-FORGE-mcp-gui.md` | `.frozen/…/hermes-view/FORGE-mcp-gui` |
| `forge-mcp-a2a-agentic` | `AAA/skills/forge-mcp-a2a-agentic` | `references/absorbed-forge-mcp-a2a-agentic.md` | `.frozen/…/aaa/forge-mcp-a2a-agentic` |
| `FORGE-mcp-a2a-agentic` (case-variant) | `.hermes/skills/FORGE-mcp-a2a-agentic` | `references/absorbed-FORGE-mcp-a2a-agentic.md` | `.frozen/…/hermes-view/FORGE-mcp-a2a-agentic` |
| `external-platform-mcp` | `AAA/skills/domains/general/forge/mcp-ops/external-platform-mcp` | `references/absorbed-external-platform-mcp.md` + `references/absorbed-external-platform-mcp/references/` | `.frozen/…/aaa/domains/general/forge/mcp-ops/external-platform-mcp` |
| `mcp-context-compression` | `AAA/skills/mcp-context-compression` | `references/absorbed-mcp-context-compression.md` | `.frozen/…/aaa/mcp-context-compression` |
| `forge-minimax-mcp-direct-invoke` | `AAA/skills/domains/general/forge/mcp-ops/forge-minimax-mcp-direct-invoke` | `references/absorbed-forge-minimax-mcp-direct-invoke.md` | `.frozen/…/aaa/domains/general/forge/mcp-ops/forge-minimax-mcp-direct-invoke` |
| `telegram-mcp-product-line` | `AAA/skills/domains/general/forge/mcp-ops/telegram-mcp-product-line` | `references/absorbed-telegram-mcp-product-line.md` + `…/references/build-log-2026-08-31.md` | `.frozen/…/aaa/domains/general/forge/mcp-ops/telegram-mcp-product-line` |

## Stage 4 — TEST

| Absorbed name | Original location | Body preserved at | Frozen copy |
|---|---|---|---|
| `mcp-testing` | `AAA/skills/engineering/mcp-testing` | `references/absorbed-mcp-testing.md` | `.frozen/…/aaa/engineering/mcp-testing` |

## Stage 5 — GOVERN

| Absorbed name | Original location | Body preserved at | Frozen copy |
|---|---|---|---|
| `forge-mcp-governance-wrapper` | `AAA/skills/domains/general/apex/governance-core/forge-mcp-governance-wrapper` | `references/absorbed-forge-mcp-governance-wrapper.md` + `references/` + `templates/mcp-governance-policy.toml` | `.frozen/…/aaa/domains/general/apex/governance-core/forge-mcp-governance-wrapper` |
| `federation-mcp-drift-audit` | `AAA/skills/domains/general/apex/governance-core/federation-mcp-drift-audit` | `references/absorbed-federation-mcp-drift-audit.md` + `scripts/mcp_surface_usage_audit.py`, `scripts/mcp_surface_conformance_sweep.py` | `.frozen/…/aaa/domains/general/apex/governance-core/federation-mcp-drift-audit` |

## Not absorbed — preserved here, alias deliberately NOT made

| Name | Why | Preserved at |
|---|---|---|
| `FORGE-mcp-ops` (mcporter) | `mcp-ops` v2.1.0 already declared `supersedes: FORGE-mcp-ops`, but the live copy is reachable only through `/root/.hermes/profiles/aaa-hermes/skills/` (a **different profile** — out of scope for this merge) via the symlink `AAA/skills/capabilities/coding/mcp-ops`. Content preserved; the alias was left for the operator. | `references/absorbed-FORGE-mcp-ops.md` |
| `runtime-probe` | Wave-2 merge product (`core/mcp/runtime-probe`); its own owner, not in this cluster. Kept and cross-linked. | — |

## Duplicate locations found and collapsed

| Path | Was | Now |
|---|---|---|
| `AAA/skills/domains/forge/mcp-testing` | symlink → `AAA/skills/engineering/mcp-testing` | resolves on to `engineering/mcp-ops` |
| `AAA/skills/domains/general/forge/mcp-ops/*` (4 children) | skills inside a namespace dir | 4 alias symlinks → `engineering/mcp-ops` |
| `.hermes/skills/domains/general/forge/mcp-ops/*` | symlinks into AAA | resolve on to `engineering/mcp-ops` |

## This skill's own pre-merge body

`references/pre-merge-mcp-ops-v2.1.0.md` — the 12,322-byte v2.1.0 body (2026-08-26 consolidation of
FORGE-mcp-ops + FORGE-mcp-federation-ops + FORGE-mcp-lifeguard), preserved before the v3.0.0 rewrite.
