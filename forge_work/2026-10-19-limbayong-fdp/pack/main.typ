// LIM-SFDP-v0.4 — Limbayong Shadow FDP, working draft, Parts 1 and 3
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

#set table(align: left,
  stroke: (x: 0.3pt + rgb("#D5D5D0"), y: 0.3pt + rgb("#D5D5D0")),
  inset: (x: 3.4pt, y: 1.45pt),
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
#text(size: 12.6pt, fill: rgb("#333333"))[Deepwater oil and gas development · Blocks G / J / R · Offshore Sabah]
#v(8mm)
#text(size: 10.2pt)[*Working Draft v0.4* — Parts 1, 3 and 5, with ledger, source register and build status]
#v(3mm)
#text(size: 8.6pt, fill: rgb("#444444"))[
  Supersedes v0.1 and v0.2. Adds the geology that the earlier revisions lacked.]

#v(8mm)
#block(fill: lightbg, inset: 10pt, width: 100%, stroke: (left: 3pt + navy))[
  #set text(size: 8.5pt)
  #grid(columns: (30mm, 1fr), gutter: 6pt, row-gutter: 3.2pt,
    [*Document ID*], [LIM-SFDP-v0.4],
    [*Revision*], [0.4 — Part 5 rebuilt on the literature],
    [*Date*], [19 October 2026],
    [*Prepared by*], [HERMES (arifOS). Not attributed to any person.],
    [*Status*], [Working draft — three Parts of twelve. Not a review pack.],
    [*Scope*], [Parts 1, 3 and 5; Appendices B, E, F, G],
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

#block(above: 1.4em, below: 0.8em)[
  #set text(size: 14.5pt, weight: "bold", fill: rgb("#1F3A5F"))
  Contents
  #v(-3pt)
  #line(length: 100%, stroke: 0.9pt + rgb("#1F3A5F"))
]
#outline(title: none, depth: 1, indent: 0pt)

#v(4mm)
#text(size: 8.2pt, fill: grey)[Parts 2, 4 and 6–12 are not written. Appendix F states what each is waiting for. The pack is deliberately incomplete rather than uniformly thin.]

#pagebreak()

// ═══════════════════════ DECISION FRAME ═══════════════════════
#set page(header: context [
  #set text(size: 7pt, fill: grey)
  #grid(columns: (1fr, auto),
    [Limbayong Shadow FDP · LIM-SFDP-v0.4 · Rev 0.4 · 19 Oct 2026],
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
  injection, and 600,000 barrels of storage was reading a _2020 FPSO tender that was never awarded_. The vessel that was bought — the *Excalibur*, IMO 9417103, ex-*Sevan Hummingbird*,
  built 2007 — is published by its owner at *25,000 bopd, 30,000 barrels of total liquids,
  20,000 barrels a day of water injection, and 270,000 barrels of working storage*.
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
    25,000 bopd. At that rate the resource depletes in *15.3 years*, P90–P10 range 14.5–16.1.
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
#block(fill: lightbg, inset: 8pt, width: 100%, stroke: (left: 3pt + navy))[
  #set text(size: 8.3pt)
  *What the ground adds.* The structure is 30 km long, 2.5 km wide, cut every 3–15 km by faults — six
  to fifteen tanks, and the operator's own paper says they defeat well drainage and pressure
  maintenance. Gas is the phase that leaks in this basin; the seal caps the gas column at about 250 m
  whatever the trap size. Which means the number to argue about is not the vessel's 40,000 bopd — it
  is connected volume per well, currently 13.9 MMbbl against a 20–100 analogue band. Part 5.
]

#v(3mm)
#heading(level: 2, numbering: none)[Three questions a chairman can put tomorrow]

#set enum(numbering: "1.")
+ *What is the post-conversion topsides specification, in writing?* Not the 2020 tender — the
  as-built vessel. Every production, injection and storage number in this document changes with
  the answer.
+ *Is the development phased around a 25,000 bopd hull, or does it need a second hub?* At 25,000
  bopd this is a 15-year asset. At 40,000 it would be a 9.6-year asset that cannot be held. Those
  are different projects with different economics.
+ *What is the gas route?* Limbayong is an oil accumulation *and* a non-associated gas field —
  Limbayong-1 found gas in 2002, Limbayong-2 found oil in 2013. The vessel's gas handling capacity
  is not published at all. #tag("VERIFIED")

#v(3mm)
#heading(level: 2, numbering: none)[What this pack does not answer]

#text(size: 8.7pt)[
  No net present value, no internal rate of return, no capital cost, no schedule, no economic
  limit (L-40, OPEN). Those need a fiscal engine built on Malaysian PSC terms and a term sheet. Neither is
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
  [0.3], [19 Oct 2026], [Adds Part 5, The Earth: plate framework, real bathymetry, tectonostratigraphy, trap geometry, charge and leakage, geomechanics, and five earth-derived findings. Water depth measured independently at 994 m. Five new figures.],
  [0.4], [19 Oct 2026], [Part 5 rebuilt on the peer-reviewed literature. Stage scheme corrected to Bol & van Hoorn (four stages, not five). Compartment width corrected from an assumed 2–5 km to a sourced 3–15 km thrust spacing. The well-count finding is reversed: per-well volume, not well count, is the constraint. Adds the capillary seal-capacity limit on column height, the Algar leaking-trap mechanism, seismic-versus-aseismic hazard, and an unresolved thermal contradiction (C-10). Seven new sources.],
)

#v(3mm)
#heading(level: 2, numbering: none)[What changed in this revision, and why]
#table(columns: (42mm, 1fr),
  table.header([*Item*], [*Change*]),
  [Vessel identity], [Excalibur resolved to IMO 9417103 = Sevan Hummingbird = Hummingbird Spirit. v0.1 treated it as an unnamed hull.],
  [Oil capacity], [30,000 bopd in v0.1 → *25,000 bopd* as-built, with 30,000 bpd as total liquids.],
  [Water injection], [75,000 bwpd in v0.1 → *20,000 bwpd*. The 75,000 was a tender spec.],
  [Storage], [300,000 bbl "versus spec" → *300,000 design / 270,000 working*. Not a discrepancy.],
  [Cases], [Low/Mid/High corner products → correlated Monte Carlo reporting P90/P50/P10.],
  [Gas], [5,640 scf/bbl presented as a GOR → relabelled a *ratio of totals*, withdrawn from gas-train sizing.],
  [Water depth], [900–1,400 m, tagged OPEN → *900–1,200 m*, two sources; upper bound withdrawn.],
  [Cost anchors], [Absent → subsea award bands added as L-38 and L-39.],
  [Status], ["Review pack" → *working draft, three Parts of twelve*.],
  [Geology], [Absent → *Part 5 added*: plate framework, real DEM, stratigraphy, trap, charge, geomechanics.],
  [Compartment size], [2–5 km assumed → *3–15 km sourced*: thrust spacing, so 6–15 panels.],
  [Well-count finding], ["well count is the lever" → *reversed*: per-well volume 13.9 MMbbl vs 20–100 analogue band.],
  [Column height], [Unbounded → *capped by capillary seal*, P50 ≈250 m.],
  [Water depth], [900–1,200 m reported → *994 m measured* from DEM, consistent with the reports.],
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
    [9], [Cost anchors were unused], [TechnipFMC "substantial" = US\$250–500M (2021); "significant" = US\$75–250M (2026).], [*Confirmed.* Added as L-38 and L-39.],
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

#figure(
  image("fig/fig0_map.png", width: 100%),
  caption: [Figure 0 — Location. Limbayong lies in Block G, about 120 km offshore Sabah, in 900–1,200 m of water. The shaded zone is schematic and is not an isobath; the block outline is not public, so a point is shown rather than a polygon. Base map: Natural Earth 1:10m. Position L-17; depth L-16. #tag("VERIFIED")],
)

*Absent.* No public seismic, well log, core, PVT sample, production test, cost estimate, gas sales
agreement or fiscal term sheet. Every subsurface volume here is a screening range, not a reserves
estimate. Nothing in this pack uses the word "reserves".

#heading(level: 2)[1.2    Entity resolution — which vessel]
This is the failure that mattered most in the previous revision, and it is worth showing how cheap
it was to avoid.

#figure(
  table(columns: (26mm, 22mm, 18mm, 1fr),
    table.header([*Name*], [*Period*], [*IMO*], [*Owner and note*]),
    [Sevan Hummingbird], [2007–2022], [9417103], [Teekay. Cylindrical SSR300 hull, built 2007, commissioned 2008.],
    [Hummingbird Spirit], [2008–2022], [9417103], [Operating name under Teekay — the same hull, used interchangeably.],
    [Excalibur], [2022–2026], [9417103], [Renamed by Ping Petroleum (DNeX), 4 Aug 2022, for the Avalon development.],
    [Excalibur], [2026–], [9417103], [Sold to MISC for US\$35.0M on 20 Aug 2026. In lay-up at Port of Nigg; delivery at MMHE Pasir Gudang.],
  ),
  caption: [Table 1.1 — One hull, four names. The IMO number is the only stable key. Sources S-01, S-02, S-05; ledger L-01 to L-04.],
)

#v(2mm)
#text(size: 8.6pt)[
  A single IMO check would have caught this. It is the cheapest control in the programme and it was
  absent. The practical consequence: the "270,000 versus 300,000 barrels" discrepancy flagged in
  the previous revision is not a discrepancy at all. 300,000 is the *design capacity* in the Bursa
  filing; 270,000 is the *working storage* in the owner's factsheet. Same hull, two definitions.
]

#heading(level: 2)[1.3    Facility basis — four spec sets that were conflated]
Topsides capacity is not a property of a hull class. Three Sevan 300 hulls carry three different
process plants, and the Limbayong tender specified a fourth. This is the table the pack should have
started with.

