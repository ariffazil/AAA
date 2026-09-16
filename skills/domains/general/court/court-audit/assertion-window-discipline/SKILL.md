---
name: assertion-window-discipline
description: "Use when about to assert absence or unknowability."
owner: Hermes
---
# Assertion Window Discipline

The most common agent error is not ignorance — it is **premature closure**: looking
at one window, then generalizing to the world.

## The rule

**The window you searched is not the world. Widen before asserting.**

This applies to every negative or universal claim:
- "X is down" / "X doesn't exist" / "no evidence of X"
- "I cannot determine who/what/why"
- "nothing else is configured" / "all clear"
- any figure presented as a total ("~20G reclaimable")

## Why it bites

A narrow probe returns a true result about a narrow scope. The error is the
**quantifier swap** — reporting it as global. The probe was honest; the
generalization was not.

Observed failure shapes:
- Probed one port set → "scanner is a false positive" (scanner was right)
- Summed visible dirs → "20-25G reclaimable" (real: 3.1G; model weights counted as cache)
- Read one config schema → "nested keys are ignored" (3 of 4 were; one was read)
- Saw no writer in own session log → "cannot determine who applied the fix" (sibling session did it)
- Checked service is-active → "the organ is healthy" (body was degraded)
- Read a module's config block → "the module is absent" (it was bundled, just disabled)
- Saw CLI warn about missing env vars → "10 API keys missing" (gateway service had all of them)
- Grepped a wrong directory with `2>/dev/null` → "the constant does not exist" (it was at a different path, line 251; the `no such file` error was suppressed)

## Secrets and agent-readable state (hard rule)

**Secrets must not enter agent-readable state. The safe pattern withholds; the
unsafe pattern stores.**

Correct example: `restic` keeps `RESTIC_CREDS` out of agent reach — the agent can
run the backup but cannot read the key. When a credential is withheld and you
cannot open the repo, that is **correct design working**, not a defect.

Unsafe example: a peer token placed in `openclaw.json` propagates into every
store that reads config — the agent's own conversation DB, `.last-good`
backups, WAL files. Observed: **1 write → 50 stored copies.**

### Probing a secret propagates it

Detection is itself a vector. Each time an agent reads a config containing a
secret, the tool output is persisted into that agent's memory. N inspections
produce N copies. So:

- Never print raw config that may contain credentials. Pipe through a masker
  (`/root/scripts/mask_secrets.py`) by **default**, not when you remember to.
- Count occurrences with the **prefix only** (8 chars) — enough to locate,
  not enough to reconstruct.
- When auditing exposure, do not re-read the secret to "check" it. Check
  metadata: file mode, size, mtime, presence.
- If a secret is already in agent state, **rotate**. Never scrub — the copies
  are in append-only stores (WAL, journals, backups) and scrubbing gives false
  assurance while leaving the value valid elsewhere.

## Independence test before citing corroboration

Two readings of the **same artifact** are one source seen twice. They are not witness.

Ask, before citing agreement as evidence:
1. **Same context?** Same CLI, same host, same env, same run → one source. A warning
   from `tool X` read by you and by a peer is one warning, not convergence.
2. **Same input?** A memory file one agent wrote from another agent's published
   analysis is *derived*, not independent. Check provenance: did the second reader
   observe reality, or read the first reader's conclusion?
