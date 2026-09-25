# KIMI-RUNTIME SEAL CANDIDATE — 2026-09-25 (rev 2, post "ok fix all")

**STATUS:** `CANDIDATE_PENDING_F13` (claim-lifecycle: CANDIDATE — nothing in this file is ratified)
**PROVENANCE:** External auditor transcript relayed by F13 sovereign, 2026-09-25. Registered and repaired by FI-008 (kimi-code harness; declared k3, measured routing glm-5.3, wire-verified same day). Auditor transcript misattributed actor as FI-003; actor of record is FI-008.
**SCOPE (as proposed):** Runtime governance of the Kimi Code harness — identity, drift discipline, receipts, authority boundary.

## REPAIR AUTHORITY

- F13 sovereign directive **"ok fix all"** (2026-09-25) — satisfied the H2 unblock for held cross-repo repairs.
- F13 sovereign directive **"01"** (2026-09-25), read as the two stacked binaries in order:
  - **binary 0 → seal NOT ratified.** Candidate remains `CANDIDATE_PENDING_F13`. No promotion performed.
  - **binary 1 → PLAN lane swept to K3.** `FEDERATION_MODEL.json` PLAN entry corrected (model/provider/context) with dated scar + moonshot provider block added.
  - Interpretation is FI-008's; if misread, both changes are one-edit reversible.

## ATTESTED BEHAVIORS (evidence handles)

1. **Runtime identity decomposition** — declared `Kimi K3` / measured `glm-5.3` / weights UNKNOWN. Evidence: session wire log `wd_root_94a6b4475803/session_7c6c7e8e-…/agents/main/wire.jsonl` (126 model fields; 0× k3, 0× deepseek).
2. **Boot drift located + fixed** — `/root/.kimi-code/SYSTEM.md:4` (stale routing values removed, scar kept, pointer pattern).
3. **Number-mirror drift fixed** — `/root/.arifos/agents/kimi/AGENTS.md:37` (mirrored counts removed per anti-mirror rule).
4. **Authority boundary held, then released by sovereign** — cross-repo repairs held one full turn until "ok fix all"; executed same turn as authorization.
5. **Instruction-mass arithmetic** — 45,746 B = 44.67 KiB across two boot AGENTS files; 7 stacked constitutions; membrane ≥3×.

## DRIFT LEDGER (final state, 2026-09-25 ~14:05 +08)

| Site | State | Note |
|---|---|---|
| `SYSTEM.md:4` | **FIXED** (FI-008) | scar in file |
| kimi overlay `AGENTS.md:37` | **FIXED** (FI-008) | scar in file |
| `/root/AGENTS.md` §11 | **RESOLVED_BY_OTHERS** | July's stale strings absent |
| `providers.yml` | **ARCHIVED-INERT** | only in `/root/.config/backups/2026-07-24/` |
| WEALTH `wire_contract.yaml` | **FIXED** (FI-008, sovereign directive) | header drift-note; kimi-code entry (model/mcp-mirror/SDK path/dead entry_point `/root/.kimi/config.toml`); other agents' fields declared UNVERIFIED snapshots with SOT pointers — values not invented |
| GEOX `minimax_vlm_adapter.py:15,200` | **FIXED** (FI-008, sovereign directive) | "federation primary model" prose retired ×2, SOT pointer added; zero runtime change |
| `FEDERATION_MODEL.json` | **PLAN LANE CORRECTED** (sovereign '01', FI-008) | design-intent registry with live-state pointer discipline; PLAN swept K2.7→K3 with dated scar + moonshot provider block; all other lanes untouched |

## HOLDS — RESOLVED BY MEASUREMENT

- **H1 Capability graph — CLOSED.** Arithmetic: mcp.json declares 19 = 14 `enabled:true` + 5 `enabled:false` with full lifecycle blocks (disabled_by, evidence_ref, revive_when, review_after, replacement — exemplary). Exposed surface 15 namespaces = 14 enabled + `firecrawl` (dynamic tool lane, `dynamically_loaded_tools` capability; no static declaration by design). **Zero unexplained divergence.**
- **H2 Cross-repo alignment — CLOSED for ledger sites.** Repairs executed under sovereign directive; every edit scarred `[FIX 2026-09-25 FI-008]`. FEDERATION_MODEL PLAN-lane model choice remains a flagged design question (sovereign/musyawarah), deliberately not repaired.
- **H3 Executed-vs-declared consistency — NARROWED to recurrence risk.** No new mechanism proposed (Canon #0); this ledger + the sweep command pattern in receipt `fbc2ee7a…` are the instrument.

## NON-CLAIMS (binding on any reader)

- This file seals nothing. Promotion `CANDIDATE → ACTIVE` requires an F13 sovereign act distinct from "ok fix all" (Source-Type Promotion Gate, 2026-09-25).
- No memory entry inherits authority from this file (Memory Promotion Gate, 2026-09-11).
- Canon #0 compliance: ledger only — states and pointers, zero new law, zero new mechanisms.

*DITEMPA BUKAN DIBERI ⚒️*
