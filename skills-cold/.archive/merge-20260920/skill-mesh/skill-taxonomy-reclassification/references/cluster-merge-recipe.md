# Cluster Merge Recipe — collapsing a fragmented skill library

For when the mandate is a **merge** ("all MCP skills under one, with flow"), not a move. Read
`skill-taxonomy-reclassification` SKILL.md first; this file is the procedure and the pitfalls.

## The invariant

```
all names must resolve  ·  one owner per capability  ·  no content deleted
```

Aliases carry the old names. A merge that removes a name nothing points to is still a loss: the
next session's citation, the doctrine fragment, and the user's memory all use the old spelling.

## Procedure

1. **Backup and pin the baseline.** Record pre-merge counts from BOTH the canonical tree and the
   loader's exposed name set, and the canonical repo's HEAD sha. That pair (count, sha) is your
   rollback and your proof.
2. **Enumerate the cluster** across every tree, `-not -path '*/.archive*'`. Note each `SKILL.md`
   byte size and whether the path is real or a symlink — a symlinked leaf and a real dir look
   identical to `find` until you ask.
3. **Split the cluster into capability groups, then order each group into a flow.** The deliverable
   is a sequence a future agent executes: MCP → `discover → probe → integrate → test → govern →
   retire`; GitHub → `auth → clone → branch → commit/PR → CI → review → merge → release`;
   governance → `claim → evidence → witness → verdict → seal → receipt`. A group with no flow is a
   pile with a new name — that is the failure this whole operation exists to fix.
4. **Diff every candidate before merging it.** `cmp -s` then `diff`. Divergent frontmatter or a
   section only one copy has is content: fold it into the owner. Record specifically what you
   folded, because that sentence is the only evidence the merge was lossless.
5. **Choose the canonical owner name** — the spelling the loader will show, matching the naming
   convention in use (`forge-x`, not `FORGE-X`, if lowercase dominates).
6. **Write the owner `SKILL.md`** with the flow as its body, and push depth that is only sometimes
   needed into `references/` threaded from it — a per-topic reference file per sub-area, never one
   reference file per source skill.
7. **Alias, then verify.** Symlink every absorbed name to the owner. Then prove it: every old name
   resolves, and the SKILL.md count is unchanged or every decrement is named and justified.
8. **Commit under one `flock`.** See the SKILL.md rule — `index.lock` does not serialise a
   read-modify-write across concurrent agents.
9. **Receipt.** Write `MERGE_RECEIPT.md` (shape below) and state what you deliberately did not do.

## Grouping judgement (where merges go wrong)

| signal | action |
|---|---|
| same capability, different spelling | merge → one owner, aliases |
| same topic, one is *operating* and one is *selecting/procuring* | keep both, cross-link |
| platform-specific integration (one product per skill) | keep as leaves under a parent owner, not absorbed into it |
| organ-scoped variant (`<organ>-mcp-*`) | parent it under the organ owner, not the general one |
| policy text filed in a mechanics cluster | belongs to the governance cluster — leave it, note the handoff |
| draft / awaiting-ratification skill | never merge it; it has no settled owner |

## Umbrella shape — absorb the body, or alias the name?

Step 6 above describes folding depth into per-topic references. That is one of two shapes, and the
discriminator is whether the members are **distinct capabilities** or **one capability spelled
differently**:

| members are | shape | why |
|---|---|---|
| distinct capabilities sharing a topic | umbrella `## FLOW` + `references/<member>.md` per member, body byte-for-byte, member dir archived | each body is a *procedure*; summarising it into the umbrella destroys the procedure, and the merge becomes a deletion with extra steps |
| one capability, divergent spelling or drift | ONE owner body, every absorbed name aliased, divergent frontmatter folded in first | N reference files for one capability is the bloat the operation exists to remove |

So a 12-member cluster of genuinely different capabilities *earns* 12 reference files, and a
12-member cluster of near-synonyms earns one. Which one you have is decided by `cmp -s` / `diff` on
the bodies, never by the member count — and the receipt states the shape chosen and why.

