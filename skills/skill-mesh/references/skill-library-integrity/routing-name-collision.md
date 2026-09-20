# Routing-Name Collision — the capability that is on disk and can never load

## The mechanism

A loader indexes skills by the frontmatter `name:` field, falling back to the folder basename, and
dedupes **first-wins**: the first body it meets under a given name is kept, and every later body with
that name is skipped with a silent `continue` — no log line, no warning, no counter.

So two different bodies declaring one routing name means one of them is a **capability that exists on
disk, is byte-perfect, passes every file check, and can never be reached**. Nothing fails, therefore
nothing reports it. This is the failure mode most likely to be misdiagnosed as "the agent forgot that
procedure" — the agent never had it.

**Read the loader's real code before quoting the rule.** Do not build the diagnosis on a comment, a
docstring, or another skill that describes the loader: those are written from intent and drift. Find the
function that builds the catalogue and read the two lines that add to and test the `seen` set. In a
Hermes install that is `tools/skills_tool.py` in the installed package (not a dev checkout under the
home directory), and the shape is:

```python
name = frontmatter.get("name", skill_md.parent.name)
if name in seen_names or name in disabled:
    continue
seen_names.add(name)
```

Walk order decides the winner, so "which body is live" is a property of the scan, not of the file.

## Measure before you alarm — separate address bands from real collisions

A same-name group is **not** automatically a defect. Classify every group by its **body hash**:

| Group shape | Meaning | Action |
|---|---|---|
| N paths, **one** body hash | the intended view tree — bands (`substrate/`, `primitives/`, `capabilities/`, `domains/`) addressing one body | none; record and leave it |
| N paths, **different** body hashes | a real collision; at least N-1 bodies can never load | repair |

**The number that matters is `groups sharing a name whose bodies differ` — never `groups sharing a
name`.** Measured on one store: 60 same-name groups reduced to 2 real collisions, an overstatement of
30x by the naive count. Publishing the raw figure sends a future agent to "repair" dozens of address
bands that are working exactly as designed, and each of those repairs degrades the addressing tree.
Report the split (bands vs collisions), not the total.

## Repair, in order of cost to get wrong

1. **Read both bodies before choosing a winner.** The usual convergence rule is *newest survives* — but
   check first that the loser is not a content **superset**. A newer body can be a deliberate
   condensation, and the older one can hold rules the newer dropped by accident.
2. **Decide "lost content" by CONCEPT, not by LINE.** See the trap below.
3. **Freeze the loser, never delete it** — per-file digests computed before the move, plus an undo line.
4. **Repoint every address of the surviving name**, including the retired body's own home path, then
   sweep the mirror trees. A collision repaired in the store but left dangling in a harness view is
   still a broken name, and the census will report it as one.
5. **Remove a case-twin directory left empty by the retirement.** Casing alone is a second identity; an
   empty directory is still one.

Verify with three independent witnesses: 0 collision groups remaining (re-run the scan), 0 dangling
links across every tree, and the census's own `broken_symlinks` field.

## The trap that wastes the most time: a line diff is not content-loss proof

When choosing the survivor, the tempting evidence is `diff old new | grep '^<'` — the "removed" lines.
**That output is not a finding.** A consolidated body rewrites rules in fewer words, moves them into a
new section, or merges two clauses into one, so a rule that is fully present reads as deleted because
its *sentence* changed. Acting on it means re-adding content that already exists — which bloats the
survivor and re-introduces the duplication the merge removed.

Before restoring anything a diff appears to have dropped: **grep the NEW body for the CONCEPT.** Search
the distinguishing noun phrase of the rule (the heuristic's name, the threshold value, the field name),
not the old sentence. Only a concept that is genuinely absent is a loss. Measured: a named heuristic
appeared twice in the newer body, better worded, while the line diff reported both original occurrences
as removed.

Same rule in the other direction: before trusting a *claim* that a consolidation preserved everything,
run the retention gate (`scripts/discovery_guard.py`) — but a gate that checks names and phrases will
still miss reworded substance, so pair it with a concept grep on the rules that matter most.

## The compound defect to look for while you are already in there

**A canonical address that resolves into a DIFFERENT tree** — a harness profile, a vendor install, a
per-tool overlay — means the store publishes a body it does not hold. Every file check inside the store
reads it as present; the body belongs to another tree; and no check spans both, so the two can drift
apart silently. This is the one-writer rule violated by a symlink.

Detect it by resolving each address of the colliding name and comparing its root against the store root:

```bash
for p in <address> <address>; do readlink -f "$p"; done   # a path outside the store root is borrowed
```

Repair by re-pointing the address at the store's own body (or, if the store has no body, by promoting
one — see `references/multi-root-entropy-audit.md` §8b). Never leave a canonical address borrowed: it
is the defect that makes "the store is the source of truth" true on paper only.

## Run it

`scripts/collision_audit.py <store_root>` prints every same-name group split into bands vs collisions,
with both body hashes, and flags any address resolving outside the store root. Read-only.
