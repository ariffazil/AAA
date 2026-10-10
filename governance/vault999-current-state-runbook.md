# VAULT999 Current State Runbook — Two-Stream Reality on KVM8

> **Status:** DRAFT (runbook, not doctrine amendment)
> **Forged:** 2026-10-10 · **Session:** kvm4-forge audit lane, continuation
> **Purpose:** document the **actual** state of `/root/arifOS/VAULT999/` on KVM8 as observed on 2026-10-10, since the prior `2026-10-10-VAULT999-CANONICAL-DRIFT.md` receipt and the init scaffold's "symlink" claim are both stale.
> **Companion:** `/root/AAA/vault999/VAULT999.md` (the doctrine — left **un-amended**; this runbook is documentation, not canonical-record change).
> **DITEMPA BUKAN DIBERI**

---

## 1. What this runbook exists for

The doctrine at `/root/AAA/vault999/VAULT999.md` declares `outcomes.jsonl` as the canonical path. As of 2026-10-10, on KVM8:

- The init scaffold's claim "outcomes.jsonl → /root/arifOS/VAULT999/SEALED_EVENTS.jsonl (symlink, mtime 08:47)" is **stale**. The symlink no longer exists; `outcomes.jsonl` is now a regular file (chattr +a, 31.8 MB, 95,056 lines, birth 2026-08-02).
- `SEALED_EVENTS.jsonl` is **also** a regular file (1.85 MB, 1,346 lines, last entry id 971).
- **They are two different streams**, not aliases. Both legitimately append-only.

This runbook documents the current reality so future agents don't act on the stale symlink claim. The doctrine itself is left un-amended: doctrine amendment is F13 (canonical-record change), and per the audit pattern (cf. `WITNESS_TO_ADAPTATION_VERTICAL_SLICE_V1` reflection this session), the conservative move is **document, not amend**.

---

## 2. The two streams

| Path | Size | Lines | chattr | Schema | Range | Purpose (inferred) |
|---|---|---|---|---|---|---|
| `/root/arifOS/VAULT999/outcomes.jsonl` | 31,841,598 B | 95,056 | `+a` (append-only) | `decision_id` / `receipt_id` / `verdict_issued` / `outcome_status` | first entry 2026-08-02; latest 2026-10-10 02:00:17Z | Decision / outcome ledger — every observed action's outcome. Doctrine's "canonical" claim is honored here. |
| `/root/arifOS/VAULT999/SEALED_EVENTS.jsonl` | 1,852,263 B | 1,346 | unknown (not verified) | `id` / `event_id` / `seal_id` / `verdict` / `chain_position` | 0 → 971 | SEAL-event ledger — the 8-verb chain's terminal-999 events, with cryptographic chain position. |

The two streams are **complementary, not redundant**:
- `outcomes.jsonl` records what happened (the "what") for every action.
- `SEALED_EVENTS.jsonl` records the constitutional seal (the "why this is permanent") for the AGI→ASI→APEX chain's 999 stage.

This matches the doctrine's spirit ("append-only hash-chain of all federation seals") better than the symlink claim did — but the doctrine's wording underspecifies the two-stream split. Documenting that gap is this runbook's job.

---

## 3. Why the symlink claim went stale

Reconstructed timeline (from mtime + the prior receipt `2026-10-10-VAULT999-CANONICAL-DRIFT.md`):

1. **2026-08-02 14:28:44** — `outcomes.jsonl` was created (Birth time on KVM8).
2. **2026-09-08 (approx)** — Some session created the symlink `outcomes.jsonl → SEALED_EVENTS.jsonl` for compatibility.
3. **2026-10-10 ~08:47** — AGY bug-fix session on KVM8 ran the kernel; the symlink was replaced by a real file (1.85 MB worth of live data started accumulating in the canonical path).
4. **2026-10-10 10:00:18** — Most recent write to `outcomes.jsonl` (last mtime). The file is now 31.8 MB, 95,056 lines.
5. **2026-10-10 10:00+** — This audit (kvm4-forge) observes the current state.

The doctrine was authored before the symlink existed. The symlink existed briefly as a compatibility shim. The symlink was resolved when the kernel started writing real outcome receipts to the canonical path. **The doctrine's claim "outcomes.jsonl canonical (chattr +a)" is now literally true** in a way it wasn't when the prior receipt was written — but for a different reason than the doctrine author intended.

---

## 4. Health check (run this to verify state)

