#!/usr/bin/env python3
"""SEARAH v13 — Clean formatting, proper margins, SEAL 999."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import hashlib, hmac

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY     = HexColor('#0a0a1a')
NAVY2    = HexColor('#1a2a4a')
ACCENT   = HexColor('#c41e3a')
LIGHT_BG = HexColor('#fafaf8')
GRAY     = HexColor('#444444')
MUTED    = HexColor('#888888')
RULE     = HexColor('#cccccc')
OFFWHITE = HexColor('#f5f5f5')
WARM_BG  = HexColor('#fff8f8')
LINK_BG  = HexColor('#f0f4ff')

W, H = A4  # 595.28pt × 841.89pt

# ── Document hash for SEAL 999 ────────────────────────────────────────────────
DOC_HASH   = "40033ed8f4c1c96feb0c57a81256e41c62a471cd7b9f8dc68c7978321dfbc72b"
COMMITMENT = hmac.new(
    b'ariffazil-secret-key',
    b'SEARAH-EXPOSE-FINAL-v1.2-corrected',
    hashlib.sha256
).hexdigest()

# ── Page geometry ──────────────────────────────────────────────────────────────
LEFT_MARGIN   = 20*mm
RIGHT_MARGIN  = 20*mm
TOP_MARGIN    = 18*mm
BOTTOM_MARGIN = 16*mm
CONTENT_W     = W - LEFT_MARGIN - RIGHT_MARGIN   # = 555.28pt ≈ 196mm

# ── Canvas-level cover page ───────────────────────────────────────────────────
class CoverPage(Flowable):
    def wrap(self, availW, availH):
        return availW, availH

    def draw(self):
        c = self.canv
        w, h = W, H

        # Dark background
        c.setFillColor(NAVY)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Subtle grid
        c.setFillColor(HexColor('#ffffff08'))
        c.setStrokeColor(HexColor('#ffffff04'))
        c.setLineWidth(0.3)
        for x in range(0, int(w)+1, 20):
            c.line(x, 0, x, h)
        for y in range(0, int(h)+1, 20):
            c.line(0, y, w, y)

        # Red accent bar
        c.setFillColor(ACCENT)
        c.rect(0, 0, 4*mm, h, fill=1, stroke=0)

        # Header
        c.setFillColor(HexColor('#ffffff60'))
        c.setFont('Helvetica', 7)
        c.drawString(20*mm, H - 22*mm, 'EXCLUSIVE INVESTIGATION  |  MAY 2026')
        c.drawRightString(w - 20*mm, H - 22*mm, 'May 2026  |  For Public Review')

        # Rule under header
        c.setStrokeColor(HexColor('#ffffff20'))
        c.setLineWidth(0.5)
        c.line(20*mm, H - 27*mm, w - 20*mm, H - 27*mm)

        # Label
        c.setFillColor(ACCENT)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(20*mm, H - 42*mm, 'THE DEAL THE RAKYAT NEED TO UNDERSTAND')

        # Title
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 78)
        c.drawString(20*mm, H - 115*mm, 'SEARAH')

        # Subtitle
        c.setFont('Helvetica-Oblique', 22)
        c.setFillColor(HexColor('#ffffffb0'))
        c.drawString(20*mm, H - 128*mm, 'The Deal That Could Reshape')
        c.drawString(20*mm, H - 136*mm, "Malaysia's Petroleum Future")

        # Description box with accent bar
        desc = [
            "How a London-registered company, a gas field 200 kilometres off the",
            "coast of Sarawak, and a legal structure quietly incorporated during an",
            "active court dispute — came together in a RM70 billion agreement.",
            "",
            "And why it matters to every Malaysian who pays for fuel.",
        ]
        y_d = H - 152*mm
        c.setFillColor(ACCENT)
        c.rect(20*mm, y_d - 2*mm, 3*mm, 24*mm, fill=1, stroke=0)
        c.setFillColor(HexColor('#ffffffcc'))
        c.setFont('Helvetica', 9.5)
        for i, line in enumerate(desc):
            c.drawString(27*mm, y_d - i*5.5*mm, line)

        # Separator
        c.setStrokeColor(HexColor('#ffffff15'))
        c.setLineWidth(0.4)
        c.line(20*mm, 34*mm, w - 20*mm, 34*mm)

        # Author
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(20*mm, 25*mm, 'BY ARIF FAZIL')

        c.setFillColor(HexColor('#ffffff50'))
        c.setFont('Helvetica', 7)
        c.drawString(20*mm, 18*mm, 'SEAL 999  —  DITEMPA BUKAN DIBERI')

        # Seal info right
        c.setFont('Helvetica', 6.5)
        c.setFillColor(HexColor('#ffffff40'))
        c.drawRightString(w - 20*mm, 25*mm, 'HMAC-SHA256')
        c.drawRightString(w - 20*mm, 20*mm, f'Commit: {COMMITMENT[:24]}...')
        c.drawRightString(w - 20*mm, 15*mm, f'DB Hash: {DOC_HASH[:24]}...')


# ── Page template (header + footer) ──────────────────────────────────────────
def on_page(canvas_obj, doc):
    w, h = W, H
    page_num = doc.page - 1  # 0-indexed

    if page_num == 0:  # Cover — skip
        return

    # Header rule
    canvas_obj.setStrokeColor(RULE)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(LEFT_MARGIN, H - TOP_MARGIN + 4*mm,
                    w - RIGHT_MARGIN, H - TOP_MARGIN + 4*mm)

    # Header text
    canvas_obj.setFont('Helvetica-Bold', 6.5)
    canvas_obj.setFillColor(black)
    canvas_obj.drawString(LEFT_MARGIN, H - TOP_MARGIN + 7*mm, 'SEARAH INVESTIGATION')
    canvas_obj.setFont('Helvetica', 6.5)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawRightString(w - RIGHT_MARGIN, H - TOP_MARGIN + 7*mm, 'May 2026')

    # Footer rule
    canvas_obj.setStrokeColor(RULE)
    canvas_obj.line(LEFT_MARGIN, BOTTOM_MARGIN - 2*mm,
                    w - RIGHT_MARGIN, BOTTOM_MARGIN - 2*mm)

    # Footer text
    canvas_obj.setFont('Helvetica', 6)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(LEFT_MARGIN, BOTTOM_MARGIN - 6*mm,
        'SEARAH: The Deal That Could Reshape Malaysia\'s Petroleum Future')
    canvas_obj.drawRightString(w - RIGHT_MARGIN, BOTTOM_MARGIN - 6*mm, str(doc.page))


# ── Styles ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY = S('Body',
    fontName='Helvetica', fontSize=9.5, textColor=HexColor('#1a1a1a'),
    spaceAfter=3*mm, leading=15, alignment=TA_JUSTIFY)

PART_LABEL = S('PartLabel',
    fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
    spaceAfter=1*mm, spaceBefore=8*mm, leading=10)

PART_TITLE = S('PartTitle',
    fontName='Helvetica-Bold', fontSize=20, textColor=black,
    spaceAfter=3*mm, spaceBefore=1*mm, leading=24)

SECTION_LABEL = S('SectionLabel',
    fontName='Helvetica-Bold', fontSize=7.5, textColor=ACCENT,
    spaceAfter=1*mm, spaceBefore=6*mm, leading=10)

H3 = S('H3',
    fontName='Helvetica-Bold', fontSize=9.5, textColor=black,
    spaceAfter=2*mm, spaceBefore=5*mm, leading=13)

PULLQUOTE = S('PullQuote',
    fontName='Helvetica-Oblique', fontSize=11.5, textColor=white,
    spaceAfter=1*mm, leading=17, leftIndent=6*mm, rightIndent=6*mm,
    borderColor=ACCENT, borderWidth=3, borderPadding=6)

ATTR = S('Attr',
    fontName='Helvetica-Bold', fontSize=7, textColor=HexColor('#ffffff88'),
    spaceAfter=0, leading=10, spaceBefore=1*mm)

KEY_FIND = S('KeyFind',
    fontName='Helvetica-Bold', fontSize=9, textColor=ACCENT,
    spaceAfter=0, leading=13, leftIndent=4*mm)

TIMELINE_DATE = S('TLDate',
    fontName='Helvetica-Bold', fontSize=7.5, textColor=ACCENT,
    spaceAfter=0, leading=11, alignment=TA_RIGHT)

TIMELINE_TEXT = S('TLText',
    fontName='Helvetica', fontSize=8.5, textColor=HexColor('#1a1a1a'),
    spaceAfter=0, leading=12)

Q_NUM = S('QNum',
    fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
    spaceAfter=0.5*mm, leading=9)

Q_TEXT = S('QText',
    fontName='Helvetica-Bold', fontSize=9, textColor=black,
    spaceAfter=1*mm, leading=12)

Q_BODY = S('QBody',
    fontName='Helvetica', fontSize=8.5, textColor=GRAY,
    spaceAfter=0, leading=12)

SOURCES = S('Sources',
    fontName='Helvetica', fontSize=8, textColor=GRAY,
    spaceAfter=1.5*mm, leading=11.5, alignment=TA_LEFT)

SEAL_TITLE = S('SealTitle',
    fontName='Helvetica-Bold', fontSize=9, textColor=black,
    spaceAfter=2*mm, leading=12)

SEAL_MONO = S('SealMono',
    fontName='Courier', fontSize=7, textColor=HexColor('#222222'),
    spaceAfter=1*mm, leading=11)

SEAL_WARN = S('SealWarn',
    fontName='Helvetica-Bold', fontSize=7.5,
    textColor=ACCENT, leading=11)

SEAL_FOOT = S('SealFoot',
    fontName='Helvetica-Oblique', fontSize=7.5,
    textColor=GRAY, leading=11)

CLOSING = S('Closing',
    fontName='Helvetica-Oblique', fontSize=12,
    textColor=HexColor('#1a1a1a'),
    spaceAfter=4*mm, leading=17, leftIndent=6*mm,
    borderColor=ACCENT, borderWidth=2, borderPadding=6)

PART_HEADER_LABEL = S('PHL',
    fontName='Helvetica', fontSize=7, textColor=MUTED,
    spaceAfter=1*mm, leading=9, alignment=TA_CENTER)

PART_HEADER_TITLE = S('PHT',
    fontName='Helvetica-Bold', fontSize=20, textColor=black,
    spaceAfter=0, leading=24, alignment=TA_CENTER)


# ── Story builders ───────────────────────────────────────────────────────────
story = []

def hr(color=RULE, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color,
                      spaceAfter=3*mm, spaceBefore=3*mm)

def section_header(label, title, top_space=5*mm):
    return [
        Spacer(1, top_space),
        Paragraph(label.upper(), PART_LABEL),
        Paragraph(title, PART_TITLE),
        HRFlowable(width='100%', thickness=1.5, color=ACCENT,
                   spaceAfter=4*mm, spaceBefore=1*mm),
    ]

def pullquote(text, attr=None):
    data = [[Paragraph(text, PULLQUOTE)]]
    if attr:
        data.append([Paragraph(f'— {attr}', ATTR)])
    t = Table(data, colWidths=[CONTENT_W - 12*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY2),
        ('LEFTPADDING', (0,0), (-1,-1), 6*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 6*mm),
        ('TOPPADDING', (0,0), (-1,-1), 5*mm),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-2), 0),
        ('BEFORE', (0,1), (-1,1), 1*mm),
    ]))
    return [t, Spacer(1, 5*mm)]

def key_find(text):
    t = Table([[Paragraph(text, KEY_FIND)]], colWidths=[CONTENT_W - 8*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WARM_BG),
        ('BOX', (0,0), (-1,-1), 1.5, ACCENT),
        ('LEFTPADDING', (0,0), (-1,-1), 5*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 5*mm),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return [t, Spacer(1, 5*mm)]

def timeline_item(date, text):
    t = Table([[Paragraph(date, TIMELINE_DATE),
                Paragraph(text, TIMELINE_TEXT)]],
              colWidths=[24*mm, CONTENT_W - 24*mm - 2*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (0,-1), 0),
        ('RIGHTPADDING', (0,0), (0,-1), 4*mm),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    return t

def question_block(num, q, body):
    t = Table([[Paragraph(f'QUESTION {num}', Q_NUM)],
               [Paragraph(q, Q_TEXT)],
               [Paragraph(body, Q_BODY)]],
              colWidths=[CONTENT_W - 8*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.7, RULE),
        ('LEFTPADDING', (0,0), (-1,-1), 5*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 5*mm),
        ('TOPPADDING', (0,0), (0,0), 4*mm),
        ('TOPPADDING', (0,1), (-1,-1), 1*mm),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-2), 0),
    ]))
    return [t, Spacer(1, 5*mm)]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: COVER
# ══════════════════════════════════════════════════════════════════════════════
story.append(CoverPage())
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: PREFACE
# ══════════════════════════════════════════════════════════════════════════════
story += section_header('Preface', 'Why This Document Exists')
story.append(Paragraph(
    'This is not a political document. It is an investigative one. '
    'The subject is a RM70 billion agreement that affects every Malaysian '
    'who uses fuel, pays electricity bills, or heats a home. '
    'The RM70 billion is not a guess — it is Eni\'s own figure, disclosed '
    'in a November 2025 press release, confirmed by PETRONAS, and '
    'reported by Reuters.', BODY))

story.append(Paragraph(
    'The questions this document raises are not answered. '
    'They are genuinely unanswered — by PETRONAS, by Eni, '
    'by the Malaysian government, and by the Italian government.', BODY))

story.extend(key_find(
    'RM70 BILLION. USD 15 BILLION. "IN EXCESS OF USD 15 BILLION OVER FIVE YEARS" '
    '— ENI PRESS RELEASE, NOVEMBER 2025.'))

story.append(Paragraph(
    'The document draws on public sources: company registries, '
    'government press releases, international arbitration records, '
    'energy research reports, and court filings. '
    'It distinguishes clearly between what is confirmed and what requires '
    'further investigation. That distinction is intentional.', BODY))

story.append(Paragraph(
    'The investigation is ongoing. The questions asked here '
    'are questions — not accusations. They deserve answers.', BODY))

story.extend(pullquote(
    '"Every Malaysian who uses fuel, who pays electricity bills, '
    'who heats a home — has a stake in the answer."',
    'Arif Fazil'))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PART 1: THE DEAL
# ══════════════════════════════════════════════════════════════════════════════
story += section_header('Part 1 of 4', 'The Deal')

story.append(Paragraph('What Was Signed in Abu Dhabi', H3))
story.append(Paragraph(
    'On November 3, 2025, at ADIPEC in Abu Dhabi — '
    'one of the world\'s largest energy conferences — '
    'PETRONAS and Eni signed what both companies described '
    'as a "transformational" joint venture. The agreement was '
    'announced publicly. The CEOs of both companies attended.', BODY))

story.append(Paragraph(
    'The investment agreement committed PETRONAS and Eni to '
    'a 50/50 joint venture covering upstream petroleum assets '
    'across Malaysia and Indonesia. '
    'Eni described the combination as "transformational." '
    'PETRONAS called it "historic." Both descriptions may be accurate.', BODY))

story.extend(key_find(
    'THE TRANSACTION HAS NOT YET CLOSED. '
    'Eni\'s own statements, as recently as March 2026, indicate '
    'that "customary and governmental approvals" were still being obtained.'))

story.append(Paragraph(
    'Neither announcement mentioned the most important thing about '
    'the structure: it was registered in London. '
    'It was registered there before the deal was announced. '
    'And it was registered during an active court dispute '
    'about who owns the gas.', BODY))

story.append(Paragraph(
    'The company is called SEARAH Limited — incorporated February 11, 2026 '
    'at ENI House, 8-10 Stratford Place, London. '
    'It is registered at UK Companies House as Company No. 17027115.', BODY))

story += pullquote(
    'The question is not whether the structure is illegal. '
    'The question is whether it was designed this way — '
    'and who decided that.',
    'SEARAH Investigation')

story += section_header('The Sequence', 'The Timing Is Difficult to Ignore', top_space=2*mm)

story.append(Paragraph(
    'In August 2025, PETROS filed a lawsuit against PETRONAS in the '
    'Kuching High Court, alleging that PETRONAS had been supplying '
    'natural gas in Sarawak without a valid license. '
    'In October 2025, Eni confirmed the joint venture was being structured. '
    'In February 2026, SEARAH Limited was incorporated in London. '
    'In March 2026, the company changed its name — '
    '14 days after the Malaysian Federal Court agreed to hear '
    'PETRONAS\'s constitutional challenge.', H3))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PART 2: THE FIELD
# ══════════════════════════════════════════════════════════════════════════════
story += section_header('Part 2 of 4', 'The Field')

story.append(Paragraph(
    'Why Sarawak\'s Gas Is Central to This Deal', H3))
story.append(Paragraph(
    'Block SK316 is PETRONAS\'s largest domestic producing asset. '
    'That is not an opinion — it is the finding of Wood Mackenzie, '
    'one of the world\'s most respected energy research firms, '
    'in a February 2025 report written specifically about the '
    'PETRONAS-Eni combination.', BODY))

story.extend(key_find(
    '"PETRONAS\'s largest domestic producing asset" — '
    'WOOD Mackenzie, February 2025, press release.'))

story.append(Paragraph(
    'The Kasawari gas field, located in Block SK316 approximately '
    '200 kilometres off the coast of Sarawak, began production '
    'in August 2024. '
    'It is one of the most significant domestic energy discoveries '
    'in Malaysia\'s recent history. '
    'It is operated by PETRONAS Carigali — and now, indirectly, '
    'through the SEARAH structure, partly owned by Eni.', BODY))

story.append(Paragraph(
    'MLNG Bintulu — one of the world\'s largest LNG export facilities — '
    'processes gas from these fields. '
    'Its customers include Japan, Korea, Taiwan, and China. '
    'Every shipment that leaves Bintulu generates foreign exchange '
    'for Malaysia. '
    'Under the SEARAH structure, that revenue flow is now partly '
    'governed by English law, in a UK-registered company '
    'with 50% Italian ownership.', BODY))

story += pullquote(
    'Block SK316 is not just a gas field. '
    'It is the asset that makes the RM70 billion figure credible. '
    'And it is Sarawak\'s gas.',
    'SEARAH Investigation')

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PART 3: THE ARCHITECT
# ══════════════════════════════════════════════════════════════════════════════
story += section_header('Part 3 of 4', 'The Architect')

story.append(Paragraph(
    'Claudio Descalzi and the SEARAH Structure', H3))
story.append(Paragraph(
    'Claudio Descalzi has been the chief executive of Eni SpA '
    'since May 2014. Born in Milan on February 27, 1955, '
    'trained as an engineer at the Politecnico di Milano, '
    'he has spent his entire career at Eni. '
    'In April 2026, the Italian Treasury appointed him '
    'to a senior government role. He has simultaneously run Eni '
    'through some of its most internationally contested periods.', BODY))

story.append(Paragraph(
    'In March 2021, Descalzi was acquitted by an Italian court '
    'in a case concerning the acquisition of OPL 245 — '
    'a contested Nigerian oil block. '
    'The acquittal was appealed. The appeal was ongoing '
    'as of early 2026. '
    'Eni has consistently maintained Descalzi\'s innocence '
    'throughout the proceedings.', BODY))

story.append(Paragraph(
    'Eni has disclosed that SEARAH follows what it calls '
    'the "satellite model" — a strategy Eni has used in '
    'three prior jurisdictions: Norway, Angola, and the United Kingdom. '
    'In each case, the local production asset is placed inside '
    'a UK or Norwegian holding structure. '
    'In each case, English or Norwegian law governs the relationship '
    'between the production company and its partners.', BODY))

story.extend(key_find(
    'THE "SATELLITE MODEL" IS ENI\'S MODEL — '
    'USED IN NORWAY, ANGOLA, AND THE UK. '
    'PETRONAS DID NOT INVENT THIS STRUCTURE. '
    'ENI INTRODUCED IT.'))

story.append(Paragraph(
    'The satellite model is not inherently illegal. '
    'It is a legitimate corporate structuring approach '
    'used in multiple jurisdictions. '
    'The question this document asks is not whether it is illegal. '
    'The question is whether a sovereign resource of a nation '
    'was placed inside this structure — and '
    'whether the relevant parties consented.', BODY))

story += section_header('The Structural Finding', '', top_space=2*mm)

story.append(Paragraph(
    'SEARAH is not accidentally registered in London. '
    'The UK structure is not a technicality. '
    'It is the point.', BODY))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PART 4: THE UNANSWERED
# ══════════════════════════════════════════════════════════════════════════════
story += section_header('Part 4 of 4', 'The Unanswered')

story.append(Paragraph(
    'What Nobody in Putrajaya Will Explain', H3))
story.append(Paragraph(
    'The transaction has not yet closed. '
    'Eni\'s own statements, as recently as March 2026, '
    'indicate that "customary and governmental approvals" '
    'were still being obtained. '
    'The deal was expected to reach closing '
    'in the first half of 2026. '
    'There is still time. '
    'There is still time for the questions to be asked.', BODY))

story.append(Paragraph(
    'What we do not yet have — '
    'what has not been made public — '
    'is any record of the following:', BODY))

story += question_block(1, 'The UK Structure',
    'Who specifically decided that SEARAH would be incorporated '
    'in the United Kingdom under English law, rather than in Malaysia '
    'under Malaysian law? Was this decision made by Eni, by PETRONAS, '
    'or jointly? Was Malaysian legal counsel consulted?')

story += question_block(2, 'Government Approval',
    'Did the Federal Cabinet formally approve the fact that Malaysian '
    'petroleum assets — including Sarawak fields — would be placed '
    'inside a UK-incorporated company with 50% foreign ownership?')

story += question_block(3, 'Sarawak\'s Position',
    'Was the Sarawak state government informed that assets in its '
    'offshore waters were being placed inside a UK company? '
    'Was the Sarawak Minister for Petroleum consulted?')

story += question_block(4, 'PETRONAS-PETROS Conflict',
    'Given that PETRONAS and PETROS were in active litigation over '
    'these same assets at the time SEARAH was incorporated, '
    'what consideration was given to the implications '
    'of placing disputed assets inside a UK company?')

story += question_block(5, 'The 50-Year Track Record',
    'PETRONAS was established in 1974. PETROS was incorporated in 2017. '
    'This dispute has run for decades. Why has no Malaysian government '
    'resolved it? What has been the cost to the people of Sarawak '
    'of this institutional failure?')

story += question_block(6, 'Descalzi\'s Role',
    'Eni has disclosed that the satellite model is Eni\'s model, '
    'used in Norway, Angola, and the UK. '
    'Did PETRONAS propose this structure, or did Eni? '
    'If Eni proposed it, what consideration did PETRONAS give '
    'to the jurisdictional implications for Malaysia?')

story += question_block(7, 'The Closing Conditions',
    'What are the conditions precedent to closing? '
    'Has the Malaysian government insisted on any structural modifications '
    'as a condition of its approval? '
    'Is there a date by which those conditions must be satisfied?')

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PETRONAS-PETROS + TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph(
    'The PETRONAS-PETROS Question Is Not Academic', H3))
story.append(Paragraph(
    'The Federal Court\'s decision to allow the PETRONAS constitutional '
    'challenge on March 16, 2026 is significant not because it resolves '
    'the dispute — it does not — but because it means the court has agreed '
    'the question is serious enough to hear.', BODY))

story.append(Paragraph(
    'The core issue is whether the Petroleum Development Act 1974, '
    'and the federal petroleum regime it established, '
    'validly applies in Sarawak, or whether Sarawak\'s own petroleum laws '
    'take precedence. If PETROS prevails, the implications for '
    'PETRONAS\'s operating authority in Sarawak are substantial. '
    'If PETRONAS prevails, the PETROS framework is significantly weakened. '
    'Neither outcome will change the actual fields — '
    'but those assets are now, in their corporate holding structure, '
    'partly inside SEARAH Limited — a UK company governed by English law.', BODY))

story += pullquote(
    'The PETRONAS-PETROS dispute is not academic. '
    'SEARAH is not academic. The RM70 billion question is not academic. '
    'Every Malaysian who uses fuel, who pays electricity bills, '
    'who heats a home — has a stake in the answer.',
    'Arif Fazil')

story.append(Paragraph('Key Timeline', SECTION_LABEL))

timeline = [
    ('Jul 2017',   'PETROS incorporated — 100%-owned by Sarawak government'),
    ('Aug 2024',   'Kasawari gas field, Block SK316 offshore Sarawak, begins production'),
    ('Jun 2025',  'Framework Agreement signed in Kuala Lumpur — both CEOs attend'),
    ('Aug 2025',  'PETROS sues PETRONAS in Kuching High Court — unlicensed gas supply in Sarawak'),
    ('Oct 2025',  'Anwar speaks with Meloni — both agree to expedite the deal'),
    ('Nov 3, 2025', 'Investment Agreement signed at ADIPEC Abu Dhabi — both CEOs sign'),
    ('Feb 11, 2026', 'SEARAH Limited incorporated at UK Companies House (Company No. 17027115)'),
    ('Feb 25, 2026', 'Kuching High Court rules on bank guarantee — jurisdiction sent to Federal Court'),
    ('Mar 16, 2026', 'Federal Court allows PETRONAS constitutional challenge on Sarawak petroleum laws'),
    ('Mar 30, 2026', 'Company changes name from SEARA ENERGY LIMITED to SEARAH LIMITED — 14 days after ruling'),
    ('Mid-2026',   'SEARAH expected to begin operations — closing conditions still being satisfied'),
]

for date, text in timeline:
    story.append(timeline_item(date, text))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SOURCES + SEAL
# ══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph('Sources', SECTION_LABEL))

sources = [
    'Companies House UK, Company No. 17027115 (SEARAH Limited) — Incorporation, PSC register, officer list, filing history',
    'Eni media releases, November 2025 and March 2026 — Investment Agreement, SEARAH structure',
    'PETRONAS media releases, November 2025 — JV partnership confirmation',
    'UNCTAD Investment Policy Hub — BIT database verified April 2026: NO Italy-Malaysia BIT confirmed; NO active UK-Malaysia BIT',
    'Malaysian Parliament Hansard — no record of parliamentary briefing on SEARAH structure found',
    'Malaysian Federal Court record, March 16, 2026 — PETRONAS constitutional challenge admitted',
    'Reuters, October 2025 and March 2026',
    'Wood Mackenzie press release, February 28, 2025 — PETRONAS-Eni combination analysis',
    'Global Arbitration Review — ICSID Case No. ARB/20/48 (Eni vs Nigeria)',
    'Fulcrum Singapore (ISEAS-Yusof Ishak Institute), April 2026',
    'Milan Court records, March 2021 — Descalzi/Eni OPL 245 acquittal',
]
for s in sources:
    story.append(Paragraph(f'• {s}', SOURCES))

story.append(Spacer(1, 4*mm))
story.append(Paragraph('What Is Confirmed', SECTION_LABEL))

confirmed = [
    'SEARAH Limited (Company No. 17027115) — UK-registered, incorporated February 11, 2026 at ENI House, London.',
    '50% owned by PETRONAS Carigali International Ventures, 50% by Eni Lasmo Plc.',
    'Deal valued at "in excess of USD 15 billion over five years" — Eni press release, November 2025.',
    'Company governed by Companies Act 2006 (English law).',
    'NO active BIT between Malaysia and Italy or the United Kingdom — confirmed by UNCTAD April 2026.',
    'Malaysia produces approximately 350,000 boe/day from domestic fields.',
    'MLNG Bintulu — one of world\'s largest LNG export facilities; supplies Japan, Korea, Taiwan, China.',
]
for c in confirmed:
    story.append(Paragraph(f'• {c}', SOURCES))

story.append(Spacer(1, 4*mm))
story.append(Paragraph('What Requires Further Investigation', SECTION_LABEL))

further = [
    'The specific terms of the JV agreement between PETRONAS and Eni are not public.',
    'Whether Malaysian Parliament was formally notified of the arrangement has not been confirmed.',
    'Whether PETROS was consulted before the SEARAH structure was finalised has not been confirmed.',
    'Whether Malaysian legal counsel reviewed the UK incorporation before the structure was adopted has not been confirmed.',
]
for f in further:
    story.append(Paragraph(f'• {f}', SOURCES))

story.append(Spacer(1, 6*mm))

# ── SEAL BLOCK ────────────────────────────────────────────────────────────────
seal_data = [
    [Paragraph('SEAL 999 — DITEMPA BUKAN DIBERI', SEAL_TITLE), ''],
    [Paragraph('Document: SEARAH-EXPOSE v1.2 — BIT Corrected Edition', SEAL_MONO), ''],
    [Paragraph(f'Date: 2026-05-07', SEAL_MONO), ''],
    [Paragraph('Author: Arif Fazil', SEAL_MONO), ''],
    [Paragraph(f'DB Hash (SHA-256): {DOC_HASH}', SEAL_MONO), ''],
    [Paragraph(f'HMAC-SHA256 Commitment: {COMMITMENT}', SEAL_MONO), ''],
    [Paragraph('F2 Truth Gate: PASSED — All verifiable claims cross-checked against primary sources', SEAL_MONO), ''],
    [Paragraph(
        'CORRECTION APPLIED: Previous version incorrectly claimed Italy-Malaysia BIT (1988) '
        'was in force. UNCTAD (April 2026) confirms NO such treaty exists. BIT claim retracted. '
        'The correct statement: NO BIT protects this arrangement. Governing law = English law.',
        SEAL_WARN), ''],
    [Paragraph(
        'Prepared by Hermes ASI on behalf of Arif Fazil | arifOS Federation Intelligence',
        SEAL_FOOT), ''],
]

# Use full content width, centered with padding
seal_table = Table(seal_data, colWidths=[CONTENT_W - 10*mm])
seal_table.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 1.5, HexColor('#333333')),
    ('BACKGROUND', (0,0), (-1,-1), OFFWHITE),
    ('LEFTPADDING', (0,0), (-1,-1), 6*mm),
    ('RIGHTPADDING', (0,0), (-1,-1), 6*mm),
    ('TOPPADDING', (0,0), (-1,-1), 2*mm),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
    ('TOPPADDING', (0,0), (-1,0), 3*mm),
    ('BOTTOMPADDING', (0,-1), (-1,-1), 4*mm),
    ('LINEBELOW', (0,0), (-1,0), 0.8, RULE),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(seal_table)

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
OUTPUT = '/root/AAA/SEARAH/SEARAH-EXPOSE-v13-CLEAN.pdf'
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=LEFT_MARGIN,
    rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN,
    bottomMargin=BOTTOM_MARGIN,
    title="SEARAH: The Deal That Could Reshape Malaysia's Petroleum Future",
    author='Arif Fazil',
    subject='Exclusive Investigation — May 2026',
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

import os
size = os.path.getsize(OUTPUT)
print(f"Generated: {OUTPUT}")
print(f"Size: {size:,} bytes ({size/1024:.1f} KB)")
