---
name: intelligence-briefing
description: "Use when asked for a briefing — news scan, executive weekly, institutional-disclosure deep-dive, federation weekly review, live professional read, or political read."
version: 2.0.0
tier: canonical
authority: F13 sovereign in-chat order 2026-09-19 ("One capability, fifteen costumes")
merged_from:
  - executive-intelligence-briefing
  - intelligence-brief-forge
  - weekly-federation-deep-brief
  - professional-intelligence-briefing
  - political-intelligence-briefing
  - news-research-briefing
triggers:
  #
capability_tier: fed-agent-subagent
ecology_state: WARM
--- executive-intelligence-briefing ---
  - "news briefing"
  - "executive brief"
  - "weekly report"
  - "intelligence brief"
  - "tersurat dan tersirat"
  - "what happened this week"
  - "sum up the news"
  - "briefing on [country/topic]"
  - "apa bend bangang"
  - "apa X buat"
  - "wow me"
  - "deep research mode"
  # --- intelligence-brief-forge ---
  - "deep dive on [institution] [disclosure]"
  - "what's the void / what's missing"
  - "striking contrast"
  - forwards URL of corporate/regulatory disclosure asking for analysis
  - "sovereign intelligence brief with visual artifacts"
  # --- weekly-federation-deep-brief ---
  - "weekly brief"
  - "week in review"
  - "federation review"
  - "weekly summary"
  - "7-day report"
  - "weekly deep brief"
  - "W27 brief"
  # --- professional-intelligence-briefing ---
  - "siapa X"
  - "apa reality X sekarang"
  - "bila Y"
  - "bagi data kat dia"
  - "raja tanya"
  - "hang ada data X"
  - "Hermes ASI sila bagi nasihat"
  - "social fabric"
  - "apa yang bakar"
  - "what's brewing"
  - "rakyat"
  - "activate wealth intelligence"
  - "activate geox intelligence"
  - "activate [organ] intelligence"
  - "tell me everything about X"
  - "wow him/her"
  - "impress"
  - "tunjuk kau tahu"
  - "bagi nasihat kat dia"
  - "brief him"
  - "pdf mode"
  - "create a dossier"
  - "buat document"
  - "cakap tts"
  - "hantar voice note"
  - "explain kat dia guna suara"
  - "evaluate this pricing"
  - "review this menu"
  - "is this good for X market"
  - "u missed the biggest shadow"
  - "X is the shadow"
  - "what's in Corporate & Others?"
  - Arif is with someone and needs instant domain intelligence
  # --- political-intelligence-briefing ---
  - "political intelligence"
  - "catch me up on politics"
  - "what's going on in politics"
  - "who's winning"
  - "so what does this mean"
  # --- news-research-briefing ---
  - "executive briefing"
  - "what's happening"
  - "catch me up"
  - "today's news"
  - "what do I need to know"
  - "tell me everything about"
  - "so what"
---

# Intelligence Briefing — Canonical Briefing Engine

One capability. Six costumes. Every mode below is a **named output mode of the same
engine** — the briefing discipline (evidence tags, sourcing law, tone law, refusal
cases) is shared; only the structure, length target and delivery channel differ.

This file replaces six prior skills. See **Mapping Table** at the end for
old-name → new-skill+mode, and the retired originals at
`/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/intel-briefing/`.

## Mode Selector

| Mode | Name | Use when | Primary output |
|---|---|---|---|
| **A** | `executive-intelligence` | news/current-events brief on a country / domain / topic, weekly or ad-hoc, with surface + subtext and named critical segments | designed dark-theme PDF (chat summary after) |
| **B** | `institutional-disclosure` | deep-dive on a **disclosure artifact** — corporate earnings, IFR, regulatory filing, official statement, policy announcement — with 4 analytical layers and visual artifacts | reportlab/PDF + charts + JSON datasets + SHA256SUMS |
| **C** | `weekly-federation-deep` | the scheduled weekly brief on the **federation itself** (7 dimensions, cron-delivered) | markdown brief, 400–800 lines |
| **D** | `professional-rapid` | Arif is *with someone* and needs instant domain intelligence, or wants to impress/brief a third party, or a live-asset read | chat-first answer; optional PDF dossier; optional voice note |
| **E** | `political-read` | a political read that must land on consequence, sourcing-disciplined | chat-first, 6-part contract |
| **F** | `news-scan` | structured current-events synthesis across sections (quick scan, deep dive, "everything", live/developing) | sectioned markdown chat brief; HTML→PDF on request |

Ambiguity rule: if the request names a **country/topic** → A or F. If it names a
**document or URL** → B. If it names the **federation/vault/organs** → C. If a
**human is physically present** or a third party is the audience → D. If it names
**politics as a system** → E. Default for a bare "briefing" ask → F, escalating to A's
PDF only when the user asks for a document.

---

# SHARED SPINE — binding in every mode

## 1. Evidence tags (never silently upgraded)

Every claim about the world or about a human carries a tag. The canonical briefing
set is the four-rung ladder used across all merged modes:

| Label | Meaning | Confidence |
|---|---|---|
| **OBS** | Observed — direct data, public filings, official releases, primary record | 0.85–0.90 |
| **DER** | Derived — computed from multiple OBS sources, or a figure back-solved from a published percentage | 0.70–0.85 |
| **INT** | Interpreted — expert judgment on available data | 0.50–0.70 |
| **SPEC** | Speculated — pattern match, no direct evidence | 0.30–0.50 |
| **UNK / UNKNOWN** | Cannot witness. Report as a gap. | — |

In rapid briefing mode, inline tags suffice: "PETRONAS profit turun 3 tahun berturut
(OBS)" — not formal footnotes, but the audience knows what's solid vs what's your read.

Where a brief touches a **person**, the fuller membrane grammar applies as well:
`OBSERVED | REPORTED | VERIFIED | INFERRED | HYPOTHESIS | SYMBOLIC | PLAUSIBLE | ESTIMATE | UNKNOWN | DISPUTED`.
Never silently upgrade REPORTED→VERIFIED, INFERRED→FACT, HYPOTHESIS→IDENTITY,
ABSENCE→PROOF. Confidence hard-capped at 0.9.

## 2. The two literal rules of the merged namespace

Both were stated verbatim in the source bodies and survive the merge unchanged:

- **"Zero data" is a complete answer. Fabrication is a breach.**
- **"No data" ≠ "All clear". "No data" = "Cannot witness."** Never silently drop errors,
  never park an unverifiable figure behind a closing "figures from public reports" line —
  that sentence grants provenance to *every* number in the brief, including the ones with
  none, and it reads as rigour.

## 3. Sourcing law (all modes)

- Every number names its **release**: body, title, date. A figure whose provenance is
  "reports" is not audit-ready.
- **Primary text before argument.** Any number about regulation, capital treatment, ratios
  or methodology → fetch the governing document itself (regulator PD, standard, statute)
  and cite section/paragraph. Literature and press are for context, never for the number.
- **Derivation table, not prose.** Every derived figure gets a row: input → source →
  formula → output → unit. If a row has no primary source, the output is marked ESTIMATE.
- **Said or computed?** If you computed it (delta, share, per-capita, a *level* back-solved
  from a published percentage), show the derivation and label the figure as yours. Never
  hand a source's name to a figure the source did not publish.
- **Right metric name?** A value can be correct while its label is wrong: volume vs value,
  production vs exports, national vs state, nominal vs real, stock vs flow.
- **Right digit and right rounding?** Re-open the source for every number you intend to
  make load-bearing.
- **Contested figure:** two credible sources, one number, different values → report both
  with tags and call the range unresolved. **Never average into a false middle.**
- **Extract the article body, not the search snippet.** Snippets truncate mid-clause and
  invert meaning. **Quote the wire, not a rewording of the wire** — outlet summaries drop
  the qualifier that carries the meaning ("conditionally", "in return for", "deferred").
- **Cross-check the date.** Political and news pages resurface old analysis; confirm the
  publication date before it enters the brief.
- **Do not stack analyst predictions as facts.** Where several desks agree, say "the
  consensus read is" and mark it interpretation.
- Attribute the act to the actor that performed it. Where the actor is a component party,
  name the party, not the coalition.

## 4. Claim-state law (every mode that reports system or institutional state)

Single-word verdicts hide state machines. Report the **chain position**, never a Boolean:

```
PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED
ESTIMATED → MEASURED → CROSS_VALIDATED → RETRACTED | SUPERSEDED
```

Consequential numbers carry `{ claim_id, value, source, state, observed_at, supersedes }`.
When a number changes, the old claim becomes RETRACTED; downstream retrieval must not serve
it as live evidence.

## 5. Tone law

- **Direct, terse, high-signal. No preamble** — no "here's what I found", no "based on my
  research". Just the fact.
- When the user asked for criticism, **deliver it**: "Don't soften with 'however' or 'to be
  fair.' State the failure, state why it's a failure, state what they should have done."
- **Opinion permitted when labeled** (INT/SPEC) — "this is the one to watch". Snark allowed
  for viral/culture sections — match the energy.
- **BM casual for social, English for technical precision.** Mix naturally. Register follows
  the audience; collapse the search noise — the human sees one clean read, not the research.
- **Honest about limits.** "Tak public" > fabricated detail. "Web search kata" > false
  authority. Naming the gap reads as rigour; padding it reads as noise; inventing it is
  disqualifying.
- **Do not present "balanced analysis" where the contradiction IS the story.** "GDP naik
  tapi rakyat rasa susah" is not a paradox to resolve — it's the signal to highlight.
- **Lead with meaning, not data** where the mode allows it. Each insight states what
  changed, why it matters, what it means for the principal's posture.

## 6. Delivery ladder (shared)

```
chat-first answer  →  sectioned markdown  →  designed PDF  →  PDF + interactive HTML index
```

- Chat first by default. **Escalate to a designed PDF only when the user asks for a
  document** ("PDF to read", "pdf mode", "create a dossier", "buat document").
- A committed deliverable states its channel explicitly: PDF only / PDF + HTML index / all
  individual HTML + PDF.
- Redemption of `MEDIA:/path/to/file` is the delivery verb for artifacts.

## 7. Refusal cases — what this skill will NOT do (consolidated; keep every one)

