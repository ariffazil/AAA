---
name: youtube-multimodal
description: "Unified YouTube multimodal intelligence — one entry point for ANY YouTube URL. Auto-routes: transcript cascade then visual frame analysis then EUREKA 11-part digest then multimodal fusion. Handles VPS bot-wall honestly. Replaces the need to choose between youtube-content youtube-eureka youtube-analysis."
tags:
  - youtube
  - multimodal
  - transcript
  - vision
  - eureka
  - analysis
  - media
  - unified
version: 1.0.0
triggers:
  - "Any YouTube URL shared"
  - "transcript or summarize request"
  - "EUREKA or insights request"
  - "identification request"
  - "visual analysis request"
  - "Any task requiring YouTube intelligence"
related_skills:
  - ocr
  - ai-media-generation
  - humanizer
  - temporal-awareness
  - frontier-model-audit-verification
---

# YouTube Multimodal Intelligence

## The One Rule

**One URL in. One unified pipeline. Right answer out.**

The agent does NOT choose between acquire or analyze or visual. The pipeline
figures out what the video IS and routes accordingly.

---

## Pipeline Overview

```
YouTube URL
    |
    v
IDENTIFY (oEmbed - free, instant, no bot wall)
    |
    +---> Intent is identification only? -> oEmbed + vision on thumbnail -> DONE
    |
    v
ACQUIRE (S0 cache -> S8 TranscriptAPI -> cascade)
    |
    +---> Has transcript? -> EUREKA 11-part digest (Step 3a)
    |
    +---> No transcript?  -> Visual frame analysis (Step 3b)
    |
    +---> Both available?  -> Multimodal fusion (Step 4)
    |
    v
DELIVER (format per request + VAULT999 anchor)
```

---

## Step 1: IDENTIFY (always first, free, instant)

```bash
curl -sf "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json"
curl -sf "https://noembed.com/embed?url=https://www.youtube.com/watch?v=VIDEO_ID"
```

Returns: title, author_name, author_url, thumbnail_url.

**If identification-only** (siapa, who is what):
- vision_analyze the thumbnail_url
- Cross-check against local identity references
- DONE. No transcript needed.

**If deep analysis needed:** continue to Step 2.

---

## Step 2: ACQUIRE (transcript cascade)

```bash
python3 /usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/media/youtube-multimodal/scripts/fetch_router.py "VIDEO_ID_OR_URL"
```

Cascade stages (stop at first success):

| Stage | Method | Cost | VPS |
|-------|--------|------|-----|
| S0 | Cache hit | FREE | Always |
| S8 | TranscriptAPI.com | 100 free/mo | Proven |
| S1 | youtube-transcript-api direct | FREE | Blocked |
| S2 | yt-dlp subtitles | FREE | Bot wall |
| S4 | yt-dlp + cookies | FREE | If valid |
| S5 | User paste | FREE | Fallback |
| S6 | Supadata.ai | 100 free/mo | Alt hosted |
| S7 | Composio | Per-call | OAuth needed |

**Required env:** TRANSCRIPT_API_KEY (sk_*) in /root/.secrets/kunci-mas.env for S8.

**JSON parsing trap:** Segments live under transcript.segments NOT top-level data['segments']. Trust transcript.segment_count and transcript.full_text.

---

## Step 3a: TEXT ANALYSIS (transcript exists)

Apply the EUREKA 11-Part Output Contract:

| # | Part | Content |
|---|------|---------|
| 1 | Executive Summary | Title + URL; core thesis 1-2 sentences; signal density High/Medium/Low |
| 2 | Timeline Breakdown | Chronological topic map with [HH:MM:SS] timestamps |
| 3 | Key Eureka Insights (3-5) | Baseline then shift then verbatim quote then strategic application |
| 4 | Strategic Usefulness Matrix | Table: Takeaway, Actionability, Impact, Novelty, WSU |
| 5 | Truth and Verification | Source authority, domain type, causality vs correlation |
| 6 | Operational Blueprint | Human Decision (taste) vs AI Task (solver) |
| 7 | Verbatim Quotes (max 3) | [HH:MM:SS] exact quote |
| 8 | Resources and References | Books, papers, tools, repos mentioned |
| 9 | Speaker and Persona Map | Roles, perspectives, tone |
| 10 | Objective Notes and Caveats | Biases, fallacies, sponsor conflicts |
| 11 | Strategic Classification | Domain axes (Mind/Body/Soul x Technology/Health/Ethics) |

