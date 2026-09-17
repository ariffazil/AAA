---
name: institutional-leadership-lineage
description: "Use when profiling every holder of an office or seat. Reconstruct a whole succession — seat architecture, tenure, appointment basis — then assess each holder's fitness, in one delivered multi-holder archive."
version: 2.0.0
triggers:
  - "every CEO and chairman ever"
  - "senarai pengerusi"
  - "profile all the leaders of X"
  - "who were all the chairmen / CEOs / presidents of X"
  - "profile every leader of X and whether they deserved it"
  - "what did each one bring, what did they get"
  - "who led this thing from the beginning"
  - "reconstruct the succession"
  - "layak or not"
floors: [F2, F6, F7, F11]
---

# Institutional Leadership Lineage

Class-level workflow for "profile every CEO / chairman / minister / officeholder this institution
ever had" requests: succession, tenure, appointment basis, what each one brought and got, and
whether the record justifies the post.

> **Merged 2026-09-17.** This was written twice — as `institutional-leadership-lineage` and as
> `leadership-roster-archive` — four minutes apart in one session, with overlapping trigger wording
> and zero usage each. Two skills sharing one trigger class means the router cannot choose, so
> selection becomes a coin flip; selection precision is safety. Consolidated here. Any pointer to
> the old roster name resolves here, and the PDF builder it carried is now `templates/`.

## The ask

The request is **not one named person** — it is the whole line of them:

- "every CEO and chairman ever", "senarai pengerusi", "profile all the leaders of X"
- "who led this thing from the beginning", "reconstruct the succession"
- "why did each of them deserve the seat / not deserve it — what did they bring, what did they get"

Deliverable = **one multi-person archive** (a page-section per holder) plus roster table, pattern
section and sources. Not N free-standing dossiers, and not a bare chronology — the requester asked
why each one was qualified, so an evaluation is the deliverable.

## NOT for

- A single named person, shareable with the subject → `person-intelligence-dossier`
- One institution's crisis or decay history → `institutional-forensic-analysis`
- News/topic synthesis → `executive-intelligence-briefing`

## The two laws

**Law 1 — An office is not a person.** Most institutions have more than one leadership seat
(chair vs chief executive vs president vs secretary-general). They carry different powers, different
appointment mechanisms, different accountability. The commonest error in these dossiers is
attributing the institution's delivery to whichever name the requester happened to use. Establish
which seat the person held **in the year in question** before crediting or blaming them for anything.

**Law 2 — A gap in the list is evidence.** When a source-verified succession has a hole, the hole is
usually one of: the office was **vacant**, an **acting** holder sat in it and never appears under
the title, or the office was **merged** into another. Searching the missing title in those years
returns nothing — which is why the hole reads as ignorance. Test for vacancy / acting / merger
before writing a name as UNKNOWN. A documented interregnum is frequently the most consequential
finding in the entire dossier.

## The procedure

### Step 1 — Map the seat architecture BEFORE profiling anyone (non-negotiable)

Establish and write down:

1. **Was the office ever combined?** Many institutions start with one person holding both the
   non-executive and executive title, then split them. Get the split date.
2. **Which holders were *acting*?** An acting occupancy is a governance finding, not a footnote.
3. **Who appoints the seat, and in what political moment?** Head of government, board, ministry
   nominee, election of members? "Why was X appointed" is unanswerable without this.
4. **Do any roles overlap or run concurrently?** Concurrent seats are common in GLCs and are a
   frequent source of wrong career timelines.

> **A roster built without this model invents phantom holders and phantom gaps.** The tell is a
> claim like "there was no chairman from 2004 to 2012" — usually true only as "no **non-acting**
> chairman". State which one you mean.

### Step 2 — Find the one paragraph that lists the whole succession

Business-press retrospective columns routinely print the complete succession in a sentence or two.
Locating that single column beats mining twenty news articles, and gives you the master list to
verify person-by-person. Search for the retrospective/anniversary column, not the news.

### Step 3 — Fix the spine by hand, and mark source status per row

Build two tables before dispatching any research — one per office, one row per holder:
`name | tenure start | tenure end | appointment basis | source status`. Use the institution's own
releases and leadership pages, official appointment announcements carried by wire services, and
reputable press. Only when the spine is stable do you fan out. A corrupted spine propagates into
every profile built on it.

- **VERIFIED** = two independent sources agree.
- **VERIFY** = single source, or boundaries inferred.
- **UNKNOWN** = no source at all, or no source yet found.

Never promote a flag by inference, and never let a downstream profile silently treat a VERIFY row
as settled. Never interpolate a date to make a table look complete.

### Step 4 — Fan out per-person research to subagents

Batches of ~4, one dispatch per batch. Per-person isolation is what stops the profiles inheriting
each other's errors — never one giant "research X's whole history" call.

Two rules make the returns usable:

- **Repeat the same hard-rules block verbatim in every child's `context`.** Children do not share
  the parent's context, and one child without the sourcing rule contaminates the whole archive. The
  mandatory citation clause: *every factual claim must be followed by its source URL; if a fact
  cannot be sourced write UNKNOWN; never fill a gap with plausible detail; mark OBSERVED vs
  INFERRED.* Without it you receive fluent, confident biography with invented schooling, invented
  early career, invented honours.
- **Give every child the identical fixed output section list**, so dossiers concatenate without
  reformatting. Template in `references/office-holder-roster.md`.

**Run the money lane as a separate task.** Disclosed pay, dividends, budgets, era-by-era published
results. Kept separate, fake precision cannot leak into the narrative profiles.

**Reconcile, then write.** Where two children disagree, the disagreement is a finding: state both
and the reconciliation. Do not average them.

