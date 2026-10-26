---
name: bond-corpus-probe
description: "Use when probing a bonded person's WhatsApp chat corpus."
version: 1.0.0
owner: F13
tags: [whatsapp, corpus, bond, forensics, probe, F5-private]
floors: [F2, F5, F9]
---

# Bond Corpus Probe — sovereign-directed deep read of a bonded human's messages

> F5-PRIVATE territory. Sources live under `/root/.hermes/lanes/private/shadow/sources/` and
> `/root/.hermes/cache/documents/`. Never web. Never into USER.md / MEMORY.md / shared rooms.

## Procedure

1. **Locate the export.** WhatsApp exports: `*WhatsApp Chat with*.txt` (plain UTF-8) under
   `shadow/sources/`; zips in `cache/documents/` are often empty shells — check the `.txt` first.
2. **Parse with the exact pattern — and check the pattern against `repr()` of the file's first 200 chars BEFORE debugging anything else.** Exports differ per sender device: date order is `M/D/YY` or `D/M/YYYY`, `am/pm` may be any case, and the separator before it is often U+202F NARROW NO-BREAK SPACE, which a literal space in the regex will never match.
   ```python
   pat = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2})\s+([apAP][mM])\s+-\s+([^:]+):\s?(.*)$', re.M)
   # date order: max(first field) > 12 -> D/M/Y; if ambiguous, decide from a date both readings
   # agree on, never from habit
   # hour fix: PM & h<12 -> +12; AM & h==12 -> 0
   ```
   **A zero parse means the pattern is wrong, not that the file is empty** — go read the raw bytes.
   Count messages, per-speaker, per-year, per-hour BEFORE quoting anything.
3. **Run the base-rate pass first.** Count the SAME keyword set for BOTH speakers (sayang/rindu/
   worship/sado/tumbuk/duit/tolong...). The principal's vocabulary dominates most maps — attributing
   the principal's words to the subject is the canonical failure (lexical attribution). A claim like
   "he searches for worshippers" dies if the token appears 19x for the principal and 1x (quoting
   the principal) for the subject.
4. **Then the structure pass.** Message openings (first 3-4 words, Counter), day-starters (who
   initiates each active day), gaps >=14 days with the re-join messages quoted verbatim, ask-pattern
   counts ("hang katne", "kul bape", "jom", "sponser"), and service vs received vectors.
5. **Quote verbatim, tag provenance.** OBSERVED (in-corpus, quotable) vs SOVEREIGN-TESTIMONY-ONLY
   (said by the principal in session, zero corpus support) vs INFERENCE (labelled, never asserted).
6. **Deliver: counts + verbatim lines + named gaps.** End at evidence. "Here is what the record
   shows; here is what it cannot show (voice, presence, motive)."

## Pitfalls

- **Continuation windows are the common case** — numbered exports like `(12).zip` are slices, not the corpus. Every volume/first-time/never claim must be scoped to the window parsed; running the same token count against the oldest export is mandatory before any "in N years" phrasing.
- **Asymmetry metrics are the extraction-verdict instrument, and they cut both ways** — volume share, day-starter counts, question ratio, and inititiation counts decide "is this person being drained" in ONE table. But asymmetry ≠ extraction by itself: check whether the resource flowed (money, stock, services) was explicitly offered/shared as the pair's NORM before calling it a breach. A norm of sharing stated openly by both parties turns "he used my stock" from betrayal into bookkeeping.
- **When the sovereign names a norm you missed, log it as a scar in-session and re-frame instantly** — arguing your original extraction hypothesis after the sovereign corrected the norm re-litigates the relationship and reads as you siding against the bonded person. The correction IS the finding.
- **Verbatim rejoin/gap quotes decide ambivalence questions** — when the question is "will he come / does he want this", quote the subject's own forward-looking lines (plans, "nanti order", parking-and-late messages) rather than inferring from volume. One forward commitment outweighs ten one-line replies.
- **Channel-split is signal, not noise** — the SAME person often talks completely differently in WhatsApp DM vs Telegram group vs their private agent lane (short vs long, warm vs task). Compare a person to their own cross-channel baseline before comparing them to the principal.

- **Do not re-map the principal's interior mid-probe.** When the sovereign spirals ("why", "what's
  the reality", repeated re-probes), the answer is MORE EVIDENCE, not psychology of the asker.
  State-attribution about the principal is held by the H3/HUMAN-9 floor gate — never improvised here.
- **Late-night + repetition = ache, not research demand.** After two solid passes, further cycles
  get: what the file shows, what it cannot show, and a stop. Do not manufacture new insight layers.
- **Timezone: log/export timestamps are local MYT** — verify against `date` once before
  hour-of-day claims.
- **Check speaker-set uniqueness after parsing** (expect exactly the two parties + system lines) —
  silently merged or truncated names corrupt every per-speaker count.
- **Media lines (`<Media omitted>`) are data too** — they mark photo/video exchanges; count them
   per speaker before dismissing.
- **Scope every superlative to the window you actually parsed.** "First time he has ever X" / "X
   never happens" is only valid against the oldest full export. A fresh multi-week zip is a
   CONTINUATION of the corpus, not the corpus — re-run the same token count against the oldest file
   before "in N years" leaves your mouth.
- **A screenshot that reaches past the export's last timestamp is a request for a fresh export, not
   for pixel work.** Export attribution is exact; sender attribution from pixels is a fallback that
   needs validation anchors (`chat-screenshot-forensics`).

## Cross-references

- Falsification ledger pattern + provenance tiers: `/root/.hermes/lanes/private/shadow/syed-falsification-ledger-*.md`
- Conduct during delivery: `syed-care-mode` (external, AAA-owned) and `human-bond-action` (READ/WEIGH spine)
- If the sovereign is in distress about the bond: witness register, do not advise uninvited
  (relationship-kernel H-laws).
