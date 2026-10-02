---
name: capability-inventory-maturity
description: "Use when auditing a capability inventory. Grade maturity."
version: 1.0.0
tags: [inventory, audit, maturity, symlink, dossier, anti-fabrication, paths]
triggers:
  - "map all the skills / tools / agents"
  - "capability dossier"
  - "capability inventory"
  - "which skills exist"
  - "filesystem map"
  - "path census"
  - "organ map"
  - "what can actually run"
  - "LIVE vs executable"
  - "where does X live on disk"
---

# Capability Inventory Maturity

Producing a map of what exists (skills, tools, agents, organs, paths) is a class of task, and the
failure mode is always the same: **the map describes presence and calls it capability.** An entry
that has a file is not an entry that runs; an entry that runs is not an entry that has ever worked.
Grade the state, probe the path, and refuse any input you did not measure.

## The invariant

```
Name ≠ Path ≠ Present ≠ Loadable ≠ Executable ≠ Proven
```

Four states, ascending. The word in the document must carry the state:

| State | Means | Evidence |
|---|---|---|
| **PRESENT** | a descriptor exists (SKILL.md / manifest / handler / config) | the file resolves |
| **LOADABLE** | the loader resolves a populated body | body exists and is non-empty |
| **EXECUTABLE** | carries runnable assets | scripts/, templates/, a real binary |
| **PROVEN** | demonstrated end-to-end | produced a real artifact this run |

Never print `LIVE`, `working` or `active` from the existence of a descriptor. An inventory in which
every row reads LIVE because every row has a file is a document about the filesystem, not about
capability — and it hides the one number the reader needs. **Report the four counts explicitly**
(`n PROVEN · n EXECUTABLE · n LOADABLE · n PRESENT`) so discoverable-vs-working is visible at a
glance.

## Procedure

1. **Enumerate by path, not by name.** Build the list from the filesystem roots, then record for each
   entry: exposed path, `realpath`, `realpath != path` (symlink?), file count, byte count, descriptor
   line count, and mtime. **Walk with `os.walk(..., followlinks=True)`** — see the pitfall below.
2. **Grade each entry against the ladder** using the assets you found (scripts/templates → EXECUTABLE;
   descriptor only → LOADABLE). PROVEN is earned only by an artifact this run, never by reputation.
3. **Resolve every routing arrow to an absolute path.** A routing matrix that says "job → skill name"
   is half done; the reader needs `job → skill → /abs/path/SKILL.md`. The value of the map is that it
   removes the search.
4. **State the ownership layers separately.** Agents own the workflow; the kernel owns the gates;
   an executor owns the hands. Do not flatten them into one bar — capability ≠ authority is the point.
5. **Reconcile every count of the same object inside the document.** Two numbers that share a unit
   (`122 unique` vs a `32`-item subset; `95 + 23 = 118` vs `122 total`) read as a contradiction until
   the denominator hierarchy is declared. Declare it once, where the universe first appears.
6. **Render it so a reader can re-check it, not just read it** — see *Deliverable* below.

## Pitfalls

- **A tree census that does not follow symlinks undercounts by exactly the linked nodes.**
  `os.walk()` defaults to `followlinks=False`, so a parent whose children are symlinks reports
  near-empty — measured: one skill parent walked to `1` file while `followlinks=True` returned `52`.
  Capability stores are commonly symlink farms (`<view_root>/<x> → <canonical_root>/<x>`), so the
  default walk reports "1 file" for a 40-file skill and every downstream size judgement inherits the
  error. Walk with `followlinks=True`, and report `realpath != path` per entry so the reader can tell
  the canonical write location from the discovery view.
- **An external report's paths are CLAIMS, not findings — probe each before importing it.**
  A deep-research or third-party artifact that ships a filesystem inventory (paths, versions, tool
  names) can be wholly fabricated: measured 9 of 9 claimed paths absent, the claimed root never
  existing, and 3 of 4 version claims wrong (only the one that happened to match survived). Keep the
  *architecture* the report proposes; refuse its concrete paths and versions until each resolves on
  disk. Importing an invented path converts someone else's hallucination into your defect — and the
  reviewer who catches it grades your artifact as fabricated too.
- **A capability whose only copy lives in a view/harness tree is on loan, not canonicalised.** When a
  discovery path is a symlink into another owner's tree, the canonical write location is the target,
  not the view. Name both in the map; do not silently treat the view as the source.
- **Presence of a validator is not proof the thing validates.** A skill/manifest that *describes*
  maturity (a status field, a doctrine line) is not a measurement. Grade from the assets and the run,
  not from the descriptor's own self-report.

## Deliverable — make it re-checkable, not just readable

An audit that cannot be re-run is an opinion. When the map is rendered as a document (PDF/dossier):

- **Every data-bearing figure carries a reproducibility receipt:** provider · endpoint · as-of
  timestamp · scope · record count · raw-payload SHA-256 · rendered-figure SHA-256. `sha256(json.dumps(payload, sort_keys=True))` hashes the exact bytes. A screenshot is a claim; a hash-sealed
  receipt is a check.
- **Sentence-bearing rows become stacked cards, not table cells.** A table sized for a header
  collides when its cells carry prose. Convert each row to a small label/value card, each value on
  its own full-width line. Tables are for short cells (numbers, labels, statuses).
- **State the invariant on the page:** `Name ≠ Path ≠ Present ≠ Executable ≠ Proven`. It is the
  correction the whole document exists to make.

## Verification before delivery

- `file <out>.pdf` → `PDF document` (never a text file with a `.pdf` extension).
- Per-page char count catches spill pages: `pdftotext -f N -l N <out>.pdf - | tr -s ' \n' ' ' | wc -c`
  — a designed page carries hundreds of chars; a spill page carries < 300.
- Render every page to PNG and vision-check the map/routing pages specifically (the pages that carry
  paths and figures), plus every page carrying user-specific or source-quoted facts.
- Any figure generator that uses matplotlib on dark themes: verify the figure has non-background
  pixels (`(np.array(Image.open(f).convert('RGB')).mean(axis=2) > 200).sum() > 0`) before embedding.

DITEMPA BUKAN DIBERI.
