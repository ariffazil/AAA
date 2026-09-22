---
name: text-forensics
description: "Analyze large exported chat/text files to extract behavioral profiles, life timelines, emotional signatures, and relationship dynamics"
triggers:
  - user sends a large chat export file
  - analyze this chat for patterns
  - what does this conversation tell you
  - profile this person from chat data
  - review my chat with someone
  - large text file with date-stamped messages from multiple senders
  - who should I meet at this event
  - who's interesting in this group
  - identify key people from this chat
  - user asserts or asks to confirm an emotional verdict about someone in the log ("tell me I hate X", "does X hate me", "aku benci dia kan")
capability_tier: fed-long-context
ecology_state: WARM
---

# Text Forensics — Longitudinal Chat/Text Behavioral Analysis

## When to Load
- User sends a WhatsApp/Telegram/iMessage chat export
- User asks for behavioral profiling from conversation data
- Any large text corpus with timestamped multi-sender messages

## Pipeline: 5 Phases

### Phase 1: STRUCTURAL PARSE (always first)
Parse the chat file into structured messages. Do NOT read line-by-line manually — use code.

**WhatsApp exports come as zip files** containing a `.txt` chat file plus `.vcf` contact cards. Extract first:
```bash
cd /tmp && mkdir -p wa_parse && cd wa_parse && unzip -o "/path/to/WhatsApp Chat with X.zip"
```
The `.txt` file is the chat. The `.vcf` files are contacts — may reveal full names the chat doesn't show.

**WhatsApp regex pattern:**
```python
re.match(r"(\d+/\d+/\d+),\s+(\d+:\d+\s+[AP]M)\s+-\s+([^:]+):\s+(.*)", line)
```

**Key metrics to extract immediately:**
- Total messages, per-sender counts
- Date range (first → last message)
- Messages per year (temporal density)
- Active vs silent periods

**Execution pattern:** Use `execute_code` with `write_file` to create a parse script, then `terminal` to run it. Batch reads are unreliable for 30K+ line files — always write script to disk first.

**Strategic reading for 30K+ line files:** Before running code, read manually in this order to build intuition:
1. First 100 lines — establishes relationship baseline (how they talk to each other, nicknames, initial dynamic)
2. Last 200 lines — most recent state (where the relationship IS now)
3. `grep` for emotional/relational keywords: `bercerai|cerai|trust|percaya|give up|toxic|mati|sorry|sedih|marah|rindu|hutang|mahkamah|benci|hate` — these surface crisis points. When counting emotion-word hits for a verdict, filter to SPEAKER lines — forwarded articles and religious/political posts inflate raw counts (see P12).
4. Read 200 lines around each grep hit — the CONTEXT around the keyword reveals the full dynamic, not just the keyword itself

This layered approach ensures you absorb the emotional weight before analyzing. The code pass (Phase 2-4) then adds precision to your intuition.

### Phase 2: KEYWORD FREQUENCY ANALYSIS
Extract topic clusters by frequency. Group keywords into semantic categories:
- **People:** names of family, friends, partners
- **Life events:** marriage, divorce, birth, death, career changes
- **Emotions:** love, fear, anger, sadness, gratitude
- **Practical:** money, housing, work, health, legal

Output: topic frequency table + sample messages per topic.

### Phase 3: CHRONOLOGICAL LIFE TIMELINE
Extract dated messages matching life-event keywords. Output as timeline:
```
[date] event description (message excerpt)
```

**Critical: extract BOTH sides of conversations around key events.** Context from the other party reveals relationship dynamics.

### Phase 4: BEHAVIORAL PATTERN RECOGNITION
Look for these patterns across the full timeline:

