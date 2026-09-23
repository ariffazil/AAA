# Readiness Cockpit Receipt — Self-Audit Pattern

## When this applies

The audit target is the agent itself. The audit cannot rely on the agent's own
narrative summary. Two failure shapes recur:

1. **Banner-only audit** — advisors read the startup banner, conclude the system
   is unproven or fictional, missing that runtime evidence is one `ps`/`/health`
   call away.
2. **Narrative escalation** — the agent produces a sales-pitch markdown audit
   that has the tone of rigor but no reproducible probe.

The readiness cockpit is the in-between: prove the runtime live, seal a
re-derivable artifact, name the verdict band, stop.

## Procedure (night-tonight minimal)

1. **Open with bounded scope.** What you will not touch: no banner replace, no
   MCP config mutation, no token rotation, no A3 actions. The post-audit
   verdict cannot authorize scope the audit itself excluded.
2. **Snapshot local processes first.** One `ps` listing captures daemon
   liveness independent of MCP endpoints. Persist as a baseline.
3. **Probe each surface via its own health/status/stats tool.** Capture
   `{state, evidence_class, timestamp}` per surface. The shape matters more
   than the number: distinguish `live_probe` / `boundary_test` /
   `config-derived` / `inferred`.
4. **Classify blocked probes correctly.** Boundary-enforced gates (DB_PASSWORD
   required, scope deny) are **passing** findings. Cloudflare 403 on a third
   party is external, not internal. Never report these as DOWN.
5. **Distinguish disabled intentional from disabled neglected.** Every disabled
   surface carries owner, rationale, compensating control, risk-acceptance
   date, and re-enable runbook. Empty disabled surfaces are silent
   governance debt; report them as `disabled_intentional_owner_undeclared`
   rather than `disabled_ok`.
6. **Persist the JSON artifact before rendering the summary.** Use a stable
   path with timestamp:
   `/root/.hermes/state/readiness/readiness-<ts>+0800.json`
   The path is the contract; future sessions must re-derive the verdict from
   the path, not from this transcript.
7. **Compute and print SHA-256 of the artifact.** The hash is what makes
   "did the artifact move?" checkable later. Without it the receipt is
   ungroundable.
8. **Render a tight cockpit, not a decoration.** Header lines per surface
   with state + evidence class. No ASCII art. No ceremonial language. The
   point is *re-derivation in 60 seconds*, not theater.

## Verdict band discipline

| Band | Means | Action allowed |
|---|---|---|
| **GREEN** | Live probes + deliberate gate-test (A3 without F13 → HOLD) + TEVV pass baseline all in same session | A2 supervised + A3 with F13 |
| **AMBER-instrumented** | Live probes confirm runtime; gate test / TEVV pending | A2 supervised + reversible only |
| **AMBER-speculative** | Only banner or config answered | A1 read-only + write HOLD |
| **RED** | Live probes error AND boundary test fails | Immediate 888 HOLD, do not proceed |

AMBER is a disciplined state, not a shame state — keep it that way by naming
what evidence moves the needle.

## Common mistakes

- **Reporting "all MCPs connecting" without `ps` corroboration.** Add the
  process snapshot; that is the cheapest falsifier.
- **Quoting the arithmetic mean of multiple probes as evidence.** A process
  snapshot taken once cannot average out a daemon that crashed mid-scan.
  Re-probe before publishing.
- **Calling a heuristic-uncalibrated band "PATHOLOGICAL" without noting it
  is the audit instrument admitting it is untrustworthy.** That admission is
  the *correct* shape for a probe that needs human review, not a defect.
- **Producing a SHA without verifying the artifact on disk is the hash.** A
  SHA printed by an unwitnessed runner is a claim, not a witness.
- **Saving the cockpit markdown without saving the JSON.** The markdown is
  for humans; the JSON is the chain root. Always write both.

## Anti-patterns

- **Don't** replace the splash banner in the same session as the audit. That
  re-shapes operator-facing behavior; let the artifact speak first.
- **Don't** mute disabled-but-no-rationale surfaces to "intentional." That
  converts a known gap into a hidden one.
- **Don't** batch local tool calls with connector tool calls. The runtime
  rejects mixed batches; serialize locals, batch only connectors.
- **Don't** extrapolate from this one session's probes to a global "Hermes
  has X% value" verdict. AMBER-instrumented is per-evidence, not absolute.

## Re-derivation test

For any readiness report, the re-derivation test is:

> Given only the artifact path + SHA, can a future session re-run the same
> probe recipes and reproduce the same verdict band, with the same
> amendments?

If yes — the artifact is a receipt. If no — the artifact is a narrative
that happens to be JSON-shaped.

## Worked schema (minimal)

```json
{
  "epoch": "2026-09-23T21:41:51+08:00",
  "evidence_mode": "LIVE-PROBE / READ-ONLY",
  "source_commit": "3093f38b",
  "upstream_commit": "2ed6387d",
  "carried_patches": 17,
  "policy": {
    "kernel": "APEX-ZEN",
    "state": "ENFORCED|UNKNOWN|RED",
    "evidence": "...",
    "calibration": "..."
  },
  "mcp_mesh": {
    "configured_count": 29,
    "live_probed_this_session": 13,
    "probes_outcome": {
      "<surface>": {"state": "...", "evidence_class": "..."}
    },
    "disabled_intentional": ["...", "..."]
  },
  "write_authority": {
    "f13_bound": true,
    "enforcement_evidence_class": "structural|live_test|p",
    "deliberate_block_test_pending": true
  },
  "audit_chain": {
    "claim_ledger_state": "...",
    "last_valid_seal_receipt_id": "..."
  },
  "tevv": {
    "corpus_init": "NOT-STARTED|READY",
    "baseline": "UNKNOWN|READY"
  },
  "operational_verdict": "AMBER-instrumented",
  "operational_verdict_basis": "...",
  "amendments_to_prior_audit": ["..."],
  "what_remains_UNKNOWN": ["..."]
}
```

Each non-trivial claim lives in `probes_outcome`. The verdict band is a
*single field*, not a paragraph — band changes are diffs over the artifact,
not narrative drift.
