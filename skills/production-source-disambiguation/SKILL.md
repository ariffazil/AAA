---
name: production-source-disambiguation
description: "Find the live path before mutating duplicated code files."
trigger: "production code, live service, audit replica, source-of-truth, multiple copies"
---

# Production Source Disambiguation

When a service runs on a host and the same-named code file exists in more than one location, the live behavior is determined by **which file the running process actually imports**, not by which file is "canonical" or "source of truth". Modifying the wrong file produces the same outcome as doing nothing — the change is real on disk, the running service is unchanged.

The class includes: Python modules loaded by `node` or `systemd` via subprocess (env vars `PYTHON_PATH` / `PYTHONPATH` determine which is imported), compiled `.pyc` shadowing source `.py`, audit replicas that look identical to source repos, gitignored shadow files, and configuration templates that were never wired to the live path. The lesson is universal: **probe what the running process imports, not what the filesystem says exists**.

## Procedure

1. **Resolve the process that owns the service first, before reading any file's content.**
   - For systemd: `systemctl cat <service>` shows the `ExecStart` line. `systemctl status <service>` shows the active Main PID. The cwd of that PID is the working directory the service resolves relative imports against.
   - For Node + Python subprocess: read `server.js` (or equivalent) to find `execFile(PYTHON, [...])`. The first argument is the script path the node process actually executes — that is the *live* path, regardless of what a separate "source" repo elsewhere contains.
   - For long-running workers: `ls -la /proc/<pid>/cwd` and `cat /proc/<pid>/cmdline` together resolve the process's actual root and command line. Reading the source file on disk is necessary but not sufficient.

2. **Find every file with the same basename on the host, not just the obvious one.**
   ```bash
   find / -name 'fetch_gold.py' -type f 2>/dev/null
   ```
   List them with `stat -c '%y %s %n'` so the modification time, size, and path are visible in one glance. When three paths exist, the wrong guess is plausible until proven otherwise — never trust a single `find` result over the absence of others.

3. **Trace the import chain.** For Python: `python3 -c "import sys; print('\n'.join(sys.path))"` and `cat .pth` files referenced by the venv. For systemd drop-ins at `/etc/systemd/system/<service>.service.d/`, every file with `Environment=PYTHON*` line overrides the base unit file. For Node: `require.resolve` at the script entry point.

4. **Probe what the live process is reading at runtime, not what it should read.** The check that falsifies a wrong-file claim is a runtime behavior probe: `curl localhost:PORT/endpoint` and inspect the response shape, version string, or a unique diagnostic field. If the value matches the old code, the modification is in the wrong file.

5. **Resolve the live path FIRST, modify SECOND, restart THIRD, verify FOURTH.** Each step has its own verification: `stat -c '%y %s %n' <live>` before edit; `sha256sum <live>` after edit; `systemctl restart` to reload the imported bytecode; re-probe the runtime to confirm the change is live. Skipping the fourth step is the "fixed in source, not in service" failure.

## Pitfalls

