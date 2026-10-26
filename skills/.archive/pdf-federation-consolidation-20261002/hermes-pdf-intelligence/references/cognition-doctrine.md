# Cognition Doctrine — Evidence Base (condensed from HERMES PDF Intelligence Report, ch. 2–4)

Load this file when designing document content/layout. Every rule below carries its evidence and
magnitude. A doctrine that cites fabricated numbers forfeits its evidential standard — never quote
a number that cannot be forged from a logged experiment. DITEMPA BUKAN DIBERI: forged, not given.

## 1. The measured attention budget (ch. 2)

| Rule | Evidence | Magnitude |
|---|---|---|
| First-Screen Contract: BLUF block + 3–5 key findings on page 1 | Paragraph-fixation decay 81%→71%→63%→32% (NN/g 2013); ~10 s value verdict (Nielsen 2011, 2B-record dwell data); 57% of viewing time lands on the first screenful (NN/g 2018) | Behavioral shares, not effect sizes |
| Design for scanners, not readers | 79% scan vs 16% read word-by-word (Nielsen 1997); reading depth ceiling ~28% theoretical, ~20% realistic (Weinreich et al. 2008, 45,237 page views) | Behavioral shares |
| Headings as standalone claims (layer-cake by design) | Layer-cake = most effective scan pattern (NN/g 2017); headings causally improve recall of topics and organization (Sanchez, Lorch & Lorch 2001, n=140) | Causal recall gain |
| 4±1 chunk budget per view (bullets, cards, comparison columns) | Working-memory central capacity is 4±1 (Cowan 2001, >10,800 citations); Miller's 7±2 was strategy-assisted, not raw capacity | Visual STM 3–4 |
| Bold numbers, names, decision asks; one idea per paragraph | Spotted-scanning fixations target bold/digits (NN/g 2019); concise+scannable+objective rewrite (Morkes & Nielsen 1997) | +124% measured usability |
| Signal structure; segment dense content | Signaling meta-analysis (Richter & Scheiter 2015, N=2,500); segmentation meta (56 comparisons) | signaling r=.15; segmentation d=.36; replication: signaling retention g+=0.53 (Schneider 2018, 103 studies) |
| Restate BLUF at section boundaries; inverted pyramid per paragraph | Skimming preserves gist but loses inference (Duggan & Payne 2009); a satisficing reader who stops anywhere must still exit with the main point | Experimental |
| Progressive disclosure ≤2 levels | NN/g progressive disclosure (2006): few important items first, detail behind clearly scented cues | Practitioner-standard, evidence-aligned |

## 2. Visual doctrine (ch. 3) — every visual answers a named question or is deleted

| Rule | Evidence | Magnitude |
|---|---|---|
| Functional visuals help | Mayer & Fiorella 2014 program medians: coherence (remove extraneous) 23/23 tests; spatial contiguity 22/22; temporal contiguity 9/9; redundancy 16/16; signaling 24/28 | d = 0.86 (coherence); 1.10 (spatial contiguity); 1.22 (temporal); 0.86 (redundancy); 0.41 (signaling) |
| Honest replication discount | Cromley et al. 2025 meta of Mayer corpus (181 studies, 591 effects): overall g = 0.37; text+diagrams g = 0.39 (Guo 2020, 39 studies, independently identical) | ~half the originator program's sizes |
| Decorative imagery is a measured harm, not neutral | Seductive details meta (Rey 2012): overall g = −0.48; images g = −0.95 vs text g = −0.27; Sundararajan & Adesope 2020 (68 effects): paper-based g ≈ −0.61 vs video ≈ −0.05; end-of-document placement g = −0.70 | An irrelevant image costs ~2× an irrelevant paragraph; harm is LARGER on paper — the PDF condition |
| Pictures must represent, organize, interpret, or transform | Levin, Anglin & Carney (87 studies): every function positive EXCEPT decoration (null) | Classification meta-analysis |
| Direct labels over legends; figure at point of first citation | Split-attention / spatial-contiguity cost of separation | d = 0.72 (Ginns 2006, 37 studies); g = 0.63 (Schroeder & Cenkci 2018) |
| Encoding accuracy: position first, color last | Cleveland & McGill 1984 hierarchy, replicated crowdsourced (Heer & Bostock 2010); area worse than angle | Replicated |
| Tables for exact values, charts for patterns | Cognitive fit (Vessey 1991); tables win "retrieve value" on speed+accuracy+preference (Saket 2019); DeSanctis review: 12 pro-table, 7 pro-graph, 10 tie | Chart-with-data-labels = best of both for non-interactive PDF |
| Zero-baseline bars; no 3D; no dual axes | Truncated bars cause major misinterpretation that survives warnings (Pandey 2015; ACM 2024); 3D depth cues lower accuracy (Talbot 2014); dual axes manufacture correlation (UK ONS) | Measured cost per sin |
| Risk quantities as icon arrays with natural frequencies ("7 in 100") | Bayesian task success 4% → 24% (McDowell & Jacobs 2017 meta) | 6× success |

