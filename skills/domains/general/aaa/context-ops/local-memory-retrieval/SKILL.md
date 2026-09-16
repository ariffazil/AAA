---
name: local-memory-retrieval
description: "Use when asked what you know about X — check disk first."
---

# Local Memory Retrieval

Trigger: "cari apa hang ada pasal X", "what info u have about X", "find stored info on X", "what do you know about X" — for a person, project, machine, or past decision. Answer from disk, not from recital. Context memory is a summary of a summary; the stores below hold the original facts, the corrections, and the artifacts. Never answer this class of question from the injected memory block alone — sweep first, then speak.

**Rule 0:** disk > context memory > plausible reconstruction. If the sweep returns nothing real, the answer is "zero data" — never fill the gap with a texture-perfect guess.

## When to Load

- Any question where the expected answer is *retrieval*, not analysis.
- Before building any dossier/profile/brief — check whether one already exists (it often does) so you extend it instead of regenerating.
- Before telling the user "aku takde info" — the info is usually on disk somewhere unexpected.

## Sweep Procedure (in order — stop when the question is answered)

**1. Name sweep across roots.** One grep, case-insensitive, searching BOTH the formal name and the nickname/handle people actually use (a person filed as "Farhan" is reached via "Paan"; a project via its codename).
```bash
grep -ril -e '<name>' -e '<nickname>' /root/AAA /root/.hermes /root/arifOS 2>/dev/null | head -40
grep -ril --include='*.md' --include='*.json' -e '<name>' /root/AAA /root/.hermes 2>/dev/null | head -40
```

**2. Memory stores — highest signal per byte:**

| Store | What it is |
|---|---|
| `~/.hermes/memories/MEMORY.md` (and `USER.md`) | live memory — can LAG the consolidation queue |
| `~/.hermes/pending/memory/*.json` | background-review consolidations: each is an `old_text` → `content` diff with `created_at` — often NEWER than MEMORY.md and carrying the corrected fact |
| `~/.hermes/workspace/zen/mem0_dump.jsonl` | semantic dump, one JSON per line |
| `~/.hermes/channel_directory.json` | confirms group/DM IDs and display names |
| `/root/.hermes/state.db` | session DB, `messages` table (`session_id, role, timestamp, content`). Direct sqlite read beats grep for "what did we say about X lately" and for detecting a sibling session that already answered the same question |
| `/root/mem0_*.json` (audit / cleanup dumps) | distilled semantic memory as nested JSON — for a PERSON recall a name-walk here yields the highest fact density per byte of any store, already synthesised |
| `lanes/private/<name>.md` (find under `/root/.quarantine/*/_CANONICAL/*/lanes/`) | F5-private lane card — the only store carrying the sovereign's own standing vetoes on how that person may be described |

Print JSON with python (`python3 -c "import json;print(json.dumps(json.load(open(p)),ensure_ascii=False,indent=1)[:2500])"`), not `cat` — entries are long single-line blobs.

**3. Generated artifacts built for that entity** — dossiers, briefs, PDFs, HTML. This is where the real depth lives:
```bash
ls -la ~/.hermes/output/
find /root -maxdepth 5 -iname '*.pdf' -newermt '<recent date>' 2>/dev/null | head -30
pdftotext <file>.pdf - | sed -n '1,200p'    # read the body, never summarise from the cover page
```

**4. Cached tool output + session dumps (last resort).** Prior sessions' command output is cached verbatim and stays grep-able when live files move:
```bash
grep -oh '.\{250\}<name>.\{350\}' ~/.hermes/cache/exec/* ~/.hermes/cache/terminal-output/* 2>/dev/null | head
grep -l '<name>' ~/.hermes/sessions/*.json   # proves a mention exists; too noisy to be the fact itself
```
`~/.hermes/pastes/` holds large user-pasted blobs under the same idea.

Prior sessions also leave **working copies in `/tmp`** — extracted archives, trimmed exports, scratch chat dirs. They are ephemeral per boot, but they outlive the document cache: when the original export has already been evicted, a fragment sitting in `/tmp` is often the only verbatim source left, and quoting it beats quoting a summary of it.
```bash
find /tmp -maxdepth 3 -iname '*<name>*' 2>/dev/null | head -20
wc -l /tmp/<name>_chat/*.txt   # state the real size and date when you quote it
```

## Verbatim Self-Recall ("hang jawab apa dulu?")

