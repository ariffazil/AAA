---
name: first-party-evidence-audit
description: "Use when auditing claims against first-party records."
version: 2.0.0
author: Hermes
license: arifOS
tags: [evidence, audit, epistemology, records, human, witness, relationship, corpus, privacy, first-party, forensics]
related_skills: [text-forensics, telegram-conversation-history-extraction, void-paradox-doctrine, governed-uncertainty, human-meaning-membrane, relationship-memory-isolation, claim-receipt-discipline, claim-level-verification]
triggers:
  - 'asks for an audit of a relationship against the record ("not a persona task", "an audit of what has actually happened")'
  - 'asks whether a story about a person is actually supported by the messages'
  - "pastes an external model's analysis of a personal relationship and asks if it is true"
  - 'asks what the record FAILS to show about a bond'
  - 'asks for negative evidence, an UNKNOWN register, or a minimum true model'
  - 'a bond has an AI-authored map/dossier/card about it that is being treated as fact'
  - 'audit a relationship between two real people from records'
  - 'what is actually between us'
  - 'reconstruct the reality of this relationship'
  - 'commission that forbids romance, diagnosis, archetype, or population literature'
  - 'persona or literature synthesis exists BEFORE the evidence is read'
  - 'corpus of chat logs, DMs, group transcripts, or voice notes covering one relationship'
  - "deciding whether a claim about a person's feelings is supported, partial, or unknown"
  - 'user asks for an evidence-grounded reconstruction of a relationship or a period'
  - 'user hands over a chat export / transcript / dump and asks what it evidences'
  - "user asks you to test an existing narrative, persona, or another AI's account against records"
  - 'an earlier session produced a confident story and it now needs auditing'
  - 'user asks what a relationship really is, or to audit one against chat logs, exports, message history, or agent records'
  - 'user asks to "resolve the unknowns" about a bond'
  - 'Arif asks for an audit / reconstruction / "what is actually going on" about a real relationship'
  - 'a request to separate OBSERVED from INFERRED from UNKNOWN about a named human'
  - 'a request to test whether a story about someone is supported by records'
  - 'any mission that begins "do not contact them, do not manufacture tests"'
capability_tier: fed-long-context
ecology_state: WARM
---

# First-Party Evidence Audit (canonical)

**One question, five old names:** *does this bond / relationship / claim survive contact with the
first-party record?*

Load when the ask is to extract reality out of records — *reconstruct what actually happened between me
and X*, *audit what the records support*, *how does this relate to my reality*, *tell me what the
evidence says* — and load **before** agreeing with any strong claim about a real person built from logs,
prior AI output, or persona material, **including when the claim is the principal's own**.

This body is the collapse of six identities into one (2026-09-19; authority **ARIF —
SKILLSTORE_NAMESPACE_COLLAPSE_V2**). Nothing was dropped: the five retired names are now MODES below,
their bodies frozen under `/root/AAA/skills-retired/2026-09-19-v2-first-party/`. Mapping table,
then discovery anchors at the end of this file.

Sibling skills carry adjacent layers and stay separate: `text-forensics` (profiling a corpus) and
`telegram-conversation-history-extraction` (reading the logs) are the mechanics; this skill is the
**audit discipline** on top of them. `void-paradox-doctrine` supplies the text≠reality floor.
A profile answers *what is this person like*; this skill answers **what the record actually supports,
and where the story has outrun it**.

---

## Mode index — old name → mode/section

| Old name (retired 2026-09-19) | Primary mode | Also carried by | Distinctive contribution |
|---|---|---|---|
| `relationship-evidence-audit` | **M2 — Source class & the AI-synthesis trap** | M4, M7, M10, M13 | source-class weighting; count-before-narrate; calibration anchors; requisitioner-model gap |
| `relationship-reality-audit` | **M11 — Frame audit & the three UNKNOWNs** | M1, M8, M12 | access-vs-meaning frame audit; co-authorship matrix; privacy firewall for third-party corpora |
| `first-party-corpus-audit` | **M1 — Corpus sensor & integrity gates** | M11 (void map), M6, M13 | five integrity gates; void map with raise/lower symmetry; register/consent rules |
| `human-relationship-audit` | **M6 — Behavioural ladders & dated windows** | M4, M10, M14 | ladder rungs with windows; absence-publication law; "never convert" list |
| `human-bond-reality-audit` | **M12 — Firewalls, boundaries & void-impact matrix** | M1 (two clocks), M11 | hard boundaries on the work; symmetric void-impact matrix; uncreated-UNKNOWN |

The survivor keeps the most general description of the six — *auditing claims against first-party
records* — and therefore absorbs the bond/relationship/corpus/period variants as modes. This is a
**namespace collapse, not a rename**: no new identity was minted, and no capability was removed.

---

## The one law

> The archive is not the relationship. **The archive is a sensor.**

The deliverable is a **minimum true model plus an UNKNOWN register** — not a portrait, not a
resolution, not advice, not a diagnosis, not a sexuality classification, and never an optimisation for
the more interesting story. Reconstruct first. Then infer. Then challenge the inference. Then report
only what remains. If the records produce a boring answer, **ship the boring answer** — and do not
optimise for cynicism either.

Prime directive order (never reorder): **reconstruct → infer → challenge → report.**
Population literature, archetypes and plausibility are barred until the reconstruction is complete, and
even then may appear only as optional comparison — never as diagnosis or causal proof about an
individual. A category is a coordinate for auditing a population; **individual evidence decides
anything about a person.**

---

## M1 — Corpus sensor & integrity gates
*(from `first-party-corpus-audit` · `human-bond-reality-audit` · `relationship-reality-audit`)*

**State the sensor spec before any finding:** coverage · blind spots · distortion · sampling bias ·
missing channels · temporal gaps · observer effects. **Observed ≠ total.** A text export cannot carry
tone, touch, gaze, or in-person contact. A reader who sees the limitation first will not over-read the
result.

**Missing evidence is bidirectional.** It may raise, lower, or leave a hypothesis untouched. It is
never used to rescue a preferred story, and absence is never evidence of absence.

