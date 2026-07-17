# Organ Coordination — Multi-Loop Rules

> **Adopted 2026-06-29** from [cobusgreyling/loop-engineering/multi-loop.md](https://github.com/cobusgreyling/loop-engineering/blob/main/docs/multi-loop.md).
> Mapped to arifOS 7-organ federation topology.

## Principles

1. **One owner per branch** — at most one organ may mutate a branch per hour.
2. **Separate state files** — each organ owns its own state; `CONTEXT.md` is triage-level only.
3. **Triage reports, action organs execute** — AAA observes, A-FORGE acts, arifOS judges.
4. **Shared denylist** — same path denylist enforced across all organs.
5. **Aggregate token budget** — per-organ + federation-wide caps.

## Organ Priority When Loops Conflict

| Priority | Organ | Reason |
|----------|-------|--------|
| 1 | **arifOS** | Constitutional kernel — governance overrides all |
| 2 | **A-FORGE** | Execution — active work is time-sensitive |
| 3 | **GEOX** | Domain evidence — feeds decisions |
| 4 | **WEALTH** | Capital intelligence — advisory |
| 5 | **WELL** | Human readiness — reflective, not directive |
| 6 | **AAA** | Control plane — display and routing |
| 7 | **A-AUDIT** | Observer — runs in parallel, never blocks |

## Collision Detection

Before any organ acts on a branch/PR:
1. Read all other organ state files
2. If another organ `acting_on` matches → skip and log to `SESSION.md`
3. If conflict → escalate to arifOS for arbitration

## Human Inbox

Shared section in `CONTEXT.md`:

```markdown
## Human Inbox (ambiguous / cross-organ)
- [ ] PR #42: A-FORGE and GEOX both flagged — human pick owner
```

## Token Budget Rules

| Rule | Threshold | Action |
|------|-----------|--------|
| Per-organ daily cap | Configurable | Pause organ loop on exceed |
| Federation-wide cap | $2.00/session | Switch to cheaper models |
| Sub-agent spawn cap | 3 per run | Escalate if more needed |
| Early exit | Empty watchlist | Exit in <5k tokens |

## Safe Multi-Organ Setup

| Organ | Level | Cadence | Notes |
|-------|-------|---------|-------|
| AAA (triage) | L1 | 1d | Report-only morning scan |
| A-FORGE (build) | L2 | on-demand | Worktree + verifier |
| arifOS (judge) | — | event-driven | Constitutional verdicts |
| A-AUDIT (watch) | L1 | continuous | Parallel observer |

---

*DITEMPA BUKAN DIBERI — Coordination is governance in motion.*