Trigger: the user asks what the AGENT itself said previously — usually to test continuity, or to hold it to a claim it now needs to revise. The deliverable is the old answer quoted exactly, plus a verdict on whether its reasoning still holds.

1. `session_search(query=...)` in discovery mode hydrates the ANCHOR **user** message — that is the question, not the answer. Do not treat the snippet as the reply.
2. Pull the reply in one call: `session_search(session_id=<id>, around_message_id=<match_message_id>, window=5)`.
3. For the exact turn anywhere in a long session, read the live store. `/root/.hermes/state.db` holds `sessions` + `messages`; `/root/.hermes/sessions/sessions.db` is an empty shell on KVM8, so a query there returns 0 tables and looks like "no history".
```python
import sqlite3
con = sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True)
for r in con.execute("""SELECT id, session_id, role, datetime(timestamp,'unixepoch','localtime'), content
                       FROM messages WHERE content LIKE ? ORDER BY id""", ('%<keyword>%',)):
    print(r)
```
Scan keyword→id, then read the adjacent assistant turns in the same `session_id` and id range.
4. Report: quote the old answer VERBATIM (BM as typed, not tidied) → say plainly whether the reasoning still holds → if it was wrong, name WHY it was wrong and give the corrected reading. Never silently re-answer as though the earlier claim never existed, and never paraphrase it from the snippet.

**Pitfall — reconstructed reply:** rebuilding the old answer from the discovery snippet's surrounding text produces something plausible and false, because the snippet carries the user's words. Read the row before quoting it.

**Pitfall — flattening a reversal:** when the old claim was cost-avoidance dressed as a finding (a category verdict chosen because reading the alternative was more expensive), say that in one line. A reversed answer with no stated mechanism teaches the user that the agent's reasoning is arbitrary.

## Self-Recall — "What Did I Say Before?"

Trigger: the user points at a past exchange ("dulu aku pernah tanya hang X", "hang jawab apa masa tu?"). Answer from the transcript, not from memory of the transcript — recalled answers drift toward what is convenient now.

```bash
# 1. Locate the turn. Timestamps are epoch UTC — +8h for Asia/Kuala_Lumpur.
sqlite3 /root/.hermes/state.db "SELECT datetime(timestamp,'unixepoch','+8 hours') t, role, substr(replace(content,char(10),' '),1,200)
FROM messages
WHERE role='user' AND content LIKE '%<keyword>%' AND content NOT LIKE '%CONTEXT COMPACTION%'
ORDER BY timestamp;"
# 2. Read the exchange around it: take session_id + id from step 1, then
sqlite3 /root/.hermes/state.db "SELECT id, role, datetime(timestamp,'unixepoch','+8 hours'), substr(replace(content,char(10),' '),1,1400)
FROM messages
WHERE session_id='<sid>' AND id > <id> AND role IN ('user','assistant') AND content IS NOT NULL
ORDER BY id LIMIT 24;"
```

Pitfalls:
- **Message content lives in `/root/.hermes/state.db` (`messages`, `sessions`).** `sessions/sessions.db` exists but returned no queryable messages table — querying it yields nothing and looks like "no history".
- **Filter compaction rows** (`content NOT LIKE '%CONTEXT COMPACTION%'`): they restate whole conversations and swamp keyword hits with stale duplicates.
- **Filter blank assistant rows** (`content IS NOT NULL`): tool loops leave empty or repeated assistant entries that hide the real reply.
- **Read the full reply before restating it.** The hit shows the ask; the answer may have carried a caveat the user is now testing you on (e.g. an explicit admission that you could not substantiate the answer from the inside).
- **Report the retrieved turn verbatim.** Paraphrasing your own past answer away from the text is how a recall turns into a fabrication.

## Person-Recall Brief (pre-encounter)

Trigger: "I'm meeting X tonight — tell me everything you know about our memories." The deliverable is a short briefing the user can carry into the room: not a data dump, not therapy, not a fresh psychological analysis.

Order (stop when the encounter is covered):

1. **Private lane card first** — the only store holding his standing vetoes on that person, so nothing downstream re-opens a reading he already closed.
2. **Distilled semantic stores** (`/root/mem0_*.json`) — identity, timeline, working life, and his own reads, already synthesised.
3. **Live session DB** (`state.db`) — the last few days, and whether a sibling session already answered this exact question.
4. **Skill reference files** with a worked decode (`text-forensics/references/`, `shadow-mapping/references/`) — the hard numbers (initiation drift, silence gaps, keyword counts) usually live here, not in memory.
5. **Artifacts** (dossiers, exports) — state their real date and size when you quote them.

