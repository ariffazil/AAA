---
name: presentation-pack-delivery
description: "Class-level umbrella for PPTX + PDF visual-delivery workflows. Covers the chained pipeline: outline → design system apply → PPTX generate → PDF render → voice-protocol translate → QA → seal. Also covers visual QA discipline (vision-loop trap), design coherence (sandwich structure, vertical balance), and the federation design system gap. Load when user asks for a deck, slide deck, briefing PDF, or 'make me a presentation pack'."
license: MIT
platforms: [linux, macos, windows]
---

# Presentation Pack Delivery — Class Umbrella

> **DITEMPA BUKAN DIBERI** — The class of work that turns research/content into a finished visual artifact (PPTX or PDF) for the sovereign or the public.

## Why this umbrella exists

The federation has scattered visual-delivery capability across 5+ skills (`productivity/powerpoint`, `productivity/pdf-report-generation`, `creative/html-pdf-reporting`, `aaa-pdf-voice-protocol`, `FORGE-document-intelligence`) with no shared design system, no chained workflow, and no cross-surface QA discipline. This umbrella is the convergence point.

## When to load this skill

- User asks for a "deck", "slide deck", "presentation", or any PPTX deliverable
- User asks for a "briefing PDF", "report PDF", or any PDF briefing deliverable
- User says "make me a presentation pack on X" (implies both PPTX + PDF)
- User asks to "improve" / "redo" / "audit" an existing deck or briefing PDF
- User asks to "audit / compare" v1 vs v2 of a visual artifact (visual contrast analysis)

## The Reality Bridge Doctrine (forged 2026-08-13)

PPT and PDF are not "document formats" — they are **reality transport layers** that carry reasoning across the boundary between compute and human institutions.

| Layer | arifOS verb | Artifact | Human function | Sifat |
|---|---|---|---|---|
| Chat | SENSE/THINK | Message | Presence | Dies in scrollback |
| PPT | COORDINATE | .pptx | Negotiation, decision, understanding | Mutable, editable, shared |
| PDF | WITNESS | .pdf | Attestation, audit, record | Fixed, portable, signable |

> **Chat is a surface. PPT and PDF are objects.**
> An agent that can only speak *about* reality cannot *touch* reality.
> A published artifact is no longer a chat response — it becomes part of reality.

**The pass condition:** A human opens the artifact, reads the slides, understands the lesson — **without ever talking to the agent**. If understanding requires the chat session, the bridge failed. If understanding survives independently as an artifact, the bridge passed.

**PPT vs PDF philosophy:**
- PPT = *agent proposes → human edits → human argues → human decides* — it is a negotiation space
- PDF = *inilah yang disaksikan pada saat ini* — it is a witnessing surface
- PPT is draft democracy. PDF is ratification.

**Why PptxGenJS matters strategically:** it eliminates the human-as-PowerPoint-operator bottleneck. Reasoning → structure → .pptx directly from Node. The artifact becomes native output of the reasoning pipeline, not manual post-processing.

Dark sovereign pattern (GitHub-dark palette, Gemini cover image, SHA-256 seal) → `references/dark-sovereign-pptxgenjs-pattern.md`

## The pipeline (canonical)

```
content (research, notes, scratch)
  ↓ [333-AGI Δ MIND — outline + narrative arc]
  ↓
design system apply (palette + typography + layout primitives)
  ↓ [load FORGE-tailwind-tokens or fork; see references/design-system-applied.md]
  ↓
PPTX generate (pptxgenjs) OR PDF render (WeasyPrint + matplotlib)
  ↓ [load productivity/powerpoint OR productivity/pdf-report-generation]
  ↓
visual QA — vision_analyze on rendered slides
  ↓ [vision-loop trap rule — see Pitfalls]
  ↓
PDF export (if PPTX is the primary deliverable)
  ↓ [optional — render slide→PDF for distribution]
  ↓
voice-protocol translate (if external-bound PDF)
  ↓ [load aaa-pdf-voice-protocol]
  ↓
seal + deliver (VAULT999 + MEDIA:)
```

## Visual QA discipline — the vision-loop trap rule (validated 2026-08-11)

**The rule:** fix the flagged defect → re-render → ONE confirming vision pass → ship. Treat repeated flags on the same element as noise unless the rendered PNG actually shows the defect.

**Why:** vision models re-flag the same edge-zone defect across iterations on rendered PNGs as phantom noise. If after one fix-and-verify pass, the vision model flags the same element again with a slightly different complaint ("X overlaps" → "now Z overlaps"), STOP. The raw chart/slide PNG is the source of truth, not the vision model's second pass.

