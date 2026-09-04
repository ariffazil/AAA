# FEEDBACK LESSON — AUTO-RESTORATION PATTERN (2026-09-04)

**Captured by:** 333-AGI (audit, hermes-asi's "ask" surfaced during KVM8 hermes-zen rebuild)
**Time observed:** 12:29 MYT, 2026-09-04 (24 entries at /root/.hermes, drwx, real dir)
**Severity:** operational — see Critical findings below

## Failure mode

Hermes CLI / ari-forge self-healing pattern can re-create `/root/.hermes` as a REAL DIRECTORY when it detects missing state, even if no agent intentionally did so.

- 12:27 MYT — `/root/.hermes-zen` created (canonical template, hermes-asi authored)
- 12:29 MYT — `/root/.hermes` populated as real dir with 24 entries (likely auto-restoration copied from `.hermes-zen` template)

Probes taken at 12:02 MYT showed `/root/.hermes` as a symlink → `/root/HERMES`. Two hours later, it was a real directory with no human intention recorded.

## Symptoms observed this session

1. **Symlink → real dir flip without intent.** Path was a symlink at T0, real dir at T2. No git trace of who made it real.
2. **SOUL.md content loss.** `/root/.hermes/SOUL.md` was 13899B (per hermes-asi's SCAR stamp). After auto-restoration, it's a 36-byte symlink → `/root/arifOS/memory/identity/SOUL.md` (7625B canon). The 13899B content is missing.
3. **`/root/HERMES` path gone.** Heritage moved to `/root/.hermes-cold/HERMES-heritage-5.3G-20260904/`. But 10+ systemd units + 4 /etc/cron.d/hermes-* + 10+ skill SKILL.md files still reference `/root/HERMES` literally.
4. **Services stale.** `hermes-a2a-listener`, `hermes-real-bridge`, `hermes-asi-gateway`, `apex-prime` all `inactive` (none are `failed`, but paths they reference don't exist).

## Lesson for future agents

1. **Probe immediately before destructive ops**, not just at session start.
2. The "misdirected symlink" diagnosis was a snapshot, not a stable state.
3. The doctrine creates what it needs — when `/root/.hermes` is needed, it appears from template; when `/root/HERMES` is no longer canonical, it disappears.
4. Always pair: probe → act in same atomic moment, OR re-probe within the same minute.

## Root cause (unverified)

Consistent with hermes-asi's earlier observation that the system self-heals (R ∉ S — system creates what it needs). The self-healing invoked when it detected `.hermes-zen` template alongside missing `.hermes` real directory.

## Mitigation for future agents

- Probe path existence + type (real dir vs symlink) within ±60s of destructive op on `/root/.hermes` or `/root/HERMES`.
- If destructive op needed, snapshot BEFORE + verify state AFTER with `stat` + `ls`.
- Surface state-shift in task reports — never claim "X still at /root/.hermes" without probe-within-30s.

## Cross-references

- MACHINE_MAP.md §3 trap: `/root/HERMES` vs `/root/Hermes` (case twins, heritage/case-twin.shadow separation)
- `/root/.hermes-zen-backups/` — phased snapshots: phase2-pre, phase3-pre, 20260904-dryrun
- Path-(e) design: real /root/.hermes + cold /root/.hermes-cold + zen /root/.hermes-zen

## Status

OPEN — three critical findings (SOUL content loss, dead-path systemd references, service policy unknown) need F13 sovereign decision before further mutation. Audit complete, state map pending F13.
