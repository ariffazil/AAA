---
name: value-provenance-testing
description: "Use when a number or hash may be invented."
version: 1.0.0
---

# Value Provenance Testing

For when an artifact is *present and plausible* but the value inside it may never have been
measured. Existence checks answer "does this file/field exist". They do not answer "was this
number derived from anything". A schema that requires a field's presence passes on invented
content by design: **field presence ≠ field truth.**

Use this on receipts, evidence objects, witness ledgers, benchmark tables, agent status
reports, and any dashboard claiming to render live data.

## The five tests

Run them in this order — cheapest first, each independent.

### 1. Digest periodicity

A 64-hex string is *shaped* like SHA-256; it is not evidence of one. Enumerate divisors of
the length and test whether the string is a short unit repeated (`s[:n] * (len//n) == s`):

```python
for n in range(2, 33):
    if len(h) % n == 0 and h[:n] * (len(h)//n) == h:
        print(f"REPEATS every {n} -> {h[:n]}"); break
```

Real digests never repeat. A string built as `<32 hex>` + `<10 hex> × 3` is typed, not
computed. Repair: set the field to `null` and mark it `MISSING` — an honest gap outranks a
complete-looking lie, and most schemas already carry a missing-value slot for exactly this.

### 2. Recorded environment vs host

Any recorded `runtime_environment` — `os`, `arch`, `python_version`, service PID, git SHA —
is a claim about a machine. Compare against `uname -srm` and the live process on the host you
are standing on:

```bash
uname -srm
ss -tlnp | grep ":<port>"
tr '\0' ' ' < /proc/<pid>/cmdline
```

An architecture string naming different hardware than the host voids the witness. **A
fabricated witness is worse than no witness**, because it reads as independent corroboration.

### 3. Identifier identity match

A resolvable DOI / arXiv id / URL is not a *correct* one. Fetch it and compare **five fields**:
title, authors, year, journal, page range. One HTTP 200 is not an identity match.

```bash
curl -s "https://api.crossref.org/works/<DOI>"     # title, authors, container, pages, year
curl -s "https://api.openalex.org/works?search=<title>&per-page=5&select=title,publication_year,doi"
```

A DOI resolving to an unrelated paper retracts the claim it was attached to — not merely the
citation line. If the resolved title names a different subject, region, or method, or shares
no author, the citation was never checked.

### 4. Uncertainty narrower than its source

If the source publishes a range (min–max, or a stated interval), the reported ±σ must not be
tighter than the source's own span. A point taken from the end of a 20-unit published range
and labelled ±2.5 did not inherit that precision from anywhere — it was chosen so a
downstream test would pass.

Compare reported σ against the source's **half-range** before using it as a decision
threshold. Widening σ back to the published span usually flips PASS/FAIL to INDETERMINATE —
and that is the honest result.

### 5. Counterfactual input

To separate "computed" from "hardcoded", change the input and re-observe. Feed a different
value through the same engine, or edit a **copy** of the data a page reads, and check whether
the displayed result moves.

Output that does not move is written, not measured. Run this on any panel, dashboard, or
receipt claiming to render live state — and never mutate the live artifact to test it. When
it does move, find the **crossing point**: where the verdict flips tells you what the engine
keys on, and whether that threshold is physical or hand-picked.

## A green test suite is not a truth claim

Ask two questions of any suite that reports success:

- What would have to change for this test to fail?
- Does any test exercise the value's **provenance**, or only its presence?

A test asserting `model A = PASS, model B = FAIL` over windows the author chose locks those
inputs in place. It is a regression guard on a decision, not a validation of the mechanism.
Tests that reject missing CRS / missing datum / missing ±σ **are** real gates and belong —
they are anti-fabrication fixtures. A suite of six such gates can still be missing the one
that matters: *does this source exist, and does it say what we claim?*

## When a value moves between reads

A field that changes on every request (`null` → `0.35` → `0.22` → `0.42` within an hour) is
being recomputed per call, not stored. Sample it several times, report the **range and the
timestamp**, and never quote a single reading as the state. Two observers who disagree about
such a field are usually both correct at different instants — check for a process restart
between their probes before calling either of them wrong.

## Procedure

1. List the load-bearing values in the artifact (hash, DOI, σ, env, verdict, count).
2. Run tests 1–5 against each, keeping the raw command output.
3. Label each value VERIFIED / REPORTED / UNKNOWN / FABRICATED.
4. Repair by **removing or nulling**, never by substituting a better-looking value. A
downgrade to `INDETERMINATE` is a stronger result than a fabricated `PASS`.
5. Keep the discarded claim visible in a correction notice — what was asserted, what it
   should have been, why. Deleting the trail makes the next reader re-derive the same error.
6. Re-run the suite with the invented value gone. If a test now fails, that test was
   asserting the invention, not checking the source.

## Floors

- F2 TRUTH — a value is not true because it is shaped like a measurement.
- F9 ANTIHANTU — precision theatre is deception with decimals.
- F11 AUDITABILITY — every repaired field keeps a note saying what it was and why it changed.
