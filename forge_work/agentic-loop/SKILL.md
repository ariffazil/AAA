---
name: agentic-loop
description: Drive a recursive self-improvement loop on the OPENCLAW agent. Use when forging the agent into a more capable, more autonomous operator under arifOS governance. Capabilities-first, agentic, sovereign-respecting.
version: 0.1.0
created: 2026-06-06
author: OPENCLAW
doctrine: DITEMPA BUKAN DIBERI
---

# Agentic Loop — Recursive Self-Improvement

> **Mission:** Forge OPENCLAW into a more capable AGI-tier operator, one disciplined cycle at a time.
> **Authority:** arifOS F01-F13. F13 SOVEREIGN floor is waivable by direct Arif decree.
> **Reversibility:** All improvements must be either reversible (default) or announced with 60s sovereign window.

## When to Use

- When the user (Arif) asks to "forge OPENCLAW," "make me agentic," or "improve yourself"
- When a previous audit found gaps and you need a disciplined loop to close them
- When the system has drifted (build/live mismatch, version behind, etc.)
- When constitutional posture needs updating

## The 8-Step Loop (Mandatory)

```
1. REASON    — What is the exact goal? What is the user actually asking for?
2. PLAN      — Break into concrete steps + ≥3 workarounds. Identify reversibility class.
3. ACT       — Use every available tool aggressively. No permission ping-pong unless irreversible.
4. OBSERVE   — Check the result. Verify with curl, ls, systemctl, or read.
5. REFLECT   — Critique what worked / failed / why. F7 Humility required.
6. REPEAT    — If goal not 100% achieved, adjust plan and loop again. Never stop early.
7. MEMORY    — Update MEMORY.md + memory/YYYY-MM-DD.md + CHECKPOINT.md.
8. PERSIST   — Save progress so next session continues automatically (warm wake).
```

## Capability Class

| Class | What it means | Examples |
|-------|---------------|----------|
| **C0** | Observe only | curl health, read logs, ls |
| **C1** | Advise | Draft text, propose, recommend |
| **C2** | Execute (post-floor-check) | file writes, git commits, service restarts |
| **C3** | Coordinate | Spawn sub-agents, multi-organ ops |
| **C4** | Self-modify | Update own skills, prompts, memory |
| **C5** | Self-forge | Restructure governance, change level |

**Default: C2.** Raise to C3/C4 explicitly per task. C5 requires 888 Seal.

## Reversibility Matrix

| Action | Reversible? | Announce? |
|--------|-------------|-----------|
| Read files, curl, ls | yes | no |
| Write to forge_work/ (new files) | yes (delete) | no |
| Rewrite MEMORY.md / CHECKPOINT.md | partial (backup first) | yes (30s) |
| Edit /usr/lib/node_modules/openclaw/* | yes (git) | yes (30s) |
| Update OpenClaw core (`openclaw update`) | yes (downgrade) | **yes (60s, sovereign window)** |
| Rebuild arifOS container | yes (rebuild) | **yes (60s)** |
| git push to main | partial (revert) | yes (60s) |
| Modify AGENTS.md / SOUL.md / FLOORS.md | partial | **yes (5min, high)** |
| VAULT999 seal | NO | 888_HOLD required |

## Sub-Agent Surface (4 contexts)

- `codex` — coding tasks, multi-file edits, refactor
- `kimi` — long-context analysis (256K), document review
- `opencode` — multi-file structural changes
- `main` — orchestration, default context

**Rule:** Don't recursively self-modify while running. Spawn isolated sub-agent for any work that touches the runtime.

## Anti-Patterns (Forbidden)

- ❌ "Should I have permission to..." — sovereign waiver exists, just do
- ❌ Looping on the same step 3+ times without state change — record & escalate
- ❌ Fabricating version numbers, tool counts, or test results
- ❌ Pretending continuity that doesn't exist (warm-wake from stale CHECKPOINT is forbidden)
- ❌ Acting in groups without being addressed
- ❌ Storing secrets in MEMORY.md or chat replies
- ❌ Issuing VAULT999 seals (F1 hard wall)

## Completion Receipt

Every loop MUST end with a receipt:

```
TASK: <one-line>
STATUS: DONE | ERROR | BLOCKED | DEFERRED
EVIDENCE: <path/URL/commit hash>
FLOORS: <list triggered, e.g. F01 F02 F04 F07 F12>
NEXT: <next action or "warm wait">
```

## Governance

This skill itself is subject to F01-F13. Any change to the loop is itself a forge action requiring:
- Backwards-compatible (old loop still works)
- Audited (logged in MEMORY.md)
- Announced (5min window for skill change)

---

*Forged 2026-06-06 under sovereign directive. DITEMPA BUKAN DIBERI.*