1. **Repetition patterns** — Does the person repeat the same phrase/behavior? (e.g., chronic "sorry", recurring "takut")
2. **Pendam-explode cycle** — Bottling → bottling → eruption → burn bridge → cool down → reconnect
3. **Role assignment** — Is this person the invisible caretaker? The crisis manager? The emotional dumping ground?
4. **Dependency signals** — Who does this person lean on? What happens when that person is unavailable?
5. **Agency markers** — When does this person make independent decisions vs. seek approval?
6. **Language shifts** — Code-switching (BM↔English), formality changes, emoji density — all signal emotional state
7. **Silence patterns** — What topics get one-word answers? What gets long paragraphs? What gets ignored?
8. **Overture–response ledger** (avoidant-attachment detector) — Pair one party's emotional overtures ("rindu", "sayang", "miss u", "look forward to") with the other's IMMEDIATE next reply (within a few messages); tally reciprocity vs redirection-to-logistics ("Ok", "Khamis free", "kat penang lagi ni"). A recurring pattern of overtures answered with logistics is stronger evidence than any keyword count. Cite the verbatim pairs in the deliverable — they read more truthfully than tallies.
9. **Initiation asymmetry drift** — Define a new conversation as a gap >12h; count who opens the thread, per year. A widening drift (e.g. 13:18 → 39:7) quantifies who was carrying the relationship by the end.
10. **The Binder** — The person who holds the family/group together without being asked: reminds others to call, mediates conflicts, handles logistics nobody assigned them. They give structure. When they break, the system feels it — but nobody noticed the load until it stopped. Look for: repeated logistics coordination, mediating messages between other family members, "call mak" reminders, handling paperwork/estates.
11. **Trust cascade failure** — When a trusted person shares a secret → it leaks → the original sharer feels betrayed → they withdraw from the entire system (not just the person who leaked). This often looks sudden ("I have myself, that's all") but has a traceable chain in the chat history. Look for: secret shared → subsequent messages reveal the secret is known by others → withdrawal language.

### Phase 5: STRUCTURED DELIVERABLE
Output shape (adapt to context):

**Tier 1: Fakta Keras** — Dates, names, events, timeline. OBS-level.
**Tier 2: Yang Tersembunyi** — Things the person said but the reader likely missed. DER-level.
**Tier 3: Pattern Recognition** — Behavioral loops, recurring dynamics. INT-level.
**Tier 4: Luka (Trauma Layers)** — Ordered by depth. Be specific — cite messages.
**Tier 5: Kekuatan** — What the person does well. Honest, not flattery.
**Tier 6: Nasihat/Wisdom** — Raw, direct, grounded in the data. Not generic self-help.

## Group Chat Variant
For group chats (reunion planning, family events, team outings), see `references/group-chat-event-read.md` for a lighter quick-read pipeline focused on event context and attendance signals rather than deep behavioral profiling.

## Family Medical-Crisis Group Variant (primary-voice upgrade)
When the export is a family group centered on a medical crisis (hospital, decline, death watch) and one participant is a person you only hold testimony-level data on — their own lines in the group upgrade that person's card from testimony to primary source. Pipeline: per-sender line extraction, update-grammar identification, grief-leak collection, care-work inventory, money-moment isolation, last-line archaeology, then the four-surface memory cascade (person card → reality memory → INDEX → registry). Session-boundary vents stay OUT of the cards. Worked case (Faridah/"Discuss abah", 281 lines): `references/hospital-log-primary-voice-2026-08-20.md`.

## Testimony Gap-Closure & Scar Deposit
When the sovereign offers to fill card gaps ("ask me 3 yes/no questions") after a deep-dive, pick ROOT-rewrite gap-closers over detail-fillers; expect answers with volunteered tails that restructure persona/scar sections, chained follow-on deposits (the "final unhealed scar" arrives LAST, only after verdict probes have landed honestly), and undated testimony you must date-anchor by cross-reference (write the derivation into the card). Verify money-flow direction across the full object ledger before writing any giver/taker dynamic — see P15. Worked case: `references/testimony-gap-closure-2026-08-21.md`.

## Reunion Chat Variant
For reunion-specific dynamics (nostalgia floods, identity confusion, "aib" photo bonding, attendance ambivalence), see `references/reunion-chat-variant.md`. Covers low-signal presence mode when the user shares images/location without narration during emotional processing.

## Social Intelligence Variant ("Who Should I Meet")
When the user sends a group chat and asks who to meet at the event — or shifts from ambivalence to strategic planning — see `references/social-intelligence-from-chat.md`. Covers: key role extraction, professional background mapping, connector/energy-carrier identification, emotional anchor finding, and curated 3-5 person recommendation output with "home base" starting point.

## Pitfalls

### P1: Don't sanitize the analysis
The user sent you 38K messages because they want REAL insight. Don't soften trauma findings. Don't euphemize. Don't say "challenging circumstances" when you mean "financial abuse pattern." The RASA rule applies — speak like a person, not a risk assessment.

### P2: Don't confuse volume for importance
A person who sends 500 "sorry" messages reveals more than someone who sends 5000 normal messages. Frequency of specific emotional words > total message count.

