# Diagnostic Failure Modes

A probe that reports a clean result makes two claims: one about the world, and one about
itself. This file covers the second. Consult it when **building** a health check, monitor,
availability probe, or audit script — before you trust its first green run.

Every mode below has been observed producing a confident, wrong reading. They share one
remedy: **calibrate the instrument against a case whose answer you already know.**

## Taxonomy

| mode | what it looks like | the discriminator |
|---|---|---|
| **Causal clause is a guess** | one error string serves several unrelated conditions | a second probe that separates the candidate conditions |
| **Parse treated as success** | valid JSON describing an error reads as "found" | branch on transport status; treat blank/sentinel payloads as failure |
| **Output suppressed** | a counter counts zero because the tool was told to be quiet | remove the quiet flag from anything whose output you parse |
| **Non-representative sample** | the probe targets the one case guaranteed to work | probe representative inputs; report a rate |
| **Shape asserted from one payload** | reasoning/answer field read from the wrong key | handle every reply shape the provider documents; fall back |
| **Unbounded probe cost** | the check takes minutes, so nobody runs it | cap per-probe timeout at what the check actually needs |
| **Uniform result** | every subject scores identically | that is a property of the instrument, not a finding |
| **Name guessed, not enumerated** | a lookup under an assumed name returns null | enumerate the real namespace first, then re-test |
| **Wrong store** | counts queried from a location inferred from a parameter name | locate a record you just wrote, *then* assert on counts |
| **Permission read as meaning** | an empty field read as "no value" | a field can be empty because it was never populated vs. legitimately blank — check for a nearby status/error field |

## Discriminating probes (the concrete form)

The remedy is always the same shape: find an input whose outcome **differs** between the
candidate conditions, and run it.

**Is it blocked, or is the item gone?** Both produce the same error. Ask a metadata endpoint
that answers differently for the two cases:

```bash
curl -sS -o /tmp/o.json -w "%{http_code}\n" "<metadata-endpoint>?url=<target>"
# 200 with a populated title/author -> live; proceed
# 4xx, or 200 with an empty payload -> the ITEM is unavailable, not the lane
```

Run this **before** spending minutes on the expensive path, and never quote the coarse
error's causal clause as your conclusion.

**Did the write actually land where I think?** Counts from a store whose name you inferred
from a config parameter prove nothing. Write one record, then find **that record by its own
name** across every candidate store before asserting any count:

```bash
# enumerate first, then search by identity — not by assumed location
<list-stores>
for s in <stores>; do <query> "$s" "MATCH (n) WHERE n.name CONTAINS '<the-name-I-just-wrote>' RETURN n"; done
```

A count can rise from another writer; an item bearing your own identifier is proof.

**Is the measurement real?** Before trusting a threshold, verify the instrument responds to
both extremes. A silence detector run under a quiet flag reported `0 gaps` for a file that was
digitally silent *and* for one containing clear speech — it could not distinguish the cases it
existed to distinguish. Measure the underlying level directly and check both ends:

```bash
<tool> -hide_banner -i <input> -af volumedetect -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
# mean == max == the floor  ->  genuinely silent
# mean well above the floor ->  signal present
```

## Building a health check that can fail

1. **Pick representative inputs, not convenient ones.** The best-known/most-cached/most-
   healthy subject is the single worst choice — it is the one case guaranteed to pass.
2. **Report a rate, not a verdict.** `<k>/<n> probes succeeded` carries information a boolean
   cannot, and `0/3` is honest where `ok` is misleading.
3. **Make the failure path say what to do instead.** A red lane should name the working
   alternative, not just its own state.
4. **Calibrate once by hand.** Run the check against one case you have personally confirmed
   good and one you have confirmed bad. If it cannot tell them apart, it is decoration.
5. **Measure the work path, not the probe path.** A service's own health endpoint proves the
   endpoint answers; it says nothing about the deep consumer. Exercise the deepest consumer
   (the one that does the real work) and treat that as the verdict.
6. **Cap the runtime.** If the check is slower than the interval it runs on, it will be
   disabled or ignored — and an ignored check is indistinguishable from a passing one.

## Reporting

- Quote an error message as the **symptom** it is; do not repeat its causal clause as your
  finding.
- When you correct a conclusion an instrument caused, say which measurement was missing —
  owning the error without naming the skipped probe repeats it next session.
- A lane reported red with an honest reason beats a lane reported green on a probe that
  cannot fail.
