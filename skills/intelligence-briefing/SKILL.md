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
  #
capability_tier: fed-agent-subagent
ecology_state: WARM
# --- executive-intelligence-briefing ---
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
- **Attribute the act to the actor that performed it.** Where the actor is a component party,
  name the party, not the coalition.
- **Sanction ≠ award.** A project FID (investment approved) and the equipment selection (which
  rig, FPSO, contractor) are separate claim states. Vessel/contractor names appearing in
  "likely", "being considered", "strong candidate" reporting are CANDIDATES, not the plan.
  Write "FID taken; FPSO not yet awarded — X is the frontrunner" — never "FID with X". Check
  the vessel's published capacity against the project's stated throughput before pairing them.

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

## Mode references (moved 2026-10-23)

Moved verbatim to `references/`references/modes-a-to-f.md` (2026-10-23) — the full text is preserved there,
not summarised. Read the relevant section before acting:

```bash
grep -n -i "mode OR section OR output" references/modes-a-to-f.md
```

Index of moved sections:

- A.0 When to use
- A.1 Structure (default country-weekly; adjust sections to the domain)
- A.2 Research (parallel)
- A.3 Analysis layer — the Tersurat/Tersirat model
- A.4 Critical segments
- A.5 MakcikGPT mode (ground-level shadow intelligence)
- A.6 Institutional collapse detection (Calhoun + Acemoglu)
- A.7 Risk verdict (closing, traffic-light)
- A.8 Sources & research quality
- A.9 PDF generation (dark theme, cognitive-aligned)
- A.10 Delivery
- A.11 Principal preferences (carry forward)
- B.1 The 4-layer analytical framework
- B.2 Ground / Synthesis schema — mandatory separation, enforced by layout
- B.3 Five-phase workflow
- B.4 Void analysis methodology (highest-signal layer when applied well)
- B.5 Financial fallback (manual equivalent when the capital MCP lane fails)
- B.6 Numeric discipline (mandatory for any technical/regulatory figure)
- B.7 Table extraction
- B.8 Chart QA gate (vision-blind operator)
- B.9 Pitfalls (read before starting)
- B.10 Verification before delivery
- B.11 Output standard
- B.12 Constitutional audit per brief
- C.1 When this runs
- C.2 The 7 dimensions (in order)
- C.3 The closing question
- C.4 Style guide
- C.5 Pitfalls
- C.6 Data collection (read-only, no identity required; run in parallel)
- C.7 Deliverable shape
- 🔥 WHAT MATTERS (5 insights)   [the week in one breath → insights 1..5]
- 📦 VAULT999 SEALS THIS WEEK     | Seal | Date | Actor | Verdict | What happened |
- 📊 GIT ACTIVITY (6 organs)     | Organ | Commits | Peak Day | Quiet? |
- 📋 PENDING WORK                | # | Item | Status this week | F-floor |
- 🛡️ AUTONOMY LEDGER (system self-correction)  | Signal | What happened | Date |
- 📈 SYSTEM EVOLUTION            | Metric | Last week | This week | Trend |
- 🎯 PATTERNS                    Theme 1..4
- 🔮 FOR NEXT WEEK               3 specific things the data is asking for
- ❓ ONE QUESTION                > tight forward question, embedded tension
- D.1 When to use
- D.2 Impress mode (strategic knowledge deployment, NOT a briefing)
- D.3 PDF dossier — the impression escalation
- D.4 Pitfalls (from the 2026-07-07 deepwater session)
- D.5 When NOT to use
- D.6 Activate-organ workflow
- D.7 Core workflow
- D.8 Domain patterns
- D.9 Voice delivery (TTS)
- D.10 Live tool demonstration
- D.11 Pitfalls
- D.12 Output contract
- E.1 Procedure
- E.2 The verification ladder
- E.3 Pre-send figure ledger (mechanical — four questions per number)
- E.4 Standing protocol (locked 2026-09-18) — two checks by DEFAULT on every read
- E.5 Output contract (chat delivery)
- E.6 Pitfalls
- E.7 Scar anchors
- E.8 Related lanes (read, do not edit)
- F.0 Classify the request depth first
- F.1 Parallel delegation (for deep dives)
- F.2 "Everything" requests — include the drama
- F.3 Scope narrowing — go deeper, not just filtered
- F.4 Determine scope
- F.5 Market data extraction (when the brief includes financial data)
- F.6 Source selection & fallback chain — never stop at the first failure
- F.7 Source hierarchy by region
- F.8 Output format
- F.9 Quality checks before delivery
- F.10 Live/developing events (elections, breaking news)
- F.11 Analysis & contrast follow-up
- F.12 When the principal pastes external content
- F.13 External AI output critique & integration
- F.14 Visual document generation (HTML → PDF)
- F.15 Tone

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
