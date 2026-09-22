#!/usr/bin/env python3
"""CHRON import-resolution probe (read-only).

For every LIVE entrypoint, replicate the sys.path / cwd / PYTHONPATH that the
live unit actually gives it, then statically extract every `import X` / `from X
import Y` and resolve each to a concrete __file__ using importlib.

Nothing is executed: resolution only. This is deliberately non-destructive so it
can be run against production entrypoints without triggering side effects.

DITEMPA BUKAN DIBERI
"""
from __future__ import annotations

import ast
import importlib.machinery
import importlib.util
import json
import os
import sys
from pathlib import Path

# (label, entrypoint_path, cwd, extra_env_PYTHONPATH, prepend_paths_after_script_dir)
ENTRYPOINTS = [
    ("systemd chron-loop-closer.service",
     "/root/chron/chron_loop_close.py", "/", "/root", []),
    ("systemd chron-loop-closer.service ExecStartPost",
     "/root/chron/chron_briefing.py", "/", "/root", []),
    ("systemd chron-prediction-verifier.service",
     "/root/chron/chron_cron_verify.py", "/", "/root", []),
    ("systemd chron-task0-reconciliation.service",
     "/root/scripts/chron_personal/task0_reconciliation.py", "/", None, []),
    ("systemd chron-mcp.service",
     "/root/chron/mcp_server.py", "/root/chron", "/root", ["/root"]),
    ("crontab 30 15 * * *",
     "/root/chron/verify_due.py", "/", None, []),
    ("ALPHA-ZEN card (alpha_zen_chron import chron)",
     "/root/AAA/scripts/alpha_zen_chron.py", "/", None, ["/root/AAA/scripts"]),
    ("ALPHA-ZEN card (alpha_zen_card path-resolves chron.py)",
     "/root/AAA/scripts/alpha_zen_card.py", "/", None, ["/root/AAA/scripts"]),
    ("T1 clock entrypoint (chron.py __main__)",
     "/root/AAA/scripts/chron.py", "/", None, ["/root/AAA/scripts"]),
]

STDLIB = set(sys.stdlib_module_names)


def build_path(entry: Path, pythonpath: str | None, prepend: list[str]) -> list[str]:
    """Approximate CPython's sys.path for `python3 <entry>`.

    sys.path[0] is the script's directory (not cwd) for a script invocation.
    PYTHONPATH entries (or cwd when unset) follow by default.
    """
    p = [str(entry.parent)]
    p += prepend
    if pythonpath:
        p += [x for x in pythonpath.split(os.pathsep) if x]
    else:
        p.append(os.getcwd())
    p += [x for x in sys.path if x not in ("", str(entry.parent))]
    # de-dup, keep order
    seen, out = set(), []
    for x in p:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def top_module(name: str) -> str:
    return name.split(".")[0]


def resolve(name: str, path: list[str]):
    """Return (resolved_file_or_None, how)."""
    for finder in (importlib.machinery.PathFinder,):
        try:
            spec = finder.find_spec(name, path)
        except (ImportError, AttributeError, ValueError):
            spec = None
        if spec is not None:
            origin = spec.origin
            how = "package" if spec.submodule_search_locations else "module"
            return origin, how
    return None, "unresolved"


def imports_of(src: Path):
    tree = ast.parse(src.read_text(), filename=str(src))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                found.append((a.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.level:            # relative import; skip (same package)
                continue
            if node.module:
                found.append((node.module, node.lineno))
                for a in node.names:
                    found.append((f"{node.module}.{a.name}", node.lineno))
    return found


def main() -> int:
    report = []
    for label, ep, cwd, pypath, prepend in ENTRYPOINTS:
        entry = Path(ep)
        os.chdir(cwd)
        path = build_path(entry, pypath, prepend)
        if not entry.exists():
            report.append({"entrypoint": label, "file": ep, "exists": False})
            continue
        rows, local_names = [], set()
        try:
            found = imports_of(entry)
        except SyntaxError as e:
            rows.append({"import": "<SYNTAX_ERROR>", "error": str(e)})
            found = []
        for name, lineno in found:
            t = top_module(name)
            if t in STDLIB:
                continue
            if t.startswith(("json", "pathlib", "datetime", "subprocess", "urllib",
                             "html", "re", "os", "sys", "ast", "argparse", "typing",
                             "collections", "time", "random", "hashlib", "logging",
                             "sqlite3", "shutil", "socket", "threading", "uuid",
                             "tempfile", "traceback", "statistics", "math", "copy",
                             "contextlib", "dataclasses", "enum", "decimal", "textwrap",
                             "functools", "itertools", "dataclasses", "zoneinfo")):
                continue
            if t not in local_names:
                local_names.add(t)
            origin, how = resolve(t, path)
            # also resolve the full dotted name when it is not a bare top-level
            if origin is None and "." in name:
                origin, how = resolve(name, path)
            rows.append({
                "import": name,
                "line": lineno,
                "resolved_to": origin,
                "how": how,
            })
        # dedupe by top-level module, prefer the entry that resolved
        ded, seen = [], {}
        for r in rows:
            k = r.get("import", "").split(".")[0]
            if k in seen:
                if not seen[k].get("resolved_to") and r.get("resolved_to"):
                    ded[ded.index(seen[k])] = r
                    seen[k] = r
                continue
            seen[k] = r
            ded.append(r)
        report.append({
            "entrypoint": label,
            "file": ep,
            "exists": True,
            "cwd": cwd,
            "PYTHONPATH": pypath,
            "sys_path": path[:6],
            "imports": ded,
        })
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
