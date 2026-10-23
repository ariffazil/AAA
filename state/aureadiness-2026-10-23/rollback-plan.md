# Rollback Plan — AUTONOMOUS UNDERSTANDING READINESS v1

**generated** 2026-10-23T03:43:34+00:00

Every change this session is additive or file-local. Nothing was deployed, sealed, or paid for.

| change | where | rollback | reversible |
|---|---|---|---|
| `skills-catalog-drift.py` (new) | `/root/AAA/scripts/` | delete the file; no caller depends on it yet | yes |
| 3 recovered reference files | 2 skills' `references/` | delete the 3 files; SKILL.md trigger rows become dead links (harmless) | yes |
| 2 SKILL.md trigger-to-ref edits | live-probe-audit-pattern, claim-receipt-discipline | `git revert 2b8fb199` | yes |
| `site-preflight.py` + SKILL.md binding | `arif-sites-ops/` | `git revert 257a4519` | yes |
| census mirror classification | `/root/AAA/scripts/skills-census.py` | `git revert 257a4519` or restore `.bak-20261023-pre-mirror` | yes |
| readiness artifacts | `state/aureadiness-2026-10-23/` | delete the directory | yes |

**Commits**: 7fa2e439 · 977ed4ef · 257a4519 · 86b456b8 · 2b8fb199.

**Not covered because it did not run**: VAULT999 line repair, any execute/seal call, any KVM4
write, any deploy, any Caddy reload, any identity rebind.

**One-way doors respected**: no VAULT999 append · no force-push · no Caddy reload · no identity
rebind · no deletion of a peer skill.
