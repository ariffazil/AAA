---
name: pipeline-integrity
description: "Use when auditing a gate, threshold, or sealed artifact."
version: "1.0"
metadata:
  hermes:
    tags: [gates, verification, integrity, render, ledger, auditable-artifacts]
triggers:
  - "design or audit a quality gate / validation step"
  - "build a deny list or threshold check"
  - "a scheduled render, brief, or card"
  - "hash-sealed artifact or ledger"
  - "verify a pipeline that someone else built"
---

# Pipeline integrity

> **Trigger:** you are writing a gate, validation, deny list, threshold, or pre-send control — or
you are deciding whether to trust one. Also any pipeline whose output is a sealed or hashed
artifact produced on a schedule.

## The one rule

**A control that cannot fail is not a control.** If every input passes, you have a log line
wearing a verdict's clothes. Most of this skill is the catalogue of ways that shape gets built by
accident, because each one looks like work from the outside.

Corollary: **a control must sit upstream of the irreversible step.** Validation that runs after
publish reports on something that already shipped.

## Gates: the two directions

| direction | failure | test |
|---|---|---|
| under-block | a real violation ships | `must_catch` — each entry MUST be flagged |
| over-block | correct content is refused, so someone disables the gate | `must_allow` — each entry MUST pass |

The over-blocking side is the one people skip and the fatal one: a gate that cries wolf on correct
content gets switched off, and after that it protects nothing. Keep both lists **in the config,
beside the patterns**, not in a test file — a reviewer adding a rule should see the expectations
next to it.

Six ways a gate becomes decoration, each with a test: `references/gate-self-test-catalogue.md`.
The short list — grep **call sites** not definitions; anchor every pattern with `\b`; never let a
pattern match words the artifact is supposed to print; check the threshold's UNIT; never soften a
gate with `|| echo "[WARN]"`; and treat a counter that has never held a non-zero value as a
placeholder, not a protection.

## Time in an artifact: compute it, never type it

Anything derived from a date — a countdown, an age, an interval — is `target_date - render_date`,
evaluated as the artifact is built. A number typed into a template is right for one day and wrong
forever after, and nothing in the pipeline is positioned to notice.

Store the event, not the number:

```json
{ "id": "budget-2027", "target_date": "2026-10-09", "timezone": "Asia/Kuala_Lumpur",
  "audience": "both", "source": "...", "confidence": "HIGH",
  "consequence": "HIGH", "actionability": "MEDIUM" }
```

Three silent defects in this class:

- **Subtract dates, not datetimes.** `(end_dt - now_dt).days` truncates the partial day and reads
  one short; `(end_date - now_date).days` is right. Off by one for the life of the pipeline.
- **A computed value can still be frozen.** `x = now + timedelta(days=164)` followed by
  `return {"od1_days": 164}` computes and then discards. It greps as dynamic and behaves as a
  literal — worse than an obvious hardcode, because a reviewer sees `datetime` and arithmetic and
  moves on.
- **A wrong date survives review.** An event built inline as `datetime(2027, 10, 1)` when the real
  date is `2026-10-09` prints ~378 where the truth is 21. Nothing compares it to a stored date, so
  nothing objects, and the figure ships confidently once a day.

**The self-test that proves it moves** — a frozen number cannot pass this. Render the same spec at
two dates N days apart and require every displayed value to shift by exactly N:

```python
counts = lambda d: {e["id"]: e["days"] for e in live_events(d)[:3]}
a, b = counts(date(2026, 9, 18)), counts(date(2026, 9, 28))
assert set(a) == set(b)
for k in a:
    assert b[k] == a[k] - 10, f"{k} did not move"
```

Inject `now` as a parameter, or this test is not writable at all.

**Expiry.** An event past its target leaves the active set — it does not render as `0` or a negative
count. Test that path by rendering at a date beyond every known target and asserting no day-count
cell is produced.

**One clock only.** Two components computing the same day-count WILL eventually disagree, and both
land on the same page. Exactly one component owns time; everything else reads its output. A
content-supplier module carrying its own clock gets that clock **deleted, not repaired**.

