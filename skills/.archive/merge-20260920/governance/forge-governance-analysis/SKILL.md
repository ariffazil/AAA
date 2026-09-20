---
name: forge-governance-analysis
tags: [governance, institutional, board, corporate]
description: "Use for corporate governance analysis."
---

# FORGE Governance Analysis — Systematic Workflow

## Standing Rules

1. **Pages that don't carry dates are designed that way.** A leadership page without appointment dates, term limits, or "appointed by" disclosures is a design choice that prevents temporal questioning. Treat atemporal pages as the primary signal, not background.
2. **"Who was removed" is always the first question, not the second.** Most analysts catalog who IS on the page. The real story is who WAS on the page and isn't anymore. Compare Wayback snapshots before writing a single word.
3. **Boldness over hedging when facts are verified.** When three or more sources confirm a structural pattern, state the pattern directly. Do not dilute verified findings with unnecessary qualifiers.
4. **Counterfactual obligation: state ONE failure condition.** Before any structural critique, name ONE condition under which the analysis would fail. If you cannot name one, you do not understand the problem.
5. **F6 MARUAH: institutional critique ≠ personal defamation.** State the role, the action, the structural consequence. Do not attribute motive without evidence.
6. **Test: if the individual changes but the structure stays the same, the individual is not the unit of analysis.**

## Step 1: Temporal Anchoring (BEFORE any analysis)

Never treat a live governance page as a static snapshot. Always establish Δt.

### Sub-steps:
1. **HTTP headers** — pull `Last-Modified`, `etag` via `curl -I`. Record them.
2. **Wayback Machine CDX** — query:
   ```
   curl -s "http://web.archive.org/cdx/search/cdx?url=<page>&output=json&from=<year>&to=<year>&collapse=digest&fl=timestamp,statuscode,length,digest"
   ```
   - `collapse=digest` groups consecutive snapshots with identical content — only these represent real content changes
   - Compare digest values: same digest = no change; different digest = page was edited
3. **Image upload path dating** (Drupal sites) — extract all image URLs, group by upload folder year (`/uploads/content/2024/` = uploaded 2024). Reveals when each face was added.
4. **sitemap.xml** — pull `<lastmod>` for the specific URL. Reflects actual CMS save time.

### Pitfall:
On Drupal sites, `Last-Modified` ≈ request time because Drupal regenerates ETag on every cache cycle. Validate by fetching 4-5 sibling pages — if all show "today" → cache artifact, not content change.

## Step 2: Extract WHO Is On the Page

List every named individual: name, role, classification (Independent/Non-Independent/Executive), background.

## Step 3: Extract WHO Was REMOVED

Compare Wayback snapshots. Who is in A but not in B? Those are the removed directors. Removals without replacement are the strongest signal.

## Step 4: Cross-Reference with Official Documents

Pull the company's Integrated Report (IR) or Annual Report PDF:
- Board composition section
- Director profiles (date of appointment, qualifications)
- Committee memberships
- Remuneration framework for NEDs

### Key validation:
- Cross-validate board size: if 3 women = 43%, board = 7; if 3 women = 37.5%, board = 8
- If live page differs from IR → page updated after IR filing, possibly without announcement

## Step 5: Vote Math

- **Executive bloc:** EDs report to CEO → vote as a block
- **Non-independent NEDs:** government nominees → effectively pro-management
- **INED count:** can they outvote executive + non-independent?
- **Chairman:** breaks ties? Who appointed the chairman?

If executive + non-independent > INEDs → board cannot mathematically challenge management.

## Step 6: Corporate Event Calendar Cross-Reference

Map board changes against corporate events. **Who left before the bill came due?**

## Step 7: Structural Synthesis — Three Layers

1. What the page says (public narrative)
2. What the page doesn't say (omissions vs IR)
3. What the page is designed to prevent you from asking

## Branch: Ownership, Control and Consolidation Questions

When the question is not board composition but **who controls the institution, what constrains them, and whether a transaction is real** — stake sales, merger rumours, regulator-imposed holding conditions, family/GLC control chains — switch to `references/ownership-consolidation-analysis.md`. It covers: computing effective economic interest down a control chain, separating a standing statutory rule from a condition attached to one approval, building the shareholder motive matrix to test a deadlock rather than assert it, the base-rate ledger of prior attempts, the absence sweep plus monitoring tripwires, and the output guardrails (no rating or investment recommendation).

The premise-check rule generalises to both branches: when the request arrives carrying a counting or naming error about the institution, correct it in the first line. A brief that inherits a false premise validates it.

## Step 8: Counterfactual Discipline

Before publishing, state ONE condition under which the analysis fails.

## Pitfalls

- Treating a live page as a fixed document → miss the story
- Cataloging who IS there without asking who WAS there → miss the removals
- Not pulling IR PDFs to cross-validate → miss discrepancies
- Hedging verified patterns with unnecessary qualifiers → perceived as weakness
- Naming individuals without institutional framing → defamation risk

DITEMPA BUKAN DIBERI