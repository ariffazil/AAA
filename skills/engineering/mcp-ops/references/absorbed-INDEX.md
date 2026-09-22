# Absorbed MCP skills — full index for `mcp-ops` v3.1.1

> **All absorbed skills live as references inside `mcp-ops/`. Their original names resolve as
> symlinks to this directory (see `supersedes:` in `SKILL.md`). Do not re-create them.**

The mcp-ops skill absorbs **24 prior MCP names** across two consolidation waves plus one
llms.txt-alignment pass. Each absorbed skill retains its full body verbatim; the spine SKILL.md
organizes them into the canonical 9-stage workflow. The naming convention follows the AAA
retirement contract:

```
references/absorbed-<name>.md       (the body, where name lives as a research target)
references/absorbed-<name>/         (the body, when it had its own sub-tree)
SKILL.md.from.<tree>                (in .frozen/, timestamped + tree-named to escape census)
```

## Index — name → phase → origin → preserved path

| Name (origin) | Absorbed in | Preserved at | Owner stage |
|---|---|---|---|
| FORGE-mcp-ops | v3.0.0 (2026-08-26) | `.frozen/2026-09-20-mcp-consolidation/` (and earlier) | every stage (the spine itself) |
| FORGE-mcp-federation-ops | v3.0.0 (2026-08-26) | same | Stage 1 + 3 (federation organ discovery + probe) |
| FORGE-mcp-lifeguard | v3.0.0 (2026-08-26) | `references/absorbed-FORGE-mcp-lifeguard.md` | Stage 8g (recovery) |
| FORGE-fastmcp | v3.0.0 (2026-08-26) | `references/absorbed-FORGE-fastmcp.md` + `references/absorbed-forge-fastmcp/` | Stage 3a (server build) |
| forge-fastmcp | v3.0.1 (2026-09-20) | symlink-resolved to mcp-ops | same |
| FORGE-mcp-gui | v3.0.0 (2026-08-26) | `references/absorbed-FORGE-mcp-gui.md` + `.../absorbed-forge-mcp-gui/` | Stage 3b + 7a (Apps) |
| forge-mcp-gui | v3.0.1 (2026-09-20) | symlink-resolved to mcp-ops | same |
| FORGE-mcp-a2a-agentic | v3.0.0 (2026-08-26) | `references/absorbed-FORGE-mcp-a2a-agentic.md` + `.../absorbed-forge-mcp-a2a-agentic/` | Stage 3c + 7 (interop) |
| forge-mcp-a2a-agentic | v3.0.1 (2026-09-20) | symlink-resolved to mcp-ops | same |
| FORGE-mcp-testing | v3.1.0 (2026-09-21) | `.frozen/2026-09-21-llms-alignment/SKILL.md.from.mcp-testing` (content fully absorbed into Stage 5 TEST) | Stage 5 |
| FORGE-mcp-governance-wrapper | v3.0.0 (2026-08-26) | `references/absorbed-FORGE-mcp-governance-wrapper.md` + `.../absorbed-forge-mcp-governance-wrapper/{references,templates}/` | Stage 8e (governance overlay) |
| forge-mcp-governance-wrapper | v3.0.1 (2026-09-20) | symlink-resolved to mcp-ops | same |
| federation-mcp-drift-audit | v3.0.0 (2026-08-26) | `references/absorbed-federation-mcp-drift-audit.md` + `.../absorbed-federation-mcp-drift-audit/scripts/` | Stage 8f (drift audit) |
| mcp-organ-probe | v3.0.0 (2026-08-26) | `references/absorbed-mcp-organ-probe.md` + `.../absorbed-mcp-organ-probe/references/` (layer-drop-diagnosis) | Stage 2a (handshake + misreadings) |
| mcp-edit-activation | v3.0.0 (2026-08-26) | `references/absorbed-mcp-edit-activation.md` | Stage 2d (PID-vs-mtime + two-loader doctrine) |
| mcp-transport-fix | v3.0.0 (2026-08-26) | `references/absorbed-mcp-transport-fix.md` | Stage 2e (SSE → Streamable HTTP) |
| mcp-ecosystem-indexing | v3.0.0 (2026-08-26) | `references/absorbed-mcp-ecosystem-indexing.md` | Stage 1 + 4d (discovery + Skills-over-MCP) |
| forge-mcp-registry-publish | v3.0.0 (2026-08-26) | `references/absorbed-forge-mcp-registry-publish.md` | Stage 7 (PUBLISH) |
| external-platform-mcp | v3.0.0 (2026-08-26) | `references/absorbed-external-platform-mcp.md` + `.../absorbed-external-platform-mcp/references/` | Stage 3 (wiring third-party MCPs) |
| mcp-context-compression | v3.0.0 (2026-08-26) | `references/absorbed-mcp-context-compression.md` | Stage 3g (schema compression) |
| forge-minimax-mcp-direct-invoke | v3.0.0 (2026-08-26) | `references/absorbed-forge-minimax-mcp-direct-invoke.md` | Stage 3c (direct client invoke) |
| telegram-mcp-product-line | v3.0.0 (2026-08-26) | `references/absorbed-telegram-mcp-product-line.md` + `.../absorbed-telegram-mcp-product-line/references/` | Stage 3 (Telegram products on MCP backends) |
| mcp-testing | v3.1.0 (2026-09-21) | symlink-resolved to mcp-ops (no separate body) | Stage 5 |
| mcp-sota-shopping-list | v3.0.1 (2026-09-20) | `references/absorbed-mcp-sota-shopping-list.md` | Stage 1 (procurement) |
| ops-mcp-builder | tombstone only | n/a — operator profile-skill name, never had a body | n/a |
| ops-mcp-probe | tombstone only | n/a | n/a |
| ops-mcp-testing | tombstone only | n/a | n/a |
| ops-mcp-lifeguard | tombstone only | n/a | n/a |
| mcp-dual-era-transport | tombstone (pre-merge) | `references/pre-merge-mcp-ops-v2.1.0.md` (era-mismatch doctrine survives inside Stage 5 era-coverage matrix) | Stage 5 |
| mcp-shopping-list-2026-09 | tombstone (pre-merge) | superseded by mcp-sota-shopping-list | Stage 1 |

