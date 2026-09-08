# Gate Promotion — Detection Is Debt Until It Can Say NO

> Forged 2026-08-25 · FI-003 eureka extraction (SEAL candidate OBSERVE_ONLY → F13 ratified for instill)
> Source contradiction: kernel floors fail closed while quality/surface/supply signals fail open.

## The Law

Every observation organ in the federation must declare one of three enforcement tiers:

| Tier | Meaning | Example |
|---|---|---|
| `OBSERVE_ONLY` | Signal is recorded, never blocks | telemetry counters |
| `ANNOUNCE` | Signal surfaces to sovereign, 10s veto window | registry/doc updates |
| `GATE` | Signal can block the action/commit/deploy it guards | LSP pre-commit, supply-chain pins |

A signal that is always load-bearing but can never veto is **detection debt**: it consumes observation budget while depending on a human or agent noticing it in time.

## Why (the contradiction that forged it)

External contrast (Semantic Scholar MCP, 2026-08-25): snapshot tests FAIL the build on accidental tool-surface changes; SLSA attestation FAILS the release; the rate limiter BLOCKS the call. Their enforcement lives inside the artifact lifecycle, not in dashboards. Our `forge_surface_audit`, drift counts in health endpoints, and `AUDIT-drift-detector` report but cannot block — the same civilization that fails closed constitutionally fails open operationally.

## First instances

1. **Supply-chain pin gate (E-2, GATE)** — external tool installs (`npx`/`uvx`) in agent configs must be version-pinned and registered in `registries/supply_chain_pins.json`. Enforced by `scripts/supply_chain_gate.py` at the AAA pre-commit boundary. Unpinned install = commit fails.
2. **Drift-count promotion (open)** — GEOX `surface_drift.drift_count > 0` is a GATE candidate at deploy time, not a health-report line.
3. **Musyawawah NO-gate (E-3, OBSERVE_ONLY → GATE pending)** — F13-ratified 2026-09-08 (first real musyawawah verdict since 2026-08-11 protocol-birth, 26 days ago). Sentinel scans arifFlow ledger for T2/T3 receipts without `payload.musyawawah_reference` (pre-2026-09-08 receipts exempt under migration grace). Enforced at AAA pre-commit boundary via `scripts/musyawawah_gate.py` in `/root/A-FORGE/hooks/pre-commit-lsp-gate.sh`. Tier at commit boundary: **OBSERVE_ONLY** (advisory, no block). GATE tier is the runtime forge_shell `action_class` DENY (Phase 2 step 3, pending). Per doctrine, OBSERVE_ONLY paired with GATE = no detection debt. Set `MUSYAWARAH_STRICT=1` env to escalate commit boundary to blocking (development flag). Verdict: `musyawarah/2026-09-08-no-gate-task6/CONVERGENCE.md`. 5-scenario falsification test PASS at `scripts/test_musyawawah_gate.py`.

## Promotion rule

To promote OBSERVE_ONLY → GATE, three must hold:
1. the signal has produced at least one real catch (or a falsifiable test proves it can),
2. the blocked action is reversible via a named rollback,
3. the gate fails closed (gate-tool outage blocks, not allows).

## Non-goals

- Not every observation becomes a gate — promotion is earned by consequence, not by volume.
- Gates never bypass F13; they narrow the space where sovereign attention is required.
