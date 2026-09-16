# Loop maturity audit — is the learning loop actually learning?

Use when someone (or another agent) claims a self-improvement loop is live, sealed, or working.
The claim is almost always about *plumbing* (code exists, cron installed, receipts written), never
about *behaviour change*. These four measurements separate the two.

## 1. Inhale vs exhale

A ledger row count is not progress. Enumerate event types and check the applied column.

```python
import json, collections
ev, applied, real_diagnoses = collections.Counter(), 0, 0
for line in open(LEDGER):
    d = json.loads(line)
    ev[d.get('event', '?')] += 1
    if d.get('improvements') or d.get('improvements_proposed'):
        applied += 1
    if d.get('bottleneck') or d.get('fix'):
        real_diagnoses += 1
print('rows', sum(ev.values()), '| improvement>0:', applied, '| real diagnoses:', real_diagnoses)
print(ev.most_common(10))
```

Read it as: a ledger dominated by one per-turn heartbeat event, with a near-zero improvement count,
is a **pulse, not learning**. Report rows, applied, and diagnoses separately — a maturity claim built
on proposal count alone is theatre, because proposals are the cheap number.

- A run that proposes and applies nothing is a **FAILED run** and must be logged as such.
- "Awaiting approval" is *deferred*, not blocked: it needs a status field, an owner, and a dedupe
  key, or it accumulates silently while looking busy.
- **Recurrence increments, never appends.** If the same finding is re-derived every cycle, the
  producer must upsert on a semantic key (increment `recurrence`, bump `last_seen`) instead of
  writing a new row. See `references/live-tree-audit.md` §5 for the dedupe query.

## 2. Consequence, not activity

For each applied fix, capture a **baseline** for its own failing pattern in the window before, then
re-measure the same pattern after the window. A fix that does not move the recurrence of its own
pattern produced no consequence, however good the receipt looks.

Scoring shape: `PERSISTED` if recurrence fell materially · `PENDING` while the window is open ·
`NO_CONSEQUENCE` if unchanged. Always state the baseline's age — a baseline of zero occurrences
taken moments ago cannot be scored yet, and reporting it as success is the classic error.

An `h(t)`-style impulse response (how long one event stays causally active) is only characterizable
once half-life is non-null across event types. If the measurement tool returns
`h_characterized: false` with null half-lives, the instrument exists and the signal does not — say
that, rather than quoting the tool's existence as evidence.

## 3. Survival, not promotion

A capability graph whose nodes are all `PROVISIONAL` with `fitness: null` and `survivals: 0` is a
skeleton. Promotion events count; survival events decide. "Capability survives implementation
changes" is untested until something has actually survived one. Report both numbers.

## 4. Seal state — running is not sealed

Check, in this order:

```bash
systemctl is-active <unit> || ls -la /etc/cron.d/<job>   # does it run at all
tail -20 /var/log/.../<job>.log                          # did it ever fire
stat -c '%y %n' <the artefact it writes>                  # did the write actually land
git -C <repo> status --porcelain -- <loop-dir>            # is it committed
git -C <repo> log -1 --format='%h %s' -- <loop-dir>       # is there a commit of record
```

**A loop that runs but is untracked (`?? dir/`) is not sealed** — there is no commit of record, so
nothing can be referenced, diffed, or rolled back. Say "running and bounded, not sealed" rather than
letting "it works" stand in for seal.

Also check the boundary while you are there: run the loop's own boundary self-test and read what it
blocks. A loop that cannot write its own config, its verifier, or the constitution is bounded; one
whose forbidden-path list is configurable can relax its own limits.

## 5. Does the verifier verify?

A loop with a promotion gate still promotes nothing real if the gate cannot fail. Before crediting
the gate, enumerate its verdict classes and bucket each by whether it is *capable* of returning
False. The dispatch table is usually a `PATTERN -> callable` dict — parse it rather than reading it:

```python
import re
blk  = src[src.index('REDERIVE = {'):src.index('def _rederive_')]
rows = re.findall(r'"([A-Z_]+)":\s*lambda a:\s*([^,\n]+)', blk)
hard  = [k for k, v in rows if v.strip().startswith('(True')]   # cannot fail at all
proxy = [k for k, v in rows if '_probe' in v or '_frame' in v]  # checks something else is alive
weak  = [k for k, v in rows if 'paths' in v]                     # tolerates missing tokens
```

Three failure shapes, ordered by how well they hide:

- **Hardcoded pass** — `lambda a: (True, "...")`. Not verification; the class can never withhold.
  Report it as SELF_EVAL, never as "verified".
- **Proxy check** — the class is "confirmed" by probing a *different* subsystem's liveness (an
  observer endpoint, a kernel port). That proves the observer is breathing, not that the claim is
  true: a monitoring outage and a healthy claim then score identically.
- **Lenient re-derivation** — the check scans quoted evidence, counts path tokens that resolve, and
  returns True with the misses *tolerated inside the mechanism string* ("N missing, tolerated:
  evidence quotes history"). A claim about a dead path thereby passes its own falsifier. Fix the
  tolerance, not the finding.

State which classes cannot fail, and note that the promotion count is bounded by them.

**Then do not patch the gate yourself.** Widening or narrowing what passes changes which claims
enter the graph — that is an authority change, not a bugfix. Audit it, publish the classification,
and hand the verdict to the organ that owns the gate.

## 6. Reporting

```
VERDICT MAP   A=... B=... C=... D=...   (state each layer's status, incl. HOLD)
SEAL-READY    <what is genuinely verifiable now, with the command that proved it>
PARTIAL       <what exists but is unmeasured>
NOT SEEN      <what you could not verify — never upgrade this to SEAL, never omit it>
```

The `NOT SEEN` section is mandatory. An audit that lists only what it found reads as completeness it
did not earn.