**Rank from bands, not fake precision.** With qualitative inputs (`HIGH`/`MEDIUM`/`LOW`), rank on a
small integer product and say so. A four-decimal float over banded inputs is arithmetic theatre —
it implies precision the inputs never had. Rank urgency and consequence SEPARATELY from date
proximity: the nearest deadline is often not the most consequential one.

## Evidence must survive the next run

If a hash enters a ledger, the file behind it must not move:

```
OUT/EDITION-002.pdf            # rewritten every run — every earlier row now dangles
OUT/EDITION-002-a1b865d7.pdf   # every version stays resolvable
```

With a fixed output path, each run overwrites the file the PREVIOUS ledger row hashed, so only the
newest entry verifies. Measured on a two-artifact-per-day pipeline: **4 of 7 rows stale**, against
1 of 1 examined by the reviewer who reported the chain intact. A ledger entry whose artifact is
mutable records an event, not a verifiable claim. If content-addressing is impossible, add
`superseded_by` so an old hash resolves to its successor instead of dangling.

A file cannot contain its own hash: the content hash covers the canonical SOURCE before
substitution (so it is embeddable), the artifact hash covers the rendered bytes and ships in a
sidecar. Say plainly that **a hash proves integrity, never accuracy**.

## Render and substitution pitfalls

- **Token substitution collides on prefixes.** `$PHASE` eats `$PHASELABEL`; `$QYANG` eats
  `$QYANGSRC`. Substitute **longest token first**. A leftover-token scan for `\$[A-Z_]+` cannot see
  this class, because the bad substitution consumes the `$` and leaves bare uppercase junk
  (`"...of no use.SRC"`) on the finished page — check the token NAMES as bare words too.
- **Never generate text with a diffusion image model.** Words must be typeset, not generated;
  diffusion corrupts letterforms (`"Say Less"` renders as `"Say Lcss"`) and the damage survives a
  glance. Render text as HTML/SVG and screenshot deterministically.
- **Measure the canvas; do not guess it.** Render once at a deliberately tall window, find the last
  row carrying ink, then size to that plus a deliberate margin. A guessed height fails both ways:
  a band of empty page reads as unfinished, and too short clips the footer.
- **Filenames with spaces silently break `MEDIA:` delivery.** The path truncates at the first space
  and nothing is delivered, with no error anywhere. Use hyphens; never rely on quoting.
- **A vision pass finds candidate defects; it does not measure them.** Worth running — one caught a
  real leftover token that every code check had passed — but the same pass reported a symbol
  off-centre by ~70px that a pixel count put at -0.5px, and reported a typo that `grep` found zero
  times. Treat its output as a hypothesis: measure before changing a pixel, and never relay a
  vision-read number as a fact.

## Trusting someone else's verification

**"Verified" means verified where the verifier looked.** A verdict checked against the newest, the
most convenient, or the already-repaired instance is true of THAT and may be false of the object it
describes. This is not fabrication — the evidence exists — which is exactly why it is hard to
catch. Two observed shapes:

- *"the hash chain is intact"* — checked against the latest ledger row only; older rows hashed a
  file a later run overwrote.
- *"the data is corrected"* — checked against the component that WAS fixed, then applied to a
  sibling nobody touched that still carried a year-scale error.

Before repeating a verdict: ask **which instance was sampled**, then run the same check across every
instance. Follow the paths the report names — a report pointing at a path that does not resolve is
not false, but a verifier who follows it finds nothing and may wrongly conclude the work does not
exist. Report "unresolved path", never "absent".

**Your own probe is also a claim.** Before reporting that a source contradicts you, verify the
probe's own assumptions — a type or shape you assumed rather than read will manufacture a
contradiction that does not exist.

**Record the refuted hypotheses.** When a suspicion dies under measurement, write down both the
suspicion and what killed it, or the next reader re-derives it and burns the same hour.

## Reporting state

Three verdicts, never two: **ALLOW / HOLD / DEGRADED**. "I could not verify" is not "it is fine" —
fail CLOSED when the evidence source is unreadable.

Report transitions, not booleans: `PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED`. A gate
that has never fired has no measured behaviour; state how many real cycles it has actually seen
rather than naming a maturity stage it has not reached.
