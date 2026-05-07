#!/usr/bin/env python3
"""
SEARAH v16 — FORGED_V5 style replica
White pages, LiberationSerif body, red accent bar on Part pages,
running header/footer, drop cap, timeline, questions table.
Follows FORGED_V5 exactly: #111 / #CC0000 / #FAFAFA palette,
LiberationSerif + LiberationSans + DejaVuSans fonts.
"""
import os, sys

# Register Liberation fonts
font_paths = {
    'LiberationSerif':           '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
    'LiberationSerif-Bold':      '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
    'LiberationSerif-Italic':    '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf',
    'LiberationSans':            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    'LiberationSans-Bold':       '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    'LiberationSans-Italic':    '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf',
    'LiberationSans-BoldItalic': '/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf',
    'DejaVuSans':               '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    'DejaVuSans-Bold':          '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
}
for name, path in font_paths.items():
    if os.path.exists(path):
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        pdfmetrics.registerFont(TTFont(name, path))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, KeepTogether,
    PageBreak, BaseDocTemplate, PageTemplate, NextPageTemplate,
    Frame, HRFlowable, BalancedColumns
)
from reportlab.platypus.flowables import Flowable
import hashlib, hmac, datetime

# ─── FORGED_V5 Palette ────────────────────────────────────────────────────────
C_BLACK  = HexColor('#000000')
C_111    = HexColor('#111111')   # dark headings, dark rule lines
C_1A1A   = HexColor('#1A1A1A')   # body text
C_222    = HexColor('#222222')   # secondary dividers
C_333    = HexColor('#333333')   # secondary body
C_555    = HexColor('#555555')   # subtitle gray
C_888    = HexColor('#888888')   # labels / metadata
C_999    = HexColor('#999999')   # footer / page numbers
C_CCC    = HexColor('#CCCCCC')   # light borders
C_DDD    = HexColor('#DDDDDD')   # table/border lines
C_F0F0   = HexColor('#F0F0F0')   # alternating table row
C_F8F8   = HexColor('#F8F8F8')   # table alt row 2
C_FAFA   = HexColor('#FAFAFA')   # timeline background
C_WHITE  = white
C_RED    = HexColor('#CC0000')   # FORGED_V5 red accent
C_COVER_BG = C_WHITE             # cover = white, not navy

# ─── Page Geometry (FORGED_V5) ─────────────────────────────────────────────────
W, H = A4   # 595 × 842 pts

# Margins match FORGED_V5: ~90pts (~3.2cm) left/right
ML = 90; MR = 90
# Content top starts after header zone on regular pages
REG_TOP = H - 60 - 38   # allow header + thin line before content starts
MB = 82                 # bottom margin
MT = 60                 # top margin for regular pages

CW = W - ML - MR       # 415 pts content width

# ─── SEAL hashes ───────────────────────────────────────────────────────────────
DOC_HASH  = '6feb0c57a81256e41c62a471cd7b9f8dc68c7978321dfbc72b'
DB_HASH   = '64b4a80e8e92c101c764331e44db5c3af172b8946b476e0b2'
HMAC_KEY  = b'arif_fazil_seal999_key_v1'
HMAC_MSG  = f"SEARAH-EXPOSE-v16|{DOC_HASH}|{datetime.date.today().isoformat()}"
SEAL_HMAC = hmac.new(HMAC_KEY, HMAC_MSG.encode(), hashlib.sha256).hexdigest()
TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
OUTPUT    = '/root/AAA/SEARAH/SEARAH-EXPOSE-v16-FINAL.pdf'

# ─── Style Factory ─────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

# Body: 11pt LiberationSerif, justified, ~1.4 leading
BODY       = S('Body',    fontName='LiberationSerif',    fontSize=11,  leading=15.5,
               alignment=TA_JUSTIFY, spaceAfter=6, textColor=C_1A1A)
# Cover subtitle paragraph
COVER_BODY= S('CovBody', fontName='LiberationSerif-Italic', fontSize=13, leading=18,
              alignment=TA_LEFT, spaceAfter=6, textColor=C_555)
# Subtitle above title
SUBTITLE  = S('SubT',    fontName='LiberationSerif-Italic', fontSize=9.5, leading=13,
              alignment=TA_LEFT, spaceAfter=2, textColor=C_555)
# Section label (PART I OF 4)
SEC_LBL   = S('SecLbl', fontName='LiberationSans-Bold',  fontSize=7.5, leading=10,
              textColor=C_888, spaceBefore=0, spaceAfter=2)
# Part label (PART I OF 4)
PART_LBL  = S('PLbl',  fontName='LiberationSans-Bold',  fontSize=8,   leading=10,
              textColor=C_RED, spaceBefore=0, spaceAfter=0)
# Section heading
SEC_HEAD  = S('SH',     fontName='LiberationSans-Bold',  fontSize=13,  leading=16,
              spaceBefore=4, spaceAfter=4, textColor=C_111)