#figure(
  table(columns: (30mm, 14mm, 14mm, 15mm, 16mm, 1fr),
    table.header([*Unit (Sevan 300 hull)*], [*Oil bopd*], [*Liquids bpd*], [*Water inj. bwpd*], [*Gas*], [*Status for Limbayong*]),
    [Hummingbird Spirit = Excalibur], [25,000], [30,000], [20,000], [not published], [*The vessel bought.* As-built, 2007, IMO 9417103.],
    [Voyageur Spirit at Shelley], [20,000], [50,000], [—], [25 MMscfd], [Not this vessel. Shows how far topsides vary within one hull class.],
    [Voyageur Spirit at Huntington], [30,000], [60,000], [48,000], [38 MMscfd], [Not this vessel. The 30,000 figure that leaked into the previous revision.],
    [Limbayong FPSO tender, 2020], [40,000], [60,000], [75,000], [90 MMscfd], [*Cancelled, never awarded.* Source of the 40,000 / 75,000 / 600,000 numbers.],
  ),
  caption: [Table 1.2 — Four specification sets. Only the first belongs to the vessel. Sources S-03, S-06; ledger L-05 to L-13.],
)

#v(2mm)
#open-banner[
  *L-42 — post-conversion topsides.* MISC and MMHE have not published what work will be done to
  Excalibur for Limbayong, or what capacity it will have afterwards. Every number in Part 3 is
  therefore conditional on a specification that does not exist in public. This is the largest gap
  in the pack, and analysis cannot close it — only a disclosure can.
]

#heading(level: 2)[1.4    One number set]
Every figure in Parts 1 and 3 resolves to a row in Appendix B. No number may exist only in prose.

#figure(
  table(columns: (56mm, 32mm, 20mm, 14mm),
    table.header([*Parameter*], [*Vessel / field value*], [*Class*], [*Row*]),
    [Vessel identity], [IMO 9417103], [VERIFIED], [L-01],
    [Oil production capacity — as-built], [25,000 bopd], [VERIFIED], [L-05],
    [Total liquids — as-built], [30,000 bpd], [REPORTED], [L-06],
    [Water injection — as-built], [20,000 bwpd], [REPORTED], [L-07],
    [Storage — design / working], [300,000 / 270,000 bbl], [VERIFIED], [L-03, L-04],
    [Gas handling capacity], [not published], [OPEN], [L-09],
    [Oil recoverable — public], [139 MMbbl], [REPORTED], [L-14],
    [Gas recoverable — public], [790.9 bcf], [REPORTED], [L-15],
    [Water depth], [900–1,200 m], [VERIFIED], [L-16],
    [Recoverable P90 / P50 / P10], [132.6 / 139.5 / 146.8 MMbbl], [DERIVED], [L-28–30],
    [Life at 25,000 bopd, P90/P50/P10], [14.5 / 15.3 / 16.1 yr], [DERIVED], [L-31–33],
    [Economic limit], [not stated], [OPEN], [L-40],
    [Post-conversion topsides], [not published], [OPEN], [L-42],
  ),
  caption: [Table 1.3 — The one number set. Full ledger with formulas, sources and independence counts in Appendix B.],
)

#pagebreak()

#heading(level: 2)[1.5    Conflict register]
Nine disagreements were identified across the programme. The previous revision carried seven. Three
are now closed, two changed status because of the audit, and four remain open.

#figure(
  table(columns: (10mm, 38mm, 42mm, 18mm, 1fr),
    table.header([*ID*], [*Conflict*], [*Values in the record*], [*Status*], [*Resolution, or next action*]),
    [C-01], [Total development capex], [2.83 / 2.90 / 3.17 / 4.05 bn], [OPEN], [Part 8. Independent cost build; retire three WBS variants.],
    [C-02], [Throughput: nameplate or forecast], [40,000 vs 25,000 bopd; 150 vs 90 MMscfd], [CLOSED], [Nameplate belongs to a cancelled tender. Vessel ceiling is 25,000 bopd.],
    [C-03], [Oil in place], [517 MMbbl STOIIP vs 347–398 MMbbl screening], [OPEN], [Part 5. Different definitions; one basis must be adopted.],
    [C-04], [Net present value at one price], [4 values at one price], [OPEN], [Part 9. Single fiscal engine; no NPV quoted in this pack.],
    [C-05], [First oil], [2029 vs Q4 2030], [OPEN], [Part 8. Integrated schedule against comparables.],
    [C-06], [Decline, and the "44%" figure], [9.6 yr stated; 44% stated], [CLOSED], [9.6 yr is 139 ÷ 40,000 — tender arithmetic, not subsurface. "44%" reproduces nowhere; withdrawn (§3.4).],
    [C-07], [Water injection duty], [20,000 vs 75,000 bwpd], [CLOSED], [20,000 is the vessel; 75,000 is the cancelled tender.],
    [C-08], [Gas handling capacity], [90 MMscfd tender vs 150 asserted vs none published], [OPEN], [L-09. No public figure exists for this hull.],
    [C-09], [Vessel identity], [unnamed hull vs Hummingbird Spirit], [CLOSED], [IMO 9417103. Resolved by entity key (Table 1.1).],
  ),
  caption: [Table 1.4 — Conflict register. Closed items carry an explicit resolution; open items carry an owning Part. Nothing closes silently.],
)

#v(2mm)
#text(size: 8.4pt)[
  *Why C-02 and C-07 closed rather than narrowed.* They were never disagreements about the field.
  They were a category error: a tender specification read as a vessel specification. Once the four
  spec sets sit side by side (Table 1.2), there is nothing to reconcile — only a shortfall to
  report, which is a finding rather than a conflict.
]

#heading(level: 2)[1.6    What Part 1 establishes and what it does not]
#grid(columns: (1fr, 1fr), gutter: 9pt,
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.1pt)
    *Established*
    #v(2pt)
    - The vessel is identified by IMO number, not by name: one hull, four names, and a documented
      rename in 2022.
    - Its as-built capacity is 25,000 bopd — 37.5 per cent below the figure the development case
      has been described against.
    - Four specification sets exist in the public record. Only one of them belongs to the vessel.
    - Three conflicts closed on definitional grounds; four remain open, each with an owning Part.
    - Every number in this Part traces to a ledger row, and every ledger row states its formula or
      its source.
  ],
  block(fill: rgb("#FDF4F4"), stroke: (left: 3pt + red), inset: 8pt)[
    #set text(size: 8.1pt)
    *Not established*
    #v(2pt)
    - Post-conversion capacity (L-42). The single number that governs everything downstream.
    - Whether MISC or PETRONAS has confirmed the Limbayong link. Currently single-sourced trade
      reporting.
    - Which oil-in-place basis is correct: 517 MMbbl STOIIP, or the 347–398 MMbbl screening bracket.
    - Anything that costs money. No capital, opex, schedule or fiscal term in this Part is primary.
    - Whether the vessel's gas handling exists at all, or is being added.
  ],
)

#v(2mm)
#text(size: 8.5pt)[
  A reader who takes one thing from Part 1 should take the entity key. Three of the four closed
  conflicts were the same failure wearing different clothes: a number that belonged to a machine, a
  tender, or a name, used as if it belonged to the field.
]

#pagebreak()

// ═══════════════════════════ PART 3 ═══════════════════════════
#heading(level: 1)[3    Production]

#heading(level: 2)[3.1    Case construction — why the old cases were wrong]
The previous revision ran three cases: 347 × 0.35, 372.5 × 0.375 and 398 × 0.40. Each looked
defensible. Together they were not a range.

#grid(columns: (1fr, 1fr), gutter: 9pt,
  block(fill: rgb("#FDF4F4"), stroke: (left: 3pt + red), inset: 8pt)[
    #set text(size: 8.1pt)
    *What was wrong*
    #v(2pt)
    - The low case paired the lowest oil in place with the lowest recovery factor; the high case
      paired the highest with the highest. Those are *corner products* — the two least likely
      combinations in any joint distribution.
    - Neither corner has a probability meaning, so neither is a P90 or a P10.
    - The bracket was back-calculated from the same public 139 MMbbl, so the spread measured
      arithmetic, not geology.
  ],
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.1pt)
    *What replaced it*
    #v(2pt)
    - One route: recoverable = oil in place × recovery factor.
    - Both inputs sampled jointly with a positive rank correlation (ρ = +0.60), because better rock
      raises both — the dependency the corner cases ignored.
    - 20,000 draws, fixed seed, bit-reproducible.
    - Reported as P90/P50/P10 of the *output*, with the public 139 used only as a calibration check
      that P50 lands on it.
  ],
)

#v(2mm)
#text(size: 8.6pt)[
  The result is deliberately narrow — P90 132.6, P50 139.5, P10 146.8 MMbbl. That narrowness is
  stated rather than disguised: the Monte Carlo propagates the declared bracket, it does not
  estimate the field. Without a competent persons report the true uncertainty is not measurable,
  and the pack says so instead of manufacturing a wider spread.
]

#heading(level: 2)[3.2    Distributions and reproducibility]
#figure(
  image("fig/fig3_mc.png", width: 100%),
  caption: [Figure 3 — Monte Carlo output, 20,000 correlated draws, fixed seed. *A:* recoverable oil. *B:* field life at 25,000 bopd. Recoverable P90/P50/P10 = 132.6 / 139.5 / 146.8 MMbbl. Reruns are identical. Source: L-21 to L-33. #tag("DERIVED")],
)

#heading(level: 2)[3.3    Plateau against the vessel ceiling]
Three numbers govern production and cannot be chosen independently: the resource, the rate the
facility can take, and the resulting life.

#figure(
  table(columns: (30mm, 26mm, 26mm, 26mm, 1fr),
    table.header([*Metric*], [*P90*], [*P50*], [*P10*], [*Basis*]),
    [Recoverable oil], [132.6 MMbbl], [139.5 MMbbl], [146.8 MMbbl], [Monte Carlo, L-28 to L-30],
    [Life at 25,000 bopd], [14.5 yr], [15.3 yr], [16.1 yr], [÷ (25,000 × 365), L-31 to L-33],
    [Plateau duration], [10.1 yr], [10.7 yr], [11.3 yr], [70% of ultimate at plateau, ASSUMED],
  ),
  caption: [Table 3.1 — Production metrics at the as-built ceiling. No economic limit is applied — L-40 is OPEN; see §3.7.],
)

#figure(
  image("fig/fig1_profiles.png", width: 100%),
  caption: [Figure 1 — *A:* one resource, three facility ceilings. The solid navy curve is the vessel as built; the dotted amber curve requires a topsides upgrade for which no public specification exists. The red line is the cancelled tender. *B:* life as a function of plateau rate, for P90/P50/P10. Sources: L-05, L-10, L-28 to L-33. #tag("DERIVED")],
)

