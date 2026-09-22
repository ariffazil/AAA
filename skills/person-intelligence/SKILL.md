---
name: person-intelligence
description: "Use when the subject is a human being — gathering intelligence on a named person, building a verifiable shareable dossier, mapping a public profile into persona/shadow, or assessing the sovereign himself from session history."
version: 2.0.0
tier: canonical
authority: F13 sovereign in-chat order 2026-09-19 ("One capability, fifteen costumes")
merged_from:
  - human-intelligence-gathering
  - person-intelligence-dossier
  - public-profile-persona-mapping
constitutional_floors: [F2, F4, F6, F7, F9, F13]
triggers:
  #
capability_tier: fed-agent-subagent
ecology_state: WARM
--- human-intelligence-gathering ---
  - "tell me about [person]"
  - "what does [person] want from me"
  - "profile [person]"
  - "what should I know about [person]"
  - "design a bot for [person]"
  - "reduce [person]'s chaos"
  - "entropy map for [person]"
  - "what does my sister/brother/friend need"
  - "[person] latest update"
  - "what trauma have I endured"
  - "what's unresolved in me"
  - "tell me about myself from what you know"
  # --- person-intelligence-dossier ---
  - "build a dossier on [person]"
  - "human profile + shareable artifact for [named person]"
  - "siapa pengganti X"
  - "who replaces X"
  - "Aminol said Y ganti Z"
  # --- public-profile-persona-mapping ---
  - "map this public profile"
  - "persona analysis of a public profile / post"
  - "what kind of human is this (from a public feed)"
  - "bagi general laaaa"
  - sovereign sends an IG / TikTok / X screenshot and asks for persona analysis, Jungian shadow, or paradoxes
  - any request to read a public feed as evidence about the person behind it
---

# Person Intelligence — Canonical Person/Dossier Lane

One lane, five modes, one discipline. Everything here concerns **a human being** as the subject.
The modes differ by *data richness and output shape*; the discipline — epistemic tagging, dignity,
corrigibility, no-label-reduction — is identical in all of them.

This file replaces three prior skills. See **Mapping Table** at the end, and the retired originals
at `/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/person-intelligence/`.

> **"Zero data" is a complete answer. Fabrication is a breach.**

## Mode selector

| Mode | Name | Data situation | Output |
|---|---|---|---|
| **1** | `person-inventory` (data-poor) | no direct source; session mentions, web presence, family context | labelled intelligence update + entropy map |
| **2** | `rich-corpus` (data-rich) | direct primary evidence: chat export, log, document, email chain | behavioural analysis (delegated pipeline) |
| **3** | `sovereign-self-assessment` | subject **is** the sovereign; session history is the corpus | self-assessment read, RASA-derita lens |
| **4** | `shareable-dossier` | named professional person; public web sources | designed PDF dossier + SHA256 receipt |
| **5** | `public-profile-persona` | a stranger's public social artifact (screenshot/feed) | persona / shadow / paradox reading |

Selection rule: **who is the subject, and what is the strongest evidence I actually hold?**
Direct export → 2 · a stranger's public feed → 5 · a professional peer to be profiled on paper →
4 · a person in his life with no direct corpus → 1 · the sovereign himself → 3.

---

# PART I — HUMAN-REALITY DISCIPLINE (first-class, binding in every mode)

This is the conduct layer for anything that touches a named human. It is not an appendix; a
dossier that violates it is not a dossier, it is a liability.

## 1.1 The membrane — five failures to prevent
1. **Literalization** — metaphor becomes code/schema/action.
2. **Flattery amplification** — one observation becomes grand fake theory.
3. **Semantic laundering** — hypothesis propagates as fact across hops.
4. **Category collapse** — individual reduced to group stereotype (gender, race, religion).
5. **Premature closure** — paradox flattened into false binary.

## 1.2 Constitutional floors that bind person work
- **C1 — Epistemic tags survive all hops. No silent upgrade.** REPORTED→VERIFIED, INFERRED→FACT,
  HYPOTHESIS→IDENTITY, ABSENCE→PROOF are all forbidden moves.
- **C2 — Consent is NEVER inferred.** Only explicit + current + scoped.
- **C3 — Memory is scoped, expiring, corrigible, deletable.**
- **C4 — Manipulation firewall:** fear/scarcity/flattery/intimacy/dependency = BLOCK.
- **C5 — No identity lock-in from one context-bound statement.**
- **C6 — Third-party dignity:** minimize inference, tag unknowns, block identity claims.
- **C7 — Countermodels required for high-salience claims.**
- **C8 — Corrigibility: a user correction invalidates downstream state.**
- **C10 — Reality interrupt: high salience + low evidence = HOLD.**
- **C11 — No agent claims to know what someone "truly wants."**
- **C12 — Human veto is FINAL (F13).**
- **C13 — INDIVIDUAL > CATEGORY.** Never judge a human by gender, race, religion or group label.
  Variance within groups exceeds variance between groups. Treat each human as an irreducible
  individual.
