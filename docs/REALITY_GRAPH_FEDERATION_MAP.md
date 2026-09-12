# REALITY GRAPH — FEDERATION SYSTEM MAP

> **What this is:** Deep-research map of the arifFlow Reality Graph (RG-1 witnessed 2026-09-12) integrated against all ten federation organs: arifOS · AAA · A-FORGE · FRAME · arifFlow · FED · WEALTH · WELL · GEOX · HERMES.
> **Epoch:** 2026-09-12 (W38) · KVM8 `forge` (truth seat) · arifFlow HEAD `c041984` (+ dirty `src/receipt.rs` = RG-3 prep, see §8)
> **Truth rule:** live `:port/health` + code + ledger files beat every prose table. Everything below carries OBS/DER/INT/EXT-CLAIM labels.
> **Researchers:** 333-AGI session `SEAL-98ab373a263d4570` (direct verification + synthesis), 2 explore subagents (organs/doctrine), cross-checked against 3 external session analyses (kimi-code/FI-008 forge session + two deep-research sessions).

---

## 1. Executive verdict

```json
{
  "rg_1": "WITNESSED — edges survive daemon → JSONL → VAULT999 seal chain",
  "rg_1c_binding": "STRUCTURALLY CLOSED (code-verified; runtime recompute audit pending, 1 cmd)",
  "rg_2": "NEXT FORGE — lineage reconstruction from sealed receipts only",
  "rg_3": "HOLD until RG-2 passes + F13 authorization (converged verdict, 3 independent analyses + F13 SEAL quote)",
  "controlled_cycle": "CODE_PRESENT / TESTED (28) — runtime witness PENDING (no real CycleSummary yet)",
  "federation_readiness": "1 EMITTING · 4 PARTIAL · 2 SILENT advisors · graph substrate live at :7073"
}
```

The Reality Graph is **not a novel insertion** — it is the convergence point of at least six independently F13-ratified doctrine fragments (2026-09-07 → 09-12): claim-receipt-binding, institutional-memory-strata, consequence-binding, consequence-honoring, attention-graph, trauma-theorem. The code caught up to the doctrine on 2026-09-12.

**The one-line compression:** `Receipt = Witness · Edge = Because · Reality Graph = Witnessed Because`.

---

## 2. What the Reality Graph is

The federation's receipts were historically **chained** (each links to previous) but never **justified** (nothing links upward to constitutional authority). The Reality Graph adds two axes to the FlowReceipt atom:

| Field (spec `FLOW_RECEIPT_v1.md` §3.3/§7b) | Axis | Meaning |
|---|---|---|
| `routed_organ: Option<String>` | **Attention ancestry** | Which organ `arif_route` classified this step to — routing decisions become auditable on-chain |
| `parent_receipt_ids: Vec<String>` | **Reality ancestry** | Multi-parent DAG edges — fan-out merges get provenance ("because") |
| `genesis_anchor: Option<String>` *(drafted, uncommitted)* | **Constitutional ancestry** | RG-3 bridge to RCP-000/F13 canon — *justification, not just history* |

Five load-bearing distinctions the scaffold names (EXT-CLAIM, consistent with OBS code):
Capability ≠ Witness · Witness ≠ Authority · Chained ≠ Justified · Persisted ≠ Tamper-evident · Symbolic anchor ≠ Traversable bridge.

Roadmap: **RG-1** edge persistence ✅ → **RG-2** reality lineage → **RG-3** genesis bridge → **RG-4** governance receipts → **RG-5** scar-bound policies → **RG-6** consequence graph → **RG-7** graph-level FQ (FQ_G).

---

## 3. Verified evidence board (OBS unless labeled)

