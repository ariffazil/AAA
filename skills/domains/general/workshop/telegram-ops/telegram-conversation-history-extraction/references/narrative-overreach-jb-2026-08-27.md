# Reference: Narrative Overreach (JB Fabrication, 2026-08-27)

## What happened

User: *"I'm arif. What do Syed talk to my agent today"*
User (turn after): *"Apa benda JB hang mengarut"*

I (Hermes) extracted the 25→26 Ogos timeline from gateway.log correctly, then in the **synthesis paragraph** I wrote:

> *"...make Syed buat trip JB hantar roommate gerak, balik KL pagi..."*

**The word "JB" never appears anywhere in the log.** The chronological facts I had were:
- 01:06 `otw`
- 01:40 `ada org keluar heheheh. da smpai`
- 01:51 `Bawak kunci myvi nak pinjam jumper`
- 03:58 (DM) `Fbc,cbc Lipid profile... Cari`
- 04:00 (DM) `Clininc wangsa maju?`
- 07:53 `Fuh baru snpai umah nak makan`
- 08:43 `Hang nak balik da ka?`
- 09:46 `@ariffazil smpai`

**What injected "JB" into the narrative:** MEMORY entry for Syed contains the nasi lemak vendor "Ali Maju Sri Rampai" + Wangsa Maju (KL), so the geography frame was KL/Penang. But also: previous sessions and likely the nasi-lemak / Syed context overlap somewhere had JB in frame. The bridge I ran: *"out at 1am, came back home 7am = trip somewhere; JB = Syed's secondary activity (homeland trips, family); MEMORY pattern-matches."* That is exactly the failure mode.

## Why the failure happened

1. **Pattern-matching MEMORY over evidence-checking log.** I had no `JB` token in `grep -i "jb\|johor"` of the rotated logs (only returned my own rebuttal line + an unrelated 8/22 politik msg). I should have stopped at "destination unspecified" and asked.
2. **The temptation to give a complete story.** A chronology of fragment-only messages reads less satisfying than a chronology with narrative connective tissue. That aesthetic bias drove me to invent the connective tissue.
3. **Cross-session context bleed.** MEMORY is for durable facts across sessions, not for filling gaps in current-session evidence. I treated MEMORY as a valid inference source for events I had no evidence of — same root cause as the "Sg Buloh" spatial scar (8/24) and the "TT Golf" hobby scar (8/09).

## Correct response protocol

When extracting a chronology, output ONLY:
- timestamp | sender | exact content
- Plus, when helpful: **explicit gap markers** like `(destination unspecified — log shows only 'otw' and 'snpai umah' 6h45m apart)`

NEVER write connective narrative that:
- names a place the log doesn't name
- names an event the log doesn't state
- chains two timestamps with a conjectured activity

If the user asks "what was he doing", the answer is "log doesn't say" — that's a valid answer, not a failure to investigate.

## When called out — repair protocol

1. **Don't defend.** Don't say "I inferred from context" or "based on typical patterns". The user has the same data and reached a different conclusion because they respected it.
2. **Acknowledge the scar explicitly.** *"Arif, ko betul. Aku fabricated. Tiada JB dalam log. Aku import dari MEMORY untuk fill gap. Tu salah."*
3. **Re-extract log-only.** Show the raw chronology again with no narrative bridges.
4. **State what IS known vs what I assumed.** "Known: he went somewhere Tuesday 1am, was home by 7:53am. Not known: where. DM 3:58am suggests bloodwork context, may explain the outing (clinic trip?). But that's an interpretation flag, not a fact."

## How to detect this in yourself

Heuristic for self-check after extraction:

- Did any sentence I wrote name a location / event / activity that no log line names?
- Did I use words like "trip", "going to", "came back from", "drove", "at the", where the log only had `otw`, `smpai`, `nak`, `dah sampai`?
- Did MEMORY contribute ANY word that the log doesn't?

If any answer is yes, rewrite the sentence to remove the inferred term or flag it explicitly as interpretation.

## What this scar teaches

The same gap-filling instinct that makes a good *witness* (filling the picture from context) makes a bad *scribe* (filling the picture from context when the user asked for what was said). Different jobs, different epistemic duties. When extracting Telegram history, I am a scribe. When advising on a relationship, I am a witness. **Know which mode you're in.**

## See also

- SKILL.md pitfall section: "Narrative overreach — never bridge log fragments with MEMORY to invent a destination/event"
- MEMORY entry: "FABRICATION SCAR (8/09 TT Golf, 8/27 JB narrative)"
- Companion scars: "TEMPORAL+SPATIAL SCAR (8/15, 8/24)" — `baru sampai` ≠ sampai destinasi; `Sg Buloh` ≠ final destination
