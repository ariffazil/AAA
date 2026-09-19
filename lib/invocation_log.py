"""invocation_log — canonical federation telemetry. Tuas 2.

WHY THIS EXISTS
---------------
The 2026-09-19 KITARAN audit found that only ONE organ (GEOX) kept a real
invocation log, and only one (HERMES) could answer "how many skills were
actually loaded". Everywhere else, the ceremony/exercise ratio had to rest on a
labelled PROXY instead of a measurement. A system that emits thousands of
artifacts but never records which of them was used cannot know whether it
works.

This module is the missing measurement. One line per real invocation, one
format, every organ. It is deliberately tiny and dependency-free so that
adopting it costs an import and one call.

THE CONTRACT (frozen — seven organs wire against this)
------------------------------------------------------
  log_invocation(organ, tool, actor_id=None, ok=True, duration_ms=None, ...)

  - Appends ONE JSON object to /var/lib/arifos/metrics/tool_invocations.jsonl
  - NEVER raises into the caller. Telemetry must not break the thing it
    measures; every failure is swallowed and, at most, noted on stderr.
  - NEVER blocks on a lock. It opens O_APPEND and writes one line, which is
    atomic for small payloads on POSIX.
  - Format matches the GEOX precedent so existing readers keep working.

THE READBACK (why the numbers stop being proxies)
-------------------------------------------------
  exercise_count(organ, window_days=30)
      -> {"distinct_tools": n, "distinct_actors": n, "total": n, ...}

  That is exactly the numerator `exercised_capabilities` needs, and the
  `executors` count. Feed it into arifosmcp/runtime/asabiyyah.py and the CER/
  ASD denominators stop being proxies.

PRIVACY BOUNDARY
----------------
Record the IDENTITY of the tool, never the ARGUMENTS. No payloads, no message
bodies, no human state. A tool name and an actor id are MAP, not STORY.
`extra` exists for organ-specific counters (row counts, byte sizes) and must
never carry content.

Standard library only.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

__all__ = [
    "log_invocation",
    "timed",
    "instrument",
    "exercise_count",
    "LOG_PATH",
    "DEFAULT_WINDOW_DAYS",
]

LOG_PATH = Path("/var/lib/arifos/metrics/tool_invocations.jsonl")
DEFAULT_WINDOW_DAYS = 30
_ROTATE_BYTES = 64 * 1024 * 1024
_HOST = None


def _host() -> str:
    global _HOST
    if _HOST is None:
        try:
            _HOST = socket.gethostname()
        except Exception:  # pragma: no cover
            _HOST = "unknown"
    return _HOST


def _rotate_if_needed(path: Path) -> None:
    try:
        if path.exists() and path.stat().st_size > _ROTATE_BYTES:
            for i in range(4, 0, -1):
                src = path.with_suffix(path.suffix + f".{i}")
                dst = path.with_suffix(path.suffix + f".{i + 1}")
                if src.exists():
                    os.replace(src, dst)
            os.replace(path, path.with_suffix(path.suffix + ".1"))
    except Exception:
        pass


def log_invocation(
    organ: str,
    tool: str,
    *,
    actor_id: str | None = None,
    ok: bool = True,
    duration_ms: float | None = None,
    session_id: str | None = None,
    error: str | None = None,
    extra: dict[str, Any] | None = None,
    path: Path | str | None = None,
) -> bool:
    """Append one invocation receipt. Returns True if written.

    Never raises. A telemetry failure must never take down the caller -- that
    would make the instrument more dangerous than the disease.
    """
    try:
        p = Path(path) if path else LOG_PATH
        p.parent.mkdir(parents=True, exist_ok=True)
        _rotate_if_needed(p)
        now = time.time()
        rec: dict[str, Any] = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(now)) + "Z",
            "organ": organ,
            "tool": tool,
            "actor_id": actor_id,
            "ok": bool(ok),
            "duration_ms": round(duration_ms, 3) if duration_ms is not None else None,
            "session_id": session_id,
            "epoch": now,
            "host": _host(),
        }
        if error:
            # Truncated: an error string can carry a payload by accident.
            rec["error"] = str(error)[:200]
        if extra:
            # Counters only. Never content.
            rec["extra"] = {k: v for k, v in extra.items() if isinstance(v, (int, float, bool, str))}
        line = json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n"
        fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
        try:
            os.write(fd, line.encode("utf-8"))
        finally:
            os.close(fd)
        return True
    except Exception as exc:  # pragma: no cover - must never propagate
        try:
            print(f"[invocation_log] suppressed: {exc}", file=sys.stderr)
        except Exception:
            pass
        return False


@contextmanager
def timed(organ: str, tool: str, *, path: Path | str | None = None, **kw: Any) -> Iterator[dict[str, Any]]:
    """Time a block and log it. Failures are logged as ok=False and re-raised.

        with timed("WELL", "well_daily_checkin", actor_id=who) as ctx:
            ctx["extra"] = {"rows": 12}
            do_work()

    `path` is a sink override for tests ONLY and is routed to the logger, never
    treated as a context key -- otherwise a test silently writes into the live
    production log and pollutes real telemetry.
    """
    start = time.perf_counter()
    ctx: dict[str, Any] = dict(kw)
    try:
        yield ctx
    except BaseException as exc:
        dur = (time.perf_counter() - start) * 1000.0
        log_invocation(
            organ,
            tool,
            actor_id=ctx.get("actor_id"),
            ok=False,
            duration_ms=dur,
            session_id=ctx.get("session_id"),
            error=type(exc).__name__,
            extra=ctx.get("extra"),
            path=path,
        )
        raise
    dur = (time.perf_counter() - start) * 1000.0
    log_invocation(
        organ,
        tool,
        actor_id=ctx.get("actor_id"),
        ok=True,
        duration_ms=dur,
        session_id=ctx.get("session_id"),
        extra=ctx.get("extra"),
        path=path,
    )


def instrument(organ: str, tool: str | None = None, *, path: Path | str | None = None):
    """Decorator that logs every call of a function.

        @instrument("GEOX")
        def geox_claim(...): ...

    `path` is a sink override for tests ONLY (see `timed`).
    """

    def deco(fn):
        name = tool or fn.__name__

        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
            except BaseException as exc:
                log_invocation(
                    organ,
                    name,
                    ok=False,
                    duration_ms=(time.perf_counter() - start) * 1000.0,
                    error=type(exc).__name__,
                    path=path,
                )
                raise
            log_invocation(
                organ,
                name,
                ok=True,
                duration_ms=(time.perf_counter() - start) * 1000.0,
                path=path,
            )
            return result

        try:
            wrapper.__name__ = getattr(fn, "__name__", name)
            wrapper.__doc__ = getattr(fn, "__doc__", None)
        except Exception:
            pass
        return wrapper

    return deco


def exercise_count(
    organ: str | None = None,
    window_days: int = DEFAULT_WINDOW_DAYS,
    *,
    path: Path | str | None = None,
) -> dict[str, Any]:
    """The readback that turns a proxy into a measurement.

    Returns distinct tools and distinct actors actually receipted inside the
    window -- the numerator for `exercised_capabilities` and `executors`.
    Malformed lines are counted, not silently dropped (a log with unparsable
    lines is itself a finding).
    """
    p = Path(path) if path else LOG_PATH
    cutoff = time.time() - window_days * 86400
    tools: set[str] = set()
    actors: set[str] = set()
    organs: set[str] = set()
    total = 0
    unparsable = 0
    failed = 0
    if not p.exists():
        return {
            "organ": organ or "ALL",
            "window_days": window_days,
            "total": 0,
            "distinct_tools": 0,
            "distinct_actors": 0,
            "organs_seen": [],
            "unparsable": 0,
            "failed": 0,
            "source": str(p),
            "note": "log absent: no invocation telemetry for this path",
        }
    try:
        with p.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    unparsable += 1
                    continue
                ep = rec.get("epoch")
                if not isinstance(ep, (int, float)) or ep < cutoff:
                    continue
                if organ and rec.get("organ") != organ:
                    continue
                total += 1
                if rec.get("tool"):
                    tools.add(str(rec["tool"]))
                if rec.get("actor_id"):
                    actors.add(str(rec["actor_id"]))
                if rec.get("organ"):
                    organs.add(str(rec["organ"]))
                if rec.get("ok") is False:
                    failed += 1
    except Exception as exc:  # pragma: no cover
        return {"organ": organ or "ALL", "error": str(exc), "source": str(p)}

    return {
        "organ": organ or "ALL",
        "window_days": window_days,
        "total": total,
        "distinct_tools": len(tools),
        "distinct_actors": len(actors),
        "organs_seen": sorted(organs),
        "unparsable": unparsable,
        "failed": failed,
        "source": str(p),
    }


def _main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(prog="invocation_log", description="federation invocation telemetry")
    ap.add_argument("--organ", default=None)
    ap.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    ap.add_argument("--path", default=None)
    a = ap.parse_args(argv)
    print(json.dumps(exercise_count(a.organ, a.window_days, path=a.path), indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