### Step 5 — Assess fitness for the seat (when asked)

When the user asks "layak or not" / "did they deserve it", every holder gets, in this order:

- **what they brought** — quantified outcomes, sourced
- **what they got** — honours, post-tenure roles
- **basis of appointment** — merit / political proximity / necessity, each labelled
- an explicit **verdict on a stated scale**
- **steelman counter-points**

Wording and schema in `references/office-holder-roster.md`. A verdict without a scale and
counter-points is an opinion.

### Step 6 — Build the archive PDF

Cover → one page-section per holder (seat-type band/pill on each) → closing **roster table** →
**patterns** section → **sources & provenance** including the open questions.

Use `templates/roster_pdf_builder.py` — markdown → weasyprint, dark theme, page-per-person, SHA256
receipt printed at the end. It is a starter: edit `manifest.json`, not the script.

### Step 7 — Deliver

Send the PDF with `MEDIA:` plus a short chat summary that leads with the **structural finding**
(the seat's architecture, or the pattern in how it changes hands), not with a name list.

## Scoring: merit vs structure

Separate what the person **did** from how they **got there**. Two columns:

- **Structure (not merit):** who appointed them, which seat, whose patronage, whether the
  appointment runs on a fixed contractual cycle, whether the office was ever executive. Report as
  mechanism.
- **Merit (checkable):** projects actually completed inside their window, published operational and
  financial outcomes, capital discipline, succession quality (did they leave a competent bench), and
  the state of the institution at handover versus at entry.

Anchor every claimed outcome to its recorded start/finish date, not to the holder's tenure —
long-serving chiefs accumulate credit for work begun before them and landed after them, and
short-serving chiefs absorb blame for inherited failure. Where the only available verdict is the
requester's own framing, say whose framing it is.

## Always-on rules

1. **Dignity (F6).** Analyse decisions and outcomes. Never insult a holder, never speculate about
   private life, family, health or motive. Political/professional context is fair game; the person
   beyond the record is not.
2. **Institutional critique ≠ personal defamation.** A verdict on fitness for a seat is a judgement
   on the appointment and its outcomes, and it must be phrased that way.
3. **Every claim carries a source URL.** No source, no claim — write UNK.
4. **Open questions get their own section.** They are part of the deliverable and the honest
   receipt, not an internal note. Carry unresolved items forward explicitly; never smooth them.
5. **Verify current office-holders live before asserting them.** Never cite a cached name list as
   present-tense fact.
6. **Insider bias disclosure.** When the requester works inside the institution being audited, say so
   in the archive's framing. The dossier will be read against lived experience, so keep every number
   sourced and every gap explicit — the one thing an insider catches is a confident wrong detail.
7. **A distinguished title is not evidence of performance**, and the absence of titles is not
   evidence of failure. Report honours as facts with dates.
8. **Distinguish institutional history from current politics.** Appointment timing relative to a
   change of government is an observation about mechanism; a claim about what the appointee owes
   anyone is an inference — label it.

## Pitfalls

1. **Old office-holders are not on English Wikipedia.** For pre-internet public figures of a
   Commonwealth civil-service state, the yield order is: **vernacular Wikipedia** (far richer than
   the English page for civil servants — carries office dates, birth/death, honours) → the national
   news-archive library of scanned newspapers → university-hosted academic PDFs → the language
   authority's biographical database → national honours gazettes → the figure's published biography.
   Search the **vernacular name**, not the English transliteration. Ladder in the reference file.
2. **Two people can hold the same title in the same decade.** Combined seats, brief chairmanships
   and concurrent roles make naive "one holder per period" tables wrong. When sources disagree,
   present the competing readings rather than forcing a clean succession.
3. **Founders and early executive directors are often not on the official roster page.** If a source
   names someone by a short form (a single name, a nickname, a title), record that as the identifier
   and mark the full name OPEN. Do not silently drop a senior figure because they are hard to find —
   an unexplained absence in the roster is itself a defect.
4. **A partial-name holder must be flagged, not guessed at.** Cross-reference initials, role and
   employer before accepting any full-name expansion.
5. **Don't let the verdict section swallow the evidence.** Brought / got / basis / verdict, in that
   order, each sourced. Verdict last and short.
6. **Consistent per-person schema across every holder.** If holder 3 has "what they got" and holder 7
   does not, the archive reads as uneven treatment — which reads as bias.

## Lane notes

- Prefer per-section PDFs of an annual/integrated report (governance, board, remuneration sections)
  over whole-document extraction; full-length reports return stream noise that reads like content.
- Separate *finding the source* from *getting the number*: a search query that bundles currency
  figures can trip a money-guard and return a HOLD. Search the topic plainly, then extract the
  primary page.
- Encyclopedia entries are usable for dates and offices, weak for characterisation; treat any
  single-source personal detail as VERIFY.
- Older documents are scans: a figure read out of one is not MEASURED until a second source agrees.

## Support files

- `references/office-holder-roster.md` — seat-architecture checklist, source ladder for pre-internet
  public figures, the fitness-for-seat schema, the subagent hard-rules block, and a worked example.
- `references/petronas-leadership-lineage.md` — PETRONAS chairman and President/CEO succession 1974
  to present, including a documented eleven-year acting-chairman period, plus the fan-out contract as
  applied.
- `templates/roster_pdf_builder.py` — markdown → weasyprint archive builder (manifest-driven, dark
  theme, page-per-person, SHA256 receipt).

## Companions

- `person-intelligence-dossier` — the single-person variant; this skill is the multi-holder variant
- `institutional-forensic-analysis` — institution-level forensics; this skill is leadership-level
- `executive-intelligence-briefing` — topic/news briefings; this skill is office-holder archives
