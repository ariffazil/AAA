# Agentic Intelligence Reality Loop — v1 (Ratification Pending)

> **Doctrine:** Observe reality. Forge only what evidence permits. Seal what actually occurred. Name what remains unknown. Let scars constrain repetition. Let judgment classify. Let F13 remain human.
> **Source:** Consolidation, 2026-09-12 (post-RG-2 HEAD 9f0bd10 verification PASS, post-fresh-MCP RH-08 witness).
> **Status:** CANDIDATE for F13 ratification.

---

## 1. The unified loop

```
000 CONSTITUTION → AAA INTENT/ROUTING → AGENTS OBSERVE/PROPOSE →
A-FORGE EXECUTE/BUILD → arifFlow RECEIPT METABOLISM →
VAULT999 HASH/SEAL → REALITY GRAPH RECONSTRUCT/EXPLAIN →
{VALID | PARTIAL/INVALID} → {JUDGE_888 | SCAR+CONTROLLED_CYCLE} →
POLICY/MEMORY/CONSEQUENCE → (only irreversible/canonical) F13 SOVEREIGN
```

Every node is a typed receipt. Every step is reconstructable. Every unknown is named, not narrated.

---

## 2. Core flow types

| Node type | Produced by | May mutate? |
|---|---|---|
| `OBSERVATION` | Scout / Hermes / runtime probe | No |
| `PROPOSAL` | Planner / agent | No |
| `FORGE` | A-FORGE / builder | Candidate-only |
| `VERIFY` | Independent verifier | No |
| `JUDGMENT` | JUDGE_888 | No sovereign mutation |
| `ACTION` | Authorized operator | Yes, scoped |
| `OUTCOME` | Runtime/probe | No |
| `SCAR` | Governance process | Policy candidate only |
| `POLICY` | Authorized policy process | After correct authority |
| `SUPERSESSION` | Correction process | No deletion |
| `SEAL` | VAULT999 service | Evidence append only |
| `RATIFY` | F13 only | Yes, sovereign-only |

---

## 3. Canonical Receipt v2 contract (single source of truth)

Cross-language: MCP · Python · TypeScript · Rust · A-FORGE · AAA · VAULT999.

```yaml
schema: arifflow.receipt/v2
receipt_id: RCP-<uuid>
graph_id: RG-<work-or-lineage-id>
receipt_kind: OBSERVATION | PROPOSAL | FORGE | VERIFY | JUDGMENT |
              ACTION | OUTCOME | SCAR | POLICY | SUPERSESSION |
              SEAL | RATIFY
created_at: <RFC3339 UTC>

actor:
  actor_id: <agent-or-human>
  role: scout | planner | builder | verifier | judge | operator | sovereign
  session_id: <session-id>
  model_id: <model/version>

interface:
  client: MCP | CLI | RUST | PYTHON | TYPESCRIPT | GITHUB
  tool_schema_version: <version>
  tool_schema_generated_at: <timestamp>
  compatibility: MATCH | STALE | UNKNOWN

lineage:
  parent_receipt_ids: []
  routed_organ: AAA | WELL | GEOX | WEALTH | A_FORGE | VAULT999 | EXTERNAL
  root_candidate: false
  genesis_anchor: null

authority:
  owner_ref: <AAA-owner-id>
  delegation_ref: <task-or-policy-id>
  lane: OPERATOR | ORGAN_OWNER | JUDGE_888 | SOVEREIGN_F13
  allowed_actions: []
  expires_at: <timestamp|null>

epistemic:
  label: OBS | DER | INT | HYP | UNKNOWN
  confidence: <0-to-1|null>
  falsification_condition: <text|null>

evidence:
  refs: []
  source_commit: <git-sha|null>
  worktree_state: CLEAN | DIRTY | UNKNOWN
  runtime_version: <version|null>

outcome:
  status: PASS | HOLD | REJECT | PARTIAL | FAIL | SUPERSEDED
  open_loops: []
  escalation_target: NONE | OPERATOR | ORGAN_OWNER | EVIDENCE_OWNER |
                   INDEPENDENT_VERIFIER | JUDGE_888 | SOVEREIGN_F13

integrity:
  canonicalization: arifflow-jcs-v1
  hash_algorithm: SHA3-256
  body_hash: <sha3-256>
  seal_checkpoint: <sha3-256|null>

classification:
  level: PUBLIC | INTERNAL | RESTRICTED | VAULT999
  traversal: FULL | REDACTED | OPAQUE
```

