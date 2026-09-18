# arif-fazil.com × MCP Tool Stack — Gap Framing

**Forged:** 2026-09-18 · **Authority:** T3 pending F13 · **Status:** AWAITING_SOVEREIGN
**Forged by:** FI-008 (kimi-code / k3 lane) under /root/arif-fazil.com/AGENTS.md
**Receipts:** `/root/AAA/forensics/arif-fazil-inventory-2026-09-18.json`, `/root/AAA/forensics/aaa-skill-inventory-2026-09-18.json`

---

## TL;DR

Five things matter:

1. The site **already declares 17 MCP tools** in `/root/arif-fazil.com/dist/.well-known/mcp.json`, but the live code surface behind `mcp.arif-fazil.com/mcp` is the canonical 8 verbs (kimi-code sees 9, OpenCode sees 25 — three different surfaces, none reconciled to the public contract). Truth-class drift, low blast.
2. The **territory contract is under-declared**: `territories.json` v1.1.0 lists 4 territories (earth/economics/world/doctrine); the site ships ~10 visible territories with claims. Discovery is incomplete.
3. **Zero JSON-LD provenance** in /vitals, /earth, /makcikgpt HTML/JSX. These territories make MCP-shaped claims (geox.macrostrat, geox.prospect, geox.wells, wealth.capital) but the claims are narrative, not discoverable. This is the high-leverage gap.
4. **WELL registry is in REGISTRY_DRIFT**: 40 well_* tools registered, 19 exported, 10 canonical callable, 33 internal aliases (`well_000_init`..`well_999_vault`). Half the registry is on the wrong wire.
5. **Skill depth mismatch**: 218 active SKILL.md, but no skill for territory-provenance assertion, no skill for flow_mint discipline, no `core-constitutional-fundamentals`. Coverage is wide, attention-kill is thin.

---

## Zone 1 — Site ↔ MCP Catalog Mapping