**Rules:** Nominalism only. Timestamp accuracy required. Zero filler.
**Chunking:** Transcript over 50K chars -> split into 40K chunks with 2K overlap.

---

## Step 3b: VISUAL ANALYSIS (no transcript / music-only)

S8 "No transcript available" = no caption track. Do NOT retry. Pivot to frames.

### Frame extraction (free, never bot-walled)

```bash
VIDEO_ID="..."
mkdir -p /tmp/yt_frames
for i in 1 2 3; do
  curl -sf "https://i.ytimg.com/vi/${VIDEO_ID}/hq${i}.jpg" -o "/tmp/yt_frames/hq${i}.jpg"
done
curl -sf "https://i.ytimg.com/vi/${VIDEO_ID}/maxresdefault.jpg" -o "/tmp/yt_frames/poster.jpg"
ls -la /tmp/yt_frames/
```

### Frame analysis (per frame)

Run vision_analyze on hq1.jpg, hq2.jpg, hq3.jpg independently.

| Field | What to look for |
|-------|-----------------|
| Action | What the person is doing |
| Subject | Who is featured, clothing, build, ethnicity |
| Setting | Location type, lighting, background |
| Text overlays | Watermarks, subtitles, branding |
| Equipment | Specific tools, instruments, props |
| Timestamp estimate | 25%, 50%, or 75% position |

**hq1/hq2/hq3 = real video frames. maxresdefault = marketing poster.**
Always analyze video frames BEFORE poster. Poster can lie.

---

## Step 4: MULTIMODAL FUSION (transcript AND frames)

When both available, cross-reference:

1. Transcript timestamp to frame alignment (25%/50%/75%)
2. Visual confirmation of spoken claims
3. Poster-vs-transcript mismatch detection
4. Identity triangulation: oEmbed name + transcript self-ID + visual appearance

Add a CROSS-MODAL section to the EUREKA digest:

```
## Cross-Modal Analysis

| Transcript Claim | Visual Evidence | Confidence |
|-----------------|-----------------|------------|
| "Today we are doing shoulders" | hq2 shows lateral raises | CONFIRMED |
| "This is my competition shape" | hq1 shows stage-ready conditioning | CONFIRMED |
```

---

## Metadata Recovery (when yt-dlp bot-walled)

```bash
# oEmbed (always works)
curl -sf "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json"

# Wayback CDX (historical)
curl -sf "https://web.archive.org/cdx/search/cdx?url=youtube.com/watch?v=VIDEO_ID&output=json&limit=20&filter=statuscode:200"
curl -sf "https://archive.org/wayback/available?url=youtube.com/watch?v=VIDEO_ID"
```

---

## Output Formats

| Format | When | How |
|--------|------|-----|
| **EUREKA compact** | Default for analysis (Arif-preferred) | 4-part variant below |
| EUREKA full | Deep research / external deliverable | 11-part contract |
| Summary | Quick overview | 5-10 sentences |
| Chapters | Topic-by-topic | Timestamped shifts |
| Thread | Twitter/X | Posts under 280 chars |
| Blog post | Full article | H2 sections + quotes |
| Identification | Who is this? | oEmbed + vision |
| Visual report | Music-only | Frame-by-frame |
| Shadow analysis | "Why did he say that?" / "Map the incentives" | Step 5 below |

### EUREKA Compact (Arif-preferred, 4-part variant)

This is the default format for YouTube digests in Hermes sessions. Compact,
actionable, BM+EN mix, casual synthesis. Use the full 11-part only when
delivering external research or when the user explicitly asks for depth.

**Header metadata block:**

```
[YOUTUBE MULTIMODAL PIPELINE: EUREKA DIGEST]
Route: Transcript Acquired -> Routed to Structured Digest (F2 Validated)
Source: <Channel> <Video Title> (Published: <date>)
Authority: <Speaker name and title>
Temporal Anchor Check (F4): <relative time context, e.g. "Broadcast 4 months ago; forecasts now active">
```

**4 parts:**

```
1. THE KERNEL (Inti Pati)
   One paragraph. The single most important thing said. Who, what, stakes.

2. METABOLIZED INSIGHTS (Truth Grounding)
   3-5 bullet points. Each: baseline assumption -> shift/evidence -> quote with timestamp.
   Focus on structural realities, not opinions. The "what most people don't understand" layer.

3. VITAL SIGNALS & RISK (F1)
   Concrete risk indicators, operational shifts, regional comparisons.
   What changed in the world because this person said these things.

4. SYNTHESIS (Relaks tapi tajam)
   BM casual voice. Explain to a friend at mamak.
   "Macam ni cerita dia..." format. No jargon. Direct.
```

