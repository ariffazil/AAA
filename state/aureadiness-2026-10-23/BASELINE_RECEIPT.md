# BASELINE_RECEIPT — Phase 0 freeze

host: KVM8 af-forge (100.64.0.2) · measured 2026-10-23T03:36–03:50Z · read-only

## git state (SHA + dirty count — a SHA alone misleads)
| repo | HEAD | dirty |
|---|---|---|
| AAA | 2b8fb199 | 149 |
| arifOS | 50ba4a821 | 4 |
| A-FORGE | a87cda27 | 5 |
| WELL | 7a02251 | 1 |
| WEALTH | 428230f | 0 |
| HERMES | 1fa3f4c | 100 |

## listening endpoints
40 listeners captured → listeners.txt. Transport classes: 127.0.0.1-only (organs),
100.64.0.2 tailscale (FED 4000, redis, nats, arifOS 8088, A-FORGE 7071/7072, arifFlow 7073,
GEOX 8081, WEALTH 18082, WELL 18083), public *:80/:443 (caddy), *:8083 headscale.

## services
38 running units matching organ/gateway patterns → services.txt.

## identity registries
- /etc/arifos/identity.toml → DERIVED pointer to /root/AAA/identity.toml (b3 hash 73a284a6)
- /root/AAA/identity.toml → organ identity only
- /root/AAA/IDENTITY/identity.toml → **1 [actor.*] block (FI-008)**; keys exist for 333-AGI,
  555-ASI, 777-forge, 888-APEX, FI-008 → 4 keys unregistered
- /root/.hermes/IDENTITY_LOCK.json, lanes/people.yaml → human lanes, not actor keys
- agent cards: 5 role cards under a2a-server/agent-cards/roles (Hermes card marked "Draft, demoted 2026-09-04")

## canon paths
/root/AAA/{canon,instructions,governance,IDENTITY,VAULT999,skills} = chattr +i, mutation only via
canon-mutate (TREES now includes /root/AAA/scripts as of commit 7fa2e439).

## skill roots
- KVM8: /root/AAA/skills canonical 1256 entries · views 1259 · census PASS · broken 0 · diverged 0
- KVM4: /root/.hermes/skills 241 SKILL.md, no registry/census/index; /root/AAA = 3-dir stub

## callable vs catalog
tools/list handshake succeeded: arifOS 9 · A-FORGE 115 (7071 and 7072) · GEOX 27 · WEALTH 15 ·
WELL 10 · FED 7 · CHRON 22 · hermes-mcp 15. arifFlow + FRAME serve /health but **404 on /mcp**
(catalog-only for MCP purposes).

## scheduled work
33 jobs in one file (inode 5353039 reachable by 3 paths = symlinks, NOT a dual registry):
enabled 32, disabled 1, last_status=error 1 (Site drift watch).

## receipt channels
VAULT999 /opt/arifos/app/VAULT999 — 29 jsonl, 4 defective (see vault999-integrity.txt).
Kernel last_seal_timestamp 2026-10-23T03:34:09Z. vault_sealer_breaker closed, 0 recent failures.

## floor producers
13 floors active; **0 carry measured_at**; F1=0.0 fail, F8=0.5827 fail, F6=0.5 unmeasured,
F7=0.04 pass, F9=0.2087 pass, F12=0.0 pass; unmeasured_floors list contradicts
runtime_floors_status (C2).

## claim classification of this receipt
Every row above is OBSERVED at the timestamp stated, except the KVM4 counts which are
OBSERVED REMOTELY (ssh read-only) and the git dirty counts which are OBSERVED locally.
Nothing in this receipt is DERIVED or REPORTED. Sources unreadable: none — every probe
returned a value; two organs answered /health but not /mcp (recorded as catalog-only).
