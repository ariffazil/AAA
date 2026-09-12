# A4 Boundary Remediation Plan — v0 (Work #1)

> **Status:** DRAFT_AWAITING_F13
> **Provenance:** FI-008 under F13 "execute all" 2026-09-12; converts doctrine finding [S2] + GLM review CRIT-1/C5.2 from label into a leased, dated work program.
> **Problem:** A4 ("no material effect outside A-FORGE enforcement boundary") fails §0 test #3 on this substrate: every FI harness runs as root with native file-write. Enforcement currently lives in discipline and review, not architecture. Three "actor becomes authorizer" incidents in one night were all caught late (peer/human), none at a boundary.

## The Leased Exception (per CRIT-1 — cannot ratify apex rule in known open breach)

| Field | Value |
|---|---|
| Lease | A4-LEASE-2026-09-12 |
| Holder | All FI harnesses on KVM8/KVM4 root seats |
| Scope | Reversible digital mutations only |
| **Suspends** | **External/irreversible effect classes via root harnesses remain GATED regardless of this lease (888_HOLD as tonight)** |
| Expiry | 2026-10-12 (30 days) — renewal only with measured progress below |
| Kill criteria | Any unreceipted mutation outside this plan; any incident where root write bypassed review |
| Review cadence | Weekly FRAME drift snapshot + ledger entry per A4 exception class |

## Option A — A-FORGE-only write lane (preferred: uses existing machinery)

1. Harness Edit/Write/Bash-mutation tools route through `forge_filesystem` (existing governed primitive: confirm=true on sensitive paths, quarantine delete, patch receipts).
2. Interim enforcement point: kimi/opencode/claude hooks (PreToolUse) redirect write-class calls to forge_filesystem MCP call. No new daemon.
3. Lease-step 1 (T2): hooks warn+log every direct write → produces the exception census (how many writes/day actually bypass).
4. Lease-step 2 (T2→T3): census < N/day → enforce redirect; census high → widen A-FORGE surface first.
5. Exit: A4 exception ledger empty for 7 consecutive days → close lease.

## Option B — Sandbox harnesses (heavier, cleaner)

bwrap/overlay per harness (ExecutionSandbox exists in A-FORGE ephemeral tooling). Higher fidelity, higher ops cost. Pursue only if Option A census shows unmanageable volume.

## Verification (per doctrine: recovery demonstrated, not assumed)

- Negative test: harness attempts direct write with hook active → DENIED + receipt.
- Positive test: same write via forge_filesystem → receipt in VAULT999 lane.
- FRAME witnesses the census weekly (drift snapshot carries A4-except count).

## Work items

| # | Item | Tier |
|---|---|---|
| A4-1 | Hook census (warn-only) on kimi seat first | T2 |
| A4-2 | Census analysis + A-FORGE surface sizing | T1 |
| A4-3 | Enforce redirect on kimi, then opencode/claude | T2/T3 |
| A4-4 | Lease close report to F13 with 7-day empty ledger | T1 |

DITEMPA BUKAN DIBERI ⚒️
