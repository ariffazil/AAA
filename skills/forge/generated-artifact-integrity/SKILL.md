---
name: generated-artifact-integrity
description: "Use when a rendered artifact prints live numbers."
version: "1.0"
author: "hermes-curator"
license: "MIT"
metadata:
  hermes:
    tags: [rendering, integrity, verification, gates, templates, delivery]
    related_skills: [infographic-generation, docforge-document-lane, forge-pdf-delivery]
triggers:
  - "build a recurring poster / card / brief"
  - "render an infographic from data"
  - "the artifact prints a countdown or a price"
  - "placeholder token leaked into output"
  - "gate that cannot fail"
  - "audit a rendered artifact"
---

# Generated Artifact Integrity

> **Trigger:** you are building or auditing a rendered artifact that repeats — a daily poster, a
> status card, a dashboard brief, a PDF — and it displays numbers, dates, counts, or quotes.
>
> Companion skills (`infographic-generation`, `docforge-document-lane`, `forge-pdf-delivery`) cover
> design honesty, document lane structure, and delivery mechanics. This skill covers the thing they
> assume: that what the artifact prints is still true when it prints it.

## The one law

**An artifact is a claim.** Every number, date, countdown and quote it prints is an assertion about
reality at the moment of rendering. If a value cannot be recomputed at render time, it must not be
printed as a live value.

The characteristic failure is not a crash. It is a correct-looking artifact that quietly prints
last week's number with this week's confidence.

## Procedure

### 1. Separate content from layout

Content lives in structured JSON. Layout lives in a template. One renderer reads both. When content
and layout are interleaved, every correction becomes a code edit and neither can be diffed.

### 2. Substitute tokens LONGEST FIRST

```python
# WRONG — $PHASE is a prefix of $PHASELABEL, so the label renders as "pagiLABEL"
html = t.replace("$PHASE", phase).replace("$PHASELABEL", label)
# RIGHT — longest token first
html = t.replace("$PHASELABEL", label).replace("$PHASE", phase)
```

A prefix collision is silent and produces plausible-looking output. Sort the token list by length
descending, and keep it sorted when you add a token.

### 3. Detect surviving tokens two ways

A leftover scan for `\$[A-Z][A-Z_]+` is **not sufficient**: a prefix collision deletes the `$` and
leaves bare uppercase junk (`...of no use.QYANGSRC`). Check both:

```python
leftovers = sorted(set(re.findall(r"\$[A-Z][A-Z_]{1,}", html)))   # $-prefixed survivors
leaked    = [t for t in TOKEN_NAMES if t in html]                    # bare-name survivors
```

Keep `TOKEN_NAMES` to names that are **not** legitimate output words. Listing `ZEN` or `CHRON` when
the poster legitimately prints "APEX·ZEN CHRON" fails a correct render — the opposite defect.

### 4. Compute live values at render

- **Never type a day-count.** Store `target_date`; compute `(target_date - render_date).days`.
- **Subtract DATES, not datetimes.** `datetime_a - datetime_b` truncates the partial day and is off
  by one. `.date() - .date()` is not.
- **Expire past events.** An event whose date has passed leaves the active pool and renders as
  history — never as `0` or a negative count.
- **Rank by consequence and actionability, not by nearest date.**
- **Beware computed-then-discarded:** `x = now + timedelta(days=164)` followed by
  `return {"x_days": 164}` greps as dynamic and is static. Execute the function; never read it.

### 5. Prove the clock moves

Render the same content at two dates ten days apart in a self-test and fail unless every displayed
count shifts by exactly ten. A typed number cannot pass this. Then push the clock past every target
and confirm each event expires out of the active set and no day-count cell renders.

### 6. Measure the render, then look

```python
g = np.asarray(Image.open(png).convert("L"))
rows = np.where((g < 235).sum(axis=1) > 3)[0]
dead_space = g.shape[0] - rows.max() - 1     # size the canvas to this, not to a guess
ink_pct = 100 * float((g < 235).mean())      # a blank page reads 0.00-0.01%
```

Size `body` height just past the last row of ink. A canvas 40% taller than its content reads as
unfinished. Check the bottom margin is clear rather than assuming it.