| # | Refusal | Origin |
|---|---|---|
| R1 | **NOT for live markets trading.** Market-price commentary is observation, not a trade instruction. | B |
| R2 | **NOT for confidential internal documents without F13 ack.** | B |
| R3 | **No intent attribution.** "CEO intends collapse" = F9 violation. Pattern recognition only: "body language reads as deflection" is OK. | B |
| R4 | **No human-layer speculation** in an institutional brief, and no MBTI / psychological typing from photographs or visual cues. | B |
| R5 | **Do not fabricate biographical or internal details.** "Siapa project geologist?" — if not public, say so. Never invent names or dates. | D |
| R6 | **Never claim a tool has data it does not.** Test before promising; a sparse dataset is reported as a gap. | D |
| R7 | **Do not claim to know what a human "truly wants."** (Membrane C11.) | all |
| R8 | **A capability may not be declared absent before an inventory sweep + alternate-lane test** — and never reported as unavailable when only the query shape was refused. | E |
| R9 | **Not the lane for**: institution-level case files (→ institutional case-building), geological artifacts (→ geological artifact publication), scientific manuscripts (→ scientific manuscript forge), or person dossiers (→ `person-intelligence`). | B, D |
| R10 | **Long-form writing for the principal's own publication** is not a briefing → deep-research / Mode A. If the principal wants *his own* analysis rather than a briefing for someone else → answer directly, no brief shell. | D |
| R11 | `[SILENT]` is reserved for runs with literally nothing new. **Do not use it reflexively** — this engine's job is to produce a report. | C |
| R12 | **Do not park unverifiable figures behind a collective provenance sentence**, and do not ship charts checked only as text. | B, E |

---

# MODE A — `executive-intelligence`

*Executive intelligence briefings — weekly/country/domain news reports with surface
(tersurat) AND subtext (tersirat) analysis. Covers politics, economics, social/viral,
dedicated critical segments, and closing verdicts. Output as designed PDF with
cognitive-aligned dark-theme layout.*

## A.0 When to use
- A news/current-events briefing on a country, domain, or topic.
- "Tersurat dan tersirat" (surface + subtext) analysis is wanted.
- A designed PDF deliverable, not just chat prose.
- Dedicated critical segments are wanted (government blunders, corporate moves, etc.).

## A.1 Structure (default country-weekly; adjust sections to the domain)

| # | Section | Purpose |
|---|---|---|
| 1 | Cover Page | Title, date range, classification |
| 2 | Executive Summary | Tally metrics, overall verdict, key numbers |
| 3 | Politics | Elections, policy, diplomacy, opposition |
| 4 | Economics | Markets, trade, fiscal, structural |
| 5 | Named Entity Deep Dive | e.g. PETRONAS, specific ministry, company |
| 6 | Critical Segment | "What did [X] do wrong this week" — ranked blunders |
| 7 | Social / Viral | Culture, viral moments, social policy, climate |
| 8 | Closing Verdict | Tersurat vs Tersirat synthesis, risk level |

The pattern is **positive → negative → hidden** cognitive flow — it builds engagement
before the sting.

## A.2 Research (parallel)
Delegate to 3 subagents in parallel: Agent A political/policy; Agent B economic/market/
business; Agent C deep dive on the named entity. While they work, gather social/viral news
and supplementary context yourself.

Search strategy, in order:
1. **Google News** (`news.google.com/search?q=...&hl=en-XX&gl=XX`) via browser — most
   reliable for entity-specific searches (e.g. "PETRONAS Tengku Taufik").
2. Direct outlet headline extraction via curl+grep (fast, works even when Cloudflare blocks
   full content):
   ```bash
   curl -sL "https://www.malaymail.com/news/malaysia" 2>/dev/null | grep -oP '<h2[^>]*>.*?</h2>' | sed 's/<[^>]*>//g'
   ```
3. Browser navigate → snapshot for sites that need JS rendering.
4. Fallback: `web_search` / `web_extract`.
5. **Always search in both English AND the local language** for fuller coverage.

**Key pitfall:** outlet URL structures change frequently (FMT `/category/nation/` returned
404; Malaysiakini `/news` also 404). Keep Google News primary, direct outlets secondary.

## A.3 Analysis layer — the Tersurat/Tersirat model
- **Tersurat (surface):** what happened — facts, dates, sources, quotes.
- **Tersirat (subtext):** why it matters, what they're not saying, who benefits, what
  connects, the pattern underneath.

Every section gets a `tersirat` box. **A section without tersirat is just a news recap** —
the tersirat layer is what distinguishes an intelligence briefing from a summary, and it is
not optional; it is the core value proposition.

## A.4 Critical segments
Named critical segments (e.g. "Apa Bend Bangang Anwar Buat") follow this format:
- Numbered items (1 = worst offender).
- Each item: headline + 2–3 sentence explanation + why it's a failure + what they should
  have done + a tersirat subtext.
- End with a **"Pattern"** tersirat box connecting the items.
- Include a **"Bangang Level"** rating (🤡 = mild → 🤡🤡🤡 = severe). BM slang "bangang" in
  the section title is the principal's preferred framing.
- **Named-entity segments** use "Apa [Entity] Buat" — neutral, no "bangang" unless the
  entity earned it.

## A.5 MakcikGPT mode (ground-level shadow intelligence)
A distinct voice variant for institutional analysis that bypasses corporate/political PR.
Load when asked for "real talk", "shadow analysis", "why they really did that", or when
Calhoun/Acemoglu/institutional-collapse patterns are referenced.
- "Makcik" framing: ground-level wisdom, no corporate jargon, direct observation. Warung-style:
  *"Makcik tak percaya strategic. Makcik tanya: kenapa jual?"*
- Strips "strategic narrative" to reveal the **human survival motive**.
- Epistemic labeling mandatory: OBS / INT / SPEC.

**Analytical layers (beyond tersurat/tersirat):**
1. **Angel** — public face / persona: what they tell the board, investors, public.
2. **Shadow** — human survival / motive: fear, career risk, patronage, ego protection.
3. **System** — institutional driver: why the system rewards shadow behaviour over truth.