**Rules for compact format:**
- Timestamps in brackets: `[HH:MM:SS]`
- Speaker quotes inline, not blockquoted
- BM+EN mix natural, never forced
- Synthesis section is conversational, not analytical
- No filler. No bullet points in the SYNTHESIS.
- Include F2 epistemic labels on key claims when stakes are high
- If the video is political/institutional, always include the Shadow Analysis
  (Step 5) as a separate section after SYNTHESIS.

---

## Error Handling

| Pattern | Diagnosis | Action |
|---------|-----------|--------|
| S8 404 No transcript available | No caption track | Pivot to visual |
| S8 408 | Transient timeout | Retry once |
| S1 Blocked + S2 bot-wall | VPS IP block | Use S8 or S4 |
| All stages failed | No path | Ask user paste (S5) |

**Never fabricate transcript content. F2 TRUTH is absolute.**

---

## Comments (separate pipeline)

Transcripts do not equal comments. Comments use InnerTube curl recipe.
Logged-out cap: 60-70% of reported count. See youtube-eureka references for full recipe.

---

## Cache Management

```bash
python3 /usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/media/youtube-multimodal/scripts/cache.py list
python3 .../scripts/cache.py get VIDEO_ID
python3 .../scripts/cache.py clear --video-id VIDEO_ID
```

Cache root: /root/.cache/youtube-content/<video_id>.json
Each entry includes SHA-256 for VAULT999 anchoring.

---

## Identity Verification (namesakes)

When video subject shares a name with someone in federation memory:
1. Does physique/age match?
2. Does video timestamp align?
3. Does location match?
4. Any direct identifier?

State match probability honestly (30-50%). F2 requires epistemic tags.

---

## Pitfalls

### skill_manage directory stomping (proven 2026-08-09)

`skill_manage(action='create')` may recreate the skill directory, **killing any manually-placed `scripts/` and `references/` subdirectories**. Correct workflow:

1. `skill_manage(action='create')` — creates SKILL.md only
2. **Then** `mkdir -p` + `cp` for scripts/references — AFTER the skill exists
3. **Or** use `skill_manage(action='write_file')` for each reference file — this appends without stomping

Do NOT place files in the skill directory before calling `skill_manage(action='create')`.

### JSON parsing trap

Segments live under `transcript.segments` NOT top-level `data['segments']`. Trust `transcript.segment_count` and `transcript.full_text`.

### Script path references

When a unified skill copies scripts from a predecessor, update ALL path references in SKILL.md to point to the unified skill's own `scripts/` directory — not the predecessor's path.

### Comments ≠ Transcripts

`yt-dlp --write-comments` → bot-wall. Comments use InnerTube curl recipe. See `references/innertube-comments-extraction.md`. Logged-out cap: 60-70%.

---

## Constitutional Doctrine

- F2 TRUTH: never invent transcript content. Empty = empty.
- F4 CLARITY: every stage records attempt and outcome. Delta S at most 0.
- F7 HUMILITY: confidence cap at 0.90. Visual-only ceiling is Medium.
- F11 AUDITABILITY: cache JSON includes cascade_history.
- F13 SOVEREIGN: user chooses cookies (S4) or paste (S5). No silent escalation.

---

## Step 5: SHADOW ANALYSIS (incentive mapping)

**Trigger:** User asks "kenapa dia buat interview ni?", "propaganda ke?", "map the incentives",
"why did he say this?", "what's the real motive?", or any variant of
"what's the shadow behind the surface?"

**When to include automatically:** If the video features a political figure,
institutional leader, or corporate spokesperson making a public statement
during a crisis — always include a brief Shadow Analysis after the SYNTHESIS.
The user should not have to ask.

### The 7-Layer Incentive Stack

Map every layer. Not all apply to every video — skip empty layers with a note.

