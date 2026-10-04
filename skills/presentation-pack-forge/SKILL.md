---
name: presentation-pack-forge
description: "Orchestrate a complete presentation pack — pptx deck + companion PDF + hero image + sealed delivery receipt — under one entry point. Routes to the right skills (powerpoint, pdf-report-generation, ai-media-generation-ops, FORGE-komda-color-law, notebooklm-bridge, humanizer), enforces Komda color law pre-render, runs the codified QA loop, seals with sha256 + DELIVERY.md, and delivers via Telegram MEDIA. Triggers on 'deck about X', 'slides for board', 'presentation pack on X', 'buat slide', 'pitch deck', 'rebrand deck'. Class-level umbrella — supersedes manual orchestration across 4-5 individual skills."
license: Proprietary
platforms: [linux, mac, windows]
---

# Presentation Pack Forge

The orchestrator for "presentation pack" deliveries. Before this skill existed, building a single deck required loading `powerpoint` + `pdf-report-generation` + `ai-media-generation-ops` + `FORGE-komda-color-law` + `notebooklm-bridge` manually, running Komda lint from memory, and inventing the QA loop ad-hoc. Three of those steps were easy to forget, and one (Komda lint) was skipped on 2026-08-11, shipping an arifOS deck in wealth-territory gold.

This skill is the single entry point. It routes, enforces, runs QA, seals, and delivers.

## Quick reference — what co-skill to load for each signal

| Topic signal | Primary skill | Co-load | Why |
|---|---|---|---|
| "deck on X" (general) | `powerpoint` | `humanizer` if prose-heavy | Text humanization before sealing |
| "deck on X" + data-rich | `powerpoint` | `pdf-report-generation` | Companion report with KPI hero + appendix tables |
| "deck on X" + federation territory in filename | `powerpoint` | `FORGE-komda-color-law` | Auto-lint pre-render, fail-close on territory violation |
| "deck on X" + canon source exists | `powerpoint` | `notebooklm-bridge` | Source-grounded outline via `nlm_create_notebook(file_sources=[...])` |
| "deck on X" + cover hero image needed | `powerpoint` | `ai-media-generation-ops` | `gemini-image.py` (PRO) or MiniMax MCP fallback |
| "deck on X" + federation branding medallion | `powerpoint` | `ai-media-generation-ops` § Federation branding | Tactile medallion aesthetic, lane accent colors |
| "PDF report on X" (text-heavy, not slides) | `pdf-report-generation` | — | Direct WeasyPrint pipeline |

## The 7-step forge pipeline

### Step 1 — Territory auto-detect (if applicable)

```bash
case "$deck_filename" in
  arifos*|arifOS*) TERRITORY=arifos ;;
  wealth*)         TERRITORY=wealth ;;
  geox*)           TERRITORY=geox ;;
  well*)           TERRITORY=well ;;
  aaa*)            TERRITORY=aaa ;;
  *)               TERRITORY="" ;;  # no territory claim — skip lint
esac
```

### Step 2 — Komda lint pre-render (only if territory detected)

```bash
if [ -n "$TERRITORY" ]; then
  /root/arif-fazil.com/scripts/lint-komda-colors.sh "$deck_path" --warn-only
  # Note: --gate requires sovereign word (F13), do not promote silently
fi
```

If lint reports foreign-family violations on territory, either (a) re-color to the closed palette per `FORGE-komda-color-law` § Territory Tokens, or (b) HOLD for sovereign ack (F9 ANTIHANTU risk).

### Step 3 — Render pptx

Build with pptxgenjs (Node) or python-pptx (Python). See `powerpoint` skill SKILL.md § Creating from Scratch + `pptxgenjs.md` reference.

### Step 4 — Render PDF + extract images for QA

```bash
soffice --headless --convert-to pdf "$deck_path" "$deck_name.pdf"
pdftoppm -jpeg -r 110 "$deck_name.pdf" slide
```

### Step 5 — Codified QA loop (see `scripts/deck_qa.py`)

The QA loop is `render → pdftoppm → vision_analyze per slide → fix → re-verify → ship`. See `scripts/deck_qa.py` for the runnable version. Key pitfalls to look for:

1. **Komda color violations** — even after lint, visual confirm
2. **Mono font letter-spacing artifacts** at narrow widths (e.g., "arif_m e m ory")
3. **Italic Calibri + special chars** glyph loss (e.g., "Hem es routes" Hermes)
4. **soffice → PowerPoint line-break drift** — short phrases only
5. **Vertical alignment** of bullets in panels (top-align, not center)
6. **Panel border consistency** (both panels should have borders if either does)
7. **Connector arrows positioned in gaps**, not inside boxes
8. **Color differentiation** between cards (333-AGI vs 777-FORGE amber clash)
9. **Footer contrast** on cover/title slides
10. **Empty whitespace** in panels (panels should reach to bottom or be filled)

See `references/deck-render-pitfalls-2026-08-11.md` for the live bug catalog.

### Step 6 — Companion PDF (if data-rich)

When the deck topic is data-rich (numbers, charts, scenarios), build a companion PDF via `pdf-report-generation` skill. Same QA loop applies (page sweep + vision_analyze + full-page sweep before SEAL per `pdf-report-generation` SKILL.md § "Verifying a rendered PDF").

### Step 7 — Seal + deliver

Seal = sha256 + DELIVERY.md + append `_delivery_ledger.jsonl` + Telegram MEDIA.

