# Reconciliation annex recipe

Use when a deliverable asserts a single coherent account and your own knowledge base disagrees with
itself about it. The annex is published **with** the deliverable, framed as a finding — not as a
correction to the source files.

---

## 1. Conflict table

Four columns, one row per source file that speaks to the disputed fact:

| Source file | Value | Label it uses | Status |
|---|---|---|---|
| `<path/to/file-a>` | 21.0 Ma | "canonical collision age" | Sealed ledger |
| `<path/to/file-b>` | ~23 Ma | "collision onset" | Later synthesis |
| `<path/to/file-c>` | 16–12 Ma | "arc–continent collision" | Legacy model |

Record the **label** as well as the value. A bare phrase like "canonical" is frequently the source
of the problem: it claims authority for one of two genuinely distinct events.

## 2. Classification

Two verdicts, and they lead to different proposals:

- **Reconcilable** — the same name has collapsed two distinct events. Resolution is to adopt
  explicit dual naming ("onset ~23 Ma" and "peak ~21 Ma") and retire the ambiguous bare phrase.
- **Superseded** — an older model still sitting in the tree, structurally incompatible with the
  current one. Resolution is to mark it deprecated with a pointer, or reconcile it, but never to
  leave two mutually exclusive models in the same directory.

Do not force a single winner when the honest answer is that two events were merged. Retiring the
ambiguous label is the actual fix.

## 3. Check the arithmetic before the geology

Source documents often contradict themselves numerically before they contradict each other. Compute:

- does a stated duration match its own date range? (a `duration: 15.0` with a comment "~21 Ma to
  present" is 21, not 15)
- does a chronology list the events its own narrative calls headline findings?
- do unit conventions agree across rows of the same table? (`mm/yr` next to `m/Myr` in adjacent
  rows is a factor-of-1000 trap)
- are formation/asset names spelled consistently, or visibly corrupted?

These land in the annex as separate bullet items. They are cheap to find and they signal the corpus
was read rather than skimmed.

## 4. Proposed resolutions

End with a numbered list the owner can ratify item by item. Each item names the file, the change,
and why. Keep it to the smallest set that removes the contradiction:

1. Adopt explicit dual ageing; retire the bare "canonical" phrase.
2. Add the missing event to the chronology, with its reclassification stated inside the entry so it
   survives extraction by someone skimming.
3. Mark the legacy file deprecated with a pointer to the current one.
4. Fix the self-contradicting field, or replace it with explicit named fields.
5. Re-audit corrupted names before any of it is reused.

## 5. State what you did not do, and why

Close the annex with the boundary you held:

> This reconciliation was executed as a read-only audit. No file in the resource base was modified.
> The sealed ledger is an authority boundary — re-sealing a sealed artifact is not housekeeping.

That sentence is what makes the annex a contribution rather than an unauthorised edit. It also
tells the owner the exact decision that is waiting for them.
