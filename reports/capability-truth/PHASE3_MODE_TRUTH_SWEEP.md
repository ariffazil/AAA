# PHASE 3 · MODE-TRUTH SWEEP — the other 6 tools (333-AGI, 2026-09-18)

> Read-only sweep of the 49 advertised mode-values not covered by the `arif_memory` fix.
> Method: handler location via `CANONICAL_TOOL_HANDLERS` → per-mode string evidence
> (module-scope + handler-scope), then package-wide deep-probe for zero-evidence flags.
> **Honest limit:** hit-count is evidence of implementation, not proof of reachable
> dispatch. The strong check remains a declared universe (STEP 3 pattern).

## Result — no ghost modes found; 2 flags resolved to real delegated implementations

| tool | advertised modes | zero-evidence flags | deep-probe verdict |
|---|---|---|---|
| arif_init | 11 | — | all present (1–15 hits) ✓ |
| arif_observe | 8 | `hybrid_discovery` | **REAL** — `tools/sense.py:826` (`if mode == "hybrid_discovery"`), 11 package hits |
| arif_think | 12 | `simulate` | **REAL** — `runtime/tools_internal.py:1292` (`elif mode == "simulate"`), 47 package hits |
| arif_judge | 5 | *(invalid row — measured through OTEL wrapper)* | re-probed: handlers `_arif_judge_deliberate` / `_arif_judge_deliberate_tool`; branches at `tools.py:11509` (validate), `:19454` (judge) ✓ |
| arif_forge | 7 | — (query/generate/recall/dry_run: 0 in-handler, 9–80 in-module = delegation) | no zero-evidence ✓ |
| arif_seal | 6 | — (ledger/changelog: 0 in-handler, 3 in-module = delegation) | no zero-evidence ✓ |

**Total: 57 advertised mode-values across 7 tools → 0 ghost modes.** The single
true ghost in this family was `arif_memory.audit`, already fixed (cb2411928).

## Measurement lessons (recorded)
1. **Module-scope grep under-reports**: handlers delegate (`sense`, `tools_internal`,
   megaTools). The `audit` case looked absent in the router but was real in the
   megaTool — same class as these flags. Never call a mode phantom without a
   package-wide probe.
2. **OTEL-wrapped handlers break `inspect.getsourcefile`** — `arif_judge` measured
   through `arifos_otel_wiring.py`. Use `inspect.unwrap` for proxy measurements.

## Why this did NOT become 6 universe declarations
Declaring a universe by hand for tools without an authoritative mode table would
recreate the exact anti-pattern STEP 3 removed (hand-copied lists drift). The
derivation requires each subsystem to expose its own mode table (as
`megaTools/tool_13_arif_memory.ARIF_MEMORY_MODES` does). **Extension pattern, not
a bolt-on** — recorded as the follow-on path.

## Permanent instrument added
`capability_truth_gate.py` now runs a **mode-evidence scan** (warning-level):
every advertised mode must appear as an implementation string somewhere in the
package. Zero-evidence modes surface as CI warnings (never build-breaking —
absence is a smell, not a verdict). This converts a manual sweep into a
regression instrument for the `audit`-class.

## Evidence
- Sweep run: in-process, live venv, handler-proxy table (2026-09-17T20:1xZ)
- Deep probes: `sense.py:826`, `tools_internal.py:1292`, `tools.py:11509/19454`
- Related: `PHASE3_STEP2_STEP3.md` (audit fix), `PHASE3_DEPLOY_DECISION.md` (deploy gate)