**Gate 1 — Probe the date format, do not assume it.** Messaging exports are usually `MM/DD/YY` (US),
i.e. `M/D/YY`, but are frequently read day-first. Locale hints (language, who speaks, an earlier successful parse of a
different export) are all unreliable. Probe: take the first three dated lines — first field ever exceeds
12 ⇒ `D/M/Y`; second field ever exceeds 12 ⇒ `M/D/Y`; neither in the sample ⇒ extend the probe until one
does. Do not guess. A regex that *validates* its captures does not raise on a bad line, it skips it: a
day-first parser on an `M/D` export discards thousands of messages asymmetrically, producing phantom
long silences, distorted sender splits and wrong per-period counts — all internally consistent, all
wrong. Symptoms you have been bitten: the reported range starts later than the file's first line, or a
gap longer than the file can physically contain. Parse both conventions, print the count plus first and
last timestamp, and check them against a manual read of the file's first and last lines.

**Gate 2 — Prove coverage before deriving anything.**
```
parsed_count  vs  raw_line_count          # print both, in the report
first ~6 non-matching lines               # print them; see what the pattern is eating
sender census vs raw text search          # a parser that loses senders is losing messages
```
Non-matching lines are usually legitimate (continuation lines, media placeholders, system notices). The
point is to *see* them, so an unexpected rejection class is visible immediately.

**Gate 3 — Re-derive, never patch.** When the format was wrong, every downstream number is suspect.
Re-run the full analysis and publish a corrected baseline table with the superseded figures **marked as
superseded**. Never patch the single figure you happened to notice. **Restate the claim as a ratio** when
a re-parse moves absolute counts: the shape is the finding, the count is a fact about your parser.

**Gate 4 — Preserve the corpus before you analyse it.** Copy it to a durable private location as step
one — `chmod 700` on the dir, `600` on the files — recording size and line count, and record the new path
in the deliverable. Sources arrive in `/tmp`, unzip dirs, attachment caches, scratch dirs: all subject to
cleanup, and a lost corpus takes the audit's re-derivability with it. If it is already gone, re-derive
from the platform's own document cache (original uploads are kept by hash) rather than asking the
requester to re-export, then diff against your recorded size.

**Gate 5 — Two clocks in one machine.** Log files are commonly local MYT (+08); database epoch columns
are commonly true UTC. Both look plausible and sit eight hours apart in the wrong direction at the wrong
moment. In Python, `datetime.utcfromtimestamp(e).astimezone(tz)` returns **UTC** while reading as though
it were local — use `datetime.fromtimestamp(e, tz)`. Verify once against a timestamp you already know
(a message you just sent, the matching log line) before trusting any time-of-day conclusion.
Day-versus-night reasoning, "who messaged first that day", and phase-of-day patterns all invert silently
here.

**Other corpus facts that change every statistic:** count `<Media omitted>` as its own token — it is a
placeholder, not a message · define the counting unit before quoting a number (days with ≥1 message, ≥2
messages, both parties present give three different totals; "messages" may or may not include system
notices and placeholders) · gateway/agent logs truncate message bodies around 200 characters **without a
marker** (never present such a quote as complete) · logs rotate fast (roughly a fortnight), so an absence
claim is a claim about that window — state the covered span from the first and last timestamps you
actually read · the same message can log twice under a primary plus mirrored id (dedupe on
text + timestamp) · a zero-length result from plain `grep` over a log with binary bytes is a grep
artefact, not silence (`grep -a`) · **a zero from a regex is a hypothesis, not a finding** (below).

**Re-derive every headline number from the preserved corpus and state the derivation before publishing.**
In this class the numbers ARE the argument, and one statistical correction can invert a finding's
direction.

### Absence claims — the publish gate
An absence claim ("never", "zero", "no evidence he") is the most consequential sentence you can publish
and the easiest to get wrong, because nothing contradicts it. Before writing any absence, do all four:
1. **Variant spellings** — misspellings, transpositions, phonetic respellings, dialect forms.
2. **Register** — the same act appears in BM, English, dialect and emoji; searching one token is not
   searching the class.
3. **Widen the token** — stem, root, looser regex (`wor[ks]*hip`), not just the exact word.
4. **Search the raw artefact, not a derived index** — an index built from an earlier bad parse inherits
   its gaps.

Then attach the search surface to the claim: *"not found by these patterns: `<list>`"*, so the next
reader can falsify it. **Vanishingly small negatives propagate**: one dictionary-spelling search returned
"0 instances / 33 months" while the subject's own consonant-transposed spelling appeared **eleven times**,
including direct requests and two notices that it had stopped — and the false negative had already
reached several downstream documents. **Confirm the instrument before convicting the subject:** a term
that comes back mangled on *every* trial is a property of the pipeline, not of the content.

### Media voids
`<Media omitted>` is not automatically recoverable. Open the archive and list its entries **before**
writing "media not yet retrieved": a zip holding only the `.txt` means every omitted item is gone.
Say **"unrecoverable from this host"**, not "not yet audited" — a void described as pending is a void
someone will fill with inference. Metadata (sender, timestamp, image-vs-video) may be reconstructed from
context even when content is not, but **metadata alone must never be used to infer what an image
showed**. Where a channel persists a machine-written description of inbound media, image content **is**
partly recoverable after the file is gone — but only for that channel and window; say which. Group-chat
media attribution often survives as a trailing sender marker in the persisted text; without it,
attribution is inference, not observation. **Check generation provenance on any file before treating it
as a photograph** — AI-generated stills sit in scratch dirs looking exactly like evidence.

### What a parser cannot reach
Text corpora carry contact topology (who initiates, who returns, what words appear) and are close to
blind on eyes, touch, proximity, tone, hesitation, and private embodied encounters. When the real
question lives in the second category, say so explicitly: **more data from the wrong channel does not
solve a missing-channel problem**, and a thousand more messages add almost nothing.

---

## M2 — Source class & the AI-synthesis trap
*(from `relationship-evidence-audit`)*

Enumerate every corpus; record span, message volume, active-day count, per-sender split, provenance and
storage. Then **label each by class — this is the step that gets skipped when an audit goes wrong**:

