# ORGAN TABLE SOURCE-OF-TRUTH AUDIT & DEDUPLICATION REPORT

> **Status:** AUDIT COMPLETE · BATCH C (2026-09-08)  
> **Authority:** ARIF (F13 Sovereign Directive — Batch Execution Ordering)  
> **Axiom:** One Organ Registry · One Owner · One Source of Truth · Many Projections  
> **Canonical Human SOT:** [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md)  
> **Canonical Machine SOT:** [`/root/AAA/federation/organs.yaml`](/root/AAA/federation/organs.yaml)  
> **Canonical Node SOT:** [`/root/AAA/docs/MACHINE_MAP.md`](/root/AAA/docs/MACHINE_MAP.md)  
> **Truth Rule:** `live :port/health` beats every prose table. Re-probe before SEAL claims.

---

## 1. Executive Summary

A comprehensive scan across `/root/AAA`, `/root/arifOS`, and `/root/A-FORGE` identified over **110+ static projections** of organ tables, capability tables, and federation topologies.

The audit confirms:
* **The Knowledge Problem is Solved:** The true federation topology is completely established.
* **The Drift Problem is Mechanical:** Tables were copied into individual READMEs, contracts, briefs, and historical reports, causing **silent divergence** as new organs (`arifFlow :7073`, `FRAME :18085`) were born and older planes (`FLAME :18901`) were decommissioned.
* **The Invariant:** Every organ table must be explicitly classified into **SOT**, **Thin Projection**, **Pointer**, or **Historical Archive**.

---

## 2. Canonical SOT Declaration (The Triad)

| SOT Class | Canonical File | Owner | Format | Purpose |
|---|---|---|---|---|
| **Human SOT** | [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md) | AAA Control Plane | Markdown | Authoritative architecture, anatomy, roles, authority ceilings, and boundaries. |
| **Machine SOT** | [`/root/AAA/federation/organs.yaml`](/root/AAA/federation/organs.yaml) | AAA Control Plane | YAML | Schema-validated machine configuration for ports, systemd units, endpoints, and automation. |
| **Node Mesh SOT** | [`/root/AAA/docs/MACHINE_MAP.md`](/root/AAA/docs/MACHINE_MAP.md) | AAA / Infra | Markdown | 3-node topology mapping (KVM8 truth seat, KVM4 execution, KVM2 witness). |

---

## 3. Detailed Audit Matrix

### Object 1: Core Organ Master Table (Ports, Roles, Ceilings)
* **Owner:** AAA Control Plane
* **Canonical SOT:** [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md) §1–§2 & [`/root/AAA/federation/organs.yaml`](/root/AAA/federation/organs.yaml)
* **Projection Count:** 18 active projections
* **Key Locations:**
  * `/root/AAA/instructions/topology.md` (fragment rendered to `AGENTS.md`)
  * `/root/AAA/docs/FEDERATION_CONTRACT.md` (§2)
  * `/root/AAA/docs/CALL_MAP.md` (§4)
  * `/root/AAA/docs/ORGAN_AUTHORITY.md` (§1)
  * `/root/AAA/docs/MATRIX.md` (§🗺️ ORGAN MAP)
  * `/root/AAA/docs/MCP_FEDERATION_ZEN.md` (§🔥 Organ Map)
  * `/root/AAA/docs/EXTERNAL_ARCHITECTURE_REFERENCE.md`
  * `/root/arifOS/FEDERATION.md`
  * `/root/arifOS/docs/README-FULL.md`
* **Drift Status:** **CRITICAL DRIFT DETECTED**
  * `CALL_MAP.md` and `MATRIX.md` omit `FRAME (:18085)` and `arifFlow (:7073)`.
  * `MATRIX.md` lists `VAULT999` as an organ with an empty port (category error: VAULT999 is an append-only filesystem ledger, not a network organ).
  * `ORGAN_AUTHORITY.md` (forged 2026-06-14) represents an ancient 6-organ state.
  * `arifOS/FEDERATION.md` still lists outdated permission strings and lacks live metabolic planes.
* **Action:**
  1. Declare `ORGAN.md` / `organs.yaml` as sole SOT.
  2. In `topology.md`, keep as **thin projection** with SOT header comment.
  3. In `CALL_MAP.md`, `FEDERATION_CONTRACT.md`, update to thin projection pointing directly to `ORGAN.md`.
  4. In `MATRIX.md`, remove fake organ row for VAULT999 and add SOT pointer.
  5. In legacy satellite `ORGAN_AUTHORITY.md`, add explicit header: `[SATELLITE PROJECTION - SOT: AAA/docs/ORGAN.md]`.

---

### Object 2: Public MCP Doors & Gateway Surfaces
* **Owner:** AAA / Infra Guardian
* **Canonical SOT:** [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md) §2 & Caddy / Cloudflare Configs
* **Projection Count:** 8 projections
* **Key Locations:**
  * `/root/AAA/instructions/topology.md` (§Public MCP doors)
  * `/root/AAA/docs/EXTERNAL_ARCHITECTURE_REFERENCE.md`
  * `/root/AAA/docs/MCP_FEDERATION_ZEN.md`
  * `/root/arifOS/llms.txt`
  * `/root/arifOS/docs/MCP_SOURCE_OF_TRUTH.md`
* **Drift Status:** **MODERATE DRIFT**
  * `MCP_FEDERATION_ZEN.md` lists `forge.arif-fazil.com/mcp` instead of canonical `mcp.arif-fazil.com/mcp` (`127.0.0.1:7072`).
  * `llms.txt` static generation lags behind live public endpoints.
