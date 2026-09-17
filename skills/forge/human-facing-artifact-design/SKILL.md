---
name: human-facing-artifact-design
id: human-facing-artifact-design
version: 1.0.0
description: Use when forging PDFs, briefs, resumes, dossiers, logos.
owner: Hermes (curator-managed)
risk_tier: low
floor_scope: [F1, F2, F4, F6]
autonomy_tier: T1
tags: [artifact-design, pdf, reportlab, resume, dossier, brief, logo, audience, hierarchy, density]
---

# Human-Facing Artifact Design

> The human reads the artifact. The agent reads the source. Never confuse the two.

Load when asked to build any document a person will read — resume, interview brief, dossier, decision memo,
one-pager, encouragement note — or a logo/mark, or when a draft comes back rejected as too sparse, too dense,
or laid out for the wrong reader.

## 1. Audience decides the layout — split the two explicitly

Name the reader **before** laying anything out. There are two, and they want opposite things:

- **Human artifact** (resume, interview brief, encouragement note, decision memo, logo) — meaning first, confidence second, technical depth only as a backup annex. The reader must leave feeling something is now clear, not that they must study.
- **Technical artifact** (basin dossier, prospect review, interpretation record) — evidence first, epistemic tags mandatory, density is a virtue.

Never fuse them. Handing a technical dump to a human reader is a failure even when every fact is correct. For a human artifact the question is not "is this complete?" but "does the reader now know what to do or feel?"

Related: `FORGE-artifact-publisher` covers the EMD pipeline mechanics (HTML → Chrome headless → delivery). This skill owns the layer above it — who is reading, and how the page is weighted.

## 2. Attention hierarchy — visual weight follows consequence

Rank content by consequence *before* styling it. A page where a career-defining achievement renders with the same weight as a membership line has no hierarchy, and the reader will not retain the thing that mattered.

- The single most consequential item gets a dedicated band, box, or half-page block.
- Supporting items get compact rows.
- Trivia gets a comma-separated line, or is cut.

If you cannot name the one thing the reader must retain, the layout is not finished.

## 3. Density beats page count

A page limit is a density target, not permission to ship whitespace. A sparse two-page document reads worse than a packed one. When told "max N pages", produce N full pages of signal and verify by counting characters per page from the built PDF — never by eyeballing. Snippet in `references/pdf-and-image-toolchain.md`.

## 4. Care artifacts are not information transfer

When the artifact exists to steady a person — interview preparation, encouragement, hard news — the body is: their proven record stated plainly, what is actually at stake, what they control, and three or fewer instructions. Not a curriculum.

Probing the domain surfaces far more material than the person needs. The discipline is **selection, not compilation**. A twenty-page technical annex is a fine *annex*; it is not the artifact. Offer the annex as backup and lead with the short thing.

Do not answer a request for clarity with volume. When a person asks for confidence, handing them fifty more technical questions increases their load rather than transferring capability. Establish what state they are actually in before deciding what to build.

### Writing in the sovereign's own voice

When asked to say something *as* the user to another human, match his register: plain Malay/English code-switch, short sentences, no headers-as-therapy, no bullet list of feelings, no numbered framework where one sentence will do. Ground it in specific shared history rather than general encouragement — a named moment he witnessed lands; a generic pep talk does not.

### Zero system references in personal reflection artifacts

When the artifact is a personal reflection, life document, or wisdom piece — anything addressed to the human about his own life — the rendered text must contain ZERO references to any technical system: no MCP, no organs, no federation, no agents, no tools, no code, no architecture, no federation nodes. The human reads this, not the machine. 'No coding stuff' is the rule, not a suggestion. If the underlying work used 14 MCP tools and 3 subagents to produce it, the human never sees that. The artifact reads as if it was written by someone who sat with him and thought deeply — because that is exactly what happened, the tools are just the cognitive infrastructure.

**Pitfall:** Subagents asked to generate personal artifacts will default to describing their process or embedding system context if the prompt does not explicitly forbid it. The ban must be stated in the delegation prompt, not assumed.

## 5. Probe before quoting any number

Market, salary, price and status figures must come from a live probe in the same session, with source and date stated alongside the number. Reciting remembered figures is fabrication-adjacent and gets caught.

Where a domain convention differs from the obvious metric, report the convention rather than the raw metric. Example: Malaysian oil-and-gas compensation is quoted as a **total package** (base + bonus + allowances + rotation). Base alone is systematically low, and quoting it alone materially understates an offer — quote the package and say which components are in it.

## 6. Iterate one file, then send once

Build and refine a single output path; do not generate v2/v3/v4 side by side and ask the user to choose. Each intermediate is noise in their inbox. Send the artifact when it passes the checklist, then iterate if rejected, and offer to remove superseded drafts rather than leaving several near-identical files behind.

## 7. Pre-send checklist

```
[ ] Reader named, and the layout matches that reader (§1)
[ ] The one thing they must retain is the most visually weighted element (§2)
[ ] Every page is dense — chars/page counted from the built PDF, not eyeballed (§3)
[ ] No number appears without a source and a date (§5)
[ ] No internal vocabulary in the rendered text (floor IDs, tags, tool names, PASS/FAIL)
[ ] No system references in personal reflection artifacts (§4)
[ ] Page count matches the limit, verified from the file
[ ] Text extracts cleanly (pymupdf / pdftotext returns real text, not empty)
[ ] One file sent, not several drafts (§6)
```

## 8. Toolchain

See `references/pdf-and-image-toolchain.md` for ReportLab paged-footer and section-band recipes, the density
verification snippet, Matplotlib gotchas that cost time, the geological cross-section orientation rule, and
Gemini image-model selection with the `responseModalities` contract for logos and marks.

---

*DITEMPA BUKAN DIBERI — the artifact is the proof.*