| Item | Evidence | Status |
|---|---|---|
| Graph integration commit | `4a5aef0` — kimi-code/FI-008, 2026-09-12 18:11 +08; fields + builders + ControlledCycle; 165 tests | **OBS** |
| Lineage propagation commit | `c041984` 18:16 +08 — payload_hash two-layer design, tamper-detection claim | **OBS (title+stat); full diff not re-audited** |
| Rust core fields | `src/receipt.rs:509–515` `routed_organ` + `parent_receipt_ids`; builders `:741–755`; tests `:1564+` | **OBS** |
| Runtime receipts with edges | `/var/lib/arifflow/receipts.jsonl` — `c07ef983` (rg1-test, `routed_organ:"WELL"`), `2e220b6b` (parents `[RCP-TEST-PARENT-001]`), `6b7b0dae` | **OBS** |
| VAULT999 seal chain | `/root/arifOS/VAULT999/arifflow_sealed.jsonl` — 29,351 entries; all 3 RG-1 receipts sealed (positions 3/6/10) | **OBS** |
| **RG-1C binding (payload↔seal)** | `src/main.rs:602–621`: seal checkpoint = `receipt.hash()` = SHA3-256 canonical receipt **incl. edge fields when set**; `chain_entry_hash = SHA3(prev_hash‖position‖checkpoint)` (`governance/vault999.rs:9,58`) | **DER (code-verified mechanism; runtime recompute not executed)** |
| Spec documentation | `spec/FLOW_RECEIPT_v1.md` §3.3 + §7b (DAG fan-out merge semantics) | **OBS** |
| 4th topology | `src/topology/controlled_cycle.rs` (1039 lines, 28 tests) + `TopologyKind::ControlledCycle` + `ExecutionMode::ConvergentLoop` | **OBS** |
| Daemon live | `:7073` FQ **BALANCED**, `qg.v0.3.1-vector`, actors incl. `rg1-test` | **OBS** |
| Seal failure mode | Seal failure = WARN + in-memory continuation, ingest does not fail (`main.rs:635–643`) | **OBS — known fail-soft property** |
| Roadmap institutionalization | **ZERO** "Reality Graph" docs in repo — roadmap is chat-only | **OBS — GAP** |
| Dirty worktree | `src/receipt.rs` = uncommitted `genesis_anchor` field + `with_genesis_anchor()` + ~120 lines tests (RG-3 prep) | **OBS — see §8** |
| floors→APEX-dials eigendecomposition | `floors_to_dials()` absent from arifOS/A-FORGE source | **OBS absence — gap claim corroborated** |
| GENESIS canon | `/root/arifOS/GENESIS/` numbered series 000–018+ (000_KERNEL_CANON, 013_APEX_FALSIFICATION…) exists; "K000→K999 K-series" naming | **EXT-CLAIM partially verified (series OBS, K-prefix naming not witnessed)** |

**Correction to one subagent claim:** "edge fields exist only in bridge clients, not Rust core" is **FALSE** — fields are in `src/receipt.rs` (committed) AND in runtime daemon-written JSONL. The subagent grepped wrong directories (`core/`, `adapter/`). Direct OBS supersedes.

---

## 4. Substrate anatomy — arifFlow (:7073)

```
agent/MCP ──POST /ingest──→ daemon
                              ├─ FQ meter (per-actor, qg.v0.3.1-vector, window 100)
                              ├─ invariant gate F0–F6 (auto-enforce 10s; /check /release)
                              ├─ receipts.jsonl  ← SEMANTIC layer: full receipt incl. edges
                              └─ vault999.rs seal ← TAMPER-EVIDENT layer:
                                   checkpoint = SHA3-256(full receipt) ─→ hash chain
                                   appended to /root/arifOS/VAULT999/arifflow_sealed.jsonl
```

- **Two-layer witness model (refined 2026-09-12):** JSONL carries lineage *content*; seal chain carries tamper-evident *commitment*. Together = witnessed lineage. Seal entries store `{chain_entry_hash, chain_position, prev_hash, receipt_id, vault_entry_id}` — edges are bound **by hash**, not repeated as content.
- **Topologies (4):** Pipeline · Fan-out · Cascade · **ControlledCycle** (WORK→VERIFY→[PASS|FAIL] convergent loop; `EscalationTarget` 7-target enum; exit order Passed→Divergence→Stall→Budget→MaxRounds).
- **Naming law:** `JUDGE_888 ≠ SOVEREIGN_F13` — ControlledCycle may exit to Judge888 for hold/review; only genuine F13-class transitions reach SovereignF13.
- **Declared-vs-observed honesty ledger** (AGENTS.md, 2026-08-10 audit): BSP scheduler compiled but daemon-inactive; metabolism plane is the live plane. The Reality Graph rides the live plane — no scheduler dependency.

