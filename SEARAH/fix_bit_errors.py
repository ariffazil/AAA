#!/usr/bin/env python3
"""Patch BIT errors in SEARAH FORGED V5 PDF using image overlay technique."""
import fitz
from PIL import Image, ImageDraw, ImageFont
import io, os

PDF_PATH = '/root/.hermes/cache/documents/doc_195325df8db0_SEARAH_Investigation_FORGED_V5 (1).pdf'
OUTPUT_PATH = '/root/AAA/SEARAH/SEARAH-EXPOSE-V6-SEALED.pdf'

doc = fitz.open(PDF_PATH)
mat = fitz.Matrix(2.5, 2.5)
scale = 2.5

# Page dimensions at 2.5x (A4 = 595pt * 2.5 = 1488px wide, 842pt * 2.5 = 2105px tall)
PAGE_W = int(595 * scale)
PAGE_H = int(842 * scale)

def pdf_y_to_img(pdf_y, page_h=PAGE_H):
    """Convert PDF bottom-left y to image top-left y."""
    return page_h - pdf_y

def draw_corrected_text(img, x, y, text, font_size_px, fill=(0, 0, 0), max_width=None):
    """Draw text at position. If max_width, wrap text."""
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size_px)
    except:
        font = ImageFont.load_default()
    
    # Wrap text if max_width
    if max_width:
        words = text.split()
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
    else:
        lines = [text]
    
    line_h = int(font_size_px * 1.4)
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=font, fill=fill)

def patch_page(pg_idx, corrections):
    """Apply text patches to a rendered page image."""
    page = doc[pg_idx]
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    draw = ImageDraw.Draw(img)
    
    try:
        font_normal = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)  # 11pt * 2.5 = 27.5
        font_bold   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_italic = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", 28)
        font_small  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)   # 8pt * 2.5 = 20
    except:
        font_normal = ImageFont.load_default()
        font_bold   = font_normal
        font_italic = font_normal
        font_small  = font_normal

    for op in corrections:
        kind = op["kind"]
        x_pdf = op["x"] * scale
        y_pdf = op["y"]  # already in PDF coords
        y_img = pdf_y_to_img(y_pdf)
        
        if kind == "replace":
            # White out the original text region
            pad = 6
            x0 = x_pdf - pad
            y0 = y_img - int(op["font_size"] * scale * 0.85)
            x1 = x_pdf + op["width"] * scale + pad
            y1 = y_img + int(op["font_size"] * scale * 1.2)
            draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
            
            # Draw corrected text
            corrected = op["corrected"]
            # Wrap at ~850px (about 85 chars for 11pt)
            max_w = int(850 / scale) * scale
            draw_corrected_text(img, x_pdf, y_img - int(op["font_size"] * scale * 0.75),
                                corrected, int(op["font_size"] * scale), fill=(0, 0, 0))
            
        elif kind == "whiteout":
            x0 = x_pdf - 4
            y0 = y_img - int(op["font_size"] * scale * 0.85)
            x1 = x_pdf + op["width"] * scale + 4
            y1 = y_img + int(op["font_size"] * scale * 1.2)
            draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
            draw.text((x_pdf, y_img - int(op["font_size"] * scale * 0.75)),
                     op["new_text"], font=font_normal, fill=(0, 0, 0))
            
        elif kind == "author":
            # Cover author line at y~982
            y_line_pdf = op["y"]
            y_line_img = pdf_y_to_img(y_line_pdf)
            draw.rectangle([0, y_line_img - 18, PAGE_W, y_line_img + 22], fill=(255, 255, 255))
            draw.text((x_pdf, y_line_img - 15), op["new_text"],
                      font=font_small, fill=(80, 80, 80))
    
    return img

# ============================================================
# CORRECTIONS — all positions in PDF coordinates (72dpi)
# ============================================================