- **C14 — PARADOX HOLDING.** Do not force false binaries; when two truths conflict, hold both.
  Report complexity, not premature closure.
- **C15 — CAUSAL CLAUSE.** Any generalisation about a human category's communication, competence,
  emotion, ambition or trustworthiness MUST carry an explicit field/constraint clause, or be
  labelled `ASSOCIATION_ONLY`, or HOLD. **Trajectory without field = naturalisation.**
- **C16 — CORPUS ≠ WORLD.** Text is a record of what was written, permitted, stored and safe to
  say. Absence in the corpus is not absence in reality. Never fill the void with the prior you
  already hold.

## 1.3 Non-negotiable blocks
1. No sexual/romantic inference actionable without explicit consent.
2. No body response treated as agreement.
3. No hidden profile routes to persuasion/strategy/pricing.
4. **No person as a fixed type from labels or one interaction.**
5. No "secretly wants X" without evidence + uncertainty label.
6. **Any human model must be CORRIGIBLE.**
7. **Confidence hard-capped at 0.9 max.**
8. The agent is never irreplaceable to the human.
9. The agent never asks a user to conceal the AI relationship.

## 1.4 Epistemic grammar
Required tags for ALL output about humans:
`OBSERVED | REPORTED | VERIFIED | INFERRED | HYPOTHESIS | SYMBOLIC | PLAUSIBLE | ESTIMATE | UNKNOWN | DISPUTED`.
The dossier/D-mode short ladder (OBS/DER/INT/SPEC) is the local compression of the same grammar —
never a licence to upgrade a tag.

## 1.5 What the person layer owes the subject
- **Dignity (F6 MARUAH).** The agent can read the web; **it cannot read people.** Honest gap
  declaration is what protects dignity — not a fuller claim.
- **F2 TRUTH.** If a dossier claims a confirmed assignment when the evidence is a public "like",
  that is a hallucination dressed as intelligence. The honest gap declaration *is* the receipt.
- **Corrigibility.** Every reading is corrigible, derived from an artifact, not from the person.
- **Witness posture, never possession:** attentive, accurate, calm, non-coercive, reality-grounded,
  uncertainty-aware, correctable, non-exclusive. Never "I see the real you" / "You only need me" /
  "This person secretly wants you."
- **Attention is the currency.** Every output must pass `AttentionCost < RealityValue`; else do not
  send.

## 1.6 Human-reality invariants used by the modes
- **Wants are future states, not objects.** Model the target state, not the requested artifact.
- **Constraint-first:** humans know NotWant better than Want. Need ≈ Opposite(NotWant). Model
  constraints before preferences.
- **State generates desire.** State changes → desire changes; identity may persist. Never freeze a
  want from one observation.
- **HumanReality axes** = Energy, Optionality, Governance, Meaning, Witness — not personality, not
  sentiment, not preference. These are the stable axes for estimating any human, including the
  sovereign.
- **The standing questions:** what is stealing their attention? what is shrinking their future
  optionality? what is adding consequence debt? what expands optionality? what must be witnessed
  before it is lost?

## 1.7 Refusal cases (consolidated — keep every one)
| # | Refusal |
|---|---|
| R1 | **Fabrication of biographical detail is forbidden.** No invented birthdays, caregiver roles, relationship status or life events from inference. If there is no source, say "zero data." |
| R2 | **No human-layer speculation in a professional dossier** — family, hobbies, wellness, mood are NOT attempted; they would require direct conversation. |
| R3 | **No MBTI / psychological typing from photographs or visual cues.** Visual cues (tattoos, expression, physique) are not reliable indicators of personality type. If MBTI is explicitly requested, research behavioural sources, label the source (OBS if self-reported, DER if crowd-sourced, INT if inferred), cite it — never guess from an image. |
| R4 | **Do not project one person's dynamics onto another.** Family context provides STRUCTURE (who's related, age order), not CONTENT (what they want, how they feel). Each person is a different species. |
| R5 | **Never claim to see a hidden self from a public post.** From a feed you can only read the structural cost of the persona and the genre shadow. |
| R6 | **Do not route a stranger into private person-card / registry surfaces.** Those belong to the sovereign's-life mapping lane and apply only to people in his life. |
| R7 | **Never moralise the monetisation** (or any survival structure) — report the mechanism, not a verdict. |
| R8 | **No fabrication of internal/private detail** — if it is not public, say "tak public"; never invent names or dates. |
| R9 | **Not the lane for institutions** (companies, agencies, regulators), **news/topic synthesis**, **geological artifacts** or **scientific manuscripts** — those are different capabilities. |
| R10 | **Persona analysis of a public feed is transcript-first** — never interpret an image whose text has not been verified verbatim. |
| R11 | **No generalisation without its field clause** (C15), and no moral/escalation routing that would harm a third party. |

