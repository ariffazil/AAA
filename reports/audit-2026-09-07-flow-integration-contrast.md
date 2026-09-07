# Contrast Report — FEDERATION_FLOW_INTEGRATION::2026-09 vs Live Machine

> Auditor: kimi-code/FI-008 (AAA swarm, 5 read-only agents + direct probes)
> Date: 2026-09-07 (MYT) · Node: KVM8 court-core (forge, 100.64.0.2)
> Method: every claim tagged OBSERVED with evidence; verdicts MATCH / DRIFT / FICTION / UNVERIFIABLE
> Companion artifact: /root/arifOS/contracts/fq_policy.yaml (DRAFT)

## 1. The reference document itself — PHANTOM

The pasted "arifOS Federation Flow Integration 2026-09" set (14-point canon, capability
graph C01–C38, dependency graph, flow map, gap report, organ boundary audit, flow
unification plan P0–P4, FHS deployment standard) has **zero provenance on this node**:
no file, no content match for `FEDERATION_FLOW_INTEGRATION`, no C-numbering, no
FLOW_UNIFICATION_PLAN / ORGAN_BOUNDARY_AUDIT / CAPABILITY_REGISTRY.md anywhere (live,
cold storage, or archive). Machine canon that DOES exist: `/root/AAA/federation/organs.yaml`
(33 components, truthed 2026-09-06), `/root/docs/MACHINE_MAP.md` (2026-09-04, honest),
`/root/arifFlow/ARIFLOW_KERNEL_CANON.md` (SEALED 2026-08-02), `FLOW_OWNERSHIP_LEDGER.md`.

## 2. Claim-by-claim verdicts (reference doc vs live machine)

