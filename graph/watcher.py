#!/usr/bin/env python3
"""
watcher.py — v1.2 incremental re-indexer for codegraph.db.

Watches 7 federation repos for .py/.ts/.tsx/.js/.jsx/.mjs/.cjs/.pyi file
changes, debounces, and re-indexes affected files into /root/AAA/graph/codegraph.db
via indexer.py (which already handles incremental re-runs via sha256 cache).

Usage:
  /root/.venvs/codegraph/bin/python /root/AAA/graph/watcher.py
  # runs forever until SIGINT

Operational notes:
  - One Python process, ~50MB RSS
  - Latency: change → reindexed ≤5s
  - Coalesces bursts (saves multiple edits to same file)
  - Logs to /var/log/arifos/graph-watcher.log when daemonized

What this does NOT do:
  - Cross-machine (only watches local paths under /root/)
  - Watch .venv, node_modules, __pycache__ (excluded by indexer.py)
  - Push to a remote graph (single-tenant, local)

DITEMPA BUKAN DIBERI ⚒️
"""
from __future__ import annotations
import logging
import os
import subprocess
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

# Third-party
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Repo config (matches indexer.py)
REPOS = ["arifOS", "A-FORGE", "AAA", "GEOX", "WELL", "WEALTH", "arifFlow"]
ROOT = Path("/root")
INDEXER = Path("/root/AAA/graph/indexer.py")
PYTHON = "/root/.venvs/codegraph/bin/python"
DEBOUNCE_SECONDS = 3.0
LOG_PATH = "/var/log/arifos/graph-watcher.log"

logging.basicConfig(
    level=os.environ.get("WATCHER_LOG_LEVEL", "INFO"),
    format="[graph-watcher] %(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)
log = logging.getLogger("graph-watcher")


# ─── debounce + coalesce ──────────────────────────────────────────────────


class CoalesceBuffer:
    """Per-repo pending file sets, debounced."""

    def __init__(self, debounce_s: float = DEBOUNCE_SECONDS):
        self._lock = threading.Lock()
        self._pending: dict[str, set[str]] = defaultdict(set)
        self._timers: dict[str, threading.Timer] = {}
        self._debounce = debounce_s
        self._on_flush = None  # callback

    def add(self, repo: str, rel_path: str):
        with self._lock:
            self._pending[repo].add(rel_path)
            # reset timer
            t = self._timers.get(repo)
            if t:
                t.cancel()
            self._timers[repo] = threading.Timer(
                self._debounce, self._flush_repo, args=(repo,)
            )
            self._timers[repo].daemon = True
            self._timers[repo].start()

    def _flush_repo(self, repo: str):
        with self._lock:
            files = sorted(self._pending.pop(repo, set()))
            self._timers.pop(repo, None)
        if not files:
            return
        log.info(f"flush {repo}: {len(files)} files")
        if self._on_flush:
            try:
                self._on_flush(repo, files)
            except Exception as e:
                log.exception(f"flush handler failed for {repo}: {e}")


# ─── file change handler ──────────────────────────────────────────────────


class SourceFileHandler(FileSystemEventHandler):
    """Watchdog handler that filters to source files and routes to CoalesceBuffer."""

    EXTS = {".py", ".pyi", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}

    def __init__(self, buffer: CoalesceBuffer):
        super().__init__()
        self._buffer = buffer

    @staticmethod
    def _classify(path: str) -> tuple[str, str] | None:
        """Map an absolute path to (repo, rel_path). Returns None if not in any repo."""
        rp = Path(path).resolve()
        for repo in REPOS:
            root = (ROOT / repo).resolve()
            try:
                rel = rp.relative_to(root)
            except ValueError:
                continue
            if rel.parts[0].startswith("."):  # skip hidden dirs
                return None
            if any(p.startswith(".") for p in rel.parts):  # .venv, .git etc
                return None
            return repo, rel.as_posix()
        return None

    def _maybe_record(self, event):
        if event.is_directory:
            return
        info = self._classify(event.src_path)
        if not info:
            return
        repo, rel = info
        if Path(event.src_path).suffix.lower() not in self.EXTS:
            return
        log.debug(f"event {event.event_type}: {repo}/{rel}")
        self._buffer.add(repo, rel)

    def on_modified(self, event):
        self._maybe_record(event)

    def on_created(self, event):
        self._maybe_record(event)

    def on_moved(self, event):
        # Treat move as delete (old) + create (new) of the new path
        if event.dest_path:
            self._maybe_record(type("E", (), {
                "is_directory": False, "src_path": event.dest_path,
                "event_type": "moved"
            })())


# ─── indexer invocation ──────────────────────────────────────────────────


def reindex_files(repo: str, files: list[str]) -> int:
    """Run indexer.py with --repo <repo>; indexer re-reads whole repo but
    sha-cache means unchanged files skip parsing. Returns number of new
    files indexed (from indexer output)."""
    try:
        result = subprocess.run(
            [PYTHON, str(INDEXER),
             "--db", "/root/AAA/graph/codegraph.db",
             "--repo", repo, "--quiet"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            log.error(f"indexer {repo} failed: rc={result.returncode} stderr={result.stderr[:500]}")
            return -1
        # Parse "X new / ~Y upd / =Z cached   sym=A edges=B imports=C" line
        for line in result.stdout.splitlines():
            if "new" in line and "cached" in line:
                # Extract X from "+X new"
                import re
                m = re.search(r"\+(\d+)\s+new", line)
                if m:
                    return int(m.group(1))
        return 0
    except subprocess.TimeoutExpired:
        log.error(f"indexer {repo} timed out")
        return -1
    except Exception as e:
        log.exception(f"reindex_files {repo} crashed: {e}")
        return -1


# ─── main ───────────────────────────────────────────────────────────────


def main():
    log.info(f"starting watcher (repos={REPOS}, debounce={DEBOUNCE_SECONDS}s)")
    buffer = CoalesceBuffer(DEBOUNCE_SECONDS)
    buffer._on_flush = reindex_files

    observer = Observer()
    handler = SourceFileHandler(buffer)
    for repo in REPOS:
        repo_root = ROOT / repo
        if not repo_root.exists():
            log.warning(f"repo {repo_root} does not exist, skipping")
            continue
        observer.schedule(handler, str(repo_root), recursive=True)
        log.info(f"watching {repo_root}")
    observer.start()
    log.info("watcher started; press Ctrl-C to stop")

    try:
        while observer.is_alive():
            observer.join(timeout=1.0)
    except KeyboardInterrupt:
        log.info("interrupted, stopping")
        observer.stop()
    observer.join(timeout=5)
    log.info("watcher stopped")


if __name__ == "__main__":
    main()