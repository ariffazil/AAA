---
id: forge-execution-governance
name: forge-execution-governance
description: >
  Use when checking whether a service is actually governed, not just alive — verify services enforce their gates.
version: 1.0.0
owner: AAA
risk_tier: medium
autonomy_tier: T1
triggers:
  - "is this governed"
  - "alive but not governed"
  - "verify governance surface"
  - "tool registration check"
  - "immutable file"
  - "monotonicity"
  - "rollback scope"
---

# forge-execution-governance

## Core Principle

$$
\text{alive} \neq \text{governed}
$$

A service returning HTTP 200 on /health is liveness. Governance is whether that service's actions pass through the constitutional control plane (arifOS judge, lease validation, receipt emission, revocation check). These are independent properties.

## Verification Protocol

### 1. Health ≠ Governance

After confirming a service is alive, verify governance separately:

| Check | What it proves | How to verify |
|-------|---------------|---------------|
| Health endpoint 200 | Liveness | `curl :PORT/health` |
| tools/list returns tools | Tool surface exists | MCP tools/list call |
| **The tool can actually be CALLED** | The call path is open | **Call it** — not just list it |
| Tools pass FloorEnforcer | Governance enforcement | Tool execution with authority check |
| Receipts emitted | Audit trail | arifFlow receipt query |
| Revocation check works | Stop capability | Test revoke + verify denial |

A bridge can be alive (200), have tools listed, but NOT pass through FloorEnforcer. That is alive-but-not-governed.

### 1a. Listing is not calling — gates are layered, and each rejects separately

Registration, listing, and service are **three independent gates**. A tool can be
registered in code, present in `tools/list`, and still be rejected at call time by a
*separate* transport gate — a stateless whitelist, a session/ownership requirement, a
scope filter. The health endpoint stays green throughout, because the gate is working
as designed.

**Consequence:** a measurement, loop, or monitor that depends on that tool reads a
clean zero and concludes "nothing to report", while in truth it can never report
anything. **A structural zero is not a measurement.**

Probe order when a tool is expected to be usable:

```bash
# 1. Is it in the listing?          → proves registration only
tools/list | grep <name>

# 2. Can it be CALLED?             → proves the call path is open
tools/call <name> {minimal-args}
#   SESSION_REQUIRED / whitelist rejection = the tool is unreachable in this mode

# 3. Does the result mean anything? → proves the instrument works
#   Feed a known-non-empty input. If it still returns empty, it is a dead instrument.
```

Two sibling failure modes with the same signature (green light, empty result):

| Mode | Symptom | Check |
|---|---|---|
| **Registered but not served** | Listed, but every call rejected by a sibling gate | Call it; read the rejection envelope's gate name |
| **Field-name drift** | Reader reads a field the writer never emits; window structurally empty, status `OK` | Print one stored record's raw keys; grep the reader for the key it reads |

**Rule:** before reporting zero / empty / `NO_CHANGE` from any governed surface, prove the
instrument **can** return non-zero. Report **UNMEASURABLE**, not zero, when it cannot. An
instrument that reports "all clear" while incapable of saying anything else is consumed as
evidence — every inference built on it inherits the false negative, and nothing in its
output ever contradicts it.

### 1c. Consumption control — a parser is an instrument too

The same rule applies to any **parser, importer, or indexer** that feeds an analysis: prove it
consumed its whole input before trusting anything downstream of it.

```bash
# 1. count records the parser MATCHED
# 2. count records the parser REJECTED (lines with a plausible shape it skipped)
# 3. compare against the raw line count
wc -l <input>
```

A parse that silently drops a large fraction of its input still produces a complete-looking output:
plausible record counts, a plausible date range, a plausible summary. **Nothing in the output
announces the loss.** The failure is worse than a crash because every downstream metric — totals,
gaps, rates, timelines — is computed over the surviving subset and inherits the bias silently.

Two controls, both cheap:

- **Validating vs. non-validating parse, compared.** Run a permissive parser and a validating one;
  a large disagreement means the validating one is discarding records, not that the input is dirty.
