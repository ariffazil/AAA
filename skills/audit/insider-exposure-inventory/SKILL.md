---
name: insider-exposure-inventory
description: "Use when auditing published writing for ungroundable claims."
version: 1.0.0
owner: Hermes
risk_tier: T1
floor_scope: [F1, F2, F4, F6, F13]
triggers:
  - "audit my articles for risk"
  - "which sentence can't be defended"
  - "insider knowledge in published writing"
  - "pre-publication source-grounding check"
  - "SLAPP / defamation exposure review"
  - "mark every claim without a public source"
  - "flag sentences only an insider could write"
tags: [audit, source-grounding, corpus, defamation, provenance, publishing]
capability_tier: fed-long-context
ecology_state: WARM
---

# Insider-Exposure Inventory

Given a published corpus (articles, posts, columns), answer one question per sentence:
**can a reader go and look this up?** If not, it is *undefendable* — not necessarily wrong,
but impossible to answer with a document. That distinction is the entire product.

**Not legal advice.** This maps source-grounding. Whether a sentence is actionable depends on
jurisdiction and facts outside the corpus; say so in every deliverable.

## The five classes (fixed taxonomy — do not invent new ones per run)

| Class | Meaning |
|---|---|
| INSIDER_KNOWLEDGE | Requires material only obtainable inside an org: internal meetings, minutes, memos, org detail, staffing/HR, unreleased figures |
| FIRST_PERSON_ORG | Author positions himself as employee/participant inside the institution he is writing against |
| UNGROUNDED_FACT | A specific checkable number, sum, date, named act — no public source cited |
| ATTRIBUTED_INSIDE | Stated basis is a private channel: unnamed insider, hearsay, personal dossier, chat logs |
| MOTIVE_AS_FACT | Named living person's private motive/fear/intention stated as settled fact rather than opinion or question |

Severity: **HIGH** = reveals non-public institutional info, an unreleased figure, or first-person
employee knowledge. **MED** = specific checkable assertion with no source cited. **LOW** = insider
phrasing that asserts nothing checkable.

## Procedure

1. **Extract every body to plain text.** Article content is often stored as a TS/JS template
   literal or a CMS field, not a `.html` file. Write one extractor that handles both shapes:
   - `html: \`...\`` (object property)
   - `const html = \`...\`` (module-level variable)
   Scan for the delimiter generically and walk forward respecting `\\` escapes to the matching
   backtick. Skipping only the object-property form silently drops files (cost me 5 of 35 on the
   first pass — failures showed as 0-char extracts, which is the tell).
2. Verify extraction coverage: print per-file char counts and eyeball for zeros.
3. **Batch the corpus and fan out.** One reader per batch, each reading every file IN FULL —
   sampling misses the qualitative findings. 5 batches x 7 files worked well.
4. **Forbid paraphrase for verification.** The reader must return the exact sentence. Then
   programmatically assert every quote appears verbatim (normalise unicode quotes/dashes and
   whitespace first). Reject and re-run any batch with failures. Never ship an unverified quote.
5. **Dedupe and re-derive counts in code** — never by hand. Group by slug, count by severity.
6. **Write your own triage pass.** The sweep is deliberately strict, so it produces false
   positives: rhetorical questions, facts that are registerable (company records), sentences
   that are plainly opinion, and — the sharpest one — sentences that appear inside a piece
   *demonstrating* fabrication. Publish the discount list. An inventory that cannot be
   discounted is not evidence.
7. Deliver as a document, not a chat dump. Cover page with the counts, findings grouped by
   article, a triage page, and a method/limits note.

## Pitfalls

- **Subagent findings are self-reports.** The verbatim-assertion step is what makes the output
  trustworthy; without it you are relaying, not witnessing. Run it every time.
- **Do not pad.** A shorter list of real findings beats a longer list of maybes. Instruct readers
  explicitly that a file with nothing must be reported as having nothing.
- **Recurring trifecta** (seen across a whole corpus): the byline claiming inside standing;
  first-person descriptions of internal life; motive stated as fact. The byline is almost always
  the cheapest repair and the most frequently cited exposure — surface it first.
- **Cheap repairs, not deletions.** Recast assertion to question; attach a citation, widen to an
  honest range, or cut the false precision; drop the byline rather than the voice. Say this in the
  deliverable — otherwise the output reads as an instruction to stop publishing.
- **Never publish the inventory itself.** It quotes the exact sentences and names the exposure.
  It is an internal document; deliver to the principal only.
- **Result is perishable.** Any new article invalidates it. State the sweep date on the artifact and
  say plainly that it must be redone when the corpus changes.
