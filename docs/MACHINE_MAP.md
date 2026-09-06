# MACHINE MAP — arifOS Federation Three-Node SOT

> Verified live 2026-09-03 by FI-003 (from KVM8). Re-probe before acting — this map ages.
> Placement doctrine: `KVM4-WORKER/FED_PLACEMENT.md` (2026-09-02, F13 ratification pending):
> **KVM8 = Truth (forge) · AAA = Interface (Cockpit) · KVM4 = Execution (workshop) · KVM2 = Witness — labels ratified 2026-09-04 F13**

## 0. Which machine am I on? — run FIRST, every session

```bash
echo "$(hostname) $(ip -4 addr show | grep -oE '100\.64\.0\.[0-9]+' | head -1)"
```

| Fingerprint | Machine | Canonical name | Aliases (do not use as truth) |
|---|---|---|---|
| `forge` + 100.64.0.2 | KVM8 | **forge** | af-forge (legacy), vps, VPS-1325122, m1 |
| `srv1946043` + 100.64.0.5 | KVM4 | **workshop** | kvm4-forge (ssh alias), forge-core (retired) |
| `flow-edge` + 100.64.0.4 | KVM2 | **azwaos** | flow-edge, m2, wawa |

## 1. What lives where

| | KVM8 forge (truth) | KVM4 workshop (execution) | KVM2 witness |
|---|---|---|---|
| Kernel (judge) | **:8088 — THE federation kernel** | — | arifosmcp FORK (Azwa lane, NOT the judge) |
| Organs | AAA :3001 · A-FORGE :7071/7072 · GEOX :8081 · WEALTH :18082 · WELL :18083 · arifFlow :7073 · FRAME :18085 · VAULT999 · NATS · i-ARIF (no port — runs via FED chains; note **:18095 = apa-github-bridge, :18092 = apa-gemini-bridge** — corrected 2026-09-04 FI-008) | **OpenClaw edge :18789** (bind 100.64.0.5 — migrated from KVM8 2026-09-04 FI-008; caddy KVM8 vhosts claw/+openclaw.arif-fazil.com proxy here; KVM8 = state archive + CLI parity 2026.7.1-2, units disabled) | arifflow-internal fork :7073 · fed-router :7075 |
| FED :4000 | **Capability Routing Constitution** — KVM8 hosts HAProxy (intake) + fed-aware-middleware :4010 (413 clamp) + fed-router :7074 (intent classification) | **litellm (docker, KVM4 100.64.0.5:4000 — model brain)** | **Identity-preserving: each tier answers with its declared model_name (no silent cross-tier swap). 6 constitutional alias entries wired in 2026-09-04.** |
| Hermes | **LIVE `@ASI_arifos_bot` (♍ HERMES🪽)** `hermes-asi-gateway.service` · `~/.hermes` · **only poller of this bot** | KVM4 = OpenClaw `@AGI_ASI_bot` — not Hermes | `hermes-agent.service` = **Wawa persona, no Hermes Telegram token**. 2026-09-06 zen: wrapper unsets `TELEGRAM_BOT_TOKEN_ASI`. Wawa Telegram **HOLD** until a KVM2-only bot token exists (old `TELEGRAM_BOT_TOKEN` is 401). **Never source federation ASI token on KVM2.** |
| Coder CLIs | ALL 12 FI seats | agy, kimi, grok, aider (+ccc-remote pool) | none (federation) |
| Web | caddy · 25 vhost confs `/etc/caddy/vhosts/*.conf` (corrected 2026-09-04 FI-008) · docker data plane (pg/redis/qdrant/searxng/minio/falkor) | — | caddy · nasf.cloud |
| Repos | ALL origin-synced: arifOS, AAA, A-FORGE, GEOX, WEALTH, WELL, arifFlow, arif-fazil.com, HERMES | 7 read-only mirrors (AAA behind by ff-pull, arifOS mirror stale) | SAF (azwafazil identity) |
| Fence | UFW active | **UFW active 2026-09-03** (22/tcp + tailscale0; KVM8→KVM4 + FED verified post-enable) | public SSH filtered |