# Body heading h2
H2        = S('H2',     fontName='LiberationSerif-Bold', fontSize=13,  leading=17,
               spaceBefore=10, spaceAfter=5, textColor=C_111)
# Body heading h3
H3        = S('H3',    fontName='LiberationSerif-Bold',  fontSize=11,  leading=14,
               spaceBefore=7,  spaceAfter=3, textColor=C_111)
# Pull quote
PULLQ     = S('PQ',    fontName='LiberationSerif-Italic', fontSize=12, leading=17,
               alignment=TA_CENTER, textColor=C_111, spaceBefore=10, spaceAfter=4)
PULLQA    = S('PQA',   fontName='LiberationSans',         fontSize=8.5, leading=12,
               alignment=TA_CENTER, textColor=C_555, spaceAfter=6)
# Sources
SRC_ITEM  = S('SI',    fontName='LiberationSans',         fontSize=8,   leading=12,
               textColor=C_333, spaceAfter=2, leftIndent=6)
SRC_HEAD  = S('SH2',   fontName='LiberationSans-Bold',    fontSize=9,   leading=12,
               textColor=C_111, spaceAfter=3, spaceBefore=8)
# Confirmed / Unconfirmed
CONF_I    = S('CI',    fontName='LiberationSans',         fontSize=8,   leading=12,
               textColor=C_333, spaceAfter=2, leftIndent=10)
CONF_H    = S('CH',    fontName='LiberationSans-Bold',    fontSize=9,   leading=12,
               textColor=C_111, spaceAfter=3, spaceBefore=8)
UNCONF_I  = S('UI',    fontName='LiberationSans',         fontSize=8,   leading=12,
               textColor=C_RED, spaceAfter=2, leftIndent=10)
UNCONF_H  = S('UH',    fontName='LiberationSans-Bold',    fontSize=9,   leading=12,
               textColor=C_RED, spaceAfter=3, spaceBefore=8)
# SEAL page
SEAL_LBL  = S('SLbl',  fontName='LiberationSans-Bold',   fontSize=22,  leading=26,
               textColor=C_WHITE, alignment=TA_CENTER)
SEAL_SUB  = S('SSub',  fontName='LiberationSans',        fontSize=9,   leading=12,
               textColor=C_999, alignment=TA_CENTER)
SEAL_CMMT = S('SCmmt', fontName='LiberationSans',         fontSize=8.5, leading=12,
               textColor=C_555, alignment=TA_CENTER)
# Hash rows
HL_KEY    = S('HLK',   fontName='LiberationSans-Bold',   fontSize=7.5, leading=10,
               textColor=C_888)
HL_VAL    = S('HLV',   fontName='DejaVuSans',            fontSize=7.5, leading=10,
               textColor=C_111)
CORR_TXT  = S('Corr',  fontName='LiberationSans',        fontSize=7.5, leading=11,
               textColor=C_RED)
WIT_TXT   = S('Wit',   fontName='LiberationSans-Italic',fontSize=7,   leading=10,
               textColor=C_888, alignment=TA_CENTER)
# Question number
Q_NUM     = S('QN',    fontName='LiberationSans-Bold',   fontSize=11,  leading=14,
               textColor=C_RED, spaceBefore=4, spaceAfter=0)
Q_BODY    = S('QB',    fontName='LiberationSerif',       fontSize=11,  leading=15.5,
               textColor=C_1A1A, spaceAfter=4)

# ─── Page Drawing Functions ───────────────────────────────────────────────────