- **Input-consumption ratio.** `matched / raw_lines` should be explainable. In a well-formed export
  it sits near 1 modulo wrapped continuation lines; a ratio of 0.6 means 40% of the evidence is
  gone, and every count reported from it is wrong in an unknown direction.

**Locale/format assumptions are the classic silent discarder.** Timestamps, decimal separators, unit
suffixes, D/M vs M/D — an assumption that is wrong in one field can invalidate a whole column while
the rest of the parse succeeds. Detect the format from the data (e.g. if any first-field value
exceeds 12, the field cannot be a month) and assert it explicitly rather than defaulting.

**Sanity-check outputs against themselves.** Internal contradictions reveal parse artefacts cheaply:
a series whose first dated entry precedes the file's own start date, a duplicate record at a boundary,
a gap far larger than anything else in the series. Treat an impossible value as an instrument fault
until proven otherwise — the natural instinct is to read it as a finding, and that instinct is what
manufactures phantom events.

### 1b. Enumerate the bypass paths before trusting any gate

Coverage is a property of the **boundary**, not of the gate. List every path by which a capable
process can reach protected state, then measure which of them actually pass through the control
plane. Read-only — never test a live protected path by writing to it.

```bash
id; grep -E 'Seccomp|NoNewPrivs' /proc/self/status; findmnt -no OPTIONS /   # ambient capability
for d in <protected dirs>; do test -w "$d" && echo "WRITABLE $d"; done
lsattr -d <dir>   # lowercase i = immutable; uppercase I = htree indexing, NOT immutability
ls /etc/ld.so.preload 2>/dev/null; systemctl is-active auditd; auditctl -l # kernel-level monitor?
for r in <repos>; do ls "$r/.git/hooks" | grep -v sample; done             # which trees have hooks
```

Paths that routinely sit outside a governed tool surface: the agent's native shell, its own file
writer / editor tool, `git commit`, `ssh` to a peer host, `cron`, and raw shell redirection.
Report the enumeration explicitly — an unlisted bypass is an unmeasured one, and "all paths
mediated" cannot be asserted from any subset. Note also which trees have **no** hook at all: the
unprotected tree is a finding, not an omission to skip.

The commit boundary is a decorator until proven otherwise: `--no-verify` skips it, and a
post-commit hook that only logs cannot block. Prove both on a **scratch repo** (print-and-exit-1
hook → commit blocked → `--no-verify` → commits anyway), never on a live one.

**Negative control, with the side effect checked.** Invoking the governed tool out-of-envelope is
only half the test — confirm on disk that the effect did not occur:

```
governed execution tool, no envelope    ->  expect HOLD / denial envelope
ls -la <the file it would have written> ->  expect: No such file
```

**A capability census can be stale in both directions.** A registry flag reading `routable: false`
while the surface answers a real call is as wrong as a phantom "healthy" — resolve capability
claims with a live call, never with the cached flag alone.

**Label the evidence path.** Artifacts written by a concurrent session, another agent, or a
parallel workstream are a *shared evidence path*: usable, but not an independent witness.
Corroboration requires two independent observation paths — the same artifact read twice is one
observation.

### 2. Immutable File Protection

Canonical identity files (SOUL.md, agent identity artifacts) may have `chattr +i` set. This is a protection boundary, not a bug.

- `lsattr <file>` — check for `i` flag
- Removing immutable protection without authorization = governed mutation violation
- Restoration: `git checkout` + `chattr +i` (if git-tracked)
- SOUL.md is often symlinked to arifOS repo — canonical source is centrally owned

**Locking a tree freezes whatever draft happens to be inside it — so the canonical copy can be the
OLDER one.** When protected trees are sealed, later and better drafts written to an unprotected
sibling directory diverge silently, and every consumer reading the canonical path gets the superseded
text. Detect it before quoting canon as authoritative:

```bash
# canonical vs working draft: mtime AND section diff
for f in <canon_path> <draft_path>; do stat -c '%y %s %n' "$f"; done
diff <canon_path> <draft_path> | grep -E '^[0-9]' | head    # hunk headers = sections that differ
# then, for each heading present in draft but absent in canon, grep it by name
```

