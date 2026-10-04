# Deep Audit Delegation Pattern (6-Phase)

> Origin: 2026-08-10 arifFLOW governance audit (ARIFOS::M365_COPILOT_KERNEL::v1.1)
> Updated: 2026-08-10 after first full execution — added 11 verified pitfalls from live audit.
> Use when: spawning an auditor to do deep source-level analysis of any federation organ.
> Distinct from: forge-federation-probe (quick 7-probe health check, ~2s).
> This pattern: deep source code tracing + live endpoint probing + constitutional testing, ~minutes.

## When to Use

- Auditing a specific organ's constitutional compliance against its design
- Tracing actual execution paths through source code (not docs)
- Testing whether declared architecture matches live behavior
- Finding contradictions, drift, dead pathways, silent failures
- Pre-seal governance verification of organ behavior

## When NOT to Use

- Quick health check → use forge-federation-probe (7 probes, ~2s)
- Single-organ MCP conformance → use forge-mcp-probe / MCPJam
- Post-deploy drift check → use forge-federation-probe Phase 6
- Auditing deliverables (reports, docs) → use `audit-and-validate-deliverables`

## The 6 Phases

### Phase 1: REALITY INVENTORY
- Discover running services, ports, routes, timers, queues, stores, receipts, logs
- Read actual source code — don't trust docs
- Build evidence-backed system map
- **Separate OBSERVED from ASSUMED**
- Probe live endpoints with curl — don't assume docs describe reality
- Check systemd service status AND the actual binary path
- Run the test suite to assess code health

Output: `REALITY_MAP.md`

### Phase 2: FLOW TRACE
Trace an actual execution path through the organ:
```
SENSE → THINK → JUDGE → EXECUTE → WITNESS
```
For each transition identify:
- Actor, trigger, artifact, state mutation
- Receipt emission, rollback path, failure mode
- **Read actual code** — docs may describe intended flow, not actual
- Identify which code paths the live daemon mode actually uses vs which are only used in other modes

Output: `FLOW_TRACE.md`

### Phase 3: CONSTITUTIONAL TEST
Evaluate declared claims against live evidence:
- For each claim, design a test that could falsify it
- Run the test (probe endpoint, read code, check logs)
- Classify: support / weaken / falsify / unknown
- **Never force a SEAL**
- Specifically test: does the system fail open or closed on each error path?

Output: `CONSTITUTIONAL_AUDIT.md`

### Phase 4: BRIDGE NODE ANALYSIS
Look beyond specialist organs:
- Routing layers, translators, bridge processes
- Multi-domain components, hidden dependency hubs
- Which components behave as integration nodes vs specialists?
- Identify shared-state singletons (Arc<Mutex<>> patterns)
- Check for schema mismatches across language boundaries (Python↔Rust)

Output: `BRIDGE_NODE_REPORT.md`

### Phase 5: STRAWBERRY PRINCIPLE
Identify smallest set of components whose failure degrades federation:
- Dependency concentration (how many endpoints/features depend on it?)
- Routing centrality (is it on the critical path?)
- Witness centrality (does it produce audit evidence?)
- Governance centrality (does it enforce invariants?)
- Score each component 0-10 and rank

Output: `STRAWBERRY_ANALYSIS.md`

### Phase 6: ADVERSARIAL REVIEW
Assume current doctrine contains mistakes:
- Try to falsify federation/governance/memory/flow assumptions
- Required outcomes: support, weaken, falsify, unknown
- **Never force a SEAL**
- Specifically test the stated failure mode (fail-closed vs fail-open)

Output: `FALSIFICATION_REPORT.md`

## Final Deliverable

Compile all phases into `<ORGAN>_AUDIT_VERDICT.md`:

Sections:
1. Executive Summary
2. Observed Reality
3. Constitutional Matches
4. Constitutional Mismatches
5. Hidden Bridge Nodes
6. Critical Failure Paths
7. Strawberry Components
8. Falsified Assumptions
9. Remaining Unknowns
10. Verdict

Allowed verdicts: SEAL, PARTIAL, UNKNOWN, SABAR, HOLD, VOID

## Evidence Labeling (mandatory)

Every statement must carry one label:
- `[OBS]` — directly observed (probed, read in source, measured)
- `[DER]` — derived from OBS evidence via logical steps
- `[INT]` — interpretation (clearly marked as such)
- `[UNKNOWN]` — evidence insufficient to classify

## Delegation Template

```
delegate_task(
  goal="You are an INDEPENDENT EXECUTION AUDITOR...",
  context="
    [Organ] source: /root/<organ>/
    Key source files: [list]
    Live endpoint: http://127.0.0.1:<PORT>/health
    Governance docs: [list]
    Known bugs: [list]
    OUTPUT DIRECTORY: /root/forge_work/<organ>-audit/
    RULES: evidence-first, label [OBS]/[DER]/[INT]/[UNKNOWN], fail-closed, no architecture worship
  "
)
```

## Post-Audit Routing

Per Delegation Doctrine: T2+ results route through `arif_judge` at :8088 before integration.
The audit verdict is advisory — not a constitutional seal.

## Pitfalls (verified 2026-08-10, arifFLOW deep audit — 96 tests, 17 source modules)