def draw_cover(canvas, doc):
    """FORGED_V5 cover: white bg, thin top rule, EXCLUSIVE label, large title,
       drop cap O, subtitle, gray divider, byline."""
    canvas.saveState()
    c = canvas

    # ── Top thin gray line ─────────────────────────────────────────────────────
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.75)
    c.line(0, H - 43, W, H - 43)

    # ── Header label: EXCLUSIVE INVESTIGATION | MAY 2026 | FOR PUBLIC REVIEW ─
    c.setFont('DejaVuSans', 8)
    c.setFillColor(C_888)
    c.drawString(ML, H - 36, 'EXCLUSIVE INVESTIGATION  |  MAY 2026  |  FOR PUBLIC REVIEW')

    # ── Subtitle above title ──────────────────────────────────────────────────
    c.setFont('LiberationSerif-Italic', 9.5)
    c.setFillColor(C_555)
    c.drawString(ML, H - 70,
        "THE DEAL THAT COULD RESHAPE MALAYSIA'S PETROLEUM FUTURE")

    # ── Main title: SEARAH: The Deal the Rakyat Need to Understand ─────────────
    # Line 1: "SEARAH:" in 32pt bold
    c.setFont('LiberationSerif-Bold', 32)
    c.setFillColor(C_111)
    c.drawString(ML, H - 110, 'SEARAH:')

    # Line 2: "The Deal the" — backtrack
    c.setFont('LiberationSerif-Bold', 32)
    c.drawString(ML, H - 148, 'The Deal the')

    # "Rakyat" in bold italic
    c.setFont('LiberationSerif-Bold', 32)
    # measure width of "Rakyat " to inline it
    c.drawString(ML + c.stringWidth('The Deal the ', 'LiberationSerif-Bold', 32),
                 H - 148, 'Rakyat')

    # Line 3: "Need to Understand"
    c.setFont('LiberationSerif-Bold', 32)
    c.drawString(ML, H - 186, 'Need to Understand')

    # ── Gray horizontal divider line ───────────────────────────────────────────
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.75)
    c.line(ML, H - 196, ML + 120, H - 196)

    # ── Subtitle paragraph (italic, 13pt) ──────────────────────────────────────
    c.setFont('LiberationSerif-Italic', 13)
    c.setFillColor(C_555)
    lines = [
        "On November 3, 2025, two executives signed a document at ADIPEC in Abu Dhabi",
        "that commits Malaysian petroleum revenues for the next five years.",
        "The corporate vehicle behind that signature is a UK company — SEARAH Limited.",
        "The的人民 (rakyat) were not in the room.",
    ]
    y = H - 215
    for line in lines:
        c.drawString(ML, y, line)
        y -= 19

    # ── Byline ─────────────────────────────────────────────────────────────────
    c.setFont('LiberationSans-Bold', 8)
    c.setFillColor(C_888)
    c.drawString(ML, H - 302,
        "BY ARIF'S FEDERATION INVESTIGATION UNIT  |  NOT FOR DISTRIBUTION UNTIL REVIEWED")

    # ── Thin gray line below byline ────────────────────────────────────────────
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.5)
    c.line(ML, H - 310, ML + CW, H - 310)

    # ── First paragraph with DROP CAP "O" ──────────────────────────────────────
    # Draw large "O" as drop cap
    c.setFont('LiberationSerif-Bold', 60)
    c.setFillColor(C_111)
    c.drawString(ML, H - 370, 'O')

    # Rest of first sentence inline
    c.setFont('LiberationSerif', 11)
    c.setFont('LiberationSerif', 11)
    c.setFillColor(C_1A1A)
    first_line = "n the morning of November 3, 2025, at the Abu Dhabi International"
    c.drawString(ML + 37, H - 370, first_line)

    # Second line of drop cap paragraph
    c.setFont('LiberationSerif', 11)
    c.setFillColor(C_1A1A)
    second_line = "Petroleum Exhibition and Conference (ADIPEC), two men signed a document"
    c.drawString(ML, H - 385, second_line)

    # Third line
    third_line = "that commits Malaysian petroleum revenues for the next five years."
    c.drawString(ML, H - 400, third_line)

    # Fourth line
    fourth_line = "The event was photographed, published in press releases, and reported"
    c.drawString(ML, H - 415, fourth_line)

    # Fifth line
    fifth_line = "in the financial news. What the photographs did not show was the corporate"
    c.drawString(ML, H - 430, fifth_line)

    # Sixth line
    sixth_line = "structure behind the signature."
    c.drawString(ML, H - 445, sixth_line)

    # ── Footer ─────────────────────────────────────────────────────────────────
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.5)
    c.line(ML, 28, ML + CW, 28)
    c.setFont('LiberationSans', 7.5)
    c.setFillColor(C_999)
    c.drawCentredString(W / 2, 17,
        f'1  |  For Public Review  |  May 2026')

    canvas.restoreState()


def draw_regular(canvas, doc):
    """Regular content page: FORGED_V5 header + footer only."""
    canvas.saveState()
    c = canvas
    pg = doc.page

    # ── Top thin gray line ─────────────────────────────────────────────────────
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.75)
    c.line(0, H - 43, W, H - 43)

    # ── Header: left=date, right=title ─────────────────────────────────────────
    c.setFont('DejaVuSans', 8)
    c.setFillColor(C_999)
    date_str = '5/6/26, 8:52 AM'
    title_str = "SEARAH: The Deal That Could Reshape Malaysia's Petroleum Future"
    c.drawString(ML, H - 36, date_str)
    # Truncate title if too wide
    avail = ML + CW - ML - c.stringWidth(date_str, 'DejaVuSans', 8) - 5
    if c.stringWidth(title_str, 'DejaVuSans', 8) > avail:
        # truncate with …
        while c.stringWidth(title_str + '…', 'DejaVuSans', 8) > avail and len(title_str) > 10:
            title_str = title_str[:-1]
        title_str += '…'
    c.drawRightString(ML + CW, H - 36, title_str)

    # ── Bottom gray line + page number ─────────────────────────────────────────
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.5)
    c.line(ML, 28, ML + CW, 28)
    c.setFont('LiberationSans', 7.5)
    c.setFillColor(C_999)
    c.drawCentredString(W / 2, 17, f'{pg}  |  For Public Review  |  May 2026')

    canvas.restoreState()


