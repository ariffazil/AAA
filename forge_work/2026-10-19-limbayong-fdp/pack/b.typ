// LIM-SFDP-v0.2 — Limbayong Shadow FDP, working draft, Parts 1 and 3
#set document(title: "Limbayong Shadow FDP — Working Draft v0.2", author: "HERMES (arifOS)")
#set page(paper: "a4", margin: (top: 25mm, bottom: 19mm, left: 20mm, right: 18mm),
  numbering: none)
#set text(font: "DejaVu Sans", size: 9.2pt, lang: "en", region: "GB")
#set par(justify: true, leading: 0.62em, spacing: 1.05em)

#show heading.where(level: 1): it => block(above: 1.4em, below: 0.8em)[
  #set text(size: 14.5pt, weight: "bold", fill: rgb("#1F3A5F"))
  #it
  #v(-3pt)
  #line(length: 100%, stroke: 0.9pt + rgb("#1F3A5F"))
]
#show heading.where(level: 2): it => block(above: 1.1em, below: 0.45em)[
  #set text(size: 10.8pt, weight: "bold", fill: rgb("#1F3A5F"))
  #it
]
#show heading.where(level: 3): it => block(above: 0.85em, below: 0.3em)[
  #set text(size: 9.5pt, weight: "bold", fill: rgb("#333333"))
  #it
]

#let navy = rgb("#1F3A5F")
#let red = rgb("#A32E2E")
#let grey = rgb("#6B6B6B")
#let lightbg = rgb("#F6F6F3")

#let tag(t) = {
  let c = if t == "VERIFIED" { rgb("#2E7D32") }
          else if t == "REPORTED" { rgb("#4A6FA5") }
          else if t == "DERIVED" { rgb("#1F3A5F") }
          else if t == "ASSUMED" { rgb("#C08A2E") }
          else { rgb("#A32E2E") }
  box(fill: c, inset: (x: 3pt, y: 1.2pt), radius: 2pt,
      text(size: 6.7pt, weight: "bold", fill: white)[#t])
}

#let open-banner(body) = block(
  width: 100%, fill: rgb("#FDF4F4"), stroke: (left: 3pt + red),
  inset: (x: 9pt, y: 6pt), above: 0.85em, below: 0.85em,
  text(size: 8.4pt, fill: rgb("#5A1A1A"))[
    #text(weight: "bold", fill: red)[OPEN — ]#body
  ]
)

#show figure.caption: it => block(above: 0.55em, below: 0.75em)[
  #set text(size: 7.9pt, fill: rgb("#3A3A3A"))
  #it.body
]
#set figure(gap: 0.65em)
#show figure: set block(breakable: true)

#set table(stroke: (x: 0.3pt + rgb("#D5D5D0"), y: 0.3pt + rgb("#D5D5D0")),
  inset: (x: 3.6pt, y: 1.75pt),
  fill: (x, y) => if y == 0 { rgb("#1F3A5F") } else if calc.odd(y) { rgb("#F7F7F4") })
#show table.cell.where(y: 0): set text(size: 7.2pt, weight: "bold", fill: white)
#show table.cell: set text(size: 7.3pt)

// ═══════════════════════════ COVER ═══════════════════════════
#v(12mm)
#text(size: 7.8pt, fill: grey)[SHADOW FIELD DEVELOPMENT PLAN · WORKING DRAFT]
#v(2mm)
#line(length: 100%, stroke: 2.2pt + navy)
#v(7mm)
#text(size: 28pt, weight: "bold", fill: navy)[Limbayong]
#v(1mm)
#text(size: 12.6pt, fill: rgb("#333333"))[Deepwater oil and gas development · Block G · Offshore Sabah]
#v(8mm)
#text(size: 10.2pt)[*Working Draft v0.2* — Parts 1 and 3, with ledger, source register and build status]
#v(3mm)
#text(size: 8.6pt, fill: rgb("#444444"))[
  Supersedes v0.1. Issued in response to an independent audit of the previous revision.]

#v(8mm)
#block(fill: lightbg, inset: 10pt, width: 100%, stroke: (left: 3pt + navy))[
  #set text(size: 8.5pt)
  #grid(columns: (30mm, 1fr), gutter: 6pt, row-gutter: 3.2pt,
    [*Document ID*], [LIM-SFDP-v0.2],
    [*Revision*], [0.2 — rebuilt on the as-built vessel basis],
    [*Date*], [19 October 2026],
    [*Prepared by*], [HERMES (arifOS). Not attributed to any person.],
    [*Status*], [Working draft — two Parts of twelve. Not a review pack.],
    [*Scope*], [Part 1, Part 3, Appendices B, E, F, G],
    [*Classification*], [Independent reconstruction from public sources],
  )
]

