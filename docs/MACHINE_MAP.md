# MACHINE MAP — arifOS Federation Three-Node SOT

> Verified live 2026-09-03 by FI-003 (from KVM8). Re-probe before acting — this map ages.
> Placement doctrine: `KVM4-WORKER/FED_PLACEMENT.md` (2026-09-02, F13 ratification pending):
> **KVM8 = Truth (Court) · AAA = Interface (Cockpit) · KVM4 = Execution (Workshop) · KVM2 = Witness (pending)**

## 0. Which machine am I on? — run FIRST, every session

```bash
echo "$(hostname) $(ip -4 addr show | grep -oE '100\.64\.0\.[0-9]+' | head -1)"
```

| Fingerprint | Machine | Canonical name | Aliases (do not use as truth) |
|---|---|---|---|
| `forge` + 100.64.0.2 | KVM8 | **af-forge** | vps, VPS-1325122, m1 |
| `srv1946043` + 100.64.0.5 | KVM4 | **kvm4-forge** | forge-core |
| `flow-edge` + 100.64.0.4 | KVM2 | **azwaos** | flow-edge, m2, wawa |

## 1. What lives where

| | KVM8 af-forge (seat) | KVM4 kvm4-forge (workshop) | KVM2 azwaos (witness) |
|---|---|---|---|
| Kernel (judge) | **:8088 — THE federation kernel** | — | arifosmcp FORK (Azwa lane, NOT the judge) |
| Organs | AAA :3001 · A-FORGE :7071/7072 · GEOX :8081 · WEALTH :18082 · WELL :18083 · arifFlow :7073 · FRAME :18085 · i-ARIF :18095 · VAULT999 · NATS | — | arifflow-internal fork :7073 · fed-router :7075 |
| FED :4000 | HAProxy front door → KVM4 | **litellm (docker, binds `100.64.0.5:4000` ONLY)** | TCP blocked (ICMP OK) |
| Hermes | `/root/HERMES` heritage (reclaim-gated) + `/root/Hermes` case-twin shadow | **LIVE gateway** `~/.hermes` → KVM8 :8088 + :4000 | Azwa's own hermes-agent (kunci-mas vault) |
| Coder CLIs | ALL 12 FI seats | agy, kimi, grok, aider (+ccc-remote pool) | none (federation) |
| Web | caddy · 28 vhosts `*.arif-fazil.com` · docker data plane (pg/redis/qdrant/searxng/minio/falkor) | — | caddy · nasf.cloud |
| Repos | ALL origin-synced: arifOS, AAA, A-FORGE, GEOX, WEALTH, WELL, arifFlow, arif-fazil.com, HERMES | 7 read-only mirrors (AAA behind by ff-pull, arifOS mirror stale) | SAF (azwafazil identity) |
| Fence | UFW active | **UFW active 2026-09-03** (22/tcp + tailscale0; KVM8→KVM4 + FED verified post-enable) | public SSH filtered |

## 2. Lanes (live-probed 2026-09-03)

- KVM4 → KVM8 kernel/AAA/FED = **200**
- KVM2 → KVM8 kernel/FED = **200**
- KVM2 → KVM4 :4000 = **TCP blocked, ICMP OK** (mechanism UNKNOWN — docker iptables or ts ACL)
- KVM4 Hermes FED path = KVM4 → KVM8 :4000 → back to KVM4 litellm (**hairpin — KVM8 is mesh SPOF**)

## 3. Traps (each one has already bitten an agent)

| Trap | Truth |
|---|---|
| FED health endpoint | `/health/liveliness` ✅ — `/health` returns 000 (false-DOWN diagnosis) |
| Port meaning changes per machine | 7073 = arifFlow (KVM8) / arifosmcp-fork (KVM2); 4000 = HAProxy (KVM8) / litellm (KVM4); **7074 = fed-router on BOTH KVM8 (0.0.0.0, UFW-blocked off-box) + KVM2 (127.0.0.1)** — node-local agentic-loop redundancy, allowed. Always machine-prefix a port. |
| `/root/HERMES` vs `/root/Hermes` | case twins on KVM8. UPPERCASE = heritage (4.6G); lowercase = **receipts-only shadow (164K, no install)** |
| `/opt` typo-twins on KVM8 | arifflow+ariflow · arifOS+arifos · a-forge+af-forge — **resolved 2026-09-04**: dead twins (ariflow, arifOS, arifos-archive, a-forge + stray .baks) quarantined to `/root/BACKUPS/opt-quarantine-20260904/`; live = arifos (kernel 36G), arifflow, well, af-forge(→/root symlink) |
| A-FORGE :7071 drop-ins | `a-forge.service.d/` has 4 drop-ins — `privilege-inversion.conf` wins User=forge (lexical). 2026-09-04 split-brain fix: :7071 now serves fresh `/root/A-FORGE` dist (was stale `/opt/a-forge/app` Aug-19 build) |
| arif-fazil.com repo | local +63 / origin −13 **FORKED**; live site builds from the local 63 (dirty: vitals/index.html) |
| VAULT999 | ~~single copy~~ **mirror restored 2026-09-04**: `vault999-backup.timer` 03:47 nightly → KVM4 `/root/VAULT999-mirror-KVM8` (additive rsync, witness copy) |
| KVM4 mirrors | read-only compile inputs by doctrine — **single pen = KVM8**; never commit/push from KVM4 |
| AGENTS.md renderer | `render-agents.sh` referenced in header is PHANTOM — fragment + AGENTS.md must be synced manually |
| Machine aliases | each box answers to 3+ names across docs/memory — fingerprint (§0) is the only truth |
| KVM2 extras | ollama :11434 (local) · :8080 public · fed-router :7074 (corrected from stale :7075 in earlier map) |

## 4. Verification ledger

| When (MYT) | Verifier | Result |
|---|---|---|
| 2026-09-03 17:15 | FI-003 from KVM8 | all rows OBS; FED = 62 models via HAProxy; 9/9 KVM8 organs 200 |
| 2026-09-03 17:45 | FI-003 cross-check | freeze branch pushed ✓ · re-arm units disabled ✓ · AAA KVM4 = behind-not-diverged ✓ |
| 2026-09-04 02:20 | FI-008 from KVM8 | 3-machine inventory OBS: KVM4 = 26 units (litellm+hermes+opencode) · KVM2 = 31 units (forks+witness) · KVM8 split-brain FIXED · /opt quarantine · VAULT999 mirror armed |
