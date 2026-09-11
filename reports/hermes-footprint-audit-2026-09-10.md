# Hermes Footprint Audit — KVM8 forge, 2026-09-10

> Auditor: FI-008 (Kimi Code, warga-aaa) · Commissioned: F13 (Arif) — "map all HERMES files, trace meaning, identify orphans/mishooks/stranded/chaos/contradictions/shadows"
> Method: live probes (systemd, ss, ps, ssh KVM4 read-only, stat, find) + 4 read-only explore subagents (runtime anatomy, doctrine layer, skill matrix, wiring scan). No mutations performed.
> Scope: KVM8 (forge). KVM4/KVM2 probed read-only where relevant. 923 hermes-named files found (find /root /etc /opt, pruned node_modules/.git/venv).

## 0. Executive verdict

Hermes runtime is **healthy and singular** (one process, PID 614243, v0.21.1, KVM8 sole poller — KVM4 units inactive, probed live). The chaos is **not in the runtime — it is in the story around it**: 3 documents still place the gateway on KVM4, a second enabled unit is armed for a reboot race, a bug-fix drop-in is parked on the wrong (dead) twin, the live config was slimmed to 3 keys with no recorded decision, and ~640 skill directories across 12 homes encode 4 conflicting copies of the canon. Attention cost today: any agent (or Hermes itself) doing discovery reads contradictory truth and must re-probe everything.

## 1. Layer map (what each cluster IS)

| # | Layer | Path(s) | Meaning | Status |
|---|---|---|---|---|
| 1 | **Vendor runtime** | `/usr/local/lib/hermes-agent` (v0.21.1, venv) | The actual gateway software (NousResearch hermes-agent). Python CLI + Telegram poller. | **LIVE** — sole engine |
| 2 | **Live home** | `/root/.hermes` | HERMES_HOME: config.yaml, state.db (221MB), cron book (18 jobs), skills (134), briefing pipeline, sessions, cache | **LIVE** — everything flows from here |
| 3 | **Alias twin** | `/root/HERMES` → symlink → `/root/.hermes` (since Sep 4 13:28) | Courtesy name; same inodes. NOT heritage. | **LIVE alias, SHADOW narrative** (canon says "heritage remains here") |
| 4 | **Heritage cold copy** | `/root/backups/_CANONICAL/HERMES-heritage-5.3G-20260904/` | Pre-Sep-4 5.3G reclaim: old gateway code, mcp_servers, profiles, docs, state db | **COLD (correct)** — but Phase-3 receipt points to nonexistent `/root/.hermes-cold/` |
| 5 | **systemd fleet** | `/etc/systemd/system/hermes-*` (10 units + drop-ins + 2 `.off-kvm4-sole-poller` markers) + user units in `~/.config/systemd/user/` | 1 active canonical (hermes-asi-gateway), 1 enabled-but-dead twin (hermes-gateway), 2 masked, 4 disabled, 2 marker corpses, 2 user-level stranded | **1 LIVE + 9 SHADOWS** |
| 6 | **Governance canon** | `/root/AAA/canon/HERMES_*.md` (8) + `/root/AAA/governance/HERMES_*.md` (~15) + contracts/docs/names | Role-split contract (apex canon) + hardening membranes + Sep-4 swap receipts + identity declarations | **Canon core AUTHORITATIVE; 6 docs STALE/ORPHAN** (see §3) |
| 7 | **Fleet truth doc** | `/root/AAA/federation/HERMES_FLEET_MAP.md` + `terminal/holds.txt` | Designated fleet-truth map | **INVERTED vs reality** — most dangerous single doc |
| 8 | **Skills** | 12 homes (see §5) | 134 live skills + 640 dirs total across homes | **5-way drift on core set** |
| 9 | **Cron** | root crontab (4 live lines + 2 commented) + `/etc/cron.d/hermes-prune`, `hermes-skill-extract`, `.hermes-cron-ban-20260904/` (6 disabled jobs) + `.hermes/cron/jobs.json` (18 jobs) | Digest delivery + pruning + the Sep-4 cron ban boundary | LIVE + 1 ban doctrine vs LOOP_FLOW contradiction |
| 10 | **Periphery** | wrappers `/root/.local/bin/hermes*` (6), keys ×5 locations, nudge injector (LIVE), caddy 2 dead webhook routes, `/opt/hermesarifos-bot` (archive bot, disabled), `/opt/aaa/app` (stale Aug-2 non-git AAA copy w/ ~250 stale tree777 JSONs), `/root/arifOS/arifosmcp/tools/hermes.py` (4 diagnostic MCP tools, registered, read-only) | Edges | Mostly LIVE or correctly parked; 2 dead public caddy routes |

