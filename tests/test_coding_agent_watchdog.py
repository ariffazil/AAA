#!/usr/bin/env python3
"""Contract tests for coding_agent_watchdog.py.

Runs the watchdog as a subprocess against a SYNTHETIC /proc tree via CAW_PROC_ROOT,
so no real process is inspected and nothing outside the temp dir is written.

Provable contract:
  1. a measurement failure yields UNKNOWN + exit 2, never OK
  2. a corrupt state file is a failure, not a clean slate
  3. an idle agent produces no signal
  4. high CPU + zero bytes written across STREAK runs -> STUCK_CANDIDATE + exit 1
  5. high CPU + advancing writes -> HIGH_CPU_ACTIVE (advisory), exit 0
  6. the watchdog never watches itself
  7. unmeasurable processes are counted out loud, not silently dropped
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPT = "/root/AAA/scripts/agent-cockpit/coding_agent_watchdog.py"
FAILS = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{'' if cond else '  -> ' + detail}")
    if not cond:
        FAILS.append(name)


def make_proc(root: Path, pid: int, cmdline: str, utime: int, stime: int, wb: int):
    d = root / str(pid)
    d.mkdir(parents=True, exist_ok=True)
    (d / "cmdline").write_bytes(cmdline.encode() + b"\0")
    # fields after the last ')': state + 10 more, then utime(11) stime(12)
    (d / "stat").write_text(
        f"{pid} ({cmdline.split()[0][:15]}) S 1 {pid} {pid} 0 -1 4194560 100 0 0 0 "
        f"{utime} {stime} 0 0 20 0 12 0 100000\n"
    )
    (d / "io").write_text(
        f"rchar: 1\nwchar: 1\nsyscr: 1\nsyscw: 1\nread_bytes: 0\n"
        f"write_bytes: {wb}\ncancelled_write_bytes: 0\n"
    )


def prime(state: Path, pid: int, ticks: int, wb: int, streak: int, ago: float = 300.0):
    """Write prior-sample state so the next run computes a deterministic delta.

    `ticks`/`wb` are the PREVIOUS sample; the synthetic /proc must separately be
    advanced to the CURRENT sample, or the delta goes negative and cpu_pct stays None.
    """
    st = json.loads(state.read_text()) if state.exists() else {}
    st["_ts"] = time.time() - ago
    st[str(pid)] = {"ticks": ticks, "wb": wb, "streak": streak, "harness": "qwen"}
    state.write_text(json.dumps(st))


QWEN_CMD = "/root/.local/lib/qwen-code/lib/cli-entry.js -y"


def advance(proc: Path, pid: int, ticks: int, wb: int, cmdline: str = QWEN_CMD):
    """Move the synthetic process forward to a new cumulative sample."""
    make_proc(proc, pid, cmdline, ticks, 0, wb)


def run(root, state, signals, extra=None):
    env = dict(os.environ, CAW_PROC_ROOT=str(root), CAW_STATE=str(state),
               CAW_SIGNALS=str(signals), CAW_STREAK_RUNS="3", CAW_HIGH_CPU_PCT="85",
               **(extra or {}))
    p = subprocess.run([sys.executable, SCRIPT], env=env, capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def env_new():
    d = Path(tempfile.mkdtemp(prefix="caw-"))
    return d / "proc", d / "state.json", d / "signals.jsonl"


print("T1  missing proc root -> UNKNOWN, exit 2, never OK")
proc, state, sig = env_new()
rc, out, err = run(proc / "does-not-exist", state, sig)
check("exit 2", rc == 2, str(rc))
check("says UNKNOWN", out.startswith("UNKNOWN"), out)
check("does not claim OK", "OK " not in out, out)

print("\nT2  corrupt state file is a failure, not a clean slate")
proc, state, sig = env_new()
proc.mkdir(parents=True)
state.write_text("{ this is not json")
rc, out, err = run(proc, state, sig)
check("exit 2", rc == 2, str(rc))
check("says UNKNOWN", out.startswith("UNKNOWN"), out)
check("names the unreadable state", "state" in out.lower(), out)

print("\nT3  idle agent -> no signal, exit 0")
proc, state, sig = env_new()
proc.mkdir(parents=True)
make_proc(proc, 4242, QWEN_CMD, 1000, 200, 5_000_000)
rc, out, err = run(proc, state, sig)          # first run: baseline only
check("baseline run exit 0", rc == 0, f"{rc} {err}")
advance(proc, 4242, 1400, 5_000_200)          # +200 ticks over 300s => 0.67% cpu
prime(state, 4242, 1200, 5_000_000, 0)        # prior sample
rc, out, err = run(proc, state, sig)
check("idle verdict OK", out.startswith("OK "), out)
check("no signals file written", not sig.exists(), str(sig))
check("exit 0", rc == 0, str(rc))

print("\nT4  high CPU + zero writes for 3 runs -> STUCK_CANDIDATE, exit 1")
proc, state, sig = env_new()
proc.mkdir(parents=True)
make_proc(proc, 5150, QWEN_CMD, 0, 0, 900)
rc, out, _ = run(proc, state, sig)
ticks, wb = 0, 900
verdicts = []
for i in range(3):
    prev_t, prev_w = ticks, wb
    ticks += 30_000                            # 300s of CPU over a 300s interval = 100%
    advance(proc, 5150, ticks, wb)             # write_bytes frozen at 900
    prime(state, 5150, prev_t, prev_w, i)
    rc, out, _ = run(proc, state, sig)
    verdicts.append(out.split()[0])
check("first two runs not yet STUCK", verdicts[:2] == ["OK", "OK"], str(verdicts))
check("third run is STUCK", verdicts[2] == "STUCK", str(verdicts))
check("exit 1 on STUCK", rc == 1, str(rc))
check("names the pid and harness", "5150" in out and "qwen" in out, out)
check("states zero output explicitly", "write_delta=0" in out, out)
lines = [json.loads(l) for l in sig.read_text().splitlines()] if sig.exists() else []
check("signal appended to jsonl", len(lines) == 1 and lines[0]["signal"] == "STUCK_CANDIDATE", str(lines))
check("signal carries evidence", lines and lines[0]["cpu_pct"] >= 85 and lines[0]["streak_runs"] == 3,
      str(lines))

print("\nT5  high CPU but writes advancing -> advisory only, exit 0")
proc, state, sig = env_new()
proc.mkdir(parents=True)
make_proc(proc, 6161, QWEN_CMD, 0, 0, 1_000)
run(proc, state, sig)
ticks, wb = 0, 1_000
for i in range(3):
    prev_t, prev_w = ticks, wb
    ticks += 30_000
    wb += 50_000                               # real work: bytes are leaving the process
    advance(proc, 6161, ticks, wb)
    prime(state, 6161, prev_t, prev_w, i)
    rc, out, _ = run(proc, state, sig)
check("verdict BUSY not STUCK", out.startswith("BUSY"), out)
check("exit 0 (advisory is not a failure)", rc == 0, str(rc))
check("explicitly says it is not a loop", "bukan loop" in out, out)
lines = [json.loads(l) for l in sig.read_text().splitlines()] if sig.exists() else []
check("logged as HIGH_CPU_ACTIVE", lines and lines[-1]["signal"] == "HIGH_CPU_ACTIVE", str(lines))

print("\nT6  the watchdog never watches itself")
proc, state, sig = env_new()
proc.mkdir(parents=True)
make_proc(proc, 7007, "python3 /root/AAA/scripts/agent-cockpit/coding_agent_watchdog.py", 0, 0, 0)
make_proc(proc, 7008, "python3 /root/AAA/scripts/agent-cockpit/stuck_detector.py", 0, 0, 0)
make_proc(proc, 7009, "node /root/.local/lib/qwen-code/lib/cli-entry.js serve --no-web", 0, 0, 0)
rc, out, _ = run(proc, state, sig)
check("self and sibling watchdog excluded", "agents=0" in out, out)
check("serve lane excluded (not a coding session)", "tiada coding-agent ditemui" in out, out)

print("\nT7  unmeasurable process is counted out loud, not silently dropped")
proc, state, sig = env_new()
proc.mkdir(parents=True)
make_proc(proc, 8080, "/usr/bin/opencode run", 0, 0, 0)
(proc / "8080" / "io").unlink()                # process vanished mid-scan
rc, out, _ = run(proc, state, sig)
check("reports unmeasurable count", "unmeasurable=1" in out, out)
check("does not claim a clean bill of health without disclosure", "unmeasurable" in out, out)

print("\n" + ("ALL CODING-AGENT WATCHDOG TESTS PASSED" if not FAILS else f"FAILURES: {FAILS}"))
sys.exit(1 if FAILS else 0)
