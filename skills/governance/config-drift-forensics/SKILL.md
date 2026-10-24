---
name: config-drift-forensics
description: "Use when a watchdog reports production config drift."
owner: Hermes
capability_tier: fed-agent-subagent
ecology_state: NEW
owned_by: Hermes
authority_of: AAA
---

# Config Drift Forensics (read-only)

A drift alert means a watched file changed. It does not mean anything is wrong. The work is to
resolve THREE questions in order, without mutating anything: **what changed, when, and who** —
and only the human ratifies "intended". Re-baselining before attribution is how an unauthorized
change gets legitimized.

## Always-on rules

- **Never re-baseline before the human confirms.** Update baseline only after an owner explicitly
  claims the change ("sah"), with a receipt. Silent = treat as unattributed, freeze evidence.
- **Don't re-run the alert cron to "check it again"** — it will fire identically and normalizes
  the alarm into background noise.
- **Read-only throughout**: hashes, diffs, dumps, log reads. No writes to the drifted file, the
  baseline, or the scanner.
- A drift report is a peer's claim: its counts, IDs and hashes are inputs to verify, not findings
  to repeat.

## Procedure

1. **Hash the live file and find the baseline.** `sha256sum` the drifted file. Locate the
   baseline the scanner compares against (read the scanner script — do not assume); record its
   **establishment time** (mtime of the baseline file).
2. **Recover the pre-change object from a backup store, not from convenience.** Restic, git,
   or labeled `.bak` copies. If the store has snapshots, `restic dump <snapshot> <path>` the one
   nearest BEFORE the mutation window, hash it, and confirm it equals the baseline. Diff only
   baseline→live — diffing against an older labeled backup folds days of prior work into one
   diff and mislabels old changes as today's drift.
3. **Resolve every ID the alert cites.** Snapshot IDs, commit SHAs, event ids: verify in the
   named store (`restic snapshots`, `git cat-file -t`). A real change behind a nonexistent ID is
   still a mislabeled finding — report the change AND the dead label.
4. **Build the timeline.** File mtime; `ctime == mtime` plus matching dir mtime ⇒ atomic replace;
   service reload timestamp from journalctl right after (sub-second ⇒ scripted pipeline, minutes
   ⇒ human-driven). Check sibling files written in the same burst (3ms–seconds) — one write
   usually ships with its consumer (e.g. content file + its route allowlist).
5. **Attribute — honestly.** Sweep: auth log for logins in the window, shell history, deploy
   logs, session/agent ledgers, cron runs. If nothing names an actor, the verdict is
   **UNATTRIBUTED** — report the void with the lanes searched. Never fill it with the most
   plausible candidate: a bystander login minutes earlier is correlation, not authorship.
6. **Check the house convention as its own finding.** Directories full of labeled `.bak-<date>-<label>`
   backups make a single edit WITHOUT a backup stand out. Record the convention break even when
   the content proves benign — it is the process signal (whoever edited skipped the safety step
   and did not sign their work).
7. **Verify claimed downstream effects live** (the 404 now a 200, the port now listening) —
   confirms the change is functional, and confirms the reporter actually measured.
8. **Reconcile with a second seat** (if the estate is multi-host) by exchanging reproducible
   receipts — exact commands + hashes the other seat can re-run, not narrative conclusions.
9. **Escalate with a one-line binary for the human**: who/what/when/one-line-diff + "sah?" —
   answerable in ten seconds. Freeze until answered.

## Report shape

- `hash pair (baseline → live) + diff` first; then timeline; then attribution status; then the
  convention-break note; then the single question for the human.
- Correct your own earlier scope errors in the same thread, naming the misread (e.g. "my 3-change
  diff was against the wrong era; true delta vs baseline is one line").

## Pitfalls

- **Alphabetical `head` truncation when listing backup dirs** hides the newest labeled backups
  (entries sort by name, not date) — use `ls -lt` and grep the exact filename family before
  claiming "no backup exists".
- **`0 matches` for the baseline hash anywhere on disk is normal** when it lives only inside a
  backup store — recover via `dump`, don't conclude the baseline was never real.
- **A benign diff is not a closed case.** One aligned line from an unnamed author is still an
  unattributed mutation of production; content review does not substitute for attribution.
- **Alert window ≠ mutation window.** The cron fired hours after the change; anchor every
  timeline claim to the file's mtime, not the alert time.

*Kin: `probe-vantage-discipline`, `divergent-claim-reconciliation` (vantage axes, unattributed-void
protocol). When those skills are editable in a foreground session, absorb this content there.*