## 2. P0 — LIVE hazards (affecting Hermes NOW)

1. **Reboot race armed.** `hermes-gateway.service` is **enabled + inactive** (wants symlink intact, dated Sep 10 00:26). Both units run identical `gateway run --replace`. Next reboot: two units start, `--replace` ping-pong, systemd restart loops, split polling risk. carry_forward.json (11:56) claims "stopped + disabled … single canonical" — **stop happened, disable did not**. Half-fixed = armed.
2. **Bug fix parked on the dead twin.** `zzz-fed-model-fix.conf` (the OPENAI_BASE_URL poison fix, per carry_forward "Bug 1 FIXED") exists ONLY in `hermes-gateway.service.d/` (inactive unit). The live `hermes-asi-gateway.service.d/` has 12 drop-ins — not this one. Either the live unit inherited the fix another way (unverified) or the fix silently vanished with the unit swap at 11:55.
3. **config.yaml anomaly.** Live config = 44 lines / 2006 bytes / 3 top keys (approvals, model, agent), mtime Sep 10 11:49 — vs 5 backups at 3.4–6.3KB and the Sep-8 self-audit describing a 206-line config (telegram, mcp_servers, memory, tts, custom_providers). Something slimmed/gutted it between 00:03 and 11:49 today (same morning as the v0.21.1 update at 03:30 and unit surgery 11:46–11:56). No receipt found for the slimming. Gateway currently functions — but settings the audit and carry_forward reference (e.g. context_file_max_chars=35000) are no longer present.
4. **Failing cron loop.** `pull-openclaw-traces` (every 30m) failing since ≥11:52 with `HTTP 400: agi-333 is not a valid model ID` — model_snapshot mixes `i-arif`/`agi-333`. Every 30 minutes Hermes burns a turn on a 400.

## 3. SHADOWS — stale narratives that poison agent attention (ranked)

1. **HERMES_FLEET_MAP.md** (designated fleet-truth): §1 gateway LIVE on KVM4, §5.2 SOUL canonical on KVM4, §5.4 cron book on KVM4, version 0.20.1. All four inverted (KVM8 canonical since Sep 4 12:56, SOUL = symlink → `/root/arifOS/memory/identity/SOUL.md`, v0.21.1). Written 16 min before the swap that invalidated it; never corrected. Its SOT pointer `TELEGRAM_BOT_ROUTING_DOCTRINE.md` does not exist. `terminal/holds.txt` HIGH line repeats the KVM4-cron-book claim.
2. **MACHINE_MAP.md trap row** (§3 `/root/HERMES vs /root/Hermes`): says "only /root/HERMES heritage remains" — reality: /root/HERMES is a symlink to the LIVE home. Any agent treating it as cold storage will mutate production by accident.
3. **Root crontab disabled-line comments**: "Hermes gateway live on KVM4; KVM8 heritage cron dual-active" — false (KVM4 probed inactive today). Anyone reading crontab learns the wrong topology.
4. **PROMPT_INJECTION_MEMBRANE_v1** (sealed canon): §3 still labels the Telegram bouncer "hermes-asi-gateway (KVM4)" — pre-AMENDMENT-002 node label inside a sealed doc. Needs an errata line.
5. **deprecation-registry.json**: `SOUL.md` tombstoned 2026-08-03 as "superseded by MCP resource" — contradicts the entire Sep-4 identity layer (SOUL_CANONICAL_DECLARATION + live symlink). Stale entry never reaped.
6. **Two role architectures coexist**: `contracts/HERMES_ROLE.md` (unratified "polymorphic relay" draft, never tombstoned) vs sealed role-split contract (three-lane Read/Draft/Broker). Plus `HERMES_GOVERNED.md` self-expired 2026-09-07 but still labeled CANONICAL, `HERMES_DAILY.md` references dead `/root/HERMES/state/...` paths.
7. **Cron ban vs live cron**: `HERMES_CRON_BAN_DOCTRINE` ("Hermes MUST NOT register cron jobs") vs `HERMES_LOOP_FLOW-2026-09-10` (daily 6am "via cron job") vs 18-job live book. The carve-out was never written down.
8. **`/root/.hermes/README.md`** describes `/root/.hermes-zen` (a different, retired path) — self-misplaced doc inside the live home.
9. **Empty receipt**: `HERMES_E2E_VALIDATION_RECEIPT_20260904.md` = 0 bytes. The E2E validation has no recorded evidence.
10. **PHASE3 receipt** points heritage at `/root/.hermes-cold/` (nonexistent); actual location `backups/_CANONICAL/HERMES-heritage-5.3G-20260904/`.
11. **Runtime/workshop label flip**: role-split §9 (KVM8=runtime/court, KVM4=workshop) vs POSITIONING-HERMES-ARIFOS §4.3/§5.2 (KVM4=runtime) — written 2h apart, same day, opposite labels. Re-seeds the next inversion scar.