## 2. Lanes (live-probed 2026-09-03)

- KVM4 → KVM8 kernel/AAA/FED = **200**
- KVM2 → KVM8 kernel/FED = **200**
- KVM2 → KVM4 :4000 = **OPEN (HTTP 200 / 3.4 ms)** — ACL rule 7 (`tag:flow-dmz` → `tag:forge:22,7071,7072,7073,8088,4000,7422` + `tag:arifos:7073,22888,7422`) explicitly ACCEPTS. Added 2026-09-04 13:49 (during FI-008 OpenClaw cutover, BEFORE the canon entry was written 13:55). KVM4 UFW open on `tailscale0` (all tailnet) → Headscale ACL is the only cross-node gate. ICMP 1-2 ms. Other KVM2→KVM4 ports (`:18789/:4010/:8081/:18082/:6379`) remain correctly TCP-blocked. **CANON CORRECTION 2026-09-04 10:56 UTC FI-003**: prior entry was written before rule 7 was added; the lane was actually OPEN when MACHINE_MAP claimed it BLOCKED. Same probe (KVM2→KVM4:4000 curl /health/liveliness) — pre-FI-008 fix = 000, post-rule-7 = 200. Test-then-seal falsification gate passed.
- KVM4 Hermes FED path = KVM4 → KVM8 :4000 → back to KVM4 litellm (**hairpin — KVM8 is mesh SPOF**)

## 3. Traps (each one has already bitten an agent)

