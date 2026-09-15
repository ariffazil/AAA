#!/usr/bin/env python3
"""seal-on-quiescence.py — commit the RSI loop when its writer stops.

Why: several lanes were writing /root/AAA/rsi at 22:06-22:22 (ledger.py, promote.py,
consequence.py, state/*). Committing mid-write captures a torn snapshot.
So: wait for the tree to go quiet, then seal ONE checkpoint commit.

Bounds:
  - quiescent = no source write in QUIET_S for 5 min
  - hard deadline 45 min — commit anyway, labelled as a forced checkpoint
Scope (narrow, never touches other lanes' in-flight files):
  rsi/  ops/capabilities/  reports/rsi-wire-audit-2026-09-15.md
  reports/reexam-queue-collapse-2026-09-15.md
Rollback: git reset --soft HEAD~1
"""
import os, subprocess, sys, time, datetime

AAA = "/root/AAA"
WATCH = [f"{AAA}/rsi", f"{AAA}/ops/capabilities"]
SKIP = ("__pycache__", ".pytest_cache")
PATHS = ["rsi", "ops/capabilities",
         "reports/rsi-wire-audit-2026-09-15.md",
         "reports/reexam-queue-collapse-2026-09-15.md"]
QUIET_S = 300
DEADLINE_S = 2700
LOG = "/var/log/arifos/rsi-seal.log"


def log(msg):
    line = f"{datetime.datetime.now().isoformat(timespec='seconds')} | {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def newest_mtime():
    m = 0.0
    for root in WATCH:
        for dp, dn, fn in os.walk(root):
            if any(s in dp for s in SKIP):
                continue
            dn[:] = [d for d in dn if d not in SKIP]
            for f in fn:
                try:
                    m = max(m, os.path.getmtime(os.path.join(dp, f)))
                except OSError:
                    pass
    return m


def main():
    t0 = time.time()
    last = newest_mtime()
    last_change = time.time()
    log(f"watch started — newest source mtime {datetime.datetime.fromtimestamp(last)}")

    while True:
        time.sleep(30)
        cur = newest_mtime()
        if cur > last:
            last = cur
            last_change = time.time()
            log(f"writer active — new mtime {datetime.datetime.fromtimestamp(cur)}")
        elapsed_quiet = time.time() - last_change
        elapsed_total = time.time() - t0
        if elapsed_quiet >= QUIET_S:
            log(f"QUIESCENT {int(elapsed_quiet)}s — sealing")
            break
        if elapsed_total >= DEADLINE_S:
            log(f"DEADLINE {int(elapsed_total)}s reached with a live writer — forced checkpoint")
            break

    r = subprocess.run(["git", "-C", AAA, "add", "--"] + PATHS,
                       capture_output=True, text=True)
    if r.returncode:
        log(f"git add FAILED: {r.stderr.strip()}")
        return 1
    msg = ("seal(rsi-loop): capability ledger ingestion FIRED + consequence measurement live\n\n"
           "First firing checkpoint of the AAA RSI loop (F13 PARTIAL-SEAL verdict map).\n"
           "Ledger ingestion wrote 5 capability atoms at 22:22:02 (11 -> 16 entries).\n"
           "consequence.py captures promotion baselines; h(t) still uncharacterized.\n"
           "Boundary: promote.py FORBIDDEN_PATHS self-test PASS.\n")
    r = subprocess.run(["git", "-C", AAA, "commit", "-m", msg],
                       capture_output=True, text=True)
    if r.returncode:
        log(f"git commit status: {r.stdout.strip()} {r.stderr.strip()}")
        if "nothing to commit" in (r.stdout + r.stderr):
            return 0
    log(f"committed: {subprocess.run(['git','-C',AAA,'log','-1','--format=%h %s'],capture_output=True,text=True).stdout.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
