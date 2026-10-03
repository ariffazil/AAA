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

---

## FINAL STATE after the convergence pass (2026-09-20, v3.0.1)

Two agents worked this cluster in parallel. The orchestrator's MCP agent (`/root/forge_work/merge-2026-09-20/_mcp_merge/`)
found the v3.0.0 umbrella already on disk and **completed it instead of duplicating it**:

| Their action | Effect |
|---|---|
| triggers 33 -> 71 | union of all 14 assigned members' declared triggers; `triggers_lost: []` |
| folded `mcp-sota-shopping-list` | `references/absorbed-mcp-sota-shopping-list.md` + **Stage 1b** (procurement lane) |
| archived 13 member dirs | `/root/AAA/skills/.archive/merge-20260920/mcp/<member>/` + tombstone symlinks at the old paths |
| wrote | `alias-mcp.json`, `mcp-receipt.json` in `/root/forge_work/merge-2026-09-20/` |

Their pass also **restored** a number of member directories to their original paths (22:37:32) as part of
its own procedure. Five names that were NOT in its 14-member list were left as real dirs and had their
aliases re-applied by the wave-1 agent:

| Name | Re-applied outcome |
|---|---|
| `forge-fastmcp` | symlink -> `mcp-ops`; restored original preserved at `.frozen/2026-09-20-mcp-consolidation/restored-by-convergence-pass/forge-fastmcp` |
| `telegram-mcp-product-line` | symlink -> `mcp-ops`; original preserved at `.../restored-by-convergence-pass/domains/general/forge/mcp-ops/telegram-mcp-product-line` |
| `federation-mcp-drift-audit` | symlink -> `mcp-ops`; original preserved at `.../restored-by-convergence-pass/domains/general/apex/governance-core/federation-mcp-drift-audit` |
| `wealth-mcp-testing` | symlink -> `wealth-mcp-ops`; original preserved at `.../restored-by-convergence-pass/domains/wealth/forge/mcp-ops/wealth-mcp-testing` |
| `wealth-mcp-tool-hardening` | symlink -> `wealth-mcp-ops`; original preserved at `.../restored-by-convergence-pass/domains/wealth/forge/mcp-ops/wealth-mcp-tool-hardening` |

Two preservation containers therefore hold the same originals: `.archive/merge-20260920/mcp/` (the
orchestrator's convention) and `.frozen/2026-09-20-mcp-consolidation/` (this cluster's convention).
That is deliberate redundancy, not duplication of authorship: content is byte-identical in both.


## Second pass — 2026-09-20 (v3.0.1)

| Absorbed name | Original location | Body preserved at | Archive | Frozen copy |
|---|---|---|---|---|
| `mcp-sota-shopping-list` | `AAA/skills/mcp-sota-shopping-list` | `references/absorbed-mcp-sota-shopping-list.md` (4-line provenance header; body byte-identical) | `.archive/merge-20260920/mcp/mcp-sota-shopping-list` | — |

**Second-pass corrections to this file's own claims**

- The 14 assigned member names are now archived under
  `/root/AAA/skills/.archive/merge-20260920/mcp/<name>/` (all 14 carry a `SKILL.md`) *and* their
  original paths are tombstones resolving to this directory. Between ~22:37 and the second pass those
  paths had been restored as real directories, so the claim "every absorbed name still resolves — as a
  symlink to `mcp-ops`" was temporarily false for 13 of the 14; it is true again for those 13.
- Still **false** for three names this file lists as absorbed, which are outside the second pass's
  member list and were therefore not touched: `forge-fastmcp`,
  `domains/general/apex/governance-core/federation-mcp-drift-audit`,
  `domains/general/forge/mcp-ops/telegram-mcp-product-line` (all still live directories).
- Trigger list corrected: v3.0.0 advertised 33 triggers, which dropped 36 of the members' declared
  triggers (`mcp-testing` 18, `mcp-organ-probe` 9, `mcp-edit-activation` 6, `mcp-ops` 3). v3.0.1
  carries 71 = full declared union (58) + 2 procurement phrases + the 13 legacy siblings' triggers.
