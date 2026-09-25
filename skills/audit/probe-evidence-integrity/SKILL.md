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
capability_tier: fed-agent-subagent
ecology_state: WARM
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

## The second law — a reading requires a reading

Every case below assumes the probe **ran**. The parallel defect is a claim of state with **no
probe behind it at all** — fluent, specific, and indistinguishable in tone from a real finding,
because the fabrication is in the verb rather than in the number. Nothing here can be caught by
re-reading the value, since there is no value.

- **Observation fabrication** — "I probed X and found Y" when no call was issued. The tell is
  that you cannot name the command or its response. Rule: **a reading requires a tool call in
  this session.** Did not run it → the state is `NOT_PROBED`, and if the answer matters, probe
  now rather than narrating a plausible result.
- **Self-knowledge fabrication** — describing your own runtime (which model, which provider, the
  fallback chain, spend, routing order) from inference rather than from the runtime context
  actually injected into the session. This is the seductive one: it feels like introspection and
  arrives complete. Rule: **the injected runtime block is the only admissible source for claims
  about your own configuration.** Anything reconstructed is inference and must be labelled
  `INFERRED` or refused.

The tell to watch for in your own output: **an answer more specific and more structured than its
evidence.** A tidy multi-rung cascade diagram, or an exact percentage, is a smell when the only
input was a two-line config block. Generated structure reads as confidence — which is precisely
why this is the fabrication that survives review. Score it `ARTIFACT` in the step-8 table, with
the probe recorded as absent.

**Repair is retraction, not correction-in-place.** Withdraw the fabricated content explicitly,
state what the real source supports, and re-answer from that source alone. Quietly emitting a
corrected-sounding version leaves the reader unable to distinguish the two — and the retraction
is the only part they can verify.

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

### 3b. Read WHY it refused — a malformed request is not an authority denial

Both come back as a refusal, and from the outside they look identical. A call rejected for a *schema*
reason — wrong parameter name, missing required argument, wrong type — has said nothing about the
caller's authority; it says the **probe** was malformed. Reporting that as enforcement is a false pass
for the gate you set out to test, because the boundary was never actually exercised.

Split them before drawing any conclusion:

1. Read the refusal's own text. A validation error names the offending field and the expected type; an
   authority denial names the actor, the missing grant, or the floor that failed.
2. Fetch the target's real parameter schema (`tools/list`) and re-issue with **well-formed** arguments.
   Never probe a protected verb with an empty `{}` and call the result a gate test.
3. Only a refusal returned to a *well-formed* request is evidence about the gate.

Measured: two calls to a seal verb returned `HOLD` when sent with empty arguments — evidence of
nothing, since a schema rejection would have produced the same `HOLD` string. Re-issued with correct
parameter names, the refusal turned substantive: a named authority class, an unverified actor, and the
specific floors that failed. The gate held both times; only the second reading could say so.

Carry the distinction into the finding — `REFUSED_BY_AUTHORITY` versus `REFUSED_BY_REQUEST_SHAPE` —
because only the first is a security property. A probe that reported the schema case as enforcement
would have certified a gate it never touched.

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

- **A delta between two readings taken in different warm states is an artifact of the state
  difference.** A cold first call returns an empty or truncated body; a warm one returns the full
  payload. Anything that replays a stored baseline against a first-call reading will report a change
  that never happened — repeatedly and with confidence. Before reporting drift, take several
  consecutive readings and compare like-with-like: if the warm readings are byte-identical, the
  flagged delta is measurement, not change. Suspect this whenever a change is reported at a regular
  interval by an automated prober that runs on its own schedule.

- **A steady reading is not a live reading.** A monitor that reads from a file on disk (a seal
  ledger, an audit log, a fingerprint snapshot) returns the last value written even when the file
  stopped being appended to hours or days ago. The five identical daily reports prove nothing about
  today — they are five identical reads of the same yesterday. **The fingerprint is the input
  artifact's mtime vs current epoch, not a comparison between successive readings.** Record
  `input_mtime`, `now - input_mtime`, and the count of records, and let the reader see that the
  monitor's view is at least `Δt` stale. If `Δt` exceeds the staleness threshold for the claim you
  want to make, the finding is `STALE` and loses decision force — the same as a service that has
  not restarted but whose data feed has. Suspect this whenever the consumer reads an artifact, the
  producer is a separate process, and the report does not state when the file was last touched.
