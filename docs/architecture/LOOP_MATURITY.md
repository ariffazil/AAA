# Loop Maturity Levels — L1/L2/L3

> **Adopted 2026-06-29** from [cobusgreyling/loop-engineering](https://github.com/cobusgreyling/loop-engineering).
> Orthogonal to T1/T2/T3 autonomy tiers (consequence axis). This is the **maturity axis**.

## The Two Axes

| Axis | What It Gates | Levels |
|------|--------------|--------|
| **Consequence** (T1/T2/T3) | What happens if it goes wrong | T1 AUTO-DO → T2 ANNOUNCE → T3 888_HOLD |
| **Maturity** (L1/L2/L3) | How much the loop has proven itself | L1 Report → L2 Assisted → L3 Unattended |

A new loop starts at **L1+T1** (report-only, auto-observe). It graduates to **L2+T2** (assisted, announce). **L3+T3** (unattended, hold-gated) only after 2 weeks of clean L2.

## Level Definitions

### L1 — Report (Start Here)

- Triage → state. No auto-action.
- Human reads output, decides next step.
- Token cost: low (~50k/run for triage).
- **Required:** Triage skill, state file, `Last run` timestamp.
- **Gate:** 1–2 weeks of consistent triage quality before L2.

### L2 — Assisted

- Small auto-fixes with separate verifier sub-agent.
- Worktree isolation for all code changes.
- Max 3 attempts per item → escalate to human.
- Token cost: medium (~200k/run with implementer + verifier).
- **Required:** Verifier skill, worktree isolation, attempt caps, path denylist.
- **Gate:** 2 weeks of clean L2 (no S2 failures) before L3.

### L3 — Unattended

- Runs without human watching.
- **Hard requirements (all must exist):**
  - Path denylist in skills
  - Auto-merge off or strict allowlist
  - Connector scopes reviewed
  - Human gates documented
  - Token budget + run log + kill switch
  - Observability (every run logged)
- Token cost: high (budget-dependent).
- **Gate:** Only after denylist + budget + metrics + human gates all verified.

## Quick Red Flags (Stop and Fix)

- Same item retried >3 times without progress
- Verifier is same agent session as implementer
- No state file — loop has amnesia every run
- Notifications on every run regardless of findings
- Auto-merge enabled without path allowlist

## Mapping to Federation Autonomy

| L1+T1 | L1+T2 | L2+T1 | L2+T2 | L3+T3 |
|-------|-------|-------|-------|-------|
| Report, auto-observe | Report, announce | Assisted fix, auto | Assisted fix, announce | Unattended, hold-gated |
| **Default start** | Active sprints | Proven loops | Production loops | Mature loops only |

---

*DITEMPA BUKAN DIBERI — Loops are forged in phases, not overnight.*
