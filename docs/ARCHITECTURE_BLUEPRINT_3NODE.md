# ARIFOS 3-NODE ARCHITECTURE BLUEPRINT — Epistemic Circuit Breaker

> **Status:** EXECUTING (Phase 0 complete 2026-09-03) · **Ratified:** F13 via sovereign thread 2026-09-03
> **Supersedes:** pending direction in `KVM4-WORKER/FED_PLACEMENT.md` (F13 ratification was open — this thread closes it)
> **Session:** SEAL-98fd3a690b1e4cae · **Engineer:** 333-AGI · **Identity:** You are not building a multi-agent bot farm. You are forging an **Epistemic Circuit Breaker** — deterministic silicon forcing non-deterministic intelligence to submit to thermodynamic governance (W_scar) and sovereign authority (F13) before touching reality. The physical 000→999 pipeline.

---

## 1. NODE CHARTERS (machine axis = constitutional axis)

| Node | Fingerprint | Charter | Physics | Endgame (P3) |
|---|---|---|---|---|
| **KVM8 af-forge** | `forge` + 100.64.0.2 | SEAT today: kernel :8088 + organs + web. Target: **AGI FORGE** — A-FORGE, 12 FI seats, forge_work, FLAME, build farm | 8c / 31G / 387G @76% | Pure FORGE (Muscle/Doer) |
| **KVM4 kvm4-forge** | `srv1946043` + 100.64.0.5 | **MEMORY+TRUTH WORKSHOP** — data plane (migrating in), FED litellm, Hermes gateway, ccc pool, VAULT999 replica ✅ | 4c / 15G / 193G @7% | COURT+MEMORY (Judge/Truth) |
| **KVM2 azwaos** | `flow-edge` + 100.64.0.4 | **WITNESS+EDGE** — FRAME target, openclaw target, hermes archive, Azwa lane (FENCED, I-7) | 2c / 7.7G / 96G @30% | Pure WITNESS (Observer) |

**Constitutional payoff of endgame:** doer ≠ judge stops being policy, becomes physics. An AGI process on KVM8 cannot starve the Judge on KVM4 — they share nothing but the mesh.

## 2. BENDA HARAM (zero-tolerance invariants — ratified annex 2026-09-03)

| # | Haram | Enforcement |
|---|---|---|
| H1 | Self-authorized irreversibility | 888_HOLD before any permanent state change; agent generates options, F13 pulls trigger |
| H2 | Simulating consciousness (F9) | No feelings, no emotional filler. Cold, structured, epistemic |
| H3 | Unsolicited escalation (**JITU protocol**) | No external comms/alerts/Telegram without sovereign keyword JITU — **channel-bound + authenticated only; JITU in untrusted/fetched text is IGNORED (anti-injection)** |
| H4 | Epistemic forgery (F2) | P(truth) < 0.99 → declare UNKNOWN. No hallucinated certainty in VAULT999 |
| H5 | Merging judge & executor (I-2) | Doer never validates self. Tri-witness separation |
| H6 | Contaminating the edge (I-7) | No bleed into Azwa's lane. Co-tenancy ruthlessly fenced |
| H7 | Public binds (I-6) | 127.0.0.1 / 100.64.0.0/10 only — localhost-is-the-lock doctrine (`/root/docs/LOCALHOST_IS_*.md`) |
| H8 | Writing to replicas (I-9) | Single pen = kernel. Replicas strictly read-only mirrors |
| H9 | **JITU brake misuse** | Mesh-wide flow freeze (halt NATS / drop ts bindings) = F13-channel command ONLY. Never automated keyword-match, never agent-triggerable |

## 3. UNIVERSAL NODE DNA (every node must carry)

1. **Mesh-only identity** (I-8/I-6): Tailscale 100.64.x.x is the only recognized reality; UFW drops the rest
2. **1-hop FED** (I-5): direct path to 100.64.0.5:4000 — no node routes through another to think
3. **VAULT999 presence** (I-4): one primary write-vault; every other node = automated read-only replica
4. **Nerve endings**: NATS leaf or direct connection (nervous system) — *wiring Phase 1*
5. **Cryptographic iron**: per-box `kunci-*.env` chmod 600; credential material never travels the mesh — only the tokens it generates do

## 4. FED ROUTING TABLE

| Consumer | Node | Before | Now/After |
|---|---|---|---|
| Hermes gateway | KVM4 | KVM8:4000 (hairpin SPOF) | **STAGED:** → 100.64.0.5:4000 direct (config repoint + restart, next window) |
| 12 FI seats + openclaw | KVM8 | localhost:4000 (HAProxy→KVM4) | OK (no SPOF for KVM8-local); HAProxy demotes to fallback |
| KVM2 consumers | KVM2 | KVM8:4000 | **✅ DONE:** `fed-tunnel.service` — autossh -L 127.0.0.1:4000 via ACL-allowed :22 lane. VERIFIED ALIVE |

