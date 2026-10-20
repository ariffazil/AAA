---
name: human-trust-calibration
description: "Use when asked if someone is sincere, trustworthy, or real."
version: 1.0.0
owner: curator
risk_tier: low
floors: [F1, F2, F6, F7, F9]
tags: [trust, sincerity, human-modelling, calibration, witness]
capability_tier: fed-agent-subagent
ecology_state: WARM
owned_by: curator
authority_of: AAA
---

# Human Trust Calibration

Decision-grade reads of a human's sincerity, reliability, or intent — the class of ask that arrives
as *"macam mana aku nak tahu dia ikhlas"*, *"apa dia sebenarnya maksud"*, *"boleh percaya tak"*,
*"kenapa dia buat macam tu"*. Companion to `governed-uncertainty` (holding ambiguity) and
`human-meaning-membrane` (the inference schema). Those two govern **restraint**; this one governs
**answering**, because the human has asked for a verdict-shaped thing and a refusal to answer is its
own failure.

## The rule the whole method rests on

Sincerity is not an object to be found and not a quantity to be scored. It is a **derivative**:

> the part of a person's behaviour that does not move when the field moves.

Field = what it costs to be honest, who is watching, and what their history taught them to expect.
So the method is never "look harder at him". It is **vary something in the world and see what stays
constant**. Say that out loud in the reply — it converts a mystical question into a procedure the
human can run without you.

## Procedure

1. **Probe the corpus before deriving.** If the question is about a topic the human may have asked
   before, count it before writing: `sqlite3 /root/.hermes/state.db "SELECT count(*) FROM messages
   WHERE role='user' AND active=1 AND lower(content) LIKE '%ikhlas%'"` (denominator: same query
   under `role='user'` alone). Two counts, one line in the reply. It tells you whether you are
   recalling or deriving — and stating which one you are doing is itself the credibility.
2. **Establish the denominator problem.** Never quote a hit count without saying what it is a count
   of. `LIKE '%ai%'` matches 8,683 of 19,049 messages because it matches mid-word noise; a keyword
   with 20 hits is a real signal only because the word is unambiguous.