Report the divergence by **section name** ("canon lacks the paradox section added later"), not as a
byte diff. A tree that is `+i` is not thereby up to date — immutability guarantees *integrity*, never
*currency*, and the two are routinely confused.

**Cross-read the mutation receipt against the document's own authority claim.** Where a locked tree's
writes are receipted, the receipt records how the write was attributed; the document records what it
claims to be. Compare them:

```bash
tail -3 <mutation_receipt_log>   # look at the actor / trace_id / attribution fields
```

An artifact that declares sovereign ratification while its own write receipt reads
`trace=<...unattributed>` is a **contradiction on the record**, and the receipt is the machine answer.
Report both strings verbatim — the doc's claim and the receipt's value — and let the issuer resolve
it. This is the sharpest form of §6's rule: a self-declared authority is a claim, and a receipt that
records no attributable source for the write is the measurement that contradicts it. It is also the
most honest finding an audit can produce, because it is the governance layer failing its own test
rather than a constituent failing the governance layer.

### 3. Monotonicity

In hook chains, restriction can only increase or stay same:

$$
D_{\text{effective}} = \argmax_{D_i}(\text{restriction level}(D_i))
$$

Ordering: ALLOW(0) < OBSERVE_ONLY(1) < SABAR(2) < HOLD(3) < VOID(4) < REVOKED(5)

On attempted downgrade: preserve existing maximum restriction. Never replace REVOKED/VOID with HOLD.

### 4. Rollback Scope

In degraded sandbox mode, only sandbox-contained rollback is permitted:
- Allowed: delete_created, restore_backup, restore_process_local_state
- Denied: git_revert, service_rollback, config_restore, database_rollback, external reversal

If the action requires non-sandbox rollback, the action class is not LOCAL_REVERSIBLE.

### 5. Context Loading

Hermes context files have different loading rules:

| File | Loading rule |
|------|-------------|
| SOUL.md | Always loaded from $HERMES_HOME |
| AGENTS.md | Loaded from cwd only |
| MEMORY.md | NOT auto-loaded (mem0 injection only) |
| USER.md | NOT auto-loaded (mem0 injection only) |
| CLAUDE.md | Loaded from cwd only |

### 6. Evidence Receipt ≠ Authority Receipt

A mutation can carry a flawless evidence chain — sources, dates, commit references, the reasoning
that made it correct — and still carry no record of permission. The two are separate questions and
a review that checks only the first will pass an unauthorized write.

| Question | Artifact that answers it |
|---|---|
| Is this correct? | evidence chain (sources, tests, diffs) |
| Was this permitted? | authority record (envelope, scope, issuer, objective, session, expiry) |

- **A commit body should carry both, and a missing authority chain is a finding in its own right.**
  Read the protected-path writes and ask of each: which envelope covered this, and which session
  and objective did it serve? A body with five evidenced sources and no authority reference is the
  common shape, and the correct verdict is "no authority record present" — which is *not* the same
  as "unauthorized". Absence of a record is not proof of absence of permission; report the absence
  and let the issuer answer.
- **A writer log that records a configured name records a label, not an identity.** Where a
  governance regime logs mutations, check whether the log stores a real session id and host or only
  the writer's configured name: N entries under one label are N unattributable events, and an
  artifact that self-declares one owner while the commit records a different actor cannot be
  attributed at all. Identity before action — request the identity fix before quoting such a log as
  attribution.
- **Measure coverage on the protected surface, and report it as an upper bound.** Enumerate the
  writes that touched protected paths (governance, canon, instructions, registries, identity files),
  then count how many carry envelope/scope language and how many carry a session or objective
  reference. Committed artifacts are the artifact surface only — a writer with shell access can
  change protected state without producing a commit, and those attempts never enter the
  denominator. Say "coverage of the committed surface = X", never "enforcement coverage = X".
- **Coverage is prior to prevention rate.** A gate can block every attempt it sees and still leave
  the surface open: a prevention percentage computed over gate-visible attempts is silent about
  everything that bypassed the gate, and reads as safety. Report prevention only alongside coverage
  and escape rate, and treat a prevention figure with no coverage figure as uninterpreted.