## Wave timeline

| Wave | Date | What happened |
|---|---|---|
| **v1.0** | 2026-08-26 | first consolidation: FORGE-mcp-ops + FORGE-mcp-federation-ops + FORGE-mcp-lifeguard → engineering/mcp-ops |
| **v2.0/v2.1** | 2026-08-26 | absorbed 7 more MCP-named skills; pre-merge snapshot at `references/pre-merge-mcp-ops-v2.1.0.md` |
| **v3.0.0** | 2026-09-20 | first big merge: 19 names absorbed. 6-stage spine (DISCOVER → PROBE → INTEGRATE → TEST → GOVERN → RETIRE). 32 reference docs. |
| **v3.0.1** | 2026-09-20 | trigger list completed; `mcp-sota-shopping-list` folded into Stage 1b |
| **v3.1.1** | 2026-09-21 | **0-index renumber per Arif SEAL.** All stages N → N−1 (LEARN=0, DISCOVER=1, PROBE=2, BUILD=3, SECURE=4, TEST=5, EXTEND=6, PUBLISH=7, GOVERN=8; RETIRE = 8h sub-section inside GOVERN). Procurement sub-stage correctly re-parented from LEARN to DISCOVER. v3.1.0 frozen at `.frozen/2026-09-21-llms-alignment/SKILL.md.from.mcp-ops-v3.1.0`. See `references/changelog-v3.1.1-renumber.md`. |
| **v3.1.0** | 2026-09-21 | **this pass**: llms.txt alignment. Spine reorganised to 9-stage canonical workflow (LEARN → DISCOVER → PROBE → BUILD → SECURE → TEST → EXTEND → PUBLISH → GOVERN-RETIRE). `mcp-testing` content absorbed into Stage 5. SECURE, EXTEND, PUBLISH, LEARN newly covered. Frozen v3.0.x in `.frozen/2026-09-21-llms-alignment/`. See `pre-merge-mcp-ops-v3.1.0.md`. |

## Tombstone symlinks currently in production (22+, verified 2026-09-21)

```
/root/AAA/skills/capabilities/coding/mcp-testing                          → mcp-ops
/root/AAA/skills/capabilities/coding/mcp-ops                              → hermes profile (legacy)
/root/AAA/skills/domains/forge/mcp-testing                                → mcp-ops
/root/AAA/skills/domains/forge/mcp-ops                                   → mcp-ops
/root/AAA/skills/domains/forge/mcp-ops.DEPRECATED-2026-09-19              → mcp-ops
/root/AAA/skills/domains/general/apex/governance-core/forge-mcp-governance-wrapper  → mcp-ops
/root/AAA/skills/domains/general/apex/governance-core/federation-mcp-drift-audit    → mcp-ops
/root/AAA/skills/domains/general/aaa/catalog-ops/forge-mcp-registry-publish         → mcp-ops
/root/AAA/skills/domains/general/forge/mcp-ops/external-platform-mcp                → mcp-ops
/root/AAA/skills/domains/general/forge/mcp-ops/forge-minimax-mcp-direct-invoke        → mcp-ops
/root/AAA/skills/domains/general/forge/mcp-ops/mcp-ecosystem-indexing                → mcp-ops
/root/AAA/skills/domains/general/forge/mcp-ops/telegram-mcp-product-line              → mcp-ops
/root/AAA/skills/devops/mcp-transport-fix                                     → mcp-ops
/root/AAA/skills/devops/mcp-edit-activation                                   → mcp-ops
/root/AAA/skills/.archive/mcp-ops                                             → mcp-ops
/root/AAA/skills/forge-fastmcp                                                → mcp-ops
/root/AAA/skills/forge-mcp-a2a-agentic                                        → mcp-ops
/root/AAA/skills/forge-mcp-gui                                                → mcp-ops
/root/AAA/skills/mcp-context-compression                                      → mcp-ops
/root/AAA/skills/mcp-edit-activation                                          → mcp-ops
/root/AAA/skills/mcp-organ-probe                                              → mcp-ops
/root/AAA/skills/mcp-sota-shopping-list                                       → mcp-ops
/root/AAA/skills/mcp-transport-fix                                            → mcp-ops
/root/AAA/skills/engineering/mcp-testing                                      → mcp-ops (inode-level)
/root/AAA/skills/governance/mcp-organ-probe                                   → mcp-ops

(mirrored across /root/.opencode/skills, /root/.agents/skills, /root/.claude/skills)
```

Each symlink resolves to `engineering/mcp-ops/SKILL.md`. **Verified**: 0 dead links across the
4 skill trees at consolidation time (2026-09-21).

## "Why not merged here" — sibling skills kept separate

See SKILL.md "Sibling skills (kept separate, deliberately)" — these have distinct intent that
mcp-ops is the wrong destination for:

| Skill | Why separate |
|---|---|
| `wealth-mcp-ops` | WEALTH-organ MCP tools; organ-bounded. |
| `runpod-mcp` | Runpod platform lane; distinct triggers/setup. |
| `touchdesigner-mcp` | TouchDesigner platform lane; distinct surface. |
| `runtime-probe` | Stage 2c-as-a-tool; one-shot health + schema. |
| `agent-tool-verification` | General tool claim discipline; not MCP-only. |
| `qwen-harness-tools` | Model-side built-in; not MCP at all. |
