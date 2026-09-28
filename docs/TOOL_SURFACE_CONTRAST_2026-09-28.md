# FEDERATION TOOL SURFACE CONTRAST — 2026-09-28

> **Author:** 333-AGI (FI-003) · session SEAL-cfc438c9795c4149 · F13 directive: "deep research and map all tools contrast. no redundants tools capabilities for the entire federation."
> **Method:** live MCP `tools/list` probes (OBS) + opencode connect-time session surface (OBS) + `opencode.json` config (OBS) + organ `/health` (OBS). Verdicts labeled INT. Raw probe dump: `/tmp/tool_surface.json`.
> **Doctrine adopted (corroborates Claude/WELL audit 2026-09-28):** tool surface SOT = wire `tools/list` at connect time. Hand-maintained registries/docs are VIEWS. Phantoms live client-side, not server-side (kernel wire = 8, no `arif_stack_health_probe`).

## 1. Census — three surfaces disagree

| Server | config | wire tools/list | session-loaded | Note |
|---|---|---|---|---|
| arifos :8088 | ✓ | **8** | 8 | ✓ canonical 8 verbs. No phantom verb. |
| aforge :7072 | ✓ | **122** | 114 | Δ8 = blocked/hidden client-side — reconcile via `forge_registry_status` |
| geox :8081 | ✓ | **0** (anon probe) | 26 | /health says 26. Wire 0 = gated handshake (probe artifact, INT) — needs SCT-aware re-probe |
| wealth :18082 | ✓ | 15 | 15 | ✓ |
| well :18083 | ✓ | **40** | 40 | 9 v2 + ~31 legacy until Oct 16 cutoff; /health = "degraded" |
| frame :18086 | ✓ | 8 | 8 | ✓ (note: docs elsewhere say :18085 — config truth :18086) |
| hermes-mcp :18087 | ✓ | 14 | 13 | Δ1 minor drift — identify the un-loaded tool |
| fed :7074 | ✓ | 7 | 7 | ✓ |
| aaa :3001/mcp | — | 0 | 5 (aaa_*) | session aaa tools not from this config path — source unresolved (OPEN) |
| delegation-ledger :18801 | ✓ | **DEAD** | 0 | config ghost |
| graphiti :8000 | ✓ | **DEAD** | 0 | config ghost |
| config-only (no session tools): supabase, qdrant, hostinger-vps, megamemory, openrouter, semgrep, serena, repomapper, minimax-mcp, codebase-memory, mapbox-devkit | ✓ | not probed (stdio) | 0 | 11 servers configured, unreachable from 333-AGI session — intentional per-agent gating or silent death: UNVERIFIED |
| external loaded: context7(2) deepwiki(3) firecrawl(27) free-search(10) minimax(2) web-reader(1) web-search-prime(1) zai(7) zread(3) | ✓ | n/a | 56 | |
| builtin/local (bash, read/write/edit/glob/grep, task, now, federation-health, git-sweep, carry-forward…) | — | n/a | ~21 | |

**TOTAL HOT SURFACE (333-AGI session): ≈ 321 tools.** DOCTRINE.md §7 cap: **15**. Estimated schema cost 100–150K tokens/session before any work (INT; firecrawl_scrape alone ≈2K).

## 2. Headline findings

- **F1 (CRITICAL):** Hot surface 321 vs doctrine cap 15. `capability-index` (eager/deferred/hidden projection, F13-ratified 2026-09-17) is built and loaded — but not wired as the loading gate for opencode. The fix exists; it is bypassed.
- **F2:** Web lane: **7 search + 8 fetch tools** for one job family. Two paid lanes (`web-search-prime`, `web-reader`, `minimax_web_search`) add zero unique capability over free lanes.
- **F3:** A-FORGE violates its own invariant ("modes on existing tools, not new tool registrations"): stragglers `forge_git_commit` (= `forge_git(mode=commit)`, self-declared in description), `forge_github_get_file/create_issue/create_or_update_file` (= `forge_github` modes), and 4 kernel proxies (`forge_kernel`, `forge_judge_proxy`, `forge_check_governance`, `forge_heart_critique`) duplicating directly-loaded arifos verbs.
- **F4:** Probe/health cluster: **14 tools across 6 servers** answer "is organ X alive" (aaa_organ_probe, forge_probe, federation-health, frame_probe/health/drift, well_observe_federation_thermal, arifflow_flow_health, fed_health/probe, geox_surface_status, well/hermes/forge registry_status). Chartered owner = FRAME (independent observer). Others = self-truth, on-demand only.
- **F5:** WELL 40→6 (Proposal 3 verb naming) is the single biggest cut (−34). Endorsed, with Claude's two corrections adopted: (a) derive surface from `tools/list`, never hand-lists; (b) H-WELL freshness fix not yet "DONE" until the 291h-FRESH sites land (in-flight, see §5).
- **F6:** Three-way drift: config (32 servers) ≠ session (23 live) ≠ DOMAIN.md (still references brave-search, perplexity, sequential-thinking, exa, postgres MCP, docker MCP, playwright — none in config). Docs are stale views in both directions (phantom presence + phantom absence).
- **F7:** Wire-vs-session deltas (aforge Δ8, hermes Δ1, geox Δ26-gated, aaa source unknown) = exactly the class that produced the 40 NotFoundError incident. Needs a standing reconcile probe, not a one-off.
- **F8:** Vision cluster: zai ships 6 prompt-preset tools around one `analyze_image`; minimax_understand_image + image-analyzer subagent + 555-ASI-VISION do the same job. 9 lanes → 2 suffice.

