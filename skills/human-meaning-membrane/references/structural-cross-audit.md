# Structural Cross-Audit — pattern for relational subjects

> Companion to `human-meaning-membrane` insight D ("tell me everything about X").
> Use when the user has explicitly chosen `audit structural` mode for a bonded
> person's data (chat export, voice notes, identity card, image stream).

## What this IS

A bounded parse of a relational data corpus. Five counts, three boundaries,
no motive inference. Reportable as observation. Dispute-able by either party.

## What this is NOT

- Not a window into the third party's interior
- Not a model of why X does what X does
- Not a stepping stone to "and therefore X feels Y"
- Not a substitute for asking X directly

## The five counts

1. **Sender ratio** — message count by sender over the window. Asymmetry is signal,
   not verdict. e.g. Arif:Syed = 755:453 means Arif over-replies 1.67×. Report
   as number, not as "Arif is clingier".

2. **Initiator ratio** — first message of each day, by sender. e.g. Arif:30 days,
   Syed:2 days. Report as counts. **Do not infer** "Syed is passive because he
   doesn't care" — he may be reactive under dfm-treat, he may have an
   unanswered inner channel, he may simply not be a chat person. The count is
   fact. The motive is what the user owns.

3. **Hour-of-day distribution** — message density by 24h hour. Reads
   "morning person vs evening person", "timezone", "sleep cycle signal". Two
   peaks (10-12 morning, 17-18 evening) is the typical Malaysian profile.

4. **Affection-keyword count per sender** — words like `sayang`, `love`, `hug`,
   `cling`, `manja`, `🥰`, `🙏🙏🙏`, emoji-only reactions. Asymmetry here is
   reportable but the load is bigger. e.g. Arif:29 vs Syed:4 (7×) — high
   asymmetry, but only to surface if user asks. **Do not introduce this count
   uninvited**; the user's own admission is the load-bearing data, not the count.

## The three boundaries

1. **No quote-by-name in unprompted structure** — if the user asks for
   structural only, do not surface the literal text of affection messages.
   Counts only. If user asks "what does he actually say to me?", surface
   the short-message frequency table, not the surface.

2. **No media-content extraction by default** — `<Media omitted>` count is
   the structural signal. If user wants to see actual photos, separate
   consent pass.

## Why this is class-level reusable

- WhatsApp export, Telegram export, Instagram DM, signal mirror, voice note
  transcripts, Discord channel, Slack channel — same five counts.
- Bonded-person identity card, biometric pilot, attendence agent history —
  same counts on the relational dimension.
- Patient medical timeline, court case docket, employee review history —
  same counts but different boundary conditions (F6 MARUAH + F1 AMANAH apply).

## Sample parse script (WhatsApp-style .txt)

```python
# Pseudo — adapt the line pattern to your source format.
LINE_PAT = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2})\s*(am|pm)\s*-\s*([^:]+?):\s*(.*)$')
# count[0] = total messages
# count[1] = sender breakdown
# count[2] = first-of-day initiators
# count[3] = 24h density
# count[4] = affection keywords per sender
```

## Failure modes this pattern is designed for

- **Fabrication drift** — agent extends structural count to motive claim
- **Aesthetic projection** — agent frames a raw asymmetry ("Arif talks, Syed
  listens") as a character verdict, when it is a count the user may interpret
  many ways
- **Co-reader leak** — agent emits affection register from Arif's side,
  third party (if they read this) sees a one-sided view that they themselves
  might be in
- **Motive inflation** — agent says "Arif is clingier" instead of
  "Arif sends 1.67× as many messages"

## What is not in this skill

- Voice/lane writing toward the bonded person → `syed-care-mode`
- Voice clone / shadow mode tender register → `abang-sado-tenderness-arc`
- Witness / discovery mode for relational anxiety → `governed-uncertainty`
- Bond conduct + cron touch + field of forces → `human-bond-action`

## Provenance

Forged from a 2026-10-02 cross-audit of WhatsApp export
(`/root/.hermes/cache/documents/doc_33347cefa871_WhatsApp Chat with Syed
Kudin(1).zip`) where Arif explicitly chose `audit structural` after a
"tell me everything about Syed + why he come to me" question. The
structural mode was the right answer; the agent almost pivoted to
motive inference mid-session. The pivot was caught and stayed in the
structural reading.

**Lesson that earned this file:** the structural reading is reportable
and useful; motive inference is what the user owns. Do not cross that
line. If the user prompts "and therefore", stop and re-anchor.