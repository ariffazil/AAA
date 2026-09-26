---
name: forge-pdf-delivery
description: Turn markdown into a real PDF and deliver via MEDIA:. Never claim an attachment that was not built and verified.
capability_tier: fed-long-context
ecology_state: WARM
---

# forge-pdf-delivery

Class-level skill. Trigger: the user wants a portable document, not a chat reply. Examples: KWSP briefing for a friend, contract summary, research digest, weekly report, market brief. Trigger phrases: "bagi pdf", "buat pdf", "send me the PDF", "I need a doc on X".

## The one rule

**A file with the `.pdf` extension is NOT a PDF.** Always confirm via `file <path>` that the output shows `PDF document, version 1.7` (or similar) before delivering. If `file` returns `Unicode text`, you wrote text with a wrong extension — fix the pipeline, don't ship.

## Pipeline (use this exact order)

1. **Author content as Markdown.** One source of truth. Use proper headings (`##`, `###`), pipe-table syntax, lists — pandoc/weasyprint render them well.
2. **Build HTML.** Either:
   - Wrap markdown manually with a styled HTML template (recommended for design control).
   - Or `pandoc input.md -o output.html --standalone --metadata title="..."`.
3. **Render PDF.** `weasyprint input.html output.pdf` — local, no API call, renders tables / emoji / unicode (✅ ❌ ⚠️ ·) cleanly. Engine is at `/usr/local/bin/weasyprint`.

## Register whether the document is for reading or for showing — before you author

The pipeline above lets you do either; the trap is choosing the wrong one and producing a document the user didn't ask for. Distinguish at intake:

| Signal in the request | Track | Visual posture |
|---|---|---|
| "PDF biasa", "literature grade", "no fancy visual", "just for me to read", "deeper analysis", "dossier for myself", "Aku nak baca je", "no need fancy" | **Plain typography** | A4 portrait, serif body (Georgia / Times), 10–11pt, light page background, gold rule separators, no gradient stat cards, no colored severity chips |
| "PDF to impress", "pdf mode", "create a dossier for [third party]", "intelligence briefing", "dark theme", visual artifact needed | **Image-based pipeline** | A4 landscape, dark `#0a0a0f` background, gradient stat cards, RGB-coded severity, color-functional design (see `references/image-based-pdf-pipeline.md`) |

The plain track is the default for anything reading-oriented. The image-based track earns its weight when a third party will leaf through it on the screen and the document needs to read as "research product" — a dark dossier signals to the recipient that the principal has a research team.

**Pitfall:** skill defaults learned from fashion-mag-style past outputs can pull the agent toward the image-based track even when the user asked for the plain one. When in doubt, render plain first; the cost of a re-render to add visuals is small, the cost of a rejected "fancy" version is not. The user has been observed re-prompting with "No need fancy" after receiving an over-designed first pass — treat that re-prompt as a signal the plain track should have been picked at intake, not a refinement step.

**The plain-track is a default, not a fallback.** A user who reads a lot of their own material wants the document to disappear as a container, not to be a designed artifact. Resist the temptation to add visual hierarchy markers, color-coded chips, gradient cards, or iconography to "make it look better" — the user is reading the words, not the design. The right test for "is this too designed?" is: if you removed all visuals and kept only text, would the document lose meaning? If no, the visuals are decoration.

**Ask "panjang atau pendek" before building — don't default to exhaustive.** When the request is a "final pdf with visual cover page" or "comprehensive analysis," it sounds like the user wants the full treatment. They often don't. After building a 7-page comprehensive version and receiving "Panjang aku PON x mau baca" + "1-page quick version please," the lesson is: at intake, ask one short binary question — *long/detailed* vs *condensed/1-page* — and offer the condensed version as the first delivery, then build full as a follow-up if requested. The cost of an extra clarification is small; the cost of a rejected multi-page version is the user re-prompting in frustration ("buat pendek la"). When the user explicitly says they want depth (e.g., "deep research"), default to long; when they just say "PDF" without scope qualifier, ask or default to condensed.

