# Corpus forensics pitfalls

## Timezones — two clocks in one investigation

`~/.hermes/state.db` message timestamps are **true UTC epochs**. `gateway.log` lines are written in
**local MYT (+08)**. Mixing them mislabels every event by eight hours. Anchor the two against one line
present in both before trusting any timeline.

`datetime.utcfromtimestamp(epoch)` returns a naive **UTC** value; attaching `+08` to it *displays* UTC
while looking like local time. Use `datetime.fromtimestamp(epoch, tz)` for a true local rendering.

## Exported chat logs — date order is not universal

WhatsApp exports default to **`M/D/YY`**. A parser reading day-first **silently discards every line
whose first field exceeds 12** — thousands of messages — and manufactures phantom gaps of hundreds of
days. Symptoms: a "longest silence" longer than the corpus span supports, plus a suspiciously large
count of date-rejected lines.

**Always count and print the rejected lines before drawing any conclusion from a gap analysis.**

## Preserve recovered corpora immediately

A first-party export found in scratch storage (`/tmp`, agent caches, unzipped working dirs) may be
cleaned between sessions and take the strongest evidence with it. Move it to a durable directory the
moment it is identified: `chmod 700` the directory, `chmod 600` the files, record the provenance.

## Stale figures propagate

When a parser is corrected, **every metric from the broken pass must be re-derived and the old figures
marked superseded.** Numbers already quoted into reviews and external documents travel onward as fact.

## Media that is gone, and media that is not what it seems

- `<Media omitted>` in an export is unrecoverable content. **Metadata alone must never be used to
  infer image content.**
- Where a channel persists a machine-written description of inbound media, image content **is** partly
  recoverable after the file is gone — but only for that channel and window. Say which.
- Sender attribution for group-chat media often survives as a trailing sender marker in the persisted
  text; without it, attribution is inference, not observation.
- Check generation provenance on any file before treating it as a photograph. AI-generated stills sit
  in scratch directories looking exactly like evidence.

## Asking for the missing channel

Identify which gaps are **recoverable by the principal** (a device-level re-export including media,
which would close the visual layer) versus **human-only** (anything that exists only inside another
person's head). Do not propose collecting the second kind.
