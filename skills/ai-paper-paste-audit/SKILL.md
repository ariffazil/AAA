---
name: ai-paper-paste-audit
description: "Use when Arif pastes an AI paper link or arXiv-cited draft."
tags: [arxiv, citation, verification, paste, ai-research, kunyah]
---

# AI Paper Paste Audit — kunyah pasted AI/ML claims against the source

Arif pastes AI-research papers and tweet summaries constantly (zero-prompt triage lane), and
multi-citation AI-governance drafts that must be verified citation-by-citation. This is the
procedure. `viral-citation-falsification` (institution-attribution drift) runs alongside it when
the paste names an institution or named researcher.

## Procedure

1. **Resolve every arXiv ID against its own `/abs` page.**
   `web_extract(urls=['https://arxiv.org/abs/<ID>'])` returns the full abstract plus the author list
   in one hop — enough to confirm or reject headline figures, benchmark numbers and authorship.
   A tweet's numbers are usually accurate to the paper; still run the check, never presume drift.
   Open `/html/<ID>` or the PDF only when ablations, tables or method detail actually matter.

2. **Quote the paper's number, not the paste's.** If they differ, reject the paste's figure and state
   the paper's. Paraphrase is not a quotation.

3. **One verdict per citation, never a blanket pass.** For each cited source report one of:
   *claim matches* / *claim drifts* (say how) / *source silent on the claim*. Then give the draft an
   overall verdict. When all citations hold, say so plainly as a finding — a clean audit is a result,
   not a failure of the audit to find anything.

4. **End at value, not at error-hunting.** After verdicts, add what the cited sources imply that the
   draft missed — a contradiction, an instrument's own assumptions, a supporting-but-unused result.
   Example shape: a benchmark scored by LLM judges is itself subject to the judge-bias phenomenon
   the draft cites as a separate section; pointing that out strengthens the draft.

5. **Deliver in human language (BM dapur register), 'so what' framing.** No audit table, no
   claim-receipt jargon, no system vocabulary. For a single paper: what it is, whether the numbers
   hold, hype-vs-physics, and the value for Arif's world — 2-3 short paragraphs, no closing question.

## Pitfalls

- **A paraphrased figure never ships as a quotation.** If the paste says "~4,000×", write the
  paper's actual number or "~4,000× (paper reports 3,906×)".
- **Citation strings can be right while the attribution is wrong.** "The paper exists" is not
  "the paper says what the draft says it says" — always diff contents, not existence.
- **Caveats that weaken a correct claim belong in one clause, not a hedge paragraph.** E.g. a study
  pooled from multiple human studies is reported as "sekitar 100K tindak balas dari kajian manusia",
  not "well actually the methodology…".
- **Never ratify the draft as a whole on the strength of its citations.** Verified sources make the
  claims *berasas* (grounded), which is a different verdict from correct.

## Skills-library note

The natural home for this was `viral-citation-falsification` and the `web-ops` extract-lane pitfalls
(both under /root/AAA/skills, externally owned, read-only to autonomous curation). Until a curator
session merges this in, this skill is the working home; when merging, fold Procedure §1 and the
first two pitfalls into `viral-citation-falsification` and delete this file.
