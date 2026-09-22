# Conservation Accounting — the per-hop balance test

Topical depth for `SKILL.md` § *Conservation accounting*. Read when a loop reports success while
its conversion stages report zero, and you need to prove whether that is idleness or absorption.

## The invariant

For any hop that maps `X → Y`:

```
N_input = N_accepted + Σ N_rejected(named reason) + N_deferred(future condition)
```

Report the ratio, not just the balance: `accounted / N_input`. `100.00%` is the only passing value.
Anything less is unaccounted state, and the shortfall is the size of the finding.

## The probe pattern

Load the production module by path so its own predicates and constants govern the replay. Never
transcribe the filter logic into the probe.

```python
import importlib.util, json
from datetime import datetime, timezone, timedelta
from pathlib import Path

spec = importlib.util.spec_from_file_location("target", SRC_PATH)
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)   # module-level constants only; guard against running its main()
```

Then replay the production branch order and record a reason at each exit:

```python
import collections
rej, detail, eligible = collections.Counter(), collections.Counter(), []
for e in entries:
    if e.get("kind") != "open_loop":
        rej["not_open_loop"] += 1; detail[f"not_open_loop:{e.get('kind')}"] += 1; continue
    if e.get("status", "OPEN") in ("DONE", "CLOSED"):
        rej["status_closed"] += 1; continue
    hit = set(e.get("tags", [])) & mod.SOVEREIGN_TAGS      # the module's own constant
    if hit:
        rej["sovereign"] += 1
        for t in hit: detail[f"sovereign_tag:{t}"] += 1
        continue
    if not mod._is_stale(e, now):                           # the module's own predicate
        rej["not_stale"] += 1
        # ... break down why: no_timestamp | recently_touched | too_young(Nd<Md)
        continue
    eligible.append(e)

picked   = eligible[:mod.MAX_PICKS]
deferred = eligible[mod.MAX_PICKS:]
assert len(entries) == len(picked) + sum(rej.values()) + len(deferred)
```

Rules that make the replay trustworthy:

- **Granularity is the proof.** `sovereign: 8` says nothing; `sovereign_pattern:DELIBERATE NEXT
  SESSION ×4`, `sovereign_pattern:F13 BINARY ×2`, `sovereign_tag:money ×1`, `sovereign_pattern:KHAIRIL
  ×1` proves the guards fired on precisely the entries they were written for. A blunt filter and a
  specific one produce the same aggregate and completely different histograms.
- **The deferred bucket is not waste.** It is the exact worklist for the next run — print the item
  ids. It also exposes the throughput ceiling, which is a different finding from a broken filter.
- **Both passes matter.** Observed (live clock) shows the loop's behaviour now; reconstructed
  (clock pinned to the run under audit, entries filtered by their own `ts`) shows what the audited
  run saw. Reconstructed ≠ restored: an absent backup means approximation, and that belongs in the
  report.
- **Read-only by construction.** Never call the module's write path. If the question cannot be
  answered without mutating the store, you are no longer in a read-only probe and must declare the
  write and its byte delta.

## What a balanced result means

Balanced means **the filter is innocent**. That is a real result and must be reported as one:
retract the hypothesis in writing, with the arithmetic that refuted it, and name which of your
earlier claims survive. Do not soften it into "partially confirmed".

Balanced at hop 1 does **not** clear the loop. Move the same equation to the next hop — the
judgment, and the write-back. Empirically the interesting failure is one stage downstream of where
you first looked, because the first hop is usually the one that already has tests.

## Worked shape — filter clean, judgment leaking

```
HOP 1 filter     : 138 = 3 accepted + 128 rejected(named) + 7 deferred   ✅ 100.00%
HOP 2 judgment   : 14 executions -> 14 verdicts persisted, 0 reasons persisted ❌  0%
HOP 3 write-back : consumer rewrote the queue to `remaining` only
                   -> dedupe key destroyed -> 3 loop ids re-examined 2-3x each,
                      all still unresolved
```

Each hop is individually plausible and the system reports success at every one. The defect is only
visible when the three are read as a series. That is the whole argument for testing the invariant at
every hop instead of once.

## Generalisation

The same equation applies to every selection surface in a federation, not only loop machinery:
memory retrieval, search reranking, policy gates, tool routing, candidate selection, claim
filtering, affordance routing. One shape, repeatable check: **the token is emitted; the reason is
not.** A selection mechanism without pass-through accounting cannot distinguish "there was nothing"
from "I consumed it all", and will report both as healthy.