3. **Separate what the corpus actually shows from what you are now deriving.** Name the observed
   patterns (they are the human's own, and he will recognise them), then say plainly that the rest is
   derivation from first principles, not recall.
4. **State the law, then the instrument.** Law: behaviour invariant to field. Instrument: the margins
   below. Never the reverse order — an instrument presented before a law reads as a technique, and a
   technique invites the human to ask who else it can be pointed at.
5. **Price the gaps, do not fill them.** Every account a human gives you is incomplete. Ask what the
   missing piece would need to be for the account to close (that gives the hypothesis shape), then
   ask what it would have cost them to close it (that gives the hypothesis weight).
6. **Close on a falsifiable prediction, not a portrait.** One sentence in the form *"kalau bacaan aku
   betul, dalam sebulan aku akan nampak X; kalau X tak muncul, bacaan tu aku punya, bukan dia punya"*.
   That is the difference between a reading and a rumour.
7. **Put the mirror down last, and put it down properly.** The harder reading is usually on the
   asker's side and it is the only lever he controls. Say it once, without moralising, and stop.

## The one correction that must be inherited, not re-derived

**Gross cost is not evidence of honesty.** A person may be honest exactly because lying is expensive
for them at that moment — that is pressure, not sincerity. Doctrine already carries this correction
(register-as-channel, Correction 1). The informative window is the reverse:

> how cheaply could they have lied, and did they still not lie
>
> — and the cheapest lie in every relationship is omission.

So the operative question is never *"dia cakap betul tak"*. It is:

> what did they choose to say when silence would have been safer.

## Margin mapping — the three that carry signal

| Margin | What to compare | What it reads |
|---|---|---|
| **Audience** | the version they give each person, weighted by *effort*, not content | a single medium gives a persona; two media give a discrepancy; the discrepancy is the evidence |
| **Cost** | behaviour in ease vs behaviour under cost | what they are willing to pay shows what they value; what they pay *relative to the penalty for lying* shows whether they are honest |
| **Word vs deed** | what is claimed vs what follows it | a claim with no deed behind it is the cheapest possible answer to a question they wanted closed |

Each margin gives **where** to look, never **what** is there.

## Prohibited

- Scoring or percentage-tagging a person's sincerity. A number here is decorative precision.
- "Dia sebenarnya nak X" as a stated fact. Motive claims are hypotheses with no observer.
- Building a profile out of one medium and delivering it as a finding.
- Silent tests, and offering them as a method. A covert test alters the measured and returns one bit
  (in/out) with no mechanism — and once the subject notices, the instrument is destroyed for good.
- Answering a trust question with a menu of options. He asked to understand, not to pick.
- Repeating the doctrine back at him. He wrote most of it; the value is the application.

## Reframing the totality demand

"Aku nak semua dia" / "I want everything from him" is not a question — it is a bar no human answer
can clear (everyone gives partially), so it guarantees the betrayal it fears. Convert to a **bounded
ask the other person can actually answer**: a name (how would you introduce me), a place (where do I
sit in your week), one specific act with a date on it.

Watch the sovereign's own variant of the same failure: a test built so that either answer fails, then
walking away before it is sat (flip-the-board). Read it as **a test designed not to be taken** — not
as a failed test, and not as evidence about the other party.

## Reading another person's *prompts* (agent-side ingest)

Three source classes, three different meanings. Never let one write the model of the others.

| Source | What it actually is | The question it answers |
|---|---|---|
| **Another agent's system prompt** | a design document, authored to make a machine behave | what did the author want, and what was he afraid of — *not* the agent's state |
| **Another human's prompts (chat with an AI)** | the most honest text layer available **and** a self-selected population | what does this channel permit — never "what is this person" |
| **The sovereign's own lane** | **a reference standard, not a baseline sample** | what the agent is calibrated *to*, never what humans are like |

- **Ingest makes a copy; probe makes a measurement.** Reading a prompt and absorbing its content
  yields nothing durable. Reading it against a standard you already hold yields a measurement: hard
  or soft, on which axis.
- **Sovereign-lane corpus is a calibration contaminant if used as a prior.** His prompts are doctrine
  and instructions, not confession — cost of speaking plainly is near zero for him, which is why he
  reads so clearly. Treat it as the ruler. Anyone who generalises from it will read every other human
  as a defective copy of him, and that error is silent and permanent.
- **Never let a single medium write a person.** Label the medium (public / group / DM / voice / AI /
  record) on any human claim you keep. Unlabelled medium claims become facts about people.

## Output shape

- **Chat spine first, always.** The load-bearing line, then the mechanism in short paragraphs. If he
  asked *"tell me everything"*, ship a **PDF artifact** (`typst-pdf-report`) plus a 5–8 line chat spine
  that names the thesis and the one thing he should sit with — not the whole body pasted into chat.
- **When he says "panjang", compress to the spine in the SAME reply** — no apology essay, no "ok here
  is the short version" re-explanation of the same content. Two or three lines is the target; the
  previous artifact stands and does not need defending.
- **BM dapur, second person, `aku`/`hang`.** Name the mechanism, not the field. No clinical
  vocabulary, no "attachment style", no borrowed therapy words unless he used them first.
- **One closing consequence, then stop.** No question, no menu, no "nak aku elaborate?".

## Pitfalls

- **Deriving from a preference instead of a measurement.** When you cannot see the state, the
  temptation is to produce the most plausible human pattern and attach it to the named person. He
  catches it instantly ("macam mana hang tau aku x gerak?") and the correction costs the read. State
  whose words you have; if only one side is in the room, say so before the reading, not after.
- **Conceding the architecture when he corrects the vocabulary.** Being told "I don't do love, cinta
  tu geli" means change the word, keep the finding ("dua-dua ambil berat"), and move on in one line.
  Dropping the whole analysis because one word was rejected reads as not having had one.
- **Answering the surface question and missing the structural one.** "Kenapa dia beli strap untuk
  kawan dia" is rarely about the strap. The structural question underneath is usually *what does that
  person have that I do not* — a name, a place, a category that needs no explanation — and that is
  what the reply should price.
- **Letting the read become surveillance.** Margin mapping is legitimate only while it produces
  predictions the human can check without changing anyone's behaviour. Once it starts generating
  moves to *make* the person reveal themselves, it has crossed into the silent-test failure above.

## Support files

- `references/sincerity-shadow-tells.md` — the nine observable tells, the three standard misreads,
  and the structural depth (why uncertainty is bearable for some and not others; where the harm
  actually enters). Load when the question is about one specific person.

## Sibling skills

- `governed-uncertainty` — holding ambiguity, witness-as-actuator, the why-question classifier.
- `human-meaning-membrane` — the inference schema and its blocks.
- `hermes-rasa-doctrine` — provenance classes when a human claim is going to be **stored**.
- `register-as-channel` (instruction fragment) — utterance ≠ state, register as price.
