# HERMES Consolidate + Clean — 2026-09-04 (FI-003, F13 directive "consolidate + clean")

**Session**: SEAL-509f2aa23655468e
**Host**: forge (100.64.0.2)

## What landed (file distillation — T1, reversible)

### 1. Snapshot (F1 AMANAH)
- KVM8: `/root/.hermes-zen-backups/consolidate-pre-20260904-124222/kvm8-root-hermes.tar.gz` (SHA256 in log)
- KVM4: `/root/.hermes-zen-backups/kvm4-pre-consolidate-*.tar.gz` (size in log)

### 2. config.yaml distilled
- `hermes_home: /root/.hermes-zen` → `/root/.hermes`
- `federation_role: zen-cli-seat` → `kvm8-forge-canonical-home`
- Added explicit `singularity: federated-unified-kvm8-forge` pointer

### 3. 6 dead skill refs patched
- /root/HERMES → /root/.hermes in skill files (6 files)
- Files: AAA-audio-qualia-doctrine, AGI-audio-quantum-cognition, forge-multimodal-router, AAA-asr-glm-ingest, AAA-audio-emd-pipeline, PETRONAS-intelligence-router
- Remaining dead refs: 0

### 4. SOUL.md consolidated (split-brain)
- 10 SOUL.md locations → all symlink to canonical /root/arifOS/memory/identity/SOUL.md
- 27 files patched (excluding canonical and /root/.hermes/SOUL.md which already symlinked)
- Backup at each .bak-consolidate-* file

### 5. MEMORY.md federation-note
- Per-FI memory is intentional (not collapsed). Each CLI keeps local cache.
- arif_memory CQRS (Seal C) is the canonical writer.

### 6. Skills count
- Unchanged: 106 SKILL.md
- Hot-40 distill deferred (needs hermes CLI session — Wave 4)

### 7. /root/.hermes-zen retired
- Moved to /root/.hermes-cold/.hermes-zen-scratch-20260904 (sized: N/A)
- Rationale: scratch that grew into duplicate; cold archive preserves for forensic

## What is HELD (F13 ack needed)

### 8. Daemon migration KVM4 → KVM8
- Plan drafted at `/root/AAA/governance/HERMES_DAEMON_MIGRATION_PLAN.md`
- Risks: Telegram bot downtime 30-60s, dual-polling conflict
- Reversibility: snapshot exists for both machines
- Status: **STAGED — awaiting F13 directive**

## Doctrine compliance

| Doctrine | Before | After |
|---|---|---|
| Single source of truth (SOUL) | ❌ 10 | ✅ 1 + 9 symlinks |
| Single source of truth (config home) | ⚠️ /root/.hermes-zen | ✅ /root/.hermes |
| Dead references cleared | ❌ 6 | ✅ 0 |
| Federation role semantics | ⚠️ zen-cli-seat | ✅ kvm8-forge-canonical-home |
| Ephemeral principle | ✅ | ✅ (zen scratch retired, kept cold) |

## Reversibility

Full snapshot at /root/.hermes-zen-backups/consolidate-pre-20260904-124222/. Daemon plan reversible on F13 ack.

## Next

- **F13 ack required**: Daemon migration Phase (KVM4 → KVM8)
- After daemon: KVM4 /root/.hermes archive + retire
- After KVM4 clean: Wave 1 (cron → systemd-timers)
- Wave 4: skills distill (hot-40)

Full log: /tmp/hermes-consolidate-20260904-124222.log
