#!/usr/bin/env python3
"""Conformance suite for the ESM require() guard (SCAR-001).

Run directly: python3 /root/AAA/scripts/test_esm_require_guard.py

The negatives are the point. The guard replaced a grep that produced 3 findings
and 0 real defects, so every shape the OLD check wrongly flagged must now pass,
and every shape that genuinely throws at runtime must still be caught.
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

GATE = Path(__file__).with_name("esm_require_guard.py")
spec = importlib.util.spec_from_file_location("erg", GATE)
if spec is None or spec.loader is None:
    print(f"cannot load {GATE}", file=sys.stderr)
    sys.exit(2)
erg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(erg)

fails = []


def check(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        fails.append(label)


def make(tmp, name, body, pkg_type="module"):
    pkg = Path(tmp) / "package.json"
    pkg.write_text(json.dumps({"type": pkg_type}))
    f = Path(tmp) / name
    f.write_text(body)
    return f


print("=" * 74)
print("MUST PASS — shapes the old grep wrongly flagged")
print("=" * 74)

with tempfile.TemporaryDirectory() as t:
    f = make(t, "doc-comment.mjs", """
/**
 * CommonJS `require('./foo')` is treated as a generic call expression and
 * never enters analysis.imports. Patched with a focused regex pass.
 */
// require('node:os').tmpdir() in a line comment
export const x = 1;
""")
    check("require() only in comments → CLEAN", erg.check_file(f) == [])

with tempfile.TemporaryDirectory() as t:
    f = make(t, "shim-crypto.mjs", """
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
const require = createRequire(resolve('package.json'));
export const hash = (s) => require('node:crypto').createHash('sha256').update(s).digest('hex');
""")
    check("createRequire binding at module scope → CLEAN", erg.check_file(f) == [])

with tempfile.TemporaryDirectory() as t:
    f = make(t, "shim-lazy.mjs", """
export function tmp() {
  const require = createRequire(import.meta.url);
  return require('node:os').tmpdir();
}
""")
    check("createRequire(import.meta.url) → CLEAN", erg.check_file(f) == [])

with tempfile.TemporaryDirectory() as t:
    f = make(t, "cjs.js", "const os = require('node:os');\nmodule.exports = os;\n",
             pkg_type="commonjs")
    check("CommonJS package (type=commonjs) → CLEAN", erg.check_file(f) == [])

with tempfile.TemporaryDirectory() as t:
    f = make(t, "no-require.mjs", "import { tmpdir } from 'node:os';\nexport const t = tmpdir;\n")
    check("no require() at all → CLEAN", erg.check_file(f) == [])

print()
print("=" * 74)
print("MUST BLOCK — shapes that genuinely throw at runtime")
print("=" * 74)

with tempfile.TemporaryDirectory() as t:
    f = make(t, "bare-require.mjs",
             "import { join } from 'node:path';\nexport const d = join(require('node:os').tmpdir(), 'x');\n")
    r = erg.check_file(f)
    check("bare require() in ESM, no binding → VIOLATION", len(r) > 0)

with tempfile.TemporaryDirectory() as t:
    f = make(t, "bare-simple.mjs", "const os = require('node:os');\n")
    check("bare require() assignment (no binding) → VIOLATION",
          len(erg.check_file(f)) > 0)

with tempfile.TemporaryDirectory() as t:
    # require() in code, with the WORD createRequire appearing only in a comment
    f = make(t, "shadow-comment.mjs", """
// we could use createRequire here but we forgot
export const d = require('node:os').tmpdir();
""")
    check("createRequire only in comment → VIOLATION (not a real binding)",
          len(erg.check_file(f)) > 0)

print()
print("=" * 74)
print("COMMENT STRIPPER — line NUMBERING preserved (the property that matters)")
print("=" * 74)
# The guarantee is line-number alignment, so reported `line N` still matches the
# file. Measured limit: a trailing newline is not re-emitted, so counting "\n"
# would be the wrong metric — count LINES.
src = "a\n/* x\n y */\nrequire('z')\n"
stripped = erg.strip_comments(src)
check("line count preserved (splitlines)",
      len(stripped.splitlines()) == len(src.splitlines()))
check("block-comment content removed", "x" not in stripped)
check("line after block comment lands on the same line number",
      stripped.splitlines()[3].strip() == "require('z')")
check("code before block comment survives", stripped.splitlines()[0] == "a")

print()
print("-" * 74)
if fails:
    print(f"FAILED: {len(fails)}")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED — false positives gone, real violations still caught")
sys.exit(0)
