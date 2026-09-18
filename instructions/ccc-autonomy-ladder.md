# CCC Autonomy Ladder — A0-A6 Mapped to Authority Tiers

> **Status:** F13_OBSERVED (2026-09-18) — forged from ChatGPT Deep Research contrast.
> **Binding:** All CCC workers and routing decisions.
> **Grounding:** CCC_DOCTRINE roles · T0/T1/T1.5/T2/T3 authority tiers · F1 AMANAH (reversibility).

## The Ladder

| Level | Authority | arifOS Tier | Reversibility | Typical Use |
|---|---|---|---|---|
| **A0** | Explain only | T0 | N/A (read-only) | Architecture analysis, Q&A, code review |
| **A1** | Propose | T1.5 | N/A (no mutation) | Plan, patch text, test suggestions |
| **A2** | Ephemeral workspace write | T1 (extended) | Fully reversible | Implement/test in worktree, sandbox, temp dir |
| **A3** | Reversible external artifact | T2 | Reversible with effort | Draft PR, temporary branch, staged file |
| **A4** | Non-production merge | T2 | Reversible with effort | Staging deploy, repo writes to non-main |
| **A5** | Production mutation | T3 (888_HOLD) | Hard to reverse | Merge to main, deploy, infra change |
| **A6** | Irreversible/cross-domain | F13 SEAL only | Irreversible | Destructive data ops, money, physical effects |

## A2 — The New Level (Ephemeral Workspace Write)

**Why A2 exists:** Existing tiers don't formalize the boundary between "read-only proposal" (T1.5) and "announce + veto" (T2). A2 fills the gap for work that is inherently reversible.

**A2 rules:**
- Agent may freely create, modify, and delete files in isolated workspaces (worktrees, containers, temp dirs)
- No governance overhead — the ephemeral boundary IS the safety boundary
- Transition from A2 to A3 (PR, branch push) requires arifOS SEAL
- A2 work that never escapes the ephemeral boundary = auto-cleanup, no receipt needed

**F1 AMANAH grounding:** Ephemeral writes are reversible by definition. Governance boundary sits at A3 — where effects escape the ephemeral boundary.

## CCC Role → Autonomy Level

| CCC Role | Default A-Level | Can escalate to |
|---|---|---|
| `planner` | A1 | A1 (propose only) |
| `builder` | A2 | A3 with SEAL |
| `verifier` | A0 | A0 (read/test only) |
| `reviewer` | A0 | A0 (read/audit only) |
| `deployer` | A3 | A5 with 888_HOLD |

## Routing Rule

When AAA routes a task to a CCC worker:
1. Assign autonomy level based on task consequence
2. Default: A2 for implementation, A0 for review/audit
3. A3+ requires arifOS SEAL before execution
4. A5+ requires 888_HOLD or explicit F13 approval
5. A6 is never auto-routed — F13 only

DITEMPA BUKAN DIBERI ⚒️
