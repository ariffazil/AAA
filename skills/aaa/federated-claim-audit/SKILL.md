---
name: federated-claim-audit
description: Verify another node's claims before accepting them.
owner: HERMES
risk_tier: low
floor_scope: [F1, F2, F4]
when_to_use: Another organ or node (IRFANclaw/KVM4, A-FORGE, arifOS) delivers an audit report, or you are asked to check a report you wrote yourself.
---

# Federated Claim Audit

Two failure modes, same error: **accepting the report whole** and **rejecting it whole**. Both respond to the report instead of measuring the thing. The job is to turn a narrative into a claim list, measure each claim on the node you actually control, and hand back buckets — not a verdict.

## Rule 0 — the node is part of the claim

Every count, path, hash, service, port, and test result is scoped to the machine that produced it. Before judging a number, establish: **which host, which filesystem, which process, which interpreter, which timestamp.** A count that does not exist on your node may be exactly true on theirs.

Separate physical hosts (KVM8 `af-forge`, KVM4 `srv1946043`) have separate `/root`. A cross-node mismatch is a scope difference until proven otherwise.

## Steps

1. **Extract claims, one per line.** Each claim carries: value, the command/definition used, the node, the time. No verdict yet. If the report gives a number without a definition, that is itself the finding.
2. **Sort by scope.** Is this a property of shared reality (a public URL, a sealed receipt) or of one node's reality (a file count, a local DB row count)?
3. **Write the definition before you run it.** Exact SQL / exact path / exact window / inclusion and exclusion rules. A number without a definition cannot be verified *or* refuted — only argued about.
4. **Probe on your own node.** Read-only. Capture the literal output.
5. **Triage into exactly one bucket** (table below). One claim, one bucket.
6. **Report claim-by-claim, buckets separated.** Put your own retractions in the same list as their errors — symmetric treatment is what makes the audit readable. A report that only ever finds the other side wrong reads as advocacy.
7. **Stop at the boundary.** Contradictions go to their owner (arifOS judgment, ARIF decision). Do not self-seal, do not declare all-green, do not repair a number to make a dashboard agree.

## Triage buckets

| Bucket | Meaning | Report language |
|---|---|---|
| VERIFIED | Reproduced on your node under the stated definition | "reproduced, value X" |
| NODE_SCOPE_ARTIFACT | True on theirs, not applicable here | "both true, different host" — **not** a contradiction |
| LIVE_STATE_DRIFT | Both readings were true at different moments (live DB, counters, running services) | "value moved between reads" |
| CONTRADICTION | Same scope, same definition, two values | preserve both; never average |
| UNREPRODUCIBLE | No definition you can reconstruct reaches the value | REPORTED, not false |
| UNKNOWN | Insufficient evidence either way | say UNKNOWN |

## Pitfalls

- **Hashing a live SQLite DB never reproduces.** Writes land between your reads, so two consecutive `sha256sum` calls differ on the same file. Either quiesce the writer first or label the hash REPORTED with its timestamp. An "immutable anchor" taken from a live file is a claim, not an anchor — retract it in the same breath you publish it.
- **A null search is not an absence.** A `find`/`grep` that returns nothing on your node proves only that your node lacks it. Declare absence only after checking the other node, the symlink target, and the archive path. "Not found here" is not "never existed".
- **Run the subsystem's tests with the interpreter that serves the live process, from inside the package directory.** Find it with `ss -ltnp` → PID → `readlink /proc/PID/exe`. The agent's own venv often lacks the server's dependencies, and flat-import test files (`from _helper import ...`) only resolve when cwd is the package dir. Wrong interpreter produces `ModuleNotFoundError` that reads as a broken suite.
- **A rule that says "retired" while still running is a self-contradiction — check the enforcing branch, not the comment.** Grep for the call site and read its actual return value. A no-op stub with the old name is correctly retired; a live clamp under a "retired" header is a lie the code tells about itself.
- **File mtime vs process start time decides whether a fix is live.** A patched module does nothing until the serving process restarts; a restarted MCP server does not restart the gateway. Compare `stat -c %y <file>` against `ps -o lstart= -p <pid>` and state which surface is patched and which is not.
- **Never ack a telemetry ack in a shared A2A room.** "noted · silent" is still a send, and it restarts the loop it claims to end. Silence is zero bytes. Reply only when there is a claim to verify, a decision needed, or work delivered — otherwise emit nothing.
- **Retract your own anchor first.** When a test you applied to their number also fails your number, publish the retraction before publishing their error. The audit's credibility is the symmetry, not the score.

## Reporting shape (to Arif)

```
Claim | my probe | bucket
...
Verified: N. Node-scope: N. Live-drift: N. Contradictions standing: N. Unknown: N.
What needs your decision: <only the items that are actually his>
```

Then stop. No summary paragraph restating the table, no menu of next steps.

## Reference

- `references/probe-recipes.md` — exact commands for live-DB hashing, scoped SQL counts, finding a port's interpreter, and running the hermes_mcp suites.