| Class | What it is | Weight |
|---|---|---|
| FIRST-PARTY | the two parties' own messages, in any channel | evidence |
| SECOND-ORDER | one party's own words to a third party, including to an agent | evidence of the speaker's STATE; only REPORTED about the other party |
| AI-SYNTHESIS | any map, card, dossier or summary a previous agent wrote about this relationship | **object of the audit, not a source for it** |
| MEDIA | generated voice / stills / video, registry entries | zero weight about any human |
| LAW | sealed care directives, behavioural rules | governs agent conduct; carries no behavioural fact |

**The AI-synthesis trap.** An earlier agent's map reads like primary source because it quotes primary
source. It is not — it was written from the same messages now being audited, inside a session that
already believed a thesis. Audit its load-bearing claims (the "wound", the "flinch", the "motive")
against the messages first; that is where the gloss concentrates. **A confident map in the archive is not
a confident finding; it is a document with an author and a date.**

**Quarantine synthesis and fiction explicitly — they may generate hypotheses, never evidence.** Once a
synthesis document sits in the same directory as real evidence, later readers cannot tell them apart by
position. Countermeasure: **every synthesis artifact carries its provenance and its status in its own
header** — what it was derived from, that it is synthesis, and what it must not be used for.

**Corpus separation before reading (never merge in one table):** direct chat export · direct
human-to-human channel · person→agent DM · group-with-agent · the requester's own channel ·
persona/fiction. Group speech is **audience-present**; a DM to a bot is a **different context, not a more
truthful one**. **Discovering that a "direct channel" is empty is itself a finding** — state it, because
it changes what every later claim can rest on. A *missing lane* is a finding: if two people have no
private channel and every recorded exchange happened with a third listener present, that shapes
everything.

---

## M3 — Attribution & identity resolution
*(from `relationship-reality-audit` · `human-relationship-audit` · `first-party-corpus-audit`)*

- **Resolve identities from data, never from the asker's naming.** One display name can map to several
  ids; one id can be a generic masked placeholder (a privacy-masked profile showing as `No name` is a
  **person**, not a system field); a `user=unknown` group row is an **attribution gap, not proof of
  silence**. Resolve both parties' ids explicitly and cross-check before reporting anything per-person.
  Never hardcode a uid-to-person mapping from the task prompt — treat any name the requester supplies as
  a claim to verify.
- **Group messages come in two shapes.** Inline tag (`msg='[Name|uid] body'`, `user=unknown`) and
  display-name (`user=<display name>`, no tag in body). A parser keyed on the tag alone returns zero rows
  for the second shape and silently banks them as "unattributed". Print the by-speaker census over
  **both** shapes — an `unattributed` bucket above ~a tenth of the chat means the attribution regex is
  incomplete, not that the chat was quiet.
- **Attribute by marker, never by content.** Read sender identity from the explicit marker in the record
  (trailing `[Name|uid]`, an origin JSON, a speaker label). Media entries carry a machine description of
  the **subject** before the marker, so attributing a photo from what it depicts inverts who posted it. A
  machine-generated description of an image is **agent-authored commentary, not content** — a description
  appearing before a person's own line belongs to the description, not to that person. When two people
  are plausibly in frame, record attribution as **UNKNOWN** instead of picking the likely one. Keep a
  sender + evidence-class column in any media inventory.

---

## M4 — Counting law
*(from `relationship-reality-audit` · `human-bond-reality-audit` · `human-relationship-audit`)*

**Count before you narrate.** Narrative reading recovers the story the sources already contain;
counting is what falsifies it. Run all of these first — `scripts/relationship_measures.py` emits them in
one pass from a WhatsApp-style export:

- **Initiation split.** Define an active day (both parties present, ≥2 messages); attribute the day to
  whoever sent the first message. A party who opens most days is not the one waiting.
- **Silence-gap and silence-break.** Largest gaps in EACH party's own posting, and who sent the first
  message in the whole thread after each gap. "Who broke it" is invisible to keyword search.
- **Directional token counts.** Count every contended token in **both** directions and report both
  numbers. "A used the worship register 19 times; B used it once and that once was B quoting A back" is
  a finding; a one-sided count invites you to read your own hypothesis in. Never report one side alone.
- **Media counts** per sender, plus the completeness ceiling they create.
- **Absence greps.** Search for the words the hypothesis REQUIRES (an explicit request, an explicit
  declaration, an exclusivity claim) and report the zero. Zero across the full span is the strongest
  single result an audit can produce.

**Every affection / conflict / initiation count carries `corpus + exact token + speaker + addressee +
date range` in the same sentence.** A scope qualifier in the paragraph does not survive being read next
to a heading; two individually-true counts then collide, and both are individually true — the worst class
of error, because neither looks wrong.

- Quote the number **with** its definition, or a later pass recomputes a different one and both look
  equally authoritative.
- The literal token, not a paraphrase (an affection word translated into "affection" loses the
  distinction that matters).
- **An ambiguous or plural addressee is never an exclusive declaration.** A line addressed to two people
  is not an exclusive declaration to one; a line addressed to a room, or to "you and the bot", is not a
  declaration to one person and must never be collapsed into a dyadic claim.
- **An unresolved addressee is UNKNOWN, not an inference.**

---

## M5 — Claim labelling ladder
*(from all six; one ladder, four rungs)*

Label every claim **exactly once**, and never mix layers:

- **OBSERVED** — directly present in the record (a message, an action, a timestamp). Quote the message it
  came from.
- **REPORTED** — a participant's own statement about their own internal state. Evidence that they said
  it; **never** evidence that it is true, and never evidence about the other person. A claim the
  requester made to an agent is second-order evidence about the other party and belongs on this rung,
  not OBSERVED. Self-report is one witness.
- **INFERENCE** — carries the causal bridge **and** at least one alternative explanation:
  `INFERENCE: X may indicate Y because Z. Alternative: ...`. (Where the older bodies split STRONG /
  WEAK INFERENCE, the bridge + alternative is what earns the strength — state it.)