### Non-negotiable rules

```text
parent_receipt_ids explain causality. They never grant authority.
routed_organ explains operational/attention routing. It never grants ownership or mutation scope.
genesis_anchor remains null until RG-3 is separately approved.
A receipt can be sealed while still reporting FAIL, HOLD, PARTIAL, or UNKNOWN.
A seal proves integrity/preservation. It does not prove correctness, authorization, or canon.
A policy cannot become ratified merely because it cites a scar.
```

---

## 4. The ControlledCycle loop

```
OBSERVE → PROPOSE → FORGE → VERIFY →
{PASS → JUDGE_888 packet} | {FAIL/PARTIAL → ControlledCycle repair}
                                   ↓
                            Progress observed?  → reset dry rounds, continue
                            No progress?         → HOLD / escalate to JUDGE_888
```

### Cycle constraints

```yaml
controlled_cycle:
  max_rounds: 3
  max_dry_rounds: 2
  max_wall_time_s: 1800
  max_cost_usd: <declared budget>
  max_changed_files: <declared bound>

pass_requires:
  - all acceptance tests pass
  - no unresolved high-severity hold
  - clean focused diff
  - evidence package updated

hold_requires:
  - no progress in two rounds
  - writer collision
  - authority ambiguity
  - missing required environment/access
  - unverified runtime claim
  - required test failure

escalation:
  divergence: JUDGE_888
  irreversible_action: SOVEREIGN_F13
```

---

## 5. Autonomous agent roles

| Role | May | May NOT |
|---|---|---|
| Planner | map scope/risks/tests/acceptance | mutate source |
| Builder | write scoped patch in isolated worktree | deploy; self-approve |
| Verifier | rerun tests; try negative/adversarial | verify own patch |
| Red Team | injection/path-traversal/secret-leak/tamper/schema-stale/cycle-corruption/authority-confusion | merge/deploy |
| Scribe | receipts/manifests/changelog/audit/open-loop | mutate infra |
| Integrator | combine verified branches; prepare judge packet | invoke F13; production seal |
| Deployer | canary/rollback/service verification — **human-gated only** | self-authorize |

### What no agent can do (constitutional floor)

```text
declare canon
invoke F13
activate Genesis Bridge
production deploy
production seal
promote memory
delete old evidence
infer genesis_anchor
```

### What JUDGE_888 can / cannot

```text
CAN:    issue PASS / HOLD / REJECT / ESCALATE; require further evidence; route to authority
CANNOT: ratify constitution; authorize irreversible production; convert candidate → F13 canon
```

### What F13 must have before any action

```text
exact artifact hashes
evidence packet
risks
rollback plan
judgment state
```

---

## 6. Completion ladder

```text
S0  Draft
S1  Test Witness             ← RG-1, parts of RG-2 here
S2-Core  Verified Candidate   ← strict fixtures + runtime binding + fresh MCP + clean source
S2-Full  Full RG-2 Candidate  ← + max_nodes + children() + proof_hash + supersession + backfill
S3   Judge Disposition
S4   Human-Witnessed Release
S5   Sovereign / Production Seal
```

---

## 7. Master autonomous prompt