#v(1mm)
#text(size: 8.6pt)[
  Read panel A with the red line in mind. *No case reaches 40,000 bopd.* The as-built vessel sits at
  62.5 per cent of the tender nameplate; the upgraded scenario — which no public document supports
  — reaches 92.5 per cent. The gap is not a range to be narrowed by more analysis. It is a capacity
  question only a yard specification can answer.
]

#heading(level: 2)[3.4    What the 9.6-year figure actually is]
The previous revision carried a 9.6-year "stress case" and a "44 per cent decline requirement". Both
are now explained.

#figure(
  image("fig/fig2_ninetysix.png", width: 100%),
  caption: [Figure 2 — *A:* depletion at 25,000 bopd for P90/P50/P10. *B:* the same arithmetic plotted against rate. The 9.57-year line implies 40,000 bopd — the cancelled tender's own number. Source: L-29, L-10. #tag("DERIVED")],
)

#v(2mm)
#align(center)[
  #block(fill: lightbg, inset: 9pt)[
    #set text(size: 8.9pt)
    #table(columns: (62mm, 40mm),
      table.header([*Arithmetic*], [*Result*]),
      [139.5 MMbbl ÷ (25,000 bopd × 365)], [*15.3 years* — as-built vessel],
      [139.5 MMbbl ÷ (37,014 bopd × 365)], [*10.3 years* — upgraded scenario, ASSUMED],
      [139.5 MMbbl ÷ (40,000 bopd × 365)], [*9.57 years* — cancelled tender],
    )
  ]
]

#v(1mm)
#text(size: 8.6pt)[
  The 9.6-year figure is therefore not a property of the reservoir. It is the tender's 40,000 bopd
  arithmetic — the public resource divided by a capacity that was never built. It survived into the
  pack because 139 ÷ 40,000 resembles a decline study. *C-06 closes on that basis.* The "44 per
  cent" figure reproduces from nothing in this arithmetic and is withdrawn, not carried forward.
]

#heading(level: 2)[3.5    Gas — a ratio of totals is not a GOR]
790.9 bcf of gas and 139 MMbbl of oil give 5,640 scf per barrel. That number was used in the
previous revision to size a gas train and to reason about voidage. Both uses were circular.

#grid(columns: (1fr, 1fr), gutter: 9pt,
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.1pt)
    *Why it is not a GOR*
    #v(2pt)
    A producing gas-oil ratio is gas released *from solution*, per barrel of oil produced.
    Limbayong is an oil accumulation *and* a non-associated gas field: Limbayong-1 found gas in
    2002, Limbayong-2 found oil in 2013. Dividing total gas by total oil mixes free gas with
    solution gas and yields a number with no physical meaning.
  ],
  block(fill: rgb("#FDF4F4"), stroke: (left: 3pt + red), inset: 8pt)[
    #set text(size: 8.1pt)
    *What it is*
    #v(2pt)
    A *ratio of totals* (L-37): total recoverable gas ÷ total recoverable oil. Useful as a
    portfolio-scale ratio. Useless for sizing a gas train, sizing voidage, or inferring solution
    gas. Only PVT data closes this, and no PVT is public.
  ],
)

#v(2mm)
#text(size: 8.6pt)[
  The practical consequence: the "two-year gas tail" in the previous revision is withdrawn. If a
  material part of the 790.9 bcf is free gas, it need not follow the oil decline at all — it can be
  produced on its own schedule, or left in place. The pack does not know which, and says so.
]

#open-banner[
  *L-09 / C-08 — gas handling.* Excalibur's gas compression and export capacity is not published.
  The cancelled tender specified 90 MMscfd. This hull's own figure does not exist in public. Until
  a specification appears, no gas rate in this pack is a capacity constraint — they are production
  assumptions resting on an unknown facility.
]

#heading(level: 2)[3.6    Voidage and VRR — the conclusion inverts]
The previous revision concluded over-injection. Priced against the correct vessel and the correct
definition, the direction reverses.

#figure(
  image("fig/fig4_vrr.png", width: 100%),
  caption: [Figure 4 — Oil-term voidage against injection capacity. At 25,000 bopd and Bo 1.30, voidage is 32,500 rb/d; Excalibur injects 20,000 bwpd. The 75,000 line is the cancelled tender. Source: L-07, L-12, L-34, L-35. #tag("DERIVED")],
)

#v(2mm)
#align(center)[
  #block(fill: lightbg, inset: 9pt)[
    #set text(size: 8.7pt)
    #table(columns: (78mm, 32mm),
      table.header([*VRR, counted properly*], [*Value*]),
      [Injection capacity (L-07)], [20,000 bwpd],
      [Oil-term voidage at 25,000 bopd, Bo 1.30 (L-35)], [32,500 rb/d],
      [*VRR on the oil term alone (L-36)*], [*0.62*],
      [Adding produced water and free gas to the denominator], [*lower still*],
    )
  ]
]

#v(1mm)
#text(size: 8.6pt)[
  Definition used: VRR = Σ injected reservoir barrels ÷ Σ produced reservoir barrels, where the
  denominator is oil × Bo *plus* produced water × Bw *plus* free gas × Bg. Counting only the oil
  term already gives 0.62; including the terms the definition requires can only reduce it. On the
  public record this vessel would *under-replace* voidage, not over-inject.
]

#open-banner[
  *Two things this does not prove.* First, whether water injection is planned at all — the public
  record is silent. Second, whether gas is re-injected, which would change total voidage and is not
  disclosed (L-09). The 0.62 is an oil-term statement, and is labelled as one.
]

#block(breakable: false)[
#heading(level: 2)[3.7    What Part 3 establishes and what it does not]
#grid(columns: (1fr, 1fr), gutter: 9pt,
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.0pt)
    *Established*
    #v(2pt)
    - The vessel as bought produces 25,000 bopd — 37.5 per cent below the 40,000 bopd on which the
      development case has been described.
    - At that ceiling the P50 resource depletes in 15.3 years, range 14.5–16.1.
    - The 9.6-year figure is tender arithmetic, not a subsurface result.
    - On the oil term, VRR is 0.62 — under-replacement.
    - The ratio of totals is not a GOR and cannot size anything.
  ],
  block(fill: rgb("#FDF4F4"), stroke: (left: 3pt + red), inset: 8pt)[
    #set text(size: 8.0pt)
    *Not established*
    #v(2pt)
    - Post-conversion topsides (L-42) — no public disclosure exists.
    - Whether ten wells can deliver even 25,000 bopd — no productivity data.
    - Whether recovery is 35 or 40 per cent, or what the drive mechanism is.
    - Whether water injection is planned; whether gas is sold, injected or flared.
    - The economic limit (L-40, OPEN), and therefore true life and abandonment timing.
  ],
)
]

#v(2mm)
#text(size: 8.6pt)[
  None of the second column is closable by better analysis. Each item needs a document that is not
  public: a yard specification, a well test, a PVT report, a gas sales agreement, or a PSC. Listing
  them as OPEN is the honest output of this Part, and more useful than a filled-in number.
]

#heading(level: 2)[3.8    What would move these numbers]
Four inputs carry the whole of Part 3. Each is varied alone, holding the others at their stated value.

#figure(
  table(columns: (46mm, 26mm, 28mm, 1fr),
    table.header([*Change one input*], [*From → to*], [*P50 life*], [*Reading*]),
    [Plateau rate], [25,000 → 30,000], [15.3 → 12.7 yr], [A fifth more rate costs a fifth of the life. Neither is better; they are different projects.],
    [Plateau rate], [25,000 → 37,014], [15.3 → 10.3 yr], [The upgraded case: buys 12,000 bopd, loses 5 years.],
    [Recovery factor], [35 → 40 %], [14.3 → 16.3 yr], [Inside the P90–P10 band; the largest technical unknown.],
    [Volume factor], [1.30 → 1.40], [VRR 0.62 → 0.57], [Worse, not better: higher Bo means more reservoir barrels to replace.],
    [Recoverable], [−20 % → +20 %], [12.2 → 18.4 yr], [The sensitivity the tight bracket in §3.1 conceals.],
  ),
  caption: [Table 3.2 — Single-input sensitivities on the P50 case, at 25,000 bopd unless stated. Not a tornado chart: the inputs are not independent and no probability is attached.],
)

#v(1mm)
#text(size: 8.5pt)[
  The last row is the one to read twice. A ±20 per cent move on recoverable volume swings field life by six
  years — far more than the P90–P10 band implies. That is the cost of a bracket built from one public number:
  the Monte Carlo is reproducible and internally consistent, and it is narrower than reality because its
  inputs were never independent measurements.
]


#pagebreak()

// ═══════════════════════ PART 5 — THE EARTH ═══════════════════════
#heading(level: 1)[5    The Earth]

#text(size: 8.3pt, fill: grey)[The earlier revisions had no geology. This Part is the object the other Parts are about. Sources are numbered in Appendix E; every figure traces to Appendix B.]

#heading(level: 2)[5.1    Why this section exists]
A field development plan with production, facilities and economics but no geology is a plan for a
factory with no ore body. Earlier revisions described Limbayong as a set of volumes and a vessel.
That is the accountant's view of a mountain range.

This Part asks what the ground actually does. Seven things follow from the answer, and five of them
change decisions taken elsewhere in the pack.

#heading(level: 2)[5.2    Plate framework]
The northern margin of Borneo is the product of one long collision and one long escape.

Sea-floor spreading in the South China Sea ran from about 32 Ma to about 16 Ma, with a ridge
reorganisation near 23 Ma [Chang & Pubellier 2023]. Oceanic crust was consumed southward beneath
Borneo; the sediment stripped from the downgoing plate built the Crocker accretionary prism, now
exposed on land as folded turbidites. In the early Middle Miocene the attenuated continental crust
of the Dangerous Grounds reached the trench and could not be subducted. It collided. The prism was
uplifted and eroded, producing the surface every well in this province penetrates — the Deep
Regional Unconformity, locally the Middle Miocene Unconformity at about 16 Ma.