Plain-track CSS skeleton (copy-paste-ready):

```css
@page { size: A4; margin: 18mm 16mm 18mm 16mm; @bottom-right { content: counter(page) " / " counter(pages); font-family: Helvetica, sans-serif; font-size: 9pt; color: #7a7a7a; } }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt; line-height: 1.45; color: #1c1c1c; }
h1 { font-family: Helvetica, sans-serif; font-size: 18pt; color: #0e0e0e; margin: 0 0 4mm 0; padding-bottom: 3mm; border-bottom: 1.5pt solid #a8884a; }
h2 { font-family: Helvetica, sans-serif; font-size: 13pt; color: #0e0e0e; margin: 8mm 0 3mm 0; }
h3 { font-family: Helvetica, sans-serif; font-size: 11pt; color: #5b5b5b; margin: 5mm 0 2mm 0; }
p { margin: 0 0 2.5mm 0; text-align: justify; }
table { width: 100%; border-collapse: collapse; margin: 3mm 0 4mm 0; font-size: 9.5pt; }
th { background: #0e0e0e; color: #f5f1e8; padding: 1.5mm 2mm; text-align: left; font-family: Helvetica, sans-serif; font-weight: 700; }
td { padding: 1.2mm 2mm; border-bottom: 0.5pt solid #d4d4d4; vertical-align: top; }
tr:nth-child(even) td { background: #f5f1e8; }
ul, ol { margin: 0 0 2.5mm 4mm; }
li { margin-bottom: 1mm; }
hr { border: 0; border-top: 0.5pt solid #c0c0c0; margin: 5mm 0; }
code { background: #f5f1e8; padding: 0.4mm 1.2mm; font-family: Menlo, Consolas, monospace; font-size: 9pt; }
blockquote { border-left: 3pt solid #a8884a; padding-left: 4mm; color: #5b5b5b; font-style: italic; margin: 2mm 0; }
```

Workflow:
1. Author content as Markdown (one source of truth).
2. `markdown.markdown(md, extensions=['tables','fenced_code'])` to convert.
3. Wrap with the skeleton above in HTML.
4. `HTML(string=full).write_pdf(out_pdf)`.
5. Verify with `file out.pdf` returning `PDF document, version 1.7`.
4. **Verify.** `file output.pdf` must return `PDF document, version 1.7`. If it returns `Unicode text`, start over from step 1 with the real content.
5. **Layout QA without a vision lane.** When the active model has no native vision (or `vision_analyze` returns no transcript), verify layout programmatically instead of eyeballing screenshots: `pdfinfo <file>.pdf | grep -E 'Pages|Page size'` — page count must match the number of designed `.page` blocks (a mismatch = overflow spilled an extra page) — then `pdftotext -f N -l N <file>.pdf - | head` per page to confirm each section landed in order with no truncation. `pdftoppm` still works for pixel-render smoke checks but the text-layer check is the reliable gate.

5b. **Browser-print engine gate.** If the PDF came from headless Chrome/Chromium (`--print-to-pdf`) or any HTML deck, the page-count check is the primary defect detector, and it fails silently. Full recipe: `references/browser-print-layout-gate.md`. Two recurring traps:
   - **Fixed-size slide divs + non-zero `@page` margin = every slide splits into two pages.** A `.slide { width:297mm; height:210mm }` under `@page { size: A4 landscape; margin: 1cm }` leaves only 277×190 mm printable, so each slide overflows and Chrome emits *two* pages per slide — title on one, figure on the next, plus a blank tail. A 12-slide deck silently became a 24-page PDF with four near-empty pages. Fix: `@page { margin: 0 }` (the deck supplies its own padding) or size the slide to the printable box.
   - **Browser furniture prints on every page** unless suppressed: render date/time, document title, and the raw `file:///` source path. Always pass `--no-pdf-header-footer`. Never ship a third-party deliverable carrying an internal filesystem path.