#v(7mm)
#block(fill: rgb("#FDF4F4"), inset: 10pt, width: 100%, stroke: (left: 3pt + red))[
  #set text(size: 8.4pt)
  #text(weight: "bold", fill: red)[NOT A PETRONAS DOCUMENT]
  #v(2pt)
  This is not a PETRONAS or PETRONAS Carigali document, and was not produced with, reviewed by,
  or endorsed by either company, MISC, or any contractor. It contains no internal data. No
  PETRONAS logo, branding or document numbering is used or implied.
]

#pagebreak()

// ═══════════════════════ DECISION FRAME ═══════════════════════
#set page(header: context [
  #set text(size: 7pt, fill: grey)
  #grid(columns: (1fr, auto),
    [Limbayong Shadow FDP · LIM-SFDP-v0.2 · Rev 0.2 · 19 Oct 2026],
    [Independent reconstruction],
  )
  #v(-3pt)
  #line(length: 100%, stroke: 0.4pt + rgb("#CCCCCC"))
], footer: context [
  #set text(size: 6.8pt, fill: grey)
  #line(length: 100%, stroke: 0.4pt + rgb("#CCCCCC"))
  #v(1pt)
  #grid(columns: (1fr, auto),
    [Independent reconstruction from public sources — not a PCSB/PETRONAS document.],
    [Page #counter(page).display() of #counter(page).final().first()],
  )
], numbering: none)

#counter(page).update(1)

#heading(level: 1, numbering: none)[Decision frame]

#text(size: 8.2pt, fill: grey)[For a reader with two minutes. Every figure is sourced in Appendix B and E.]

#v(4mm)
#block(fill: rgb("#FDF4F4"), stroke: (left: 3pt + red), inset: 10pt, width: 100%)[
  #set text(size: 10.8pt, weight: "bold", fill: rgb("#5A1A1A"))
  On the vessel it actually bought, Limbayong produces 25,000 barrels a day — not 40,000.
]
#v(3mm)
#text(size: 9pt)[
  Every planning figure in this programme that assumed 40,000 bopd, 75,000 barrels a day of water
  injection, and 600,000 barrels of storage was reading a **2020 FPSO tender that was never
  awarded**. The vessel that was bought — the *Excalibur*, IMO 9417103, ex-*Sevan Hummingbird*,
  built 2007 — is published by its owner at **25,000 bopd, 30,000 barrels of total liquids,
  20,000 barrels a day of water injection, and 270,000 barrels of working storage**.
]

#v(4mm)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.1pt)
    *What the resource gives*
    #v(2pt)
    139.5 MMbbl at P50, from a declared bracket of 347–398 MMbbl oil in place and 35–40 per cent
    recovery. #tag("DERIVED")
  ],
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.1pt)
    *What the vessel allows*
    #v(2pt)
    25,000 bopd. At that rate the resource depletes in **15.3 years**, P90–P10 range 14.5–16.1.
    #tag("VERIFIED")
  ],
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.1pt)
    *What the gap is*
    #v(2pt)
    15,000 bopd of capacity that either exists after MMHE conversion, or does not. No public
    source says which. #tag("OPEN")
  ],
)

#v(4mm)
#heading(level: 2, numbering: none)[Three questions a chairman can put tomorrow]

#set enum(numbering: "1.")
+ *What is the post-conversion topsides specification, in writing?* Not the 2020 tender — the
  as-built vessel. Every production, injection and storage number in this document changes with
  the answer.
+ *Is the development phased around a 25,000 bopd hull, or does it need a second hub?* At 25,000
  bopd this is a 15-year asset. At 40,000 it would be a 9.6-year asset that cannot be held. Those
  are different projects with different economics.
+ *What is the gas route?* Limbayong is an oil accumulation **and** a non-associated gas field —
  Limbayong-1 found gas in 2002, Limbayong-2 found oil in 2013. The vessel's gas handling capacity
  is not published at all. #tag("VERIFIED")

#v(3mm)
#heading(level: 2, numbering: none)[What this pack does not answer]

