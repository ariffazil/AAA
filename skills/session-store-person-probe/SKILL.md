---
name: session-store-person-probe
id: session-store-person-probe
version: 1.0.0
description: "Use when probing a person's messages to the agent."
risk_tier: medium
floor_scope: [F2, F4, F9]
autonomy_tier: T1
triggers:
  - "did X message you / what did X say to you privately"
  - "anything urgent or emergency X told you"
  - "is everything X wrote in the group"
  - "he never DMs me / no DM between him and me"
  - "the agent asserted a person never contacted it"
  - "read a specific person's Telegram history"
  - "session db / state.db person probe"
---

# session-store-person-probe — what a person actually wrote

The class: questions about **one person's** messages to or around the agent — "did he message
you?", "what did he say last night?", "anything urgent he told you?", "is everything he wrote in
the group?". These are answered from the Hermes session store, not from gateway logs alone, and
they carry a failure mode no chronology work has: **the negative answer is easy to produce and
usually wrong.**

## The two questions, and why one store is not enough

1. **What did this person say privately?** Group history lives in gateway logs. A DM lane is a
   separate session (`chat_type='dm'`, `chat_id` = the person's Telegram user_id). A chat_id-scoped
   group grep does not merely miss the DM lane — it returns a clean, confident zero.
2. **Did this person contact the agent at all?** This is an absence claim. Absence in one search
   surface is not absence, and the person is not what produced the zero; the filter was.

There is one store per profile. `shared-state.db` holds only hosted-room tables — no `messages`.
`messages` carries `session_id`, not `chat_id` — join through `sessions`. Never answer from the
main profile's DB alone.

## Procedure

1. **Resolve the person to a Telegram user_id** from the lane register
   (`channel_directory.json`, lanes/people register), never from the asker's description of who
   someone "really" is. Two ids are easy to swap on this federation: `1042200555` is Syed,
   `267378578` is Arif. Keying the probe on the wrong id manufactures a false negative.
2. **Probe every store** with the recipe below (read-only). It reports the DM lane(s), the group
   sessions in the window, and the person's own recent messages.
3. **Read the transcript yourself** before summarising. The probe is an index; the wording is the
   evidence.
4. **Separate lanes in the answer.** What the person said in a shared room and what they said
   privately are different findings with different scopes. Never merge them into one narrative.
5. **State the denominator.** "No DM lane across 5 stores" is reportable. "No DM" is not.

### Probe recipe

```python
import glob, os, sqlite3, datetime as dt

DB_GLOBS = ("/root/.hermes/state.db", "/root/.hermes/profiles/*/state.db")
UID = "<person's telegram user_id>"          # not the asker's
GROUP = "<group chat_id>"                    # e.g. -1003815535761 SADO
SINCE = dt.datetime(2026, 9, 28).timestamp()  # window start
PLUMBING = "Gateway message origin"

def myt(v):
    return dt.datetime.fromtimestamp(float(v)).strftime("%Y-%m-%d %H:%M")

stores = sorted(p for g in DB_GLOBS for p in glob.glob(g) if os.path.exists(p))
for db in stores:
    print("=", db)
    cur = sqlite3.connect(f"file:{db}?mode=ro", uri=True).cursor()   # read-only, always
    # 1. the DM lane — the leg a group scan cannot see
    cur.execute("SELECT id, last_activity_at, message_count FROM sessions"
                " WHERE chat_type='dm' AND chat_id=? ORDER BY started_at", (UID,))
    dms = cur.fetchall()
    for sid, last, n in dms:
        print("  DM", sid, myt(last), n)
    # 2. group session(s) in the window
    cur.execute("SELECT id, last_activity_at, message_count FROM sessions"
                " WHERE chat_id=? AND last_activity_at>=?"
                " ORDER BY last_activity_at DESC LIMIT 6", (GROUP, SINCE))
    groups = cur.fetchall()
    for sid, last, n in groups:
        print("  GROUP", sid, myt(last), n)
    # 3. that person's own rows (group rows are tagged inline as [Name|uid])
    for sid, label in [(r[0], "PRIVATE") for r in dms] + [(r[0], "GROUP") for r in groups]:
        cur.execute("SELECT role, content, timestamp FROM messages"
                    " WHERE session_id=? AND role='user' AND content IS NOT NULL"
                    " AND timestamp>=? ORDER BY timestamp", (sid, SINCE))
        for _role, content, t in cur.fetchall():
            text = " ".join(str(content).split())
            if not text or text.startswith(PLUMBING):
                continue                       # injected routing metadata, not human speech
            if label == "GROUP" and f"|{UID}]" not in text:
                continue                       # someone else spoke in the room
            print(f"  [{myt(t)}] {label}: {text[:300]}")
print("searched", len(stores), "store(s)")     # the denominator for any negative
```

SQL form of the same read: `SELECT role, datetime(timestamp,'unixepoch','+8 hours') AS t,
substr(content,1,400) FROM messages WHERE session_id=? AND role IN ('user','assistant')
AND content IS NOT NULL ORDER BY timestamp;`

## Absence-claim gate — always on

Before writing any of: *he never messaged me · no DM between him and me · everything he wrote is in
one place · he said nothing that night · no entries*:

- **Enumerate every lane × every store.** DM and each group, every profile DB. A per-sender
  `session_key LIKE '%<uid>%'` filter finds DM lanes and old group lanes but silently misses
  today's group messages, which live in one session per chat with no per-sender suffix.
- **Re-read the query before trusting its empty result.** Ask: *could this filter have matched the
  data at all?* A query against a column that does not exist, or a sender-tag format that changed,
  returns a perfect zero.
- **When a prior turn already asserted the absence and it was wrong, the correction comes first** —
  before the new content, in one plain sentence, with how the error happened. Trust in a later
  correct answer is built by owning the earlier wrong one.
- An empty result is still a valid finding. Report it with its denominator rather than filling the
  gap with a plausible story.

## Reporting shape

- **Safety-shaped asks** ("anything emergency he mentioned?", "aku risau") get the verdict in the
  first line — acute red flags present or not — then the correction, then the private-lane items
  with exact times and the person's own wording, then what is UNVERIFIED, then **one** action.
  Never open with the chronology, never close with a menu.
- **Never diagnose.** Report what the person said and what the documents show, and do not soften a
  real finding either — the ask was for signals, not reassurance.
- **Third parties stay out of the profile.** If the lane mentions a partner or relative, keep it to
  what the person himself wrote about them.
- **Provenance in one clause, not a footnote.** "Rosser 2013, ~60%" — not a bibliography.

## Pitfalls

- **`messages` has no `chat_id`.** Querying it by chat_id returns nothing and proves nothing; join
  through `sessions` (`chat_id`, `user_id`, `chat_type`, `session_key`, `last_activity_at`).
- **`display_identity` is a compact binary BLOB — do not `json.loads` it.** In group sessions the
  sender identity is inline in the user content as `[Display Name] [Display Name|<user_id>]`; parse
  that tag. It is also what resolves against `channel_directory.json`.
- **Skip the plumbing rows.** Any user row whose content starts with `Gateway message origin` is
  injected routing metadata. Skip `role='tool'` entirely.
- **Group history is ONE session per chat.** Older per-sender sessions are frequently near-empty —
  a hit there does not mean you found the traffic.
- **Long histories get compacted.** `compacted`, `active` and `_compressed_summary` mean the full
  turn may be a summary. Say so rather than quoting it as verbatim.
- **Assistant turns are often several near-empty rows** around the real text; take the last
  non-empty row, and never conclude "the agent never replied" from an empty row.
- **Open every store read-only** (`sqlite3.connect(f"file:{db}?mode=ro", uri=True)`) — this is a
  live store serving an in-flight session.
- **Convert timestamps, do not eyeball them.** Values are unix epoch; render MYT with
  `datetime(timestamp,'unixepoch','+8 hours')` (SQL) or `fromtimestamp` (Python).