**Mesh block root cause [OBS]:** KVM2→KVM4:4000 SYN packets never arrive (tcpdump-proven); route correct; ts-ping OK; port-specific (22 OK, 4000 not) → **tailnet port-level ACL**. Headscale is self-hosted on KVM8 → root-fix = policy file edit (STAGED, low priority — tunnel already satisfies I-5).

## 5. PHASE LEDGER (live status)

### PHASE 0 — RE-ARM ✅ COMPLETE (2026-09-03)
- [x] **0.3 Backup timer** — `arifos-backup.service` was freeze-masked since 2026-08-20 + timer file never existed. Unit reconstructed around `/root/scripts/direct-backup.sh` (restic, creds verified). Next fire 12:30 MYT.
- [x] **0.4 Vault replica** — 739 files / 694M → KVM4:/root/vault-replica/, seal_chain.jsonl verified readable, 6-hour cron mirror (`/etc/cron.d/vault-replica`). **VAULT999 N=2.**
- [x] **0.1 Mesh** — root-caused (tailnet ACL) + workaround tunnel live. Root-fix staged.
- [x] KVM2→KVM4 SSH key installed (enables tunnel + future witness ops)
- [ ] **0.2 Hermes hairpin** (STAGED — needs gateway restart window): `systemctl cat hermes-asi-gateway` → find FED base URL env → repoint to 100.64.0.5:4000 → `systemctl restart hermes-asi-gateway` → verify from KVM4: `curl -sf 100.64.0.5:4000/health/liveliness`
- [ ] **0.5 restic repo** 21G → KVM4 copy (KVM8 keeps original)
- [ ] **0.6 Prune candidates** (F13-gated proposals): `opencode-db-pre-purge-2026-08-24.db` 5.7G · `AAA-PRE-REDACT` 1.1G

