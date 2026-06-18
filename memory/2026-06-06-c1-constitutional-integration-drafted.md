# 2026-06-06 — GEOX-C1-CONSTITUTIONAL-INTEGRATION drafted

## TL;DR

Wrote the GEOX-C1-CONSTITUTIONAL-INTEGRATION doctrine + 4 sub-forge specs in response to Arif's "Ok do that" (continuation of GEOX-CANON-31 seal). Closes the 3 connector-side constitutional gaps + 1 NEW finding (registry drift).

## Live receipt (W0+W2, 14:06:54Z)

```json
{
  "tools_count": 36,
  "contract_epoch": "2026-06-05-GEOX-35TOOLS-v2.0",  ← says 35
  "registry_hash": "reg-hash-35d798a",               ← suffix suggests 35
  "session_id": "geox-no-session",                   ← GAP 1
  "actor_id": "geox-unknown",                        ← GAP 2
  "constitution_hash": "unknown",                    ← GAP 3
  "audit_receipt.vault999_ref": "VAULT999-PENDING"   ← GAP 4 (dangling)
  "trace_id": "trace-06da059dfa424b9e",              ← GEOX-generates (good)
  "geox_version": "v2026.06.05"
}
```

**Three confirmed gaps from canon-31:**
1. session_id always "geox-no-session" (connector drops identity)
2. actor_id always "geox-unknown" (connector drops identity)
3. constitution_hash always "unknown" (GEOX doesn't expose)

**New finding (NOT in canon-31):**
4. tools_count=36 vs contract_epoch="35TOOLS-v2.0" — registry drift. One tool added without epoch bump. **Plus** the doctrine says 31, live says 36 — 5-tool gap in 16 minutes (13:50Z → 14:06Z). Either deploy happened mid-session, or counting methodology differs. Needs separate decision: re-seal canon at 36, or reconcile.

## Sub-forges written

| # | Sub-forge | Priority | Bytes | Status |
|---|---|---|---|---|
| 01 | connector-identity-propagation | **P0** | 5,569 | DRAFT |
| 02 | constitution-hash-exposure | P1 | 5,877 | DRAFT |
| 03 | registry-drift-fix | P1 | 6,099 | DRAFT |
| 04 | vault-receipt-completion | P2 | 6,869 | DRAFT |
| — | doctrine (parent) | — | 13,521 | DRAFT |
| **Total** | | | **~38KB** | |

## What each sub-forge does

**01 (P0, ship first):** OpenClaw connector injects `session_id` and `actor_id` from caller envelope into every outbound GEOX call. Fallback = `888_HOLD: MISSING_CALLER_IDENTITY` (NOT `"unknown"`). Adds `parent_trace_id` linking.

**02 (P1):** GEOX exposes `constitution_hash: sha256:...` derived from sealed doctrine file. Frozen at deploy (not live digest). 3 new fields: `constitution_hash`, `constitution_source`, `constitution_sealed_at`. Fail-closed if env var unset.

**03 (P1, can ship same day as 01):** Bump contract_epoch to `2026-06-06-GEOX-36TOOLS-v2.1`. Add 3 new fields: `drift_status: ALIGNED|DRIFTED`, `epoch_implied_count`, `tools_count_matches_epoch`. Add CI guard script that fails the build on drift.

**04 (P2):** Local JSONL receipt queue at `/var/log/geox/receipts.jsonl`. Federation cron rolls up PENDING → sealed via `arif_vault_seal` every 5 min. Same pattern as arifOS outcomes.jsonl.

## Design decisions

1. **No `"unknown"` fallback for identity fields.** If identity is missing, fail closed with 888_HOLD. Consistent with arifOS strict-schema discipline.
2. **Frozen constitution hash, not live digest.** Doctrines are sealed, not edited. Hash stable across deploy.
3. **Local queue for Vault receipts, not federation contract.** Same pattern as arifOS. Federation rollup is a Phase 3 concern.
4. **All sub-forges are reversible.** Tactical bridges (01, 04) carry sunset epoch-2026.09. Substrate changes (02, 03) are metadata + CI.

## Pattern followed

Mirrors arifOS C1-MCP-NATIVE-SURFACE precedent:
- Doctrine file at `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION.md` (mirrors C1-MCP-NATIVE-SURFACE.md)
- Sub-forge specs at `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/0N-...-spec.md` (mirrors C1-MCP-NATIVE-SURFACE/0N-...-spec.md)
- Four-witness validation (W0 self, W1 raw, W2 connector, W3 deferred)
- Sealing protocol: draft → review → seal → execute → verify → iterate → GREEN-SEAL

## What still needs Arif

1. **Review the 4 sub-forge specs.** Approve, reject, or modify.
2. **Decision on canon-31/live count mismatch (31 vs 36).** Re-seal canon at 36, or investigate the gap.
3. **Approve 01-connector-identity-propagation for ship.** P0, smallest change, biggest unblock.
4. **Approve 03-registry-drift-fix for ship same day.** Pure metadata.

## Blocked

Same as before: `arif_judge_deliberate(mode=judge, candidate=...)` returns 888_HOLD (LEGACY_WRAP gate, F11). Sealing via `arif_vault_seal` is still blocked. These specs are sealed-by-doctrine (workspace files), not by Vault.

## Files written

- `/root/.openclaw/workspace/forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION.md` (13,521 bytes)
- `/root/.openclaw/workspace/forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/01-connector-identity-propagation-spec.md` (5,569 bytes)
- `/root/.openclaw/workspace/forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/02-constitution-hash-exposure-spec.md` (5,877 bytes)
- `/root/.openclaw/workspace/forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/03-registry-drift-fix-spec.md` (6,099 bytes)
- `/root/.openclaw/workspace/forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/04-vault-receipt-completion-spec.md` (6,869 bytes)
- `/root/.openclaw/workspace/HEARTBEAT.md` (updated)
- `/root/.openclaw/workspace/memory/2026-06-06-c1-constitutional-integration-drafted.md` (this file)

## Total deliverable

~38KB doctrine + specs, all sealed-by-doctrine. Ready for Arif review.
