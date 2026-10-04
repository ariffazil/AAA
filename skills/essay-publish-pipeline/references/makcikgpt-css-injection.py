#!/usr/bin/env python3
"""Inject Primer Dark CSS into MakcikGPT articles. Idempotent.
Created 2026-08-14. Sentinel: 'MAKCIKGPT ARTICLE — Primer Dark reader'
Run from anywhere: python3 <this-file>
"""
import os, re, glob

MARKER = "MAKCIKGPT ARTICLE — Primer Dark reader"
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&family=JetBrains+Mono:wght@400;500&family=Inter:wght@400..900&display=swap" rel="stylesheet">'

STYLE = """<style>
/* MAKCIKGPT ARTICLE — Primer Dark reader */
:root{--bg:#0a0a0a;--bg-card:#111;--fg:#f0f0f0;--fg-muted:#9a9a9a;--red:#e0301e;--blue:#1f3fd4;--yellow:#f2b705}
body{background:var(--bg);color:var(--fg);font-family:"Newsreader","Georgia",serif;font-size:18px;line-height:1.7;max-width:720px;margin:0 auto;padding:60px 24px}
h1{font-family:"Cabinet Grotesk","Inter",sans-serif;font-size:clamp(28px,5vw,42px);font-weight:800;line-height:1.1;letter-spacing:-0.02em;margin:0 0 16px}
h2{color:var(--yellow);font-size:1.4em;margin:2em 0 0.8em;font-weight:700}
h3{color:var(--red);font-size:1.1em;margin:1.5em 0 0.6em;font-weight:700}
p{margin-bottom:1.2em}
a{color:var(--yellow);text-decoration:underline;text-underline-offset:3px}
a:hover{color:var(--fg)}
blockquote{border-left:4px solid var(--blue);padding:12px 20px;margin:1.5em 0;background:rgba(31,63,212,0.06);border-radius:0 8px 8px 0;font-style:italic;color:var(--fg-muted)}
strong{color:var(--yellow);font-weight:700}
em{color:var(--fg-muted)}
code{font-family:"JetBrains Mono",monospace;background:rgba(255,255,255,0.06);padding:2px 6px;border-radius:4px;font-size:0.9em}
pre{background:var(--bg-card);border:1px solid #2a2a2a;border-radius:8px;padding:16px;overflow-x:auto}
pre code{background:none;padding:0}
hr{border:none;border-top:1px solid #2a2a2a;margin:2em 0}
ul,ol{margin-bottom:1.2em;padding-left:1.5em}
li{margin-bottom:0.4em}
img{max-width:100%;border-radius:8px;margin:1em 0}
table{width:100%;border-collapse:collapse;margin:1.5em 0}
th{text-align:left;padding:10px 12px;border-bottom:2px solid var(--yellow);color:var(--yellow);font-weight:700;font-size:0.85em;text-transform:uppercase;letter-spacing:0.04em}
td{padding:8px 12px;border-bottom:1px solid #2a2a2a}
</style>"""

base_dir = "/var/www/html/arif/makcikgpt-md"
injected = skipped = errors = 0

for f in sorted(glob.glob(os.path.join(base_dir, "*.html"))):
    basename = os.path.basename(f)
    if basename == "index.html":
        continue
    
    with open(f, 'r', errors='replace') as fh:
        content = fh.read()
    
    if MARKER in content:
        skipped += 1
        continue
    
    if '</head>' not in content:
        errors += 1
        print(f"✗ no </head>: {basename}")
        continue
    
    content = content.replace('</head>', f'{FONT}\n{STYLE}\n</head>', 1)
    
    with open(f, 'w') as fh:
        fh.write(content)
    
    injected += 1
    print(f"✓ injected: {basename}")

print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"injected={injected} · skipped={skipped} · errors={errors}")