- **A file on disk is not a file being served.** Confirm the published path, not the authored copy.
  An artifact present under an authoring directory returned 404 on every candidate URL because that
  directory was never wired into the reverse proxy — so a finding of "the published copy is stale"
  was itself false: nothing was published at all. Fetch the artifact at the URL a consumer would
  use before auditing its contents, and distinguish *absent from the served surface* from *absent*.
- **Read the comparison, not the operator printed beside it.** A machine-generated reason string can
  render a failed threshold as satisfied — a score of 0.960 reported as `>= 0.99` against a 0.99
  floor. The numbers are the evidence; the operator and the connective words came from the same code
  path that produced the failure. When a verdict's justification is generated rather than measured,
  re-check the arithmetic yourself before reporting the floor as passed.
- **A capability reachable without credentials is a surface, not yet a breach — test the boundary
  before naming it.** An unauthenticated endpoint that returns a full tool schema has exposed the
  schema; that is all it has shown. Call the operations that actually mutate state and read the
  refusal they return. Report the exposure and the enforcement separately, with the operation you
  attempted named for each.
- **A file on disk is not a reachable artifact, and the gap between them is the finding.** "Shipped"
  and "reachable by an outsider with no credentials" are two claims; audit them separately. Registry
  records, advertised remote endpoints, `.well-known` discovery documents and the literal first
  command in a quickstart are all surfaces a consumer touches, and each can be stale, stubbed, or
  absent while the code behind it is fine. Recipe: `references/public-surface-probes.md`.
- **A refusal probe without its control certifies nothing.** Refusal-only evidence reads as "nothing
  works here" — an unrelated gate, a missing credential, or a malformed request all produce the same
  refusal string. Always pair the negative probe with the accept path, or state explicitly that the
  accept path is `UNVERIFIED`. Then read the refusal's **named** reason (and grep it in source) rather
  than scoring the bare verdict.
- **A counter in a document is a claim, and its numbers about your own system are the cheapest tell
  that it was never measured.** Recount the objects it names — skills, tools, endpoints, organs, hosts —
  from live sources before weighing any finding: a count off by an order of magnitude means nothing in
  that document came from the target, so every finding is *shape-only* (a plausible class of problem) and
  must be re-derived from the machine or dropped. Same class of tell: a document whose own sections
  contradict each other (one section forbidding exactly what two others recommend) is boilerplate —
  delete the remedy list wholesale instead of adjudicating it item by item.
- **A negative read against the wrong store is a manufactured finding.** Absence is evidence
  only when you searched where the record would actually be written. Resolve the path from the
  *writer's own* declaration — its path constant, its config, the file it opens — never from
  the name that sounds right. Measured: commit receipts sought in the seal-events ledger
  returned zero hits for all seven organs, which reads as *the auto-seal never ran*; the
  writer's real target was a different ledger in the same tree, where all seven were present
  and correct. Name such a result a near-miss rather than a finding: a phantom defect consumes
  the same attention as a real one and, once reported, discounts the probes that were right.

- **A claim of completion is itself a claim that must be probed — write ≠ enforce.** When a prior session, subagent, or peer declares "fail has been updated", "config has been patched", "channel_aliases.json is now active", or any other "X is done" statement, treat the completion claim the same as any other probe-bearing claim: probe the filesystem reality independently before echoing, summarizing, or building on it. Three distinct probes are required because they verify different things: (1) file existence + content (`ls`/`cat`/`grep`) — proves the write happened; (2) consumer reference (`grep -rl` for the filename across the codebase) — proves the runtime would actually read it; (3) live service pickup (restart timestamp vs file mtime, or process env vs SOT file) — proves the runtime IS reading it. "Write ≠ enforce" is the rule; "restart reloaded" or "config hot-reload" claims fail this gate whenever the cached config pre-dates the edit. State the gap explicitly: `FILES_MODIFIED but NO_CONSUMER` is a different verdict from `FILES_MODIFIED and CONFIGURED_BUT_NOT_RELOADED`, which is different from `FULLY_RUNTIME_BOUND`. Don't collapse all three into "done". This compounds under recursive audit: when a session claims enforcement of its own claim, the second session's probe must verify the first session's claim, not just re-state it.