5c. **Ink-coverage sweep — the automated blank-page detector.** Counting pages is not enough; a page can be counted and still be empty.

```bash
pdftoppm -png -r 110 out.pdf /tmp/qa/page
python3 - <<'EOF'
import glob
from PIL import Image
for f in sorted(glob.glob('/tmp/qa/page-*.png')):
    im = Image.open(f).convert('L'); w,h = im.size; px = im.load()
    dark = tot = 0
    for y in range(0,h,3):
        for x in range(0,w,3):
            tot += 1
            if px[x,y] < 235: dark += 1
    print(f, f"{100*dark/tot:5.2f}%")
EOF
```

Healthy text-and-figure pages land ~4–25 %. Under ~2 % is a split or empty page; a wide spread (0.3 % beside 24 %) is the signature of a layout break, not of intentional design. Over ~60 % is a full-bleed cover — fine on screen, but it eats toner and its gradients band on paper, so flag it if the deliverable is meant to be printed.
6. **Copy to forge_work.** `cp output.pdf /root/AAA/forge_work/<date>-<slug>/<descriptive-name>.pdf` — durable location, not `/tmp`.
7. **Deliver.** Include `MEDIA:/absolute/path/to/file.pdf` in your Telegram reply. Hermes auto-attaches as a document.

## Carrying numbers in the deliverable — content gate (not layout)

The five checks above prove the file renders. They do **not** prove the document says what you think. When the deliverable carries monetary figures, invoices, ledgers, settlements or splits of any kind:

**One invoice per order.** A document that prints a prior settled payment alongside a new unpaid item, then subtracts one from the other to derive a "balance", manufactures a debt that did not exist in any contract. The recipient reads the resulting "balance due" as a claim. If a prior transaction belongs on the page at all, it sits in a separate EXCLUDED block with a status label (SETTLED / VOID / REFUNDED) and does not enter the arithmetic that decides what is owed. See `references/invoice-content-discipline.md` for the full rule set and the canonical "one order / one page" template.

**Lock the source on the original receipt, not on whichever party spoke last.** When two people describe the same transaction differently, the temptation is to revise the document after each speech act. Hold the record on its first source (a receipt photograph, a logged transfer, a confirmed reply) until that source is contradicted by a higher-warrant observation. Surface disagreements inside the document ("party A states X; party B states Y") instead of re-rendering. A fresh-looking PDF built on an unverified record is the same defect as a stale figure presented as current.

**Tag every line with its evidence class on the page itself.** When two readers can have read the same artifact and come away with different amounts, the artifact failed — not the readers. Print three classes inline, each with its own visual treatment: `VERIFIED` (printed on a receipt the user photographed), `REPORTED` (spoken by one of the parties), `DERIVED` (your arithmetic, every input labelled). Empty cells are the right answer for line items where no source exists — never a confident blank-style default.

## Pitfalls (read before authoring)

