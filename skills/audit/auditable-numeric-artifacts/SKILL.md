---
name: auditable-numeric-artifacts
description: "Use when issuing checkable numbers. Source every figure."
version: 1.0.0
risk_tier: low
floor_scope: [F2, F9]
autonomy_tier: T0
tags: [epistemic, numbers, primary-source, verification, artifacts]
---

# Auditable Numeric Artifacts

> **DITEMPA BUKAN DIBERI** — A number you cannot quote from its source is a liability, not an asset.

## When this applies

Any deliverable carrying numbers a reader can independently check: financial or operational
analysis, institutional briefings, due-diligence notes, data-backed PDFs and reports. The
governing assumption is **the recipient will open the primary document and check you line by
line** — not because they distrust you, but because that is the correct way to read an
evidential document.

This is the authoring counterpart to the audit skills. Those govern reading someone else's
claims adversarially; this governs producing your own so they hold up.

---

## The layer that rots is the number layer, and it rots silently

Measured failure mode, 2026-09-19 — a human-facing explanation of this system was audited before it
reached its outside reader. Eleven claims in it. The structural claims all held: the architecture,
the authority analogy, the floor count, the named-citizen count. **Every error was a number, and
every error had one cause: the figure was recalled from a previous working session instead of
measured at write time.**

The author caught one himself and corrected it — then the correction was also wrong, including its
denominator. Two of the three figures in that correction matched nothing ever recorded. The reader
would have had no way to tell, because nothing in the text distinguished a measured figure from a
remembered one.

**The rule that follows.** A number that reaches a human must carry its witness. In practice, one of:

- the path or query that produced it, inline or in a footnote;
- the command output pasted verbatim;
- an explicit `UNVERIFIED` label when no witness exists.

An unwitnessed number is not a lesser fact — it is a different kind of object, and it must be
labelled as such or omitted.

