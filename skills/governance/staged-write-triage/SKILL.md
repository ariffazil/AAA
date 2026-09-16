---
id: staged-write-triage
name: staged-write-triage
risk_tier: low
floor_scope: [F1, F2, F4, F7, F11]
version: 1.0.0
owner: Hermes
description: "Use when an approval or staged-write queue has piled up."
trigger_when:
  - approval_queue_has_accumulated
  - staged_memory_or_skill_writes_awaiting_review
  - deciding_whether_to_approve_a_batch_of_staged_changes
  - a_background_process_keeps_staging_writes
  - user_asks_to_approve_all
tags: [meta, triage, approvals, memory, governance, hygiene]
---

# Staged Write Triage

> For any queue of changes staged for approval: memory writes, skill writes,
> file edits, outbound messages. The class-level problem is the same everywhere —
> work is produced on one side and consumed on the other, and when the consumer
> stops, the queue keeps growing and looks like output.

---

## §0. USE WHEN

```
USE WHEN:
  1. An approval/staging queue has grown large or has sat untouched
  2. The human says "approve all" (or asks you to clear the queue)
  3. A background review or daemon keeps staging writes
  4. Deciding whether a staged change is memory-worthy, correct, or safe
  5. Cleaning up a queue of generated-but-unapplied work in a repo or store
```

---

## §1. THE FAILURE MODE: A QUEUE WITH NO CONSUMER

A staging gate exists to stop bad writes. If nothing ever consumes the queue, the
gate stops doing that and starts doing something else: **accumulating**. Work that
is produced and never resolved reads exactly like output while being amnesia.

Two signals, both easy to measure:

- **Age.** Items older than the review cadence nobody acted on.
- **Same-edit-re-derived.** The same entry appears in several batches with
  different replacement text, because each run re-derived it independently.

When the second signal is present, **"approve all" was never a coherent action.**
The batches overwrite each other: applying them in order means the newest silently
clobbers the rest, and an older batch may **delete** a standing rule that a newer
one kept. Say this plainly rather than executing the instruction literally.

---

## §2. MEASURE BEFORE ACTING

Never replay a pile. Read every payload in full first, then produce counts:

- how many items, grouped by **theme** (which entries/targets they touch)
- how many **distinct generations** of each theme
- how many items are **dead on arrival** — their anchors/targets no longer match
  anything live, so they would fail on apply regardless of content
- how many would **remove** something a live rule or entry currently holds

A batch built against a stale snapshot is producer drift, and the fix belongs
upstream. Do not treat it as a priority conflict to resolve here.

---

## §3. THE TWO GATES — KEEP THEM SEPARATE

| Gate | Governs | Failure mode if wrong |
|---|---|---|
| **Staging gate** | *when* a write lands — queues it for human review | a queue with no consumer is not a gate, it is an accumulation |
| **Content gate** | *whether* a write is worth keeping at all | inflation: every observation becomes permanent |

The content questions, in order: is this derivable from something that already
exists? (reject) · would a capability vanish if this were deleted tomorrow?
(reject) · does it change a future decision? (record, do not store) · is this a new
example or a new rule? (example → record, rule → candidate).

**When staged writes accumulate, fix the content gate — do not route routine
approvals to the sovereign.** Staging every write for a human is a tax on their
attention for work an automated filter can adjudicate. Answer the content defect at
the content layer; conflating the two gates makes a filter problem look like a
governance problem.

---

## §4. TRIAGE PROCEDURE

1. **Archive verbatim before touching anything.** Dumping the raw payloads to a
   dated registry is the only proof the queue existed. A failed content gate means
   *compress to a ledger*, not delete.
2. **Classify each item: SALVAGE · REJECT · DEAD.** State the reason for every
   verdict in the receipt; an unexplained rejection is indistinguishable from a
   dropped item.
3. **Apply the salvaged content at the right layer** — the destination has its own
   rules (a memory store has budgets and a memory map; a skill has frontmatter
   conventions). Resolve those rules before drafting, not after.
4. **Move processed items out of the pending path**, into a dated processed
   directory. Never delete; never leave them where the next run will re-read them.
5. **Write a receipt** — counts, verdicts, reasons, what was salvaged, what was
   reversibly removed, and how to reverse it.
6. **Fix the producer** if the same generation reappeared. The queue emptying is
   not the success criterion; the queue staying empty is.

---

## §5. REJECTION CLASSES THAT RECUR

- **Third-party identity** — given name plus employer plus social handle, or a note
  about someone's private disclosure — going into a store that renders in **every**
  session, including rooms other people read. PII belongs in the vault.
- **An inferred fact asserted as certain.** An age is given, a birth year gets
  written. Unknown stays unknown until the human states it.
- **Psychological or affection modelling of a third party.** Check the human's own
  standing rules first: where they forbid labelling a person, no entry of that
  shape is acceptable however well-evidenced it looks.
- **Compression that drops a clause.** Shortening an entry is fine; losing a fact
  from it is not. Diff before and after and confirm every clause survives.
- **Anything derivable from an existing artifact.** Do not pay ongoing rent for a
  fact that a loaded document or skill already carries.

---

## §6. REVERSIBILITY AND REPO HYGIENE

- Archive and processed directories, never deletes. Prefer moving files to
  discarding content; the human can always reverse a move.
- **Personal-data directories must be gitignored in any repo with a remote** —
  staged write queues, inbound message queues, memory stores. Staged writes are
  evidence and belong where they can be read, not where they can be pushed.
- If a resolution commit already carries them and the commit is **unpushed**,
  re-commit without them and keep the files on disk: `git rm -r --cached <dir>`
  plus a `.gitignore` entry. That is a pre-push fix, not a history rewrite.
- If the environment refuses a write to a protected config, record it as an open
  item. Do not route around a guard with a shell command — the guard is the point.

---

## §7. ANTI-PATTERNS

```
❌ Replaying the queue in order        → later batches clobber earlier ones.
❌ Approving all because the human said so → the instruction assumed coherence it lacks; say so.
❌ Deleting staged items to "clean up" → the archive is the only proof; move, never delete.
❌ Leaving processed items in place   → the next run re-reads and re-stages them.
❌ Staging every write for a human    → attention tax for work a filter can do.
❌ Fixing the queue, not the producer → it refills; the empty queue is not the goal.
❌ Writing inferred facts as certain  → a guess becomes a permanent premise.
```

---

## §8. REFERENCE

- `references/queue-resolution-recipe.md` — concrete resolution steps, the receipt
  shape, and the before/after verification that the queue stayed empty.

---

*DITEMPA BUKAN DIBERI*
