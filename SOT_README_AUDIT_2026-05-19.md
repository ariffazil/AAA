<!--
SOT-MANIFEST
owner: Arif
last_verified: 2026-05-19
valid_from: 2026-05-19
valid_until: 2026-06-19
confidence: high
scope: /root
epistemic_status: CLAIM
-->

# SOT + README Audit — 2026-05-19

**Auditor:** Kimi Code CLI  
**Scope:** All SOT-MANIFEST files + all README.md files under `/root`  
**Method:** Automated discovery + manual sampling + content freshness check

---

## Part I: SOT Map (30 Files)

All SOT-MANIFEST files discovered under `/root`:

| # | File | LV | VU | Status |
|---|------|-----|-----|--------|
| 1 | `.openclaw/system.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 2 | `.openclaw/workspace/AAA_A2A_ACK_2026-05-19.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 3 | `.openclaw/workspace/AAA_HOLDS_PROTOCOL_v0.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 4 | `.openclaw/workspace/ARCH_OMEGA_MEMORY_v0.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 5 | `.openclaw/workspace/SI_v0_COMMANDS.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 6 | `AGENTS.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 7 | `CONTEXT.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 8 | `MEMORY.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 9 | `SECRETS.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 10 | `SECRET_ROTATION_LEDGER.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 11 | `USER.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 12 | `A-FORGE/deploy/arifOS/RUNBOOK.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 13 | `AAA/wiki/raw/repos/AGENTS_REFERENCE.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 14 | `AAA/wiki/raw/repos/ARCHITECTURE_CONTRAST.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 15 | `AAA/wiki/raw/repos/ARCHITECTURE_SCORECARD.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 16 | `AAA/wiki/raw/repos/ARIF-REGISTRY.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 17 | `arifOS/deploy/RUNBOOK.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 18 | `arifOS/docs/constitutional/annex-anti-sink-invariants.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 19 | `arifOS/docs/thoughts/calhoun-ai-human-earth-2026-05-14.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 20 | `arifOS/docs/WELL_ARIFOS_CONTRACT.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 21 | `arif-sites/specs/SPATIAL_INTELLIGENCE_STATE_MAP.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 22 | `prompts/CLAUDE.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 23 | `WELL/FOUNDATION.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 24 | `WELL/specs/WELL_ARIFOS_CONTRACT.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 25 | `wiki/AGENTS_REFERENCE.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 26 | `wiki/ARCHITECTURE_CONTRAST.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 27 | `wiki/ARCHITECTURE_SCORECARD.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 28 | `wiki/ARIF-REGISTRY.md` | 2026-05-19 | 2026-06-19 | ✅ |
| 29 | `CONFIG/SOT-SEAL-REMEDIATION-LOG-20260505153323.md` | — | — | 📜 Historical (no SOT) |
| 30 | `CONFIG/SOT-SEAL-v1-LOCKED.md` | — | — | 🔒 Locked (no SOT) |

**Wiki duplicates:** `AAA/wiki/raw/repos/*` and `/root/wiki/*` are **synced** (identical content).

---

## Part II: README Audit (Major Projects)

### 🔴 CRITICAL — Stale or Wrong

| File | Issue | Evidence |
|------|-------|----------|
| `/root/README.md` | **STALE** — Version `v2026.05.02.2` | Front door of federation; last updated May 2. No mention of A2A bridge, AAA_HOLDS loop, Ω-MEMORY v0. |
| `/root/arifOS/arifos/README.md` | **VERY STALE** — `2026-04-17` | Claims `mcp.arif-fazil.com/health` returns 200 with 22 tools. Current live test (2026-05-17) shows 16 tools. Also no mention of graphiti, semantic floor, or ml_floors. |
| `/root/AAA/hermes-workspace/README.md` | **WRONG CONTENT** | File is in `AAA/hermes-workspace/` but describes **arifOS constitutional kernel**, not the Hermes workspace. Copy-paste error or never updated after creation. |
| `/root/.openclaw/workspace/README.md` | **MISLEADING** | Says "AAA — Agents · API · Apps" with badge `v2026.05.10`, but this file lives in **OpenClaw workspace**, not AAA repo. Confuses ownership. |

### 🟡 WARNING — Stale Dates

| File | Issue | Evidence |
|------|-------|----------|
| `/root/A-FORGE/arifOS-supabase/README.md` | **STALE** | Date: `2026-04-17`. Version 2.0.0. No SOT. |
| `/root/AAA/workspace/README.md` | **STALE EPOCH** | `EPOCH: 2026-04-25`. Channel says Telegram primary (correct) but GITHUB_TOKEN note says "Session-only". |

### 🟢 OK — Recent or Accurate

| File | Assessment |
|------|-----------|
| `/root/arifOS/README.md` | Recent (2026-05-17 ref). Accurate tool counts. |
| `/root/WEALTH/README.md` | Recent (2026-05-17 ref). Accurate MCP surface description. |
| `/root/WELL/README.md` | Recent (2026-05-17 ref). Accurate MCP surface description. |
| `/root/.secrets/README.md` | Accurate vault documentation. Clear agent rules. |
| `/root/compose/README.md` | Accurate deployment workflow. No dates but describes current topology correctly. |

### ⚪ NO DATE — Cannot Assess Staleness

| File | Notes |
|------|-------|
| `/root/A-FORGE/README.md` | No version/date. Describes ownership correctly. |
| `/root/AAA/README.md` | No version/date. Describes ownership correctly. |
| `/root/arif-sites/README.md` | No version/date. Describes ownership correctly. |
| `/root/geox/README.md` | No version/date. Describes ownership correctly. |
| `/root/geox/geox-gui/README.md` | Minimal — just title + tagline. |
| `/root/HERMES/README.md` | **CONFUSING** — Directory is `HERMES/`, README says "Formerly HERMES. Rebranded to APEX." But this directory ALSO stores Nous Research Hermes runtime data. The README conflates two different things named Hermes. |

### 🔵 External / Satellite

| File | Assessment |
|------|-----------|
| `/root/browser-harness/README.md` | External project (browser-use). Not federation-owned. |
| `/root/msap/README.md` | Minimal. Minimal Sovereign ACK Protocol. No dates. |
| `/root/zkpc/README.md` | Minimal. ZKPC v2 Epoch Chain Circuit. No dates. |
| `/root/arifos-command-center/README.md` | Not audited (satellite). |
| `/root/arifos-model-registry/README.md` | Not audited (satellite). |

---

## Part III: Missing AGENTS.md

**AGENTS.md** provides agent landing instructions per directory. It is **missing** from:

| Directory | Impact |
|-----------|--------|
| `WEALTH/` | Agents landing here have no local rules |
| `WELL/` | Agents landing here have no local rules |
| `HERMES/` | Agents landing here have no local rules |
| `geox/` | Agents landing here have no local rules |
| `compose/` | Agents landing here have no local rules |

**Present in:** `arifOS/`, `A-FORGE/`, `AAA/`, `arif-sites/`, `.openclaw/workspace/`

---

## Part IV: Missing SOT Headers in READMEs

**Zero** README.md files have SOT-MANIFEST headers. This means:
- READMEs can drift silently
- No automatic expiry detection
- No canonical ownership declaration

**Recommendation:** Add SOT headers to top-level READMEs of each major project (arifOS, A-FORGE, AAA, WEALTH, WELL, GEOX, arif-sites, HERMES, compose).

---

## Summary Table

| Project | README | SOT | AGENTS.md | Staleness |
|---------|--------|-----|-----------|-----------|
| `/root` | ✅ | ❌ | ✅ | 🔴 STALE |
| `arifOS` | ✅ | ❌ | ✅ | 🟢 OK |
| `arifOS/arifos` | ✅ | ❌ | — | 🔴 VERY STALE |
| `A-FORGE` | ✅ | ❌ | ✅ | ⚪ No date |
| `AAA` | ✅ | ❌ | ✅ | ⚪ No date |
| `WEALTH` | ✅ | ❌ | ❌ | 🟢 OK |
| `WELL` | ✅ | ❌ | ❌ | 🟢 OK |
| `HERMES` | ✅ | ❌ | ❌ | ⚪ Confusing |
| `arif-sites` | ✅ | ❌ | ✅ | ⚪ No date |
| `geox` | ✅ | ❌ | ❌ | ⚪ No date |
| `compose` | ✅ | ❌ | ❌ | 🟢 OK |

---

## Recommended Actions (Priority Order)

1. **🔴 Fix `/root/README.md`** — Update to v2026.05.19, mention A2A bridge, AAA_HOLDS loop, Ω-MEMORY v0.
2. **🔴 Fix `/root/arifOS/arifos/README.md`** — Update tool counts, mention semantic floor, graphiti, ml_floors.
3. **🔴 Fix `/root/AAA/hermes-workspace/README.md`** — Rewrite to describe Hermes workspace, not arifOS kernel.
4. **🟡 Fix `/root/.openclaw/workspace/README.md`** — Clarify ownership (OpenClaw, not AAA).
5. **🟡 Fix `/root/A-FORGE/arifOS-supabase/README.md`** — Update date or add deprecation notice.
6. **🟡 Create `WEALTH/AGENTS.md`** — Local build/test commands, MCP surface rules.
7. **🟡 Create `WELL/AGENTS.md`** — Local build/test commands, state.json rules.
8. **🟡 Create `geox/AGENTS.md`** — Local build/test commands, Docker/frontend rules.
9. **⚪ Create `HERMES/AGENTS.md`** — Clarify APEX vs Nous Hermes boundary.
10. **⚪ Add SOT headers to all top-level READMEs** — Prevent silent drift.

---

*DITEMPA BUKAN DIBERI — Audits are forged, not assumed.*
