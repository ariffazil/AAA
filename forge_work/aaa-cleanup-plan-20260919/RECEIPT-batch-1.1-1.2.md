# AAA Cleanup Batches 1.1 + 1.2 — Receipt

## What landed
Two batches committed to feature branch `proposals/orthogonality-v02-hermes-mapping`.

| Batch | Commit | Files | Size moved |
|---|---|---|---|
| 1.1 | `66d7f90a0` chore(cleanup): batch 1.1 — archive tmp artifacts + regenerable codegraph.db | 283 | ~104M (tmp/: 30M, graph/codegraph.db: 74M, 3 audit snapshots: 300K) |
| 1.2 | `666a3cbb4` chore(cleanup): batch 1.2 — archive dated backups snapshots | 128 | ~157M (backups/skill-collapse-20260918: 2.3M, backups/skills/aaa-pre-remerge bundle: 147M, pre-collapse tar.gz: 7M) |

Total moved: **~261M to archive/2026-09-19-aaa-cleanup/**

## What's now in archive/2026-09-19-aaa-cleanup/
```
graph-codegraph/         (FalkorDB db + dated audit logs — regenerable)
tmp-pet1h26*             (PETRONAS PDF/txt dumps — temporary by name)
tmp-ptuk/                 (PT UK tmp dir)
tmp-smd/                  (SMD-related tmp dir)
backups-skill-collapse/   (Sep 18 namespace collapse snapshot + restore script)
backups-skills-bundle/    (Sep 18 git bundle, pre-remerge)
skills-pre-namespace-collapse-2026-09-19.tar.gz  (pre-collapse skills tarball)
```

## What's preserved (live surface)
- `tmp/` — now empty (was 30M, all gitignored so never tracked)
- `graph/` — now 124K scripts/docs only (indexer.py, mcp_audit.py, prune_context.py, query.py, schema.py, watcher.py, fi011_hook.py + 3 .md docs)
- `backups/` — now empty dir, ready for future snapshots
- All other live surfaces untouched (a2a-server/, agents/_external/*, skills/, etc.)

## Validators
- ✅ AAA :3001/health: `healthy`, `deployment_drift: false`
- ✅ arif-fazil.com: HTTP 200, 9499B
- ⚠️ `npm run validate:aaa`: **FAILED** with 7 pre-existing errors (NOT caused by these batches — same state pre-batch)

## Pre-existing npm validate errors (next batch — 1.6)
These are the "redundant/chaos" the user wanted cleaned. They are A2A registry integrity issues:

```
- antigravity: unknown host_binding 'gemini-cli-antigravity'
- 777-forge: A2A registry references unknown agent
- gemini-cli: missing local A2A card 'agents/_external/gemini-cli/agent-card.json'
- openclaw-edge-2026-08: missing local A2A card 'agents/_external/openclaw-edge-2026-08/agent-card.json'
- openclaw-edge-2026-08: A2A registry references unknown agent
- well-known-agent-card: published surface does not match aaa gateway source card
- well-known-agent-legacy: published surface does not match aaa gateway source card
```

Diagnosis path (batch 1.6):
1. Identify where `antigravity`, `gemini-cli`, `openclaw-edge-2026-08`, `777-forge` are referenced
2. Determine if these agents should be (a) re-added, (b) removed from registry, or (c) marked retired
3. Rebuild `well-known-agent-card.json` and `well-known-agent-legacy.json` from current AAA gateway source
4. Re-run validate:aaa until clean

## Code coordination
Codex is concurrently cleaning. Its workspace is `.quarantine-redundancy-2026-09-19/` (don't touch). The 20+ dirty .md files at repo root are codex's bulk edit from 12:07:59 — they remain dirty in the working tree, will be committed by codex separately.

## Not yet touched (remaining batches)
- Batch 1.3 — telegram-miniapp (verify live/dead, then archive 173M node_modules + surface)
- Batch 1.4 — node_modules bloat (gitignored, no action; verify .gitignore covers them)
- Batch 1.5 — skills-retired (4.8M, migrate to archive)
- Batch 1.6 — A2A registry integrity (npm validate fixes — the actual A2A alignment work)
- Batch 1.7 — agent-card verification for all 13 _external cards (build on prior federation-shadow-ack work)
- Phase 2 — git push + production deploy (after all batches)

## Reversibility
All moves are `git mv` operations in tracked archive paths. To reverse any batch:
```bash
git revert <commit-hash>
```
Or to move back manually:
```bash
mv archive/2026-09-19-aaa-cleanup/<path> <original-location>
```

## Trust class
DERIVED — script-driven derivation, archive-not-delete policy followed throughout. Working tree is shared with codex's parallel cleanup, which is acknowledged and bounded by the batch boundary.
