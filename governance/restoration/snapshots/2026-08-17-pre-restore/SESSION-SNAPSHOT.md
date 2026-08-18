# Pre-Restore Probe Snapshot — 2026-08-17

> **Captured by:** 333-AGI / Kimi Code (FI-008) at session `SEAL-e2efa4c498024472`
> **Captured at:** 2026-08-17T23:44-23:50 UTC (≈07:44-07:50 MYT 2026-08-18)
> **Authoritative for:** comparing the federation state before vs after runbook execution

## Identity & authority

| Field | Value |
|---|---|
| session_id | `SEAL-e2efa4c498024472` |
| actor | `ARIF` (sovereign, identity claim recognized, system_exempt verification) |
| authority_band | `LIMITED_MUTATE` (mutation yes, seal no) |
| actor_cryptographically_verified | **false** ← sct_renew cron dead |
| substrate_state (init) | HEALTHY |
| substrate_state (observe, degraded) | DEGRADED ← kernel fragility on thin evidence |
| kernel_baseline G | 0.5188 |
| apex_scalars G / C_dark / h | 0.4417 / 0.1891 / 0.9455 |
| kernel epoch | 2026-07-03 |
| software release | arifos-1d03abe4c01d (drift=false) |

## VPS substrate (from arif_init snapshot)

| Metric | Value | Status |
|---|---|---|
| hostname | forge | — |
| load_1m | 2.23 | healthy |
| mem_used_pct | 57.7% | healthy |
| disk_used_pct | **80.2%** ⚠ | yellow zone, watch |
| organ SHAs | arifOS=1d03abe, A-FORGE=4c12b66, AAA=2980bad, GEOX=2aa1000, WEALTH=7c5634f, WELL=95ea631 | current |

## Federation probe (forge_probe)

| Organ | Alive | Latency |
|---|---|---|
| arifOS | ✓ | 9 ms |
| GEOX | ✓ | 75 ms |
| WEALTH | ✓ | 10 ms |
| WELL | ✓ | 28 ms |
| AAA | ✓ | 69 ms |

(6 of 7 — `arifFlow` per sovereign BOOT v6.0 boot is reported `down`; daemon service listed `running/active` in `forge_vps_services`, MCP call returned cached/static data — see arifFlow vector below.)

## arifFlow vector (QG.v0.3.1-vector, 100-window)

| Dimension | Band | Value | Pathological | Producer |
|---|---|---|---|---|
| ΔS (ds) | HEALTHY | −0.22 | no | arifOS |
| C_dark | HEALTHY | 0.1156 | no | A-FORGE |
| FQ | **PATHOLOGICAL** | 9.0 | **yes** | arifFlow |
| G | CAUTION | 0.5188 | no | A-FORGE |
| J | HEALTHY | 0.4588 | no | A-FORGE |
| Ω | **CAUTION** | 0.04 | no | 333-AGI |
| W3 | CAUTION | 0.7439 | no | A-FORGE |

**Diagnosis:** SIMULATION constellation (pathological) — verify-dominance, execution starvation. The constitution is on rails, but no one is driving.

**Scalars (deprecated):** `FQ=9.0` — fossilized (verify=90 / execute=10 over last 100 receipts)

## Service snapshot (forge_vps_services)

- All systemd services `running/active`
- 7 Docker containers healthy (searxng 3d, mcpjam-federation 54min, minio 2w, falkordb 2w, qdrant 9d, postgres 12d, searxng-redis 5d)
- mcpjam-federation: 54-minute uptime — recent spawn, verify it's the expected A2A test harness

## Cron registry drift (forge_vps_cron assert)

- **Added (9):** vault999-daily-backup, backup-federation, external_witness_probe, forge-drift-scanner, zero_day_sentinel, refresh_briefing (the 6 migrated to `/etc/cron.d/arifos-governed-obligations`) + `asi-pulse.sh` (cron: 30m), `sync-cockpit-static.sh` (cron: 5m), `forge-work-gc.sh` (cron: 19:00 daily)
- **Removed (15):** 6 duplicates of the migrated items + 9 casualties:
  1. `sct_renew.py` (30m) — **CRITICAL, gates crypto-verify**
  2. `fq-probe.sh` (15m) — feeds arifFlow FQ gate (fails-open without it)
  3. `arifFlow sync.sh` (5m) — keeps ledger fresh
  4. `machine_telemetry.py` (5m) — WELL telemetry (WELL state reported FRESH at 240s, so something else feeding it)
  5. `skill-mesh-sync.sh --check` (5m) — AAA mesh integrity
  6. `completion-promise-verifier.sh` (5m) — 888-APEX deployment gate
  7. `live-market.py` (15m) — arif-fazil.com live prices
  8. `refresh-institutional.sh` (30m) — arif-fazil.com public attestation
  9. `dynamic-gate.sh` (5m) — web-canon gate
