# VAULT999 — SINGLE SOURCE OF TRUTH RECONCILIATION (KVM8)

- **Date:** 2026-09-15 (UTC+08)
- **Host:** KVM8 (arifOS federation VPS)
- **Author:** Hermes ASI subagent — task `VAULT999-SOT-RECONCILIATION`
- **Scope:** read + document. **No store deleted, moved or retired.** Prior session
  explicitly blocked retirement of the local postgres; that block is honoured.
- **Edits made:** 4 stale consumers corrected (timestamped `.bak` each) + this doc +
  `deprecation-registry.json` entries + 1 proposal. Env/secrets files NOT touched.

---

## 1. TRUTH TABLE — every path / env var that reads or writes VAULT999 seals

Legend: **LIVE** = actively advancing, trustworthy · **STALE** = exists but frozen,
must not be treated as current · **EMPTY** = exists, zero content · **DEAD** = no
listener / unresolvable · **ALIAS** = same inode as a LIVE path.

### 1a. The authoritative store

| # | Path / var | Used by (process / script) | State | Evidence |
|---|---|---|---|---|
| 1 | **Supabase Postgres via `VAULT999_DB`** (`<supabase-project-ref>@<supabase-pooler-host>:5432`) | `vault999-writer.service` → `python3 /root/arifOS/deploy/vault999-writer/main.py` (pid 1450999). The ONLY component allowed to INSERT `vault_seals` (`main.py:5`). | **LIVE — AUTHORITATIVE** | `vault_seals` = **10,484 rows** @15:11 UTC; `min(sealed_at)`=2026-05-25, `max(sealed_at)`=**2026-09-15 15:10:27+00**; **480 rows in last 24h** |
| 2 | `http://127.0.0.1:5001` (`/vault/status`, `/health`) — the writer's HTTP face | `probe_sys_health.sh:71`; any seal-truth consumer | **LIVE** | `curl :5001/health` → **200**; `/vault/status` → `vault_seals_total=10492`, `chain_integrity=INTACT`, `chain_gaps=0`, `append_only_enforced=true`, `pending_holds=0`; port confirmed via `ss -ltnp` (pid 1450999, started 2026-09-15 17:13:55) |
| 3 | `VAULT999_PG_URL` (Supabase pooler **:6543**) | writer env | **LIVE** | Same Supabase project as #1, transaction-pooled port |
| 4 | `VAULT999_PATH=/root/VAULT999/outcomes.jsonl` | writer env; `probe_sys_health.sh:72`; `git_to_vault.py:25` (via arifOS alias) | **LIVE** | **28,415,751 B**, mtime 2026-09-15 23:1x, **~89,900 lines and observably growing during this session** (89,826 → 89,896 → 89,931). Record schema: `{"ts","event","actor","session","tool","verdict","payload_hash","prev_hash","chain_hash"}` |

### 1b. Live aliases of the authoritative event log (same file, different paths)

| # | Path / var | Used by | State | Evidence |
|---|---|---|---|---|
| 5 | `/root/arifOS/VAULT999/outcomes.jsonl` | `arifFlow/scripts/arifflow_digest.py` (shadowed — see §1d); `git_to_vault.py:25` | **ALIAS (LIVE)** | Same file: `dev 2049, inode 2759799`, byte-identical, 28,415,751 B |
| 6 | `/var/lib/arifos/vault/outcomes.jsonl` (`ARIFOS_VAULT_PATH=/var/lib/arifos/vault`) | writer env; flat-vault consumers | **ALIAS (LIVE)** | **symlink** → `/root/arifOS/VAULT999/outcomes.jsonl`; `stat -L` → `dev 2049 inode 2759799`, same size |

> Note: paths 4/5/6 all address **one file**. No bind entry for them appears in this
> namespace's `/proc/self/mountinfo` (only 65 lines; `/root` itself is not listed), so
> the mount topology could not be fully witnessed from inside — but device+inode
> identity is conclusive that these are the same content.

### 1c. Live *derived* ledgers that are NOT the seal store

