# Autonomous Loop Runtime — concrete recipe

> Depth for `autonomous-loop-engineering`. Load when writing or hardening the
> runtime of an unattended loop.

---

## 1. Lock implementation

```python
import atexit, fcntl, os

LOCK_PATH = "<state-dir>/.loop.lock"
_held = None
_depth = 0

class AlreadyRunning(RuntimeError):
    """A second cycle is in flight. Exit non-zero so triage sees it."""

class LoopLock:
    def __init__(self, blocking=False, path=LOCK_PATH):
        self.path, self.blocking, self.fd = path, blocking, None

    def __enter__(self):
        global _held, _depth
        if _held is not None:        # reentrant within this process
            _depth += 1
            self.fd = _held
            return self
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        fd = open(self.path, "a+")
        flags = fcntl.LOCK_EX if self.blocking else fcntl.LOCK_EX | fcntl.LOCK_NB
        try:
            fcntl.flock(fd, flags)
        except BlockingIOError:
            fd.close()
            raise AlreadyRunning("another cycle holds the state lock")
        _held, _depth, self.fd = fd, 1, fd
        return self

    def __exit__(self, *exc):
        global _held, _depth
        if _held is None:
            return False
        _depth -= 1
        if _depth <= 0:
            try:
                fcntl.flock(_held, fcntl.LOCK_UN)
            finally:
                _held.close(); _held = None; _depth = 0
        return False
```

Wrap the entry point once and keep inner modules lock-free:

```python
def run(window_days=7, dry_run=False):
    with LoopLock():
        return _run_locked(window_days, dry_run)
```

In `main()`, catch `AlreadyRunning` and return the skip code — never let it traceback.

---

## 2. Race test (verify the lock, do not read it)

```python
p1 = subprocess.Popen([sys.executable, "loop.py", "--window", "7"], ...)
time.sleep(0.35)
p2 = subprocess.Popen([sys.executable, "loop.py", "--window", "7"], ...)

assert {p1.returncode, p2.returncode} == {0, 4}, "lock did not hold"
```

Mirror it for the notifier: same cycle twice must produce sends `1, 0` and exactly
one new event row.

---

## 3. Cron entry shape

```cron
# header: purpose · authority · the problem it closes · doctrine pointer · boundary
# rollback: rm this file · verify: tail the log
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

7 */6 * * *  root /usr/bin/python3 <loop.py> --window 7 >> <log> 2>&1; \
             tail -n 3000 <log> > /tmp/x && mv /tmp/x <log>

43 4 * * *   root /usr/bin/python3 <promote.py> >> <boundary.log> 2>&1
```

Write the cadence reason in the header — slower than the thing it must not miss,
faster than the cadence it must not alias.

If the installed entry lives outside the loop's directory, keep a copy under the
loop's own `deploy/` so the live job is diffable against its source of truth. If the
write tool refuses to touch a system path, install it with the shell and keep the
`deploy/` copy as the diffable record.

---

## 4. Boundary self-test

```python
FORBIDDEN_PATHS = ("<governance>", "<canon>", "<kernel>",
                   "<loop>/config.yaml", "<loop>/verify.py", "<loop>/lock.py")

def assert_not_governance(target, intent):
    t = os.path.abspath(target)
    for f in FORBIDDEN_PATHS:
        if t == os.path.abspath(f) or t.startswith(os.path.abspath(f).rstrip("/") + "/"):
            raise GovernanceHold(f"forbidden: {intent} -> {target}")

def self_test():
    return [{"target": t, "blocked": _blocked(t)} for t in FORBIDDEN_PATHS]
```

What makes it a real boundary:

- the list lives **in the module**, never in a config the loop may read and edit
- the loop's own verifier, promoter, and lock modules are themselves on the list
- a hit raises; it never warns and continues
- `self_test()` runs every cycle and its result is recorded in the ledger

The agent operating the loop honours this too: if the environment refuses a write to
a protected config, record it as an open item. Do not route around the guard with a
shell command — that is exactly the bypass the boundary exists to prevent.

---

## 5. Notification gate wiring

```python
substance = json.dumps({
    "promoted":    sorted(...),      # sets, not counts
    "held":        sorted(...),
    "consequence": sorted(...),      # verdict TRANSITIONS only
}, sort_keys=True)
digest = hashlib.sha256(substance.encode()).hexdigest()[:16]
marker = os.path.join(state_dir, ".last_notify")
if os.path.exists(marker) and open(marker).read().strip() == digest:
    return                            # same substance already reported — stay silent

# ... send ...
with open(marker, "w") as fh:        # only AFTER the send reported success
    fh.write(digest)
```

Exclude unchanged `PENDING` verdicts from the substance set — a still-unelapsed
window is not news. Include a verdict that **changed** to `REGRESSED` and raise the
severity when it appears. Wrap the whole notify path so delivery can never fail the
loop.

---

## 6. Baseline schema

```json
{
  "<item>": {
    "pattern": "<what recurs>",
    "promoted_at": "<ISO>",
    "window_days": 7,
    "baseline_occurrences": 23,
    "backfilled": true,
    "status": "PENDING"
  }
}
```

`backfilled: true` means the window starts at the backfill — say so in the record so
the first verdict cannot be read as covering time before the instrument existed.

---

## 7. Ledger record shape

The record that makes the loop auditable:

```json
{
  "ts": "<ISO>", "actor": "<loop-id>", "type": "diagnose",
  "counts": {"found": 84, "novel": 4, "applied": 3, "held": 0, "withheld": 1},
  "applied": ["<id>", "<id>"],
  "exhale": true,
  "measurement": {"readable": true, "<signal>": "<value>"},
  "consequence": {"summary": {"by_verdict": {"PENDING": 5}},
                  "rows": [{"item": "...", "verdict": "PENDING", "detail": "..."}]},
  "boundary": [{"target": "...", "blocked": true}],
  "status": "EXHALED"
}
```

Write it **after** the actions. A run with an empty `applied` list and no holds is
`INHALE_ONLY` and must say so.
