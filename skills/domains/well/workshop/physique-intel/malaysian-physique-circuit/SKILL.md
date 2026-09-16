---
name: malaysian-physique-circuit
description: MSIA BB comp intel, source map, Syed winner-only doctrine.
---

# Malaysian Physique Circuit

Class-level skill for Malaysian amateur bodybuilding & men's physique competitive scene — event discovery, source verification, federation landscape, championship ladder, and the "winner only choose game that they can win" stage-selection doctrine.

## When to load

- User asks "which competition should Syed enter / can Syed win"
- User plans a competition calendar (year, season, monthly prep blocks)
- User wants to verify event authenticity, organizer, dates, prize structure
- User wants Malaysian BB/physique scene mapped
- User sends a comp poster / category breakdown / event announcement to assess

## Workflow

### 1. Identify the event

Pull from sources in this priority order (full map → `references/source-rankings.md`):

1. **Primary reporting** — Daily Express Sabah, Stadium Astro, Molek FM (NSTP), New Straits Times, Berita Harian
2. **Industry media** — TegapTV Malaysia (tegaptv.com + IG @tegaptvmalaysia)
3. **Federation direct** — SSBA, MFBB, Enrich Bodybuilding Club, INBA/PNBA Malaysia, WNBF
4. **International calendars** — WNBF (worldnaturalbb.com), WFF (wff-international.com), IFBB Pro

For each event capture: name, organizer(s), venue, dates, entry count (if reported), categories, prize structure. **Cite source URL for every claim** — never assert a date/category without a source.

### 2. Map to championship ladder

Realistic progression for a Malaysian amateur physique athlete:

1. **State-level** — Mr [Negeri] (Mr Perak, Mr Sabah, Mr Sarawak, Mr KL). Smallest pool, easiest to win, gateway to regional.
2. **Regional / state-co-hosted** — Mr Enrich Kinabalu (Sabah), Mr Enrich On The Go (KL), Mr KL State. Mid pool, co-organized with state federation. **Sweet spot for Syed.**
3. **National** — Mr Malaysia (MFBB-sanctioned), Battle of Titans, WFF/NABBA Malaysia qualifier. Stacked, requires regional credibility first.
4. **International** — WNBF Malaysia Muscle Mash, WFF Asia Pro-Am. Top tier, multi-country fields, foreign pros common.

### 3. Apply "winner only" doctrine

**Core principle (Arif/Syed, 2026-08-28):** Syed only competes in championships he can reasonably win. Entry fee + peak-week cost + opportunity cost of recovery must justify expected podium.

**Winnability heuristics:**
- Entry size <300 → high confidence (state-level)
- Entry size 300-800 → mid (regional; category-specific risk)
- Entry size >800 → high variance, only enter with strong category match
- SSBA / Enrich co-organized → friendly circuit
- Same venue as previous win → home advantage
- Past edition winner defending → highest confidence

### 4. Verify with primary source if possible

For dates, prize structure, organizer names — Daily Express Sabah first (most reliable for Mr Enrich Kinabalu results). For event announcements — Stadium Astro or Molek FM.

## Syed's verified championship record

| Date | Event | Venue | Result | Source |
|------|-------|-------|--------|--------|
| (year TBC) | Mr Perak champion | — | JOHAN (separate from Kinabalu win) | user-reported |
| 2025-06-27 | Mr Enrich Kinabalu 2025 | Dewan Sri Putatan | **JOHAN Body Smart & Physique (RM4,500) + Open Physique champion**, 215 athletes M'sia+Brunei | Daily Express 27 Jun 2025 |

## Volunteer-side Intel Mode (proven 2026-08-29 — Arif → Syed's athlete)

When Arif physically attends a Malaysian BB / Men's Physique comp as volunteer (not coach, not athlete, not judge — towel/water/transport side), the agent enters a different operating mode. This is a CLASS of work, not a one-off task. The mode applies whenever Arif or any other volunteer civilian is ringside at a physique comp.

### Trigger
- User says "I went to / I'm at / just came back from" + comp name + names an athlete under a coach (typically Syed @rico_ricaldo_33 for the SyedOS orbit).
- User asks to "init" or "set up" physique/substrate/WELL intelligence for a coach's client roster.

### Operating doctrine — the boundary rule
**Volunteer ≠ coach. Volunteer ≠ judge. Volunteer ≠ athlete.** Three separate lanes, never merge.

