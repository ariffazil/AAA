# state.db Session + Message Extraction (Syed/Live-Log Pattern)

## Pattern
User asks: "extract raw logs [person] ↔ Hermes, write to txt file"
→ Probe state.db → write full session dump → deliver file path

## state.db Schema (Helix, Hermes)

```
/root/.hermes/state.db  (605MB, ~23 tables)

Key tables:
  sessions:       id, session_key, user_id, chat_id, chat_type, thread_id,
                 started_at, last_activity_at, message_count, display_name, ...
  messages:       id, session_id, role, content, timestamp,
                 display_kind, display_metadata, tool_name, tool_calls,
                 finish_reason, token_count, ...

Timestamp: Unix seconds (e.g. 1786936834 = 2026-08-17 03:20 MYT)
session_key format: agent:main:telegram:{dm|group}:{chat_id}
```

## Full Extraction Script

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('/root/.hermes/state.db')
cur = conn.cursor()

# 1. Find all sessions touching target user (by chat_id or user_id)
TARGET = '1042200555'  # Syed's Telegram chat_id

cur.execute("""
    SELECT id, session_key, chat_id, started_at, last_activity_at, message_count, display_name
    FROM sessions
    WHERE session_key LIKE ?
       OR user_id = ?
       OR chat_id = ?
    ORDER BY started_at ASC
""", (f'%{TARGET}%', TARGET, TARGET))
sessions = cur.fetchall()

# 2. For each session, dump all messages
for sid, key, chat_id, started_at, last_activity, msg_count, disp_name in sessions:
    cur.execute("""
        SELECT id, role, content, timestamp, display_kind, display_metadata,
               tool_name, tool_calls, finish_reason, token_count
        FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
    """, (sid,))
    msgs = cur.fetchall()
    # Format: [ts_str] [ROLE] content\n...
```

## Session Key Channel Types

| Pattern in key | Channel |
|---|---|
| `telegram:dm:` | Direct message with target |
| `telegram:group:` | Group chat |
| `telegram:thread:` | Threaded sub-session (e.g. DM topic) |

## Timestamps

```python
# MYT = UTC+8
# session timestamp: started_at = Unix seconds (UTC)
# Convert: datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Common ranges (2026):
# 8/16 23:00 MYT = 1755346800
# 8/17 09:00 MYT = 1755382800
```

## Output Format (Human-Readable)

```
SESSION: 20260816_154725_68f631b8
  Channel: DM
  Chat ID: 1042200555
  Started: 2026-08-16 15:47:25 MYT
  Message count: 5
  Display name: No name
-----------------------------------------------------------------------

  [2026-08-17 03:20:29] [USER]
  content:
    Bape % body fat ni
    [Image attached: /root/.hermes/cache/images/img_9dd5209d24a6.jpg]

  [2026-08-17 03:21:26] [ASSISTANT]
  tool: vision_analyze
  content:
    Bape ni ~15-17% punya range. Lean, tapi tak cut...
```

## Privacy Note (F5)
- Sessions with named third parties are sovereign data
- Don't infer relationship type from session_key alone
- Confirm scope with user before dumping all timestamps if unsure
