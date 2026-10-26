#!/usr/bin/env python3
"""Assemble Limbayong FDP report: markdown sections -> styled HTML -> PDF."""
import subprocess, pathlib, datetime, sys, re

WS = pathlib.Path('/root/AAA/forge_work/2026-10-19-limbayong-fdp')
sections = sorted((WS/'sections').glob('S*.md'))
front = WS/'CEO_MEMO.md'

parts = []
if front.exists():
    parts.append(front.read_text())
for p in sections:
    parts.append(p.read_text())

md = "\n\n\\newpage\n\n".join(parts)
(WS/'report.md').write_text(md)

css = (WS/'report.css').read_text()
html = subprocess.run(['pandoc','-f','markdown','-t','html5','--standalone',
                       '--metadata','title=Limbayong FDP',
                       '-c', str(WS/'report.css')],
                      input=md, capture_output=True, text=True, check=True).stdout
# inline the css so chromium finds it
html = html.replace(f'<link rel="stylesheet" href="{WS}/report.css" />', f'<style>{css}</style>')
# page breaks between h1
html = html.replace('<h1', '<h1 style="page-break-before:always"', 1)
html = html.replace('\n<h1', '\n<h1 style="page-break-before:always"')
(WS/'report.html').write_text(html)

out = WS/'Limbayong_FDP_HERMES_2026-10-19.pdf'
subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu',
                '--no-pdf-header-footer', f'--print-to-pdf={out}', f'file://{WS}/report.html'],
               check=True, capture_output=True)
print('PDF:', out, out.stat().st_size, 'bytes')
