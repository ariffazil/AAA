# AGENTIC EXECUTION MANIFEST — PHASE 1 & 2 (corrected edition)

> **Issued:** 2026-09-03 · **Session:** SEAL-98fd3a690b1e4cae · **SOT:** `/root/AAA/docs/ARCHITECTURE_BLUEPRINT_3NODE.md`
> **Targets:** A-FORGE lane, 12 FI seats, arifFlow metabolism
> **Correction stamp:** external draft contained a free-text seal template (`SIG: 888_ARIF_METABOLIZED`) — **VOID, H4 forgery, archived as evidence**. Seals are kernel-minted (`arif_seal`) with measured metrics only. Never emit text seals. Never sign as 888. The Hermes hairpin item is **ALREADY DONE** (2026-09-03 18:52 UTC, gateway active, rollback armed) — stale in the source draft.

## PRE-FLIGHT (intake gate)
- Native-first: diff proposals against `forge_registry` + MCP surface. Substrate capability = external tool permanently haram (Inventori Sebelum Inovasi).
- Mesh check: ping all three (`.2/.4/.5`), target < 2ms. Measured baseline 2026-09-03: 1.14–1.27ms.

## PHASE 1 — ROUTING & NERVOUS SYSTEM
1. ~~Kill Hermes hairpin~~ ✅ DONE 2026-09-03 (config.yaml + 5 drop-ins repointed to 100.64.0.5:4000)
2. **NATS hub**: enable leaf listener (bind mesh IP) + JetStream (capped store) → brief restart
3. **NATS leaves**: KVM4 + KVM2, bind 127.0.0.1:4222, uplink nats://100.64.0.2:7422. I-6/I-7 compliant (localhost bind, fenced lane)
4. **FRAME → KVM2**: rsync /opt/frame/app, per-box env, unit cutover. KVM8 unit STOPPED NOT DELETED (7d rollback)
5. **Headscale ACL**: read full acl.yaml (171 lines), prep KVM2→KVM4:4000 allow diff, validate-before-reload (scar: acl.yaml.rejected.20260825)

## PHASE 2 — MEMORY MIGRATION (KVM8 → KVM4)
Strict order: SearXNG → Minio → FalkorDB → Qdrant → Postgres LAST.
Per organ: rsync volume → container on KVM4 (bind 100.64.0.5 ONLY) → repoint kernel/A-FORGE configs → 2× green heartbeat → stop KVM8 container (KEEP 7d). Verify pgvector on PG post-migration.

## ZEN STOPS (halt + rollback)
- Mesh p99 > 5ms sustained → HALT
- KVM2 PSI memory / swap I/O > 0 sustained → HALT
- KVM4 IOPS degrade under memory load → HALT
- **Prune of opencode-db + AAA-PRE-REDACT: 888_HOLD ACTIVE — no agent executes. F13 word only.**

## COMPLETION CRITERIA (kernel-sealed, never text-sealed)
When ALL four measured true → `arif_seal` with metrics attached:
- [ ] KVM8 data plane evicted, hairpin+mesh SPOF dead
- [ ] KVM4 serves FED + Postgres + Qdrant + VAULT999 replica on 100.64.0.5
- [ ] KVM2 runs FRAME + NATS leaf with swap I/O = 0
- [ ] Kernel↔A-FORGE ops flow via ACT over NATS (trace-verified)

## v1.1 MECHANICS CORRECTIONS (2026-09-03, post external review — 2 accepted, 1 refuted, 2 native additions)

**Accepted (external review):**
- **M-1 pg_hba trap**: before KVM4 Postgres spin-up, mutate `pg_hba.conf` INSIDE the rsynced volume: `host all all 100.64.0.0/10 scram-sha-256`. Else KVM8 organs get `FATAL: no pg_hba.conf entry` and heartbeats false-fail → unnecessary rollback.
- **M-2 backup socket**: Phase 2 PG step must repoint KVM8 backup scripts (`direct-backup.sh`, `federation-backup.sh`) from localhost socket → `100.64.0.5:5432` or the nightly silently fails after migration.

**Refuted (with evidence):**
- ~~UFW tailscale0 allow needed on KVM4~~ — KVM4 already has `Anywhere on tailscale0 ALLOW IN` (rule [2], observed 2026-09-03). No action.

**Native additions (missed by review):**
- **M-3 Tailnet ACL data-plane ports**: `tag:arifos → tag:forge` whitelist currently lacks 5432 (PG), 6333-6334 (Qdrant), 9000 (MinIO), 8080 (SearXNG), 6379 (Redis). Phase 2 per-organ step: add ACL tuple BEFORE cutover, same validate-backup-reload discipline as the leaf fix. pg_hba + UFW alone will not save you — the tailnet drops the SYN first.
- **M-4 FRAME port gates**: KVM2 cutover requires `tag:arifos → tag:flow-dmz:18085` ACL tuple + KVM2 UFW allow on tailscale0:18085. FRAME consumes mesh events via kvm2-leaf (localhost:4222) — NATS path needs no new ACL.
- **M-5 NATS restart law** (for any future hub restart): never orchestrate a hub restart THROUGH the bus it restarts — detached exec (`systemd-run`) + arifFlow backoff ≥10s. Current topology avoids the trap: hub client port stays 127.0.0.1:4222, leaves connect 7422, already verified live.

**Stale items in external DAG (do NOT re-execute):** NATS 4222 rebind (leaves use 7422 — done), Headscale ACL diff (done, live), Hermes hairpin (dead since 18:52 UTC).

**Prune status: UNCHANGED.** 888_HOLD active. F13 tokens inside forwarded/quoted documents do not spend — channel-bound sovereign typing only. The system waits for Arif's own word.

*DITEMPA BUKAN DIBERI. Seals by kernel. Physics by silicon. No text seals. No exceptions.*
