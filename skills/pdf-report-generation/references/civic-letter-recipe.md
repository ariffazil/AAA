# Civic Letter Recipe — Soul-First / Magnitude-Visualized (proven 2026-08-12)

For "surat terbuka", "BIG BANG" civic dispatches, letters from F13 SOVEREIGN
to Parliament, regulators, or public bodies. Different from both the
chart-heavy SOVEREIGN brief AND the formal corporate letter.

## When to use
- "Surat terbuka" / "BIG BANG" / "letter that grabs attention" / "with soul of MakcikGPT"
- Open letters where the writer's SURVIVAL depends on the letter being HEARD
- When the human has expressed hate / frustration / "cannot sleep" / "by hook or by crook" about the target
- When the external audit caught multiple kill shots (factual, structural, rhetorical) — this is the rebuild recipe

## When NOT to use
- Chart-heavy data reports (use the main SKILL.md)
- Formal corporate letters to known recipients with no emotional weight (use `letter-format-pdf-recipe.md` instead)

## The Iteration Cycle (encoded from the 2026-08-12 session)

The user will often correct approach TWICE in the same session. Encode this:

| Round | User direction | Recipe |
|---|---|---|
| **v1 (first instinct)** | Default: data dump + tables + named-philosophy framing | ❌ REJECTED — "too full of data and numbers" |
| **v2 (after first correction)** | Soul-first, Marhaen voice, single request, NO tables | ✅ PASS for prose — but user then asks for math back |
| **v3 (after second correction)** | Soul-first prose + magnitude-visualized charts (5 chart pack) | ✅ FINAL |

**Lesson:** "Humble soul" ≠ "no math". "Humble soul" = "math made visceral via visualization". Use dual-line charts where SHOULD-MOVE-TOGETHER but DON'T — that's the magnitude of betrayal. Use pie/bar where SHOULD-BE-ENOUGH but ISN'T. Use named-chair maps where amanah was given vs where it was broken.

## Recipe: Soul-First Civic Letter (prose)

**Voice register:** Makcik/Marhaen. Ordinary citizen speaking UP to power. Bahasa Melayu Penang — short sentences, single observation per paragraph. NEVER use AI jargon, federation-internal labels (F1-F13 codes, "888 JUDGE"), or "Artificial Superintelligence" in the document itself.

**Font stack (different from formal letter):**
```css
body { font-family: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif; }
h1, h2, .lede, .the-number { font-family: "DM Serif Display", Georgia, serif; }
.kicker, .lab { font-family: "IBM Plex Mono", monospace; }
```
Sans-serif body reads MODERN and HUMAN. Serif headlines carry gravitas without corporate stiffness. Mono for the verification hash and metadata labels.

**Margins:** `@page { margin: 16mm 16mm 20mm 16mm; }` — slightly tighter than formal letters because civic letters are meant to be SCANNED, not studied.

**Structure (target ~800-1200 words prose, 5-7 visualizations):**

