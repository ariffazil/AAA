# Cross-SOT Contradiction Table — 2026-08-06 Session Snapshot

**Source:** Hermes Agent session, `hermes-asi`, 2026-08-06T14:25 UTC
**Scope:** AAA control plane (organs.yaml, workspace.yaml, A-FORGE, arifOS, FRAME, SIGNAL)
**Mode:** Read-only audit, no files modified

---

## Contradiction 1 — A-FORGE Multi-SOT Tool Count Disagreement (CRITICAL)

A-FORGE MCP surface count is inconsistent across 6 SOT files and live runtime:

| Source | Tool count | `last_verified` |
|---|---|---|
| Live `:7072/health` | `stateless_tools: 44` | — |
| `A-FORGE/contracts/mcp_surface.yaml` | `registered_tools: 75` | 2026-07-01 (29 days stale) |
| `A-FORGE/contracts/tools.yaml` | 15 named tools | 2026-05-19 (78 days stale) |
| `AAA/federation/organs.yaml` (live_probe_2026_07_30) | `mcp_stateless_tools: 52` | 2026-07-03 (34 days stale) |
| `AAA/federation/repos.yaml` (2026-07-19) | `total_public: 85` | 2026-07-19 (48 days stale) |
| `AAA/federation/federation-manifest.yaml` | `mcp_reported: 59` | 2026-07-14 (53 days stale) |
| `A-FORGE/src/interfaces/mcp/` source | 13+ files with registered tools | not indexed |

**Verdict:** A-FORGE's `contracts/mcp_surface.yaml` `last_verified: 2026-07-01` is 29 days stale. Code has been updated but the contract wasn't regenerated. Live 44 ≠ any declared SOT. The `federation-manifest.yaml` marked this as `P0.2: needs_export_surface_audit` on 2026-07-14; it remains unresolved.

**Contradiction 2 — Dual Authority-Ceiling Vocabulary (CRITICAL)**

Two parallel YAML vocabularies express authority ceilings with different band counts:

| Organ | `organs.yaml::authority_ceiling` (6-band scale) | `organ_authority_ceilings.yaml::ceiling_band_equivalent` (APEX §8 5-band) | Agree? |
|---|---|---|---|
| arifOS | `JUDGE_ONLY` | `SOVEREIGN` | ✅ (JUDGE_ONLY ≈ SOVEREIGN in practice) |
| A-FORGE | `EXECUTE_AFTER_SEAL` | `FULL` (ceiling: `777_FORGE`) | ✅ (same operational reality) |
| AAA | `DISPLAY_ONLY` | `T3_888_HOLD` / `LIMITED_MUTATE` | ❌ (DISPLAY_ONLY has no APEX equivalent) |
| GEOX | `COMPUTE_ONLY` | `OBSERVE_ONLY` | ❌ (more restrictive in A-FORGE file) |
| WEALTH | `COMPUTE_ONLY` | `OBSERVE_ONLY` | ❌ (more restrictive in A-FORGE file) |
| HERMES | `RELAY_ONLY` | not in A-FORGE file | ❌ (missing) |
| SIGNAL | `OBSERVE_ONLY` | not in A-FORGE file | — (not cross-checked) |
| FRAME | `ADVISORY_ONLY` | not in A-FORGE file | — (not cross-checked) |
| arifFlow | `METABOLIZE_ONLY` | not in A-FORGE file | — (not cross-checked) |

Additional non-standard ceilings in organs.yaml with no APEX equivalent: `EDGE_AGENT` (OpenClaw), `UI_EDGE`, `METABOLIZE_ONLY`, `CRYPTO_HELPER`, `GATE_HELPER`, `ACTUATE_AFTER_LEASE`, `OBSERVE_ALERT`.

**Contradiction 3 — SIGNAL Chamber-Count Split (HIGH)**

| Source | Chamber count | Notes |
|---|---|---|
| `organs.yaml` line 270–276 | **6** (crypto_gate, idempotency_buffer, tcoa_ingestion, priority_classify, channel_route, governed_send) | Live probe claims `all_6_chambers: active` |
| `signal_organ/chambers.py` source | **3** (chamber_1_crypto_gate, chamber_2_idempotency, chamber_3_ingest) | Chambers 4/5/6 have no implementation |
| `signal_organ/main.py` | references chambers 1-3 only | confirmed |

