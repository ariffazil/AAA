---
name: research-paper-sourcing
description: "Use when a pasted draft cites papers that must be verified."
tags: [research, papers, arxiv, verification, evidence]
version: 1.0.0
capability_tier: fed-long-context
---

# Research Paper Sourcing — from cited claims to a verified primary-source shortlist

Trigger: he pastes a long analysis draft, a social post, or his own synthesis that carries
claims about research (numbers, named methods, attributed findings) and the ask is
"find the primary papers" or "verify the citations" — not a general web answer.

Distinct from `viral-citation-falsification` (that one verifies ONE figure he attributes to
ONE authority). This skill covers the whole-claim-set case: many claims, one sourcing pass,
a shortlist as the deliverable.

## Procedure

1. **Extract the claim set first, before searching.** List every load-bearing claim:
   each number, each named method/benchmark, each attribution ("a Google paper", "a
   100,000-person study"). A draft with N claims needs the list written down — searching
   while reading loses claims silently, and the deliverable is judged claim-by-claim.
2. **Run parallel searches, one per distinct claim family, in ONE batched turn.** Queries
   are keyword-style, not questions: method name + distinctive number + `arxiv` beats any
   sentence. 3-4 searches per batch; a second batch only for claims the first missed.
   Search-backend chatter (`backend_error`, fallback tiers) goes in the same batch —
   batching hides per-call latency.
3. **Resolve every hit to the primary record before using it.** Social PDF mirrors
   (`alphaxiv.org/pdf/<id>`) and reposts resolve to `arxiv.org/abs/<id>` — the abstract
   page carries the headline numbers AND the full author list, which the mirror never
   shows. DOIs and publisher pages work the same way: fetch the record, not the summary.
4. **Diff every pasted claim against the primary record.** Numbers usually survive the
   repost; framing and attribution frequently do not. "A Google paper" is an affiliation
   claim — check the author list and affiliations on the abs page, not the poster's
   framing. Verdict per claim: BETUL / SALAH / SEPARUH, with the primary id attached.
5. **Present grouped by the draft's own structure, not chronologically.** Each paper gets
   one line: what it claims, and the DELTA it adds to the draft — a paper that merely
   confirms what the draft already says gets half a line. He reads the shortlist to see
   where his draft is thin, so lead with the papers that strengthen or break it, and end
   with the two or three that matter most.
6. **Flag the gaps honestly.** Claims with no findable primary source stay marked, never
   silently dropped — and never backfilled from the draft's own authority.

## Pitfalls

- **A `web_search` result carrying `backend_error` plus a fallback `served_by` tier is a
  valid result — use it.** The configured backend failed and a fallback answered; re-running
  to get a "clean" result burns a call for the same data. Treat `backend_error` as
  provenance metadata, not task failure.
- **Never verify a reposted paper against the repost.** The repost is the propagation
  artifact; the abs page is the witness. One hop is enough for an author list to become
  "Google" or "researchers".
- **Do not adopt the draft's framing as the search query.** Its vocabulary may be the
  poster's coinage, not the paper's title — search the distinctive NUMBER and the
  benchmark name, which survive translation through reposts better than adjectives do.
- **An existing primary record outranks adding new commentary.** If a claim is already
  covered by a verified paper, the deliverable cites it; do not paraphrase it back as a
  new finding — restating sourced claims dilutes the shortlist he diffs against.
