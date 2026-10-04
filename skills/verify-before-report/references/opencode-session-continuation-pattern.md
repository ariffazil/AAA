---
title: OpenCode Session Continuation Pattern
category: verify-before-report
date: 2026-08-11
author: verified via human correction
tags: [opencode, session-continuation, idle-resume]
---

# OpenCode Session Resumption via Message Injection — Session Record (2026-08-11)

**Context:** OpenCode process hit iteration cap and entered idle state (`"bounded reality loop stopped (iter cap)"`). No new session needed — just continue the existing one.

**Pattern discovered:** `opencode run --session <id> "<message>"` injects a continuation prompt directly into an idle session without launching TUI. This is cleaner than starting fresh for follow-ups on the same workstream.

---

## The Failure Mode (What NOT To Do)

When an OpenCode session stops (iteration cap, timeout, Ctrl+C):

```bash
# ❌ WRONG: Start brand new session
opencode run 'Continue from previous'  

# Problem: loses all context from the previous session, starts over

# ❌ WRONG: Say "done" without verification  
Agent: "OpenCode finished. All repos committed."

# Reality check: local commit exists ≠ GitHub remote pushed = false claim
```

---

## The Correct Pattern (How To Continue)

### Step 1: Find running sessions

```bash
# List all opencode sessions
opencode session list

# Look for the right one (check title + time_updated)
# Output example:
# Session ID                      Title                                               Updated
# ────────────────────────────────────────────────────────────────────────────────────
# ses_00fe18e70ffee4OynFRyIBeyXV  New session - 2026-08-11T09:19:14.831Z              6:33 PM
```

### Step 2: Verify session state before continuing

```bash
python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.local/share/opencode/opencode.db')
con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
cur = con.cursor()
sid='ses_00fe18e70ffee4OynFRyIBeyXV'
row = cur.execute('SELECT id,title,directory FROM session WHERE id=?',(sid,)).fetchone()
print('Session:', row[1], '| DIR:', row[2])
msg_count = cur.execute('SELECT count(*) FROM message WHERE session_id=?',(sid,)).fetchone()[0]
print('Messages:', msg_count)
last_msg = cur.execute('''
  SELECT data FROM message 
  WHERE session_id=? ORDER BY rowid DESC LIMIT 1
''', (sid,)).fetchone()
if last_msg:
  import json
  obj = json.loads(last_msg[0])
  print('Last finish reason:', obj.get('finish'))
"
```

If `finish` = `"stop"` → session ended gracefully, safe to resume.

### Step 3: Inject continuation message

```bash
timeout 120 opencode run \
  --session ses_00fe18e70ffee4OynFRyIBeyXV \
  --dir /root \
  "Continue your FED / FLAME / FRAME work. Status at last stop:
- FED: git status clean except untracked push.sh
- FLAME: M README.md (modified)
- FRAME: M README.md (modified)

Do this now:
1. Commit ALL pending changes across all 3 repos
2. Run verification: ensure all ops pass, no syntax errors
3. Produce final summary report

Use default model (litellm-federation/opencode)." 2>&1 | tail -60
```

### Step 4: Verify completion (don't trust agent claims!)

After `opencode run` returns, ALWAYS verify:

```bash
# Check LOCAL state first
git -C /root/FED status --short && echo "FED:" || echo "FED: FAILED"
git -C /root/FLAME status --short && echo "FLAME:" || echo "FLAME: FAILED"
git -C /root/FRAME status --short && echo "FRAME:" || echo "FRAME: FAILED"

# THEN check REMOTE existence (GitHub probe)
curl -sfI "https://github.com/ariffazil/FED" >/dev/null && echo "FED EXISTS ✅" || echo "FED MISSING ❌"
curl -sfI "https://github.com/ariffazil/FLAME" >/dev/null && echo "FLAME EXISTS ✅" || echo "FLAME MISSING ❌"
curl -sfI "https://github.com/ariffazil/FRAME" >/dev/null && echo "FRAME EXISTS ✅" || echo "FRAME MISSING ❌"
```

---

## Key Insights

### Why `--session` + `run` beats TUI resume

| Method | When to use |
|--------|-------------|
| `opencode -c` (continue) | You want interactive TUI back |
| `opencode run --session X` | You want headless continuation + capture output |
| `opencode run 'New task'` | Starting fresh with new context |

The `--session` flag reuses all prior conversation context. `run` wraps it in a bounded execution. Perfect for "keep working until done" patterns.

### Timeout matters

Long-running agents may take minutes. Use `timeout 120` (or longer) to prevent the shell wrapper from cutting off mid-execution:

```bash
timeout 300 opencode run --session $SESSION_ID "<multi-step instruction>"
```

### Verify GitHub EXISTS before claiming "pushed"

Local `git push` = nothing if repo doesn't exist on GitHub. Always probe:

```bash
# For ANY repo claimed "pushed":
curl -sfI https://github.com/<org>/<repo>.git | grep -qE "^HTTP/1\.[01] [23][0-9][0-9]" && echo "✅ EXISTENT" || echo "❌ MISSING"
```

This pattern saved us from reporting false success.

---

## Prevention Checklist (Next Time)

Before claiming an OpenCode session "completed successfully":

- [ ] Session ID identified? (`opencode session list`)
- [ ] Session state verified? (`sqlite3 opencode.db`, check `finish` field)
- [ ] Continuation message injected? (`opencode run --session <id>`)
- [ ] Local git state checked? (`git status --short` per repo)
- [ ] Remote GitHub verified? (`curl -sfI https://github.com/<org>/<repo>`)
- [ ] Final report generated? (file path + line count confirmed)

---

## Related Skills

- `verify-before-report` — core discipline for not hallucinating real-world actions
- `federation-runtime-forensics` — multi-agent box forensics, similar verification mindset

DITEMPA BUKAN DIBERI.
