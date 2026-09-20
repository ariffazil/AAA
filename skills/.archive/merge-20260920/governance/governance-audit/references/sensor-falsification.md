# Sensor Falsification — proving an instrument before trusting its output

A coverage audit is arithmetic on top of measurements. If any measurement is produced by an
instrument that cannot return non-zero, or is reported without the method that produced it, the
resulting coverage figure is fiction. Run this before computing coverage.

## Rule 1 — Every sensor needs a positive control

Before reporting a zero, negative, empty, or "clean" result, run the same instrument against an
input that MUST produce a hit.

- If the instrument returns empty on a known-non-empty input, the instrument is dead, not the
  world. Report `UNMEASURABLE`, never `zero`.
- The dangerous form is a monitor whose only possible output is "all clear": every inference built
  on it inherits the false negative, and nothing in its output ever contradicts it.

```bash
# positive control — choose an input certain to match, run the same command shape
<probe> <known-hit>     # must return a hit
<probe> <target>        # only NOW does an empty result mean anything
```

## Rule 2 — Dereference before counting

A probe that reads a symlink measures the map, not the territory.

- Plain `find` over a symlink farm returns 0 for a populated tree. Use `find -L`,
  `os.walk(root, followlinks=True)`, or `realpath`.
- Identical trees reachable from two mount points or symlinked surfaces are ONE tree seen twice.
  Deduplicate on realpath before reporting a count.
- Absence claims are the highest-risk output. A false-empty is indistinguishable from a true-empty
  in the result, so it must be confirmed by a second, differently-constructed probe.

## Rule 3 — De-metadata before matching

Structured corpora commonly prefix the field you want with machine metadata (routing tags, tier
and floor annotations, bracketed prefixes). Matching on that prefix makes every tagged item
"similar" to every other tagged item and manufactures one large fake cluster.

- Strip the metadata prefix **repeatedly until stable** — bracketed forms can nest or contain the
  closing delimiter, so a single-pass strip leaves residue that still matches.
- Filter by document frequency as a backstop: tokens appearing in a large fraction of the corpus
  carry no discriminating signal.

## Rule 4 — Never separate a number from its method

Any figure quoted onward is quoted as fact. A bare percentage is uninterpretable.

Always state: **matching rule + threshold + corpus/surface list.** Two defensible measurements of
the same corpus can differ by an order of magnitude purely on rule choice — token overlap versus
phrase match — and both be "correct". When you find such a disagreement, report it as a method
divergence and name the deciding parameter; do not average them and do not pick the survivor.

## Rule 5 — Re-probe before repairing, and re-probe before reporting

Any recorded state table is a snapshot with a TTL, not a state.

- Re-run the probe before acting on a stored verdict — this includes stored FAILURES, which have a
  habit of being already fixed while the table still shows them broken.
- State-flipping classes (quota walls, funding gates, rate limits, transient upstream errors) can
  change between two probes minutes apart. Report the conflict as a boundary condition rather than
  declaring the subject "alive" or "dead" from a single sample.
- When two sensors disagree, the disagreement is the finding. Do not silently prefer the newer,
  the faster, or the one that agrees with expectation.

## Rule 6 — Sensor state may not be self-reported

When the measurement is about the system that produced it (a gate's own coverage, an agent's own
mutation history, a monitor's own health), the producer is not an acceptable source of the number.
Compute it from an independent artifact: the filesystem, the version-control log, the live endpoint,
the boundary ledger.

## Output

```
Instrument:        <command or query>
Positive control:  PASS | FAIL (input: <known-hit>)
Method:            <matching rule + threshold + corpus>
Dereference:       yes/no   Metadata-stripped: yes/no
Staleness:         probe run at <time>; prior verdict <time>
Verdict:           MEASURED | UNMEASURABLE | DIVERGENT (vs <other method>)
```