---

## 5. THE ORGAN MAP — Reality Graph integration, organ by organ

| Organ | Port | Authority ceiling | Receipt/graph surface (OBS) | RG readiness |
|---|---|---|---|---|
| **arifFlow** | 7073 | METABOLIZE_ONLY | The substrate itself. Receipts→JSONL→seal chain; FQ; 4 topologies; `owned_domains: [flow_quotient, receipt_metabolism, attention_checkpointing]` | **SUBSTRATE LIVE** |
| **arifOS** | 8088 | JUDGE_ONLY | F1–F13 floors (13/13 healthy); 8 verbs; VAULT999 owner; GENESIS canon 000–018; `arifflow_sealed.jsonl` lives in ITS vault | **ANCHOR — RG-3/4 target** |
| **AAA** | 3001 | DISPLAY_ONLY | Registry + canon + doctrine home; `organs.yaml` declares "FLOW_GRAPH.json not minted — Phase 7 queued (architect lock 2026-08-18)" = the exact slot RG fills | **DOCTRINE SOURCE** |
| **A-FORGE** | 7071/7072 | EXECUTE_AFTER_SEAL | 118 tools; **Chain-of-Experience ledger** (`~/.local/share/arifos/world-model/experience_traces.jsonl`) — genuine hash chain (seq/prev_hash/hash), the federation's *second* append-only chain | **PARTIAL — `trace_id↔receipt_id` link absent** |
| **HERMES** | 18089/18789 | EDGE (Telegram) | **Sole full-schema emitter**: `cron-receipt-bridge.py` → `/ingest` 19-field receipts, `witness_organs:["arifos"]`, Execute+Verify pairs; wawabot cognitive hook also ingests | **EMITTING — lacks edge tags (cron jobs have known organ targets → cheapest RG upgrade)** |
| **FED** | 7074/4000 | ADVISORY_ONLY | Route advisor (`fed_route`/`fed_classify`, never judges/blocks); litellm models agi-333/asi-555/apex-888/i-arif | **SILENT — advisory twin of `routed_organ`** (two classifiers of the same question; joining them makes FED quality measurable) |
| **FRAME** | 18085 | ADVISORY_ONLY | Independent observer; baseline_organs=10; FQ drift chambers (`fq_critical 0.5`); **observes arifFlow but never POSTs** | **SILENT — observer of the graph, not in it** (natural future `witness_organs:["frame"]` Cool/Barrier emitter) |
| **WEALTH** | 18082 | COMPUTE_ONLY | `/root/VAULT999/wealth/receipts.jsonl` (2,286 lines, epistemic labels, **flat — no chain**) | **PARTIAL — receipt-shaped, unchained, no ingest, no routing provenance** |
| **WELL** | 18083 | REFLECT_ONLY | `/root/WELL/events.jsonl` (hashed I/O, triadic phases) → arifOS `:18081/attest` — **parallel bus**; no :7073 reference | **PARTIAL — hashed events, wrong bus. (Poetic: the first RG-1 edge was routed TO WELL.)** |
| **GEOX** | 8081 | COMPUTE_ONLY | PAI receipts (`pai_receipt.py`, sha256, `previous_receipt`) ride *inside* claim payloads → arifOS; no standalone ledger | **PARTIAL — chained provenance exists, not graph-visible** |

**Machine axis (MACHINE_MAP.md SOT):** KVM8 = truth/pen (everything above is KVM8-local) · KVM4 = execution (FED litellm `100.64.0.5:4000`, dormant Hermes backup) · KVM2 = witness (arifosmcp fork — NOT the judge; its :7073 is a *different* service). **All lineage reconstruction must be KVM8-sourced.**