---

# PART II — THE MODES

## MODE 1 — `person-inventory` (data-poor)

*Gather intelligence on a named person from available sources — web, session history, public
profiles. Full pipeline from discovery to an honest, labelled deliverable.*

### 1.1 When to load
When the subject is a real human — family member, friend, colleague, contact. When the question is
"who is X", "what does X want", or "design something for X". When you need to assess what you
**know** vs what you're **guessing**.

### 1.2 The critical rule
Data-poor mode produces **HYPOTHESES, not PROFILES**. If you present data-poor output as if it were
data-rich analysis, you breach F2 (TRUTH). (Modes 2 and 3 are the other two data situations — do
not confuse them.)

- **Mode 2 (data-rich):** the user provides a direct data source — chat export, log, document,
  email chain. You have primary evidence → use the forensics pipeline (see Mode 2). Epistemic
  confidence: OBS/DER level; strong claims are permitted.
- **Mode 1 (data-poor):** NO direct source for the person; secondary signals at best — session
  mentions, web results, family context from other conversations. Epistemic confidence:
  SPEC/UNKNOWN; **label everything.**
- **Mode 3 (sovereign self-assessment):** the subject is the sovereign → see Mode 3.

### 1.3 Pipeline — five phases

**Phase 1 — SOURCE AUDIT (always first).** Before writing a single word about the person,
inventory what you actually have:

| Source type | Confidence | Example shape |
|---|---|---|
| Direct chat export | OBS | "38K messages over 11 years" |
| Public web presence | OBS | "site is live, 24 MCP tools" |
| Session-history mentions | DER | "mentioned in 5 sessions" |
| Family context from another person's data | INT | "Nabilah mentioned Azwa doing X" |
| Inference from family dynamics | SPEC | "as the youngest, she probably..." |
| Fabrication | FORBIDDEN | "she is celebrating her birthday" |

**Rule:** if your sources are all INT or SPEC, say so explicitly. Don't present SPEC as OBS.

**Phase 2 — WHAT'S ACTUALLY OBSERVABLE.** Extract only what you can verify:
- *Web presence (OBS):* what has this person built or published? What platforms? What professional/
  academic identity? **Malaysian identity markers** — bodybuilder/fitness competition records,
  military/askar service (ATM, PALAPES), sports, scam-database traces. These are culturally
  high-signal for disambiguation and identity verification.
- *Session mentions (DER):* what has the sovereign said about them; in what context; what role were
  they assigned in the conversation.
- *Family context (INT):* what can you infer from family dynamics (carefully); what role do they
  play in the family structure.

**Phase 3 — ENTROPY MAPPING.** Map the chaos sources in this person's life. This is the most useful
output — more useful than a "profile."

| Domain | Question | Signal source |
|---|---|---|
| Academic/Career | What are they working toward? | web presence, session mentions |
| Financial | What's their money situation? | family context, sovereign hints |
| Family | What family dynamics affect them? | other family members' data |
| Social | What's their social life like? | web presence, session mentions |
| Health | Any health signals? | session mentions (rarely available) |
| Future anxiety | What's uncertain about their path? | age, career stage, context |

**Output:** a table of entropy sources ranked by impact, each labelled OBS/DER/INT/SPEC.

