#!/usr/bin/env python3
"""
forge-artifact-publisher — Slide builder utility.
Generates individual slide HTML files, combines with page breaks,
converts to PDF via Chrome headless.

Usage:
  python3 build_slides.py <slides_dir> <output.pdf> [--portrait]
  
Where <slides_dir> contains slide_01.html ... slide_NN.html
Each slide HTML should contain a <div class="slide">...</div> block.
Use --portrait for portrait A4 (dossiers, reports). Default is landscape (slide packs).
"""
import os
import re
import sys
import shutil
import subprocess
from html.parser import HTMLParser


class SlideExtractor(HTMLParser):
    """Robust HTML parser that extracts <div class="slide">...</div> blocks.

    Handles nested divs correctly by counting depth, and is immune to
    false matches on substrings like 'slide-title'.
    """

    def __init__(self):
        super().__init__()
        self.slides = []
        self._current_slide = None
        self._depth = 0
        self._start_pos = None
        self._raw = ""

    def feed(self, data):
        self._raw = data
        super().feed(data)

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            cls = dict(attrs).get("class", "")
            if cls == "slide" and self._current_slide is None:
                self._current_slide = []
                self._depth = 1
                self._start_pos = self.getpos()
            elif self._current_slide is not None:
                self._depth += 1

    def handle_endtag(self, tag):
        if tag == "div" and self._current_slide is not None:
            self._depth -= 1
            if self._depth == 0:
                # Reconstruct the raw HTML for this slide block
                start_line, start_col = self._start_pos
                end_line, end_col = self.getpos()
                lines = self._raw.split("\n")
                if start_line == end_line:
                    chunk = lines[start_line - 1][start_col:end_col]
                else:
                    chunk_lines = [lines[start_line - 1][start_col:]]
                    chunk_lines.extend(lines[start_line:end_line - 1])
                    chunk_lines.append(lines[end_line - 1][:end_col])
                    chunk = "\n".join(chunk_lines)
                self.slides.append(chunk)
                self._current_slide = None
                self._start_pos = None


def extract_slide_div(html_content):
    """Extract slide divs from a complete HTML document.

    Uses HTML parser (not regex) for robustness against nested divs,
    class name variants, and malformed HTML. Returns list of slide HTML
    strings (usually 1, but caller should handle multiple).
    """
    extractor = SlideExtractor()
    extractor.feed(html_content)
    return extractor.slides[0] if extractor.slides else None


# Error taxonomy for structured diagnostics
class ArtifactError(Exception):
    """Structured error with code for diagnostics."""
    def __init__(self, code, message, remediation=""):
        self.code = code
        self.remediation = remediation
        super().__init__(f"[{code}] {message}")


ERR_NO_SLIDES = "NO_SLIDES"
ERR_NO_HTML = "NO_HTML"
ERR_CHROME_MISSING = "CHROME_MISSING"
ERR_PDF_EMPTY = "PDF_EMPTY"
ERR_PAGE_MISMATCH = "PAGE_MISMATCH"
ERR_SIZE_EXCEEDED = "SIZE_EXCEEDED"
ERR_PDFINFO_MISSING = "PDFINFO_MISSING"


def extract_css(html_content):
    """Extract the <style> block from an HTML document."""
    match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    return match.group(1) if match else ""


def combine_slides(slides_dir, output_html, orientation="landscape"):
    """Combine individual slide HTMLs into one document with page breaks.

    Args:
        slides_dir: Directory containing slide_*.html files.
        output_html: Path for combined HTML output.
        orientation: 'landscape' or 'portrait' (affects @page CSS).
    """
    files = sorted(
        [f for f in os.listdir(slides_dir) if f.endswith(".html")]
    )
    if not files:
        raise ArtifactError(ERR_NO_HTML, f"No HTML files found in {slides_dir}",
                            "Ensure slides_dir contains slide_*.html files")

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

    # Build combined HTML with orientation-aware @page
    page_size = "297mm 210mm" if orientation == "landscape" else "210mm 297mm"
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@page {{ size: {page_size}; margin: 0; }}
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


def _find_chrome():
    """Find Chrome/Chromium binary. Returns path or None."""
    for name in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]:
        path = shutil.which(name)
        if path:
            return path
    return None


def _verify_pdf(output_pdf, expected_pages=None, max_size_mb=10):
    """Verify PDF output with structured checks."""
    if not os.path.exists(output_pdf) or os.path.getsize(output_pdf) == 0:
        raise ArtifactError(ERR_PDF_EMPTY, f"PDF is empty or missing: {output_pdf}",
                            "Check Chrome headless stderr for rendering errors")

    size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
    if size_mb > max_size_mb:
        print(f"WARNING [{ERR_SIZE_EXCEEDED}]: PDF is {size_mb:.1f}MB (limit: {max_size_mb}MB)")

    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        print(f"WARNING [{ERR_PDFINFO_MISSING}]: pdfinfo not found, skipping page count verification")
        print(f"  PDF generated: {os.path.getsize(output_pdf)} bytes")
        return

    verify = subprocess.run([pdfinfo, output_pdf], capture_output=True, text=True)
    if verify.returncode == 0:
        pages = None
        for line in verify.stdout.split("\n"):
            if "Pages:" in line or "File size:" in line:
                print(f"  {line.strip()}")
                if "Pages:" in line:
                    pages = int(line.split(":")[1].strip())
        if expected_pages and pages and pages != expected_pages:
            print(f"WARNING [{ERR_PAGE_MISMATCH}]: Expected {expected_pages} pages, got {pages}")
    else:
        print(f"  PDF generated: {os.path.getsize(output_pdf)} bytes")


def html_to_pdf(input_html, output_pdf, expected_pages=None, max_size_mb=10):
    """Convert HTML to PDF using Chrome headless.

    Falls back through: google-chrome → chromium → chromium-browser.
    """
    chrome = _find_chrome()
    if not chrome:
        raise ArtifactError(ERR_CHROME_MISSING,
                            "No Chrome/Chromium binary found in PATH",
                            "Install: apt-get install -y chromium-browser or google-chrome-stable")

    print(f"  Using Chrome: {chrome}")
    result = subprocess.run(
        [
            chrome,
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
        raise ArtifactError(ERR_PDF_EMPTY,
                            f"Chrome headless failed (exit {result.returncode}): {result.stderr[:200]}",
                            "Check HTML validity and Chrome dependencies")

    _verify_pdf(output_pdf, expected_pages, max_size_mb)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <slides_dir> <output.pdf> [--portrait]")
        print(f"  --portrait  Use portrait A4 (default: landscape)")
        sys.exit(1)

    slides_dir = sys.argv[1]
    output_pdf = sys.argv[2]
    orientation = "portrait" if "--portrait" in sys.argv else "landscape"
    output_html = output_pdf.replace(".pdf", ".html")

    print(f"=== forge-artifact-publisher ===")
    print(f"Slides dir: {slides_dir}")
    print(f"Output: {output_pdf}")
    print(f"Orientation: {orientation}")
    print()

    try:
        count = combine_slides(slides_dir, output_html, orientation)
        print()
        html_to_pdf(output_html, output_pdf, expected_pages=count)
        print()
        print(f"Done. {count} slides → {output_pdf}")
    except ArtifactError as e:
        print(f"\nFAILED [{e.code}]: {e}")
        if e.remediation:
            print(f"  Fix: {e.remediation}")
        sys.exit(1)


if __name__ == "__main__":
    main()
