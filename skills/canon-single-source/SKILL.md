---
name: canon-single-source
description: "Use when one invariant is duplicated and copies disagree."
---

# Canon Single-Source

One rule, five files, five slightly different wordings. Each file reads correct on its own, every
surface contradicts the next, and no compiler objects. This skill is the repair: find the sealed
authority, own the invariant in one machine-readable module, make every surface derive from it, and
test the drift instead of trusting the prose.

Division of labour that makes this necessary: **a resource does not enforce anything.** Resources,
docs and schemas supply context to a model; enforcement is a check on the execution path. So
"document the right value better" fixes nothing — the surfaces keep diverging because nothing derives
from anything.

## When this is the right skill

- two surfaces of one system answer differently about the same invariant (a name, a threshold, a
  capability count, a status)
- a constant appears as a dict literal or hardcoded default in several modules
- a tool schema advertises a parameter, mode or field the handler cannot actually accept
- an amendment was ratified but the code still enforces the pre-amendment value

If only one definition exists, this is not the problem — look for the single wrong value instead.

## Procedure

### 1. Enumerate definition sites, not mentions

```bash
grep -rn '<the invariant name or literal>' --include=*.py <pkg> | grep -v test | grep -v build/
```

Separate *definitions* (dict literals, dataclass defaults, hardcoded lists) from *mentions*. Five
definitions is normal; that number is the size of the repair, and it is usually bigger than expected.

### 2. Find the sealed canon, not the rendered surface

The rendered resource is downstream of authority and is frequently the copy that drifted. Look for
the ratified artefact — a signed genesis table, charter, sealed manifest — and read its structured
fields (`rule`, `sealed_range`, `doctrine_note`, amendment note) before deciding which of two
conflicting values is canonical.

**Hard rule:** a number written in a resource is a claim, not authority. Before adopting it, ask
whether an amendment already superseded it. Amendments reach canon far more reliably than they reach
code, so the copy you are about to "correct" may be the only honest one.

### 3. Write one module that owns it

Shape that survives contact:

- one entry per item, immutable (frozen dataclass or literal tuple)
- **frozen machine id** (persisted in receipts, policy hashes, ledgers) as a separate field from the
  **display name** — normalise display freely, migrate ids never
- aliases declared explicitly, so reconciliation of historical prose is mechanical
- every derived bound computed from the canon's own field, never retyped as a new literal
- named renderers (`doctrine_block()`, `catalogue()`, `description_map()`, `table()`) returning the
  exact shapes the surfaces already emit, so callers change import lines and nothing else

### 4. Derive, or mirror under test

Every old site either imports from the canon or mirrors it. Where an import is impossible (circular
import, cross-language, test double), mirror **and** add a test asserting equality. A mirror with an
equality test is a copy that cannot silently drift; a mirror without one is the bug you started with.

When two names for one concept are both sealed (an internal register and a public register), encode
the dual registry explicitly with a layer field. Do not "resolve" the duplication by picking one —
that deletes a ratified distinction and looks like progress.

### 5. Test every surface, plus one grep

For each renderer assert: the canon block is a substring of the rendered text; each item's identity
line matches; each numeric value sits inside the canon band. Then add the cheap one that catches what
you missed — a package-wide scan for the stale literal, failing with file:line for every hit.

```python
for path in pkg.rglob("*.py"):
    if "test" in path.parts:
        continue
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if "0.90" in line and "cap" in line.lower():
            offenders.append(f"{path.relative_to(pkg)}:{n}")
```

This scan is what finds the fourth and fifth copies. Run it before claiming the surface is clean.

### 6. Prove the live surface, not the diff

Restart the service, then read the surface back: fetch the resource and call the tool. A source-level
assertion proves the module is right; only a live read proves the deployed binary serves it.

## Wire contracts are part of the runtime

A schema advertising what the handler cannot accept is the same defect class: declaration drifted from
the thing that executes. It presents as an unhelpful argument error, not as a schema bug, so it burns
time.

- Build the advertised surface from the executable: `inspect.signature(handler)`, filter the declared
  parameter set, and drop announced-but-unreachable fields **loudly at registration** (one log line
  naming tool and fields). Silent filtering is the same lie in a quieter register.
- Watch for handlers being *reassigned after registration*; the signature that matters is the one on
  the live handle, not the one in the module you were reading.
- Keep the offending field name in any sanitised validation message. Collapsing every cause into
  "invalid input types" means the caller cannot self-correct and you cannot triage.
- Verify with a real call through the transport, not with a unit test of the handler.

## Verify a change when the suite is already red

Repos of this age carry pre-existing failures. Claiming "no regression" from a run that was already
failing is not evidence, and neither is a green run on a subset you chose.

```bash
git worktree add /tmp/base HEAD          # pristine baseline, no stash, no disturbance
cd /tmp/base && PYTHONPATH=/tmp/base <venv>/bin/python -m pytest <same selection> -q > /tmp/base.log
cd <repo>   && <venv>/bin/python -m pytest <same selection> -q > /tmp/new.log
sed 's/ - .*//' /tmp/base.log | grep '^FAILED' | sort > /tmp/b.txt
sed 's/ - .*//' /tmp/new.log  | grep '^FAILED' | sort > /tmp/n.txt
diff /tmp/b.txt /tmp/n.txt    # empty = no regression, stated as a diff, not a vibe
```

Use the identical `-k` selection on both sides. If a failure appears in one list and not the other but
the selection excluded it, probe it directly on the baseline before reporting either way.

## Committing when other writers share the tree

A shared repo with several agents and a lane-identity gate makes "commit my files" non-obvious.

- Never `git add -A`; you will claim someone else's work.
- When the identity gate inspects the committer, commit through the lane wrapper, not raw `git commit`.
- When the tree is dirty with other people's edits, stage only your paths through a throwaway index so
  the shared index is untouched:

```bash
GIT_INDEX_FILE=/tmp/idx git read-tree HEAD
for f in <your paths>; do GIT_INDEX_FILE=/tmp/idx git add "$f"; done
GIT_INDEX_FILE=/tmp/idx <lane-wrapper> commit -m '...'
```

Then reset the real index back to HEAD so the next agent finds the tree as they left it.

## Pitfalls

- **Adding a resource that documents the correct value.** It becomes the sixth copy. Derive or delete.
- **Renaming a persisted id to match the display name.** Receipts and ledgers stop resolving.
- **Migrating enforcement clamps in the same pass as the display fix.** A clamp the system refuses to
  cross is a governance decision. Measure it, publish the count, name what would have to change, and
  leave the decision where it belongs — an instrument that classifies sites and exits 0 is the honest
  deliverable.
- **Trusting the tests as canon.** Tests can assert the stale value and agree with the drifted code
  while both disagree with the ratified canon. A red test is not automatically a bug in your fix.
- **Collapsing two conflicting values into whichever is in the file you opened first.** Find the
  sealed authority before touching either.
- **Silently filtering a phantom parameter.** Filter, but log the drop; otherwise the next caller has
  the same problem with no trace.
- **Reporting a subset run as "the suite passes".** Say which selection ran and what the baseline was.