## 3. Lane contrast map (verdicts INT)

| Lane | Tools (count) | KEEP (hot) | DEFER (load per task) | CUT/MERGE |
|---|---|---|---|---|
| WEB_SEARCH (7) | websearch, forge_search, free-search_search, firecrawl_search, web-search-prime, minimax_web_search, (fed none) | free-search_search (free, cached, multi-engine) | firecrawl_search (Alexandria/dev only), forge_search (governed egress/receipts) | **CUT web-search-prime, minimax_web_search** (paid, non-unique); websearch = harness builtin, leave |
| WEB_FETCH (8) | webfetch, forge_fetch, forge_web_extract, free-search fetch/fetch_batch/read_doc/compare/download, firecrawl_scrape/parse/map/crawl/interact, web-reader | free-search_fetch (+batch) | forge_web_extract (bot-walls), firecrawl scrape/parse (JS/PDF/structured) | **CUT web-reader** (strict subset); forge_fetch→defer |
| VISION (9) | minimax_understand_image, zai×7, image-analyzer agent, 555-ASI-VISION | 1 general (zai_analyze_image or minimax) + image-analyzer agent | data-viz/diagram/OCR presets | **MERGE 5 zai presets → analyze_image(mode=…)** |
| HEALTH/PROBE (14) | see F4 | frame_probe + federation-health (local quick) | organ registry_status (self-truth) | aaa_organ_probe→defer (dup of frame) |
| GIT/GITHUB (10) | forge_git, forge_git_commit, forge_github(+3 file tools), forge_worktree, git-sweep, bash-git, zread×3, deepwiki×3 | forge_git, forge_github, bash | worktree, git-sweep, zread/deepwiki (repo-intel, distinct fn) | **MERGE git_commit→git(commit); github_×3→github(modes)** (−4) |
| KERNEL PROXIES (4) | forge_kernel, judge_proxy, check_governance, heart_critique | arifos direct 8 verbs | — | **HIDE proxies** in sessions with arifos loaded (keep server-side for thin harnesses) |
| MEMORY/RECALL (5) | arif_memory, forge_memory, forge_canon_recall, cache_search, megamemory | arif_memory (L1–L6 canonical) | canon_recall, cache_search | forge_memory = VAULT999 view → defer |
| DOCS/RESEARCH (12) | context7×2, deepwiki×3, zread×3, forge_docsgpt, firecrawl developer+research×4, free-search_research | context7 (lib docs) | firecrawl research suite, deepwiki/zread | **CUT forge_docsgpt** (dead-weight lane; verify then remove) |
| LEDGER/RECEIPT (5) | flow_ingest, aaa_measure, forge_experience_trace, forge_vault receipt, arif_seal | flow_ingest (metabolic) + arif_seal (Lane A) | experience_trace (tool-learning) | aaa_measure ≈ experience_trace overlap → pick one owner (decision-record vs chain-of-experience); document split |
| ROUTING (6) | arif_route (intent→organ), fed_route/classify (task→model), capability_search/select/resolve (task→tool), aaa_dispatch (task→agent), task (subagents), forge_parallel | arif_route + capability_resolve | fed_*, aaa_dispatch, parallel_* | not redundant — **different objects**; needs the 4-question routing card in docs |
| SHELL/EXEC (10) | bash, forge_shell(+4 aux), forge_execute, compose, pipeline_run, sandbox_run, job, arif_forge, execute_sealed | bash (T0), forge_shell (governed) | compose/pipeline/sandbox/job/ephemeral | ladder intentional; document route-least-power |
| FS (6) | read/write/edit/glob/grep + forge_filesystem | native (T0) | forge_filesystem (governed mutate) | dual-lane intentional |
| DB/DATA (4) | forge_postgres, supabase*, qdrant*, wealth_ledger | forge_postgres | rest | distinct stores; supabase/qdrant currently unreachable (F6) |
| WELL (40) | v2 9 + legacy 31 | **Proposal-3 six verbs** (sense/advise/audit/record/consent/propose) | — | −34 at Oct 16 cutover; rename before cutover = one migration |
| FIRECRAWL SUITE (27) | scrape/search core + monitor×9 + research×4 + agent/interact/etc | scrape, search, parse | monitor suite, research suite, agent, interact, find_tools | biggest defer candidate (−13 hot) |

