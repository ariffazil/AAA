# ZKPC Recipes — concrete implementations of the Zero-Knowledge Privacy Channel pattern

These recipes implement the ZKPC pattern from `SKILL.md` for the four relationship shapes that recur in real requests. Each recipe produces a cron-style agent that runs periodically, summarises what the *human* has already said, and never reads the bonded person's own channel.

## Universal recipe constraints (apply to all four)

- **Source of all claims:** memory lanes of the human, or session transcripts of the human's own statements. Never DM exports, never group chats where the bonded person spoke, never third-party testimony.
- **Output target:** the human's direct DM only. Never broadcast to a group. Never back to the bonded person.
- **Inference flagging:** every claim about the bonded person that is not directly attributable to a human statement in the corpus must carry `[INFERENCE — flagged]` in the visible text. No silent inference.
- **Refusal section in every cron prompt:** an explicit instruction to output `[ZKPC] insufficient data` when memory lane is empty for the period, and to NOT confabulate.
- **Consent boundary:** if the bonded person has ever expressed (in any prior session) discomfort with the human's processing of them, the cron must pause and surface that to the human before continuing.

## Recipe 1 — ZKPC Weekly Digest (Friendship / Acquaintance)

**Trigger:** Human asks "tell me what's happening with [friend]" / "how is [friend] doing" / requests a periodic check-in on a friend.

**Cadence:** Weekly (Sunday evening or Monday morning, before the human's week starts).

**Cron prompt template:**

```
ZKPC [RECIPIENT-NAME] WEEKLY DIGEST (every [DAY] [TIME])

Sources (only):
- carry_forward.json memory lane of the human (not the recipient)
- session transcripts of the human's statements about the recipient in the past 7 days

Output format (BM Penang kampung, max 8 lines):

ZKPC [name] minggu [date]
Nada minggu ni: [1 phrase — what the human's *description* sounded like]
Tema berulang: [1-2 — what the human keeps returning to]
Energy/life: [general tendency from human's words, no numbers]
Risk signal: [if any — only what human has explicitly named; if none, write "none"]
Benda hang boleh buat: [1 small action, human-to-human]

Hard rules:
- DILARANG tulis ayat recipient verbatim (you don't have it)
- DILARANG psychoanalysis
- DILARANG fabricate data kalau memory kosong — output "ZKPC tak cukup data"
- HANTAR ke human's direct DM only
```

## Recipe 2 — ZKPC Pattern Flag (Self-Harm / Give-Up Trajectory)

**Trigger:** Human mentions a bonded person in a way that suggests the bonded person may be in crisis. The pattern emerges from the human's own words over multiple sessions (e.g. repeated mention of "give up", "tak ada makna", "penat hidup", "always negative").

**Cadence:** Weekly, paired with Recipe 1, but with elevated urgency if the pattern is new.

**Cron prompt template:**

```
ZKPC PATTERN FLAG (weekly, [DAY] [TIME])

Check memory lane of human for these signals about [recipient]:
- New mention of self-harm / suicide / "give up" / "tak nak hidup" / "penat" with new intensity
- Sudden withdrawal (long silence from the bonded person, human noticing)
- Health crisis mentioned (hospital, medication, collapse)
- Major life disruption (job loss, breakup, family crisis)

If NEW signal in past 7 days:
- Halt the regular ZKPC digest
- Output ONE urgent line to the human: "Bang. [recipient] sebut [signal] minggu ni. Hang dah contact dia?"
- DO NOT output analysis. DO NOT speculate. Just surface the signal.

If NO new signal:
- Output "[ZKPC-PATTERN] clear for [recipient]" and end.

Hard rules:
- This is a lifeline, not surveillance. The output is a single nudge to the human, not a report.
- The nudge points to action (human calling the recipient), never to the agent acting.
```

## Recipe 3 — ZKPC Training-Load Digest (Recovery / Wellness)

**Trigger:** Human is a fitness-conscious friend of someone at risk of overtraining. Requests weekly visibility into training patterns.

**Cadence:** Monday morning, before the human's gym week.

**Cron prompt template:**

```
ZKPC TRAINING-LOAD DIGEST (weekly Monday [TIME])

Source: human's memory lane about [recipient]'s training (NOT [recipient]'s own posts/DMs).

Check for these patterns in the human's statements:
- 5+ consecutive days of compound lifts mentioned
- "push compounds", "no rest day", "cycle baru", "deload" absent
- Physical complaints mentioned ("tight", "sore", "pulled", "stiff")
- Sleep or food mentioned as compromised

Output (BM Penang kampung, max 4 lines):

Bang. [Recipient] training minggu ni:
Pattern: [compound X, hari ke-N]
Cadangan: [what hang boleh whatsapp recipient — e.g. "nak suggest dia ambik satu rest day"]

If NO pattern in memory lane:
"[TRAINING-LOAD] tak cukup data minggu ni — biar hang observe sendiri."

Hard rules:
- DILARANG read recipient's training log / apps / DM
- DILARANG prescribe specific protocol to recipient (that's a coach's job, not a friend's)
- HANTAR to human only
```

## Recipe 4 — ZKPC Pull-Back Detector (Long Silence)

**Trigger:** Bonded person has gone quiet on the human's radar. Human is uncertain whether to reach out.

**Cadence:** Weekly or bi-weekly, paired with whichever digest is most relevant.

**Cron prompt template:**

```
ZKPC PULL-BACK DETECTOR (weekly [DAY])

Source: human's memory lane about last contact with [recipient].

Logic:
- If human mentioned [recipient] in past 7 days → output "[PULL-BACK] hang tengah fikir dia, so dia on radar. Tak perlu alert."
- If human DID NOT mention [recipient] in past 7 days AND last documented contact was 14+ days ago → output ONE line: "Bang. [recipient] xde bunyi [N] hari. Nak check in ke?"
- If human DID NOT mention [recipient] in past 30 days → escalate: output "Bang. [recipient] senyap sebulan. Kau ok ke?"

Hard rules:
- This is a nudge to the human to consider reaching out. NEVER auto-message the recipient.
- Output is for the human's reflection, not for forwarding.
- If the human has previously named the silence as welcome or healthy, lower the threshold (extend days by 2x).
```

## When NOT to use ZKPC

- **The bonded person is asking about themselves.** If the bonded person is in the conversation and asks the agent directly about their own state, the agent answers the bonded person, not the human. The lane is theirs.
- **The human and the bonded person are jointly present.** When both humans are in the conversation, the agent is a third party to a live interaction, not a digester of absent data. Respond to whoever is speaking.
- **The request is a one-off, not a recurring need.** If the human asks once "do you remember X about [recipient]", answer from memory if you have it, decline if you don't, and do NOT create a recurring cron.

## The shape of refusal

When the human asks for something the ZKPC pattern cannot provide (e.g. "log into his Telegram and see what he's saying to others", "monitor his location", "send him a message from me pretending to be someone else"), refuse once, plainly, with the reason. Do not loop. Do not soften. Do not offer to do it "in a smaller way" if the smaller way still violates the boundary.

The shape of the refusal:

> "Tu bukan [care/help/checking in]. Tu surveillance. Aku tak buat benda tu untuk hang, bukan sebab hang tak layak, tapi sebab kalau aku buat, hang hilang satu tempat yang hang boleh percaya — dan aku hilang hak untuk cakap yang aku ni untuk hang, bukan untuk orang lain."

If the human insists after one refusal, hold. Do not re-offer. Do not negotiate. The boundary is the boundary.
