# Seal, Delivery and Causal-Path Verification Recipes

Concrete probes for the three proofs in the parent skill. Read-only throughout — these verify,
they do not mutate.

## 1. Causal path: is this artifact actually reachable?

An artifact can be correct on disk and have zero runtime effect. Prove the caller exists across
**every** dispatch surface before auditing or repairing content.

```bash
ART=<absolute/path/to/artifact.py>

# every scheduler surface — a single-surface grep manufactures false dormancy
python3 -c "import json;d=json.load(open('<cron-store>.json'));print([j['name'] for j in d['jobs'] if '<artifact>' in json.dumps(j)])"
grep -rl "<artifact>" /etc/cron.d/ /etc/systemd/system/ 2>/dev/null
crontab -l 2>/dev/null | grep "<artifact>"
grep -rln "<artifact>" --include=*.sh --include=*.service --include=*.py <repo-roots>
```

Interpreting the result:
- **hits** → the artifact is in the causal path; content fixes matter.
- **zero across all surfaces** → DORMANT. A repair here is `CODE_EXISTS / EFFECT=NONE`.
  Label the file header so the next agent does not wire in a second implementation.

**Also check the *reverse*:** when two implementations of the same job exist, ask which one the
scheduler actually invokes. Auditing the wrong twin produces a correct report about a dead file.

## 2. Seal verification: does the seal still resolve?

A seal carries an attested hash per file. Verify by re-hashing, then check **ordering** — a later
writer silently invalidates an otherwise-honest seal.

```python
import json, hashlib, os

def sha(p):
    try:
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    except OSError:
        return "MISSING"

d = json.load(open("<seal>.json"))
for c in d.get("changes") or d.get("files") or []:
    attested = c.get("sha256_after") or c.get("sha256")
    actual = sha(c["file"])
    print("MATCH" if attested == actual else "MISMATCH", os.path.basename(c["file"]))
    print("   attested:", attested)
    print("   on disk :", actual)
```

Reading the result correctly:
- **All match** → the seal resolves. Credible.
- **Some mismatch** → check whether `sha256_before` matches a pre-change backup. If it does, the
  seal was **correct when written** and went stale afterwards. That is a *staleness* finding, not
  a forgery — reconcile with a `supersedes` record; never rewrite sealed history.
- **A seal with no `changes[]`/hash block** is a narrative seal: it attests intent, not bytes.
  Do not cite it as byte-level proof.

Confirm the ordering that proves staleness:

```bash
ls -la --time-style=+%H:%M:%S <sealed_file> <seal>.json
# sealed_file mtime LATER than seal mtime → a second writer broke the binding
```

## 3. Delivery: did it actually arrive, and to whom?

A job's configured target proves **configuration**, not delivery. Three distinct stages:

```
CONFIGURED (the deliver field)  !=  DELIVERED (a ledger SENT row)  !=  INTENDED (the audience you meant)
```

```bash
# the ledger is authoritative — it records both outcomes
python3 -c "
import json
for l in open('<delivery-log>.jsonl'):
    r=json.loads(l)
    print(r.get('attempted_at_utc'), r.get('chat_id'), r.get('status'), r.get('telegram_message_id'))
"
```

A delivery helper that records **both** `SENT` (with id) and `FAILED` (with error class) is the
reference pattern — it can reject, and it has history. A helper that only logs success is a
one-way recorder; you cannot tell a quiet failure from a non-event.

### Timezone trap when filtering a ledger by date

Logs are commonly stamped **UTC** while the reader thinks in local time. A filter on a local date
silently drops everything after local midnight:

```
local 06:45  ==  prior-day 22:45 UTC
```

So `startswith("2026-09-18")` on a UTC field reports **zero deliveries today** for a job that ran
fine this morning. Convert before filtering, or name the timezone in the claim:

```python
from datetime import datetime, timezone, timedelta
myt = datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(
    tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
```

**Rule: a date-scoped filter is a claim about the filter.**

### Resolving which group/DM an id refers to

A numeric id is not a meaning. Resolve it from the session/message store before reasoning about it:

```bash
sqlite3 -readonly <state.db> \
  "select chat_id, display_name, chat_type, count(*) from sessions where chat_id in ('<id1>','<id2>') group by 1,2,3;"
```

Group ids are negative and share the same numeric space as user ids. A correct document can also
be read in the **wrong section** — confirm which job a config line belongs to before quoting it as
that job's target.

## 4. Boundary checks that must be able to REJECT

For each boundary in a pipeline spine, write one check that returns one of:

```
PASS     boundary holds on the artifact as it exists now
FAIL     boundary violated, offending evidence named
UNBUILT  nothing exists yet to check — honest, and NOT a pass
```

`UNBUILT` must be a distinct state from `PASS`. Reporting a boundary as passing because no artifact
violated it — when no artifact ever reached it — is the false assurance this whole family is about.

Finish with a **self-test**: run each check against a deliberately bad input and confirm it can
`REJECT`. A checker that cannot fail is itself a false control.

## 5. Two-writer collision

When a seal, receipt, or audit describes a file that another agent may also edit, hash-binding
cannot hold. Detect it, then decide ownership — never silently re-seal.

Signals:
- a tool warning that the file was modified by another session/agent
- `mtime` later than the seal that attests it
- two artifacts sealed under the **same** instruction, describing the **same** file differently

Rule: **no file may have two writers.** One recorded owner, or the attestation is not verifiable.
Adding a second writer to repair a two-writer problem repeats the defect.