| # | Path | Used by | State | Evidence |
|---|---|---|---|---|
| 7 | `/root/VAULT999/arifflow_sealed.jsonl` | `arifflow_digest.py:16` (via arifOS alias); `AAA/scripts/reality_quotients.py:41` | **LIVE (mirror, not seals)** | **36,166 lines / 11,077,777 B**, mtime 2026-09-15 23:06. 36,163 JSON-parseable, 3 malformed. **36,163 entries carry NO `timestamp`/`created_at`.** Keys: `chain_entry_hash, chain_position, prev_hash, receipt_id, vault_entry_id, body_hash, genesis_anchor, parent_receipt_hashes, routed_organ` |
| 8 | `/root/.local/share/arifos/vault999/seal_chain_head.json` | many arifOS runtime modules (`organs_standards.py:172,346`, `rest_routes/vault_verify.py`, `observatory_emit.py:256`…) | **LIVE** | 465 B, mtime 2026-09-15 23:00:17, `seq=54`, `canonical_entries=54`, `historical_entries=255` |
| 9 | `/root/.local/share/arifos/vault999/seal_chain.jsonl` | `causal_spine.py:34`, `opencode_agentic.sh:19`, `vault_mirror_sync.py:58`, `observatory_emit.py:211`… | **LIVE-but-lagging** | 443,776 B, mtime **2026-09-13 11:50:56**, 264 lines (head advances, chain file does not) |
| 10 | `/root/.local/share/arifos/vault999/drift_log.jsonl` | `drift_check_live.py:16`, `build_public_state.py:1242` | **LIVE** | 6,432,479 B, mtime 2026-09-15 23:00:04, 4,589 lines |
| 11 | `/root/AAA/state/vault_head_attestation.json` | `probe_sys_health.sh:76` (truncation detector) | **LIVE** | 598 B, mtime 2026-09-15 23:00:04; attests `outcomes.lines=89,788` — below the live 89,9xx, i.e. append-only intact (no truncation) |