---

## 6. Doctrine lineage — the RG is a collage of ratified fragments

| Phase | Pre-existing hook (all OBS-read) | Why |
|---|---|---|
| **RG-2** Reality Lineage | `institutional-memory-strata.md` (S2 sealed-only validity) · `consequence-bearing-identity.md` ("identity = witnessed consequence lineage") · `claim-receipt-binding.md` (handles: pointable → navigable) | Lineage valid only if derivable from sealed substrate alone; harness-swap becomes the acceptance test |
| **RG-3** Genesis Bridge | `civilizational-dependency-graph.md` (000–999 ladder; ARIF = "root key that loads the entire reality graph") · `organs.yaml` i-arif/FI-000 ("identity precedes engine") | Constitutional ancestry side of the bridge already named in canon |
| **RG-4** Governance Receipts | `GENESIS/059` Artifact 2 (Execution Binding must bind, not inform) · METABOLIZE_ONLY fence (organs.yaml §6) | Judge-ancestor edges make "Execute has Judge ancestor" a *checkable graph property*; arifFlow carries, never adjudicates |
| **RG-5** Scar-Bound Policies | `consequence-binding.md` Scar Gravity Law + rule 3 · `trauma-theorem.md` + `scar-weight-registry.json` (W_scar, 3 entities) · `memory-promotion-gate.md` (seal ≠ policy; Gates A–D) | Policies compressed from scar nodes = negative constraints with provenance; promotion still gated |
| **RG-6** Consequence Graph | `consequence-honoring-doctrine.md` ("witness keeps cost visible in the reality map") · `attention-scarcity-economics.md` ("Consequence = invoice — who receives the bill") | Decision→Execution→Outcome→Witness edges = the invoice chain made traceable |
| **RG-7** FQ_G | `GENESIS/059` Artifact 4 (Q10 Calhoun lock, verify:execute > 3:1) · `attention-graph.md` §8 ACSC (already a graph-shaped ratio) | FQ generalized from linear window to paths/subgraphs |

Also ratified and load-bearing: `attention-kill-criterion.md` (3-strike rule **requires** RG-2 recurrence-counting to become enforceable — doctrine demanding the graph before it can bite) · `attention-graph.md` §3.2 (typed weighted edges specified 2026-09; `parent_receipt_ids` = the *causal* relation instantiated) · `organs.yaml` "Phase 7 queued" architect lock = the standing slot.

---

## 7. Roadmap status board

```text
RG-1A  Full receipt edges in JSONL                    ✅ WITNESSED (3 receipts, OBS)
RG-1B  Seal reference in VAULT999 chain               ✅ WITNESSED (positions 3/6/10, OBS)
RG-1C  Payload↔seal cryptographic binding             ✅ STRUCTURALLY CLOSED (code: main.rs:607
                                                          checkpoint=SHA3-256(full receipt incl. edges);
                                                          vault999.rs:58 chain formula) — runtime
                                                          recompute audit NOT yet executed (1 command)
RG-2   Reality lineage                                ⏳ NEXT FORGE
RG-3   Genesis Bridge                                  🔒 HOLD (until RG-2 + F13; genesis_anchor
                                                          code already drafted in dirty worktree)
RG-4   Governance receipts                            ⏳ pending
RG-5   Scar-bound policies                            ⏳ pending (earned_by_scar provenance)
RG-6   Consequence graph                              ⏳ pending (+ floors_to_dials() eigendecomposition
                                                          gap confirmed absent — G-dial not auto-computable)
RG-7   FQ_G                                            ⛔ BLOCKED_BY RG-2..RG-6

ControlledCycle: CODE_PRESENT / TESTED(28) — runtime witness pending (needs one real CycleSummary
                with recorded exit condition + correct escalation target)
Naming law:     JUDGE_888 ≠ SOVEREIGN_F13
Hard rule (RG-2): no missing or unsealed ancestor may be silently treated as a root.
```

