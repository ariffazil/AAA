# Runtime Tools Module — Containment Contract (X9 declaration)

> **Status:** X9 Option B declared (2026-09-27).
> **Authority:** T2 (10s announce window honored — see carry_forward receipt).
> **Subject:** `/root/arifOS/arifosmcp/runtime/tools.py` (28,447 deployed lines, 28,909 measured).

## The cycle, named

```
runtime.tools (28,447 LOC, 60 importers, 64 import 2-cycles)
└── tools.session  (15 back-edges to runtime.tools — the hot hub)
```

Substrate package is TIGHT (e-f76fd017 added 14 lines to runtime/tools.py while
calling it "tight"). Containment strategy is real AND the cycle is real. Both stand.

## Declaration (Option B — declare contained monolith)

This module is **declared as a contained monolith** with the following import-layer
contract. It is NOT a candidate for split until either (a) the WEALTH pattern is
back-ported, or (b) a downstream cycle hot-spot becomes a measured bottleneck.

### Allowed imports IN to runtime/tools.py
- `arifosmcp.runtime.*` — internal siblings
- `arifosmcp.kernel.*` — constitutional boundary (F1/F2/F13 enforcement)
- `arifosmcp.governance.*` — seal / verdict
- stdlib only at the leaf level

### Forbidden imports
- ❌ `from arifOS.kernel.tools.*` (kernel should not depend on runtime/tools)
- ❌ `from arifOS.skills.*` (skills are harness-level, never runtime)
- ❌ `from arifOS.federation.*` (federation reaches in via well-defined bridges)
- ❌ `from hermes.*`, `from aaa.*` (other organs are external — use arifOS routes)

### Cycle accounting

A 2-cycle is permitted if BOTH directions are inside the same module cluster
(`arifosmcp.runtime.*`). A 3-cycle is permitted ONLY if it stays within the
`runtime` cluster. Any cycle that touches a different cluster (kernel, governance,
federation, hermes, aaa) is a **CONTAINMENT BREACH** and must be reported as a
scar, not silently allowed.

### Future split trigger (when X9 will re-open)

Re-open X9 if ANY of:
1. `runtime/tools.py` exceeds **40,000 lines** (current 28,447, ~12,000 lines headroom)
2. Any single cycle hub has more than **30 back-edges** (current top: 15)
3. Two distinct call patterns emerge that share < 5% of imports (use signal from
   `forge_runtime_verify` or runtime profiler)
4. WEALTH's split pattern is back-ported and proven stable for 90 days

## Verification gate

```
[X] cycle count documented (64 import 2-cycles, 15 back-edge hot hub)
[X] import direction contract written (above)
[X] no current cycle touches external cluster
[ ] runtime/tools.py > 40,000 lines — RE-OPEN X9
[ ] back-edge count > 30 — RE-OPEN X9
```

## Reversibility

This contract is documentation. It does not mutate runtime/tools.py. No
blast radius. To undo: delete this file.

## What was deliberately NOT done

- Did NOT split runtime/tools.py (Option A). Reason: split is a T2 refactor with
  federation-wide blast radius; 10s announce window is insufficient to safely
  verify the refactor across 60 importers.
- Did NOT enforce import direction with a linter. Reason: too coarse — first cycle
  would be a linter scar, not a substrate scar. Wait for measured evidence.

DITEMPA BUKAN DIBERI ⚒️