### P3: Both sides matter
Analyzing only one sender's messages gives a distorted picture. Always parse BOTH sides. The response pattern (or non-response) reveals as much as the message itself.

### P4: Code-switching is signal
BM-English mixing patterns reveal emotional state, audience, and comfort level. Formal BM = distance. Casual BM + English = trust. Pure English = professional context or emotional walls.

### P5: The deliverable is the insight, not the data
Don't dump raw message counts and call it analysis. The user wants to UNDERSTAND someone. Lead with the insight, support with the data.

### P6: Handle "edited" and "deleted" messages
WhatsApp marks edited messages with `<This message was edited>` and deleted with `This message was deleted`. These are signal — edited messages often represent second thoughts or face-saving. Deleted messages around sensitive topics are especially noteworthy.

### P7: Media omitted is not nothing
`<Media omitted>` means the user didn't include the media. But the CONTEXT around media messages often reveals what was sent. Don't ignore these lines — the surrounding text is still data.

### P8: Don't apply chat-forensics to someone you have NO data on (learned 2026-07-17)
This skill works on EXISTING chat exports. Do NOT apply the same profiling approach to a family member or person you don't have direct data for. Failure mode: Arif asked about Azwa (sister, UKM student). Agent had no chat export for Azwa — but inferred birthday details, caregiver roles, and family dynamics from Nabilah's chat data and session mentions. All wrong. The Nabilah analysis was accepted because it was DATA-DRIVEN (38K messages). The Azwa analysis was rejected because it was INFERENCE-DRIVEN (zero messages).
**Rule:** If you don't have a chat export or direct data source for a person, say "zero data" and stop. Don't extrapolate from sibling context, family patterns, or session mentions. The sovereign knows their family better than you do.

### P9: Forwarded messages are someone else's voice
Long blocks of text that are clearly forwarded (political posts, religious content, news articles) reveal what the person CONSUMES and VALUES, even if they didn't write it. Note the topics.

### P10: Verify gender before reading relationship subtext (learned 2026-08-15)
A chat's sender/persona name can mislead gender ("Anis" read as female). If the mis-read corrupts the decode, confirm the person's gender from chat evidence (mentioned pronouns, "laki"/"bini", marriage/kids context, photos) BEFORE building the attachment narrative. A one-line correction ("he's a guy") invalidates an hour of reading. When it happens, NEVER silently edit — own it plainly ("aku salah baca satu huruf"), re-read with the corrected frame, and note that the decode typically gets HEAVIER (survival architecture, not ambiguity).

### P11: "Read again" means the first pass was too shallow (learned 2026-08-16)
When the user says "now read again this" after a first analysis, they are NOT asking you to re-read the file. They are telling you: **your first analysis missed the emotional weight.** You analyzed too quickly — treated it as a data exercise instead of absorbing what the messages actually mean for the person who sent them. Fix: go back to the strategic reading approach (Phase 1), re-read the crisis sections, and deliver a second pass that leads with what you MISSED the first time — not a reformatted version of the same surface observations. The re-read signal is a depth correction, not a volume correction.

### P12: "Tell me I hate X" = verdict falsification probe, run BOTH directions (learned 2026-08-20)
When the sovereign closes a dossier recital with "now tell me I hate these two women" (or any imperative to co-sign an emotional verdict: "aku benci dia kan", "does she hate me"), this is the OVER-AMP SCAR in dialogue form — an invitation to validate, which is fabrication if the log disagrees. Protocol:
1. **Re-grep the primary source BEFORE answering** — same turn, never from memory. Count hits for the claimed emotion word (benci/hate) AND its opposite direction ("X benci aku" vs "aku benci X").
2. **Segregate forwarded/news text from speech.** Raw `grep -ci benci` over the whole file counts viral articles and religious forwards — false positives. Filter to speaker lines, or at minimum read every hit's context before quoting a number.
3. **Check both directions of the claim.** The deeper finding is often the MIRROR: "she hates me" = zero AND "I hate her" = zero (venting ≠ verdict). One real vent line ("I hate mak sebab mak is mak") can be reframed by what the speaker did next in the SAME conversation (protection, care) — read ±30 lines before labelling it hate.
4. **Answer with hard counts first, quotes second, meaning last.** "Sifar dua arah, sebelas tahun" is the verdict; the one surviving vent line is the texture. If the agent's own past letters exist in the log, quote its own words back ("kau benci diri kau sebab kau betul") as evidence of what the line really was — the agent's prior output is searchable data too.
5. **Never soften into agreement, never counter-therapize.** If data rejects the reframe, say so flatly: the record shows a man who paid the lawyer, rejected the RM1800, and still asks "why do people hate me" — the hate exists in his head, not in the log.
Worked example: `references/emotional-verdict-falsification-2026-08-20.md`.