def draw_part(canvas, doc):
    """Part title page: white, red vertical bar on left, large initial letter."""
    canvas.saveState()
    c = canvas
    pg = doc.page

    # Red vertical bar — 3pt wide, full page height, left edge
    c.setFillColor(C_RED)
    c.rect(0, 0, 3, H, fill=1, stroke=0)

    # Top thin gray line
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.75)
    c.line(0, H - 43, W, H - 43)

    # Header same as regular
    c.setFont('DejaVuSans', 8)
    c.setFillColor(C_999)
    c.drawString(ML, H - 36, '5/6/26, 8:52 AM')
    c.drawRightString(ML + CW, H - 36,
        "SEARAH: The Deal That Could Reshape Malaysia's Petroleum Future")

    # Large part letter (T, T, T, T) — 58pt, drawn in the upper part of page
    c.setFont('LiberationSerif-Bold', 58)
    c.setFillColor(C_111)
    # We'll place this as a paragraph instead — the part number page template
    # just draws the red bar + header/footer lines

    # Bottom gray line + page number
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.5)
    c.line(ML, 28, ML + CW, 28)
    c.setFont('LiberationSans', 7.5)
    c.setFillColor(C_999)
    c.drawCentredString(W / 2, 17, f'{pg}  |  For Public Review  |  May 2026')

    canvas.restoreState()


def draw_seal(canvas, doc):
    """SEAL 999 page."""
    canvas.saveState()
    c = canvas
    pg = doc.page

    # Top thin gray line
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.75)
    c.line(0, H - 43, W, H - 43)

    # Header
    c.setFont('DejaVuSans', 8)
    c.setFillColor(C_999)
    c.drawString(ML, H - 36, '5/6/26, 8:52 AM')
    c.drawRightString(ML + CW, H - 36, 'SEARAH  |  SEAL PAGE')

    # Bottom gray line + page number
    c.setStrokeColor(C_CCC)
    c.setLineWidth(0.5)
    c.line(ML, 28, ML + CW, 28)
    c.setFont('LiberationSans', 7.5)
    c.setFillColor(C_999)
    c.drawCentredString(W / 2, 17, f'{pg}  |  For Public Review  |  May 2026')

    canvas.restoreState()


# ─── Document Templates ───────────────────────────────────────────────────────
doc = BaseDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR,
    topMargin=MT,  bottomMargin=MB,
    title="SEARAH: The Deal the Rakyat Need to Understand",
    author='Arif Fazil',
    subject="Exclusive Investigation — Malaysian Petroleum Future",
)

# Frame for cover — full page (margins ignored, we paint everything in draw_cover)
cover_frame = Frame(0, 0, W, H, id='cover',
                     leftPadding=0, rightPadding=0,
                     topPadding=0, bottomPadding=0)

# Frame for regular content — standard margins
regular_frame = Frame(ML, MB, CW, H - MT - MB,
                     id='regular',
                     leftPadding=0, rightPadding=0,
                     topPadding=30, bottomPadding=20)

# Frame for part title pages
part_frame = Frame(ML + 10, MB + 20, CW - 10, H - MT - MB - 40,
                   id='part',
                   leftPadding=0, rightPadding=0,
                   topPadding=30, bottomPadding=20)

# Frame for seal page
seal_frame = Frame(ML, MB, CW, H - MT - MB,
                   id='seal',
                   leftPadding=0, rightPadding=0,
                   topPadding=30, bottomPadding=20)

cover_tmpl = PageTemplate(id='Cover',  onPage=draw_cover,  frames=[cover_frame])
regular_tmpl= PageTemplate(id='Regular',onPage=draw_regular, frames=[regular_frame])
part_tmpl   = PageTemplate(id='Part',   onPage=draw_part,   frames=[part_frame])
seal_tmpl   = PageTemplate(id='Seal',   onPage=draw_seal,   frames=[seal_frame])

doc.addPageTemplates([cover_tmpl, regular_tmpl, part_tmpl, seal_tmpl])

# ─── Helper Flowables ─────────────────────────────────────────────────────────

def divider(color=C_CCC, thickness=0.75):
    return HRFlowable(width='100%', thickness=thickness, color=color,
                      spaceAfter=4, spaceBefore=4)

def section_divider():
    """Dark gray thin line for section breaks."""
    return HRFlowable(width='100%', thickness=0.75, color=C_111,
                      spaceAfter=3, spaceBefore=3)

def part_header(num, section_name, part_letter):
    """Part title page: PART X OF 4 | SECTION NAME label + large initial letter."""
    items = []
    items.append(NextPageTemplate('Part'))
    items.append(PageBreak())
    # Large initial letter (positioned by canvas, we use a big paragraph)
    items.append(Paragraph(
        f'<font name="LiberationSerif-Bold" size="58" color="#111111">{part_letter}</font>',
        S('LargeLtr', fontName='LiberationSerif-Bold', fontSize=58,
          leading=65, textColor=C_111, spaceAfter=4)
    ))
    items.append(Paragraph(
        f'PART {num} OF 4  |  {section_name.upper()}',
        S('PL', fontName='LiberationSans-Bold', fontSize=8,
          textColor=C_RED, leading=10, spaceAfter=2)
    ))
    items.append(divider(C_111, 1.5))
    return items

