# PROPOSAL — VAULT999 lane & store consolidation (F13 decision required)

- **Date:** 2026-09-15 · **Host:** KVM8 · **Author:** Hermes ASI subagent
- **Status:** PROPOSED — **not executed.** No env file, no store, no container was changed.
- **Evidence:** `/root/AAA/registry/VAULT999-SOT-RECONCILIATION-2026-09-15.md`
- **Registry entry:** `DIV-VAULT999-MULTIPATH-SOT` in `/root/AAA/docs/deprecation-registry.json`

## Why this is not mine to decide

Three of the findings below are one-line config corrections in *shared* artefacts —
`/root/.secrets/kunci-root.env` and `kunci-mas.env` (sourced by the writer, the Hermes
gateway and multiple lanes) and `arifOS/deploy/docker-compose.yml`. Fixing them
silently would (a) modify a sovereign secrets file that other concurrent sessions are
also editing, (b) pre-empt a two-lane design that compose still declares, and (c) touch
store lifecycle — which the previous session explicitly blocked. So they are raised
here instead of executed.

## P1 — One declared seal writer: `:8100` (compose) vs `:5001` (systemd)

**Reality.** Two definitions of the vault writer coexist:

- **LIVE:** `vault999-writer.service` → `python3 /root/arifOS/deploy/vault999-writer/main.py`,
  listening on **`127.0.0.1:5001`** (pid 1450999). `curl :5001/health` → 200;
  `/vault/status` → `vault_seals_total=10492, chain_integrity=INTACT, chain_gaps=0`.
- **DEAD:** `arifOS/deploy/docker-compose.yml:20,78,82,124` declares a `vault999`
  service on **`:8100`**, expose to peers as `http://vault999:8100`. No such container
  runs (`docker ps`), and **nothing listens on `:8100`** (`ss -ltnp`: 0 matches;
  `curl :8100/health` → HTTP 000).

**The defect.** `/root/.secrets/kunci-root.env:298` and `kunci-mas.env:299` export
`VAULT_WRITER_URL=http://127.0.0.1:8100`, and lines 296/297 export
`VAULT_API_URL=http://localhost:8100`. These **override correct `:5001` defaults** in:

- `AAA/a2a-server/vault.js:12` (default `http://vault999-writer:5001`) — used at :136, :184, :202
- `AAA/a2a-server/seal_chain.js:96` (`REMOTE_URL = process.env.VAULT_WRITER_URL || null`)
- `arifOS/arifosmcp/cli/check.py:99` and `cli/seal.py:37` (defaults `/` on `:5001`)

So every seal/health call from those four consumers goes to a dead port. Only
`AAA/bin/probe_sys_health.sh` compensates — it records `env_writer_url` and
`env_writer_url_live=false` and falls back to `:5001` (lines 162-176, 343-344).

**Option A (recommended).** Repoint `VAULT_WRITER_URL` / `VAULT_API_URL` to
`http://127.0.0.1:5001` in `kunci-root.env` (296,298), `kunci-mas.env` (297,299),
`kunci-root.flat.env` (175,177), `kunci-mas.flat.env` (304,306); delete or comment the
compose `vault999` service stanza so one writer is declared once. *Cost:* a
`kunci-root.env` edit that every lane re-sources — needs a quiet window.
**Option B.** Stand the compose `vault999` service back up on `:8100` as the declared
edge. *Cost:* two writers, and `:5001` is the one already holding the Supabase DSN
(sourced from `/root/.secrets/vault.flat.env` by
`/usr/local/bin/vault999-writer-launcher.sh`), so this duplicates authority.
**Option C.** Leave as-is and keep the probe's STALE annotation as the only guard.
*Cost:* four consumers stay broken; the probe keeps reporting a dead env override.

## P2 — Retire, or formally tombstone, the frozen seal logs

`RULES: retirement blocked until telemetry store migrated/unified` (prior session).
The block is honoured; nothing was deleted. Re-confirmed independently today: the
local docker postgres on `127.0.0.1:5432` is **the live Kabarkan telemetry store**
(`observations` ins=58,454 / upd=406,136, autoanalyzed 2026-09-15 08:42; three
`kabarkan-*` units `active running`; `POSTGRES_URL=…@127.0.0.1:5432/vault999`), and only
its `vault_seals` *table* is stale (12 rows, `ins=0`, never analyzed). So the DB must
stay. That does not block retiring the **files**:

| Candidate | Size / mtime | Today's status |
|---|---|---|
| `/root/.local/share/arifos/vault999/outcomes.jsonl` | 1,894,697 B / 2026-08-25 16:45 | frozen; 3 consumers already repointed 2026-09-15; file retained |
| `/agent/vault999/receipts/outcomes.jsonl` | 11,401,151 B / 2026-08-26 05:44 | stale default in `memory_promotion_smoke.py:41` |
| `/root/VAULT999/state.db` | 0 B / 2026-09-08 | empty named "state" surface |
| `/root/VAULT999/{SESSION_SEAL_aa1cdfcb676f458b.json, epoch_state.json, outcomes.jsonl.gz, outcomes_manual.jsonl}` | — | broken symlinks into `/agent/vault999` |

**Ask:** F13 name the canonical write path for receipts that are *not* constitutional
seals. Today `git_to_vault.py`, `probe_sys_health.sh` and the tools I just fixed all
write/read `/root/VAULT999/outcomes.jsonl`, while the constitutional path is the
Supabase writer on `:5001` — those are two different things sharing the word "seal",
and the ambiguity is what produced this whole divergence.

## P3 — Small truth defects found while proving P1/P2 (no owner assigned)

1. `seal_chain_head.json` reports `seq=54`; `vault_head_attestation.json` reports
   `seal_head.seq=37` for the same chain. One is wrong.
2. `/root/.local/share/arifos/vault999/seal_chain.jsonl` last moved 2026-09-13 11:50
   while its `_head.json` moves every run — the chain file is lagging its head.
3. `arifflow_sealed.jsonl` carries 1,243 duplicate `receipt_id`s and 20 canned
   placeholder UUIDs (`550e8400-…`, `660e8400-…`), so any receipt count derived from it
   overstates distinct receipts (34,920 unique of 36,163 lines).

## Decision requested from F13

1. P1: Option **A / B / C**?
2. P2: name the canonical non-constitutional receipt path; authorise (or decline)
   tombstoning the four broken symlinks and `state.db`.
3. P3: assign or defer — no action taken.