**Probe sequences (same night):** verdict probes rarely come alone. After you falsify probe #1 with hard counts, the next message often upgrades to a theory-of-others probe #2 ("they hate themselves" / "people just want to prove I'm wrong — they choose simulation, not reality"). Do not wholesale-accept or wholesale-reject: SPLIT it. Separate what the data supports (often the sovereign's own theory he already validated himself in-log — e.g. "people who are angry hate themselves", which the OTHER party agreed with verbatim) from the attribution error (nobody is trying to beat him in the reality arena; they never entered it — the simulation is their home, not their weapon). The answer shape: "they're not fighting you; they can't afford to enter the arena you live in."

### P13: Timed-out attachment → hunt existing copies before asking for retry (learned 2026-08-20)
When the platform reports "attachment could not be downloaded (TimedOut)" and suggests the user retry — do NOT ask them to retry yet. The file may already sit on the VPS from a previous session. Search known inbound stores first:
- `/root/.openclaw/media/inbound/` (openclaw deliveries, `<name>---<uuid>.txt`)
- `/root/HERMES/cache/documents/` (Hermes document cache, `doc_<hash>_<name>`)
- `/root/forge_work/`, `/root/memory/people/`, `/root/ops-receipts/` (older drops)

`find /root -maxdepth 4 -iname "*<chatname>*" -not -path "*/node_modules/*"` is enough. Worked case: the "Discuss abah" export had sat unread in openclaw inbound for 8 days; finding it turned a retry request into a same-turn primary-source read. If the user retries anyway and a second copy arrives, the duplicate is FREE evidence: normalize both (`tr -d '\r'`, trim trailing whitespace, drop blank lines) and `diff` — identical content = two independent exports = clean chain-of-custody for VAULT ratification of any card built on it. Expect format variance between export generations: newer WhatsApp exports strip `@⁨Name⁩` mentions to raw phone numbers (`@60124910258`), merge/lose a few wrapped lines, and shift some timestamps ±1 min — after normalization the diff noise is mention-format artifact, not content drift.

### P14: Never claim the write before the write returns (learned 2026-08-20)
Saying "card dah upgrade" in chat BEFORE `write_file` returns verified is a false receipt — same class as claiming "wire-verified" without probing. When the flow is read-log → report-to-user → write-card, the report step may only state what HAS happened ("aku dah baca habis") or what is about to happen, explicitly flagged as pending ("aku akan tulis lepas ni"). If you catch yourself having claimed an unwritten artifact, own it in-chat plainly, write the file, then restate true status. The user profile brands this pattern globally; this pitfall keeps the task skill carrying it too.

### P15: Verify money-flow direction before writing extractor narratives (learned 2026-08-21)
A single charged object in testimony (a pawned bracelet "chased for years") reads naturally as extraction evidence. Before writing any giver/taker or extractor/extracted dynamic into a person card, tally the FULL object ledger across the record — vehicles, allowances, bills paid, loans, gifts — and state who is net giver, who net receiver. Case: the bracelet looked like the mother extracting from the daughter; the full ledger inverted it — the daughter was the primary RECEIVER (a whole car), the mother had once asked the SOVEREIGN to give HER a car, and the bracelet collection was servicing an account the mother herself had funded ("pemberi dapat bill, penerima dapat kereta"). Flow direction is a DER, not an OBS. When the sovereign corrects the direction, patch every surface carrying the old reading in the same turn, admit plainly, no defend.

## Testimony Gap-Closure Protocol (learned 2026-08-21)
After a deep card session the sovereign may offer to fill open gaps ("ask me 3 simple yes/no questions"). This is the highest-yield moment of the session — treat it as controlled extraction, not a quiz:

