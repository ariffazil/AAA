---
name: federation-alignment-probe
id: federation-alignment-probe
version: 1.0.0
description: "Use when a /000 INIT federation audit is requested."
owner: F13
risk_tier: high
floor_scope: [F1, F2, F4, F11, F13]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
triggers:
  - "/000 INIT federation probe"
  - "audit federation alignment"
  - "verify role split"
  - "audit-trail classification"
  - "read-only audit, classify by mutability"
  - "federation drift check"
  - "MACHINE_MAP verification"
tags: [federation, audit, read-only, F13, F2, drift, classification, role-split, gate-map]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Federation Alignment Probe — read-only audit with mutability classification

A read-only audit that proves whether declared roles match runtime behavior across a federation.
The discipline is **classify-before-mutate**: every discovered file gets a mutability class before
any mutation is even proposed. This is the only audit posture that produces an honest gate map
without breaking F2 (evidence-integrity) or F13 (sovereign authority).

**Canonical sources** (load for depth, do not inline):
- `bridge-protocol` — human-facing register for the audit report itself
- `state-transition-discipline` — the transition chain for any audit finding that requires mutation
- `authority-envelope` (AGENTS.md) — what an envelope MUST carry; the audit reports on its absence
- `handoff-contract` (core/federation) — what cross-organ envelopes must carry; audit reports on gaps
- `MACHINE_MAP.md` — the SOT for federation topology (re-probe before acting — the map ages)

## The one invariant

```
Audit-trail files are F2 evidence. Their mutability class is read-only-by-default.
A mutation that rewrites audit trail = F2 HOLD, regardless of cosmetic intent.
```

This is non-negotiable. "Tidy up NSFW mentions", "remove stale references", "clean up backups" —
none of these authorize touching F2-class files. The cosmetic cleanup is itself the failure mode the
rule catches.

## Stage 0: Witness demand check (mandatory before any probe)

Before the first tool call, anchor the audit's temporal and host context:

```
1. date '+%H:%M %Z %z'                          # temporal grounding (MANDAAT TEMPORAL)
2. hostname + ip -4 addr                        # host fingerprint (KVM8 forge vs KVM4 workshop vs KVM2 witness)
3. carry_forward.json schema + last entry       # what loops are open
4. git log -1 on /root/.hermes and /root/AAA    # what is the live HEAD vs source
```

If any of these cannot be obtained, the audit cannot honestly claim topology_visibility = full.
Mark the gap and downgrade the verdict band one level (full → partial, partial → none).

## Stage 1: Multi-probe sweep — every probe earns its keep

A federation probe must triangulate, not rely on one source. For each role claim (Hermes, OpenClaw,
AAA, arifOS, A-FORGE, coding-agent mesh, witness layer), at least THREE independent probes:

| Probe | Source class | What it proves |
|---|---|---|
| Live process | `probed` | systemd unit present? user/group? uptime? |
| Live endpoint | `probed` | health endpoint reachable? identity_hash returned? |
| Source declaration | `source-derived` | AGENTS.md / SKILL.md / SOUL.md claims |
| Git HEAD | `config-derived` | live source tree = deployed binary? |
| Cross-reference | `log-derived` | receipts / envelopes / traces name the right path? |

If all three converge → green for that role. If one diverges → mark AMBER and name the gap.
If none converge → UNKNOWN for that role, the audit cannot speak to it.

**Pitfall — single-probe overclaim.** A federation audit that reads only systemd units and reports
"clean role separation" is asserting governance posture from declarative config. Live behavior, receipt
chain, and delegation manifests may all violate what the unit file promises. The probe set must
include at least one *behavior* probe (e.g. `curl /health` returns 200, `git log` shows the right
HEAD, delegation manifest carries envelope fields).

## Stage 2: Mutability classification — every file gets a class

Before any audit proposes a mutation, sweep every discovered file and tag it with one of these
classes. The class determines whether mutation is even an option.

