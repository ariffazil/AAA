# VAULT999 Correction Receipts — Append-Only Workflow (2026-08-08)

Concrete recipe for fixing schema-drift entries in `outcomes.jsonl` without
violating F1 AMANAH (reversibility) or VAULT999's `chattr +a` immutability.

## The trap

VAULT999 `outcomes.jsonl` has mixed schemas — tool_call entries use
`{ts, chain_hash}`; some legacy/loop entries (JUDGE_SEAT_DEPUTY, COMMIT_RECEIPT,
JUDGE_SEAT_UNAVAILABLE, FORBIDDEN_MODEL_FOR_ROLE) use `{timestamp, ..., chain_hash: null}`.
Pre-chain legacy rows (~30K) have no `chain_hash` key at all. `chattr +a` blocks edits.

## The rule

**Never edit, never `chattr -a`. Append a `CHAIN_CORRECTION_RECEIPT` event.**

The correction receipt lists the orphaned line numbers + their content hashes
(SHA-256 of canonical-JSON), declares its own `chain_hash`, and stamps
`reversibility: "F1-REVERSIBLE (append-only)"`. Original entries stay bit-identical.
Reverse path = append another counter-receipt.

## The recipe (worked, 2026-08-08)

### Step 1: Snapshot

```bash
TS=$(date -u +%Y-%m-%dT%H%M%SZ)
cp /root/arifOS/VAULT999/outcomes.jsonl /root/arifOS/VAULT999/outcomes.jsonl.snap-${TS}
lsattr /root/arifOS/VAULT999/outcomes.jsonl   # expect: ----ia--------
sha256sum /root/arifOS/VAULT999/outcomes.jsonl.snap-${TS}
```

### Step 2: Re-count (DRIFT WARNING)

**Counts drift during audits** because emitting loops keep firing.
The 47→50 drift here was the `agi-gate-010-cycle` actor emitting 3 more
`JUDGE_SEAT_DEPUTY_ACTIVATED` entries while the audit was running.
Always re-count immediately before applying:

```bash
grep "JUDGE_SEAT_DEPUTY_ACTIVATED" /root/arifOS/VAULT999/outcomes.jsonl \
  | jq -c 'select(.chain_hash == null) | {line: input_line_number, ts: .timestamp}'
```

### Step 3: Dry-run script

```bash
python3 /root/arifOS/scripts/vault999_deputy_correction.py
# prints receipt preview, NOT appending
```

### Step 4: Apply

```bash
python3 /root/arifOS/scripts/vault999_deputy_correction.py --apply
# appends 1 line to outcomes.jsonl, prints chain_hash
```

### Step 5: Verify

```bash
tail -1 /root/arifOS/VAULT999/outcomes.jsonl | jq '{event, correction_type, entries_corrected, chain_hash}'
# Expect: CHAIN_CORRECTION_RECEIPT, JUDGE_SEAT_DEPUTY_CHAIN_BACKFILL, 50, c4d3ac4d...

# Optional — verify orphan line numbers are listed in the receipt
python3 -c "
import json
with open('/root/arifOS/VAULT999/outcomes.jsonl') as f:
    for line in f:
        e = json.loads(line)
        if e.get('event') == 'CHAIN_CORRECTION_RECEIPT':
            print('corrected lines:', e['entry_line_numbers'][:3], '...')
            print('content hashes:', e['entry_content_hashes'][:3], '...')
            break
"
```

## Working scripts (as of 2026-08-08)

| Script | Purpose | Mode |
|---|---|---|
| `vault999_deputy_correction.py --apply` | 50-entry JUDGE_SEAT_DEPUTY chain backfill | `--apply` flag required |
| `vault999_schema_correction.py --execute` | 39K legacy pre-chain entries (T3 deferred) | Dry-run by default |
| `verify_vault_chain.py` | Canonical Merkle-V3 walker (SEALED_EVENTS/v2 + vault999.jsonl, NOT outcomes.jsonl) | Audit-only |

## What the canonical verifier DOES and DOES NOT cover

`verify_vault_chain.py` walks three ledgers:
- `SEALED_EVENTS.jsonl` (v1, frozen historical)
- `SEALED_EVENTS_v2.jsonl` (v2, active canonical)
- `vault999.jsonl` (live, mixed nested/flat ledger v3)

It does **not** walk `outcomes.jsonl`. So outcome corrections don't reduce the
verifier's `broken_links` count — they reduce it in `outcomes.jsonl` line count
(no, actually they don't, because the original broken lines stay) and produce
an audit-receipt link. The receipt IS the chain linkage for outcomes.

## Push/deploy catch-22 (parallel trap)

After any `scripts/vault999_*.py` commit, `git push origin main` triggers the
deploy guard (GATE 1 E2E tests + GATE 3 drift check). It refuses because
`/opt/arifos/app` is behind source HEAD. `make deploy-local` refuses with
`888_HOLD: local HEAD is not origin/main`. Three paths:

1. `git push --force-with-lease origin main` (T3, needs `ACK_M10_PUSH_BRANCH`).
2. `git reset --soft HEAD~N`, deploy from origin/main, re-apply.
3. Leave local pending, push at next forge cycle.

Don't bypass. Report. Wait for sovereign.

## Reversal (when corrections are wrong)

Append another receipt:

```json
{
  "ts": "<now>",
  "event": "CHAIN_CORRECTION_REVOCATION",
  "actor": "<whoever>",
  "session": "<sid>",
  "revokes_receipt_chain_hash": "<original correction chain_hash>",
  "reason": "..."
}
```

The original orphans stay orphans. The revocation receipt documents the
attempted correction was rolled back. **Never `chattr -a` to edit.** That's T3.

## Numbers from this session (frozen snapshot 2026-08-08T052525Z)

| Bucket | Count |
|---|---|
| Total outcomes.jsonl lines (pre-correction) | 42,403 |
| Total outcomes.jsonl lines (post-correction) | 42,495 |
| Orphaned JUDGE_SEAT_DEPUTY entries (re-counted at apply) | **50** (not 47 — drift during audit) |
| Snapshot SHA256 | a09cca6cd97dbf42749d1f822a2a5598020e5d3520da2831944043b601aab5a8 |
| Correction receipt chain_hash | c4d3ac4d6f5f4b81107749309db11028ade5ca81cc3514dcd264f9d172c3932b |
| Orphan line range | 29464–42241 |
| Orphan timestamp range | 2026-07-30T17:16:21 → 2026-08-08T05:26:06 |
| Commits landed (local) | `6f748f2b8` (wire + schema script), `cb5afef7d` (deputy correction) |
| Commits pushed to origin | None — deploy guard held |
