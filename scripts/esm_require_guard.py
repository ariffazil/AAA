#!/usr/bin/env python3
"""ESM require() guard — SCAR-001, made precise.

WHY THIS REPLACED A GREP (2026-09-18):
The original check inside pre-commit-lsp-gate.sh was:

    grep -nE '\\brequire\\s*\\(' "$file" | grep -v 'import.*require' | grep -v 'node_modules'

Measured on a real merge, it produced 3 findings and **all 3 were false positives**:

  * extract-import-map.mjs — every hit is inside a `/** ... */` JSDoc block that
    *documents* how CommonJS require() is handled. Prose, not code.
  * prepare-incremental.mjs — `const require = createRequire(resolve(pluginRoot, 'package.json'))`
    is declared at module scope (line 41), so `require('node:crypto')` resolves.
  * scan-project.mjs — same shape, binding declared at line 78.

Proven rather than argued: under `node --input-type=module`, `require('node:crypto')`
through a createRequire binding returns a working hash, while a bare `require('node:os')`
throws "require is not defined". The gate was flagging the working case.

This is the same class of defect as the W_scar v1 gate (a lexical grep cannot tell
structure from assertion) and the doctrine-status negation bug (a word inside a
disclaimer read as a claim). Three instances, one invariant: **read the construct
in its enclosing scope before calling it a violation.**

WHAT IS ACTUALLY A VIOLATION:
A `.mjs`/`.js` file inside a `{"type":"module"}` package that CALLS `require(...)`
outside a comment, when the file does NOT establish a require binding.

Exit codes: 0 clean, 1 violations found, 2 could not run (fail-closed).

Usage:
  esm_require_guard.py FILE [FILE ...]     check specific files
  esm_require_guard.py --staged            check git-staged code files
"""
import json
import re
import subprocess
import sys
from pathlib import Path

CODE_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs"}

# A file that establishes any of these OWNS its `require`, so calling it is legal.
BINDING_RE = re.compile(
    r"(?:const|let|var)\s+require\s*=\s*createRequire|"
    r"createRequire\s*\(\s*import\.meta|"
    r"\brequire\s*=\s*module\.createRequire|"
    r"\bconst\s+require\s*=",
)

CALL_RE = re.compile(r"\brequire\s*\(")


def strip_comments(text: str) -> str:
    """Remove block and line comments while preserving line count.

    Line-preserving so reported line numbers still match the file. Strings are
    not parsed -- a `require(` inside a string literal is rare in this tree and
    would be a conservative (over-reporting) error, not a silent miss.
    """
    out = []
    in_block = False
    for line in text.splitlines():
        if in_block:
            end = line.find("*/")
            if end == -1:
                out.append("")
                continue
            line = " " * (end + 2) + line[end + 2:]
            in_block = False
        # strip any block comments opening on this line (possibly several)
        while True:
            start = line.find("/*")
            if start == -1:
                break
            end = line.find("*/", start + 2)
            if end == -1:
                line = line[:start]
                in_block = True
                break
            line = line[:start] + " " * (end + 2 - start) + line[end + 2:]
        # strip line comments (not perfect for `//` inside strings; conservative)
        for marker in ("//",):
            idx = line.find(marker)
            if idx != -1:
                line = line[:idx]
        out.append(line)
    return "\n".join(out)


def nearest_package_json(path: Path) -> Path | None:
    for parent in [path.parent, *path.parents]:
        pkg = parent / "package.json"
        if pkg.is_file():
            return pkg
    return None


def check_file(path: Path) -> list[str]:
    """Return violation strings for one file (empty = clean)."""
    if path.suffix.lower() not in CODE_EXT or not path.is_file():
        return []
    pkg = nearest_package_json(path)
    if pkg is None:
        return []
    try:
        meta = json.loads(pkg.read_text())
    except Exception:
        return []
    if str(meta.get("type", "")).lower() != "module":
        return []  # not an ESM package — require() is legitimate

    try:
        text = path.read_text(errors="replace")
    except OSError:
        return []

    code = strip_comments(text)
    if not CALL_RE.search(code):
        return []  # no require() in code (comments don't count)

    if BINDING_RE.search(code):
        return []  # file establishes its own require binding — legal

    hits = [
        f"    line {i}: {ln.strip()[:100]}"
        for i, ln in enumerate(code.splitlines(), 1)
        if CALL_RE.search(ln)
    ]
    return [
        f"SCAR-001 {path} — require() called in an ESM package ({pkg}) "
        f"with no createRequire binding"
    ] + hits


def staged_files() -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, timeout=20,
    )
    if out.returncode != 0:
        print("esm-require-guard: git error — fail-closed", file=sys.stderr)
        sys.exit(2)
    return [Path(p) for p in out.stdout.split("\n") if p.strip()]


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    files = staged_files() if args == ["--staged"] else [Path(a) for a in args]

    violations = []
    for f in files:
        violations.extend(check_file(f))

    if violations:
        for v in violations:
            print(f"  ✗ {v}")
        return 1
    print(f"esm-require-guard: {len(files)} file(s) checked, 0 violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