Report shape: the numbers for the whole span → the arc (peak → silence → reconnect → today) → verbatim pairs over summaries → his own reads quoted back as HIS, never as yours → close with what you do NOT have. A brief with no void section reads as more complete than the data supports.

Command-level detail for each store: `references/store-command-catalogue.md`.

## Precedence & Staleness

- **Pending-memory consolidations outrank live MEMORY.md for facts that change.** When two stores disagree, report BOTH with their `created_at` / file mtime and name which is newer. Never silently pick a side and present it as fact.
- When the disagreement is about a person's or system's *current* state and neither store is authoritative, say so explicitly ("dua-dua version ada dalam nota aku") and let the user settle it. Stated uncertainty beats a clean wrong answer.
- A fact sourced only from a session dump or a cached grep of an older probe is a lead, not evidence — verify before asserting.

## Artifact Facts Come From the Artifact

Before quoting a generated document's date, size, or contents: `stat -c '%n %s bytes %y' <file>` and read it with `pdftotext`/`read_file`. A memory entry saying "dossier compiled on D" while the file mtime says otherwise means one is wrong — the file wins, and flag the mismatch instead of smoothing it over.

When the artifact answers the question, DELIVER it (`MEDIA:/absolute/path`) and summarise its sections — do not describe a document you could hand over.

## Reporting Shape

- Lead with what exists, grouped by the entity's life (identity → relationship/context → artifacts). Cite the source implicitly ("nota lama aku", "dossier yang aku forge") without dumping filenames at the user.
- State active uncertainty in one line, in the user's own register — not as a disclaimer block.
- Offer one concrete next action (refresh, build a tracker, re-verify a live claim). No menus.
- Match the user's language and length: casual BM for Arif, short and direct, no headers unless the content is genuinely tabular.

## Support Files

- `references/store-command-catalogue.md` — copy-pasteable sweep commands per store (memory stores, artifacts, caches, session DB, person-recall sweeps) plus the roots worth grepping.

## Pitfalls

- **Answered too fast:** replying from the injected memory block without a disk sweep misses corrections, artifacts, and newer consolidations. The injected block is a digest, not the record.
- **Nickname miss:** grepping only the formal name returns nothing while the entity lives in the stores under its handle. Always search both.
- **Truncated grep context:** `grep -io '.\{200\}X.\{300\}'` windows cut mid-sentence — read the file when surrounding meaning matters.
- **Lane card skipped:** a lane card can carry a standing veto (the sovereign's own falsification of a reading, and the pronoun he wants used for that person). Briefing past it re-opens a question he already settled and makes the agent look like it kept score. Read the card before the sweep; reprint his reads as his.
- **Sibling session already answered:** in a multi-session runtime the same question can land in two live sessions minutes apart, producing two identical sweeps and two deliveries. Before a long sweep, query `state.db` for that user message in the last ~30 minutes; if a sibling already answered, verify its facts rather than re-deriving them.
- **Discovery crowded out by the live session:** when the query is built from words the user JUST typed, FTS discovery returns the current session as the top hit and the older session holding the answer may be absent from the result set entirely — a discovery call that mirrors the live message is not evidence of absence. Query `state.db` `messages` directly with a distinctive keyword from the earlier discussion (`SELECT id, session_id, role, content FROM messages WHERE content LIKE '%<keyword>%' ORDER BY id`), then take the `session_id` and read that session whole. `session_id` is date-prefixed (`YYYYMMDD_HHMMSS_hash`), so the id itself names the day — no need to hydrate a session to date it.
- **Self-recall answered from memory:** when the question is what the agent said, the agent's memory of the session is the least reliable source in the room — the row is on disk. Query, quote, then judge whether the old reasoning still holds.
- **"The full log is gone" is an answer, not a gap to fill:** long exports expire from the document cache, leaving a fragment plus distilled entries. Say exactly that. Never imply a decade of source was read, and never reconstruct detail from summaries to make the brief look complete.
- **Scope:** person-profile depth (source audit, entropy mapping, honest-deliverable format, anti-fabrication rules) lives in the `human-intelligence-gathering` skill — load it for anything beyond retrieval. This skill covers only where stored facts live and how to report them.