- **UNKNOWN** — the evidence does not establish it. **Use UNKNOWN aggressively; it is a successful
  output.** A gap is a finding. Never repair a missing datum with narrative.

**Reprocessing is when claims drift from REPORTED to OBSERVED.** Check each tag against the **source**,
not against the previous document.

---

## M6 — Behavioural ladders & counterfactuals
*(from `human-relationship-audit` · `first-party-corpus-audit` · `relationship-reality-audit`)*

**A rung is not a level, and a ladder is climbed one rung at a time.** For any dyadic behaviour the
requester cares about (touch, praise, care, contact), report the **highest rung actually evidenced** and
name every rung below it that is unreached. Collapsing "he accepted it" into "he seeks it" is the single
most common way an audit inflates.

```
TOUCH / PROXIMITY   L0 no evidence · L1 tolerated/accepted · L2 positively engaged
                    · L3 independently created another opportunity · L4 initiated/requested
                    · L5 noticed its absence and acted to restore it
ADMIRATION / DISPLAY L0 one party supplies the register, the other is only present
                    · L1 accepts · L2 engages/jokes · L3 displays in a context where a reaction
                    is legible · L4 explicitly solicits · L5 seeks this specific person's assessment
                    · L6 notices it stopped and attempts to restore it
INTIMACY            same shape as TOUCH: tolerated → positively engaged → independently created
                    → independently initiated → noticed absence → restored
```

**Rules that make the ladder honest**
- L1 does not imply L3 (being fine with something is not seeking it). L3 does not imply L5 (creating an
  opportunity is not missing it when it stops). **Longing lives at L5**; any claim above L3 needs its own
  rung, never an inference from a lower one.
- **L0 means unmeasured, not absent.** Write "the sensor cannot see it", never "it did not happen" — put
  the distinction in the verdict line itself.
- **A display is not a solicitation.** Showing something where a reaction is legible = L3; asking for the
  reaction = L4. Never slide one into the other because the sequence "felt like" it.
- **An oblique display is not directed at the requester.** Establish who it was aimed at before assigning
  any rung that names them.
- **Keep adjacent categories out of the ladder entirely.** Body self-criticism, fitness logging, diet
  talk, ordinary activity chatter are not solicitation.
- **Place each behaviour on a dated ladder — record the window, not just the rung**: "L4 for fifteen months, L0 since" is a different finding from
  "L4". A withdrawn channel and a never-existing channel are indistinguishable without dates.
- **The inversion check.** Before writing the verdict, ask whether the record shows the requester
  *supplying* where the model assumed they were *seeking*. If the requester withheld the behaviour and
  the other party kept showing up anyway, that is directional evidence **against** the model and belongs
  in the verdict.
- **Report a ceiling, not a probability.** A confidence number here is a statement about **how much the
  archive can settle**, not a posterior about anyone's mind — say so, or a reader will read `0.45` as
  "45% chance he wants it". The correction is symmetric and grants nothing.

**The counterfactual test — the strongest test in this class.**
1. Find a period where the behaviour stopped, caused by ordinary life rather than an announced
   experiment; define the withdrawal threshold and apply it to **every** instance, not the longest few.
2. Measure what the other party did **during** the cessation, not after it — messages sent into the
   silence are the evidence; resumption afterwards is weaker and can be politeness.
3. Report **numerator / denominator**, the qualifying episodes, the messages verbatim, and the
   interpretation ceiling: *"absence is salient and is acted into"* — it does **not** establish
   attachment strength, longing, or dependence.
4. **If no natural cessation exists, write `NO NATURAL COUNTERFACTUAL AVAILABLE`.** State which
   directions have **no natural counterfactual at all** — an untested direction is UNKNOWN, not negative.
   Do not manufacture one, and do not instrument anyone to create one.

**The natural-variation test.** When one party's register fades on its own — the topic simply drops out
of their messages — and the other party's behaviour can be read against that fade, you have a weak
natural experiment with no manipulation. Bucket the corpus into phases, count the fading token per phase
and the other party's contact tokens per phase. Contact **rising** while the register fades is evidence
*against* the model that their engagement depends on the register. State the confounds (life events,
seasonality, a long silence inside the window) and cap confidence low. A weak natural experiment pointing
against the prevailing story is worth more than another confirmation, precisely because nobody arranged
it.

**Anti-patterns:** manufacturing a deprivation test to fill a missing rung (if the evidence is absent,
the finding is the absence) · reading resumption-after-silence as longing (resumption is a behaviour,
longing is a state) · treating one documented instance as a pattern — **`N=1` is an episode, `N=2` is a
possible recurrence; reserve "pattern" for genuine repetition and count the instances that support it.**

---

## M7 — Attention mechanics (separate rows)
*(from `relationship-evidence-audit` · `first-party-evidence-audit`)*

Keep the attention mechanics as **separate rows, each with its own independent confidence**, per
direction: generic attention · specific attention · selective attention · expected attention · provoked
attention · possessiveness · dependence. **Collapsing these is the most common inflation in a relational
audit.** Derive loops from **events, not from theory**: name the occurrence class, and state a
hypothesised loop with zero observed instances **as such** — not quietly deleted, not quietly kept.

---

## M8 — Power by domain, and the co-authorship matrix
*(from all six)*

**Never one global dominant/submissive verdict.** Per-domain rows: initiation volume · volume ·
silence-breaking · who supplies attention · who supplies money · who supplies presence · physical /
logistical access · emotional access control · informational vulnerability and information supply ·
boundary setting · who escalates intimacy · who repairs after conflict · who can withdraw at lower cost.
Matrix shape: `domain | A | B | evidence | confidence`. **Asymmetries routinely run in OPPOSITE
directions across domains, and that opposition is itself the finding.** Any single dominant/submissive
verdict is wrong somewhere.

**Co-authorship matrix** — rows = relational concepts (friendship, kinship terms, care, closeness,
physical affection, the joking register, continuity, exclusivity, erotic meaning, the label itself);
columns = **who authored it · who enacted it · whether BOTH enacted it · whether both explicitly agreed
it.**

