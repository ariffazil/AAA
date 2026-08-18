# Canonical pointers

| Where | What |
|---|---|
| `/root/CLAUDE.md` | AAA-grade executor doctrine (EUREKA 6-plane, binding) |
| `/root/AAA/docs/ORGAN.md` | **Canonical topology SOT** (human map) |
| `/root/AAA/federation/organs.yaml` | **Machine SOT** (organs, ports, ceilings) |
| `/root/AAA/federation/workspace.yaml` | **Workspace topology** (fragments, renders, symlinks — monorepo pattern) |
| `/root/AAA/prompts/INIT.md` | **Boot prompt** — Trinity-33 · RSI · Constitutional Friction |
| `/root/AAA/prompts/SEAL.md` | **Exit prompt** — two-lane SEAL/RECEIPT |
| `/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` | Federation-wide Zen (supersedes per-runtime AGENTS.md where conflict) |
| `/root/AAA/governance/QQQ_RECOMMENDATION_PROTOCOL.md` | QQQ doctrine |
| `/root/AAA/governance/AGENCY_LEVELS.md` | Seven-agent-contract + L0–L6 ladder |
| `/root/AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` | EUREKA architecture |
| `/root/AAA/docs/INVARIANTS.md` | 7 Physics + 7 Zen (AAA-scope agent behavior) |
| `/root/AAA/docs/deprecation-registry.json` | Zombie tool/contract registry |
| `/root/arifOS/GENESIS/000_KERNEL_CANON.md` | Constitutional kernel canon root |
| `/root/arifOS/GENESIS/FLOOR_TABLE.json` | **Canonical F1–F13 definitions** |
| `/root/arifOS/GENESIS/INVARIANTS.md` | MCP-level constitutional physics |
| `/root/RUNBOOK.md` | Restart / health / rollback |
| `/root/.secrets/INDEX.md` · `/root/.secrets/kunci-root.env` | Secrets vault index + golden key (`kunci-mas.env` is an alias) |
| `/root/.local/share/arifos/carry_forward.json` | **Live** session state |
| `/root/VAULT999` | Append-only sealed receipts |
| `/root/AAA/instructions/` | **Canonical instruction fragments** — edit these, not the generated output |
| `/root/scripts/render-agents.sh` | **Fragment composer** — generates AGENTS.md + adapter files |
| `/root/scripts/doctor.sh` | **Federation health dashboard** — unified probe |
| `/root/AAA/governance/ARIF_FLOW_METABOLIC_PLANE.md` | **Plane SOT** — 10 roles · 6 SOTs · metabolism. `FLOW_GRAPH` not minted |
| `/root/AAA/governance/SIX_CONSTITUTIONAL_LEDGERS.md` | Six ledgers (LAW STATE BRAIN CAPS TOOLS SKILLS) |
| `/root/AAA/terminal/BOOT.md` | Clerk contract — inherit `state.json`, increment X |

## Sketchpad & Receipts (canonical, 2026-08-15)

> **Single sketchpad:** `/root/forge_work`. No parallel roots.
> (Pre-consolidation `AAA/forge_work` quarantined 2026-08-15 → `/root/forge_work/_quarantine/aaa-forge-work-preconsolidation-20260815`.)

| Layer | Convention | Status |
|---|---|---|
| Working dir | `/root/forge_work/YYYY-MM-DD-<topic>/` | ✅ canonical |
| Cross-cutting drafts | `/root/forge_work/_drafts/` | ✅ canonical |
| Named receipts | `YYYY-MM-DD-FI-XXX-<slug>.md` at `/root/forge_work/` root | ✅ canonical (organic winner) |
| Session ledger | append to `/root/forge_work/<fi>-sessions/sessions.jsonl` | ✅ canonical |
| ~~`_receipts/` container~~ | deprecated 2026-08-15 (agents never adopted it) | 🪦 |
| Promotion | `forge_canonize` → `/root/forge_work/CANON/` (SHA256 sidecar) → `arif_seal` → VAULT999 | ✅ path exists; receipts ≠ canon artifacts |

Decay: hot → `_archive/` → `_cold-storage/`/`_cold_2026-Q3/` → `_tombstone/`. `_quarantine/` holds 7-day-grace isolates.

## AAA Tool Rights Policy

> **Canonical:** `/root/AAA/governance/AAA_TOOL_RIGHTS_POLICY.md`
> **Axiom:** Basic rights are governed pathways, not direct possession of tools.

| Role | Tool Doctrine |
|------|---------------|
| 333-AGI | Constructive tools under A-FORGE gate |
| 555-ASI | Read-only or sandboxed verification tools |
| 888-APEX | No mutation tools directly |
| A-FORGE | Execute only after governed authorization |
| Kernel | Defines boundaries and fail-closed exits |

## FQ TRUTH (metabolism)

```
Clerk card:     /root/AAA/terminal/state.json   (hero already thought)
Hero/doctor:    arifFlow :7073/health  → vector.diagnosis
Cache:          /root/AAA/state/flow_state.json  (TTL 15 min)
```

Clerks do **not** curl `:7073` at init. Hero is the only thinker.  
**Never SEAL high-stakes work on cache alone.**

## Skill Mesh & MCP Testing (2026-08-08)

| Where | What |
|---|---|
| `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` | **Skill SOT** — 95 logical skills, 3-layer-3-axis |
| `/root/AAA/skills/SKILL_ALIAS_TABLE.json` | **Alias table** — 166 rows (V3 short name → disk) |
| `/root/AAA/skills/CONTRAST_ANALYSIS_2026-08-08.md` | **Zen contrast report** — 10-surface audit template |
| `/root/AAA/skills/scripts/skill-mesh-sync.sh` | Mesh sync — grok/claude/codex/opencode symlinks |
| `/root/AAA/skills/AUDIT-recursive-audit/` | **v2.0** multi-surface audit — drift/dual-name detection |
| `/root/AAA/skills/FORGE-mcp-testing/` | **MCP testing doctrine** — use MCPJam Inspector, not coding agents |
| `http://127.0.0.1:6274` | **MCPJam Inspector** — local test/debug/evals for any MCP server |
| `100.64.0.2:6274` | MCPJam via Tailscale (Arif's Windows) |
| `https://stateless.mcpjam.com/mcp` | Stateless MCP compliance server (protocol 2026-07-28) |

**Skill mesh rule:** AAA is the catalog. Harnesses are views. Edit `/root/AAA/skills/`, run `skill-mesh-sync.sh --apply`. Kimi & hermes are copy-based — mirror manually after AAA changes.
