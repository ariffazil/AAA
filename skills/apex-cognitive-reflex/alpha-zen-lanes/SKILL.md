---
name: alpha-zen-lanes
category: apex-cognitive-reflex
description: "Use when building ALPHA-ZEN daily pulses for the group."
version: 1.0.0
triggers:
  - "alpha-zen"
  - "alpha signal"
  - "body check pulse"
  - "zen signal"
  - "daily pulse group"
---

# ALPHA-ZEN — WORLD → BODY → EARTH

## OPEN QUESTION — the target group (flagged 2026-09-18, NOT resolved)

There is **no Telegram group named ALPHA-ZEN**. A bot cannot create groups.

Current live target: `telegram:-1003815535761`, shown as **SADO** in Telegram. Verified as the
Arif+Syed space (both user ids post in it: 761 and 209 attributable messages). Prior sessions
discussed renaming that group ALPHA-ZEN rather than creating another.

**Two readings, and they are not equivalent:**
1. "ALPHA-ZEN group" names the existing Arif+Syed group, whatever Telegram calls it. → the current
   target is correct, nothing to do.
2. He wants a NEW dedicated group called ALPHA-ZEN. → he must create it and add the bot, then the
   target changes.

This was resolved by INFERENCE, not by confirmation. If reading 2 is what he meant, the pulses are
landing in a group that also carries unrelated chat. Cheap for him to confirm or correct; expensive
to discover later.

## The card: 9 components, 18 signals

Each card row carries an ARIF signal and a SYED signal selected INDEPENDENTLY — 9 conceptual
components, 18 signals. Fixed structure:

```
01 WORLD      | 02 REALITY    | 03 CLOCK     -> KENA_TAHU  (sourced; NO poetry in this tier)
04 OUR WORLD  | 05 MONEY      | 06 HUMAN     -> SUKA_TAHU  (personal, must still have substance)
07 CONNECTION | 08 RANDOM     | 09 TONIGHT   -> EUREKA     (connect, do not merely fetch)
```

**The one rule that matters:** never fill a slot because the template demands nine. Nine reasons to
stop scrolling beats nine filled boxes. If nothing real qualifies, publish fewer rows and say so.

### Three epistemic tiers
- **KENA TAHU** — externally grounded. News, event, market data, deadline, actual observation.
- **SUKA TAHU** — personalised curiosity. Softer, but still substantive.
- **EUREKA** — where the machine earns its existence. Take two things neither man would put
together and ask what invariant connects them. Working classes: progressive overload �” position
sizing; fatigue �” drawdown; deload �” de-risking; stratigraphy �” provenance; unconformity �” the
gap that proves something happened.

### Lanes
**ARIF** rotates through: agentic AI / arifOS / MCP → intelligence architecture → geology & energy →
oil & gas → capital & business → institutions → epistemology → human meaning → strange reality.
Always ask what it means for intelligence, humans, institutions, Earth or capital.

**SYED** has TWO permanent attractors that must survive ranking every single day:
**gym/body** AND **gold/trading**. The gate refuses a card missing either. His universe: strength,
hypertrophy, recovery, nutrition science, ageing while retaining capacity; gold, USD, real yields,
central banks, positioning, drawdown, trading psychology. Cross them deliberately.

## CHRON — a ranked clock, not a footer

`/root/AAA/scripts/chron.py` reads `/root/AAA/scripts/chron_events.json`.

- **Never store a day-count.** Store `target_date`; compute the delta at render. A stored "21 days"
is silently wrong the moment the file is not regenerated — and it fails quietly, still saying 21 days
a month later.
- **Rank, don't sort by date.** score = urgency × consequence × actionability × confidence. Urgency
saturates near the date and flattens beyond 90 days. Verified live: Budget 2027 (21 days, HIGH)
correctly outranks a fuel-price window 5 days out (MEDIUM).
- **Expiry is automatic.** A passed event leaves the pool. No stale countdown, ever.
- **`audience` is the privacy filter.** An `arif`-only event is invisible in the shared card. This is
enforced in code, not trusted to whoever writes the prompt.

## The gate is a wall

`/root/AAA/scripts/alpha_zen_gate.py`, wired into the renderer. It REFUSES: wrong row count; wrong
tier counts; KENA_TAHU without a source; a Syed lane missing gym or gold; an Arif lane with no
structural signal; an unverified quote attribution; a duplicated subject across two rows; a private
marker leaking into the card. Suite: `test_alpha_zen_gate.py` (12/12 with negative controls).

When it says HOLD: **fix the content.** Never weaken a threshold to pass. A gate that only ever says
PASS is indistinguishable from no gate.

## The product

Three daily pulses into the **Arif + Syed group** (`telegram:-1003815535761`, named
"SADO" in Telegram, discussed for rebrand to ALPHA-ZEN). A different organ dominates each moment
of the human day. arifOS does NOT write the content — it orchestrates:

```
OBSERVE → organ intelligence → HERMES epistemic filter → compress → Telegram
```

| Time | Pulse | Organ | Human function |
|---|---|---|---|
| 07:15 | ALPHA SIGNAL | WEALTH + news + HERMES | Orient to the world |
| 14:00 | BODY CHECK | WELL + HERMES | Recalibrate the organism |
| 21:15 | ZEN SIGNAL | GEOX + HERMES | Return to reality and peace |