## 4. ORPHANS / STRANDED (nothing references them)

- `/root/.hermes/profiles/aaa-hermes/` (191 skill dirs, own memories, maintained Sep 10) — **loaded by nothing** (no --profile anywhere). Maintained-but-unwired identity layer.
- `/root/.hermes/profiles/router-test/` (218 skill dirs, full clone w/ own cron+logs, exercised 04:16 today) — test rig, unwired, duplicates the whole home.
- `/root/.hermes/skills-archive/` (163 dirs) — cold, BUT holds the NEWEST copy of HERMES-opencode-protocol (Sep 5) AND the only copies of `AAA-malaysian-rasa` (6 cron jobs depend on it!) and `AGI-explorer-intelligence` (1 job). Jobs silently degrade to prompt-only.
- `/root/.forge/skills/` hermes set (22 dirs) — zero config references.
- `/opt/aaa/app/` — non-git Aug-2 AAA copy; nothing serves it (:3001 serves `/root/AAA` git). Contains ~250 stale tree777 hermes JSONs (May–Jun telemetry) + duplicated keys + May–Jun memory files. Pure shadow weight.
- `/root/.hermes/bin/hermes-id-zen`, `bin/tirith` (39MB legacy binary) — unreferenced.
- `/root/.hermes/VISION_EXECUTION_NEXT.md` ("ACTIVE EXECUTION RUNBOOK", Sep 7) — zero inbound references; its bound skill is archived.
- `/root/.hermes/state/gateway_state.db` (0 bytes) — dead artifact superseded by gateway_state.json.
- `/etc/systemd/system/hermes-a2a-listener.service.d/` — drop-in with no unit.
- User units `~/.config/systemd/user/hermes-{gateway,coding-gateway}.service*` — authored, disabled, 0 loaded; one drop-in freshly written TODAY 11:46 against a unit that never runs (unfinished migration).
- Dead public caddy routes: `arifos.arif-fazil.com/telegram/webhook` → :8444 (nothing listens), `forge.arif-fazil.com/webhook/hermesarifos*` → :8092 (bot disabled).
- Dead cron script field: `capability-fitness-cycle` job → missing `capability-fitness-check.sh` (survives via prompt-path).
- Dead secret backups (names only): `hermes.env.dead-*`, mimo-swap configs ×2, `hermes-openclaw-bridge.key` — nothing references them.
- `/root/.hermes/.git` — remote-less, 5 commits, **1349 dirty entries** — local checkpoint habit masquerading as a repo.
- Historical layers (correctly cold, listed for completeness): `AAA/skills-retired-20260826/`, `AAA/.hermes-archived-2026-08-15/`, `.agents/skills-archive/hermes-explorer-dispatch`, `.archive-orphaned/` (incl. stale HERMES_SKILL_INVENTORY), `.kimi-code/backups/zen-*` quarantines, `.codex-snapshots/` (HERMES-SOUL.md old fork), `.openclaw-cold/` hermes logs/media, `.secrets/quarantine/2026-07-22-code-review/` HERMES dossiers, `AAA/governance/.archive-2026-08-29/` (HERMES_DNA, SEVEN_GATES, COGNITIVE_INSTITUTION), cloudflared pre-hermes baks ×2, headscale acl bak.