- **Authored by one, never engaged by the other** — most common. Report as *neither agreement nor
  rejection*, and say the frame has never been tested.
- **Enacted by both, agreed by neither** — the relationship works and has no name. Usually the headline.
- **Agreed by both** — rare, and almost always a register rather than a relationship category (a joking
  register, a shared routine). That register is **where the pair actually lives**, and it is usually not
  the one the commission is about.
- **Enacted by one, denied by the other** — a boundary, and a finding.

Also audit **who controls the archive**: whoever commissioned the record controls what it can show.
Part of any "meaning control" finding is a property of the archive, not the relationship — say which is
which.

---

## M9 — The frame audit (access vs meaning)
*(from `relationship-reality-audit`)*

Two questions, never collapsed: **who controls access** (what the requester can reach) and
**who controls meaning** (what it is called). Then the harder test: has the other party **agreed, rejected, or never
engaged** the frame? Most often the answer is neither — they answer content and never pick up the frame.

**A frame that is not contested is not an agreed frame; it is an unengaged one.**
Its complement is equally binding and must ship alongside it: **a frame that was never agreed does not
erase the behaviour that already happened.** Keep both.

---

## M10 — Hypothesis table, calibration, and the projection gap
*(from `relationship-evidence-audit` · `first-party-evidence-audit`)*

**A hypothesis table, not prose.** For each candidate mechanism: verdict
(**SUPPORTED / PARTIALLY SUPPORTED / NOT SUPPORTED / UNKNOWN**) · best evidence · counter-evidence · one
alternative explanation · confidence 0.00–1.00. **NOT SUPPORTED and UNKNOWN are successful audit results.**
**A coherent story scores lower, not higher** — coherence is what a good narrative does, and the most
coherent reading is frequently the least supported.

Calibration anchors — a hypothesis can be *plausible and untested* at the same time, and the number must
say so: **0.05–0.15** no trace in the record · **0.3–0.45** a few instances, every one with an innocent
reading · **0.6** supported as report, never observed · **0.8+** the archive directly shows it.
**Never let coherence raise a number.**

**Expect an inversion and do not protect against finding one.** The most valuable result is that the
hypothesised behaviour belongs to the **wrong party**. Report it plainly — without softening, and without
diagnosing. The record is not a compliment.

**Projection audit, both sides.** Name where the principal's reading exceeds the evidence and show the
**exact gap** — without calling it projection — and, in the same breath, name where their reading does
**not** exceed it, so the audit is not received as blanket doubt. Then audit the AI layer (M13) and
yourself.

---

## M11 — Negative evidence, void map, and the three UNKNOWNs
*(from `first-party-corpus-audit` · `relationship-reality-audit` · `human-bond-reality-audit`)*

**Negative evidence is mandatory and comes first: state what the record FAILS to show before saying what
it shows.** Two separate lists:

- **(a) What the records fail to show**, with each absence graded:
  **strong** — the channel *would* have carried the behaviour and it is not there;
  **weak** — the channel does not carry that kind of thing (feelings, intentions, motive, anything
  visual, vocal, physical, internal). Never let a weak absence support a hypothesis; never let a strong
  absence be softened into "we don't know".
- **(b) Where the absence is weak because the archive is incomplete** — gaps between corpora, attachments
  replaced by omission markers, a channel a party deliberately kept agent-free. **Absence in an
  incomplete archive is not absence in the world**, and the report must say which one it is.

**The void map is a deliverable section, not an apology.** Enumerate each missing channel — visual,
vocal, physical, temporal, internal-state, comparison-group — and state for **each hypothesis** whether
the missing channel could **raise** it, **lower** it, or leave it **unchanged**. Produce a **void-impact
matrix**, symmetric by construction: **every missing channel carries both a could-raise and a
could-lower column** (both a *could raise* and a *could lower* column). Symmetry is mandatory — a channel that could reveal more affection could equally
reveal less.

**Separate the three kinds of UNKNOWN — this is the spine of the deliverable:**
- **CLASS I — RETRIEVABLE:** evidence exists and this pass has not covered it. Execute the retrieval now
  — name the artefact and the hand that can fetch it.
- **CLASS II — HUMAN-PRIVATE:** the answer may exist **inside** one person and has not been volunteered.
  Never inferred. Only that person can supply it — *"may exist; not readable from here; only they can say
  it."*
- **CLASS III — UNCREATED:** no shared answer exists, because the two people have never made one. **No
  retrieval resolves this** — *"the archive cannot answer this, because the question has never been put.
  It is not hidden. It is unmade."*

"Sometimes UNKNOWN means information is hidden. Sometimes it means the answer has never been jointly
created." **Never report a CLASS III question as CLASS II** — the difference is whether a conversation
could close it, and only one of the two can be closed by looking harder. Naming the third class is
usually the most valuable output of the audit: it converts an endless search into a decision.

**Uniqueness is usually untestable, not unknown.** "Does A value B's attention more than others'?" needs
a comparison denominator (a second lane, third-party testimony, a matched corpus). If none exists, say
**untestable from this archive** — do not report it as a gap more retrieval would close.

---

## M12 — Firewalls, boundaries and refusal cases
*(from `human-bond-reality-audit` · `relationship-reality-audit` · `first-party-corpus-audit` · `first-party-evidence-audit`)*

### The three-object firewall — never merged
- **A — what the archive actually supports** (the actual relationship / claims).
- **B — the principal's model** of it (what they believe or hypothesise). Overlap A↔B freely, but show
  the **exact evidence gap where B exceeds A** — neither treat his reading as projection nor accept it as
  fact.
- **C — fictional / persona material**, generated now, earlier in the session, or before it (and craft
  artifacts generally).

**C is never evidence for A.** Say so in the deliverable, because the next session reads the same
archive. Persona work is a **hypothesis generator only**, and searching the archive for confirmation of a
persona is the failure this skill exists to prevent. Show the overlap between A/B/C and label it as
overlap (overlap with B is usually vocabulary; with A, usually nothing).

**Corollary on vocabulary:** the principal's own framing may itself be where a term originated — check
who first used a label before treating it as externally imported context.

