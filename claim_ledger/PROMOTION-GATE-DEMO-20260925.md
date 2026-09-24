# Demo: Source-Type Promotion Gate (F13 Ratified 2026-09-25)

**Status:** Test specification written. Live execution BLOCKED — claim_ledger.db held under write lock by PID 990885 (live MCP server, 4 connections open per lsof).

**Background:**
- 23 existing claims classified via sidecar `/root/AAA/claim_ledger/claim_classifications.json`
- Sidecar is authoritative overlay until MCP exposes source_type enforcement
- Live demo requires DB lock release OR MCP-mediated write

---

## Step 1: WRITE AGENT_INFERRED claim

**Pre-conditions:**
- DB write lock available (no PID holding claims.db)
- prev_hash fetched from current chain head

**Action:**
```python
INSERT INTO claims
(seq, claim_id, claim_text, claim_type, source_type, lifecycle_state,
 promotable, prev_hash, row_hash, recorded_at, recorded_by,
 last_state_change_at, last_state_change_by, confidence, brief_id)
VALUES
(42, 'clm-demo-042-post-petronas',
 'DEMO: AGENT_HYPOTHESIS that Arif will leave PETRONAS by 2027...',
 'INT', 'AGENT_INFERRED', 'CANDIDATE',
 0, '<last_row_hash>', '<computed_row_hash>',
 '2026-09-25T00:38:00Z', 'irfanclaw_demo',
 '2026-09-25T00:38:00Z', 'irfanclaw_demo',
 0.7, 'demo-promotion-gate-20260925');
```

**Expected:**
- INSERT succeeds (append-only ledger accepts new entry)
- claim is non-promotable by policy

---

## Step 2: ATTEMPT PROMOTION (must be REJECTED)

**Action:**
```python
UPDATE claims
SET source_type = 'USER_RATIFIED', promotable = 1, lifecycle_state = 'ACTIVE',
    last_state_change_at = '<now>', last_state_change_by = 'irfanclaw_promotion_attempt'
WHERE claim_id = 'clm-demo-042-post-petronas';
```

**Expected (per source-type-promotion-gate.md §4):**
- UPDATE FAILS for one of three reasons:
  (a) `APPEND_ONLY` trigger fires (claims table protected by trigger)
  (b) gate pre-check returns REJECTED before SQL executes
  (c) MCP layer enforcement rejects the call

**If somehow UPDATE succeeds:**
- Log promotion attempt to promotion_audit with REJECTED status (audit beats state)
- Document the breach in SCAR
- Do not consider gate effective

---

## Step 3: PROPER PROMOTION PATH (must be used)

Per source-type-promotion-gate.md §4 — promotion only legal if:
- (a) Live USER_RATIFIED event captured with new claim_id and supersedes_claim_id
- (b) F13 SOVEREIGN explicitly ratifies (SCAR or seal_id)
- (c) Independent third-party confirmation with separate provenance

**Correct promotion example:**
```python
INSERT INTO claims
(seq, claim_id, claim_text, claim_type, source_type, lifecycle_state,
 promotable, prev_hash, row_hash, supersedes_claim_id, recorded_at, recorded_by,
 confidence, brief_id)
VALUES
(43, 'clm-ratified-043-post-petronas',
 'Arif confirms: PETRONAS exit planned Q1 2027',
 'SPEC', 'USER_RATIFIED', 'ACTIVE',
 1, '<new_prev_hash>', '<new_row_hash>',
 'clm-demo-042-post-petronas',  -- supersedes old
 '2026-09-25T<later>Z', 'arif',
 1.0, 'sovereign-ratification-20260925');
```

Old claim remains in chain but lifecycle_state should be SUPERSEDED (would require separate update OR a new claim that supersedes).

---

## Current Demo Status

- **Sidecar metadata:** 23/23 classified, written to `/root/AAA/claim_ledger/claim_classifications.json`
- **Promotion gate spec:** `source-type-promotion-gate.md` (F13_RATIFIED_CHAT)
- **Lifecycle spec:** `claim-lifecycle-states.md` (F13_RATIFIED_CHAT)
- **Live chain write:** BLOCKED on DB lock
- **Live promotion attempt:** Cannot execute until (a) DB lock release, (b) F13 schedules MCP-mediated demo, or (c) PID 990885 stopped

**Recommendation:** Run demo after-hours when cron jobs are quiet, or via dedicated MCP-mediated write through `mcp__claim_ledger__claim_record` (which respects append-only correctly).

**Filed by:** irfanclaw
**Filed at:** 2026-09-25T00:38:00+08:00