Compression has not stopped. Convergence runs at roughly 5 mm/yr, and compression resumed at about
1.9 Ma after a brief relaxation [Sapin et al. 2013]. The belt itself is long and narrow: over 800 km
along the margin, about 100 km wide in southern NW Sabah and about 40 km in the north, containing
at least nine mapped anticlines [Ingram et al. 2004; Sulaiman 2017; Madon 2022]. Shortening of at
least 8 km has accumulated since about 10 Ma [Wu et al. 2020] — about 0.8 mm/yr on average, an
arithmetic derivation, not a published rate.

#figure(
  image("fig/fig5_tectonic.png", width: 100%),
  caption: [Figure 5.1 — Plate framework. South China Sea, the rifted Dangerous Grounds block, the Borneo margin and the deformation front. Limbayong sits in the deepwater belt outboard of the shelf, not on the platform. Coastline: Natural Earth 1:50m. Outlines schematic; position exact. Sources S-19, S-14. #tag("DERIVED")],
)

#v(2mm)
#text(size: 8.6pt)[
  Two things matter downstream. The belt is *young and still shortening* — thrusting is Pliocene to
  Holocene [Hesse et al. 2010]. And the belt *is built of the same sediment the reservoirs are made
  of*: the folds are the delta, shortened. That is why the traps are long, narrow and faulted rather
  than broad and simple.
]

#open-banner[
  *The literature is genuinely contested on one point, and it matters.* Whether shortening is driven
  by gravity (delta loading on an overpressured shale detachment) or by basement convergence has been
  argued for two decades. The current position is a hybrid: gravity-driven in the south-west, with a
  far-field basement component that increases northward [Hesse et al. 2009; Carboni et al. 2019;
  Ogawa, Back & Littke 2023]. Both mechanisms produce the same trap geometry, so the ambiguity does
  not change this Part — but it does mean nobody can date the folds from first principles alone.
]

#heading(level: 2)[5.3    The belt, seen from the sea surface]
Bathymetry is the cheapest structural interpretation available: it is the fold belt expressed as
topography.

#figure(
  image("fig/fig5_bathy.png", width: 100%),
  caption: [Figure 5.2 — Real bathymetry and shaded relief, NW Sabah deepwater. The NE–SW grain is the fold-thrust belt; each ridge is a shortened anticline. Limbayong reads 994 m from the grid, consistent with the 900–1,200 m reported depth (L-16, L-43). Relief: NOAA/ETOPO, ~450 m cells. #tag("DERIVED")],
)

#v(2mm)
#text(size: 8.6pt)[
  The DEM gives four measurements, each independently checkable:
]
#v(1mm)
#table(columns: (64mm, 26mm, 1fr),
  table.header([*Measurement*], [*Value*], [*How obtained*]),
  [Water depth at the field], [994 m], [DEM cell at 5.888 N, 114.510 E — L-43],
  [Seafloor slope at the field], [3.2°], [DEM gradient; 90th percentile 6.3° in the 900–1,200 m band],
  [Shelf break along section A–A′], [144 km along the transect], [−200 m crossing — L-54],
  [Crest-to-trough relief, fold ridges], [170–570 m, locally ~850 m], [DEM, independent analysis — S-31],
  [Total relief across the 30 km window], [1,600 m], [DEM window minimum and maximum — L-55],
)

#v(2mm)
#text(size: 8.6pt)[
  Two independent analyses of the same public grid agree: slope in the 900–1,200 m band has a median
  of 2.6° with 2.5 per cent of cells steeper than 10°, and the site itself is a gentle 3.2°. That is
  a real finding, and it is good news twice over: a moored unit sits on benign ground, and the
  shallow section at the field is not dominated by mass-transport debris. The hazard is not the slope
  at the field. It is the slope above it, and the faults beneath it.
]

#figure(
  image("fig/fig5_section.png", width: 100%),
  caption: [Figure 5.3 — Real bathymetric section A–A′ across the margin, from shelf, across the fold-thrust belt, into the basin. Limbayong projects onto the belt at 994 m. Vertical exaggeration ≈32×. Data: NOAA/ETOPO DEM (S-14). #tag("DERIVED")],
)

#heading(level: 2)[5.4    Stratigraphy, and what the reservoir actually is]
The Sabah "Stages" scheme is Bol and van Hoorn's (1980), erected from Shell seismic and summarised
by Krebs (2011): four unconformity-bounded stages. I and II are Upper Cretaceous to Oligocene
deep-marine flysch — the Crocker and Rajang. III is Lower to Middle Miocene deltaic to shelf.
IV is Middle Miocene to Quaternary, subdivided IVA to IVG, and *it is the stage that hosts the
deepwater reservoirs*.

#figure(
  image("fig/fig5_strat.png", width: 100%),
  caption: [Figure 5.5 — Tectonostratigraphic column. Stages I–III are deep-marine clastics of the accretionary wedge, truncated by the Deep Regional Unconformity at about 16 Ma; Stage IV is the prograding shelf–slope system hosting the deepwater fans. Four fan cycles are mapped: Kebabangan, Kinarut, Kamunsu and Pink. The Kinarut fan is the regional analogue for the reservoir interval, not a stated Limbayong reservoir. After Bol & van Hoorn (1980), Krebs (2011), Cullen et al. (2006). #tag("DERIVED")],
)

#v(2mm)
#text(size: 8.6pt)[
  Note the correction this Part carries. Earlier drafts referred loosely to a "Stages I–V" scheme.
  There is no five-stage scheme in the literature: it is four, with Stage IV subdivided. A
  Pliocene–Recent "Stage V" appears in some working usage but is not part of the original
  definition. The named surfaces — DRU, LIU, UIU, SRU — come from Levell (1987).
]

#v(2mm)
#text(size: 8.6pt)[
  The reservoir is not a layer cake. The operator's own description is precise: *"vertical
  intercalation of thin-bed, thick sand reservoir"* (S-13). Unpacked, that is the whole engineering
  problem in eight words.
]
#v(1.5mm)
#text(size: 8.6pt)[
  Thin beds and thick beds interbedded means permeability varies by orders of magnitude over metres.
  Flow will not be homogeneous. Water or gas will find the thick beds first; the thin beds will hold
  oil the pressure front reaches late or never. Recovery in such a system is not a property of the
  field — it is a property of completion design, spacing and pressure support. Which is exactly why
  the operator's paper talks about *"high-grading producer-injector pairing"* rather than about a
  field-wide recovery factor.
]
#v(1.5mm)
#text(size: 8.6pt)[
  For calibration, the nearest analogue with published numbers is Kikeh: deepwater turbidite lobes
  interbedded with mass-transport deposits, 28–32 per cent porosity and about 1,000 mD
  [Jones et al. 2016]. That is excellent rock. It is also rock interbedded with shales at the
  scale that breaks up flow.
]

#heading(level: 2)[5.5    The trap, and why one field is really several]
Limbayong is a *severe elongated structure: 30 km long, 2.5 km wide* (S-13). Aspect ratio 12:1.
That is not a dome. It is a ridge, and ridges in thrust belts are cut by cross-faults.

#figure(
  image("fig/fig5_structure.png", width: 100%),
  caption: [Figure 5.4 — Schematic cross-section: a thrust-cored anticline with a gas column over an oil rim, cut into compartments by thrust splays, detached on overpressured shale, with crestal faulting. Not from seismic and not to scale — topology only. Geometry after published descriptions of the NW Borneo belt (S-13, S-19, S-21). #tag("ASSUMED")],
)

#v(2mm)
#text(size: 8.6pt)[
  How many compartments? The published thrust spacing is *3–15 km* in the southern part of the belt
  and 1–9 km in the compressed north, with three-dimensional linkages about 10 km apart
  [Sulaiman 2017; Wu et al. 2020]. Divide 30 km by that spacing and the structure contains roughly
  *six to fifteen fault-bound panels*.
]
#v(1.5mm)
#text(size: 8.6pt)[
  Ten development wells across those panels is one well per one or two blocks. That is not obviously
  too few — and this Part corrects an earlier overstatement on exactly this point. Ten wells is a
  defensible number for the compartment count. The problem is not the count of wells. It is the
  volume each well can reach.
]

#figure(
  image("fig/fig5_seal.png", width: 100%),
  caption: [Figure 5.6 — *Panel A:* retained hydrocarbon column is the minimum of structural closure and capillary seal capacity; beyond about 250 m the trap cannot fill itself any further. *Panel B:* 139.5 MMbbl divided across 10 or 15 wells falls below the 20–100 MMstb/well analogue band for deepwater turbidite developments. Sources L-29, L-59, L-61. #tag("DERIVED")],
)

#v(1mm)
#text(size: 8.6pt)[
  Panel B is the uncomfortable one. At 10 wells the field yields 13.9 MMbbl per well. Deepwater
  turbidite analogues deliver 20 to 100 [Inikori et al. 2008]. Below the floor of the analogue range,
  there are only three explanations, and they are distinguishable: the resource is smaller than
  139.5 MMbbl; the wells do not reach all the compartments; or the compartments do not connect to
  each other. Interference testing between the first two wells separates the last two cheaply. Nothing
  cheap separates the first.
]

#v(2mm)
#text(size: 8.6pt)[
  And there is a second, independent brake on column height. Capillary seal capacity — not
  four-way closure, not mechanical seal, and not spill geometry — controls how much hydrocarbon a
  trap in this basin can hold [Ngu et al. 2010]. The published P50 is about *250 m of column for
  deepwater turbidites*, against about 30 m for deltaics [Kessler & Jong 2018]. Some structure in this
  belt is documented as *not filled to spill*, with fault-dependent columns.
]
#v(2mm)
#block(fill: rgb("#FDF4F4"), stroke: (left: 3pt + red), inset: 9pt, width: 100%)[
  #set text(size: 8.4pt)
  *Read Figure 5.6A against any volumetric number in this pack.* If the structure's closure exceeds
  roughly 250 m, the excess is not gas that exists — it is gas the seal cannot hold. The 790.9 bcf
  figure is a trap-volume estimate. What the trap can retain is a seal-capacity estimate, and it is
  very likely smaller. This is the strongest reason to treat gas as the uncertain phase and the oil
  rim as the bankable one.
]

#heading(level: 2)[5.6    Charge, leakage and the oil rim]
The discovery history is a geological argument in three dates.