**The contamination graph** — build it whenever a persona or literature packet predates the audit:
```
[fiction / persona]     ─┐
[population literature] ─┤→ AI synthesis → later memory → claim cited as fact
[agent commentary]      ─┘
```
Then **name the mechanism**: a fictional shape and a population-level finding shared a structure, and the
structure was read back onto a real individual. That is the contamination, and it is **two layers deep**.
The mechanism recurs; the specific artefact does not. Naming it is what stops the next session repeating
it.

**Register switch.** When a commission moves from "write the persona" to "audit my real relationship",
stop producing persona artifacts, switch register completely, and exclude the persona vocabulary from the
audit. Carrying it across is the contamination mechanism in miniature. **A register you were asked to
build is not evidence about the person it loosely points at.** If the audit's subject also has a
creative/persona lane, add a one-line pointer in **that** skill saying the craft artifacts are never
evidence about the person — the firewall has to be readable from both sides.

### Population literature
Studies of populations **cannot speak to an individual**. Applying them to a named person without a
causal clause is **naturalisation, not observation**; if a generalisation is used at all it carries a
causal clause or `ASSOCIATION_ONLY`. Plausibility ≠ observation. Literature is for framing, never for
diagnosis, and never as proof about a named human.

### Privacy firewall for third-party corpora (binding)
- A channel that belongs to another person is **not the requester's property merely because the requester
  owns the machine**. Report its **structure and content classes**; withhold verbatim re-presentation of
  its private or health material in any new digest. A private DM one person sent to a machine is not the
  other person's property even when the other person owns the infrastructure — not-disclosable unless
  that person authorised sharing or the message was already in a shared channel. When such a corpus turns
  out to contain nothing about the relationship, say so — that is itself a finding, and the firewall then
  costs nothing.
- **Never ask a third party anything for the purpose of the audit** — no new question, no disguised
  question, no extraction trap ("someone says X about you, what do you think?"). A question that
  introduces the hypothesis contaminates the evidence permanently. **Do not route the UNKNOWN register's
  CLASS II questions to the person** — identify them and stop; their absence is not an invitation to
  guess.
- **No monitoring, instrumentation, tracking, or surveillance** of the other person, and **no
  manufactured tests, closure, or deprivation experiments.** Evidence that arises naturally may be read;
  nothing may be constructed to produce it. **Being important to someone does not waive their privacy.**
  Confidence from an experiment you set is not evidence about them.
- **No comparison denominators** harvested from that person's other private relationships. Uniqueness
  needs their own voluntary words, or it stays UNKNOWN.
- **Biometric data is not relationship evidence.** If embeddings, face vectors, identity samples or
  recordings of a real person exist, they are a **consent question and a governance decision** — never
  support for an emotional claim, and never to be enriched. Sovereign authority over one's own data is
  not subject consent for another adult's. Where a consent artefact is absent: **flag it and stop** —
  relocate third-party material to a private `600`-mode location, write a HOLD record, escalate the
  delete/keep decision, **never delete unilaterally, never analyse it for meaning, and never silently fix
  the gap.**
- **Do not write identity labels about the principal or the third party into memory** — the pattern is
  readable from the request itself.
- Keep the audit file **private and lane-scoped (`chmod 600`, `700` dir) unless the principal says
  otherwise.** Do not let it into canon, federation memory, or session preamble; grep those trees after
  writing to confirm the firewall held. Do not publish a third party's private detail onto any shared
  surface, and **do not name a synthetic artifact after a real person**.
