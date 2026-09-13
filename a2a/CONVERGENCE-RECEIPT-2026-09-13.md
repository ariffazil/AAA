# APEX-ZEN convergence receipt (READ-ONLY)

> **Status:** RECEIPT · not kernel SEAL · 2026-09-13T06:25Z
> **Mode:** observe. No purge, no Caddy, no key, no push.
> **Against claim:** “EXECUTED & COMMITTED / Zero Drift / all repos clean / 100% blocked”

## Repositories (OBS)

| Repo | Claimed | Live HEAD | Branch | Worktree | vs origin |
|---|---|---|---|---|---|
| arifOS | `4f4554597` | `4f455459771a` **match** | `main` | clean | **ahead 1** (not pushed) |
| AAA | `a7a4a0044` | `6f57db5d02c4` | `main` | **dirty** | **ahead 3** |
| arifFlow | `4d27ede` | `4d27edebdec7` **match** | **`forge/rg2-lineage-reconcile`** not `main` | clean | `main` is `309f12e`, 13 ahead of origin |
| A-FORGE | (none) | `a4ef6b9ba894` | `main` | clean | in sync |

AAA after claimed commit: `6f57db5d0 chore(a2a): sanitize internal ports…` then **uncommitted** this session: `M a2a/CANONICAL_SURFACE.md`, `?? a2a/APEX-ZEN-A2A-MASTER-SPEC.md`.

**“Committed to main across all federation repos” is false.** arifFlow is not on main. AAA HEAD ≠ claimed SHA. AAA is dirty.

## Supply chain (OBS)

`@z_ai/mcp-server@0.1.4` is in `AAA/registries/supply_chain_pins.json` (pin dated **2026-08-25**, not a new seal). Live configs also show `@0.1.4`:

- `/root/.claude/settings.json`
- `/root/.config/opencode/opencode.json`
- `/root/.qwen/settings.json`

No `@z_ai/mcp-server@latest` found in those watch paths. Lockfile / deployed-image integrity: **not verified this receipt**.

## A2A public surface (OBS)

| Probe | Result |
|---|---|
| `GET …/.well-known/agent-card.json` | 200, 14839 B, sha256 prefix `70f483c908aa07d8` |
| `protocolVersion` | **`1.2`** (not a valid A2A wire version) |
| advertised JSON-RPC URL | `https://aaa.arif-fazil.com/a2a` |
| leak `:8088` | **still present** |
| leak key fingerprint | **still present** |
| later commit `6f57db5d0` claims sanitize | **not reflected on the live Caddy disk card** |

Live runtime remains `aaa-a2a.service` → `a2a-server/server.js`.

## Memory sanctuary / Pilihan A (OBS)

Denylist `/root/arifOS/config/memory-sanctuary-denylist.json`  
hash `sha256:dd8e1d582a299163e55a1b4b9f958f82895ec78a69cdc183b26e3eeefc582d50`  
count **3** IDs (not two). Rule: deny operational and historical recall. **No payloads read.**

Tests this session:

| Suite | Result |
|---|---|
| AAA `contracts/memory/test_admissibility.py` | **8 passed**, 3 warnings (receipt said 7 passed, 1 skipped — **mismatch**) |
| arifOS `tests/constitutional/test_memory_sro_admissibility.py` | **20 passed**, 3 warnings (matches receipt count) |

Negative-access across RAG/A2A/MCP/backups: **not fully matrixed**. A remediation backup file still exists under `forge_work/`. “100% blocked” remains an **objective**, not a proof.

## Runtime (OBS)

| Item | Result |
|---|---|
| `hermes-asi-gateway` | active, MainPID **1736251** (matches receipt) |
| MemoryCurrent | 526204928 (~502 MiB; receipt said ~488M) |
| WELL | degraded (prior `now --json`) |
| Merkle / WELL biometrics / open ledgers | not mutated this session |

## Verdict

```yaml
verdict_class: RECEIPT
lane: B
converged: false
deviations:
  - AAA_HEAD_NOT_CLAIMED_SHA
  - AAA_WORKTREE_DIRTY
  - ARIFFLOW_NOT_ON_MAIN
  - PUBLIC_CARD_STILL_LEAKS_AND_SAYS_1.2
  - SANITIZE_COMMIT_NOT_DEPLOYED_TO_CADDY_DISK
  - TEST_COUNT_MISMATCH_8_PASS_NOT_7_SKIP_1
  - ZERO_DRIFT_OVERCLAIM
holds:
  merkle_lane: 888_HOLD
  well_biometrics: 888_HOLD
  medical_purge: 888_HOLD   # Pilihan A stands
  caddy_reload: 888_HOLD
```

Pilihan A (quarantine, no purge) is the live denylist policy. That part of the receipt is **directionally true**. The rest of “zero drift / all clean / fully sealed” is not.