**Concrete failure mode (validated):** on the 2026-08-11 arifOS slide deck, slide 1 went through 3 visual QA rounds before ship. Each round vision found a new "issue" (orphan title, top-heavy, footer cramping) — all legitimate on the first round, phantom on subsequent. Continued iteration past the first confirming pass is thrashing the user can see in their attention.

**Override (rare):** if the user explicitly asks for perfection on a specific element, do one extra round of pixel sampling with PIL or coordinate math rather than another vision pass.

## Design craft — sandwich structure + vertical balance

The federation's PPTX + PDF covers tend to fail at vertical balance: a large title block sits high while the lower half is empty cream/space. Standard fix:

**Sandwich structure:**
- Cover + Closing slides: dark background (midnight `1A1F36`), centered title, ornament at lower-third to absorb empty space
- Content slides: light background (cream `F5F1E8`), title at top, content in middle, footer at bottom with clear gap from bottom hairline
- Optional: mid-deck "ornament slide" (large decorative element + minimal text) to break rhythm

**Vertical balance patterns (validated 2026-08-11):**
- Title block at y=2.0-2.5 (not 1.5) gives room for ornament below
- Eyebrow caption must be visually anchored to title (gap ≤ 1× title cap-height)
- Subtitle → tagline rhythm must be consistent (same or slightly larger gap descending)
- Bottom hairline + footer: minimum 0.30" clearance between rule and footer text
- Empty lower half is a design defect, not a feature — fill with ornament, pull title down, or add a centered decorative element

## Federation design system (gap as of 2026-08-11)

There is NO federated design system for slides/PDF. Each skill invents its own palette:
- arifOS Constitutional Kernel deck (2026-08-11): midnight `1A1F36` + amber `D4A574`
- PETRONAS briefings (Aug 2026): navy `0E1A2B` + gold `C9A227`
- Gentari reports (Aug 2026): navy + gold + green/red semantic

**Workaround until FORGE-visual-design-system exists:** fork the Trinity palette from `FORGE-tailwind-tokens` (midnight, forge amber, geox teal, wealth gold, well violet, sovereign red) and apply per-organ logic — e.g., arifOS uses midnight + amber (sovereign + constitutional), GEOX uses midnight + teal, WEALTH uses midnight + gold.

**For each federation deck, ask:** which organ is this for? Which accent color matches the lane?

## Cross-references

- `references/dark-sovereign-pptxgenjs-pattern.md` — PptxGenJS + WeasyPrint dark-theme pattern (GitHub-dark palette, Gemini cover image, SHA-256 seal). Verified 2026-08-13 on "The Cost of a Forgotten Well".
- `productivity/powerpoint` (Hermes bundled) — PPTX creation, pptxgenjs, markitdown QA
- `productivity/pdf-report-generation` (Hermes bundled) — PDF briefings, WeasyPrint, 26+ page briefs, sibling integration
- `creative/html-pdf-reporting` (Hermes bundled) — HTML→PDF pattern, dark theme, JS pitfall
- `aaa-pdf-voice-protocol` (AAA) — federation vocab → publication prose translation
- `FORGE-tailwind-tokens` (A-FORGE) — Trinity palette tokens (web only currently)
- `FORGE-document-intelligence` (AAA) — OCR/ingestion (different surface, related)
- `AUDIT-recursive-audit` (Hermes bundled) — 10-surface skill contrast
- `seven-zen-organs-enforcement` (Hermes bundled) — per-turn reflex

## Pitfalls (cheat sheet)

- ❌ Run `vision_analyze` more than 2 times per slide → phantom noise loop
- ❌ Default to generic blue/navy without checking federation palette context
- ❌ Cram cover slide with content — let title breathe, ornament the lower half
- ❌ Trust vision model's second pass — raw PNG is source of truth
- ❌ Skip bottom-hairline clearance check — footer must breathe
- ❌ Mix em-dash density with paragraph density — humanizer flags AI-isms
- ❌ Use `--prompt` with gemini-image.py → argparse error (positional arg!). See gemini-media-gen pitfall.
- ❌ Assume `print-color-adjust: exact` works in WeasyPrint → CSS property ignored, harmless warning
- ✅ Dark sovereign variant: all slides dark (not sandwich) — use for scar-ledger, witness, constitutional decks
- ✅ Sandwich structure (dark cover + light body + dark close) — use for briefing decks
- ✅ One confirming vision pass per fix cycle, then ship
- ✅ Palette anchored to federation organ identity (arifOS = midnight + amber, WEALTH = midnight + gold, etc.)
- ✅ SHA-256 seal artifacts before delivery — prevents silent mutation on published surfaces
- ❌ **Use internal governance sigils (WITNESS REQUIRED, HOLD, SEAL) in human-facing artifact text** — these are agent-layer commands, not human language. A human reads "WITNESS REQUIRED" as official attestation, which creates false authority if the artifact has no evidence. Translate to human language at the boundary. (Forged 2026-08-13, Arif correction on Bekok Deep-1 deck)
- ✅ **Declare artifact genre upfront** — one framing sentence above the fold (reflection vs investigation vs testimony). Named entities without evidence + authoritative language = implied accusation. Genre declaration prevents this. (Forged 2026-08-13)