- **A "ratified" / "sealed" stamp with no receipt identifier.** When a document asserts
  ratification, look for the chain hash, seal id, or event-ledger entry its peers carry — and check
  whether that entry exists. An artifact can use the *identical* wording as a sealed sibling while
  having no receipt behind it, so absence is only measurable against a set that otherwise carries
  one. Name both the stamp and the missing identifier.
- **Absorbing a doctrine is not a grant of authority.** An incoming review, essay, or argument that
  concludes "reasoning must not be a source of authority" is itself reasoning. Acting on it because
  it is persuasive reproduces the defect it names — the agent has manufactured the very permission
  the doctrine forbids. Cite it, adopt it into the record, and still wait for an envelope that
  covers the write.

### 7. Control-Wiring Liveness — a gate must leave fresh receipts

Classify every control on four rungs before making any claim about it:

| Rung | Test | Evidence |
|---|---|---|
| **DECLARED** | named in a skill, doc, config key, or README | a grep hit |
| **REACHABLE** | the harness could invoke it now | `hooks list` / `tools/list` / a bound port |
| **FUNCTIONAL** | invoked once, returned a correct-shaped result | one live call |
| **EFFECTIVE** | invoked by the workflow it exists for, output consumed | a production invocation or downstream artifact |

**A control that is DECLARED or REACHABLE but not EFFECTIVE is the normal case — never report it as "we have X".** The trap is sharpest here because the artifact looks finished: the file exists, the
implementation is complete, the doctrine describes it as live, and nothing invokes it.

Wiring probe, in order:

```bash
# 1. Ask the HARNESS, not the filesystem.
hermes hooks list                 # the harness's own answer; "No shell hooks configured" is decisive
grep -n 'hook' ~/.hermes/config.yaml          # empty = no config-level wiring

# 2. Read candidate modules' OWN headers — gates often self-declare.
grep -rniE 'deprecated|not wired|skeleton|library only|phase 2|placeholder' <gate files>

# 3. Find the LIVE candidate, not just a candidate. Estates hold several same-named gates
#    (a deprecated one in the tool home, the live one in the repo tree).
grep -rn '<gate-name>' <config> <plugin manifests>   # which path does the harness load?
```

**The decisive test — correlate the receipt stream with the activity window.** A gate's receipts are
its only external proof of execution; a module's success message is not evidence.

```bash
ls -la <receipt_path>; wc -l <receipt_path>; tail -2 <receipt_path>
# then compare the newest receipt against how many gate-relevant calls THIS session made
```

**Rule — control liveness is proven by exactly one of two artifacts:** (a) a receipt whose
timestamp falls **inside the activity window**, or (b) a **blocked violation** — an action in the
gate's own deny class attempted and refused. A file, a config key, and a doctrine paragraph satisfy
neither. **Zero receipts across a session that made dozens of mutation-capable calls is positive
proof the gate is not on that path** — report it as measured, not as a suspicion.

**Subtract the control's own test receipts before counting.** A gate shipped with a self-test,
a benchmark, or a `__main__` block writes receipts every time anyone runs the tests — so a
non-empty receipt stream is not evidence of a live path. Filter first:

```bash
wc -l <receipt_path>
python3 -c "import json,sys,collections; \
  ev=[json.loads(l) for l in open(sys.argv[1])]; \
  ids=[e.get('details',{}).get('claim_id','') for e in ev]; \
  print('total',len(ev),'synthetic',sum(1 for i in ids if i.startswith(('TEST','G','A','T'))))" <receipt_path>
```

Worse: if the receipt payload does **not record the caller** (no session id, no process, no
pid), you cannot separate test traffic from production traffic after the fact, and the log is
permanently uninterpretable for this purpose. That is a schema defect worth reporting on its own —
**a receipt stream that cannot distinguish its own test harness from its production callers cannot
prove liveness for anything.** Fix the receipt schema before arguing about the count.

**Distinguish "not wired" from "never invoked yet".** A freshly-built, correctly-wired gate that no
workflow has exercised also shows zero receipts. Resolve by asking the harness (`hooks list`) rather
than by counting: if the harness does not list it, wiring is absent regardless of how many receipts
exist; if the harness lists it and receipts are absent, the wiring is present and unexercised. The
two have different remediations (one config entry vs. nothing) and conflating them sends the fix to
the wrong place.

