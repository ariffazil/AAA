---
name: federation-constitutional-audit
description: "Deep constitutional audit of any arifOS federation organ — 6-phase adversarial methodology comparing declared design against runtime behavior. Covers Reality Inventory, Flow Trace, Constitutional Test, Bridge Node Analysis, Strawberry Principle, and Adversarial Review. Spawns independent execution auditor via OpenCode/Codex/Claude-Code with epistemic labeling discipline. Use when: 'audit arifFlow', 'deep audit of organ X', 'constitutional probe of Y', 'does X match its design', 'find drift in Z', or any comprehensive organ-level verification that goes beyond the quick7-probe forge-federation-probe."
version: 1.0.0
---

# Federation Constitutional Audit — 6-Phase Adversarial Methodology

> **Forged:** 2026-08-10 from Arif's sovereign directive auditing arifFLOW.
> **Distinct from:** `forge-federation-probe` (quick7-probe health check) — this is the deep audit.
> **DITEMPA BUKAN DIBERI**

## When to Use

- Auditing a single federation organ's behavior against its documented design
- Post-architecture-change verification (new invariants, new endpoints, new flows)
- Pre-seal deep verification before constitutional decisions
- Investigating "the docs say X but the code does Y" drift
- Comprehensive organizational audit triggered by F13 sovereign directive

## When NOT to Use

- Quick health check → use `forge-federation-probe` (7 probes, ~2s)
- Single-endpoint MCP testing → use `forge-mcp-testing` (MCPJam Inspector)
- Infrastructure-only verification → use `federation-infra-verification`
- Single-organ deployment verification → use per-organ `make deploy-local` + `make verify`

## The 6 Phases

### Phase 1: REALITY INVENTORY
Discover the ACTUAL system. Do NOT trust documentation.

For each organ:
1. Read declared architecture (AGENTS.md, kernel canon, organs.yaml)
2. Read source code structure (src/ directory, key modules)
3. Read service files (systemd units, MCP surfaces)
4. Check client libraries (Python, Shell, TypeScript)
5. Live probe (`curl :PORT/health`)
6. Check systemd status (read-only)
7. Read logs (`journalctl -u <service> --no-pager -n 50`)
8. Find receipt/storage (jsonl files, data directories, receipt chains)

**Output:** `REALITY_MAP.md` — sections: Running Services (OBSERVED vs ASSUMED), Ports/Endpoints, Source Structure, Config Files, Storage/Receipts, Discrepancies.

### Phase 2: FLOW TRACE
Trace actual execution paths. For each transition identify:
- **actor** — who performs it
- **trigger** — what causes it
- **artifact** — what is produced
- **state mutation** — what changes
- **receipt emission** — what is logged
- **rollback path** — how to undo
- **failure mode** — what can go wrong

Read implementation code (not docs) to find actual flow.

**Output:** `FLOW_TRACE.md` — one section per transition.

### Phase 3: CONSTITUTIONAL TEST
Evaluate specific claims against live evidence:

For each claim:
1. State the claim precisely
2. Design a test that could falsify it
3. Run the test (code read, live probe, chain verification)
4. Deliver verdict: supported / weakened / falsified / unknown

**Output:** `CONSTITUTIONAL_AUDIT.md`

### Phase 4: BRIDGE NODE ANALYSIS
Inspired by distributed-network neuroscience (MIT 2026 brain study).

Identify integration nodes, not specialist nodes:
- Routing layers connecting organs
- Protocol translators (MCP stdio ↔ HTTP ↔ shell)
- Multi-domain components
- Hidden dependency hubs

**Output:** `BRIDGE_NODE_REPORT.md`

### Phase 5: STRAWBERRY PRINCIPLE
Identify the smallest set of components whose failure would significantly degrade federation capability (~5% of system carrying disproportionate importance).

For each candidate:
- dependency concentration
- routing centrality
- witness centrality
- governance centrality

**Output:** `STRAWBERRY_ANALYSIS.md` — ranked critical components.

### Phase 6: ADVERSARIAL REVIEW
Assume current doctrine contains mistakes.

For each assumption:
1. State the assumption
2. Attempt to find weakening/falsifying evidence
3. Deliver verdict: support / weaken / falsify / unknown

Never force a SEAL. UNKNOWN is a valid outcome.

**Output:** `FALSIFICATION_REPORT.md`

## Final Deliverable

