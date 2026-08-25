# Graph Watcher v1.2 — Install & Operate

> **DITEMPA BUKAN DIBERI** ⚒️ — Watcher sleeps until files change,
> then re-indexes in 3s. Single daemon, ~50MB RSS.

## Files shipped

| File | What |
|------|------|
| `/root/AAA/graph/watcher.py` | Daemon process — inotify + debounce + indexer invocation |
| `/etc/systemd/system/graph-watcher.service` | systemd unit (T2 territory, NOT auto-activated) |

## Quick start (foreground, debug)

```bash
# foreground (Ctrl-C to stop)
/root/.venvs/codegraph/bin/python /root/AAA/graph/watcher.py
```

Logs to stdout + `/var/log/arifos/graph-watcher.log`.

## Background (T2, Arif gates activation)

```bash
# load unit, but don't enable auto-start
systemctl daemon-reload
systemctl start graph-watcher.service       # start now
systemctl status graph-watcher.service      # check
# optional: enable on boot
systemctl enable graph-watcher.service
```

The unit has `NoNewPrivileges` + `ProtectSystem=strict` + `ProtectHome=read-only`
hardening. Watcher still works under these because it only writes to
`/root/AAA/graph/codegraph.db` and `/var/log/arifos/`. If those paths
fail under strict mode, loosen to `ProtectSystem=full` (less safe).

## Behaviour

- Watches 7 repos: `arifOS, A-FORGE, AAA, GEOX, WELL, WEALTH, arifFlow`
- Source files: `.py, .pyi, .ts, .tsx, .js, .jsx, .mjs, .cjs`
- Excludes: `.*` (hidden), `node_modules`, `.venv`, etc. (handled in
  indexer.py; watcher filters to source exts at the watcher level)
- Debounce: 3.0 seconds (configurable via env `WATCHER_DEBOUNCE`)
- Per-repo flush: if multiple files in same repo change within debounce,
  the indexer is invoked once with `--repo <repo>` and runs the sha-cache
  to skip unchanged files. Net cost: ~0.3s per repo when cached.

## Verified (smoke-test, 2026-08-25)

```
$ touch /root/arifOS/test_watcher_trigger.py
[graph-watcher] flush arifOS: 1 files    # 3s after touch (debounce)
$ sqlite3 .../codegraph.db "SELECT symbol_count FROM files WHERE rel_path='test_watcher_trigger.py';"
1                                           # 1 symbol indexed ✓
```

## Known limitations (v1.2)

1. **No deletion handling** — if you `rm` a source file, the row stays in
   codegraph.db (orphan). Workaround: re-run full `indexer.py` periodically
   to clean. v1.3: add file-missing sweep.
2. **No moves** — `mv a.py b.py` fires `on_moved` which is mapped to
   `on_created` of the new path. The old path is left as orphan.
3. **Indexing is per-repo, not per-file** — coarse reindex; sha-cache
   keeps it fast (0.3s) but not optimal for huge bursts.
4. **No cross-repo renames** — if you move a file between repos, watcher
   doesn't propagate.

## Promotion criteria for cron

Per GOTONG_ROYONG.md, FI-008 cron pattern. Watcher doesn't need cron
(it's already a daemon), but consider:
- log rotation (`/var/log/arifos/graph-watcher.log` → daily)
- alert if watcher dies (`systemd RestartSec=10` covers this)

## Rollback

```bash
# stop daemon
systemctl stop graph-watcher.service
# (optional) disable auto-start
systemctl disable graph-watcher.service
# remove files
rm /root/AAA/graph/watcher.py
rm /etc/systemd/system/graph-watcher.service
# graph DB is untouched — reindex as needed via indexer.py
```

DITEMPA BUKAN DIBERI.