**One mediated lane is not coverage.** A reference monitor can genuinely refuse an action inside
its own lane (a kernel rejecting its own seal on a precondition) while every execution lane around
it stays open. Report coverage per-lane and name the unmediated set; see §1b and §6. This is also
where the honest verdict shape matters: **exists-but-unwired is not the same finding as missing.**
The former is a supply problem (one config entry); the latter invites building a duplicate, which is
the most expensive mistake available in an audit-driven session. Name which one you mean.

### 8. Causal Closure — the join key first, then the terminal states

A store claimed to provide traceability fails in two independent ways. Test them in this order.

**Join key — presence before nullity.** Inspect each store's schema/keys across ALL stores: does
ANY carry a join key (`trace_id` / `correlation_id` / `objective_id` / `run_id`)? Only if present,
measure nullity, coverage, and referential integrity.

**An ABSENT join key is a different and worse defect than a NULL-populated one.** Nulls mean the
column exists and the writer is not filling it — a plumbing fix. Absence means the causal fabric was
never in the schema, so no query joins a mutation to its objective and no backfill repairs history.
Any prior "N records with trace_id=NULL" claim presumes a field: measure presence first, and if the
field is not there at all, **retract the claim explicitly** rather than repeating it.

**Hash-chaining is not causal joinability.** `prev_hash`/`chain_hash` proves tamper-evidence and
order; it says nothing about which objective an action served. A ledger can be cryptographically
sound and causally silent. Test both properties independently.

**Terminal-state distribution — closure is a property of the whole store.** Dump the status
histogram, never a sample:

```python
import json, collections
st = collections.Counter(); n = bad = 0
for line in open(path):
    n += 1
    try: d = json.loads(line)
    except Exception: bad += 1; continue
    if not isinstance(d, dict): bad += 1; continue      # mixed-type JSONL — see pitfall
    st[d.get('status') or d.get('outcome_status') or '?'] += 1
print(n, bad, st.most_common(10))
```

- **No object may remain OPEN with no expected next transition.** For every non-terminal object
  require `{owner, next_action, expected_evidence, next_check/deadline, witness, current_state}`. A
  large PENDING population with no owner and no deadline is not "in progress" — it is an unowned
  queue that silently absorbs the closure credit of the work that did finish.
- **Report the terminal fraction, not the row count.** "N records in the ledger" is uninterpreted
  without it; large stores frequently carry a majority of records with no terminal status at all.
- **A committed-but-empty store is primitive-exists, primitive-unused** — REACHABLE, not EFFECTIVE.
  Report it as evidence *for* the mechanism (already built) and *against* any claim it is operating.

**Pitfall — JSONL ledgers mix line types.** A ledger's first line may be a bare string, a header, or
a partial write while later lines are objects; a naive `json.loads` + `.get()` loop dies on line 1
(`AttributeError: 'str' object has no attribute 'get'`) and reports a false "unreadable store". Skip
non-dict lines and **report the bad-line count** — bad lines are themselves a finding (truncation,
concurrent-write interleaving) and the reason a first parse must never ground a verdict.

### 9. Audit Entry Discipline — verify the machine before the narrative

**Hostname and tailnet IP are facts; a persona header, a SOUL/AGENTS stamp, a session-context block,
or your own system prompt is a claim.** These drift silently after migrations and are exactly the
"always true" facts nobody re-checks.

```bash
hostname; cat /etc/hostname; ip -4 addr show | grep -oE 'inet [0-9.]+'   # act on THIS
tailscale status | head                                                 # node identity + peers
```

Run this FIRST, before any topology, bottleneck, or capability conclusion — an audit anchored to
the wrong host silently mis-attributes every finding to the wrong machine. When a header contradicts
the host, **retract the header explicitly in the report**; do not quietly work from the correct value
while the written record stays wrong.