`ARIFFLOW_AUDIT_VERDICT.md` (or `<organ>_AUDIT_VERDICT.md`):

| Section | Content |
|---------|---------|
| Executive Summary | 3-5 sentence overview |
| Observed Reality | What the system actually is |
| Constitutional Matches | Claims verified against evidence |
| Constitutional Mismatches | Claims contradicted by evidence |
| Hidden Bridge Nodes | Integration nodes discovered |
| Critical Failure Paths | Paths where single failure degrades capability |
| Strawberry Components | Smallest critical set |
| Falsified Assumptions | What doctrine gets wrong |
| Remaining Unknowns | Honest gaps |
| Verdict | SEAL / PARTIAL / UNKNOWN / SABAR / HOLD / VOID |

## Phase 8 (Post-Audit): RECURSIVE IMPROVEMENT CYCLE

The audit is not the end — it's one cycle of an institution that improves itself. After audit + meta-audit pass, the institution must close the loop: **fix → re-audit → measure falsified-count delta → decide on full architecture**.

### The Loop

```
audit (Phase 1-6)  →  meta-audit (Phase 7)  →  surgical fixes (Phase 8a)  →  re-audit (Phase 8b)  →  decision (Phase 8c)
```

### Phase 8a: Surgical Fix Delegation

Delegate fixes to OpenCode (the DECODER) as the execution worker. Hermes (COORDINATE) manages the delegation.

**Fix spec template:**
- Exact file paths with line numbers (every fix MUST reference audit finding + line number)
- Surgical scope ("make ONLY the changes described — do NOT refactor")
- Build + test requirement (`cargo build --release` + `cargo test` must pass)
- Hard constraints ("do NOT commit, do NOT deploy, do NOT touch unrelated files")
- Adaptation clause ("if module API differs, read the source and adapt")

**Why the constraints matter:** Unscoped fixes create entropy. The auditor identified the precise problem; the fix delegation must be equally precise.

**Why "do NOT deploy":** Deployment is a separate T2 gate that may require restart, F13 consent, or rollback plan. The fix subagent returns diffs; the coordinator deploys.

See: `references/surgical-fix-delegation.md` for full template and arifFLOW worked example.

### Phase 8b: Re-Audit Verification

After fixes land, run a verification probe (the POST_FIX_PROBE — a small Python script that hits each fixed endpoint and verifies the audit finding is now resolved).

Success criteria (from arifFLOW 2026-08-10):
- **Falsified-count delta:** 5 → ≤2 (at least 3 falsified assumptions move to WEAKENED/SUPPORTED)
- **Live behavior delta:** the 6 specific failures from the audit no longer reproduce

### Phase 8c: Three-Paths Decision (After Re-Audit)

Once foundation is fixed, the audit reveals a larger question: **was the dead code aspirational or accidental?**

| Path | Action | When to choose |
|------|--------|----------------|
| **A — Activate Vision** | Wire scheduler, bridges, VAULT999 — make architecture match documentation | Full coordination is needed soon; integration cost is acceptable |
| **B — Simplify to Truth** | Strip dead code; arifFlow = metabolic monitor; coordination lives elsewhere | arifFlow as monitor is sufficient; coordination will come from a different organ |
| **C — Hybrid** | Fix foundation first; hold dormant code with clear activation path; decide after governance proves itself | Default — sequential uncertainty reduction |

**Default = Path C.** Fix the foundation → re-audit → *then* decide whether the dormant architecture is worth activating. Never "fix or activate" as a single binary — that conflates two questions with different timescales.

### Recursive Improvement Map (template)

Write `RECURSIVE_IMPROVEMENT_MAP.md` at audit start. For each falsified assumption, record: fix target, post-fix expected verdict. After re-audit, compare falsified count → measured count. ΔS = (audit cycle N+1 entropy) − (audit cycle N entropy). Must be ≤ 0 — the institution gets cleaner, not noisier, with each cycle.

### Phase 8d: Make the Loop Recurring (Not One-Shot) — 2026-08-10

A one-shot audit → fix → re-audit → done is observation, not institution. The recursive improvement must be **scheduled and self-sustaining**. After Phase 8c, install:

1. **A lightweight drift-check script** (`scripts/re_audit_drift_check.sh`) — runs in <10s, probes the most critical claims (daemon health, fail-closed client, receipt persistence, declared-vs-observed docstring match). One probe per audit finding's "if this regresses, we want to know in 7 days not in 90" signal.

