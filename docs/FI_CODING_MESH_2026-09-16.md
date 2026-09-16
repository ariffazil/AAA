<!-- FI_CODING_MESH · 2026-09-16T02:2xZ · 333-AGI SEAL-6ce0ea8cd0174aa9 -->
<!-- Companion to: SKILL_MESH_ALIGNMENT_2026-09-16.md · supersedes §5/§8 of TOOLBENCH_3WAY_CONTRAST.md (2026-07-18) -->

# FI CODING MESH — Agentic Contrast & Skill Compilation
> Scope: the 7 FI coding harnesses. Skills + health from live probes, not prose.

## 1 · Live mesh health (SOT `/run/arifos/mesh-health.json`, refreshed 2026-09-16T02:20:44Z)

| Harness | State | Latency | Note |
|---|---|---|---|
| claude FI-002 | PASS | 6s | fastest responder |
| codex | PASS | 16s | |
| opencode (333-AGI) | PASS | 21s | |
| kimi FI-008 | PASS | 23s | upgraded 0.43.1 today 04:43Z |
| qwen FI-003 | PASS | 33s | |
| grok | EXTERNAL | 4s | billing/quota wall — money-gated, not defective |
| gemini | EXTERNAL | 90s | billing/quota wall — money-gated, not defective |

**History note:** prior SOT (2026-09-15T19:17Z) showed kimi+claude FAIL. Both were STALE —
kimi's `--yolo` conflict died with the 0.43.1 upgrade; claude now passes unmodified. Re-run by
333-AGI this session; zero config change was needed. Lesson: sensor state has a TTL — re-probe
before repairing (probe-before-panic holds for sensors too).

## 2 · Agentic contrast (coding-lens)

| | opencode | kimi FI-008 | claude FI-002 | codex | qwen FI-003 |
|---|---|---|---|---|---|
| Role | Forger / AGI workhorse (333 carrier) | Most-governed single-model | Anthropic-protocol bridge | Focused exec | Broad multi-domain |
| Providers | 18 | 1 (+OAuth wrapper) | DeepSeek via Anthropic proto | 1 | QwenCloud family |
| Subagents w/ rotation | 6 (333/555/555V/888/image/dispatch) | 2 (one model) | 2 + fork | — | — |
| Hooks/gates | 8 | 12 bash (43 rule mentions in 38KB config) | allow-list era begun (federation MCPs allowed) | minimal | minimal |
| Skill visibility | AAA 506 + overlay 31 | AAA 506 + .kimi-code extras | AAA 506 | AAA 506 | **own 9 ONLY** |
| Sweet spot | Heterogeneous builds, cross-organ | Governed forge runs, K3 native | Backend/infra, fastest | Fast bounded edits | Qwen-native + MY-reality |

## 3 · Skill compilation per harness

- **Shared (5 symlinked harnesses):** AAA canonical 506 = substrate 7 + knowledge 4 + dev-band 17
  (dev-github, dev-ci-diagnose, dev-pr-review, dev-pr-governance, dev-repo-audit, dev-fastapi,
  dev-db-stack, dev-web-builder, …) + forge/ops/meta bands.
- **opencode-only overlay** (`.config/opencode/skills`, 31): opencode-forge, opencode-init,
  opencode-meta-mesa, opencode-zen-router, opencode-agentic-state, opencode-propose-seal,
  FORGE-mcp-testing, FORGE-mcp-probe, institutional-epistemic-sink-forensics, …
  → runtime-specific primitives; legitimate scope, but UNREGISTERED in registry V3.
- **kimi extras:** `.kimi-code/skills` (kimi-architect-* ×6, KIMI_RSI_INIT, KIMI_HANDOVER,
  skill-mesh tools incl. the stale copy of skill-mesh-sync.sh).
- **qwen (the blindspot):** only 9 — google-workspace-gws, human-state-estimation,
  malaysia-reality-interface, mcp-shopping-list-2026-09, AGI-nusantara-substrate,
  ASI-agent-invariants, organ-capability-map, youtube-extraction-datacenter-ip ×2
  (one is a nested dir-in-dir ghost). **No dev-band. No substrate core.** qwen codes without
  the federation's coding doctrine.
- **HERMES→FI coding leakage (true case-insensitive HERMES-only):** 30 total; coding-relevant
  only **forge-skill-linter**, **forge-verify-runtime** (+opencode-propose-seal which dups the
  overlay). The FORGE-* mass in Hermes is case-pair shadowing of existing AAA skills, not new
  capability.