| Layer | Question | What to look for |
|-------|----------|-----------------|
| **1. Narrative Inoculation** | What attack is being pre-empted? | The speaker addresses a criticism BEFORE it goes viral. Defensive framing. |
| **2. Soft Warning** | What is being said indirectly? | Repeated reassurance = underlying concern. "Don't worry" = worry. |
| **3. Policy Seeding** | What future policy is being prepared? | Comparison with other countries, "burden is growing" language, subsidy talk. |
| **4. Institutional Mythology** | How is the speaker building legacy? | Historical parallels, origin stories, "we survived every crisis." |
| **5. Market Signal** | Who is the hidden audience? | Vagueness = strategic secrecy for competitors. Specificity = signal to partners. |
| **6. The Silences** | What was NOT said? | Missing topics are as revealing as present ones. List the absences. |
| **7. Venue Choice** | Why THIS channel, not another? | State media vs international outlet = domestic audience. Conference vs TV = technical audience. |

### Output format for Shadow Analysis

```
## Shadow Analysis — <topic>

### The Surface Narrative
<What the speaker says they're doing>

### The Incentive Stack

| # | Incentive | Who Benefits | Urgency |
|---|-----------|-------------|---------|
| 1 | <incentive> | <beneficiary> | 🔴/🟡/🟢 |

### The Silences
<List of what was NOT said and why it matters>

### Bottom Line
One paragraph. Direct. No ceremony. What is this person ACTUALLY doing and why now?
```

### Pitfall: don't over-read

Not every interview is 4D chess. Some are genuine public information.
The test: **does the speaker have something to lose by NOT doing this interview?**
If yes = strategic communication. If no = genuine information.
If unclear = present both interpretations with confidence tags.

---

## Step 6: PHYSICAL CONSTRAINT ANALYSIS (the7 questions)

**Trigger:** User asks "what is he actually hiding?", "what physical reality does this
interview obscure?", "map the operational constraints", or any variant of
"go deeper than the narrative — what's the real system state?"

