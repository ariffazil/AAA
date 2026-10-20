---
name: priority-claim-verification
description: "Use when asked who coined a term or if a name is new."
version: 1.0.0
owner: curator
risk_tier: medium
triggers:
  - "has anyone coined this"
  - "who coined this term"
  - "is this a new field"
  - "is this original"
  - "first use of this phrase"
  - "has this been done before"
  - "priority claim"
floors: [F2, F5, F7]
tags: [priority, coinage, provenance, research, doctrine, naming]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
owned_by: curator
authority_of: AAA
---

# Priority Claim Verification

Governs the question "is this name/concept/field mine, or does it already have an owner?". It shows up when the
principal is naming doctrine, framing a research programme, launching a discipline, or defending a claim of
originality, and often arrives with a pasted analysis from another AI that already states a verdict.

The deliverable is not a yes/no. It is a **dated record**: what exists, who published it, when, in what sense, and
what remains unclaimed.

## The core error this skill prevents

An LLM answering "I could not establish an authoritative first use" is reporting the limits of its own search.
That sentence reads as a finding about the world, gets repeated as one, and collapses the moment someone in the
room has read the paper. Absence of a hit in an academic index is the weakest possible evidence of absence,
because the venues where a practitioner names their own programme are mostly outside those indexes.

Never pass a negative priority verdict forward without the sweep below. If it survives the sweep, label it as a
search limit — "no dated use found across open web, preprint servers and the field's journals" — not as
"nobody has used it".

## Procedure

1. **Exact phrase, open web, quoted.** Then a second pass adding one of: `manifesto`, `new discipline`, `new field`,
   `research programme`, `call for`, `introducing`. People naming their own programme use those words, and they
   publish on Medium, Substack, LinkedIn, a personal site or a blog — not in a journal.
2. **Sweep the venues the open web misses.** Preprint servers (Zenodo, SSRN, arXiv, OSF), conference proceedings
   in the adjacent field (AIES, CHI, FAccT), edited special issues, and non-English literature — search the phrase
   in translation too when the field has a large literature in another language.
3. **Weigh a hit by author standing, not venue prestige.** A post by a working practitioner of that exact field,
   with an institutional affiliation and a publication list, is a **dated public priority record**. An anonymous
   post is a use, not a record. Say which one you found, and never upgrade a blog to a record or downgrade a
   qualified practitioner to a blogger because the venue is a blog.
4. **Look for a second, older, unrelated sense of the same words.** Academic prose often carries the phrase years
   earlier in a different sense — a philosophical position rather than a proposed discipline. Report both senses,
   separated. Reporting only the sense that competes with the principal's claim, or only the one that does not, is
   distortion in whichever direction you chose.
5. **Delineate the neighbourhood even when the exact phrase is free.** List the works that establish the same
   conceptual ground, with dates and venues. "The term is available but the field is occupied" is the most common
   real answer, and it is the one a naive check misses.
6. **Test the name against the field's strongest paper.** A new label usually contains the error it should be
   interrogating. If the best work in the area denies the very predicate the name asserts, state the tension and
   supply the reading that survives it — or advise a different name. Do not ship a name that dies in the first
   seminar room.
7. **Re-aim the deliverable at what is unclaimed.** When the name is taken, the value moves to a standard, a
   method, an experiment, a dataset, or a definition sharp enough to survive the strongest objection. Name those
   assets and rank them by what the principal can actually produce with the resources he already has.
8. **Correct any earlier answer explicitly, in the document.** If a previous turn said the term was unverified,
   the artifact states what changed and why. He acts on the earlier answer as fact; a quiet correction leaves him
   defending a claim you have already abandoned.

## What the record must contain

| Field | Why it decides the matter |
|---|---|
| Exact title and author | A phrase is not owned; a titled work by a named person is |
| Date, precise to day | Priority is a date comparison, and month-level is often not enough |
| Venue and its status | Peer-reviewed vs preprint vs personal post changes what the record can bear |
| Author standing | Affiliation, field, publication list — what makes a post a record |
| Sense of the phrase | Two senses are two records; conflating them is the usual error |
| What it actually argues | Read the abstract, not the title; titles flatter and abstracts confess |

## Reporting shape for the principal

- **Lead with the thing that changes his position**, before the survey. If the phrase has an owner, that fact is
  the first paragraph, not a finding buried in a literature review.
- **Give the neighbour table** — work, date, what it establishes, status — so he can see the occupied ground
  himself rather than trusting a summary.
- **Close on the unclaimed assets**, ranked. "Stop defending the name, own the standard" is the useful sentence;
  a survey of who did what is not.
- **Keep every claim killable.** State which single observation would overturn the verdict (a dated use earlier
  than the record you found, in the same sense).

## Pitfalls

- **Shipping a negative verdict as a finding.** "No first use established" is a report about your search. Sweep
  the practitioner venues and preprint servers first, and label it as a limit if it survives.
- **Trusting a pasted verdict from another AI.** Treat it as a claim to ground, claim by claim, not as a starting
  point to restate. It found what it found; it did not run the sweep you can run.
- **Stopping at the exact phrase.** The absence of the string says nothing about the presence of the concept. The
  neighbourhood is the finding that usually decides the case.
- **Upgrading a self-description into a discipline.** A practitioner calling their project "a new discipline" does
  not create a discipline. Report the claim and the venue's status separately, and never launder the first into
  the second.
- **Letting the principal's enthusiasm set the verdict.** He often wants the answer to be yes. The record does not
  move because he needs it to, and telling him early costs him one hour; telling him late costs him a room.
- **Confusing "defensible" with "original".** A definition can be sharp, useful and true while the name, the
  method and the frame are all already published. Say both things in one breath.