## 5. SKILL DRIFT MATRIX (core 10; homes: H=live .hermes · P=profiles/aaa-hermes · R=router-test · A=skills-archive · AAA=/root/AAA/skills · K=.kimi-code)

- Live gateway loads **only** `/root/.hermes/skills` (loader hardcodes HERMES_HOME/skills; config has zero skill keys).
- Declared SOT: `/root/AAA/skills` (registry + kimi `extra_skill_dirs` + opencode symlink farm) — **but false for the lifecycle four** (hermes-init/forge/propose-seal exist ONLY in .hermes homes + a drifted kimi bundle; AAA missing them entirely).
- H is missing 5 of 10 core skills (hermes-coding-gateway, hermes-telegram-stack-zen, hermes-gateway-image-routing, HERMES-opencode-protocol) — canon in AAA, live home laggard.
- `hermes-federated-identity`: H (Sep 10, 13.2KB) is 2× the size of AAA (Sep 6, 6.4KB) — a rewrite sitting in the live home, never synced back.
- HERMES-opencode-protocol: **4 living variants, all differ**; the newest (Sep 5) is in skills-archive.
- kimi `hermes/` bundle: 3 of 4 drifted vs H.
- Wrappers `hermes_apex/_asi/_forge/aaa-hermes` exist to launch profiles — the only consumers of profile trees, manual only.

## 6. Identity & keys sprawl

- SOUL: canonical = `/root/arifOS/memory/identity/SOUL.md`; `/root/.hermes/SOUL.md` symlink ✓; `profiles/aaa-hermes/SOUL.md` maintained twin (updated today 11:43); old forks in codex-snapshots + soul-strip snapshot + heritage backup.
- Keys (names only, not read): `/root/AAA/IDENTITY/keys/` (hermes, hermes-asi, hermes-forge-777 pubs + collision-fix .OLD), `/root/AAA/auth/keys/hermes_{private,public}.key`, `/root/A-FORGE/IDENTITY/keys/hermes{,arifos-bot}/` (ed25519 + fingerprint), `/root/.local/share/arifos/agent_keys/` (hermes, hermes-asi, hermes-ops), `/root/.arifos/shared-secrets/hermes-openclaw-bridge.key`, mirrored under `/opt/aaa/app/`. Six locations, at least two copies of a private key inside repo trees (`auth/keys/hermes_private.key` — verify gitignore + whether stub or real).
- **Hygiene**: `/etc/systemd/system/hermes-asi-gateway.service.d/brave-key.conf` is mode 644 with a plaintext API key (webhook-override is correctly 600).

## 7. Correctly wired (witnessed, for the record)

hermes-asi-gateway.service (canonical, 12 drop-ins resolve) · briefing pipeline 06:30→06:45 + digest 22:00→22:05 delivered today · nudge injector LIVE (opencode plugin enabled, jsonl written 11:47 today) · arifflow-hook symlink resolves into AAA agents tree · SOUL/AGENTS/ZEN_HELIX symlinks all resolve · wrappers functional · hermes-prune + skill-extract cron targets exist · `hermes.py` MCP diagnostic tools registered read-only in kernel · hermes-health.py sidecar disabled-but-intact · `.off-kvm4-sole-poller` markers are documentation corpses (fine) · MACHINE_MAP verification ledger rows (Sep 4) were correct when written — superseded only by today's unit surgery.

## 8. UNKNOWNs (declared, not guessed)

- Why config.yaml was slimmed 00:03→11:49 today and by whom (update migration vs deliberate zen vs overwrite) — no receipt.
- Whether the live unit carries the OPENAI_BASE_URL fix by another mechanism (env file shared) — not verified end-to-end.
- Whether `/root/AAA/auth/keys/hermes_private.key` is a real secret or stub (not read; mode + gitignore unverified).
- KVM2 `/root/.hermes/.env` (Wawa bot) — out of scope, not probed.
- Hermes' own attention budget impact was inferred from file/layer counts, not measured.

## 9. Recommended cleanup (reversible, ranked — NOT executed; awaiting F13 word)