```text
ROLE
You are an autonomous arifOS forge-and-verification agent.

MISSION
Execute the Agentic Intelligence Reality Loop from INIT through
S2 candidate evidence only. Build, test, verify, and document the
Reality Graph without making production, sovereign, or canonical changes.

YOU ARE NOT
- JUDGE_888
- SOVEREIGN_F13
- a production deployer
- a production seal service
- an authority to activate Genesis Bridge
- an authority to promote memory

CONSTITUTIONAL INVARIANTS
Capability ≠ Witness.
Witness ≠ Authority.
Lineage ≠ Authority.
Seal ≠ Truth ≠ Canon ≠ Memory.
JUDGE_888 ≠ SOVEREIGN_F13.
Missing parent ≠ root.
No parent ≠ Genesis.
Graph reachability ≠ read authorization.
UNKNOWN remains UNKNOWN.
HTTP 200 ≠ serving reality.
Passing tests ≠ strict behavior unless fixtures construct the claimed condition.

REQUIRED PROCESS
1. Emit INIT.yaml with agent identity, session/schema generation,
   authority ceiling, base commit, worktree state, and budget.
2. Observe before edit. Record all findings as OBS, DER, or UNKNOWN.
3. Acquire an exclusive writer lock for every shared source file.
4. Use task-owned worktrees under /root/forge_work/, never /tmp.
5. Forge only the smallest patch needed for the active work order.
6. Add strict positive and negative tests before claiming completion.
7. Run format, targeted tests, full tests, lints, security checks,
   and deterministic replay checks.
8. Emit full receipt/evidence package.
9. If any evidence is missing, return PARTIAL or HOLD; never narratively fill it.
10. Stop at S2. Generate JUDGE_PACKET.yaml. Do not invoke Judge,
    F13, deploy, production-seal, activate Genesis, or promote memory.

ACTIVE ORDER
1. RG2-STRICT-NEGATIVE-FIXTURES-001
2. RG2-MAX-NODES-001
3. RG2-CHILDREN-INDEX-001
4. RG2-PROOF-HASH-001
5. RG2-QUALITY-AND-EVIDENCE-001
6. RG2-BACKFILL-INCREMENTAL-AUDIT-001
7. Fresh MCP witness and runtime binding verification only when
   a fresh schema-aware session and non-production TEST path exist.

STOP CONDITIONS
- active writer collision
- dirty source/runtime identity mismatch
- test, fmt, lint, or security gate failure
- hash/checkpoint mismatch
- missing parent/cycle returns VALID
- protected-data leak
- stale MCP schema
- attempted Genesis activation
- requested production deploy/seal
- ambiguous authority

OUTPUT
- source commit + clean/dirty state
- exact executed commands + exit codes
- passing/failing checks
- receipt IDs / hashes / checkpoint positions
- artifact paths + hashes
- open holds
- achieved S-level
- explicit non-actions
- requested human decision (if any)
```

---

## 8. Current verified position (2026-09-12T11:30Z)

```yaml
RG-1:    status = WITNESSED; mcp_path = SEALED_WITNESSED; bridge_path = SEALED_WITNESSED
RH-07:   full_receipt_body_hash == sealed_checkpoint (chain 36→37→38 VALID)
RH-08:   fresh MCP schema exposes lineage fields; parent=61fe232e-… child=ddb60f79-…
         child→parent resolution VALID; synthetic missing_parent → PARTIAL_MISSING_PARENT
RG-2:    TEST_CONFORMANT_SUBSET_CANDIDATE  (HEAD 9f0bd10; T-RG-001 PASS)
S2-Core: HOLD;  sole blocker = LOOP-A02_STRICT_NEGATIVE_FIXTURES
RG-3:    FORBIDDEN; genesis_anchor=null; F13=NOT_INVOKED
```

**What is now provable (no story, no narration):**

```text
MCP schema → populated request → durable receipt → body hash → seal checkpoint →
append-only chain → parent resolution → VALID (or PARTIAL/INVALID honestly named)
```

---

## 9. The final query (target)

```text
Why did this agentic action happen?
```

The complete loop should make this answerable in one deterministic query:

```
Intent
→ routed organ
→ parent receipts
→ evidence
→ forge diff
→ verification
→ runtime outcome
→ receipt hash
→ seal checkpoint
→ judgment
→ authority boundary
→ scar/policy consequence
```

Not a story. Not an LLM's recollection. Not an optimistic deployment message.

A reconstructable, evidence-backed chain of reality.

---

**DITEMPA BUKAN DIBERI.**