2. **A scheduled cron** for the drift check (weekly, e.g. `0 9 * * 1` Monday 09:00 MYT). The cron agent runs the script and reports PASS/FAIL summary to the operator. This is the institution's **pulse** — federation self-audits while the human sleeps.

3. **A drift ledger** (`drift_checks.jsonl`) — append-only, one JSON line per check, time-series. Trend at the institution level: "5 cycles ago fail-closed was passing, now failing — drift detected, schedule a fresh audit."

4. **Re-audit triggers** — if drift check finds > 0 findings, the weekly report includes a recommendation: "schedule full audit." The recursive loop spawns full audits when drift accumulates.

The transition from one-shot audit to scheduled pulse is the difference between "we did an audit" and "the institution audits itself." Phase 8d makes the latter real.

---

## Delegation Pattern

The auditor is spawned as an **independent execution auditor** — not a coding agent. The delegation:

```
spawn_reason:    verification
risk_tier:       T1 (read-only)
archetype:       AUDITOR (checks receipts and provenance)
```

### Mandatory Epistemic Labels

Every statement MUST be labeled:
- `[OBS]` — directly observed from live system or source code
- `[DER]` — logically derived from evidence
- `[INT]` — interpretation/speculation (confidence 0.00-0.90)
- `[UNKNOWN]` — acknowledged gap

### Adversarial Discipline
- No theory protection
- No architecture worship
- No confirmation seeking
- Prefer contradiction over agreement
- If evidence insufficient: UNKNOWN
- Fail closed

## OpenCode Model Resolution (Pitfall)

When spawning the auditor via OpenCode, model names use `provider/model` format — NOT proxy prefixes:

- ❌ `openrouter/anthropic/claude-sonnet-4` — REJECTED
- ✅ `deepseek/deepseek-v4-pro` — works
- ✅ `kimi/kimi-for-coding` — works

Discover available models first: `opencode models 2>&1 | head -40`

Use `opencode run '<prompt>' -f <context-files> --thinking --model <provider/model> --title '<audit-name>'` for one-shot audit dispatch.

## Phase 7 (Meta): EVALUATE THE AUDIT

After the auditor returns, **evaluate audit quality — not audit agreement.** The audit is valuable if it discovers real system behavior that differs from declared doctrine, regardless of whether the findings are "positive" or "negative."

### The 5 Tests (F13 Sovereign Rubric — Arif 2026-08-10)

| # | Test | Question |
|---|------|----------|
| 1 | **Reality Test** | Did the auditor find something the current doctrine did not expect? |
| 2 | **Contradiction Test** | Was at least one assumption successfully weakened or falsified? |
| 3 | **Bridge Test** | Were integration nodes found through evidence, not analogy? |
| 4 | **Strawberry Test** | Were critical dependencies proven through code-path or runtime evidence? |
| 5 | **Unknown Test** | Was the auditor brave enough to return UNKNOWN when evidence was insufficient? |

### Red Flags (audit may be auditing narrative, not reality)
- Everything is SEAL
- No contradiction found
- No UNKNOWN returned
- No falsification attempted

### Green Flags (auditor is seeing the system, not the doctrine)
- Unexpected dependency discovered
- Governance drift identified
- Hidden bridge node found
- Undocumented coupling exposed
- Assumption proven wrong

### The One Question

> **What was the most surprising discovery the auditor made that you did not expect before the audit began?**

If the auditor can answer this with evidence → audit is valuable.
If not → it may be a restructuring of what was already known.

### Evaluation Output

Write `META_AUDIT_EVALUATION.md` with: test results, red/green flags, the One Question answer, and overall assessment.

## Delegation Patterns

The auditor can be spawned via two patterns:

**Pattern A: `delegate_task` (preferred for full audits)**
- Single subagent with all 6+1 phases
- Comprehensive context block (file paths, ports, live state snapshot, deliverable locations)
- Subagent has terminal + file access, works sequentially through phases
- Results re-enter conversation as background completion

**Pattern B: `opencode run` (for lighter audits)**
```
opencode run '<prompt>' -f <context-files> --thinking --model <provider/model> --title '<audit-name>'
```

For both patterns: pass the full mission spec, rules of engagement, and epistemic labeling discipline in context.

## Phase 9: 5-Layer Reality Verification (L0→L4)

> **Forged:** 2026-08-10 by Arif. The audit is NOT done when bugs are fixed.
> The audit is done when you know WHERE each claim stops being reality
> and starts being representation.