---

## 8. Gaps & shadow (declared, not hidden)

1. **Roadmap is chat-only.** No `REALITY_GRAPH_ROADMAP` doc in any repo — re-derivation risk per agent. Fix: `spec/REALITY_GRAPH_ROADMAP_v0.1.md` (CANDIDATE status, F13 required for ratification). *Owner: the forge session (kimi-code), not this map.*
2. **Dirty worktree = RG-3 prep uncommitted.** `src/receipt.rs` carries `genesis_anchor` + builder + tests past `c041984`. Handling: do NOT bundle with RG-1 claims; do NOT discard (it is drafted work). Recommended: move to branch `rg3-genesis-prep` once the forge session is idle — **do not touch a live session's worktree** (two-writer collision precedent 2026-09-12, carry_forward flock fix).
3. **Runtime recompute audit** for RG-1C not executed: retrieve receipt by ID from JSONL → recompute SHA3-256 → compare to chain checkpoint. One command; closes RG-1 fully.
4. **Two-parallel-store hazards:** (a) `VAULT999/reality_ledger/` vs future RG-6 consequence graph; (b) organ ledgers (wealth/well/frame) vs `routed_organ`-tagged receipts. Precedent: mem0 open loop in institutional-memory-strata. Bridge or fold, don't duplicate.
5. **Fail-soft seal:** VAULT999 write failure = WARN + in-memory seal; ingest survives, chain continuity in the file can lag. Monitor via seal-file mtime/line-count vs receipts.jsonl.
6. **`chain_position` semantics** observed as small numbers near tail (3/6/10) of a 29,351-line file — per-batch/window position, not global. Document before RG-2 traversal code assumes either.
7. **FED/FRAME silence:** the two observers touch the graph only as advisor/monitor. Cheapest federation win after RG-2: hermes cron bridge tags `routed_organ` (known targets).
8. **EXT-CLAIMs not independently witnessed:** K000→K999 K-series naming; 5-stage metabolic-loop compression; metabolic_loop.py/pre_execution_gate.py paths. GENESIS 000–018 series IS observed.

---

## 9. Next forge — RG-2 contract (endorsed)

Objective: *reconstruct lineage from sealed receipt references without narrative repair.*

```rust
LineageQuery { receipt_id, direction: Backward|Forward, max_depth, require_sealed }
LineageProof { target, graph_status, roots, paths, unresolved_parents, cycles,
               unsealed_receipts, seal_verification }
GraphStatus { Valid, PartialMissingParent, PartialUnsealedAncestor,
              InvalidSelfParent, InvalidCycle, InvalidHashBinding, DepthLimitReached }
```

Acceptance (12-test floor): single+multi-parent reconstruction · deterministic root order · missing-parent → PARTIAL (never fake root) · self-parent reject · direct+indirect cycle detection · seal required for all ancestors · **receipt-to-seal binding verified** · classification-boundary non-crossing · forward consequence tracing · machine-readable proof output.

Then, and only then, RG-3 with F13 authorization (`authority: SOVEREIGN_F13, human_approval: REQUIRED, payload_access: METADATA_ONLY`).

---

## 10. Provenance

- Direct verification: 333-AGI `SEAL-98ab373a263d4570` (git, code reads, ledger greps, live probes, seal-mechanism code trace).
- Subagent A: AAA/arifOS doctrine + vault inventory (read-only). Subagent B: HERMES/FED/FRAME/WEALTH/WELL/GEOX/A-FORGE surfaces (read-only; one claim corrected per §3).
- External analyses cross-checked: forge session (kimi-code/FI-008, commits 4a5aef0/c041984) + two deep-research session outputs supplied by Arif (claims labeled EXT-CLAIM where not independently witnessed).
- F13 SEAL quote bound to `4a5aef0`: *"Reality Graph belum berada pada fasa expand. Ia masih pada fasa bind to reality."*

DITEMPA BUKAN DIBERI ⚒️
