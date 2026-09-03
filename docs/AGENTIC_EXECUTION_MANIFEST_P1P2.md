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

*DITEMPA BUKAN DIBERI. Seals by kernel. Physics by silicon. No text seals. No exceptions.*
