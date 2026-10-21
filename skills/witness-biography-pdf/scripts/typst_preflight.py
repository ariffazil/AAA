#!/usr/bin/env python3
"""Typst source preflight — shared by witness-biography-pdf + forensik-institutional-audit.
Run BEFORE `typst compile`. Exit 0 = safe to compile. Exit 1 = fix listed defects first.
Usage: python3 typst_preflight.py <file.typ> [file2.typ ...]
"""
import sys, re, os

DEFECTS = []

def check(path):
    src = open(path, encoding="utf-8").read()
    lines = src.split("\n")
    issues = []

    # 1. Unmatched square brackets per file (rough — brackets inside strings may false-positive)
    ob, cb = src.count("["), src.count("]")
    if ob != cb:
        issues.append(f"BRACKET-MISMATCH: {ob} '[' vs {cb} ']' (check near first mismatch)")

    # 2. Asterisk hazards: unbalanced * at line start, or 3+ asterisk runs
    for i, ln in enumerate(lines, 1):
        if "***" in ln:
            issues.append(f"L{i} TRIPLE-ASTERISK: '***' opens strong+emph that may not close. Replace with dashes.")
        # lines starting with single '*' are LEGAL when emphasis is balanced on the same line
        # (e.g. "*Bold intro* — rest of sentence"). Only flag if odd/unclosed.

    # 3. Unbalanced asterisk emphasis — BLOCK-level balance (emphasis may span lines)
    block_ast = src.replace("\\*", "").count("*")
    if block_ast % 2 != 0:
        issues.append("BLOCK-ODD-ASTERISK: odd total count of '*' — unclosed emphasis somewhere.")
    # 3b. Stray paren after a closing markup bracket (renders as literal ')' garbage in output)
    for i, ln in enumerate(lines, 1):
        if re.match(r"#\w+\[[^\]]*\]\)", ln):
            issues.append(f"L{i} STRAY-PAREN-AFTER-BRACKET: '#fn[...]') renders a stray ')' in the PDF. Drop the ')'.""")

    # 4. raw() with non-string
    for i, ln in enumerate(lines, 1):
        if re.search(r"raw\(\s*[^\"\'`#]", ln):
            issues.append(f"L{i} RAW-NONSTRING: raw() should receive a string.")

    # 5. Table pipes (markdown tables silently render as literal pipes)
    for i, ln in enumerate(lines, 1):
        if re.match(r"^\s*\|.*\|\s*$", ln):
            issues.append(f"L{i} MARKDOWN-TABLE: '|' rows do NOT render as tables in Typst. Use #table().")

    # 6. Unclosed #block / #figure by paren depth on function-start lines
    depth = 0
    for i, ln in enumerate(lines, 1):
        depth += ln.count("(") - ln.count(")")
        if depth < 0:
            issues.append(f"L{i} NEGATIVE-PAREN-DEPTH: extra ')' before this line.")
            depth = 0
    if depth > 0:
        issues.append(f"EOF UNCLOSED-PAREN: {depth} '(' never closed (find the last #block/#figure).")

    # 7. Missing local images
    base = os.path.dirname(os.path.abspath(path))
    for m in re.finditer(r'image\("([^"]+)"', src):
        img = m.group(1)
        if not os.path.isabs(img) and not os.path.exists(os.path.join(base, img)):
            issues.append(f"MISSING-IMAGE: {img} not found relative to .typ")

    # 8. orphan heading check (heading directly before #pagebreak = likely stranded)
    for i in range(1, len(lines)):
        if lines[i].strip().startswith("#pagebreak()") and (
            lines[i-1].startswith("== ") or lines[i-1].startswith("= ")):
            issues.append(f"L{i+1} ORPHAN-HEADING: heading immediately before #pagebreak() — body separated from header.")

    return issues

for path in sys.argv[1:]:
    if not os.path.exists(path):
        print(f"FILE-NOT-FOUND: {path}")
        DEFECTS.append(path)
        continue
    issues = check(path)
    if issues:
        print(f"--- {path}: {len(issues)} defect(s)")
        for it in issues:
            print(f"  {it}")
        DEFECTS.extend(issues)
    else:
        print(f"--- {path}: clean")

sys.exit(1 if DEFECTS else 0)