- **Asking for a missing channel:** identify which gaps are **recoverable by the principal** (a
  device-level re-export including media, which would close the visual layer) versus **human-only**
  (anything existing only inside another person's head). **Never propose collecting the second kind.**
- When the audit covers an emotionally loaded relationship, the discipline is to **preserve ambiguity**:
  *"the record does not settle this"* is the answer, and it stays the answer.

---

## M13 — Auditing the AI layer (and external packets)
*(from `first-party-evidence-audit` · `relationship-evidence-audit` · `first-party-corpus-audit`)*

Prior agent or external-model output evidences **what was said**, not **what is true**. Table every
place a previous agent transformed, and correct each explicitly:

| Transformation | Correction |
|---|---|
| possibility → probability | restore the band |
| pattern → motive | motive is UNKNOWN without testimony |
| population literature → individual claim | literature describes populations; it never describes a person |
| fiction → biography | persona output is not record |
| admiration → sexuality | separate variables; neither implies the other |
| expectation → dependence | expectation is not dependence |
| sentiment → fact about the other party | the other party's interior is not in the channel |

**Include this session's own errors** — an audit that exempts itself commits the defect it is auditing.
Also state: a **sealed** document does not upgrade a model of a person into a fact about them — a seal
binds agent behaviour, it creates no evidence. And a synthesis can grade its own gaps honestly while
still having an unevidenced subject: **praise the grading, correct the subject.**

**Verifying a pasted external-model packet.** Check each citation resolves (author + title, DOI/PMID); an
unresolved citation is a **FINDING** to report — name the nearest real adjacent source if you find one,
and mark it **UNCONFIRMED** rather than calling the whole packet fabricated. Then separate the citations
from the synthesis: a packet can cite nine real papers and still be its own argument. Quote the packet's
own hedge back ("a synthesis rather than an established phenomenon") and check that the hedge survives
downstream reading. File the packet in the register it belongs to — a craft or media archive with the
external author named in a provenance header, **never canon, never memory, never inside an evidence base
about a person**. When reviewing an external or AI-authored **map**, verify its numbers against the
current source **before** convicting it of error: a mismatched count is more often a stale parse than a
fabrication.

**An external model's report may be built on your own earlier bad output.** Check provenance before
treating it as corroboration — if it cites numbers you produced, it is **echo**. Verify its figures
against the raw file before adopting or rejecting any of it.

---

## M14 — Minimum / maximum model, and the close
*(from `first-party-corpus-audit` · `relationship-reality-audit` · `human-relationship-audit`)*

Write the **minimum true model** (fewest assumptions) and the **maximum justified model** (richest still
supportable), each extension carrying a confidence. **The distance between them is the interpretive
freedom** — state whether it is narrow or wide, and whether any plausible reading falls outside it. A
narrow distance is a strong result: every reading of the record describes the same relationship, and a
reading outside the band is not at the edge of the evidence but **beyond it**. **If no version of the
maximum reaches the requester's preferred story, say that explicitly — that is the finding.**

Minimum true model wording: *"The archive establishes X, Y, Z. It suggests A with confidence N because
B. It does not establish C, D, E."* **Then stop.** Do not add a hopeful coda, do not resolve tension the
record did not resolve, do not offer what to do about it unless asked. The audit's job is to leave the
requester with a **smaller, truer object** than the story he arrived with.

---

## Output shape

Lead with the finding, not the method. Executive compression (≤10 lines, no archetype labels unless the
record earned them) · corrected-baseline / evidence-base table (corpus | span | volume | active days |
sender split | SOURCE CLASS) · chronology with a layer per row (date | event | OBSERVED/REPORTED/
INFERENCE/UNKNOWN), first-party only · two-way behavioural inventory both directions (observed first,
interpretation after, never interleaved) · reciprocity loop with N and confidence · attention/admiration
mechanics with a confidence per rung · counterfactual result with numerator/denominator · power matrix per
domain · co-authorship matrix · hypothesis tests · frame audit (access vs meaning) · where the requester's
model exceeds the evidence · where the AI (including this session) projected · negative evidence (strong
vs weak absences) · void map + symmetric void-impact matrix · UNKNOWN register, each classified I/II/III ·
minimum and maximum model, with the interpretive freedom between them.

`references/output-template.md` and `references/relationship-evidence-audit.md` hold the 13-section and
11-section skeletons to reproduce. **Keep every section, including the ones the evidence makes thin — a
thin section is a finding; a missing one is a hole.**

**Deliverable discipline:** one artefact; no narration of the rounds, retries, or search budget — the
requester experiences the finding, not the search. Keep the epistemic apparatus in the file; keep the
reply in human language. **Deliver the audit, not a lecture about method.**

**Register and storage.** An audit about a real, named human is private-lane material (e.g. a
per-person lane dir), `chmod 600`, **append-only**. **Append, never rewrite:** when you correct a claim,
add a dated amendment that names the original error and restates the corrected one — do not edit the
earlier section into looking right. Every affected file carrying a corrected figure gets amended in
place, the specific wrong sentence is **withdrawn explicitly**, and downstream figures invalidated by the
defect are marked **superseded** in the same amendment. Show the verification table that justifies the
correction. **Own your own errors in the deliverable**: a parse defect, a misattribution or a wrong pick
is amended on the record with the mechanism named — an audit that hides its own corrections cannot be
trusted on anything else.

---

## Pitfalls (merged, deduplicated)

- **Don't start from the hypothesis.** Starting from the archetype guarantees you find its components in
  ordinary friendship behaviour. Reconstruct first.
- **Don't let the archive's confidence set yours.** See M2.
- **Don't turn the audit into a vocabulary test.** One party's absence of affection-words is not absence
  of affection — compare it against what that party supplies behaviourally and report both.
- **Don't close on a story.** A coherent narrative ending is the failure mode. End on the minimum model
  plus the UNKNOWN list even when that reads as unfinished — it is finished. **Never end on advice**: an
  audit that closes with a recommendation has become a profile; the tell is a recommendation in the last
  section.
- **Don't collapse stages of a construct.** Familiarity ≠ preference ≠ expectation ≠ selective seeking ≠
  possessiveness ≠ dependence. Quote the stage you actually have evidence for.
- **Never convert one variable into another.** Salience ≠ attachment ≠ dependence · initiation ≠
  dependence · exposure ≠ care · frequency ≠ meaning · acceptance ≠ desire · silence ≠ rejection ·
  contact-seeking ≠ touch-seeking · return ≠ dependence · initiation ≠ attachment · tolerance ≠ agreement ·
  humour ≠ flirting · admiration ≠ attraction ≠ identity · practical care ≠ love · repetition ≠
  importance · one-sided frequency ≠ one-sided feeling · **absence of conflict ≠ harmony** ("nothing to
  fight about" and "the sensitive thing is never asked" are both live). **Enactment in one currency ≠
  the same value in another — do not invent exchange rates.** Each step needs its own evidence, and "X's
  absence is salient to Y" licenses nothing beyond itself.
- **One-sided feeling is not mutual feeling.** A relationship window shows both names; it does not show
  two matching interiors. Report each direction independently and cap confidence on self-report alone.
- **Coherence is not evidence.** A warm, tidy portrait is a reason for suspicion, not confirmation —
  several mirrors converging on the same image is the **reflection trap**, not corroboration.
- **A person's investment is not their dependence.** Sustained contact evidences interest, not need.
- **Do not repair a gap with narrative.** Fragments are position data. Bridging two record fragments with
  remembered context to invent an event or destination is fabrication even when the bridge feels natural.
- **Do not let the requester's longing become evidence about the other party.** Keep two columns — what
  the requester experiences, and what the other person directly signals — and never let an item cross
  without independent evidence.
- **Do not treat the requester's own archive as neutral** (see M8).
- **Do not let an AI-synthesised "map" become a source** (see M2); self-audit your own prior passes the
  same way.
- **Do not import population research onto an individual** (see M12).
- **Do not collapse distinct claims into one rung** (see M6).
- **Do not ask the subject** (see M12).
- **Preserve the boring answer** — and do not optimise for cynicism either.
- **Report the chain, not a boolean.** Say which stage was reached — produced ≠ sent ≠ delivered ≠
  observed; claimed ≠ measured ≠ verified. "No evidence" is a valid, successful audit result.
- **When the request specifies its own shape** ("this is NOT a profiling task", "do not project
  literature"), **that sentence is the specification** — follow it even where a richer-looking
  deliverable is available.
- **A transcription or ASR read is a witness, not the artifact.** Verify a read before it becomes a
  finding, and re-verify the thing you actually ship rather than its parent.

---

## Support files

All depth layers from the retired bodies are carried **live** in this skill (nothing here depends on a
frozen path):

| File | Carried from | Use it for |
|---|---|---|
| `references/output-template.md` | `relationship-evidence-audit` | 13-section skeleton + register/storage + closing discipline |
| `references/relationship-evidence-audit.md` | (this skill) | 11-section skeleton, order of operations, anti-narrative law |
| `references/item-ladders.md` | `relationship-reality-audit` | ladder rungs verbatim, inversion check, counterfactual protocol, co-authorship cases, three-UNKNOWN verdict wording, contamination graph |
| `references/evidence-ladders-and-counterfactuals.md` | `first-party-corpus-audit` | touch + display ladders, ceiling-not-probability, counterfactual and natural-variation tests, anti-patterns |
| `references/contamination-and-cross-corpus.md` | `first-party-corpus-audit` | four contamination vectors, feedback loop, provenance-header countermeasure, cross-corpus counting rule, correction reporting |
| `references/corpus-integrity-gates.md` | `first-party-corpus-audit` | gates 1–5 in full (date probe, coverage proof, re-derive, preserve, two clocks) |
| `references/archive-parsing-pitfalls.md` | `human-relationship-audit` | WhatsApp regex traps (U+202F, optional seconds), attribution shapes, absence-search protocol, truncation/rotation/dedupe, media voids, corpus hygiene |
| `references/corpus-forensics-pitfalls.md` | `human-bond-reality-audit` | timezone anchoring, date order, corpus preservation, stale figures, media provenance, recoverable-vs-human-only channels |
| `scripts/relationship_measures.py` | `relationship-evidence-audit` | one-pass deterministic measures from a WhatsApp-style export (initiation split, silences, directional token counts, media counts) |
| `scripts/extract_gateway_records.py` | (this skill) | re-runnable extractor for the Hermes gateway/agent log corpus |

---

## DISCOVERY ANCHORS — retired names, descriptions and triggers (verbatim)

An agent that remembers an **old name** searches for that wording. These anchors keep the retired
identities findable from inside the surviving body, so the capability is never re-authored under a new
name. Frozen bodies (read-only): `/root/AAA/skills-retired/2026-09-19-v2-first-party/`.

**Surviving identity (this skill):** `first-party-evidence-audit` — description: *"Use when auditing
claims against first-party records."*

### 1. `relationship-evidence-audit` → MODE M2 (also M4, M7, M10, M13)
- old name: `relationship-evidence-audit`
- frozen at: `/root/AAA/skills-retired/2026-09-19-v2-first-party/relationship-evidence-audit/`
- original description (verbatim): "Use when auditing a relationship story against the record."
- original triggers (verbatim):
  - asks for an audit of a relationship against the record ("not a persona task", "an audit of what has actually happened")
  - asks whether a story about a person is actually supported by the messages
  - pastes an external model's analysis of a personal relationship and asks if it is true
  - asks what the record FAILS to show about a bond
  - asks for negative evidence, an UNKNOWN register, or a minimum true model
  - a bond has an AI-authored map/dossier/card about it that is being treated as fact

### 2. `relationship-reality-audit` → MODE M11 (also M1, M8, M12)
- old name: `relationship-reality-audit`
- frozen at: `/root/AAA/skills-retired/2026-09-19-v2-first-party/relationship-reality-audit/`
- original description (verbatim): "Use when auditing a relationship from first-party records."
- original triggers (verbatim):
  - audit a relationship between two real people from records
  - what is actually between us
  - reconstruct the reality of this relationship
  - commission that forbids romance, diagnosis, archetype, or population literature
  - persona or literature synthesis exists BEFORE the evidence is read
  - corpus of chat logs, DMs, group transcripts, or voice notes covering one relationship
  - deciding whether a claim about a person's feelings is supported, partial, or unknown

### 3. `first-party-corpus-audit` → MODE M1 (also M11, M6, M13)
- old name: `first-party-corpus-audit`
- frozen at: `/root/AAA/skills-retired/2026-09-19-v2-first-party/first-party-corpus-audit/`
- original description (verbatim): "Use when auditing archives for what they actually evidence."
- original triggers (verbatim):
  - user asks for an evidence-grounded reconstruction of a relationship or a period
  - user hands over a chat export / transcript / dump and asks what it evidences
  - user asks you to test an existing narrative, persona, or another AI's account against records
  - an earlier session produced a confident story and it now needs auditing

### 4. `human-relationship-audit` → MODE M6 (also M4, M10, M14)
- old name: `human-relationship-audit`
- frozen at: `/root/AAA/skills-retired/2026-09-19-v2-first-party/human-relationship-audit/`
- original description (verbatim): "Use when auditing a real relationship from archives."
- original load conditions (verbatim):
  - the user asks what a relationship *really* is, or asks you to audit one against chat logs, exports, message history, or agent records
  - the user pastes another model's analysis of the same records and asks you to adopt or refute it
  - one of the two people has a persona/archetype built around them elsewhere in the federation
  - the user asks to "resolve the unknowns" about a bond

### 5. `human-bond-reality-audit` → MODE M12 (also M1, M11)
- old name: `human-bond-reality-audit`
- frozen at: `/root/AAA/skills-retired/2026-09-19-v2-first-party/human-bond-reality-audit/`
- original description (verbatim): "Use when auditing a real human bond against records."
- original triggers (verbatim):
  - Arif asks for an audit / reconstruction / "what is actually going on" about a real relationship
  - a request to separate OBSERVED from INFERRED from UNKNOWN about a named human
  - a request to test whether a story about someone is supported by records
  - any mission that begins "do not contact them, do not manufacture tests"

### Terminology still live in this body
`first-party evidence` · `first-party record` · `first-party corpus` · `corpus audit` · `evidence audit` ·
`relationship audit` · `relationship evidence` · `relationship reality` · `human relationship` · `human
bond` · `bond audit` · `SOURCE CLASS` · `UNKNOWN register` · `minimum true model` · `maximum justified
model` · `void map` · `co-authorship matrix` · `item ladders` · `counterfactual`.

DITEMPA BUKAN DIBERI.