**Carry a retraction ledger.** When fresh measurement contradicts an earlier claim in the same
thread — a quoted overlap figure, a record count, a field name, a host — list it as RETRACTED with
the corrected value. A claim repeated without re-measurement is the most common source of staleness,
and retracting is how the record stays usable.

## Failure Modes
| Mode | Action |
|------|--------|
| Service alive but not governed | Wire into MCP governance surface |
| Tool listed but not callable (transport gate) | Read the rejection's gate name; fix the gate or the caller — do not treat the listing as evidence |
| Instrument returns a structural zero | Report UNMEASURABLE, not zero; repair the read/write field contract before trusting any value |
| Parser/importer silently dropped part of its input | Compute matched-vs-raw ratio before quoting any count; a plausible-looking output over a partial parse inherits the bias silently in an unknown direction |
| A timestamp/format assumption invalidated one field | Detect the format from the data and assert it; a wrong locale assumption discards records without erroring, and the resulting phantom gaps read as real events |
| Immutable flag removed without auth | Restore immediately, incident report |
| Downgrade in hook chain | Preserve max restriction, log violation |
| Rollback escapes sandbox | HOLD, scope violation |
| Context file loaded when it shouldn't be | Check loading rules, adjust config |
| Mutation carries an evidence chain but no authority record | Report "no authority record present", not "unauthorized" — absence of a record is not absence of permission |
| Writer log keyed on a configured name | Unattributable: request session id + host before quoting the log as attribution |
| Prevention rate reported without coverage | Report coverage and escape rate alongside; a prevention rate alone describes only the gate's own input |
| "RATIFIED" stamp with no chain/seal id while sibling artifacts carry one | Name the stamp and the missing identifier; check the event ledger for the entry |
| Gate exists on one surface; the mutation path never reaches it | Report coverage **at the boundary** = 0 and name each unmediated path — a gate's own pass rate says nothing about it |
| Gate file present and complete, but not invoked | Check the harness's own wiring answer (`hooks list`), read the module's self-declaration, and correlate receipt freshness with the activity window — zero receipts during real activity = not on the path |
| Receipt stream looks healthy but was written by the gate's own tests | Subtract synthetic/test callers before counting; if the payload does not record the caller at all, report the schema defect — liveness is unprovable from that log |
| Control wired but unexercised vs. control unwired | Disambiguate with the harness listing, not the receipt count; the remediations differ (config entry vs. nothing) |
| Locked canonical tree quoted as authoritative | Check mtime and section-diff against the working draft; `+i` guarantees integrity, never currency — a sealed tree routinely holds the older text |
| Document declares sovereign ratification; its own write receipt reads `unattributed` | Quote both strings verbatim and report the contradiction. The receipt is the machine answer; a self-declared authority is a claim |
| Control declared REACHABLE and reported as "we have X" | The claim stops at REACHABLE; EFFECTIVE requires a production invocation with its output consumed. Report the rung by name |
| "N records with trace_id=NULL" quoted from a prior session | Test for the FIELD before the values across all stores; if no store carries a join key, retract the claim — absence is a worse defect than nulls |
| Ledger parse fails on line 1 | JSONL mixes line types; skip non-dict lines, report the bad-line count, and never ground a verdict on the first parse |
| Large store cited as proof work is tracked | Report the terminal-vs-non-terminal distribution; non-terminal objects need owner + next action + deadline, or they are an unowned queue |
| Audit anchored to a host named in a header/stamp/prompt | Verify `hostname` + tailnet IP first; a metadata header is a claim and drifts silently after migrations |
| Census flag contradicts a live call | Trust the call; re-stamp the census or record it stale. A cached negative is as wrong as a cached positive |
| Concurrent session wrote artifacts you are auditing | Grade them a shared evidence path, not an independent witness |

## References
- Cross-registry reconciliation: `references/cross-registry-reconciliation.md` — pattern for auditing multiple registries of the same entity class, finding discrepancies, and building unified heartbeat monitors
- Federation topology: FORGE-federation-manifest
- Verification: FORGE-verify-runtime
- Drift detection: ASI-drift-watch
- Hermes context loading: `hermes-agent` skill, `references/project-context-files.md` (present in the aaa-hermes profile's skill tree, not this one)