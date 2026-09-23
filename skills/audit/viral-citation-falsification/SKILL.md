---
name: viral-citation-falsification
description: "Verify user-cited academic studies."
version: 1.0.0
risk_tier: low
floor_scope: [F2, F6, F9]
autonomy_tier: T0
tags: [epistemic, verification, citation, attribution, paste]
capability_tier: fed-long-context
ecology_state: COLD
---

# Viral-Citation Falsification

> **Quoted and forwarded ≠ verified and found.** A study quoted at third hand has already lost
> the author, the institution, and the figure — usually in that order.

The three standard checks (`pasted-review-falsification`) target reviews **of our system**.
This skill covers a different failure shape: the user pastes text they read somewhere and
attributes it to a named authority. The text may be real, but the user's framing about where
it came from has travelled further than the paper has.

## The propagation path

```
paper → resend → social reshare → repost → user
```

Each hop is a chance for the attribution to drift. By the time a paper reaches the user's
chat:

- institution may have shifted (Helsinki ↔ Stanford ↔ "researchers");
- figure may have amplified (3,906× → "4,000× → "by a factor of thousands");
- year may have collapsed (2026 paper → "recent research");
- framing may have hardened ("proved" replaces "suggests").

The user's quote is treated as evidence because the attribution sounds authoritative. But
**the chain is already broken by the time it reaches us.**

## Two mandatory checks, in addition to whatever the existing falsification flow does

### Check 1 — Verify the institution that named it

Search the institution's own domain for the paper, the title, or key terms from the claim.

```bash
# example
web_search(query='site:helsinki.fi "Cognitive Divergence" OR "Delegation Feedback Loop"', limit=5)
```

A paper not indexed under the citing institution **may still exist** — but with different
authorship. If the user's "Helsinki" attribution does not match, the credibility chain is
broken. Report the discrepancy plainly. Do **not** smooth it over: the user made the
attribution, the paper did not.

### Check 2 — Diff the paper's own numbers against the quote

Open the arxiv / DOI / publisher abstract. Read the title, author list, institution field,
and the actual reported figure. Three possible outcomes:

| User says | Paper says | What to do |
|---|---|---|
| "3,906× growth" | paper reports 3,906× growth, 2017–2026 | Match — accept, **quote paper verbatim**, not user |
| "3,906× growth" | paper reports different number | **Reject the user's figure**, quote the paper's |
| "3,906× growth" | paper doesn't report a number | **Reject the entire claim** — paraphrase ≠ source |

If the user is not quoting from the paper (paraphrase, summary, meme), say so explicitly.
A citation you cannot trace is a rumour with an author attached.

## The single-sentence rule

> **The user can be mistaken about where they read something. The paper cannot.**

Do not adopt the user's institutional framing just because they said it first. When the
attribution is wrong, say so plainly:

- ❌ "Ya, Helsinki memang cakap macam tu"
- ✅ "Helsinki tak — arxiv 2603.26707 nyatakan Stanford."

Mirroring the user's framing imports their error into your credibility chain. The user
trusts you to be the verification layer; if you echo unverified framing, that trust is
spent.

## Pitfalls

- **Never relay a paraphrased figure as a quotation.** If the user says "~4,000×", do not
  write "4,000×" in a reply back to them — quote the paper's actual number, or write
  "approximately 4,000× (paper reports 3,906×)".
- **Never echo back the user's institution before checking it.** The earlier you verify, the
  smaller the propagation surface. If you wait until you are quoting the figure, by then
  you've already mid-signed the framing.
- **A paper can be real but the citation can still be wrong.** "arxiv 2603.26707 exists" ≠
  "arxiv 2603.26707 says what the user said it says." Verify the contents, not just the
  existence.
- **Do not soften a wrong attribution into "partly right".** Wrong institution is wrong
  institution. The user can correct their forward; you owe them the unamended record.
- **A diagram/figure inside a paper is a claim, not an observation.** Treat every visual
  claim (chart, headline, growth curve) as needing the same verification as text.

## How this fits the existing flow

`audit-ops` → `references/pasted-review-falsification.md` runs the three standard checks
when text is pasted. Run **this skill after** those three when:

- the text is attributed to a specific institution or named researcher;
- the text carries a specific figure, ratio, year, or growth-rate;
- the text will be repeated, amplified, quoted, or written into a deliverable.

Use the verdict shape from `pasted-review-falsification` (`which claim failed which check`),
and add a fourth column for the institution check.

DITEMPA BUKAN DIBERI
