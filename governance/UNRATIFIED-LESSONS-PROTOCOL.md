# UNRATIFIED-LESSONS PROTOCOL — Append Triggers + Promotion Rule

> **Status:** ACTIVE protocol (2026-09-12) — operationalizes [S3] of FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1 (F13_RATIFIED_CHAT) · Gate-2 item 3 (U20)
> **Tool:** `scripts/unratified_lessons.py` (append / validate / list) — flock-protected, append-only
> **Grounding:** lane practice UL-001..010 (FI-008, 2026-09-12) · UL-009 sovereign synthesis · UL-010 canonization grading

## Lane discipline

- **Append-only.** Entries are never edited or deleted; corrections and closures arrive as NEW entries with `supersedes` (precedent: UL-006 supersedes UL-003). Numbering gaps are flagged, never renumbered (UL-005 gap observed 2026-09-12 — open lane matter).
- **Concurrent writers are live** (parallel lanes append same-night). All writes go through the tool's `flock` — no hand-edits, no heredoc appends.
- **Schema:** required `id, ts_utc(ISO-Z), lane, class, title, finding, status(UNRATIFIED*|PROMOTED*), recorded_by, session`; evolved optional fields pass through (see tool's `KNOWN_OPTIONAL`).

## MUST-append triggers

An agent discovering any of these appends an entry in the same session as discovery:

| # | Trigger | Precedent |
|---|---|---|
| A | Rollback/revert of a material mutation (including working-tree round-trips that left no trace) | UL-002 (K6), UL-004 |
| B | HOLD escalation that reveals a defect or drift | UL-001 |
| C | Peer-caught bypass attempt (authority invented ahead of mandate) | UL-002, UL-004 |
| D | Verifier/observer downtime discovered | UL-011 (chain_walk dead-at-HEAD ~2.5d) |
| E | Deploy-gap: source ≠ runtime discovered | UL-006 |

Near-misses, warts, and drift findings MAY append. "No file, no scar" is the institutional weakness this lane exists to close.

## Promotion rule (UL → scar)

Per the sovereign synthesis (UL-009, 2026-09-12) — the maturity chain:

```
Narrative → Guardrail → Test → Receipt → Independent Audit → F13 instrument
```

**A scar is not real because it was recorded. A scar is real because future behavior is constrained by it.** Grading follows UL-010: each chain term is graded **Witnessed** (receipt-auditable) or **ASSERTED** (unauditable from this seat); full SEAL requires the IndependentAuditability term closed (UL-010 close_condition is the live example).

Mechanics:
- Promotion is a NEW lane entry: `class=promotion`, `supersedes=<UL-id>`, `scar_ref`, `instrument`.
- The tool **rejects** any promotion whose instrument lacks an F13 marker + date (mirrors doctrine_status_gate R1 — the same law at a different boundary).
- The original entry is never rewritten.

## Declared promotion candidates (not fired — F13 pen)

- **UL-011** — chain complete: guardrail live (cockpit sentinel, `c25202aa2`), test (live probe + review reproduction from raw git object), receipts (commits + FlowReceipts), independent audit (review sha256 `92bbf923…`). Awaiting instrument.
- **UL-002** — already absorbed by the scar lane as SCAR-AGY-001 (`32fa8f126`); a promotion entry is optional bookkeeping.