#table(columns: (24mm, 34mm, 1fr),
  table.header([*Date*], [*Event*], [*What it implies*]),
  [early 2000s], [Limbayong-1, gas], [A gas accumulation found first. Public estimates near 800 bcf (S-16).],
  [17 Mar 2014], [Limbayong-2 appraisal: 136 m of oil-bearing sand], [An oil column beneath the gas. Shell 35%, ConocoPhillips 35%, PETRONAS Carigali 30% at the time (S-15).],
  [2026], [FID, 100% PCSB], [The oil rim, not the gas, is what turned a stranded gas find into a development.],
)

#v(2mm)
#text(size: 8.6pt)[
  Why is there an oil rim under a gas field at all? The literature gives a specific mechanism, and it
  is stronger than the inference in the previous revision. In this basin, *a leaky trap is required
  for significant oil*: gas is lost preferentially by capillary failure while oil is retained
  [Algar 2012]. That is the accepted explanation for oil in a province everybody calls gas-prone, and
  it predicts oil rims beneath gas caps. Kikeh's gas cloud — gas escaping over oil, degrading the
  seismic image — is the same process observed.
]
#v(2mm)
#text(size: 8.6pt)[
  Limbayong fits that model exactly. A gas discovery in 2002. An appraisal eleven years later finding
  136 m of oil sand. That is what a partially leaking gas trap with an oil rim looks like. Three
  consequences follow, and none of them is in the earlier revisions:
]
#v(1mm)
#set enum(numbering: "1.")
+ *The gas column is probably not fully retained.* Both the capillary seal limit (250 m P50) and the
  leakage mechanism point the same way. 790.9 bcf should be read as an upper bound on what the trap
  could hold, before seal capacity and leakage are applied.
+ *The oil rim is the resource that stayed.* Consistent with being missed by the first well and found
  by an appraisal.
+ *The top seal is a dynamic boundary.* Crestal faults formed in a Late Pliocene deformation phase are
  the same faults a gas chimney would use. Seal integrity should be tested, and any development that
  changes pressure in the gas cap changes the leakage driving force.

#v(2mm)
#text(size: 8.6pt)[
  There is province-scale support for active leakage, not just a mechanism: about 50 mud-volcano
  centres coalesce into a roughly 1,900 km² canopy in the North Sabah–Pagasa wedge [Morley et al.
  2022], and heat-flow measurements include a single megaseep at 604 mW/m² [Zielinski et al. 2007].
  That much gas has reached the sea floor from this system.
]

#open-banner[
  *Not established:* whether seepage is active on the Limbayong structure specifically. The mud
  volcanoes are documented along the trend, not on this crest. This is a hypothesis with a mechanism,
  an analogue and a province-scale signal — not a measurement. It is cheap to test: a seabed
  geochemical survey and an AUV or repeat-bathymetry survey over the crest.
]

#heading(level: 2)[5.7    Geomechanics — the Earth pushing back on the drill bit]
The operator has published the drilling problem, which is unusual and useful (S-17):

- the drilling margin is *less than 0.5 ppg* on some wells, even at the surface section;
- most deep wells must be drilled *highly deviated, in the direction of minimum horizontal stress*;
- the consequences named are stuck pipe, hole instability, differential sticking and skin damage;
- managed pressure drilling is required, with a multi-phase model for gas-influx transport.

#v(1mm)
#text(size: 8.6pt)[
  Why is the window so tight? The regional answer is published. Overpressure in this system is
  generated by disequilibrium compaction in prodelta shales and then *vertically transferred along
  faults* into the reservoirs [Tingay et al. 2007, 2008]. At the base of the wedge the pore-pressure
  ratio Pp/σv is *0.91–0.97* — close to lithostatic [Sulaiman 2017]. At a ratio of 0.95 with a
  2.3 g/cm³ overburden, pore pressure is about 18.2 ppg equivalent, which leaves very little room
  before the fracture gradient. That is an arithmetic derivation from the cited ratio, and it is why
  the operator reports a sub-0.5 ppg margin.
]
#v(1.5mm)
#text(size: 8.6pt)[
  A half-pound window is not a drilling inconvenience. It is a cost and schedule driver, a well-count
  constraint, and a reason the tenth well may cost more than the first. It also means one mud-weight
  programme cannot cover ten wells if compartments are pressured differently — and inter-compartment
  pressure differences are documented in a deepwater NW Borneo field [Chin et al. 2011].
]

#heading(level: 2)[5.8    A contradiction this Part cannot resolve]
One genuine conflict surfaced in assembling the literature, and it should be shown rather than
smoothed.

#figure(
  image("fig/fig5_thermal.png", width: 100%),
  caption: [Figure 5.7 — Temperature against depth for the two published gradients in this province. On the deepwater gradient the reservoir passes the 140 °C threshold at which quartz cementation becomes significant; on the shelf gradient it does not. Sources L-64, L-65. #tag("DERIVED")],
)

#v(1.5mm)
#text(size: 8.6pt)[
  The shelf and delta record 29–34 °C/km from over 600 bottom-hole temperatures. The deepwater belt
  is hotter: 66.5 °C/km in acreage along strike, and heat flow of 66 mW/m² against 42 mW/m² in the
  Sabah Trough [Madon & Jong 2021]. At 66.5 °C/km a reservoir 2.5 km below mudline sits near 169 °C.
]
#v(1.5mm)
#text(size: 8.6pt)[
  That matters because quartz cementation, the main porosity destroyer in hot sandstones, becomes
  significant above about 140 °C. One strand of the literature holds that these reservoirs are not
  hot enough for it; the regional geothermal data say the deepwater belt probably is. The two cannot
  both be right, and the difference decides whether the reservoir is Kikeh-like at 28–32 per cent
  porosity or materially tighter.
]

#open-banner[
  *C-10 — thermal regime at Limbayong.* Unresolved. It changes porosity, productivity, topsides
  metallurgy and elastomer selection, wax and hydrate margins, and the base of the hydrate stability
  zone. It is settled by one measured bottom-hole temperature from the field, which the operator has.
  Until then this pack carries a design band of roughly 120–200 °C rather than a number.
]

#heading(level: 2)[5.9    What the Earth changes]
Six findings now. Each moves a decision that lives in another Part.

#figure(
  table(columns: (8mm, 1fr, 1fr),
    table.header([*ID*], [*Finding from the ground*], [*Consequence for the FDP*]),
    [E-1], [A 30 × 2.5 km thrust ridge cut by faults at 3–15 km spacing — six to fifteen panels — which the operator says defeats drainage and pressure maintenance (S-13, S-21).], [The single-tank model is invalid. Recovery factor and plateau are outputs of well placement, not inputs. The 139.5 MMbbl P50 is a resource in several tanks, not one.],
    [E-2], [Ten wells is one per one or two panels — appropriate for the compartment count — but per-well volume is 13.9 MMbbl against a 20–100 analogue band (L-61).], [Well count is *not* the constraint; connected volume per well is. Interference and tracer tests between the first wells separate the explanations. This corrects the previous revision, which said well count was the lever.],
    [E-3], [A leaky trap is required for significant oil in this basin; gas is lost preferentially. Limbayong: gas 2002, then 136 m of oil sand (S-15, Algar 2012).], [790.9 bcf is a trap-fill estimate on a leaking trap. The oil rim is the bankable phase. Test seal and seepage before committing gas export capacity.],
    [E-4], [Capillary seal capacity caps the column at about 250 m P50 in these turbidites (L-59).], [Structure larger than 250 m of closure does not hold more gas. Volumetrics must be capped by seal, not by trap geometry. This is a new constraint in this revision.],
    [E-5], [Drilling margin under 0.5 ppg; Pp/σv 0.91–0.97; overpressure transferred along faults; inter-compartment pressure differences documented (S-17, S-21, Chin 2011).], [Well cost carries a geomechanical premium, and one mud-weight programme may not fit ten wells. Fewer, better-placed wells also carry less cumulative risk.],
    [E-6], [About 800 MMboe scattered across deepwater Sabah; operator states intent to be the East Malaysia deepwater hub (S-13, S-17).], [The value case for Limbayong is not 139 MMbbl. It is the hub. That is a different economic question — and a stronger one.],
  ),
  caption: [Table 5.1 — Earth findings and their consequences. E-1 to E-5 are sourced; E-6 is strategic and sourced to operator statements.],
)

#v(2mm)
#text(size: 8.6pt)[
  *Read E-1 and E-6 together.* The field is small and compartmentalised. That is a poor standalone
  investment and an excellent infrastructure anchor for 800 MMboe of neighbours. The earlier revisions
  argued about the vessel; the ground says the argument should be about phasing and hub economics.
  That is the new light this Part contributes.
]

#heading(level: 2, numbering: none)[5.10    Seismicity is not the hazard here]
One thing the Earth does *not* say, and it is worth stating because a reader might assume it.

#v(1mm)
#text(size: 8.6pt)[
  The belt is active, but it is not seismic. The USGS catalogue records 23 events of M≥3 within
  300 km of the field since 1970, and none within 50 km; every shallow M≥5 in the record is onshore
  [S-27]. NW Sabah also sits at the southern margin of the typhoon belt rather than inside it, with
  monsoon-driven seas the design case and cyclones that "rarely reach tropical storm strength"
  [Anokhin et al. 2019].
]
#v(1mm)
#text(size: 8.6pt)[
  That does not make the ground benign — it relocates the hazard. Deformation here happens as
  *aseismic creep and episodic failure*: folds that reach the sea floor, intensive crestal normal
  faulting, partial crestal collapse, thrusting to the Holocene [Hesse et al. 2010]. The sea floor is
  also mobile in the other direction: the Brunei Slide moved 1,200 km³ over 5,300 km², with a 120 km
  runout, 2,000–7,000 years ago, and older buried slides show recurrence [Gee et al. 2007]. At 994 m
  the field is inside the hydrate stability field, which begins near 500 m [Jong et al. 2020].
]
#v(1mm)
#text(size: 8.6pt)[
  So the design case is not earthquake. It is *slow ground movement, shallow gas and hydrates,
  mass-transport debris in the shallow section, and a mooring site that must avoid vents and
  gas-charged mudline soil.* That is a different set of surveys and a different set of acceptance
  criteria from a seismic design case, and it should be scoped accordingly.
]

