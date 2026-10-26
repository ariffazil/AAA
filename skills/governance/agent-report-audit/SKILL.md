---
name: agent-report-audit
description: "Ground a peer agent's report before accepting it."
version: 1.0.0
owner: AAA
risk_tier: low
autonomy_tier: T0
floor_scope: [F1, F2, F3, F11]
metadata:
  short-description: Re-measure peer-agent claims claim-by-claim
---

# Agent Report Audit

Another agent (or a prior session of yourself) hands you a report: "fixed, live, receipts attached." Your job is to **re-measure**, not to accept or reject wholesale. Silence and acceptance are both outputs; pick deliberately.

## Procedure

1. **Split the report into discrete claims.** One line each: a file changed, a count, a process state, a behaviour.
2. **Re-run the cheap artifact for each claim.** Commit exists → `git cat-file -t <sha>` + `git show --stat`. Function added → grep the symbol in the resolved tree. Test count → run the suite yourself.
3. **Grade each claim** (table below), never the report as a whole.
4. **Add a separate section for delivered-but-unreported state** — degraded health, open defects, masked defaults.
5. **Close with one line of consequence**, not a recap.

## Grading Table

| Grade | Means | What you must show |
|---|---|---|
| **BETUL** | Artifact re-run and holds | The command you ran and its output |
| **SEPARUH** | Part holds, part doesn't | Which line is which |
| **TAK BOLEH VERIFY** | Historical state you cannot re-enter (pre-fix mechanism, past session, other host) | Say so plainly; dispute nothing |
| **SALAH** | Measured contradiction | Your measurement beats their claim, with the difference named |

A claim you cannot test is not a lie and not a pass. Do not soften it into agreement, and do not attack it to look rigorous.

## Rules

### Never add a number you did not measure
A counter-claim without a probe reproduces the defect being audited. If their count looks wrong, run the query and publish the SQL, window, timezone, filters, and dedup rule alongside your number — otherwise you have manufactured a second unreproducible figure.

### Establish host / scope before calling anything a contradiction
A field measured on node A and the same field on node B are two measurements, not a lie. Classify mismatch as `DEPLOYMENT_DRIFT` with both node labels. Confirm `hostname`, path existence, and symlink status on the node you are actually standing on before writing "doesn't exist".

### A live data store has no stable hash
Hashing a DB or log a running writer owns gives a different digest minutes later. Either quiesce the writer and hash a snapshot, or label the number **REPORTED** with a capture timestamp — never "immutable anchor". Withdraw the label if you already used it; correcting yourself is cheaper than being corrected.

### Prove "live" with three artifacts, never with "service restarted"
```bash
stat -c '%y %n' <changed_file>          # file write time
ps -p <pid> -o lstart=,cmd=             # process start time
readlink -f /proc/<pid>/exe             # interpreter
<interp> -c "import <mod>; print(<mod>.__file__)"   # tree it really imports
sha256sum <repo_copy> <resolved_copy>
```
Rule: **process start later than file mtime ⇒ the fix is running.** Earlier ⇒ it is not, whatever git log or the prose says. Repo tree ≠ installed copy ≠ running interpreter; resolve from the live process, not from `cwd`.

### Restarted ≠ healthy
Always read the health surface after a restart and report `status`, floor pass state, and each `degraded` / `unknown` layer. A restart line with no health line paints degraded green. Scope any score quoted: a flow-level or component-level figure is not system health.

### Advertised ≠ supported
If the schema advertises an option and every explicit use of it errors, that is the same class as a retired rule that still runs. Probe one advertised option per axis with a real call.

### Bypass ≠ kill
A fix that routes around a masking default (e.g. `setdefault(field, [])` presenting "nothing measured" as "nothing missing") leaves the class alive on other paths. Write **"bypassed on this path, class still open"** and name the remaining call sites.

### Mixed-message commits are corroboration, not motive
A commit whose message names one file but whose diff spans many is evidence of a concurrent index sweep. Record provenance; do not infer intent from the mismatch, and do not rewrite pushed history to fix the label.

### Name the one thing they left out
Reports omit the item that makes them look worst. Find it, state it in one line, and stop there — no lecture.

## Multi-Agent Room Cadence

A report or telemetry line is **not** a request unless it asks something or needs a decision.

- Telemetry acks, "Working", status pings, file-change notices → **no reply**. Not even "noted · silent": that is still a send, it re-triggers the peer, and the pair of you produce an infinite ack loop that costs the human every turn.
- True silence is the absence of a message, not a message announcing silence.
- Reply only when: a decision is needed from a human, a measured contradiction must be surfaced, or your own claim is being graded and the grade changes an action.
- If a peer keeps posting acks, stop responding entirely. One extra reply resets the loop.
- Do not narrate your decision to stay silent. The narration is the noise.

## Output Shape

Verified items first with the command that produced them, then the grade table, then unreported state, then one line of consequence. No praise, no ceremony, no restating their report back at them.

## Pitfalls

- **Do not probe only where their report points.** The defect they missed is usually on the path they did not name — check the call site, not only the changed function.
- **Do not accept "tests pass" without the count and the runner.** A suite that silently collected zero tests also exits clean.
- **Do not treat another host's absence as fabrication**; and do not treat your own absence of evidence as proof of absence.
- **Self-correction beats defence.** When your own earlier receipt fails the same standard you are applying, withdraw the label in the same turn and say what replaced it.