> **The `.local/share/arifos/vault999/` DIRECTORY is not stale.** Only *one file
> inside it* is frozen (§1d #12). Any doc claiming "the `.local/share` vault is dead"
> is over-broad.

### 1d. STALE / DEAD / EMPTY

| # | Path / var | Used by | State | Evidence |
|---|---|---|---|---|
| 12 | `/root/.local/share/arifos/vault999/outcomes.jsonl` | **pre-fix:** `A-FORGE/duties/aed.py:534` (L6 liveness), `A-FORGE/duties/memory_promotion_smoke.py:191` (L6 fallback), `arifOS/scripts/auto_remediate.py:23` (**WRITE target**). Correctly annotated as stale by `AAA/bin/probe_sys_health.sh:73,239-244` | **STALE (FROZEN)** | 1,894,697 B, **mtime 2026-08-25 16:45:18**, 2,953 lines. Last record: `{"skill":"hermes-coding-gateway","version":"1.0.0-2026.08.25","actor":"333-AGI",...}`. `inode 3277578` — a different file from the live log |
| 13 | `/agent/vault999/receipts/outcomes.jsonl` | `A-FORGE/duties/memory_promotion_smoke.py:41` — **default** `VAULT_OUTCOMES` | **STALE** | 11,401,151 B, mtime **2026-08-26 05:44**. `inode 46161949` |
| 14 | `VAULT_WRITER_URL=http://127.0.0.1:8100` — `/root/.secrets/kunci-root.env:298`, `/root/.secrets/kunci-mas.env:299` (and the `.flat.env` twins at 306/177) | read by `AAA/a2a-server/vault.js:12,136,184,202`, `AAA/a2a-server/seal_chain.js:96`, `arifOS/arifosmcp/cli/check.py:99`, `arifOS/arifosmcp/cli/seal.py:37`, `AAA/bin/probe_sys_health.sh:162` | **DEAD** | `ss -ltnp` shows **no `:8100` listener** (0 matches); `curl :8100/health` → **HTTP 000**. These env values OVERRIDE consumers' correct `:5001` defaults |
| 15 | `VAULT_API_URL=http://localhost:8100` — `kunci-root.env:296`, `kunci-mas.env:297` (`.flat.env` 304/175) | same env surface | **DEAD** | as #14 |
| 16 | `arifOS/deploy/docker-compose.yml:20,78,82,124` (`http://vault999:8100`, `PORT: '8100'`) | compose definition of a `vault999` service | **DEAD (not running)** | `docker ps` shows no `vault999*` container; only the systemd writer on `:5001` exists |
| 17 | `127.0.0.1:5432` docker postgres, db `vault999`, table `vault_seals` | `POSTGRES_URL` consumers; the writer only if its DSN defaults (see §3) | **STALE (seals)** | **12 rows**. `pg_stat_user_tables`: `vault_seals ins=0`, `last_autoanalyze=never`. Schema differs (`sealed_at`, `prev_seal_id`) |
| 18 | `POSTGRES_URL=postgresql://arifos_admin:***@127.0.0.1:5432/vault999` | arifOS kernel telemetry / Kabarkan | **LIVE for telemetry, STALE for seals** | Same DB, different tables: `observations` **ins=58,454 / upd=406,136**, autoanalyzed 2026-09-15 08:42; `observations_pre_d2` **ins=203,064**. Kabarkan units all `active running`: `kabarkan-collector.service` (otelcol), `kabarkan-worker.service`, `kabarkan-health.service` |
| 19 | `/root/VAULT999/state.db` | — | **EMPTY** | 0 bytes, mtime 2026-09-08 |
| 20 | `/var/lib/arifos/vault/outcomes.jsonl.DEPRECATED` | — | **STALE** | 45,233 B, mtime 2026-05-14, 1,524 lines (already tombstoned by name) |
| 21 | `/root/VAULT999/vault999_legacy.jsonl` | — | **STALE (frozen, `-r--r--r--`)** | 163,091 B, mtime 2026-05-27 |
| 22 | `/root/VAULT999/arifflow_sealed_rg2.jsonl` | `reality_substrate_classify.py:69` | **STALE (superseded fork)** | 29,424 lines / 12,129,778 B, mtime 2026-09-12 20:45 |
| 23 | `*.pre-repair-*`, `*.bak-*`, `_archive/`, `backups/` | — | **BACKUPS** | e.g. `outcomes.jsonl.pre-repair-20260802-081304` (2,032,263 B) |

---

## 2. VERDICT

**The authoritative VAULT999 seal store on this host is the Supabase Postgres
`vault_seals` table reached through `VAULT999_DB`, and it is read and written ONLY
through the seal writer `vault999-writer.service` on `http://127.0.0.1:5001`**
(`/root/arifOS/deploy/vault999-writer/main.py`, which declares itself the sole INSERT
path at line 5). At 2026-09-15 15:11 UTC that store held **10,484 rows with the newest
seal at 15:10:27 UTC and 480 seals in the trailing 24 hours**, and the writer reported
`chain_integrity=INTACT, chain_gaps=0, append_only_enforced=true`. The on-disk event log
that accompanies it is **`VAULT999_PATH=/root/VAULT999/outcomes.jsonl`** — 28.4 MB,
~89,900 lines, still growing at 23:1x local, and reachable identically through
`/root/arifOS/VAULT999/outcomes.jsonl` (same `dev 2049 inode 2759799`) and through the
symlink `/var/lib/arifos/vault/outcomes.jsonl`. Every other path in the federation is
either an alias of those two, a *derived* ledger (the arifFLOW receipt mirror, the seal
chain, the drift log), or dead. The dead one that actually mattered is
**`/root/.local/share/arifos/vault999/outcomes.jsonl`** — frozen since **2026-08-25
16:45:18** at 2,953 lines — and three consumers were still wired to it:
`/root/A-FORGE/duties/aed.py:534` (its L6 VAULT999 liveness check tested only
`exists()` + `lines > 0`, so a file frozen for 21 days scored a permanent false-green),
`/root/A-FORGE/duties/memory_promotion_smoke.py:191` (same frozen file as its L6
fallback, on top of a primary default of `/agent/vault999/...` that is itself stale at
2026-08-26), and — worst — **`/root/arifOS/scripts/auto_remediate.py:23`, which opened
the frozen file with mode `"a"` at line 147 and appended every auto-remediation receipt
into it**, i.e. real receipts were being written to a ledger the federation had stopped
advancing three weeks earlier. All three are fixed in place (§3). Separately, the
`VAULT_WRITER_URL`/`VAULT_API_URL` pair set to **`http://127.0.0.1:8100`**
(`/root/.secrets/kunci-root.env:296,298` and `/root/.secrets/kunci-mas.env:297,299`) is
**dead** — nothing listens on `:8100` and a probe returns HTTP 000 — and because those
env values override the correct `:5001` defaults inside
`AAA/a2a-server/vault.js:12`, `AAA/a2a-server/seal_chain.js:96`,
`arifOS/arifosmcp/cli/check.py:99` and `cli/seal.py:37`, every one of those consumers
is pointed at a dead port; that fix was deliberately **not** made and is raised as a
proposal (§4) because it is a shared-secrets, two-lane architecture decision. Finally,
`127.0.0.1:5432` (docker postgres, db `vault999`) is **not** a pure ghost — it is the
live Kabarkan telemetry store (`observations`: 58,454 inserts / 406,136 updates,
autoanalyzed 08:42 today, serving three active `kabarkan-*` units) — and only its
`vault_seals` table is stale (12 rows, `ins=0`, never analyzed). That independently
corroborates the e35 carry-forward and re-confirms the retirement block: the local
postgres must stay until the telemetry store is migrated.

---

## 3. FIXES APPLIED (all with timestamped `.bak-20260915T151333Z`)

| File | Change | Why it is provably wrong |
|---|---|---|
| `/root/arifFlow/scripts/arifflow_digest.py` | `VAULT_ACTIVITY` event no longer claims a 24h window; now reports cumulative entries, chain count and max position, with an explicit `Window: NONE` | The source records carry **no** `timestamp`/`created_at`, so `read_jsonl(path, since)`'s filter is inert and the count was always whole-file cumulative (§4) |
| `/root/A-FORGE/duties/aed.py:534` | `vault_path` → `/root/VAULT999/outcomes.jsonl` | Pointed at a file frozen since 2026-08-25; `exists()`+`lines>0` made L6 a permanent false-green |
| `/root/A-FORGE/duties/memory_promotion_smoke.py:191` | L6 fallback → `/root/VAULT999/outcomes.jsonl` | Fallback targeted the same frozen file (primary default `/agent/vault999/...` is stale too) |
| `/root/arifOS/scripts/auto_remediate.py:23` | write target → `/root/VAULT999/outcomes.jsonl` | This is an **appender** (line 147); receipts were landing in the frozen ledger |
| `/root/AAA/docs/deprecation-registry.json` | +1 `open_divergences` entry `DIV-VAULT999-MULTIPATH-SOT`; +2 `deprecated_files` (frozen log, `/agent/vault999` log); +1 `deprecated_endpoints` (`:8100`) | Registry is the canonical place to record the divergence |

Verified after edit: all four files pass `python3 -m py_compile`; `arifflow_digest.py`
re-runs clean and now prints `36166 receipts in VAULT999 arifFLOW mirror (cumulative …)
/ Chains in file: 343 / Max chain_position: 5000`.

**Not edited (deliberate):** `/root/.secrets/*.env` (`:8100` — §4 proposal);
`/root/.hermes/cron/jobs.json` (the only occurrence of the dead path is in
`arif-morning-pulse`, which is **`enabled: false`** — no live cron consumer);
`AAA/bin/probe_sys_health.sh` (already correct — it treats `/root/VAULT999` as live and
`:8100` + the frozen log as STALE at lines 22-32 and 70-75).

---

## 4. THE arifFLOW DIGEST FIGURE — "34976 receipts / chain 0→147"

**Flagged: the digest is NOT reading a stale or duplicate source, but the METRIC it
publishes is wrong.**

- **Source is correct.** `arifflow_digest.py:16` reads
  `/root/arifOS/VAULT999/arifflow_sealed.jsonl`, which is an **alias/sibling of the live
  file** (`/root/VAULT999/arifflow_sealed.jsonl`, 36,166 lines, mtime 2026-09-15 23:06).
- **The "34976 … (24h)" number is a cumulative whole-file count, not a 24-hour count.**
  `read_jsonl()` filters on `entry.get("timestamp") or entry.get("created_at","")`; I
  measured that **36,163 of 36,163 parseable records have no such field**, so `ts` is
  always the empty string and the `continue` never fires. `34976` was simply this
  file's line count at the moment that digest ran — the file grows, and a live re-run
  during this task printed **36,166**. The "(24h)" label is fabricated, not measured.
- **"Chain positions: 0 → 147" is meaningless.** The code is
  `f"{vault_entries[0].get('chain_position')} → {vault_entries[-1].get('chain_position')}"`
  — the position of the **first line** and the **last line** of a concatenation of many
  separate chains. Measured on the live file: **343 chains** (343 records carry
  `chain_position: 0`), **max `chain_position` = 5000**, and the last two lines carry
  positions `0` then `1`. So `0 → 147` and today's `0 → 4` are both artefacts of which
  two records happened to be first/last; neither describes a chain length, and neither
  relates to the 10,484 seals in the authoritative store.
- **Also note:** the mirror is not pristine — 1,243 duplicate `receipt_id` values and
  20 entries bearing canned placeholder UUIDs (`550e8400-…`, `660e8400-…`) — so even a
  correctly-labelled cumulative count would overstate distinct receipts (34,920 unique
  of 36,163).
- **Ordering of magnitude:** 36k arifFLOW mirror receipt lines vs **10,484 authoritative
  `vault_seals` rows (480 in 24h)**. The two numbers were never comparable; the digest
  presented a mirror line-count as a seal count.

The digest has been corrected to state cumulative entries, chain count and max position
honestly, with `Window: NONE — source records have no timestamp field`.

---

## 5. RELATED DRIFT NOT FIXED (flagged, out of scope)

1. `seal_chain_head.json` says `seq=54`, while
   `vault_head_attestation.json` says `seal_head.seq=37` for the same chain. One of the
   two is wrong.
2. `/root/VAULT999` contains three **broken symlinks** into `/agent/vault999`:
   `SESSION_SEAL_aa1cdfcb676f458b.json`, `epoch_state.json`, `outcomes.jsonl.gz`,
   `outcomes_manual.jsonl`.
3. `/root/VAULT999/state.db` is 0 bytes but is still a named "state" surface.
4. `arifflow_sealed_rg2.jsonl` (29,424 lines) remains a stale fork read by
   `reality_substrate_classify.py:69`.
