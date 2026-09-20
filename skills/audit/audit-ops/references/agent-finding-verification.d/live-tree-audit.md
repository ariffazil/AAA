# Live-tree audit recipes

For audits where the tree is being written by other sessions while you read it, and for counts that
must survive a symlink mesh. All snippets are read-only unless marked.

## 1. Count once — dedupe by realpath

A symlinked mesh makes `os.walk` / `find -L` report the same file once per surface. Always resolve
before quoting a number.

```python
import os, collections

def unique_skill_files(roots):
    seen, dups = {}, collections.Counter()
    for r in roots:
        for dp, dn, fn in os.walk(r, followlinks=True):
            if 'SKILL.md' in fn:
                rp = os.path.realpath(os.path.join(dp, 'SKILL.md'))
                dups[rp] += 1
                seen.setdefault(rp, dp)
    return seen, dups

seen, dups = unique_skill_files(['/root/AAA/skills'])
print('unique files:', len(seen))
print('surfaces scanning the same file >1x:', sum(1 for v in dups.values() if v > 1))
```

Report BOTH numbers (`unique` and `raw-with-symlinks`) so the reader can see the inflation. Then
check whether the "duplicate names" claim survives dedupe:

```python
names = collections.Counter(name.lower() for name in per_file_names)
dup = [k for k, v in names.items() if v > 1]
```

A 78-name collision list is typically symlink repetition; the real count is often 1–2.

**Also dedupe frontmatter parsing.** A hand-rolled regex for `description:` that uses a lazy
single-line match returns 0 chars for anything but the simplest values, which fabricates a
"everything has an empty description" finding. Parse the YAML frontmatter block properly before
reporting thin or empty fields.

## 2. Before a negative verdict — freshness re-probe

```bash
stat -c '%y  %n' <artefact>              # when did it actually last change
grep -c '<id>:' <ledger>                 # did the counter move
tail -3 <ledger-or-queue>                # newest rows carry their own timestamps
ls -lt <state-dir> | head               # is a writer still active
```

Rule of thumb: **"unfired" is a claim about mtime, not about the existence of the code.** If a
module was written at 22:13 and the artefact it writes still shows an earlier date, say "written,
unfired as of HH:MM" — and re-check before publishing.

## 3. Concurrent-writer sweep before attributing a change

```bash
ps aux | grep -iE '<agent-cli>' | grep -v grep         # who is alive right now
find <tree> -newermt '-10 minutes' -type f | head      # what moved recently
```

If you cannot show a write from a specific session in the window, report the change without an
author. A partial window is never the world.

## 4. Quiescence-then-seal (commit only when the writer stops)

Do not commit a tree a live writer is touching. Poll it, wait for a quiet interval, then take one
checkpoint commit. Bound it with a hard deadline so the watcher cannot hang forever, and label the
deadline case as a forced checkpoint rather than pretending it was quiescent.

```python
import os, time, subprocess
SKIP = ('__pycache__', '.pytest_cache', '.git')

def newest_mtime(roots):
    m = 0.0
    for r in roots:
        for dp, dn, fn in os.walk(r):
            dn[:] = [d for d in dn if d not in SKIP]
            for f in fn:
                try: m = max(m, os.path.getmtime(os.path.join(dp, f)))
                except OSError: pass
    return m

roots = ['/root/AAA/rsi']
QUIET_S, DEADLINE_S = 300, 2700
last, changed = newest_mtime(roots), time.time()
t0 = time.time()
while True:
    time.sleep(30)
    cur = newest_mtime(roots)
    if cur > last:
        last, changed = cur, time.time()
    if time.time() - changed >= QUIET_S: break        # quiescent
    if time.time() - t0 >= DEADLINE_S: break           # forced checkpoint
# then: git add <narrow path list> && git commit
```

**Scope the commit narrowly** (only the paths this work owns). A repo with many concurrent lanes
carries other sessions' in-flight files; `git add -A` captures their half-finished work. Rollback for
any checkpoint commit is `git reset --soft HEAD~1`.

## 5. Queue-depth truth check

```python
import json, collections
rows = [json.loads(l) for l in open(queue) if l.strip()]
open_rows = [r for r in rows if r.get('status') == 'PROPOSED']
key = lambda r: (r.get('tool'), r.get('trigger'), r.get('proposal'))
print('depth:', len(open_rows), '| distinct findings:', len(set(map(key, open_rows))))
for k, v in collections.Counter(map(key, open_rows)).most_common(5):
    print(v, k)
```

If `distinct findings` ≪ `depth`, the producer appends duplicates. Fix the producer with an upsert
keyed on the same triple (increment a `recurrence` field and bump `last_seen`), never by pruning the
queue — pruning loses the recurrence signal that made the finding worth fixing.

## 6. Report shape that survives staleness

```
<HEADLINE: what changed, with timestamps>
AMENDMENT (HH:MM) — <finding> is superseded: <what happened>. <superseded text kept below.>
§ evidence table: claim | measured | when
§ what is genuinely SEAL-ready
§ what is PARTIAL / UNVERIFIED (never omit this section)
```

The amendment line and the UNVERIFIED section are the two things that keep an audit honest when the
substrate moves under it.