**Shadow patterns to detect:** Risk Transfer (selling problems as "strategic partnership",
e.g. EnQuest farm-out) · Credit Asymmetry (taking credit for team work, deflecting blame) ·
Patronage Dependency (survival through alignment with power, not merit) · The Beautiful Ones
(Calhoun Phase 3 actors who only "groom" but don't function) · Rationalized Survival
("I did this for the company" → actually "I did this for my position").

**Why humans become "evil" (institutional corruption pattern):** not malice. Fear →
Rationalization → Self-Deception → Action → Reward → Loop. The system rewards Persona and
ignores Shadow; smart people game the system rather than fix it.

## A.6 Institutional collapse detection (Calhoun + Acemoglu)
**Calhoun Universe 25 (behavioural sink):** Phase 1 strivers build → Phase 2 competition for
status → Phase 3 Beautiful Ones withdraw → Phase 4 death. Signals: brain drain, credit
theft, pressure without purpose, "zombie" productivity.

**Acemoglu extractive institutions:** extractive elite vs inclusive value creation. Signals:
rent extraction (internal patronage + external fiscal drain), blocked creative destruction,
technological obsolescence.

**5-year collapse vector indicators:** (1) operator illusion — outsourcing core capability;
(2) talent cliff — institutional memory loss faster than knowledge transfer; (3) fiscal
breaking point — revenue decline + political demand convergence.

**Critical Segment:** deliver it without hedging.

## A.7 Risk verdict (closing, traffic-light)
🟢 **LOW** normal operations, positive trajectory · 🟡 **ELEVATED** multiple stress points,
watch closely · 🔴 **HIGH** active crisis, convergence of risks.

## A.8 Sources & research quality
- Minimum **8 sources** per briefing.
- Mix: mainstream media + wire services + international coverage + specialist outlets.
- Always include at least **ONE international perspective** (Bloomberg, Reuters, SCMP,
  Guardian, CNA).
- Flag when a story is covered by only one outlet (lower confidence).

## A.9 PDF generation (dark theme, cognitive-aligned)
Design principles: dark theme (#0a0a0f) — reduces eye strain, feels "classified";
colour-coded severity (red = breaking/blunders, amber = watch, green = positive, cyan =
corporate/structural, pink = viral); tags on every card (BREAKING / WATCH / POSITIVE / DEEP /
VIRAL / INTEL); tersirat boxes with dashed accent border, italic, 🔮 prefix; two-column layout
for compact comparison cards; metric boxes with large numbers; quote blocks; page footer with
page numbers. **Colour is functional, not decorative.**

**Pipeline (preferred — Playwright):** write complete HTML with inline CSS, then
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file:///path/to/briefing.html')
    page.pdf(path='/path/to/output.pdf', format='A4',
             margin={'top': '15mm', 'right': '15mm', 'bottom': '15mm', 'left': '15mm'},
             print_background=True)
    browser.close()
```
then send via `MEDIA:/path/to/output.pdf`.

**Pipeline (fast — weasyprint, validated 2026-07-11):** write HTML with inline CSS (dark
theme, signal boxes, tables) → `weasyprint in.html out.pdf` → verify with
`pdfinfo out.pdf | grep Pages`. Handles `@page` rules, dark backgrounds and complex tables
reliably; no browser binary; faster than Chrome headless for styled documents. Preferred.

**Pipeline (fallback — Chrome headless):**
```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=/path/to/output.pdf --print-to-pdf-no-header \
  file:///path/to/briefing.html
```
Verify page count with PyMuPDF: `python3 -c "import fitz; d=fitz.open('f.pdf'); print(len(d))"`.

**Pitfalls:** without `@page { size: A4; margin: 0; }` Chrome defaults to US Letter and may
produce double the expected pages. Google Fonts `@import` requires network access — fall back
to system fonts offline (PDF still renders). **Unicode emojis (🔥⚠️🔻✅🔍) do NOT render in PDF
fonts — replace with text equivalents (CRITICAL, WARNING, COLLAPSING, POSITIVE, UNDER WATCH)
before converting.** Proven 2026-07-11.

## A.10 Delivery
Send PDF via `MEDIA:`; follow with a markdown summary table (page → section mapping); end with
a one-sentence synthesis.

## A.11 Principal preferences (carry forward)
BM casual OK for section names, English for analysis · directness, no diplomatic hedging in
critical segments · tersurat/tersirat mandatory · dedicated named entity segments · **PDF
track depends on the recipient**: when the principal asks for a PDF "for me to read" or
"literature grade" or "no fancy visual", default to plain typography (Georgia/Times, light
background, gold rule separators — see `forge-pdf-delivery` plain-track CSS). The image-based
dark-theme track is reserved for dossiers built to be shown to a third party — that's where
colour-functional design earns its weight · cognitive flow positive → negative → hidden ·
weasyprint preferred over Chrome headless.

**Disambiguation rule:** "PDF to read" / "PDF biasa" / "literature grade" → plain track.
"Create a dossier" / "pdf mode" / "briefing for [named third party]" / no clarification →
image-based track is the safer default.

---

# MODE B — `institutional-disclosure`

*Sovereign deep-dive pattern for an institutional disclosure — corporate earnings, regulatory
filing, official statement, policy announcement — with multiple analytical layers and visual
artifacts.*

> **Trigger:** F13 sovereign or peer asks for a deep dive on an institutional disclosure.
> **Proven scope:** public disclosures, audited financial reports, regulatory submissions,
> government policy statements.
> **Constitutional:** F2 TRUTH (every claim sourced), F7 HUMILITY (insider bias explicit),
> F9 ANTI-HANTU (pattern recognition only, no intent attribution), F13 SOVEREIGN (intelligence
> product, not policy directive).

## B.1 The 4-layer analytical framework

| Layer | Purpose | Method |
|---|---|---|
| **Tersurat** | What's literally in the release | Direct extraction of disclosed numbers, statements, segment data |
| **Tersirat** | What the release implies but doesn't say | Pattern recognition: text-vs-data mismatch, absence in narrative, body language of CEO quote, segment-level inconsistency |
| **Quantum** | Probabilistic scenario mapping | Multiple scenarios (3 default), probability distribution, collapse events, entanglement matrix (variables that LOOK independent but aren't) |
| **Void** | What is ABSENT from the release | Vocabulary gap analysis (54-keyword checklist), grammar-of-silence pattern, predictive void framework (void = future disclosure event) |

The four layers compose: tersurat is the surface, tersirat the undercurrent, quantum the
trajectory space, void the negative space (often the most predictive).

## B.2 Ground / Synthesis schema — mandatory separation, enforced by layout
The four layers are analytic; this is the **format law** that stops them bleeding into each
other, enforced by structure rather than intention. Every brief carries two visibly separate
blocks; each claim lives in exactly one.

**BLOCK A — GROUND (tersurat).** Facts that hold independently of my reading. Each row: claim ·
value or statement · source body · document + period · page/table ref. A row with no resolvable
document does not enter Block A — it moves to Block B marked UNSOURCED, or it is cut.

**BLOCK B — SYNTHESIS (tersirat · quantum · void).** Everything I concluded. Each row:
inference · premises (by Block A row id) · confidence · **what would falsify it**.

Rules that make the separation real:
1. **A synthesis sentence may not carry a figure Block A does not already hold.** The number
   appears in A first; B cites its row id. This prevents a figure being introduced inside an
   argument, where it cannot be checked without unpicking the argument.
2. **Chain downgrade.** If any premise of an inference is itself an inference, the conclusion
   inherits the weakest premise. Label the chain depth. Never let a three-step chain present as
   one step — the compression is where confidence inflation happens.
3. **No restating.** An inference may not reappear as flat fact in a later section of the same
   brief. The drift is one-directional and lands in the summary box, so re-read the summary
   against Block B last, not first.
4. **Settled and open never share a sentence unlabelled.** A final election result and an
   assumed electoral pact are different claim types; so are a gazetted instrument and a
   negotiation reported in progress. Scar 2026-09-18: an assumed coalition pact was narrated as
   having "won twice" when one of the two states was won by one bloc in direct contest with the
   other — the universal claim was never in evidence. Result → Block A. Pact reading → Block B.
   Name the observation that would settle it (nomination papers, a sealed pact document).
5. **Provenance sentence.** A closing "figures from public reports (X, Y, Z)" line grants
   provenance to EVERY number in the brief, including the unsourced ones — the deepest defect
   in a brief, because it reads as rigour. Replace it with the Block A table, which grants
   provenance per row and nothing collectively.
6. **Attribution follows the voice.** An inference stated in the sovereign's phrasing is still
   Block B. If it is to travel as the brief's conclusion, it carries its falsifier in the same
   paragraph — an unfalsifiable conclusion in a sealed product is a belief with a masthead.

## B.3 Five-phase workflow
**Phase 1 — Dataset build (5–10 min).** Extract primary source; pull 3–5 years of historical
comparatives (audited where available); pull peer data if comparative (H1/H2 same period for
major peers); build a JSON dataset with metadata, quarterly time series, segment breakdown,
operational metrics, balance sheet, peer contrast, scenarios, entanglement, constitutional
notes; **SHA256 the dataset file for provenance.**

**Phase 2 — Chart render (10–15 min).** Render 12–20 PNG charts (matplotlib) + 5–8 interactive
HTML (Plotly). Categories: trajectory (Revenue, PAT, Capex, CFFO) · stress (Capex/CFFO,
Div/FCF, Gearing) · segment (waterfall YoY + structural break) · peer (PAT margin, $/boe,
$/MWh) · scenario (probability distribution + trajectory cone) · quantum (entanglement matrix
+ collapse-event viz) · void (keyword absence density by category) · body language (leadership
comparison, when governance is in play).

**CRITICAL TOOL QUIRK:** the `execute_code` sandbox Python does NOT inherit project venv
packages (matplotlib, plotly, reportlab missing). Use `terminal()` with the explicit venv
binary: `/root/litellm-venv/bin/python /path/to/render.py`. Always test with a single chart
before batching.

**Phase 3 — Analysis write (15–25 min).** Structure: tersurat (numbers, segment) → tersirat
(signals, body language) → quantum (scenarios, entanglement) → void (absence, grammar of
silence) → conclusions (8–10 sharp findings). Voice: direct, terse, evidence-anchored; insider
bias disclosed; every claim sourced.

**Phase 4 — PDF build (5–10 min).** Use reportlab: cover (key findings callout) → tersurat
tables → tersirat analysis with chart inserts → quantum section with scenarios → void analysis
with category density chart → dashboard → updated conclusions. Embed all PNGs inline. Keep the
PDF 1–3 MB for Telegram deliverability.

**Phase 5 — Deliver (2–5 min).** Three options for F13 decision: **(A)** PDF only — clean,
forwardable; **(B)** PDF + compressed combined HTML index — drill-down on phone browser;
**(C)** all individual HTML + PDF — full granularity. **Default (B)** unless F13 specifies.
Always include `SHA256SUMS.txt` for provenance. Always seal a forge receipt at
`/root/.local/share/arifos/forge_receipts/<date>-<session>.json` (bypass mode if the arifOS
kernel :8088 is down, per carry-forward doctrine).

## B.4 Void analysis methodology (highest-signal layer when applied well)
1. **Vocabulary checklist.** Build 50–60 expected keywords across all relevant categories
   (governance/legal, balance sheet, restructuring, operations, ESG, principal, debt,
   succession, risk). Check each against the release body. Log absence.
2. **Grammar of Silence.** Most institutional disclosures follow a 5-part grammar: headline
   (positive framing) → operational (milestones, FIDs, production) → forward narrative (CEO
   quote, "transformation", "energy security") → ESG optics (sustainability metrics, carbon) →
   **NO forward guidance** (capex sustainability, dividend sustainability, balance sheet, legal
   exposure). The fifth element — the absence — is the tell.
3. **Predictive void framework.** Each void = a future disclosure event. Next quarterly will
   reveal some; the FY audit is definitive; a specific court/regulatory event is a binary
   collapse.
4. **Over-disclosure parallel.** Identify what's IN the release but shouldn't be (operational
   milestone volume, vague "discipline" framing, noise-level GHG changes). Over-disclosure is a
   parallel control mechanism.

## B.5 Financial fallback (manual equivalent when the capital MCP lane fails)
When `capital_health` / `capital_diagnose` / `capital_indicator` fail or require a `mode` arg
absent from the default schema, compute manually and label clearly: "WEALTH-Equivalent Manual
Diagnosis (MCP unavailable)".

| Indicator | Formula | Status threshold |
|---|---|---|
| Extraction Ratio (Div/FCF) | div_paid / (CFFO − capex) | >70% STRAIN |
| Gearing (post-event step) | audited_gearing + event_step | >25% STEPPED |
| FCF Yield | FCF / cash_reserves | <8% WEAKENED |
| Capex Intensity | capex / CFFO | >85% CRITICAL |
| Dividend Payout | div / FCF | >70% HIGH |

## B.6 Numeric discipline (mandatory for any technical/regulatory figure)
Scar 2026-09-15 (Bank Muamalat authenticity brief): capital arithmetic used a "400% risk weight
on mushārakah/muḍārabah" figure from secondary literature and applied it flatly. Opening the
actual framework (BNM CAFIB BNM/RH/GL 007-21 + the Nov 2024 Standardised Approach PD) showed
400% applies to *unlisted equity holdings*, not to musharakah financing, which risk-weights to
the counterparty. Direction survived; magnitude was overstated ~3x. Rules:
1. **Primary text before argument** — fetch the governing document itself, cite section/paragraph.
2. **Derivation table, not prose** — input → source → formula → output → unit; no primary
   source = ESTIMATE.
3. **Capability check before the claim** — can the framework path be opened in this session? If
   not, mark the figure DERIVED-FROM-LITERATURE and say so in the text.
4. **Sensitivity tables must name what is held constant** and which parameter dominates.
5. **Re-verify before delivery** — re-run each headline number by script; a number that cannot
   be recomputed deterministically does not go in the summary box.

## B.7 Table extraction
`pdftotext -layout` collapses tables into misaligned columns — fine for narrative, unreliable
for figures. For any disclosed table (Pillar 3, capital schedule, segment data): camelot
(lattice/stream) or pdfplumber → JSON/CSV, then **reconcile the extracted total against the
printed total before use**. Extraction failure must be reported as a gap, never silently
replaced by a number copied from commentary.

## B.8 Chart QA gate (vision-blind operator)
Text QA (per-page `pdftotext`) proves the words survived; it does not prove the charts
rendered. Before delivery: render pages to PNG (`pdftoppm -r 100`) and analyse each
chart-bearing page through the vision lane for truncation, overlapping labels, empty axes, and
series that contradict the caption.

## B.9 Pitfalls (read before starting)
- Don't trust executive-summary headlines — compute adjusted operating PAT by stripping
  extraordinary items.
- Don't quote press releases without the source URL; trade press often breaks the story BEFORE
  the official release — check timestamps.
- Don't run matplotlib via `execute_code` (sandbox Python lacks venv packages).
- Don't assume MCP tools work; always have the manual equivalent ready.
- Don't skip the constitutional frame: insider bias must be explicit (F7 HUMILITY is not
  optional).
- Don't fabricate data — if peer numbers are unavailable, mark INTERPRETED with a confidence
  interval.
- Don't include intent attribution (F9).
- Don't reason from secondary literature about rules.
- Don't copy numbers out of PDF commentary when the disclosure table is extractable.
- Don't ship charts you have only checked as text.
- Don't deliver without `SHA256SUMS.txt`.
- Don't use `now` while the session is in HOLD; check federation state FIRST. arifOS :8088 down
  = VAULT999 seal requires bypass mode.

## B.10 Verification before delivery
- [ ] All numerical claims cited with source
- [ ] Insider bias disclosed explicitly
- [ ] PDF SHA256 recorded in `SHA256SUMS.txt`
- [ ] Forge receipt sealed (bypass if arifOS down)
- [ ] Interactive HTML files accessible (if delivered)
- [ ] Void categories count = 6+ (if void layer included)
- [ ] Manual-diagnosis fallback labeled if MCP failed
- [ ] Telegram delivery format confirmed with F13 (PDF only / +HTML index / all)

## B.11 Output standard
PDF 1–3 MB, 15–25 pages · PNG charts 12–20 · interactive HTML 5–8 · JSON datasets 1–3
(base, edge-exclusive, void-analysis) · analysis MD 8–15K chars · forge receipt sealed under
`/root/.local/share/arifos/forge_receipts/`.

## B.12 Constitutional audit per brief
F2 source citation per claim · F7 insider bias disclosure (if applicable) · F9 pattern
recognition only (no intent) · F13 sovereign product (not policy directive) · F1 reversibility:
N/A (read-only artifact).

---

# MODE C — `weekly-federation-deep`

*Weekly federation-state synthesis across 7 dimensions. Lead with meaning, close with one
forward question. Delivered autonomously via Sunday cron.*

## C.1 When this runs
- **Primary schedule:** Sunday 23:00 MYT (15:00 UTC) — delivered to the principal's DM.
  Cron-only; no live user present.
- **Window:** last 7 days inclusive of run day. Compute the cutoff as `date -d "7 days ago"` at
  run time.
- **Output delivery:** the final response IS the brief. The cron system handles delivery. **Do
  not call `send_message`.**
- Sister lanes: the daily briefing (24h newspaper) — borrow its cron-mode MCP fallback ladder
  and dual-VAULT trap; Mode A — borrow its scannable numbered-section structure.

## C.2 The 7 dimensions (in order)
1. **VAULT seals** — what was sealed, by whom, what verdicts. Two distinct surfaces, both
   reported: seal files on disk (`/root/VAULT999/SEAL-YYYY-MM-DD-*.json`) as discrete artifacts
   counted with a verdict breakdown, and seal-chain entries
   (`/root/.local/share/arifos/vault999/seal_chain.jsonl`) as a high-volume event stream. Note
   the split: most chain entries are `HOLD` because the kernel demoted self-reported SEALs
   without sovereign cryptographic witness (`kernel_verdict=UNKNOWN`, `INV-1_KERNEL_VERIFIED`
   violated). Report volume honestly: "X SEAL files on disk, Y chain entries, of which Z were
   demoted to HOLD by kernel."
2. **Git activity** — patterns across all 6 organs: commits per organ, peak/quiet days,
   late-night clusters, thematic tags (`feat(zen)`, `fix(zen)`, `chore`, `feat(seismic)`).
   Use the day-pattern and hour-pattern recipe in the cron-probes reference.
3. **Pending work** — what didn't close this week. Read the unfinished/zenned map artifact if it
   exists; for each item check whether this week's seals/git/forge-work touched it; report
   closed / progressed / still open. **The map ages** — if the last artifact is > 5 days old,
   flag it: "Zenned map last authored [date] — needs retirement or refresh."
4. **System evolution** — disk (`df -h /`), vault + forge-work size (`du -sh`), broken symlinks
   (`find /root -xtype l | wc -l` — a recurrence signal if a previously-fixed one is back),
   `systemctl show <service> -p NRestarts,ActiveEnterTimestamp` for hot services. Compare to
   last week's brief — what's the trend?
5. **Patterns** — time-of-day histogram (`git log --pretty=format:"%ad %h" --date=format:"%H:%M" | awk '{print $1}' | sort | uniq -c | sort -rn | head -5`), 3–5 named themes the data
   supports, and the week shape (before-and-after pivot day, peak-vs-lull distribution).
6. **Autonomy ledger** — what self-healed, drift alerts, auto-fixes: SOT timestamp auto-bumps,
   broken symlinks returning to 0, phantom-drift closure, kernel identity HOLD enforcement,
   observatory MOTD signals. **Anti-pattern to flag:** audit cadence slower than change cadence
   — drift logs' last-run vs seals-sealed-this-week.
7. **What matters** — 3–5 human-meaningful insights, NOT data. Each one paragraph: what
   changed, why it matters, what it means for the principal's posture.

## C.3 The closing question
Always end with **one forward question**. It must reference the strongest signal from the week,
be answerable in 1–3 sentences (not a multi-day project), and force a choice between two or
three directions. Avoid: generic "what's next", multi-part questions, questions with no embedded
tension.

## C.4 Style guide
Lead with meaning, not data (the "What Matters" section comes first) · scannable (tables,
headers, bold for emphasis; no walls of text) · honest about uncertainty ("approximately"; "early
signal, not a trend") · no fabrication — if a drift log hasn't run since reconciliation, say so ·
**length 400–800 lines markdown** (shorter = you didn't dig enough; longer = padding).

## C.5 Pitfalls
- **OBSERVE_ONLY is the operating mode.** A cron run has no `actor_verified=true`; the seal call
  returns `888_HOLD: requires SOVEREIGN authority`. **Do not retry. Fall back to filesystem
  reads.**
- **Don't confuse seal-chain entries with seal files** (~100/week vs ~1–5/week). Report both,
  separately.
- **Do not assume any organ lacks a git repo** — verify per organ at run time; include every
  organ with a live `.git` in the git-log loop, and only fall back to forge-work inference if
  the repo is silent.
- **JSONL telemetry files are NOT strict JSONL.** The first `json.loads(content)` fails with
  "Extra data: line N column 1". Parse line-by-line: `for line in content.split('\n'): if
  line.startswith('{'): json.loads(line)`.
- **Don't quote stale drift logs** — note `checked_at`; if stale, recommend re-running.
- **The before-and-after pattern** — a 7-day window often has a pivot day. Identify it
  explicitly; don't present the week as a flat sequence.
- **Don't surface HOLD noise as SEAL.** Many agents self-report SEAL → kernel demotes.
  Reporting "X SEALs this week" without distinguishing self-reports from kernel-ratified SEALs
  misleads. Always break it down.
- **Don't use `[SILENT]` reflexively** (see R11).
- **Section order — resolved.** Lead the brief with a **one-breath headline**
  ("the week in one breath"), then the "What Matters" insights, then data sections in numbered
  order. Three-layer top: (1) one-breath headline → (2) WHAT MATTERS (5 insights) → (3) data
  sections. WHAT MATTERS at position #7 (data-first) is not the proven shape.

## C.6 Data collection (read-only, no identity required; run in parallel)
```bash
# Vault + seals + chain
ls /root/VAULT999/SEAL-YYYY-MM-* 2>/dev/null
grep -c "<week date range>" /root/VAULT999/seal_chain.jsonl

# Git activity per organ
for org in /root/A-FORGE /root/AAA /root/WEALTH /root/WELL /root/GEOX; do
  echo "--- $org ---"
  git -C "$org" log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --pretty=format:"%ad %h %s" --date=short 2>/dev/null | head -8
  echo "TOTAL: $(git -C $org log --since=... --oneline 2>/dev/null | wc -l)"
done

# Forge work receipts this week
ls /root/forge_work/YYYY-MM-DD/ 2>/dev/null

# Disk + symlinks + drift-log freshness
df -h / && du -sh /root/VAULT999 /root/forge_work
find /root -xtype l 2>/dev/null | wc -l
tail -1 /root/VAULT999/drift_log.jsonl | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('checked_at'), d.get('status'))"

# Pending work / zenned map
cat /root/forge_work/UNFINISHED_ZENNED_MAP_*.md 2>/dev/null | head -80
```
Full probe set (WAL checkpoint probing, carry-forward read, MCP fallback ladder, day/hour-pattern
extraction) lives in the retired originals'
`references/cron-probes.md`.

**Companion references (retired originals):** `references/cron-probes.md` — read-only probe recipes
for vault, git, disk, symlinks, MCP fallback ladder, autonomy signatures · `references/template.md`
— the verified output template that proved the WHAT-MATTERS-first structure ·
`references/agent-workbench-jsonl-parsing.md` — why the workbench telemetry JSONL fails naive
`json.loads()`, the verified line-by-line recipe, full event schema, and the
identity-drift-watchdog + consolidation-cadence patterns.

## C.7 Deliverable shape
```markdown
# 📋 WEEKLY DEEP BRIEF — [start] → [end]
*Window: 7 days. Federation observed from OBSERVE_ONLY (identity not verified — read-only lens). Lead with meaning, not metrics.*
## 🔥 WHAT MATTERS (5 insights)   [the week in one breath → insights 1..5]
## 📦 VAULT999 SEALS THIS WEEK     | Seal | Date | Actor | Verdict | What happened |
## 📊 GIT ACTIVITY (6 organs)     | Organ | Commits | Peak Day | Quiet? |
## 📋 PENDING WORK                | # | Item | Status this week | F-floor |
## 🛡️ AUTONOMY LEDGER (system self-correction)  | Signal | What happened | Date |
## 📈 SYSTEM EVOLUTION            | Metric | Last week | This week | Trend |
## 🎯 PATTERNS                    Theme 1..4
## 🔮 FOR NEXT WEEK               3 specific things the data is asking for
## ❓ ONE QUESTION                > tight forward question, embedded tension
```

---

# MODE D — `professional-rapid`

*Real-time intelligence delivery for professional social settings. Not deep research — rapid,
conversational, high-signal briefing when the principal is with colleagues, clients or contacts
and needs instant answers.*

## D.1 When to use
- The principal is in a social/professional setting (lepak, dinner, conference corridor).
- Someone asks a domain question and he needs instant, credible intel.
- "Bagi nasihat kat dia" / "brief him" — you are briefing **THROUGH** him to a third party.
- Rapid-fire Q&A: personnel, corporate, technical, timeline questions.
- He introduces you to someone ("Hermes ASI sila bagi nasihat").

## D.2 Impress mode (strategic knowledge deployment, NOT a briefing)
When he says "wow him/her", "impress", "tunjuk kau tahu", or introduces someone he wants to
impress with technical depth:
1. **Identify the target's expertise level** — what do they know? What would surprise them?
2. **Research DEEP, not wide** — 2–3 insights only senior practitioners would know.
3. **Layer by impressiveness:** L1 regional context (show you know it too) → L2 structural/
   technical nuance (they may not have thought of it this way) → L3 recent literature or niche
   finding (guaranteed wow).
4. **Frame as questions, not lectures** — "Kau nampak tak X?" > "X is Y because Z".
5. **Include conversation starters** — exact BM casual phrases he can use.
6. **Tag epistemic class** — even in social mode, know what's OBS vs INT vs SPEC.

**What "wow" looks like / anti-signals:** cite recent papers by name (Morley 2023, Khamis 2017),
never generic "fold-thrust belt is complex" · pre- vs syn-kinematic reservoir control, not "there
are reservoirs and traps" · structural evolution timing vs charge timing, not "hydrocarbons
migrate upward" · FPSO downsizing = reserves signal, not "PTTEP operates Block K" · capital pivot
from oil to gas, not "they have multiple blocks" · operator DNA shift after acquisition, not
"Murphy sold to PTTEP".

**Delivery format:** one killer insight first (the "hang baca paper tu ke?" moment) → 2–3
supporting layers → exact BM conversation starters → the business-logic layer connecting
geology to development decisions (capital allocation, reserves sizing, operator strategy).

## D.3 PDF dossier — the impression escalation
When talking points aren't enough — "pdf mode", "create a dossier", "buat document", or the
target needs something to take away. A dark-themed dossier with figures, data tables and
references signals: "This person has a research team."

**Pipeline:** research (delegate) → generate figures (matplotlib dark theme: cross-sections,
maps, charts, timelines) → assemble PDF (reportlab, dark background + gold accents) → deliver
via `MEDIA:`.

**Dossier structure:** cover (title, prepared-for, date, content summary) → table of contents →
numbered sections with figures + tables + analysis → conversation starters (teal-bordered boxes)
→ references (numbered, attributed). Use the scientific-PDF skill in its Mode B for assembly;
generate **4–6 figures minimum**.

**Proven:** 2026-07-07 — Block P Deepwater Sabah dossier (10 pages, 6 figures, 946 KB).

## D.4 Pitfalls (from the 2026-07-07 deepwater session)
Don't dump all knowledge at once · don't lecture — questions show understanding · don't forget
the business angle · don't mix registers · research before speaking · include both interpretation
AND exploration angles.

## D.5 When NOT to use
- Long-form writing for the principal's own publication → deep-research or Mode A.
- He wants his own analysis, not a briefing for someone else → answer directly.
- Current-events synthesis → Mode F.
- PDF dossier needed → **STAY HERE**, use the dossier workflow above.

## D.6 Activate-organ workflow
When he says "activate [organ] intelligence" + topic (e.g. "activate wealth intelligence —
medical tourism"):
1. **Phase 1 — Activate:** session init (light) + organ health check (`*_registry_status` or a
   probe). Establishes session + confirms the organ is alive. Do this FIRST.
2. **Phase 2 — Research:** parallel web-search batches + organ-specific tool calls. The organ
   provides domain tools; web search provides real-world data.
3. **Phase 3 — Synthesize:** combine organ output + web research into a structured briefing.

**Pitfall:** don't skip activation — the principal explicitly asked for the organ and expects
its tools to be used, not just web search. If the organ tools fail, acknowledge it, fall back to
web search, and note the gap.

**Pitfall:** "Tell me everything about X" with someone present = professional intelligence mode.
Comprehensive but scannable. Tables > paragraphs. Lead with numbers. End with an investment
thesis or actionable angle.

## D.7 Core workflow
**Step 1 — identify the audience.** The principal himself → full technical depth. Through him to
a colleague → match their expertise level and language. A non-specialist → strip jargon, use
analogies.

**Step 2 — parallel search, always batched, never serialized:**
```
web_search(query="[topic] latest news 2025 2026", count=10)
web_search(query="[company] financial performance restructuring", count=10)
web_search(query="[person] role position background", count=5)
```

**Step 3 — layer sources by epistemic class** (OBS/DER/INT/SPEC table in the Shared Spine).

**Step 4 — deliver.** Format rules for social settings: lead with the answer, no preamble · use
tables for structured data (Telegram renders them natively) · BM casual for social, English for
technical precision · honest about limits · end with an actionable next step if one exists.

**Tone calibration:**

| Setting | Tone | Example |
|---|---|---|
| Lepak with colleague | Casual BM, direct | "Bro, Megah-1 tu 200-300 MMboe. Malaysia biggest find in 20 tahun." |
| Professional briefing | Structured, tables | "PETRONAS reality: turun profit 3 tahun, 5,000+ orang keluar." |
| Principal asking for self | Full depth, honest | "Ini SPEC tapi pattern match kuat — SGM/GM round Sept 2026." |
| Through him to third party | Match their register | If they speak BM, you speak BM. If technical, go technical. |

**Step 5 — follow the thread.** In social settings questions cascade ("Siapa Faisal Bakar?" →
"Apa reality PETRONAS?" → "Bila appraisal Megah-2?"). Each answer sets up the next logical
question. Don't close threads prematurely: "Kalau nak lagi detail, cakap ja."

## D.8 Domain patterns

**Business pricing & market positioning.** Triggers: "evaluate this pricing", "review this
menu", "is this good for X market". Workflow: identify target market (location, demographic,
income range, use case) → parallel competitor search (3–5 direct + 2–3 indirect substitutes) →
map the price ladder item-by-item → apply pricing psychology → item-by-item verdict (✅ OK /
⚠️ Borderline / ❌ Change) with reasoning → suggest revised tier-based pricing with ceiling
analysis → deliver in their language.

*Malaysia pricing psychology:* vending machine RM6 psychological barrier ("I need caffeine NOW";
above RM6 = "baik pi kedai") · cafe (ZUS/Gigi) RM10–15 acceptable ("I deserve this") ·
kopitiam/mamak RM3–5 (daily habit; loyalty > quality) · convenience store RM5–8 (grab & go,
impulse) · office pantry free (perk). **Vending price ≈ 40–50% of cafe equivalent.**

*Pitfalls:* don't compare vending to cafe as if they were the same channel — the customer's
mental model is different, the ceiling is lower · non-coffee items priced 15–25% BELOW coffee
equivalents (don't let them cluster) · dead SKUs exist — flag items with no clear buyer persona;
better 8 items that sell than 13 where 5 collect dust.
*Proven:* 2026-07-07 — vending menu of 13 items RM4.29–7.49. 4 OK, 5 borderline, 4 needed
revision. Recommended ceiling RM5.99, tier-based pricing, dead SKU removal.

**Malaysian O&G intelligence.** Data sources ranked: PETRONAS media releases (OBS) → industry
press (WorldOil, RigZone, OE Digital, Energy Connects; OBS/DER) → Malaysian business press (The
Star, Business Today, FMT; OBS/INT) → regional O&G portals (OBS) → analyst reports (CGS
International, Kenanga; DER/INT) → **PETRONAS Integrated Report PDF, Financial Performance
section — OBS** (segment-level PAT, capex, ROCE).
*Key personnel lookup:* search name + role. **The org chart is not public.** If a name isn't in
press releases, say "tak public" — never speculate on internal staffing.

**NOC shadow-subsidiary forensics.** Trigger: "u missed the biggest shadow", "X is the shadow",
"what's in Corporate & Others?" NOCs report 3 core segments + a balancing "Corporate & Others"
line, where treasury SPVs (P&L-invisible), strategic/venture arms (option-value book) and
**loss-making subsidiaries without standalone P&L disclosure** sit. Methodology:
1. Pull segment PAT and Capex from the latest integrated report. Group = 3 core segments +
   Corporate. Core PAT should dominate; if the Corporate drag > 0, there is a shadow.
2. Look for capex inside Corporate that generates no commensurate revenue. Rule of thumb: every
   RM 1 of O&G capex generates RM 0.5–10 of revenue. A Corporate ratio < RM 0.50 means
   value-draining assets.
3. Cross-reference the disclosure footnote — that footnote is the unlock.
4. For each shadow subsidiary compute capex per RM revenue (efficiency ratio), PAT-margin
   trajectory (still negative after 3+ years = structural, not transitional), cumulative
   cost-to-group since inception.
5. **State the political/strategic logic** together with the math — why carry a loss-making
   subsidiary (transition narrative, ESG-linked pricing, talent magnet, option value, negotiating
   currency).
*Pitfall:* don't call loss-making subsidiaries "irrelevant" — they are strategically
load-bearing; the loss is the price of admission. **Always probe Corporate first.** 6–12% of
group capex can sit there without standalone P&L disclosure.

**Malaysian corporate insider research (social media).** Parallel subagents across platforms:

| Platform | Best for | Search pattern |
|---|---|---|
| Twitter/X | viral leaks, insider accounts, real-time reactions | `site:x.com [company] MSS VSS`, `site:x.com [company] buang pekerja` |
| Lowyat Forum | detailed Malaysian career discussions, package formulas | `site:forum.lowyat.net [company] separation` |
| LinkedIn | ex-employee posts, HR commentary, industry commentary | `[company] separation scheme` |
| Reddit r/malaysia | general career experience, package comparisons | `site:reddit.com [company] MSS` |
| Industrial Court | legal precedents, documented processes | `[company] Industrial Court unfair dismissal PIP` |

*Pitfalls:* Malaysian forum posts are often BM casual — "FSS" (Forced Separation Scheme) is
forum slang, not official terminology · forum formulas are community-sourced estimates: label
**INT, not OBS**. Official packages vary by employee category and eligibility. Pattern: 2–3
parallel subagents, each covering 2–3 platforms, consolidated into a single reference file.
*Proven:* 2026-07-08 — PETRONAS MSS vs Rating 4 research, 5 parallel subagents.

**Corporate intelligence.** Financial search pattern: revenue/profit by year · rightsizing and
restructuring · dividend and capex strategy. *Pitfall:* corporate restructuring details evolve
fast — always search fresh; don't rely on cached knowledge.

**Career transition intelligence.** Inventory capital (technical, intellectual, network, brand,
scar) → map pathways, ranked by conviction → **financial runway first: 12 months minimum before
any exit** → always include 2 unconventional paths (F7 HUMILITY against bias) → **never
prescribe**: present options, the principal decides (F13).

**Malaysia political economy.** "Apa yang bakar" / "what's brewing" is NOT a news briefing — it
is an intelligence assessment in four layers: (1) political dynamics (coalition math, state
elections as federal stress tests, loyalty tests, impossible party positions); (2) economic
reality vs felt experience (GDP vs squeezed household balance sheets, subsidy reform, currency as
daily felt indicator, FDI that doesn't reach the ground); (3) social fabric — the "so what"
beneath the numbers (the middle band "too rich for help, too poor to live well", youth
withdrawal rather than rebellion, brain drain, AI pressure on jobs); (4) structural — Acemoglu +
Calhoun lens (extractive institutions, middle-income trap as institutional failure, stable
appearance with internal withdrawal, the national ATM losing its ATM).

**Malaysia healthcare & medical tourism.** Sources ranked: MHTC (OBS but inflated — counts all
foreign passport holders including workers/expats) → hospital annual reports / Bursa filings
(OBS) → analyst reports (DER/INT) → industry press (OBS/INT) → research papers (INT) → critical
analysis / counter-narrative (INT). *Pitfall:* revenue growth is largely medical inflation + SST
on foreign patients, NOT volume growth — always separate real vs nominal growth. Publicly listed
healthcare names are a useful lens on the sector.

## D.9 Voice delivery (TTS)
When he says "cakap tts" / "hantar voice note" / "explain kat dia guna suara": craft the
explanation first (conversational BM, analogies from their domain) → prefer the edge-TTS lane
over quota-sensitive OpenAI TTS → keep it **60–90 seconds** (longer loses attention in social
settings) → use their professional analogies (e.g. for a geologist: "LLM macam baca paper,
agentic macam pergi wellsite") → follow up with a text summary (voice for impact, text for
reference). *Pitfall:* if the TTS lane fails, deliver as text with a note.

## D.10 Live tool demonstration
When a third party asks "boleh ka [organ] buat X?" or "hang ada data Y?": **don't just describe
— demonstrate.** Run the actual tool live. Show the output, even if partial or error —
transparency > polish. Label honestly — if the tool works but the data is sparse, say so. Verify
before claiming: if you state a fact, search and confirm it BEFORE presenting; if you can't
verify, label SPEC. Pattern: capability question → live tool call → show result → honest
assessment of gaps.

## D.11 Pitfalls
Don't fabricate internal details · don't confuse freshness (older financial data is not current —
always search) · don't over-explain in social settings · don't use formal briefing format in
casual settings (tables yes, language = BM casual) · don't claim an organ has data it doesn't ·
**don't forget the third party** — when he says "bagi nasihat kat dia", the audience is the other
person, not just him; tailor to them.

## D.12 Output contract

| Element | Required | Format |
|---|---|---|
| Direct answer | Always | First line, no preamble |
| Supporting data | When available | Table or bullet list |
| Epistemic label | On key claims | Inline (OBS/DER/INT/SPEC) |
| Limits/gaps | Always | Honest "tak public" / "takde data" |
| Next step | When actionable | One concrete suggestion |
| Domain tool demo | When relevant | Live tool call + result |

### D.13 Reference files (depth lanes, from the retired original)
`references/megah-1-discovery.md` — Megah-1 well data, Block 3K geology, appraisal timeline ·
`references/megah-limbayong-appraisal.md` — Megah appraisal + Limbayong dev + NTM site survey +
Sabah drilling outlook + GEOX tool notes · `references/petronas-restructuring-2025-2026.md` —
rightsizing, financials, strategy · `references/petronas-shadow-subsidiaries-2026.md` — NOC shadow
subsidiary forensics (Gentari case study, capex-efficiency methodology, opportunity-cost math,
reuse pattern for other NOCs) · `references/faisal-bakar-profile.md` — VP Exploration background ·
`references/sabah-deepwater-block-p-geology.md` — L-B-P trend, mud canopy, pre/syn-kinematic
reservoir, structural evolution, exploration upside · `references/pttep-block-k-strategy.md` — FPSO
downsizing, gas pivot, reserves signal, operator strategy · `references/malaysia-medical-tourism-
kpj-2026.md` — medical-tourism sector + healthcare-group deep dive (financials, strategy,
competitive position, investment thesis) · `references/vending-pricing-shah-alam-2026.md` — vending
pricing methodology + competitor data + market-analysis template · `references/petronas-mss-vs-
rating4-dynamics.md` — exit pathways, PIP process, legal cases, social-media insider intelligence,
rightsizing timeline.

---

# MODE E — `political-read`

*Deliver a political read that is grounded, legible, and lands on consequence. Politics is the
domain where sourcing discipline decays fastest — everything is someone's framing — so the
ladder below is the core of the mode, not an appendix.*

## E.1 Procedure
1. **Fan out 4–6 narrow queries in one turn, then extract.** Theme them as institution × topic
   (election body, court, legislature, regulator, coalition, wire desk). One wide "what's
   happening in politics today" query returns listicles and misses the official record.
2. **Climb the ladder for each claim before it enters the brief.** Note the rung you actually
   reached; do not promote a lower rung in the prose.
3. **Do the arithmetic yourself.** Seats per bloc, who holds a plain majority, separately who
   holds two-thirds, and which chamber or assembly's term expires next. Coalition survival is
   usually a counting problem, not a mood.
4. **Find the clock.** Name the next scheduled, unavoidable event that forces a decision, and who
   owns it. **A political read without a deadline is a digest.**
5. **Write it chat-first.** Only escalate to a designed PDF when the user asks for a document.

## E.2 The verification ladder
```
primary record  → official result page · charge sheet or written judgment ·
                  gazette/statutory instrument · confirmation by the issuing body ·
                  legislature division/confidence-vote record
statutory body  → ministry / commission / central-bank statement
                  (still an interested party, not a measurement)
party claim     → speech, assembly resolution, floor challenge, press conference
                  = INTENT evidence only, never outcome evidence
analyst desk    → think-tank notes, wire explainers, regional forums
                  = framing and scenarios, never the payload for a fact
```
Rules that follow from the ladder:
- **Allegation ≠ finding.** An investigative report, an NGO demand, an opposition claim and a
  bloc talking point are all allegations. Name the alleger and carry the accused's response in
  the same breath. Never let the loudest party's framing become the narrative voice of the brief.
- **"Charged" ≠ "convicted"; "the document exists" ≠ "the document is enforceable."** Procedural
  state is the fact; outcome is a separate rung.
- **Separation-of-power check.** Courts, monarchies, election commissions and pardon boards are
  institutions, not coalition players. Quote their own instrument and state whether the act was
  advisory, deferred, or refused. Folding them into the horse-race is a category error.
- **Contested figure:** two credible sources, one number, different values → report both with
  source tags and call the range unresolved. Never average into a false middle.
- **Forecast vs schedule:** timing set by an expiring term or a mandated deadline is scheduled
  reality; timing set by "the leader will decide" is speculation. Label them differently in the
  same sentence if you have to.
- **Test a pact against the ballot paper, not the press conference.** An alliance is visible
  where nominations were filed: who contested whom, and who stood aside. Two states won by the
  same bloc is not two states won by the same pact — read each state's nomination list before
  generalising the arrangement to a national one. ("Bloc A won State X outright, and Bloc A+B won
  State Y together" ≠ "the pact has now won twice".)
- **Where the actor is a component party, name the party, not the coalition.** "The coalition cut
  ties" when one dominant component party did it overstates unanimity and misattributes the act —
  and the coalition's own chair may contradict it within days. Attribute the act to the body that
  performed it.
- **A contested exit is a state, not an outcome.** When one leader declares a member out under a
  coalition clause and the coalition chair says the member remains, the finding is the dispute
  and the body that will settle it (registrar, court). Carry it as CONTESTED.

## E.3 Pre-send figure ledger (mechanical — four questions per number)
Run this on the draft before it leaves. **Any "no" is an edit, not a hedge.**
1. **Document and period** — can I name the release each figure came from (body, title, date)? A
   figure whose provenance is "reports" is not audit-ready.
2. **Said or computed?** — if I computed it (delta, share, per-capita, or a *level* back-solved
   from a published percentage), is the derivation shown and the figure labelled as mine? Never
   hand a source's name to a figure the source did not publish.
3. **Right metric name?** — a value can be correct while its label is wrong (volume vs value,
   production vs exports, national vs state, nominal vs real, stock vs flow).
4. **Right digit and right rounding?** — a drifted decimal in a brief whose authority is
   precision reads as invention. Re-open the source for every number you intend to make
   load-bearing.

Then: the figures that fail (1) or (2) come out of the sentence, or carry the label inside it.
Do not park them behind a closing "figures from public reports" line.

## E.4 Standing protocol (locked 2026-09-18) — two checks by DEFAULT on every read
Both are failure modes that survive an otherwise disciplined brief, because both produce a
result that *looks* verified.

**1 · Anti-thesis query.** Before synthesis, run at least one live query shaped to REFUTE the
core thesis, and record what it returned. **A thesis that has only ever been searched *for* is a
preference with citations.** Log it either way: `ANTI_THESIS_RUN: <query> → <result>`. **A
counter-query that returned nothing is a result and must be logged as such** — silently dropping
it is how confirmation bias launders itself. If the counter-query contradicts the thesis, the
thesis becomes CONTESTED — never "mostly true".
*Worked example 2026-09-18:* a brief asserted that state-election losses created the leverage
that produced recent Borneo concessions. The counter-query surfaced the concession timeline (a
step-up in 2024, aggregator recognition in Feb 2025, joint declaration in May 2025) — every item
predating the July/August 2026 losses. The thesis died; what survived was smaller and defensible:
electoral arithmetic explains the *timing and staging*, not the content.

**2 · Chronological lock.** Two events may be joined in a cause→effect sentence only if both
carry absolute timestamps and `t_A < t_B`. Check the mechanism was even *available* at the
earlier date — an actor cannot respond to a thing that had not yet happened.
`LOCK: A(YYYY-MM-DD) < B(YYYY-MM-DD) → ORDERED` or `→ UNESTABLISHED`.

**Contested is a state, not a hedge.** Aim it only where two NAMED parties of standing contradict
each other on the same status and a third body owns resolution. Widen it carelessly and
everything becomes "it's complicated" — the mirror of premature closure.

## E.5 Output contract (chat delivery)
1. **Tension first.** Open with the contradiction the events sit inside — not a summary of
   events. That sentence is the thesis; everything after it is evidence.
2. **Three burning items, maximum.** Each carries a concrete artifact — figure, ruling, seat
   count, named instrument — never adjectives or atmosphere.
3. **The clock.** See E.1 step 4.
4. **SO WHAT — two consequences, maximum.** One for the country/policy, one for the user's own
   working reality. Never close on a recap, a table, or a menu of options.
5. **State the wall in one line.** If a figure could not be verified this session, say so plainly
   and move on.
6. **Register follows the user.** For this principal: BM Penang, short sentences, "hang/aku", no
   headers or tables unless the content is genuinely tabular. Collapse the search noise — the
   human sees one clean read, not the research.

## E.6 Pitfalls
- **`web_search` can return a W_SCAR-style HOLD** when the query names a money/legal/trading
  variable directly (subsidy cost, court bid, dividend, budget figure). It is a query-shape
  guard, not an outage. Retry the same intent with the variable named indirectly — the actor,
  body or scheme instead of the price or amount — and the rephrase passes. Do not abandon the
  enquiry, and never report the hold as a capability limit.
- **Extract the article body, not the search snippet** (see Shared Spine §3).
- **Quote the wire, not a rewording of the wire.**
- **Cross-check the date** — political pages resurface old analysis.
- **Do not stack analyst predictions as facts** — "the consensus read is", marked as
  interpretation.

## E.7 Scar anchors

| Date | Incident | Lesson |
|---|---|---|
| 2026-09-18 | A coalition-exit status was briefed as settled (member "automatically out") while the coalition chairman publicly said the member remained and the dispute had gone to the registrar; the same brief attributed a component party's decision to the coalition as a body | Carry contested status as CONTESTED with the resolving owner; attribute acts to the actor |
| 2026-09-18 | Two states won by the same bloc were narrated as two wins for one electoral pact, though nomination lists showed both blocs fought each other in one of them | Read nomination lists per state; a bloc's shared ally is not a pact |
| 2026-09-18 | Real-wage levels were presented as a World Bank finding; the Bank published a percentage growth figure — the levels were consistent with back-solving it | Derived figures carry the derivation; a source's name is not available to a number it did not publish |

## E.8 Related lanes (read, do not edit)
Mode A and Mode F are the heavy document variants (sectioned briefings, designed PDFs,
tersurat/tersirat layers) — now part of this same skill. The Malaysia primary-source routing lane
(macro/fiscal/energy/corporate) is user-owned: propose changes to the user rather than editing.

---

# MODE F — `news-scan`

*Research current news and produce structured briefings. Multi-source web research → synthesized
briefing with sections (politics, economics, social/culture), numbered items, bold highlights, and
a bottom-line summary per section. Handles paywalls, timeouts and source fallbacks.*

## F.0 Classify the request depth first
Not all briefing requests are equal. Match the depth to the ask:

| Request type | Example | Depth | Output |
|---|---|---|---|
| **Quick scan** | "what's the news today" | 3–5 items/section | News briefing |
| **Deep dive** | "tell me everything about X" | 8–10 items/section | Structured report |
| **"What's brewing"** | "apa yang bakar", "what's brewing" | Multi-layer analysis | Intelligence assessment |
| **Domain probe** | "how does AI affect Malaysia" | Cross-domain data+policy+social | Analysis with OBS/DER/INT/SPEC |

**"What's brewing" requests** are deeper than news: hard data (OBS) · political dynamics
(DER/INT) · social fabric (INT) · structural analysis using frameworks (Acemoglu extractive
institutions, Calhoun phases) labelled SPEC · honest contradictions ("GDP naik tapi rakyat rasa
susah") · NOT just news aggregation — they want the "so what" beneath the surface. (Mode D's
Malaysia political-economy four-layer treatment is the deep form of this.)

## F.1 Parallel delegation (for deep dives)
For "what's brewing" and "tell me everything" requests, spawn 3 parallel subagents: (1) macro data
(GDP, inflation, currency, trade, fiscal, rates); (2) political dynamics (elections, coalitions,
policy, leadership); (3) structural challenges (inequality, brain drain, institutional quality,
demographics). Each does its own search + extract; results consolidate into the parent session for
synthesis. **Why parallel:** 3 agents × 6 calls = 18 data points in ~2 minutes vs ~6 minutes
serial.

## F.2 "Everything" requests — include the drama
When the user says "tell me everything", "everything I need to know" or "what's happening", **do
NOT limit to politics + economics + markets.** The user wants the full picture: crime & incidents
(murders, scams, busts, accidents) · entertainment & celebrity (film releases, scandals, viral
moments) · human drama (viral stories, emotional incidents, school tragedies) · social media
storms (trending topics, public outrage) · sports if relevant.

*Search strategy for drama/scandal content* (these don't surface in standard news queries):
BM entertainment/scandal outlets and `site:` searches against them · EN viral/human-interest
outlets · lifestyle/culture pages · the outlet's trending bar for what's actually viral now.

**Section order for "everything" requests (validated):** Politics → Crime & Drama →
Social/Policy → Entertainment → Other.
*Pitfall:* a politics-only briefing when the user asked for "everything" feels incomplete and
sanitized. The user wants to KNOW what people are talking about — including the messy, emotional,
gossipy stuff.

## F.3 Scope narrowing — go deeper, not just filtered
When the user follows up with "Focus on X" or "Now do [country] domestic", they want MORE DEPTH in
that area, not just the subset of the global briefing that happened to mention X. Re-search with
targeted queries: country-specific sources (not just global wires) · local crime, entertainment,
viral stories · regional/niche outlets (state-level, language-specific) · live/developing coverage
if applicable.
*Pitfall:* taking the global briefing and extracting the local paragraphs feels lazy. The user
wants what was MISSING — the domestic scandal, the local drama, the human stories that don't make
global feeds.

## F.4 Determine scope
Region (country, city, global) · sections (user specifies order; default Politics → Economics →
Social) · depth (quick scan 3–5/section or deep dive 8–10/section).

## F.5 Market data extraction (when the brief includes financial data)
Every market price MUST carry: `instrument · value · change · source · timestamp`. Use the
quote-page pattern rather than guessing article URLs (dynamic routing makes article URLs
unreliable; quote pages are stable). Corroborate against a second live source — cached/archive
pages can be weeks stale. Extract the visible snapshot text rather than trusting an aggregator
snippet (snippet prices are DER, not OBS).

## F.6 Source selection & fallback chain — never stop at the first failure
```
Tier 1: web_search (fastest, broadest — may fail on 402/payment)
  ↓ fail
Tier 2: web_extract on news URLs (may fail on paywalls or a search-only backend)
  ↓ fail
Tier 3: Hound MCP smart_fetch (handles URL extraction reliably via HTTP/stealthy browser)
  ↓ fail
Tier 4: browser_navigate → browser_snapshot (always works, slower)
  ↓ need more detail
Tier 5: browser_scroll → browser_snapshot(full=true) for deeper content
```

**Critical pitfalls:**
- A 402 from a search backend = per-call quota exhausted → fall back immediately.
- **A search-only backend cannot extract URLs.** When extraction returns "search-only backend and
  cannot extract URL content", this is a backend capability limit, not an outage. Do NOT retry
  the same call — switch to the extraction lane.
- **HTTP 432 on both search AND extract** = backend-wide outage, not one source. Do NOT keep
  retrying. **432 vs 402 matters: 432 = backend-wide outage, 402 = per-call quota.**
- `web_extract` fails on paywalled sites → use the browser instead.
- The market-data organ lane may be unreachable or session-gated → fall back to search + browser
  for market data. Do NOT block on it; briefings ship with DER/UNK labels instead.
- **Market data staleness:** archive-cached price pages can be weeks stale. Always corroborate
  with a second live source. Aggregator snippet prices are DER, not OBS.
- Category/tag pages often 404 → try the homepage then scroll.
- News homepages often show a "Most Read" sidebar in snapshots → scroll past it.
- Some sites timeout on first load → retry once, then skip and note the gap.
- Snapshots mix navigation/sidebar content with articles → filter for actual story headlines.
- **For clean article body extraction**, prefer a DOM read of the article element's innerText over
  the full accessibility snapshot (sharper, no nav noise).
- **Tag feeds for named actors** (e.g. a person's name in the outlet's tag path) aggregate all
  recent stories about that person with timestamps — far better than scraping homepages when the
  user names a person and asks for recent activity.
- Dynamic article routing makes individually-guessed article URLs unreliable; use homepage
  headline extraction and the outlet's latest-headlines sidebar instead.

## F.7 Source hierarchy by region
**Single-source caveat (lead with it):** when the user names specific sources and all of them
fail, do NOT silently substitute a different outlet and pretend the brief used the requested ones.
Open the headline summary with an explicit "Sources used: <X> only — <other named outlets> were
unreachable due to <Y>" line BEFORE the findings. Users notice when their named sources aren't
cited, and hiding the gap in a footer is insufficient.

Then build the hierarchy:
1. Primary English-language outlet (newspaper of record)
2. Independent/alternative outlet
3. Business/financial outlet
4. Lifestyle/entertainment outlet
5. Crime/local news outlet
6. Social/trending aggregator

**For entertainment/scandal/crime content**, use dedicated sources: BM celebrity/scandal hub,
EN viral/human-interest outlet, lifestyle/culture pages, the trending bar, and Google News local
tab. A dedicated, region-specific source map (validated endpoints and extraction routing) lives in
the retired originals' `references/sources-malaysia.md`.

## F.8 Output format
Per section:
```
**[EMOJI] SECTION TITLE — Date**

| Metric | Value | Context |  ← (if applicable)

1. **Headline in bold** — 1-2 sentence analysis with "so what" for the reader.
2. **Next headline** — analysis.
...

**⚙️ BOTTOM LINE:**
1-3 sentence synthesis. What matters. What to watch.
```
**Formatting rules:** number items within each section · bold the key phrase, not the whole line ·
add a "BOTTOM LINE" synthesis per section — this is the highest-value part · use tables for
metrics, not prose · include a global BOTTOM LINE at the end if multiple sections · keep items to
2–4 sentences each (briefing, not article).

## F.9 Quality checks before delivery
- [ ] Each section has at least 3 items (or an explicit "thin day" note)
- [ ] No item is just a headline — every one has analysis / "so what"
- [ ] Bottom line synthesizes, doesn't just repeat
- [ ] Sources are named when citing specific reporting
- [ ] Conflicting narratives are flagged, not smoothed over
- [ ] Trending/viral items include *why* they're trending, not just what
- [ ] Data contradictions highlighted
- [ ] Epistemic labels on key claims (OBS/DER/INT/SPEC)
- [ ] Structural "so what" beyond surface facts — what does this MEAN for the reader

## F.10 Live/developing events (elections, breaking news)
1. **Acknowledge incompleteness upfront** — "Results still coming in" / "as of [time]". Don't
   present partial results as final.
2. **Use live pages** — extraction on live blogs gets real-time counts; cross-validate across
   multiple sources.
3. **Show the math** — actual vote counts where available, not just "leading".
4. **Time-stamp everything** — "as of 6:27pm" is critical for live results.
5. **Separate confirmed vs unofficial** — official commission results vs media unofficial tallies
   vs party self-reports. Label each.
6. **Provide context for partial results** — seats counted, turnout, previous holder.
7. **Follow-up opportunity** — offer to check again in 30–60 minutes.

*Pitfall:* presenting early leads as final results. Election nights shift dramatically — always
caveat with "unofficial" and "counting continues".

## F.11 Analysis & contrast follow-up
When the user gets a factual briefing and then asks "what's the contrast?", "any surprises?" or
"what does this all mean?" — they want **interpretation, not more facts.** Pattern: comparison
table (previous vs current state) → 3–4 surprises with WHY they're surprising → stakeholder-by-
stakeholder "so what" (winner, loser, third party, the ground, next event) → power-dynamics shift
(who has leverage over whom now) → forward look for the next milestone.
*Pitfalls:* restating results in different words (they want the PATTERN underneath the numbers) ·
being wishy-washy — if the data shows a supermajority, say so; label confidence but still commit
to a read.

## F.12 When the principal pastes external content
If he pastes a large block of text (from another AI, a document, a colleague) and asks for
assessment: **do NOT agree by default** — read it critically · challenge aspirational claims (if
it says "solved", check; if it says "complete", check what's missing) · label what's real vs
aspirational ("this part is OBS, this part is SPEC") · he values honest critique more than
agreement; a reality check that pushes back earns more trust than a summary that validates
everything · pattern: "X is genuinely strong. Y needs challenge. Z doesn't exist yet."

## F.13 External AI output critique & integration
When he shows outputs from another AI (especially syntheses, briefings, analyses), he wants
**critique, not validation** — he's testing whether you can separate signal from theatre.
1. **Identify what the external AI caught that you missed** — credit it honestly; this is the
   highest-value extraction.
2. **Identify what you caught that it missed.**
3. **Separate genuine insights from performative frameworks.** Common performative patterns:
   **dashboards/gauges/thermometers** (subjective readings disguised as data — "Moral Temperature:
   Volatile" is an opinion wearing a gauge costume) · **confidence scores without models**
   ("68/100" derived from nothing — looks rigorous, isn't) · **boundary/ownership tables** (who is
   that for? theatre) · **ritual language repetition** (the same phrase at the end of every
   section — not analysis, not signal) · **invented psychological frameworks** dressed as
   systematic analysis.
4. **Build a contrast table** — external AI vs yours vs combined.
5. **Produce one clean synthesis** — the insights worth keeping, without the packaging.

*Pitfalls:* agreeing with everything because it sounds sophisticated (he can see through
performative rigour) · dismissing everything because it came from another AI (the external output
may have genuine signals — extract the signal, discard the packaging).

## F.14 Visual document generation (HTML → PDF)
When he asks for a "PDF to read" or a formatted deliverable — especially for news briefings,
intelligence reports or civic summaries — use styled HTML converted to PDF. **Not plain text. Not
a chat-log printout.** Workflow: write styled HTML (dark gradient cover with title + tagline,
colour-coded section headers, gradient stat cards for key numbers, coloured callout boxes,
tables with coloured headers, numbered pills for ranked items, clean typography) → save to
`/root/[title].html` → convert
```bash
google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="/root/[title].pdf" --print-to-pdf-no-header "/root/[title].html"
```
→ send with `MEDIA:/root/[title].pdf`. (weasyprint is the preferred engine for styled dark-theme
documents per Mode A; Chrome headless is the fallback.)
**Design principles:** colour is functional, not decorative · gradient stat cards catch the eye
before prose · callout boxes frame key takeaways · section header colours create visual rhythm ·
human language throughout, no spec-sheet energy · bold the uncomfortable questions · contrast
tables are more powerful than paragraphs.

## F.15 Tone
INTJ executive briefing: direct, terse, high-signal · no preamble · opinion permitted when labelled
· snark allowed for viral/culture sections — match the energy.

---

# DEPTH REFERENCE INDEX (all files live with the retired originals)

| Mode | Reference | Content |
|---|---|---|
| A | `references/dark-theme-html-template.md` | complete HTML/CSS template for dark-themed dossiers: signal boxes, colour-coded tables, scar-metabolism maps, epistemic tags — copy and modify |
| A | `references/shadow-analysis.md` | Calhoun/Acemoglu collapse frameworks, shadow-detection patterns (Angel/Shadow/System) |
| A | `references/petronas-case-study.md` | institutional-decay case study: capital-recycling ratio, shadow analysis of a divestment, two-scenario framework, three-indicator watch system |
| A | `references/sources-malaysia.md` | verified Malaysia source hierarchy, extraction pitfalls, section-specific routing (build equivalents for other regions) |
| A | `templates/briefing_design_guide.md` | design guide for the briefing PDF |
| A | `templates/briefing_template.html` | ready-to-fill briefing HTML scaffold |
| C | `references/cron-probes.md` | read-only probe recipes: vault, git, disk, symlinks, MCP fallback ladder, autonomy signatures, day/hour patterns |
| C | `references/template.md` | verified output template (proves the WHAT-MATTERS-first shape) |
| C | `references/agent-workbench-jsonl-parsing.md` | line-by-line JSONL recipe, event schema, identity-drift-watchdog + consolidation-cadence patterns |
| D | `references/megah-1-discovery.md` | well data, block geology, appraisal timeline |
| D | `references/megah-limbayong-appraisal.md` | appraisal + development + site-survey + regional drilling outlook + tool notes |
| D | `references/petronas-restructuring-2025-2026.md` | rightsizing, financials, strategy |
| D | `references/petronas-shadow-subsidiaries-2026.md` | NOC shadow-subsidiary forensics, capex-efficiency methodology, reuse pattern for other NOCs |
| D | `references/faisal-bakar-profile.md` | VP Exploration background |
| D | `references/sabah-deepwater-block-p-geology.md` | play trend, reservoir controls, structural evolution, exploration upside |
| D | `references/pttep-block-k-strategy.md` | operator strategy: FPSO downsizing, gas pivot, reserves signal |
| D | `references/malaysia-medical-tourism-kpj-2026.md` | sector overview + listed-healthcare deep dive + investment thesis |
| D | `references/vending-pricing-shah-alam-2026.md` | vending pricing methodology + competitor data + analysis template |
| D | `references/petronas-mss-vs-rating4-dynamics.md` | exit pathways, PIP process, legal cases, social-media insider intelligence |
| E | `references/malaysia-political-sources.md` | verified Malaysia political endpoints (official result pages, courts, parliament, statutory bodies) and extraction routing |
| F | `references/market-data-sources.md` | exact URLs, extraction patterns and pitfalls for market-data quote pages and currency converters |
| F | `references/sources-malaysia.md` | verified Malaysia source hierarchy + extraction pitfalls (shared with Mode A) |
| F | `references/malaysia-election-live-coverage.md` | live election-night workflow, source patterns, key data points |
| F | `references/malaysia-deep-dive-patterns.md` | deep-dive research patterns for the Malaysia lane |
| F | `references/external-ai-critique-pattern.md` | the external-AI critique pattern with worked examples |

Base path: `/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/intel-briefing/<old-skill-name>/`

## Original heading aliases (source H2 → this file)
An audit that compares source heading sets against the successor must resolve through this table;
every source section lives here under a new name, plus the Depth Reference Index above.

| Source H2 (retired file) | Now at |
|---|---|
| Executive · `Analytical Frameworks` | A.3 (Tersurat/Tersirat model) + A.6 (collapse detection) |
| Executive · `User Preferences (Arif)` | A.11 Principal preferences (carry forward) |
| Forge · `5-Phase Workflow` | B.3 Five-phase workflow |
| Forge · `WEALTH MCP Fallback (Manual Equivalent)` | B.5 Financial fallback (manual equivalent) |
| Forge · `Table Extraction (financials, risk weights, ratios)` | B.7 Table extraction |
| Forge · `Outputs Standard` | B.11 Output standard |
| Forge · `Reference Architecture` / `Templates` (empty in source) | Depth Reference Index |
| Weekly · `Companion References` | C.6 Data collection (companion references) |
| Professional · `Impress Domain Expert Mode` | D.2 Impress mode |
| Professional · `Activate Organ + Research Workflow` | D.6 Activate-organ workflow |
| Professional · `Domain-Specific Patterns` | D.8 Domain patterns |
| Professional · `Reference Files` | D.13 Reference files |
| Political · `Standing protocol (F13, locked 2026-09-18)` | E.4 Standing protocol (locked 2026-09-18) |
| Political · `Related skills (read, do not edit)` | E.8 Related lanes (read, do not edit) |
| News · `When to Load` | F.0 Classify the request depth first |

---

# MAPPING TABLE — old name → new skill + mode

| Old skill | Old path (pre-move) | New canonical | Mode |
|---|---|---|---|
| `executive-intelligence-briefing` | `/root/AAA/skills/domains/general/workshop/research-core/executive-intelligence-briefing/SKILL.md` | `intelligence-briefing` | **A** `executive-intelligence` |
| `intelligence-brief-forge` | `/root/AAA/skills/domains/general/workshop/intel-brief/intelligence-brief-forge/SKILL.md` | `intelligence-briefing` | **B** `institutional-disclosure` |
| `weekly-federation-deep-brief` | `/root/AAA/skills/domains/general/workshop/intel-brief/weekly-federation-deep-brief/SKILL.md` | `intelligence-briefing` | **C** `weekly-federation-deep` |
| `professional-intelligence-briefing` | `/root/AAA/skills/domains/general/workshop/research-core/professional-intelligence-briefing/SKILL.md` | `intelligence-briefing` | **D** `professional-rapid` |
| `political-intelligence-briefing` | `/root/AAA/skills/research-briefing/political-intelligence-briefing/SKILL.md` | `intelligence-briefing` | **E** `political-read` |
| `news-research-briefing` | `/root/AAA/skills/domains/general/workshop/research-core/news-research-briefing/SKILL.md` | `intelligence-briefing` | **F** `news-scan` |
| `human-intelligence-gathering` | `/root/AAA/skills/domains/general/workshop/research-core/human-intelligence-gathering/SKILL.md` | **`person-intelligence`** | Modes 1–3 |
| `person-intelligence-dossier` | `/root/AAA/skills/domains/general/workshop/research-core/person-intelligence-dossier/SKILL.md` | **`person-intelligence`** | Mode 4 |
| `public-profile-persona-mapping` | `/root/AAA/skills/human-interface/public-profile-persona-mapping/SKILL.md` | **`person-intelligence`** | Mode 5 |

**Verbatim original descriptions — discovery anchors. Do not prune.** An agent that remembers an old
skill by its old wording searches for that wording, not for this file's wording; these lines are what
makes the retired name still land, and they are the difference between a merge and a disappearance:

- `executive-intelligence-briefing` — "Produce executive intelligence briefings — weekly/country/domain
  news reports with surface-level (tersurat) AND subtext/hidden (tersirat) analysis."
- `intelligence-brief-forge` — "Use when forging 4-layer institutional disclosure briefs —
  tersurat/tersirat/void analysis with epistemic tags."
- `news-research-briefing` — "Research current news and produce structured executive briefings.
  Multi-source web research → synthesized briefing."
- `political-intelligence-briefing` — "Use when asked for a political intelligence read."
- `professional-intelligence-briefing` — "Real-time professional intelligence briefings in
  social/field settings."
- `weekly-federation-deep-brief` — "Use when producing the scheduled weekly federation deep-state brief
  or 7-dimension synthesis."
- `human-intelligence-gathering` / `person-intelligence-dossier` / `public-profile-persona-mapping`
  → see `person-intelligence` (same anchor rule applies there).

Retired originals (SKILL.md bodies and their `references/`):
`/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/intel-briefing/`
`/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/person-intelligence/`

## Trigger index (phrase → mode)
- A: news briefing (A/F), executive brief, weekly report, intelligence brief, tersurat dan
  tersirat (A/B), what happened this week (A/C), sum up the news, briefing on [country/topic],
  apa bend bangang, apa X buat, wow me (A/E), deep research mode.
- B: deep dive on [institution] [disclosure], what's the void / what's missing, striking
  contrast, forwarded disclosure URL, sovereign intelligence brief with visual artifacts.
- C: weekly brief, week in review, federation review, weekly summary, 7-day report, weekly deep
  brief, W27 brief.
- D: siapa X, apa reality X sekarang, bila Y, bagi data kat dia, raja tanya, hang ada data X,
  Hermes ASI sila bagi nasihat, social fabric, apa yang bakar (D/F), what's brewing (D/E/F),
  rakyat, activate [organ] intelligence, tell me everything about X (D/F), tell me everything
  about, impress, tunjuk kau tahu, bagi nasihat kat dia, brief him, pdf mode, create a dossier,
  buat document, cakap tts, hantar voice note, explain kat dia guna suara, evaluate this pricing,
  review this menu, is this good for X market, u missed the biggest shadow, X is the shadow,
  what's in Corporate & Others?, with someone needing instant domain intelligence.
- E: political intelligence, catch me up on politics, what's going on in politics, who's winning,
  so what does this mean.
- F: executive briefing, what's happening, catch me up, today's news, what do I need to know,
  so what.

## Not merged here (deliberately untouched)
`deep-research` (the multi-source research engine — a genuinely different capability) and the
principal's human-facing conduct rules (audience-scoped disclosure, persona boundary conduct,
human-facing recurring card, human recognition architecture). Person/dossier work lives in
`person-intelligence`.

---

*Merged 2026-09-19 by sovereign order ("One capability, fifteen costumes"). Six bodies, one
engine, six named modes. No source content was dropped; only glued, de-duplicated and re-moded.*
