# Store-by-store command catalogue

Exact, copy-pasteable sweep commands per store. Extend this file when a new store is discovered; keep SKILL.md procedural only.

## Roots worth grepping

- `/root/AAA` — governance, doctrine, reports, skills, agent configs.
- `/root/.hermes` — runtime: memories, pending, workspace, sessions, state DB, caches, output.
- `/root/arifOS`, `/root/A-FORGE`, `/root/GEOX`, `/root/WEALTH`, `/root/WELL` — organ repos.
- `/root/HERMES` — lanes/private pointers + document caches. **The live lanes tree may have moved; canonical copies now sit under `/root/.quarantine/*/_CANONICAL/*/` — search quarantine too before declaring a card missing.**
- `/opt/arifos/app` — kernel runtime (probe it, don't grep blindly).
- Do NOT let a `find /` reach `/var/lib/docker`, `/var/lib/containerd`, or `*/cesium/*` — overlay layers and bundled JS drown the hits and the command gets killed before it finishes.

## Memory stores

```bash
# live memory
ls -la /root/.hermes/memories/
python3 -c "print(open('/root/.hermes/memories/MEMORY.md').read())"

# pending consolidations — print each far enough to read the old_text → content diff
for f in /root/.hermes/pending/memory/*.json; do
  python3 -c "import json;d=json.load(open('$f'));print('==','$f');print(json.dumps(d,ensure_ascii=False)[:700])"
done

# semantic dump (mem0)
q='<name>'
grep -i -o ".\{200\}$q.\{400\}" /root/.hermes/workspace/zen/mem0_dump.jsonl | head -10

# channel / group identity
python3 -c "import json;d=json.load(open('/root/.hermes/channel_directory.json'));print(json.dumps(d,ensure_ascii=False,indent=1)[:2000])"
```

## Person-recall sweeps (highest yield for "what do you know about X")

`/root/mem0_audit_data.json` and `/root/mem0_cleanup_plan.json` are the densest distilled store for a person — a name-walk returns every synthesised entry (identity, timeline, working life, the sovereign's own reads). Dedupe before printing; there are many near-copies.

```python
import json
NAME = '<name>'
hits = []
for f in ('/root/mem0_audit_data.json', '/root/mem0_cleanup_plan.json'):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    def walk(o):
        if isinstance(o, dict):
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
        elif isinstance(o, str) and NAME in o.lower():
            hits.append(o)
    walk(d)
seen = list(dict.fromkeys(hits))
print('unique:', len(seen))
for t in seen: print('-', t[:380])
```

Session DB — one db, one messages table. Read-only URI so a live gateway is never disturbed:

```python
import sqlite3, time
con = sqlite3.connect('file:/root/.hermes/state.db?mode=ro', uri=True)
q = '%<name>%'
for r in con.execute("SELECT session_id, role, timestamp, substr(content,1,500) FROM messages "
                     "WHERE content LIKE ? AND timestamp > ? ORDER BY timestamp",
                     (q, time.time() - 14*86400)):
    print(r)
# newer-than marker: keep the max timestamp and page forward instead of re-scanning
```

Duplicate-answer check — did a sibling session already field this exact question?

```python
for r in con.execute("SELECT session_id, timestamp FROM messages WHERE role='user' AND content=? "
                     "AND timestamp > ? ORDER BY timestamp", (question_text, time.time() - 1800)):
    print(r)   # 2+ rows = concurrent sessions, one is answering too
```

Private lane cards and prior maps:

```bash
find /root/.hermes /root/.quarantine -maxdepth 9 -path '*lanes/private*' -name '*.md' 2>/dev/null | head
ls /root/memory/people/ 2>/dev/null
```

Cached exports and fragments (delivered documents keep an opaque prefix like `doc_<hash>_<name>.txt`), plus any working copy already extracted:

```bash
ls /root/.hermes/cache/documents/ | grep -i '<name>'
find /root/.hermes/cache/documents /tmp -maxdepth 3 -iname '*<name>*' 2>/dev/null
```

## Artifacts and caches

```bash
ls -la /root/.hermes/output/ /root/.hermes/output/preview/ 2>/dev/null
find /root/.hermes -maxdepth 4 -iname '*<topic>*' -newermt '<date>' 2>/dev/null
stat -c '%n %s bytes %y' <file>
pdftotext <file>.pdf - | sed -n '1,200p'
head -c 3000 <file>.html            # HTML deliverables hold the same text and are easier to grep

# verbatim prior tool output
grep -ril '<name>' /root/.hermes/cache/exec/ /root/.hermes/cache/terminal-output/ 2>/dev/null | head

# session JSON dumps (noisy; only to prove a mention)
grep -ril '<name>' /root/.hermes/sessions/ 2>/dev/null | head
```

## Reporting rule of thumb

Quote the store, not the conclusion: "pending memory entry (created <ts>) says X, live MEMORY.md still says Y" beats "X is true".
