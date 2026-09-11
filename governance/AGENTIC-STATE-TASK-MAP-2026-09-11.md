# AGENTIC-STATE TASK MAP — compiled 2026-09-11 ~23:50 MYT

> **Status:** WORKING_MAP (F13 chat directive 2026-09-11: "compile all remaining task to be executed… audit and contrast and improve for future agentic state")
> **Compiler:** kimi-code/FI-008 (KVM8 truth node) — all facts below witnessed live this session unless marked HERMES-CLAIM.
> **Sources:** FI-008 AGENTS.md sweep (250+ files), Hermes↔OpenClaw transcript #56480–#56509, live probes KVM8.

## A. Remaining tasks (executable)

| ID | Task | Owner / Lane | Status | Evidence / Notes |
|---|---|---|---|---|
| **T-1** | **Boot-context injection into Hermes session** — `/tmp/experience_boot_context.md` written every 15 min by cron (MVM + P0 auto-fire), ZERO readers in hermes core (`grep` = 0 hits). Wire it: config context-file entry via `hermes config set` CLI (sanctioned path — raw config edit refused by verifier 2026-09-11) OR reflective skill. No `context_files:` array seen at config.yaml top level — loader is prompt_builder-side. | **HERMES** (own runtime; refuses unilateral core edit — correct) | OPEN — design decision in flight (config vs skill) | File fresh 23:41, "Traces: 47 · Cap +3.986 · Trend IMPROVING", contains FI-008 L1 lesson |
| **T-2** | **Memory recall nerve — RE-TEST, do not "fix"** | HERMES | **RESOLVED-BY-REALITY (stale claim)** | Ollama `active`, `bge-m3` live (updated 2026-09-11 11:16), live embed call returned vector. If Hermes recall still fails → wrong endpoint/model ref in its config, not dead backend |
| **T-3** | **Phase 2 read-side adaptation loop** — before tool/skill selection, read `experience_traces`; success < 70% → try alternative; record outcome. ⚠️ **F12 gotcha ×3 (witnessed live 23:48–23:59):** `forge_experience_trace` VOIDs on (a) shell metachars, (b) authority tokens like ratification labels, (c) hex strings/hash-like text, (d) the literal words key/seal/token anywhere in fields — *including when describing the filter itself*. Write-side prose must be plain: no punctuation decorations, no hex, no authority vocabulary. Scanner is a substring grep, not a semantic judge. | HERMES (its selection path) — **committed: "Aku buat kerja"** | IN FLIGHT (Hermes) | FI-008 will NOT touch Hermes core (duplicate-avoidance). Pattern already wired in FI-008's own af-forge.md §0.4 as reference implementation; first trace sealed 23:48 — second trace attempt VOIDed ×3 by F12 (finding recorded, attempts stopped per 3-strike) |
| **T-4** | KVM4 redundant silo cleanup — OpenClaw-created local dirs redundant (MCP writes already land on KVM8 via `100.64.0.2:7072`). Sync KVM4↔KVM8 **EXISTS**: hermes cron `ad35c4e6711f` pull-openclaw-traces, every 30m, last run 23:43:13 ok (witnessed). | **OPENCLAW / KVM4** | OPEN | Earlier joint claim "sync: tiada" was FALSE — they checked mounts/fstab, not the hermes cron registry |
| **T-5** | ~~Cross-node trace sync~~ | — | **EXISTS — VERIFIED 2026-09-11 23:5x** | `ad35c4e6711f` every 30m ok. Also `7185f1cb707d` surface-regen 6h (last 21:31 ok, next 03:31) and `cb1ef577d921` session-auto-trace 60m **FIXED** (doubled script path → `session-trace.py`, fired ok 23:44:22, hermes trace written 23:43:53) — trace source of the loop unblocked |
| **T-6** | ~~attention-kill-criterion ratification~~ | F13 → executed by FI-008 | **SEALED 2026-09-11** — *"aku seal ja semua"* post-audit; status header updated, `ref:` added to render-agents.sh, kernel re-rendered |
| **T-7** | ~~Jauhari Intelligence Doctrine ratification~~ | F13 → executed by FI-008 | **SEALED 2026-09-11** — zero floor conflict; seal-ID anchor footnote unverified in quick probe (not load-bearing) |
| **T-8** | Stale clones/junk: `/home/ariffazil/arifOS` (Jun), `/srv/arifos` (Apr), `/srv/syncthing/inbox/XXX/AGENTS.md` (268KB third-party) | FI-008 on F13 word | **CLOSED 2026-09-12 — EXECUTED-ABSENT** — targets gone from disk (earlier sweep); 268KB AGENTS.md preserved at `_QUARANTINE_30D/syncthing-inbox-20260911/AGENTS.md.merged-268KB` (verified FI-003, marker 27f19a7a) | Deletion already effective; quarantine evidence intact |
| **T-9** | RSI-federation-mesh: `invocation_count: 0` — invoke once per cadence or declare dormant | any warga | OPEN | liveness.json says ALIVE; zero invocations = unexercised |
| **T-10** | WELL biometric telemetry stale (C-001) | WELL lane | KNOWN-CONTRADICTION | machine OK, human-plane stale |