- **Pandoc CANNOT read PDFs.** `pandoc file.pdf -o out.html` errors with "Unknown input format pdf". The reverse direction (md → html → pdf) is the only valid flow.
- **Weasyprint unicode.** ✅ ❌ ⚠️ · (middle dot) — and Malay diacritics all render fine. If you see boxes/squares, install `fonts-noto-core`.
- **Tables.** Always pipe-table syntax in markdown. Don't lay out tables with spaces or hand-rolled HTML — pandoc/weasyprint will eat them.
- **Don't `cat << EOF > file.pdf`.** That writes text with a misleading extension. Use the pipeline.
- **Don't try to generate PDFs inside execute_code.** The sandbox doesn't ship matplotlib/weasyprint. Use `terminal` or write `/tmp/script.py` and run via `python3 /tmp/script.py`.
- **NEVER claim an attachment you did not build.** If a reply says "[PDF Attachment]" but no file was created and no `MEDIA:` path was included, that is fabrication — the user WILL call it out ("Tepek sini"). Recovery: build the real file via the pipeline above, deliver with `MEDIA:/abs/path.pdf`, and own the miss plainly in one line. The `file <path>` verify step exists precisely to gate this.
- **Simple one-pagers can use reportlab directly** (`from reportlab.pdfgen import canvas`) when the content is headings + bullets, no markdown source needed. Still verify with `file output.pdf` → `PDF document` and still deliver via `MEDIA:` with a durable path (forge_work), not `/tmp`.
- **"Redo / semua / complete / full expansion" → expand maximally, not selectively.** When the user re-prompts with "redo, jangan ikut list aku bagi, hang buat la list SEMUA!!!" or "include all" or "every one, not just what I named" the scope has changed from "respond to my list" to "give me everything in this category". Build the comprehensive version. Going from 7 archetypes → 80+ (Nusantara heroes, Malaysian icons, anti-heroes, villains, mythological, cinematic personalities, pop culture, quantum superposition) is what "ALL" means in this register. Treat "redo" as trigger to identify the natural category boundary, then enumerate inside it. The user is signalling: don't gate-keep what counts. The expanded version comes AFTER the user complains, never preemptively as the first answer — wait for their signal.
- **User's first "X not Y" read of scope is the trigger to ask, not to comply.** When the user lists 7 archetypes and then says "Grindelwald, Dumbledore, Bang Non PMx, CEO PETRONAS. SEMUA" — they have realised the list is too narrow. Don't ask "do you mean only those 4 or wider?" — the word SEMUA and ALL means wider. Build the wider version.
- **Read every source PDF BEFORE the first draft, not after the rejection.** When the request is grounded in real-world documents attached in the same conversation (a syllabus, a policy PDF, a regulation, a personal file), the failure shape is `v1 (drafted from inference) → user attaches the actual doc → v2 (rebuilds with corrected facts) → user adds more context → v3 → v4`. The cost is the user's full attention budget across four turns. The fix is at intake: when the request lands, list every attachment and read the load-bearing ones first. Three PDFs in, the marginal cost of reading them is one extra `pdftotext` call; the cost of four wrong drafts is the user's time. If a follow-up document arrives mid-build (the user attaches the actual policy after the first guide is sent), treat it as the canonical source and rebuild from it — even if v1 was approved, it is wrong by definition once the source it ignored is in evidence.
- **Match intake depth to decision urgency, not to the agent's instinct for completeness.** A "pick one of three options" decision does not warrant a five-question introspective intake. The failure shape is "5 deep questions + wait for answers + 4 versions of the answer" when one tiebreaker and a recommendation would have closed the loop in two turns. When the user asks "what should X take?" and X must decide soon, give a decision frame and a recommended pick first; offer the deeper self-reflection only on request.
- **When the user states a fact in casual form ("masuk tahun 2 lAAAA", "today la", "ASAP"), it is not less authoritative than formal form — it is often a correction.** Lower register signals "I'm correcting your prior assumption" more often than it signals "I'm just being casual." Default: the user's latest stated fact wins, even when it contradicts an inference made from earlier context. The prior artifact scoped to the wrong timeline is wrong by definition; rebuild it.
- **External-facing deliverables need multi-page vision verification, not single-page.** When the artifact will be posted publicly or sent to a third party (a friend's brief, a social-media draft, a dossier for someone else), defects amplify. Single-page vision checks (cover + last page only) caught defects in v1 of the same artifact that v2 caught only after rendering every page. The pattern is: (i) generate full PDF, (ii) render every page to PNG, (iii) vision-verify cover + every region that carries source-quoted material + every region that carries user-specific facts + last page, (iv) patch any defects, (v) re-render. Two defects per artifact is the rule, not the exception. The cost of one extra `vision_analyze` per page is small; the cost of a typo reaching a public post is the user's standing.
- **Never elevate inference to stated fact when source material only implies.** When the source document says "umur dia (ayah) tak panjang, kami berpisah" — the death of a parent is a strong but unspoken implication. Writing "Ayah Meninggal" as a header, or "sebab ayah meninggal" as causal fact, elevates a reader's interpretation into a sourced claim. The defect survives every prose revision, but it shows up the moment the document reaches a reader who goes back to the primary. Use source-faithful paraphrase ("Kehilangan Ayah" instead of "Ayah Meninggal") and label the inference explicitly: `[per quoted source: "tak panjang, kami berpisah"]`. The label is cheap; the fix is to swap the word, not to argue about whether the inference was right.
- **`@username` in HTML breaks via hyphenation.** Markdown's `@khairulaming` triggers a silent unicode-aware line break inside the string when rendered through WeasyPrint, producing `@khairulam-ing` in the PDF. Defensive fix: write `&commat;khairulaming` (HTML entity) inside HTML strings, or run the handle through the full-wrap step only after escaping. Verify on every cover/footer that handles survive.
- **T2I models corrupt title text — even short words.** `qwen-image-plus` rendered "SABTU HAK KAU" as "SABU HAK KAU" (lost the `T`), and "SABU" reads as a Malaysian word for methamphetamine. That one letter change turns a poster for a sick day into something that gets the image flagged, taken down, or reported. For any deliverable whose title carries meaning, render the text via matplotlib / WeasyPrint instead of leaving it to the diffusion model — text-heavy posters are text artifacts, not mood imagery. The routing rule in this skill ("Text-bearing artifact → render deterministically") is the same rule restated here for posters specifically.

## Text-Bearing Artifact Routing (F13 ratified 2026-09-24)

The skill enforces one routing rule for any artifact where exact text matters:

1. **Text-bearing artifact (logo, poster, dokumen, infografik, artifact gaya-chat)** → render deterministically. Use this pipeline (`weasyprint`, `google-chrome --headless`, `pandoc`, or `reportlab` as documented above). Never call a generative image model (`image-01`, `minimax-image-gen`, `qwen-image`, etc.) for an artifact whose value depends on the literal text it carries.
2. **Generative image model** → only for content without text: mood, tekstur, cahaya, pemandangan. Treat any text the model emits as decorative, never authoritative.
3. **Gate before claim:** when the deliverable carries text, verify via text-layer (`pdftotext -f N -l N <file>.pdf -`) not model eyes. If the text-layer check is missing or wrong, the artifact is not built — fix and re-render.

Why: diffusion text-to-image reliably corrupts spelling, fabricates plausible-looking gibberish, and inserts phantom glyphs/watermarks. The class is structural, not a model/tune defect. Read-side `poster-vision-extraction` (SCAR 2026-08-27) already forbids fill-from-memory on visual reads; this rule is the write-side mirror.

Scope: this routing rule does not change the engine, the toolchain, or any code path. It routes existing artifacts to the deterministic renderer that already shipped here. No new skill, no new MCP, no new API call.

Companion reference: `domains/general/workshop/creative-design/civic-social-infographic/SKILL.md` — same routing applied to civic posters and infographics (HTML+CSS → Chrome headless → PNG, never image-gen).

## Companion pattern

For live market data charts that get delivered the same way (PNG image via MEDIA:), see `forge-finance-chart-delivery` — same verify-then-deliver discipline, same forge_work destination convention.

For PDF + multi-image infographic bundles (timeline + checklist + chart), see `references/infographic-image-companion.md` — matplotlib pipeline proven for Malaysian biohacking/competition guides.

For image-based magazine-style PDFs (custom layout per page, dark themes, callout boxes, code-switching typography), see `references/image-based-pdf-pipeline.md`. Read it before attempting multi-page visual PDFs — the pitfalls there (matplotlib text truncation, AI cover text artifacts, unicode glyph missing, vision-only verification) cost several re-renders each time.