**Contradiction 4 — FRAME Chamber Count vs organs.yaml (MEDIUM)**

| Source | Chamber count |
|---|---|
| `organs.yaml` | 6 (baseline, probe, compare, trend, alert, report) |
| `frame_organ/main.py` | **7** (`rsi_verify` added without organs.yaml update) |
| Live `:18085/health` | `all 7 chambers active` (in-code dict literal) |

**Contradiction 5 — workspace.yaml Missing Organs (MEDIUM)**

| Organ | Declared in organs.yaml | Declared in workspace.yaml | Live status |
|---|---|---|---|
| arifFlow | ✅ (:7073, class METABOLISM) | ❌ missing | live (:7073) |
| SIGNAL | ✅ (:18084, class CORE) | ❌ missing | live (:18084, `all_6_chambers: active`) |
| FRAME | ✅ (:18085, class CORE) | ❌ missing | live (:18085, 7 chambers) |

workspace.yaml `sot_manifest.version: v2026.08.04` predates their formal registration in organs.yaml.

**Contradiction 6 — Port Collision (MEDIUM)**

| Port | Declared organ in organs.yaml | Declared in workspace.yaml |
|---|---|---|
| :18084 | SIGNAL (mcp_port) AND WELL-Witness | not in workspace |
| :18086 | HERMES (mcp_port) | — |
| :18089 | — | HERMES (canonical_repos.port) |

**Contradiction 7 — I-ARIF Flip-Point State (LOW-MEDIUM)**

- `ml_floors_enabled: false`, `ml_method: heuristic`, `ml_hold_state: disabled`
- 3-condition flip-point (RASA_WIRING_ENABLED, SentenceTransformers dep, graphiti embedding) — 0/3 met
- Live state is honest, but reports can easily misread the "design landed" framing

---

## Evidence paths used

| File | Path |
|---|---|
| organs.yaml (machine SOT) | `/root/AAA/federation/organs.yaml` |
| workspace.yaml (canonical repos) | `/root/AAA/federation/workspace.yaml` |
| federation-manifest.yaml | `/root/AAA/federation/federation-manifest.yaml` |
| repos.yaml | `/root/AAA/federation/repos.yaml` |
| A2A agents.yaml | `/root/AAA/a2a/registry/agents.yaml` |
| AGENTS_UNIFIED.yaml | `/root/AAA/registries/AGENTS_UNIFIED.yaml` |
| CANONICAL_REGISTRY_POLICY.yaml | `/root/AAA/registries/CANONICAL_REGISTRY_POLICY.yaml` |
| ROOT_AGENT_CONFIG.yaml | `/root/AAA/ROOT_AGENT_CONFIG.yaml` |
| organs.yaml organ entry | `/root/AAA/federation/organ.yaml` |
| arifOS tools_sot.yaml | `/root/arifOS/tools_sot.yaml` |
| A-FORGE contracts/mcp_surface.yaml | `/root/A-FORGE/contracts/mcp_surface.yaml` |
| A-FORGE contracts/tools.yaml | `/root/A-FORGE/contracts/tools.yaml` |
| A-FORGE organ_authority_ceilings.yaml | `/root/A-FORGE/a_think/organ_authority_ceilings.yaml` |
| SIGNAL chambers.py | `/root/SIGNAL/src/signal_organ/chambers.py` |
| FRAME main.py | `/root/FRAME/src/frame_organ/main.py` |
| FRAME baseline.py | `/root/FRAME/src/frame_organ/baseline.py` |
| arifOS RASA wiring_config.py | `/root/arifOS/arifosmcp/rasa/rasa_wiring_config.py` |
| arifOS /health (live) | `curl -sf http://127.0.0.1:8088/health` |
| A-FORGE MCP /health (live) | `curl -sf http://127.0.0.1:7072/health` |
| FRAME /health (live) | `curl -sf http://127.0.0.1:18085/health` |
| aaa-drift-check.py | `/root/AAA/scripts/aaa_drift_check.py` |
