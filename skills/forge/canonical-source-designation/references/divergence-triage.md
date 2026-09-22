# Divergence triage — decision table and probe recipes

Depth for `canonical-source-designation` Steps 1–2. Load when a specific pair is genuinely hard to
call.

## Probe recipes

### Which tree executes

```bash
# every unit that names the organ, with the exact ExecStart and its working dir
grep -H -E '^(ExecStart|ExecStartPost|WorkingDirectory|Environment)' /etc/systemd/system/<organ>-*.service

# resolve the package under the unit's own path setting
PYTHONPATH=/root python3 -c "import <pkg>; print(<pkg>.__file__)"

# whether any unit references the suspect tree (expect no output)
for f in /etc/systemd/system/<organ>-*.service; do grep -l '<suspect>' "$f"; done

# live service identity — the running process's argv and cwd
tr '\0' ' ' < /proc/$(pgrep -f <organ> | head -1)/cmdline; readlink /proc/<pid>/cwd
```

### How frozen is the duplicate

```bash
# one bulk commit touching every diverged copy == a frozen snapshot, not an active tree
git -C <tree> log -1 --format='%h %ci %s' -- <path>
for f in <names>; do git -C <tree> log -1 --format="$f %h %ci" -- "<subdir>/$f"; done
```

```python
# line-level unique counts — the actual classifier
import difflib
def uniq(a_path, b_path):
    a = open(a_path).read().splitlines()
    b = open(b_path).read().splitlines()
    d = list(difflib.unified_diff(a, b, n=0))
    return ([l for l in d if l.startswith('-') and not l.startswith('---')],
            [l for l in d if l.startswith('+') and not l.startswith('+++')])
```

### Recovering a true pre-state when a backup captured the wrong file

When another lane's backup holds something that is not the original (a draft, a shim, a file you were
mid-way through writing), recover from the version-control object store and **prove** it:

```bash
cd <repo>
git cat-file blob HEAD:<path> > <recover-dir>/<name>          # materialise the committed original
[ "$(git hash-object <recover-dir>/<name>)" = "$(git rev-parse HEAD:<path>)" ] && echo MATCH
cp -p <recover-dir>/<name> <hold-dir>/                        # place beside, do not replace
```

`git hash-object` returning the same OID as `git rev-parse HEAD:<path>` is a byte-equality proof, not a
copy claim — prefer it to quoting a sha256 computed elsewhere. Then compare against the hold set's own
recorded hashes: agreement between two independent sources is the strongest confirmation available.

## Decision table for a confidently-diverged pair

| Observation | Read it as |
|---|---|
| unique lines are only docstrings/comments/blank | strict subset — safe to converge |
| unique lines are old signatures of functions that still exist, changed | superseded versions — converge, record why |
| unique lines are a whole function/branch the winner lacks entirely | **HOLD** — read both before deciding |
| loser is much larger than winner | suspect a *replaced full implementation*; the winner may be a delegating shim |
| loser filters on a field the current writer no longer sets | wrong on current data, not merely older — returns empty with no error |
| loser has its own log writer, own store, or rewrites an append-only file | a second writer — converge to one writer, reason recorded |
| both sides agree on one metric but not another | two universes — report both, do not pick |

## Two-universe signature

Derived, not guessed — reconstruct the arithmetic before claiming a disagreement:

```
mean over A's decisive rows = (a1 + a2) / 2
mean over B's decisive rows = (b1 + b2) / 2
```

If each figure reproduces exactly from its own store's rows, the surfaces are not contradicting each
other; they are solving different problems over disjoint populations. That is a *finding*, and it
usually means an observation was double-counted (one event, two hypotheses written against it) or a
store was split. Both are data defects that survive code dedup.
