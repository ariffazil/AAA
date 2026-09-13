# F13 Chat Ratification — 2026-09-12 (Lane B Receipt of Sovereign Selections)

> **Lane:** RECEIPT (Lane B) — chat-directive record per the F13_RATIFIED_CHAT house pattern.
> **Actor:** kimi-code FI-008 (sovereign chat channel, structured multi-select answered directly).
> **Forged:** 2026-09-12T15:35Z (23:35 MYT).
> **Scope note:** These are chat-directive receipts, NOT kernel SEALs. The kernel F13
> cryptographic path remains blocked by the signing-lane key drift
> (`signing-lane-key-drift-20260912T1535Z.md`). No SEAL vocabulary is claimed.

## 1. The directive

Sovereign was presented the queue from `sovereign-decision-20260912T2244Z.md` and selected,
via structured chat answer: **"5.1 + 5.9: ratify via :18900"**, **"5.8 / 5.4 / 5.7:
chat-ratify doctrine"**, and **"5.2: KVM8 cron migration"**. This file records the doctrine
lane (5.4, 5.7, 5.8). The signing lane (5.1/5.9) is recorded in the key-drift finding.
The KVM8 lane (5.2) is recorded in `kvm8-jobs-phase2-plan-20260912T1535Z.md`.

## 2. Ratified items

### 5.4 — G / W³ floor exceptions: RATIFIED as documented exceptions

- G=0.51 and W³=0.74 are ratified as **documented exceptions**, not new floors.
- Live at ratification time: G=0.5092, W³=0.7439 (arifFlow vector, witnessed this session).
- Task-map proposed a 30-day window (`AGENTIC-STATE-TASK-MAP-2026-09-11.md` line 263);
  the sovereign selected the bundle as presented — window assumed 30 days unless
  corrected. R-1/R-2 exception status: recorded. Floor targets (0.80/0.75) unchanged.

### 5.7 — Init-to-seal autonomous upgrade: RATIFIED to proceed

- Audit basis: `/root/forge_work/2026-08-26-FI-003-init-to-seal-audit.md` (7 wires + 13 findings).
- Status: ratified to implement per the audit's own wire plan and findings.
- Caveat: wires that depend on kernel SEAL privilege are physically blocked by the
  key drift until Option B/A/C is chosen; implementation should sequence around them.

### 5.8 — PATCH-LIFECYCLE-001-revocation: RATIFIED

- `/root/AAA/governance/PATCH-LIFECYCLE-001-revocation.md` (10195B) moves
  `DRAFT_AWAITING_F13 → F13_RATIFIED_CHAT`.
- Effect: REVOKED becomes a first-class lifecycle state; revocation_condition[] schema
  field canonical; Receipt/Seal layer separation codified; skill cannot self-revoke;
  death-law symmetry added. R-16 and R-17 (sticky-capability opt-out sub-ask) may
  proceed to implementation as Lane B work.
- ATTESTED-boundary note from the prior session stands: transition to REVOKED at the
  ATTESTED boundary still requires sovereign ack per the patch's own text.

## 3. Receipt

```
verdict_class: RECEIPT (Lane B) — F13 chat-directive ratification record
ratified:      5.4 (G/W³ documented exceptions, 30-day window assumed),
               5.7 (init-to-seal upgrade proceed), 5.8 (PATCH-LIFECYCLE-001)
channel:       sovereign structured chat answer, kimi-code FI-008, 2026-09-12
not_claimed:   kernel SEAL, judge_state_hash, VAULT999 append (blocked: key drift)
cross_ref:     sovereign-decision-20260912T2244Z.md, signing-lane-key-drift-20260912T1535Z.md
```

DITEMPA BUKAN DIBERI ⚒️