### 7. Seal, and state retention

Hash the artifact and write a sidecar. But see "Mutable target" below — a hash of a file that will
be overwritten is an event log, not a verifiable claim.

### 8. Deliver with a hyphenated filename

`MEDIA:/path/NAME WITH SPACES.png` truncates at the first space and **silently sends nothing** — the
file is correct on disk and never arrives. Name artifacts `lowercase-with-hyphens`, no spaces, and
let the builder script do the naming so it cannot recur by hand.

## Pitfalls

- **A gate that cannot fail is not a gate.** If a check returns the same result for every subject it
  has never discriminated anything. Suspect the check before the data.
- **Anchor a structural regex on structure, not on an exact class string.** `class="cell a"` misses
  `class="cell a q"` and reports a present cell as empty. Match the prefix.
- **A non-greedy regex can end before the block you meant.** `r'<div class="row">.*?</div></div>'`
  stops at the first `</div></div>`, which occurs *inside* the label before any cell. Split on the
  row marker instead of matching a nested closing sequence.
- **A marker that is a substring of legitimate vocabulary fires everywhere.** `ward` matches
  `forward-deployed`; `rasa` matches `ketakselarasan` (the geology term for an unconformity).
  Always `\b` both ends, and never list a word the subject matter uses normally — a rule that fires
  on the domain itself gets switched off, and then it protects nothing.
- **A deny pattern that spans a whole document produces nonsense matches.** Window person-adjacent
  patterns: `\b(name)\b[^.]{0,160}\b(state-word)\b`, not "document contains both".
- **List inner-state words in every language the content uses.** A single-language list missed
  "Arif is worried about the outcome".
- **Vision output is a lead, not an instrument.** Any geometry claim (off-centre, overflowing,
  misaligned) → measure pixels before acting; a vision pass has reported ~70px off-centre where
  measurement showed 0.5px. Any quoted-text claim → diff against the rendered source; a vision pass
  has reported a phrase that appears zero times. Substituting measurement often reveals a *different*
  real defect — fix the measured one and record that the reported one was refuted.
- **Mutable target.** A ledger row recording `{artifact, artifact_sha256}` against a FIXED output path
  dies the moment the next render overwrites the file: the newest row verifies, every prior row is
  stale. Content-address the artifact (`name-<hash8>.ext`) so old hashes stay resolvable, or carry
  `superseded_by` on the row. Determinism (re-render identical input → identical hash) proves
  reproducibility and says nothing about retention; hold the two properties separately.
- **Design label boxes for unequal word lengths.** A 5-letter word beside a 3-letter word centres
  geometrically and still looks crooked. Give the labels equal-width boxes, not just centring.

## Two-way gate self-test

Any refusal gate needs a self-test that proves it works **in both directions**, and it runs before
the thing it guards:

```python
def selftest(rules):
    problems = []
    for bad in MUST_CATCH:            # real leaks
        if not scan(bad, rules): problems.append(f"MISSED: {bad!r}")
    for good in MUST_ALLOW:           # legitimate content the rule must not fire on
        if scan(good, rules): problems.append(f"FALSE ALARM: {good!r}")
    return problems
```

A gate that has only ever passed has not been shown to work. A gate that cries wolf on correct
content gets disabled by whoever holds the release, and then it protects nothing. Both halves belong
in the same test.

## Anti-patterns

| Anti-pattern | What to do |
|---|---|
| Countdown typed into the template | Store `target_date`, compute at render, expire past events |
| Short token replaced before long token | Sort tokens by length descending |
| Leftover check greps only `$TOKEN` | Also test bare token names |
| Gate verified only by "it passed" | Add a must-trip fixture and a must-not-trip fixture |
| Vision report treated as the finding | Measure, then look; re-measure before believing |
| Fixed output path + recorded hash | Content-address, or record `superseded_by` |
| Space in the delivered filename | Hyphenate; make the builder name the file |
| Canvas height guessed | Measure last row of ink, size to content |

---

*Class: recurring rendered artifacts. Sibling skills cover design honesty
(`infographic-generation`), lane structure (`docforge-document-lane`) and transport
(`forge-pdf-delivery`); this one covers whether the artifact is still telling the truth when it
prints.*