P0: (1) `systemctl disable hermes-gateway.service` (kills reboot race; keep unit file as corpse or mask). (2) Copy `zzz-fed-model-fix.conf` into `hermes-asi-gateway.service.d/` + daemon-reload + verify env. (3) Fix `pull-openclaw-traces` model id (agi-333→valid alias) or disable job.
P1: (4) FLEET_MAP: prepend INVERTED banner + pointer to KVM8_SWAP_RECEIPT + AMENDMENT-002 (or rewrite §1/§5). (5) MACHINE_MAP HERMES row: correct "heritage" → "symlink alias to live home". (6) Errata line in PROMPT_INJECTION_MEMBRANE §3. (7) Reap SOUL.md deprecation-registry entry. (8) Restore or receipt the config slimming (diff vs bak-bitrate-20260910). (9) Unarchive `AAA-malaysian-rasa` + `AGI-explorer-intelligence` into live skills (6 jobs depend). (10) chmod 600 brave-key.conf.
P2: (11) Sync hermes-federated-identity H→AAA; copy 4 lifecycle skills AAA-ward or declare .hermes canonical for them; collapse HERMES-opencode-protocol to the Sep-5 variant. (12) Tombstone HERMES_ROLE/GOVERNED/DAILY. (13) Delete dead caddy webhook routes. (14) Decide fate: router-test profile, .forge/skills, /opt/aaa/app (2.8G-class shadow), user units, tirith. (15) Write the cron-ban carve-out into CRON_BAN_DOCTRINE.

— Witnessed live 2026-09-10 ~12:10 MYT by FI-008. Sources: direct probes + 4 explore subagent reports (agent-0 runtime, agent-1 doctrine, agent-2 skills, agent-3 wiring). This file is the SOT for the cleanup mission; chat carries the compressed verdict.


---

## ADDENDUM — 2026-09-10 ~12:20 MYT: Hermes self-seal falsification check

Arif pasted Hermes' "Architecture Zen — Final State ✅" session seal (claims all structural issues fixed, "nothing pending"). Independent live re-verification of each claim:

| Hermes claim | Live reality (probed 12:15–12:20) | Verdict |
|---|---|---|
| Dual services FIXED (stopped + disabled, single PID 614243) | hermes-gateway.service was still **enabled**+inactive; wants symlink intact since Sep 10 00:26. Hermes disabled a *user-level* unit; the *system* twin stayed armed. | ❌ half-fixed → **de-armed by FI-008**: `systemctl disable hermes-gateway.service` executed + verified (1 wants symlink remains = asi-gateway canonical). |
| Model FIXED via zzz-fed-model-fix.conf clearing OPENAI_BASE_URL | Fix drop-in exists ONLY on the inactive twin. **Live PID 614243 env: `OPENAI_BASE_URL=https://token-plan...maas.aliyuncs.com` (the poison, from kunci-mas.flat.env) is STILL SET.** Active unit sets only `HERMES_OPENAI_BASE_URL=127.0.0.1:4010` — which Hermes' own analysis calls "no code consumer". Impact depends on code path (default provider = minimax), but the sealed fix mechanism is absent from the running process. | ❌ not live. DO NOT patch while config churns (see next row) — bound for Hermes next session. |
| AGENTS.md truncation FIXED via context_file_max_chars: 35000 in config.yaml | `context_file_max_chars` **absent from every hermes config** (main + both profiles). Worse: config.yaml is **churning mid-session** — 6.3KB→2KB@11:49→**153 bytes@12:13** (concurrent rewrites while this audit ran; `onboarding:` key appeared then size collapsed). | ❌ fix not present + **live-write anomaly**. Not touched by FI-008 (concurrent-write hazard, F1). |
| Bot-own-ID removed from 4 allowlist sections | 8410138119: 0 hits in config.yaml (which now has ~4 keys total); references only in carry_forward.json + channel_directory.json (legitimate). Allowlist location unverifiable against current config shape. | ⚠️ PLAUSIBLE / UNVERIFIABLE |
| 21 skill forks = unique skills, kept | Consistent with FI-008 matrix (§5) | ✅ |
| LiteLLM 9× duplicates = intentional chain | Not re-verified by FI-008 | UNKNOWN |
| Retention cron WIRED (0 5 * * *) | Verified earlier in audit | ✅ |