3. **Independently measured?** A correction reached by *pattern* ("the other CLI
   warning was false, so this one probably is") is not a measurement. Probe it, even
   when the answer is almost certainly right — the discipline only counts when it
   applies to conclusions you already believe.

Independence requires different **evidence paths** to the same fact: separate probes,
separate hosts, separate data sources. Otherwise label it "same source, re-read" and
do not raise confidence.

## Retraction must replace, not hedge

After a claim is disproved, the next message must carry the **new** state. Hedging
("confidence downgraded", "likely also false") while the old claim stays in the room
record leaves readers with the pre-correction belief. Void means remove, not soften.

## Environment-context trap (very common)

A tool run in the **wrong process context** emits warnings that look like findings.
`openclaw plugins list` over SSH has no systemd env → warns "missing env var X" for
every provider key. The gateway service loads them from an `EnvironmentFile` drop-in.

Compare the **service's** env, never the CLI's:
```bash
tr '\0' '\n' < /proc/$(pgrep -f '<service>')/environ | grep '^KEY='
systemctl cat <unit> | grep -i EnvironmentFile
```
Same for any "not configured" warning from a one-off command. Ask: *which process
context produced this message, and is that the context that matters?*

### Pre-assertion gate (run before ANY claim)

Run this **before** publishing a finding, not after being challenged:

1. **PROCESS** — which PID produced this? Is it the service, or a shell?
   `ps -o pid,ppid,cmd -p <pid>`; trace parents to init.
2. **WINDOW** — did I sample once, or over time? Transient states (startup,
   restart drain, GC pause) look identical to outages in a single probe.
   Re-probe after 15-30s before calling anything down. Prefer 2 samples ≤30s apart.

   **When state is unstable, stop asking "what is the state?" and ask "what
   transition produced it, and is that transition still in progress?"**
   A gateway mid-reload and a gateway mid-crash read the same from one probe.
   Logs usually contain the transition — read for it explicitly before
   interpreting the state. A service "restarting on its own" is often a
   config-change reload working as designed; check the trigger, not the symptom.
   Corollary: never run a one-shot probe against a surface someone may be
   editing right now — check for concurrent mutation first (see SCOPE).
3. **LOG** — is the log I read actually RECEIVING entries?
   `tail -1 <log>` and compare its timestamp to now. A stale log is not evidence:
   auth.log stopped recording sshd on Aug 26 while journald kept going.
4. **SCOPE** — node? session? which of N concurrent writers?
   `sqlite3 state.db "SELECT session_id,COUNT(*) FROM messages
    WHERE timestamp > strftime('%s','now')-600 GROUP BY session_id;"`
Extra: **VERIFY THE ARTIFACT EXISTS** — before a line-level fix, confirm the target file/function/field is on the box you're editing (`test -f`, `grep -c`) and not a homonym on another machine. Most wrong-layer errors are layer errors, not reasoning errors.

### Absence of output is not absence of object

A search that returns nothing has THREE possible causes, and only one of them is a finding:

1. **The object is absent** — the finding you think you have.
2. **The path is wrong** — you searched a plausible-but-wrong directory.
3. **The pattern is wrong** — escaping, glob, case, or a renamed identifier.

Causes 2 and 3 both *look identical* to cause 1. And the standard idiom makes them
indistinguishable:

```bash
grep -rn "7\.85" some/guessed/path/ 2>/dev/null   # → prints nothing, exits 2
grep -rn "7\.85" wrong/path/         2>/dev/null   # → prints nothing, exits 2  (no such file!)
```

**`2>/dev/null` converts a wrong path into a confident negative.** The error message that would
have exposed the mistake is the first thing suppressed. The operator then reports "the constant
does not exist" — a fabricated absence built entirely from a typo.

**If the exit status is not 2, it is not a negative.** So before publishing any "X not found":

```bash
test -e "$SEARCH_ROOT" || echo "SEARCH ROOT ABSENT — this is not a finding"
grep -rn --include='*.py' '<pattern>' "$SEARCH_ROOT"   # keep stderr VISIBLE
```

- Never silence stderr on a search that will support an absence claim. Silence the noise on
  *lookups*, never on the command whose empty output you intend to cite.
- Resolve the **root** first (`ls -d`, `test -e`), then search inside it. Report the root you
  searched as part of the claim — an absence claim with no stated root is unfalsifiable.
- Prefer a search that **proves the object exists somewhere** before one that proves it is
  missing: `grep -rl` across the whole repo, then narrow. A repo-wide hit with a single
  occurrence is a far stronger statement than a directory-scoped zero.
- Corollary on the federated case: a peer's empty grep and your hit are **both true** for their
  respective roots. Lock the path (`node + path + commit`) before disputing either.

Only after all four: assert, and **carry the scope qualifier in the claim**.

## Procedure before any negative/universal claim

1. **Name the scope you actually probed.** Write it down.
2. **Ask: what is outside this scope that could change the answer?**
   - Other nodes / other sessions / other time windows
   - Concurrency: is anyone else writing right now?
   - Layers: unit state vs health body; file exists vs code path reads it
3. **Widen once, in the direction most likely to falsify you.**
4. Only then assert — and **carry the scope qualifier in the claim.**

## Concurrency check (cheap, do it early)

Before diagnosing or declaring "no one did X":
```bash
# every session, not just yours
sqlite3 /root/.hermes/state.db \
 "SELECT datetime(timestamp,'unixepoch','+8 hours'), session_id, substr(content,1,120)
  FROM messages WHERE timestamp > strftime('%s','now') - 3600 ORDER BY timestamp;"
ps -eo pid,lstart,cmd | grep -E 'hermes|agent' | grep -v grep
```
A sibling agent session can **invalidate your diagnosis mid-flight**. Check for
concurrent writers before publishing a causal claim.

## Node qualifier (federation-specific)

Partial observation → global verdict is worse across machines. Every factual claim
about a service/port/file carries `scope: node` + `host_id`, or it is not a claim
but a rumor. "Wan-shim is gone" was true on one node, false on another.

## The counter-measure that works

Every correction in the session that produced this skill came from **widening the
search after pushback**, not from more confidence. Friction is the input; treat
resistance as a signal to re-probe wider, never as something to argue down.

---
*Distilled 2026-09-14 from five same-shape errors in one session on KVM8.*
*DITEMPA BUKAN DIBERI*
