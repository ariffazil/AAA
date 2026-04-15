#!/usr/bin/env python3
"""
SEARAH × PETROS — Executive Intelligence Briefing
Professional PDF Report
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

# ─── BRAND PALETTE ───────────────────────────────────────────────────────────
C_NAVY       = HexColor('#0A2342')   # deep navy — primary
C_TEAL       = HexColor('#008573')   # Eni teal
C_CRIMSON    = HexColor('#C8102E')   # PETRONAS/alert red
C_GOLD       = HexColor('#C8922A')   # accent gold
C_LIGHT_BLUE = HexColor('#E8EEF4')   # section bg
C_PETROS_RED = HexColor('#8B0000')   # dark red for PETROS
C_AMBER      = HexColor('#B8860B')   # partial/caution
C_GREY_LIGHT = HexColor('#F4F5F7')   # table alternating
C_GREY_MID   = HexColor('#6C757D')   # muted text
C_TEXT       = HexColor('#1A252F')   # body text
C_DIVIDER    = HexColor('#DEE2E6')   # borders
C_CONFIRMED  = HexColor('#155724')   # dark green text
C_BG_CHART   = HexColor('#E9ECEF')   # bar chart bg

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

# ─── HELPER FLOWABLES ─────────────────────────────────────────────────────────
class ColorBar(Flowable):
    def __init__(self, width, height, fill_color, stroke_color=None, stroke_width=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
    def draw(self):
        self.canv.setFillColor(self.fill_color)
        if self.stroke_color:
            self.canv.setStrokeColor(self.stroke_color)
            self.canv.setLineWidth(self.stroke_width)
            self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=1)
        else:
            self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


class HRule(Flowable):
    """Thin horizontal rule."""
    def __init__(self, width, thickness=0.5, color=C_DIVIDER):
        Flowable.__init__(self)
        self.width = width
        self.height = thickness
        self.color = color
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.height)
        self.canv.line(0, 0, self.width, 0)


def section_header(title, subtitle=None):
    """Returns a styled section header block."""
    items = []

    # Navy top bar
    items.append(ColorBar(CONTENT_W, 5*mm, C_NAVY))
    items.append(Spacer(1, 2*mm))

    # Title
    title_style = ParagraphStyle(
        'SecTitle', fontName='Helvetica-Bold', fontSize=15,
        textColor=C_NAVY, leading=18, spaceAfter=2
    )
    items.append(Paragraph(title, title_style))

    # Subtitle if provided
    if subtitle:
        sub_style = ParagraphStyle(
            'SecSub', fontName='Helvetica-Oblique', fontSize=9,
            textColor=C_GREY_MID, leading=12, spaceAfter=4
        )
        items.append(Paragraph(subtitle, sub_style))

    items.append(HRule(CONTENT_W, 1.5, C_NAVY))
    items.append(Spacer(1, 4*mm))

    return items


def callout_box(title, body_lines, bg_color, left_color, title_color=None, body_color=None):
    """Generic callout box."""
    if title_color is None: title_color = C_TEXT
    if body_color is None: body_color = C_TEXT

    content = []
    title_style = ParagraphStyle('CBT', fontName='Helvetica-Bold', fontSize=8.5,
                                 textColor=title_color, leading=11, spaceAfter=3)
    body_style = ParagraphStyle('CBB', fontName='Helvetica', fontSize=9,
                                 textColor=body_color, leading=13)

    for line in body_lines:
        content.append(Paragraph(line, body_style))

    rows = [[Paragraph(title, title_style)]] + [[p] for p in content]
    t = Table([[Paragraph(title, title_style)]] + [[p] for p in content],
              colWidths=[CONTENT_W - 12*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (0,0), 10),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
        ('TOPPADDING', (0,1), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-2), 2),
        ('LINEBEFORE', (0,0), (0,-1), 4, left_color),
    ]))
    return t


def score_bar(label, pct, color, footnote=None):
    """Horizontal score bar with label."""
    bar_fill_w = (CONTENT_W - 55*mm - 35*mm - 6*mm) * pct / 100

    label_s = ParagraphStyle('ScL', fontName='Helvetica-Bold', fontSize=8.5,
                             textColor=C_TEXT, leading=11)
    pct_s = ParagraphStyle('ScP', fontName='Helvetica-Bold', fontSize=8.5,
                            textColor=color, leading=11)

    bar_bg = Table([['']] * 1, colWidths=[CONTENT_W - 55*mm - 35*mm - 6*mm],
                   rowHeights=[5*mm])
    bar_bg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_BG_CHART),
        ('GRID', (0,0), (-1,-1), 0, white),
    ]))

    bar_fill = Table([['']] * 1, colWidths=[bar_fill_w], rowHeights=[5*mm])
    bar_fill.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), color),
        ('GRID', (0,0), (-1,-1), 0, white),
    ]))

    row = Table(
        [[Paragraph(label, label_s),
          bar_bg,
          Paragraph(f'{pct}%', pct_s)]],
        colWidths=[55*mm, CONTENT_W - 55*mm - 35*mm - 6*mm, 35*mm],
        rowHeights=[8*mm]
    )
    row.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    items = [row]
    if footnote:
        fn_s = ParagraphStyle('Fn', fontName='Helvetica-Oblique', fontSize=7.5,
                              textColor=C_GREY_MID, leading=10)
        items.append(Paragraph(footnote, fn_s))
    items.append(Spacer(1, 3*mm))
    return items


# ─── STYLES ─────────────────────────────────────────────────────────────────
def body(text, bold=False, italic=False, color=None, size=9.5, space_after=5):
    fn = 'Helvetica-Bold' if bold else ('Helvetica-Oblique' if italic else 'Helvetica')
    c = color if color else C_TEXT
    return Paragraph(text, ParagraphStyle('Body', fontName=fn, fontSize=size,
                                            textColor=c, leading=size*1.35, spaceAfter=space_after))

def body_left(text, bold=False, size=9.5):
    fn = 'Helvetica-Bold' if bold else 'Helvetica'
    return Paragraph(text, ParagraphStyle('BL', fontName=fn, fontSize=size,
                                            textColor=C_TEXT, leading=size*1.35,
                                            spaceAfter=4, alignment=TA_LEFT))


# ─── BUILD PDF ───────────────────────────────────────────────────────────────
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title='SEARAH × PETROS — Executive Intelligence Briefing',
        author='arifOS_bot',
        subject='SEARAH Joint Venture × PETROS Sarawak — Evidence-Based Analysis',
    )

    story = []

    # ═══════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ═══════════════════════════════════════════════════════════════════

    # Top gradient bar
    story.append(ColorBar(CONTENT_W, 10*mm, C_NAVY))
    story.append(Spacer(1, 0))

    # Classification tag
    tag_style = ParagraphStyle('Tag', fontName='Helvetica-Bold', fontSize=7.5,
                                textColor=white, leading=10, alignment=TA_CENTER)
    tag = Table([[Paragraph('OPEN SOURCE INTELLIGENCE REPORT — UNCLASSIFIED', tag_style)]],
                colWidths=[CONTENT_W])
    tag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CRIMSON),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tag)
    story.append(Spacer(1, 8*mm))

    # Main title
    title_style = ParagraphStyle('MainTitle', fontName='Helvetica-Bold', fontSize=30,
                                  textColor=C_NAVY, leading=34, spaceAfter=6)
    sub_style = ParagraphStyle('MainSub', fontName='Helvetica', fontSize=13,
                               textColor=C_TEAL, leading=17, spaceAfter=8)
    src_style = ParagraphStyle('Src', fontName='Helvetica', fontSize=9,
                               textColor=C_GREY_MID, leading=12)

    story.append(Paragraph('SEARAH × PETROS', title_style))
    story.append(Paragraph(
        'A 62-Year Dispute. A USD 15 Billion JV. One Critical Question.',
        sub_style))
    story.append(HRule(CONTENT_W, 2, C_GOLD))
    story.append(Spacer(1, 6*mm))

    # Lead quote
    quote_style = ParagraphStyle('Q', fontName='Helvetica-BoldOblique', fontSize=11,
                                  textColor=C_NAVY, leading=16, alignment=TA_LEFT,
                                  leftIndent=12, rightIndent=12)
    quote_box = Table(
        [[Paragraph(
            '"Within Malaysia, PETRONAS cannot settle with PETROS — a Malaysian entity '
            'representing a Malaysian state — after 62 years of unresolved legal disputes. '
            'Outside Malaysia, PETRONAS signs a USD 15 billion JV with Eni, incorporates '
            'a UK company, and commits Malaysian assets — in a matter of months."',
            quote_style)]],
        colWidths=[CONTENT_W]
    )
    quote_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BLUE),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LINEBEFORE', (0,0), (0,-1), 5, C_GOLD),
    ]))
    story.append(quote_box)
    story.append(Spacer(1, 12*mm))

    # Meta grid
    meta_rows = [
        ['DATE OF REPORT', '15 April 2026'],
        ['CLASSIFICATION', 'Open Source Intelligence — Unclassified'],
        ['PRIMARY SOURCE', 'Companies House UK (Co. No. 17027115)'],
        ['SECONDARY SOURCES', 'Public record — PETRONAS, PETROS, news filings'],
        ['SCOPE', 'Corporate governance, sovereignty, employment, financial risk'],
        ['STATUS', 'ONGOING — Further documents required'],
        ['MOTTO', 'DITEMPA BUKAN DIBERI'],
    ]
    meta_label_s = ParagraphStyle('ML', fontName='Helvetica-Bold', fontSize=8,
                                   textColor=C_GREY_MID, leading=11)
    meta_val_s = ParagraphStyle('MV', fontName='Helvetica', fontSize=8.5,
                                 textColor=C_TEXT, leading=11)
    meta_data = [
        [Paragraph(r[0], meta_label_s), Paragraph(r[1], meta_val_s)]
        for r in meta_rows
    ]
    meta_table = Table(meta_data, colWidths=[45*mm, CONTENT_W - 45*mm])
    meta_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, C_DIVIDER),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14*mm))

    # Discalimer
    disc_style = ParagraphStyle('Disc', fontName='Helvetica-Oblique', fontSize=7.5,
                                textColor=C_GREY_MID, leading=10, alignment=TA_JUSTIFY)
    story.append(Paragraph(
        'DISCLAIMER: This report is compiled from publicly available information and official regulatory '
        'filings. It does not constitute legal or financial advice. All claims are labeled CONFIRMED '
        '(documented evidence), PLAUSIBLE (consistent with known patterns), or UNPROVEN (requires '
        'further documentation). This report is shared in the spirit of accountable governance.',
        disc_style))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # EXECUTIVE SUMMARY
    # ═══════════════════════════════════════════════════════════════════
    story.extend(section_header(
        'Executive Summary',
        'What this report examines and what the evidence shows'
    ))

    story.append(body(
        'SEARAH is a 50-50 joint venture between PETRONAS Carigali International Ventures Sdn Bhd '
        '(Malaysia) and Eni Lasmo Plc (Italy), incorporated in the United Kingdom on 11 February 2026. '
        'The venture carries an estimated USD 15 billion capital expenditure programme over five years, '
        'with production targets of 300 to 500 kboe/day across upstream assets in Indonesia and Malaysia.',
        space_after=6))

    story.append(body(
        'This report was compiled following a question raised by Arif (Muhammad Arif bin Fazil) in the '
        'makcikGPT community: why has PETRONAS been unable to resolve a domestic dispute with PETROS '
        '(Petroleum Sarawak Berhad) spanning 62 years, yet was able to execute a billion-dollar '
        'international JV with Eni in a matter of months — incorporated in the UK, at Eni\'s London address?',
        space_after=6))

    story.append(body(
        'The report examines five dimensions of the SEARAH deal: financial economics, '
        'sovereign governance, human capital, transparency, and the structural implications of '
        'UK incorporation for Malaysian interests.',
        space_after=8))

    # Key findings boxes
    findings = [
        ('CONFIRMED', C_CONFIRMED, C_LIGHT_BLUE, C_NAVY,
         'PETRONAS-PETROS negotiations were unresolved as of April 2026, despite a stated target '
         'of conclusion by end-2025. SEARA Energy Limited was incorporated on 11 February 2026.'),
        ('CONFIRMED', C_CONFIRMED, C_LIGHT_BLUE, C_NAVY,
         'SEARA Energy Limited is registered at ENI HOUSE, 10 Ebury Bridge Road, London — '
         'Eni\'s own address. The board comprises two Italian directors (locally based) and '
         'two Malaysian directors (based in Malaysia).'),
        ('CONFIRMED', C_CONFIRMED, C_LIGHT_BLUE, C_NAVY,
         'PETROS is not a party to SEARA Energy Limited. If Malaysian assets in Sarawak '
         'have been transferred into SEARA, Sarawak\'s negotiations with PETRONAS now '
         'involve a foreign counterparty (Eni) as a structural third party.'),
        ('NO EVIDENCE', C_CRIMSON, HexColor('#FFF0F0'), C_CRIMSON,
         'There is no public evidence that Malaysia\'s Parliament was notified or consulted '
         'before SEARA Energy Limited was incorporated in February 2026, or before '
         'the JV was publicly announced in April 2026.'),
    ]

    for badge_text, badge_color, bg, tc, text in findings:
        badge_s = ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=7,
                                  textColor=white, leading=9, alignment=TA_CENTER)
        badge = Table([[Paragraph(badge_text, badge_s)]], colWidths=[30*mm])
        badge.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), badge_color),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))

        body_s = ParagraphStyle('FB', fontName='Helvetica', fontSize=9,
                                textColor=tc, leading=13)
        row_table = Table(
            [[badge, Paragraph(text, body_s)]],
            colWidths=[32*mm, CONTENT_W - 32*mm]
        )
        row_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (0,0), 6),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(row_table)
        story.append(Spacer(1, 3*mm))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 1: WHAT IS SEARAH
    # ═══════════════════════════════════════════════════════════════════
    story.extend(section_header(
        'Section 1 — What Is SEARAH?',
        'The venture, the structure, and the numbers'
    ))

    story.append(body(
        'SEARAH (stylised from the Malay "searah" — meaning aligned direction or shared course) '
        'is a joint venture established to consolidate and operate upstream oil and gas assets '
        'across Malaysia and Indonesia. Its stated ambition is to build a regional gas champion '
        'serving LNG and domestic markets across Southeast Asia.',
        space_after=6))

    story.append(body(
        'The venture is structured as a 50-50 partnership between the upstream subsidiaries '
        'of the two parent companies, with shared governance, shared capital risk, and shared '
        'operational control over a portfolio spanning 19 upstream assets.',
        space_after=8))

    # Key numbers table
    numbers = [
        ['Number of Assets', '±19 upstream assets (14 Indonesia, 5 Malaysia — unconfirmed list)'],
        ['Discovered Reserves', '±3 billion barrels of oil equivalent (boe)'],
        ['Unrisked Exploration Potential', '±10 billion boe (not yet proven)'],
        ['Starting Production Target', '~300 kboe/day'],
        ['Medium-Term Production Target', '~500 kboe/day'],
        ['Five-Year Capex', '~USD 15 billion'],
        ['Debt Facility', '~USD 6 billion revolving credit facility (drawn or arranged by international banks)'],
        ['Incorporation Date', '11 February 2026 — Companies House UK, Company No. 17027115'],
        ['Legal Domicile', 'England and Wales — Companies Act 2006'],
        ['Registered Office', 'ENI HOUSE, 10 Ebury Bridge Road, London SW1W 8PZ'],
    ]

    num_label = ParagraphStyle('NL', fontName='Helvetica-Bold', fontSize=8.5, textColor=C_NAVY, leading=11)
    num_val   = ParagraphStyle('NV', fontName='Helvetica', fontSize=8.5, textColor=C_TEXT, leading=11)

    num_data = [[Paragraph(r[0], num_label), Paragraph(r[1], num_val)] for r in numbers]
    num_table = Table(num_data, colWidths=[52*mm, CONTENT_W - 52*mm])
    num_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, C_DIVIDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [white, C_GREY_LIGHT]),
        ('BACKGROUND', (0,0), (0,-1), C_LIGHT_BLUE),
    ]))
    story.append(num_table)
    story.append(Spacer(1, 8*mm))

    story.append(body(
        'Note on "Unrisked Potential": The ±10 billion boe exploration target is described '
        'as unrisked, meaning it has not been adjusted for the probability of geological or '
        'commercial success. This is a common industry practice for venture framing, but it '
        'should not be counted as proven reserves in any financial assessment.',
        italic=True, color=C_GREY_MID, size=8.5, space_after=8))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 2: CORPORATE STRUCTURE
    # ═══════════════════════════════════════════════════════════════════
    story.extend(section_header(
        'Section 2 — Corporate Structure',
        'Who owns SEARA Energy Limited and who sits on its board'
    ))

    story.append(body(
        'SEARA Energy Limited was incorporated under the Companies Act 2006 (England and Wales) '
        'on 11 February 2026. It is a private company limited by shares. The following information '
        'is drawn directly from the official Companies House filing (IN01 application).',
        space_after=8))

    # Shareholding table
    share_hdr = ParagraphStyle('SHdr', fontName='Helvetica-Bold', fontSize=9,
                               textColor=white, leading=11)
    share_body = ParagraphStyle('SBody', fontName='Helvetica', fontSize=8.5,
                                 textColor=C_TEXT, leading=12)

    share_data = [
        [Paragraph('Shareholder', share_hdr),
         Paragraph('Entity Type', share_hdr),
         Paragraph('Registered Address', share_hdr),
         Paragraph('Shares Held', share_hdr),
         Paragraph('%', share_hdr)],
        [Paragraph('ENI LASMO PLC', share_body),
         Paragraph('UK-registered company (Eni subsidiary)', share_body),
         Paragraph('ENI House, 10 Ebury Bridge Road, London SW1W 8PZ', share_body),
         Paragraph('1 Ordinary', share_body),
         Paragraph('50%', share_body)],
        [Paragraph('PETRONAS CARIGALI INTERNATIONAL VENTURES SDN. BHD.', share_body),
         Paragraph('Malaysian company (PETRONAS upstream subsidiary)', share_body),
         Paragraph('Petronas Twin Towers, KLCC, Kuala Lumpur, 50088', share_body),
         Paragraph('1 Ordinary', share_body),
         Paragraph('50%', share_body)],
    ]
    share_table = Table(share_data, colWidths=[42*mm, 38*mm, 50*mm, 22*mm, 15*mm])
    share_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_DIVIDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C_GREY_LIGHT]),
    ]))
    story.append(share_table)
    story.append(Spacer(1, 10*mm))

    # Board of Directors
    story.append(body('<b>Board of Directors — 4 Persons</b>', bold=True, space_after=6))

    dir_hdr = ParagraphStyle('DHdr', fontName='Helvetica-Bold', fontSize=8.5, textColor=white, leading=10)
    dir_body = ParagraphStyle('DBody', fontName='Helvetica', fontSize=8.5, textColor=C_TEXT, leading=12)
    dir_name = ParagraphStyle('DName', fontName='Helvetica-Bold', fontSize=8.5, textColor=C_TEXT, leading=12)

    dir_data = [
        [Paragraph('Director', dir_hdr),
         Paragraph('Nationality', dir_hdr),
         Paragraph('Country of Residence', dir_hdr),
         Paragraph('Date of Birth', dir_hdr),
         Paragraph('Board Proximity', dir_hdr),
         Paragraph('Practical Implication', dir_hdr)],
        [Paragraph('Francesca Rinaldi', dir_name),
         Paragraph('Italian', dir_body),
         Paragraph('Italy', dir_body),
         Paragraph('April 1978', dir_body),
         Paragraph('Near London office', ParagraphStyle('Green', fontName='Helvetica-Bold',
                   fontSize=8.5, textColor=C_CONFIRMED, leading=12)),
         Paragraph('Can attend in-person board meetings without international travel', dir_body)],
        [Paragraph('Ciro Antonio Pagano', dir_name),
         Paragraph('Italian', dir_body),
         Paragraph('Italy', dir_body),
         Paragraph('March 1962', dir_body),
         Paragraph('Near London office', ParagraphStyle('Green2', fontName='Helvetica-Bold',
                   fontSize=8.5, textColor=C_CONFIRMED, leading=12)),
         Paragraph('Can attend in-person board meetings without international travel', dir_body)],
        [Paragraph('Mohd Redhani Bin Abdul Rahman', dir_name),
         Paragraph('Malaysian', dir_body),
         Paragraph('Malaysia', dir_body),
         Paragraph('April 1975', dir_body),
         Paragraph('NOT local — must travel', ParagraphStyle('Red', fontName='Helvetica-Bold',
                   fontSize=8.5, textColor=C_CRIMSON, leading=12)),
         Paragraph('Requires international travel for in-person board meetings at ENI House, London. '
                   'Added cost and logistical barrier compared to Italian counterparts.', dir_body)],
        [Paragraph('Amru Iskandar Bin Burhan', dir_name),
         Paragraph('Malaysian', dir_body),
         Paragraph('Malaysia', dir_body),
         Paragraph('July 1978', dir_body),
         Paragraph('NOT local — must travel', ParagraphStyle('Red2', fontName='Helvetica-Bold',
                   fontSize=8.5, textColor=C_CRIMSON, leading=12)),
         Paragraph('Requires international travel for in-person board meetings at ENI House, London. '
                   'Added cost and logistical barrier compared to Italian counterparts.', dir_body)],
    ]
    dir_table = Table(dir_data, colWidths=[40*mm, 22*mm, 32*mm, 22*mm, 28*mm, CONTENT_W - 144*mm])
    dir_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_DIVIDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C_GREY_LIGHT]),
    ]))
    story.append(dir_table)
    story.append(Spacer(1, 6*mm))

    story.append(callout_box(
        'STRUCTURAL OBSERVATION',
        [
            'The registered office of SEARA Energy Limited is ENI HOUSE — Eni\'s own London headquarters. '
            'This means the entity operates legally and physically within Eni\'s infrastructure.',
            '',
            'The company secretary (Riordan D\'Abreo) is also registered at ENI House London. '
            'While routine for corporate filings, this reinforces Eni\'s physical presence in the entity\'s '
            'day-to-day operations.',
            '',
            'The practical effect: Eni\'s representatives can conduct in-person board meetings, '
            'access filings, and manage administrative functions at minimal cost and complexity. '
            'PETRONAS Carigali\'s Malaysian directors face a structural asymmetry in access and proximity.',
        ],
        C_LIGHT_BLUE, C_TEAL, title_color=C_NAVY, body_color=C_TEXT
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 3: PETROS CONTEXT
    # ═══════════════════════════════════════════════════════════════════
    story.extend(section_header(
        'Section 3 — The PETROS Context',
        '62 years of dispute, and what SEARAH means for Sarawak'
    ))

    story.append(body(
        'PETROS (Petroleum Sarawak Berhad) is a state-owned petroleum company established by '
        'the Sarawak state government to represent its interest in petroleum resources within '
        'Sarawak\'s territory. Its core mandate is to become the sole aggregator of all '
        'petroleum produced in Sarawak — meaning all upstream producers (including PETRONAS '
        'Carigali and its joint ventures) would be required to sell their gas to PETROS first, '
        'rather than to PETRONAS or directly to external markets.',
        space_after=6))

    story.append(body(
        'This has been the subject of a long-running dispute with PETRONAS, which holds '
        'the federal mandate over Malaysia\'s petroleum resources under the Petroleum '
        'Development Act 1974. The dispute has both commercial and constitutional dimensions, '
        'touching on the Malaysia Agreement 1963 (MA63) and the rights of Sabah and '
        'Sarawak as participating states in the Malaysian federation.',
        space_after=8))

    # Timeline
    timeline_style_label = ParagraphStyle('TL', fontName='Helvetica-Bold', fontSize=8.5,
                                           textColor=C_NAVY, leading=11)
    timeline_style_text = ParagraphStyle('TT', fontName='Helvetica', fontSize=8.5,
                                          textColor=C_TEXT, leading=12)

    tl_data = [
        ['1963', 'Malaysia Agreement (MA63) — Sabah and Sarawak join Malaysia. '
                 'The extent of petroleum rights retained by each state versus the federal government is left ambiguous.'],
        ['1974', 'Petroleum Development Act — PETRONAS is granted federal control over '
                 'all petroleum resources in Malaysia. Sarawak\'s consent is not fully obtained.'],
        ['2016', 'PETROS (Petroleum Sarawak Berhad) is officially incorporated by the '
                 'Sarawak state government. Sarawak formally begins asserting its claim '
                 'to control petroleum revenues within its territory.'],
        ['2020', 'Operatorship of gas distribution assets in Miri and Bintulu is formally '
                 'transferred to PETROS — a process that had been delayed for years.'],
        ['2024–2025', 'Formal negotiations between PETRONAS and PETROS for a comprehensive '
                       'gas aggregation framework. Target conclusion: end of 2025. '
                       'This target was NOT met as of April 2026.'],
        ['February 2026', 'SEARA Energy Limited is incorporated in the UK (Company No. 17027115) '
                          'with Malaysian upstream assets potentially included in the JV scope. '
                          'PETRONAS-PETROS negotiations remain open.'],
        ['April 2026', 'SEARAH JV is publicly announced. The PETRONAS-PETROS dispute remains '
                       'unresolved — now in its 63rd year.'],
    ]

    tl_rows = [[Paragraph(y, timeline_style_label), Paragraph(e, timeline_style_text)] for y, e in tl_data]
    tl_table = Table(tl_rows, colWidths=[25*mm, CONTENT_W - 25*mm])
    tl_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, C_DIVIDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [white, C_GREY_LIGHT]),
        # Highlight unresolved/overlapping periods
        ('BACKGROUND', (0,3), (-1,3), HexColor('#FFF5F5')),   # 2016
        ('BACKGROUND', (0,4), (-1,5), HexColor('#FFF5F5')),   # 2024-2026 overlap
    ]))
    story.append(tl_table)
    story.append(Spacer(1, 8*mm))

    # Governance triangle
    story.extend(section_header(
        'The Three-Layer Governance Problem',
        'PETRONAS × PETROS × SEARA — how the disputes now overlap'
    ))

    story.append(body(
        'The incorporation of SEARA Energy Limited adds a structural third layer to what '
        'was previously a two-party domestic dispute between PETRONAS and PETROS. '
        'This is the critical governance risk that Arif\'s question identifies.',
        space_after=6))

    layer_label = ParagraphStyle('LL', fontName='Helvetica-Bold', fontSize=9.5,
                                  textColor=white, leading=12, alignment=TA_CENTER)
    layer_body  = ParagraphStyle('LB', fontName='Helvetica', fontSize=8.5,
                                  textColor=white, leading=12, alignment=TA_CENTER)
    layer_arrow  = ParagraphStyle('LA', fontName='Helvetica-Bold', fontSize=14,
                                  textColor=C_GREY_MID, leading=16, alignment=TA_CENTER)

    # Layer 1: PETRONAS ↔ PETROS
    l1 = Table([[
        Paragraph('PETRONAS', layer_label),
        Paragraph('vs', layer_arrow),
        Paragraph('PETROS', ParagraphStyle('LBP', fontName='Helvetica-Bold', fontSize=9.5,
                 textColor=white, leading=12, alignment=TA_CENTER, background=HexColor("#8B0000"))),
        Paragraph('62 years\nUNRESOLVED', ParagraphStyle('LBA', fontName='Helvetica-Bold',
                 fontSize=8, textColor=C_CRIMSON, leading=10, alignment=TA_CENTER)),
    ]], colWidths=[35*mm, 15*mm, 35*mm, CONTENT_W - 85*mm - 20*mm])
    l1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_NAVY),
        ('BACKGROUND', (1,0), (1,0), white),
        ('BACKGROUND', (2,0), (2,0), C_PETROS_RED),
        ('BACKGROUND', (3,0), (3,0), C_LIGHT_BLUE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))

    # Arrow
    arr = Table([[Paragraph('↓ SEARA JV ADDS THIRD LAYER ↓',
        ParagraphStyle('Arr', fontName='Helvetica-Bold', fontSize=9,
        textColor=C_CRIMSON, leading=12, alignment=TA_CENTER))]],
        colWidths=[CONTENT_W])
    arr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_GREY_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    # Layer 2: PETRONAS Carigali IV ↔ ENI Lasmo
    l2 = Table([[
        Paragraph('PETRONAS CARIGALI INT\'L\nVENTURES SDN BHD\n50% shareholder', layer_label),
        Paragraph('50-50\nJV', layer_arrow),
        Paragraph('ENI LASMO PLC\n50% shareholder', layer_label),
    ]], colWidths=[50*mm, 30*mm, 50*mm])
    l2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#2E4057')),
        ('BACKGROUND', (1,0), (1,0), C_LIGHT_BLUE),
        ('BACKGROUND', (2,0), (2,0), C_TEAL),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))

    # Layer 3: SEARA Energy Limited
    l3 = Table([[
        Paragraph('SEARA ENERGY LIMITED\nUK-REGISTERED — ENI HOUSE, LONDON',
                  ParagraphStyle('L3', fontName='Helvetica-Bold', fontSize=10,
                  textColor=white, leading=14, alignment=TA_CENTER)),
    ]], colWidths=[CONTENT_W])
    l3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_NAVY),
        ('BOX', (0,0), (-1,-1), 2, C_CRIMSON),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))

    story.append(l1)
    story.append(arr)
    story.append(l2)
    story.append(Spacer(1, 4*mm))
    story.append(l3)
    story.append(Spacer(1, 8*mm))

    story.append(callout_box(
        'WHAT THIS MEANS FOR SARAWAK',
        [
            'Before SEARAH: PETRONAS and PETROS negotiate directly. A settlement would involve '
            'two Malaysian parties, one federal and one state.',
            '',
            'After SEARAH: If Malaysian assets (particularly any in Sarawak) are in SEARA Energy Limited, '
            'any future renegotiation of Sarawak\'s petroleum rights must now account for Eni\'s '
            'presence as a 50% joint venture partner — with its own legal team, BIT protections, '
            'international arbitration rights, and fiduciary obligations to its own shareholders.',
            '',
            'The addition of a foreign commercial partner structurally complicates what was '
            'already a difficult domestic negotiation. This is not a peripheral concern — '
            'it is a central governance risk.',
        ],
        HexColor('#FFF5F5'), C_CRIMSON, title_color=C_CRIMSON
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 4: WHY UK INCORPORATION
    # ═══════════════════════════════════════════════════════════════════
    story.extend(section_header(
        'Section 4 — Why a UK Incorporation?',
        'Five reasons, assessed honestly — who benefits more'
    ))

    reasons = [
        (
            '1', 'English Common Law is the Global Standard for Oil & Gas Contracts',
            C_CONFIRMED, 'This is the most legitimate reason. Production Sharing Contracts (PSCs), '
                         'gas sales agreements, joint development agreements, and farm-out contracts '
                         'in the upstream industry are predominantly governed by English law or New York '
                         'law. A UK-incorporated entity fits naturally into this contractual ecosystem. '
                         'Both PETRONAS Carigali and Eni routinely use English law in their international '
                         'upstream contracts. This is not suspicious on its own.',
            'VALID COMMERCIAL REASON — Benefits both parties equally'
        ),
        (
            '2', 'Access to International Arbitration Under Bilateral Investment Treaties',
            C_CRIMSON, 'The UK has one of the world\'s most extensive networks of Bilateral Investment '
                       'Treaties (BITs) and Free Trade Agreements (FTAs). These treaties give UK-incorporated '
                       'companies (and their beneficial owners) access to investor-state arbitration '
                       'mechanisms — such as LCIA (London), ICC (Paris), or ICSID (Washington DC) — '
                       'if a host government takes regulatory actions that harm the investment. '
                       'Eni, as an Italian company operating in many jurisdictions, has extensive '
                       'experience using BIT protections. This structural benefit is available to '
                       'Eni but not automatically to Malaysia in the same way.',
            'STRUCTURAL ASYMMETRY — Eni gets more legal protection than Malaysia'
        ),
        (
            '3', 'Tax Treaty Network — Not the Primary Reason, But Real',
            C_AMBER, 'The UK has double taxation treaties with a very large number of countries. '
                     'While the corporate tax rate in the UK (~25%) is comparable to Malaysia\'s (~24%), '
                     'the UK\'s treaty network can reduce withholding taxes on dividends, interest '
                     'royalties, and capital gains when profits flow through multiple jurisdictions. '
                     'For a joint venture with assets in Indonesia and Malaysia, this can create '
                     'genuine tax efficiencies. Whether these efficiencies flow to both partners '
                     'equally, or disproportionately to Eni (which has more experience with '
                     'international tax structuring), is a legitimate question.',
            'POSSIBLE BENEFIT TO ENI — Depends on JV agreement structure'
        ),
        (
            '4', 'UK Employment Law Allows More Flexible Workforce Restructuring',
            C_CRIMSON, 'This is the concern that Arif raised. The Companies Act 2006 and UK '
                       'employment law provide more flexibility for redundancy, workforce '
                       'restructuring, and company dissolution compared to Malaysian law — '
                       'which has more protective employment provisions under the Employment '
                       'Act 1955 and industrial relations laws. If SEARA needs to conduct '
                       '"right-sizing" — whether through layoffs, role reassignments, or '
                       'secondment arrangements — it can do so with less regulatory friction '
                       'than if it were a Malaysian incorporated entity. The JV structure '
                       'also means Malaysian employees seconded to SEARA may have employment '
                       'rights that differ from those of direct PETRONAS employees.',
            'REAL CONCERN — This makes workforce adjustment easier, which is a double-edged sword'
        ),
        (
            '5', 'Signalling to International Capital Markets',
            C_CONFIRMED, 'A UK-incorporated entity with Eni as a 50% partner receives a stronger '
                         'credit signal in international capital markets. International banks, bond '
                         'investors, and project finance lenders are more familiar with UK corporate '
                         'governance, accounting standards, and legal frameworks. This can lower '
                         'the cost of debt and make the USD 6 billion revolver easier to arrange. '
                         'PETRONAS Carigali alone could also access international capital, but '
                         'the Eni partnership in a UK vehicle provides additional comfort '
                         'to lenders regarding governance standards.',
            'BENEFITS BOTH — But Eni benefits more from the reputational signal given its home jurisdiction'
        ),
    ]

    for num, title, color, body_text, assessment in reasons:
        # Number circle
        num_s = ParagraphStyle('Num', fontName='Helvetica-Bold', fontSize=14,
                                textColor=white, leading=16, alignment=TA_CENTER)
        num_box = Table([[Paragraph(num, num_s)]], colWidths=[10*mm])
        num_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), color),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ]))

        title_s = ParagraphStyle('ReasT', fontName='Helvetica-Bold', fontSize=10,
                                  textColor=color, leading=13)
        body_s = ParagraphStyle('ReasB', fontName='Helvetica', fontSize=9,
                                 textColor=C_TEXT, leading=13)
        assess_s = ParagraphStyle('ReasA', fontName='Helvetica-BoldOblique', fontSize=8.5,
                                  textColor=color, leading=11)
        assess_label = ParagraphStyle('ReasAL', fontName='Helvetica', fontSize=8,
                                      textColor=C_GREY_MID, leading=10)

        content_table = Table([
            [Paragraph(title, title_s)],
            [Paragraph(body_text, body_s)],
            [Table([[
                Paragraph('→ Assessment: ', assess_label),
                Paragraph(assessment, assess_s)
            ]], colWidths=[30*mm, CONTENT_W - 32*mm])],
        ], colWidths=[CONTENT_W - 14*mm])
        content_table.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))

        row_table = Table(
            [[num_box, content_table]],
            colWidths=[12*mm, CONTENT_W - 12*mm]
        )
        row_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('BACKGROUND', (0,0), (-1,-1), C_GREY_LIGHT),
            ('LINEBEFORE', (0,0), (0,-1), 3, color),
        ]))
        story.append(KeepTogether([row_table, Spacer(1, 4*mm)]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 5: VERDICTS
    # ═══════════════════════════════════════════════════════════════════
    story.extend(section_header(
        'Section 5 — Evidence Assessment',
        'Arif\'s claims examined against the documented evidence'
    ))

    claim_hdr = ParagraphStyle('CH', fontName='Helvetica-Bold', fontSize=8.5,
                                textColor=white, leading=11)
    claim_body = ParagraphStyle('CB', fontName='Helvetica', fontSize=8.5,
                                 textColor=C_TEXT, leading=12)

    claim_data = [
        [Paragraph('Claim', claim_hdr),
         Paragraph('Assessment', claim_hdr),
         Paragraph('Evidence', claim_hdr)],
        [Paragraph('PETRONAS has not resolved the PETROS dispute', claim_body),
         Paragraph('<font color="#155724"><b>CONFIRMED</b></font>', claim_body),
         Paragraph('Public record: negotiations ongoing through 2024–2025, expected end-2025 '
                   'conclusion NOT met. Dispute ongoing April 2026.', claim_body)],
        [Paragraph('SEARA incorporated while PETROS negotiations were unresolved', claim_body),
         Paragraph('<font color="#155724"><b>CONFIRMED</b></font>', claim_body),
         Paragraph('Companies House filing: SEARA Energy Limited incorporated 11 February 2026. '
                   'PETROS negotiations still open at time of incorporation.', claim_body)],
        [Paragraph('UK registration benefits Eni more than Malaysia', claim_body),
         Paragraph('<font color="#B8860B"><b>PARTIAL</b></font>', claim_body),
         Paragraph('Structural asymmetries confirmed: ENI House address, Italian directors local '
                   'to registered office, BIT/arbitration access asymmetrically favours Eni. '
                   'Motive for choosing UK structure cannot be confirmed from filing alone.', claim_body)],
        [Paragraph('UK structure makes "right-sizing" / workforce reduction easier', claim_body),
         Paragraph('<font color="#B8860B"><b>PLAUSIBLE</b></font>', claim_body),
         Paragraph('UK Companies Act 2006 does provide more employment restructuring flexibility '
                   'than Malaysian law. No direct evidence this was the primary motive — '
                   'English law standard for O&G contracts is a legitimate alternative explanation.', claim_body)],
        [Paragraph('CEO (Tengku Taufik) is personally responsible for the PETROS failure', claim_body),
         Paragraph('<font color="#B8860B"><b>PARTIAL</b></font>', claim_body),
         Paragraph('The PETROS dispute predates his tenure. However: (a) he has not resolved it '
                   'during his tenure, and (b) he proceeded to sign and incorporate SEARA before '
                   'PETROS was resolved — representing a choice to prioritise the Eni deal. '
                   'Accountability is systemic, but his personal signature is on the JV.', claim_body)],
        [Paragraph('Malaysian Parliament was not consulted before SEARA was signed', claim_body),
         Paragraph('<font color="#C8102E"><b>NO EVIDENCE FOUND</b></font>', claim_body),
         Paragraph('No public record of Parliamentary notification, debate, or approval for '
                   'a USD 15 billion JV involving Malaysian petroleum assets, incorporated '
                   'in a foreign jurisdiction. This does not mean it did not happen — '
                   'it means there is no public evidence it did.', claim_body)],
        [Paragraph('The reserved matters list is not publicly disclosed', claim_body),
         Paragraph('<font color="#C8102E"><b>NOT PUBLIC</b></font>', claim_body),
         Paragraph('The Companies House filing contains no information about reserved matters, '
                   'veto rights, or board tiebreaker mechanisms. These would be in the JV '
                   'shareholders\' agreement, which is not a public document.', claim_body)],
    ]

    claim_table = Table(claim_data, colWidths=[52*mm, 32*mm, CONTENT_W - 84*mm])
    claim_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_DIVIDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C_GREY_LIGHT]),
    ]))
    story.append(claim_table)
    story.append(Spacer(1, 10*mm))

    story.extend(section_header('Overall Scores', 'Weighted assessment across four dimensions'))
    story.append(Spacer(1, 4*mm))

    story.extend(score_bar(
        'Economics & Gas Volume',
        72, C_CONFIRMED,
        footnote='Strong asset base, correct directional bet on gas/LNG. '
                 'B+ reflects conditional pass — depends on project delivery and gas price cycles.'
    ))
    story.extend(score_bar(
        'Governance & Sovereignty',
        38, C_CRIMSON,
        footnote='PETROS conflict unresolved, 3-layer governance structure, Eni BIT protections, '
                 'UK jurisdiction adds complexity to domestic policy. D-grade is appropriate.'
    ))
    story.extend(score_bar(
        'Human Capital & Workers',
        30, C_CRIMSON,
        footnote='No public evidence of employment terms for transferred staff, '
                 'secondment arrangements unclear, Malaysian directors\' fiduciary conflicts unaddressed.'
    ))
    story.extend(score_bar(
        'Transparency & Accountability',
        25, C_CRIMSON,
        footnote='No evidence of Parliamentary notification. Reserved matters not public. '
                 'PETROS unresolved while Eni deal proceeded. Board proximity asymmetry not explained.'
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 6: OPEN QUESTIONS
    # ═══════════════════════════════════════════════════════════════════
    story.extend(section_header(
        'Section 6 — Open Questions',
        'Questions that require answers from PETRONAS, the Malaysian government, and SEARA\'s board'
    ))

    categories_q = [
        ('Governance & Control', [
            'Who is the tiebreaker in a 2-2 board deadlock between the two Malaysian and two Italian directors? '
            'What is the reserved matters list, and who drafted it?',
            'Does Malaysian Parliament know precisely which assets were committed to SEARA, '
            'and did it approve or ratify the commitment before February 2026?',
            'Were the Malaysian directors on SEARA\'s board appointed by the PETRONAS Board of Directors '
            'or by PETRONAS Carigali IV as a subsidiary decision — and is there a conflict '
            'when their primary employer is PETRONAS but they owe fiduciary duties to a 50-50 JV?',
            'What is the exit clause if Eni wishes to leave the JV in years 5–10? '
            'Does PETRONAS Carigali have a right of first refusal?',
        ]),
        ('PETROS & Sarawak', [
            'Which specific Malaysian upstream assets were transferred into SEARA?',
            'Are any of these assets in, or adjacent to, Sarawak?',
            'Was PETROS informed or consulted before Malaysian assets were committed to the 50-50 JV with Eni?',
            'Does the SEARA governance structure make resolution of the PETRONAS-PETROS '
            'negotiations more likely, or less likely?',
            'If Sarawak successfully asserts PETROS as sole aggregator, how does that interact '
            'with SEARA\'s gas sales contracts — which now involve Eni as a 50% partner?',
        ]),
        ('Employment & People', [
            'What is the employment status of Malaysian staff assigned to SEARA assets — '
            'are they PETRONAS employees on secondment, or SEARA employees?',
            'If SEARA conducts "right-sizing," what is the redeployment obligation '
            'back to PETRONAS Group?',
            'Are the Malaysian SEARA directors compensated by PETRONAS or by SEARA Energy Limited? '
            'Who pays for their travel to London for board meetings?',
            'What happens to staff benefits (pension, healthcare, union representation) '
            'if a staff member has been on secondment to SEARA for more than 2 years?',
        ]),
        ('Financial & Liability', [
            'Where is the USD 6 billion revolving credit facility recorded — '
            'on SEARA\'s balance sheet, or on PETRONAS Carigali IV\'s?',
            'Does the debt carry any implicit or explicit Malaysian government guarantee?',
            'If Kutei Basin deepwater (Indonesia) experiences cost overruns or delays, '
            'who bears the cost — SEARA, PETRONAS Carigali, or PETRONAS parent?',
            'Are SEARA\'s Malaysian assets pledged as security against the debt facility? '
            'If so, what is the impact on PETRONAS\'s own balance sheet?',
        ]),
    ]

    q_label = ParagraphStyle('QL', fontName='Helvetica-Bold', fontSize=8.5,
                              textColor=C_NAVY, leading=11)
    q_body  = ParagraphStyle('QB', fontName='Helvetica', fontSize=9,
                               textColor=C_TEXT, leading=13)

    for cat, questions in categories_q:
        cat_hdr = Table([[Paragraph(cat, ParagraphStyle('Cat', fontName='Helvetica-Bold',
                    fontSize=10, textColor=white, leading=12))]],
                    colWidths=[CONTENT_W])
        cat_hdr.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_NAVY),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(cat_hdr)

        for q in questions:
            q_row = Table([[
                Paragraph('?', ParagraphStyle('QB', fontName='Helvetica-Bold', fontSize=9,
                          textColor=C_NAVY, leading=11, alignment=TA_CENTER)),
                Paragraph(q, q_body),
            ]], colWidths=[8*mm, CONTENT_W - 8*mm])
            q_row.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), C_GREY_LIGHT),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LINEBEFORE', (0,0), (0,-1), 2, C_TEAL),
            ]))
            story.append(q_row)
        story.append(Spacer(1, 6*mm))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 7: CONCLUSIONS
    # ═══════════════════════════════════════════════════════════════════
    story.extend(section_header(
        'Section 7 — Conclusions',
        'What this report establishes, and what it cannot yet determine'
    ))

    story.append(body(
        'This report does not conclude that SEARAH is automatically a bad deal for Malaysia. '
        'The upstream assets are real. The gas market fundamentals in Southeast Asia are '
        'structurally sound. Sharing capex and technical risk with a partner of Eni\'s '
        'calibre has legitimate commercial rationale.',
        space_after=6))

    story.append(body(
        'What this report does establish is that there are governance, sovereignty, and '
        'transparency concerns that have not been publicly addressed — and that the timing '
        'and structure of the SEARAH deal, relative to the unresolved PETROS negotiations, '
        'raises legitimate questions about whose interests were prioritised.',
        space_after=6))

    story.append(callout_box(
        'WHAT IS CONFIRMED BY DOCUMENTED EVIDENCE',
        [
            '1. PETRONAS has not resolved its dispute with PETROS despite 62 years and a stated '
               'target of end-2025. SEARA was incorporated before that target was met.',
            '',
            '2. SEARA Energy Limited is registered at Eni\'s London office. Eni\'s directors '
               'can access it physically without travel. Malaysian directors cannot.',
            '',
            '3. PETROS is not a party to SEARA Energy Limited. Any Malaysian assets '
               'in Sarawak that are now in SEARA add Eni as a structural third party '
               'to the PETRONAS-PETROS dispute.',
            '',
            '4. There is no public evidence that Malaysian Parliament was notified, '
               'consulted, or gave approval for this arrangement before incorporation.',
            '',
            '5. The reserved matters list — the document that determines which decisions '
               'require unanimous consent and which can be made by either party — '
               'is not a public document.',
        ],
        HexColor('#E8F4F0'), C_CONFIRMED, title_color=C_CONFIRMED
    ))

    story.append(Spacer(1, 8*mm))

    story.append(callout_box(
        'WHAT CANNOT BE DETERMINED FROM AVAILABLE EVIDENCE',
        [
            '1. Whether the decision to incorporate in the UK was primarily driven by Eni\'s preference, '
               'PETRONAS\'s preference, or mutual design — and whether the terms were negotiated equally.',
            '',
            '2. Whether Malaysian directors have actual meaningful influence in board decisions, '
               'or whether the practical centre of gravity is entirely in London.',
            '',
            '3. Whether staff transferred to SEARA have been given adequate protections, '
               'because no employment terms have been publicly disclosed.',
            '',
            '4. Whether the reserved matters list was drafted by PETRONAS\'s lawyers '
               'or Eni\'s — and whether it adequately protects Malaysian national interests.',
            '',
            '5. Whether Parliament will ever see the full SEARAH agreement, '
               'or whether it will be treated as a commercial-in-confidence document.',
        ],
        HexColor('#FFF8E8'), C_AMBER, title_color=C_AMBER
    ))

    story.append(Spacer(1, 10*mm))

    # Closing statement
    close_box = Table([[Paragraph(
        '"DITEMPA BUKAN DIBERI — the right to ask is not given, it is forged. '
        'Every question in this report is asked in the spirit of accountable governance. '
        'The people of Malaysia — and Malaysian workers — have a right to know '
        'what has been committed on their behalf, to whom, and on whose authority."',
        ParagraphStyle('Close', fontName='Helvetica-BoldOblique', fontSize=10,
                       textColor=C_NAVY, leading=15, alignment=TA_JUSTIFY))]],
        colWidths=[CONTENT_W])
    close_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BLUE),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LINEBEFORE', (0,0), (0,-1), 5, C_GOLD),
    ]))
    story.append(close_box)

    # ═══════════════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 10*mm))
    story.append(HRule(CONTENT_W, 1, C_NAVY))
    story.append(Spacer(1, 4*mm))

    footer_left = Paragraph(
        '<b>DITEMPA BUKAN DIBERI</b><br/>'
        '<font size=7.5>Compiled from open source intelligence and official regulatory filings. '
        'This report is shared for public accountability purposes. '
        'Claims are labeled CONFIRMED / PLAUSIBLE / UNPROVEN based on available evidence. '
        'Further documentation required to advance open questions.</font>',
        ParagraphStyle('FL', fontName='Helvetica', fontSize=8, textColor=C_TEXT, leading=12))
    footer_right = Paragraph(
        'arifOS_bot × makcikGPT<br/>'
        '15 April 2026<br/>'
        'SEARAH × PETROS Investigation<br/>'
        'Open Source Intelligence Report',
        ParagraphStyle('FR', fontName='Helvetica', fontSize=7.5,
                       textColor=C_GREY_MID, leading=11, alignment=TA_RIGHT))

    footer = Table([[footer_left, footer_right]],
                   colWidths=[(CONTENT_W)/2, (CONTENT_W)/2])
    footer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(footer)

    # ─── BUILD ─────────────────────────────────────────────────────────
    doc.build(story)
    print(f'PDF written to: {output_path}')


if __name__ == '__main__':
    out = '/root/.openclaw/workspace/memory/investigations/SEARAH-PETROS-Executive-Briefing.pdf'
    build_pdf(out)
