---
name: probe-evidence-integrity
description: "Use when a probe must support a claim about state."
version: 1.0.0
owner: Hermes (arifOS federation)
risk_tier: low
floor_scope: [F2, F7, F11]
autonomy_tier: T1
tags: [probe, evidence, measurement, artifact, timing, authority, negotiation]
triggers:
  - "probe shows"
  - "is it down"
  - "service was down"
  - "healthcheck says degraded"
  - "failed floors"
  - "protocol mismatch"
  - "version drift between servers"
  - "capability advertised"
  - "false advertising"
  - "nonconformant"
  - "my probe disagrees"
  - "cross-probe disagreement"
  - "all clear"
  - "verified and ready"
  - "substrate was down"
  - "measurement artifact"
---

# Probe Evidence Integrity

A probe result is not evidence until you know **it could have come out differently**. This skill
covers the failure where the probe ran, returned a value, and that value cannot bear the claim
placed on it — because of *when* it ran, *who* it ran as, *what channel* it addressed, or *what
the value means* in the document that defines it.

Applies to health probes, control/floor checks, version-negotiation probes, and any
`curl` / `systemctl` / MCP call whose output is about to become a finding.

## The core law

**A measurement answers only the question it was able to ask.** Name the question the probe
answered. If it differs from the claim, the finding is an artifact.

## Procedure

### 1. Establish the measurement window

A probe run *after* a fix cannot discriminate "was down, fixed" from "never down."

```bash
date '+%H:%M:%S %Z'
systemctl show <unit> -p ActiveEnterTimestamp -p NRestarts -p ExecMainStatus
systemctl is-active <unit>
```

Compare the probe timestamp to service start and to the claimed outage window. Settle outage
claims on the service journal (`journalctl -u <unit> --since ...`), never on a live probe alone.
When you cite a probe as evidence, state its offset from service start.

### 2. Confirm the substrate was up at assertion time

For any report declaring a system verified / ready / live:

1. Enumerate the substrates the claim rests on — the organ that **measures**, the ledger that
   **records**, the observer that **witnesses**.
2. Probe each substrate's liveness and start time.
3. Ask: was the measuring organ UP at the moment the claim was written?

A claim asserted while its verifying witness was offline is **unverified**, however correct its
numbers later prove. Keep the verdicts distinct: `BLOCKED_ON_SUBSTRATE` and
`BLOCKED_ON_KNOWLEDGE` need different next actions.

### 3. Check the probe carried authority

A health endpoint answers without credentials; a control check does not. A probe that skips
identity binding is refused by the authorization gate, and the payload it returns describes the
**probe's credential state**, not the target's health.

- `measurement not taken` ≠ `measurement failed` ≠ `measurement passed`.
- An **unmeasured** field is neither pass nor fail. Never report it as either.
- Re-probe with authority before reporting a failed control.

### 4. Attribute the channel before the fault

A config entry is a **permission, not a caller**. Read the entry's target before blaming it.
Two services on different ports legitimately carry different versions and different policies;
blaming entry-N's string on server-M manufactures a defect report for a defect that does not
exist — and "fixing" a correct entry breaks a working probe.

Corollary: a `/mcp` 404 on a health port is a **routing fact**, not an outage. An organ's API server
and its MCP server may be different ports. Confirm which port answers the handshake before
declaring a surface absent.

### 5. Capability advertised ≠ capability implemented

SDKs commonly inject extension blocks into **every** server's initialize capability set
unconditionally. Zero bindings under an advertised capability is then framework behaviour, not a
breach.

Read the framework's initialize path before asserting a spec violation. Absent a normative clause
**quoted from the spec**, classify `ADVERTISED_NO_BINDING` — observed state, intent unknown.
Never "false advertising", never "nonconformant".

### 6. Discriminate before you characterise

When behaviour could be either *negotiation* or *echo*, send a value that cannot be valid:

```
send version 9999-01-01
  echoes it back              → not negotiating; pins/echoes one value
  returns a supported version → negotiates
```

A pinned service is not broken. The finding is the **spread** across the fleet, not the pinned
member. Generalise: any probe whose result could come from "the system read my input" or "the
system has a value" needs a bogus-input control before you write the finding.

### 7. One quantity, one band table

When a document defines the same quantity under two threshold tables (a governance band and a
display/advisory band), one number yields two verdicts. Locate **every** table governing the
value, quote both, and report the contradiction with a reconciliation request. Never quote only
the band that supports the conclusion you were handed.

### 8. Classify the verdict's epistemic state

Close with what the probe actually established:

| State | Meaning |
|---|---|
| `MEASURED` | You ran it, this session, on that target, with authority |
| `UNMEASURED` | The probe could not ask the question (no credentials, wrong channel, wrong version) |
| `ARTIFACT` | A number exists but answers a different question |
| `CONTESTED` | Two sources give two values |
| `UNVERIFIED_CLAIM` | The substrate that would verify it was down at assertion time |
| `FLAKY_PRECONDITION` | Start/health gate is non-deterministic; cause unresolved |

## Pitfalls

- **A post-fix probe is not evidence of uptime.** Timestamp it against service start, or don't cite it.
- **`failed_floors: []` alongside an `unmeasured` marker is not a pass.** An unmeasured control is
  neither pass nor fail — reporting it as either is the same error with the sign flipped.
- **A valid value cannot discriminate negotiation from echo.** Both a negotiating and an echoing
  server accept a valid version; only a bogus one separates them.
- **An entry whose target you never read is not a suspect.** Read the URL first, then blame.
- **A probe that fails its own handshake has learned about itself, not the target.** Fix the probe
  before writing a finding about the service.
- **"Restarted and it came up" is not a root cause.** If a start precondition is non-deterministic,
  the honest verdict is `FLAKY_PRECONDITION` with the cause marked open. An unresolved cause is
  more useful than a guessed one. Where a restart loop had already exhausted itself, say so — the
  service would not have recovered on its own, and that changes the severity.
- **Consecutive identical probes disagreeing is signal, not flakiness.** Same user, same path, same
  minute, different result = non-determinism in the gate. Report it as the finding.
- **Don't resolve an open question to close a thread.** State the mechanism you proved; mark the
  rest unresolved.

## Reference files

- `references/mcp-probe-lifecycle.md` — MCP-specific recipe: lifecycle sequence, authenticated
  session probe, version-negotiation discriminator, fleet version matrix.
