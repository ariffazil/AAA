---
name: public-claims-maintenance
description: "Use when public claims drift from reality or a figure has no source."
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
  - "two documents disagree on the number"
  - "which one is right"
  - "the slot number conflicts"
  - "the registry says X, this table says Y"
  - "this number has no source"
  - "which figures can I actually stand behind"
---

# Public Claims Maintenance

The audited direction of this work — checking someone else's report against live state — lives elsewhere (`arifos-evidence-policy` for a pasted verdict and its figures, `live-system-audit-discipline` for probing a running system). This skill is the **repair direction**: the claims a repository makes about *itself*, in files whose entire purpose is that people believe them.

When the repair is not to fix a sentence but to **publish a record a stranger can re-derive** — receipts, denominators, defects, each with a verifier beside it — go to `arifos-evidence-policy` → `references/verifiable-accountability-surface.md`. That is the constructive counterpart to this skill: here you repair a claim, there you make the estate's own numbers checkable from outside.

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

## An ungroundable FIGURE — repair the shape of the claim, never label its provenance

A published number can be neither stale nor arithmetically wrong and still be unsourced. The repair
is not "find the right number" — it is **change the shape of the claim**. The sorting step below is
what stops a repair pass from deleting true claims while keeping the false ones.

### 1. Sort every disputed figure BEFORE touching it

| Class | Test | Repair |
|---|---|---|
| **A — publicly traceable** | Resolves to a filing, a regulatory disclosure, a counterparty's own published statement, a press release | **Add the citation. Do not caveat it.** |
| **B — real, privately sourced** | You know its origin and the reader cannot go there | Soften the *attributive phrasing* to the honest reading; the figure stays |
| **C — a quotation with no home** | Presented as someone's words, but no document contains them | Convert to a labelled inference in the writer's own voice; never keep quotation marks around text with no source |
| **D — opinion / motive / register** | A judgement about intent, not a measurement | **Out of scope. Do not touch.** |

**Class A is the one most often mis-handled.** A figure that reads like insider knowledge is
frequently a published counterparty or regulatory disclosure — so the reader's suspicion is a
*sourcing* gap, not a *truth* gap. Widen the search to the counterparty and the regulator before
concluding a number is unsourceable; a two-party disagreement over a figure is settled by sourcing
it, never by hedging it. Hedging a sourced number weakens it for no gain.

### 2. Never label provenance on a public surface

The tempting repair — attaching an "internal estimate, no public confirmation"-style tag — is the one
move that makes the document **worse**, and it fails in both directions: to a hostile reader it
**confirms inside access** to the subject institution, while to an ordinary reader it asserts
something they cannot verify anyway. It is a confession formatted as diligence. It protects neither
the writer nor the reader.

### 3. The four legitimate repairs

When a figure cannot be sourced, change the claim rather than annotating it:

