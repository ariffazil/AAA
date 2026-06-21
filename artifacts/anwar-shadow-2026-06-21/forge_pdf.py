#!/usr/bin/env python3
"""Anwar Ibrahim Persona vs Shadow — PDF Forge."""
from weasyprint import HTML, CSS
import markdown

with open("/root/AAA/artifacts/anwar-shadow-2026-06-21/anwar-ibrahim-persona-vs-shadow.md") as f:
    md = f.read()

html_content = markdown.markdown(md, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4;
    margin: 2cm 1.8cm;
    @bottom-center {{
        content: "Anwar Ibrahim: Persona vs Shadow | 2026-06-21 | Page " counter(page) " of " counter(pages);
        font-family: 'Liberation Sans', sans-serif;
        font-size: 9pt;
        color: #555;
    }}
}}
body {{
    font-family: 'Liberation Serif', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #1a1a1a;
}}
h1 {{
    font-family: 'Liberation Sans', sans-serif;
    font-size: 22pt;
    color: #8B0000;
    border-bottom: 3px solid #8B0000;
    padding-bottom: 8px;
    margin-top: 0;
}}
h2 {{
    font-family: 'Liberation Sans', sans-serif;
    font-size: 16pt;
    color: #8B0000;
    margin-top: 28px;
    border-left: 4px solid #8B0000;
    padding-left: 12px;
}}
h3 {{
    font-family: 'Liberation Sans', sans-serif;
    font-size: 13pt;
    color: #444;
    margin-top: 20px;
}}
h4 {{
    font-family: 'Liberation Sans', sans-serif;
    font-size: 11.5pt;
    color: #555;
    margin-top: 16px;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 14px 0;
    font-size: 10pt;
}}
th, td {{
    border: 1px solid #999;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
}}
th {{
    background-color: #f0e8e8;
    color: #8B0000;
    font-weight: bold;
}}
code {{
    background-color: #f4f4f4;
    padding: 1px 4px;
    border-radius: 2px;
    font-family: 'Liberation Mono', monospace;
    font-size: 10pt;
}}
pre {{
    background-color: #f4f4f4;
    padding: 10px;
    border-left: 3px solid #8B0000;
    overflow-x: auto;
    font-size: 10pt;
}}
blockquote {{
    border-left: 3px solid #888;
    margin: 12px 0;
    padding: 6px 14px;
    color: #444;
    font-style: italic;
    background: #fafafa;
}}
hr {{
    border: 0;
    border-top: 1px solid #ccc;
    margin: 24px 0;
}}
ul, ol {{
    padding-left: 24px;
}}
li {{
    margin: 4px 0;
}}
strong {{
    color: #8B0000;
}}
.epistemic-box {{
    background: #fff8e8;
    border: 1px solid #d4a017;
    border-left: 4px solid #d4a017;
    padding: 10px 14px;
    margin: 14px 0;
}}
</style>
</head>
<body>
{html_content}
</body>
</html>
"""

HTML(string=full_html).write_pdf(
    "/root/AAA/artifacts/anwar-shadow-2026-06-21/anwar-ibrahim-persona-vs-shadow.pdf"
)
print("PDF forged:", "/root/AAA/artifacts/anwar-shadow-2026-06-21/anwar-ibrahim-persona-vs-shadow.pdf")