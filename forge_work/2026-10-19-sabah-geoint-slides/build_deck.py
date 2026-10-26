#!/usr/bin/env python3
"""GEOX Sabah Regional Geological Intelligence — slide pack builder."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import os

BASE = "/root/AAA/forge_work/2026-10-19-sabah-geoint-slides"
FIG = f"{BASE}/fig"
OUT = f"{BASE}/out"
os.makedirs(OUT, exist_ok=True)

DARK = RGBColor(0x0A, 0x0A, 0x0F)
BLUE = RGBColor(0x2D, 0x5F, 0x8B)
BROWN = RGBColor(0x8B, 0x45, 0x13)
GOLD = RGBColor(0xFF, 0xD5, 0x4F)
WHITE = RGBColor(0xE8, 0xE6, 0xE3)
GREY = RGBColor(0x6B, 0x72, 0x80)
RED = RGBColor(0xC0, 0x39, 0x2B)
GREEN = RGBColor(0x2E, 0x8B, 0x57)
PANEL = RGBColor(0x12, 0x14, 0x1A)

def C(x):
    """Accept RGBColor or '#RRGGBB' hex string."""
    if isinstance(x, RGBColor):
        return x
    if isinstance(x, str):
        x = x.lstrip("#")
        return RGBColor(int(x[0:2],16), int(x[2:4],16), int(x[4:6],16))
    return RGBColor(0,0,0)


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = 13.333, 7.5

def bg(slide, color=DARK):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def box(slide, l, t, w, h, fill=PANEL, line=None, line_w=1.0):
    sh = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = C(fill)
    if line: sh.line.color.rgb = C(line); sh.line.width = Pt(line_w)
    else: sh.line.fill.background()
    return sh

def txt(slide, l, t, w, h, text, size=14, color=WHITE, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font="Calibri", italic=False):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = Emu(45720); tf.margin_right = Emu(45720)
    tf.margin_top = Emu(22860); tf.margin_bottom = Emu(22860)
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = line
        r.font.size = Pt(size); r.font.color.rgb = C(color)
        r.font.bold = bold; r.font.name = font; r.font.italic = italic
    return tb

def bullet(slide, l, t, w, h, lines, size=12, color=WHITE, gap=6):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.color.rgb = C(color); r.font.name = "Calibri"
    return tb

def banner(slide, text, t=0.12, size=9, color=GOLD):
    txt(slide, 0.3, t, W-0.6, 0.28, text, size=size, color=color, align=PP_ALIGN.CENTER, bold=True)

def footer(slide, page, total=14):
    txt(slide, 0.3, H-0.38, W-0.6, 0.26,
        f"PETRONAS INTERNAL · LOCAL ONLY · INTERPRETATION · PARTIAL · NOT SEALED     |     GEOX renders; ARIF adjudicates     |     {page}/{total}",
        size=8, color=GREY, align=PP_ALIGN.CENTER)

def title(slide, text, sub=None):
    txt(slide, 0.45, 0.42, W-0.9, 0.62, text, size=26, color=GOLD, bold=True)
    if sub: txt(slide, 0.45, 1.02, W-0.9, 0.38, sub, size=12, color=WHITE)

def pic(slide, name, l, t, w, h):
    slide.shapes.add_picture(f"{FIG}/{name}", Inches(l), Inches(t), Inches(w), Inches(h))

BAN = "PETRONAS INTERNAL · LOCAL ONLY · INTERPRETATION · PARTIAL · NOT SEALED"
BAN2 = ("AI_IMAGE_GENERATION: NOT AVAILABLE · EXTERNAL_IMAGE_GENERATION: BLOCKED_C28 · "
        "AI-READY CONCEPTUAL VISUAL LAYER · CURRENT IMPLEMENTATION: GOVERNED PROCEDURAL RENDER")

# ============ 1 COVER ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
box(s, 0, 0, W, 2.55, BLUE)
txt(s, 0.6, 0.55, W-1.2, 0.85, "GEOX SABAH REGIONAL", size=40, color=WHITE, bold=True)
txt(s, 0.6, 1.35, W-1.2, 0.6, "GEOLOGICAL INTELLIGENCE", size=30, color=GOLD, bold=True)
txt(s, 0.6, 1.95, W-1.2, 0.4, "East Sabah → Dangerous Grounds  ·  Regional Earth system / Basin domain / Local calibration",
    size=13, color=WHITE)
banner(s, BAN, t=2.72, size=11)
txt(s, 0.6, 3.15, W-1.2, 0.35, BAN2, size=8.5, color=GREY, align=PP_ALIGN.CENTER)
box(s, 0.6, 3.72, W-1.2, 0.95, PANEL, GOLD, 1.4)
txt(s, 0.8, 3.82, W-1.6, 0.8,
    "Build correctness is not Earth truth. GEOX renders; ARIF adjudicates.\n"
    "No model is canonical, preferred or closed. P, L and R are drawn with equal weight.",
    size=15, color=GOLD, align=PP_ALIGN.CENTER, bold=True, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.6, 4.85, W-1.2, 1.7,
    "THREE NESTED SCALES\n"
    "  SCALE 1 · Regional Sabah — East Sabah → Dangerous Grounds (this transect)\n"
    "  SCALE 2 · Basin / structural domain — Sabah Trough, toe thrust, thrust sheet, inboard, platform (BIF-KL6)\n"
    "  SCALE 3 · Local calibration — KB-KL2 Rotan–Maligan–Barton",
    size=13, color=WHITE)
txt(s, 0.6, 6.55, W-1.2, 0.5,
    "Sources: SRC-XS-PUB · SRC-BIF23-KL6 · v4.2 chronostrat · v4.1 RHG payload · v3.1 surface system (SRC-REST15) · SRC-ESDG-MODELS (hypotheses)",
    size=8.5, color=GREY)
footer(s, 1)

# ============ 2 EXECUTIVE RAIL ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN); title(s, "EXECUTIVE INTERPRETATION RAIL",
    "No single grand narrative: competing models are listed side by side; nothing here is adjudicated.")
rows = [
    ("DIRECTLY SUPPORTED", GREEN,
     "One composite seismic display (BIF-KL6) over NW Sabah Platform, Sabah Trough, toe-thrust and thrust-sheet domains: "
     "rugose platform seabed, flat trough floor ≈3800 ms, seabed rising SE toward shelf, offset reflectors in toe-thrust panel. "
     "Navigation, datum and depth absent."),
    ("LOCAL TO KB-KL2", BLUE,
     "Digitised horizons · Rotan-1 / Maligan-1 / Barton-2 ties (C20: Rotan SRU/H3 FAIL, Maligan SRU FAIL) · "
     "Block H operator horizons (H-series, H400 age unassigned) · restoration-pack chronology behind EVENT-C-S."),
    ("MAY BE REGIONAL", "#8B6B4A",
     "Shallowing-to-SE seabed trend and trough → toe-thrust → thrust-sheet → shelf domain order, visible on BIF-KL6, "
     "consistent with public A–A′ frame order."),
    ("REMAINS A CORRELATION", GOLD,
     "DRU, SRU and H-series continuity from KB-KL2 onto BIF-KL6 · MMU vs DRU across the trough (C9) · "
     "KL6 panel positions relative to frame A–A′."),
    ("REMAINS A HYPOTHESIS", RED,
     "EVENT-C-M (Sabah Trough tectono-magmatic branch) · crustal models R1–R4 · Models A/B/C of SRC-ESDG-MODELS · "
     "onshore–offshore magmatic correlation · 'Mesozoic' attribution of deep SE section."),
    ("NOT REPRESENTED BY DATA", GREY,
     "East Sabah and interior Sabah subsurface · mapped surface geology along transect · Dangerous Grounds below seabed · "
     "crust and Moho everywhere · depth everywhere."),
]
y = 1.52
for head, col, body in rows:
    box(s, 0.45, y, 2.55, 0.82, col if col != GREY else RGBColor(0x2A,0x2D,0x36), WHITE, 0.75)
    txt(s, 0.5, y+0.06, 2.45, 0.72, head, size=10.5,
        color=WHITE if col != GOLD else RGBColor(0x1A,0x1A,0x1A), bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 3.08, y, W-3.55, 0.82, PANEL, col, 1.1)
    txt(s, 3.18, y+0.03, W-3.75, 0.76, body, size=10, color=WHITE)
    y += 0.9
txt(s, 0.45, 6.92, W-0.9, 0.28,
    "WHAT CHANGES EXPLORATION UNDERSTANDING: KB-KL2 cannot be used as the regional reference — its failed ties stay local. "
    "Regional play statements need a navigated dip keyline across the trough tied to wells. (Consequence statements = interpretation, not fact.)",
    size=9, color=GOLD)
footer(s, 2)

# ============ 3 ORIENTATION + TRANSECT ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "REGIONAL TRANSECT · SEGMENT EVIDENCE CLASS",
      "EAST SABAH (SE)  ◄  DISPLAY ORIENTATION  ►  DANGEROUS GROUNDS (NW)")
pic(s, "01_transect_segments.png", 0.35, 1.35, W-0.7, 3.6)
box(s, 0.45, 5.05, W-0.9, 1.55, PANEL, GOLD, 1.2)
txt(s, 0.6, 5.12, W-1.2, 1.45,
    "Station order in SRC-XS-PUB: Dangerous Grounds (8.30 N, 113.00 E) → Sandakan Basin (5.85 N, 118.40 E).\n"
    "Display reverses frame km so East Sabah is on the LEFT. BIF-KL6 is NW→SE as sourced; panels shown unflipped, each with a reversal marker.\n\n"
    "Segment widths on the display are NOT to a common horizontal scale. Segment km ranges are GEOX display boundaries constructed on the "
    "public schematic A–A′ frame (RG-01); BIF-KL6 panels are placed by structural-domain name, not by coordinates.",
    size=11, color=WHITE)
footer(s, 3)

# ============ 4 SEGMENT DETAIL ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "SEGMENT-BY-SEGMENT · WHAT EACH ONE CONTROLS")
segs = [
    ("SEG-1 · East Sabah", "CONCEPTUAL BRIDGE", GREY,
     "Geological-map control. SRC-XS-PUB stations (Telupid, Kinabatangan, Sandakan Basin). SB505 / Sandakan / SB304 documents inventoried, NOT ingested.\n"
     "Unknowns: mapped surface geology along transect; subsurface geometry; seismic. Confidence: LOW. Gate: RG-01."),
    ("SEG-2 · Interior Sabah / Crocker–Kinabalu", "DERIVED", "#8B6B4A",
     "SRC-XS-PUB topographic nodes (Mt Kinabalu 4.095 km as quoted). SRC-BB-V5 cross-check (secondary).\n"
     "RC-06: granite root in secondary schematics NOT adopted. Unknowns: surface geology; crustal geometry; emplacement depth/shape of Kinabalu body. Gate: RG-02."),
    ("SEG-3 · Western Sabah onshore-to-offshore", "CONCEPTUAL BRIDGE", GREY,
     "SRC-XS-PUB (Kota Kinabalu coast station). No seismic, no well. Unknowns: any seismic or well tie across the coastline. Confidence: LOW. Gate: RG-01."),
    ("SEG-4 · Inboard offshore / thrust-sheet", "DIRECT", BLUE,
     "SRC-BIF23-KL6 px 1130–1590 ('Thrust Sheet'). TWT ms 0–10000. Wells: Dudar, Tekuyong, Kandi, Sugut, Solisip. Navigation UNVERIFIED. Gates: C27, RG-03."),
    ("SEG-5 · Toe-thrust / Sabah Trough", "DIRECT", BLUE,
     "SRC-BIF23-KL6 px 393–1130 ('NW Sabah Trough', 'Toe Thrust') + KB-KL2 local calibration (v4.1). Wells: Permai, Buluh, Rotan. C9/C20/C27/C30 open. EVT-C-M corridor has NO geometry."),
    ("SEG-6 · NW Sabah Platform", "DIRECT", BLUE,
     "SRC-BIF23-KL6 px 63–393. Rugose seabed ≈1900–2200 ms. RC-03: 'NW Sabah Platform' not in SRC-XS-PUB province list — boundary is a GEOX display construct. Gates: RG-03, RG-04."),
    ("SEG-7 · Dangerous Grounds", "NO DATA", RGBColor(0x2A,0x2D,0x36),
     "SRC-XS-PUB stations only (Dangerous Grounds, Layang-Layang; schematic bathymetry nodes). Nothing below seabed. Confidence: UNKNOWN. Gates: C9, RG-04."),
]
y = 1.28
for name, cls, col, body in segs:
    box(s, 0.4, y, 3.15, 0.72, col, WHITE, 0.7)
    txt(s, 0.45, y+0.03, 3.05, 0.66, f"{name}\n{cls}", size=9,
        color=WHITE if col != GOLD else RGBColor(0x1A,0x1A,0x1A), bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 3.62, y, W-4.05, 0.72, PANEL, col, 1.0)
    txt(s, 3.7, y+0.01, W-4.25, 0.70, body, size=8.5, color=WHITE)
    y += 0.78
footer(s, 4)

# ============ 5 NESTED SCALES ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "THREE NESTED SCALES", "Object IDs unchanged across scales · local picks NOT propagated regionally (C20 FAIL ties)")
pic(s, "02_nested_scales.png", 1.4, 1.45, 10.5, 5.3)
footer(s, 5)

# ============ 6 CHRONOSTRAT ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "CHRONO-STRATIGRAPHIC FRAME · KB-KL2 SURFACES",
      "SCALE BREAK 24 Ma · 0–24 Ma = 72% of height · 24–66 Ma = 28% · piecewise linear · P, L and R drawn with equal weight")
pic(s, "03_chronostrat.png", 0.3, 1.35, 8.6, 5.6)
box(s, 9.1, 1.4, 3.85, 5.5, PANEL, GOLD, 1.2)
txt(s, 9.22, 1.48, 3.6, 0.55, "MODEL STATUS", size=13, color=GOLD, bold=True)
txt(s, 9.22, 2.0, 3.6, 4.8,
    "P · PROJECT_2026\n     top-of-stage · SRC-UNI, SRC-P1 not local\n\n"
    "L · LEGACY_TB\n     base-of-stage · SRC-PEN local\n\n"
    "R · LEGACY_RECAL\n     re-dated legacy · hypothesis by construction\n\n"
    "DERIVED MODEL SPREAD\nNOT a measured uncertainty interval\n\n"
    "Age not assigned: H400, H136, H120, U-*\n\n"
    "H400 → review card · NO AGE · UNSET\n\n"
    "GTS2020 stage column + NN (GTS2012)\n"
    "TS (interpretation) TTSS00–TTSS55",
    size=10, color=WHITE)
footer(s, 6)

# ============ 7 SURFACE CALLOUTS ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "SURFACE CALLOUTS · KB-KL2", "P / L / R ages where assigned · restoration-pack quotations marked · confidence per surface")
callouts = [
    ("SEABED", "P 0.0 · L 0.0 · R 0.0", "INTERP LOW-MED · P-gap 0g · C20 UNSET · C20"),
    ("H50", "2.6 Ma · REST15", "INTERP LOW-MED · REST15 0g · UNSET"),
    ("H1", "P 2.0 · L 3.8 · R 3.7", "INTERP MED · P-gap 1g · C6"),
    ("H2", "P 3.1 · L 5.5 · R 5.59", "INTERP MED · P-gap 1g · C6"),
    ("H3", "P 8.11 · L 6.7 · R 6.7", "INTERP MED · P-gap 1g · C20 · C5"),
    ("SRU", "P 9.53 · L 9.4 · R 9.53", "INTERP MED · P-gap 4g · C20 · C-NWB-05 · C-T6"),
    ("UIU", "P 10.46 · L 10.6 · R 10.55", "INTERP MED · P-gap 2g · C-NWB-01 · C3"),
    ("LIU", "P 11.63 · L 12.0 · R 11.9", "INTERP LOW-MED · P-gap 1g · C4"),
    ("DRU", "P 14.2 · L 15.4 · R 14.91", "INTERP MED · P-gap 2g · C20 · C1 · C9"),
    ("MMU", "P 16.0 · L 16.0 · R 16.0", "INTERP LOW-MED · P-gap 1g · C9"),
    ("BMU", "P 23.13 · L 21.0 · R 21.0", "INTERP LOW-MED · P-gap 1g · C7"),
    ("BU", "P 30.8 · L 30.8 · R 30.8", "INTERP LOW-MED · P-gap 0g"),
    ("LEU", "P 34.1 · L 34.4 · R 34.4", "INTERP LOW-MED · P-gap 1g · C11"),
    ("ROU", "P 56.0 · L 56.0 · R 56.0", "INTERP LOW-MED · P-gap 1g · C-NWB-04"),
]
y = 1.42
for i, (nm, ages, conf) in enumerate(callouts):
    yy = y + i * 0.365
    box(s, 0.45, yy, 1.35, 0.33, BLUE, WHITE, 0.6)
    txt(s, 0.48, yy+0.01, 1.3, 0.31, nm, size=9, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 1.9, yy+0.01, 3.5, 0.31, ages, size=9, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 5.5, yy+0.01, 7.4, 0.31, conf, size=9, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.45, 6.75, W-0.9, 0.4,
    "Restoration surfaces (REST15): H50 2.6 · H75 3.6 · H110 8.1 · H150 9.0 · H300 10.1 · H350 11.1 · H370 13.0 Ma — all INTERP LOW-MED, pack quotations, not governed ages.",
    size=9, color=GOLD)
footer(s, 7)

# ============ 8 WELLS ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "WELL TIES · KB-KL2 AND REGIONAL CALIBRATION",
      "C20: failed ties stay local — NOT propagated regionally")
box(s, 0.45, 1.5, 6.0, 4.3, PANEL, RED, 1.3)
txt(s, 0.6, 1.58, 5.7, 0.4, "KB-KL2 WELLS (on the local screenshot)", size=13, color=RED, bold=True)
txt(s, 0.6, 2.05, 5.7, 3.6,
    "ROTAN-1\n"
    "  Compiled NN: NN11 / NN10 · checkshot/VSP\n"
    "  SEABED ◆ EDGE ·  SRU ✕ FAIL ·  H3 ✕ FAIL\n\n"
    "MALIGAN-1\n"
    "  Compiled NN: NN11 / NN10 / NN9 · checkshot/VSP\n"
    "  SRU ✕ FAIL ·  H3 ? UNKNOWN\n\n"
    "BARTON-2\n"
    "  No NN control · checkshot/VSP\n\n"
    "Shared object: WELL-ROTAN-1 (5 km off BIF-KL6 as tabulated)\n"
    "KB-KL2 position on regional transect: navigation UNVERIFIED",
    size=11, color=WHITE)
box(s, 6.75, 1.5, 6.1, 4.3, PANEL, BLUE, 1.3)
txt(s, 6.9, 1.58, 5.8, 0.4, "REGIONAL CALIBRATION WELLS (compiled NN, SRC-PEN)", size=13, color=GOLD, bold=True)
txt(s, 6.9, 2.05, 5.8, 3.6,
    "GAJAH HITIGA · TIGA PAPAN · MALIGAN · SOLISIP\n"
    "GLAYZER-3 · RUSA TIMUR · IMBOK · BULUH\n"
    "DELUAR · KETAM · SOUTH LOKA\n\n"
    "Not on KB-KL2 · C12\n\n"
    "Gap grammar applied:\n"
    "  Erosion — not drawn (no source asserts located truncation)\n"
    "  Non-deposition — not drawn\n"
    "  Hiatus unresolved: UNKNOWN: EROSION OR NON-DEPOSITION\n"
    "  CONDENSATION CANDIDATE (inferred only)\n"
    "  Poor recovery / caving candidate (C12)\n"
    "  Reworking candidate (C12)",
    size=10.5, color=WHITE)
box(s, 0.45, 5.95, W-0.9, 0.85, RGBColor(0x2A,0x2D,0x36), GOLD, 1.1)
txt(s, 0.6, 6.02, W-1.2, 0.78,
    "RC-04 · Well stick-to-name ambiguity on BIF-KL6 — three sticks under labels Buluh + Rotan (px 1011/1019/1024) and three under Kandi + Sugut (px 1398/1420/1429). OPEN.\n"
    "RC-01 · KL2 marker on BIF-KL6 is BIF-KL2, not KB-KL2 — under C27 the printed 'KL2' at the 2W block (trough) is BIF-KL2; KB-KL2 relates to BIF-KL6 only through Rotan-1. OPEN · ARIF_REVIEW.",
    size=9.5, color=WHITE)
footer(s, 8)

# ============ 9 EVENTS ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "TECTONIC EVENT FRAME",
      "All events: Block H and regional as sourced · extent NOT demonstrated beyond Block H lane · every event is INTERPRETATION · PARTIAL")
pic(s, "04_events.png", 0.35, 1.4, W-0.7, 4.55)
box(s, 0.45, 6.05, W-0.9, 0.85, PANEL, RED, 1.2)
txt(s, 0.6, 6.12, W-1.2, 0.78,
    "EVENT-C SCOPE — EVENT-C-S: localized H370–H300 kinematic reorganisation in the Tanjung / Rotan restoration corridor (Block H, outboard). Magmatism not shown.\n"
    "EVENT-C-M: Sabah Trough tectono-magmatic branch — HYPOTHESIS · HOLD · no geometry · no emplacement age (C30). Neither explains the regional transect.\n"
    "Competing models for EVENT-C-S: syn-compressional gravitational collapse · back-limb extension · strain partitioning · oblique reactivation · mobile-shale decoupling · restoration artefact.",
    size=9, color=WHITE)
footer(s, 9)

# ============ 10 EVENT TABLE ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "EVENT DETAIL · PALEO SYSTEM CONSEQUENCE",
      "Every row: evidence class = INTERPRETATION · PARTIAL · open gates G4/G5 (G6 for Event C)")
ev = [
    ("EVT-T0", "Paleogene inherited substrate", "Deep surfaces NP14 46.29 / NP8 57.21 Ma model-assigned", "Substrate controls heat flow & deep kitchens · unresolved", "G4,G5"),
    ("EVT-T1", "Early Miocene basin initiation", "RELQ25 p.22 · how NSPW emplaced above older prism (C-T3)", "Future mobile-shale supply · NSPW a theoretical source", "G4,G5"),
    ("EVT-T2", "NSPW development", "circa 18–13 Ma (RELQ25 p.22) · composite NSPW origin (C-T4)", "Overpressure potential (analogue)", "G4,G5"),
    ("EVT-T3", "H400 structural boundary", "Age NOT assigned · pack labels H400 and H370 both 13 Ma (REST15)", "Deep kitchens and conduits below H400 poorly imaged", "G4,G5"),
    ("EVT-T4", "Localized extension during shortening", "13 → 11.1 Ma · collapse / shale-withdrawal / thrust-top? (C-T7)", "This depocentre later becomes the Tanjung kitchen", "G4,G5"),
    ("EVT-T5", "EVENT-C-S kinematic reorganisation", "13 → 10.1 Ma · not mapped to stored surfaces · link to Trough? (C26)", "Alters routing of later sands and kitchen geometry", "G4,G5"),
    ("EVT-T6", "H300 compressional pulse", "10.1 Ma restored → ~10 Ma deformed · detachment geometry open", "Rotan trap forms", "G4,G5"),
    ("EVT-T7", "Confined-minibasin system", "No age assigned · minibasin mechanism (C-T7) · mud genesis (C-T14)", "Ponded reservoirs · mud-bounded traps", "G4,G5"),
    ("EVT-T8", "Reduced regional confinement", "No age assigned · where and why confinement persisted open", "Fairways must stay horizon-specific", "G4,G5"),
    ("EVT-T9", "SRU surface system", "P 9.53 / L 9.4 / R 9.53 Ma · pack-marker equivalence CORRELATION HOLD", "Shelf foreset pay · deepwater expression not erosional", "G4,G5"),
    ("EVT-T10", "Local reactivation and burial", "9.0 → 8.1 Ma · spatial extent of reactivation open", "Trap modification · possible breach", "G4,G5"),
    ("EVT-T11", "Gravity-dominated overprint", "H50 2.6 Ma · Stage IVF (RELQ25 p.24) · gravity vs compression (C-T10)", "Hikmat-1: 4.6 m net gas in H50", "G4,G5"),
    ("EVT-T12", "Present day", "Stress tensor on KL2 UNKNOWN · fluid escape not demonstrated", "Partial leakage · most accumulations not filled to spill", "G4,G5"),
]
y = 1.38
for eid, name, ev_txt, cons, gate in ev:
    box(s, 0.35, y, 1.05, 0.38, BLUE, WHITE, 0.5)
    txt(s, 0.37, y+0.01, 1.0, 0.36, eid, size=8, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 1.48, y+0.01, 2.55, 0.36, name, size=8, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 4.1, y+0.01, 4.75, 0.36, ev_txt, size=7.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 8.95, y+0.01, 3.35, 0.36, cons, size=7.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 12.35, y+0.01, 0.85, 0.36, gate, size=7.5, color=GREY, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.41
txt(s, 0.35, 6.85, W-0.7, 0.3,
    "H400 AGE · GOVERNED PAYLOAD: UNASSIGNED · REST15 QUOTATIONS: 13 Ma · STATUS: HOLD · ARIF DECISION: UNSET",
    size=9.5, color=RED, bold=True, align=PP_ALIGN.CENTER)
footer(s, 10)

# ============ 11 SPATIAL EVIDENCE MATRIX ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "SPATIAL EVIDENCE MATRIX",
      "Segment widths NOT to a common scale · SEG boundaries are GEOX display constructs (RG-01)")
pic(s, "05_evidence_matrix.png", 0.4, 1.35, 6.3, 5.2)
box(s, 6.95, 1.4, 6.0, 5.2, PANEL, GOLD, 1.2)
txt(s, 7.1, 1.48, 5.7, 0.4, "KEY GATES OPEN", size=13, color=GOLD, bold=True)
txt(s, 7.1, 1.95, 5.7, 4.6,
    "RG-01  Segment display boundaries on frame A–A′\n"
    "RG-02  Designate DEM topographic source\n"
    "RG-03  Freeze BIF-KL6 identity and navigation\n"
    "RG-04  NW Sabah Platform vs Dangerous Grounds boundary\n"
    "RG-05  Designate East Sabah geological-map control\n"
    "RG-06  Carry or reject operator 'Mesozoic' attribution\n"
    "RG-07  Crustal control for R1–R4 (wide-angle / MT)\n\n"
    "C9   MMU vs DRU across Sabah Trough — kept separate\n"
    "C20  Failed KB-KL2 ties stay local\n"
    "C27  BIF-KL6 namespace: REGIONAL-COMPOSITE-KL6\n"
    "C30  EVENT-C-M: no geometry, no emplacement age\n"
    "RC-06 Kinabalu root / igneous corridor NOT adopted\n"
    "RC-07 Public-frame Moho depths NOT adopted\n\n"
    "All decisions: UNSET. GEOX recommends nothing as closed.",
    size=10.5, color=WHITE)
footer(s, 11)

# ============ 12 EPISTEMIC SEPARATION ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "EPISTEMIC SEPARATION · WHAT IS KNOWN WHERE",
      "Build correctness is not Earth truth. GEOX renders; ARIF adjudicates.")
pic(s, "06_epistemic.png", 1.35, 1.35, 10.6, 5.5)
footer(s, 12)

# ============ 13 REVIEW QUEUE ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "ARIF REGIONAL REVIEW QUEUE", "geox_sabah_regional_v1 · all decisions UNSET · GEOX recommends nothing as closed")
queue = [
    ("1", "RG-01", "Approve GEOX segment display boundaries (SEG-1…SEG-7 km ranges)", "ARIF confirmation or replacement transect polyline"),
    ("2", "RG-02", "Designate a topographic source (DEM e.g. GEBCO/SRTM) to replace schematic nodes", "approved DEM extraction along the transect"),
    ("3", "RG-03", "Freeze BIF-KL6 identity and navigation; fix well positions", "SEG-Y / navigation, well header coordinates (SRC-SABAH-WSM)"),
    ("4", "RG-04", "NW Sabah Platform vs Dangerous Grounds boundary and naming", "regional province map"),
    ("5", "RG-05", "Designate East Sabah geological-map control (SB505 MR2 / Sandakan / other)", "ARIF designation; then ingestion audit"),
    ("6", "RG-06", "Carry or reject the operator 'Mesozoic' attribution on BIF-KL6", "well / outcrop age control"),
    ("7", "RG-07", "Crustal control for R1–R4 (wide-angle, refraction, MT)", "geophysical acquisition or published constrained model"),
    ("8", "ARIF-H400-AGE", "H400 age: governed UNASSIGNED vs REST15 13 Ma · HOLD", "adjudicate 13 Ma REST15 quotation vs unassigned governed age"),
    ("9", "C27 / RC-01", "Confirm BIF-KL6 namespace; printed 'KL2' marker is BIF-KL2", "line identity"),
    ("10", "C9", "MMU vs DRU across the Sabah Trough (kept separate)", "dip keyline across DG platforms"),
    ("11", "C20", "Failed KB-KL2 ties stay local (no regional propagation)", "VSP, navigation, DSG export"),
    ("12", "RC-06", "Keep Kinabalu root / igneous corridor out of the governed model", "cited constrained model"),
]
y = 1.32
for n, id_, dec, ev_ in queue:
    box(s, 0.35, y, 0.45, 0.37, GOLD, WHITE, 0.5)
    txt(s, 0.36, y+0.01, 0.43, 0.35, n, size=9, color=RGBColor(0x1A,0x1A,0x1A), bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 0.88, y+0.01, 1.7, 0.35, id_, size=8.5, color=GOLD, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 2.65, y+0.01, 6.3, 0.35, dec, size=8, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 9.05, y+0.01, 4.0, 0.35, ev_, size=8, color=GREY, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.41
txt(s, 0.35, 6.35, W-0.7, 0.55,
    "NEW CONTRADICTIONS: RC-01 KL2 marker identity · RC-02 KB-KL2 position unknown · RC-03 Platform vs Dangerous Grounds province · "
    "RC-04 well stick-to-name ambiguity · RC-05 'Mesozoic' outside 0–66 Ma chart · RC-06 Kinabalu root NOT adopted · RC-07 public Moho NOT adopted.",
    size=9, color=RED)
footer(s, 13)

# ============ 14 DATA + CONSEQUENCE ============
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s); banner(s, BAN)
title(s, "HIGHEST INFORMATION VALUE DATA · AND WHAT IT CHANGES")
box(s, 0.45, 1.45, 6.05, 3.15, PANEL, GREEN, 1.3)
txt(s, 0.6, 1.53, 5.75, 0.4, "WHAT DATA HAVE THE HIGHEST INFORMATION VALUE", size=12, color=GREEN, bold=True)
txt(s, 0.6, 1.98, 5.75, 2.5,
    "1)  Navigated SEG-Y of BIF-KL6 (or equivalent dip line) with well ties\n"
    "     → resolves C9 and the trough-to-shelf correlation\n\n"
    "2)  Survey IDs and header coordinates for the KL6 wells\n"
    "     (SRC-SABAH-WSM lists several) → resolves RC-04, RG-03\n\n"
    "3)  Wide-angle / MT along the margin for R1–R4 → resolves RG-07\n\n"
    "4)  Digitised geological map for SEG-1 / SEG-2 → resolves RG-05",
    size=11, color=WHITE)
box(s, 6.8, 1.45, 6.05, 3.15, PANEL, GOLD, 1.3)
txt(s, 6.95, 1.53, 5.75, 0.4, "WHAT CHANGES EXPLORATION UNDERSTANDING", size=12, color=GOLD, bold=True)
txt(s, 6.95, 1.98, 5.75, 2.5,
    "KB-KL2 cannot be used as the regional reference: its failed ties stay local.\n\n"
    "Regional play statements need a navigated dip keyline across the trough tied to wells — until then regional maps should carry "
    "CORRELATION, not TIE, status.\n\n"
    "(Consequence statements are interpretation, not fact.)",
    size=11, color=WHITE)
box(s, 0.45, 4.85, W-0.9, 1.85, RGBColor(0x2A,0x2D,0x36), GOLD, 1.2)
txt(s, 0.6, 4.95, W-1.2, 0.42, "SOURCES", size=12, color=GOLD, bold=True)
txt(s, 0.6, 5.35, W-1.2, 1.3,
    "SRC-XS-PUB (public schematic frame + place coordinates) · SRC-BIF23-KL6 (NWB23 deck seismic display raster) · "
    "kinabalu_chronostrat_v2.json (scale, GTS2020, NN, megasequences, regional wells) · v4.11 RHG payload (surfaces, ties, gates, Wheeler) · "
    "v3.1 surface system (operator ages, SRC-REST15) · SRC-ESDG-MODELS (hypotheses) · SRC-RELQ25 · SRC-REP15 · SRC-NWB23 · SRC-ARIF-EVC · SRC-ENT-LL1\n\n"
    "Inventoried, NOT ingested: SB505 MR2 · Sandakan publication · SB304 deck. No external calls. No image generation. "
    "Base chart: rhg_v4_2_chronostrat KL2_v4_2_CHRONOSTRAT.svg embedded unchanged (hash-checked).",
    size=9.5, color=WHITE)
footer(s, 14)

path = f"{OUT}/GEOX_Sabah_Regional_Geological_Intelligence.pptx"
prs.save(path)
print("SAVED:", path)