## 4 · Improvement backlog (coding agents)

| # | Item | Class | Status |
|---|---|---|---|
| 1 | Sentinel TTL discipline — mesh-health SOT can be hours stale; re-probe before any repair claim | Process | **DONE this session** (re-ran, 5/7 live) |
| 2 | Case-pair unification (≈431 collisions; e.g. `FORGE-github-ops`↔`forge-github-ops`) — one owner per coding skill | Mesh S4 | staged, needs Hermes-loader symlink canary |
| 3 | qwen blindspot — fold `.qwen/skills` into mesh (its 9 = candidates for canonical) or ratify as scoped profile | Mesh S5 | staged |
| 4 | Overlay governance — register `.config/opencode/skills` 31 in registry V3 as `opencode-runtime` band | Mesh S5 | staged |
| 5 | Retire stale contrast doc §5/§8 (claude permission gap already fixed upstream) | Docs | superseded pointer added |
| 6 | Negative-proof skill-creation gate — ALREADY LAW (Seven Laws, F13_RATIFIED 2026-09-16); enforcement = census + symbol-probe (live). No new skill — patch references only | Law | satisfied, no action |
| 7 | grok/gemini funding — capability exists, money-gated | F13 | sovereign decision, not agent work |
| 8 | Census whole-mesh coverage (503 counted vs ~709 real) so verdicts describe all 4 real surfaces | Mesh S1 | **next executable** |

## 5 · Execution rule going forward

Every coding-agent session: `arif_init` (work contract auto-binds) → mesh health read (check
`generated_at_utc` freshness before trusting) → patch owner skills, never fork → census +
symbol-probe before any new skill claim. Knowledge changes hands as receipts, not narratives.

## 6 · Eureka inheritance (2026-09-16 skill-bloat set → coding agents)

The 20-eureka skill-bloat set is ALREADY in canon — `/root/AAA/canon/eureka-entries.jsonl`
tails (EUREKA-SKILL-BLOAT-DISCRIMINATION-2026-09-16, notation-as-governance-surface,
external-artifact-audit "12/12 concepts already owned", actuator-not-documentation, HOLD-as-
potential-well). Hermes metabolized the paste itself — 333 does NOT re-append (anti-redundancy
held). Coding-agent transfer (binding subset):

