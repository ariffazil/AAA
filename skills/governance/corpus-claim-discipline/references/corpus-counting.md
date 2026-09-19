# Corpus counting — probe recipes

Companion to the procedure in SKILL.md. Every snippet here was run against a live message store
before being written down.

## 1. Locate the corpora

| Corpus | Where | Shape |
|---|---|---|
| WhatsApp 1:1 export | private shadow sources under `/root/.hermes/lanes/private/.../sources/` | `M/DD/YY, H:MM AM/PM - Sender: body`; `<Media omitted>` marks images |
| Telegram group / DM | the Hermes state DB | join `messages` → `sessions` on `sessions.chat_id` |

Schema traps that each cost a turn:

- the timestamp column is **`timestamp`** (unix float), not `ts`;
- **the sender is not a column** — it is a `[Name|uid]` prefix inside `content`;
- `sessions.chat_id` is the lane. One lane spans many session ids across resets: sweep `chat_id`,
  never a single `session_id`;
- joining `messages` to `sessions` attributes every line to a room in one query.

Verified query shape:

```python
import sqlite3
c = sqlite3.connect('/root/.hermes/state.db'); c.row_factory = sqlite3.Row
sad = [r['id'] for r in c.execute("select id from sessions where chat_id=?", ('<chat_id>',))]
q = ",".join("?" * len(sad))
rows = c.execute(f"select id, session_id, role, content, timestamp from messages "
                 f"where session_id in ({q}) order by id", sad).fetchall()
```

## 2. Extract sender + body

```python
import re
m = re.match(r'^\[([^\]|]{0,40})\|(\d+)\]\s*(.*)$', content.strip(), re.S)
if m:
    name, uid, body = m.group(1).strip(), m.group(2), m.group(3).strip()
```

`No name` means the display name is unset. Resolve the `uid` against the channel registry or
`sessions.user_id` — never infer identity from the label.

## 3. Dedupe funnel (print this with every figure)

Pass 1 — collapse identical bodies inside the same minute:

```python
key = (ts[:16], body)
```

Pass 2 — collapse an identical body whose message ids are near-adjacent (the same line replayed
through a quote chain):

```python
seen_ids = collections.defaultdict(list)
dup = any(x['id'] - prev < 400 for prev in seen_ids[body])
```

Report: `raw N → minute-dedupe N → replay-dedupe N`. Skip this and the counts invent patterns.

## 4. Speaker profile

Per speaker: line count, share of room, median line length, hour-of-day histogram, per-day volume,
and a register histogram (logistics / body / money / family / affect / addressed-to-agent).

Median length sets the analysis level: a subject speaking in ~28-character fragments cannot be read
with sentence-level semantics. The hour histogram surfaces the late-night band, which usually carries
a different register from the daytime.

## 5. Access-token test

For each recurring content word, sample ALL its lines and ask one question: *referent or
permission?*

Clustering probe — count how many of the word's lines also contain availability/absence language:

```python
ACCESS = re.compile(r'line clear|xleh stay|xde org|da balik|da tido|boleh datang|otw|smpai', re.I)
```

A word whose lines concentrate in that set is a control token — a door switch in the shared
vocabulary — and must not be read as the conversation's topic.

## 6. Two-sided test

Run the same token frequency over the OTHER party's lines and over the principal's lines. Both sides
using it ⇒ co-authored ⇒ not attributable to the subject as a private device.

## 7. Era-check

Print every hit with its date. Before any pattern becomes a claim, attach a date; where a dated line
appears to conflict with the principal's framing, surface the date rather than a conclusion — then
pull dated lines on both sides before writing anything durable.

## 8. Ceiling statement

Close every count with what it cannot reach: attachment, motive, interior, shared meaning. A clean
number does not license a claim about a person's inside.