- **A session-narrative that summarizes a previous session's findings is itself a claim.** When the prior session writes "fail X dikunci" / "fail Y dikemaskini" / "system telah dimeteraikan" and the current session echoes that back as fact without probing, the current session has produced a narrative — not a finding. The current session's only admissible position on the prior session's claim is: `OBSERVED_AND_RECONFIRMED`, `OBSERVED_BUT_GAP_FOUND`, or `NOT_REPROBED`. State which one. Default to `NOT_REPROBED` if no fresh probe ran.

- **A probe recipe that requires the user to widen scope is a reflex defect, not a user instruction.** A `search_files` run with default exclusions on a tree containing hidden directories (`.hermes/logs`, `.hermes/pastes`, `.git/objects`, `~/.cache/...`) returns zero matches for content that is actually present in those excluded trees — and the resulting "no record" verdict reads as the agent's first answer, not a second-order nuance. Treat every absence claim as null until the probe lists which surfaces it searched AND the writer could plausibly have written there. Before declaring a name, conversation, or fact "not present in the machine," probe (1) all hidden directories under the relevant root, (2) the paste/drop/cache/log folders the gateway actually writes to, and (3) any `.gitignored` paths the user might have authored privately.

- **Receipt-stated expiry dates are unverifiable in most AI provider surfaces.** A prior-session
  receipt claiming "expires 09-29, ~305K remaining" for a free-tier model is a claim about
  state at the moment that receipt was written. The provider's quota dashboard is usually
  reachable only via authenticated browser session, not API; there is no machine-readable
  endpoint that returns remaining quota + expiry for most free-tier models. Re-probing the
  endpoint proves whether the model is still drawable; it does NOT prove the expiry or
  remaining count stated in a prior receipt. Treat any pasted "X days remaining" or "expires
  YYYY-MM-DD" claim as unverified when it comes from a prior receipt, and never let it become
  the premise for a binary decision. Probe the live endpoint instead, then state what you
  observed without inheriting the receipt's time-bound claim.

- **A documented path shape is not the only path shape that works; probe each, do not inherit.**
  Provider endpoints often accept two or more payload shapes for the same verb (e.g. Cohere
  vs native, REST vs compatible-mode). A prior receipt may state "Cohere-shape OR native
  both work" when in fact only one does — and the error from the rejected shape often masks
  itself as a path/URL error rather than a payload-shape error, because the gateway sees the
  wrong key first. Always issue a cheap probe with each candidate shape and compare HTTP
  status AND response body shape before naming the working surface; never re-state a prior
  receipt's claim about which shape works without a live re-confirm.

## Reference files

- `references/mcp-probe-lifecycle.md` — MCP-specific recipe: lifecycle sequence, authenticated
  session probe, version-negotiation discriminator, fleet version matrix.
- `references/public-surface-probes.md` — Unauthenticated probes of a platform's *public* surfaces:
  registry records and cross-record drift, whether an advertised remote is a real protocol endpoint,
  discovery documents, identity-enforcement probes (negative probe + positive control), and
  reconciling the same count stated on several public surfaces.
- `references/ai-provider-endpoint-probes.md` — Probe recipe for AI provider endpoints
  (embeddings, rerank, generation). Covers path-vs-payload shape disambiguation, dashboard-vs-
  drawable capability checks, expiry-claim verification limits, and the shape of a probe matrix
  that scales across candidate shapes without burning the free-tier quota.
