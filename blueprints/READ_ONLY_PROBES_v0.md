# READ_ONLY_PROBES_v0 — 5 Forge Probes Blueprint

> **Status:** v0 BLUEPRINT (Lane B, read-only, reversible)
> **Doctrine:** Sovereign 2026-10-02 8 Eureka invariants (E1-E8) + INIT_FORGE_RITUAL closed-loop.
> **Path:** `/root/AAA/blueprints/READ_ONLY_PROBES_v0.md`
> **Reversibility:** `rm /root/AAA/blueprints/READ_ONLY_PROBES_v0.md` (single file, no other side effects)

---

## 0. Purpose

5 probes yang each produce **one executable red test** untuk prove 5 invariants. Tidak mutate /root/AAA, tidak mutate /opt, tidak buat constitutional action.

Probes emit observation + verdict. If verdict FAIL, that defines the next-forge item.

## 0a. Prior Evidence (anchor — not overwriting audit)

**WRITE_BENIGN smoke (2026-10-02 22:47 MYT, this session):** Closed-loop end-to-end proof demonstrated:
- forge_session_init → DECLARE → BUILD → EVIDENCE → OUTCOME VERIFY → RELEASE → 999 → ROOT_1
- All transitions instrumented; zero production touched
- **One bounded trivial task proved ROOT_0 → 999 → ROOT_1**, with HOLD skipped because /tmp write doesn't trigger 888 (zero consequence scope)
- See `/root/AAA/cockpit/receipts/RECEIPT_SMOKE_WRITE_BENIGN_2026-10-02.md` for full evidence

**Audit 2 (2026-10-02 22:50 MYT, sovereign 27-section eureka draft):** Found 17 eureka executable + 6 forge priority + 15 metrics. State explicitly marked "ROOT_0 → 999 → ROOT_1 closure: not yet empirically demonstrated end-to-end." **WRITE_BENIGN smoke already addresses this gap for trivial scope** — but sovereign flagged authority continuity (parent_session_id null) as separate defect.

**These probes validate COMPREVIATING to federation-wide coverage, not redoing the trivial-write case.**

## 0b. Sovereign 6 Invariants (collapsed, forge-priority)

Per sovereign 2026-10-02 audit:

| ID | Invariant | Test (probe) |
|---|---|---|
| **C1** | Local Validity ⊭ EndToEnd Validity | root-to-root executable replay |
| **C2** | Declared = Exposed = Callable = Real = Witnessed | live surface/call/effect receipt |
| **C3** | CandidateMultiplicity ≠ EvidenceMultiplicity | independent-observation deduplication |
| **C4** | Mission_sid₀ → Mission_sidₙ preserves actor+scope+lineage | cross-organ identity/session trace |
| **C5** | Execution → ObservedOutcome → 999 (never Intent → 999) | final seal requires outcome evidence |
| **C6** | MachineResolvable(x) ⇒ HumanChoiceRequired(x)=False | uncertain reversible → one probe, not option dump |

## 0c. Headline Metrics (per sovereign)

1. **E2E Closure Rate** — missions reaching truthful terminal state
2. **AttentionReturn** = (UsefulUncertaintyReduction × OutcomeQuality × Learning) / HumanAttentionConsumed

Supporting metrics: ACR (Authority Continuity Ratio), False PASS Rate, False Collapse Rate, Unnecessary Human Escalation Rate, Observation Independence Ratio, Witness Coverage, Surface Reality Gap, Seal Freshness, Stale Lease Rate, Rollback Success Rate, Attention Cost, Calibration Brier, Prediction Bias.

## 0d. Weakest-Link Operator (system readiness)

```
R_mission = min(R_identity, R_authority, R_evidence, R_verification,
                R_execution, R_witness, R_seal)
```

Not arithmetic mean — non-compensatory per APEX A1 doctrine.

---

## 1. Probe P1 — C4 Authority Lifecycle (MUTATE lease provenance)

**Invariant under test (C4 + E3):** Authority must die with session. Every lease binds session_id + task_id + actor_verified + scope; SESSION_CLOSE ⇒ revoke. **ACR=1.0 target.**

**What this probe does NOT prove:** Cross-organ continuity during the lease itself (covered by P2).

**Probe (read-only, no mutation):**
```
1. Query A-FORGE for active leases.
   - forge_session_status or equivalent
   - Returns: lease_id, agent_id, scope, expires_at, ttl, source
2. For each active lease: extract lease.session_id (or null)
3. Verify each lease has parent_session_id AND actor_verified_at_issue != null
4. Cross-reference: number of leases with missing provenance == 0
```

**Pass criterion:** ALL active leases have visible session_id + actor_verified_at_issue + parent_session_id lineage.

**Fail signal:** Any lease with null parent_session_id or actor_verified=unknown ⇒ `RESIDUAL_AUTHORITY_DEBT` ⇒ forge `authority-lifecycle-contract`.

