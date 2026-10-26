# HERMES 3-NODE CONTRAST — KVM2 / KVM4 / KVM8
**Date:** 2026-10-19 21:45 MYT (13:45 UTC)
**Mode:** read-only probes (SSH, files, systemd, git refs, logs). No config or code mutation.
**Upstream truth:** `NousResearch/hermes-agent` — latest release **v0.22.2** (2026-10-15), `main` = `349e4f7e620` (2026-10-19).

---

## 0. VERDICT (one paragraph)

Ini bukan satu deployment Hermes. Ini **tiga fork berbeza dengan tiga identiti, tiga versi, tiga set undang-undang**. KVM8 ialah mulut sebenar (1,706 DM log lines hari ini, gateway aktif, arifOS :8088 hidup). KVM4 ialah **zombie twin**: identity lock KVM8 menandakan `@hermesarifos_bot` sebagai `DORMANT`, tetapi SOUL-nya mendakwa "KVM4 = LIVE mouth, KVM8 gateway RETIRED, arifOS BUTA" — ketiga-tiga dakwaan **false** pada hari ini. KVM2 ialah tenant Wawa/Azwa yang berasingan, tetapi masih boleh menjawab DM Arif, dengan 44 KB AGENTS.md lama dan hanya 7 skills.

**Jangan upgrade apa-apa lagi.** Tiga benda mesti dibetulkan dahulu: (1) KVM4 SOUL yang menipu reality, (2) KVM8 self-echo + hook skip, (3) dirty tree KVM8 yang akan hilang jika `hermes update` dijalankan.

---

## 1. NODE TRUTH TABLE (OBS)

| Axis | KVM8 `forge` | KVM4 `srv1946043` | KVM2 `flow-edge` |
|---|---|---|---|
| Tailscale | 100.64.0.2 | 100.64.0.5 | 100.64.0.4 |
| Declared role | `kvm8-forge-canonical-home` | SOUL: "LIVE mouth" | SOUL: `EDGE_BRIDGE_AZWA`, persona Wawa |
| Hermes version | **0.21.5+4034** (`cdd6901`, upstream base `b221050c`) | **0.20.1** (`254b7b7`) | **0.21.5+3916** (`35272ce`) |
| Config schema | v48 (847 lines) | v42 (231 lines) | v47 (806 lines) |
| Gateway unit | system `hermes-asi-gateway.service`, active 10:00 today | **user** `hermes-gateway.service` under `user@0`, active since 17 Oct 08:06 UTC | system `hermes-agent.service` via wrapper |
| Bot identity | `@ASI_arifos_bot` (id 8410138119) | `@hermesarifos_bot` (id 7958220838, **DORMANT** in KVM8 lock) | `@Azwafazil_bot` (Wawa) |
| Activity today | 1,706 DM log lines; 3,910 gateway lines | 81 DM log lines; last successful send **18 Oct 17:34** | 59 DM lines; last response 12:47 (latency 1,532s) |
| Cron registry | 30 jobs (`~/.hermes/cron/jobs.json`, hard-linked to `/root/HERMES/cron`) | **two registries:** 15 live (`~/.hermes`, only 2 enabled) + 28 stale (`/root/HERMES`, executions.db dead since 2 Sep) | 3 jobs (Azwa only) |
| MCP servers | 28 | 5 | 7 |
| Hooks | 6 | 6 (different set) | **0** |
| Plugins | 9 | 1 | 0 |
| Profiles | 5 (`default`, `aaa-hermes`, `hermes_apex`, `hermes_asi`, `hermes_forge`) | 0 | 0 |
| Skills indexed | **1,203** (~26k tokens index) | 104 | 7 |
| System timezone | Asia/Kuala_Lumpur (+08) | **UTC** | **UTC** |
| Git state | branch `fix/ci-ruff-lint`, 1 carried commit, **2 modified + 1 untracked** | branch `fix/entity-grounding-gate`, 4 local carries, 1 modified + untracked `profiles/` | `main` clean, 0 carries |

---

## 2. UPSTREAM DRIFT (OBS/DER)

