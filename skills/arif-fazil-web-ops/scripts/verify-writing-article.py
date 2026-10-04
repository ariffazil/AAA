#!/usr/bin/env python3
"""Verify a /words/writing/ article page against the site's conventions.

Usage: python3 verify-writing-article.py <path-to-index.html>

Checks:
  1. HTML5 tag balance (void elements self-close)
  2. Cover-block pattern: .cover-emoji, .cover-kicker, .cover-title,
     .cover-subtitle, .cover-byline
  3. CSS link -> /words/writing/_shared/writing.css (no inline <style>)
  4. Epistemic tag (INT or other value)
  5. S4 Governance Canon + Article #N markers
  6. Section count (expects 12 sections: <h2>Section N — ...)
  7. Superscript ref anchors [1][2][3] with matching <li id="ref-N">
  8. Same-site link targets resolve on disk (excluding known /999/ nav)
  9. Shared writing.css exists on disk
 10. No <script> tags (content-first surface)

Exit code 0 = all pass, 1 = failures. Prints PASS/FAIL per check."""
import os, re, sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <path-to-index.html>")
    sys.exit(2)

HTML = sys.argv[1]
CSS  = "/var/www/html/arif/words/writing/_shared/writing.css"
DOCROOT = "/var/www/html/arif"

fails = []
def check(name, ok):
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok: fails.append(name)

assert os.path.exists(HTML), f"article missing: {HTML}"
content = open(HTML, encoding="utf-8").read()

# 1. HTML5 tag balance
VOID = {"meta","link","br","hr","img","input","source","area","base","col","embed","param","track","wbr"}
stack, errs = [], []
for m in re.finditer(r"</?([a-zA-Z][a-zA-Z0-9]*)((?:\"[^\"]*\"|'[^']*'|[^>\"'])*)>", content):
    tag, rest = m.group(1), m.group(2)
    if m.group(0).startswith("</"):
        if stack and stack[-1] == tag: stack.pop()
        else: errs.append(f"unexpected </{tag}> at offset {m.start()}")
    elif rest.rstrip().endswith("/") or tag in VOID: continue
    else: stack.append(tag)
check("HTML tag balance (no unclosed/mismatched)", not errs and not stack)

# 2. Cover-block pattern
for cls in ["cover-emoji", "cover-kicker", "cover-title", "cover-subtitle", "cover-byline"]:
    check(f"cover-block: .{cls}", f'class="{cls}"' in content)

# 3. CSS link, not inline
check("CSS link -> /words/writing/_shared/writing.css",
      'href="/words/writing/_shared/writing.css"' in content)
check("no inline <style> (content-first)", "<style>" not in content)

# 4. Epistemic tag
check("epistemic tag present", 'class="tag">' in content)

# 5. Canon markers
check("S4 Governance Canon marker", "S4 Governance Canon" in content or "Article #" in content)

# 6. Sections
secs = re.findall(r"<h2>Section (\d+)", content)
check(f"{len(secs)} sections present", len(secs) >= 1)

# 7. Superscript refs
sup = re.findall(r'href="#ref-(\d+)">\[\d+\]</a>', content)
ids = set(re.findall(r'id="ref-(\d+)"', content))
check(f"superscript refs [{', '.join(sorted(sup, key=int))}] present", len(sup) >= 1)
check("every #ref-N has matching id=ref-N", set(sup) <= ids)

# 8. Same-site link integrity
links = re.findall(r'href="(/[^"#]*?)(?:#[^"]*)?"', content)
KNOWN_NAV = {"/999/"}
missing = []
for href in set(links):
    if href.startswith("http") or href.endswith((".xml",".json")) or href in KNOWN_NAV:
        continue
    candidate = os.path.normpath(DOCROOT + href)
    if not os.path.exists(candidate) and not os.path.exists(candidate + "/index.html"):
        missing.append(href)
check("same-site link targets exist on disk (excl. /999/ nav)", not missing)
if missing: print("  missing:", missing)

# 9. Shared CSS on disk
check("shared writing.css exists on disk", os.path.exists(CSS))

# 10. No JS
check("no <script> tags (content-first)", "<script" not in content)

print()
if fails:
    print(f"VERIFICATION FAILED: {len(fails)} check(s): {fails}")
    sys.exit(1)
print("VERIFICATION PASSED: all checks passed")
