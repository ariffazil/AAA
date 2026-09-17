---
name: institutional-leadership-lineage
description: "Use when profiling every past leader of an institution."
---

# Institutional Leadership Lineage

> Class-level workflow for "profile every CEO / chairman / minister / officeholder
> this institution ever had" requests: succession, tenure, appointment basis,
> what each one brought and got, and whether the record justifies the post.

## Triggers

- "who were all the chairmen / CEOs / presidents of X"
- "profile every leader of X and whether they deserved it"
- "what did each one bring, what did they get"
- Any question spanning more than two successive officeholders of one institution

## The two laws

**Law 1 — An office is not a person.** Most institutions have more than one
leadership seat (chair vs chief executive vs president vs secretary-general).
They carry different powers, different appointment mechanisms, different
accountability. The most common error in these dossiers is attributing the
institution's delivery to whichever name the requester happened to use.
Establish which seat the person held **in the year in question** before
crediting or blaming them for anything.

**Law 2 — A gap in the list is evidence.** When a source-verified succession
list has a hole, the hole is usually one of: the office was **vacant**, an
**acting** holder sat in it and never appears under the title, or the office was
**merged** into another. Searching for the missing title in those years returns
nothing — which is why the hole reads as ignorance. Test for vacancy / acting /
merger before writing a name as UNKNOWN. A documented interregnum is frequently
the most consequential finding in the entire dossier.

## Procedure

1. **Fix the spine by hand before dispatching any research.** Build two tables —
   one per office, one row per holder: `name | tenure start | tenure end |
   appointment basis | source status`. Use the institution's own releases and
   leadership pages, official appointment announcements carried by wire
   services, and reputable press. Only when the spine is stable do you fan out.
   A corrupted spine propagates into every profile built on it.
2. **Mark source status per row.** VERIFIED = two independent sources agree.
   VERIFY = single source or inferred boundaries. UNKNOWN = no source. Never
   promote a flag by inference, and never let a downstream profile silently
   treat a VERIFY row as settled.
3. **Fan out one subagent per holder or per era-cluster** — never one giant
   "research X's whole history" call. Per-person isolation is what stops the
   profiles inheriting each other's errors.
4. **Every subagent task carries the mandatory citation clause verbatim:**
   *every factual claim must be followed by its source URL; if a fact cannot be
   sourced write UNKNOWN; never fill a gap with plausible detail; mark OBSERVED
   vs INFERRED.* Without this clause you receive fluent, confident biography
   with invented schooling, invented early career, invented honours.
5. **Run the money lane as a separate task.** Disclosed pay, dividends,
   budgets, era-by-era published results. Kept separate, fake precision cannot
   leak into the narrative profiles.
6. **Reconcile, then write.** Where two children disagree, the disagreement is
   a finding: state both and the reconciliation, do not average them.
7. **Deliver an evaluation, not a list.** The requester asked why each one was
   qualified; a bare chronology fails the ask.

## Scoring: merit vs structure

Separate what the person **did** from how they **got there**. Two columns:

- **Structure (not merit):** who appointed them, which seat, whose patronage,
  whether the appointment runs on a fixed contractual cycle, whether the office
  was ever executive. Report as mechanism.
- **Merit (checkable):** projects actually completed inside their window,
  published operational and financial outcomes, capital discipline, succession
  quality (did they leave a competent bench), and the state of the institution
  at handover versus at entry.

Anchor every claimed outcome to its recorded start/finish date, not to the
holder's tenure — long-serving chiefs accumulate credit for work begun before
them and landed after them, and short-serving chiefs absorb blame for inherited
failure. Where the only available verdict is the requester's own framing, say
whose framing it is.

## Guardrails

- **Critique the record and the mechanism, never a person's dignity.** No
  invented wealth, schooling, family, health, or motives. For a living or
  recently deceased holder an unsourced biographical detail is a defamation
  risk, not a colour note.
- **A distinguished title is not evidence of performance**, and the absence of
  titles is not evidence of failure. Report honours as facts with dates.
- **Distinguish institutional history from current politics.** Appointment
  timing relative to a change of government is an observation about mechanism;
  a claim about what the appointee owes anyone is an inference — label it.
- When the requester is himself an insider of the institution, the dossier will
  be read against lived experience: keep every number sourced and every gap
  explicit, because the one thing an insider catches is a confident wrong detail.

## Lane notes

- Prefer per-section PDFs of an annual/integrated report (governance, board,
  remuneration sections) over whole-document extraction; full-length reports
  return stream noise that reads like content.
- Separate *finding the source* from *getting the number*: a search query that
  bundles currency figures can trip a money-guard and return a HOLD. Search the
  topic plainly, then extract the primary page.
- Encyclopedia entries are usable for dates and offices, weak for
  characterisation; treat any single-source personal detail as VERIFY.
- Older documents are scans: a figure read out of one is not MEASURED until a
  second source agrees.

## Worked example

`references/petronas-leadership-lineage.md` — PETRONAS chairman and President/CEO
succession 1974 to present, including a documented eleven-year acting-chairman
period, plus the fan-out contract as applied.
