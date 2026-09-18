---
name: sealed-deliverable-provenance
description: "Use when a deliverable needs a verifiable integrity seal."
version: 1.0.0
triggers:
  - "hash seal this"
  - "seal the PDF"
  - "give me a hash"
  - "auditable edition"
  - "prove this was not edited"
  - "daily briefing with a seal"
---

# Sealed Deliverable Provenance

Class-level skill. Trigger: an artifact is produced for someone who needs to trust it — a briefing,
report, edition, certificate — and the ask is to *seal* it, not merely to send it.

For the mechanics of building the document itself (markdown → HTML → weasyprint, page-count and
ink-coverage QA, MEDIA: delivery), use `forge-pdf-delivery`. This skill is only about the seal.

## The one rule, and the constraint that forces the design

**A hash proves integrity, never accuracy.** A perfect digest over a wrong document is a perfectly
intact wrong document. Say this inside the document, because a reader who sees a hash will assume
it validates the content.

**A file cannot contain its own hash.** Any digest printed inside the artifact is computed over a
different byte string than the one holding it. A document that prints its own SHA-256 is either
self-referential nonsense or a hash of something other than the delivered file. So split the seal
in two — and state in the document which is which.

| Hash | Computed over | Lives | Proves |
|---|---|---|---|
| **content_sha256** | the canonical *source* text, computed BEFORE any placeholder is filled | injected into the rendered document | the words were not edited after sealing |
| **artifact_sha256** | the rendered file's bytes, computed AFTER render | a sidecar file beside the artifact | the delivered file is the file that was built |

Order matters: hash the source first, inject it, render, then hash the render. Never hash a source
that already contains its own hash.

## Procedure

1. **Hash the source, then inject.** `content_sha256 = sha256(template_with_placeholders_still_literal)`.
   Substitute that value into the document's provenance block.
2. **Render.** Produce the artifact with the content hash already baked in.
3. **Hash the render.** `artifact_sha256 = sha256(output_bytes)`.
4. **Write the sidecar.** `<edition>.sha256` in `sha256sum` format: `<hash>  <filename>`.
5. **Ledger the edition.** Append one JSONL row:
   `{edition, date, built_at, content_sha256, artifact_sha256, chain_prev, seal_authority}`.
   `chain_prev` carries the *previous* edition's artifact hash, so editions form a chain, not a pile.
6. **Verify, then deliver.** Run the block below and show the reader the `OK` line.

## Rules

- **State which hash is inside and which is outside.** Print the content hash; where the artifact
  hash would go, say plainly that it is delivered alongside because a file cannot embed its own
  hash. Never print a placeholder that reads like a real digest — a reader will treat it as one.
- **Name the seal's authority.** If it is a lane-level or procedural seal and not the top
  constitutional authority, the document must say so. An unlabelled seal reads as the strongest one.
- **A corrected edition must not descend from the superseded one.** If an error is caught before
  sealing, rebuild from the corrected source and keep the bad build out of the ledger entirely — do
  not commit it as an ancestor. Record the correction in the commit message instead. The ledger's
  job is to make a *silent* correction impossible, not to make a corrected build permanent.
- **Never let an internal filesystem path reach the artifact.** Print engines stamp `file:///`
  source paths and render dates; strip them. A deliverable carrying `/root/...` leaks your layout.
- **Do the hashing inside the build script**, not by hand: compute → substitute → render → hash →
  sidecar → ledger row → run `sha256sum -c` and fail the build if it does not print `OK`. A seal
  that depends on remembering to run a command will be skipped on exactly the rushed edition that
  needs it most.

## Verification block — run before delivering

```bash
file out.pdf                                      # PDF document, version 1.7
pdfinfo out.pdf | grep -E '^Pages|^Page size'     # page count matches the design
pdftotext out.pdf - | grep -c "$CONTENT_HASH"     # >= 1  content hash IS embedded
pdftotext out.pdf - | grep -c "$ARTIFACT_HASH"    # == 0  cannot self-embed
pdftotext out.pdf - | grep -c 'file:///\|/root/'  # == 0  no internal path leaked
sha256sum -c <edition>.sha256                     # OK
```

The `== 0` on the artifact hash is the one worth keeping: it asserts the *design constraint*, not
just the bytes. A build that starts printing the artifact hash inside the file has broken the seal
contract, however green everything else looks.

## Pitfalls

- **A hash in a footer proves nothing if it was computed after the string was inserted.** Get the
  order wrong and the digest describes a document that never existed. This is the whole reason the
  content hash is taken from the *template*, before substitution.
- **Do not describe an integrity seal as verification of the content.** The moment the document
  implies "this has been checked and is true", the seal is doing work it cannot do, and the first
  corrected figure destroys the reader's trust in every other number.
- **Do not carry a superseded edition's hash in `chain_prev`.** A chain that links a withdrawn
  build legitimises it. Break the chain and start the corrected edition clean.
- **A sidecar is only a seal if it ships with the artifact.** Name it after the edition and place it
  beside the file; a hash mentioned in a chat message is not a deliverable seal.