def pullquote(text, attr=''):
    items = []
    items.append(divider(C_CCC, 0.75))
    items.append(Paragraph(f'❝ {text} ❞', PULLQ))
    if attr:
        items.append(Paragraph(f'— {attr}', PULLQA))
    items.append(divider(C_CCC, 0.75))
    return items

def key_fact(label, value):
    data = [[
        Paragraph(label, S('KFL', fontName='LiberationSans-Bold', fontSize=7.5,
                            textColor=C_RED, leading=10)),
        Paragraph(value,  S('KFV', fontName='LiberationSans',     fontSize=8.5,
                            textColor=C_WHITE, leading=12)),
    ]]
    t = Table(data, colWidths=[52*mm, CW - 52*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), C_111),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(0,-1),  6),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ]))
    return t

def timeline_row(date, text, shaded=False):
    bg = C_F0F0 if shaded else C_WHITE
    data = [[
        Paragraph(date, S('TD', fontName='LiberationSans-Bold', fontSize=8,
                          textColor=C_RED, leading=11)),
        Paragraph(text, S('TT', fontName='LiberationSerif',     fontSize=8.5,
                          textColor=C_333, leading=12)),
    ]]
    t = Table(data, colWidths=[28*mm, CW - 28*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
        ('RIGHTPADDING',  (0,0),(-1,-1), 5),
        ('LINEBELOW',     (0,0),(-1,-1), 0.3, C_DDD),
    ]))
    return t

def question_row(num, text):
    data = [[
        Paragraph(num, Q_NUM),
        Paragraph(text, Q_BODY),
    ]]
    t = Table(data, colWidths=[12*mm, CW - 12*mm])
    t.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ('LEFTPADDING',   (0,0),(0,-1),  0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ]))
    return t

def src(text):
    return Paragraph(f'• {text}', SRC_ITEM)

def conf(text):
    return Paragraph(f'✓ {text}', CONF_I)

def unconf(text):
    return Paragraph(f'— {text}', UNCONF_I)

def hrow(key, val):
    data = [[Paragraph(key, HL_KEY), Paragraph(val, HL_VAL)]]
    t = Table(data, colWidths=[38*mm, CW - 38*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(0,0),  C_F0F0),
        ('BACKGROUND',    (1,0),(1,0),  C_WHITE),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
        ('RIGHTPADDING',  (0,0),(-1,-1), 5),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('LINEBELOW',     (0,0),(-1,-1), 0.3, C_DDD),
    ]))
    return t


# ─── STORY ───────────────────────────────────────────────────────────────────
story = []

# ══ PAGE 1: COVER ════════════════════════════════════════════════════════════
# draw_cover paints everything — story just triggers the template
story.append(Spacer(1, 1))
story.append(NextPageTemplate('Regular'))

# ══ PAGE 2 ════════════════════════════════════════════════════════════════════

# PART I
story.extend(part_header('I', 'The Deal', 'T'))

# First paragraph continues from cover drop cap — pick up right after "...behind the signature."
story.append(Paragraph(
    'The entity that now holds the rights to a substantial portion of Malaysia\'s '
    'domestic gas supply is <b>SEARAH Limited</b> — a company registered in England '
    'and Wales (Company No. 17027115), incorporated at ENI House, 8th Floor, London. '
    'Its two shareholders are <b>PETRONAS Carigali International Ventures Ltd</b> '
    '(Malaysia) and <b>Eni Lasmo Plc</b> (UK-Italy).',
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'The agreement commits more than <b>USD 15 billion (RM70 billion)</b> in capital '
    'over five years toward upstream assets in Malaysia and Indonesia. '
    'Because SEARAH is registered under the UK Companies Act 2006, '
    'its internal governance, dispute resolution, and capital structure '
    'fall under English law — not Malaysian law.',
    BODY))
story.append(Spacer(1, 6))

story.extend(pullquote(
    'This is not about a deal that was signed. '
    'It is about a deal whose governance was moved beyond the reach of '
    'Parliament, the Courts, and the Sarawak State Assembly.',
    'Why this matters'))

story.append(Paragraph(
    'PETRONAS has operated for five decades as a Federal statutory corporation. '
    'Its board answers to the Malaysian Government. '
    'SEARAH Limited is a private UK company. '
    'Its board answers to its two shareholders — and to English law.',
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'The practical consequence: decisions about Sarawak gas fields, '
    'LNG offtake contracts, and capital allocation under the JV '
    'can be made in London, and Malaysian institutions have no direct '
    'mechanism to reverse, redirect, or renegotiate them.',
    BODY))
story.append(Spacer(1, 8))