- Live count: 66

## Surface audit findings (forge_surface_audit)

| Surface | Reality | Audit report | Verdict |
|---|---|---|---|
| A-FORGE affordances.yaml | 120 entries | says 50 PHANTOM, 50 drift | **broken** |
| A-FORGE live registry | 116 tools, 116 unique fingerprints, 0 dups | says 70 tools | **stale snapshot** |

**Action:** quarantined — `/root/.aforge/QUARANTINE-2026-08-17-surface-audit.md`

## A-FORGE write capability

- `/root/.aforge/` exists, mode 0755
- Last modified 2026-08-17T23:18:23 (5h before snapshot)
- Underlying EROFS on `cron.json` writes — consistent with systemd `ProtectSystem=full` lacking `ReadWritePaths=/root/.aforge`
- Fix queued in runbook step 3

## Port surface (forge_vps_ports)

- **18 public ports** (0.0.0.0 binding): 80, 443 (caddy), 3001 (tailscaled AAA), 4000 (haproxy), 4011 (litellm), 6274 (mcpjam), 7071 (tailscaled A-FORGE), 7072 (tailscaled), 8080 (haproxy), 8081 (tailscaled), 8083 (headscale), 8088 (tailscaled, arifOS main port), 8444 (hermes), 18082, 18083 (tailscaled GEOX/WELL), 22888 (sshd), 46590, 47166 (tailscaled)
- Internal-only ports: most everything else, bound to loopback
- Critical observation: arifOS `:8088` should be loopback-only per LOCALHOST_IS_PASSWORD doctrine but is now also reachable via tailscaled 100.64.0.2 → fd7a:115c:a1e0::2 — verify this is intentional Caddy/Cloudflare ingress

## Scars active (60 total, key ones)

- `scar_1786299569519_8ea94508` — GEOX registry drift (2026-08-09, 8d)
- `scar_1786367593205_8dc66fd4` — AAA partial-failure UP-vs-LOADED (2026-08-10, 7d)
- `scar_1786095766160_884859dd` — forge_vault aspirational receipt (2026-08-07, 10d)
- `scar_scar_004_16cdb990` — `actor_verified` single-writer violation (CRITICAL, 2026-07-04, ~6w)
- `scar_1785068666659_325f09a3` — structure-before-purpose COPILOT EUREKA (2026-07-26)

## Harness scope limits (this session)

- allowed roots: `/root`, `/tmp`, `/data`, `/var/log`
- `/etc/cron.d/`, `/var/spool/cron/`, systemd units: **OUT OF SCOPE**
- `forge_shell`: blocked by `LEASE_KERNEL_UNREACHABLE` (`arif_lease_inspect` not on canonical public surface)
- System-surface mutations require sovereign or another surface with shell access

---

## Post-restore delta (capture this after runbook execution)

To validate the runbook succeeded, capture the same fields again and check:

| Field | Pre | Expected Post |
|---|---|---|
| `actor_cryptographically_verified` | false | **true** |
| `substrate_state` (observe) | DEGRADED | HEALTHY |
| arifFlow FQ | 9.0 PATHOLOGICAL | 0.2-0.5 HEALTHY |
| arifFlow Ω | 0.04 | >0.30 |
| Cron drift added/removed | 9 / 15 | ≈ 9 / 0 (no phantom removals) |
| forge_surface_audit phantom_count (aforge) | 50 | ≤5 |
| A-FORGE EROFS on cron.json write | yes | no |
| Active cron `sct_renew.py` | no | yes |
| `arif_init` re-run: `actor_verified:cryptographically_verified=true` | no | yes |

If any "Expected Post" doesn't hold, step 6 of the runbook was incomplete.