| Node | Local | Upstream equivalent | Behind upstream `main` | Missing releases |
|---|---|---|---|---|
| KVM8 | `b221050c` (v0.21.4 canary, 28 Sep) | `349e4f7e` (19 Oct) | **11,087 commits** (GitHub compare; 38 fork-side commits) | v0.22.0, v0.22.1, v0.22.2 |
| KVM2 | `35272ce` (v0.21.4 canary, 28 Sep) | `349e4f7e` | **11,166 commits** | v0.22.0, v0.22.1, v0.22.2 |
| KVM4 | `254b7b7` (v0.20.1, 13 Aug) | `349e4f7e` | **34,279 commits** | v0.21.x + v0.22.x |

**Version-check trap (OBS):** KVM8 says "Up to date" because `origin` = `ariffazil/hermes-agent` fork. Its `upstream/main` ref is stale at `ee5f49b` (29 Sep); GitHub upstream is `349e4f7e` (19 Oct). So "up to date" is **fork-relative, not upstream-relative**. KVM2's "Update available" is correct. KVM4 does not even run the check.

**Upstream v0.22.0 "Threshold Release" (15 Oct)** — relevant to this federation:
- stable SemVer release channel (source installs follow releases, not `main`)
- `hermes pm` unified package manager (atomic env switch, no half-applied update)
- Bot Mode + one gateway/backend for every profile (proper per-persona bots)
- checkpoints & rollback
- managed scope (admin-pinned config/secrets)
- secrets providers (1Password, Bitwarden, command source)
- egress proxy / iron-proxy / Docker network isolation
- curator maturity (skill usage, staleness, archival)
- gateway reboot-start fix (#138594) — directly relevant to KVM4's user unit and KVM8 boot
- v0.22.2 fixes 0.22.1's wrong-commit gateway and session deletion bug

---

## 3. BANGANG CONTRADICTIONS (ranked)

| # | Severity | Contradiction | Evidence | Reality | Impact |
|---|---|---|---|---|---|
| C1 | **CRITICAL** | KVM4 SOUL says "KVM8 `hermes-asi-gateway.service` RETIRED", "arifOS :8088 BUTA sejak 2026-10-08", "JANGAN start semula" | KVM4 `SOUL.md` lines 37–40 | KVM8 gateway **active**, MainPID 2577323, NRestarts=0, active since 10:00 today; `100.64.0.2:8088/health` = **200** from KVM8 *and* KVM4 | Every KVM4 turn is grounded in a false world model. It may refuse to route to the live kernel/gateway or escalate wrongly |
| C2 | **CRITICAL** | KVM4 SOUL = "LIVE mouth"; KVM8 identity lock = `hermesarifos_twin` **DORMANT** | KVM4 SOUL header; `/root/.hermes/IDENTITY_LOCK.json` on KVM8 | KVM8 handles 1,706 DM log lines today; KVM4 last successful Telegram send **18 Oct 17:34**, only 81 DM lines | Two contradictory "primary" identities. Human gets different answer depending which bot he opens |
| C3 | **HIGH** | Three bots can answer Arif's DM | KVM8 `@ASI_arifos_bot`, KVM4 `@hermesarifos_bot`, KVM2 `@Azwafazil_bot`; all allow chat `267378578` | KVM8 = primary; KVM2 answered Arif at 12:47 with **1,532s** latency; KVM4 zombie | Split memory/voice/latency. Arif may talk to Wawa believing it is Hermes |
| C4 | **HIGH** | KVM8 processes its own bot messages as inbound | 128 inbound events today from `chat=8410138119` (= Hermes bot id) out of 298 total inbound (~43%); one turn **4,090s, 39 API calls, 2,770 chars** | Delivery guard blocks the reply, but ingestion + LLM work already happened | Token burn, session pollution, queue overflow (15–20 events queued) |
| C5 | **HIGH** | `pre_tool_call` constitutional hook silently skips | 49 skips today: "skipped after previous timeout or while still running"; hook timeout=10s, fail_closed=true | Manual run = 43 ms, but under gateway load it overlaps/skips | Gate looks enforcing but is not. Capability ≠ authority |
| C6 | **HIGH** | KVM8 production runs an unmerged CI branch with 5,347 uncommitted insertions | `fix/ci-ruff-lint`, 1 commit ahead of fork main; `cron/scheduler_delivery.py` 807+/234−, `telegram/adapter.py` 4,540+/1,208−, untracked `gateway/delivery_guard.py` | Any `hermes update` = `git reset --hard` → identity-lock gate gone | Bot-to-bot delivery bug returns; silent constitutional regression |
| C7 | **HIGH** | KVM8 skill index obese | 1,203 skills in `.skills_prompt_snapshot.json` (~104k chars ≈ 26k tokens/turn); 797 symlinks; `.broken-archive/2026-10-18-f13-fasa1` still indexed; home 60 MB + AAA 46 MB | Capability is *less* because attention is diluted; archived skills still visible | Cost, latency, wrong-skill selection |
| C8 | **HIGH** | KVM8 Telegram ingress too open | `require_mention: false`, 30 `free_response_chats`, 634 blocked unauthorized users + 488 bot-target blocks + 155 "can't send to bot" today | Bot replies in many groups and to bots; only delivery is blocked | Noise, loops, wasted turns |
| C9 | **HIGH** | Version split | KVM8 0.21.5 / KVM2 0.21.5 / KVM4 0.20.1 vs upstream 0.22.2 | KVM4 is two minor releases behind; KVM8/KVM2 one | Different bugs, different behavior, update risk |
| C10 | **MED-HIGH** | KVM4 unit facts in SOUL are stale | SOUL: `RestartSec=30`, `StartLimit 5/300s`, `MemoryMax=1.5G`, boot 9 Oct 01:29 UTC | Actual user unit: `Restart=always`, `RestartUSec=5s`, `StartLimitInterval=0`, `MemoryMax=infinity`, active 17 Oct 08:06 UTC | Capacity/restart assumptions false |
| C11 | **MED-HIGH** | KVM4 has two cron registries | `~/.hermes/cron/jobs.json` = 15 jobs, only 2 enabled; `/root/HERMES/cron/jobs.json` = 28 jobs, executions.db last write **2 Sep** | Dead registry + duplicate `iron-radar` Friday 12:00 with KVM8 | Phantom jobs, duplicate human messages, false audit trail |
| C12 | **MED-HIGH** | KVM2 injects 44 KB stale law, but has 7 skills | `.hermes/AGENTS.md` 1,078 lines (44,545 bytes, rendered 11 Sep); KVM8 equivalent 161 lines (11,395 bytes) | Wawa carries a stale constitution and almost no capability | Context bloat; Wawa may cite doctrine that no longer exists |
| C13 | **MED-HIGH** | Timezone split | KVM8 system `Asia/Kuala_Lumpur` (+08); KVM4 & KVM2 system **UTC**; KVM4 config `Asia/Kuala_Lumpur`; KVM2 config `""` | Logs and systemd timers are 8h apart; KVM2 cron `05:00/13:00` likely fires 13:00/21:00 MYT | Incident correlation wrong; Azwa reminders at wrong hour |
| C14 | **MED** | Memory configuration split | KVM8 16,000/10,000 chars; KVM2 2,200/1,375; KVM4 defaults. All `MEMORY.md` sit exactly at cap (16,020/10,119 on KVM8 *and* KVM4) | KVM4 shares KVM8 memory via hourly sync but has a contradictory SOUL | Amnesia asymmetry; cognitive dissonance on KVM4 |
| C15 | **MED** | KVM4 external skills paths broken/duplicated | `external_dirs: ["/root/.hermes/skills-execution", "/root/.hermes/skills", "/root/AAA/skills"]`; last path **MISSING**; middle duplicates home | 30 extra skills only; missing AAA skills silently ignored | Capability claims false |
| C16 | **MED** | KVM8 remotes polluted | `origin` + `ariffazil-fork` same URL; `hermes-repo` → `github.com/ariffazil/HERMES` (different repo); upstream ref stale 20 days | Update/fetch ambiguity; wrong repo can be fetched | Wrong-branch/update mistakes |
| C17 | **MED** | KVM4 model note lies about address | Config note: "FED canonical KVM8 (af-forge) http://100.64.0.5:4000/v1" | `100.64.0.5` is KVM4 itself (local LiteLLM container), not KVM8 (100.64.0.2) | Wrong failover assumption; local container becomes single point |
| C18 | **MED** | KVM4 fallback bypasses FED | Fallbacks: direct `https://api.z.ai/...` + local `:4000` | Direct provider call outside FED governance | Authority/cost bypass; no federation telemetry |
| C19 | **MED** | KVM2 security posture | `group_allowed_chats` includes `"*"`; `allow_from: "*"`; email IMAP auth failing (281 errors today) | Any group + any sender; email reconnect noise | F6 privacy boundary weak; wasted cycles |
| C20 | **LOW-MED** | KVM8 profiles share one bot | `hermes_apex`, `hermes_asi`, `hermes_forge` all `bot_username: @ASI_arifos_bot`, same `ASI_ARIFOS_BOT_TOKEN` | Multiplex currently **skips Telegram** ("no bot credential in this profile's secrets") — latent only | If credentials are added, token conflict/409 |
| C21 | **LOW-MED** | KVM8 A2A binds `0.0.0.0:18089` | `ss` shows `0.0.0.0:18089` | KVM4 tunnel only needs `127.0.0.1` via SSH | Unnecessary network exposure |
| C22 | **LOW** | KVM8 service inventory | `hermes-health` :18791, `hermes-voice-governor`, `hermes-rasa` :18420, `hermes-a2a` :18089 | `hermes-mcp` :18087 has active callers (Hermes + OpenCode); others have no observed established callers | Inventory, not capability; verify consumers before keeping |

---

## 4. CONFIG DIFF MATRIX (OBS)

| Key | KVM8 | KVM4 | KVM2 |
|---|---|---|---|
| `model.default` | `hermes-default` | `i-arif` | `asi-555` |
| `model.provider` | `custom:fed-federation` (4012) | `custom` (`100.64.0.5:4000`) | `fed-litellm` (`100.64.0.2:4000`) |
| Fallbacks | MiniMax-M3, mimo-v2.5, DeepSeek direct | glm-5.3 (Z.AI direct), forge-777, MiniMax-M3 | agi-333, forge-777 |
| Memory | builtin; 16k/10k | defaults; 16k/10k files (synced) | 2.2k/1.375k |
| Skills roots | `~/.hermes/skills` + `/root/AAA/skills` (same as create_dir) | 3 roots (1 missing, 1 duplicate) | only `~/.hermes/skills` |
| Hooks | arifflow, inbound-injection-gate, reality-claim-gate, state-intake, temporal-seal, well-voice-bridge | arifflow, arifos-route, constitutional-guard, metabolism, reality-claim, verify-enforce | **none** |
| Plugins | 9 | 1 | 0 |
| MCP count | 28 | 5 | 7 |
| Cron | 30 | 15 live (2 enabled) + 28 stale | 3 |
| Profiles | 5 | 0 | 0 |
| `gateway.multiplex_profiles` | true | unset | unset |
| Telegram `require_mention` | false | unset (free_response specific) | true |
| Telegram group policy | free_response 30 chats; allow_from 21 | free_response 2 groups | group wildcard `"*"` |
| Timezone | Asia/Kuala_Lumpur | Asia/Kuala_Lumpur (system UTC) | `""` (system UTC) |
| Config version | 48 | 42 | 47 |

---

## 5. REMOVE — what to delete/archive

### All 3 nodes
1. **`.env.bak*`** in `~/.hermes/` (KVM8 1, KVM4 3, KVM2 5) — secret sprawl. Move to sealed vault; rotate any key that touched disk.
2. **SOUL/AGENTS/MEMORY backups** inside the live home (KVM4 8 SOUL + 18 MEMORY + 4 USER; KVM8 2 SOUL archives + 6 MEMORY backups; KVM2 2 SOUL + 2 USER) — archive to `/root/AAA/archive/`, not live.
3. **Old one-shot cron jobs** already past (KVM8 `arifos-deck-to-syed`; KVM4 `Wake up Arif ... 2026-08-29`) — delete.
4. **`.hermes_history` backups** (KVM8 6.1 MB + 2.2 MB; KVM4/KVM2 small) — archive.
5. **Stale `.skills_prompt_snapshot.json` backups** (KVM8 724 KB stale) — delete.

### KVM8 only
6. **1,203 → <200 skills.** Remove `.broken-archive` from the scan root; 797 symlinks are a maintenance trap; archive stale/duplicate skills. Target <20k tokens index.
7. **Duplicate/broken skills** — `apex_verdict_hold`, `qrl-arifos` appear in both home and AAA; decide one owner.
8. **Duplicate remotes** — keep `origin` + `upstream`; remove `ariffazil-fork` (same URL) and `hermes-repo` (different repo `ariffazil/HERMES`).
9. **Stale branches** (12 local) — tag then delete old deploy/upgrade/rescue branches after verifying no unique commits.
10. **`default` profile** — 1 file, stale since 6 Oct; remove or document as generator.
11. **`jobs.json.bak-*` (10 copies) + `jobs.json.proposed.json`** — archive outside cron dir.
12. **`hermes-health` :18791 and `hermes-voice-governor`** — no observed consumer; run a 7-day no-consumer proof, then remove. Keep `hermes-mcp`, `hermes-rasa`, `hermes-a2a` (named consumers/config).

### KVM4 only
13. **`/root/HERMES/cron/jobs.json` (28 jobs) + `executions.db` (last write 2 Sep)** — dead registry. One live registry only.
14. **18 `MEMORY.md.bak-fed-*` + 4 `USER.md.bak-*`** — archive.
15. **Stale SOUL topology block (lines 30–45)** — delete/replace; it is factually false.
16. **`profiles/` untracked in install tree** — remove or gitignore.
17. **Broken external dirs** — drop `/root/AAA/skills` (missing) and duplicate `/root/.hermes/skills`; keep `skills-execution` if used.
18. **Direct Z.AI fallback** — remove or justify as an explicit F13 bypass; prefer FED.
19. **Duplicate `iron-radar`** — disable on KVM4; KVM8 is owner.

### KVM2 only
20. **44 KB `.hermes/AGENTS.md` (1,078 lines, 11 Sep)** — replace with the KVM8-style pointer (161 lines) or regenerate from current fragments.
21. **Email platform** — disable until IMAP credentials are fixed (281 auth errors today).
22. **Group wildcard `"*"`** — remove; explicit allowlist only.
23. **Arif DM access** — remove `267378578` from Wawa's allowed/free-response if Wawa is Azwa-only.

---

## 6. FIX & HARDEN — before any improvement

### P0 — truth, identity, safety (do first, no upgrade)

| # | Action | Acceptance test | Rollback |
|---|---|---|---|
| P0-1 | **Freeze + anchors.** Tag all 3 installs `pre-reconcile-20261019`; snapshot configs; do not update. | 3 tags exist; configs backed up outside live dir | tags are immutable |
| P0-2 | **KVM4 SOUL truth repair.** Replace false topology block. Either (a) satellite worker: "KVM8 = live mouth, KVM4 = worker/A2A", or (b) distinct twin persona with its own bot. F13 binary required for (b). | `grep -E "RETIRED|BUTA|LIVE mouth"` returns only corrected text; KVM4 answer to "where is Hermes live?" matches probe | restore SOUL backup |
| P0-3 | **One mouth.** Only KVM8 `@ASI_arifos_bot` answers Arif DM. Disable KVM4 Telegram polling; remove Arif from KVM2 Wawa. | Exactly one bot replies in DM 267378578; KVM2/4 have no Arif DM sessions | re-enable unit |
| P0-4 | **KVM8 self-echo ingress filter.** Drop inbound if `from.id` ∈ IDENTITY_LOCK bots or `from.is_bot`. | 0 inbound from 8410138119/8149595687/8727562763; self-chat sessions absent for 24h | feature flag |
| P0-5 | **Hook enforcement.** Fix `pre_tool_call` concurrency/timeout; prove fail-closed. | Synthetic forbidden tool call blocked; no "skipped" warnings under 10 concurrent calls | disable hook only with F13 |
| P0-6 | **Commit/patch-carry identity lock.** Commit `delivery_guard.py` + `scheduler_delivery.py` + `adapter.py` to a carry branch; apply same discipline to KVM4's 4 carries + 21-line adapter fix. | `git status` clean; `git log origin/main..HEAD` documents each carry; update dry-run preserves files | revert commit |
| P0-7 | **Secrets hygiene.** Archive `.env.bak*`; rotate keys; restrict file modes (600); remove from repo trees. | No `.env.bak*` under `~/.hermes`; `find` shows 600 | vault restore |
| P0-8 | **Telegram ingress.** KVM8 `require_mention: true` for groups; cut `free_response_chats` to DM + named groups; KVM2 remove `"*"`. | Unauthorized/bot attempts drop >90% in 24h | config restore |

### P1 — convergence (before upgrade)

| # | Action | Acceptance |
|---|---|---|
| P1-1 | **Role matrix + config schema.** Publish one `HERMES_NODE_MATRIX.md`: KVM8 mouth, KVM4 worker/A2A (or distinct twin), KVM2 Azwa tenant. Align config version to 48 where possible. | Matrix reviewed; each node's SOUL points to it |
| P1-2 | **Cron ownership.** One owner per human job. Disable KVM4 duplicate `iron-radar`; delete dead registry; cap KVM8 human jobs to intentional set. | No two nodes same job/time; `jobs.json` valid |
| P1-3 | **Skills curation.** Exclude `.broken-archive`; dedupe; archive stale; run curator. Target <200 skills / <20k tokens. | Snapshot count <200; no broken category; latency drop measured |
| P1-4 | **KVM4 systemd normalization.** Convert user unit to system unit with wrapper (vault env), `--replace`, `ExecStartPre` duplicate check, `TimeoutStopSec` consistent; or explicitly document user-unit exception. | Reboot survives; exactly one gateway process; no 409 |
| P1-5 | **Timezone.** Set all system clocks to Asia/Kuala_Lumpur (or all UTC + explicit config); fix KVM2 `timezone: ""`. | `date` consistent; cron next-run matches intended MYT |
| P1-6 | **Model routing.** KVM4: local LiteLLM as FED seat; remove direct Z.AI fallback or label as sovereign override; fix the `100.64.0.5` vs `100.64.0.2` note. | Fallback chain passes through FED; telemetry visible |
| P1-7 | **Service inventory.** 7-day no-consumer proof for `hermes-health`, `hermes-voice-governor`; keep only named consumers. Bind `hermes-a2a` to `127.0.0.1`. | Services list = consumers list |

### P2 — upgrade & adoption

| Phase | Action | Gate |
|---|---|---|
| P2-1 | **Sync fork to upstream v0.22.2.** Merge upstream into fork; rebase/reapply KVM8 1 carry + dirty identity-lock patch; reapply KVM4 4 carries. | Fork builds; carry tests pass |
| P2-2 | **Canary KVM2** (cleanest, lowest risk) → v0.22.2; verify Wawa wrapper token isolation, Telegram, cron, memory. | 24h stable; one gateway; no token collision |
| P2-3 | **KVM8** → v0.22.2 after P0-6 + P1-3; verify gateway, kernel, MCP, hooks, delivery guard, DM. | 24h stable; self-echo 0; hook no skips; skill index <20k tokens |
| P2-4 | **KVM4** → v0.22.2. Prefer clean reset to fork carry branch + reapply 4 carries; convert to system unit. | 24h stable; one process; correct SOUL; no dead registry |
| P2-5 | **Adopt upstream features:** stable channel, `hermes pm`, checkpoints, managed scope, bot mode/multi-profile gateways, secrets providers, egress proxy, session storage recovery. | Each feature has an owner, test, and rollback |

---

## 7. UPSTREAM FEATURE CONTRAST

| Feature (v0.22.2) | KVM8 0.21.5 | KVM2 0.21.5 | KVM4 0.20.1 | Decision |
|---|---|---|---|---|
| Stable release channel | no (tracks fork main) | no (tracks main) | no (old branch) | Adopt — stops commit-chasing |
| `hermes pm` atomic package manager | no | no | no | Adopt — prevents half-applied updates |
| Bot Mode / per-profile bots | partial (multiplex, no bot creds) | no | no | Adopt for persona separation |
| Multi-profile gateways | partial | no | no | Adopt or remove dead profiles |
| Checkpoints & rollback | no | config key present | no | Adopt on KVM8/KVM4 |
| Managed scope | no | no | no | Adopt for satellite immutability |
| Secrets providers | flat `.env` | flat `.env` | flat `.env` | Adopt (1Password/Bitwarden/command) |
| Egress proxy / iron-proxy | no | no | no | Evaluate for KVM2 tenant isolation |
| Curator | dirs exist, 1,203 skills | 7 skills | 74 skills | Adopt + prune |
| Gateway reboot-start fix | no | no | no | **Critical** for KVM4 user unit |
| Session storage recovery | no | no | no | Adopt |
| Local models / desktop / connectors | n/a | n/a | n/a | Not needed for server nodes |

---

## 8. IMPROVEMENT PLAN (ordered, with evidence gates)

1. **Day 0 — Freeze & truth.** Tags, config snapshots, KVM4 SOUL correction, one-mouth decision. No upgrade.
2. **Day 1 — Stop the bleeding.** Self-echo filter, hook enforcement, Telegram ingress tightening, secrets archive, commit KVM8 identity-lock patch.
3. **Day 2–3 — Convergence.** Role matrix, cron ownership, timezone, skills curation (1,203 → <200), KVM4 systemd normalization.
4. **Day 4–5 — Fork sync.** Upstream v0.22.2 merge, carry reapply, build/test on a staging worktree.
5. **Day 6 — Canary KVM2.** Upgrade, 24h observation.
6. **Day 7–8 — KVM8.** Upgrade canonical, 24h observation, full functional probe (DM, group, cron, kernel, MCP, hooks).
7. **Day 9–10 — KVM4.** Rebuild/upgrade, convert unit, 24h observation.
8. **Week 2 — Adoption.** Stable channel, `hermes pm`, checkpoints, managed scope, bot mode, secrets providers, egress, session recovery.
9. **Week 3 — Measure.** Skill index tokens, DM latency, self-echo count, hook skip count, duplicate cron count, unauthorized attempts. Seal a before/after receipt.

**Do not:** run `hermes update` on KVM8 before committing the 5,347-line diff; reset KVM4 before capturing its 4 carries; delete skills before a snapshot; enable multiple profiles on the same bot token.

---

## 9. EVIDENCE APPENDIX (key probes)

- `hostname && tailscale ip -4`: forge/100.64.0.2, srv1946043/100.64.0.5, flow-edge/100.64.0.4.
- `hermes --version`: 0.21.5+4034 (KVM8), 0.21.5+3916 (KVM2), 0.20.1 (KVM4).
- `git rev-list --left-right --count HEAD...upstream/main`: KVM8 39/591 (stale ref); GitHub compare b221050c→349e4f7 = 11,087 behind.
- KVM2 `HEAD...origin/main` = 0/11,166; KVM4 `HEAD...nous/main` = 4/34,279.
- `systemctl show hermes-asi-gateway`: active, MainPID 2577323, NRestarts=0.
- `systemctl --user show hermes-gateway` on KVM4: MemoryMax=infinity, RestartUSec=5s, StartLimitInterval=0, active 17 Oct 08:06 UTC.
- KVM4 `SOUL.md` lines 37–40: false "KVM8 RETIRED / arifOS BUTA".
- KVM8 `IDENTITY_LOCK.json`: `hermesarifos_twin` = 7958220838, status **DORMANT**.
- KVM8 logs today: 298 inbound, 128 from chat 8410138119 (own bot id); one turn 4,090.6s / 39 API calls.
- KVM8 hooks today: 49 "pre_tool_call ... skipped".
- KVM8 skills snapshot: 1,203 skills, ~104,026 chars ≈ 26k tokens; 797 symlinks; `.broken-archive` indexed.
- KVM8 `git status`: 2 modified (+5,347/−1,442) + untracked `gateway/delivery_guard.py`.
- KVM4 cron: `~/.hermes` 15 jobs (2 enabled), `/root/HERMES` 28 jobs (executions.db last 2 Sep).
- Timezones: KVM8 +08; KVM4/KVM2 UTC; KVM2 config `""`.
- `100.64.0.2:8088/health` = 200 from both KVM8 and KVM4.

**Limits:** no Telegram bot getMe calls (identity from config/lock only); no secret values printed; no live config mutation; `git fetch` updated remote-tracking refs only. KVM4 last-success timestamps are from gateway logs, not Telegram API.
