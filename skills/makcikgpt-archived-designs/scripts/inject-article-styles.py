#!/usr/bin/env python3
"""Inject canonical Primer Dark CSS into MakcikGPT articles.

Uses the UNIFIED 17px/1.65/max-680px typography (2026-08-14).
Idempotent — skips files that already have the new style block.
Run: python3 /tmp/inject-article-styles.py
From: makcikgpt-archived-designs skill
"""
import os, re, glob

MARKER = "font-size:17px;line-height:1.65"
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&family=JetBrains+Mono:wght@400;500&family=Inter:wght@400..900&display=swap" rel="stylesheet">'

STYLE = """<style>
:root{--bg:#0a0a0a;--bg-card:#111;--fg:#f0f0f0;--fg-muted:#9a9a9a;--red:#e0301e;--blue:#1f3fd4;--yellow:#f2b705}
body{background:var(--bg);color:var(--fg);font-family:"Newsreader","Georgia",serif;font-size:17px;line-height:1.65;max-width:680px;margin:0 auto;padding:48px 24px}
h1{font-family:"Cabinet Grotesk","Inter",sans-serif;font-size:clamp(24px,4vw,36px);font-weight:800;line-height:1.15;letter-spacing:-0.02em;margin:0 0 12px;color:var(--fg)}
h2{color:var(--yellow);font-size:1.3em;font-weight:700;margin:1.8em 0 0.6em}
h3{color:var(--red);font-size:1.15em;font-weight:700;margin:1.4em 0 0.5em}
p{margin-bottom:1em}
a{color:var(--yellow);text-decoration:underline;text-underline-offset:3px}
a:hover{color:var(--fg)}
blockquote{border-left:3px solid var(--blue);padding:10px 18px;margin:1.2em 0;background:rgba(31,63,212,0.05);border-radius:0 6px 6px 0;font-style:italic;color:var(--fg-muted);font-size:0.95em}
strong{color:var(--yellow);font-weight:700}
em{color:var(--fg-muted)}
hr{border:none;border-top:1px solid #2a2a2a;margin:1.5em 0}
ul,ol{margin-bottom:1em;padding-left:1.5em}
li{margin-bottom:0.3em}
table{width:100%;border-collapse:collapse;margin:1.2em 0;font-size:0.95em}
th{text-align:left;padding:8px 10px;border-bottom:2px solid var(--yellow);color:var(--yellow);font-weight:700;font-size:0.85em;text-transform:uppercase;letter-spacing:0.04em}
td{padding:6px 10px;border-bottom:1px solid #2a2a2a}
.footer-sig{margin-top:3rem;border-top:1px solid #2a2a2a;padding-top:1.2rem;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#666;text-align:center;letter-spacing:0.04em}
.footer-sig .kicker{color:var(--yellow);font-weight:600;margin-bottom:0.4rem;display:block}
</style>"""

base_dir = "/var/www/html/arif/makcikgpt-md"
injected = skipped = errors = 0

for f in sorted(glob.glob(os.path.join(base_dir, "*.html"))):
    basename = os.path.basename(f)
    if basename == "index.html":
        continue

    with open(f, "r", errors="replace") as fh:
        content = fh.read()

    if MARKER in content:
        skipped += 1
        continue

    if "</head>" not in content:
        errors += 1
        print(f"no </head>: {basename}")
        continue

    content = content.replace("</head>", f"{FONT}\n{STYLE}\n</head>", 1)

    with open(f, "w") as fh:
        fh.write(content)

    injected += 1
    print(f"  injected: {basename}")

print(f"injected={injected} skipped={skipped} errors={errors}")