```bash
# Compute sha256
sha256sum "$deck_path" "$deck_pdf" > SHA256SUMS

# Write DELIVERY.md (template under templates/DELIVERY.md)
# Append ledger entry
printf '{"ts":"%s","artifact":"%s","sha256_pptx":"%s","sha256_pdf":"%s","topic":"%s","status":"SEALED"}\n' \
  "$(date -Iseconds)" "$deck_path" \
  "$(sha256sum "$deck_path" | awk '{print $1}')" \
  "$(sha256sum "$deck_pdf" | awk '{print $1}')" \
  "$topic" >> /root/forge_work/_delivery_ledger.jsonl

# Deliver via Telegram
# Reply must include: MEDIA:/abs/path/to/file.pptx
```

## Step 0 (NEW 2026-08-13) — Framing Check

Before any deck references a real entity (named well, person, company), declare
its type. See `references/framing-discipline.md`.

```
FRAMING DECLARATION:
  Artefact type: [reflection | investigation | testimony | pitch | briefing]
  Real entities named: [list, or "none — archetypes only"]
  Evidence chain: [yes — sources/OBS-DER-INT | no — universal philosophy]
  Language authority: [WITNESS/ATTEST/SEAL | REFLECTION/PRINCIPLE | NEUTRAL]

  IF real entities + no evidence + WITNESS language → STOP. Reframe as reflection
  OR add evidence chain. "WITNESS REQUIRED" without evidence = implied accusation.
```

**Boundary Vocabulary Scan (mandatory, Step 0b):**
Scan the entire artifact for internal governance sigils before delivery:
- `WITNESS REQUIRED` → remove or replace with human-language tagline
- `HOLD` in non-agent context → replace with "A question left open"
- `SEAL` / `888` / `arifOS` / `SCT` / `AMANAH` → remove or translate to plain language
- Any term that would be meaningless or misleading to a non-agent reader

If any hit → STOP. Translate before continuing to Step 1.
See `references/framing-discipline.md` § Boundary Vocabulary Translation.

## Files

| File | Purpose |
|---|---|
| `scripts/deck_qa.py` | Codified QA loop — convert → vision batch → issue list. Run before declaring success. |
| `references/deck-render-pitfalls-2026-08-11.md` | The 3 LibreOffice/pptxgenjs pitfalls with fixes, learned live on the arifOS deck. |
| `references/komda-territory-palette-table.md` | Closed palette per territory — quick reference for new decks. |
| `references/framing-discipline.md` | Authority-without-evidence trap + framing sentence discipline + reality bridge test. |
| `templates/DELIVERY.md` | Sealed-delivery manifest boilerplate. |
| `templates/pres-pack-forge-checklist.md` | Pre-flight checklist for any "deck on X" request. |

## Out of scope (don't try via this skill)

- Live-site edits (use `arif-fazil-web-ops` / `arif-fazil-site-ops`)
- Internal audit reports (use `pdf-report-generation` directly)
- Open letters / civic intelligence (use `civic-advocacy` + `pdf-report-generation`)
- Charts-only / matplotlib batch (use `pdf-report-generation` + `html-pdf-reporting`)

## Reversibility

This skill is F1 AMANAH-compliant. Skill deletion = reverse-remove from profile skill dir; no production state mutated. The `_delivery_ledger.jsonl` ledger is append-only — skill removal does NOT remove past seals.

## When NOT to use

- The user wants to edit an EXISTING pptx file with surgical changes (use `powerpoint` skill directly + `editing.md` reference)
- The user wants a single quick chart, not a deck
- The user is iterating on a specific slide and doesn't want a fresh forge (use `powerpoint` directly)

## Pitfall — invented narrative around a named real entity (2026-08-13, Bekok Deep-1)

When forging a deck/PDF that anchors to a **named real well, incident, person, or scar**, do NOT manufacture the EVENT → DECISION → OUTCOME → RCA chain to fill a narrative gap. The test artifact "The Cost of a Forgotten Well" used `BEKOK DEEP-1` (a real PCSB well) with fully-invented pressure-anomaly / operator-bypass / RCA-unconfirmed content. The sovereign corrected: *"Bekok Deep-1 is real. You just told me: 'it was a real well btw'. That changes everything."*

**Three checks before shipping any artifact built on a named real entity:**

1. **Reconcile registry metadata against live public record.** The scar registry can carry unreconciled dates. Bekok Deep-1 example: registry said `27 Mar 2023 spud`; public record said `drilled May 2024, discovery announced Aug 2024`. The Bekok-A gas leak (4 Apr 2023) was a separate platform event. Web-search the entity first; if public record contradicts the framing, stop.
2. **If the entity is `HOLD` / `RESTRICTED` / `awaiting F13 sovereign narrative testimony`, do NOT generate the narrative.** The correct deck content is *the fact of the gap itself*, not a manufactured chain. Use framing like *"a well I was involved with. A scar I carry. The details are not ready to share."*
3. **If a single framing sentence changes the reader's whole frame, add it above the download button.** Proven rescue: *"This is not an incident report. It is a reflection on how institutions remember outcomes while individuals remember consequences."* Without it, an artifact built on a named real entity reads as implied attestation (F2/F9 risk). With it, the same artifact becomes an explicit reflection anchored in lived experience — publishable.

**Empathy override.** If the sovereign reveals trauma mid-session (e.g. "they said the well collide? wtf. I'm geologist. it's shallow gas duhhh" → "I can see it live" → "I'm traumatic. But I was roped in post blowout to help the official team. But the moment nobody cares to listen. Fuck off I quit the team"), STOP artifact work entirely. The next correct move is a plain human check ("hang ok tak sekarang?"), not any further governance, floor analysis, or skill housekeeping. The deck/PDF is not the priority anymore. The person is.

*DITEMPA BUKAN DIBERI — the orchestrator that enforces the law, runs the QA loop, seals the artifact, delivers via Telegram.*