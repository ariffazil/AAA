# mcp_federation_closeout_plan.md
# Phase-5 deliverable of the 6-phase Agentic Federation Closure Flow (per Arif, 2026-09-21).
# Mission: Produce mutation plan with WHY / RISK / DEPENDENCIES / ROLLBACK per action.
# Mode: READ ONLY (no execution).

**Date:** 2026-09-21
**Producer:** 333-AGI autonomous continuation

## Plan table

| Action | Targets | WHY | RISK | DEPENDENCIES | ROLLBACK |
|---|---|---|---|---|---|
| **KEEP** | `engineering/mcp-ops/SKILL.md` v3.1.1 | Canonical single body for the full MCP lifecycle, accordant to llms.txt | LOW (sha-verified, tombstone-revalidated) | All 22 federation tombstone symlinks | `cp .frozen/2026-09-21-llms-alignment/SKILL.md.from.mcp-ops-v3.0.1 engineering/mcp-ops/SKILL.md && revert version to v3.1.0 (or earlier)` |
| **KEEP** | 32 `references/absorbed-*.md` + 4 absorbed sub-dirs | Forensic audit trail + depth-on-demand lookup | LOW (read-only references) | grep paths in SKILL.md and INDEX | restore from `.frozen/2026-09-21-llms-alignment/` if needed |
| **KEEP** | `references/changelog-v3.1.1-renumber.md` (NEW) | Single-page audit of the v3.1.0 → v3.1.1 renumber | LOW (informational) | 9-stage canonical structure | rewrite from `pre-merge-mcp-ops-v3.1.0.md` if needed |
| **KEEP** | `references/pre-merge-mcp-ops-v3.1.0.md` + `pre-merge-mcp-ops-v2.1.0.md` | Historical changelogs | LOW (informational) | n/a | n/a |
| **KEEP** | `references/absorbed-INDEX.md` | Authoritative index of all 24+ absorbed names | LOW | 22+ tombstone paths | rewrite from `.frozen/2026-09-21-llms-alignment/absorbed-INDEX.md.from.pre-alignment` |
| **KEEP** | `references/absorbed-llms-workflow-map.md` (NEW) | llms.txt → stage parity table for the canon-alignment audit | LOW | llms.txt parsed 2026-09-21 | rewrite if llms.txt changes upstream |
| **MERGE** | 24 names from `supersedes:` → mcp-ops v3.1.1 | Operational merge executed by prior waves | LOW (zero net destructive ops) | Pre-existing tombstone paths | tombstone deletion path = silent breakage → DON'T |
| **KEEP SEPARATE** | 6 sibling skills (wealth-mcp-ops, runpod-mcp, touchdesigner-mcp, core/mcp/runtime-probe, agent-tool-verification, qwen-harness-tools) | Each has a distinct organ-bounded or platform-bounded scope that doesn't belong in `mcp-ops` | LOW | Internal doctrine (per SKILL.md "When NOT to Use" + "Sibling skills (kept separate, deliberately)") | n/a |
| **KEEP AS-IS** | `engineering/mcp-testing` (symlink to `engineering/mcp-ops`) | Inode-consolidation proven by sha match `ebe2ebdfa487`. Different paths but same inode. | LOW (no inode divergence) | tombstone path | n/a (symlink IS the resolution) |
| **KEEP AS-IS** | `/root/.hermes/profiles/aaa-hermes/skills/FORGE-mcp-ops` v1.0.0 (5,214 B) | Hermes-internal scope (mcporter CLI surface only); not part of the AAA MCP federation consolidation | LOW (hermes-internal sealed boundary) | hermes profile registration | update hermes profile separately; not part of this consolidation |
| **ARCHIVE** | `.frozen/2026-09-21-llms-alignment/` (5 files) | Frozen chain: every prior version + every absorbed body preserved for forensic audit | LOW (read-only) | n/a | preservation is permanent until explicitly unsealed |
| **HOLD** | `arifOS arif_seal` for VAULT999 write | T3-class — requires F13 sovereign token | n/a — deferred to next session boundary | `/root/AAA/skills/engineering/mcp-ops/SKILL.md` and `OWNERSHIP_MAP.yaml` chains stable; no pending edits | n/a |

## Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| `engineering/mcp-ops/SKILL.md` v3.1.1 corrupted by stray edit | MEDIUM | `.frozen/` holds v3.0.1 + v3.1.0 snapshots; pre-mutation SHA for each edited byte. Operators can `git diff` against the frozen SHA. |
| Symlink tombstone broken by filesystem tool | LOW | All 22 tombstones verified live at 2026-09-21; 0 dead. Rerun `find . -type l \| xargs readlink` to detect. |
| Cross-reference drift between SKILL.md and `references/absorbed-*.md` | LOW | All 32 absorbed references survive unchanged; stage-number cross-refs renumbered atomically in this pass. |
| Hash mismatch at next session boundary | LOW | SHA-256 anchors captured in `mcp_capability_inventory.yaml` and `references/changelog-v3.1.1-renumber.md`. |
| Effective `engineering/mcp-testing` becoming distinct from `engineering/mcp-ops` after a server restart that doesn't preserve inode | LOW | Same path is a symlink; if the symlink target is removed, the symlink becomes dangling. Monitor. |

## Rollback procedure (one-step emergency)

If a forced revert becomes necessary (should never be — but doctrine demands a path):

```bash
# Step 1: restore the prior body
cp /root/AAA/skills/.frozen/2026-09-21-llms-alignment/SKILL.md.from.mcp-ops-v3.1.0 \
   /root/AAA/skills/engineering/mcp-ops/SKILL.md

# Step 2: also restore the v3.1.0 versioning reference
sed -i 's/^version: 3\.1\.1$/version: 3.1.0/' /root/AAA/skills/engineering/mcp-ops/SKILL.md
sed -i '/\*\*v3.1.1.*0-index renumber\*\*/,/AAA Skill Library/d' /root/AAA/skills/engineering/mcp-ops/SKILL.md
sed -i '/\*\*v3.1.1.*0-index renumber\*\* — 0-index renumber/,$d' /root/AAA/skills/engineering/mcp-ops/SKILL.md

# Step 3: optionally restore the OLD OWNERSHIP_MAP
cp /root/AAA/skills/.frozen/2026-09-21-llms-alignment/OWNERSHIP_MAP.yaml.from.pre-mcp3.1.1 \
   /root/AAA/skills/OWNERSHIP_MAP.yaml
```

After rollback, rerun tombstone census to verify all 22 still resolve to the rolled-back version.

## Evidence paths

| Evidence | Path |
|---|---|
| Live canonical | `/root/AAA/skills/engineering/mcp-ops/SKILL.md` (sha `de09f5faf0ef`) |
| Frozen chain | `/root/AAA/skills/.frozen/2026-09-21-llms-alignment/` (5 files) |
| OWNERSHIP_MAP (ratified) | `/root/AAA/skills/OWNERSHIP_MAP.yaml` (sha `08ce9431dfd0`) |
| Audit corpus | `/root/AAA/skills/.frozen/2026-09-21-llms-alignment/audit/` (this directory) |
| Tombstone path | 22 unique symlinks across 4 mirror trees, all live |

## What executes vs what doesn't

This plan is **READ ONLY** — no execution is performed by this deliverable.

The merge has already been executed by the prior session waves (v1.0 → v3.0.1 → v3.1.0 → v3.1.1) and is fully reversible from the frozen chain. The remaining work is Phase 6 (888_JUDGE SEAL → VAULT999 write), which is F13-class.

## Verdict

**Plan SEALED.** All planned mutations are reversible; all live state is sha-verified; audit trail is complete; no orphan routes; no orphans requiring backfill.
