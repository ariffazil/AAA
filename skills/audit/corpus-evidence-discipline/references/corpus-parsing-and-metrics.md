# Corpus parsing, metric definitions and epistemic tags

Working recipe for `corpus-evidence-discipline`. Keep every extraction script in the working directory
so the numbers are reproducible a second time — a count nobody can re-run is not evidence.

---

## 1. WhatsApp export

Exports arrive as a zip. Two format traps break a naive regex:

- **U+202F NARROW NO-BREAK SPACE** between the time and AM/PM.
- The timestamp may or may not carry seconds, and both forms appear in the same file.

```python
raw = open(P, encoding="utf-8", errors="replace").read().replace("\u202f", " ")   # essential
HDR = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?::\d{2})?) ([AP]M) - ([^:]{1,40}): (.*)$")
```

- Continuation lines (wrapped messages) belong to the previous message — append, never drop.
- Normalise speaker labels through one helper (`side()`), then never match on raw names again.
- `datetime.strptime` must try both `%I:%M:%S %p` and `%I:%M %p`.
- Container check before declaring a void: `zipfile.ZipFile(p).namelist()`.
- Move the export out of `/tmp` into the working directory (`chmod 600`, dir `700`) before parsing.

## 2. Gateway / agent-log extraction

When the record is a live agent gateway rather than an export, two line shapes carry traffic:

- `inbound message: platform=… user=… chat=… msg='…' reply_to_id=… reply_to_text='…'` — note that it
  **truncates long bodies**; find the ceiling before quoting a message as complete.
- Group relays prepend a speaker tag `[name|uid]` *inside* the body. Older lines carry `user=unknown`
  with no tag. Parse the tag, report the unattributed count, and never silently attribute those lines.

Extract to JSONL `{ts, chat, uid, name, body}` sorted by ts. Message bodies legitimately contain quotes
and commas — a naive `split` corrupts them, so keep the raw line alongside the parsed fields.

## 3. Metric definitions (state these in the output)

| Metric | Definition to state |
|---|---|
| messages | parsed real messages; system notices excluded |
| active day | day with ≥1 / ≥2 / ≥5 messages — pick one, report the others |
| day-opener | first real message of the day, per side |
| initiation | day-opener count, and separately first-message-after-a-gap |
| per-side share | messages and characters, both |
| response latency | seconds to the other side's previous message; report median and % under 1 min |
| humour | marker count per side, as % of that side's messages |
| gaps | consecutive active days more than N apart, with the first speaker after each |
| return-after-silence | for gaps ≥14 days: who spoke first, and the verbatim first line |

Recompute all of these from source on every pass; never carry a previous session's figures forward.

## 4. Classifying hits (more important than counting them)

For any keyword sweep, classify each hit rather than reporting a total: **initiated by A · initiated by
B · neutral · quoted/forwarded · joke · self-criticism · logistics · admiration · solicitation ·
invitation · boundary**. A raw count mixes viral forwards, quotes and the person's own speech; filter to
speaker lines and read every hit's context before quoting a number.

## 5. Reading a channel's life-cycle

- first evidenced instance · densest window · last instance (date + verbatim)
- count by year and by side
- whether both sides' usage stopped together, or one side stopped first
- adjacent events within ±10 days of the stop, marked **sequence, not cause**

## 6. Epistemic tags

OBSERVED (present in the record) · SELF-REPORTED (a participant said it about their own state) ·
STRONG INFERENCE (state the causal bridge) · WEAK INFERENCE · UNKNOWN. Use UNKNOWN aggressively; do not
repair missing information with narrative.

## 7. Amendment discipline

The audit file is append-only. Corrections go in as dated amendments carrying: the defective claim, the
method that exposed it, the corrected statement, and the effect on earlier confidences. Never overwrite
the earlier text — a later session needs to see the drift in order to trust the file at all.