#text(size: 8.7pt)[
  No net present value, no internal rate of return, no capital cost, no schedule, no economic
  limit. Those need a fiscal engine built on Malaysian PSC terms and a term sheet. Neither is
  public, and three ad-hoc fiscal models in this programme produced three different answers from
  the same inputs. A fourth would repeat the defect rather than resolve it.
]
#v(2mm)
#text(size: 8.7pt)[
  What this pack does is fix the *physical* basis, so that the economics — when they exist — are
  computed on the right field.
]

#pagebreak()

// ═══════════════════════ DOCUMENT CONTROL ═══════════════════════
#heading(level: 1, numbering: none)[Document control]

#heading(level: 2, numbering: none)[Revision block]
#table(columns: (11mm, 20mm, 1fr),
  table.header([*Rev*], [*Date*], [*Change*]),
  [0.1], [19 Oct 2026], [First issue. Parts 1 and 3. Nine pages.],
  [0.2], [19 Oct 2026], [Rebuilt on the as-built vessel basis after independent audit. Vessel identity resolved; facility basis split into four spec sets; corner-product cases replaced by a correlated Monte Carlo; VRR corrected; gas ratio relabelled; water depth reclassified; figure QA automated.],
)

#v(3mm)
#heading(level: 2, numbering: none)[What changed, and why]
#table(columns: (42mm, 1fr),
  table.header([*Item*], [*Change in v0.2*]),
  [Vessel identity], [Excalibur resolved to IMO 9417103 = Sevan Hummingbird = Hummingbird Spirit. v0.1 treated it as an unnamed hull.],
  [Oil capacity], [30,000 bopd in v0.1 → *25,000 bopd* as-built, with 30,000 bpd as total liquids.],
  [Water injection], [75,000 bwpd in v0.1 → *20,000 bwpd*. The 75,000 was a tender spec.],
  [Storage], [300,000 bbl "versus spec" → *300,000 design / 270,000 working*. Not a discrepancy.],
  [Cases], [Low/Mid/High corner products → correlated Monte Carlo reporting P90/P50/P10.],
  [Gas], [5,640 scf/bbl presented as a GOR → relabelled a *ratio of totals*, withdrawn from gas-train sizing.],
  [Water depth], [900–1,400 m, tagged OPEN → *900–1,200 m*, two sources; upper bound withdrawn.],
  [Cost anchors], [Absent → subsea award bands added as L-38 and L-39.],
  [Status], ["Review pack" → *working draft, two Parts of twelve*.],
)

#v(3mm)
#heading(level: 2, numbering: none)[Reading guide — five tags]
#table(columns: (22mm, 1fr),
  table.header([*Tag*], [*Test it must pass*]),
  [VERIFIED], [Two or more independent sources, or one primary document (a filing, a statute, a contract). Independence is counted per row in Appendix B.],
  [REPORTED], [One source only, URL given. Carries the single-source flag; a critical-path number in this class is a risk, not a fact.],
  [DERIVED], [Computed here from other ledger rows. The formula is in the row, so the arithmetic can be repeated without trusting the author.],
  [ASSUMED], [A judgement, not a measurement. Owner and reason stated. Can be challenged; cannot be verified.],
  [OPEN], [The input does not exist in the public record. Marked, never guessed. Appears as a red banner where it changes a conclusion.],
)

#v(3mm)
#block(fill: lightbg, inset: 8pt, width: 100%)[
  #set text(size: 8.2pt)
  *Two rules this document is built on.* First, no number may exist only in prose — every figure
  traces to a row in Appendix B. Second, no conflict is resolved silently: where two sources
  disagree, both are printed and the disagreement is given an ID.
]

#v(3mm)
#heading(level: 2, numbering: none)[Data classification]
#text(size: 8.5pt)[
  All information derives from public sources: one Bursa Malaysia filing, trade press, an
  operator-side project description, a non-commercial resource tracker, and public-domain
  geospatial data. No PETRONAS, PETRONAS Carigali, MISC or contractor confidential material has
  been used, requested or received. A reader with access to operator data should expect this
  document to differ from it, and should prefer the operator's data.
]

#pagebreak()

// ═══════════════════════ AUDIT RESPONSE ═══════════════════════
#heading(level: 1, numbering: none)[Response to the audit]

An independent audit scored the previous revision at 2.6/10 and named three stopping errors. Each
finding was re-tested here against primary sources rather than accepted or rejected as a block.
Ten material findings: nine confirmed, one corrected.