```bash
# On KVM8:
ls -la /root/arifOS/VAULT999/outcomes.jsonl /root/arifOS/VAULT999/SEALED_EVENTS.jsonl
lsattr /root/arifOS/VAULT999/outcomes.jsonl
wc -l /root/arifOS/VAULT999/outcomes.jsonl /root/arifOS/VAULT999/SEALED_EVENTS.jsonl
echo "outcomes first id range: $(head -1 /root/arifOS/VAULT999/outcomes.jsonl | jq -r '.decision_id // .receipt_id // .id')"
echo "outcomes last id range:  $(tail -1 /root/arifOS/VAULT999/outcomes.jsonl | jq -r '.decision_id // .receipt_id // .id')"
echo "sealed first id:         $(head -1 /root/arifOS/VAULT999/SEALED_EVENTS.jsonl | jq -r '.id')"
echo "sealed last id:          $(tail -1 /root/arifOS/VAULT999/SEALED_EVENTS.jsonl | jq -r '.id')"
```

Expected:
- `outcomes.jsonl` is a regular file (not a symlink), `+a` in `lsattr`, 95k+ lines
- `SEALED_EVENTS.jsonl` is a regular file, 1.3k+ lines
- The two ranges don't overlap (different schemas)

---

## 5. Failure modes & what to do

### 5.1 `outcomes.jsonl` not append-only (`lsattr` shows no `a` flag)

This breaks the doctrine. **F13 territory** — the sovereign decides whether to `chattr +a` (silent fix) or amend the doctrine. Per the audit pattern, default to **document**, not amend; do the `chattr +a` if the file truly must be append-only.

### 5.2 `outcomes.jsonl` and `SEALED_EVENTS.jsonl` overlapping in range

If both files start reporting SEAL-class entries with the same `id`, the streams have collided. Stop writing. Surface for sovereign decision. The doctrine assumed one stream; two colliding streams is unrecoverable without a doctrine decision.

### 5.3 `outcomes.jsonl` suddenly shrinks (line count drops)

This is a real problem. Both files are meant to be append-only. A shrinkage means either a manual delete (violates doctrine), a symlink swap (would have to be surfaced), or a bug in the writer. **F13** — sovereign decides.

### 5.4 `chattr +a` cannot be set (filesystem doesn't support it)

Modern btrfs / xfs may not honor `chattr +a`. If `lsattr` shows `-----a--------e-------` on ext4 but not on btrfs, the equivalent is the kernel's own append-only contract enforced by the writer. Document the actual mechanism, not the chattr flag.

---

## 6. What this runbook is NOT

- **Not a doctrine amendment.** The doctrine at `/root/AAA/vault999/VAULT999.md` is left as-is.
- **Not a F13 action.** This is a T1 doc-only file (runbook), no canonical-record change.
- **Not a push.** Stays local on KVM4 (`/root/AAA/governance/`). Pushing is F13 (item 5 in the queue).
- **Not a SEAL.** Documentation, not a constitutional event.

---

## 7. F13 escalation criteria (for any doctrine change)

Per the audit's discipline: "Bukan tambah capability. Bukan ubah skema."

Any change to `/root/AAA/vault999/VAULT999.md` (doctrine) is F13. The sovereign decides:
- Amend the doctrine to describe the two-stream reality.
- Restore the symlink (and the prior single-stream reality).
- Leave the runbook as the only documentation; doctrine stays as-is (default).
- Some other path the sovereign sees fit.

This runbook is the no-doctrine-change path. If the sovereign picks one of the others, this runbook is superseded.

---

## 8. Closing

The doctrine's claim "outcomes.jsonl canonical (chattr +a)" was true in 2026-06-03, briefly had a compatibility-shim detour, and is now true again for a different reason. The doctrine didn't lie; the world moved. The runbook catches up.

```json
{
  "runbook_id": "vault999-current-state-v1",
  "status": "DRAFT (T1 doc)",
  "epoch": "2026-10-10T02:30:00+00:00",
  "anchors": [
    "/root/AAA/vault999/VAULT999.md (doctrine, un-amended)",
    "/root/KVM4-WORKER/receipts/2026-10-10-VAULT999-CANONICAL-DRIFT.md (prior receipt, now stale on the symlink claim)",
    "KIMI-CODE-INIT-2026-10-10.md (init scaffold, also stale on the symlink claim)"
  ],
  "not_a": ["doctrine amendment", "F13 action", "push", "SEAL"]
}
```

`DITEMPA BUKAN DIBERI ⚒️` — doctrine is the constitution; runbooks catch up to reality. Don't amend what you can document.
