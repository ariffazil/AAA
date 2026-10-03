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
2. **Parse with the exact pattern.** Export format is `M/D/YY, H:MM AM/PM - Name: text`.
   ```python
   pat = re.compile(r'^(\d+/\d+/\d+),\s+(\d+):(\d+)\s+(AM|PM)\s+-\s+([^:]+):\s*(.*)$')
   # hour fix: PM & h<12 → +12; AM & h==12 → 0
   ```
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

## Cross-references

- Falsification ledger pattern + provenance tiers: `/root/.hermes/lanes/private/shadow/syed-falsification-ledger-*.md`
- Conduct during delivery: `syed-care-mode` (external, AAA-owned) and `human-bond-action` (READ/WEIGH spine)
- If the sovereign is in distress about the bond: witness register, do not advise uninvited
  (relationship-kernel H-laws).