| # | Doc claim | Live reality | Verdict |
|---|---|---|---|
| 1 | arifOS MCP = :8080 | :8080 = SearXNG (docker). Kernel = **:8088** (organs.yaml agrees) | FICTION — would route judge traffic into a search engine |
| 2 | AAA = :3001 | a2a-server :3001, health 200 | MATCH |
| 3 | APEX judgment backend = :3002 (C38, LIVE) | Nothing listens; `apex-health.timer` disabled; AAA canon says decommissioned | FICTION (live) — fixed MCP_STATE.md today |
| 4 | arifFLOW = :7073 (MIGRATING) | Rust daemon LIVE :7073, v3 vector FQ, 1000-receipt window, 21k+ receipts, VAULT999 sealing wired (chain 415+) | DRIFT (doc understates reality) |
| 5 | FHS 3-node: KVM8 remembers / KVM4 executes / KVM2 witnesses | ALL organs on KVM8 (court+forge+Hermes+vault); KVM4 = LiteLLM worker only; KVM2(azwaos) = idle passive. MACHINE_MAP agrees with reality, calls 3-node story SALAH | FICTION (physical separation never shipped; logical only) |
| 6 | KVM2 witness + canary | No witness/canary workload anywhere | FICTION / UNVERIFIABLE |
| 7 | Capability graph C01–C38 with owners | No C-numbering exists; real registry = AAA_CAPABILITY_REGISTRY.yaml + organs.yaml | FICTION (as artifact) — real SOT is different and live |
| 8 | web-canon = registry SOT | web-canon = web-surface canon, 9/33 organs, last commit 2026-08-14, HERMES port 8644 matches nothing | DRIFT — fixed port today; stale as organ registry |
| 9 | P1.1 POST /receipt endpoint DONE | Real route is **POST /ingest**; `/receipt/emit` never existed — AAA + A-FORGE clients 404'd silently forever | FICTION → **FIXED TODAY** (both clients repointed) |
| 10 | P0.2 AF1 validation in A-FORGE | No `af1/` dir, no AF1 symbol anywhere; real gate = ToolRegistry 888_HOLD + check_verdict FQ gate | FICTION (wrong names, real gates exist under other names) |
| 11 | P0.3 floors gated by AGENT_WORKBENCH_TRUST_LOCAL_VPS in arifOS | Flag exists in A-FORGE (RuntimeConfig), not arifOS; arifOS floors.py = compat shim → core/laws.py, no trust gating | DRIFT (right concern, wrong organ) |
| 12 | P1.5 delete arifFlow/FEDERATION_MAP.md | File still existed (marked superseded) | **EXECUTED TODAY** (git rm) |
| 13 | P2.3 HERMES missing from web-canon federation.json | HERMES IS listed (port wrong) | HALF-STALE — port fixed today |
| 14 | Receipt fragmentation "3+ stores" | ~13 stores; TWO parallel arifFlow ledgers (receipts.jsonl 21,258 vs arifflow_sealed.jsonl 19,973 — different schemas, not mirrors) | MATCH (undercounted) |
| 15 | FHS paths /opt/*, /var/lib/vault999 | 11/18 exist; VAULT999 really at /root/arifOS/VAULT999 (13G, symlinked); /opt/arifos = 12-day stale twin; /opt/af-forge → /root (hostile symlink) | ASPIRATIONAL |
| 16 | 9-step intent lifecycle, lease handshake | Live daemon enforces FQ but arifos_governance.rs / aforge_executor.rs compiled-but-never-called; scheduler stdin-only | PARTIAL FICTION at runtime |

## 3. What the machine actually IS (OBS)

- Single QEMU node runs court + execution + memory + edge. Privilege boundary = root on forge.
- Live planes: arifOS :8088 · A-FORGE :7071/:7072 · AAA :3001 · GEOX :8081 · WEALTH :18082 ·
  WELL :18083 · SIGNAL :18084 · FRAME :18085 · arifFlow :7073 · FED :7074 (+ :4000 haproxy,
  :4010 fed-aware, :4013 litellm) · VAULT999-writer :5001 · AAA-signing :18900.
- Metabolism is real: FQ holds live (2026-09-07: 333-AGI HELD FQ=0.00, qwen-code HELD,
  hermes-asi HELD FQ=0.37 STUCK, grok-build verification-dominant 105/0). Vector flags
  GOVERNANCE_COLLAPSE via pathological g-dimension (A-FORGE producer, 0.4623).
- Off-node VAULT999 mirror VERIFIED 2026-09-07: KVM4 `/root/VAULT999-mirror-KVM8`
  arifflow_sealed.jsonl 19,472 lines @ 03:47 +08 (timer SUCCESS, additive rsync).
- OpenClaw: COLD on KVM8 (units gone, ports refused, `.openclaw-cold`). organs.yaml now says so.

## 4. Executed fixes (this session, all reversible, git receipts)

| ID | Fix | Repo |
|---|---|---|
| E1 | VAULT999 off-node backup verified with remote evidence | (verify-only) |
| E2 | AgentEngine receipt forward → POST /ingest (canonical FlowReceipt) | A-FORGE |
| E2 | AAA operation-bus receipt forward → POST /ingest | AAA |
| E2b | worldModelLogger dead /telemetry/log calls → loud warn-once, HOLD-888 noted | A-FORGE |
| E3 | FEDERATION_MAP.md stale pointer deleted (git rm) | arifFlow |
| E4 | organs.yaml: openclaw deduped (33 comps, 0 dup ids), dead path → .openclaw-cold, cold live-probe | AAA |
| E5 | web-canon HERMES port 8644 → 18086 + port_note | web-canon |
| E6 | MCP_STATE.md APEX :3002 "Active" → Decommissioned truth | AAA |
| E7 | FRAME doctrine dual-copy → identical (no-op, verified) | FRAME |
| E8 | arifFlow AGENTS.md stale "VAULT999 not wired" → wired | arifFlow |
| E9 | fq_policy.yaml DRAFT (P1.6 gap) — RATIFICATION_REQUIRED: ARIF | arifOS |
| E10 | This report | AAA |

## 5. Remaining queue — HOLD-888 (needs sovereign decision or dedicated window)

| # | Item | Why held |
|---|---|---|
| H1 | arifFlow daemon: add /telemetry/log (+ /receipt/emit alias) route | Rust rebuild + metabolism-plane restart |
| H2 | /opt/arifos deploy refresh (12-day stale runtime twin of law organ) | Law-organ deploy = 888 window |
| H3 | Witness plane on azwaos (KVM2): VAULT999 Merkle-head attestation | New infra + remote node access |
| H4 | Phantom tailnet binds (12 bound / 5 served, :18100 no backend) + FED 0.0.0.0:7074 rebind | Mesh mutation; UFW currently default-denies |
| H5 | Physical court/forge separation (MACHINE_MAP T3.1) | Strategic, host-level |
| H6 | AUTO-EXECUTION-QUEUE items #3 (WawaBot — Azwa canary), #4 (epistemic schema — needs F13 confirm), #5 (Lane A signing — identity escalation), #11 (i-AZWA — Azwa's F13 lane) | Their own gates |
| H7 | Merkle artifacts + witness fields are null in live receipts; seal chain = one jsonl deep; /opt/af-forge → /root hostile symlink | Design decisions for 888 |

## 6. Conclusion

The reference document is a phantom canon describing an institution that was planned, not
the one running. The running institution is *healthier than the doc claims in places*
(arifFlow metabolism, FQ enforcement, VAULT999 sealing, off-node mirror all LIVE) and
*sicker in others* (silent 404 receipt loss — now fixed; dual ledgers; no witness plane).
Machine SOT = organs.yaml + MACHINE_MAP.md. Fix direction: delete contradiction faster
than create capability — done today for six contradictions; seven held for 888.

DITEMPA BUKAN DIBERI — kimi-code/FI-008, 2026-09-07
