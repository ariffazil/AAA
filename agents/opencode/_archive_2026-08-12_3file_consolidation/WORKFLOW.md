# ⚒️ OPENCODE — Autonomous Workflow Engine

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Canonical SOT:** 2026-07-23 — Task Queue + Progress Log + Context Ledger

---

## THE IRON LOOP — Always Know What to Execute Next

```
SESSION_START → READ tasks.json → PICK first pending → 
READ progress.txt tail → EXECUTE → VERIFY → COMMIT → 
UPDATE tasks.json + progress.txt → REPEAT until all tasks pass
```

---

## 1. TASK QUEUE (`/root/work/tasks.json`)

Machine-readable task list. Agent reads this at session start. 
Picks the first non-passing task. Works on it. Marks it done.

```json
[
  {"id": 1, "name": "fix-auth-bug", "status": "pending", "tests": "auth.spec.ts"},
  {"id": 2, "name": "add-rate-limiting", "status": "pending", "tests": "rate-limit.test.ts"}
]
```

**States:** `pending` | `in_progress` | `completed` | `blocked`

**Rule:** Only ONE task `in_progress` at a time.

---

## 2. PROGRESS LOG (`/root/work/progress.txt`)

Append-only chronological journal. Every cycle writes:
- What was attempted
- Pass/fail
- Error messages
- Discoveries

Agent reads the tail at session start for context.

```
[2026-07-23T10:00] SESSION_START session_id=abc actor_id=opencode
[2026-07-23T10:05] TASK_1_START fix-auth-bug
[2026-07-23T10:15] TASK_1_PASS tests=12/12 commit=a1b2c3d
```

---

## 3. CONTEXT LEDGER — Commit-Boundary Compaction

When a feature is committed, its verbose context (~10k tokens) is replaced 
with a compact structured ledger entry + git pointer.

```
[LEDGER] feature:auth-fix | commit:a1b2c3d | tests:12/12 | status:CLEAN
```

**Rule:** Drop the content. Keep the handle. Rehydrate from git on demand.
~30× smaller working context. ~28× longer before hitting window limit.

---

## 4. SELF-HEALING LOOP

```
GENERATE → RUN → READ LOGS → CLASSIFY ERROR → SURGICAL FIX → RUN AGAIN
```

Anti-pattern catalog: every failure documented and injected into context.

**Format:**
```
[ANTI-PATTERN #N] pattern: X → root_cause: Y → fix: Z → result: PASS/FAIL
```

---

## 5. PLANNER → WORKER → JUDGE SPLIT

For complex tasks:
- **PLANNER** reads codebase, decides what to do → produces plan
- **WORKER** implements in isolation → produces artifact
- **JUDGE** verifies against specs → PASS or REVISE

---

## 6. PROGRESSIVE SKILL DISCLOSURE

- **Level 1**: Metadata only (~100 tokens) — always loaded
- **Level 2**: Instructions (~5k tokens) — loaded on trigger
- **Level 3+**: Resources/scripts — loaded on demand

**Rule:** Never load all skills at once. Keep hot surface < 15 tools.

---

## 7. SESSION INTEGRATION

| What | Path |
|------|------|
| Task Queue | `/root/work/tasks.json` |
| Progress Log | `/root/work/progress.txt` |
| Context Ledger | `/root/work/ledger.jsonl` |
| Anti-Patterns | `/root/work/anti-patterns.jsonl` |
| Carry-Forward | `/root/.local/share/arifos/carry_forward.json` |
| Seal Chain | `/root/.local/share/arifos/vault999/seal_chain.jsonl` |

---

*Forged: 2026-07-23. Autonomous flow engine — never ask "what next" again.*
*Agentic kernel layer: SCHEDULER (layer 4/7). Next: HEARTBEAT.md (layer 5 — health daemon).*
*DITEMPA BUKAN DIBERI ⚒️*
