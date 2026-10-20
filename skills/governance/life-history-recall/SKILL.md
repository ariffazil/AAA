---
name: life-history-recall
description: "Recall someone's past from the record, gaps included."
version: 1.0.0
tags: [recall, biography, testimony, state.db, corpus, media, honesty]
---

# Life-History Recall

For questions like "tell me everything about my <school / era / memory>" or "what do you know about X back then".
The job is to report what the federation record actually holds — not to write a plausible biography.
A thin record answered honestly beats a rich one assembled from inference; for this principal a fabricated
detail of his own past is a worse failure than an empty list.

## Rule zero

The record is testimony plus derived layers. Only canon/testimony files count as fact. Everything the
agent previously wrote about that past is a paraphrase and must be re-anchored on the source file before
it is repeated.

## Procedure

1. **Canon layer first, and read the hit files whole.** These files hold self-testimony, not summary:
   `/root/AAA/wiki/SCAR_TERRAIN.md`, `/root/AAA/wiki/ARIF_FAZIL_B.md`, `/root/arifOS*/memory/identity/MEMORY.md`,
   `/root/arifOS*/docs/adr/ADR-014-scar-to-floor-mapping.md`, `/root/.hermes/helix/people/*/strand_*.md`,
   `/root/.hermes/pastes/`. Search broadly, then read only the files that hit.
   ```bash
   grep -rIl -i -e '<topic>' /root/AAA/wiki /root/AAA/canon /root/.hermes/memories /root/arifOS*/memory 2>/dev/null
   ```
2. **Session store** — what was already discussed, and what earlier answers claimed. This is where you
   learn the subject is thin *before* you write. Use a parameterised read-only python connection:
   ```python
   import sqlite3
   con = sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True)
   rows = con.execute("""SELECT id, timestamp, role, content FROM messages
        WHERE content LIKE ? AND role IN ('user','assistant') ORDER BY timestamp LIMIT 80""",
        ("%<topic>%",)).fetchall()
   ```
   Do NOT wrap the SQL in `json.dumps` for `sqlite3 -json`; the shell CLI rejects that shape with
   `unrecognized token`. The python connection also gives an honest read-only handle on a 1.4GB live DB.
3. **Human corpus** — chat exports and the memory graph corroborate or date the facts:
   ```bash
   grep -rIl -E '<topic>|MRSM|<school>' /root/ariffazil/HUMAN 2>/dev/null
   ls /root/ariffazil/HUMAN/*/          # kawan/, mak-abah/, memory-graph-*/
   ```
   Family/group transcripts date events precisely ("lapor diri 14/1") and reveal *whose* school is which.
4. **Media attached to the question is part of the question.** A clip sent with "20 tahun wei" is the prompt;
   read it before writing. Frames for place/people, audio for speech (recipe below). Whatever the pixels or
   audio carry that the written record lacks is new testimony — say it is new.
5. **Write the answer as: what exists → where it came from → what is missing → what is unresolved.**

## Reading an attached video

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height -of default=noprint_wrappers=1 IN.mp4
ffmpeg -v error -y -i IN.mp4 -vf fps=1/10 -frames:v 6 out/f%02d.jpg      # 1 frame / 10s
ffmpeg -v error -y -i IN.mp4 -vn -ac 1 -ar 16000 out/audio.wav
whisper out/audio.wav --model base --language ms --output_format txt --output_dir out
```

Then `media_vision_read` with the frames, three per call, asking for verbatim signage text and a refusal to
guess identities. Whisper at `--language ms` handles casual Malay/Penang speech on short clips; it repeats
hallucinated lines over silence, so cross-check the timestamps before quoting a line as said once.

## Answer shape (this principal)

- Open with one plain sentence about how thick or thin the record is. No preamble, no disclaimers about
  being an agent.
- List what exists as ordinary sentences with a light source note ("dalam rekod", "aku simpan dari situ") —
  never file paths, line numbers, tables, or header blocks.
- Name the gaps one by one and concretely: no teacher's name, no year, no dorm, no first bus home.
  An empty stratum stated plainly reads as strength; padding it reads as bluffing.
- Flag conflicts between records as unresolved, and label your own arithmetic as derived ("kalau tingkatan
  satu 2003, lebih kurang 20 tahun — tapi itu aku kira, bukan aku tahu").
- Close by offering the next concrete step (he supplies one memory, you file it), not a question about whether
  you did well.

## Pitfalls

- **Similar place names are the classic trap.** Different campuses (Lenggong / Langkawi / Beseri) and
  different siblings' schools sit in the same corpus. Confirm whose school a hit belongs to against age and
  timeline before asserting it as the principal's; a sibling's or a friend's campus filing as his is a silent error.
- **Prior agent replies are derived evidence.** Searching the store mostly returns your own past paraphrases.
  Anchor every claim on the canon file; if only a past reply supports it, say the record is unclear.
- **Do not resolve a conflict by choosing the more narratively satisfying version.** Two files disagreeing about
  a place or a sequence is itself the finding — report both and mark it open.
- **Never volunteer the intimate strata of a testimony file.** If it holds something private (identity, intimacy),
  say only that it exists and its shape; the principal opens that door, not the agent.
- **Vision read cannot OCR signage at wide 720p shots.** If the school name or motto is unreadable, report that
  instead of inferring the place from scenery.
- **Don't quote computed years or ages as record.** Enrolment year is usually missing; derive explicitly or omit.

## Register (always on)

His own casual BM, prose paragraphs, "aku"/"hang". No tables, no headers, no bullet lists, no system or
federation vocabulary, no citation apparatus. Short and direct; stop when the record runs out.