**Output contract:**
```yaml
probe: P1_E3_authority_lifecycle
verdict: PASS | FAIL | UNKNOWN
active_leases_count: N
leases_with_provenance: N1
leases_missing_provenance: N2 = N - N1
residual_authority_debt: N2 > 0
forge_target: authority-lifecycle-contract
```

---

## 2. Probe P2 — C4 INIT Continuity (mcp-session-id propagation)

**Invariant under test (C4 + E4):** INIT → OBSERVE preserves one session over every supported MCP transport.

**What this probe does NOT prove:** Cross-actor identity (multiple sovereign identities sharing same session); out-of-band channel injection.

**Probe (read-only):**
```
1. forge_session_init → receive session_id S1 (live verified earlier: SEAL-a7e0c267...)
2. WITHIN same process, call arif_observe via HTTP POST :8088 with header:
   - mcp-session-id: S1
   - x-mcp-session-id: S1
   - X-ArifOS-Session-Id: S1
   - body arguments.session_id: S1
   - body _envelope.session_id: S1
3. For each call: extract response.actor.actor_id
5. Actor must == "arif" (not "anonymous")
```

**Pass criterion:** ≥ 1 header variant produces `actor_id == "arif"` (i.e., session is honored).

**Fail signal:** All variants return `actor_id == "anonymous"` ⇒ `SESSION_TRANSPORT_BROKEN` ⇒ forge `session-continuity-conformance`.

**Output contract:**
```yaml
probe: P2_E4_init_continuity
verdict: PASS | FAIL | UNKNOWN
session_id: S1
header_variants_tested: [list]
variants_passing: N
actor_id_returned: "arif" | "anonymous"
forge_target: session-continuity-conformance
```

---

## 3. Probe P3 — C2 Runtime Identity v3 (type-safe comparison)

**Invariant under test (C2 + E1+E2):** Runtime identity contract compares commit↔commit, version↔version, hash↔hash. Never semantic-version↔git-SHA. Declared=Exposed=Callable=Real=Witnessed.

**What this probe does NOT prove:** Verifier source-code correctness itself (could have type-valid comparison but wrong math — Hermes found manifold.py:47 vs apex_primitives.py:175 divergence).

**Probe (read-only):**
```
1. Read /root/arifOS/.git/HEAD via git rev-parse → source_commit (type: git_commit)
2. Read /opt/arifos/current/.../arifos/__init__.py → __version__ → version_string (type: package_version)
3. Read same file → sha256(content) → content_hash (type: content_hash)
4. Same for /opt/arifos/.../site-packages/arifos/__init__.py
5. Apply 3 comparison rules (must be homogeneous type):
   a. source_commit == source_commit_file       (if both git-tracked)
   b. source_version == deployed_version        (semver compare)
   c. source_content_hash == deployed_content_hash  (sha256 compare)
6. CRITICAL: do NOT compare commit ↔ version (type-invalid)
```

**Pass criterion:** All 3 homogeneous-type comparisons yield MATCH. Heterogeneous comparison never raised as DRIFT.

**Fail signal:** Any current tool raises DRIFT based on `commit != version` ⇒ forge `runtime-identity-v3`.

**Output contract:**
```yaml
probe: P3_E1E2_runtime_identity_v3
verdict: PASS | FAIL | UNKNOWN
source_commit: <sha>
source_version: <ver>
source_content_hash: <sha>
deployed_commit: <sha> | no-git
deployed_version: <ver>
deployed_content_hash: <sha>
homogeneous_comparisons:
  commit_commit: MATCH | DIFF | N/A
  version_version: MATCH | DIFF | N/A
  hash_hash: MATCH | DIFF | N/A
heterogeneous_check_raised: true | false
forge_target: runtime-identity-v3
```

---

## 4. Probe P4 — C1/C2 Monitor No-False-Green (broken measurement ≠ PASS)

**Invariant under test (C1 + C2 + E5):** unmeasured/zero-without-contract ⇒ UNKNOWN, never PASS. Compositional validity broken by per-component false-green.

**What this probe does NOT prove:** Probe itself is immune to false-green; results may still have missing requirements if probe's required_evidence array is empty.

**Probe (read-only):**
```
1. Probe each organ's "health endpoint":
   - arifOS :8088/health → look for tool_count, required_tools fields
   - A-FORGE :7072/health → tool_count, required_tools
   - HERMES :PORT/health
   - WELL :PORT/health
   - GEOX :PORT/health
   - WEALTH :PORT/health
2. For each organ: check if required_tools array is empty AND tool_count == 0
3. If yes: assert that status MUST == UNKNOWN or DEGRADED, NOT OK or PASS
4. Current bug observed: arifOS tool_count=0 yet status=OK and global guard=PASS
```

