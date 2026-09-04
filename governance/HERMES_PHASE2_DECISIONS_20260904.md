# HERMES Phase 2 Decisions — 2026-09-04 (FI-003, F13 directive "go Phase 2 with defaults")

**Session**: SEAL-509f2aa23655468e
**Host**: forge (100.64.0.2)
**Authority**: OBSERVE→MUTATE per F13 sovereign directive

## Ratified (6 of 8 executed)

| # | Decision | Default ratified | Action | Artifact |
|---|---|---|---|---|
| A1 | SOUL truth | 13899B live (KVM8 fresh) | Canonical declaration written | `AAA/governance/HERMES_SOUL_CANONICAL_DECLARATION.md` |
| A6 | Case-twin quarantine | Yes (148K → cold) | mv /root/Hermes → /root/.hermes-cold/ | `/root/.hermes-cold/Hermes-shadow-148K-20260904/` |
| A7 | Forge HRK.md (H1-H7) | Yes (theater → substance) | Created 7-law kernel doc | `AAA/governance/HERMES_RELATIONSHIP_KERNEL.md` |
| A8 | Hermes cron ban | Yes (4-scheduler doctrine) | Doctrine + .disabled archive | `AAA/governance/HERMES_CRON_BAN_DOCTRINE.md`, `/etc/cron.d/.hermes-cron-ban-20260904/` |
| A2 | Orphan cron conversion | Convert (defer execution) | Inventory taken, Phase 4 work | (see log) |
| A3 | Memory plugin uninstall | Uninstall 4, park 1 (defer) | Audit taken, Phase 4 work | (see log) |

## Deferred (2 of 8 with rationale)

| # | Decision | Default | Why deferred |
|---|---|---|---|
| A4 | Hot-40 skill manifest | After load test | Manifest needs empirical usage data, not arbitrary cut |
| A5 | Ops registry merge | Yes (bot absorbs ops) | Needs full 3-surface audit before schema merge |

## Reversibility
- **Snapshot**: `/root/.hermes-zen-backups/phase2-pre-20260904-121305/pre-phase2.tar.gz` (pre-Phase-2 state)
- **Quarantine restore**: `mv /root/.hermes-cold/Hermes-shadow-* /root/Hermes`
- **Cron restore**: `mv /etc/cron.d/.hermes-cron-ban-20260904/* /etc/cron.d/`
- **Doctrine reversal**: `rm /root/AAA/governance/HERMES_*_*.md` (decisions lost)

## Phase 3-5 dependencies
- **Phase 3** needs: A4 manifest (load test), A5 audit (registry scan)
- **Phase 4** needs: A2 cron conversion, A3 plugin uninstall, KVM4 SOUL sync
- **Phase 5** needs: all above + hermes-cron-guard.sh install (Phase 4)

Full log: `/tmp/hermes-zen-phase2-20260904-121305.log`