### P1: Docs may be wrong
The organ's AGENTS.md or canon may describe intended behavior, not actual. Code is truth. Live endpoints are truth. Documentation is a pointer.

### P2: Tautological invariant detection
When invariant enforcement checks "does X exist?" and X doesn't exist, the invariant always passes. This is NOT enforcement — it's a tautology. In arifFLOW, 5 of 7 F0-F6 invariants (F0, F2, F4, F5, F6) were tautological — they pass because the prohibited capability doesn't exist, not because active checking catches violations. **Detection:** check if the enforcement code has a runtime probe or just an architectural assertion. If it only checks "no POST /X endpoint exists", it's tautological.

### P3: Dual measurement formula problem
When a system has legacy and v2.1 metrics measuring INVERSE properties, enforcement using one and reporting the other creates operator confusion. arifFLOW: legacy fq = execute/verify (high = bad), v2.1 quotient = verify/execute (high = good). Enforcement used legacy; /health reported v2.1. An operator seeing "OPTIMAL" on /health while the enforcer sees "STUCK" is a measurement integrity failure. **Fix:** choose one formula or explicitly document the duality.

### P4: push_force vs push pattern
When a codebase has both validated and unvalidated insertion paths, check which one the live API actually uses. arifFLOW: `ReceiptStore::push()` validates chain hashes; `push_force()` bypasses validation. The daemon's /ingest uses `push_force()`. Chain verification exists but is never exercised by live code — it's test infrastructure, not runtime infrastructure. **Detection:** trace from the HTTP handler to the storage call and check which variant is used.

### P5: Advisory vs mandatory execution gates
The /check endpoint is advisory because the system has no mechanism to ensure agents actually call it. True enforcement requires (a) mandatory proxy (all traffic goes through the gate), (b) signed receipts (gate stamps approval), or (c) network-level interception (firewall/iptables). An HTTP endpoint that agents voluntarily call is a request, not a gate. **Detection:** check if the system can detect an agent that skipped the gate.

### P6: Fail-open client defaults
When client libraries default to "allowed" on connection failure, this contradicts any "Fail-Closed" architecture claim. arifFLOW Python client: `return {"allowed": True, "reason": "arifFlow unreachable"}` on connection error. Shell client: returns exit code 2 with "proceed with caution." Both fail-open. **Detection:** grep client code for `allowed.*True` in error/except paths.

### P7: Enforcement without timer
An enforcement system that requires manual triggering via POST /enforce is not automatic. Check for timer/cron/interval-based triggering in the daemon's main loop. arifFLOW daemon's `daemon_mode()` has no `loop { sleep(interval); enforce(); }` — enforcement only runs when a human or monitoring tool calls /enforce. At audit time, cycle_count=0 despite 7h uptime. **Detection:** search the main loop for periodic enforcement.

### P8: Actor model as documentation vs runtime concept
Federation organ names (GEOX, WEALTH, WELL, HERMES) may be documentation-layer abstractions, not runtime concepts. The daemon treats all actors as opaque strings. No organ registry, no capability scoping per organ. **Detection:** check if the code has organ-specific logic or just accepts arbitrary actor_id strings.

### P9: Two-operation-mode discovery
Many Rust daemons have dual modes (pipe/stdin vs TCP). Always check if the live mode differs from the protocol mode. arifFlow: daemon mode = receipt store + invariant gate. Stdin mode = full BSP scheduler with Merkle trees, cooling ledger, Kabarkan tracer. The two modes share a library but have COMPLETELY SEPARATE STATE. Code paths exercised in one mode are dead in the other. **Detection:** check the main() dispatch and trace which state objects are used in each mode.

### P10: Schema mismatch across language boundaries
When Python and Rust share data, check type compatibility. arifFLOW: Python bridge sends `previous_receipt_id` (UUID) to `previous_receipt_hash` (expected SHA3-256 hex). The chain is ALREADY broken in practice. **Detection:** compare the Python client's field values against the Rust struct's expected types.

### P11: Mutex panic poisoning
Arc<Mutex<>> with `.lock().unwrap()` means any panic while holding the lock poisons the mutex and kills the daemon. Check for unwrap() on lock results. arifFLOW: all handlers use `.lock().unwrap()`. **Detection:** grep for `.lock().unwrap()` in daemon code.

## Worked Example Summary: arifFLOW 2026-08-10

| Phase | Key Finding | Verdict |
|-------|------------|---------|
| Reality | Daemon running, 95 receipts, 3 actors, 96 tests passing | FUNCTIONAL |
| Flow Trace | /check is read-only advisory; /ingest uses push_force; no timer enforcement | ARCHITECTURE GAP |
| Constitutional | 5/7 invariants tautological; FQ dual formulas disagree; system fails OPEN | 2 FALSIFIED, 3 WEAKENED |
| Bridge Nodes | InvariantEnforcer is 5-plane hub; Mutex panic-poisonable | 6 nodes identified |
| Strawberry | InvariantEnforcer (10/10) + ReceiptStore (8/10) = minimum critical set | 2 critical components |
| Adversarial | 5/7 assumptions falsified; fail-open contradicts fail-closed constraint | HOLD |

**Output directory:** `/root/forge_work/arifflow-audit/` (7 deliverables)
