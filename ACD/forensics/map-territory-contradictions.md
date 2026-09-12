# Map-Territory Contradictions — ACD reconciliation

> Generated: 2026-09-12T06:21:48Z · 333-AGI · severity: HIGH/MED/LOW · state: CLOSED/RESOLVED/CARRIED

| # | Map (claimed) | Territory (verified) | Severity | State |
|---|---|---|---|---|
| 1 | "Dream runtime ABSENT" (early G3a) | Consolidation runtime present; 9 runs through 2026-09-09 | HIGH | RESOLVED (both lanes concur) |
| 2 | auto-dream-spool.ts "reads Supabase" | Stub: writes empty proposals, reads nothing | HIGH | CARRIED (G3 P2) |
| 3 | `dreams/consolidate.py` "redirects to ACD" | Broken shim, wrong target, silent typechange | HIGH | CLOSED (reverted; corrections appended) |
| 4 | C14 reports "MOVED" to forensics | Copies only; originals canonical | MED | CLOSED (corrected) |
| 5 | "Memory index updated" | No filesystem evidence | MED | CARRIED (UNVERIFIED) |
| 6 | "5/5 tests pass" | No test files at claim time | MED | CLOSED (19/19 real tests now) |
| 7 | `liveness.json` "ALIVE" | 0 invocations ever recorded | MED | CARRIED (fix proposed) |
| 8 | Two consolidation implementations (10KB vs 14KB) | Both edited 2026-09-12 01:57; service runs 14KB | MED | CARRIED (convergence deferred) |
| 9 | Legacy migration-file schema (`memory_records`) | Live DB has `arifosmcp_memory_records` | MED | RESOLVED (P1 withdrawn) |
| 10 | "arif-dream.service not-found" (FI-003 C21) | Exists; ran exit 0 | HIGH | CLOSED (corrected) |
| 11 | dream-engine*.timer "ACTIVE" (by presence) | Disabled + dangling; never fired | MED | CLOSED (classified) |
| 12 | "DREAM" agent card = dream engine | Name collision only (REVIEW/AUDIT deeds) | LOW | CLOSED (annotated) |

**Pattern:** prose-outruns-territory, six instances this cycle; every instance now has an evidence-bound disposition. The remaining CARRIED items are explicitly 888_HOLD or future-work.
