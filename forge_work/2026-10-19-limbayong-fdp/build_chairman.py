#!/usr/bin/env python3
import subprocess, pathlib
WS = pathlib.Path('/root/AAA/forge_work/2026-10-19-limbayong-fdp')
md = (WS/'SHADOW_FDP_CHAIRMAN_PAPER.md').read_text()
css = (WS/'report.css').read_text()
css += """
@page { margin: 22mm 20mm 22mm 20mm; }
body { font-size:10.2pt; line-height:1.52; }
h1 { font-size:17pt; letter-spacing:-0.3pt; margin-bottom:2pt;}
h2 { font-size:11.8pt; margin-top:15pt; border-bottom:0.5pt solid #bbb;}
table { font-size:8.4pt; }
blockquote { font-size:9.4pt; }
"""
html = subprocess.run(['pandoc','-f','markdown','-t','html5','--standalone'],
                      input=md, capture_output=True, text=True, check=True).stdout
html = html.replace('</head>', f'<style>{css}</style></head>')
out_html = WS/'chairman.html'
out_html.write_text(html)
out = WS/'Limbayong_Shadow_FDP_Chairman_Paper.pdf'
subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu',
                '--no-pdf-header-footer', f'--print-to-pdf={out}', f'file://{out_html}'],
               check=True, capture_output=True)
print('PDF:', out, out.stat().st_size)
