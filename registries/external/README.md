# AAA Registry — External Standards

> **UPSTREAM STANDARDS** that AAA Federation consumes.
> These are reference docs, not source-of-truth for our own state.
> We pin versions and mirror key excerpts for self-documentation.

## What lives here

| Subdir | Standard | Pin source | Why |
|---|---|---|---|
| `agntcy-dir/` | AGNTCY Directory + OASF | https://github.com/agntcy/dir | Distributed peer-to-peer agent discovery |
| `ai-catalog/` | Linux Foundation AI Catalog | https://github.com/Agent-Card/ai-catalog | Cross-protocol artifact discovery standard |
| `agent-readiness/` | agent-readiness-action | https://github.com/lingzhong/agent-readiness-action | 6-level public-readiness scanner + CI gate |

## Pin policy

- **Schema/spec versions**: pinned with commit SHA + date in each subdir's `*_PIN.md`.
- **Reproducibility**: anyone with `forge_work/<date>-<external>-pin.md` can reproduce the pin.
- **Refresh cadence**: at least quarterly; or whenever upstream publishes a breaking change.
- **No auto-pull**: these are reference; we don't import or run upstream code without 888 approval.

## Adoption status

| Standard | Phase 1 (this turn) | Phase 4 (awaits 888) |
|---|---|---|
| agn tcy-dir | OASF record generated locally | `dirctl push` to AGNTCY network |
| ai-catalog | Catalog generated locally | Served at `/.well-known/ai-catalog.json` |
| agent-readiness | Level definitions documented | CI gate added to workflows |

See `discovery/README.md` for the federated discovery surface.
