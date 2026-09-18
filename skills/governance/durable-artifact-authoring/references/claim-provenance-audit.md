# Claim Provenance Audit — Trace the Figure, Don't Re-derive It

Use when a number is disputed, surprising, or contradicts an earlier pass. Re-deriving produces a
second opinion; tracing produces the origin. Only the origin settles it.

## Procedure

### 1. Resolve every citation to an instance
For each source named beside the claim, open it and search for the digits.

| Source named | Opened where | Contains the digits? | Verdict |
|---|---|---|---|

- Class-level citations ("H1 report", "UOB note", "analysts say") are unresolvable — escalate them
  to UNSUPPORTED rather than treating them as weak support.
- A citation that does not contain the number is not a citation.
- **A citation list is not a search plan.** The named sources are the ones you were handed, not the
  ones most likely to hold the figure. After resolving them, ask which party is *obliged* to publish
  it and search there — step 1b.

### 1b. Widen to the party that must disclose

When the claim touches an asset, contract, or branch involving a **foreign listed** counterparty,
that counterparty's mandatory filings (SEC EDGAR for US-listed issuers) are primary record and are
often the *only* dated record of the event. The host country's filings may not exist yet; the
counterparty files on its own calendar.

```bash
UA="<Org>-Research <contact@example.com>"     # required; a browser UA is refused as undeclared
curl -s -A "$UA" "https://efts.sec.gov/LATEST/search-index?q=<term>&forms=10-K&ciks=<CIK>"
curl -s -A "$UA" --compressed "<filing .htm URL>" -o filing.htm
grep -o -i "<term>" filing.htm | wc -l        # count raw HTML, then read the context
```

Two findings this yields that host-country sources cannot:

- **A dated exit.** A country's mention count falling to zero between successive annual reports,
  while the subsidiary exhibit (EX-21) still lists the local entity, distinguishes *operations
  exited, entity retained* from a genuine withdrawal. Always carry a **control term** whose count
  must not move, so the zero cannot be a parse artefact.
- **An equity baseline.** Entity-level working interests published years earlier are often the only
  available basis for testing a transfer arithmetic, when nothing current discloses the split.

### 1c. Confirm the document postdates the event

A report whose as-at date precedes the transaction **cannot** contain the resulting figure.
Establish the event date and the report's as-at date before searching. If the report predates the
event, confirming absence is a category error, not a finding — name the edition that will carry it
(next quarterly, next annual) and stop. Never report a confident negative from a document that could
not have known.

### 1d. Check the claim's TIME DIRECTION before opening anything

Date logic cuts both ways, and the second way saves the whole audit.

- A **backward-looking** claim — what happened, what was paid, what was produced — can legitimately
  cite a past report. A citation that lacks the figure is an error to be resolved by opening it.
- A **forward-looking** claim — a future entitlement, a pending handover, a rate not yet effective,
  anything whose realisation postdates the latest published report — **cannot** carry a past-report
  citation by construction. No annual report, interim or quarterly can contain a quantity that has
  not yet occurred.

So when a forward-looking figure carries a citation to a past document, the citation is refuted
**without opening it**. Apply the test in this order, because it is cheapest in this order:

1. Ask what the claim *refers to*, and whether that thing has happened yet.
2. If it has not: stop. Report `CITATION IMPOSSIBLE BY CONSTRUCTION` and ask for the internal
   document, the signatory, or the dated instrument that will eventually carry it.
3. If it has: proceed to open every named source (step 1).

The finding is about the **citation, never about the truth of the number.** A forward-looking figure
may be perfectly accurate from internal knowledge, a meeting, or a signed-but-unpublished agreement
— none of which will ever surface in a public record, so the absence of a possible public source is
*expected* rather than suspicious. What is defective is the borrowed authority: an invented citation
converts a checkable claim into an uncheckable one, and it is the more damaging defect precisely when
the number underneath is true, because the figure then travels unexamined on the strength of a source
that never said it.

### 2. Read the attribution field — as a channel, not an author

Claims accumulate in memory, ledgers, and canon. Each record usually carries who placed it.

```bash
# Search the memory export, not only the file that quotes the claim
grep -n "<digits>" /root/AAA/reports/*mem0-export*.jsonl
```

Read `"attributed_to"` — but it names **who last spoke the figure in that channel**, not who
originated it. An agent restating the principal's earlier words is filed as `assistant`. So
`assistant` **cannot** by itself distinguish an invented number from repeated human testimony, and
reading it as an invention has produced a fabrication charge against a figure that was accurate
first-party testimony.

Before concluding self-generation, walk the thread backwards and look for the human:

```bash
# the origin is often the principal, minutes before the agent echoed it
session_search(query="<digits>", sort="oldest")
```