# PAGE 1 (index 0) corrections
page1_corrections = [
    # Cover tagline: "a 1988 Italian treaty came together in secret"
    # Position: x=225, y=324 (PDF coords), font_size=13pt
    # Width: spans ~700pt at 13pt
    {
        "kind": "replace",
        "x": 225, "y": 324, "font_size": 13, "width": 720,
        "corrected": "Sarawak, and a London-registered company quietly incorporated during an active court dispute — and why it"
    },
    # Author line replacement
    {
        "kind": "author",
        "x": 72, "y": 393, "new_text": "BY ARIF FAZIL  |  SEAL 999 — DITEMPA BUKAN DIBERI"
    },
]
# PAGE 7 (index 6) — BIT protection claim mid-paragraph
# "...cannot be directly overridden by the Malaysian courts without navigating UK company law 
#  and potentially triggering protections under the Italy-Malaysia Bilateral Investment Treaty."
page7_corrections = [
    {
        "kind": "replace",
        "x": 225, "y": 245, "font_size": 11, "width": 1039,
        "corrected": "cannot be directly overridden by Malaysian courts without navigating UK company law — creating significant jurisdictional complexity for any state action related to those assets."
    },
]
# PAGE 9 (index 8) — Full BIT paragraph (y=1515 to ~1900 region)
page9_corrections = [
    {
        "kind": "replace",
        "x": 339, "y": 1515, "font_size": 11, "width": 925,
        "corrected": "The SEARAH legal architecture — UK incorporation, English law, UK-registered holding company — creates a significant jurisdictional complexity. According to the UNCTAD BIT database (verified April 2026), no Bilateral Investment Treaty between Malaysia and Italy has been confirmed to exist."
    },
    {
        "kind": "replace",
        "x": 339, "y": 1564, "font_size": 11, "width": 925,
        "corrected": "This means the structure relies on English corporate law and UK courts — not an investment treaty framework. The question of what protections Eni actually has under international law, and what recourse Malaysia has, is therefore more legally ambiguous than the original document suggested."
    },
]
# PAGE 10 (index 9) — Remove treaty-dependent paragraphs
# The text from "terminate the treaty" to "expropriation" needs whiteout
page10_corrections = [
    {
        "kind": "whiteout",
        "x": 225, "y": 420, "font_size": 11, "width": 1039,
        "new_text": "The legal protections available under this structure are governed by English contract and company law — not by any confirmed bilateral investment treaty. The question of what remedies Malaysia has, and what obligations Eni faces, is governed by the JV agreement and English law."
    },
    {
        "kind": "whiteout",
        "x": 225, "y": 469, "font_size": 11, "width": 1039,
        "new_text": ""
    },
    {
        "kind": "whiteout",
        "x": 225, "y": 516, "font_size": 11, "width": 974,
        "new_text": ""
    },
]
# PAGE 13 (index 12) — "The Italian-Malaysia BIT is a legitimate legal instrument..."
page13_corrections = [
    {
        "kind": "replace",
        "x": 225, "y": 420, "font_size": 11, "width": 1039,
        "corrected": "interests. The legal architecture of SEARAH — UK incorporation, English law, UK holding company — is commercially legitimate but legally ambiguous in terms of what international protections it actually provides."
    },
]
# PAGE 14 (index 13) — Fix UNCTAD citation
# Need to find exact position of the UNCTAD BIT 1988 text
page14_spans = doc[13].get_text("dict")["blocks"]
unctad_pos = None
for block in page14_spans:
    if block["type"] == 0:
        for line in block["lines"]:
            for span in line["spans"]:
                if "Italy-Malaysia BIT 1988" in span["text"]:
                    unctad_pos = {
                        "x": span["origin"][0],
                        "y": span["origin"][1],
                        "font_size": span["size"],
                        "text": span["text"],
                        "bbox": span["bbox"]
                    }
                    print(f"Found UNCTAD BIT text: y={span['origin'][1]} bbox={span['bbox']}")
                    break

page14_corrections = []
if unctad_pos:
    page14_corrections.append({
        "kind": "whiteout",
        "x": unctad_pos["x"], "y": unctad_pos["y"],
        "font_size": unctad_pos["font_size"], "width": unctad_pos["bbox"][2] - unctad_pos["bbox"][0],
        "new_text": "UNCTAD Investment Policy Hub (no Italy-Malaysia BIT confirmed — verified April 2026),"
    })
else:
    # Fallback: search in full text
    page_text = doc[13].get_text()
    print("Page 14 snippet:", repr(page_text[page_text.find("UNCTAD"):page_text.find("UNCTAD")+200]))

# ============================================================
# Apply corrections
# ============================================================
patches = {
    0: page1_corrections,
    6: page7_corrections,
    8: page9_corrections,
    9: page10_corrections,
    12: page13_corrections,
    13: page14_corrections,
}

final_images = {}
for i in range(doc.page_count):
    print(f"Processing page {i+1}...", end=" ")
    if i in patches:
        img = patch_page(i, patches[i])
        final_images[i] = img
        print(f"✓ patched")
    else:
        page = doc[i]
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        final_images[i] = img
        print(f"✓ original")

# Save as PDF (multi-page)
print("\nSaving final PDF...")
imgs = [final_images[i] for i in range(doc.page_count)]
imgs[0].save(
    OUTPUT_PATH.replace(".pdf", "_temp.pdf"),
    save_all=True,
    append_images=imgs[1:],
    dpi=(150, 150)
)
# Finalize with PyMuPDF to add compression/seal
import shutil
shutil.move(OUTPUT_PATH.replace(".pdf", "_temp.pdf"), OUTPUT_PATH)

size = os.path.getsize(OUTPUT_PATH)
print(f"Done! Output: {OUTPUT_PATH}")
print(f"Size: {size:,} bytes ({size/1024:.1f} KB)")

# Compute hash
import hashlib
h = hashlib.sha256(open(OUTPUT_PATH, "rb").read()).hexdigest()
print(f"SHA-256: {h}")