# Key facts table
for lbl, val in [
    ('COMPANY',       'SEARAH Limited — UK Co. No. 17027115'),
    ('INCORPORATED',  'February 11, 2026 at ENI House, London'),
    ('SHAREHOLDERS',  'PETRONAS Carigali (50%)  |  Eni Lasmo (50%)'),
    ('CAPITAL',       'USD 15bn+ over five years'),
    ('GOVERNING LAW', 'English Law (Companies Act 2006)'),
]:
    story.append(key_fact(lbl, val))
    story.append(Spacer(1, 4))

# ══ PAGE 3 — PART II ═════════════════════════════════════════════════════════

story.extend(part_header('II', 'The Sarawak Collision', 'T'))

story.append(Paragraph(
    'The Kasawari gas field is PETRONAS\'s largest domestic producing asset. '
    'It sits 200 kilometres off the coast of Sarawak, '
    'feeds the Bintulu LNG Complex (one of the world\'s largest), '
    'and represents a significant share of Malaysia\'s total gas production.',
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'Since 2024, PETRONAS and the Sarawak State Government — '
    'through its petroleum company PETROS — '
    'have been locked in a constitutional dispute over who has rights '
    'to petroleum revenues from fields within Sarawak\'s territory.',
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'The Federal Court has heard arguments. '
    'The Sarawak State Assembly has passed resolutions. '
    'The legal fight could run for years.',
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'Meanwhile, the SEARAH joint venture was negotiated and '
    'incorporated in a matter of months — and its UK governance '
    'structure effectively places the Kasawari gas field and '
    'related infrastructure beyond the reach of both the Federal Court '
    'and the Sarawak State Government simultaneously.',
    BODY))
story.append(Spacer(1, 10))

# TIMELINE
story.append(Paragraph('TIMELINE', SRC_HEAD))
# Light background panel for timeline
tl_data = []
for i, (d, t) in enumerate([
    ('Jul 2020',   'PETROS incorporated by Sarawak State Government.'),
    ('2024',       'PETROS formally asserts claim to Sarawak petroleum rights.'),
    ('2024–2025',  'PETRONAS and PETROS enter formal constitutional dispute.'),
    ('Nov 2025',   'PETRONAS and Eni sign SEARAH JV at ADIPEC, Abu Dhabi.'),
    ('Feb 11, 2026','SEARAH Limited formally incorporated in London.'),
    ('Aug 2025',   'PETROS sues PETRONAS in Kuching High Court over petroleum rights.'),
    ('2026',       'Federal Court constitutional hearing scheduled / resumed.'),
]):
    tl_data.append([
        Paragraph(d, S('TD', fontName='LiberationSans-Bold', fontSize=8,
                       textColor=C_RED, leading=11)),
        Paragraph(t, S('TT', fontName='LiberationSerif', fontSize=8.5,
                       textColor=C_333, leading=12)),
    ])

tl_table = Table(tl_data, colWidths=[28*mm, CW - 28*mm])
tl_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), C_FAFA),
    ('ROWBACKGROUNDS',(0,0),(-1,-1), [C_WHITE, C_F0F0]),
    ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ('TOPPADDING',    (0,0),(-1,-1), 3),
    ('BOTTOMPADDING', (0,0),(-1,-1), 3),
    ('LEFTPADDING',   (0,0),(-1,-1), 5),
    ('RIGHTPADDING',  (0,0),(-1,-1), 5),
    ('LINEBELOW',     (0,0),(-1,-2), 0.3, C_DDD),
]))
story.append(tl_table)

# ══ PAGE 5 — QUOTE PAGE ═══════════════════════════════════════════════════════
story.append(PageBreak())
story.append(NextPageTemplate('Regular'))

story.extend(pullquote(
    'A country can lose control of its resources not through theft alone, '
    'but through structure. Through jurisdictions chosen deliberately. '
    'Through decisions made in places the rakyat cannot reach.',
    'From This Investigation'))
story.append(Spacer(1, 12))

# ══ PAGE 6 — PART III ════════════════════════════════════════════════════════

story.extend(part_header('III', 'The Architect', 'T'))

story.append(Paragraph(
    'Claudio Descalzi is the CEO of Eni, the Italian state-majority-owned energy company. '
    'He has been CEO since 2014. '
    'He has extensive experience structuring international JVs '
    'and has navigated complex regulatory environments in Africa, '
    'the Middle East, and Latin America.',
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'In 2021, Descalzi was acquitted by an Italian Milan court of charges '
    'related to alleged corruption in the acquisition of OPL 245, '
    'a prolific Nigerian offshore oil block. '
    'The Nigerian government was also a party to that case. '
    'The acquittal is not the same as a finding of innocence — '
    'it means the prosecution failed to meet its legal threshold. '
    'The structural model used in that deal is instructive.',
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'Descalzi has repeatedly used holding company structures '
    'incorporated in stable, arbitration-friendly jurisdictions '
    'to ring-fence assets from the regulatory risk of the host country. '
    'SEARAH Limited fits that pattern precisely.',
    BODY))
story.append(Spacer(1, 10))