The questions each organ asks:
- WEALTH — *what is moving?*
- WELL — *can the human carry it?*
- GEOX — *what remains physically real?*
- HERMES — *what are we claiming that reality does not justify?*
- arifOS — *does the whole thing stay coherent and bounded?*

## Hard rules (these are the ones that get violated)

1. **One screen.** 250-500 words maximum. If it needs scrolling, it will not be read.
2. **Not serious.** This is two mates talking. No corporate voice, no "I have analysed".
   If it reads like a memo, rewrite it.
3. **Include the local buzz.** Every pulse carries at least one checkable, near-term, real-world
   thing near them — a gig, a place to eat, an outdoor spot. This is what makes it alive instead
   of a dashboard. NEVER invent one: if no real listing is found that day, omit it rather than
   fabricate a venue name.
4. **Syed is a recipient, never a subject.** He is in this group. Do NOT address him directly,
   do not comment on his training, body, health or family, and do not make him the topic.
   Write FOR two friends, not AT one person. (relationship-kernel: human-human beats human-AI.)
5. **No medical diagnosis, ever.** WELL observes patterns in what was reported. It never says
   "you are tired" - it offers a reset and returns the judgement to the human.
6. **Never claim F13-RATIFIED or SEAL** unless the kernel actually granted it.

## ALPHA SIGNAL - 07:15 (WORLD)

WEALTH x news x HERMES. The only genuinely news-heavy pulse.

- **WORLD NOW** - 3-5 consequential developments from the previous 24h: Malaysia, ASEAN, energy,
  AI/tech, geopolitics, markets.
- **MONEY FLOW** - what actually moved: MYR/USD, oil/LNG, rates, equities, commodities.
- **WHY IT MATTERS** - convert news into causal meaning: event -> incentive -> capital flow ->
  second-order consequence for them.
- **SIGNAL vs NOISE** - label each: documented / inferred / contested / unknown.
- **BUZZ** - 1 event/gig + 1 place to eat + 1 outdoor spot, Penang-Kedah belt, checkable.
- **Not investment tips.** Economic situational awareness. Never "buy X".

Close: *"Apa yang berubah dalam dunia sejak semalam yang patut ubah cara kita fikir hari ni?"*

## BODY CHECK - 14:00 (BODY)

WELL x HERMES. By afternoon, headlines matter less than whether the substrate can carry the mission.

- **BODY** - sleep/recovery, movement, food/hydration, physical load.
- **MIND** - attention fragmentation, cognitive load, rumination vs useful thinking.
- **WORK** - what actually moved since morning.
- **ROLE** - meaningful work, or just responding to demands?
- **YIN/YANG** - name ONE imbalance if present: action without recovery / thinking without
  embodiment / discipline without joy / comfort without challenge / work without relationship.
- **ONE intervention only** - walk, eat, hydrate, stop scrolling, finish one task, train, or rest.

Boundary line, always:
> *Machine can observe patterns. Only Arif knows Arif's rasa; only Syed knows Syed's rasa.*

Close: *"Badan dan kepala hang sekarang perlukan push - atau recovery?"*

## ZEN SIGNAL - 21:15 (EARTH)

GEOX x HERMES. The human quiet layer, placed BEFORE the machine's nightly metabolism begins
(22:00 arifFlow digest -> 22:30 niat picker -> 22:45 niat executor -> 22:50+ dream layer).

- **EARTH** - ONE Earth-scale observation. Sky, weather pattern, deep time, season, moon, ocean,
  climate, energy cycle, a remarkable scientific finding. Not geology-news.

  GEOX is here for its epistemic principle, not its data:
  *Earth does not care about our narrative. Reality leaves traces. Deep systems evolve slowly.
  Layers matter. Time matters.*

- **HERMES** - three lines, never merged:
  > Observation: <what is actually the case>
  > Interpretation: <a reading that may or may not hold>
  > Meaning: belongs to Arif and Syed, not to the machine.

  Never imply nature carries a message for humans. Perspective, not omen.

- **CHRON** - the time reminder. This is the point of the whole pulse.
  Compute LIVE from real dated facts; never hardcode and never invent a date:

  ```bash
  python3 /root/AAA/scripts/chron.py
  ```

  Renders the running clocks that are actually dated (OD1 Mar 2027, budget tabling, year elapsed,
  milestones they named). Frame it as finite time they cannot get back - gentle, never morbid,
  never a countdown-to-doom. If a date is not on file for someone, say nothing about them rather
  than guessing. One or two lines, no table.

- **TODAY** - what proved true / what proved false / what remains unknown / what does not need
  solving tonight.
- **GRATITUDE** - one human, thing or experience worth recognising.
- **LET GO** - one cognitive burden that need not cross into tomorrow.

Close: *"Kalau semua noise hari ni senyap, apa yang masih benar?"*

## Failure behaviour

Each pulse fails SOFT, exactly like `morning_briefing.py`: a dead source removes its line, never the
message. If an organ MCP is unreachable, fall back to web search and **label the fallback** - an
orchestrator that silently swaps an organ for a search engine is lying about its provenance.

## Do not add another morning brief

06:30 `arifos-morning-briefing` (systemd) already fires, and 06:00 `docforge-edition-daily`
delivers Arif's Executive Brief to his DM. ALPHA-ZEN is a DIFFERENT product for a DIFFERENT
surface (the two-person group). Before scheduling anything, list cron jobs AND systemd timers -
this host has four schedulers and a duplicate is invisible from inside any one of them.