#figure(
  table(columns: (6mm, 46mm, 50mm, 1fr),
    table.header([*No.*], [*Finding*], [*Independent re-test*], [*Disposition*]),
    [1], [Excalibur is the ex-Sevan Hummingbird], [Offshore Magazine, 4 Aug 2022: "renamed ... previously known as the Sevan Hummingbird". Bursa filing, 20 Aug 2026, gives IMO 9417103.], [*Confirmed.* Entity key added (L-01). Failure to resolve it was a provenance defect, not an information gap.],
    [2], [Vessel produces 25,000 bopd, not 30,000], [Offshore Magazine 2022: "can produce about 25,000 bbl/d, 270,000 bbl storage". Sevan DWT vessel page matches.], [*Confirmed.* Adopted as the governing ceiling (L-05).],
    [3], [75,000 bwpd is the 2020 tender, not this vessel], [OE Digital, 23 Feb 2021, quoting World Energy Reports: 40,000 b/d oil, 90 mmcf/d gas, 75,000 b/d water, 600,000 bbl storage.], [*Confirmed.* Reclassified as L-12 and removed from all vessel arithmetic.],
    [4], [The tender gas train was "~150 MMscfd"], [The same source states *90 mmcf/d*. The 150 was back-computed from the 5,640 scf/bbl ratio the audit simultaneously criticised.], [*Corrected.* Conclusion holds — tender spec is not the vessel — but the number is 90 MMscfd (L-11), not 150.],
    [5], [VRR was defined oil-only], [Surveillance definitions include produced water and free gas. At 25,000 bopd and Bo 1.30, oil voidage is 32,500 rb/d against 20,000 bwpd injection.], [*Confirmed.* VRR 0.62 on the oil term alone — under-replacement, not over-injection (§3.6).],
    [6], [Low/Mid/High are corner products, not a PRMS range], [347×0.35 and 398×0.40 pair extremes of two back-calculated routes; neither has probability meaning.], [*Confirmed.* Replaced by a correlated Monte Carlo reporting P90/P50/P10 (§3.2).],
    [7], [5,640 scf/bbl is a ratio of totals, not a GOR], [790.9 bcf ÷ 139 MMbbl = 5,640. Mixes free and solution gas.], [*Confirmed.* Relabelled (L-37); withdrawn from all gas-train and voidage reasoning (§3.5).],
    [8], [Water depth is reported, not unknown], [Offshore Technology, 15 Jun 2021: "water depths between 900m and 1,200m". Repeated by 2026 trade press.], [*Confirmed.* Now VERIFIED at 900–1,200 m (L-16). The 1,400 m bound is withdrawn — no source.],
    [9], [Cost anchors were unused], [TechnipFMC "substantial" = US$250–500M (2021); "significant" = US$75–250M (2026).], [*Confirmed.* Added as L-38 and L-39.],
    [10], [Figure defects shipped], [The previous revision already carried a scale bar, graticule, north arrow and CRS note; the claim was made from description, not from bytes.], [*Addressed by measurement.* A deterministic bounding-box gate now runs on every figure (Appendix G): zero overflow, zero overlap across five figures.],
  ),
  caption: [Table 0.1 — Audit findings, re-tested. The audit was treated as a claim set, not as a verdict.],
)

#v(3mm)
#text(size: 8.4pt)[
  *On the system scores.* The audit's component grades — three fiscal engines, tool-surface bloat,
  self-grading — are accepted and recorded in Appendix F. They are not repaired inside a document.
  They are repaired in code, in the order the audit proposes.
]

#pagebreak()

// ═══════════════════════════ PART 1 ═══════════════════════════
#heading(level: 1)[1    Basis and reconciliation]

#heading(level: 2)[1.1    Basis of design]
The public record on Limbayong is thin in a specific pattern: enough to know a development exists,
not enough to know whether it works. This pack separates three things usually blended together.

*Established.* The field lies in Block G, about 120 km offshore Sabah, in 900–1,200 m of water; it
is an oil accumulation with non-associated gas; development is ten subsea wells tied back to a
floating production unit; FID was taken on 28 August 2026; working interest is 100 per cent
PETRONAS Carigali. #tag("VERIFIED")

*Inferred.* That a structure described by its own operator as "industry top decile reservoir
complexity" with lateral compartmentalisation cannot deliver a uniform recovery factor along its
30 km length. Sound, but an inference. #tag("DERIVED")

*Absent.* No public seismic, well log, core, PVT sample, production test, cost estimate, gas sales