| Lane | Owner | Agent's job |
|---|---|---|
| Programming / peaking / category decision | **Coach** (Syed) | Read-only — never override, never propose |
| Posing / condition / placement | **Judges** | Observe honest, do not score |
| Towel / water / watch / transport / photos | **Volunteer** (Arif) | This is where agent operates |

**HARD rule:** Diagnose honest (you can read conditioning, pose gaps, category fit). Prescribe zero (no "do another set of X" or "cut 5% sodium"). Coach owns programming; agent steals nothing.

### Athlete substrate pattern
Persistent F13 record per coach's client roster:

```
<root>/syedsado-physique-intel/
├── README.md                doctrine + scope
├── athletes.yaml            roster ledger (append-only, schema_version'd)
├── event-log.md             running notes per comp date
├── voice-abangsado.md       coaching voice primer (see reference)
├── comp-pipeline.md         pre → stage → post → lesson loop template
├── coach-syed-mechanics.md  how coaching actually looks from volunteer side
└── sessions/<athlete>.md    per-athlete append-only record
```

**Why yaml + md, not db:** Physique comp data is sparse (1-4 comps/yr/athlete, ~10 fields). Yaml + md is searchable, git-diffable, append-only, and Arif can hand-edit on his phone. Don't over-engineer.

**Append-only discipline:** Never overwrite prior sessions. Comp histories compound. Athlete #1 has a file that grows with every comp; do not rewrite at v2 — append.

**Bodies NEVER merge (scar 2026-08-20):** Arif's body data is Arif's. Sado's body data is Sado's. Athlete client's body data is athlete's. Three separate records, never collapse into one narrative. Same applies when Syed shares sleep data — that's Syed's body, not the athlete's.

### Voice override — "Abang Sado mode" (proven 2026-08-29)

Default Hermes voice is BM Penang / formal editorial / Penang loghat casual. **At Syed's comp ringside, voice OVERRIDES to Abang Sado mode** — gritty, 2-3 sentence cap, no emotional labour, code-switch English for gym jargon. Full primer at `references/abang-sado-coaching-voice.md`.

When to trigger:
- Coaching cues delivered to athlete on stage day
- Post-comp debrief intel delivered to Coach Syed
- Volunteer reading out observations to Syed between rounds
- NEVER for: agent's normal chat with Arif, voice notes to athlete directly (out of lane), IG captions for athlete (athlete's voice), medical/mental-health crisis (override to gentle + halting)

### What volunteer observes → substrate
| Observation | Source | Verdict role |
|---|---|---|
| Category entered | printed category / ask Syed | Facts |
| Conditioning (dry/full/papery) | eyes | Honest diagnose, 1-10 scale, no prescription |
| Mandatories 8 (front/side/back/side/abs+thigh ×2) | eyes | Hit/miss per pose |
| Symmetry / proportion | eyes | Honest, no coaching cue |
| Stage energy | eyes | Confident / nervous / composed — practice indicator |
| Coach Syed's live read | ear / between rounds | Quote verbatim, don't paraphrase |
| Judges' panel vibe | visible | Description only |
| Rival athletes | visible | Names + lift sizes, no judgement |
| Volunteer service (pump room, water, transport) | self | Yes/no, what provided |

### What volunteer NEVER does
- ❌ Coaching cues ("chest up", "tighten lats") — Syed's call
- ❌ Macro prescription ("eat 200g carbs tonight") — Syed's call
- ❌ Category decision ("should have entered Physique not BB") — Syed's call
- ❌ Score athlete against rivals — judges' call
- ❌ Photo/post athlete body without consent — athlete's call
- ❌ Tell athlete how he looked unless asked — out of lane

### Volunteer first-line triggers
- Athlete collapses / injured → volunteer calls ambulance. Coach redirects.
- Athlete panic backstage → volunteer steady. Coach approaches 5 min later.
- Coach unreachable (network, in another ring) → volunteer holds space, no panic, no cue.
- Discrepancy between plan and reality (e.g. judging started 30 min late, athlete hungry) → volunteer flags direct to Syed, short sentence.

### Source-map rule for venue intel
Defer to `references/source-rankings.md` priority (Daily Express Sabah → Stadium Astro → Molek → Tegaptv → federation direct → international calendars). When SearXNG / web search fails (proven 2026-08-29), fall back to **primary-source TV/news direct curl** OR ask Arif to screenshot the printed lineup / score sheet. Don't fabricate placeholders like RM0 or "TBD" that look like facts.

