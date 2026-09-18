# The shared failure shape — worked examples

## Pattern

A claim is checked against the newest or most convenient state. It is TRUE of
that state. It is FALSE of the object the claim names. Nothing about it looks
like deception; it looks like diligence clipped short.

## Instances observed in one session

| Claim | What was checked | What was true of the whole object |
|---|---|---|
| "sha256 chain intact" | the newest ledger row | 4 of 7 rows stale |
| "corrected data" | the gate that was fixed | the clock was 356 days wrong |
| "3 PNGs rendered" | one directory | 7 across two trees |
| "OD1 hidden from Syed" | a metadata flag | the renderer printed it |
| "4-day freshness window" | nothing | the window did not exist in that component |

## Why it matters more than ordinary error

A verifier's report is a POINTER, not a proof. Downstream, "verified" stops
meaning "checked" and starts meaning "checked where the verifier happened to
look". Once that drift sets in, every later decision inherits it.

## Counter-discipline

1. Re-derive from disk; never accept a summary, including a friendly one.
2. Check the WORST entry, not the newest. The newest is guaranteed current.
3. For any count, count it. Do not read a report of a count.
4. When a claim is confirmed only partly, say which part. "Gate fixed, data
   not" is a complete sentence and it prevents the next reader's error.
5. Audit your own probe too. An auditor who does not is a second narrator.