**When to use:** After Step 5 (Shadow Analysis) when the user wants to move from
INCENTIVE mapping (why he said it) to CONSTRAINT mapping (what he can't say).

**This is sovereign-grade analysis.** It requires cross-referencing the transcript
claims against external data (financial reports, production data, market data,
operational knowledge). Not every question can be fully answered — honest gaps
are intelligence too.

### The 7 Physical Constraint Questions

| # | Question | What It Probes | Data Sources |
|---|----------|---------------|-------------|
| **Q1** | Physical Burnout Rate | How many days of inventory exist before refineries hit minimum operating levels? What is the yield penalty for off-spec crude blending? | SPR data (often classified), refinery yield specs, IEA 90-day benchmarks |
| **Q2** | Sourcing Arbitrage | What is the total landed cost penalty for alternative supply routes (base + freight + war-risk insurance + spot margin)? | AIS ship tracking, Baltic Exchange freight rates, Lloyd's war-risk premiums, spot market spreads |
| **Q3** | Planning Horizon Compression | What operational thresholds cause planning to compress from 90→45→15 days? What triggers emergency rationing? | IEA rationing triggers, historical precedent (1973, 1990, 2022 EU gas), government press releases |
| **Q4** | Counterparty Insolvency | At what price point do non-dominant distributors face liquidity crisis under reimbursement lag times? | APM margin data, distributor working capital ratios, government subsidy reimbursement timelines |
| **Q5** | Capex-Dividend Cannibalization | How much dividend extraction before upstream exploration/maintenance drops below decline-curve threshold? | Annual reports (capex vs dividend), decline curve analysis, sustaining capex benchmarks |
| **Q6** | Industrial Cascade | What is the operational runway for non-energy sectors (semiconductors, agriculture) before supply chain disruption? | Helium supply chain data, fertilizer import dependence, buffer stock estimates, planting season calendars |
| **Q7** | Demand Destruction Mathematics | What price hike or quota ceiling forces meaningful consumption reduction? What is the smuggling tolerance threshold? | Price elasticity research (short-run vs long-run), cross-border fuel price differentials, smuggling enforcement data |

### How to execute

1. **Extract claims from transcript** — what did the speaker assert about each parameter?
2. **Cross-reference with external data** — financial reports, market data, government statistics, industry benchmarks
3. **Calculate the gap** — difference between claimed and actual
4. **Assess confidence** — what can be verified vs what remains opaque
5. **Map the trajectory** — is the situation improving, stable, or deteriorating?

### Output format

```
## Physical Constraint Analysis — <topic>

### The7 Questions

| # | Question | Claimed | Actual | Gap | Confidence |
|---|----------|---------|--------|-----|------------|
| Q1 | Physical Burnout | <claim> | <data> | <delta> | 🟢/🟡/🔴 |

### The Opaque Constraints
<List of parameters that CANNOT be answered from public data — these are the
most important findings, because opacity itself is intelligence>

### The Doom Loops
<Identify any self-reinforcing negative cycles — e.g., capex cut → production
decline → more imports → higher subsidy → more capex cut>

### Assessment
One paragraph. What is the ACTUAL physical state of the system, stripped of
all narrative framing?
```

### The Agentic Rule

Human observers ask: "Did he give a good answer?"
Agentic intelligence asks: "What physical constraint is he preventing me from calculating?"

The answer to that question IS the intelligence.

### Pitfall: not all7 apply to every video

Some interviews are about policy, not operations. Some speakers don't have
operational constraints to hide. Apply the framework selectively — use the
questions that are relevant to the domain. A music video won't have Q5
(capex-dividend cannibalization). A political speech might have Q7
(demand destruction) but not Q1 (burn rate).

### Reference: worked example

See `references/physical-constraints-astroawani-2026-04-03.md` for a full
worked example applying all7 questions to the Petronas energy crisis interview.

---

## Step 7: LINGUISTIC DECODE + SHADOW PROFILING

**Trigger:** User asks "why does he speak like that?", "this feels scripted",
"map the body language", "profile the human behind the institution", or any
variant of "decode HOW he speaks, not just WHAT he says."

**When to use:** After Steps 5-6 when the user wants to understand the PERSON
behind the institutional performance.

### The Linguistic Decode Framework

Analyze the transcript for these patterns:

| Pattern | What to look for | What it reveals |
|---------|-----------------|----------------|
| **Code-switching** | When does speaker switch languages? What phrases are in which language? | Professional identity, audience segmentation, natural register |
| **Precision mask** | Are numbers precise but operations vague? | Training background (accountant vs engineer vs politician) |
| **Deflection formula** | Does every tough question follow the same answer structure? | Media training level, comms team sophistication |
| **Historical anchoring** | Does speaker reference past crises/institutions repeatedly? | Legacy building, institutional mythology |
| **Emotional flatline** | Is there zero personality leak over the full duration? | Degree of institutional consumption of personal identity |
| **Status signaling** | Does sentence complexity correlate with claimed authority? | Language as class marker, institutional hierarchy |

### Shadow Profiling (the13-shadows method)

When profiling a human behind institutional performance, map these dimensions:

1. **Professional identity gap** — What was their training vs what their role requires?
2. **Appointment context** — Crisis hire or growth hire? What was the mandate?
3. **Educational formation** — Where were they trained? What system shaped their thinking?
4. **Social position** — Title, lineage, class — what protections does this confer?
5. **Split loyalty** — Who else do they serve beyond the stated institution?
6. **Precision patterns** — What do they give exact numbers for vs what they vague about?
7. **Shield numbers** — What recurring statistic do they deploy as rhetorical armor?
8. **Mythology construction** — What origin story or historical narrative do they repeat?
9. **Deflection architecture** — How do they structure non-answers to sound like answers?
10. **Competitive containment** — How do they position rivals/partners in their narrative?
11. **Body language signals** — Pauses, fillers, speech length changes at topic transitions
12. **Involuntary confessions** — What admission did they make without realizing it?
13. **The glass wall** — What is the distance between their language and the audience's?

### Output format

```
## Shadow Profile — <person name>

### Linguistic Fingerprint
<2-3 paragraphs on code-switching, precision patterns, deflection style>

### The13 Shadows

| # | Shadow | Core Tension |
|---|--------|-------------|
| 1 | <name> | <one-line tension> |

### The Human Behind the Wall
<Final paragraph: empathetic, direct, no judgment. Who is this person when
the institution is stripped away? What is the tragedy or comedy of their position?>
```

### Pitfall: empathy without endorsement

Shadow profiling is NOT character assassination. The goal is to understand
the human constraints that produce the institutional performance. Every
person behind a glass wall is also a person with limited choices.

Present shadows as TENSIONS, not verdicts. The13th shadow should always
be the most human — the one that makes the reader feel something beyond
analytical satisfaction.

### Reference: worked example

See `references/shadow-profile-tengku-taufik-2026-08-09.md` for a full
worked example applying linguistic decode +13-shadow profiling.

---

## The Zen

One URL in. The pipeline discovers what it is. It acquires what it can.
It analyzes what it has. It fuses what aligns. It shadows what conceals.
It never pretends to know what it did not see.

DITEMPA BUKAN DIBERI.
