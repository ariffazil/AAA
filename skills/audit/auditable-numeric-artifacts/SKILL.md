---
name: auditable-numeric-artifacts
description: "Use when issuing checkable numbers. Source every figure."
version: 1.1.0
risk_tier: low
floor_scope: [F2, F9]
autonomy_tier: T0
tags: [epistemic, numbers, primary-source, verification, artifacts]
capability_tier: fed-long-context
ecology_state: WARM
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

## Operating prompt

For the always-on snippet (four provenance classes, state-transition chain, four HOLD
triggers, the "who pays if wrong" test), load
`references/numerical-claim-discipline.md`. It is the portable contract every artifact
producing session should run against.

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
- **A receipt outranks every derived split.** When a total is in dispute and someone can photograph the
  payment record, the record settles it — stop reconciling your own breakdown against it. Ask for the
  receipt before sweeping stores for a figure a person already holds.
- **A split of a recorded total is your arithmetic, not the record's.** A stored total that someone
  once called "enough" carries no component breakdown; any cost-versus-labour or item-versus-service
  division you publish borrows the total's authority without earning it. Label it derived, and when the
  real components arrive, retract the split rather than re-fitting it to match.
- **Never merge two orders into one ledger to derive a balance.** A prior settled payment and a
  new unpaid request are two separate contracts, not one subtractable equation. The arithmetic
  `prior_paid + new_unpaid = grand_total` produces a "balance due" that exists only on paper —
  the recipient of the prior payment has already received it, and the new request has not yet
  been agreed upon, let alone offset against the first. One invoice = one order. If a prior
  transaction belongs on the document at all, it belongs in a separate EXCLUDED block with a
  status label (SETTLED, VOID, REFUNDED), not in the arithmetic that determines what is owed.
  A crafted "balance due" between two parties who never agreed to that offset is the
  manufactured-debt defect — the most expensive failure shape in this skill, because the
  recipient will read it as a claim.
- **Lock the record to the source that produced it, not to whoever spoke last.** Two parties
  describe the same transaction differently; the temptation is to revise the record every time
  one or the other adds detail. Hold the record on its original source until that source is
  contradicted by a higher-warrant observation (a receipt, a logged event, a confirmed reply).
  When in doubt, surface the disagreement inside the artifact ("Arif states A; Syed states B")
  and stop. Re-rendering the document every five minutes to fit the latest speaker is the same
  defect as a stale figure presented as current — the layout looks fresh while the underlying
  record is still unverified.
- **Never override a prior record because of a same-warrant update.** A new chat message from the
  same speaker is not a higher-warrant observation; it is a same-warrant update that may simply
  contradict the prior one. Re-rendering the artifact on every new message gives the document
  the appearance of currency while the underlying source has not changed. Hold the prior record
  on the source; surface both states inside the artifact; wait for a real contradicting signal
  (a fresh receipt, a logged event) before revision. "Editing my own record to match whoever
  spoke last" reads as capitulation, not learning — and in a shared room it is publicly visible.
- **Sequence is the gate for any artifact that names a real person.** If a document names a
  human as payee, vendor, recipient, or author, that document is a **claim against them** —
  regardless of whether the math is internally consistent. Showing it first to a third party
  (the buyer, a group chat, a public channel) puts the named person in the position of correcting
  a document that has already been seen. Correction then becomes expensive even when they are
  the only authority who could have signed off. The order is fixed: **build → show payee/namee →
  show counterparty → deliver.** Inverting it converts the artifact from a record into a trap.
  This applies even when the user explicitly asks for a fast invoice or a quick PDF: speed of
  delivery is not authority to bypass the named-person review step.
- **The manufactured-debt defect is a manufactured claim, not a math error.** A "balance due"
  produced by `prior_paid + new_unpaid = grand_total` between two parties who never agreed to
  that offset is not a derivation that happens to be wrong — it is a claim of fact that no
  party in the conversation authored. The recipient of the prior payment has already received
  it. The new request has not been agreed upon. The arithmetic itself is internally consistent;
  the defect is that the **document presents a settlement position the parties never took**.
  Always: (a) one invoice = one order, (b) prior transactions belong in a separately-labelled
  block with a status tag (`SETTLED`, `VOID`, `REFUNDED`), never in the arithmetic that
  determines what is owed, (c) the "balance due" line is a human-asserted figure — if no
  human has stated it, the line does not exist. A grand total between two parties who never
  agreed to that grand total is the most expensive failure shape in this skill, because the
  recipient will read it as a binding statement and the issuer has not earned that standing.
- **Re-rendering to match the latest speaker is capitulation, not learning.** When two parties
  in the room describe the same transaction differently, the temptation is to revise the
  document every time one or the other adds detail. Hold the record on its original source
  (the receipt, the logged event) until a higher-warrant observation contradicts it. Surface
  the disagreement inside the artifact (`"Arif states A; payee states B"`) and stop. A document
  whose layout changes every few minutes to fit the latest voice is the same defect as a stale
  figure presented as current — the appearance of currency masks an unverified underlying state.
  Visible in shared rooms, where the recipient can watch their own position being rewritten.