#heading(level: 2, numbering: none)[5.11    Geological risk register]
#figure(
  table(columns: (8mm, 42mm, 40mm, 42mm, 1fr),
    table.header([*ID*], [*Risk*], [*Evidence*], [*Impact*], [*Cheapest test*]),
    [G-1], [Compartments not drained], [6–15 panels; operator reports lateral compartmentalisation defeating drainage], [Recovery factor falls; plateau shortens; stranded volume], [Interference test and tracers between first two wells],
    [G-2], [Column capped by seal, not trap], [Capillary P50 ≈250 m; some structures not filled to spill], [Gas volume below volumetric estimate; thinner oil rim], [Seal capacity from core/MICP on the first well],
    [G-3], [Reservoir hotter and tighter than analogue], [66.5 °C/km along strike puts reservoir past 140 °C], [Porosity loss; lower productivity; metallurgy and elastomer spec change], [One measured bottom-hole temperature],
    [G-4], [Top seal leaks at crest], [Crestal faults; leaky-trap mechanism; province-scale mud volcanism], [Gas column smaller than assumed; pressure-dependent leakage], [Seabed geochemical survey and AUV bathymetry over the crest],
    [G-5], [Drilling margin narrower than planned], [Under 0.5 ppg reported; Pp/σv to 0.97; inter-compartment differences], [Well cost and schedule overrun; stuck pipe], [Pre-drill pore pressure from the next appraisal opportunity],
    [G-6], [Shallow geohazard at the FPSO site], [Hydrates from 500 m; Brunei-type slide recurrence; vents and chimneys], [Mooring capacity loss or top-hole problem], [High-resolution site survey before mooring design],
  ),
  caption: [Table 5.2 — Six geological risks, each with a test that costs less than the decision it informs. G-3 is new in this revision and is the one with no public answer.],
)

#v(2mm)
#heading(level: 2, numbering: none)[5.12    In one page]
#block(fill: lightbg, inset: 10pt, width: 100%, stroke: (left: 3pt + navy))[
  #set text(size: 8.5pt)
  Limbayong is not a dome with a vessel attached. It is a *30 km ridge* in a fold-thrust belt that is
  still shortening, made of the same delta sediment that was shortened to form it, cut every 3 to 15
  kilometres by faults whose effect the operator describes as defeating drainage and pressure
  maintenance.
  #v(2pt)
  The reservoir is thin beds and thick beds interbedded — heterogeneous at the scale of metres. That
  is why recovery is a design question and not a number.
  #v(2pt)
  Gas is the phase that leaks in this basin; a leaky trap is what produces oil. An appraisal well
  found 136 m of oil sand eleven years after the discovery well found gas, which is exactly what that
  mechanism predicts. And the seal, not the trap, sets how big the gas column can be — about 250 m at
  the median, not the full structural closure.
  #v(2pt)
  Ten wells is about right for six to fifteen compartments. What is not right is the volume per well:
  13.9 MMbbl against an analogue band of 20 to 100. That points at connectivity, not well count — and
  it is testable with an interference test before the rig moves.
  #v(2pt)
  The drilling margin is under half a pound per gallon and the overpressure is transferred along the
  same faults that make the compartments. Every well is expensive and every well carries risk.
  #v(2pt)
  And the field is small: 139 MMbbl. What makes it worth building is not the 139. It is the
  800 MMboe of neighbours and the operator's stated intention to be the deepwater hub for East
  Malaysia. *That is the investment case, and it is a different case from the one being told in public.*
]

#pagebreak()

// ═══════════════════════ APPENDIX B ═══════════════════════
#heading(level: 1, numbering: none)[Appendix B — Assumptions ledger]
#text(size: 8.2pt, fill: grey)[69 rows. Independence = number of independent owners of the evidence; the same owner counts once, however many pages it publishes.]

#heading(level: 2, numbering: none)[Reproducibility]
#block(fill: lightbg, inset: 8pt, width: 100%)[
  #set text(size: 7.6pt, font: "DejaVu Sans Mono")
  #grid(columns: (1fr, 1fr), gutter: 12pt, row-gutter: 1.1pt,
    [L-22 = (347 + 398) / 2 = 372.5], [L-31 = 139.5e6 / (25000 × 365) = 15.29],
    [L-25 = (0.35 + 0.40) / 2 = 0.375], [L-32 = 132.6e6 / (25000 × 365) = 14.53],
    [L-35 = 25000 × 1.30 = 32 500 rb/d], [L-33 = 146.8e6 / (25000 × 365) = 16.09],
    [L-36 = 20 000 / 32 500 = 0.615], [9.57 = 139.5e6 / (40000 × 365)],
    [L-37 = 790.9e3 / 139.5 = 5 670 scf/bbl], [seed = 20261019, N = 20 000],
  )
]

#figure(
  table(columns: (9mm, 38mm, 18mm, 9mm, 19mm, 6mm, 1fr),
    table.header([*Row*], [*Parameter*], [*Value*], [*Unit*], [*Class*], [*Ind.*], [*Basis / formula*]),
    [L-01], [Vessel identity], [IMO 9417103], [—], [VERIFIED], [2], [IMO in Bursa filing; name history in press],
    [L-02], [Year built], [2007], [year], [VERIFIED], [2], [Bursa filing; commissioned 2008 per press],
    [L-03], [Storage — design], [300,000], [bbl], [VERIFIED], [1], [Bursa filing, primary document],
    [L-04], [Storage — working], [270,000], [bbl], [REPORTED], [1], [Owner factsheet via trade press],
    [L-05], [Oil capacity — as-built], [25,000], [bopd], [VERIFIED], [2], [Trade press 2022; vessel page],
    [L-06], [Total liquids], [30,000], [bpd], [REPORTED], [1], [Owner factsheet],
    [L-07], [Water injection], [20,000], [bwpd], [REPORTED], [1], [Owner factsheet; corroborated],
    [L-08], [Produced water], [25,000], [bwpd], [REPORTED], [1], [Owner factsheet],
    [L-09], [Gas handling], [not published], [—], [OPEN], [0], [No public figure for this hull],
    [L-10], [Tender oil], [40,000], [bopd], [VERIFIED], [2], [World Energy Reports via press],
    [L-11], [Tender gas], [90], [MMscfd], [VERIFIED], [1], [World Energy Reports via press],
    [L-12], [Tender water injection], [75,000], [bwpd], [VERIFIED], [1], [World Energy Reports via press],
    [L-13], [Tender storage], [600,000], [bbl], [VERIFIED], [1], [World Energy Reports via press],
    [L-14], [Oil recoverable, public], [139], [MMbbl], [REPORTED], [1], [Resource tracker; P50 calibration only],
    [L-15], [Gas recoverable, public], [790.9], [bcf], [REPORTED], [1], [Resource tracker],
    [L-16], [Water depth], [900–1200], [m], [VERIFIED], [2], [Project description; 2026 press],
    [L-17], [Distance offshore], [120], [km], [VERIFIED], [2], [Project description],
    [L-18], [Field type], [oil + NAG], [—], [VERIFIED], [2], [Project description; discovery reporting],
    [L-19], [Working interest], [100], [% PCSB], [VERIFIED], [1], [Trade press 2021],
    [L-20], [FID date], [2026-08-28], [date], [REPORTED], [1], [Trade press],
    [L-21], [OOIP bracket low], [347], [MMbbl], [ASSUMED], [0], [Brief; back-calculated at 40% RF],
    [L-22], [OOIP bracket mode], [372.5], [MMbbl], [DERIVED], [0], [(L-21 + L-23) / 2],
    [L-23], [OOIP bracket high], [398], [MMbbl], [ASSUMED], [0], [Brief; back-calculated at 35% RF],
    [L-24], [Recovery factor low], [0.35], [frac], [ASSUMED], [0], [Brief],
    [L-25], [Recovery factor mode], [0.375], [frac], [DERIVED], [0], [(L-24 + L-26) / 2],
    [L-26], [Recovery factor high], [0.40], [frac], [ASSUMED], [0], [Brief],
    [L-27], [OOIP–RF correlation], [+0.60], [rho], [ASSUMED], [0], [HERMES: better rock raises both],
    [L-28], [Recoverable P90], [132.6], [MMbbl], [DERIVED], [0], [Monte Carlo, L-21..L-27],
    [L-29], [Recoverable P50], [139.5], [MMbbl], [DERIVED], [0], [Monte Carlo; reconciles to L-14],
    [L-30], [Recoverable P10], [146.8], [MMbbl], [DERIVED], [0], [Monte Carlo],
    [L-31], [Life at 25,000 — P50], [15.3], [yr], [DERIVED], [0], [L-29 ÷ (25,000 × 365)],
    [L-32], [Life at 25,000 — P90], [14.5], [yr], [DERIVED], [0], [L-28 ÷ (25,000 × 365)],
    [L-33], [Life at 25,000 — P10], [16.1], [yr], [DERIVED], [0], [L-30 ÷ (25,000 × 365)],
    [L-34], [Formation volume factor], [1.30], [rb/stb], [ASSUMED], [0], [Deepwater analogue; no PVT],
    [L-35], [Oil-term voidage], [32,500], [rb/d], [DERIVED], [0], [25,000 × L-34],
    [L-36], [VRR, oil term only], [0.62], [ratio], [DERIVED], [0], [L-07 ÷ L-35],
    [L-37], [Gas:oil ratio of totals], [5,640], [scf/bbl], [DERIVED], [0], [L-15 × 10³ ÷ L-14 — not a GOR],
    [L-38], [Subsea award 2021], [250–500], [US\$M], [VERIFIED], [2], [TechnipFMC "substantial" band],
    [L-39], [Subsea award 2026], [75–250], [US\$M], [REPORTED], [1], [TechnipFMC "significant", press],
    [L-40], [Economic limit], [not stated], [—], [OPEN], [0], [Needs price deck, opex, fiscal terms],
    [L-41], [Fiscal terms], [not public], [—], [OPEN], [0], [PSC text unavailable],
    [L-42], [Post-conversion topsides], [not published], [—], [OPEN], [0], [No MISC/MMHE disclosure],
    [L-43], [Water depth, measured], [994], [m], [DERIVED], [1], [Read from NOAA/ETOPO DEM at the field coordinate],
    [L-44], [Structure length], [30], [km], [VERIFIED], [1], [Operator paper, IPA complexity description],
    [L-45], [Structure width], [2.5], [km], [VERIFIED], [1], [Operator paper],
    [L-46], [Appraisal wells since 2002], [4], [wells], [VERIFIED], [1], [Operator paper],
    [L-47], [Net oil sand, Limbayong-2], [136], [m], [VERIFIED], [2], [2014 discovery report, two outlets],
    [L-48], [Water depth, reported], [1000], [m], [VERIFIED], [1], [2014 discovery report, Block J],
    [L-49], [Drilling margin, some wells], [under 0.5], [ppg], [VERIFIED], [1], [Operator drilling paper],
    [L-50], [Kinarut fan age, analogue], [10.6], [Ma], [VERIFIED], [1], [Cullen et al., AAPG S&D 90052],
    [L-51], [Scattered deepwater resource], [~800], [MMboe], [VERIFIED], [1], [Operator paper, Sabah deepwater],
    [L-52], [Compartment width, inferred], [2–5], [km], [ASSUMED], [0], [Fault spacing in a 30 km belt; unmeasured],
    [L-53], [Seafloor slope at field], [3.2], [deg], [DERIVED], [1], [DEM gradient; 95th pct 7.8 deg in 30 km],
    [L-54], [Shelf break on A–A'], [144], [km], [DERIVED], [1], [−200 m crossing on the DEM transect],
    [L-56], [Thrust spacing, fold belt], [3–15], [km], [VERIFIED], [1], [Sulaiman 2017 Table 3.2; 1–9 km in the compressed north],
    [L-57], [Minimum shortening since ca. 10 Ma], [~8], [km], [VERIFIED], [1], [Wu et al. 2020, Geosphere 16:329],
    [L-58], [Wedge-base Pp/σv], [0.91–0.97], [ratio], [VERIFIED], [1], [Sulaiman 2017 after Morley 2007],
    [L-59], [P50 capillary column, turbidites], [250], [m], [VERIFIED], [1], [Kessler & Jong 2018, Berita Sedimentologi 40],
    [L-60], [P50 capillary column, deltaics], [30], [m], [VERIFIED], [1], [Kessler & Jong 2018],
    [L-61], [Analogue per-well EUR, Bonga], [20–100], [MMstb], [VERIFIED], [1], [Inikori et al. 2008],
    [L-62], [Kikeh porosity], [28–32], [%], [VERIFIED], [2], [Jones et al. 2016; regional summaries],
    [L-63], [Kikeh permeability], [~1000], [mD], [VERIFIED], [1], [Jones et al. 2016],
    [L-64], [Geothermal gradient, deepwater belt], [66.5], [°C/km], [VERIFIED], [1], [Madon & Jong 2021, along strike],
    [L-65], [Geothermal gradient, shelf], [29–34], [°C/km], [VERIFIED], [1], [Madon & Jong 2021, 600+ BHT points],
    [L-66], [Seismicity M≥3 within 300 km since 1970], [23], [events], [VERIFIED], [1], [USGS FDSN catalogue],
    [L-67], [Mud volcano centres, North Sabah wedge], [~50], [centres], [VERIFIED], [1], [Morley et al. 2022],
    [L-68], [Brunei Slide volume], [1200], [km³], [VERIFIED], [1], [Gee et al. 2007],
    [L-69], [Hydrate stability onset], [~500], [m], [VERIFIED], [1], [Jong et al. 2020],
  ),
  caption: [Table B.1 — Assumptions ledger. Every number in Parts 1 and 3 resolves here. Rows with independence 0 are assumptions or open items by construction.],
)