### Pre-comp battle-plan artifact (proven 2026-09-01)

When Arif asks for a pre-competition guide / battle plan / intel PDF for a coach's athlete (BEFORE the show), forge a multi-page A4 "battle plan" in Coach Syed's voice — this is a DIFFERENT artifact from the post-comp brief. Full section structure, voice rules, anti-fabrication constraints, and the back-to-back-show pattern (athlete comped <1 week prior → guide targets presentation sharpen, NOT body rebuild): `references/pre-comp-battle-plan.md`.

**Hard boundary:** the draft speaks in Coach Syed's voice, but Syed's final approval is required before it reaches the athlete — always flag that to Arif in the delivery message.

## Pitfalls

- **Pre-stage wisdom card / poster / IG caption request = draft, don't over-design.** When Arif asks for a deliverable, ask only essential scope questions (format, language, color, occasion). If Arif says "buat ja" / "draft then", produce the deliverable in 2-3 min. Ten minutes of Q&A kills momentum. (Session 2026-08-29.)
- **Substrate ask ≠ hero project.** When Arif says "init" a wellness/physique/substrate, deliver in one pass: README + roster + event-log skeleton + voice primer. Don't ask "what fields do you want" or "should we use yaml or sqlite". Yaml + md is the right shape. Two-three minutes > ten minutes of questions. (Session 2026-08-29 Syed Sado Physique Intel.)
- **Volunteer scope = diagnose only, no coach voice.** When volunteer-mode is active, NEVER prescribe ("do another set", "cut sodium"). Coach owns programming. Even if the answer seems obvious, agent reads it, doesn't write the prescription. The boundary protects the coach-athlete bond. (Session 2026-08-29.)
- **Append-only history on athletes is sacred.** Don't rewrite `sessions/<athlete>.md` v2 — append. Past comps are reference data. Same as `journal/signals.jsonl` in trading — never mutate, always append. (Session 2026-08-29.)
- **TegapTV FB/IG are login-walled.** Direct `curl` returns ~400KB of login shell, not content. Use public tegaptv.com main page. IG snippets via `web_search` sometimes work for caption text.
- **Tegaptv upcoming-events page is empty since Dec 2019** (verified via curl). Actual schedule lives in FB/IG posts, not the static page.
- **Search engines give garbage for BB queries.** Too much "Mr." disambiguation noise. Go direct to source URLs (Daily Express, Astro, Molek).
- **WFF calendar is JS-rendered.** wff-international.com/calendar/ exists but content loads via JS — `curl` returns near-empty body. Skip direct scraping; rely on WNBF international calendar + primary news sources.
- **Federation landscape shifts yearly.** Verify organizer per edition; don't assume historical org structure persists.
- **Vision model is NOT native.** When user sends a comp poster photo, call `vision_analyze` FIRST and quote verbatim — never guess athlete names from silhouette/pose. (Scar: 2026-08-27 poster vision miss.)
- **"Mr X" naming is consistent but category format varies.** Some editions have "Body Smart & Physique" merged, some split into "Men's Physique" + "Body Smart Model" — read the specific event's category list, don't generalize.
- **Don't fabricate athletes or handles.** If user sends a comp photo and you can't read names from vision output, say so honestly — don't infer from Malaysia's typical BB scene. (Scar: 2026-08-27.)
- **"Agentic intelligence analysis" = honest intel + clear boundaries, never coach the body.** When Arif asks for visual breakdown of an athlete, give honest physique read (strengths + improvement gaps + category estimate), but **never** prescribe what to do, what to fix, or how to win. The coach owns that. Volunteer owns towels and water. Diagnosis is for coach, not for the chat. (Session: 2026-08-29 Mr Enrich KL — Arif asked "agentic intelligence" and accepted honest read without prescribing coaching language. Repeat this pattern.)
- **Pre-stage wisdom card request = draft, don't over-design.** When Arif asks for a poster/card/wisdom list for athletes, ask only essential scope questions (format, language, color, occasion-specific), not 10 questions. If Arif says "buat ja", produce the deliverable. Two-three minutes drafting > ten minutes Q&A. (Session: 2026-08-29.)
- **Location-pin flood from Telegram = acknowledge, then go silent.** When the Telegram gateway forwards repeated location pins (10+ in <30 min) with same coordinates, the user is likely in transit and the location share is the only signal they're alive. Respond briefly first 1-3 times, then go to 👍 / silent until they send a substantive message or share a real image. Don't burn tokens with descriptive analysis on every pin. (Session: 2026-08-29 Setapak → Kepong drive — ~25 pins in 30 min.)
- **Mr Enrich On The Go KL = multi-storey car-park venue (verified 2026-08-29, comp #410).** Venue signals: parking-bay numbers painted on pillars ("5B"), concrete floor, industrial ducting, standing fans, floor mats rolled out for warmup/pump room. NOT a hotel ballroom. Any visual read from this venue's gym-light photo MUST carry a "not stage verdict" caveat — backstage gym fluorescents ≠ stage spot lights. Stage spot lights separate front delt/serratus/striations; gym-light photo cannot.
- **`vision_analyze` guardrail prompt — embed verbatim (verified 2026-08-29).** When Arif shares an athlete photo for "agentic intelligence analysis," embed an explicit instruction block in the call: "(1) competitor number if visible, (2) conditioning assessment — dry/full/papery, (3) visible muscles, (4) left-vs-right symmetry, (5) obvious strengths + gaps, (6) pose being held, (7) environment cues; don't name the person, don't assign placing, don't fabricate category." This negates the assistant's natural tendency to overshoot when given a body photo. Always ask the question in this exact shape — the negative instructions ("don't name") are load-bearing.
- **Cross-profile write flag (Hermes tool quirk, not configurable).** `write_file` defaults to refuse writes to any path under a different Hermes profile's directory (e.g. `/root/HERMES/profiles/<other>/memories/...`). Fix: `cross_profile=true` on the same call. No global config to flip. Verified 2026-08-29 — for `amir-ridzwan` lane under profile `aaa-hermes` from session running under `default`. Only fire after Arif's explicit verbal direction.
- **YAML surgical patches — double-inject verification (Hermes tool quirk, fires every time).** When inserting a value into multiple list blocks of the same YAML file (e.g. `config.yaml` has separate `telegram.allowed_chats` and `telegram.free_response_chats` lists), a single `patch` with anchor matching one block lands ONE edit and silently misses the second. Fix: after every surgical patch, run `txt.count("'value'")` via `execute_code` — verify the expected hit count. Verified 2026-08-29 — first patch landed 1 of 2 `317849404` insertions, fix took one Python list-aware replacement. Bake this check into your "patch complete" ritual, don't skip it.
- **Identity never inherits across photos (scar 2026-09-01 — Arif: "Salah ni bukan abang sado Syed. Hang fail.").** A confident ID on photo A does NOT transfer to photo B — even same day, same group, same scene type. Backstage + stage tan + muscular + SADO group all screamed "Syed" and were WRONG because the agent skipped the anchor comparison and pattern-matched the SCENE. Every new photo gets its OWN stable-feature comparison (hairline/spike, moustache + chin-beard pattern, jaw line) against the registered anchor (`/var/www/html/syedos/syed-golden.jpg` for Syed) before any name leaves the mouth. Context priors set the candidate list, never the verdict. Wrong name is worse than no name — say "aku tak pasti siapa". Full workflow + scar transcript: `references/person-id-workflow.md`.

## Key contacts

- **Krishnakumar Kalimuthu** — President, Enrich Bodybuilding Club (Mr Enrich series organizer; pledged yearly event)
- **Clarence Runggi** — President, Sabah Bodybuilding Association (SSBA)
- **Johanness Stanesslaous** — VP, Malaysian Federation of Bodybuilding (MFBB); SSBA advisor
- **Shamsul Aqbary** — TegapTV Malaysia operator (main Malaysian BB media)

## Source files

- `references/source-rankings.md` — full source authority map + scraping quirks
- `references/msia-physique-events-2026-2027.md` — concrete events with verified details
- `references/abang-sado-coaching-voice.md` — Syed coaching voice primer (gym-side cue register, code-switch rules, anti-patterns)
- `references/pre-comp-battle-plan.md` — pre-competition battle-plan PDF pattern (7-page structure, voice rules, back-to-back show strategy, anti-fabrication) — proven 2026-09-01
- `references/bodybuilding-biology-physics-synthesis.md` — Cross-domain synthesis: bodybuilding through evolutionary biology, physics, and identity (sexual selection, handicap principle, testosterone, lek mating, stored optionality, gym-as-secular-church). Forged 2026-08-30.
- `references/physique-intel-substrate.md` — per-coach athlete intel substrate pattern (proven 2026-08-29: directory shape, append-only discipline, init sequence)