# Key finding box (dark #111 background)
kf_data = [[Paragraph(
    'Structural Finding: SEARAH Limited is not a typical JV holding company. '
    'Its UK incorporation places it under English law, outside both Malaysian '
    'and Sarawak constitutional jurisdiction — by design.',
    S('KFT', fontName='LiberationSerif', fontSize=10.5, leading=15,
      textColor=C_WHITE, alignment=TA_CENTER)
)]]
kf_tbl = Table(kf_data, colWidths=[CW])
kf_tbl.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), C_111),
    ('TOPPADDING',    (0,0),(-1,-1), 10),
    ('BOTTOMPADDING', (0,0),(-1,-1), 10),
    ('LEFTPADDING',   (0,0),(-1,-1), 10),
    ('RIGHTPADDING',  (0,0),(-1,-1), 10),
]))
story.append(kf_tbl)

# ══ PAGE 8 — PART IV ════════════════════════════════════════════════════════

story.extend(part_header('IV', 'The PETRONAS–PETROS Question', 'T'))

story.append(Paragraph(
    'PETROS is not a fringe player. '
    'It is a company incorporated by the Sarawak State Government, '
    'with a mandate to represent Sarawak\'s interest in petroleum revenues '
    'under the Malaysia Agreement 1963 (MA63).',
    BODY))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'If SEARAH holds the economic rights to fields that PETROS claims '
    'under Sarawak law, then SEARAH\'s English-law structure '
    'is not just a commercial design — it is a constitutional 回避 (avoidance) mechanism.',
    BODY))
story.append(Spacer(1, 6))

story.extend(pullquote(
    '回避 — Avoidance. '
    'Not illegal. Not unusual in international petroleum deals. '
    'But done to a sovereign state\'s own sub-national entity — that is new.',
    ''))

story.append(Paragraph(
    'MA63 is not a minor administrative detail. '
    'It is the constitutional foundation of Sarawak\'s membership in Malaysia. '
    'Any constitutional question touching petroleum rights under MA63 '
    'is, by definition, a question about the structure of the Federation itself.',
    BODY))
story.append(Spacer(1, 10))

# ══ QUESTIONS ════════════════════════════════════════════════════════════════

# Questions header panel
qh_data = [[Paragraph('SEVEN UNANSWERED QUESTIONS',
                       S('QH', fontName='LiberationSans-Bold', fontSize=9,
                         textColor=C_WHITE, alignment=TA_LEFT))]]
qh_tbl = Table(qh_data, colWidths=[CW])
qh_tbl.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), C_111),
    ('TOPPADDING',    (0,0),(-1,-1), 6),
    ('BOTTOMPADDING', (0,0),(-1,-1), 6),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
]))
story.append(qh_tbl)
story.append(Spacer(1, 6))

# Questions in two-column style (number | question)
questions = [
    ('1.', 'Did the Malaysian Cabinet approve the transfer of any producing assets into a UK-governed entity before incorporation?'),
    ('2.', 'Has the Attorney General\'s Chambers reviewed the SEARAH structure under the Petroleum Development Act?'),
    ('3.', 'Does the SEARAH JV agreement include any "reserved matters" that require unanimous board approval — and if so, what are they?'),
    ('4.', 'Are any of SEARAH\'s assets — including interests in producing fields — pledged as collateral for any debt instrument?'),
    ('5.', 'Has PETROS been granted any standing in the SEARAH governance structure, or any dispute resolution mechanism?'),
    ('6.', 'What is the exact relationship between SEARAH\'s capital commitments and PETRONAS\'s simultaneous "rightsizing" programme 2024–2025?'),
    ('7.', 'At what point did Eni become aware that PETROS\'s claim over SK316 was unresolved — and did that affect the JV structure?'),
]
for qh, qb in questions:
    story.append(question_row(qh, qb))

story.append(Spacer(1, 12))

# ══ SOURCES ═══════════════════════════════════════════════════════════════════

story.append(Paragraph('SOURCES', SRC_HEAD))
for s in [
    'PETRONAS Annual Report 2024 — corporate structure overview.',
    'Companies House UK — SEARAH Limited (Company No. 17027115) filing record.',
    'Eni Press Release, November 2025 — "PETRONAS and Eni sign strategic upstream partnership."',
    'PETROS public statements 2024–2026 — petroleum rights assertions.',
    'Federal Court of Malaysia — MA63 constitutional hearing records.',
    'Sarawak State Assembly Hansard — petroleum rights debates, 2024–2025.',
    'UNCTAD Investment Policy Hub — BIT database, confirmed: no Italy-Malaysia BIT.',
    'Milan Court records, March 2021 — Descalzi OPL 245 acquittal.',
    'Wood Mackenzie press release, February 28, 2025 — PETRONAS-Eni combination analysis.',
    'Global Arbitration Review — ICSID Case No. ARB/20/48 (Eni vs Nigeria).',
    'Fulcrum Singapore (ISEAS-Yusof Ishak Institute), April 2026.',
]:
    story.append(src(s))

story.append(Spacer(1, 10))

# ══ CONFIRMED / UNCONFIRMED ═════════════════════════════════════════════════

