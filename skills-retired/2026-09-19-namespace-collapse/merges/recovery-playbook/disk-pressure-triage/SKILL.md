---
name: disk-pressure-triage
description: "Use when a host's disk is filling; reclaim space safely."
owner: Hermes
---
# Disk-Pressure Triage

A full disk is a consequence, not a cause. Reclaiming space before attributing the growth deletes the
wrong thing and destroys the evidence of what is actually filling the volume.

## Order of work

1. **Quantify, then rank.** Headline number first, then the top tree:
   ```bash
   df -h /
   du -sh /root/* 2>/dev/null | sort -rh | head -10
   ```
   Re-read `df` at the *end* of the session: a percentage that moved while you were reading means
   something is still writing, and the fix is not a one-time delete.

2. **Attribute the growth — newest first.** Disk pressure is almost always recent copies, not organic
   data:
   ```bash
   find <backup_root> -maxdepth 1 -type d -newermt '-2 days' -exec du -sh {} \;
   ```
   Pre-deploy snapshot trees, "unpushed-commits" bundles, and per-deploy site copies are the usual
   suspects — and also the safest to remove, *once proven obsolete* (step 5).

3. **Measure a content-addressed repo before proposing anything about it.** `du` reports the
   *physical* size of a deduplicating store, so the number a naive cleanup plan quotes as reclaimable
   is wrong by an order of magnitude:
   ```bash
   du -sh <repo>
   restic snapshots --compact | tail -3      # snapshot count + newest
   restic stats --mode restore-size          # logical size — compare against du
   ```
   A repo holding ~146 GiB logical in ~23 GB on disk is deduplicating ~84%: it is efficient, not
   bloated, and pruning it reclaims almost nothing while cutting the restore chain. **Never propose
   reclaiming `du` bytes from a dedup repo.**

4. **Verify retention is running — from the snapshot count, not the script text.** A policy declared
   in a backup script (`keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune`) is only a claim; the
   test is arithmetic against what exists. If the policy sum matches the snapshot count, pruning is
   happening and the repo is at its floor. If snapshots far exceed the policy, the `forget`/`prune`
   step is failing — *that* is the finding.

5. **Prove a one-off copy obsolete before deleting it.** For git bundles and "pushed-work" snapshots
   the contents are what matter, not the bundle's age or filename:
   ```bash
   for d in <repos>; do
     printf '%-10s %-40s ahead=%s\n' "$(basename $d)" \
       "$(git -C $d rev-parse --abbrev-ref HEAD)" \
       "$(git -C $d rev-list --count @{u}..HEAD 2>/dev/null || echo '?')"
   done
   ```
   `ahead=0` on every branch means the bundle can never be needed again. **Any repo with a non-zero
   count is off the delete list** — that is live unpushed work, and a bundle may be its only copy.

6. **Report two numbers, never one.** *Safe to reclaim now* (proven-obsolete copies, byte total) and
   *needs the owner's call* (retention class, tier-A/vault copies, anything authored by someone
   else). "Clean up the backups" is not a finding; "3.6 GB in already-pushed bundles — safe; the 23 GB
   repo is healthy and must not be touched; WAITING on the owner for the pre-deploy trees" is.

## Traps

- **An auth failure against a backup repo is not evidence the repo is damaged.** A wrong password
  source returns `wrong password or no key found`, which reads like corruption and is not. Check which
  credential file the backup script actually sources before concluding anything about the store.
- **A backup job that writes no log and no journal is blind.** `journalctl -u <backup>` returning
  `No entries` alongside an empty log directory means failures stay invisible until a restore is
  needed: the job ran (snapshots prove it) but nothing would ever have announced it stopping. Say so
  when you see it — silent success and silent failure are the same signal.
- **Deletion is a different authority class from measurement.** Removing copies you have proven
  obsolete is routine; changing a retention policy, touching an encrypted backup store, or deleting
  anything whose owner is not you is not. Ask first, in binary form.
- **Never `rm -rf` a glob you have not listed.** Emit the explicit paths, read them, then delete those
  paths.

---
*DITEMPA BUKAN DIBERI ⚒️*