| Territory | Claim (page-level) | Expected MCP Tool | Discoverable? | Receipt Path | Gap |
|---|---|---|---|---|---|
| `/vitals` | 9 tripwires (BODY/SPINE/SOUL), W-007 NOC calibration, Pacemaker panel | `mcp__wealth__capital_health`, `mcp__wealth__capital_polix`, `mcp__wealth__capital_entropy`, `mcp__wealth__capital_market` | **NO** | sites/arif-fazil.com/dist/vitals/index.html | **HIGH** — narrative claims without discoverable provenance. Fix path: PROP-2026-09-18 |
| `/earth` | geo.macrostrat pipe-verified; geox.prospect 888_HOLD; geox.wells witness chain intact; wealth.capital human-in-loop | `mcp__geox__geox_basin`, `mcp__geox__geox_prospect`, `mcp__geox__geox_well`, `mcp__geox__geox_petrophysics`, `mcp__wealth__capital_judge_handoff` | **NO** | sites/arif-fazil.com/dist/earth/index.html | **HIGH** — five cockpits claim MCP behavior; zero JSON-LD |
| `/makcikgpt` | 30 articles, seal 999 each, BM civic intelligence | `mcp__hermes__hermes_makcik_render`, `mcp__hermes__hermes_claim_validate`, `mcp__hermes__hermes_contradiction_scan` | **NO** (no dist output found) | (source: src/data/makcikgpt/*; prerender-articles.cjs) | **MEDIUM** — no discoverable voice-law receipt per article |
| `/world` | civic journalism + commodity dashboards | `mcp__wealth__capital_market`, `mcp__hermes__hermes_makcik_render` | partial (territories.json declares) | dist/.well-known/territories.json | **LOW** — covered by territories.json |
| `/world/2027` | 5 engines of chaos, 19 graded receipts, permanent citations | `mcp__wealth__capital_civx`, `mcp__wealth__capital_entropy` | **NO** | content/world/2027/ (cited in llms.txt, no JSON-LD) | **MEDIUM** — 19 receipts lack machine-checkable verification |
| `/999` | SEAL ledger, claims publicly verifiable | `mcp__arifos__arif_seal`, `mcp__aforge__forge_fingerprint_check`, `mcp__aforge__forge_runtime_verify`, `mcp__aforge__forge_verify_timeline` | **NO** | dist/999/* | **HIGH** — 999 proof-chamber claims need receipt-bound verification |
| `/000` | sovereign human root, ZKPC | `mcp__arifos__arif_seal`, `mcp__arifos__arif_judge`, `mcp__arifos__arif_memory` | **NO** | (no dist entry found in this snapshot) | **MEDIUM** |
| `/human` | agent contract | all 8 canonical arifOS verbs | **YES** | dist/.well-known/agent.json + dist/human/index.html | none |
| `/institution` | briefing path | `mcp__arifos__arif_observe`, `mcp__arifos__arif_think`, `mcp__hermes__hermes_handoff_package` | **NO** | dist/institution* | **MEDIUM** |
| `/vitals/data` (claim-gate-report.json) | machine-readable CrisisAlert | n/a | **YES** | dist/vitals/claim-gate-report.json | none — actually a positive outlier |
| `/malaysia` | sovereign intelligence dossier | `mcp__wealth__capital_civx`, `mcp__wealth__capital_polix` | **NO** | dist/malaysia/index.html | **MEDIUM** |
| `/doctrine`, `/missions`, `/work` | constitutional floors, missions, well record | n/a (informational) | partial (territories.json) | dist/.well-known/territories.json | **LOW** |
| `/.well-known/agent.json` | canonical MCP contract | n/a | **YES** | dist/.well-known/agent.json (2.6K, version 1.4.0) | tools_summary (17) disagrees with arifOS canonical (8) |
| `/.well-known/mcp.json` | MCP manifest | `mcp__arifos__arif_*` (8 verbs) | **YES** | dist/.well-known/mcp.json | tools_summary stale |
| `/.well-known/capabilities.json` | federated capability registry | webmcp + mcp + a2a + http | **YES** | dist/.well-known/capabilities.json (7.2K) | generated 2026-07-15 — 62 days stale |
| `/.well-known/territories.json` | territory contract | n/a | **YES** (but incomplete) | dist/.well-known/territories.json | only 4 of ~10 territories declared |

**Zone 1 verdict:** **3 territories at HIGH severity need a single bounded change**: /vitals, /earth, /999. Together they cover the entire F2/F11/F13 evidence-bearing story of the site.

---

## Zone 2 — AAA Skills ↔ MCP Tools Mapping

Scoring on (a) tool catalog cited, (b) kill-switch presence, (c) F11/F13 reference, (d) reversibility class.

| Skill (representative) | Expected Tool Categories | Tool Catalog Cited? | Kill-Switch | F11/F13 Ref | Reversibility | Notes |
|---|---|---|---|---|---|---|
| `agi-agentic-web-delivery` | all MCP tools named in receipts | partial | unknown | yes (DoE convention) | reversible (read mostly) | needs 'MCP canonical surface' section added |
| `forge-agentic-web-builder` | `mcp__aforge__forge_*`, mcp arifos routers | partial | partial (T3 HOLD gates) | yes | reversible | already referenced in /root/arif-fazil.com/AGENTS.md |
| `forge-musyawarah-gotong` | `mcp__arifos__arif_init`, `arif_think`, `arif_judge` | yes (designed for) | yes (sabar cooling gate) | yes | reversible | model template |
| `arifos-eight-verb-canonical` | all 8 verbs | yes (definitionally) | yes (verb-by-verb) | yes | reversible | canonical reference |
| `arifos-kernel-zen-audit` | audit verbs | yes | yes | yes | reversible | strong |
| `geox-basin-evaluation` | `mcp__geox__geox_basin` | yes | partial | unknown | reversible | organ-aligned |
| `geox-claim-falsification` | `mcp__geox__geox_claim` | yes | yes (popperian falsify) | partial | reversible | strong |
| `geox-prospect-evaluation` | `mcp__geox__geox_prospect` | yes | partial | unknown | REVERSIBLE_PRE_SEAL | organ-aligned, prior 888_HOLD |
| `wealth-claim-state` | `mcp__wealth__capital_*` | partial | unknown | unknown | partial | needs depth |
| `xauusd-trading` | `mcp__wealth__capital_indicator/backtest/entry_plan` | yes | partial | unknown | reversible | mature |
| `malaysia-reality-interface` | `mcp__wealth__capital_civx/polix/entropy` | unknown | unknown | partial | irreversible-sensitive | NICHE |
| `civic-publishing` | `mcp__hermes__hermes_makcik_render` | partial | unknown | partial | irreversible (publication) | needs F13-bound gates |
| `arifos-auto-memory` | memory verbs | yes | yes | yes | reversible | claude-code-federation bound |
| `counseling`, `ped-hormone-advisory`, `human-state-estimation` | `mcp__well__well_*` | partial | unknown | partial | non-diagnostic | depth-first, not breadth |
| `hermes-telegram-stack-zen` | `mcp__hermes__hermes_*` | yes | yes | yes | reversible | strong |
| `aaa-pdf-voice-protocol`, `aaa-audio-qualia-doctrine` | well + hermes | partial | unknown | partial | reversible | niche quality |
| `verify-gate`, `verify-pages` (proposed) | web_zen, caddy validate | yes | yes | yes | reversible | needed |
| **`(missing)` territory-provenance-assertion** | `mcp__geox__geox_claim` + `mcp__hermes__hermes_*` + WebMCP | proposed | proposed | proposed | reversible | **DOES NOT EXIST** — this is the gap |
| **`(missing)` flow-mint-discipline** | `mcp__arifFlow__flow_ingest` | proposed | yes | yes | reversible | **DOES NOT EXIST** — this is the gap |
| **`(missing)` site-deploy-receipt-parser** | web_zen + caddy + nuclei + assertion gate | proposed | yes | yes | reversible | **DOES NOT EXIST** — gates `make verify-pages` |
| **`(missing)` federation-onboarding`** | all 8 verbs + 7 organs + 13 floors + 6 missions | proposed | n/a | yes | reversible | **DOES NOT EXIST** — every new agent needs this |

**Zone 2 verdict:** **4 SKILL.md files needed**, none exist. Highest leverage: `territory-provenance-assertion` directly addresses the user's ask ("apply MCP tools to improve sites"). Second: `flow-mint-discipline` (FQ governance).

---

## Zone 3 — Cross-Zone HIGH-Leverage Bridges

A **HIGH-leverage bridge** = a fix that closes a gap in BOTH Zone 1 and Zone 2 simultaneously.

### Bridge 1: Add JSON-LD provenance to /vitals, /earth, /999 + write `territory-provenance-assertion` skill

- Zone 1: territory pages that make MCP-shaped claims become machine-verifiable
- Zone 2: agent gains a reusable skill to assert provenance on any future territory
- Cost: 2 hours bounded forge work (PROP-2026-09-18 already drafted at `/root/arif-fazil.com/forge_work/proposals/2026-09-18-site-mcp-provenance/`)
- Risk: low (read-mostly JSON-LD additions; no claim-score change)
- Reversibility: full

### Bridge 2: Reconcile `mcp.json` tools_summary (17) with arifOS canonical (8) + add `canonical_tools` field

- Zone 1: discovery surface becomes honest; agents know exactly which 8 verbs to call
- Zone 2: every agent that calls `arif_route` no longer has to guess
- Cost: 30-minute config change + generate-discovery.cjs regen
- Risk: low (additive)
- Reversibility: full

### Bridge 3: Mint `flow-mint-discipline` skill + wire to all 8 canonical verbs' first call

- Zone 1: every page that consumes an MCP answer gets a FlowReceipt for FQ tracking
- Zone 2: skill becomes the default agentic discipline
- Cost: 1 hour skill authoring + 30 min wiring
- Risk: low (observational, no execution change)
- Reversibility: full

### Bridge 4: Update `territories.json` to declare 10 territories (add vitals, makcikgpt, malaysia, malaysia-vitals, world-2027, 000, 999, missions, doctrine, work, plus existing 4)

- Zone 1: discovery completeness
- Zone 2: agents can do `if in territories: claims_have_provenance else: skip`
- Cost: 15 min JSON edit
- Risk: low (additive)
- Reversibility: full

### Bridge 5 (F13-bound): Decide if /vitals dossier is published as a **verifiable witness** vs **interpretive treatise**

- Zone 1: changes how /vitals self-describes
- Zone 2: changes which `arif_judge` verdicts route through it
- Cost: **F13 binary choice — single bit**
- Risk: high (sets the constitutional posture for the whole site)
- Reversibility: full (forward-only declarations)

---

## Gaps requiring F13 decision (architecture · money · irreversible)

These must wait for Arif:

1. **/vitals posture** (Bridge 5 above) — is this a witness ledger or a public-policy work? Both are defensible. The decision changes the `verdict` shape on 9 tripwires.
2. **WELL registry_drift resolution path** — collapse or expose? 30+ tools currently invisible. Moving them public expands the agent surface but also the attack surface.
3. **Antigravity skills canonicalization** — 19 skills in `/root/AAA/registries/antigravity/skills/*` are external-harness-bound. Promote to canonical / root / sandbox?
4. **n_skills 218 → governance budget** — should the skill library itself be auditable per Attention-Kill F13 (2026-09-11)? Each SKILL.md is a doctrine without a kill unless proven otherwise. This is an **organism-wide audit**, not a single fix. **F13-bound.**
5. **/a2a 404 stay-or-open?** — currently 17-byte 404 per agentic-web/DEPLOYMENT-POLICY.md. Opening = external contract; staying = local-first. Currently unspecified.

---

## Gaps safely executable (reversible, no authority expansion)

Agents can pick these up without F13:

1. Update `territories.json` to declare 10 territories (Bridge 4)
2. Reconcile `mcp.json` tools_summary with arifOS canonical (Bridge 2)
3. Author 4 missing SKILL.md stubs (`territory-provenance-assertion`, `flow-mint-discipline`, `site-deploy-receipt-parser`, `federation-onboarding`)
4. Generate the JSON-LD provenance snippet template (for Bridge 1)
5. Regenerate `llms.txt` and `capabilities.json` against current federation state
6. Add a `make receipt-for-f13` Makefile target that emits a sealed-style summary
7. Add `forensic-audit-trail` to `forge_work/proposals/` so each proposal's edits become machine-traceable

---

## Verification receipts

- [x] **frame_probe (T-1 evidence)** — 10 organs probed at 2026-09-18T07:29:31Z; arifos degraded, all others healthy or ok — receipt in `mcp__frame__frame_probe`
- [x] **fq health (T0)** — federation FQ = 1.073, vector verdict HEURISTIC_ADVISORY — receipt in `mcp__arifFlow__flow_health`
- [x] **well_observe_federation_thermal (M-WELL)** — same 10 organs, weakest = arifos, route = RECOVER — receipt in `mcp__well__well_observe_federation_thermal`
- [x] **well_registry_status (registry reality)** — verdict REGISTRY_DRIFT, 40/19/10/33 — receipt in `mcp__well__well_registry_status`
- [x] **MAKE verify-pages (T1)** — not invoked in this forge pass; deferred to the bounded forge work per agent / deploy gate mandate (NEVER run whole deploy)
- [ ] **forge_runtime_verify (T2)** — pending execution by future T3 agent that picks up PROP-2026-09-18
- [ ] **frame_rsi_verify (T3)** — pending RSI integrity check on the bounded edit set

---

## Discoveries NOT in original ask (honest accounting)

1. **The site has 3 MCP truth surfaces** (mcp.json says 17 tools, arifOS canonical says 8, ROOT_AGENT_CONFIG says 25 via OpenCode) — none reconcile. F2 risk.
2. **The 2026-08-03 deploy gate incident** still ships: `make verify-pages` is the non-bypassable artifact from a 49-page-404 incident. Any forge work must respect it.
3. **`xxx-webmaster` MASTER doc** mentions a 7-loop automation pipeline + 53 public surfaces — far more than the 4 territories that territories.json declares.
4. **The "Phase 3" phase metadata** (Lebih Bijaksana / Lebih Arif / Penuh Clarity) — federation is mid-phase. Boundaries are still moving. Don't over-canonicalize.

---

## Operator attention estimate

**Read this file:** ≤90s
**Decide on the 5 HIGH-leverage bridges:** ≤5 min
**Sign-off on /vitals posture (F13 binary):** ≤60s
**Then a future agent can pick up PROP-2026-09-18 + the 4 SKILL.md stubs in ≤8 hours bounded work**

---

DITEMPA BUKAN DIBERI · forged, not given.
