# D4 — INFRA-WRITE LOCK DOCTRINE (DRAFT v0)

> **Status:** PROPOSED — awaiting F13 SOVEREIGN ratification (Arif). Not applied.
> **Origin:** Carry-forward open loop, 2026-09-15 · Author: 333-AGI (SEAL-ceba17c0b47340f6)
> **Authority ceiling:** This draft does NOT change A-FORGE behavior until ratified + wired into actionClassifier.

## 1. Problem

A-FORGE shell/filesystem actuators can mutate infrastructure surfaces (systemd units,
crontabs, Caddy configs, docker compose, `/etc`, secrets dir) with the same authority
as workspace edits. One ungoverned `forge_shell` call can take down the kernel, the
ledger writer, or the public edge. Today's F6-crypto-seal incident chain (writer pointed
at a ghost DB for 12 days) is the failure *smell*; the failure *class* is ungoverned
infra mutation.

## 2. Rule (proposed)

**INFRA_WRITE_LOCK (F1 AMANAH + F13 SOVEREIGN):**

> A mutation targeting an infrastructure surface requires, BEFORE execution:
> 1. `forge_lock(mode="acquire", resource_id=<canonical infra path/class>)` — held
>    for the mutation's duration, released with a receipt.
> 2. `arif_judge` verdict ≥ SEAL when the action class is irreversible
>    (service restart of another organ, unit file edit, crontab edit, Caddy, DNS).
> 3. An audit receipt naming: actor, target, diff-shape, rollback path.

**Infra surface classes (initial):**

| Class | Examples | Gate |
|---|---|---|
| `svc_unit` | `/etc/systemd/system/**`, drop-ins | lock + judge |
| `cron` | root crontab, `/etc/cron.d/**` | lock + judge |
| `edge` | Caddyfile, `/etc/caddy/**`, DNS/tunnel | lock + judge |
| `compose` | docker compose files, container lifecycle | lock + judge |
| `secrets` | `/root/.secrets/**` | F13 explicit (T3) |
| `kernel` | arifOS deploy/restart paths | lock + judge |
| workspace | `/root/<repo>` source edits, forge_work | current rules (no new gate) |

## 3. Enforcement point

A-FORGE `actionClassifier`: extend path classifier to tag infra classes
`EXECUTE_HIGH_IMPACT | INFRA`. `forge_shell` / `forge_filesystem` check the tag:
no `lock_id` in context → deny with `INFRA_WRITE_LOCK_REQUIRED` (fail-closed).
Session auth alone is insufficient — the lock is per-mutation.

## 4. Separation of powers alignment

- FRAME observes infra drift (ports/services/cron scanners) — FRAME never mutates.
- WELL mirrors machine state — WELL recommends, A-FORGE executes, under this lock.
- F6 hazard rule (separate, also pending F13): no organ may observe AND mutate the
  same object in one cycle. This lock is the mutation-side half of that rule.

## 5. Reversibility

- Lock acquire/release is metadata-only (reversible).
- The mutation itself keeps existing rollback requirements (backup before mutate).
- Rejecting ungoverned writes is fail-closed; no workflow depends on bypassing.

## 6. Ratification checklist (for F13)

- [ ] Arif ratifies doctrine text
- [ ] A-FORGE actionClassifier infra tags wired
- [ ] forge_lock resource classes registered
- [ ] One falsification test: ungoverned infra write attempt → INFRA_WRITE_LOCK_REQUIRED
- [ ] Receipt from first governed infra mutation (e.g., the pending ghost-postgres retirement)
