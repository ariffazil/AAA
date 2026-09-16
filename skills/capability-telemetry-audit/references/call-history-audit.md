# Call-History Audit — queries, counters, pricing

Read-only SQLite against `~/.hermes/state.db`. Companion to §2–§7 of the skill. Every number in the
report must be re-derivable from a query printed beside it.

| Table | Read it for |
|---|---|
| `messages` | `tool_name`, `tool_calls` (JSON args), `role`, `content` — the call history |
| `sessions` | `end_reason`, `message_count`, `tool_call_count`, cost columns |
| `delivery_obligations` | `state` — delivered / failed / abandoned |
| `async_delegations` | `state` — completed / error; tracked vs untracked children |
| `session_model_usage` | per-model call counts and cost |

## 1. Fired-tool census

```python
import sqlite3, collections
c = sqlite3.connect('/root/.hermes/state.db')
fired = dict(c.execute("SELECT tool_name, COUNT(*) FROM messages "
                       "WHERE tool_name IS NOT NULL GROUP BY 1"))
print('distinct fired:', len(fired), 'total calls:', sum(fired.values()))
mcp = {k: v for k, v in fired.items() if k.startswith('mcp__')}
print('per server:', dict(collections.Counter(k.split('__')[1] for k in mcp)))
```

Compare distinct-fired against the wired count from `mcp_servers:` in `config.yaml`. Wired servers with
zero calls are the triage queue — each contributes schema and routing cost with no demonstrated value.
Split into **redundant** (another owner already does this) and **untapped** (consequence-bearing, rarely
needed) before proposing anything.

## 2. Reading call ARGUMENTS — how a capability is used

```python
import json
args = []
for (tc,) in c.execute("SELECT tool_calls FROM messages WHERE tool_calls LIKE '%<tool>%'"):
    for call in json.loads(tc or '[]'):
        fn = call.get('function', {})
        if fn.get('name') == '<tool>':
            args.append(fn.get('arguments', ''))
```

Framing, not volume. Example — delegation that gathers versus delegation that falsifies:

```
FALS = r'falsif|disprove|refut|attack|adversar|red.?team|independent|prior.art|devil'
PROVE= r'prove|demonstrat|evidence|verify'
```

N children sharing one prior gives N× compute for ~1× independent information. That is the finding —
report it as such.

## 3. Closure — promise versus landed

```python
print(dict(c.execute("SELECT state, COUNT(*) FROM delivery_obligations GROUP BY 1")))
print(dict(c.execute("SELECT state, COUNT(*) FROM async_delegations GROUP BY 1")))
print(dict(c.execute("SELECT end_reason, COUNT(*) FROM sessions GROUP BY 1")))
```

- Fired calls minus tracked rows = **witnessing gap**, not proven failure.
- Failed/abandoned means a promise did not land — a defect.
- Sessions with no `end_reason` are unclosed inventory, not a defect, until something depends on them.

## 4. Mutation → verification adjacency

Answers "does the agent check its own work?" with a number instead of an opinion.

```python
rows = c.execute("SELECT session_id, tool_name FROM messages "
                 "WHERE tool_name IS NOT NULL ORDER BY session_id, id").fetchall()
seq = collections.defaultdict(list)
for s, t in rows: seq[s].append(t)
MUT = {'write_file', 'patch', 'skill_manage'}
VER = {'terminal', 'execute_code', 'read_file', 'search_files'}
n = v = 0
for s, q in seq.items():
    for i, t in enumerate(q):
        if t in MUT:
            n += 1
            if any(x in VER for x in q[i+1:i+4]): v += 1
print(f"{v}/{n} mutations followed by a check within 3 calls")
```

Run this **before** asserting that verification or closure is missing. A high ratio falsifies the
thesis.

## 5. Reply-level behaviour counters

The unit is the agent's human-facing text, not its tool calls.

```python
txt = [r[0] for r in c.execute("SELECT content FROM messages "
       "WHERE role='assistant' AND content IS NOT NULL AND content != ''")]
```

Count, then interpret each ratio as **an action class the agent could take autonomously but does not**:

| Pattern | Regex sketch |
|---|---|
| asks permission for a reversible decision | `nak aku\|mahu aku\|do you want\|you want me to` |
| ends with a question | tail `endswith('?')` |
| states a hypothesis before acting | `\b(hypothesis\|aku expect\|aku jangka\|kalau betul)\b` |
| names a second-order effect | `second.order\|kesan kedua\|downstream\|ripple\|when every agent` |
| flags its own uncertainty | `not sure\|tak pasti\|unknown\|aku tak nampak` |
| references a prior decision or contradiction | `bulan lepas\|dulu kau\|earlier we\|already exists\|superseded\|contradict` |
| names what is absent | `takde\|tiada\|missing\|no owner\|never fired\|not wired` |

Human input volume — how much manual typing the machine still costs him:

```sql
SELECT COUNT(*), SUM(LENGTH(content)) FROM messages WHERE role='user';
```

## 6. Pricing

Convert every count before it reaches the human: occurrences × seconds per occurrence → hours or days
of his life, always paired with the manual work he currently performs because of the gap. A count
without a price is not a finding; a price without the manual work is not actionable.

## Caveats

- Volume is not value. State the class of each capability (redundant · rare-event · convenience) and
  the action that class implies.
- Do not name a tool, server or port in the human-facing reply. The query names it; the reply must not.
- Re-run at least one counter after any change — an audit without a second reading has no evidence the
  fix landed.