* **Action:**
  * Harmonize all public door projections to match `ORGAN.md` §2 (`arifos`, `mcp`, `geox`, `wealth`, `well`, `aaa`).
  * Add canonical pointer in `MCP_SOURCE_OF_TRUTH.md` to `AAA/docs/ORGAN.md`.

---

### Object 3: Organ Authority Ceilings & Boundary Matrix
* **Owner:** arifOS Kernel / 888 APEX
* **Canonical SOT:** [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md) §6 (`JUDGE_ONLY`, `EXECUTE_AFTER_SEAL`, `COMPUTE_ONLY`, `REFLECT_ONLY`, `DISPLAY_ONLY`, `METABOLIZE_ONLY`, `ADVISORY_ONLY`)
* **Projection Count:** 12 projections
* **Key Locations:**
  * `/root/AAA/docs/ORGAN_AUTHORITY.md`
  * `/root/AAA/docs/AGENT_BRIEF.md`
  * `/root/AAA/docs/MCP_FEDERATION_ZEN.md` (§Organ Roles)
  * `/root/arifOS/docs/AUTHORITY.md`
  * `/root/arifOS/docs/canon/CANON_APEX_V2/04_ARIFOS_REAL_INTELLIGENCE_KERNEL.md`
* **Drift Status:** **LOW SEMANTIC DRIFT / HIGH TEXTUAL DUPLICATION**
  * The boundaries (GEOX cannot authorize drilling, WEALTH cannot trade without seal, WELL cannot prescribe, arifOS cannot execute, A-FORGE cannot self-authorize) are conceptually rock-solid across all files.
  * However, textual duplication is rife; `ORGAN_AUTHORITY.md` restates the same table 3 times under different headings.
* **Action:**
  * Maintain ceiling tokens in `organs.yaml` as the machine invariant.
  * Point all prose descriptions to `ORGAN.md` §6.

---

### Object 4: Static Tool & Capability Counts
* **Owner:** Live Probes (`now`, `make health`, `scripts/doctor.sh`)
* **Canonical SOT:** **Live Execution Reality** (`live :port/health beats every prose table`)
* **Projection Count:** 22 static tables
* **Key Locations:**
  * `/root/AAA/docs/MCP_TOOL_MAP.md`
  * `/root/AAA/docs/FEDERATION_CODE.md`
  * `/root/AAA/docs/NEXT_HORIZON_SEAL_2026-07-15.md`
  * `/root/AAA/docs/MCP_FEDERATION_ZEN.md` ("Live tools 2026-07-30")
  * `/root/arifOS/docs/AGI_SUBSTRATE_ASSESSMENT.md`
* **Drift Status:** **CHRONIC TEMPORAL DRIFT**
  * Every static table with numbers (e.g. "8 tools", "33 tools", "116 tools") drifts the moment a new tool or MCP decorator is added or pruned.
  * E.g. `MCP_FEDERATION_ZEN.md` is hardcoded to 2026-07-30 counts.
* **Action:**
  * Enforce the rule: **Never cite static tool counts in permanent doctrine.**
  * Add disclaimer to historical docs: `[HISTORICAL SNAPSHOT - NOT SOT]`.
  * Point active queries to `make health` and `AAA/federation/organs.yaml`.

---

### Object 5: Historical & Archived Organ Topologies
* **Owner:** Archive / Archaeology
* **Canonical SOT:** None (Historical Record only)
* **Count:** 50+ files in `archive/`, `forge_work/`, `snapshots/`
* **Key Locations:**
  * `/root/AAA/archive/...`
  * `/root/AAA/docs/FEDERATED_DOMAIN_STRUCTURE_ZEN_v2026.07.15.md`
  * `/root/arifOS/.arifos/federation-topology-map-2026-06-20.md`
  * `/root/arifOS/docs/canon/CANON_APEX_V2/...`
* **Drift Status:** **INTENTIONAL HISTORICAL DRIFT**
  * These files reflect prior evolutionary stages of the federation.
* **Action:**
  * Mark with top banner: `<!-- ARCHIVE / HISTORICAL RECORD · SOT: /root/AAA/docs/ORGAN.md -->`.
  * Do NOT delete (Archive ≠ Delete); preserve historical lineage.

---

## 4. Anti-Inflation & Compression Recommendations

1. **One Authority, One SOT, Many Projections:**
   * Human readers consult [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md).
   * Scripts, daemons, and CI consult [`/root/AAA/federation/organs.yaml`](/root/AAA/federation/organs.yaml).
   * All other markdown files (`CALL_MAP.md`, `MATRIX.md`, `FEDERATION_CONTRACT.md`) must reduce their organ sections to **thin pointers** referencing `ORGAN.md`.
2. **Eliminate Category Confusion:**
   * Remove `VAULT999` and `HERMES` from "Core Organ" tables; classify them properly as `MEMORY (Filesystem)` and `EDGE (Gateway Bridge)`.
3. **Harmonize `CALL_MAP.md` and `MATRIX.md`:**
   * Update `CALL_MAP.md` §4 to include `FRAME (:18085)` as advisory/measurement organ so agents do not suffer split-brain visibility.
4. **No New Registries:**
   * Do not create a new "unified registry" file. The triad (`ORGAN.md` + `organs.yaml` + `MACHINE_MAP.md`) is complete and sufficient.

---

## 5. Conclusion & Verification

```text
Total Files Audited:         110+
Canonical Human SOT:         /root/AAA/docs/ORGAN.md
Canonical Machine SOT:       /root/AAA/federation/organs.yaml
Canonical Node Mesh SOT:     /root/AAA/docs/MACHINE_MAP.md

Drift Identified:            Omission of FRAME (:18085), static tool counts, VAULT999 category error
Resolution Vector:           Collapse projections to thin pointers → Zero new tables → ΔS ≤ 0
```

DITEMPA BUKAN DIBERI.
