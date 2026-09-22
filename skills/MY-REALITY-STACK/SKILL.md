---
id: MY-REALITY-STACK
name: Malaysia Reality Stack — Primary-Source Routing
version: 1.0.0-2026.08.15
description: Route all Malaysia macro/policy/energy/corporate claims through primary government/financial sources using EXISTING federation tools. NO new MCP servers. Hard F2 provenance law for any MY figure.
owner: F13 SOVEREIGN (directive 2026-08-15, external proposal adapted)
risk_tier: low
floor_scope: [F2, F7, F9, F10]
autonomy_tier: T0
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# MY-REALITY-STACK — Malaysia Reality Routing

> **DITEMPA BUKAN DIBERI.** Agents speak of Malaysia only through her own ledgers.
> Public registry: https://arif-fazil.com/world/malaysia/reality-stack/

## THE LAW (non-bypassable)

1. **NO NEW MCP SERVERS.** The external proposal (bnm-mcp, parlimen-mcp) is implemented as THIS SKILL + existing organs, not as new servers. Federation rule: modes on existing tools, not new registrations.
2. **F2 PROVENANCE — THE HARD RULE:** No Malaysia macro figure (OPR, CPI, GDP, FX reserve, energy demand, water level, corporate capex) may be stated without a payload tag from a primary source below, fetched THIS session. Unverifiable → say UNKNOWN, cite nothing.
3. **VECTOR MEMORY:** memory geometry is mathematical — `vector_memory` (embeddings, cosine distance), never biological metaphors. Aligned with F9/F10 anti-anthropomorphism.

## CLAIM CLASS → SOURCE OF RECORD (a lock, not a preference)

Read every claim-class from the body that OWNS it. A news portal is never the source of record
for any row below — it is a pointer to one.

| Claim class | Source of record | Never sufficient alone |
|---|---|---|
| Party / coalition membership, registration, dissolution | **Registrar of Societies (RoS)** under Societies Act 1966 — register entry, RoS letter, or the court reviewing it | A leader's declaration about ANOTHER party's status; a press conference |
| Election result, seat count, turnout | **SPR** `spr.gov.my` · `mysprsemak.spr.gov.my` (result / candidate / roll lookup) | Outlet "unofficial" counts and live blogs |
| Boundary, redelineation, new seats | **SPR** gazetted recommendation + **Federal Gazette** notice | A news summary of the EC's display exercise |
| Statute, ordinance, amendment, commencement | **AGC** `lom.agc.gov.my` · **Federal Gazette** `federalgazette.agc.gov.my` · **Sarawak** `lawnet.sarawak.gov.my` | A ministry press release about the law |
| Ministerial position, written answer, division | **Hansard** `hanpar.parlimen.gov.my` / `parlimen.gov.my` | A reported quote with no Hansard citation |
| Corporate capex / equity / board / privatisation | **Bursa announcements** `bursamalaysia.com/market_information/announcements/company_announcement` + issuer IR `bursa.listedcompany.com` | Analyst note or press write-up |
| Macro, fiscal, monetary | **DOSM** (`open.dosm.gov.my`, `storage.dosm.gov.my`) · **MOF** budget documents · **BNM** `bnm.gov.my/publications` (AR · EMR · FSR) | Any article that pairs two of their figures |
| Gas / petroleum regulatory posture | The governing instrument's own text (PDA 1974 · OMO 1958 · DGO 2016) — see `petronas-petros-shell-dispute` | Political sentiment read as contract |
| Ownership / beneficial ownership | **SSM** (paid e-info) or the filing itself | Inferred control from who appears at events |

**The status rule (scar 2026-09-18).** Where a **registrar** owns a status — membership,
registration, dissolution — that status may be read *only* from the registrar or a court. A party
leader declaring ANOTHER party's status is making a claim about a rule, not reporting the register.
The two diverged live: one coalition president declared a member "automatically out" under a
coalition clause (7 Aug); the coalition **chairman** said the member remained, and the member filed
with RoS (9 Aug). Carrying the first as the state of the world was transcribing the loudest voice,
not reading the record.

Output shape: `CONTESTED — declared by X, contradicted by Y, owner = RoS`. Never a bare status.

**Statement ≠ status.** Every rung below the primary is a claim *about* the primary. A reported
number that names a primary ("BNM said", "per DOSM") still needs that primary opened THIS session
before it is tagged PROBED. The name of a body is not a payload.

## ROUTING TABLE (tool → use)

| Need | Tool (existing) | Pattern |
|---|---|---|
| JSON endpoint pull | `forge_fetch` (mode=json) or `arif_observe(mode=fetch)` | Direct GET, cache TTL default |
| Blocked-from-VPS host (000/403) | SearXNG (`forge_fetch` query=) or browser (`forge_browser_navigate`) | parlimen.gov.my, hanpar, bursa, bernama block DC IPs — route via search cache or browser render |
| Recurring structured pull | `forge_ephemeral` (generate → invoke → retire) | Temporary tool, dissolves after mission — NOT a new server |
| News validation | `hermes_fact_check` / `arif_observe(mode=search)` | Wire claim → primary source cross-check before memory write |
| Figures into reasoning | `arif_think` after payload in context | Hooded-engine rule: no payload in window = no capability |

