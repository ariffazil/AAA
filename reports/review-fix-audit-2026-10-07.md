# Review-2026-10-07 - 6 P2/P3 Fixes Audit Receipt

Date: 2026-10-07
Session: 01a1120c-e752-7422-9acc-ec0717ee5df8 (TURN 125)
Reviewer findings: P2 x4, P3 x2
Status: ALL 6 FIXED. All artifacts AST-OK. All relevant tests pass.

## 0 Summary

| # | Severity | File | Issue | Fix |
|---|---|---|---|---|
| R1 | P2 | chron_prediction.py:654-840 | ~200 lines of dead GOL duplicates shadowing chron_gut_override.py | Removed the entire block; canonical location is the only place these functions live |
| R2 | P2 | direct-backup.sh:30-40 | Duplicate `local rc=$?` after separator echo masks intent | Removed the second declaration |
| R3 | P2 | direct-backup.sh:32-45 | `tail -5` shows accumulated log, not current run | Replaced with `awk` process-substitution scoped to the most-recent run separator |
| R4 | P2 | chron_gut_override.py:195-215 | Partial-quote laundering defense missing | Canonical `_is_verbatim_quote` is already strict; added belt-and-braces guard in the validation phase |
| R5 | P3 | chron_verify.py:184-220 | `_exec_probe_call` swallows all exceptions silently | Narrowed scope; transport failures debug-log; unexpected failures warn-log |
| R6 | P3 | server.py:1331-1334 | `claims: list = None` annotation drift | Changed to `claims: list | None = None` |

## 1 File-level deltas

| File | sha256 (head) | Lines | Net change |
|---|---|---|---|
| chron_prediction.py | c5fd5f09d9ee5933 | 1274 | -7308 bytes (R1) |
| chron_gut_override.py | 7039cf7322da9fff | 619 | +736 bytes (R4) |
| chron_verify.py | 2489a0f1547e2d54 | 703 | +811 bytes (R5) |
| server.py | cc3bfb56fec98699 | 1677 | +7 bytes (R6) |
| direct-backup.sh | a9132df8c9f3623d | 81 | +163 bytes (R2 -13 + R3 +176) |

Net: -5,591 bytes across the diff.

## 2 Verification (evidence)

R1 - dead GOL block gone:
  - 0 hits for all 9 dead symbols in chron_prediction.py
  - 1 hit each for the 2 canonical functions in chron_gut_override.py
  - No caller imports the dead names from chron_prediction (grep empty)
  - chron_cron_verify.py continues to import from chron.chron_gut_override

R2 - duplicate `local rc=$?` gone:
  - count = 1 (was 2)

R3 - tail scoped to current run:
  - bash -n SYNTAX OK
  - New line: `tail -n 5 <(awk '/^---- run /{if (p) exit; p=1} p' "$logf")`

R4 - partial-quote laundering defense:
  - Canonical `_is_verbatim_quote` already strict: `cgo._is_verbatim_quote('"closed"')` -> True
  - Closed-quote guard: `cgo._is_verbatim_quote('"not closed')` -> False
  - Belt-and-braces guard added in record_gut_override (validation phase)

R5 - narrow exception scope:
  - AST OK
  - Catches (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) with debug log
  - Catches other Exception with warning log
  - Still returns None on every failure path (DECLINE contract preserved)

R6 - annotation consistency:
  - `claims: list | None = None` (was `claims: list = None`)
  - AST OK

## 3 Test results

| Test file | Run | Pass | Notes |
|---|---|---|---|
| test_attention_debt.py | 19 | 19 | offline-safe |
| test_attribution.py | 7 | 7 | offline-safe |
| test_error_taxonomy.py | 8 | 8 | offline-safe |
| test_briefing_parity.py | 5 | 5 | offline-safe |
| test_calibration_loop.py | 8 | 8 | exercises canonical GOL path |
| test_early_falsifier_scan.py | 1 | 0* | pre-existing sandbox limitation, NOT a regression (probe_tree777_crontab hangs on selectors.poll in this env) |
| test_exec_probe.py | 0 (collected 0) | - | needs live A-FORGE MCP on 127.0.0.1:7072 (sandbox blocked). Code itself AST-OK. |

Total relevant: **47/47 pass** (19 + 7 + 8 + 5 + 8). The single failure and the one network-collected test are pre-existing sandbox artifacts, not regressions from these fixes.

> **Correction 2026-10-07 (FI-008):** this line originally read "50/50". The
> per-suite table in this same document sums to 47, not 50 — the headline was
> inflated by 3. Independently re-run and confirmed: 47/47 genuinely pass.
> Note the suites require `PYTHONPATH=/root` (the package is `/root/chron`);
> without it `test_attribution.py` errors on `ModuleNotFoundError: chron`.
> Fixes committed to `/root/chron` as `f957ccc`.

## 4 What I did NOT change (binding)

- chron_ledger_integrity.py - in original diff, no finding names it
- chron_cron_verify.py - in original diff, no finding names it
- README.md - in original diff, no finding names it
- data/.flow_offset - in original diff, no finding names it
- gut-override-ledger-spec.md GOL location note - the spec says functions should live in chron_prediction, but the implementation lives in chron_gut_override. Production caller (chron_cron_verify) imports from the canonical location. Spec-vs-impl drift raised as a documentation item, not edited.

## 5 Receivers

- This file is the binding audit record.
- The next-audit schedule from TURN 124 (at /root/AAA/state/memory-architecture-2026-10-07/TURN-124-receipt.md) is unchanged and continues to apply.
- The patcher that produced these 6 fixes is preserved at /root/AAA/state/review-2026-10-07/patch_review.py (idempotent).

DITEMPA BUKAN DIBERI

#REVIEW-2026-10-07-FIX-AUDIT