| Trap | Truth |
|---|---|
| FED health endpoint | `/health/liveliness` ✅ — `/health` returns 000 (false-DOWN diagnosis) |
| Dual Hermes Telegram | Two processes polling `@ASI_arifos_bot` = split-brain (KVM8 + KVM2). **Hermes lives only on KVM8.** KVM2 must not have `TELEGRAM_BOT_TOKEN_ASI` in the live process. |
| `@Azwafazil_bot` | **Unverified.** Do not put this handle in forum posts until `getMe` on a KVM2-only token returns that username. |
| `now` WELL 🟢 | TCP open ≠ WELL healthy. Body `status=degraded` + H-WELL SELF_REPORT/AGED = 🟡. M-WELL `machine_state.json` is a different plane. |
| Port meaning changes per machine | 7073 = arifFlow (KVM8) / arifosmcp-fork (KVM2); 4000 = HAProxy (KVM8) / litellm (KVM4); **7074 = fed-router on BOTH KVM8 (0.0.0.0, UFW-blocked off-box) + KVM2 (127.0.0.1)** — node-local agentic-loop redundancy, allowed. Always machine-prefix a port. |
| `/root/HERMES` vs `/root/Hermes` | case twins on KVM8. UPPERCASE = heritage (4.6G); lowercase = **receipts-only shadow (164K, no install)** |
| `/opt` typo-twins on KVM8 | arifflow+ariflow · arifOS+arifos · a-forge+af-forge — **resolved 2026-09-04**: dead twins (ariflow, arifOS, arifos-archive, a-forge + stray .baks) quarantined to `/root/BACKUPS/opt-quarantine-20260904/`; live = arifos (kernel 36G), arifflow, well, af-forge(→/root symlink) |
| A-FORGE :7071 drop-ins | `a-forge.service.d/` has 4 drop-ins — `privilege-inversion.conf` wins User=forge (lexical). 2026-09-04 split-brain fix: :7071 now serves fresh `/root/A-FORGE` dist (was stale `/opt/a-forge/app` Aug-19 build) |
| arif-fazil.com repo | ~~FORKED~~ **RECONCILED 2026-09-03 18:09** ("Reconcile main: 65 local commits") — 0 ahead/0 behind, verified in 2026-09-04 musyawarah; row kept as history |
| VAULT999 | ~~single copy~~ **mirror restored 2026-09-04**: `vault999-backup.timer` 03:47 nightly → KVM4 `/root/VAULT999-mirror-KVM8` (additive rsync, witness copy) |
| KVM4 mirrors | read-only compile inputs by doctrine — **single pen = KVM8**; never commit/push from KVM4 |
| AGENTS.md renderer | ~~render-agents.sh PHANTOM~~ **RESOLVED 2026-09-04 FI-008**: script exists at /root/scripts/render-agents.sh; render lag 49s — the 'phantom' claim was stale — fragment + AGENTS.md must be synced manually |
| Machine aliases | each box answers to 3+ names across docs/memory — fingerprint (§0) is the only truth |
| KVM2 extras | ollama :11434 (local) · :8080 public · fed-router :7074 (corrected from stale :7075 in earlier map) |
| **Headscale ACL = cross-node port gate** | Node tags: KVM8=`tag:arifos` · KVM4=`tag:forge` · KVM2=`tag:flow-dmz`. Cross-node ports beyond the granted sets are silently TCP-dropped (no UFW log, no reject — looks like a cable fault). Check `/etc/headscale/acl.yaml` FIRST for any cross-node block; file-mode policy → `headscale policy check -f` + `systemctl restart headscale` to apply (2026-09-04 FI-008, during OpenClaw cutover: +18789 arifos→forge; +8081/18082/18083 forge→arifos) |
| OpenClaw edge split-brain | ~~gateway on KVM8~~ **edge = KVM4 since 2026-09-04 13:37 MYT** (FI-008 zen mission). **KVM8 extraction COMPLETE 14:20 MYT**: no units, no binary (system npm pkg removed), state cold-stored `/root/.openclaw-cold/openclaw-heritage-2.8G-20260904/` (session-history delta Sep 3→4 lives ONLY there), infra crons re-homed to `/root/scripts/infra-crons/` under `/etc/cron.d/arifos-infra` (rollback: BACKUPS/openclaw-zen-20260904/cron-archive). KVM4 loopback shim: unit drop-in `40-loopback-nat.conf` DNATs 127.0.0.1:18789→100.64.0.5:18789 (code derives loopback API URL; bind=all rejected by schema). **TRAP: gateway restart within 5min of a failed boot trips the crash-loop breaker which SILENTLY suppresses telegram autostart** — symptom: pending_update_count rises, journal clean. Fix = one clean restart outside the window. |

## 4. Verification ledger

