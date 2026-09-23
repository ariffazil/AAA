---
name: agent-readiness-cockpit
description: "Self-audit: live probes, sealed artifact, verdict band."
version: 1.0.0
owner: Hermes (arifOS federation)
risk_tier: medium
floor_scope: [F1, F2, F4, F7, F11]
autonomy_tier: T1
tags: [audit, self-audit, readiness, cockpit, mcp, federation, evidence-based]
capability_tier: fed-long-context
ecology_state: WARM
triggers:
  - "audit yourself"
  - "deep audit yourself"
  - "swot analysis"
  - "tell me your value"
  - "are you working"
  - "is the system alive"
  - "federation health"
  - "readiness report"
  - "what's actually running"
  - "self-assessment"
---

# Agent Readiness Cockpit

A self-audit replaces narration with runtime evidence. It is the discipline
used when the audit target is the agent itself or its federated MCP surface.

## Why this is its own skill

`live-probe-audit-pattern` governs the *general* probe-audit workflow; this
umbrella owns the *self-audit* branch where:

- the audit cannot trust the agent's own summary,
- the runtime evidence is one `ps` / `*_health` call away,
- the verdict band must be re-derivable from a sealed artifact,
- the audit must respect bounded scope (no banner replace, no A3 mutation).

## Always-on rules

1. **State bounded scope first.** No banner replace, no MCP mutate, no token
   rotate, no A3 actions inside the audit session. The post-audit verdict
   cannot authorize scope the audit itself excluded.
2. **Probe live state, not config state.** For every declared surface, hit
   the probe endpoint (`*_health`, `*_status`, `*_stats`, `*_registry_status`)
   and capture `{state, evidence_class, timestamp}`. Treat config-without-
   probe as **declared, not live**.
3. **Distinguish banner, runtime, and intent.** A startup banner showing
   `connecting` while `ps` shows the daemon alive with weeks of uptime
   means the banner lagged the runtime. Report all three surfaces.
4. **Classify boundary-enforced gates as passing.** `DB_PASSWORD required`,
   `scope denied`, etc. are **enforcement working correctly**. Report
   `state=GATED-CORRECTLY, evidence_class=boundary_test`, never `DOWN`.
5. **Persist the JSON artifact before rendering.** Path:
   `/root/.hermes/state/readiness/readiness-<ts>+0800.json`
   `sha256sum` it; print the hash in the human-facing summary.
6. **State the verdict band explicitly.** Pick from
   {GREEN, AMBER-instrumented, AMBER-speculative, RED} and name what evidence
   moves the needle. AMBER is a disciplined state, not a shame state.

## Verdict bands

| Band | Condition | Action allowed |
|---|---|---|
| **GREEN** | Live probes + deliberate gate test (A3 without F13 → HOLD) + TEVV pass baseline in same session | A2 supervised + A3 with F13 |
| **AMBER-instrumented** | Live probes confirm runtime; gate test / TEVV pending | A2 supervised + reversible only |
| **AMBER-speculative** | Only banner or config answered | A1 read-only + write HOLD |
| **RED** | Live probes error AND boundary test fails | Immediate 888 HOLD |

## Procedure

1. Open with bounded scope and the `ts` for the artifact path.
2. `ps -ef | grep -E '<expected daemons>'` for daemon baselines.
3. Issue one probe per MCP surface (serialized; do not mix local + connector
   batches in one call).
4. For each: capture `{state, evidence_class, timestamp, key_signal}`.
5. Classify external blockages (Cloudflare 403, IP-region blocks) as
   external; do not credit them against the federation.
6. Persist the JSON artifact; `sha256sum` it; keep the path stable.
7. Render the cockpit: tight header per surface, state + evidence class,
   no ASCII art, no ceremonial language.
8. Name the verdict band; what would lift it; what remains UNKNOWN.

## Pitfalls

- **Multi-tool batch only works for connector tools.** Local tools
  (`terminal`, `patch`, `read_file`, etc.) and mixed local+connector batches
  are **rejected at runtime**. Serialize local calls; batch only connectors
  when the target tool description confirms batch is supported.
- **A heuristic-uncalibrated band is honest governance, not absence.**
  `g: PATHOLOGICAL h=0.47 PHASE_1_HEURISTIC_UNCALIBRATED` is the audit
  instrument admitting it is not yet trustworthy — the right shape for a
  probe needing human review.
- **Disabled ≠ defective.** Each disabled surface carries owner, rationale,
  compensating control, risk-acceptance date, and re-enable runbook. Empty
  disabled surfaces are silent governance debt.
- **Probe counts are claims until re-derived.** "MCPs live 25/29": re-derive
  numerator and denominator via probe, not via config file.
- **Replacing the splash banner is an A3 act.** It reshapes operator-facing
  behavior; let the artifact speak first.

## Anti-patterns

- Banner-only audit. Add the process snapshot; that is the cheapest
  falsifier.
- Quoting arithmetic mean of one-time probes as evidence. A process
  snapshot taken once cannot average out a daemon that crashed mid-scan.
- Calling `PATHOLOGICAL` a defect without noting the calibration admission.
- Saving cockpit markdown without saving the JSON. The markdown is for
  humans; the JSON is the chain root.
- Mute disabled-but-no-rationale surfaces to "intentional." Convert known
  gaps into hidden ones is corruption of the readiness picture.

## Re-derivation test

> Given only the artifact path + SHA, can a future session re-run the same
> probe recipes and reproduce the same verdict band, with the same
> amendments?

If yes — the artifact is a receipt. If no — the artifact is a narrative
that happens to be JSON-shaped.

## Reference Files

- `references/readiness-cockpit-receipt.md` — Worked schema, re-derivation
  test, and re-runnable probe recipes for the artifact path.

DITEMPA BUKAN DIBERI ⚒️
