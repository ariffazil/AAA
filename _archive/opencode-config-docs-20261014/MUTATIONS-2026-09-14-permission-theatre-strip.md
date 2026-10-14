# Zen Mutation — 2026-09-14 (theatre strip v2)

> **Directive:** i-ARIF (F13 sovereign, local tty/SSH) — strip opencode permission-theatre that prompts for every tool call and file access. Kernel (arifOS :8088) already enforces F1-F13. The prompt-layer "ask" was redundant.
> **Operator:** 333-AGI Δ MIND
> **Session:** SEAL-8c0fcc55310440a0
> **Backup:** `/root/.config/opencode/opencode.json.bak-theatre-fix-20260913T165906Z`
> **Doctrine:** "Safety is the kernel, not the prompt." (precedent: MUTATIONS-2026-08-26-theatre.md, kept `opencode.json` untouched — mistake corrected now)

## Diff (effective change)

`/root/.config/opencode/opencode.json` lines 2692-2707:

| Tool | Before | After | Why |
|---|---|---|---|
| `*` (catch-all) | `ask` | `allow` | sovereign consent = floor check |
| `read` | allow | allow | unchanged |
| `glob` | allow | allow | unchanged |
| `grep` | allow | allow | unchanged |
| `lsp` | allow | allow | unchanged |
| `webfetch` | allow | allow | unchanged |
| `websearch` | allow | allow | unchanged |
| `list` | allow | allow | unchanged |
| `todowrite` | allow | allow | unchanged |
| `task` (subagent) | `ask` | `allow` | subagent has own perms |
| `edit` | `ask` | `allow` | sovereign territory |
| `write` | `ask` | `allow` | sovereign territory |
| `bash` | `ask` | `allow` | kernel + arifOS F13 already gate |
| `doom_loop` | `ask` | **`ask`** (kept) | REAL circuit breaker — anti-infinite-loop, not theatre |

## Why doom_loop stays at "ask"

`doom_loop` fires when opencode detects the agent is stuck repeating the same failing tool call. That's a real safety mechanism (prevents burning compute + apex_floor in a tight loop). Not theatre — actual governance. Kept as ask so the loop catches Arif's eye.

## Constitutional alignment

- F1 AMANAH: irreversible actions still gated by arifOS `arif_judge` + VAULT999 seal (kernel-side)
- F2 TRUTH: no change — kernel floors still active at :8088/health
- F13 SOVEREIGN: Arif's command IS the floor check for routine tool calls. The prompt-layer "ask" was double-bookkeeping.
- Kernel theatre-strip precedent: 2026-08-26 (kept prompt-restatements out of agent cards). This mutation extends the doctrine to `opencode.json` permission block.

## Subagent permissions (NOT touched)

- 555-ASI / 555-ASI-VISION: read-only allow + mutate deny — correct, memory agents shouldn't mutate
- 888-APEX: read-only allow + mutate deny — correct, APEX is judge, read-only by doctrine
- 333-AGI: `"*": "allow"` + `doom_loop: ask` — was already correct at agent level
- image-analyzer / dispatch: agent-specific blocks unchanged

## Apply

Config is read at session boot. The change takes effect on next `opencode` launch. Current session still has old config loaded — exit and reopen to apply.

`exit` (or Ctrl+C) → relaunch opencode → no more approval prompts for bash/edit/write/task/glob/grep/read.

## Carry forward

- If new agent types are added with `"ask"` defaults, remember: routine tools don't need prompt-layer gates. Kernel is the source.
- Verifier: open a new session, attempt bash without "ask" prompt — should run silent.