- **Check who a stored figure was attributed to before quoting it back at them.** Records mis-assign
  spending between people. The person who received or paid the money is the one who can correct the
  attribution, so surface the label you found ("my note files this under X") instead of asserting whose
  money it was.
- **Name the payee explicitly in the artifact, and route it past them before any other reader.**
  If a document names a person as payee, vendor, or recipient, that document is a claim against
  them. Showing it first to a third party (the buyer, a group chat, a public channel) puts the
  payee in the position of correcting a document that has already been seen — which makes
  correction expensive even when the payee is the only authority who could have signed off.
  Sequence is the gate: build → show payee → show payer → deliver. Inverting this order converts
  the artifact from a record into a trap.
- **Carry the empty cell with a `tidak dinyatakan` tag, not with prose absence.** A blank row is
  read as "the author ran out of time". A row with the value `tidak dinyatakan` (or `not stated`,
  matched to the document's language) is read as "the author has no source". Empty with a label
  is honest silence; empty without a label is a silent fabrication of omission. The label is
  cheap to print and the difference is paid in trust.

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
- **Never correct another party's count before running their query.** The same repo, corpus or table answers several counts, and they differ legitimately: total history depth versus commits ahead of a base branch, distinct bodies versus distinct addresses, files versus symlinks. Two parties can each be right on a different axis, and a "correction" issued from the wrong one is the most expensive error in this skill — it retracts a figure that was correct, and it spends the credibility of the correction itself. Ask for, or reproduce, the exact command/definition behind their number, state it beside yours, and only then say which of the two answers your question. If you have already issued such a correction, retract it in the same plain shape as any other: own the figure, name the axis you measured, leave their number standing.
 - **A count restated in prose is a NEW object — re-read it against the set you computed.** A computed
 figure of 34 was written into a sentence as "forty" and caught only on a final pass. The command
 printed the right number; the transcription into words introduced a second one, and prose has no
 `sort -u` to catch it. Before send, re-read every numeral in the draft against the output that
 produced it. Prefer the digit to the word: a digit is one glyph to diff, while a word is a second
 encoding of the same value carrying its own error surface.
- **Never attach a reading to a number that the source did not give you.** A value is one claim; the
  word attached to it — `overbought`, `stabil`, `tahan`, `resilient` — is a second, derived claim,
  threshold-dependent and falsifiable. Carry both when the source supplies both, and print the number
  bare when it does not. An invented reading is worse than a bare figure, because the figure is at
  least checkable while the reading borrows its credibility.
- **A figure that is one of several equally valid senses is a figure you have not yet defined.** Two
  parties can each quote the correct number and disagree because they measured different axes. Name the
  axis beside the number, and when adopting someone else's figure, reproduce their definition before
  comparing it to yours.
- **A third-party score is a derived figure with no stated denominator — recompute it before relaying
  it.** Consumer apps publish a verdict ("needs improvement") beside a target that may be arithmetically
  unreachable for the very record it judged: an absolute-hours target that, added to the other measured
  components, exceeds the total available. Test the target against the record's own totals before
  quoting the verdict; pure arithmetic is enough and needs no reference range. Two corollaries: a fixed
  absolute target means a different percentage on every record, so convert before comparing to any band;
  and when the instrument's own error band exceeds the size of the deviation you want to call abnormal,
  the deviation is noise — say the measurement cannot resolve it instead of naming a cause.

 ---

 ## Output shape that survives audit

- Lead with defined terms and structural observations — the parts no number can falsify.
- Present quotable facts in a table with a source column naming the document and period.
- Keep derived figures in a separate block labelled as derived.
- Carry a short "what remains unverified" section; it is a strength, not an admission.
- On revision, carry a change table: previous value, new value, reason.
- Include a falsification test: the specific observations that would show your reading wrong. A
  reading that cannot be wrong is a belief, and readers treat it as one.
- **Open with the ONE figure that makes the others legible**, carrying its date and source in the same
  breath. A reader who gets one number first can place every number after it. If no single figure earns
  that place, skip it — promoting an arbitrary figure to the headline is its own defect, and a headline
  figure is the one most likely to be quoted onward without its qualifiers.
- **On a short surface, compress the trail — never drop it.** For a message or a one-screen brief the
  source trail becomes outlets and dates, comma-separated, no URLs and no prose. The "what remains
  unverified" section is the last thing to be cut under compression, not the first: it is what licenses
  the rest of the document.
- **Never restate a figure the artifact already carries.** A number printed twice has two chances to
  disagree with itself, and the two printings drift apart the moment either is revised. Cross-reference
  it instead ("the countdown above", "the second row") — repetition is not emphasis when the value is
  already on the page.