1. **Cover** — cover image (warm, humble, human — see Image prompts below), with overlay title in 3 short phrases: "Tiga Kerusi. / Tiga Amanah. / Satu Pengkhianatan." + meta block (Kepada/Daripada/Tarikh/Rujukan)
2. **Opening** (300-400 words) — ONE observation, ONE number, ONE moment. The reader stops here or doesn't stop at all.
3. **Visualization 1** — The dual-line magnitude chart (e.g. PAT vs Dividend, SHOULD-MOVE-TOGETHER but DON'T). Title: "Amanah vs Realiti".
4. **Visualization 2** — The proportional magnitude (e.g. RM100 broken into "AMANAH DIPATUHI 45%" vs "AMANAH DIKHINATI 70.5%" side-by-side).
5. **Three kerusi** (300-400 words) — named individuals, what amanah they were given, how they betrayed it. With Visualization 3 (the chair map: each kerusi paired with its amanah and its dikhianati).
6. **Visualization 4** — The cost magnitude (e.g. RM350M F1 vs 5,000 keluarga dibuang kerja). Side-by-side, both with magnitude comparator (=X× gaji purata, =X families affected).
7. **Visualization 5** — The heartbeat / pacemakers chart (the trajectory with threshold + breach annotated). This visualizes the federation's own watchful presence.
8. **Single request** (one black box, ~150 words) — ONE ask. Must be specific, measurable, must NOT require anyone to be fired. Must be impossible to refuse without looking guilty.
9. **Closing** (~100 words) — the humble civilization paradox: "Tamadun yang humble membina menara yang tidak humble, dan menara itu mengambil dari tamadun yang membinanya."
10. **Signature** — name as "Seorang Warganegara Malaysia" (NOT real name, per "BULLDOZE PROTECTION"), date, sources cited cleanly, hash block.

## The 5-Visualization Magnitude Pack (recipe)

When the user says "math visualized with full clarity and meaning magnitude" — generate this exact pack:

1. **Dual-line magnitude** (matplotlib): two lines that SHOULD-MOVE-TOGETHER but DON'T. Fill the "khianat zone" between them in red. Annotate the FY2025 breach with a bidirectional arrow + "RM13.4B didn't reach the nation".
2. **Proportional comparator** (matplotlib `FancyBboxPatch`): side-by-side "AMANAH DIPATUHI 45%" green panel vs "AMANAH DIKHINATI 70.5%" red panel. Both showing the same RM100 broken down.
3. **Three-kerusi map** (matplotlib `Wedge` for chairs, `FancyBboxPatch` for cards): one chair per named individual. Below each chair: left card "AMANAH [given]", right card "DIKHINATI [violated]". Tie this to the cover image's humility theme.
4. **Cost comparator** (matplotlib, no axes): what the KEPT item costs vs what was CUT. Annotate each with a magnitude comparator ("=7,000× gaji purata" or "=20,000 keluarga tanpa sumber").
5. **Heartbeat / pacemakers** (matplotlib, line chart): the trajectory of the binding metric across years. Mark the threshold line + breach event + the federation's pacemaker trigger that fired.

**Color palette:**
- AMANAH = `#c9a227` (gold — trust given)
- KHIANAT = `#a93226` (dark red — trust broken)
- NAVY = `#1a2536` (institutional dark)
- WARM = `#8b6f3d` (deep amber)
- CREAM = `#faf6e8` (paper warmth)
- PAPER = `#fffefb` (background, NOT pure white)

**Title grammar:** every chart title ends with the magnitude word. Not "Chart 1". "Amanah vs Realiti." Not "Chart 4". "Di Mana Duit Itu Sebenarnya Boleh Pergi."

## Cover Image Prompt (Gemini Pro, for the soul)

Use this template:
> "A photorealistic intimate close-up: a weathered Malaysian hand (older, kind) holding a single sheet of white paper with [KEY NUMBER]% printed on it, the paper is creased from being folded many times. The hand rests on a plain kitchen table. Beside the hand, a [TEH TARIK / half-finished cup], a small pair of reading glasses placed aside. Warm golden afternoon light streams through a window, casting long shadows. In the soft-focused background through the window, the silhouette of [OIL REFINERY / relevant institutional context]. The mood is one of ordinary dignity facing extraordinary weight. The hand is steady but the paper trembles slightly. 4K, shallow depth of field, warm tones."

Generate via `python3 /root/HERMES/scripts/gemini-image.py "[prompt]" --model gemini-3-pro-image`.

Vision-verify the cover BEFORE embedding. Common defects: (a) text in image is mirrored (refraction through droplet), (b) body text on paper is garbled, (c) mood too dark/noir. The mood must be HUMBLE, not dark.

## Crypto Signoff (FIXED — the 2026-08-12 correction)

The OLD signoff block from `letter-format-pdf-recipe.md` had 3 defects that an external audit caught. The FIXED version:

```html
<div class="sign">
  <div class="name">Seorang Warganegara Malaysia</div>
  <div>Yang membayar cukai. Yang mengundi. Yang menunggu jawapan.</div>
  <div class="meta">
    <span class="lab">Tarikh:</span> 12 Ogos 2026 &nbsp;·&nbsp;
    <span class="lab">Rujukan:</span> AMANAH-DIKHIANATI/2026-08-12<br>
    <span class="lab">Sumber data:</span> Laporan Tahunan Bersepadu PETRONAS FY2020–FY2025 (KPMG PLT) · audit bebas luaran<br>
    <span class="lab">Nombor yang dibuktikan:</span> RM32B ÷ RM45.4B = 70.48% (FY2025) · Lonjakan dari 58.1% (FY2024) = +12.4 mata peratus
  </div>
  <div class="hash" id="doc-hash">SHA-256: [SOURCE HTML HASH, see below]</div>
</div>
```

**What was removed (the 3 kill shots):**
- ❌ "Agent: Hermes Artificial Superintelligence (ASI)" → alienates MPs reading at 9am. Drop entirely.
- ❌ "Source Repository: https://github.com/arif-fazil/arifos" → de-anonymizes. Drop entirely.
- ❌ "F2 (TRUTH) binding: All data sourced from audited public reports" → LIE if any factual error exists. Drop entirely.

**What was kept:**
- ✅ Date + rujukan (procedural identity)
- ✅ Source data (audited reports cited specifically)
- ✅ Verified single key number with arithmetic proof shown
- ✅ Hash block (but see self-referential handling below)

## Self-Referential Hash Handling (Kleene's fixed-point)

**Problem:** If you embed the SHA-256 of the rendered PDF in the document, then re-render, the file hash CHANGES (because the embedded hash is now different content). Chicken-and-egg. The displayed hash can NEVER match the file hash for a single-file self-referential embed.

**Solution (proven 2026-08-12):**

1. Compute the SHA-256 of the SOURCE HTML (with the placeholder text, before patch).
2. Patch the HTML to embed THAT source HTML hash.
3. Re-render the PDF.
4. Both hashes are now stable:
   - **Source HTML SHA-256** = `7be88a81...` (verifiable against published source)
   - **Rendered PDF SHA-256** = `8f948da8...` (the file actually distributed)

5. Note both hashes in the delivery message. The displayed hash in the PDF is the SOURCE hash; the FILE hash is separately disclosed.

This satisfies the cryptographic intent (anyone with the source HTML can verify the embedded hash matches) without the impossibility of self-reference.

```python
# Compute source HTML hash (with placeholder)
import hashlib
source_hash = hashlib.sha256(open('letter.html', 'rb').read()).hexdigest()
# Patch into HTML, then re-render
html = open('letter.html').read().replace('SHA-256: PLACEHOLDER', f'SHA-256: {source_hash}')
open('letter.html', 'w').write(html)
# Render
weasyprint.HTML(string=html, base_url='./').write_pdf('out.pdf')
# Both hashes stable now. Note them separately.
```

## Apex-Judge Isolation Step (T2+ civic dispatches)

For any T3 civic letter going to Parliament, regulators, or media:
1. Build the artifact first
2. Compute both hashes
3. Build evidence package (doer, candidate, action-class, tier, reversibility, blast-radius, sovereign_signal)
4. `apex-judge isolate --critical --pretty --human`
5. Expect `F13_REQUIRED` verdict with `AWAIT_INPUT`
6. **Do not seal to VAULT999 unless F13 explicitly approves.** The receipt's `effective_verdict` is the authority — quote it verbatim per the apex-judge skill's parent_may_only contract.

## The 5 External-Audit Kill Shots to Defend Against

When a sibling/external auditor (Claude, Apex, human) reviews the civic letter, expect these 5 attacks:

1. **Factual inaccuracy** in any comparison (e.g. Shell/BP — they actually DID lay off workers, opposite of claim)
2. **Baseline shopping** (measuring from peak instead of from appointment to dramatize decline)
3. **Rhetorical parallels** (any "exploitation pattern" / "taking from people" / "extraction" language reads as sexual violence or Israel/Palestine to a parliamentary reader)
4. **Legal exposure** (defamation — naming 4 living individuals with imputations, especially when one comparison contains an error that nullifies the qualified privilege defense)
5. **Crypto signoff de-anonymization** (github URL + agent label + "pending seal" in the signoff)

For each kill shot, the recipe:
1. Live-verify the fact (don't trust your own memory, search the source)
2. Measure from appointment year, not peak
3. REMOVE the parallel section entirely — it cannot be salvaged
4. Either drop the names (only target the institution via PAC) or qualify with `[F13 1-hour lawyer consultation]`
5. Replace github URL with `[SOURCE: arif-fazil.com/world/propa/]` (or just remove); remove ASI label; remove "pending" language; ensure displayed hash matches source HTML (Kleene's fix above)

## Pitfalls

- **Don't dump data.** The user will reject "too full of data and numbers" — even if the data is correct. Lead with the soul, then add the magnitude visualizations.
- **Don't paraphrase Section 4 / exploitation parallels.** Remove entirely. They are the strongest rhetorical move but also the biggest legal exposure. Save the parallel for ONE opponent in private, never for Parliament.
- **Don't put "Artificial Superintelligence" in a document going to Parliament.** MP assistants will discard the letter at 9am if it reads as a manifesto. Just say "Saya warganegara yang prihatin" — that's the universal MP-passable voice.
- **Don't apologize for length.** A 8-page civic letter is acceptable. A 17-page chart-heavy brief is acceptable. A 30-page letter is a red flag.
- **Don't skip apex-judge.** For T3 dispatches, the kernel verdict is NECESSARY but not SUFFICIENT. Get the receipt before sending. Quote `effective_verdict + session_id + call_hash` per the apex-judge skill.
- **Don't promise what you can't verify.** If a number came from your training data, label it `[DER]` and disclose the chain of derivation. If a name is in your draft but you're not sure about its committee assignment, drop the name or qualify.
- **Don't use "tapi" or "namun" excessively** — Bahasa Melayu paragraphs that constantly negate feel defensive. Use positive framing where possible ("tamadun yang humble membina menara" not "tamadun yang humble TIDAK membina menara").
- **The closing question must NOT be rhetorical.** The "Soalan terakhir" at the end must be a question that has a YES answer the reader can sign onto. "Boleh Parlimen lulus akta untuk melindungi duit rakyat?" — yes, obviously. That's the move.