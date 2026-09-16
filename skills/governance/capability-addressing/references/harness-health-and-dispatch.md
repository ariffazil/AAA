# Harness Health & Worker Dispatch

Depth for the *worker* layer of capability addressing: which harness is alive, whether the
health reading can be trusted, and the false-absence traps that make a working worker look
dead. Load this when routing work to a coding harness or quoting a mesh health matrix.

## Run the probe script — do not hand-type the probes

```bash
bash /root/AAA/scripts/mesh-health-probe.sh
echo /run/arifos/mesh-health.json   # SOT, schema arifos.mesh-health.v1
```

The script is the **SOT writer**: it runs every harness probe, classifies
PASS / EXTERNAL / FAIL / DOWN, writes the SOT with a `generated_at_utc` stamp, and appends
ONE transition line to `/root/AAA/terminal/holds.txt` only when a harness newly goes dead
(that file's law is: delete the line when resolved). Running it is the intended way to
refresh state. Read the SOT afterwards rather than re-deriving CLI invocations by hand —
if a hand-written invocation disagrees with the script, the script is right.

## Freshness is part of the reading (sensor TTL)

The SOT carries `generated_at_utc`. A stale SOT is a previous session's answer, not this
session's. Check the stamp, then re-probe before quoting a verdict — and re-probe AGAIN
before any repair claim. States flip within the hour in BOTH directions: a money-gated
harness returning to PASS once the ledger is topped up is normal, and so is a fresh FAIL on
a harness that passed this morning. Always report the stamp alongside the matrix.

## EXTERNAL is not FAIL

A 402 / 429 / quota wall means the harness is **alive and money-gated**, not broken. Report
those rows as alive-but-unfunded. Collapsing them into FAIL misreports a sovereign budget
question as an infrastructure fault and sends the next session chasing a phantom config bug.

## Version drift between hosts is informational, not a defect

A remote worker pool carries its own copies of harnesses, and their versions legitimately
differ from the primary node's. Difference ≠ defect unless behaviour differs materially,
protocol compatibility breaks, a security patch is missing, or reproducibility requires
equality. Report **"versions known + compatibility proven"**, never "versions identical" —
making all versions equal an invariant costs a maintenance loop and buys nothing.

## False absence on a remote pool

**Never declare a remote harness DOWN from a bare `command -v` over SSH.** Node-based
harnesses there commonly live under a user-local node install and are absent from a default
non-interactive SSH PATH, so a bare probe reports MISSING for a harness that is installed,
configured, and working. Probe through the pool's dispatch wrapper (which bootstraps each
harness's PATH itself) or source the node environment first.

Phantom absence and ghost capability are the same defect: the map lies in both directions.
A capability may be declared **down** only after an inventory sweep plus an alternate-lane
test, and declared **present** only if the artifact resolves right now.

## Reporting shape

```
MATRIX     harness × verdict × latency × note
SOT STAMP  <generated_at_utc>  (state it; a verdict without a stamp is a rumour)
EXTERNAL   listed as money-gated / alive, never folded into FAIL
FIXES      attributed to the responsible lane, not self-assigned cross-lane edits
```