| Class | Examples | Mutation default | Why |
|---|---|---|---|
| **Operational / mutable** | active USER.md, SOUL.md, MEMORY.md, lanes.yaml, profile fixtures, active skill SKILL.md | yes, with F13 envelope | loads for runtime, change is the point |
| **Audit trail / immutable** | USER.md.bak-*, .hermes_history, logs/agent.log, hermes_hook_receipts.jsonl, .git/objects, VAULT999 SEALED_EVENTS, build-info.json | **NO — F2 HOLD** | evidence trail; rewrite = integrity break |
| **Cryptographic / immutable** | .curator_backups/blobs/* (sha256 hex), git packfiles, content-addressed snapshots | **NO — corruption** | touch = hash chain break |
| **Worktree / active repo** | /root/forge_work/*, /root/<repo> working tree | yes, but inside worktree only | active repo write must go to a target branch |
| **Archive / pristine** | /root/hermes_work/pristine-full/, /root/AAA/src/seed/, .archive_* | **NO — historical record** | preserves the "before" state |
| **Ephemeral / regeneratable** | cache/spillover, skills/.hub/index-cache, terminal-output logs | yes, can regenerate | low blast radius, auto-rotate |
| **User-content / private** | pastes/paste_*.txt, user-owned memory files | **NO without explicit user** | the human's content, not the agent's purview |

**Pitfall — broadcast patch across mutable copies.** When the same file (USER.md, AGENTS.md) appears
in N paths, the reflex is either patch-one-and-leave-drift or patch-all-N-and-pretend-consistency.
Both are wrong. Probe the active loader first; patch the active file; tag the rest for drift audit
without rewriting them. See `bridge-protocol` pitfall #18 — "Multi-location file ambiguity."

**Pitfall — cosmetic cleanup of audit trail is itself the failure mode.** The common request:
"sweep all NSFW mentions", "remove stale references", "tidy up backups". Whatever the cosmetic
target, the F2 rule still applies: backup snapshots, log files, .hermes_history, git objects are
immutable regardless of content. The right answer is classify, not clean.

## Stage 3: F13 binary table — present options, do not pre-decide

After classification, present the mutation options as a 2-3 row F13 binary table. Each option must
be reversible and named with its trade-off.

```
Q1: Operational files (USER.md active, profile fixtures) — patch / leave?
Q2: Audit trail (.bak-*, .hermes_history, logs/, git objects) — rewrite / leave?
Q3: User-content (pastes/, private memory) — read / leave?
```

Default answer per class:
- Q1 → YES patch (targeted, one canonical file; tag mirrors for drift, do not rewrite)
- Q2 → **NO — F2 HOLD** — leave audit trail intact; backups age out naturally
- Q3 → **NO** — user content is the human's purview; agent does not read or rewrite

**Pitfall — present the table, do not collapse.** A reflex to "I'll patch operational files only,
leave everything else" is the agent deciding for F13. F13 decides. The table is the
decision-shape, not a polite wrapper for the agent's pre-chosen answer. The agent may recommend
with reasoning; the human approves.

## Stage 4: Propose → inspect → resolve scope → show diff → F13 approves → mutate → verify → receipt

Any audit finding that requires mutation must follow this exact sequence. Reversed or compressed
sequences are governance-rotten even when the mutation itself is reversible.

| Step | Required artifact | Failure mode if skipped |
|---|---|---|
| Propose | exact file paths + intent | vague instruction → drift |
| Inspect | load target + check live loader + check git HEAD | patch wrong file → invisible mutation |
| Resolve scope | confirm targeted vs broadcast, one canonical vs N copies | broadcast patch → drift amplifier |
| Show diff | `git diff` or proposed patch text | mutation before approval = unratified |
| F13 approves | explicit binary in conversation, with payload hash binding | unratified mutation |
| Mutate once | single commit, single scope, one canonical target | multi-mutation race |
| Verify | git log / curl / loader check post-mutate | unverified mutation |
| Receipt | trace_id + session_id + envelope_id + parent_trace_id | orphan mutation |

**Pitfall — receipt after commit, not before.** An audit tool that emits a `flow_ingest` receipt
*after* the commit, with the trace_id carried by the same agent that did the commit, is not
causally binding. The receipt attests to an event that already happened. The right sequence:
mint trace_id from parent objective → stamp before mutation → emit receipt only after verify.
See `state-transition-discipline` §"PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED".

## Stage 5: Probe-set reconcile across parallel audits

When multiple agents audit concurrently (e.g. probe-agent sandbox + main session), their
reports may differ. Reconciliation, not echo-detection:

1. **Convergent findings** = the probes agree → state once, cite both probes' evidence_refs
2. **Divergent findings** = the probes disagree → name both, run a third probe to break the tie,
   or mark UNKNOWN with both claims preserved
3. **Echo findings** = one probe's findings match the other probe's output character-for-character
   → suspect that one probe read the other's transcript → mark as LOW-CONFIDENCE independent
   witness; the probe may still be true, but the witness is not independent

**Pitfall — claim independent witness when probe is actually echo.** Two probes that both read the
same `.git/objects` directory and both report "deployed commit 4b4c7c89d" are NOT independent
witnesses — they share evidence. The audit's claim of "triple-verified" is decorative if all three
probes read the same surface. Independence requires different evidence paths (live endpoint vs
git HEAD vs running process vs source declaration).

## Stage 6: Honest gate map — what the audit can and cannot claim

The report ends with the five-class closeout:

1. **What the system can truthfully claim now** — green facts, named with evidence_ref
2. **What it must not claim yet** — UNKNOWN / PARTIAL / unratified claims, with the gap named
3. **The single next read-only test** — one specific command, not a menu
4. **Every required 888 HOLD** — explicit list, not embedded in conclusions
5. **HONEST GATE MAP + RECOMMENDATIONS** — verdict band (GREEN / AMBER / RED / UNKNOWN) with
   the five highest-confidence facts, five highest-risk unknowns, and the F13 binary items
   the agent will NOT decide alone

**Pitfall — present the gate map, do not narrate the audit process.** The human does not want
"I first verified the host, then I checked X, then I checked Y…" — they want the map. Process
narration is the agent managing its own register; the report's gate map is the load-bearing
artifact. See `bridge-protocol` pitfall "No meta-narration of internal process."

## Verdict band rubric

| Band | When |
|---|---|
| **GREEN** | every probed role has full convergence (3+ independent probes agree), no audit-trail drift, F13 chain intact |
| **AMBER** | role separation declared correctly but live behavior has gaps (hook WITNESSES-only, missing envelope fields, schema drift), or audit-trail drift is acknowledged but not yet remediated |
| **RED** | role separation declared AND live behavior both broken, OR audit-trail integrity violated, OR F13 envelope chain unprovable |
| **UNKNOWN** | topology or runtime visibility insufficient to verdict (probes failed, schema not found, hosts unreachable) |

Most real audits land on AMBER. GREEN means the federation has been recently aligned and tested.
UNKNOWN means the audit was under-specified for the scope. RED means immediate F13 envelope
required before any further mutation.

## Pitfalls (imperative)

- **Don't mutate anything during the audit.** Read-only means read-only. The audit may *propose*
  mutations; it may not execute them. The proposal goes to the F13 binary table, not to disk.
- **Don't claim "clean role separation" from declarative config alone.** Unit files are evidence
  the role is *claimed*, not evidence it is *enforced*. Live behavior, receipt chain, and
  delegation manifests are the enforcement proof.
- **Don't echo one probe's findings into another's report.** If the audit runs multiple
  probes in parallel, name which probe produced each fact. Echo-stacked reports claim
  triple-verification without independent witnesses — that is decoration, not discipline.
- **Don't rewrite audit-trail files for cosmetic reasons.** Backups, logs, history SQLite,
  git objects, content-addressed blobs are F2 HOLD. Classify and leave; the cleanup is the
  failure mode, not the recovery.
- **Don't pre-decide the F13 binary.** Present 2-3 options with explicit trade-offs. The agent
  may recommend; F13 decides. See `bridge-protocol` pitfall #17 "Boundary negotiation under
  pressure".
- **Don't compress the audit's transition chain.** Propose → inspect → resolve scope → show diff
  → F13 approves → mutate → verify → receipt. Any compression (e.g. mutate before show diff, or
  receipt before commit) is governance-rotten even when the mutation itself is harmless.

## Support files

- `references/mutability-classification.md` — extended table with concrete path examples per
  class, plus a worked example of the Q1/Q2/Q3 F13 binary table for USER.md-style files.

DITEMPA BUKAN DIBERI ⚒️