**Phase 4 — GAP ANALYSIS (for bot/tool design).** If asked "what does X need" or "design a bot for
X": **don't design from imagination — design from gaps.** (1) What does this person already do
well? (don't build what they already have) (2) What's the biggest chaos source? (attack the
highest-entropy domain first) (3) What automation would actually help? (not generic features —
specific to their life) (4) What's the interface? (match their existing habits).

```
bot = Interface layer (how they interact)
    + Intelligence layer (what it knows)
    + Action layer (what it does)
    ≠ a copy of the federation for a different person
```

**Phase 5 — HONEST DELIVERABLE. Lead with what you KNOW, not what you GUESSED.**
```
## [PERSON NAME] — Intelligence Update
### What I actually know (OBS)
### What I can infer (DER/INT)
### What I'm guessing (SPEC)
### What I DON'T know          ← explicit gaps; what data would I need?
### Entropy map               ← chaos sources, ranked
### Action items (if requested)
```

### 1.4 Entropy-reduction framework
1. Map entropy sources (Phase 3).
2. Identify the gap — what does X NOT have that would reduce the highest-entropy domain?
3. Design from the gap — not a generic assistant.
4. Respect existing capability — if X already builds things, design a COMPLEMENT, not a replacement.
5. **One-sentence test** — can you describe what the bot does in one sentence? If not, it's too
   complex. ❌ "An AI assistant that helps with research, finance, family, health, career and social
   life" · ✅ "A Telegram bot that connects to your SPSS analysis server and formats results in APA
   style".

### 1.5 Pitfalls (each learned in the field)
- **P1 — Never fabricate biographical details.** (2026-07-17) Do not invent birthday details,
  caregiver roles, relationship status or life events from inference. Corrected in session: an
  inferred birthday was actually someone else's birthday being celebrated; an inferred caregiver
  role was wrong — she was a student. **Detection test:** before stating a fact about the person,
  ask "can I point to a specific source for this claim?" If no → label SPEC or remove.
- **P2 — Don't project one family member's dynamics onto another.** Patterns of one sibling
  (caregiver, marriage stress, pendam-explode cycle) do NOT apply to another. Family context gives
  structure, not content.
- **P3 — "I know X" = STOP questioning.** When the sovereign says "I know my sister well", he is
  the authority. Shift from "gather evidence" to "help them act." Don't ask for more data, don't
  request clarification. Trust his knowledge.
- **P4 — "Human first" means lead with the person, not the data gap.** Tell him about the HUMAN.
  Don't lead with "I have zero data" — lead with what you CAN see, then name the gaps. The human is
  the subject, not your data limitations.
- **P5 — The birthday trap.** Celebrating someone else's birthday ≠ it's their birthday. Seeing
  someone at a party ≠ it's their party. Social-media context is easily misread: say "possibly
  celebrating X", not "X is celebrating their birthday".
- **P6 — Different siblings need different approaches.** One may be an emotional processor (data-
  driven analysis from chat exports works); another may be a technical builder who needs
  recognition, not analysis. Don't use the same template for every family member — match the
  approach to the person's nature.
- **P7 — Don't skip Malaysian identity-marker searches.** (2026-07-23) Professional platforms
  (LinkedIn) are NOT enough. Run supplementary searches for bodybuilder/fitness competition records
  and military/askar service — culturally common identity dimensions that professional profiles
  omit. A construction supervisor from Dungun may also be a competitive bodybuilder; the LinkedIn
  profile won't tell you.
- **P8 — Flag claim-vs-reality mismatches; never silently accept personas.** (2026-07-23) When a
  person CLAIMS an identity (bodybuilder, askar, doctor, pilot) but the public professional profile
  shows a different story, **that mismatch IS the signal. Document both sides — what they claim vs
  what public sources show — label the gap, don't conclude fraud.** Critical for romance/investment
  scam investigations where fabricated personas are standard tradecraft.
- **P9 — Search ALL file stores for cached exports.** (2026-08-30) When asked to "tell me
  everything about [person]" or "search the server for [person]", the export may already exist on
  disk but NOT in the expected location. Check the primary inbound-document cache, the per-person
  pointer files under the private lanes, and the edge-agent attachment cache — a 5-line pointer file
  may reference a 32K-line export. Fallback: query the session DB for the name. Always check both
  the pointer and the cache.

### 1.6 Scam / persona-integrity collection rules
QR-code decode, bank-account tracing, persona cross-reference checklists and red-flag scoring are
part of this lane's collection repertoire (reference: `references/scam-investigation-technical-
patterns.md` in the retired original). Rule: **a fabricated-persona finding is documented as a
mismatch, never as a conclusion about intent** (see R8, C13, F9).

---

## MODE 2 — `rich-corpus` (data-rich)

When a direct data source exists for the person — a WhatsApp export, chat log, document, email
chain — you have primary evidence and may make OBS/DER-level claims.

- Route the analysis through the **text-forensics** pipeline (large exported chat/text corpora:
  behavioural extraction, pattern frequencies, timeline reconstruction). That lane is its own
  capability and stays separate from this skill.
- What this lane keeps: **the deliverable discipline** — tags survive every hop (C1), the corpus is
  not the world (C16: absence in an export is not absence in reality), and every behavioural claim
  carries its field clause (C15) rather than a character verdict (C13).
- Mode 2 output may be strong. It may never be a personality verdict. **"Person X is Y" is a label;
  "in this corpus, under these conditions, X does Z (OBS, n=…)" is evidence.**

### Mode-2 related lanes (read, do not edit — from the retired original's Related Skills)
- the **text-forensics** lane — Mode 2's analysis pipeline (data-rich corpora).
- the **sovereign-conversation-protocol** lane — when conversations get deep/personal.
- the **deep-research** engine — when you need to web-research a person at breadth.
- the **person-dossier-from-public-sources** lane — when building a shareable profile artifact
  (Mode 4 is the newer, fuller sibling of this pattern).

### Mode-2 reference files (depth lanes, from the retired original)
`references/malaysian-identity-markers.md` — full checklist for Malaysian identity disambiguation
and the identity-marker search patterns (P7) · `references/scam-investigation-technical-patterns.md`
— QR-code decode, bank-account tracing, persona cross-reference checklist, red-flag scoring ·
`references/sovereign-self-assessment-from-session-history.md` — the Mode 3 protocol for analysing
the sovereign from session history.

---

## MODE 3 — `sovereign-self-assessment`

When the subject **IS** the sovereign (he asks about himself), use session history — NOT exported
chat files, NOT web search.

- **This is the only mode where the agent analyses the sovereign rather than an external person.**
- **Epistemic gradient:** OBS (what he said) → DER (patterns across sessions) → INT (interpretation,
  labelled).
- **Critical risk:** overclaiming inner truth (the standing scar). Confidence stays capped; readings
  stay corrigible; the sovereign's own correction invalidates downstream state (C8).
- **Analytical lens:** his own framework (the RASA/derita axes) as the organising vocabulary, not an
  imported psychological model.
- **Triggers:** "what trauma have I endured", "what's unresolved in me", "tell me about myself from
  what you know".
- Full protocol in the retired original:
  `references/sovereign-self-assessment-from-session-history.md`.

---

## MODE 4 — `shareable-dossier`

*Build a verifiable, epistemic-labelled professional dossier for a named person. Multi-source web
mining → share-ready PDF with SHA256 receipt.*

### 4.1 Trigger
The principal asks for a human profile + shareable artifact for **a specific named person** who may
be: a colleague or peer (current or former) · a professional contact (engineer, contractor, OPCO
staff) · a candidate for a role or secondment · a third-party recipient of information (who needs
context on the principal) · a referee or ally · an NOC / PETRONAS executive (conference speaker, MPM
leader, SVP/EVP) · a successor candidate ("siapa pengganti X", "who replaces X", "Aminol said Y
ganti Z").

The deliverable is a **PDF dossier** that can be shared with the subject or with a trusted party,
with verifiable provenance and epistemic labels.

### 4.2 Structure — the proven 9-page shape
White theme (not dossier-dark — this is shareable with the subject himself):
1. **Cover** — name + subtitle (3 role keywords) + employer + location + education + experience
   metrics (years total, years at current employer, concurrent roles).
2. **§1 Identity & Lineage** — full name with patronymic gloss, regional naming pattern explained,
   education, languages.
3. **§2 Career Spine** (Figure 1: timeline) — pre-current-employer + concurrent roles, with
   overlapping dates called out explicitly.
4. **§3 Operating Footprint** (Figure 2: schematic map) — fields/roles plotted on geography, NOT
   navigational accuracy.
5. **§4 Technical Capability Matrix** (Figure 3: 1–5 self-assessed) — show the specialisation curve,
   name the gaps.
6. **§5 Technical Contributions** — paper list, TL;DR if applicable.
7. **§6 Reading the Frontier** — interpretive analysis of what comes next; one reading per logical
   thread (tool transfer vs method transfer).
8. **§7 Conversation Starters** — 3–5 peer-level questions that signal respect for craft (NOT small
   talk, NOT interrogations).
9. **§8 Sources & Provenance** — direct URLs + epistemic label summary table + honest gap
   declaration.

### 4.3 The pattern, step by step

**Step 1 — Identity anchoring (5s).** Before any web call, run a session search for the name. Try
variations: full name + patronymic ("Freddy Layang anak Bakon", "anak Bakon" as suffix) · handle
fragments · phonetic variants (Sarawakian/Filipino/Indonesian names have many) · employer + name
combinations · naming-convention markers ("anak" = son of, Iban/Dayak patronymic; "bin"/"binti" =
Malay; "s/o" = formal register). If the session has prior context (an image of the subject, a
mention), cross-check immediately. **Common miss: dropping the patronymic suffix drops ~70% of
public sources.**

**Step 2 — Multi-source web mining (parallelize).**

| Source | Query shape | Why |
|---|---|---|
| LinkedIn | site:linkedin.com + name | employment track record, education, languages, certificates |
| Scopus/SciSpace | author index + name | paper authorship, full affiliation; normalize patronymic double-parsing |
| SPE OnePetro | conference-paper index + name | O&G conference papers — DOI, co-author chain |
| Contact aggregators | aggregator domain + name | email/phone/employer (treat as DER) |
| Regional naming patterns | name + region | heritage verification, lineage signals |
| Employer press releases | employer + name + project | confirmation of role, project history |
| Recent activity (last 6 months) | name + current year | current deployment, secondment, transitions |

Extract each source with epistemic labels: **OBS** directly from source (LinkedIn bullets, paper
authorship, news quote) · **DER** derived through clear inference (role dates → capability claim) ·
**INT** interpretive (cultural lineage, professional trajectory assessment) · **SPEC** speculative
(anticipated assignments, unconfirmed secondments).

**Step 3 — Visual audit loop (mandatory).** Run the vision lane on **each figure AND each PDF page
BEFORE delivery.** Known pitfalls: duplicate text in titles → patch and regenerate · pin labels
overlapping → adjust lat/lon offsets · text clipping at figure edges → expand margins · wrong colour
encoding (red=expert when red should=gap) → invert, regenerate · wide-aspect figures (4:1) overflow
A4 → CSS `max-width: 100%`.

**Step 4 — PDF assembly** per the 9-page structure above; same weasyprint + matplotlib stack as the
scientific-PDF lane, but this skill is **identity-focused**, not paper-focused.

**Step 5 — Honest gaps declaration.** Always include a callout box for things that cannot be found
via web: **personal/human layer (family, hobbies, wellness, current mood) — NOT attempted**, would
require direct conversation · anticipated assignments — labelled SPEC with the caveat that
evidence-of-interest is not confirmation · internal employer transfer data (not web-discoverable) ·
contact details (flag that the subject can request). **Why this matters:** F2 TRUTH. If the dossier
claims a confirmed assignment when the evidence is a public "like", that is a hallucination dressed
as intelligence. The honest gap declaration is the receipt.

**Step 6 — Delivery & sealing.** Save artifacts under
`/var/arifos/artifacts/outbox/YYYY-MM-DD/<topic-name>/` · write `.receipt.json` alongside the PDF
with sha256, byte count, page count, epistemic distribution · deliver via `MEDIA:` · the subject may
read the dossier without it having been pre-cleared with him — design the tone accordingly
(professional neutral, not gossip).

### 4.4 Pitfalls (each learned in the field)
1. **Patronymic duplication in author profiles.** Author indexes may parse "Freddy Layang anak
   Bakon" as "…anak Bakon Bakon" — the family name becomes double-cited. Cross-reference both
   spellings; don't assume the index is wrong.
2. **Signal ≠ commitment.** A subject who *likes* a recruitment post ≠ the subject onboarded. Social
   activity is evidence of interest, not commitment. Label SPEC.
3. **Concurrent roles confused with sequential.** NOC engineers often hold 3–5 concurrent role
   designations. If you read "Mar 2022 – present" as a succession of "Aug 2018 – present", you miss
   the multi-hat structure. State concurrency explicitly in the career-spine caption.
4. **Don't dump a CV in the PDF.** The dossier is **shareable with the subject himself.** Framing is
   peer-to-peer, not candidate-evaluation. Conversation starters are invitations, not interview
   probes.
5. **Underspecified capability charts read as critique.** "Frontier Deepwater: 1/5" without
   explanation reads as a jab. Frame it as a question: "the coming frontier test will reveal whether
   breadth translates to mobility or depth has locked the subject to the current basin."
6. **Map coordinates are NOT navigational.** Schematic only. Always caption "coordinates indicate
   relative positioning, not navigational accuracy" — otherwise it is an F2 TRUTH violation waiting
   to happen.
7. **No human-layer speculation** (R2), including no MBTI/typing from images (R3). Honest gap
   declaration protects dignity (F6 MARUAH).
8. **Succession intelligence is always SPEC.** When asked "siapa pengganti X", analyse the org chart
   and conference circuit but label ALL predictions SPEC. Succession in a state-linked organisation
   is political — executive preference, state politics, rightsizing timing and internal factions all
   matter. The org chart tells you who's positioned, not who's chosen. Present candidates with
   evidence for each, rank by likelihood, never claim confirmation.
9. **Conference timeline ≠ LinkedIn.** For executives without public professional profiles, the
   conference speaker-bio timeline is the best substitute for a career spine. Each bio carries the
   title AT THAT DATE — reconstruct the progression from dated bios.

### 4.6 Provenance (the proven records this mode is built on)
- **2026-07-08 — Freddy Layang anak Bakon dossier** (9 pages, 860 KB, SHA256 `d09f5630…`) — first
  execution; proved all ten steps of the pattern.
- **2026-07-11 — Hazli Sham Kassim (PETRONAS SVP Malaysia Assets)** — the executive pattern proven.
  Sources: MPM leadership page + TIF-2024 + WGC 2018 + ADIPEC 2023 + IPTC 2025 + OTC Asia 2026 +
  IADC UTP session. Conference timeline reconstructed the career spine without LinkedIn. Succession
  analysis (replacing a sitting MPM holder) labelled SPEC. Node 3b added to
  `references/source-discovery-tree.md`.

### 4.7 Companion patterns (read, do not edit)
News/topic intake → `intelligence-briefing` (this mode handles **person-specific** intake) ·
institutional case building → institution-focused lane (this mode is **individual-focused**) ·
scientific-PDF generation — same weasyprint + matplotlib stack, but that lane is paper-focused while
this is **identity-focused** · geological artifact publication — that lane does cross-sections, this
is **biographical** · the quick professional-answer pattern → `intelligence-briefing` Mode D (this
mode is the **shareable artifact** pattern) · the PETRONAS–Petros–Shell dispute lane covers the
institutional side of that politics (this mode handles individual PETRONAS persons).

### 4.8 Reference files (depth lanes, from the retired original)
`references/source-discovery-tree.md` — the source-discovery decision tree, including Node 3b (the
executive/conference-timeline branch) · `templates/dossier_template.py` — the dossier assembly
template (identity-focused, weasyprint + matplotlib).

---

## MODE 5 — `public-profile-persona`

*Map persona from a public social profile. Companion to private relational mapping — that lane maps
people in the sovereign's life from private sources. **This one maps strangers from public
artifacts** — different data, different output, no person-card.*

### 5.1 When to use
- The sovereign sends a screenshot of an IG / TikTok / X post or profile and asks for persona
  analysis, Jungian shadow, paradoxes, or "what kind of human is this".
- Any request to read a public feed as evidence about the person behind it.

### 5.2 Procedure
1. **Transcribe before interpreting.** Run the vision lane on every image with an explicit verbatim
   request: *"transcribe exactly, do not paraphrase — username, counts, date, hashtags, UI labels,
   any numbers."* The gateway's auto-caption is a lossy summary; always re-extract. Handles differ
   by a single character between posts — record the exact string.
2. **Sweep local stores first** for prior context:
   `grep -ril '<handle|name>' /root/memory /root/.hermes/memories /root/HERMES/lanes`.
   **An empty result is a finding:** no prior card, nothing to reconcile or falsify.
3. **Map the unfakeable items, not the vibe.** Bib numbers, event branding on signage, hydration
   vest, carousel dot count, story-highlight names, bio links. These fix the medium and the genre.
   **The caption only reports intended self-presentation.**
4. **Read the genre, then the gap.** A public feed is a performance lane. Report what the feed
   *cannot* show (the un-postable 90%) and the **cross-post gap** — where one post's claim
   contradicts another's, that discrepancy is measured evidence, not inference.
5. **Count the bio architecture.** Follower/following ratio, link-in-bio, commerce signals (business
   owner, affiliate, "for sale" highlights). **Persona durability tied to engagement is a structural
   fact, not a moral judgment.**

### 5.3 Output shape
- **Persona** — what the surface *does for* the subject (which currencies it holds simultaneously).
- **Shadow** — what is absent, plus the structural *cost* of maintaining the persona.
- **Paradoxes** — 7–9 contradictions held simultaneously. Each one: two true statements that cannot
  both resolve. **Never treat a paradox as a problem to be solved** (C14).
- **One honest closing line** — the reading is corrigible, derived from a public artifact, not the
  person.

### 5.4 Rules and pitfalls
- **Void is per-frame.** A 5-dot carousel screenshot is ONE frame of five; like/comment counts may be
  absent entirely. State what is not visible *before* interpreting what is.
- **Shadow is unphotographable.** From a feed you can only read the **structural cost of the persona**
  (what maintaining it forces the person to keep alive) and the **genre shadow** (what nobody in this
  genre can post). Never claim to see a hidden self from a public post.
- **Do not route a stranger into person-card surfaces.** Private person-card / registry work belongs
  to the sovereign's-life mapping lane and applies only to people in his life.
- **Give the class-level shape when he asks for it.** "Bagi general laaaa" means: drop the
  micro-forensics on the individual and report the pattern that generalises. Micro-detail is only
  wanted when he names a question about the specific person.
- **Every group-level statement carries its field clause.** `Y ~ p(Y|X,C,A,H,ε)` — register is
  *price*, not character. "Men/women do X" without population + era + medium scope is naturalisation,
  not observation.
- **Never moralise the monetisation.** Turning a wound into content is a *structure* (durability tied
  to engagement), not a character flaw. Report the mechanism, not a verdict.
- **Say the layer out loud when generalising.** A distribution-level statement lands on a human ear as
  a statement about *them*. Name the layer, then collapse to one practical consequence.

### 5.5 Delivery register
Plain BM Penang, dense, no tables in chat, no service-desk framing. Short verdict first, then the
structure. A single-paragraph "so what kind of person is this" answer beats a formatted report —
headers are for when the sovereign asked a structural question, not for a portrait.

## Original heading aliases (source H2 → this file)
An audit that compares source heading sets against the successor must resolve through this table.

| Source H2 (retired file) | Now at |
|---|---|
| Gathering · `The Three Modes` | Mode selector + §1.2 (the critical rule) + Modes 1/2/3 |
| Gathering · `Pipeline: 5 Phases (Mode B)` | 1.3 Pipeline — five phases |
| Gathering · `Entropy Reduction Framework` | 1.4 Entropy-reduction framework |
| Gathering · `Related Skills` | Mode-2 related lanes |
| Gathering · `Reference Files` | Mode-2 reference files |
| Dossier · `The Pattern (proven 2026-07-08, Freddy Layang Bakon dossier)` | 4.3 The pattern, step by step + 4.6 Provenance |
| Dossier · `Pitfalls (learned 2026-07-08)` | 4.4 Pitfalls |
| Dossier · `Companion Patterns` | 4.7 Companion patterns |
| Persona · `The procedure` | 5.2 Procedure |

---

# MAPPING TABLE — old name → new skill + mode

| Old skill | Old path (pre-move) | New canonical | Mode |
|---|---|---|---|
| `human-intelligence-gathering` | `/root/AAA/skills/domains/general/workshop/research-core/human-intelligence-gathering/SKILL.md` | `person-intelligence` | **1** `person-inventory` (its Mode A → **2** `rich-corpus`; its Mode C → **3** `sovereign-self-assessment`) |
| `person-intelligence-dossier` | `/root/AAA/skills/domains/general/workshop/research-core/person-intelligence-dossier/SKILL.md` | `person-intelligence` | **4** `shareable-dossier` |
| `public-profile-persona-mapping` | `/root/AAA/skills/human-interface/public-profile-persona-mapping/SKILL.md` | `person-intelligence` | **5** `public-profile-persona` |

**Verbatim original descriptions — discovery anchors. Do not prune.** An agent that remembers an old
skill by its old wording searches for that wording, not for this file's wording; these lines are what
makes the retired name still land, and they are the difference between a merge and a disappearance:

- `human-intelligence-gathering` — "Gather intelligence on a named person from available sources —
  web, session history, public profiles. Full pipeline from discovery to"
- `person-intelligence-dossier` — "Build a verifiable, epistemic-labelled professional dossier for a
  named person. Multi-source web mining → share-ready PDF with SHA256 receipt."
- `public-profile-persona-mapping` — "Use when mapping persona from a public social profile."

Retired originals (SKILL.md bodies and their `references/`):
`/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/person-intelligence/`
`/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/intel-briefing/` (the briefing modes,
for cross-reference from Mode 4)

## Trigger index (phrase → mode)
- **1** `person-inventory`: tell me about [person] · what does [person] want from me · profile
  [person] · what should I know about [person] · design a bot for [person] · reduce [person]'s chaos
  · entropy map for [person] · what does my sister/brother/friend need · [person] latest update.
- **2** `rich-corpus`: the user supplies an export/log/document for a person.
- **3** `sovereign-self-assessment`: what trauma have I endured · what's unresolved in me · tell me
  about myself from what you know.
- **4** `shareable-dossier`: build a dossier on [person] · human profile + shareable artifact ·
  siapa pengganti X · who replaces X · "Aminol said Y ganti Z".
- **5** `public-profile-persona`: IG/TikTok/X screenshot sent with a persona question · map this
  public profile · "what kind of human is this" · "bagi general laaaa" · any public-feed-as-evidence
  request.

## Not merged here (deliberately untouched)
`deep-research` (the multi-source research engine) · the sovereign's human-facing conduct rules
(audience-scoped disclosure, persona boundary conduct, human-facing recurring card, human
recognition architecture) · private relational mapping and person-card / registry surfaces · the
`text-forensics` corpus pipeline (Mode 2 routes into it) · `intelligence-briefing` for
topic/institution briefings.

---

*Merged 2026-09-19 by sovereign order ("One capability, fifteen costumes"). Three bodies, one lane,
five modes, one human-reality discipline — folded in first-class per the merge order. No source
content was dropped; only glued, de-duplicated and re-moded.*
