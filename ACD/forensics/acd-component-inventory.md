# ACD Component Inventory — consolidated (Phase 111/222)

> Generated: 2026-09-12T06:21:48Z · by 333-AGI reconcile lane · branch `feat/acd-federated-unification`
> Sources: FI-003 probe (preserved: `probe-fi003-inventory-20260912.md`) + 333-AGI first-party verification + corrections.
> Machine-readable: `acd-component-inventory.json` (32 components, hashes, status classes).

## Corrections to the FI-003 probe (first-party verified)

| # | Probe claim | Verified reality |
|---|---|---|
| 1 | C21 "arif-dream.service — DISABLED, not-found" | **WRONG**: `arif-dream.service` EXISTS, triggered by `arif-dream.timer` (enabled), last run 2026-09-09 exit 0. It is the LIVE consolidation path. |
| 2 | C01 "consolidate at engines/dream_engine.py" | **TWO implementations**: `engines/dream_engine.py` (10KB) vs `dream_engine/dreams/consolidate.py` (14KB). The SERVICE runs the latter. Convergence deferred (UNKNOWN_PENDING_EVIDENCE). |
| 3 | C02 symlink → replaced by shim | Shim reverted: silent repoint + broken target (`ACD/core/memory_metabolism.py` never existed). Original symlink restored via git. |
| 4 | C14 reports "MOVE" | Actually COPY: originals remain canonical at `reports/dream-federation-2026-09-12/`. |
| 5 | "Memory index updated (3 entries)" | NOT EVIDENCED in filesystem. UNVERIFIED. |
| 6 | "5/5 tests pass" (claimed) | No test files existed at claim time. Now: **19/19 pytest pass** (real files: `tests/test_contract.py`, `test_governance.py`, `test_memory_contract.py`). |

## Summary by status class

| Status class | Count | Components |
|---|---|---|
| ACTIVE_WITH_RUNTIME_EVIDENCE | 2 | C01 live consolidation · C04 arif-dream.service |
| RUNTIME_VERIFIED | 4 | C14 core · C15 memory · C16 CLI · C18 tests (C32 ACD dir) |
| SCHEDULE_PRESENT | 1 | C05 arif-dream.timer |
| SCHEDULE_DANGLING | 3 | C06-C08 (disabled, missing targets) |
| DOCTRINE_PRESENT | 6 | C12 C13 C26 C27 C28 C31 |
| SCHEMA_PRESENT | 2 | C17 schemas · C25 dream-555 card |
| RECEIPT_PRESENT_UNVERIFIED | 4 | C09 C19 C20 C23 |
| ADAPTER_PRESENT | 2 | C03 symlink · C21 spooler stub |
| STATE_RESIDUE_ONLY | 5 | C10 C11 C22 C24 C29 |
| RUNTIME_PRESENT_UNTESTED | 2 | C02 variant B · C30 distill |
| UNKNOWN | 1 | (any not otherwise classified) |

## Key distinctions (do not conflate)

1. **Possibility generation (ACD)** vs **memory consolidation (arif-dream)**: separate concerns, separate authorities. ACD does not consolidate; consolidation does not dream.
2. **Interactive `/dream_what`** (hermes cognitive-command, LLM-side) vs **scheduled runtime** (systemd): different execution paths; ACD becomes the shared contract.
3. **DREAM (555-ASI) A2A card** (REVIEW/AUDIT agent role) vs **dream engine**: name collision only; do not absorb.
4. **AIO** (adaptation from witnessed consequences) vs **ACD** (possibility search): boundary kept (Article 8).

*Full records: `acd-component-inventory.json`.*
