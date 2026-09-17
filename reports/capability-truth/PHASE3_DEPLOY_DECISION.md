# APEX-777 · PHASE 3 — DEPLOY DECISION PACKET (F13) · 333-AGI 2026-09-18

## The single binary
**Deploy `cb2411928` (memory-mode truth) — yes / hold.**

## What deploys
`arifosmcp/runtime/tools.py` (+36/−9, commit `cb2411928`). Two mechanisms:
1. **Routing derives from the dispatch table** — `v5_native_modes = frozenset(ARIF_MEMORY_MODES)` (13 modes). Fixes the phantom `audit` mode: implemented in `memory_handlers_v5`, advertised in `constitutional_map`, **never routed**.
2. **Registration guard** — advertised enum filtered ⊆ handler `__dispatch_modes__`. The schema physically cannot list a mode the handler lacks. Dormant for undeclared handlers (extension point).

## Evidence
| check | result |
|---|---|
| in-process routing proof | `audit → v5` · `recall → v5` · `banana → legacy` ✓ |
| enum baseline pre-deploy (live, v0.2) | 7 tools advertise **57 mode-values**; **0 declared universes** → enum truth dormant |
| enum check post-deploy (simulated, repo universes) | `arif_memory` **8 ⊆ 13 ✓** · `schema_mismatch: {}` |
| CI gate (STEP 5) | **PASS** — phantom 0 · missing 0 · schema 0 · alias 0 |
| py_compile | clean · script writes backups before any copy |

## Command
```bash
bash /root/arifOS/scripts/deploy-memory-mode-fix.sh --dry-run   # plan only (safe, verified)
bash /root/arifOS/scripts/deploy-memory-mode-fix.sh             # deploy (requires F13)
```
Script is guarded: marker checks, idempotent (refuses if already deployed), backs up live+app, py_compile, restart, health check, universe verify, **auto-rollback** on compile/verify failure. Syncs only the live venv + app copy.

## Pre-deploy test evidence (2026-09-18, repo tree with staged patch)
- Patch-relevant suite (public registry · alias check · capability map gate · tool surface): **all PASS**.
- `27 passed` on core files; wider run: `test_registry.py` failures = environment class (needs model-registry stub / `ARIFOS_REGISTRY_ROOT`, the CI pattern); `test_surface_lock` fastmcp import failure = **pre-existing** (fails in the live venv too — `fastmcp.tools.tool` absent in 4.0.x).
- `test_legacy_modes_are_non_destructive_aliases` — **verified pre-existing on a clean worktree at `6491a4ab0`** (`'arif_init' == 'arif_session_init'` stale expectation; runtime shape is canonical). Not a patch regression.

## Risk / blast radius
**Low.** One file. Reversible (`.bak-333-20260918-deploy` + git revert). Affects only `arif_memory` mode routing + a dormant registration guard. No schema or verdict-semantics change. Restart ≈5 s.

## Not in this deploy (separate decisions)
- **Status-plane semantics** (STEP 4 Options A/B) — F13/888.
- `/opt/arifos/arifosmcp` **skewed lineage** (carries a "C1 FIX 2026-09-17 · tool-degradation ≠ substrate-degradation" variant the live copy lacks) — reconciliation item.
- **6 remaining mode-bearing tools** without declared universes (49 advertised mode-values still unverified-by-declaration) — future passes.

## Verification after deploy (I run immediately)
`capability_truth.py` live enum re-measure (expect `arif_memory` checked 8⊆13) + wire `arif_memory mode=audit` probe + gate PASS.

## Evidence anchors
- Commits: `cb2411928` (patch) · `dc7e09f1e` (gate) · baseline JSONs in `/root/AAA/reports/capability-truth/`
- Backups on deploy: `*.$STAMP` (`bak-333-20260918-deploy`)
