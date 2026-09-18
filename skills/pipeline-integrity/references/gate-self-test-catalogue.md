# Gate self-test catalogue

A gate is a control. This is how to prove it controls, distilled from defects that each passed a
review and then failed reality.

## The two directions

| direction | failure | test |
|---|---|---|
| under-block | a real violation ships | `must_catch`: each entry MUST be flagged |
| over-block | correct content is refused, so someone disables the gate | `must_allow`: each entry MUST pass |

Keep both lists in the config, beside the patterns. A reviewer adding a rule should see the
expectations next to it.

## Catalogue of defect shapes

### 1. Threshold in the wrong unit

A fraction stored as a percentage: the bounds read `0.06 <= 9.94 <= 0.75` and every healthy artifact
fails a correct measurement. Assert the unit in the failure message, and calibrate the bound against
a measurement you have actually taken.

### 2. Uncalibrated threshold

A blank-page floor chosen rather than measured refuses legitimately short pages. Measure your own
renderer, then record the reference figures beside the constant so the next editor knows where the
number came from.

### 3. Unanchored pattern

`ward` matches `forward-deployed`. `rasa` matches *ketakselarasan*. Anchor every deny pattern with
`\b`, and test each one against the subject matter the artifact actually discusses — bond yields,
training terminology and structural geology all contain words that look like violations.

### 4. Pattern that matches legitimate output

A leaked-token list containing `ZEN` or `CHRON` fails every correct render, because the artifact is
supposed to print those words. Keep only names that cannot legitimately appear.

### 5. Detector blind to its own failure mode

A leftover-token check for `\$[A-Z_]+` cannot see a prefix collision, because the bad substitution
consumes the `$` and leaves bare uppercase junk. Check the token NAMES as bare words as well — and
write the check **after** seeing a real failure. A detector written only from theory tends to miss
precisely the case that motivated it.

### 6. Detector that has never rejected anything

A sweep that always returns clean is decoration. Feed it a synthetic bad input and assert it is
caught, on every run. Same rule for a deny list: prove it can fire.

### 7. Gate defined, never called

Grep CALL SITES, not definitions. `len(re.findall(r'def _gate', src))` returning 1 says nothing;
`call sites - 1 == 0` says the protection does not exist.

### 8. Gate after the thing it checks

A validation stage invoked after publish reports on something already shipped. Check stage ORDER
explicitly — the control must sit upstream of the irreversible step.

### 9. Gate softened by fallback syntax

`... || echo "[WARN] ..."` converts a refusal into a log line. A gate must be able to stop the
pipeline; if it cannot, it is telemetry wearing a gate's name.

### 10. Counter field that is permanently zero

`privacy_rejections: 0` on every record ever written describes a mechanism that has never fired, and
a reader who greps the field name concludes protection exists. Prefer a field observed to reach
non-zero at least once, or label it UNPROVEN.

## Self-test shape

```python
CATCH = ["Syed rasa down hari ni", "his MSS package lands in March", "/root/AAA/x.py"]
ALLOW = ["forward-deployed engineers", "the unconformity marks a hiatus", "bond yields rose"]

def selftest(scan, cfg):
    problems = []
    for bad in CATCH:
        if not scan(bad, cfg):
            problems.append(f"MISSED: {bad!r}")
    for good in ALLOW:
        if hits := scan(good, cfg):
            problems.append(f"FALSE ALARM: {good!r} -> {hits[0]}")
    return (not problems), problems
```

Both lists grow from real failures, never from imagination. When a pattern is added, add the case
that justified it to `CATCH`; when one cries wolf, add the innocent string to `ALLOW`.

## Calibrating a numeric gate

Take the measurement first, then set the bound from it, and write the reference figures into the
test so the constant is not mysterious later:

```python
# measured: empty page 0.00-0.01% ink | heading-only 0.06% | real short page 0.17%
INK_FLOOR = 0.0005
```

Prefer a RELATIVE test where the population varies — a page under ~25% of the document's median ink
is an orphan, even if it clears an absolute floor.