Escalate to a fabrication finding only when **no** human utterance and no internal document
precedes the agent's first use. Where a human principal originated it, the verdict is
`UNVERIFIED — first-party testimony`, and the canon entry is corrected for its **citation**, not
retracted for its content. A fabrication charge resting on a restatement record is itself a
fabrication — and the more damaging one, because it discredits the audit along with the figure.

### 3. Check the unit against the reporting convention
Confirm how the source denominates the metric before accepting or deriving it.
- Rate vs volume is the common collision: `’000 boe/day` (rate) vs `billion boe` / `MMboe` (volume).
- A metric a source publishes only as a rate, restated in a volume unit, was not read from that source.
- State the convention explicitly in the reply so the user can check it themselves.

### 4. Enumerate digit collisions
A short digit string can occupy several unrelated roles inside one transaction cluster. List every
distinct quantity sharing the leading digits, each with its own unit and source. If two roles sit
adjacent, resist reconciling them by subtraction — digit coincidence is not evidence of a
relationship. Real example shape: an initial production RATE, a target RATE on an entitlement basis,
another company's reserve VOLUME, and the group's own entitlement RATE were all quoted as "300".

### 5. Separate what is disclosed from what is not
- **Disclosed:** totals, asset counts, targets, financing, structure.
- **Not disclosed:** asset-level names, reserves, production splits.

Where a party discloses price and total but withholds the split, write `NOT DISCLOSED` and stop. Do
not fill it by subtraction; name the gap as a finding.

### 5b. Qualify the surface before you quote from it

Decide whether a source is usable **before** extracting a figure. Treat these as disqualifying:

- **The source disclaims its own numbers.** A caption that reads like data but is labelled
  *illustrative / placeholder / awaiting feed* is not data. Flagging such a figure and printing it
  anyway is not caution — the caveat is dropped the moment the sentence is reused, and the number
  travels on its own. If a figure cannot be used, do not quote it at all.
- **The host is not the entity it imitates.** A staging, preview or mirror host carrying a near-miss
  legal name for the company is unusable even when the layout looks official. Verify the registered
  name against the entity's own letterhead before extracting anything.
- **The same surface contradicts itself.** Two pages of one site giving different values for the
  same metric means at least one is wrong and neither is citable. Compare before quoting.

When a figure you already relayed turns out to come from such a surface, **retract it explicitly**.
A silent drop leaves the reader still holding the number from the previous message.

### 5c. Harvest instance-level names from the party's own surface

When a party withholds asset-level detail, the naming you need usually exists on its *own* published
material — image captions, map labels, press releases. That is legitimate instance-level attribution
because the party published it, and it is stronger than an analyst's paraphrase. Cite it as *their*
disclosure and say which surface it came from, so the reader can check it.

### 5d. Separate ownership from operatorship

One transaction can move two different things at two different layers. Ownership is who holds the
interest; operatorship is who runs the asset. Counterparties routinely describe only their own layer
("the assets retain their current operating set-up") while the host country reports the operational
handover on its own date. Record both findings separately, each with its own source and date.
Collapsing them either overstates the exit or hides the capability transfer — and the operatorship
finding is usually the one that matters, because it moves **skill**, not just equity.

### 5e. Read the counterparty's own accounts for the value asymmetry

When a party contributes assets to a vehicle and books the investment **above the book value of what
it contributed**, that is its own disclosure that the assets changed hands below worth. It appears in
the acquirer's statements and nowhere in the seller's records. Quote it as the acquirer's disclosure
and treat it as the strongest available evidence of transfer value when no price is published.

### 6. Mark any arithmetic coincidence
If a derived figure lands near a real disclosed figure, label it coincidence. Never present agreement
between two unrelated transactions as corroboration.

## Correction staging

When the audit retracts something already written to a location you do not own, follow the retraction
procedure in the parent SKILL.md. Summary: stage the correction to a path you own, quote the claim
verbatim, give `VERDICT: UNSUPPORTED — RETRACT` with the citation-resolution table, show the
provenance chain, supply the replacement at instance level, retain the surviving neighbouring claims,
and tell the user the correction is staged rather than landed.

## Output rules

- **Lead with the verdict, then the provenance chain.** The user asked whether the number is valid;
  answer that in the first line.
- **When the trail leads to your own or a peer agent's earlier utterance, say so plainly** and name
  the failure by its mechanism. A self-audit that stops short of naming the mechanism teaches nothing.
- **When the trail leads to the principal's own testimony, say so plainly too — and do not call it
  fabrication.** Internal knowledge, a meeting, a document only they hold: none of it will appear in
  a public record, so the absence is expected rather than suspicious. Report what would settle it and
  when (the filing, edition, or disclosure that will carry it).
- **Keep every verifiable figure tagged with document AND page/table.**
- **Do not re-derive what you cannot source.** Negating a bad figure with a fresh unsourced figure is
  the same defect one layer down.