## PRIMARY SOURCES (probed 2026-08-15, from VPS)

### 1 · Fiscal / Macro / Financial
- **BNM Open API** `https://api.bnm.gov.my` — OPR, base rates, FX, interbank, gov bond, consumer alerts; KijangAPI gold at `/v2/kijang`. Requires registered `app` header token. Domain LIVE but 404s unauthenticated/DC-IP — register token, or route via search.
- **BNM portal** `https://www.bnm.gov.my` — 200 OK. Statements, MCPM minutes, FX policy.
- **OpenDOSM** `https://open.dosm.gov.my` — 200 OK. Official statistics dashboard (CPI, labour force, trade).
- **DOSM data lake** `https://storage.dosm.gov.my` — 200 OK. Dataset JSON/CSV releases.
- **data.gov.my** `https://data.gov.my` — CKAN paths currently 404 (post-migration drift) — use OpenDOSM until stable.

### 2 · Legislative
- **Hansard** `https://hanpar.parlimen.gov.my` + `https://www.parlimen.gov.my` — 000 from VPS (geo-block). Route via SearXNG/browser. Written answers (jawapan bertulis) = minister-level primary record.
- **LOM (AGC)** `https://lom.agc.gov.my` — 200 OK. Acts, amendments. Federal Gazette via AGC portal.

### 3 · Energy / Water / Earth
- **Suruhanjaya Tenaga** `https://www.st.gov.my` — 200 OK. Grid data, MSO (Malaysia Energy Statistics Outlook), coal retirement schedule, commission rulings.
- **JPS/DID flood+river telemetry** `https://publicinfobanjir.water.gov.my` — 200 OK. Live river level/rainfall stations (Johor basin cases).
- **JPS hydrology portal** `https://hydrology.water.gov.my` — 000 from VPS; use publicinfobanjir mirror.
- **PETRONAS/MPM** — NO public API (INT). Production/reserves: PTG annual reports (PDF via st/bnm-style fetch) + EIA international for cross-check. Never fabricate well/block names — GEOX `geox_basin` for geometry ground-truth.
- **GEOX organ** — all geometry claims (basin boundaries, block coords, well inventory) route through GEOX MCP, not memory.

### 4 · Corporate
- **Bursa announcements** `https://www.bursamalaysia.com` — 403 bot-wall from VPS; browser-render or SearXNG cache. Announcements = capex/equity/board primary record.
- **SSM** `https://www.ssm.com.my` — 302 alive; UBO lookups are PAID (e-info account). Flag as gated; never infer ownership without document.

### 5 · Electoral & Registry (primary for every status claim)
- **SPR / Election Commission** `https://spr.gov.my` — official results, candidate lists, redelineation recommendations, state election pages. `https://mysprsemak.spr.gov.my` — public result / candidate / roll lookup.
- **Registrar of Societies (RoS)** — party and coalition registration under Societies Act 1966. No clean public API: route via the body's own letter or statement, the court reviewing it, or the Gazette notice. A registration dispute is CONTESTED until the Registrar or a court decides — never settled by which side spoke last, or loudest, or which wing is larger.
- **Federal Gazette** `http://www.federalgazette.agc.gov.my` — PU(A)/PU(B) notices; the instrument that makes an amendment, an appointment or a redelineation *effective*.
- **AGC Laws of Malaysia** `https://lom.agc.gov.my` — consolidating Acts.
- **Sarawak Laws Online** `https://lawnet.sarawak.gov.my` — state ordinances (OMO 1958, DGO 2016). For any Borneo petroleum claim the state's own law library outranks every wire.

### 6 · News Wires (secondary until primary-anchored)
- The Edge `https://www.theedgemarkets.com` (301→200), Malaysiakini RSS `https://www.malaysikini.com/rss/` (301), Bernama RSS path currently unreachable from VPS — use site search. **Wire text = INT until anchored to a §1–§5 payload.**

**Hard demotion — wire text is a pointer, never the payload.** Two failures get zero tolerance:

- **A wire's PAIRING of two figures is an argument, not a fact.** When an article juxtaposes two
  numbers that came from different bodies, cite each to its own document. The juxtaposition enters
  your brief as though the source asserted the relationship, and then you sign it.
- **A wire's CHARACTERISATION of a legal or registral status is a paraphrase.** Go to the
  instrument, the registrar, or the court. A quote is testimony about what someone said; it is
  never a read of the register.

## ANTI-HALLUCINATION CONTRACT

- Sandakan-class well-name errors → GEOX ground-truth or UNKNOWN.
- Macro figure without payload → UNKNOWN + "fetch first via MY-REALITY-STACK".
- News claim without wire provenance → not eligible for memory write (any tier).
