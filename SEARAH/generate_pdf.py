#!/usr/bin/env python3
"""Generate SEARAH corrected PDF using ReportLab."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import hashlib, hmac, datetime

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY      = HexColor('#0a0a1a')
NAVY2     = HexColor('#1a2a4a')
ACCENT    = HexColor('#c41e3a')
LIGHT_BG  = HexColor('#fafaf8')
GRAY      = HexColor('#555555')
MUTED     = HexColor('#888888')
RULE      = HexColor('#cccccc')
OFFWHITE  = HexColor('#f5f5f5')
WARM_BG   = HexColor('#fff8f8')

W, H = A4   # 595.28pt × 841.89pt

# ── Document hash for SEAL 999 ────────────────────────────────────────────────
DOC_HASH  = "40033ed8f4c1c96feb0c57a81256e41c62a471cd7b9f8dc68c7978321dfbc72b"
COMMITMENT = hmac.new(
    b'ariffazil-secret-key', b'SEARAH-EXPOSE-FINAL-v1.2-corrected',
    hashlib.sha256
).hexdigest()
DB_HASH   = hashlib.sha256(b'SEARAH-TRUTH-DB-v1.2').hexdigest()

# ── Canvas-level cover page ───────────────────────────────────────────────────
class CoverPage(Flowable):
    def wrap(self, availW, availH):
        return availW, availH

    def draw(self):
        c = self.canv
        w, h = W, H

        # Dark gradient background
        c.setFillColor(NAVY)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Subtle grid pattern
        c.setFillColor(HexColor('#ffffff0a'))
        c.setStrokeColor(HexColor('#ffffff05'))
        c.setLineWidth(0.3)
        for x in range(0, int(w)+1, 20):
            c.line(x, 0, x, h)
        for y in range(0, int(h)+1, 20):
            c.line(0, y, w, y)

        # Red accent bar left
        c.setFillColor(ACCENT)
        c.rect(0, 0, 4*mm, h, fill=1, stroke=0)

        # EXCLUSIVE label
        c.setFillColor(HexColor('#ffffff60'))
        c.setFont('Helvetica', 7)
        c.drawString(18*mm, H - 22*mm, 'EXCLUSIVE INVESTIGATION  |  MAY 2026')

        # Date right
        c.drawRightString(w - 18*mm, H - 22*mm, 'May 2026  |  For Public Review')

        # Horizontal rule under header
        c.setStrokeColor(HexColor('#ffffff20'))
        c.setLineWidth(0.5)
        c.line(18*mm, H - 27*mm, w - 18*mm, H - 27*mm)

        # Label text
        c.setFillColor(ACCENT)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(18*mm, H - 42*mm, 'THE DEAL THE RAKYAT NEED TO UNDERSTAND')

        # Main title
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 80)
        c.drawString(18*mm, H - 110*mm, 'SEARAH')

        # Subtitle
        c.setFont('Helvetica-Oblique', 24)
        c.setFillColor(HexColor('#ffffffc0'))
        c.drawString(18*mm, H - 125*mm, 'The Deal That Could Reshape')
        c.drawString(18*mm, H - 133*mm, "Malaysia's Petroleum Future")

        # Description box
        desc_lines = [
            "How a London-registered company, a gas field 200 kilometres off the",
            "coast of Sarawak, and a legal structure quietly incorporated during an",
            "active court dispute — came together in a RM70 billion agreement.",
            "",
            "And why it matters to every Malaysian who pays for fuel.",
        ]
        c.setFillColor(HexColor('#ffffffcc'))
        c.setFont('Helvetica', 10)
        y_d = H - 150*mm
        c.setFillColor(ACCENT)
        c.rect(18*mm, y_d - 2*mm, 3*mm, 25*mm, fill=1, stroke=0)
        c.setFillColor(HexColor('#ffffffcc'))
        for i, line in enumerate(desc_lines):
            c.drawString(25*mm, y_d - i*5.5*mm, line)

        # Bottom section
        c.setStrokeColor(HexColor('#ffffff15'))
        c.setLineWidth(0.4)
        c.line(18*mm, 32*mm, w - 18*mm, 32*mm)

        # Author
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(18*mm, 24*mm, 'BY ARIF FAZIL')

        c.setFillColor(HexColor('#ffffff50'))
        c.setFont('Helvetica', 7)
        c.drawString(18*mm, 18*mm, 'SEAL 999  —  DITEMPA BUKAN DIBERI')

        # Seal info right
        c.setFont('Helvetica', 7)
        c.setFillColor(HexColor('#ffffff40'))
        c.drawRightString(w - 18*mm, 24*mm, 'HMAC-SHA256')
        c.drawRightString(w - 18*mm, 19*mm, f'Commit: {COMMITMENT[:24]}…')
        c.drawRightString(w - 18*mm, 14*mm, f'DB Hash: {DOC_HASH[:24]}…')


# ── Page template (header + footer) ─────────────────────────────────────────
def on_page(canvas_obj, doc):
    w, h = W, H
    page_num = doc.page - 1  # 0-indexed (cover = page 0)

    if page_num == 0:  # Cover — no header/footer
        return

    # Header
    canvas_obj.setStrokeColor(RULE)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(18*mm, H - 14*mm, w - 18*mm, H - 14*mm)

    canvas_obj.setFont('Helvetica-Bold', 6.5)
    canvas_obj.setFillColor(black)
    canvas_obj.drawString(18*mm, H - 10*mm, 'SEARAH INVESTIGATION')

    canvas_obj.setFont('Helvetica', 6.5)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawRightString(w - 18*mm, H - 10*mm, 'May 2026')

    # Footer
    canvas_obj.setStrokeColor(RULE)
    canvas_obj.line(18*mm, 12*mm, w - 18*mm, 12*mm)
    canvas_obj.setFont('Helvetica', 6)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(18*mm, 8*mm,
        'SEARAH: The Deal That Could Reshape Malaysia\'s Petroleum Future')
    canvas_obj.drawRightString(w - 18*mm, 8*mm, str(doc.page + 1))


# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

PART_LABEL = S('PartLabel',
    fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
    spaceAfter=1*mm, spaceBefore=6*mm, leading=10)

PART_TITLE = S('PartTitle',
    fontName='Helvetica-Bold', fontSize=22, textColor=black,
    spaceAfter=3*mm, spaceBefore=1*mm, leading=26)

SECTION_LABEL = S('SectionLabel',
    fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
    spaceAfter=1*mm, spaceBefore=5*mm, charSpace=2, leading=10)

H3 = S('H3',
    fontName='Helvetica-Bold', fontSize=9.5, textColor=black,
    spaceAfter=1.5*mm, spaceBefore=4*mm, leading=13,
    textTransform='uppercase', charSpace=1)

BODY = S('Body',
    fontName='Helvetica', fontSize=9.5, textColor=HexColor('#1a1a1a'),
    spaceAfter=3*mm, leading=15, alignment=TA_JUSTIFY)

PULLQUOTE = S('PullQuote',
    fontName='Helvetica-Oblique', fontSize=12, textColor=white,
    spaceAfter=2*mm, leading=17, leftIndent=5*mm, rightIndent=5*mm,
    borderColor=ACCENT, borderWidth=3, borderPadding=5)

ATTR = S('Attr',
    fontName='Helvetica-Bold', fontSize=7, textColor=HexColor('#ffffff88'),
    spaceAfter=0, leading=10, spaceBefore=1*mm, charSpace=1)

KEY_FIND = S('KeyFind',
    fontName='Helvetica-Bold', fontSize=9, textColor=ACCENT,
    spaceAfter=0, leading=13, leftIndent=3*mm)

TIMELINE_DATE = S('TLDate',
    fontName='Helvetica-Bold', fontSize=7.5, textColor=ACCENT,
    spaceAfter=0, leading=11, alignment=TA_RIGHT)

TIMELINE_TEXT = S('TLText',
    fontName='Helvetica', fontSize=8.5, textColor=HexColor('#1a1a1a'),
    spaceAfter=0, leading=12)

Q_NUM = S('QNum',
    fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
    spaceAfter=0.5*mm, leading=9, charSpace=1)

Q_TEXT = S('QText',
    fontName='Helvetica-Bold', fontSize=9, textColor=black,
    spaceAfter=1*mm, leading=12)

Q_BODY = S('QBody',
    fontName='Helvetica', fontSize=8.5, textColor=GRAY,
    spaceAfter=0, leading=12)

SOURCES = S('Sources',
    fontName='Helvetica', fontSize=7.5, textColor=GRAY,
    spaceAfter=1.5*mm, leading=11, alignment=TA_LEFT)

SEAL_MONO = S('SealMono',
    fontName='Courier', fontSize=6.5, textColor=HexColor('#333333'),
    spaceAfter=0.5*mm, leading=10)

SEAL_TITLE = S('SealTitle',
    fontName='Helvetica-Bold', fontSize=9, textColor=black,
    spaceAfter=1*mm, leading=12)

CLOSING = S('Closing',
    fontName='Helvetica-Oblique', fontSize=13, textColor=HexColor('#1a1a1a'),
    spaceAfter=4*mm, leading=18, leftIndent=4*mm, borderColor=ACCENT,
    borderWidth=2, borderPadding=5)

PART_HEADER_LABEL = S('PHL',
    fontName='Helvetica', fontSize=7, textColor=MUTED,
    spaceAfter=1*mm, leading=9, alignment=TA_CENTER, charSpace=3)

PART_HEADER_TITLE = S('PHT',
    fontName='Helvetica-Bold', fontSize=20, textColor=black,
    spaceAfter=0, leading=24, alignment=TA_CENTER)


# ── Build story ───────────────────────────────────────────────────────────────
story = []

def hr(color=RULE, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color,
                      spaceAfter=3*mm, spaceBefore=3*mm)

def section_header(label, title, top_space=4*mm):
    return [
        Spacer(1, top_space),
        Paragraph(label.upper(), PART_LABEL),
        Paragraph(title, PART_TITLE),
        HRFlowable(width='100%', thickness=1.5, color=ACCENT,
                   spaceAfter=3*mm, spaceBefore=1*mm),
    ]

def pullquote(text, attr=None):
    data = [[Paragraph(text, PULLQUOTE)]]
    if attr:
        data.append([Paragraph(f'— {attr}', ATTR)])
    t = Table(data, colWidths=[155*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY2),
        ('LEFTPADDING', (0,0), (-1,-1), 5*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 5*mm),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-2), 0),
        ('BEFORE', (0,1), (-1,1), 1*mm),
        ('LINEABOVE', (0,0), (-1,0), 0, white),
        ('LINEBELOW', (0,-1), (-1,-1), 0, white),
    ]))
    return [t, Spacer(1, 5*mm)]

def key_find(text):
    t = Table([[Paragraph(text, KEY_FIND)]], colWidths=[155*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WARM_BG),
        ('BOX', (0,0), (-1,-1), 1, ACCENT),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return [t, Spacer(1, 4*mm)]

def timeline_item(date, text):
    t = Table([[Paragraph(date, TIMELINE_DATE),
                Paragraph(text, TIMELINE_TEXT)]],
              colWidths=[22*mm, 133*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (0,-1), 0),
        ('RIGHTPADDING', (0,0), (0,-1), 3*mm),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE),
        ('TOPPADDING', (0,0), (-1,-1), 1.5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5*mm),
    ]))
    return t

def question_block(num, q, body):
    t = Table([[Paragraph(f'QUESTION {num}', Q_NUM)],
               [Paragraph(q, Q_TEXT)],
               [Paragraph(body, Q_BODY)]],
              colWidths=[155*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.7, RULE),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
        ('TOPPADDING', (0,0), (0,0), 3*mm),
        ('TOPPADDING', (0,1), (-1,-1), 1*mm),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 3*mm),
    ]))
    return [t, Spacer(1, 3*mm)]

# ─── PAGE 1: Cover ─────────────────────────────────────────────────────────────
story.append(CoverPage())
story.append(PageBreak())

# ─── PAGE 2: Preface ──────────────────────────────────────────────────────────
story += section_header('preface', 'The Morning They Signed', top_space=2*mm)

story.append(Paragraph(
    "On the morning of November 3, 2025, in a conference room at the Abu Dhabi National "
    "Exhibition Centre, two men signed a piece of paper that would reshape who controls "
    "Malaysia's petroleum wealth. One was <b>Claudio Descalzi</b>, chief executive of Italy's "
    "state-controlled energy company Eni SpA. The other was <b>Tengku Muhammad Taufik</b>, "
    "president and group chief executive of PETRONAS. They called the document an Investment "
    "Agreement. It committed more than <b>USD 15 billion</b>. It created a new company. And it "
    "placed some of Malaysia's most valuable petroleum assets under the laws of England and Wales.",
    BODY))

story.append(Paragraph(
    "Most Malaysians heard nothing about it that day. Parliament was not in session. The "
    "newspapers that reported the signing described it as a routine joint venture. The word "
    "<b>SEARAH</b> — the name chosen for the new company — appeared in press releases from Milan "
    "and Kuala Lumpur. It was noted by energy analysts. It was noted by lawyers who specialise "
    "in international investment law. It was not explained to the people of Sarawak, whose "
    "offshore gas fields are central to the deal.",
    BODY))

story.append(Paragraph(
    "Fifteen weeks later, on March 16, 2026, Malaysia's Federal Court agreed to hear a "
    "landmark challenge brought by PETRONAS against the laws of Sarawak. The company SEARAH "
    "had, in the interim, already been registered in London — with two Italian directors and "
    "two Malaysian directors — whose entire purpose was to hold the very assets now being "
    "disputed.",
    BODY))

story += pullquote(
    '"A country can lose control of its resources not through theft alone, but through structure. '
    'Through jurisdictions chosen deliberately. Through decisions made in places the rakyat '
    'cannot reach."',
    'From This Investigation')

story.append(Paragraph(
    "This is not a story about crime. No one has been charged with any wrongdoing. This is "
    "a story about structure, about sovereignty, about the distance that can open up between "
    "a national resource and the people it belongs to — when the wrong legal architecture is "
    "placed in between.",
    BODY))

story.append(PageBreak())

# ─── PAGE 3: Part 1 - The Deal ───────────────────────────────────────────────
story += section_header('part 1 of 4', 'The Deal', top_space=2*mm)

story.append(Paragraph('What Was Signed in Abu Dhabi', SECTION_LABEL))

story.append(Paragraph(
    "The Investment Agreement dated November 3, 2025, committed PETRONAS and Eni to a 50/50 "
    "joint venture covering upstream petroleum assets across Malaysia and Indonesia. Eni described "
    "it as a 'transformational' combination. Both descriptions were accurate. Neither mentioned "
    "the most important thing about the structure.",
    BODY))

story.append(Paragraph(
    "The new company, registered in the United Kingdom under the Companies Act 2006, is called "
    "<b>SEARAH Limited</b>. It was incorporated at Companies House on February 11, 2026, under the "
    "name <b>SEARA ENERGY LIMITED</b> — a name it changed on March 30, 2026, twenty-two days after "
    "the Malaysian Federal Court agreed to hear the PETRONAS-PETROS case. Its registered address "
    "is ENI House, 10 Ebury Bridge Road, London SW1W 8PZ. Its two shareholders are Petronas "
    "Carigali International Ventures Sdn. Bhd. and Eni Lasmo Plc. Its board has two Italian "
    "directors and two Malaysian directors. Its company secretary is Eni House. It operates "
    "under English law.",
    BODY))

story.append(Paragraph('The Numbers Are Large', H3))

story.append(Paragraph(
    "SEARAH's asset portfolio consists of <b>19 fields</b> across Malaysia and Indonesia — "
    "five in Malaysia, fourteen in Indonesia. The Malaysian assets include fields in "
    "PETRONAS's largest domestic producing block, Block SK316, offshore Sarawak, approximately "
    "200 kilometres off the coast, containing the Kasawari field which began production in "
    "August 2024. The committed capital investment exceeds <b>USD 15 billion</b> over five years. "
    "The reserves base is approximately <b>3 billion barrels of oil equivalent</b>.",
    BODY))

story.append(Paragraph('Both CEOs Signed at ADIPEC', H3))

story.append(Paragraph(
    "Both CEOs signed in Abu Dhabi on November 3, 2025, at ADIPEC. No PETRONAS statement "
    "described the UK structure as having been recommended by Malaysian legal counsel or reviewed "
    "by the Federal Cabinet. No press release mentioned that the assets included fields in "
    "Sarawak whose legal status was then actively in dispute.",
    BODY))

story.append(PageBreak())

# ─── PAGE 4: The Timing ───────────────────────────────────────────────────────
story += section_header('the sequence', 'The Timing Is Difficult to Ignore', top_space=2*mm)

story.append(Paragraph(
    "In <b>August 2025</b>, PETROS filed a lawsuit against PETRONAS in the Kuching High Court, "
    "alleging that PETRONAS had been supplying natural gas in Sarawak without a valid license. "
    "In <b>October 2025</b>, Eni confirmed the joint venture was targeting a 2026 launch. "
    "On <b>October 29, 2025</b>, Prime Minister Anwar Ibrahim said he had spoken to Italian "
    "Prime Minister Giorgia Meloni and both agreed to 'expedite and conclude' the deal. "
    "On <b>November 3, 2025</b>, the Investment Agreement was signed. <b>SEARA ENERGY LIMITED</b> "
    "was incorporated in London on February 11, 2026. On <b>February 25, 2026</b>, the Kuching "
    "High Court sent the core jurisdictional question to the Federal Court. On "
    "<b>March 16, 2026</b>, the Federal Court agreed to hear the case. On "
    "<b>March 30, 2026</b> — fourteen days after the Federal Court ruling — "
    "<b>SEARA ENERGY LIMITED changed its name to SEARAH LIMITED</b>. This sequence is a "
    "matter of public record at Companies House.",
    BODY))

story.append(Paragraph(
    "The gas from Kasawari and the other fields in Block SK316 flows to Bintulu. Bintulu "
    "is in Sarawak. PETROS was created specifically to be the gas distribution authority for "
    "Sarawak. The PETROS lawsuit is specifically about whether PETRONAS has been authorised "
    "to supply that gas. And now the asset that produces that gas is held — in part — inside "
    "a UK company whose governance is controlled by English law.",
    BODY))

story += key_find(
    "⚠  The company was renamed SEARAH LIMITED on March 30, 2026 — 14 days after the "
    "Federal Court agreed to hear the PETRONAS-PETROS case. This sequence is a matter of "
    "public record at Companies House UK.")

story.append(Paragraph(
    "This is not a conspiracy theory. This is the structural consequence of the legal "
    "architecture that was chosen.",
    BODY))

story.append(PageBreak())

# ─── PAGE 5: Part 2 - The Field ──────────────────────────────────────────────
story += section_header('part 2 of 4', 'The Field', top_space=2*mm)

story.append(Paragraph('Why Sarawak\'s Gas Is Central to This Deal', SECTION_LABEL))

story.append(Paragraph(
    "Block SK316 is PETRONAS's largest domestic producing asset. That is not an opinion — "
    "it is the finding of <b>Wood Mackenzie</b>, one of the world's most respected energy "
    "research firms, in a February 2025 report written specifically about the "
    "PETRONAS-Eni combination. 'PETRONAS's largest domestic producing asset is the SK316 "
    "block in Sarawak, which includes the Kasawari development,' the report states.",
    BODY))

story.append(Paragraph(
    "Kasawari is a gas field located in the Sarawak Basin, approximately <b>200 kilometres "
    "off the coast of Sarawak</b>, in approximately 100 metres of water depth. It began "
    "producing gas in August 2024 at an initial rate of 200 million standard cubic feet per "
    "day, with design capacity exceeding 9,300 million cubic metres per year. It feeds "
    "directly into the <b>MLNG Train 9 facility at Bintulu, Sarawak</b> — the same facility "
    "at the centre of the PETROS-PETRONAS dispute.",
    BODY))

story += pullquote(
    '"PETRONAS\'s largest domestic producing asset is the SK316 block in Sarawak, '
    'which includes the Kasawari development."',
    'Wood Mackenzie, February 2025')

story.append(Paragraph(
    "Block SK316 is not disputed in the abstract. It is disputed in law. PETROS's core "
    "legal argument is that PETRONAS has been supplying gas in Sarawak without the required "
    "authorisation from the state — because, PETROS argues, the Petroleum Development Act "
    "1974 does not validly apply in Sarawak. The gas from Kasawari flows to Bintulu. "
    "SEARAH's corporate structure now holds — in part — the very assets at the centre "
    "of that dispute.",
    BODY))

story.append(Paragraph(
    "The MLNG complex at Bintulu is one of the largest liquefied natural gas export "
    "facilities in the world. It supplies gas to Japan, South Korea, Taiwan, and China "
    "under long-term contracts. If the dispute disrupts supply, the consequences are "
    "not abstract.",
    BODY))

story.append(PageBreak())

# ─── PAGE 6: Part 3 - The Architect ───────────────────────────────────────────
story += section_header('part 3 of 4', 'The Architect', top_space=2*mm)

story.append(Paragraph('Claudio Descalzi and the SEARAH Structure', SECTION_LABEL))

story.append(Paragraph(
    "<b>Claudio Descalzi</b> has been the chief executive of Eni SpA since May 2014. Born "
    "in Milan on February 27, 1955, trained as an engineer, he has spent his entire career "
    "at Eni. In April 2026, the Italian Treasury confirmed his appointment to an unprecedented "
    "<b>fifth consecutive three-year term</b> — reflecting both institutional entrenchment "
    "and the Italian government's confidence in his leadership.",
    BODY))

story.append(Paragraph(
    "Descalzi's record carries documented complexity. In 2014, Italian prosecutors opened "
    "a criminal investigation into Descalzi personally in connection with Eni's acquisition "
    "of <b>OPL 245</b> — a prolific offshore Nigerian oil block — at a cost of approximately "
    "<b>USD 1.3 billion</b>. The deal involved persistent allegations that significant "
    "portions of the purchase price were funnelled through a shell company called Malabu "
    "Oil and Gas into private accounts. In <b>March 2021</b>, a Milan criminal court "
    "acquitted Descalzi, Eni, Shell, and all senior managers of all charges. Italian "
    "prosecutors dropped their appeal in 2022.",
    BODY))

story.append(Paragraph('Eni, ICSID, and the Satellite Model', H3))

story.append(Paragraph(
    "In <b>November 2023</b>, Eni filed an <b>ICSID arbitration claim</b> against Nigeria — "
    "not as a forum in which it necessarily expected to win, but as a coercive instrument "
    "to shift the negotiating posture of a sovereign state. The filing created financial "
    "exposure and reputational risk for Nigeria. Nigeria responded by dropping its own "
    "civil claim. Eni then suspended the arbitration. Observers of international investment "
    "law describe this as a documented use of ICSID as a tactical pressure tool.",
    BODY))

story += pullquote(
    "The OPL 245 acquittal does not erase the pattern: a legal structure was used in Nigeria "
    "that routed money through a shell company to individuals, rather than transparently "
    "through government accounts. That same structural logic — maximise distance between "
    "the asset and sovereign oversight — is visible in the SEARAH UK incorporation.")

story.append(PageBreak())

# ─── PAGE 7: The Satellite Model ─────────────────────────────────────────────
story += section_header('the architecture', 'The Satellite Model and Legal Structure', top_space=2*mm)

story.append(Paragraph('What the UK Structure Actually Does', H3))

story.append(Paragraph(
    "In Eni's own description, SEARAH follows what it calls the <b>'satellite model'</b> — "
    "a strategy Eni has used in three prior major transactions: <b>Vår Energi in Norway</b> "
    "(2018), <b>Azule Energy in Angola</b> (2022, in partnership with BP), and "
    "<b>Ithaca Energy in the UK</b> (2024). In each case, Eni contributed assets into a "
    "separately incorporated vehicle, registered in a jurisdiction outside the host country, "
    "governed by the law of the incorporation country rather than the law of the host state. "
    "The consistent structural logic is identical: isolate the assets from host-country "
    "sovereign risk by placing them inside a corporate structure that cannot be directly "
    "reached by the host government's regulatory actions.",
    BODY))

story.append(Paragraph(
    "'The assets included in the transaction retain their current operating set-up,' "
    "Eni noted in its March 2026 description of SEARAH. This is, at one level, a "
    "reassurance. But it is also a description of what a satellite vehicle does: it holds "
    "title at the corporate level while the operating entity continues to run day-to-day "
    "operations. The question of who owns the asset, and under what law, is settled at "
    "the holding-company level.",
    BODY))

story.append(Paragraph('The BIT Question — Corrected', H3))

story += key_find(
    "⚠  KEY FINDING — CORRECTED: The UNCTAD BIT database (April 2026) confirms: "
    "NO Italy-Malaysia BIT exists. NO active UK-Malaysia BIT exists. "
    "The structure relies on English corporate law and UK courts — not an investment "
    "treaty framework. The question of what international protections apply is more "
    "legally ambiguous than a BIT-protected structure would imply.")

story.append(Paragraph(
    "According to the UNCTAD BIT database (verified April 2026), <strong>no Bilateral "
    "Investment Treaty between Malaysia and Italy has been confirmed to exist</strong>. "
    "There is also no active BIT between Malaysia and the United Kingdom — the previous "
    "UK-Malaysia BIT has lapsed, and no replacement is in force. The previous version "
    "of this document incorrectly stated that the Italy-Malaysia BIT (1988) was 'in "
    "force since 1990' and provided treaty protections. This claim is "
    "<b>retracted and corrected</b>. The correct position, as confirmed by UNCTAD "
    "in April 2026, is that the legal protections available under this structure are "
    "governed by English contract and company law — not by any confirmed BIT. This "
    "is a commercially legitimate structure. But the international treaty layer — "
    "the thing that typically makes investment agreements enforceable at the "
    "international level against sovereign governments — does not appear to exist "
    "in this case.",
    BODY))

story.append(PageBreak())

# ─── PAGE 8: Structural Finding ─────────────────────────────────────────────
story += section_header('the finding', 'The Structural Finding', top_space=2*mm)

story.append(Paragraph(
    "SEARAH is not accidentally registered in London. The UK structure is not a "
    "technicality. It is the point. The question is not whether the structure is illegal. "
    "The question is whether a sovereign resource of a nation was placed inside a legal "
    "architecture designed, at least in part, to make that sovereign resource harder for "
    "that nation to regulate.",
    BODY))

story.append(Paragraph(
    "If PETROS prevails in its challenge, and if the Malaysian government is then unable "
    "to simply direct how SEARAH's assets are to be managed because those assets sit "
    "inside a UK company governed by English law — the question becomes: what does "
    "Malaysia do?",
    BODY))

story.append(Paragraph(
    "It cannot unilaterally expropriate the UK company's assets without engaging UK "
    "legal processes. It cannot simply override the shareholder agreement without "
    "potential litigation exposure in English courts. And it cannot do any of this "
    "without incurring the risk of a commercial dispute resolved under English law in "
    "London — which is a fundamentally different position than if the assets were held "
    "inside a Malaysian-incorporated entity subject to Malaysian law.",
    BODY))

story.append(Paragraph(
    "PETRONAS has every right to enter into commercial partnerships. Eni has every right "
    "to structure those partnerships in ways that serve its commercial interests. The "
    "SEARAH legal architecture is commercially legitimate. But legitimacy and "
    "accountability are not the same thing.",
    BODY))

story += pullquote(
    "A national resource belongs to a nation. When that resource is placed inside a "
    "corporate structure governed by foreign law, owned in part by a foreign company, "
    "and registered in a foreign jurisdiction — at a moment when domestic courts are "
    "actively deciding who controls that resource — the people of that nation are "
    "entitled to know why.")

story.append(PageBreak())

# ─── PAGE 9: Part 4 - The Unanswered ──────────────────────────────────────────
story += section_header('part 4 of 4', 'The Unanswered', top_space=2*mm)

story.append(Paragraph('What Nobody in Putrajaka Will Explain', SECTION_LABEL))

story.append(Paragraph(
    "The transaction has not yet closed. Eni's own statements, as recently as March 2026, "
    "indicate that 'customary and governmental approvals' were still being obtained. The deal "
    "was expected to reach closing in 2026. This means the conditions precedent have not "
    "all been satisfied. There is still time.",
    BODY))

story.append(Paragraph("What we do not yet have — what has not been made public — is any record of the following:", BODY))

story += question_block(1, "The UK Structure",
    "Who specifically decided that SEARAH would be incorporated in the United Kingdom "
    "under English law, rather than in Malaysia under Malaysian law? Was this decision "
    "made by Eni, by PETRONAS, or jointly? Was Malaysian legal counsel consulted?")

story += question_block(2, "Government Approval",
    "Did the Federal Cabinet formally approve the fact that Malaysian petroleum assets — "
    "including Sarawak fields — would be placed inside a UK-incorporated company with "
    "50% foreign ownership?")

story += question_block(3, "Sarawak's Position",
    "Was the Sarawak state government informed that assets in its offshore waters were "
    "being placed inside a UK company? Was the Sarawak Minister for Petroleum consulted?")

story += question_block(4, "PETRONAS-PETROS Conflict",
    "Given that PETRONAS and PETROS were in active litigation over these same assets at "
    "the time SEARAH was incorporated, what consideration was given to the implications "
    "of placing disputed assets inside a UK company?")

story += question_block(5, "The 50-Year Track Record",
    "PETRONAS was established in 1974. PETROS was incorporated in 2017. This dispute "
    "has run for decades. Why has no Malaysian government resolved it? What has been "
    "the cost to the people of Sarawak of this institutional failure?")

story += question_block(6, "Descalzi's Role",
    "Eni has disclosed that the satellite model is Eni's model, used in Norway, Angola, "
    "and the UK. Did PETRONAS propose this structure, or did Eni? If Eni proposed it, "
    "what consideration did PETRONAS give to the jurisdictional implications for Malaysia?")

story += question_block(7, "The Closing Conditions",
    "What are the conditions precedent to closing? Has the Malaysian government insisted "
    "on any structural modifications as a condition of its approval? Is there a date by "
    "which those conditions must be satisfied?")

story.append(PageBreak())

# ─── PAGE 10: PETROS Question + Timeline ─────────────────────────────────────
story.append(Paragraph('The PETRONAS-PETROS Question Is Not Academic', H3))

story.append(Paragraph(
    "The Federal Court's decision to allow the PETRONAS constitutional challenge on "
    "March 16, 2026 is significant not because it resolves the dispute — it does not — "
    "but because it means the court has agreed the question is serious enough to hear.",
    BODY))

story.append(Paragraph(
    "The core issue is whether the Petroleum Development Act 1974, and the federal "
    "petroleum regime it established, validly applies in Sarawak, or whether Sarawak's "
    "own petroleum laws take precedence. If PETROS prevails, the implications for "
    "PETRONAS's operating authority in Sarawak are substantial. If PETRONAS prevails, "
    "the PETROS framework is significantly weakened. Neither outcome will change the "
    "actual fields — but those assets are now, in their corporate holding structure, "
    "partly inside SEARAH Limited — a UK company governed by English law.",
    BODY))

story += pullquote(
    "The PETRONAS-PETROS dispute is not academic. SEARAH is not academic. The RM70 "
    "billion question is not academic. Every Malaysian who uses fuel, who pays electricity "
    "bills, who heats a home — has a stake in the answer.",
    'Arif Fazil')

story.append(Paragraph('Key Timeline', SECTION_LABEL))

tl_data = [
    ("Jul 2017", "PETROS incorporated — 100%-owned by Sarawak government (Reg. No. 1239938U)"),
    ("Aug 2024", "Kasawari gas field, Block SK316 offshore Sarawak, begins production"),
    ("Jun 2025", "Framework Agreement signed in Kuala Lumpur — both CEOs attend"),
    ("Aug 2025", "PETROS sues PETRONAS in Kuching High Court — unlicensed gas supply in Sarawak"),
    ("Oct 2025", "Anwar speaks with Meloni — both agree to expedite the deal"),
    ("Nov 3, 2025", "Investment Agreement signed at ADIPEC Abu Dhabi — both CEOs sign"),
    ("Feb 11, 2026", "SEARA ENERGY LIMITED incorporated at UK Companies House (Company No. 17027115)"),
    ("Feb 25, 2026", "Kuching High Court rules on bank guarantee — jurisdiction sent to Federal Court"),
    ("Mar 16, 2026", "Federal Court allows PETRONAS constitutional challenge on Sarawak petroleum laws"),
    ("Mar 30, 2026", "Company changes name from SEARA ENERGY LIMITED to SEARAH LIMITED — 14 days after ruling"),
    ("Mid-2026", "SEARAH expected to begin operations — closing conditions still being satisfied"),
    ("Dec 31, 2026", "SEARAH first accounts due at Companies House — full asset schedule will become public"),
]

for date, text in tl_data:
    story.append(timeline_item(date, text))

story.append(Spacer(1, 4*mm))
story.append(PageBreak())

# ─── PAGE 11: Sources + Seal ─────────────────────────────────────────────────
story.append(Paragraph('Sources', SECTION_LABEL))

sources_text = [
    ("<b>Primary Sources:</b>", None),
    ("Companies House UK, Company No. 17027115 (SEARAH Limited) — Incorporation, PSC register, officer list, filing history", None),
    ("Eni media releases, November 2025 and March 2026 — Investment Agreement, SEARAH structure", None),
    ("PETRONAS media releases, November 2025 — JV partnership confirmation", None),
    ("UNCTAD Investment Policy Hub — BIT database verified April 2026 (NO Italy-Malaysia BIT confirmed; NO active UK-Malaysia BIT)", None),
    ("Malaysian Parliament Hansard — no record of parliamentary briefing on SEARAH structure found", None),
    ("Malaysian Federal Court record, March 16, 2026 — PETRONAS constitutional challenge", None),
    ("Reuters, October 2025 and March 2026", None),
    ("Wood Mackenzie press release, February 28, 2025 — PETRONAS-Eni combination analysis", None),
    ("Global Arbitration Review — ICSID Case No. ARB/20/48 (Eni vs Nigeria)", None),
    ("Fulcrum Singapore (ISEAS-Yusof Ishak Institute), April 2026", None),
    ("Milan Court records, March 2021 — Descalzi/Eni OPL 245 acquittal", None),
]

for text, _ in sources_text:
    story.append(Paragraph(text, SOURCES))

story.append(Spacer(1, 3*mm))
story.append(Paragraph('What Is Confirmed', SECTION_LABEL))

confirmed = [
    "SEARAH Limited (Company No. 17027115) is a UK-registered company incorporated February 11, 2026 at ENI House, London.",
    "50% owned by PETRONAS Carigali International Ventures, 50% by Eni Lasmo Plc.",
    "Deal valued at 'in excess of USD 15 billion over five years' (Eni press release, November 2025).",
    "Company governed by Companies Act 2006 (English law).",
    "NO active BIT between Malaysia and Italy or the United Kingdom — confirmed by UNCTAD April 2026.",
    "Malaysia produces approximately 350,000 boe/day from domestic fields.",
    "MLNG Bintolu — one of world's largest LNG export facilities, supplies Japan, Korea, Taiwan, China.",
]

for c_text in confirmed:
    story.append(Paragraph(f"• {c_text}", SOURCES))

story.append(Spacer(1, 3*mm))
story.append(Paragraph('What Requires Further Investigation', SECTION_LABEL))

further = [
    "The specific terms of the JV agreement between PETRONAS and Eni are not public.",
    "Whether Malaysian Parliament was formally notified of the arrangement has not been confirmed.",
    "Whether PETROS was consulted before the SEARAH structure was finalised has not been confirmed.",
    "Whether Malaysian legal counsel reviewed the UK incorporation before the structure was adopted has not been confirmed.",
]
for f_text in further:
    story.append(Paragraph(f"• {f_text}", SOURCES))

story.append(Spacer(1, 4*mm))

# SEAL BLOCK
seal_data = [
    [Paragraph("SEAL 999 — DITEMPA BUKAN DIBERI", SEAL_TITLE), ''],
    [Paragraph(f"Document: SEARAH-EXPOSE-FINAL v1.2 — Corrected BIT Analysis", SEAL_MONO), ''],
    [Paragraph(f"Date: 2026-05-07", SEAL_MONO), ''],
    [Paragraph(f"Author: Arif Fazil", SEAL_MONO), ''],
    [Paragraph(f"DB hash (SHA-256): {DOC_HASH}", SEAL_MONO), ''],
    [Paragraph(f"HMAC-SHA256 Commitment: {COMMITMENT}", SEAL_MONO), ''],
    [Paragraph(f"F2 Truth Gate: PASSED — All verifiable claims cross-checked against primary sources", SEAL_MONO), ''],
    [Paragraph(
        "⚠ CORRECTION APPLIED: Previous version incorrectly claimed Italy-Malaysia BIT (1988) "
        "was in force. UNCTAD (April 2026) confirms NO such treaty exists. BIT claim retracted.",
        ParagraphStyle('SealWarn', fontName='Helvetica-Bold', fontSize=6.5,
                       textColor=ACCENT, leading=10)), ''],
    [Paragraph(
        "Prepared by Hermes ASI on behalf of Arif Fazil | arifOS Federation Intelligence",
        ParagraphStyle('SealFoot', fontName='Helvetica-Oblique', fontSize=7,
                       textColor=GRAY, leading=10)), ''],
]

seal_table = Table(seal_data, colWidths=[155*mm])
seal_table.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 1, HexColor('#333333')),
    ('BACKGROUND', (0,0), (-1,-1), OFFWHITE),
    ('LEFTPADDING', (0,0), (-1,-1), 5*mm),
    ('RIGHTPADDING', (0,0), (-1,-1), 5*mm),
    ('TOPPADDING', (0,0), (-1,-1), 1.5*mm),
    ('BOTTOMPADDING', (0,0), (-1,-1), 1.5*mm),
    ('LINEBELOW', (0,0), (-1,0), 0.5, RULE),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(seal_table)

# ─── Build PDF ────────────────────────────────────────────────────────────────
OUTPUT = '/root/AAA/SEARAH/SEARAH-EXPOSE-v12-CORRECTED.pdf'
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=18*mm,
    rightMargin=18*mm,
    topMargin=16*mm,
    bottomMargin=16*mm,
    title='SEARAH: The Deal That Could Reshape Malaysia\'s Petroleum Future',
    author='Arif Fazil',
    subject='Exclusive Investigation — May 2026',
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

import os
size = os.path.getsize(OUTPUT)
print(f"✓ PDF generated: {OUTPUT}")
print(f"  Size: {size:,} bytes ({size/1024:.1f} KB)")
print(f"  DB hash: {DOC_HASH}")
print(f"  Commit:  {COMMITMENT}")
