# arXiv ID Reassignment — Confirmed Cases and Detection Protocol

> arXiv IDs that have been permanently reassigned to unrelated papers. Future SCOUT
> sessions must verify every cited ID directly and pivot to venue-based citation
> when matched.

## Why this happens

When a paper is withdrawn from arXiv, the ID slot MAY be reused by a later
submission. The original paper then has no arXiv URL — only its conference/journal
record. arXiv's citation system does not redirect; the new paper inherits the
ID with no warning.

## Confirmed cases (from 2026-08-12 session)

### 2303.02381

- **Was**: Madaan, A., Tandon, N., Gupta, P., et al. "Self-Refine: Iterative Refinement with Self-Feedback." NeurIPS 2023.
- **Now**: Abhignan, V. and Muthuganesan, R. "Effects of intrinsic decoherence on discord-like correlation measures of two-qubit spin squeezing model." (Physica Scripta 96 (2021) 125114, quant-ph preprint on arXiv 2023-03-04)
- **Detection**: title mismatch when curling `https://arxiv.org/abs/2303.02381`. The current title is "Effects of intrinsic decoherence..." not "Self-Refine..."
- **Citation rule**: cite Self-Refine via NeurIPS 2023 proceedings, not arXiv URL.

### 2310.19049

- **Was**: Chen, J., Chen, L., Zhu, J. "More Agents Is All You Need." LLM-ensemble preprint (2023).
- **Now**: Sanz-Alcaine, J.M., Sebastian, E., et al. "Estimation of Semiconductor Power Losses Through Automatic Thermal Modeling." (2023-10-29)
- **Detection**: title mismatch when curling. Current title is about semiconductors.
- **Citation rule**: cite via the conference version or the original preprint title-only.

## Detection protocol

Before citing any arXiv ID in a SCOUT output, verify it:

```bash
curl -sS -L --max-time 12 -A "Mozilla/5.0" \
  "https://arxiv.org/abs/<id>" \
  | grep -oE '<meta name="citation_title" content="[^"]+"|<meta name="citation_author" content="[^"]+"'
```

The returned title MUST match the title you intend to cite. If it doesn't:

1. Mark the source as `canonical_but_not_refetched` in the YAML inputs block.
2. Cite by venue (NeurIPS/ICML/ICLR/etc.) rather than the arXiv URL.
3. Add a caveat to `source.caveats` listing the ID and the new paper it points to.

## What NOT to do

- DO NOT link the original arXiv ID in the rendered output. The reader will click
  through and land on a physics paper, which is a credibility-destroying failure.
- DO NOT silently replace the URL with a search URL. Cite by venue.
- DO NOT assume the ID is stable. arXiv reassignment is invisible until you fetch.

## Why this matters more than it sounds

For audit-grade artifacts, every cited URL is a falsifiability test. If a reader
clicks your Self-Refine citation and lands on a quantum-physics paper, the entire
provenance chain is compromised. The discipline of venue-based citation is what
separates a research-grade output from a hallucinated one.