**The second-order trap: a stale number is not a false one.** Of the figures audited, two were
*somewhere correct* — they had been measured mid-operation, during a window when a transient
condition held, and the condition then changed. A count of broken links read 24, then 18, then 0
inside one day, because a background repair was mid-flight. Quoting the 16 that a note had captured
was not a fabrication; it was a photograph of a moving object presented as a still. When a quantity
is known to move, report the *state and its trajectory* ("0 now; 24 this morning; expected during a
merge, repaired same day"), never a single frozen sample.

**The third trap: a proxy number silently substitutes for the thing it proxies.** "Number of skills"
has at least two defensible answers here — distinct bodies, and distinct addresses — differing by
about 15%. They answer different questions. Quoting one without naming which question it answers
means the reader supplies their own definition, and any later audit appears to contradict you.
Name the definition in the same breath as the number.

**Consequence for review.** When auditing a document of this kind, do not sample the numbers — take
all of them, and sort them into *measured today*, *measured, moving*, *recalled*, *proxied*, and
*cannot be verified*. The last bucket is the finding. A document that is intellectually right and
numerically unpinned is the most dangerous kind, because its correctness up top buys credit for the
figures below.

---

## Procedure

1. **Classify each claim before writing it.** Two classes, handled differently:
   - **Quotable fact** — a figure stated in a primary document. Cite it, and quote the source's own wording where the wording carries the meaning.
   - **Derived figure** — anything computed (delta, annualised rate, product, ratio, comparison). These are what get destroyed under audit. Allow them only when every input is itself quotable, and label what you did.
2. **Locate the primary.** Company filing or annual report, regulator database, official statistical release, the system's own logs. A news article, broker note, or colleague's slide is a **summariser**, never a source of record.
3. **Match the metric name, not just the value.** Same number under a different label is a wrong number.
4. **Check whether the source publishes the metric on more than one basis.** If it does, both are usually legitimate — quote both with their labels.
5. **Label every assumption at the point of use.** "Assuming an average cost of X" is a variable the reader may change; a bare X is a defect they will expose.
6. **Lead with observations that rest on no numbers.** Structural and definitional findings survive every audit; a figure-dependent finding survives only until the figure is corrected.
7. **Treat the artifact as versioned.** On any correction, publish a new version and a short table of what changed and why.

---

## Metric identity

Between the primary and your reply there is usually a summariser. Summarisers are lossy in three
specific ways, and each loss is invisible unless you go back to the primary:

| Loss | Signature | Recovery |
|---|---|---|
| **Metric collapse** | One word — commonly "cash" — standing for a balance, a net position and a flow at once | Pull the primary, match the *label* |
| **Series collapse** | Two published series for one period presented as one | Read the source table row by row |
| **Wording collapse** | An accounting event reported as an operating outcome | Quote the primary's sentence verbatim |

**Rule:** before any consequential number leaves your hands, ask *which document does this come
from, and does that document use the same metric name I am about to use?* If the honest answer is
a summariser, either go to the primary or label it secondary **inside the artifact**.

A number correct to four significant figures under the wrong metric name is a wrong number, and
it will be caught precisely because it looks precise.

---

## Stock versus flow

A change in a balance is the difference between two stocks. Converting it into "per month" or
"per year" silently asserts a flow that was never measured.

Before attributing a decline in a balance to operations:
- read the **flow statement** for the actual operating figure;
- check whether the **other side of the balance sheet moved** — new borrowing, translation effects,
  declared distributions and lease additions all produce the same balance-sheet signature as
  genuine cash consumption.

A balance-sheet delta presented as a burn rate is one of the easiest errors to falsify, because
the correcting document sits in the same filing.

---

## Scenarios versus measurements

**Any product containing an assumed factor is a scenario, not a measurement.**

If one input is assumed — a typical unit cost, an average headcount, a blended rate — the result
may appear only as a labelled scenario. It may not be compared against a measured figure as
though both were measurements, because the comparison then carries precision it never earned.

When the temptation arises to make an argument land harder by multiplying two plausible numbers:
make the argument from fewer, harder numbers instead. A comparison built on four quotable facts
survives a hostile reader; one built on an assumed unit cost does not, and its failure takes the
argument with it.

---

## Attribution

An attributed claim requires a **nameable artefact**: author, title, date — something the reader
can open.

- "Analysts say", "sources indicate", "it is understood" cannot be checked.
- When a reader tries and finds nothing, the cost is not the sentence. It is the whole document's
  standing, because you have shown that at least one claim was never anchored.
- If you cannot name it, cut it. Losing one sentence is cheaper than losing the argument.

Distinguish this from *aggregate* attribution ("the industry expects") — a different defect: an
unnamed sample presented as a consensus.

---

## Dual series

When a source publishes the same metric on two bases for the same period — different definitions,
different scopes, different measurement points — both are usually valid.

- Quote both with their labels. **Declaring one wrong is itself an error.**
- Where two series are laid out as adjacent rows or columns, transposing them is the most findable
  mistake a reader can catch, because the correcting table is on the page they are already
  looking at. Verify two-series tables **column-to-column, not row-to-row**.
- State which series you are using and why, once, then be consistent.

---

## Hedging asymmetry

Over-hedging is the same defect class as over-claiming, pointed the other way.

- An "unverified" list is for claims whose **source is unreachable** — not for claims you
  personally did not open.
- Demoting a figure the primary document actually states weakens a case that would have held, and
  it teaches the reader to distrust your confidence signal generally.
- Conversely, a claim carried as verified because a summariser stated it is an asserted unverified
  claim. Both directions cost the same credibility.

---

## Receiving an audit of your own artifact

When a reader returns line-by-line corrections against the primary:

1. **Go to the primary yourself before responding.** Do not concede or defend from memory —
   agreeing quickly is as unreliable as refusing.
2. **Classify each correction.** Metric confusion, series transposition, and accounting-versus-
   operating misreads need different fixes. Say which class each one is.
3. **Retract in the open, quoting the source's own wording.** A retraction that quotes the primary
   is evidence the claims were removable — which is what makes the surviving claims trustworthy.
4. **Recompute from the corrected input; do not merely delete the line.** Deleting leaves the
   conclusion the wrong number induced still standing.
5. **Re-examine everything built on the corrected number.** A derived figure usually supports a
   larger argument; fixing the figure without checking the argument is half a correction.
6. **Version the artifact** with a short table of what changed and why. Never silently patch — a
   reader holding the old number cannot tell which document they have.
7. **Report what remains unverified, and remove what cannot be sourced at all.** Some corrections
   resolve in your favour; say so plainly rather than over-conceding.
8. **Record the failure mode** where the next session will load it, so the same class of error is
   not re-learned.

---

## A number spoken about a present person

The hardest audit surface is not a document. It is a live conversation where the subject of your
number is also reading it.

A figure about someone's own work — how many they sold, how long they slept, what time they left —
is checked instantly by the one person who counted it, and they will rarely tell you they noticed.
Unlike a document there is no version bump available: no change table, no previous-value column,
only a sentence already in the room.

- **If the source is not in hand, the sentence is not available.** Not hedged, not rounded, not
  "roughly" — unavailable. An approximate figure about a real event is still a fabricated figure.
- **Check who the question was addressed to.** A question the principal aimed at someone else is a
  signal you are about to speak without a source; answering it for them, then instructing them to
  answer, is the same defect twice.
- **Never invent the cause, either.** A number replaced by a mechanism — "he slept late because…" —
  is the same fabrication wearing prose.
- **Keep one epistemic posture across rooms.** Marking something UNKNOWN in a private thread and
  stating it as fact in a group is not two audiences; it is one false claim.
- **Retract in the same room, in the same shape.** One plain line owning the figure, then the
  correction built from the record — not a tightened estimate.
- **Before claiming a figure came from the record, sweep it.** Logs, prior messages, data files,
  and the skill's own pointers (a referenced data file may not exist at all). If the sweep is
  empty, the figure was yours.

---

## Pitfalls

- **Never take a number from a news article when the primary exists.** Summarisers collapse related-but-distinct metrics under one word; the value survives and the meaning does not.
- **Never annualise a balance-sheet delta and call it a burn rate.** Check the other balance-sheet side and the flow statement first.
- **Never present a product of an assumed factor as a measurement.** Label it a scenario or drop it.
- **Never attribute a claim to unnamed third parties.** Name the artefact or cut the sentence.
- **Never declare one of two published series wrong.** Quote both with labels; verify two-series tables column-to-column.
- **Never read a recognition as an operating result.** Accumulated-loss recognition triggered by a capital injection is a balance-sheet event; read the exact wording before calling it a period loss.
- **Never silently revise a published artifact.** Version it, and show what changed.
- **Never state a count about a real person's own work in front of that person without the source.** They are the auditor, and the utterance cannot be versioned.
- **Never present an unsourced figure as background colour.** Detail that feels like context is still a claim; add it only from the record.
- **Never let a headline figure be one you cannot quote.** If it must be derived, say what it is derived from, in the artifact.
- **Never derive a figure by scraping digits out of prose.** An automated reader that takes the
  largest number found in a page and compares it to a threshold will happily score a **year** as a
  **currency amount**. Measured: a verifier extracting "the reported value" from a search snippet
  returned `~2026.0` against a claim of `>= 30,000,000,000`, then recorded a decisive *incorrect*
  verdict against a real prediction — a fabricated number manufactured by the checker itself, and
  the precise failure the check existed to prevent. A magnitude comparison needs a **unit-aware
  extractor over a named data source** (a filing, a statistical release, a field in a database).
  Absent that, **decline and leave the claim open**. No verdict is cheaper than a false verdict:
  a false one silently corrupts the ledger every later decision is calibrated against.
- **Never let a keyword stand in for a magnitude.** "Announced", "effective" or "implemented" in
  a snippet say an event happened, not what it was worth. If the claim carries a threshold, only a
  comparable value decides it.
- **Bind the snippet to the claim before it may vote.** Require distinctive tokens from the claim
  itself to appear in the source text; otherwise a generic page about the same country or company
  casts a verdict on a specific claim it never addressed.
- **Don't skip the full document for a summary of it.** The summary carries the framing; the full document carries the footnotes where the real figure lives.

---

## Output shape that survives audit

- Lead with defined terms and structural observations — the parts no number can falsify.
- Present quotable facts in a table with a source column naming the document and period.
- Keep derived figures in a separate block labelled as derived.
- Carry a short "what remains unverified" section; it is a strength, not an admission.
- On revision, carry a change table: previous value, new value, reason.
- Include a falsification test: the specific observations that would show your reading wrong. A
  reading that cannot be wrong is a belief, and readers treat it as one.