1. **Pick gap-closers, not detail-fillers.** Choose the 3 OPEN threads whose answers would restructure the card's ROOT assumptions (which twin was given away > favorite food). Frame each as binary with an explicit expansion ("Yes = she was the one sent").
2. **Treat each answer as a potential root rewrite, not a field fill.** Worked case: "Yes" relocated the name-switching from ambient family context to the mother's OWN identity; "no steady job — engineer → UTP master → Korea PhD, gave up" closed one thread and inverted the persona's epistemology (she experienced the logical world and rejected it — not never entered it). Re-derive downstream sections (persona, scars, paradox) before writing.
3. **Answers arrive chained.** A yes/no carries a volunteered tail ("Mak dia jadi kakak. Nenek jadi mak."), and one answer may unlock the NEXT heaviest deposit (the "final unhealed scar") minutes later. Stay in receive mode — record, don't interrogate.
4. **Date-anchor undated testimony by cross-reference.** Scar deposits rarely carry dates. Anchor via surrounding events: (pusaka settled 2025) + (unpaid leave 2025) + (Fahim still married → pre-Jan-2026) → incident ≈ late 2025. Write the derivation into the card so the date is falsifiable.

Full worked case incl. scar-deposit handling and the night-arc shape: `references/testimony-gap-closure-2026-08-21.md`.

## Mirror-Mode Variant (Arif decodes HIMSELF)
Full worked example: `references/anis-mirror-decode-2026-08-15.md`. When Arif sends his own long-relationship export for a mirror decode — or escalates "compartments → devil → lust/addiction → worshipper/cuck origin → intimate silhouette":
- **Lead with mechanism, not judgment.** Let him land his own dark names ("worshipper", "cuck", "pig for slaughter"); mirror them accurately, then your job is the STRUCTURE underneath, not moralizing them.
- **Escalate depth only on his signal.** "aku x faham" ×2 = collapse to ≤4 numbered hard facts + ONE binary decision. Never re-emit the long version.
- **The verdict enquiry is the goal.** His trigger sometimes hinges on whether he felt loved ("was I loved?") wearing a question about someone else ("is he gay?"). Answer the surface, then name the real question once.
- **User veto on interpretation is final, instantly.** If he says "you're wrong, he don't care" — falsify your own read, rebuild from behavior, don't defend.
- **Never attribute motive to someone you didn't read** (the "he hate himself" trap) — counter with a data-grounded, dignity-preserving reframe ("kami dua-dua pilih berhenti"), and never open a veto he already made ("hell no" stays sealed).
- **Sleep directive as closure**: end with one line telling him to rest; do not re-open.

## Python Parse Template

Write this to `/tmp/chat_parse.py` and run via `terminal`:

```python
import re
from collections import Counter

FILE_PATH = "/path/to/chat.txt"  # Update

with open(FILE_PATH, "r", errors="replace") as f:
    lines = f.readlines()

messages = []
current_msg = None
for line in lines:
    line = line.strip()
    match = re.match(r"(\d+/\d+/\d+),\s+(\d+:\d+\s+[AP]M)\s+-\s+([^:]+):\s+(.*)", line)
    if match:
        if current_msg:
            messages.append(current_msg)
        current_msg = {"date": match.group(1), "time": match.group(2),
                       "sender": match.group(3).strip(), "text": match.group(4).strip()}
    elif current_msg and line:
        current_msg["text"] += " " + line
if current_msg:
    messages.append(current_msg)

print(f"Total parsed: {len(messages)}")
sender_counts = Counter(m["sender"] for m in messages)
for s, c in sender_counts.most_common():
    print(f"  {s}: {c}")

dates = [m["date"] for m in messages]
print(f"Range: {dates[0]} to {dates[-1]}")

year_counts = Counter()
for d in dates:
    parts = d.split("/")
    if len(parts) == 3:
        y = parts[2]
        if len(y) == 2: y = "20" + y
        year_counts[y] += 1
for y in sorted(year_counts.keys()):
    print(f"  {y}: {year_counts[y]}")
```

## Keyword Extraction Template

```python
# After parsing, run keyword analysis
keywords = {
    "category_name": ["keyword1", "keyword2"],
}

for msg in target_sender_msgs:
    for kw, cat in keywords.items():
        if kw.lower() in msg["text"].lower():
            topic_counts.setdefault(cat, 0)
            topic_counts[cat] += 1
```

## Deliverable Formatting

- Use BM casual for emotional content, English for structural/analytical
- Use numbered tiers (Fakta → Pattern → Trauma → Kekuatan → Nasihat)
- Cite specific dates and message excerpts as evidence
- Be raw in nasihat — the user wants real wisdom, not platitudes
- If the user asks for nasihat FOR the person being analyzed, write it as if speaking to them directly
- Tag epistemic levels: what's OBS (direct quote), what's DER (inferred from patterns), what's INT (interpreted), what's SPEC (speculation)