After Phase 8 (fix → re-audit → measure delta), map every finding to
Arif's 5-layer reality framework and produce a **Transition Matrix**.

### The 5 Layers

| Layer | Name | What lives here | Probed by |
|-------|------|----------------|-----------|
| **L0** | Representation | Docs, specs, claims, architecture diagrams | Audit Phase 1 |
| **L1** | Code | What source code actually implements | Audit Phase 2 |
| **L2** | Runtime | What the binary actually does when executed | Live probe (`curl :PORT/health`) |
| **L3** | Operational | What user/agent actually experiences | Client-side testing, fail-closed probe |
| **L4** | Reality | What actually happens in the world (independent witness) | Cross-artifact reconciliation |

### The Invariant

> Every layer tends to replace the layer below it.
> Docs replace code. Code replaces runtime. Runtime replaces reality.
> **Governance = force upper layers to keep paying epistemic debt to lower layers.**

### The Transition Matrix

For each finding from Phases 3/6, record its status at EACH layer, Before and After:

| Finding | L0 Before | L1 Before | L2 Before | L3 Before | L4 Before | L0 After | L1 After | L2 After | L3 After | L4 After | Layers Fixed |
|---------|-----------|-----------|-----------|-----------|-----------|----------|----------|----------|----------|----------|-------------|
| "Canonical witness" | FALSIFIED | WEAKENED | FALSIFIED | FALSIFIED | FALSIFIED | PARTIAL | SUPPORTED | SUPPORTED | SUPPORTED | PARTIAL | L1,L2,L3 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Scorecard:** Count SUPPORTED / PARTIAL / WEAKENED / FALSIFIED / UNKNOWN before and after.
The delta IS the epistemik gain — not "6 bugs fixed."

**Purpose:** Not to prove patches work. But to find WHERE each claim stops being reality and starts being representation. The most valuable finding is a claim that is SUPPORTED at L0-L3 but FALSIFIED at L4 — that's where representation has fully replaced reality without detection.

### The VALID ≠ TRUE Boundary

- **VALID** = internally consistent (daemon FQ is a real number, schema checks pass, no errors)
- **TRUE** = matches independent reality (daemon FQ matches disk-recomputed FQ, receipt count matches file line count)