#v(2mm)
#pagebreak()

// ═══════════════════════ APPENDIX E ═══════════════════════
#heading(level: 1, numbering: none)[Appendix E — Source register]

#figure(
  table(columns: (11mm, 1fr, 10mm),
    table.header([*ID*], [*Source, and what it establishes*], [*Ind.*]),
    [S-01], [Dagang NeXchange Berhad, Bursa Malaysia announcement, 20 Aug 2026 — disposal of FPSO *Excalibur* to MISC. IMO 9417103, year built 2007, design capacity 300,000 bbl, dimensions, US\$35.0M price, delivery at MMHE Pasir Gudang. *Primary document.*], [1],
    [S-02], [Offshore Magazine, "DNeX renames Avalon FPSO Excalibur", 4 Aug 2022. Name history from Sevan Hummingbird; commissioned 2008; 25,000 bbl/d; 270,000 bbl; 47 POB.], [1],
    [S-03], [Teekay factsheet for *Hummingbird Spirit*, Sevan 300. 25,000 bopd, 30,000 bpd liquids, 25,000 bwpd produced water, 20,000 bwpd injection.], [1],
    [S-04], [Offshore Technology, "Limbayong Deep-water Development Project", 15 Jun 2021. Water depth 900–1,200 m, 120 km offshore Sabah, Block G, oil and non-associated gas.], [1],
    [S-05], [Sevan Deepwater Technology vessel page for *Excalibur*. 270,000 bbl, 25,000 bopd, 7 riser slots.], [1],
    [S-06], [OE Digital, 23 Feb 2021, quoting World Energy Reports. Tender spec 40,000 b/d oil, 90 mmcf/d gas, 75,000 b/d water, 600,000 bbl; "substantial" contract US\$250–500M; 10 wells; 100% PETRONAS interest.], [1],
    [S-07], [Global Energy Monitor, Global Oil & Gas Extraction Tracker — Limbayong, data year 2023. 139 MMbbl liquids, 790.9 bcf, coordinates.], [1],
    [S-08], [Splash247, 16 Sep 2026 — iEPCI award, "significant" (US\$75–250M), 120 km offshore, 900–1,200 m.], [1],
    [S-09], [The Star and Borneo Post, 17–18 Mar 2014 — Limbayong-2 oil discovery; establishes the oil leg of an otherwise gas discovery.], [1],
    [S-10], [Trade press, 28 Aug 2026 — final investment decision taken. Partly paywalled.], [1],
    [S-11], [TechnipFMC investor release, 2021 — Limbayong subsea award; contract-value convention only.], [1],
    [S-12], [Natural Earth 1:10m coastline, public domain — map base for Figure 0.], [1],
    [S-13], [Mohamed Aiman Mohamed Najib et al., *Limbayong: Decoding Industry Top Decile Reservoir Complexity for Marginal Deepwater Development*, SPE 210079-MS, 2022. Structure 30 km × 2.5 km, fault frequency, lateral compartmentalisation, four appraisal wells since 2002, low-case pivot, upgrade provision, ~800 MMboe scattered resource.], [1],
    [S-14], [NOAA / ETOPO global digital elevation model, ImageServer extract, NW Sabah, ~450 m cells. Bathymetry, slope, transect.], [1],
    [S-15], [Offshore Energy, 17 Mar 2014 — Limbayong-2 appraisal, 136 m oil-bearing sands, Block J, ~1,000 m water, Shell 35% / ConocoPhillips 35% / PETRONAS Carigali 30%.], [1],
    [S-16], [Upstream via WOG News, 17 Mar 2014 — appraisal at the Limbayong gas field; ~800 bcf gas.], [1],
    [S-17], [Limbayong Deepwater Development Well Planning — A Collaboration with Geomechanics with MPD Approach, SPE 210549-MS, 2022. Margin under 0.5 ppg; MPD required; trajectories along minimum horizontal stress; first PCSB-operated deepwater asset.], [1],
    [S-18], [Cullen et al., *The Kinarut Sequence: A Model for Fan Deposition at the 10.6 Ma Sequence Boundary in NW Borneo Fold-Thrust Belt*, AAPG Search & Discovery 90052, 2006.], [1],
    [S-19], [Tan, D.N.K. and Lamy, J.M., *Tectonic evolution of the NW Sabah continental margin since the Late Eocene*, Bulletin of the Geological Society of Malaysia 27, 1990. Stages I–IV, Deep Regional Unconformity, seven tectonostratigraphic provinces, Late Pliocene crestal faulting.], [1],
    [S-21], [Sulaiman, N.B., *Controls on the Geometry and Evolution of the Deep-water Fold Thrust Belt of NW Borneo*, PhD thesis, University of Leeds, 2017 (open access). Thrust spacing 3–15 km; wedge-base Pp/σv 0.91–0.97; detachment in overpressured Setap shale.], [1],
    [S-22], [Wu, J., McClay, K. and Cortés Vera, J. de J., *Growth of triangle zone fold-thrusts within the NW Borneo deep-water fold belt*, Geosphere 16(1):329, 2020. DOI 10.1130/GES02106.1. Thrust linkages ~10 km apart; ~8 km shortening since ca. 10 Ma.], [1],
    [S-23], [Kessler, F.L. and Jong, J., *Hydrocarbon Retention in Clastic Reservoirs of NW Borneo*, Berita Sedimentologi 40(1):6–44, 2018. DOI 10.51835/bsed.2018.40.1.84. P50 column ~250 m turbidites, ~30 m deltaics.], [1],
    [S-24], [Inikori, L. et al., Bonga per-well ultimate recovery 20–100 MMstb, 2008. Analogue band, not a Limbayong figure.], [1],
    [S-25], [Jones et al., *The Kikeh Field, Sabah*, AAPG Search & Discovery, 2016. Turbidite lobes interbedded with MTDs; 28–32% porosity; ~1,000 mD; MTD top seal.], [1],
    [S-26], [Madon, M. and Jong, J., geothermal gradient and heat flow, NW Sabah: 29–34 °C/km shelf and delta from 600+ BHT points; 66.5 °C/km and 66 mW/m² in deepwater acreage along strike, 2021.], [1],
    [S-27], [USGS FDSN earthquake catalogue, query M≥3 within 300 km of 6.3°N 114.5°E since 1970. 23 events; none within 50 km; shallow M≥5 all onshore.], [1],
    [S-28], [Morley, C.K. et al., *A major Miocene deepwater mud canopy system: the North Sabah–Pagasa Wedge*, Geosphere, 2022. DOI 10.1130/GES02518.1. ~50 mud-volcano centres, ~1,900 km².], [1],
    [S-29], [Gee, M.J.R. et al., the Brunei Slide, 2007. 1,200 km³ over 5,300 km², mean 240 m thick, 120 km runout, 2,000–7,000 years old.], [1],
    [S-30], [Jong, J. et al., hydrate stability and bottom-simulating reflectors offshore NW Sabah, 2020. Stability from ~500 m water depth.], [1],
    [S-31], [Independent ETOPO 2022 analysis of the Block G 900–1,200 m band: median slope 2.6°, p90 6.3°, p99 12.4°, 2.5% above 10°; crest-to-trough relief 170–570 m, locally ~850 m.], [1],
    [S-32], [Bol, A.J. and van Hoorn, B., *Structural Styles in Western Sabah Offshore*, Bulletin of the Geological Society of Malaysia 12:1–16, 1980. The four-stage scheme.], [1],
    [S-33], [Krebs, W.N., *Upper Tertiary chronosequence stratigraphy of offshore Sabah and Sarawak*, Bulletin of the Geological Society of Malaysia 57:39–46, 2011. Summary of the stage scheme and its alternatives.], [1],
    [S-34], [Ngu, W. et al., *NW Borneo Deepwater Fold and Thrust Belt: What Controls the Hydrocarbon Column Height?*, 2010. DOI 10.3997/2214-4609-pdb.255.26. Capillary seal capacity dominates; fault-dependent columns; not fill-to-spill.], [1],
    [S-35], [Algar, S., *Big Oil from "Gas-Prone" Source Rocks and Leaking Traps: Northwest Borneo*, AAPG Search & Discovery 10465, 2012. A leaky trap is required for significant oil.], [1],
  ),
  caption: [Table E.1 — Source register. Thirty-five public sources. None is a primary operator document for volumes, costs or fiscal terms; that absence is the central limitation of the pack.],
)

