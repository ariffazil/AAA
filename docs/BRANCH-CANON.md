# BRANCH CANON — AAA (S1.6, 2026-09-24, F13 stabilization directive)

- **main = canonical.** Local ref == origin/main == working tip (08ddf64a).
- Working checkout lives on `proposals/orthogonality-v02-hermes-mapping` — it IS the federation working-state lane and is kept identical to main after S1 merge. History: 145-commit divergence (333-AGI 89 / FI-007 26 / Hermes 25+) was the live work, not orphan WIP; merged with origin/main 2026-09-24.
- `canon/**` carries per-file + directory `chattr +i` (canon-lock ritual). Git operations that must rewrite canon need temporary `chattr -i` + snapshot insurance (see 2026-09-24 S1 merge receipt).
- Runtime telemetry (state/ops-fabric, state/event-bridge, cockpit last-run) is gitignored — never commit it.
