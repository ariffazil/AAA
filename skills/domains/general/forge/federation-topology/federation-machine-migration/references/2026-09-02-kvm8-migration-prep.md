# KVM8 Migration Prep — Executed Manifest (2026-09-02)

First run of the federation-machine-migration playbook. Source: forge / KVM8 / 72.62.71.199 (af-forge compute, Tailscale 100.64.0.2). Target: UNKNOWN at close — sovereign said "get ready to move to new machine", details pending.

## Machine state at zen-close

- %st 76.3 (SEVERE Hostinger throttle) — cooldown protocol active (freeze non-critical, concurrency 1, IDLE >90%).
- Load 2.32 (falling from 9.52); mem 23G avail; disk 79% (304G/387G, 84G free).
- Box rebooted ~30 min prior (docker containers up 22 min: searxng, searxng-redis, minio, falkordb, qdrant, postgres).
- Known issues: `fq-probe.service` FAILED; tailscale `NoState` (control key error 522, logged out); SCT/token state normal otherwise.

## Git inventory (all pushed to github.com/ariffazil)

- arifOS, A-FORGE, GEOX, WEALTH, WELL: clean.
- AAA: committed `registries/federation/` + `registries/identity/` (4d97b418).
- HERMES: committed SOUL.md (Reality Compiler block), cron/jobs.json (28 jobs), kvm4-ccc-dispatch (f9cb4424).
- LEFT UNCOMMITTED deliberately: `skills/apex_verdict_hold/claude/SKILL.md` + `hermes/SKILL.md` deleted, `skills/apex_verdict_seal/` EMPTY dir — unverified half-finished consolidation; flagged in carry_forward for dedicated review.

## Deferred (until %st < 15)

- pg_dump / qdrant snapshot / minio mirror of postgres, qdrant, minio, falkordb, redis.
- Service restart investigations (fq-probe).
- Cron re-registration on target (jobs.json committed; local-only per session).

## What carried in carry_forward.json

`/root/AAA/carry_forward.json` (2026-09-02T00:40:00Z) + backup stamped to `~/.local/share/arifos/carry_forward_backups/cf-pre-migration_20260902T004527Z.json`. Contains zen_state, migration_manifest (what_moves_via_git / what_moves_manually / verification_after_move / deferred_heavy_ops), next_session.

## Next session start

1. Confirm target details (IP/user/OS).
2. Cooldown until %st < 15 → data dump → secrets transfer (SCP/rsync, never git) → deploy → run Step 4 verification.
3. Investigate fq-probe.service; resolve HERMES skill consolidation.