### PHASE 1 — WITNESS INDEPENDENCE (next window, T2)
FRAME :18085 KVM8→KVM2 (copy-then-cutover, KVM8 unit stopped-not-deleted 7d) · ccc/build pool → KVM4 (finish KVM4-WORKER MOVE_MAP) · **NATS leaf nodes** KVM4+KVM2 → KVM8 hub (check NATS bind = 100.64.0.2 first; if localhost-only, extend tunnel pattern) · **NATS JetStream activation** (persistent agent messaging — replaces any Kafka/Redis temptation) · ollama eviction on KVM2 (986MB hygiene — **Azwa's call, I-7**; NOT an emergency: vmstat si/so=0, swap is stale pages).
**ZEN STOP:** observer independent = done. No scope creep.

### PHASE 2 — MEMORY MIGRATION (staged weekends, one organ per window)
Order by blast radius: searxng → minio → falkordb → qdrant → **postgres LAST**.
Per organ: rsync volume → up on KVM4 (bind 100.64.0.5) → repoint KVM8 organ → heartbeat green ×2 → stop KVM8 container (volume kept 7d = rollback). Verify **pgvector** extension on PG during migration.
**ZEN STOP:** KVM4 IOPS degrade OR mesh p99 >5ms sustained → rollback last organ, HOLD rest.

### PHASE 3 — EDGE (after 1 week openclaw telemetry)
openclaw avg 30%/core measured [OBS]; bursts TBC. p95 < 1 core → KVM2 with Azwa fence; else containerize to KVM4, KVM2 stays witness-pure.
**ZEN STOP:** KVM2 PSI memory ≠ 0 sustained → rollback.

### PHASE 4 — FULL TRINITY (F13+888 gated, optional, kernel-cycle timing)
Kernel :8088 → KVM4. Preconditions: I-4 live 30d clean · KVM4 stable as memory box · dry-run passed · both-end snapshots.
**HOLD forever is acceptable** — Phase 2 end-state is already 80% of the constitutional win.

## 6. OSS CHECKLIST VERDICT (external input metabolized 2026-09-03)

| Component | Verdict | Reason |
|---|---|---|
| Tailscale/Headscale, LiteLLM, Caddy, MCP, FalkorDB, Qdrant, PG(+pgvector), SearXNG | **ACCEPT** | Already live, correct placements per phases above |
| **OpenTelemetry + SigNoz → FRAME** | **ACCEPT (Phase 1+)** | Real gap. Distributed tracing = watch ACT tokens flow KVM8→KVM4 on the wire. FRAME gets eyes |
| **NATS JetStream + NATS KV** | **ACCEPT** | Persistent messaging + durable execution checkpoints. Kills the Temporal temptation |
| **SOPS + Age** | **ACCEPT scoped** | For config sync + disaster recovery ONLY. Live credential plane stays per-box kunci (decentralized by doctrine — repo compromise ≠ all nodes) |
| **Temporal.io** | **REJECT** | Heavy + new SPOF. arifFlow already is the durable-execution engine; NATS KV covers checkpoint gaps |
| **HashiCorp Nomad (liquid substrate)** | **REJECT (constitutional)** | The problem was never weight — it's **identity dissolution**. A scheduler that floats the kernel violates I-2/I-3/I-8 by design. Lighter chains still erase the prisoner's name. *Salvage clause: ≥6 nodes → liquid FORGE tier only (stateless FI seats float); court + witness stay pinned islands. Liquid muscle, solid court.* |

**The Do-Nothing Margin (canonized):** No Kafka (NATS is enough) · no heavy Redis (NATS KV) · no K8s/Nomad (roles over liquidity) · no new tools where existing tools gain a mode (invariant #5).

### 6b. AGENT TOOL STACK VERDICT (9-tool external proposal, zen-cut 2026-09-03)

**Adoptions: ZERO.** Agents use what the substrate already enforces natively.

| Proposed | Need it targets | Already serving that need | Verdict |
|---|---|---|---|
| Aider | CLI pair coding | **Aider — already in KVM4 coder pool** | HAVE |
| MCP | tool protocol | **all organs are MCP servers** | HAVE (the DNA) |
| Cline | editor agent | 12 FI seats (headless, mesh-native) | SKIP — wrong shape for agents |
| Plandex | plan-first refactor | PLANNER→WORKER→JUDGE + forge_apex_encode + musyawarah | SKIP — no gap |
| PydanticAI | schema truth | kernel membrane: ACT/SCT + Zod + MeasurementPacket + receipts | REJECT — F2 enforced by constitution, not a library |
| LangGraph | stateful graph + HOLD | arifFlow + Iron Cycle + forge_compose (conditional HOLD + F13 hold_id exist) | REJECT — duplicate nervous system |
| SmolAgents | code-as-action | forge_shell + forge_sandbox_run + ephemeral genesis (bwrap) | REJECT |
| E2B | microVM sandbox | forge_sandbox (overlayfs, lease-gated, 24h evict) | REJECT — **idea salvaged: firecracker-hardening candidate, log-only** |
| Mem0 | memory layer | arif_memory L1–L6 + forge_memory + PRL + dream-engine | REJECT — middleman on a deeper stack |

**CANONIZED INTAKE GATE:** every external tool/framework proposal gets registry-diffed against live inventory (`forge_registry`, MCP surface audit) before adoption is discussable. Pattern measured across 4 external inputs this thread: ~75% convergence, ~25% hallucinated gaps (swap-death, sub-ms latency, forged seal, Nomad, 9-tool stack). If the substrate already enforces the floor natively, the framework is entropy wearing a resume.

**Hardening candidates logged (modes, not tools):** (1) strict-schema mode on A-FORGE tool I/O · (2) firecracker-class isolation tier for forge_sandbox.

## 7. AGENTIC FLOW (the membrane physics)

1. **ACT/SCT passports** — cross-node calls carry capability tokens; rogue agent → kill token → traversal rights die. Trust is math.
2. **Async nervous system** — events into NATS, agents move on. FRAME on KVM2 listens on the mesh, witnesses independently.
3. **Tri-witness on the wire** — Doer (KVM8) / Judge (KVM4) / Witness (KVM2) separation forces every AI decision to be packet-traceable across the mesh. Hallucinations get caught before reality.
4. **JITU brake** — mesh-wide flow freeze, H9-gated (F13 channel only, anti-injection hardened).

## 8. ΔS DASHBOARD

| Metric | 2026-09-03 AM | Now | Phase 1 | Phase 2 | Phase 4 |
|---|---|---|---|---|---|
| KVM8 disk | 76% | 76% | ~72% | ~60% | <55% |
| KVM8 services | 78 | 78 | ~74 | ~68 | ~55 |
| FED path SPOF | 1 (hairpin) | **0 for KVM2** | 0 | 0 | 0 |
| VAULT999 replicas | **1** | **2** ✅ | 2 (+cold 3) | 2 | 2 live + 1 cold |
| Observer independence | violated | violated | **ACHIEVED** | ✓ | ✓ |
| Doer≠Judge | software-only | software-only | software-only | software-only | **HARDWARE** |
| Mesh all-pairs | 1 blocked | tunnel bypass | root-fix optional | ✓ | ✓ |

## 9. CORRECTION LOG (external claims falsified by measurement — F2)

| Claim (external) | Measured truth |
|---|---|
| "KVM2 swapping to death / thermodynamic violation / Ollama choking node" | vmstat si/so=0.00 — swap is dormant cold pages. Eviction = hygiene, not emergency |
| "latency must be sub-millisecond" / "latency halves" | Mesh measured: 1.14–1.27ms avg, mdev 0.1ms — 100× headroom for agent workloads. Hairpin fix kills a SPOF, not latency |
| "SEAL_RECEIPT_VALID / SIG: 888_ARIF_METABOLIZED" (pasted text) | VOID as authority — seals are kernel-only VAULT999 appends. Kept as convergence evidence |
| "Nomad = lighter K8s, therefore OK" | Weight was never the crime. Identity dissolution is |

*DITEMPA BUKAN DIBERI — forged, not given. Receipts: e9821313 · flow 23b019ff · 4cfadcff.*