- **Widen to a range** — the honest uncertainty is usually the more defensible claim.
- **Reframe as a question** — moves the assertion from the writer to the reader without losing the point.
- **Attribute the ACT OF COUNTING, not the number**, to a named public source ("the contracts
  announced to date total …"). This is the commonest real repair, because the underlying facts are
  usually public even when the aggregate is the writer's own.
- **Drop the precision** — an order of magnitude the writer will stand behind beats a unit they will not.

### 4. Never invent a source

A number with no citation is **exposed**. A number with a fabricated citation is **defended** — it
survives exactly the audit that would have caught it. If the source cannot be found, that *is* the
finding: label it unverified and say so. Manufacturing a plausible report, page number, or URL is a
worse act than the unsourced figure it was meant to protect.

### 5. Repair the claim, not the voice

Where the text carries a named persona or a deliberate register, **the register is the writer's, not
the auditor's** — only the claim's shape moves. On the same ground: **label, never delete.** Deleting
loses the truth; a labelled claim keeps it as a labelled inference.

### 6. The pass is not landed until every rendering carries it

A published claim usually exists in more than one rendering — the canonical source, a generated
markdown mirror, a compiled bundle. Repairing one and reporting the pass complete is the standard
failure mode. Read back what the *served* surface returns, and report the pass as
`cited / labelled / replaced / deleted` counts, with `deleted` expected to be **zero** for any pass
whose rule is never-delete. A count of zero deletions is a result worth stating, not an omission.

## A claim about the system's own AUTHORITY STATE

A surface asserting a governance state — `SEALED`, certified, verified, all-clear — is not a stale
figure. It is a claim about the system, and the system's own state endpoint is its witness. Diff the
claim against that endpoint before treating the surface as merely behind:

```bash
curl -s <organ>/health | jq '{runtime_seal_state, working_tree, git_commit, verified}'
grep -rn 'SEAL ALIVE\|SEALED\|certified\|all green' <surface tree>
```

A badge the state endpoint contradicts is a **false public claim**, not stale copy. Two repairs
exist and they are not equivalent: change the surface, or change the state. A wording edit here is an
authority act, not bookkeeping — it either downgrades what the estate asserts about itself, or it
leaves the state alone and merely hides the gap.

**When the same badge is mirrored across many surfaces, neither repair is safe to do unilaterally.**
One edit leaves an inconsistent estate; editing every surface is a federation-wide brand decision
that sits above the repair lane. Present it as ONE binary — keep, or demote everywhere — together
with the witness that contradicts it, and let the sovereign decide. This is distinct from the
identifier case below: there, two contracts disagree and the estate can settle it itself; here the
estate is not in doubt about the fact, only about who may change what it says.

## Identifier claims — slot numbers, ids, versions of record

A roster table, an agent registry, or an identity map states *which* thing owns *which* identifier (a slot number, an agent id, a repo name, a version of record). These drift harder than status rows because identifiers get **renumbered**, and a renumber leaves every narrative copy of the old scheme reading as authority.

**Never hand the conflict to the human.** "Which one is right — you pick?" converts a provenance problem into sovereign attention that the estate can already answer. Run the trace, return a verdict. Escalate only if two equally authoritative **live** contracts still disagree after the whole trace — and name that outcome `GENUINELY_AMBIGUOUS`: it is a verdict, not a question.

1. **Find the named SOT.** A registry that declares itself canonical beats prose. Look for an explicit `SOT: <path>` line, a `_meta.rule` clause, or the file the others point back to.
2. **Probe the runtime registration path.** A seeder or id-map consumed by a running service is reality; a narrative table is commentary. `grep` the seeder's map before reading any prose.
3. **Read the commit history for the RENUMBER.** `git log -1 --format="%h %an %ad %s" -- <file>` on each contender. A renumber leaves a commit that says so and names the decision behind it. Age is evidence, not authority — a *newer* narrative doc can carry an *older* numbering if it was written from memory rather than from the registry.
4. **Classify the OUTLIER, not the winner.** Name the lone dissenter, who authored it, which era's scheme it encodes, and what superseded it. "Three live sources agree, one narrative is stale" is `RESOLVED` — not ambiguity.
5. **Conform the outlier in place and mark the SOT.** Add a header line to the narrative doc naming the registry as SOT and forbidding local renumbering, then commit with the evidence chain in the message. Reversible; no round-trip required.

```
VERDICT:  RESOLVED | GENUINELY_AMBIGUOUS
SOT:      <path> (why it wins)
AGREEING: <n> live sources — <paths>
OUTLIER:  <path>, authored <how>, era <scheme>, superseded by <commit>
MUTATION: <what was conformed> — reversible, committed <sha>
```

### Pitfalls for identifier claims

- **A stale DERIVED artifact outranks nobody but still lies.** A compiled or generated view (a bundle JSON, a generated `*_identity.json`) produced by a loader can lag the hand-edited law file. Do NOT hand-edit the generated view to match — that is the same disease one level down, and it will be regenerated. Fix the writer, or leave it and flag it; always name the writer in the report.
- **An identifier can be a ROLE, not a seat.** A duty can sit in a roster table looking exactly like a numbered slot. Before treating a row as a second owner, check whether the underlying contract assigns that duty to an existing owner. Two rows for one agent = a phantom seat: delete the row, don't renumber it.
- **"Three agree" is not a quorum unless the sources are independent.** Two copies of one document plus a derived view of it is one source wearing three hats. Count independent *registration* paths, not file paths.
- **The root cause is rarely the wrong number — it is that no sweep happens when the number changes.** A renumber landing without a repository-wide grep leaves three eras of numbering alive in one tree. Sweep the identifier, not just the file you were shown.

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
