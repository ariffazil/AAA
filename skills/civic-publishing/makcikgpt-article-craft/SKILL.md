---
name: makcikgpt-article-craft
description: Use when drafting a MakcikGPT article for the site.
---

# MakcikGPT Article Craft

Drafting op-eds for the user's own civic publication (arif-fazil.com → `/world/makcikgpt/`). The voice is a pasar-malam auntie; the standard is a dossier. Satire carries the argument, never replaces it.

## When to use

- "buat satu makcikgpt article", "draft for me to publish", "kutuk <person>"
- Any request to write for the MakcikGPT series: PETRONAS, governance, politics, economy, tech sovereignty
- Any request to turn a live news event into a piece for the site

## Standing rules — these are non-negotiable

### 1. Assume zero context. This is the rule most often missed.

The reader has never heard of the statute, the two companies, the number in dispute, or the parties. **Define everything before you argue anything.**

A piece that opens with the argument is a failed draft and must be rewritten, not patched. The user has rejected a draft for exactly this reason.

Before the first point is made, the piece must establish:

- **Who the actors are**, in one plain clause each — not their titles, their function
- **What the legal instrument is** and what year it is from, and what it does
- **The actual number** being fought over, and who currently receives it
- **Why the two sides disagree**, stated fairly enough that a partisan of either side would accept the description

The published template puts this in a self-contained section near the top (`DULU — KONTEKS UNTUK PEMBACA BARU`) and only enters the argument after it. Follow that shape.

### 2. Draft in chat. Publish only on approval.

Never deploy a MakcikGPT piece on your own initiative. Present the full draft in conversation, say the deploy step is waiting, and stop. Deploy is a separate, explicit instruction.

### 3. Land on a type, not just an act.

A generic criticism ("he is bad") fails. The piece must name a *kind of person* the reader recognises: the one with courage to travel but not to sign; the one whose hands are clean because someone else holds the pen. The user states the type they want ("jenis tadak teluq") — build the piece to that target rather than restating the news.

Pair the insult with a **mechanism**. The pieces that land always do:

- a cash transfer reframed as rent paid to keep the status quo (rather than as a settlement)
- the same man holding two opposite registers on the same day, framed as a price paid per audience
- an entity's output measured against what it withholds

Without the mechanism you have only written down that the user is angry.

### 4. Close with a one-line quotable.

The series always ends with a single sentence the reader can paste into a WhatsApp group with no article attached. Write it deliberately, not as a summary of the last paragraph. Expect to be asked for it separately — offer it.

### 5. When asked to simplify, cut. Do not rephrase.

"Simplify 7 line" means seven lines. "Combine into one" means one, with the sections merged rather than stacked. The user has weighed an eight-hundred-word answer against an eight-word one and asked which was more efficient — length that survives a compression request is a defect.

Applies to chat replies as much as to drafts.

### 6. Every figure gets verified before publish.

Cross-check numbers against the primary source, not against the news article that reported them. See `petronas-entity-filings-probe` → `references/group-financial-report-audit.md` for the financial case (accumulated-loss recognition vs operating loss, cash-flow statement vs computed burn, deck percentage vs report absolute, declared dividend vs analyst target, two price series cross-labelling).

Label each figure by class, on the page where it appears:

| Class | Treatment |
|---|---|
| Court-recorded or official filing | State plainly, name the source |
| Party assertion (a claim in a filing or a statement) | Attribute to the party, say untested |
| Analyst / press estimate | Name it as an estimate and name who made it |
| You could not verify it | Drop it, or name it as unverified |

A precise-looking unsourced number is a liability, not a rhetorical asset: it discredits the verified material beside it.

### 7. Attribute quotes exactly — or say you could not.

If a verbatim quote cannot be confirmed at time of writing, paraphrase it and **declare the paraphrase in the corrections footer**. Do not attribute a source you did not read.

### 8. Ship the corrections footer.

Every published piece carries a short honesty block at the foot, in three parts:

- **Verified** — what was checked, and against what
- **Corrected from the original** — what the first draft got wrong and what replaced it
- **Could not be verified at publication** — named plainly, including any quote you had to paraphrase

This exists because prior drafts contained corrected figures. It is part of the house style, not an apology.

## Draft checklist

1. Zero-context section present, before the argument? 
2. Each actor described by function, not title?
3. The disputed number stated, with its source class?
4. Every figure traced to a primary source, or labelled?
5. Villain framed as a type, with a mechanism attached?
6. One-line quotable written and deliberately placed?
7. Corrections footer drafted (verified / corrected / unverified)?
8. Draft presented in chat with deploy waiting on approval?
9. After deploy: page verified by **content**, not by HTTP status (see `references/publication-pipeline.md`)

## Pitfalls

- **Resolving a live event to a conclusion the article has not earned.** The series is satirical; the facts underneath are not. If the argument needs a fact that does not exist, the piece is the wrong length, not the fact missing.
- **Opening with the insult.** The insult is the closer. Opening with it means the reader has to take your word for something you have not yet shown.
- **Treating a near-settlement as a settlement.** "Almost done", a signed framework and a transfer of funds are three different things, and the piece is worthless if it conflates them. Name which one exists.
- **Inheriting a figure from another article in the series.** Series pieces get quoted into each other; a wrong number propagates. Re-verify per piece.
- **Publishing before approval.** Deployment is never implied by a request to draft.

## References

- `references/publication-pipeline.md` — the three registration surfaces an article must reach, why an HTTP-200 page gate passes while the article is unreachable, and how to render and verify a PDF artifact.
