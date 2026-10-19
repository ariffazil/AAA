---
name: taste-profile-artifact
description: Use when profiling taste or ranking picks for people.
version: 1.0.0
triggers:
  - "how does <platform> know what I like"
  - "what would I / he / we like"
  - "build a watch / read / listen list"
  - "rank these for me, him, us"
  - "compare my taste with <person>"
floors: [F2]
tags: [curation, recommendation, taste, artifact, two-reader]
---

# Taste Profile Artifact

Governs the case where the principal asks you to model what a person enjoys and turn it into a
ranked list — for himself, for someone close to him, or for the two of them together. The deliverable
is a curated artifact, not a platform review and not a genre dump.

Two things make this fail: guessing the taste from who the person *is*, and hiding that you guessed.
Both are fixed before the first item is chosen.

## 1. Anchor on titles he named, never on the person's role

**Never derive taste from profession, seniority, or life situation.** A geoscientist does not
automatically like documentaries; a coach does not automatically like sports films; a parent does not
automatically like family drama. Role tells you how someone spends the day, not what they choose when
nobody is watching. A list inferred from role reads as a horoscope — flattering, plausible, worthless.

Take the anchors he states ("I'm into X and Y", "he watches Z") as the only hard data. Two or three
anchors are enough to find a pattern, never enough to declare a taste complete. Say so on the face of
the artifact.

**When he pushes back with "based on what?", the next artifact answers that in its first section, not
a footnote.** A short explicit basis — what was given, what was inferred, what was assumed — costs
three sentences and buys the document its authority. Presenting inference in the grammar of
measurement is the same defect as an unlabelled forecast.

Recheck before defending. If the correction is factual ("he actually watches Z"), rebuild around the
new anchor; do not argue that the old list still fits. A pattern derived from two anchors is weak
evidence and should be replaced without ceremony.

## 2. Read the pattern as a question, not a genre

The useful abstraction is the **question the viewer is asking**, not the category. Two titles in
different genres can occupy one question; two titles in one genre can ask different ones.

- "Breaking Bad" + "You" → *can I understand someone who became rotten?* (justification, interiority).
- "The Good Doctor" → *can a good person survive the system?* (competence under contempt).
- What the pair shares is the level of **stakes**: both are a person inside an unfair system. That
  overlap is the shared rail's foundation, not a coincidence to ignore.

Write one sentence per profile in that form and put it in the artifact. A genre list ("crime,
thriller, drama") explains nothing and cannot generate a pick the reader has not already seen.

## 3. The shared list is a different construction, not an average

For two people, do not merge two solo lists by score. A shared list is built under **two filters**
instead of one — which is exactly why it usually reads stronger than either solo list:

- One filter keeps what lands for person A; two filters also discard everything that lands for only
  one of them, which is most of any solo list.
- What survives tends to be the work with two layers — a human story for one reader, a system/stakes
  story for the other. Those are better works, not compromises.
- A solo list repeats one colour because one filter never forces variety. A shared list needs heavy
  and light, or the pair stop watching together.

When he asks "why is the shared list better than mine?", this is the answer. Give him the honest part
too: some shared picks earned their place by being excellent, not by fitting the profile. Stepping
outside the pattern is allowed; claiming it was predicted is not.

## 4. Building it

1. **Choose the titles first as a plain text list and check the count against the ask.** Eleven means
   eleven per rail, not fifteen with eleven kept — he states counts as contracts.
2. **One line of why per item, in his register, naming the mechanism** ("same lane: you sit inside the
   head of someone doing wrong"), never "you'll love this".
3. **Metadata and artwork from a public API** so the artifact stays offline-capable and does not
   hotlink: `https://api.tvmaze.com/singlesearch/shows?q=<title>` returns `name`, `premiered`,
   `network`/`webChannel`, `genres`, `image.medium|original`.
   **Verify the returned name and network against what you meant.** A fuzzy single-search match is the
   normal failure — a local remake, a same-titled documentary, a foreign adaptation. Reject and
   re-query with the original-language title rather than shipping the wrong poster and year.
4. **Down-scale artwork before embedding.** `PIL` thumbnail to ~300×450, re-save JPEG q≈82: roughly
   25 KB per poster, ~1 MB for a 33-title file.
5. **State the status of the numbers.** A "98% match" is your confidence — not the platform's score,
   not viewing data. One line on the face of the artifact, and never imply you read an account you
   did not.
6. **When it ships onto a site**, the page carries the same basis line. Deploy and routing rules for
   the host belong to the site-ops skills, not this one.

## Pitfalls

- **Profession-as-taste.** The most common failure. The tell is that every pick is a genre you could
  have guessed from a job title.
- **A profile with no stated basis.** The reader assumes the machine looked at his account. If it did
  not, the omission is a lie by framing, not a stylistic choice.
- **Defending the first list.** Anchors are cheap to re-derive and the artifact is cheap to rebuild;
  arguing costs more attention than rebuilding.
- **Treating a two-person list as a compromise list.** It is a stricter construction — say so, and do
  not include items only one of them will finish.
- **Naming a title you did not verify exists.** A wrong title with a right-sounding poster is the
  fastest way to lose the artifact's credibility.
