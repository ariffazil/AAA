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
| **Permission read as meaning** | an empty field read as "no value" | a field can be empty because it was never populated vs. legitimately blank |

## Building a health check that can fail

1. Pick representative inputs, not convenient ones.
2. Report a rate, not a verdict.
3. Make the failure path say what to do instead.
4. Calibrate once by hand against known good and known bad.
5. Measure the work path, not the probe path.
6. Cap the runtime.

## Reporting

- Quote error as symptom, not causal clause.
- Name which measurement was missing when correcting.
- Red with honest reason beats green on unchallengeable probe.