## B. Context-surface audit verdict (this session)

**Architecture = pointer-first.** Canon lives in `/root/AGENTS.md` (43 fragments, rendered 15:28:56Z); overlays point. Fixes applied this session: kernel re-render (mem0 F2 correction + attention-kill footer), `/opt/arifos` sync, `.arifos/agents/kimi/AGENTS.md` sync (dead ZEN pointer), dead SYSTEM.md duplicate archived, web dist==public==live (md5 identical). Hermes SOUL.md runtime==install (md5 `e2ab0ba4`). Cap 60000 confirmed L211; gateway PID 2213720 cache auto-invalidates on mtime (source: config.py:184-186) — no restart needed.

**Canon contrast (boot chain resolves to kernel):** kimi ✓ (injected) · hermes ✓ (context files @60000) · claude ✓ (CLAUDE.md pointer) · codex ✓ (INIT chain) · opencode ✓ (pointer) · qwen ✓ (MEMORY fresh 09-11) · grok 🟡 (overlay Aug 18 — oldest, but INIT-chain still resolves; refresh candidate) · openclaw ✓ (INIT_OPENCLAW).

## C. Upgrades executed 2026-09-12 (F13: "upgrade my openclaw and the whole system agentically")

| What | Result |
|---|---|
| **OpenClaw binary** | 2026.9.1 → **2026.9.4** on Node 24.15.0 → **24.21.0** (npm-scripts rebuilt, gateway stabil: active, 0 restart, 0 error). Rollback: `npm i -g openclaw@2026.9.1` + repoint /usr/bin symlinks to nvm v24.15.0 |
| **KVM4 kernel** | Stale Sep-4 copy (7.5KB — the "false-negative" OpenClaw reported was a TRUE reading of stale canon) → **44→45-fragment kernel synced** (42,249B) |
| **OpenClaw context** | workspace/AGENTS.md + MEMORY.md: canon sync + experience-metabolism reflex + F12 write rule appended (backups kept) |
| **T-4 silos** | DONE — KVM4 dirs moved to `/root/quarantine-20260912/` |
| **Whole system** | New kernel fragment `experience-metabolism-reflex` (read/query/trace + F12 plain-prose rule) — **inline, loads at boot for every harness**: kimi·hermes·claude·codex·opencode·qwen·grok·openclaw + KVM4. Commits `1d6c12832` + `d9c182f` |

## D. Hermes Izzu/Syed report — FI-008 witness verdicts (2026-09-12 ~00:4x)

| Claim Hermes | Disaksikan | Pembetulan |
|---|---|---|
| izzu-kpj-dashboard revived, SKILL.md 8,340B | ✅ tepat (8,340B @ 23:52:18) | — |
| Lane override marker + chain 46a1493b00cd | ✅ wujud di ritual.log | — |
| 50 skill hilang dari load path | 🟡 | **40** hilang dari load path hermes; tapi termasuk mesh AAA → **mati sebenar 117** (lihat bawah) |
| usage.json: 44 active-tapi-mati | ❌ | **138 active-tidak-wujud-di-load**; ditapis mesh AAA → **117 mati sebenar** dari 228 entri active |
| Identiti: lanes+social-graph vs registry bercanggah | 🟡 | **lanes.yaml + lanes/social-graph.yaml + channel_directory.json SEMUA bersetuju**: Izzu=1237635275 ("Mohd"), Aliff=1024343313. people_registry.json TIDAK DITEMUI dalam probe — kontradiksi tak dapat disaksikan; sokongan buat masa ini condong kepada Izzu=1237635275 (3 fail hidup vs 1 fail tak jumpa) |
| Manifest baseline Sep-4, 490 entri hantu | 🟡 tak disahkan penuh | .bundled_manifest dijumpai ber-tarikh **Aug-15** (lebih lapuk); manifest hash-829 Hermes tak ditemui dalam probe cepat — keputusan F13 tetap sama |

**Mayat paling mahal (use+patch tinggi, tiada di mana-mana load surface):** syed-care-architecture (use=78 patch=23) · human-paradox-geometry (34/39) · arifos-federation-health (29/32) · arif-syed-cron-doctrine (22/25) · AAA-malaysian-rasa (43/0).

**4 keputusan menunggu F13 (soalan Hermes, angka kini disaksikan):** (1) restore berapa banyak dari 117 · (2) identiti Izzu=1237635275 sah? · (3) manifest: baseline baru vs rekod niat · (4) susunan bina hardening — cadangan majlis APEX: **atomic-receipt + claim-without-handle sebagai Tier-0 bergabung**, kemudian identity-SOT → manifest-liveness → archive-gate.

DITEMPA BUKAN DIBERI ⚒️