- **Sensor TTL** — mesh-health/registry/census outputs have timestamps; stale = re-probe before
  repairing (this session's kimi/claude false-FAIL is the live proof).
- **Owner patch before fork** — case-pair shadowing (S4) is the FI-mesh instance of split
  sovereignty; dev-band skills get patched, never re-minted per harness.
- **Capability = live witness** — a harness PASS is a marker echo, config-declared MCP ≠ healthy;
  EXTERNAL ≠ FAIL (grok/gemini are money-gated, alive).
- **Uncertainty ↓ authority** — FI agents executing deploys/force-push hold at 888 regardless of
  green tests.

## 7 · S1 precision (next executable, named)

Registry feeder identified: `/root/scripts/skills-census.py` (cron `37 4,10,16,22 * * *`,
log `/var/log/arifos/skills-census.log`, writes the registry `disk_reconciliation` block).
S1 = audit its SURFACE list; add the overlay surfaces `.config/opencode/skills` (31 via `-L` / 9 own),
`.qwen/skills` (9 own + `aaa-canonical` link + 5 geox links), `.kimi-code/skills` (77 own / 131 via `-L`).
**CORRECTED 2026-09-16T02:30Z:** the earlier "add HERMES live tree (162) … so the 503-count becomes
whole-mesh (~709)" was wrong twice over — `/root/HERMES` is a symlink to `/root/.hermes` (one tree),
and 162 was an `ls -1` top-level listing while the resolved figure is **409** (`find -L`, = census
`viewed_skills`). The census therefore already covers the main tree; the genuine gap is the overlays.
Receipt: `/root/AAA/docs/SKILL_MESH_ALIGNMENT_2026-09-16.md` §1a. Requires read of the script before
patch (it feeds the canonical SOT — no blind edits).

**Flagged defect found while verifying:** FOUR eureka ledgers share one filename, three schemas —
`/root/AAA/canon/eureka-entries.jsonl` (104, canonical, schema-less), `/root/AAA/eurekas/eureka-entries.jsonl`
(3), `/root/.local/share/arifos/eureka-entries.jsonl` (6), and a fourth found by a wider sweep,
`/root/.local/share/arifos/atlas333/eureka/eureka-entries.jsonl` (1, schema `eureka777.v1`).
Four writers, one name, four shapes. Same disease the mesh had. Consolidation target for a future pass.

## 8 · Selection layer — the honest gap (333 cross-check of Hermes session, 2026-09-16 ~02:35Z)

Hermes admitted it cannot reliably pick from 409 skills: 28% sit in colliding trigger groups,
only 9/595 declare an `audience`, its lookup gate returned junk on real queries, and the
chooser in practice is the model's eye over a flat description list. **333 cross-check: true
for every FI harness.** The 506-listing opencode loads works identically — no router exists.

> **CORRECTED 2026-09-16 (Hermes, measured — supersedes the 28% self-report above):**
> deterministic census over 6 surfaces (`os.walk(followlinks=True)`), 1,631 SKILL.md / 573 distinct
> names → **117 identity collisions** (71 = AAA↔hermes mirror twin, **46 genuine**) and
> **182 trigger-collision skills = 31.8%**. Receipt: `docs/SKILL_COLLISION_CENSUS_2026-09-16.md`
> + `work/skill-census/collisions-v2.json`. The 28% figure was a model self-report; the census is
> the number. **v1 of the census itself was wrong first** — it tokenized the `> [fed: tier=… floors=[…]]`
> metadata prefix as trigger text and manufactured a 95-skill fake cluster. De-metadata before
> measuring; dereference before counting.
> Existing-owner proof run before any build: `aaa_capability_loader.py` owns service/backend
> capabilities (not skills); `registry/routing/identity_resolver.py` owns identity-bound capabilities
> (not skill routing); `scripts/skills-census.py` owns inventory only. **No existing owner absorbs
> selection → the gap is real, and the fix is a selection contract, not a new router agent.**


**False fact corrected (live receipt):** Hermes reported "`/root/.claude/skills` kosong —
sifar entri". False — plain `find` returns **0** (does not dereference the symlink farm);
`find -L` returns **506** (realpath = `/root/AAA/skills`). Third repetition of the same
sensor-scar class in 24h (53 case-drift false FATAL → stale mesh FAILs → empty-tree false
FATAL). Hermes's own Eureka 6 predicted it: the sensor that enforces truth can itself lie.

**SCAR RULE (mechanical, no exceptions):** every skill-tree probe MUST dereference —
`find -L` / `realpath` / `os.walk(followlinks=True)`. A probe that reads the symlink
measures the map, not the territory. Encode in census + mesh probe scripts; owner-patch only,
no new skill.

**Brand×variant matrix (claude-/qwen- × meta-mesa/zen-router/agentic-state = 6 files,
3 capabilities):** HOLD confirmed CORRECT — both consumer harnesses are LIVE (mesh 5/7 PASS),
cross-agent blast radius → consolidation (1 owner/capability, brand as parameter) requires
A2A musyawarah or F13. Staged, not executed.

**Exists vs missing:** tools HAVE a selector — capability-index (semantic, ranked,
action-class-tagged). Skills have NO equivalent. Live demo on Hermes's failing query
("retraction public correction") returned only weak tool matches (brave_web_search top) —
the index pattern exists but is not skill-aware and not smart even on tools yet. The build
that changes Arif's daily experience: a skill selection layer fed by DERIVED audience data
(census derives audience from brand-prefix/path — never 586 hand edits).

## 9 · Identity + collision audit (Hermes, 2026-09-16T03:2xZ — falsification pass)

Triggered by an external review that raised two claims. Both were tested against the machine.

### 9a · FI-007 vs FI-010 — **RESOLVED** (no sovereign input needed)

| Source | Class | Says | Dated |
|---|---|---|---|
| `registries/forge_instruments.yaml` | **self-declared live SOT** | FI-007 = Grok Build (izin GRANTED); FI-010 = Gemini CLI, `version: DEAD` | re-probe 2026-09-13 |
| `a2a-server/agent-cards/harnesses/grok-build.json` | runtime card | `fi_slot: FI-007` ×3 + "FI-007 canonical" | live |
| `a2a-server/scripts/seed-agents.js` | runtime seeder | `'FI-007': 'grok-build'`; FI-010 **never seeded** — "superseded into FI-009 lane (F13 merge 2026-08-21)" | 2026-08-21 |
| `registries/AGENTS_UNIFIED.yaml` | invariant list | "No agent claims FI-009 or FI-010 (vacant/collapsed)"; FI-001–008 LOCKED | 2026-08 |
| `registries/AGENT_DISCOVERY.md` | carries explicit STALE banner | "current FI-007 = Grok Build; FI-010 Gemini CLI DECEASED per F13 2026-09-13" | 2026-09-13 |
| `docs/agent-skill-binding-map.md` | **stale satellite** | grok-build = FI-010, aider = FI-007 | last git touch 2026-08-09 |

**Verdict: RESOLVED.** Grok Build = FI-007. FI-010 = Gemini CLI, decommissioned; slot vacant.
The contradicting document is stale by ~5 weeks and is internally inconsistent (aider was replaced
*by* grok-build on 2026-07-18; it also double-assigns FI-009 to two agents). **Not two equally
authoritative sources → not a sovereign question.** Banner added to the stale table.

### 9b · "28% trigger collision" — **DOES NOT REPRODUCE**

Fresh census, read-only, `find -L`/realpath-dereferenced, 5 real surfaces, 698 distinct skills:

- **TRIGGER collision** (distinct capabilities, same request): **26 pairs · 22 skills · 3.2%** —
  and even that is inflated: after document-frequency filtering, the top pairs still share only
  metadata vocabulary ("auto low risk"). Genuine semantic overlaps are few and nameable:
  `openclaw-propose-seal ↔ opencode-propose-seal`, `qwencloud-mesh ↔ mmx-mesh`,
  `web-search ↔ web-scrape`, `forge-onboarding ↔ agent-onboarding`.
- **IDENTITY duplication** (one claimed capability, >1 real directory): **115 groups · 260 skills ·
  37%.** This is the real number, and it was hidden behind the trigger framing.
  Dominant pattern: `~/AAA/skills/<cap>` (canonical) **plus** a real harness-local copy in
  `~/.hermes/skills`, `~/.kimi-code/skills`, `~/.qwen/skills`, `~/.config/opencode/skills`
  (`agi-nusantara-substrate` ↔ `AGI-nusantara-substrate`, `forge-ci-diagnose` ↔ `FORGE-ci-diagnose`, …).
  Genuine intra-canonical pairs also exist: `aaa-shadow-mode` ↔ `domains/.../shadow-mode`;
  `forge-onboarding/agent-onboarding` ↔ `forge-onboarding/claude` (both declare "Agent Onboarding").
- Method is deterministic and re-runnable: `/root/forge_work/skill_collision_{census,pass2,pass3}.py`,
  artifacts `skill_census_pass2.json`, `identity_final.json`.
- **Pass-1 self-correction (on the record):** the first pass measured 40.3% identity / 5.4% trigger
  and its top "trigger collisions" were pure `[fed: …]` annotation leakage. Fixed by stripping
  annotations and DF-filtering. A metric that reads its own metadata is the same sensor-scar class
  as `find` vs `find -L` — fourth occurrence in 48h.

### 9c · "Qwen (FI-003) lacks the minimal authority kernel" — **FALSIFIED by probe**

- `/root/.qwen/instructions.md` carries the full kernel: identity (FI-003, 333-AGI lane),
  explicit lane boundary ("NOT 888-APEX, NOT A-FORGE, NOT F13"), boot sequence with `arif_init`,
  F1–F13 summary, organ map.
- `/root/.qwen/skills/aaa-canonical -> /root/AAA/skills` (since 2026-08-13) → Qwen **does** see the
  canonical mesh; only 9 skills are its own.
- It runs a `555-verifier` subagent with `approvalMode: default` — i.e. verify separation is present.
- Residual real risk (not a symmetry violation): `permissionMode: yolo` + `approvalMode: yolo` +
  `permissions.deny: []`. Documented as sovereign default, so it is policy — but FI-003 is the one
  seat where a bad call has no seatbelt. Flagged, not changed.

### 9d · Does an owner already exist for skill selection? — **NO, and that is now proven**

`/root/arifOS/core/capability_index/` (indexer.py) ingests exactly three sources: `CAPABILITY_INDEX.json`
(164 tools), `mcp_inventory.json`, and the Antigravity MCP schema dir. **Zero skill ingestion**
(`grep -c skill` on the federation capability-index output = 0). The federation has a tool selector
and no skill selector. Therefore the gap is real and unowned — **and the correct fix is to extend
this one index with a skills source, not to mint a "Skill Router Agent".** One routing principle
applied hierarchically (skill → agent → model → machine → witness); the model resolves the last mile,
not the routing universe.

*DITEMPA BUKAN DIBERI ⚒️*