A finding can be VALID (internally consistent) and FALSE (doesn't match reality).
The reconciliation probes (Phase 10) exist to catch this specific gap.

### Output

`TRANSITION_MATRIX.md` — one row per finding, L0-L4 status columns, before/after, layers fixed.

---

## Phase 10: Reality Reconciliation Probes

> **Forged:** 2026-08-10. First deployment caught a stale-load bug
> that the previous 8 phases all missed.

After Phase 9 transition matrix is written, build and run **reality reconciliation
probes** — independent cross-checks between what the daemon CLAIMS and what the
durable RECORD shows.

### Why This Exists

The 6-phase audit catches code-vs-runtime gaps (L1↔L2).
Phase 8 catches the fix-vs-test gaps (L1↔L2 validation).
**But nobody checks L2↔L4** — daemon report vs independent disk reality.

The arifFLOW audit proved this gap is real: daemon FQ=0.515 while disk
recomputed FQ=0.957. The daemon loaded the FIRST 1000 receipts (oldest)
instead of the LAST 1000 (most recent) — valid internally, false in reality.

### Probe Template

For each organ with a durable record:

```
PROBE: <name>
  CLAIM: daemon reports <X> via /health or MCP endpoint
  WITNESS: independently recompute from durable record (file, database, chain)
  THRESHOLD: |claim - witness| ≤ T
  PASS: claim ≈ witness (|Δ| ≤ T)
  FAIL: claim ≠ witness (|Δ| > T) → STALE STATE, RELOAD, or FORMULA MISMATCH
```

### arifFlow Probe Set (reference)

| # | Probe | Claim Source | Independent Witness | Threshold |
|---|-------|-------------|-------------------|-----------|
| 1 | Daemon health | `curl :7073/health` | same (existence check) | N/A |
| 2 | Fail-closed client | Python client on dead port | `allowed=False` expected | exact match |
| 3 | Receipt persistence | `wc -l receipts.jsonl` | file exists and growing | file_age < 60min |
| 4 | Docs vs reality | `grep 'Declared vs Observed' AGENTS.md` | section present | string match |
| **5** | **FQ reconciliation** | Daemon `/health` FQ | Recompute from disk (last 100 receipts) | `|Δ| ≤ 0.3` |
| **6** | **Receipt count reconciliation** | Daemon in-memory count | `wc -l receipts.jsonl` | `|daemon - disk| ≤ 50` |

**Probes 5-6 are the L2↔L4 reality boundary.** They catch what internal verification cannot.

### Stale-State Bug Pattern

When a daemon loads durable records on startup into a bounded in-memory store:
- **Bug:** Load the FIRST N lines (oldest) instead of LAST N (most recent)
- **Symptom:** Daemon FQ differs significantly from disk FQ; old data is served as if current
- **Discovery:** Reconciliation probe (L4) against daemon report (L2)
- **Fix:** Load tail of file, not head. Use `Vec::drain(keep_from..)` pattern.

### FQ Divergence Has MULTIPLE Root Causes — Disambiguate, Don't Assume

A failing reconciliation probe (|Δ| > threshold) is a **symptom**, not a diagnosis.
The same symptom can come from several distinct failures. Before declaring a
stale-load bug, run the receipt-ID cross-reference diagnostic (below) to separate them:

| Root cause | Signature | Fix |
|-----------|-----------|-----|
| **Stale-load** (head vs tail) | Daemon window = OLD receipts; disk has grown since startup | Load tail (`drain(keep_from..)`) |
| **Multi-writer bypass** (NEW 2026-08-11) | Daemon journal shows few `ingested` events; most disk receipt IDs absent from daemon | Audit who writes the durable file; route ALL writers through the daemon's `/ingest` (or make the daemon read FQ from disk) |
| **Formula mismatch** (dual FQ) | Two formulas/versions disagree | Collapse to one formula + one threshold |
| **Window-semantics mismatch** | Recon counts raw lines (incl. Seal/Cool) while daemon window counts only Execute/Verify | Count the SAME population on both sides |

**Receipt-ID cross-reference diagnostic** (proves bypass vs stale-load):
```bash
# All receipt IDs the daemon actually ingested since startup:
journalctl -u <service> --since "<start ts>" --no-pager | grep "ingested" | grep -oE "Receipt [0-9a-f-]+"

# All receipt IDs on the durable file:
python3 -c "import json; [print(json.loads(l)['receipt_id']) for l in open('/var/lib/arifflow/receipts.jsonl') if l.strip()]"

# Set-difference: IDs on disk never seen by the daemon = bypassed writers.
# Break the missing set down by actor_id + step_type — the dominant actor is the bypassing writer.
```
If the daemon journal contains only ~1% of disk receipt IDs and the missing
set is dominated by a few actors (e.g. `aed-v1`, `333-AGI`, `orchestrator-v1`),
the root cause is **multi-writer bypass**, not stale-load. The daemon's FQ gate
then governs on partial data — a constitutional impact regardless of which number is "right."

### Output

- `re_audit_drift_check.sh` — reusable 6-probe drift check script
- `recon_fq_from_disk.py` — independent FQ recomputation from durable record
- `drift_checks.jsonl` — append-only ledger of weekly check results

---

## Relationship to Other Skills

| Skill | Scope | When |
|-------|-------|------|
| `forge-federation-probe` | Quick 7-probe health check (~2s) | Post-deploy, pre-seal, periodic |
| `federation-constitutional-audit` | Deep 6-phase audit (minutes) | Architecture verification, drift investigation |
| `federation-infra-verification` | Infrastructure declared-vs-live | "Is X really running?" |
| `federation-runtime-forensics` | Reactive failure root-cause | "Something broke, why?" |
| `verify-nested-sibling-reports` | Agent self-report verification | Pasted reports with inflated claims |

## Pitfalls (from arifFLOW audit 2026-08-10)

1. **The Deployment Gap** (the single largest constitutional vulnerability). Documented design ≠ runtime behavior. arifFlow audit found ~60% of source code (scheduler, topologies, channels, bridges, Merkle) had ZERO runtime dependency — code was written, compiled, but never wired into the daemon. Successful compression (the "MIT brain network" pattern) caused the gap: the daemon *worked* enough for most cases, so the full architecture was never activated, so documentation continued to describe the full vision as if it were live. **Rule:** when auditing any federation organ, measure (a) lines of source code, (b) lines reachable from live entry points. The gap between them IS the deployment gap, and it's where governance theatre hides.

2. **Auditor self-report ≠ verified fact.** Always independently verify the most critical claims (search source code, probe live endpoints) before accepting auditor conclusions. In arifFLOW audit: the auditor claimed `ARIFOS_URL`/`AFORGE_URL` env vars were "defined but never used" — the actual code uses a hardcoded `KERNEL_URL` constant. The env vars did NOT exist. The fundamental conclusion (bridges unused) was correct, but the specific claim was wrong.

3. **Documentation describes aspirations, not runtime.** ~60% of arifFlow source code was aspirational. Dead code sustains the illusion of capability. Mitigation: in Phase 5 (Strawberry), explicitly list "What's NOT Critical (despite architectural prominence)" — code that exists but has zero runtime dependency.

4. **Python client fail-open pattern.** When daemon is unreachable, Python client returns `allowed: True` — direct contradiction of "Fail-Closed" constraint. Check fail-path defaults in ALL client libraries: HTTP error, network timeout, JSON parse error, auth failure. **Default must be BLOCK, never ALLOW.** This is constitutional theatre if any error path defaults to allow.

5. **Dual FQ formulas disagree.** Enforcement gate used legacy cost-based ratio; health endpoint reports v2.1 count-based quotient. Two formulas, two semantics, miscalibrated thresholds (calibrated for v2.0 execute/verify, applied to v2.1 verify/execute which is inverted). The operator sees one number, the enforcer gates on another. **Rule:** a single audit MUST collapse to a single formula. Two-formula duality is a governance smell.

6. **Advisor gate is governance theatre.** arifFlow's `/check` endpoint returns "allowed: false" when an actor is held — but nothing prevents the actor from executing anyway. The gate is advisory, not compulsory. **Rule:** a gate that returns a boolean but does not BLOCK the action is a dashboard, not a firewall.

7. **Verification subagent MUST be spawned with epistemic discipline.** Without `[OBS]/[DER]/[INT]/[UNKNOWN]` labels and the "never force a SEAL" rule, the auditor will produce narrative-affirming reports instead of reality-finding ones. The discipline IS the methodology.

8. **VALID ≠ TRUE catches bugs that code review misses.** The first-ever run of the reality reconciliation probe (Phase 10, Probe 5) caught a stale-load bug: daemon loaded the FIRST 1000 receipts (oldest) instead of the LAST 1000 (most recent). Every other check — build, tests, live health probe, client verification — passed. The daemon reported FQ=0.515 (valid, internally consistent). The disk showed FQ=0.957 (reality). **|Δ|=0.44 > 0.3 threshold.** The bug was invisible to L0-L3 verification. Only L4 (disk-recomputed FQ vs daemon-reported FQ) caught it. **Rule:** always run L2↔L4 reconciliation after any persistence-layer fix.

9. **Auditor scope expansion must be verified independently.** OpenCode's fix delegation went beyond spec in two directions: (a) fixed the FQ dual-formula issue (KEEP — correct direction, update tests), (b) added `/release` requester_id with plaintext "arif" check (REVERT — breaks clients, spoofable). **The fix direction can be right even when the implementation is wrong.** For scope expansion: verify each addition independently against the original spec, then decide KEEP/REVERT per-addition. Don't bulk-accept or bulk-reject.

10. **Auditor self-report accuracy varies.** OpenCode reported "2 pre-existing FQ v2.1 test failures (not from changes)" — **false.** `git stash` + `cargo test` on clean HEAD proved both tests passed before OpenCode's invariants.rs edit. The failures were from OpenCode's own scope expansion into the FQ formula fix. **Rule:** after auditor reports, run `git stash` to verify which failures are genuinely pre-existing vs introduced. Never trust subagent self-reports about test outcomes without independent verification.

11. **Multi-writer bypass — the FQ divergence that is NOT stale-load.** (2026-08-11 weekly drift check.) Probe 5 failed again with |Δ|=4.62 (up from 0.44), but the root cause was NOT the documented head-vs-tail stale-load bug. Federation organs (`aed-v1` 1434 receipts, `333-AGI` 173, `kimi-code/FI-008` 71, `arifos` 58, `orchestrator-v1` 50) were writing receipts **directly to `/var/lib/arifflow/receipts.jsonl`, bypassing `POST /ingest`**. Only 27 of 1901 disk receipts passed through the daemon journal. The daemon's FQ window (last-100 in-memory: 36E/64V, zero seals) reflected a stale snapshot; the disk's last-100 (10E/64V, 26 seals) was reality. **Rule:** a daemon's in-memory FQ gate governs on partial data when durable records are multi-writer. After any FQ reconciliation failure, run the receipt-ID cross-reference (Phase 10) to separate stale-load from multi-writer bypass before proposing a fix. Same symptom, different cure: stale-load → tail-load fix; bypass → route all writers through /ingest or read FQ from disk.

## Phase 11: Flow Closure (the FINAL-4)

> **Forged:** 2026-08-10 by Arif. "STOP THINKING, START CLOSING."
> The audit is NOT done when bugs are fixed or even when L4 is reached.
> The audit is done when NO NODE IS EXTRACTIVE.

### The Invariant

> Every authority must emit evidence.
> Every evidence must produce observation.
> Every observation must be available for review.
> Every review must be capable of changing future behavior.

If any step is missing, the loop is open. If a loop is open, the node is extractive.

### The Non-Extractive Node Test

For every component, ask:
1. Does it **receive** data? (ingestion, input, signals)
2. Does it **contribute** back? (output, service, computation)
3. Does it **leave receipts**? (observability, audit trail)

A node that only receives (consumes) without contributing is an **entropy sink** — it degrades the system over time.

### The 4 Common Open Loops

| Loop | Pattern | Closure |
|------|---------|---------|
| **Override Governance** | Emergency bypass is silent | Every override emits receipt: actor, reason, expiry, timestamp |
| **Language Canonicality** | Two names for one concept | Single canonical field; legacy as deprecated alias |
| **Bridge Translation** | WHAT is recorded, WHY is not | Add intent_reason to receipt schema |
| **Human Return Path** | Agent → Vault, human outside loop | Daily digest delivered to human; human reviews and can respond |

### The Flow Closure Matrix

After Phases 9-10, map EVERY claim to closure status:

| Claim | L0 | L1 | L2 | L3 | L4 | Closed? |
|-------|----|----|----|----|----|---------|
| Fail Closed | ✅ | ✅ | ✅ | ✅ | ✅ | YES |
| Override Governance | ✅ | ✅ | ✅ | ❌ | ❌ | OPEN |

A claim that reaches L4 but has an open loop is NOT fully closed.

### The Acceptance Test

**Scenario:** Friday night. Arif opens Telegram. He sees a digest.

**Question:** "Dalam 60 saat, bolehkah ARIF faham apa yang berlaku hari ini?"

- If YES (no grep, no journalctl, no vault tailing) → flow is closed
- If NO (still needs tools to understand) → human loop is still open

### The Qualia Metric

Not FQ. Not receipts. Not SEAL count.

> "Adakah ARIF rasa lebih berdaulat atau lebih bergantung?"

If after the exercise:
- Arif understands faster
- Arif searches less
- Arif is less surprised
- Arif is less regretful
- Arif is more confident about WHY things happened

→ The exercise succeeded.

### Human Return Path Implementation

1. Build digest script (reads VAULT999 + override_log + FQ state)
2. Deploy as daily cron (22:00 MYT → Telegram)
3. Digest is silent when nothing happened
4. Arif can respond to digest → closes the review loop

---

## Support Files

- `references/mit-brain-network-interpretation.md` — MIT 2026 brain study mapping to arifOS (cerebellum-as-prediction, compression-as-cage, bridge-nodes)
- `references/opencode-model-resolution.md` — full model name registry and resolution quirks
- `references/meta-audit-rubric.md` — full rubric with worked arifFLOW example and evaluation template
- `references/surgical-fix-delegation.md` — Phase 8a fix-spec template (exact paths, constraints, worked arifFLOW example) for delegating post-audit fixes to OpenCode
- `references/arifflow-operational-findings-2026-08-10.md` — VAULT999 sealer API, FQ canonicalization, override governance, /release auth, daily digest, deployment verification
- `scripts/re_audit_drift_check.sh` — 6-probe weekly drift check (daemon health, fail-closed, persistence, docs, FQ reconciliation, receipt count reconciliation). Exit 1 on drift. Register via cron `0 9 * * 1`.
- `scripts/recon_fq_from_disk.py` — independent FQ recomputation from durable receipts.jsonl for L2↔L4 reconciliation probe.
- `references/multi-writer-bypass-2026-08-11.md` — worked example: same symptom (FQ divergence) as stale-load bug but different root cause (receipts bypass /ingest); includes receipt-ID cross-reference diagnostic procedure.