Whatever the shape, **archive, never delete**: `mv` each absorbed member directory under a dated
archive path inside the canonical tree. The archive is part of the deliverable rather than
housekeeping — it is what lets a human review the merge with `ls` when they do not trust the commit
log.

## What the FLOW must do

Two tests separate a flow from a list of names:

- **Every branch is selected by an observable.** Write each row as `observable situation ->
  reference -> what it produces`. If you cannot say what an agent *sees* that distinguishes two
  branches, they are not two branches. The near-duplicate members are the real test — the several
  "an audit arrived" skills are exactly where the flow must supply the distinguishing observable,
  and if none exists then they genuinely are duplicates and belong folded.
- **Recovery-shaped clusters are a LADDER, not a set of peers.** Order by which failure you are
  recovering *from* (search -> extract -> extraction blocked -> fallback -> recovery), so an agent
  whose step just failed lands one hop from the fix rather than reading the whole set.

## Parallel agents on one canonical tree

Fanning clusters out to subagents is the right shape — but the **brief is the safety mechanism**, not
supervision. Give every child: the canonical tree path, the two invariants, the `flock` commit
idiom, the explicit do-not-touch list (doctrine, hooks, config, crons, ratified files), the receipt
path, and the honesty rule (*if a merge is uncertain, leave it and say so*). Budget the work so a
child that hits its ceiling reports partial rather than incomplete-and-silent.

## MERGE_RECEIPT.md shape

```
## Cluster: <name>
Before: N skills | After: M skills (K aliases)
Canonical owners created: <owner> <- absorbed: <a,b,c>
Content preserved from divergent copies: <what, specifically>
Content deliberately dropped: <what, and why it was literal duplication>
Git: <before-SHA> -> <after-SHA>
Uncertain / left alone: <list, with reason>
```

Counts come from `find`/`wc`, never from memory. "Uncertain / left alone" is a required field — a
receipt with nothing in it is a claim that the cluster was perfectly clean, which is rarely true.

## Pitfalls

- **`merged` is not a state until the loader agrees.** Verify through the loader's name set, not just
  the filesystem — `skill_view` resolves both directory and frontmatter names, so a leaf renamed for
  tidiness can break a citation that used the other.
- **Two case-variant trees are usually both real directories, not a symlink pair.** That is why they
  diverged: nothing was ever keeping them in sync. Do not assume the lowercase or the prefix-cased
  one is the source of truth — check mtime and the full `diff`.
- **A cluster count larger than the number of distinct capabilities means you counted aliases as
  skills.** Resolve real paths before reporting cluster size.
- **Do not merge a cluster whose members are updater-owned (bundled).** The updater re-seeds the
  stock layout and will recreate the duplicate you just absorbed; the alias survives, the merge does
  not.
- **The exit code of a piped command is the exit code of the last stage.** A merge loop that died
  halfway still reports success if its output was piped. Check the artifact, not the pipeline.
- **Resolve member ownership BEFORE dispatch, never at runtime.** Two workers will both see the same
  member when one member's directory sits inside another member's container, and bootstrap substrate
  skills must be excluded outright — moving one breaks session start for every agent. The orchestrator
  freezes a disjoint member list per worker, and each worker is told that anything off its list
  belongs to another agent. Overlap discovered mid-flight means two half-writes to one directory.
- **A merge whose members are a superset of another worker's cluster has no correct automatic
  resolution.** When two clusters plausibly own the same skill, decide by *which flow it serves* and
  put the loser in the winner's receipt as a cross-cluster note. Do not merge it in both places.
- **One member may be a v1/v2 pair where the filename does not say which is live.** Determine the
  supersession from body content and metadata, record it with evidence in the receipt, and preserve
  both bodies — a filename is a hint, not a source of truth.
- **Verify the file you wrote, not the draft in your head.** Re-open the written `SKILL.md` and print
  its parsed trigger count and reference list; a trigger list assembled in prose and never re-read is
  where the dropped-trigger failure hides.
