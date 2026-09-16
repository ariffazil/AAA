#!/usr/bin/env python3
"""
forge-artifact-publisher — Slide builder utility.
Generates individual slide HTML files, combines with page breaks,
converts to PDF via Chrome headless.

Usage:
  python3 build_slides.py <slides_dir> <output.pdf>
  
Where <slides_dir> contains slide_01.html ... slide_NN.html
Each slide HTML should contain a <div class="slide">...</div> block.
"""
import os
import re
import sys
import subprocess


def extract_slide_div(html_content):
    """Extract the slide div from a complete HTML document.
    
    Handles nested divs by counting open/close tags.
    """
    start = html_content.find('<div class="slide')
    if start == -1:
        return None
    
    # Find the matching closing div by counting nesting
    depth = 0
    i = start
    while i < len(html_content):
        if html_content[i:i+4] == '<div':
            # Check it's actually a tag (not inside text)
            if i + 4 >= len(html_content) or html_content[i+4] in ' \t\n>':
                depth += 1
        elif html_content[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return html_content[start:i+6]
        i += 1
    return None


def extract_css(html_content):
    """Extract the <style> block from an HTML document."""
    match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    return match.group(1) if match else ""


def combine_slides(slides_dir, output_html):
    """Combine individual slide HTMLs into one document with page breaks."""
    files = sorted(
        [f for f in os.listdir(slides_dir) if f.endswith(".html")]
    )
    if not files:
        print(f"ERROR: No HTML files found in {slides_dir}")
        sys.exit(1)

    # Extract CSS from first slide
    with open(os.path.join(slides_dir, files[0])) as f:
        css = extract_css(f.read())

    # Extract slide divs
    slide_divs = []
    for fname in files:
        with open(os.path.join(slides_dir, fname)) as f:
            content = f.read()
        div = extract_slide_div(content)
        if div:
            slide_divs.append(div)
        else:
            print(f"WARNING: No slide div found in {fname}")

    if not slide_divs:
        print("ERROR: No slide divs extracted")
        sys.exit(1)

    # Build combined HTML
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@page {{ size: 297mm 210mm; margin: 0; }}
{css}
.slide {{ page-break-after: always; }}
.slide:last-child {{ page-break-after: auto; }}
</style>
</head><body>
"""
    for div in slide_divs:
        html += div + "\n"
    html += "</body></html>"

    with open(output_html, "w") as f:
        f.write(html)

    print(f"Combined {len(slide_divs)} slides → {output_html} ({len(html)} bytes)")
    return len(slide_divs)


def html_to_pdf(input_html, output_pdf):
    """Convert HTML to PDF using Chrome headless."""
    result = subprocess.run(
        [
            "google-chrome",
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={output_pdf}",
            "--print-to-pdf-no-header",
            input_html,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: Chrome headless failed: {result.stderr}")
        sys.exit(1)

    # Verify
    verify = subprocess.run(
        ["pdfinfo", output_pdf], capture_output=True, text=True
    )
    if verify.returncode == 0:
        for line in verify.stdout.split("\n"):
            if "Pages:" in line or "File size:" in line:
                print(f"  {line.strip()}")
    else:
        size = os.path.getsize(output_pdf)
        print(f"  PDF generated: {size} bytes")


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <slides_dir> <output.pdf>")
        sys.exit(1)

    slides_dir = sys.argv[1]
    output_pdf = sys.argv[2]
    output_html = output_pdf.replace(".pdf", ".html")

    print(f"=== forge-artifact-publisher ===")
    print(f"Slides dir: {slides_dir}")
    print(f"Output: {output_pdf}")
    print()

    count = combine_slides(slides_dir, output_html)
    print()
    html_to_pdf(output_html, output_pdf)
    print()
    print(f"Done. {count} slides → {output_pdf}")


if __name__ == "__main__":
    main()
