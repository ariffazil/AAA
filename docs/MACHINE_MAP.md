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
| Hermes | **LIVE gateway** `~/.hermes` (KVM8 active, `hermes-asi-gateway.service`, arifflow-hook armed 2026-09-04) + `/root/.hermes-cold/` | KVM4 dormant backup | Azwa's own hermes-agent (kunci-mas vault) |
| Coder CLIs | ALL 12 FI seats | agy, kimi, grok, aider (+ccc-remote pool) | none (federation) |
| Web | caddy · 25 vhost confs `/etc/caddy/vhosts/*.conf` (corrected 2026-09-04 FI-008) · docker data plane (pg/redis/qdrant/searxng/minio/falkor) | — | caddy · nasf.cloud |
| Repos | ALL origin-synced: arifOS, AAA, A-FORGE, GEOX, WEALTH, WELL, arifFlow, arif-fazil.com, HERMES | 7 read-only mirrors (AAA behind by ff-pull, arifOS mirror stale) | SAF (azwafazil identity) |
| Fence | UFW active | **UFW active 2026-09-03** (22/tcp + tailscale0; KVM8→KVM4 + FED verified post-enable) | public SSH filtered |

## 2. Lanes (live-probed 2026-09-03)

- KVM4 → KVM8 kernel/AAA/FED = **200**
- KVM2 → KVM8 kernel/FED = **200**
- KVM2 → KVM4 :4000 = **TCP blocked, ICMP OK** (~~mechanism UNKNOWN~~ **SOLVED 2026-09-04 FI-008: Headscale ACL** — `/etc/headscale/acl.yaml` on KVM8, tag-based; `tag:flow-dmz` has no `tag:forge` dst grant. Same mechanism blocked KVM8→KVM4:18789 during OpenClaw cutover until ACL patch)
- KVM4 Hermes FED path = KVM4 → KVM8 :4000 → back to KVM4 litellm (**hairpin — KVM8 is mesh SPOF**)

## 3. Traps (each one has already bitten an agent)

| Trap | Truth |
|---|---|
| FED health endpoint | `/health/liveliness` ✅ — `/health` returns 000 (false-DOWN diagnosis) |
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
| OpenClaw edge split-brain | ~~gateway on KVM8~~ **edge = KVM4 since 2026-09-04 13:37 MYT** (FI-008 zen mission). KVM8 keeps `~/.openclaw` state + CLI (npm beta 2026.8.1-beta.3 REMOVED — schema-v1 state unreadable by it; single truth = /usr/bin 2026.7.1-2 = KVM4 parity). KVM8 units disabled but present (archive). KVM4 loopback shim: unit drop-in `40-loopback-nat.conf` DNATs 127.0.0.1:18789→100.64.0.5:18789 (code derives loopback API URL; bind=all rejected by schema) |

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
