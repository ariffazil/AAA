# PATH FORWARD — 2026-09-15

> **Sessions:** SEAL-9f5379ce7dc74636 (execution) → SEAL-ceba17c0b47340f6 (post-deploy verify)
> **Actor:** 333-AGI · **Kernel:** arifOS `106c82895` source==built==deployed, drift=0, /health SEAL 13/13
> **Inputs:** carry-forward gen-1789411108 (4 items) + deep-research probes across arifOS, WELL, vault999-writer, arifFlow, deploy scripts

---

## 1. CARRY-FORWARD ITEMS — ALL EXECUTED (receipts below)

### 1.1 M-WELL file path mismatch — FIXED (F1 reversible)
- **Witnessed:** repo copy `/root/WELL/machine_state.json` stale 3 days (Sep 12); live telemetry written by `well-machine-telemetry.timer` (systemd, 5-min cadence) to `/var/lib/well/machine_state.json`. `vitality_gate.py` and `/state/machine_state.json` symlink read the STALE repo copy → WELL organ degraded on 3-day-old silicon telemetry.
- **Fix:** repo copy → symlink → `/var/lib/well/machine_state.json`. One hop heals vitality_gate + `/state` chain. Rollback: `.bak` + `.bak-20260915-stale` preserved.
- **Verify:** reads live now (age ≈ telemetry cadence, ≤5 min). NOTE: the earlier carry-forward claim "missing at `/root/.local/share/well/`" was shadow — zero consumers reference that path.

### 1.2 Writer fix (rows label themselves from birth) — SHIPPED `38a474c16`
- **Witnessed (E4/G-09):** `arifosmcp/runtime/telemetry.py` hard-coded `organ="arifOS"` / `organ_id="arifOS"` at 3 emission sites (arifFlow forward, NATS, Kabarkan Postgres) → 100% of 201,495 rows mislabelled.
- **Fix:** `_derive_organ()`: `ARIFOS_ORGAN_ID` env → actor-prefix map (`geox/*`→GEOX, `333-AGI`→AAA, …) → legacy `arifOS` fallback. Conservative: agent_id format untouched (FQ lane continuity), unknown actors keep legacy label.
- **Activated** in kernel release `106c82895` (below). New rows label from birth; historic rows stay as-is (no backfill — honest).

### 1.3 F6 crypto seal — RECOVERED (root cause deeper than "signing service")
- **Symptom chain witnessed:** kernel audit receipts to `:5001/audit-receipt` 500'd since **Sep 3** (last row id 13299). Breaker flapping in kernel journal.
- **Root cause:** `vault999-writer.service` env file lacked working DSN binding → code default `host postgres` → `/etc/hosts` + docker port publish → **leftover docker postgres container** running the OLD `vault999` DB (pre-migration schema, `prev_seal_id` BIGINT) → INSERT bound seal_hash (text) into int column → 500 on every receipt for 12 days. The real (bare-metal, migrated) vault was untouched and healthy.
- **Fixes:** (a) launcher now sources canonical `/root/.secrets/vault.flat.env` (backup `.bak-20260915` kept); (b) `verify_writer_token` accepts `Authorization: Bearer` alongside `X-Writer-Token` (kernel sealer speaks Bearer; strict-only would 401 every receipt) — commit `514720b4c`.
- **Verify:** receipts **id 13301 + 13302** written to the real vault via both header paths. Writer health now reports `vault_seals_count: 10004` (real DB), was 12 (ghost DB).

### 1.4 Kernel deployment drift — RECONCILED `106c82895`
- **Witnessed:** source `490db466` (FI-008 flatten, Sep 15 16:36) vs deployed `30c7c8ff` → `arif_init` effective_verdict HOLD / DEPLOYMENT_DRIFT at session start.
- **Path:** 3 commits pushed (`38a474c16` writer self-label, `514720b4c` ToolResult kwarg + writer auth, `106c82895` canon-gate namespace fix) → `make deploy-release` (wheel build, venv install, manifest, restart, alignment check).
- **Bonus fixes inside this release:**
  - `ingress_middleware.py`: `ToolResult(structuredContent=)` → `structured_content` (fastmcp API) — was TypeError on **every 888_HOLD envelope**.
  - `deploy-release.sh` canon gate: compared ABI tool names vs policy capability ids (different namespaces — could never pass; earlier deploys used gate-less `deploy-local`). Now maps caps→tools, also rejects unknown caps.
