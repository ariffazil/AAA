# Corpus Integrity Gates

Topical depth for `first-party-corpus-audit`. Load before the first parse of any exported corpus.
These gates exist because a parser that mis-reads silently does not fail — it produces plausible
numbers, and every conclusion built on them inherits the defect.

## Gate 1 — Probe the date format, do not assume it

Messaging exports are usually `MM/DD/YY` (US) but are frequently read as day-first. Locale hints — the
language of the messages, who is speaking, an earlier successful parse of a different export — are all
unreliable.

**Probe:** take the first three dated lines and look at the slash fields.

- First field ever exceeds 12 ⇒ the export is `D/M/Y`.
- Second field ever exceeds 12 ⇒ the export is `M/D/Y`.
- Neither exceeds 12 in the sample ⇒ extend the probe to a wider slice until one does. Do not guess.

**Why this is the highest-cost defect in the class:** a regex that *validates* its captures (a real
`datetime` construction, a month range check) does not raise on a bad line — it skips it. A day-first
parser on a `M/D` export discards every line whose day-month pair is invalid, which on a multi-year
export is *thousands* of messages, asymmetrically spread. The surviving subset then produces phantom
long silences, distorted sender splits, and wrong per-period counts — all internally consistent, all
wrong.

## Gate 2 — Prove coverage before deriving anything

```
parsed_count  vs  raw_line_count      # print both, in the report
first ~6 non-matching lines           # print them; see what the pattern is eating
sender census vs raw text search      # a parser that loses senders is losing messages
```

Non-matching lines are usually legitimate (continuation lines, media placeholders, system notices).
The point is to *see* them, so an unexpected rejection class is visible immediately rather than after
the analysis.

## Gate 3 — Re-derive, never patch

When the format was wrong, every downstream number is suspect. Re-run the full analysis and publish a
corrected baseline table with the superseded figures **marked as superseded**. Patching the one number
you happened to notice leaves the others, and the reader, wrong.

## Gate 4 — Preserve the corpus before you analyse it

Working copies in transient storage get cleaned. The moment a corpus matters, copy it to a durable
private location — a `sources/` directory beside the report that cites it, `chmod 700` on the dir and
`600` on the files. If the corpus is lost, the audit stops being re-derivable and nobody can check it.

## Gate 5 — Two clocks in one machine

Log files are commonly local time; database epoch columns are commonly true UTC. Both look plausible
and sit eight hours apart in the wrong direction at the wrong moment.

**In Python:** `datetime.utcfromtimestamp(e).astimezone(tz)` returns **UTC**, while reading as though
it were local. Use `datetime.fromtimestamp(e, tz)`.

**Verify once** against a timestamp you already know — a message you just sent, or the matching log
line — before trusting any time-of-day conclusion. Day-versus-night reasoning, "who messaged first
that day", and phase-of-day patterns all invert silently here. Converting inside SQL with `'localtime'`
avoids the trap there, but the arithmetic must be redone correctly once you move to Python.
