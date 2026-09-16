---
name: public-claims-maintenance
description: "Use when a repo's public claims drift from reality."
version: 1.0.0
triggers:
  - "the README says the wrong version"
  - "status table is stale"
  - "update the gap registry"
  - "SECURITY.md says no known CVEs"
  - "docs(truth)"
  - "who maintains this"
  - "our public claims disagree with reality"
  - "a fact changed and the docs did not"
---

# Public Claims Maintenance

The audited direction of this work — checking someone else's report against live state — lives elsewhere. This skill is the **repair direction**: the claims a repository makes about *itself*, in files whose entire purpose is that people believe them.

Fire it whenever a fact changes (a release lands, a report is accepted, a review starts, a version bumps) and the surfaces stating the old fact are not swept. Status tables, `SECURITY.md` gap registries, version pins, and provenance sections are all in scope.

## The one rule

**Every row must name its own gap.** A status table's value is not that it is flattering — it is that a reader can act on it. Fixing a false claim by substituting a stronger one is the worst outcome available: you have traded a stale claim for an inflated one, in the file people trust. Downgrade honestly; never upgrade on the strength of work merely having started.

## Procedure

1. **Grep the fact, not the row.** A stale value lives in N places — a table row, inline prose, and an embedded machine-readable block near the top of the file.
```bash
grep -rn "<stale-value>" <file>      # table + prose + front-matter/SOT block
```
Sweep every hit in one pass. Fixing only the row leaves the others contradicting it four lines apart.

2. **Ask what event makes each sentence false, then check whether it already happened.** The trigger is usually earlier than the row's author assumed, and the row has been wrong for longer than anyone noticed.

| Row | Naive trigger | Actual trigger |
|---|---|---|
| `No CVE disclosure history / No known CVEs` | a CVE is assigned | a report is **accepted** — assignment is months of process later |
| `No independent penetration test — Open` | an audit report is published | an external reviewer **starts reviewing** |
| `PyPI package: <version>` | someone remembers to bump it | the publish **succeeds** |

3. **Repair shape.**
   - `Open` → **`In progress`**, naming what is still missing ("review under way since <date>; nothing published yet").
   - Never write `Verified` / `Complete` because the work feels done. When the file defines those labels, its own definition is the gate — read it back and apply it literally.
   - Leave severity alone unless the underlying fact changed. A truth sweep is not a re-grading exercise.
   - Add the fact where a stranger would look for it — a disclosure-history table, a maintainer section — rather than only amending the row that was wrong.

4. **Verify from outside the working tree.** A local `grep` proves the file on disk, not what readers see, and a CDN read seconds after a push can serve the old bytes.
```bash
gh api repos/<owner>/<repo>/contents/<file> -q .content | base64 -d | grep -c "<stale-value>"   # expect 0
```

5. **Commit the sweep on its own** — `docs(truth): ...`, stating what was stale and why — separate from any behavioural change or version bump. Otherwise a reviewer cannot tell whether the claim moved because reality moved or because the docs were corrected.

6. **Re-read before committing.** These files are the ones most likely to be edited concurrently by another session; rebase rather than force, and confirm the pushed result from outside. See `live-multiwriter-audit` for the push-race and pipeline-exit-status traps.

## Provenance: a claim about who built the thing

When a project is built by agents under a human maintainer, the readership cannot see that arrangement in the artefacts: commit authors are machine handles and packaged METADATA carries the human's name. Read together they look like pseudonyms — i.e. like something being hidden, which is the opposite of the intent. There are only two honest options:

1. state the arrangement where it will be read (a `README` section, plus the `SECURITY.md` header a reporter reads first), or
2. cut the sentence back to what the cited evidence actually shows.

Verify the artefacts before writing the sentence — `git log -1 --format='%an <%ae>'` on the fix commits, plus the built package's `Author` / `Maintainer` METADATA — then state **who is accountable**, not merely who ran what. "The design and the judgment are mine, the implementation is theirs, and the bug is mine to answer for" carries the claim; "built by agents under my rules" is invisible to the reader it is meant to inform.

## Pitfalls

- **A gap registry is not a wish list in either direction.** Understating a closed gap loses a reporter's trust exactly as fast as overstating an open one. Both are the same defect: the row no longer describes reality.
- **A pinned version in a status table is a claim about the distribution channel, not about the repo.** The repo can hold the fix for weeks while the published artifact predates it. Probe the published artifact's version and upload time against the fix's commit date, and read the release pipeline's last run, before writing that `pip install <pkg>` ships the fix.
- **A stale read is not a failing write.** An index/CDN read taken seconds after a push or publish returns the pre-write value — and two such sources can share one cache, so agreement between them is not corroboration. Re-read through a provider API or version-specific endpoint before concluding the write did not land.
- **Amending without a trail.** Where a published claim has to change, leaving the original and appending the correction is evidence; a silently-edited claim is not.
- **Sweeping one file and calling it done.** The same stale fact usually appears on the site, in an `llms.txt`/manifest surface, and in the package description. Grep the federation, not the file.

## Companion skills

- `live-multiwriter-audit` — concurrent-writer and push-race discipline.
- `responsible-disclosure-handling` — when the claim being repaired concerns an accepted vulnerability report.
- `durable-artifact-authoring` — for sealing an insight into canon rather than repairing a surface.

*DITEMPA BUKAN DIBERI*
