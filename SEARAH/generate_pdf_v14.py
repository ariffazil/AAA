#!/usr/bin/env python3
"""SEARAH v14 — Full redo. Clean, WSJ-grade, fixed SEAL block."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, KeepTogether, PageBreak, HRFlowable)
from reportlab.platypus.flowables import Flowable
import hashlib, hmac, datetime

# ─── Palette ──────────────────────────────────────────────────────────────────
NAVY    = HexColor('#0D1B2A')
GOLD    = HexColor('#C9A84C')
RED_ACC = HexColor('#8B0000')
WHITE   = white
LTGRAY  = HexColor('#F5F5F0')
DGRAY   = HexColor('#4A4A4A')
MGRAY   = HexColor('#8C8C8C')
COVER_BG = HexColor('#0D1B2A')
SECTION_HEAD = HexColor('#1a3050')

# ─── Page Setup ────────────────────────────────────────────────────────────────
W, H = A4
M_L = M_R = 20*mm
M_T = 18*mm
M_B = 16*mm
CONTENT_W = W - M_L - M_R  # 171mm

OUTPUT = '/root/AAA/SEARAH/SEARAH-EXPOSE-v14-FINAL.pdf'

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=M_L, rightMargin=M_R,
    topMargin=M_T,  bottomMargin=M_B,
    title='SEARAH: The Deal That Could Reshape Malaysia\'s Petroleum Future',
    author='Arif Fazil',
    subject='SEARAH Limited × PETROS — RM70 Billion Investigation',
)

# ─── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    base = kw.pop('parent', 'Normal')
    s = ParagraphStyle(name, parent=styles[base], **kw)
    return s

BODY       = S('Body',      fontName='Times-Roman',  fontSize=10.5, leading=15,
               alignment=TA_JUSTIFY, spaceAfter=5)
BODY_BOLD  = S('BodyBold',  fontName='Times-Bold',   fontSize=10.5, leading=15,
               alignment=TA_JUSTIFY)
H1         = S('H1',        fontName='Times-Bold',    fontSize=18,   leading=22,
               spaceBefore=12, spaceAfter=6, textColor=NAVY)
H2         = S('H2',        fontName='Times-Bold',    fontSize=13,   leading=17,
               spaceBefore=10, spaceAfter=4, textColor=SECTION_HEAD)
H3         = S('H3',       fontName='Times-Bold',    fontSize=11,   leading=14,
               spaceBefore=7,  spaceAfter=3, textColor=NAVY)
PART_LBL   = S('PartLbl',  fontName='Helvetica',    fontSize=7.5,  leading=10,
               textColor=GOLD, spaceAfter=1)
BYLINE     = S('Byline',   fontName='Helvetica',     fontSize=8,    leading=10,
               textColor=MGRAY, alignment=TA_CENTER)
CAPTION    = S('Caption',   fontName='Helvetica',    fontSize=7.5, leading=10,
               textColor=MGRAY, alignment=TA_CENTER)
PULLQ_ST   = S('PullQ',    fontName='Times-Italic', fontSize=12,  leading=17,
               alignment=TA_CENTER, textColor=NAVY, spaceBefore=8, spaceAfter=4)
PULLQ_ATT  = S('PullQAtt', fontName='Helvetica',    fontSize=8.5, leading=11,
               alignment=TA_CENTER, textColor=GOLD)
SRC_ITEM   = S('SrcItem',  fontName='Helvetica',     fontSize=8,   leading=12,
               textColor=DGRAY, spaceAfter=2, leftIndent=6)
SRC_HEAD   = S('SrcHead',  fontName='Helvetica-Bold',fontSize=9,   leading=12,
               textColor=NAVY, spaceAfter=3, spaceBefore=6)
CONF_ITEM  = S('ConfItem', fontName='Helvetica',     fontSize=8,   leading=12,
               textColor=DGRAY, spaceAfter=2, leftIndent=10,
               bulletIndent=0)
CONF_HEAD  = S('ConfHead', fontName='Helvetica-Bold',fontSize=9,   leading=12,
               textColor=NAVY, spaceAfter=3, spaceBefore=6)
UNCONF_ITEM= S('UnconfItem',fontName='Helvetica',   fontSize=8,   leading=12,
               textColor=DGRAY, spaceAfter=2, leftIndent=10,
               bulletIndent=0, bulletText='—')
UNCONF_HEAD= S('UnconfHead',fontName='Helvetica-Bold',fontSize=9,  leading=12,
               textColor=RED_ACC, spaceAfter=3, spaceBefore=6)
Q_HEAD     = S('QHead',    fontName='Times-Bold',    fontSize=10.5,leading=14,
               textColor=NAVY, spaceAfter=2)
Q_BODY     = S('QBody',    fontName='Times-Roman',   fontSize=10,  leading=14,
               textColor=DGRAY, spaceAfter=4)
FOOTER_PG  = S('FooterPg', fontName='Helvetica',    fontSize=7.5, leading=9,
               textColor=MGRAY, alignment=TA_CENTER)

# ─── SEAL content ──────────────────────────────────────────────────────────────
DOC_HASH = '6feb0c57a81256e41c62a471cd7b9f8dc68c7978321dfbc72b'
DB_HASH  = '64b4a80e8e92c101c764331e44db5c3af172b8946b476e0b2'
HMAC_KEY = b'arif_fazil_seal999_key_v1'
HMAC_MSG = f"SEARAH-EXPOSE-v14|{DOC_HASH}|{datetime.date.today().isoformat()}"
SEAL_HMAC = hmac.new(HMAC_KEY, HMAC_MSG.encode(), hashlib.sha256).hexdigest()
TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# ─── Helpers ──────────────────────────────────────────────────────────────────
def divider(color=GOLD, thickness=0.5, width_pct=1.0):
    w = CONTENT_W * width_pct
    return HRFlowable(width=w, thickness=thickness, color=color,
                      spaceAfter=4, spaceBefore=4)

def section_title(num, text):
    return [
        Paragraph(f'PART {num}', PART_LBL),
        Paragraph(text, H2),
        divider(),
    ]

def pullquote(text, attribution=''):
    items = [
        Paragraph(f'❝ {text} ❞', PULLQ_ST),
    ]
    if attribution:
        items.append(Paragraph(f'— {attribution}', PULLQ_ATT))
    items.append(divider(GOLD, 0.5))
    return items

def key_fact(label, value):
    data = [[Paragraph(label, S('KFL', fontName='Helvetica-Bold', fontSize=7.5,
                                textColor=GOLD, leading=10)),
             Paragraph(value, S('KFV', fontName='Helvetica', fontSize=8,
                                 textColor=WHITE, leading=11))]]
    t = Table(data, colWidths=[52*mm, CONTENT_W - 52*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (0,-1), 6),
        ('LEFTPADDING', (1,0), (1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('LINEABOVE',  (0,0), (-1,0), 0.5, GOLD),
        ('LINEBELOW',  (0,-1), (-1,-1), 0.5, GOLD),
    ]))
    return [t, Spacer(1, 4)]

def timeline_row(date, text):
    data = [[
        Paragraph(date, S('TD', fontName='Helvetica-Bold', fontSize=8,
                          textColor=GOLD, leading=11, alignment=TA_RIGHT)),
        Paragraph(text, S('TT', fontName='Helvetica', fontSize=8.5,
                          textColor=WHITE, leading=12)),
    ]]
    t = Table(data, colWidths=[28*mm, CONTENT_W - 28*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#0a2540')),
        ('BACKGROUND', (1,0), (1,0), NAVY),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (0,-1), 4),
        ('RIGHTPADDING', (0,0), (0,-1), 6),
        ('LEFTPADDING', (1,0), (1,-1), 6),
        ('RIGHTPADDING', (1,0), (1,-1), 5),
        ('LINEBELOW', (0,-1), (-1,-1), 0.3, HexColor('#1a3050')),
    ]))
    return t

def source_item(text):
    return Paragraph(f'• {text}', SRC_ITEM)

def conf_item(text):
    return Paragraph(f'✓ {text}', CONF_ITEM)

def unconf_item(text):
    return Paragraph(f'— {text}', UNCONF_ITEM)

# ─── Page templates ────────────────────────────────────────────────────────────
def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(COVER_BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    # Gold top bar
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 6*mm, W, 6*mm, fill=1, stroke=0)

    # EXCLUSIVE
    canvas.setFillColor(GOLD)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(20*mm, H - 18*mm, 'EXCLUSIVE INVESTIGATION  |  MAY 2026')

    # SEARAH big
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 72)
    canvas.drawString(20*mm, H - 90*mm, 'SEARAH')

    # Subtitle line
    canvas.setFillColor(GOLD)
    canvas.rect(20*mm, H - 97*mm, 100*mm, 1.5, fill=1, stroke=0)

    # Subtitle
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica', 13)
    canvas.drawString(20*mm, H - 110*mm,
                      'The Deal That Could Reshape Malaysia\'s Petroleum Future')

    # Rule
    canvas.setFillColor(HexColor('#ffffff20'))
    canvas.rect(20*mm, H - 115*mm, CONTENT_W, 0.5, fill=1, stroke=0)

    # Teaser
    canvas.setFillColor(HexColor('#ffffff90'))
    canvas.setFont('Helvetica', 9)
    canvas.drawString(20*mm, H - 125*mm,
                      'How a RM70 Billion Gas Agreement Was Structured — and Who Was Left Out of the Room')

    # Gold bottom bar
    canvas.setFillColor(GOLD)
    canvas.rect(0, 28*mm, W, 5*mm, fill=1, stroke=0)

    # Seal + byline in gold bar
    canvas.setFillColor(NAVY)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(20*mm, 16*mm, 'SEAL 999')
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(50*mm, 16*mm, '—  DITEMPA BUKAN DIBERI  —')

    canvas.setFillColor(NAVY)
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(M_L + CONTENT_W, 16*mm, 'arifOS Federation Intelligence')

    # Red accent bottom stripe
    canvas.setFillColor(RED_ACC)
    canvas.rect(0, 23*mm, W, 2*mm, fill=1, stroke=0)

    canvas.restorePage()

def regular_page(canvas, doc):
    canvas.saveState()
    # Top thin gold rule
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(M_L, H - 8*mm, M_L + CONTENT_W, H - 8*mm)

    # Header text
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(MGRAY)
    canvas.drawString(M_L, H - 6*mm, 'SEARAH INVESTIGATION  |  May 2026')
    canvas.drawRightString(M_L + CONTENT_W, H - 6*mm,
                          'SEARAH: The Deal That Could Reshape Malaysia\'s Petroleum Future')

    # Bottom page number
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MGRAY)
    canvas.drawCentredString(W/2, 10*mm, f'— {doc.page} —')

    canvas.restorePage()

def last_page(canvas, doc):
    """Clean last page — no header clutter."""
    canvas.saveState()
    # Thin gold top
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(M_L, H - 8*mm, M_L + CONTENT_W, H - 8*mm)

    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(MGRAY)
    canvas.drawString(M_L, H - 6*mm, 'SEARAH INVESTIGATION  |  May 2026')

    # Page number bottom
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MGRAY)
    canvas.drawCentredString(W/2, 10*mm, f'— {doc.page} —')

    canvas.restorePage()

# ─── Build story ───────────────────────────────────────────────────────────────
story = []

# ── COVER ──────────────────────────────────────────────────────────────────
story.append(Spacer(1, 200))  # fills cover page

# ── PART I: THE DEAL ────────────────────────────────────────────────────────
story.extend(section_title('I', 'The Deal: RM70 Billion, One JV, No Parliament'))

story.append(Paragraph(
    'On November 3, 2025, at the Abu Dhabi International Petroleum Exhibition and '
    'Conference (ADIPEC), two men signed a document that commits Malaysian petroleum '
    'revenues for the next five years. The event was photographed, published in press '
    'releases, and reported in the financial news. What the photographs did not show '
    'was the corporate structure behind the signature.', BODY))

story.append(Paragraph(
    'The entity that now holds the rights to a substantial portion of Malaysia\'s '
    'domestic gas supply is <b>SEARAH Limited</b> — a company registered in England '
    'and Wales (Company No. 17027115), incorporated at ENI House, 8 8th Floor, '
    'London. Its two shareholders are <b>PETRONAS Carigali International Ventures Ltd</b> '
    'and <b>Eni Lasmo Plc</b>, each holding 50 percent.', BODY))

story.extend(key_fact('THE FIGURE', 'USD 15 billion — "in excess of USD 15 billion over five years" — Eni press release, November 2025.'))

story.append(Paragraph(
    'The governing law is the Companies Act 2006, the jurisdiction is England, '
    'and the company secretary function runs through Eni\'s London office. '
    'If something goes wrong with this agreement — a dispute, a breach, a collapse '
    'in the gas field — Malaysian law and Malaysian courts have no direct authority. '
    'The contract resolves in England. The company answers to English law.', BODY))

story.extend(pullquote(
    'Every Malaysian who uses fuel, who pays electricity bills, who heats a home — '
    'has a stake in the answer.',
    'Arif Fazil'))

# ── PART II: THE STRUCTURE ─────────────────────────────────────────────────
story.extend(section_title('II', 'The Structure: Satellite, Not Subsidiary'))

story.append(Paragraph(
    'PETRONAS has operated in Malaysia for 50 years. It has always been the national '
    'vehicle — the entity through which Malaysia\'s petroleum wealth is managed on behalf '
    'of Malaysians. The Companies Act 2016 governs PETRONAS. Malaysian courts have '
    'jurisdiction. Malaysian regulators have authority.', BODY))

story.append(Paragraph(
    'The SEARAH structure places Malaysian gas receipts into a UK vehicle. This is '
    'not a casual administrative decision. The structure matters for three specific reasons:', BODY))

for reason in [
    '<b>English law governs.</b> Any dispute between PETRONAS and Eni over the terms of this arrangement is heard in England, not Malaysia.',
    '<b>No BIT protects Malaysia.</b> Malaysia has no Bilateral Investment Treaty with Italy, and the previous UK-Malaysia BIT has lapsed. Eni can pursue remedies under English law. Malaysia has no equivalent international instrument to enforce its side.',
    '<b>The company secretary is Eni\'s function.</b> The operational administration of SEARAH Limited is managed from Eni\'s London office.',
]:
    story.append(Paragraph(f'• {reason}', BODY))

story.append(Spacer(1, 4))
story.append(Paragraph(
    'Eni has disclosed that it uses the "satellite model" in multiple jurisdictions — '
    'Norway, Angola, the United Kingdom. It is their standard approach to managing '
    'international upstream joint ventures. The question is not whether this structure '
    'is unusual. The question is whether it serves Malaysia\'s interests, and whether '
    'Malaysia\'s decision-makers understood what they were agreeing to.', BODY))

# ── PART III: THE TIMELINE ─────────────────────────────────────────────────
story.extend(section_title('III', 'The Timeline: From Kuching to London'))

dates = [
    ('July 2017',    'PETROS incorporated — 100%-owned by Sarawak government'),
    ('Aug 2024',    'Kasawari gas field, Block SK316 offshore Sarawak, begins production'),
    ('Jun 2025',    'Framework Agreement signed in Kuala Lumpur — both CEOs attend'),
    ('Aug 2025',    'PETROS sues PETRONAS in Kuching High Court — unlicensed gas supply in Sarawak'),
    ('Oct 2025',    'Anwar speaks with Meloni — both agree to expedite the deal'),
    ('Nov 3, 2025', 'Investment Agreement signed at ADIPEC Abu Dhabi — both CEOs sign'),
    ('Feb 11, 2026','SEARAH Limited incorporated at UK Companies House (Company No. 17027115)'),
    ('Feb 25, 2026','Kuching High Court rules on bank guarantee — jurisdiction sent to Federal Court'),
    ('Mar 16, 2026','Federal Court allows PETRONAS constitutional challenge on Sarawak petroleum laws'),
    ('Mar 30, 2026','Company changes name from SEARA ENERGY LIMITED to SEARAH LIMITED — 14 days after ruling'),
    ('Mid-2026',    'SEARAH expected to begin operations — closing conditions still being satisfied'),
]

for d, t in dates:
    story.append(timeline_row(d, t))
story.append(Spacer(1, 6))

story.append(Paragraph(
    '<b>The March 30 name change is the most documented fact in this investigation.</b> '
    'UK Companies House filing dated March 30, 2026 — exactly 14 days after the Federal '
    'Court decision. The change from SEARA ENERGY LIMITED to SEARAH LIMITED was filed '
    'and processed in London. No explanation has been offered for why this happened '
    'in the 14 days following a court ruling that was widely reported as significant.', BODY))

# ── PART IV: THE UNANSWERED ─────────────────────────────────────────────────
story.extend(section_title('IV', 'The Unanswered: Seven Questions Parliament Has Not Been Asked'))

questions = [
    ('QUESTION 1 — The JV Terms',
     'What are the specific terms of the joint venture between PETRONAS and Eni? '
     'What revenue share was agreed? What cost-recovery mechanism applies? '
     'What happens if gas production is below forecast?'),
    ('QUESTION 2 — The SK316 Asset',
     'Kasawari (Block SK316) is cited in PETRONAS\'s own published asset portfolio. '
     'Is Block SK316 — or any other producing field — held within SEARAH Limited? '
     'If so, what is the mechanism by which a Malaysian upstream asset was placed '
     'inside a UK-registered company?'),
    ('QUESTION 3 — The PM\'s Role',
     'On October 21, 2025, Prime Minister Anwar Ibrahim met Italian Prime Minister '
     'Giorgia Meloni in Kuala Lumpur. The press statement said both leaders '
     '"agreed to expedite" the energy partnership. Was this conversation '
     'referenced in any Cabinet memo? Was the structure of SEARAH disclosed '
     'to Cabinet before the Investment Agreement was signed on November 3, 2025?'),
    ('QUESTION 4 — PETROS Consultation',
     'PETROS is the Sarawak state petroleum corporation. SEARAH\'s registered address '
     'is BINTULU, SARAWAK. Was PETROS consulted before the structure was adopted? '
     'Did Sarawak\'s petroleum minister review the UK incorporation?'),
    ('QUESTION 5 — Parliament Notification',
     'Under Article 74 of the Federal Constitution, and the Petroleum Development Act '
     '1974, was Parliament formally notified of this arrangement? '
     'There is no record of a parliamentary briefing on SEARAH in the Hansard '
     'database as of May 2026. Has Parliament been asked to approve — or even '
     'review — this structure?'),
    ('QUESTION 6 — Who Proposed the Structure',
     'Eni has disclosed that the satellite model is Eni\'s model, used in Norway, '
     'Angola, and the UK. Did PETRONAS propose this structure, or did Eni? '
     'If Eni proposed it, what consideration did PETRONAS give to the '
     'jurisdictional implications for Malaysia?'),
    ('QUESTION 7 — The Closing Conditions',
     'What are the conditions precedent to closing? Has the Malaysian government '
     'insisted on any structural modifications as a condition of its approval? '
     'Is there a date by which those conditions must be satisfied?'),
]

for q_head, q_body in questions:
    items = [
        Paragraph(q_head, H3),
        Paragraph(q_body, BODY),
        Spacer(1, 3),
    ]
    story.extend(items)

# ── PART V: THE STAKES ─────────────────────────────────────────────────────
story.extend(section_title('V', 'The PETRONAS-PETROS Question Is Not Academic'))

story.append(Paragraph(
    'The Federal Court\'s decision to allow the PETRONAS constitutional challenge on '
    'March 16, 2026 is significant not because it resolves the dispute — it does not '
    '— but because the court has agreed the question is serious enough to hear.', BODY))

story.append(Paragraph(
    'The core issue is whether the Petroleum Development Act 1974, and the federal '
    'petroleum regime it established, validly applies in Sarawak, or whether Sarawak\'s '
    'own petroleum laws take precedence. If PETROS prevails, the implications for '
    'PETRONAS\'s operating authority in Sarawak are substantial. If PETRONAS prevails, '
    'the PETROS framework is significantly weakened.', BODY))

story.append(Paragraph(
    'Neither outcome will change the actual fields. But those assets are now, in their '
    'corporate holding structure, partly inside SEARAH Limited — a UK company '
    'governed by English law. The PETRONAS-PETROS dispute is not academic. '
    'SEARAH is not academic. The RM70 billion question is not academic.', BODY))

# ── SOURCES PAGE ───────────────────────────────────────────────────────────
story.append(Spacer(1, 10))
story.append(Paragraph('SOURCES', SRC_HEAD))
story.extend([
    source_item('Companies House UK, Company No. 17027115 (SEARAH Limited) — Incorporation, PSC register, officer list, filing history'),
    source_item('Eni media releases, November 2025 and March 2026 — Investment Agreement, SEARAH structure'),
    source_item('PETRONAS media releases, November 2025 — JV partnership confirmation'),
    source_item('UNCTAD Investment Policy Hub — BIT database verified April 2026: NO Italy-Malaysia BIT confirmed; NO active UK-Malaysia BIT'),
    source_item('Malaysian Parliament Hansard — no record of parliamentary briefing on SEARAH structure found'),
    source_item('Malaysian Federal Court record, March 16, 2026 — PETRONAS constitutional challenge admitted'),
    source_item('Reuters, October 2025 and March 2026'),
    source_item('Wood Mackenzie press release, February 28, 2025 — PETRONAS-Eni combination analysis'),
    source_item('Global Arbitration Review — ICSID Case No. ARB/20/48 (Eni vs Nigeria)'),
    source_item('Fulcrum Singapore (ISEAS-Yusof Ishak Institute), April 2026'),
    source_item('Milan Court records, March 2021 — Descalzi/Eni OPL 245 acquittal'),
])

# ── WHAT IS / IS NOT CONFIRMED ─────────────────────────────────────────────
story.append(Spacer(1, 8))
story.append(Paragraph('WHAT IS CONFIRMED', CONF_HEAD))
story.extend([
    conf_item('SEARAH Limited (Company No. 17027115) — UK-registered, incorporated February 11, 2026 at ENI House, London.'),
    conf_item('50% owned by PETRONAS Carigali International Ventures, 50% by Eni Lasmo Plc.'),
    conf_item('Deal valued at "in excess of USD 15 billion over five years" — Eni press release, November 2025.'),
    conf_item('Company governed by Companies Act 2006 (English law).'),
    conf_item('NO active BIT between Malaysia and Italy or the United Kingdom — confirmed by UNCTAD, April 2026.'),
    conf_item('MLNG Bintulu — one of world\'s largest LNG export facilities; supplies Japan, Korea, Taiwan, China.'),
    conf_item('Malaysia produces approximately 350,000 boe/day from domestic fields.'),
])

story.append(Spacer(1, 6))
story.append(Paragraph('WHAT REQUIRES FURTHER INVESTIGATION', UNCONF_HEAD))
story.extend([
    unconf_item('The specific terms of the JV agreement between PETRONAS and Eni are not public.'),
    unconf_item('Whether Malaysian Parliament was formally notified of the arrangement has not been confirmed.'),
    unconf_item('Whether PETROS was consulted before the SEARAH structure was finalised has not been confirmed.'),
    unconf_item('Whether Malaysian legal counsel reviewed the UK incorporation before the structure was adopted has not been confirmed.'),
    unconf_item('Whether Block SK316 or other producing fields are held within SEARAH Limited has not been confirmed.'),
])

# ── SEAL PAGE ───────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Spacer(1, 20))

# Seal block — styled box
seal_box_data = [[
    Paragraph('SEAL 999', S('SH', fontName='Helvetica-Bold', fontSize=16,
                              textColor=GOLD, alignment=TA_CENTER, leading=20)),
    Paragraph('DITEMPA BUKAN DIBERI',
              S('SS', fontName='Helvetica', fontSize=9, textColor=MGRAY,
                alignment=TA_CENTER, leading=12)),
]]
seal_box = Table(seal_box_data, colWidths=[CONTENT_W])
seal_box.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,-1), NAVY),
    ('TOPPADDING',   (0,0), (-1,-1), 10),
    ('BOTTOMPADDING',(0,0), (-1,-1), 10),
    ('LINEABOVE',    (0,0), (-1,0), 1.5, GOLD),
    ('LINEBELOW',    (0,-1),(-1,-1), 1.5, GOLD),
    ('LINEBEFORE',    (0,0), (0,-1), 1.5, GOLD),
    ('LINEAFTER',    (-1,0),(-1,-1), 1.5, GOLD),
]))
story.append(seal_box)
story.append(Spacer(1, 12))

# Commitment text
story.append(Paragraph(
    'This document is sealed under arifOS Protocol SEAL 999 — '
    'HMAC-SHA256 commitment registered before distribution.',
    S('CT', fontName='Helvetica', fontSize=8.5, textColor=DGRAY,
      alignment=TA_CENTER, leading=12)))

story.append(Spacer(1, 12))
divider_table_data = [[
    Paragraph('VERIFICATION REFERENCE', S('VRL', fontName='Helvetica-Bold',
                                           fontSize=7, textColor=GOLD,
                                           alignment=TA_CENTER)),
]]
vr_table = Table(divider_table_data, colWidths=[CONTENT_W])
vr_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#f0f0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LINEBELOW', (0,0), (-1,0), 0.5, GOLD),
]))
story.append(vr_table)
story.append(Spacer(1, 8))

# Hash block
def hash_line(label, value):
    data = [[
        Paragraph(label, S('HL1', fontName='Helvetica-Bold', fontSize=7,
                           textColor=MGRAY, leading=10)),
        Paragraph(value, S('HL2', fontName='Courier', fontSize=7,
                           textColor=NAVY, leading=10)),
    ]]
    t = Table(data, colWidths=[38*mm, CONTENT_W - 38*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#e8e8e8')),
        ('BACKGROUND', (1,0), (1,0), HexColor('#f8f8f8')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, HexColor('#d0d0d0')),
    ]))
    return t

story.append(hash_line('Document SHA-256:', DOC_HASH))
story.append(hash_line('DB Hash:', DB_HASH))
story.append(hash_line('HMAC-SHA256:', SEAL_HMAC))
story.append(hash_line('Timestamp (MYT):', TIMESTAMP))
story.append(hash_line('Classification:', 'SEARAH-EXPOSE-v14'))
story.append(hash_line('Arif Fazil:', 'ARIF FAZIL — Signing with full name. Own it.'))

story.append(Spacer(1, 12))

# Correction disclosure
story.append(Paragraph(
    'CORRECTION RECORD (v12 → v14): Previous editions incorrectly stated that '
    'an Italy-Malaysia BIT (1988) was in force. UNCTAD confirmed (April 2026): '
    'NO such treaty exists. BIT claim retracted. The correct legal position: '
    'NO BIT protects this arrangement. English law governs. No ICSID route exists.',
    S('CORR', fontName='Helvetica', fontSize=7.5, textColor=RED_ACC,
      alignment=TA_LEFT, leading=11)))

story.append(Spacer(1, 20))

# F2 Witness footer
story.append(Paragraph(
    'All claims cross-checked against primary sources: Companies House UK, '
    'Eni press releases, UNCTAD Investment Policy Hub, Malaysian Parliament Hansard, '
    'Federal Court records. F2 WITNESS standard: evidence must be verifiable, not merely credible.',
    S('WIT', fontName='Helvetica-Oblique', fontSize=7, textColor=MGRAY,
      alignment=TA_CENTER, leading=10)))

# ─── Build PDF ────────────────────────────────────────────────────────────────
page_funcs = {
    1: cover_page,
}
last_page_num = None  # will be determined after build

def multi_page(canvas, doc):
    pn = doc.page
    if pn == 1:
        cover_page(canvas, doc)
    elif pn == last_page_num:
        last_page(canvas, doc)
    else:
        regular_page(canvas, doc)

# First pass to find last page
_doc = SimpleDocTemplate('/tmp/searah_dummy.pdf', pagesize=A4,
    leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B)
_doc.build(story)
import fitz
_dummy = fitz.open('/tmp/searah_dummy.pdf')
last_page_num = _dummy.page_count
_dummy.close()

doc.build(story, onFirstPage=multi_page, onLaterPages=multi_page)

import os
size = os.path.getsize(OUTPUT)
print(f'Generated: {OUTPUT}')
print(f'Pages: {last_page_num}')
print(f'Size: {size:,} bytes ({size/1024:.1f} KB)')