- **Multiple copies of the same-named file on disk is the canonical hazard.** A `find` for the basename returns 2-3+ paths in any non-trivial system. The right answer is always the *process-imported* path; the wrong answer is the *git-canonical* path. Never assume "the source tree is what the service reads" without probing.
- **Reading the running process's mtime vs the source file's mtime reveals the gap.** If the worker started before the source file's last write, the worker still has the old bytecode regardless of the source being correct. Patching the source is verified by `ls -la /proc/<pid>/cwd && grep '<change-marker>' <source>` — the worker is importing from the *current* source path *after restart*. Before restart, no claim is true.
- **`PYTHONPATH` / `PYTHON_PATH` environment variables silently override the path.** A systemd drop-in at `/etc/systemd/system/<service>.service.d/python-path.conf` containing `Environment=PYTHON_PATH=/root/somewhere/.venv/bin/python3` means the live interpreter is *that* interpreter, not `system python3`. Reading `/usr/bin/python3` to test the modified module gives the wrong answer.
- **Symlinks resolve to targets that have a different file in the same directory tree.** A symlink from `/var/www/gold/api/fetch_gold.py` to `/root/WEALTH/engines/commodity/gold-api/fetch_gold.py` looks like a single file but resolves to a different parent. `write_file(path=<link-path>)` writes to the target, not the link, and may clobber the canonical source. Before any edit on a path in a shared tree, run `readlink -f <path>`.
- **`cd` in a systemd `ExecStart` is a working-directory override, not a no-op.** `WorkingDirectory=/var/www/gold/api` means relative paths in `ExecStart` resolve against *that* dir, and the process imports any relative-to-cwd paths from there. A `cd` somewhere else in the command chain is irrelevant; the unit's `WorkingDirectory=` is the binding.
- **A calibration harness can pass against replicas and miss the live engine entirely.** When the harness imports `model_cone_at` from a same-named module in `harness.py`, and the live engine imports `cmd_forecast` from `fetch_gold.py`, modifying `harness.py` and verifying the harness is *correct* and *useless* — the live behavior is unchanged. The right test is the live API endpoint, not the harness.
- **A Python module file in the same directory as a Python package with the same name shadows the package.** `chron.py` (a module) beside `chron/` (a package) on `sys.path` makes `import chron.chron_store` fail silently with `'chron' is not a package`. Detect with `python3 -c "import <name>; print(<name>.__file__)"` and confirm the resolved path is a directory containing `__init__.py`, not a sibling `.py`.
- **Mtime / size is not enough to identify the live file.** Two same-named files can have similar size and mtime. Sort by *provenance* (systemd `ExecStart` line, `git log` of the file, import resolution, file owner and PID cwd) — not by date or bytes alone.
- **A cache masks the truth until restart.** The node server.js may have an in-memory 10-minute cache that serves the old response for the cache lifetime even after the underlying Python module is correctly updated. Probe *after* the cache window, or force a cache invalidation, or restart the service, before claiming "the change is live".
- **Restart is a mutation. Sequence it last.** For daemon patches: (1) write source, (2) verify the file, (3) restart the service, (4) probe that the new behavior is live, (5) seal. Skipping (3) means the seal describes the source, not the running system.
- **Revert quickly when the wrong file is found.** When the modification hits an audit replica instead of the live engine, the honest move is to roll back, write the receipt, and retry on the live path — not to "fix" the replica and pretend it was always the target.
- **Probe the runtime answer, not the documentation.** Service `ExecStart`, `cat /proc/<pid>/cwd`, `readlink -f` on the executable path, and a live `curl` to the endpoint — those four are the test. The README, the directory structure, and the git log are hypotheses to test, not answers.

## Step 4 — the receipt

When a production modification lands, the receipt has to carry:
- `live_path` — the exact file path the running process imports from (verified with `readlink -f` if symlinked).
- `live_sha256_before` and `live_sha256_after` — hashes of the live file, not the source file.
- `service_name` — the systemd unit or equivalent.
- `service_pid` at restart — proves a restart actually happened.
- `runtime_probe_before` and `runtime_probe_after` — the response or behavior value before and after the change, both labeled by timestamp.
- `restart_timestamp` — when the service was actually restarted.
- `cache_window_disclosed` — if the service has a cache, the cache TTL and when the next refresh will occur.

A receipt missing the `live_path` field, or carrying the source-tree path instead, is not a receipt for the production modification — it is a receipt for a different file's edit.

## Recovery — what to do when wrong file was modified

1. **Roll back the wrong file from the receipt's `before` hash** (`sha256sum` of the original, captured before edit).
2. **Write the receipt**: which file was wrongly modified, why it was wrong (which path the live process actually imports), and the SHA of the rollback.
3. **Resolve the correct live path**, modify, restart, re-probe. The receipt is the same shape; the path is different.
4. **Acknowledge in the next round of evidence that the prior round modified the wrong file.** Hiding the wrong-file incident and treating the second attempt as a fresh modification removes the audit trail; surfacing it preserves it.

DITEMPA BUKAN DIBERI ⚒️