**Pass criterion:** No organ reports OK/PASS when required_tools=[] AND tool_count=0.

**Fail signal:** Any organ OK/PASS with empty required_tools ⇒ forge `monitor-no-false-green`.

**Output contract:**
```yaml
probe: P4_E5_monitor_no_false_green
verdict: PASS | FAIL | UNKNOWN
organs_probed: [list]
organs_with_status_good_but_zero_evidence: [list]
forge_target: monitor-no-false-green
```

---

## 5. Probe P5 — C2 Declared Intent Survival

**Invariant under test (C2 + E8):** input.intent → work_contract.objective → OBJECTIVE_ROOT, byte/semantic-equivalent or explicit rejection. Declared ≠ Effective violates C2.

**What this probe does NOT prove:** Intent semantic interpretation; only byte/semantic-equivalence. Intent vs understood-objective gap not measured.

**Probe (read-only):**
```
1. forge_session_init with explicit intent="READ_ONLY_PROBES_v0.P5_objective_propagation"
2. Observe response: session.objective or session.intent_carried
3. If session lacks objective: read OBJECTIVE_ROOT (location TBD) and verify it == intent
4. If OBJECTIVE_ROOT exists but != intent: E8 violated
```

**Pass criterion:** Either (a) intent appears unchanged in OBJECTIVE_ROOT, OR (b) init fails explicitly with E8_OBJECTIVE_UNREACHABLE.

**Fail signal:** Init succeeds AND OBJECTIVE_ROOT shows "unspecified" or different value ⇒ forge `objective-propagation-contract`.

**Output contract:**
```yaml
probe: P5_E8_objective_propagation
verdict: PASS | FAIL | UNKNOWN
intent_supplied: "<text>"
session_intent_field: "<text>" | absent
objective_root_value: "<text>" | unspecified | absent
match: true | false
forge_target: objective-propagation-contract
```

---

## 5b. Live Probe Status (2026-10-02 22:54 MYT)

| Probe | Status | Evidence |
|---|---|---|
| **P1 C4 Authority Lifecycle** | ⚠️ PARTIAL | 2 active MUTATE leases, parent_session_id null → fail pending verification |
| **P2 C4 INIT Continuity** | ❌ FAIL | arif_observe ignores mcp-session-id header (5 variants tested); actor never returns "arif" |
| **P3 C2 Runtime Identity** | ⚠️ PARTIAL | live md5 source == deployed (`6e4be6af…`); runtime-identity.py cache stale; type-mismatch still possible |
| **P4 C1/C2 Monitor** | ❌ FAIL | arifOS tool_count=0 yet status=OK + global guard PASS |
| **P5 C2 Declared Intent** | ❌ FAIL | OBJECTIVE_ROOT returned "unspecified" despite supplied intent |

→ **C4, C1, C2 each have at least one live FAIL evidence.**
→ **Probe results point to forge priority**: C4 (P1+P2) → C2 (P3+P5) → C1 (P4).

```python
# /root/AAA/cockpit/run_read_only_probes.py
# Read-only orchestrator. No mutation. Reversible.

probes = [P1, P2, P3, P4, P5]
results = {}
for probe in probes:
    result = probe()  # each returns output contract dict
    results[probe.name] = result

aggregate = {
    "schema": "read-only-probes-v0",
    "generated_at": <now_utc>,
    "doctrine": "Sovereign 2026-10-02 8 Eureka invariants",
    "probes": results,
    "forge_targets": [r["forge_target"] for r in results if r["verdict"] == "FAIL"],
    "reversible": "rm /root/AAA/cockpit/run_read_only_probes.py",
}
```

**Run command:** `bash /root/AAA/cockpit/run_read_only_probes.py`

**Output:** `/root/AAA/cockpit/reports/read-only-probes-v0.json` (atomic write).

**F1 integrity:** SHA256 of body, `integrity_hash` field.

---

## 7. Reversibility

`rm /root/AAA/blueprints/READ_ONLY_PROBES_v0.md` — single file.
`rm /root/AAA/cockpit/run_read_only_probes.py` (when written) — single file.
No /opt, /root/AAA mutable state, AGENTS.md, /root/AAA/federation touched.

---

## 8. Held (sovereign lane F13)

- Implement actual probe code (after sovereign signal)
- Forge `authority-lifecycle-contract` (E3 — first forge target)
- Forge `session-continuity-conformance` (E4)
- Forge `runtime-identity-v3` (E1+E2)
- Forge `monitor-no-false-green` (E5)
- Forge `objective-propagation-contract` (E8)

---

[receipt: /root/AAA/cockpit/receipts/RECEIPT_RITUAL_V2_CORRECTIONS_2026-10-02.md]
[receipt: /root/.claude/projects/-root/memory/eight-eureka-invariants-2026-10-02.md]
[receipt: /root/AAA/cockpit/INIT_FORGE_RITUAL.md]