- **Verify:** `/health` = healthy/SEAL/13 floors/drift `[]`; fresh `arif_init` verdict **SEAL**, substrate HEALTHY, `nine_signal: SELAMAT`, mutation_allowed=true.

---

## 2. NEW SHADOWS DISCOVERED (documented, not silently dropped)

| # | Finding | Risk | Suggested owner/lane |
|---|---|---|---|
| S1 | **Ghost docker postgres** still running (old `vault999` schema) on `127.0.0.1:5432` publish | Medium — any code defaulting to `host postgres` writes to a lying DB. Root cause of 1.3. | Retirement needs compose audit → T2/T3. Pair with D4 lock ratification (first governed infra mutation candidate). |
| S2 | `vault.flat.env` has `VAULT_WRITER_URL=http://127.0.0.1:8100` — **dead port** (writer binds 5001; nothing on 8100) | Low — kernel sealer defaults to 5001 in-code, so pipeline works; env value is a latent trap | One-line env correction; touches secrets file → apply under 5-R discipline or during D4-governed change |
| S3 | carry_forward v3 entries carry `agent: "unknown"` for some writers | Low — attribution gap in the federation's own memory | carry_forward.py writer validation (small) |
| S4 | WELL organ :18083 + GEOX :8081 still `degraded` on /health | Medium | Separate diagnosis; M-WELL heal (1.1) removes one likely input — re-probe next session before acting |

---

## 3. PENDING F13 RATIFICATION (plan only — no self-authorization)

Sequenced per prior session's recommendation, updated with today's evidence:

1. **F6 hazard rule** (gates everything): *No organ may observe AND mutate the same object in one cycle. FRAME observes → reports → arifOS judges → A-FORGE mutates.* Alert→write paths must pass `arif_judge` first.
2. **D1 — consumer for `observability.observations`** (G-09: 201,495 rows, zero readers): Option **0-A** Grafana PostgreSQL datasource (trivially reversible) → then 0-B FRAME-as-reader under the F6 rule.
3. **D2 — organ taxonomy v2:** Hermes drafts against `/root/AAA/federation/organs.yaml` → Arif ratifies → `/root/AAA/federation/organ_taxonomy.json`. Gates Phase-5 step 4. (Writer now self-labels from birth — 1.2 — so taxonomy fixes going-forward labels; backfill remains out of scope.)
4. **D3 — otelcol retire-vs-elevate:** single OTLP gateway vs in-process capture. Tie-breaker = Arif's trust of collector ops.
5. **D4 — infra-write lock doctrine:** DRAFT at `/root/AAA/governance/D4-INFRA-WRITE-LOCK-DOCTRINE-DRAFT-2026-09-15.md`. Separate workstream as directed. Includes falsification checklist + first-governed-mutation suggestion (S1 ghost-postgres retirement).
6. **Phase 5 sequence** (after D1 consumer exists): **E1** trace-context propagation in `telemetry.py` (producer-side, no DDL) → **E3** verdict grammar normalisation → **E2** token columns deferred until FED `otel_export` is on (else G-09 recurs one layer down).

---

## 4. VERIFICATION LEDGER (this session)

| Claim | Evidence |
|---|---|
| M-WELL reads live | file ts 09:15Z, age ≤ cadence; chain `/state`→repo→`/var/lib/well` |
| Writer self-label deployed | commit `38a474c16`; `_derive_organ` 9/9 logic cases; wheel `106c82895` running |
| Kernel drift zero | `/health` drift `[]`; init software_release source==built==deployed==`106c82895` |
| 888_HOLD envelope fixed | fastmcp `ToolResult` kwarg probe; journal error pre-fix |
| F6 receipt path healed | HTTP 200 ×2 (Bearer + X-Token), vault rows 13301/13302 |
| Canon gate sane | mapped-caps comparison passes on real registries |
| Federation pulse | kernel SEAL · A-FORGE healthy ×2 · arifFlow ok-v3-vector · WEALTH healthy · GEOX/WELL degraded (S4) |

## 5. NEXT SESSION ENTRY POINTS

- Re-probe GEOX/WELL degraded (S4) after M-WELL heal settles a full day.
- F13 batch: ratify F6 rule + D1 + D4 (three decisions, one sitting).
- S1 ghost-postgres retirement under D4 as first governed infra mutation.
- S2/S3 small config/attribution fixes.