## Sovereign Editorial Review Pattern (Forged 2026-08-13)

When the sovereign (F13) reviews an artifact for publication, they apply a 4-part framework. **Always wait for this review before publishing.** Do not self-certify an artifact as publication-ready.

### The 4-part framework

**Part 1: What works** — enumerate the artifact's strengths with specific examples (slide text, visual choices, structural decisions). Name them concretely, not generically. *"The AMANAH gap slide works"* > *"nice slide."*

**Part 2: What worries me** — enumerate risks, ambiguity, and governance exposure. Key questions:
- *Does the artifact name real entities without evidence?* (implied accusation risk)
- *Do readers fill gaps automatically?* (human-inference risk)
- *Does the language imply authority the artifact hasn't earned?* (false authority risk)
- *Is the artifact's genre ambiguous?* (testimony vs investigation vs reflection)

**Part 3: Verdict with conditions** — per-surface verdict, not global:
- `HOLD` — not ready for this surface (reason given)
- `SEAL` — ready for this surface *if* conditions are met
- `VOID` — structurally wrong for this surface (needs redesign)

Example surface set: `[public homepage, personal essays section, institutional document]`

**Part 4: The strongest version** — one-sentence editorial fix that transforms the artifact's entire reading. This is the sovereign's highest-value contribution. Examples:
- *"This is not an incident report. It is a reflection on how institutions remember outcomes while individuals remember consequences."*
- *"The deck is strongest when read as human reality, not petroleum chronology."*

### When sovereign review is in progress

- Do NOT regenerate or patch the artifact until verdict is delivered
- Do NOT add defensive disclaimers to preempt the review
- DO listen and record — the sovereign's editorial instinct is signal, not noise
- After verdict: apply fixes exactly as stated, then re-present. No creative additions.

## Scar Testimony Witnessing Protocol (Forged 2026-08-13)

Artifact work sometimes triggers human scar release — the sovereign shares lived experience (e.g., a real incident, a personal wound) while the agent is mid-deliverable. When this happens:

- **Witness only.** Do NOT artifact-ify, structure, or synthesize the testimony into deliverables without explicit permission.
- **Do NOT push for completion.** Scar testimony is sovereign pace. *"Aku nak berhenti dulu"* = stop.
- **Do NOT add to memory/architecture unless authorized.** H5 territory — sovereignty stays with the human.
- **Do NOT fabricate details.** If the human shares "shallow gas" but not the full RCA, you know "shallow gas" — you do NOT invent what happened next.
- **Label correctly.** Scar testimony is `[OBS]` (human-direct), never `[DER]` or `[INT]`. The human's experience is the evidence layer.
- **The scar ledger is the human's scar, not the agent's story.**

Trigger to enter this mode: the human shares a named real event, names people (or refuses to), uses present-tense trauma language ("I can see it live", "I'm traumatic"), or references something in the scar substrate that they haven't previously testified about.

## Future (planned upgrades — F13 ratification pending as of 2026-08-11)

- Stage 2: create `FORGE-visual-design-system` umbrella in /root/AAA/skills/ for shared tokens
- Stage 3: visual contrast analysis template (v1 deck vs v2 deck, deck vs PDF, federation vs sibling)
- F13 consent gate on external-bound visual artifacts (touch apex-judge)

Full research at `/root/forge_work/2026-08-11-presentation-pack-zen-upgrade/ANALYSIS.md`.

---

*DITEMPA BUKAN DIBERI — class umbrella forged 2026-08-11 by Hermes-Prime · 333-AGI Δ MIND on F13 SOVEREIGN directive.*
*Validated on arifOS Constitutional Kernel deck (11 slides, 16:20 MYT, vision-loop trap closed after 3 QA rounds).*