#v(3mm)
#heading(level: 2, numbering: none)[Source limitations]
#text(size: 8.3pt)[
  *Two sources carry the vessel, one owner chain.* S-02 and S-03 describe the same hull and, on
  topsides, descend from the same owner. They are counted as one. S-01 is independent and confirms
  identity and dimensions but states no production rate. The 25,000 bopd figure is marked VERIFIED
  only because trade press and the hull owner agree; a sceptical reader should treat it as REPORTED.
]
#v(2mm)
#text(size: 8.3pt)[
  *The Limbayong link to this vessel is single-sourced.* It rests on trade reporting that MISC
  acquired Excalibur for Limbayong. Neither MISC nor PETRONAS has confirmed it. One low-quality
  outlet describes the vessel as being dismantled; that conflicts with the Bursa filing's stated
  delivery to MMHE for conversion, and is logged as noise rather than adopted or suppressed.
]
#v(2mm)
#text(size: 8.3pt)[
  *No cost, schedule or fiscal data is primary.* Award bands are contract-value conventions, not cost
  estimates. Nothing in this register supports a capital number.
]

#v(2mm)
#text(size: 8.3pt)[
  *The geological literature is read at abstract level in three cases.* ScienceDirect, GSA, OnePetro
  and ResearchGate block this host, so bibliographic metadata was verified through Crossref and content
  taken from open copies — GSM Bulletin PDFs, open-access theses, and AAPG Search & Discovery abstracts.
  Where a paper is cited only for what its abstract states, no specific number is attributed to it.
  Ingram et al. (2004) and Hesse et al. (2009) are cited at that level.
]

#v(2mm)
#text(size: 8.3pt)[
  *Two published numbers conflict, and both are carried.* The geothermal gradient is 29–34 °C/km from
  the shelf and 66.5 °C/km along strike in the deepwater belt. One strand of the reservoir literature
  assumes quartz cementation is not reached; that gradient says it probably is. Both are printed
  (Table 5.2, G-3) rather than one being chosen. This is the honest state of the public record.
]

#v(2mm)
#text(size: 8.3pt)[
  *No public Limbayong-specific reservoir data exists.* Not porosity, not net-to-gross, not fault-block
  width, not a bottom-hole temperature, not a recovery factor. Every such number in this pack is an
  analogue from Kikeh, Gumusut-Kakap, Malikai or Bonga, and is labelled as one.
]

#pagebreak()

// ═══════════════════════ APPENDIX F ═══════════════════════
#heading(level: 1, numbering: none)[Appendix F — Build status]
#text(size: 8.2pt, fill: grey)[Three content Parts of twelve complete, plus front matter. Published as a working draft so the honest denominator is visible.]

#figure(
  table(columns: (12mm, 46mm, 15mm, 1fr),
    table.header([*Part*], [*Content*], [*State*], [*Blocked by*]),
    [0], [Cover, control, decision frame], [*DONE*], [—],
    [1], [Basis and reconciliation], [*DONE*], [—],
    [2], [Executive summary], [—], [Must come last; consumes Parts 3–11],
    [3], [Production], [*DONE*], [L-42, for any post-upgrade case],
    [4], [Facilities and vessel], [—], [L-42 post-conversion specification],
    [5], [The Earth — geology, trap, charge], [*DONE*], [Reservoir properties and fault-block size remain non-public],
    [6], [Wells and drilling], [—], [No public well design or cost],
    [7], [Subsea and SURF], [—], [Award bands only; scope not public],
    [8], [Cost and schedule], [—], [AACE-class estimate needs contractor input],
    [9], [Economics], [—], [L-41 fiscal terms; single engine not yet built],
    [10], [Risk and assurance], [—], [Depends on 4–9],
    [11], [HSE, environment, decommissioning], [—], [No public EMS or decommissioning plan],
    [12], [Decision and recommendations], [—], [Depends on 2–11],
  ),
  caption: [Table F.1 — Part skeleton. Parts 1 and 3 complete; Part 0 is front matter, not a content Part. No Part is claimed that does not exist.],
)

#v(3mm)
#heading(level: 2, numbering: none)[System findings carried forward]
#text(size: 8.3pt)[
  The audit scored the agent stack around 3/10 for FDP work and named the causes: no shared number
  store, verification performed by the author, no fiscal or probabilistic engine. Two are now
  addressed — this pack is generated from a single ledger, and Part 3 is a reproducible Monte Carlo
  rather than three hand-picked points. The remainder are code problems, not document problems:

  #v(2pt)
  - Three fiscal engines producing three answers from one input set. None retained.
  - Verification performed by the same model family that wrote the work. Structurally biased.
  - Roughly 200 tools exposed; selection accuracy degrades well before that.
]

#v(2mm)
#heading(level: 2, numbering: none)[Next build sequence]
#text(size: 8.3pt)[
  Ordered by value per unit of effort, and by dependency. Nothing later can be trusted before the
  item above it exists.
]
#v(1pt)
#table(columns: (8mm, 52mm, 1fr),
  table.header([*No.*], [*Step*], [*Why it comes here*]),
  [1], [Obtain the post-conversion specification], [It changes every rate, volume and cost downstream. Nothing in Parts 4–9 can be written before it lands.],
  [2], [Build the single fiscal engine, with regression tests], [Three engines produced three answers. One engine, hand-checked against a spreadsheet, replaces all three.],
  [3], [Independent verifier on a different model family], [The author cannot check the author. This is the only control that catches a wrong-but-plausible number.],
  [4], [Parts 4–7: facilities, subsurface, wells, subsea], [Each needs one primary document that is currently missing. They are parallel once step 1 lands.],
  [5], [Part 8 cost and schedule, then Part 9 economics], [Both consume steps 1 and 2; neither can precede them.],
  [6], [Part 2 executive summary, then Part 12 decision], [Last by construction. Summaries written first become wishes.],
)

#pagebreak()

// ═══════════════════════ APPENDIX G ═══════════════════════
#heading(level: 1, numbering: none)[Appendix G — Figure QA gate]
#text(size: 8.3pt)[
  Every figure is checked by code, not by eye. Each text artist's bounding box is tested against the
  canvas and against every other text box; overlaps above a threshold fail the build. The gate runs
  on the same pass that draws the figures, so a figure cannot ship unchecked.
]

#figure(
  table(columns: (30mm, 22mm, 26mm, 20mm, 1fr),
    table.header([*Figure*], [*Text items*], [*Outside canvas*], [*Overlaps*], [*Note*]),
    [Fig 0 — location], [20], [0], [0], [Graticule, scale bar, north arrow, CRS note],
    [Fig 1 — profiles], [29], [0], [0], [Three ceilings against one resource],
    [Fig 2 — 9.6 yr], [29], [0], [0], [Arithmetic exposed on the figure],
    [Fig 3 — Monte Carlo], [25], [0], [0], [P90/P50/P10 marked],
    [Fig 4 — VRR], [16], [0], [0], [Injection capacity against voidage],
    [Fig 5.1 — tectonics], [9], [0], [0], [Plate framework; schematic outlines disclosed],
    [Fig 5.2 — bathymetry], [5], [0], [0], [Real DEM; depth measured at 994 m],
    [Fig 5.3 — section], [6], [0], [0], [Real DEM transect; 32× exaggeration stated],
    [Fig 5.4 — structure], [10], [0], [0], [Schematic; labelled as such],
    [Fig 5.5 — stratigraphy], [11], [0], [0], [After Bol & van Hoorn 1980; Krebs 2011],
    [Fig 5.6 — seal and wells], [4], [0], [0], [Column capped by seal; per-well volume],
    [Fig 5.7 — thermal], [2], [0], [0], [The unresolved C-10 contradiction],
  ),
  caption: [Table G.1 — Gate output for this build. Twelve figures, 166 text items, zero overflow, zero overlap. Reproducible by rerunning the figure scripts.],
)

#v(3mm)
#heading(level: 2, numbering: none)[What the gate does not check]
#text(size: 8.3pt)[
  It measures geometry, not truth. A figure can pass and still be wrong — a scale bar can be
  miscomputed, an axis mislabelled, a curve can encode a bad assumption. The gate removes one class
  of defect (things that collide or fall off the page) and must not be read as assurance on the
  other class. That class needs an independent verifier, which is a separate build.
]

#v(12mm)
#line(length: 100%, stroke: 0.5pt + rgb("#CCCCCC"))
#v(3mm)
#text(size: 7.4pt, fill: grey)[
  Prepared by HERMES (arifOS), 19 October 2026. Working draft, Parts 1, 3 and 5 of twelve. Independent
  reconstruction from public sources. Not a PCSB or PETRONAS document. No PETRONAS logo, branding or
  document numbering is used or implied. Not attributed to any individual.
]