## 3. Typography, polarity, layout spec (ch. 4)

| Rule | Evidence | Magnitude / spec |
|---|---|---|
| Positive polarity (dark-on-light) for sustained reading; halation penalizes light-on-dark | Buchner & Baumgartner 2007; Piepenbrock 2013/14 (pupil-constriction mechanism); halation amplified by astigmatism | 5–15% reading-speed advantage at body sizes even at identical contrast |
| Print beats screen for comprehension | Delgado 2018 meta, 54 studies, >170k participants; corroborated Clinton 2019 | g ≈ −0.21 for screen vs paper |
| Dark-Dossier Compromise | Synthesis of polarity + halation + screen-inferiority | Light default >2 pages or print; dark ONLY ≤2-page glanceables; contrast ≥7:1 either way (dark variant: surface #121212, text ~#E0E0E0, weight +1 step; #B0B0B0 on #121212 ≈ 8:1) |
| Font size is the lever; typeface is not | Rello, Pielot & Marcos 2016 (CHI, N=104): readability improves monotonically, comprehension better at 18–26 pt, plateau ~22 pt | Print body 10.5–11.5 pt; screen ≥18 pt-equivalent; never below 10 pt |
| Line length | Dyson & Haselgrove 2001 (~55 CPL comprehension); Shaikh 2005 (speed peaks ~95 CPL); failure zone past 80–100 CPL | 60–75 CPL for comprehension-first documents; 25 mm margins at 10.5–11.5 pt achieves this naturally |
| Line spacing tolerant mid-band | Rello 2016: only 0.8× and 1.8× extremes harm | 1.4–1.5×; never <1.2 or >1.8 (1.5× is a WCAG floor, not an experimental optimum) |
| Margins / contrast / alignment | WCAG 2.2 SC 1.4.3/1.4.6/1.4.8/1.4.11 | 25 mm all sides; contrast ≥7:1 target, 4.5:1 floor; left-aligned ragged right, no full justification; bold not italics (italics impair reading speed) |
| Serif vs sans | Ho Sang & Petraca 2025 PRISMA review, 42 studies; Arditi & Cho RSVP null | NULL — choose typeface for tone, not readability |
| Tags = machine interface | PDF/UA (ISO 14289-1/-2); untagged PDF has no logical order for screen reader AND extractor alike | Structure tree in reading order, H1–H6 no skips, alt text, embedded Unicode-mapped fonts, language+title, validate with veraPDF/PAC |
| Type scale | Practitioner convention (marked as convention) | 1.25–1.4× per level (e.g. 11/14/18/22/28 pt), ≤4 levels |

## 4. Debunked myths — never cite in HERMES output

| Myth | Verdict | Trace |
|---|---|---|
| "Attention span of a goldfish (8 s)" | Fabricated | Unsourced 2015 Microsoft Canada deck; BBC debunk 2017. Real measures: ~47 s avg / 40 s median screen attention (Mark 2023) |
| "Brain processes images 60,000× faster than text" (and "90% of information is visual") | Fabricated | Traced to a 1982 Business Week advertisement; no scientific source exists |
| "Serif is more readable in print / sans on screen" | Busted (null) | 42-study systematic review 2025; Arditi & Cho 2005 RSVP null |
| "Dyslexia fonts (OpenDyslexic, Dyslexie) help" | Busted | Consistent nulls (Wery & Diliberto 2017; Kuster 2018); the Dyslexie effect traced to its spacing (Marinus 2016). Real lever: extra-large letter+word spacing (Zorzi 2012 PNAS, contested stats) |
| "45–75 CPL, 66 optimal" | Part-folklore | Bringhurst convention; experiments support ~55 CPL comprehension, ~95 speed |
| "Whitespace improves comprehension ~20%" | Direction supported, number inflated | Lin 2004, small single lab study, blog-amplified |
| "1.5× line spacing is optimal" | Part-supported | Codified WCAG floor; experiments show only extremes harm |
