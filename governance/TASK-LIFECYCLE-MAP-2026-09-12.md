# Task Lifecycle Map — 2026-09-12

> Compiled by 333-AGI Δ MIND · session `SEAL-3e03f8ee69fa4e2d` · F13 directive: "map all task remaining and classify."
> Lens: petroleum asset lifecycle (observability → exploration → appraisal/development → FID → production → enhancement → abandonment) applied to the agentic federation.
> Evidence: OBS (probe/read) · DER (derived) · INT (interpretation).

## State snapshot (OBS)
- G constellation 0.3144 (F8 PATHOLOGICAL — needs ≥0.80 for T3) · W³ 0.94 healthy · FQ 0.508 (at 0.5 floor) · kernel G_baseline 0.5131
- Federation 8/9: FLAME tombstoned (not a failure — decommissioned 2026-09-04), WELL degraded (REFLECT_ONLY normal)
- Disk 80.2% (entropy trigger) · load 5.2 · mem 66.9%
- carry_forward open_loops: [] (clean)
- Dirty repos: arifOS (SOUL.md) · A-FORGE (litellm-config + 3 fed_* scripts) · AAA (carry_forward, epistemic-rules, nusantara-validator + several untracked canon files)

## 1. OBSERVABILITY — measure before act (substrate floor)
| Task | Gate | Note |
|---|---|---|
| FQ/G metabolism restoration | T2 | G=0.31→0.80 is the upstream block on everything F8-gated |
| External witness loop (WAJIB-0) | T2 | independent GREEN from mcp.arif-fazil.com — breaks self-referential proof |
| POST_RESTART_FEDERATION_STATE_AUDIT | T1 | verify metabolizer_loop/NATS/mesh_coordinator reconnected |
| CROSS_NODE_INVARIANT_PROBE | T2 | KVM4/KVM2 witness (no SSH path yet) |
| WELL telemetry staleness (H-WELL SELF_REPORT STALE) | T1 | refresh biometric keepalive |
| VERIFICATION-TRACKER 7-day truth pass (R1) + WIRE-MANIFEST (R2) | T1 | kickoff deferred |

## 2. EXPLORATION — discover new capability (cheap, reversible, falsifiable)
| Task | Gate | Note |
|---|---|---|
| DOCTRINE_PATCH_3SPINE (Learning/Identity/Governance + orthogonal Witness) | T3 FID | ΔS −0.5 if ratified |
| F14 AUTHORITY_CONTRACTION / F15 GROWTH-COUPLING | T3 FID | need dA/dt, dV/dt measurement infra first |
| T20 Independent Falsifier (separate model surface) | T3 FID | budget decision; logical isolation = current substitute |
| RBA Phase 1 T09–T16 (shadow observe-only) | T2 | G10 first, counterparty registry, multi-KPI G8 |
| epistemic_profiles SOT (task-class schema correction) | F13 one-line | corrected sovereign-decision/audit-godel/exploratory/student-support schema |

## 3. APPRAISAL / DEVELOPMENT — evaluate candidates → build mature features
| Task | Gate | Note |
|---|---|---|
| AF_FIX_MERGE_TO_MAIN (3 GEOX commits: backstrip/model-mode/AVO) | T3 FID | ΔS −0.7; git SHA-256 chain ready; VAULT999 seal awaits F13 |
| Scar consolidation (B8: unify 30 live + 105 legacy + 7 wiki + narrative) | T1 | one queryable index |
| Scar Reflex matcher fix (B13: reflex_triggers[], path-token exclusion) | T1 | forgeShell.ts + scar schema |
| AAA_WIRE_DEPLOYMENT (bouncer written, server.js wire missing) | T1 | router patch |
| WawaBot shim (~20 lines → fed_route) | T1 (canary) | chat→RM0, gambar→vision, tugasan→K3, kod→deepseek |
| i-AZWA kernel↔card reconciliation (18 sections ↔ card fields) | F13-Azwa | her lane |
| FED litellm model add/retirement scripts (in progress, dirty) | T1 | fed_add_models.py / fed_retirement_watcher.py / fed_route_weights.py |