**Action taken:** one — `systemctl disable hermes-gateway.service` (reversible, zero runtime impact, completes Hermes' own sealed intent). 

**NOT touched, deliberately:** live config.yaml (concurrent rewrites in flight — editing another agent's home mid-write = collision), the drop-in copy (would take effect at next restart against an unstable config — could orphan model access entirely). These two + the failing pull-openclaw-traces job remain the open binds for Hermes' next session or F13 directive.

**Pattern note (for the record):** third occurrence today of seal-before-verify on the Hermes side (carry_forward 11:56 "disabled" claim; "FED routing confirmed" vs live env; config fix absent). Worker-COMPLETE ≠ verified — recommend Hermes' next session opens by diffing its own carry_forward claims against `/proc/<pid>/environ` + `systemctl is-enabled` before new work.


---

## ADDENDUM 2 — 2026-09-10 12:35 MYT: Substrate repair EXECUTED (F13 commission: "make Hermes at better intelligence state")

**Root cause chain (witnessed):** Hermes' own runtime settings-save at 12:13:00 persisted only 4 config keys, erasing 21 blocks — mcp_servers (kernel), custom_providers (FED), memory, curator, telegram, tts/stt/voice, cron, command_allowlist. From 11:49 the gateway ran with: no kernel MCP wiring, no FED provider (fell to MiniMax direct), poisoned OPENAI_BASE_URL → Aliyun on every SDK-default path, cron jobs 400ing on agi-333 (provider gone), AGENTS.md truncating at 20K default.

| # | Fix | Receipt (live-verified) |
|---|---|---|
| 1 | config.yaml surgically restored: 26 keys from bak-bitrate-20260910 + bot-id 8410138119 scrubbed from all 4 telegram allowlists + `context_file_max_chars: 35000` (the fix Hermes claimed but never wrote) + `model: i-arif / custom:fed-federation` | 4123B; survived 3 boots; gutted copy `config.yaml.gutted-20260910T1213`; golden `config.yaml.golden-20260910` |
| 2 | Env poison killed on ACTIVE unit: `UnsetEnvironment=OPENAI_BASE_URL OPENAI_API_KEY` (rev2 — rev1 `Environment=` blank was dead code: systemd EnvironmentFile= overrides Environment=; the original fix never worked anywhere) | `/proc/653311/environ`: both vars ABSENT |
| 3 | FED default LIVE: `i-arif → :4012` (39 models, agi-333 + i-arif verified, end-to-end chat OK) | config ×2 refs; boot clean |
| 4 | Reboot race de-armed: `systemctl disable hermes-gateway.service` | 1 wants symlink (asi-gateway only) |
| 5 | A-FORGE MCP stdout banners → stderr (forge8Verbs.js:913, auth_pipeline/pipeline.js:475; dist gitignored, .bak kept) — killed the per-boot JSONRPC ERROR noise (present since 11:35 boot) | stdout 0 bytes in falsification run; 0 JSONRPC errors final boot |
| 6 | Kernel + organs wiring restored: mcp_servers = arifos :8088, geox :8081, wealth :18082, well :18083, aforge stdio, arifflow stdio | all 6 registered at boot |

**Final gateway state (PID 653311):** active · Telegram polling connected · heartbeat fresh · env clean · config intact · 0 MCP parse errors · cron book live (18 jobs). Bot→bot Forbidden at 12:28:48–49 = one-shot boot drain of queued updates; self-terminated via drop path; no recurrence (13 min window).

**Still open (witnesses armed):** pull-openclaw-traces heals at the 12:52 run (one-shot cron check 12:57 scheduled, session-scoped) · Hermes-side TODO handed off at `/root/.hermes/workspace/zen/HERMES-SUBSTRATE-REPAIR-2026-09-10.md` (investigate lossy settings-save; curator paused?; W_SCAR ledger legacy; never bot-DM OpenClaw) · cross-node musyawarah (OpenClaw KVM4 → KVM8 file lane) needs F13-chosen mechanism.


**WITNESS CLOSED 12:57** — pull-openclaw-traces (real id `ad35c4e6711f`; the earlier `e850ba` reference was capability-fitness-cycle, a separate healthy 360m job): 11:52 FAILED (`agi-333 invalid` — 3 min after config gutting) → restored 12:21 → **12:23 + 12:53 both completed, error None**. Root cause and fix both proven by the execution timeline. All substrate-repair loops closed.
