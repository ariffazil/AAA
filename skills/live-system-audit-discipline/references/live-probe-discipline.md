# Probing and patching a live, multi-writer system

Depth for audit work where the system keeps moving while you investigate.

## The served artifact is not the working checkout

A service runs what was built and installed, not what sits in the dev checkout. Before
concluding anything about deployed behaviour, resolve the path the process actually loads — the
unit's `ExecStart`, that interpreter, the installed root's site-packages — and compare it against
the repo tree. A patch applied to the checkout can be a silent no-op, and the checkout may be many
commits ahead of or behind the running build.

Cheapest confirmation that the running process executes the code you just read: find a log string
or literal that exists only in the new version, and confirm the process emitted it. Do this before
believing a fix is live.

`changed on disk` is not `serving`. Report the former; a reload is a separate, often gated, step.

## Same name, two stores

One logical name (vault, registry, ledger) can resolve to different physical locations on the same
host. Before designing a cleanup or migration, enumerate the candidate paths and determine which
one the consumer reads. Cleaning the path nobody reads fixes nothing while looking like progress.

## Working while others write

Assume other agents share the repo and are committing.

- Re-check the file's mtime/hash immediately before patching. If it moved, re-read before you
  edit, and redo any analysis built on the old content.
- Prefer additive edits — append a labelled correction and keep the other writer's text — over
  overwriting their section. It preserves attribution and avoids silent data loss.
- Do not plan a write against a moving target; either confirm the file is quiet or coordinate.

## Independent verification

Self-verification does not count. A fix is confirmed when a different client, seat, or method
re-probes the same input — not when the author re-runs their own probe. Where a second seat is
unavailable, say so and mark the claim author-verified.

A pre-committed prediction with declared outcomes, tested by a different seat, is the clean way to
promote a heuristic toward a predictor. One confirmed prediction is n=1, not an oracle.

## A blocked mutation is a result

A gate that refuses a write is an outcome to report, not an obstacle to route around. State the
exact blocked operation and the gate that refused it. Never hand the human a shell command to
apply on your behalf, and never describe a gated change as staged or done.

## Check the identifier before you mint it

Before introducing a symbol, prefix, or class number in a report or doctrine, check the live
symbol registry for reserved prefixes and run the namespace probe. A borrowed identifier that
collides with an existing ratified one is a high-severity defect, and it propagates: every
artifact that quotes you inherits it. Cite the source doctrine by name when you cannot verify its
number.

## When correcting another writer

Hold your own correction to the standard you are applying. Verify the specific claim before
asserting it is wrong, and check your own scoping — a correction that generalises from one probe
repeats the error it is correcting, one layer up.

## Reporting a fix you have not observed working

If a change is authored but not yet serving, say exactly that: authored, syntax-checked, on disk,
not live. Do not let "applied" or "done" describe a state the system has not reached.
