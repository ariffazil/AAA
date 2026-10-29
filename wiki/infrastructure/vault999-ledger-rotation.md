---
title: VAULT999 Ledger Rotation Policy — 2026-10-15
created: 2026-10-28
updated: 2026-10-28
type: infrastructure
tags: [infrastructure, vault999, rotation, ledger, policy]
sources: [raw/97f30e4c-receipt-log-rotation-archive-retain-2026-10-15.md]
confidence: high
contested: false
omc_run: omc-20261028-s980
---
On 2026-10-15, the VAULT999 ledger rotation policy was activated with the script `/root/scripts/rotate-ledgers.sh`, configured to run weekly on Monday at 05:17. The retention policy keeps 14 generations of ledger data. The decision was made by Arif, selecting Option A (archive-and-retain), and the action was verified with caveats. The rotation freed 491MB of space, compressed 55MB, and kept 9 generations of data. The disk usage decreased from 83% to 82%.

Key caveats include:
- `copytruncate` has a sub-second loss window for actively-appended files, accepted as a standard tradeoff.
- A test run unintentionally rotated production targets, but the outcome matched the authorized action.
- The `entropy-metabolizer` reclaimed only 1.2MB, confirming it is not the right tool for this task.
- The `/root/VAULT999` directory is a symlink to `/root/arifOS/VAULT999`, not a duplicate.
- The `/root/backups/restic-repo` (18G) is active and must not be pruned.
- The `/root/forge_work` (29G) is 0-8 days old and would only free 77MB if pruned by age.
