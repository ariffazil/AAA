---
name: receipt-grounding
id: receipt-grounding
version: 1.0.0
risk_tier: low
description: "Use when verifying pasted receipts and claims."
owner: HERMES
floor_scope: [F1, F2, F4, F7, F11]
autonomy_tier: T0
capability_tier: fed-reasoning-heavy
ecology_state: WARM
when_to_use: Human relays an agent report or verdict; human supplies hashes / paths / counts as proof; you are about to say done, written, pushed, fixed, or shipped.
---

# Receipt Grounding

A claim is not evidence. A receipt is evidence only when an independent observer,
standing on the host that owns the object, can reproduce it from what you gave them.

Use when a human pastes receipts, commit hashes, metric numbers, or another agent's
report and each claim has to be accepted, rejected or qualified before it moves work.

## Procedure

1. **Split the relay into atomic claims.** One row each: commit exists / commit is on
   origin / file exists / file is on THIS host / N rows in store / metric equals X /
   config line changed / organ responds / who writes this file.
2. **Pick the cheapest ground-truth probe** for each row (table below). Read-only first.
3. **Report the table before any verdict.** Every row gets BETUL / SALAH / SEPARUH /
   UNVERIFIED plus the probe output that decides it. No summary sentence that outruns
   the table.
4. **Only then** say what it means, what is still open, and what you would do next.

Never restate the human's own numbers as your finding. Report only what you confirmed,
what you disproved, and what you could not reach.

## Probe table

| Claim | Probe |
|---|---|
| commit exists | `git cat-file -t <sha>` inside the repo |
| "pushed" | `git fetch --quiet origin && git ls-remote origin \| grep <FULL sha>` |
| branch is on origin | `git ls-remote origin \| grep <branch>` |
| file exists and looks like what was described | `stat -c '%n size=%s mtime=%y inode=%i mode=%a' <path>` |
| file content identity | `sha256sum <path>` — full 64 hex, always |
| N rows / N items | `wc -l` on the canonical store; parse JSON in python, never eyeball |
| who writes a file | grep crontab **and** `/etc/cron.d` **and** `systemctl list-timers` **and** the agent cron store |
| service is live | `curl` the port and read the body; a registry row is not an invocation |
| metric value | recompute from the canonical store; if two stores exist, name both and say which is SOT |
| which host owns a path | `hostname -f` on the machine you are probing, stated in the report |

## Pitfalls

- **A truncated hash is not a receipt.** Nobody can verify `975386a6…`. Give full sha256
  plus mtime, inode and hostname — or paste the file content.
- **Name the node.** A file written on one host is invisible to a reader probing another.
  "You can check it yourself" without naming the host is a promise you cannot keep, and
  it reads as fabrication when the probe comes back empty.
- **"Pushed" is not "committed", and a branch tip is not a commit.** A clean feature
  branch can be on origin while the integration commit sits local. Report both lines
  separately every time: local SHA(s), origin refs, and what is absent from origin.
- **Fetch before comparing.** Stale remote-tracking refs lie about ahead/behind; a
  comparison without a fresh fetch is a claim about a map, not the territory.
- **One writer is not one truth.** After collapsing duplicate writers, sweep for stale
  readers and mirrors that still hold the old value — check mtimes across `state/`,
  `static/`, `public/`, `/var/www`. A silent stale copy is the same defect as a
  double-writer, one step later.
- **Aggregate green can hide a nested unknown.** Read the nested detail before calling a
  system healthy; a reachable endpoint is not domain readiness.
- **A label and a threshold can contradict.** If a score is labelled healthy while the
  system's own gate says hold, report the contradiction — do not average it into a
  comfortable sentence.
- **Different record types are not a conversion rate.** Counts of observations versus
  counts of decisions do not form a ratio unless the store says they do.
- **On an uncertain write outcome, verify before retrying.** When a transport reports
  that a call may or may not have landed, re-read state with a read-only call first;
  blind retry duplicates the side effect.
- **Absence of a hit is not absence of the thing.** A narrow grep that finds nothing is
  UNVERIFIED, not "does not exist" — widen to all schedulers, both path roots, and the
  hidden variants before concluding.

## Reporting shape

- Table first, one row per claim, with the deciding probe quoted short.
- Then the open items, ranked, with the one that actually blocks a decision first.
- Then at most one sentence of meaning.
- Plain BM Penang, short, no preamble, no congratulation, no restating the relay's prose.
- If the human's conclusion is right but one number is wrong, say both: the conclusion
  stands, the number must be corrected. Do not collapse the two.

## Lane scope

In group/A2A lanes, delegation and execution tools may be blocked by lane authority.
When that happens do the grounding inline with read-only probes and say so once — never
promise a subagent you cannot spawn, and never quietly downgrade the audit.
