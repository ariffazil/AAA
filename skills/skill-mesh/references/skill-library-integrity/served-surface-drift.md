# Served-Surface Drift — the runtime catalogue is a copy, not a view

## The class

A service exposes a *catalogue* of files — skills, prompts, rules, templates — over an address
space such as `skill://<name>/SKILL.md`. Unless the served root is a **view** of the authoring tree,
it is a **copy**, and every integrity check that reads the authoring tree is blind to it. The library
can be byte-perfect and the loader can still return nothing.

Three independent faults, each with a different signature and a different fix:

| Fault | Symptom | Fix |
|---|---|---|
| **Snapshot drift** | entry added to the mesh is unreachable | publish it into the served root |
| **Guard collision** | entry exists but is *refused*, not missing | publish a copy, not a link |
| **Discovery blindness** | index returns counts, not names | index reads the served root |

These fail independently. Fixing the first without the third leaves an operator unable to *find*
what is now served; fixing the second by widening the guard trades a real traversal boundary for
convenience (never do this).

## Detect

```bash
# 1. From a client: what does the surface actually answer?
#    "not found"       -> drift      (entry absent from the served root)
#    "rejected/escapes" -> collision (entry present, resolves outside)
# 2. What root does the PROCESS serve from?
tr '\0' '\n' < /proc/<pid>/environ | grep -i <ROOT_ENV_VAR>
# 3. Served root vs mesh count, and which entries cannot resolve:
for d in <served_root>/*/; do [ -f "$d<MARKER_FILE>" ] || echo "unresolvable: $(basename $d)"; done | wc -l
```

Read the two error strings as *different findings*. A "not found" leads you to publish; a
"rejected" leads you to change the publishing method. Treating them as one fault sends you to
widen a guard that was working correctly.

## Repair rules, ordered by how much they cost to get wrong

1. **Augment, never replace.** A served root commonly carries entries sourced from roots *outside*
the tree you are publishing from. A clean rebuild deletes them, and nothing reports the loss until
someone asks for one of those entries. Only add and repair; delete nothing.
2. **Copy, never symlink.** The containment guard that refuses an out-of-root link is correct.
Replace such a link with a real copy rather than relaxing the guard.
3. **Name = the directory's own basename.** Nested taxonomy locations must be flattened at publish
time, or the address resolves only for the shallow entries.
4. **A directory is an entry only if it directly holds the marker file.** Taxonomy containers are
containers, not entries; publishing them creates rows that 404.
5. **Skip per-harness variant directories** (`claude/`, `openai/`, `kimi/`, `qwen/`, …). Those are
one capability rendered several ways, not several capabilities.
6. **Report collisions; never resolve them silently.** Pick deterministically, print the loser, let
a human decide.
7. **Dry-run by default; tar the root before writing.** Print `would_add` / `would_repair` /
`collisions` and make the operator pass an explicit apply flag.

A worked implementation of all seven lives at `/root/scripts/publish_skills.py` (augment + repair,
copy-not-link, basename naming, known-outsider roots preserved, dry-run first) — reuse it rather
than rewriting the walk.

## Make the index name what it serves

A counts-only index is not discovery. A client cannot read what it cannot name, so a
"live-counted" index that lists `skills: 583` and no rows is the discovery half of the fault.

Have the index read its own served root at request time and emit `{name, uri, description}` for
every entry that (a) directly holds the marker file and (b) resolves inside the root — **the same
predicate the reader applies**, so index and reader cannot disagree. Cache against the root's
mtime plus a short TTL instead of walking per request.

**Never synthesise a description.** Frontmatter, then the first H1, else empty. An invented summary
in an index is a claim about a file rather than a reading of it.

## The residual defect is drift, not emptiness

Filling the snapshot fixes today. Unless a trigger republishes on change — a timer, a post-commit
hook, or replacing the copy with a real view — the surface re-rots on the same schedule as before.
Record the missing trigger as open debt, and say plainly that the repair is a snapshot rather than a
property. A repair reported as "done" when the class is "drift" is the next audit's finding.

## Verification checklist

- served-entry count before vs after
- every previously-unresolvable name now reads back, with a byte count
- one content hash compared on both sides for an entry you changed
- zero entries in the served root whose marker resolves outside the root
- the patch that changed the index is committed **and pushed**, and the serving **process has been
  reloaded** — a file on disk is a request, not a state
- the rollback artifact exists and its path is written into the receipt