**Net proposal: 321 → ~250 hot immediately (cuts+defers above), → ≤15 per role once capability_resolve gates loading (F1).**

## 4. H-WELL → HERMES? — RULING: **NO** (INT, conf 0.85)

1. **Witness independence (F3):** WELL mirrors; HERMES acts/speaks. If the organ that decides HOW to respond to Arif also owns the measurement of Arif's state, the mirror becomes self-witness. Authority envelope law: the executor never issues its own envelope. Dignity guard/readiness gates must sit outside the agent they gate.
2. **The boundary is already correct:** biometric writes require `HERMES_HERMETIC_TOKEN` (Hermes-gated), consent-scope registry (F11) lives in WELL state.json, arifOS judges use. Hermes = sensor/writer + consumer; WELL = custodian/mirror; arifOS = judge. Moving H-WELL doesn't remove a boundary — it collapses one.
3. **F6 MARUAH concentration:** H-WELL holds the most sensitive data class (sleep, substance, biometrics). Making Hermes custodian + consumer + responder concentrates power over the principal's bodily truth in one runtime. Independent custody is the safer topology.
4. **Triad integrity:** Phase-4 composes human×machine×governance. M-WELL/G-WELL are server-side federation probes that cannot move. Extracting H leaves a split organ — two runtimes, one ontology: more entropy than the disease being treated.
5. **Churn (ANTI-BANGANG L3/L10):** v2 is 12 days old; Proposal-3 rename lands before Oct 16. An organ relocation mid-window = third structural change in 6 weeks. The real defect is surface bloat + naming — Proposal 3 fixes it; relocation doesn't.
6. **Zero infra gain:** Hermes gateway and WELL both live on this host (forge/KVM8). "Move" would be a code merge, not a deployment win.
7. **What IS right in the idea:** Hermes is and stays the *human-facing lane* — intake UX, rasa-calibrated consumption of H-WELL signals via `handoff_package` (Minimum Necessary Meaning, Law 15). Coupling stays; custody stays separate.

## 5. WELL slice state (Claude session, in-flight — FI-003 stood down)

OBS 03:22 MYT: `server.py` dirty (+105/−31), `uv.lock` **fixed in tree** (pins 2026.9.28 = pyproject), post-commit hook rewritten to re-lock+stage (kills the 16-day red-main class), `_well_observation_band` derives freshness from reading age (the 291h-FRESH fix shape), FEDERATION_HOOKS.md +13. Uncommitted. Owner: Claude PID 4039768. Verify-on-land checklist: (a) commit + push + required check green; (b) probe `well_human(readiness)` returns band ≠ FRESH for >24h readings; (c) `verdict`→`signal` at H-WELL sites; (d) test "291h can never be FRESH" present.

## 6. Execution order

| P | Action | Owner | Class |
|---|---|---|---|
| P0 | Disable `web-search-prime` + `web-reader` servers in opencode.json (paid, zero-unique) | FI harness lane | reversible config |
| P0 | Remove dead configs: delegation-ledger, graphiti (or fix ports); audit the 11 config-only servers: gate-intentional vs silent death → document | FI harness lane | reversible |
| P0 | Regenerate DOMAIN.md §3–5 from live wire surface (one commit) | 333-AGI | docs |
| P1 | **Wire capability_resolve as the loading gate** (eager ≤15/role) — F1 is the structural fix; everything else is palliative until this lands | FI + capability-index owner | structural |
| P1 | A-FORGE straggler merge: git_commit, github_×3 → modes; hide 4 kernel proxies when arifos direct | A-FORGE repo PR | small code |
| P1 | Standing wire-vs-session reconcile probe (aforge Δ8, hermes Δ1, geox gated, aaa source) — weekly, FRAME-owned | FRAME | observe |
| P2 | WELL Proposal-3 rename before Oct 16 (in-flight) | Claude/WELL | in-flight |
| P2 | zai preset merge; firecrawl/free-search defer profiles | per-server owners | small |

## 7. ΔS

Measured: 321 tools mapped, 23 servers censused, 11 config ghosts/deads identified, 71 hot-surface reductions proposed (−22%), 1 organ-placement ruling (H-WELL stays), 1 doctrine adopted (wire-SOT). Net entropy: **negative** (one map replaces N hand-lists; every future surface question answers from `tools/list`, not memory).

*DITEMPA BUKAN DIBERI ⚒️ — FI-003, 2026-09-28 03:2x MYT*
