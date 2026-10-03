#!/usr/bin/env python3
"""Leadership roster archive builder — markdown dossiers -> one dark-theme PDF.

Usage:
    python3 roster_pdf_builder.py <archive_dir>

Expects in <archive_dir>:
    manifest.json  {"output_name": str,
                    "cover":   {"kicker", "title_html", "blurb", "meta_html"},
                    "holders": [{"slug", "name", "seat", "band"}, ...],
                    "closing": [{"slug", "title", "sub"}, ...]}
    dossiers/<slug>.md   for every slug (missing ones are reported, not fatal)
Writes <archive_dir>/out/<output_name>.html and .pdf, prints pages/bytes/sha256.

Edit manifest.json per task. Do not hand-edit this script per task.
"""
import os, sys, json, hashlib
import markdown
from weasyprint import HTML

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm;
  @bottom-center { content: counter(page); color:#6b6b7b; font-size:8pt; } }
* { box-sizing:border-box; }
body { background:#0a0a0f; color:#e6e6ef; font-family:"DejaVu Serif","Liberation Serif",Georgia,serif;
  font-size:10pt; line-height:1.55; margin:0; }
h1 { font-family:"DejaVu Sans",Helvetica,sans-serif; font-size:20pt; line-height:1.2;
  color:#fff; margin:0 0 2mm 0; }
h2 { font-family:"DejaVu Sans",Helvetica,sans-serif; font-size:13pt; color:#ffd166; margin:7mm 0 2mm 0;
  border-bottom:1px solid #23233a; padding-bottom:1.5mm; }
h3 { font-family:"DejaVu Sans",Helvetica,sans-serif; font-size:10.5pt; color:#8fd3ff; margin:4mm 0 1.5mm 0; }
p, li { margin:0 0 2mm 0; }
strong { color:#fff; } em { color:#bdbdd4; }
a { color:#8fd3ff; text-decoration:none; word-break:break-all; }
ul, ol { margin:0 0 2.5mm 4mm; padding:0; }
hr { border:0; border-top:1px solid #23233a; margin:4mm 0; }
code { font-family:"DejaVu Sans Mono",monospace; font-size:8pt; background:#16161f; padding:0 1mm; }
table { width:100%; border-collapse:collapse; margin:2mm 0 4mm 0; font-size:8.4pt;
  font-family:"DejaVu Sans",Helvetica,sans-serif; }
th { background:#1b1b2b; color:#ffd166; text-align:left; padding:1.6mm;
  border:1px solid #26263c; font-weight:600; }
td { padding:1.6mm; border:1px solid #26263c; vertical-align:top; color:#dcdce8; }
tr:nth-child(even) td { background:#101018; }
.cover { padding-top:38mm; }
.cover .kicker { font-family:"DejaVu Sans",Helvetica,sans-serif; letter-spacing:3px; font-size:8pt;
  color:#ff5d73; text-transform:uppercase; margin-bottom:6mm; }
.cover .rule { height:3px; width:36mm; background:#ff5d73; margin:6mm 0; }
.cover .sub { color:#a8a8c0; font-size:11pt; margin-top:4mm; max-width:130mm; }
.cover .meta { margin-top:26mm; color:#7a7a92; font-size:8.5pt;
  font-family:"DejaVu Sans",Helvetica,sans-serif; border-top:1px solid #23233a;
  padding-top:4mm; max-width:140mm; }
.seat { display:block; font-family:"DejaVu Sans",Helvetica,sans-serif; font-size:8.4pt;
  color:#a8a8c0; letter-spacing:0.4px; margin:0 0 3mm 0; }
.pill { display:inline-block; font-family:"DejaVu Sans",Helvetica,sans-serif; font-size:7.4pt;
  padding:0.8mm 2.2mm; border-radius:2mm; margin-right:2mm; }
.pill.founder   { background:#2b2110; color:#ffd166; border:1px solid #4d3c17; }
.pill.exec      { background:#1d2430; color:#8fd3ff; border:1px solid #29405a; }
.pill.chair     { background:#241d2e; color:#d3a8ff; border:1px solid #3d2b52; }
.pill.ceo       { background:#122b22; color:#7fe0b0; border:1px solid #1f4a3a; }
.pill.both      { background:#2c1a1a; color:#ff9d9d; border:1px solid #4d2828; }
.pill.incumbent { background:#2a1f2c; color:#ff8fd3; border:1px solid #4d2b47; }
.person { page-break-before: always; }
.foot { margin-top:8mm; border-top:1px solid #23233a; padding-top:3mm; color:#6b6b7b; font-size:8pt;
  font-family:"DejaVu Sans",Helvetica,sans-serif; }
"""


def md(text):
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "nl2br"])


def section(slug, title, seat, band, dos, foot):
    path = os.path.join(dos, slug + ".md")
    if os.path.exists(path):
        body = md(open(path, encoding="utf-8").read())
    else:
        print("  ! missing dossier:", slug, file=sys.stderr)
        body = ("<p><em>Dossier not produced — see the Sources &amp; Provenance section "
                "for the gap declaration.</em></p>")
    pill = f'<span class="pill {band}">{seat}</span>' if seat else ""
    return (f'<section class="person"><h1>{title}</h1>'
            f'<span class="seat">{pill}</span>{body}'
            f'<div class="foot">{foot}</div></section>')


def build(archive_dir):
    dos = os.path.join(archive_dir, "dossiers")
    out = os.path.join(archive_dir, "out")
    os.makedirs(out, exist_ok=True)
    man = json.load(open(os.path.join(archive_dir, "manifest.json"), encoding="utf-8"))

    cv = man.get("cover", {})
    parts = ['<section class="cover">'
             f'<div class="kicker">{cv.get("kicker", "Intelligence Archive")}</div>'
             f'<h1>{cv.get("title_html", "Leadership Archive")}</h1><div class="rule"></div>'
             f'<div class="sub">{cv.get("blurb", "")}</div>'
             f'<div class="meta">{cv.get("meta_html", "")}</div></section>']

    holders = man.get("holders", [])
    for i, h in enumerate(holders, 1):
        parts.append(section(h["slug"], h["name"], h.get("seat", ""), h.get("band", "exec"), dos,
                             f'Dossier {i} of {len(holders)}'))
    for c in man.get("closing", []):
        parts.append(section(c["slug"], c["title"], c.get("sub", ""), c.get("band", ""), dos, ""))

    html = ("<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>" + "".join(parts) + "</body></html>")
    name = man.get("output_name", "leadership-archive")
    open(os.path.join(out, name + ".html"), "w", encoding="utf-8").write(html)
    pdf = os.path.join(out, name + ".pdf")
    HTML(string=html, base_url=archive_dir).write_pdf(pdf)

    try:
        import pymupdf as pdf_lib
    except ImportError:
        import fitz as pdf_lib
    doc = pdf_lib.open(pdf)
    pages, size = len(doc), os.path.getsize(pdf)
    sha = hashlib.sha256(open(pdf, "rb").read()).hexdigest()
    print(f"PDF: {pdf}\npages={pages} bytes={size} sha256={sha}")
    return pdf


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")