| When (MYT) | Verifier | Result |
|---|---|---|
| 2026-09-03 17:15 | FI-003 from KVM8 | all rows OBS; FED = 62 models via HAProxy; 9/9 KVM8 organs 200 |
| 2026-09-03 17:45 | FI-003 cross-check | freeze branch pushed ✓ · re-arm units disabled ✓ · AAA KVM4 = behind-not-diverged ✓ |
| 2026-09-04 02:50 | FI-008 | FLAME RETIRED (888 directive): free-tier dead, zero callers, fallback burned qwen-max -> FED flash lane; archive BACKUPS/FLAME-retired-20260904; organs.yaml + deprecation-registry tombstoned |
| 2026-09-04 02:20 | FI-008 from KVM8 | 3-machine inventory OBS: KVM4 = 26 units (litellm+hermes+opencode) · KVM2 = 31 units (forks+witness) · KVM8 split-brain FIXED · /opt quarantine · VAULT999 mirror armed |
| 2026-09-04 07:55 | FI-008 | HERMES row correction: /root/HERMES is NOT pure heritage — cron/ + logs/ are SAME INODES as ~/.hermes (live cron book lives there, orphaned since gateway moved to KVM4 Sep 3 04:15). SOUL.md forked: KVM8 twins 14436B Sep-2 vs KVM4 live 13257B Sep-3. See HERMES_FLEET_MAP.md §5 + holds.txt |
| 2026-09-04 08:45 | FI-008 | HAIRPIN DISPROVEN: hermes KVM4 model path is DIRECT (.5:4000, live curl + config + HAProxy backend all agree). KVM8 'hairpin' row applies only to public front-door traffic (single hop). KVM4 litellm = single model-compute node (Q6 lethality confirmed, circular claim retired). See forge_work/2026-09-04-federation-chaos-reconstruction/REALITY_MAP.md |
| 2026-09-04 13:55 | FI-008 | OPENCLAW CUTOVER COMPLETED (P2 from EXECUTION_MAP_v2): edge live on KVM4 :18789, health `{"ok":true}` loopback+tailnet+caddy, Telegram @AGI_ASI_bot polling (queue drained 4 pending), models via .5:4000, kernel/organs via .2:* (200). Fixed: config color field · 2 missing env drop-ins · telegram token file · 6 loopback URLs · Headscale ACL (2 rules) · caddy 2 vhosts · KVM8 npm-beta split-brain removed · art-governor muted. Receipt: forge_work/2026-09-04-openclaw-zen-3machine/ |
| 2026-09-04 13:58 | Antigravity | TOPOLOGY RESOLUTION (Option A+C): KVM8 `hermes-asi-gateway` active, `arifflow-hook` symlinked into `/root/.hermes/hooks/arifflow-hook`, systemd service reloaded, flow receipts armed, topology documented. |
| 2026-09-04 14:22 | FI-008 | OPENCLAW KVM8 EXTRACTION COMPLETE (F13 directive 'no chaos in KVM8, move all to KVM4'): units archived+removed · system npm binary removed · state → `.openclaw-cold/` (2.8G, same-fs mv) · 3 infra crons re-homed `/root/scripts/infra-crons/` + `/etc/cron.d/arifos-infra` (smoke-tested: hermes fq=BALANCED, briefing Gateway:OK via mesh, watcher exit 0) · telegram poller revived after breaker-suppression trap (inbound messages flowing, pending=0, 3 ESTAB to Telegram DCs). |
| 2026-09-04 14:32 | FI-008 | WAJIB CRON SET on KVM4 (F13 directive zen/heal/auto-learn): 3-machine cron map — KVM8 = 30+ governance jobs (correct home, untouched) · KVM2 = witness pulse · KVM4 had ZERO edge heal. Built: openclaw-watchdog v2 (*/5, telegram-drain check + budgeted systemctl restart + exception alerts — catches breaker-suppression that systemd cannot) + edge-dependency-probe (*/5 log-only). Auto-learn = gateway internal Memory Dreaming (0 3 * * *, ok) — no duplicate built. art-governor stale config entry removed. Receipt phase 3. |
| 2026-09-04 10:56 | FI-003 (FI-008 canon correction) | LANE CORRECTION KVM2→KVM4:4000 — falsified by live probe (HTTP 200 / 3.4 ms). ACL rule 7 (`tag:flow-dmz` → `tag:forge:4000`) added 13:49 MYT during FI-008 OpenClaw cutover, BEFORE the BLOCKED canon row was written 13:55. Canon corrected to OPEN. Test-then-seal falsification gate: PASS. |
| 2026-09-04 15:36 | FI-008 | CRON ROOT CAUSE SEALED: root crontab carried **literal `\r` TEXT** (58 occurrences — backslash-r characters, NOT CR bytes; every byte-tool was rendering text, python repr exposed it). Daemon dispatched poisoned command names → jobs FIRED but never STARTED (unsealed-counter, observatory, direct-backup, phoenix72 class). Fix: strip → 58→0, 70 lines intact. Proof fire 16:00. F13 gates executed: 1 ratify wrapper · 2 strip · 3 Gemini embedding exception Option 2 expiry 2026-10-04 · 4 sentinel disabled · 5 Zen Governor installed to edge workspace. Repo syncs A/B/C/D per audit packet. |

