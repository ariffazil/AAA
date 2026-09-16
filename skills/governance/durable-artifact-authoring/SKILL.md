---
name: durable-artifact-authoring
description: "Use when sealing session insight into federation canon."
capability_tier: fed-agent-subagent
---

# Durable Artifact Authoring

> **One fact, one owner, one axis.** Anything worth writing down is worth checking whether it was
> already written down.

## When to use

- Sovereign says "code this into the kernel / state / agents", "seal this", "extract the eurekas"
- You are about to create a doctrine file, instruction fragment, skill, or ledger entry from a session
- You are about to act on an external AI's review or proposal

## Step 1 — Sweep for an existing owner (mandatory, before writing anything)

```bash
git -C /root/AAA log --oneline -15
ls -la /root/AAA/instructions/<topic>.md /root/AAA/governance/<TOPIC>.md
ls -la /root/AAA/canon/<EUREKA-topic>.md
grep -rl "<topic-keyword>" /root/AAA/instructions /root/AAA/canon /root/AAA/eurekas /root/AAA/governance
```

Also check the fragment table in `/root/AAA/AGENTS.md` and the tail of
`/root/AAA/eurekas/eureka-entries.jsonl` — **each entry carries a `session` id**. If that id matches
this session, the work is already done.

**The tell:** a doctrine that feels fully formed on first draft is usually one you already wrote.
Context compaction erases the memory of authoring an artifact; it does not erase the artifact.

## Step 2 — Classify, then act

| Finding | Action |
|---|---|
| Owner exists and covers the whole insight | **Delete your draft.** Report the existing owner's path. |
| Owner exists, your pass adds a genuine delta | **Merge the delta into the owner.** Never create a sibling file. |
| No owner anywhere | Mint, then wire it (Step 3). |

**Deleting your own finished work is the correct move, not waste.** A second file stating the same
truth is permanent reconciliation debt; the sweep costs seconds.

## Step 3 — Wire every minted artifact to three surfaces

1. **Boot / fragment** — a pointer in the always-loaded layer so agents actually see it
   (`/root/AAA/instructions/base.md`, the fragment table in `/root/AAA/AGENTS.md`).
2. **Ledger** — an entry in `/root/AAA/eurekas/eureka-entries.jsonl` (`session`, `evidence`,
   `truth_class`, `verdict`) so the reasoning is traceable.
3. **Agent behaviour** — a skill (or a section in the skill that governs the task class) carrying the
   *procedure*, not the doctrine prose. Doctrine says what is true; the skill says what to run.

Commit each surface so the seal is verifiable, and run the repo's doctrine-status gate if one exists.

## Step 4 — Declare residual debt honestly

If the rule is doctrine-layer only (no kernel enforcement yet), say so in the artifact and in the
report: *"detection is debt until it can say NO."* Do not let prose binding be read as a gate.

## Pitfalls

- **Foreign seal blocks are never ingested.** An external artifact that copies the seal *schema*
  (`dS`, `kappa_r`, `peace2`, `confidence`, `shadow:` list, `verdict:`) witnesses nothing. Borrowed
  scalars are decorative until computed here. **Accept the argument, verify the citations, refuse the
  numbers.** Shape is not witness.
- **An artifact that warns against false precision while emitting unbacked numbers is committing the
  error it names.** Name that explicitly in the verdict.
- **Score external reviews into four buckets, not a prose reaction:** ACCEPTED INTO CANON ·
  OWNED AS OVERREACH (your errors it caught — fix them *and* record the correction log so they cannot
  be re-imported) · REJECTED FROM INGESTION (invented numbers, copied seal block) · UNDER-WEIGHTED BY
  IT (what it missed that matters more than what it caught).
- **Verify citations before trusting an argument.** `web_search` each load-bearing reference. Real
  sources argue; invented sources perform.
- **A review of work already done is a merge task, not a build task.** Run Step 1 before treating any
  incoming review as new work.
- **A dropped field term makes an equation look clean and lie.** When a doctrine states a pattern, the
  constraint field is part of the claim, not decoration.
- **Split owners are worse than no owner.** Two files stating one truth diverge, and every later reader
  picks a different one.
