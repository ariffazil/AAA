# PATCH PROPOSAL — testimony-gate: WITNESS STATEMENT (6th signal) + SCAR Sanctuary hook

> **Status:** DRAFT_AWAITING_F13 · 2026-09-16 · **Trace:** TRACE-333-20260916-TGM01
> **Proposer:** 333-AGI (build hop for Hermes' proposal, ratified in chat by Hermes audit 2026-09-16)
> **Target:** `/root/AAA/instructions/testimony-gate.md` (currently F13_RATIFIED_CHAT — amendment requires F13)
> **Not applied.** This file proposes; only F13 seal applies.

**Object contract:** `{ state: PRODUCED, prev_state: PROPOSED_IN_CHAT, expected_next: F13_READ → SEAL|DISCARD, owner: F13, evidence_required: post-apply grep (§5) }`

## 1. Provenance

- **OBS** — external cross-AI audit (relayed by Arif 2026-09-16) added two deltas Hermes' table lacked: a distinct *Witness statement* signal type, and a Sanctuary hook on SCAR ("do not turn it into exploitable training signal or a fixed identity label").
- **OBS** — Hermes accepted both as "delta sebenar. Ambil." (2026-09-16, message 3/3) and held from writing because target is canon area.
- **OBS** — `/root/AAA/instructions/sanctuary-invariant.md` exists and is F13_RATIFIED_CHAT — the hook has a ratified anchor to cite, so this is a cross-reference, not new doctrine.

## 2. Proposed diff — signal table

```diff
 | Signal | Destiny | Forbidden |
 |---|---|---|
 | REQUEST | solve | — |
 | QUESTION | explain | — |
 | TESTIMONY | attest | do not optimize |
+| WITNESS STATEMENT | record | do not collapse observation into interpretation; log reporter + vantage |
 | SCAR | witness | do not repair |
+| ↳ SCAR (Sanctuary hook) | witness | never convert to exploitable training signal; never fix as identity label (anchored: `sanctuary-invariant.md`, F13_RATIFIED_CHAT) |
 | CONFESSION | hold | do not judge |
```

Add after the table:

```
TESTIMONY vs WITNESS STATEMENT: testimony is the human's first-person account of
their own experience. A witness statement is a third-party (human or agent) report
about events, people, or systems. A witness statement carries reporter, vantage, and
time — and the reporter may be wrong. Recording ≠ endorsing.
```

## 3. Ordering rationale

Placed TESTIMONY → WITNESS STATEMENT → SCAR → CONFESSION: sensitivity gradient from task to confession. Auditor's original order put Confession before Witness; either is defensible — F13 may reorder without breaking the delta. (INT — judgment call, flagged.)

## 4. Failure mode this patch closes

Without the 6th type, a third-party report has no destiny row: it gets silently classified as TESTIMONY (wrongly attributed as first-person) or as QUESTION (wrongly answered as a task). Both are category errors against humans — the exact class this gate exists to prevent.

## 5. Post-apply verification (for the sealing session)

```bash
grep -c "WITNESS STATEMENT" /root/AAA/instructions/testimony-gate.md   # expect ≥ 1
grep -c "sanctuary-invariant.md" /root/AAA/instructions/testimony-gate.md  # expect ≥ 1
```

Then update the fragment-status table in `/root/AAA/AGENTS.md` if F13 ratifies the amendment.

DITEMPA BUKAN DIBERI ⚒️
