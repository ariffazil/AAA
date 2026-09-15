#!/usr/bin/env python3
"""lock.py — single-writer guard for the RSI loop's own state.

Why: `/root/AAA/ops/capabilities/capability-ledger.yaml` already takes an
exclusive flock because a two-writer race clobbered it on 2026-09-12. The RSI
loop's state has the same shape (read atoms → decide → append + atomic-replace
the graph and baselines) and now has two possible writers: the cron job and any
manual/nested run. Two concurrent cycles would rewrite `capability-graph.json`
and `baselines.json` from stale reads, and baselines are the measurement the
whole consequence verdict rests on — moving them silently invalidates it.

Same pattern as probe-capabilities.py::LedgerLock and carry_forward.py::CarryLock.
Reentrant within a process so loop.py can hold it across modules without nesting
deadlocks; a second PROCESS fails fast rather than waiting, because a blocked
cron job is worse than a skipped one.
"""
from __future__ import annotations

import atexit
import fcntl
import os

LOCK_PATH = "/root/AAA/rsi/state/.loop.lock"

_held = None  # module-level: reentrancy within one process
_depth = 0


class LoopLock:
    """Exclusive, non-blocking, reentrant-within-process advisory lock."""

    def __init__(self, blocking: bool = False, path: str = LOCK_PATH):
        self.path = path
        self.blocking = blocking
        self.fd = None

    def __enter__(self):
        global _held, _depth
        if _held is not None:          # already held by this process
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
            raise AlreadyRunning(
                "another RSI loop cycle holds the state lock — "
                "refusing to run a second writer against the same state")
        _held = fd
        _depth = 1
        self.fd = fd
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
                _held.close()
                _held = None
                _depth = 0
        return False


class AlreadyRunning(RuntimeError):
    """A second cycle is in flight. Exit non-zero so cron triage sees it."""


def _release_at_exit():
    global _held
    if _held is not None:
        try:
            fcntl.flock(_held, fcntl.LOCK_UN)
            _held.close()
        except Exception:
            pass
        _held = None


atexit.register(_release_at_exit)


if __name__ == "__main__":
    with LoopLock():
        print("lock acquired:", LOCK_PATH)
    print("lock released")