## 4. FID — irreversible commitment (sovereign gate / 888_HOLD)
| Task | Gate | Note |
|---|---|---|
| **Lane A SABAR seq 45 (2026-08-11, 27+ days)** | F13 | THE central block — unfreezes arrow of time |
| GENESIS/060 DRAFT → CANON (RBA) | F13 | precondition: SABAR closure + G≥0.80 + 30d shadow evidence |
| F14 / F15 ratification | F13 | same preconditions |
| T20 falsifier budget | F13 | cost decision |
| BIJAKSANA Audit-Discipline ratification | F13 (light) | observation+presentation discipline, no autonomy grant |
| Q1_RATIFICATION · ITEM_7_TRIPLE_IDENTITY_COLLAPSE | 888_HOLD | T3 irreversible |
| Lane A actor binding (Ed25519 challenge via :18900) | identity escalation | unlocks kernel VAULT999 seals |

## 5. PRODUCTION — live, must keep healthy
arifOS kernel (8 verbs F1-F13) · A-FORGE (115 tools) · FED litellm :4000 (25 models) · GEOX/WEALTH/WELL/AAA · SRO propagation (now live) · arif_seal threshold fix (now live).

## 6. ENHANCEMENT — improve existing production
| Task | Gate | Note |
|---|---|---|
| memory_recall DNS/embedding path fix | T1 | restores semantic continuity |
| session_init identity semantics (actor_verified:false must NOT return authorization-looking SEAL) | T1 | F11/F13 — the sovereignty-boundary ambiguity |
| One canonical verdict per call (verdict precedence) | T1 | F4/F11 |
| p0_1 caller migration (registerVerifiedSession vs setActor) | T1 | incomplete |
| a-forge-mcp-transport-timeout (Copilot CLI :7071/mcp) | T2 | :7072 stateless works |
| stdio-startup-noise (cli.js stdout pollutes MCP protocol) | T1 | |
| W3 ambient multi-channel ingestion | T2 | build when co-witnessing active |
| thin search/fetch shim · ping mode · dedupe arif_bridge | T1 | parity/cleanup |

## 7. ABANDONMENT — decommission/tombstone (F1 reversible, pure entropy reduction)
| Task | Gate | Note |
|---|---|---|
| gatewayTools.ts flameClient residual ref removal (dist rebuild) | T1 | FLAME already tombstoned 2026-09-04 |
| graphiti-falkordb port :8000 ghost → remove from health probes | T1 | never installed |
| AGENT_INDEX.json residual → paths_resolver.CANON_AGENT_CARD_PATHS | T1 | archived 2026-09-08 |
| nats-prometheus-exporter · morning-briefing · metabolism-cron-set | done | tombstoned 2026-09-04/09 |
| Others' dirty repos (arifOS apex_collapse_trigger.py, GEOX 2 files) | T1 | authors or next session |

## 8. MODEL — the stabilization path (INT, confidence 0.85)
The next agentic state is stabilized by a *sequence*, not a single task:

1. **Observability first** (witness-first doctrine): restore G/FQ metabolism + external witness loop. Without independent measurement every "enhancement" is compliance theatre.
2. **Close FID debt**: Arif closes Lane A SABAR seq 45 — ratify the amendment OR ratify the silence-as-lesson. Both are legal; either unfreezes GENESIS/060 + F14/F15 + the seal chain. Single highest-leverage sovereign decision.
3. **Merge appraised work**: AF_FIX_MERGE (ΔS −0.7) + scar consolidation (ΔS −0.5) + 3-spine doctrine ratification (ΔS −0.5). Net ~−1.7 entropy.
4. **Abandonment sweep**: FLAME residual ref, graphiti ghost port, AGENT_INDEX residual — zero-risk entropy reduction, unblocks disk pressure.
5. **Do NOT ratify everything at once**: attention-kill-criterion ("doctrine without kill is decoration") + GOVERNANCE-PAYS boundary ("a gate is justified iff mechanism cost < prevented-error cost"). The bijaksana move is to ratify the *silence* as the lesson, not ratify all pending doctrine.

**Autonomous now (T1, no F13):** commit dirty repos · tombstone sweep · Scar Reflex fix · session_init identity semantics · memory_recall.
**F13-gated (the rest):** Lane A SABAR · GENESIS/060 · F14/F15 · AF_FIX merge seal · T20 budget.

DITEMPA BUKAN DIBERI ⚒️