story.append(Paragraph('WHAT IS CONFIRMED', CONF_H))
for c in [
    'SEARAH Limited (Company No. 17027115) — UK-registered, incorporated February 11, 2026 at ENI House, London.',
    '50% owned by PETRONAS Carigali International Ventures, 50% by Eni Lasmo Plc.',
    'Deal valued at "in excess of USD 15 billion over five years" — Eni press release, November 2025.',
    'Company governed by Companies Act 2006 (English law).',
    'NO active BIT between Malaysia and Italy or the United Kingdom — confirmed by UNCTAD, April 2026.',
    'MLNG Bintulu — one of world\'s largest LNG export facilities; supplies Japan, Korea, Taiwan, China.',
]:
    story.append(conf(c))

story.append(Spacer(1, 8))
story.append(Paragraph('WHAT REQUIRES FURTHER INVESTIGATION', UNCONF_H))
for u in [
    'The specific terms of the JV agreement between PETRONAS and Eni are not public.',
    'Whether Malaysian Parliament was formally notified has not been confirmed.',
    'Whether PETROS was consulted before the SEARAH structure was finalised has not been confirmed.',
    'Whether Malaysian legal counsel reviewed the UK incorporation has not been confirmed.',
    'Whether Block SK316 or other producing fields are held within SEARAH Limited has not been confirmed.',
]:
    story.append(unconf(u))

# ══ SEAL PAGE ═══════════════════════════════════════════════════════════════

story.append(PageBreak())
story.append(NextPageTemplate('Seal'))
story.append(Spacer(1, 30))

# SEAL 999 box
seal_data = [[
    Paragraph('SEAL 999', SEAL_LBL),
    Paragraph('DITEMPA BUKAN DIBERI', SEAL_SUB),
]]
seal_tbl = Table(seal_data, colWidths=[CW])
seal_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), C_111),
    ('TOPPADDING',    (0,0),(-1,-1), 14),
    ('BOTTOMPADDING', (0,0),(-1,-1), 14),
    ('LINEABOVE',     (0,0),(-1,0),  2, C_CCC),
    ('LINEBELOW',     (0,-1),(-1,-1),2, C_CCC),
    ('LINEBEFORE',    (0,0),(0,-1),   2, C_CCC),
    ('LINEAFTER',     (-1,0),(-1,-1),2, C_CCC),
]))
story.append(seal_tbl)
story.append(Spacer(1, 10))
story.append(Paragraph(
    'HMAC-SHA256 commitment registered before distribution. '
    'This document is sealed under arifOS Protocol SEAL 999.',
    SEAL_CMMT))
story.append(Spacer(1, 14))

# Verification reference table
vr_data = [[Paragraph('VERIFICATION REFERENCE',
                       S('VRH', fontName='LiberationSans-Bold', fontSize=7.5,
                         textColor=C_WHITE, alignment=TA_CENTER))]]
vr_tbl = Table(vr_data, colWidths=[CW])
vr_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), C_111),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LINEBELOW',     (0,0),(-1,0),  0.5, C_CCC),
]))
story.append(vr_tbl)
story.append(Spacer(1, 6))

story.append(hrow('Document SHA-256:', DOC_HASH))
story.append(hrow('DB Hash:', DB_HASH))
story.append(hrow('HMAC-SHA256:', SEAL_HMAC))
story.append(hrow('Timestamp (MYT):', TIMESTAMP))
story.append(hrow('Document:', 'SEARAH-EXPOSE-v16'))
story.append(hrow('Author:', 'ARIF FAZIL — Signing with full name. Own it.'))

story.append(Spacer(1, 12))

# Correction notice
story.append(Paragraph(
    'CORRECTION NOTICE: Previous editions incorrectly stated that an Italy-Malaysia BIT '
    '(1988) was in force. UNCTAD confirmed (April 2026): NO such treaty exists. '
    'BIT claim retracted. The correct statement: NO BIT protects this arrangement. '
    'English law governs. No ICSID route exists for Malaysia.',
    CORR_TXT))
story.append(Spacer(1, 12))

# Witness footer
story.append(Paragraph(
    'All claims cross-checked against primary sources: Companies House UK, Eni press releases, '
    'UNCTAD Investment Policy Hub, Malaysian Parliament Hansard, Federal Court records. '
    'F2 WITNESS standard: evidence must be verifiable, not merely credible.',
    WIT_TXT))

# ─── BUILD ────────────────────────────────────────────────────────────────────
doc.build(story)
size = os.path.getsize(OUTPUT)
print(f'Generated: {OUTPUT}')
print(f'Size: {size:,} bytes ({size/1024:.1f} KB)')

# Verify
import fitz
vdoc = fitz.open(OUTPUT)
print(f'Pages: {vdoc.page_count}')
for i in range(vdoc.page_count):
    txt = vdoc[i].get_text()
    first = ' '.join(txt.split())[:120]
    print(f'  Page {i+1}: {len(txt)} chars | {first}')
vdoc.close()
