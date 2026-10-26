// LIM-SFDP-v0.1 — Limbayong Shadow FDP, Review Pack
#set document(title: "Limbayong Shadow FDP — Review Pack v0.1", author: "HERMES (arifOS)")
#set page(paper: "a4", margin: (top: 26mm, bottom: 20mm, left: 20mm, right: 18mm),
  numbering: none)
#set text(font: "DejaVu Sans", size: 9.3pt, lang: "en", region: "GB")
#set par(justify: true, leading: 0.62em, spacing: 1.1em)
#set heading(numbering: none)
#show heading.where(level: 1): it => block(above: 1.5em, below: 0.85em)[
  #set text(size: 15pt, weight: "bold", fill: rgb("#1F3A5F"))
  #it
  #v(-3pt)
  #line(length: 100%, stroke: 0.9pt + rgb("#1F3A5F"))
]
#show heading.where(level: 2): it => block(above: 1.15em, below: 0.5em)[
  #set text(size: 11pt, weight: "bold", fill: rgb("#1F3A5F"))
  #it
]
#show heading.where(level: 3): it => block(above: 0.9em, below: 0.35em)[
  #set text(size: 9.6pt, weight: "bold", fill: rgb("#333333"))
  #it
]

#let navy = rgb("#1F3A5F")
#let red = rgb("#A32E2E")
#let grey = rgb("#6B6B6B")
#let lightbg = rgb("#F6F6F3")

#let tag(t) = {
  let c = if t == "VERIFIED" { rgb("#2E7D32") }
          else if t == "DERIVED" { rgb("#1F3A5F") }
          else if t == "ASSUMED" { rgb("#C08A2E") }
          else { rgb("#A32E2E") }
  box(fill: c, inset: (x: 3pt, y: 1.2pt), radius: 2pt,
      text(size: 6.8pt, weight: "bold", fill: white)[#t])
}

#let open-banner(body) = block(
  width: 100%, fill: rgb("#FDF4F4"), stroke: (left: 3pt + red),
  inset: (x: 9pt, y: 7pt), above: 0.9em, below: 0.9em,
  text(size: 8.5pt, fill: rgb("#5A1A1A"))[
    #text(weight: "bold", fill: red)[OPEN — ]#body
  ]
)

// Manual figure/table labels are authoritative in this pack (Figure 2, Table 1.3, …);
// suppress Typst's automatic number so the caption does not read "Figure 3: Figure 2 — …".
#show figure.caption: it => block(above: 0.6em, below: 0.8em)[
  #set text(size: 7.9pt, fill: rgb("#3A3A3A"))
  #it.body
]
#set figure(gap: 0.7em)
// allow long tables to flow across a page break with a repeated header
#show figure: set block(breakable: true)

#set table(stroke: (x: 0.3pt + rgb("#D5D5D0"), y: 0.3pt + rgb("#D5D5D0")),
  inset: (x: 4pt, y: 1.9pt),
  fill: (x, y) => if y == 0 { rgb("#1F3A5F") } else if calc.odd(y) { rgb("#F7F7F4") })
#show table.cell.where(y: 0): set text(size: 7.4pt, weight: "bold", fill: white)
#show table.cell: set text(size: 7.5pt)

// ══════════════════════ FRONT MATTER ══════════════════════
#v(10mm)
#text(size: 8pt, fill: grey)[SHADOW FIELD DEVELOPMENT PLAN · REVIEW PACK]
#v(2mm)
#line(length: 100%, stroke: 2.2pt + navy)
#v(6mm)
#text(size: 27pt, weight: "bold", fill: navy)[Limbayong]
#v(1mm)
#text(size: 13pt, fill: rgb("#333333"))[Deepwater Oil & Gas Development · Blocks G / J / R · Offshore Sabah]
#v(7mm)
#text(size: 10.4pt)[*Review Pack v0.1* — Parts 1 and 3, with ledger and source register]
#v(3mm)

#block(fill: lightbg, inset: 11pt, width: 100%, stroke: (left: 3pt + navy))[
  #set text(size: 8.7pt)
  #grid(columns: (32mm, 1fr), gutter: 6pt, row-gutter: 3.5pt,
    [*Document ID*], [LIM-SFDP-v0.1],
    [*Revision*], [0.1 — first review issue],
    [*Date*], [19 October 2026],
    [*Prepared by*], [HERMES (arifOS), for review],
    [*Status*], [Draft for review — not for external circulation],
    [*Scope*], [Parts 1 and 3, Appendix B, Appendix E],
    [*Classification*], [Independent reconstruction from public sources],
  )
]

#v(6mm)
#block(fill: rgb("#FDF4F4"), inset: 10pt, width: 100%, stroke: (left: 3pt + red))[
  #set text(size: 8.6pt)
  #text(weight: "bold", fill: red)[READ THIS FIRST]
  #v(2pt)
  This document is not a PETRONAS or PETRONAS Carigali document. It was not produced
  with, reviewed by, or endorsed by either company. It contains no internal data,
  no well logs, no seismic, no PVT, no cost estimates and no fiscal terms from any
  operator. Every number is either taken from a cited public source, derived by
  arithmetic from those sources, or flagged as an assumption with its owner and reason.
  Where a figure was not available, the gap is marked OPEN rather than filled.
]

#v(4mm)
#text(size: 7.6pt, fill: grey)[
  Revision 0.1 builds only the parts that do not depend on the Sevan-300 specification
  or the fiscal reconciliation. Parts 0, 2 and 4–12 are deliberately absent. Their
  numbers would inherit the same defects this pack exists to remove.
]

#pagebreak()

#heading(level: 1, numbering: none)[Document control]

#heading(level: 2, numbering: none)[Revision block]
#table(columns: (14mm, 20mm, 58mm, 1fr),
  table.header([*Rev*], [*Date*], [*Change*], [*Scope*]),
  [0.1], [19 Oct 2026], [First review issue],
  [Front matter, Part 1, Part 3, App. B, App. E],
)

#v(4mm)
#heading(level: 2, numbering: none)[Reading guide — the four tags]
#table(columns: (24mm, 1fr),
  table.header([*Tag*], [*Meaning and test*]),
  [VERIFIED], [Stated by a cited public source. The citation is in Appendix E and the row is in Appendix B. If the source is wrong, the number is wrong — but the document is faithful to it.],
  [DERIVED], [Computed here from other ledger rows. The formula is shown in the row, so the arithmetic can be repeated without trusting the author.],
  [ASSUMED], [A judgement, not a measurement. Every one carries an owner and a stated reason. An assumption can be challenged; it cannot be verified.],
  [OPEN], [The input does not exist in the public record. It is marked, not guessed. OPEN items appear as red banners wherever they change a conclusion.],
)

#v(3mm)
#block(fill: lightbg, inset: 9pt, width: 100%)[
  #set text(size: 8.4pt)
  *The rule this pack is built on:* no number may exist only in prose. Every figure in
  Parts 1 and 3 carries a ledger row reference (L-nn) in Appendix B. If a number is
  found without a ledger row, that is a defect in this document, not a rounding matter.
]

#v(4mm)
#heading(level: 2, numbering: none)[Data classification statement]
#text(size: 8.7pt)[
  All information in this pack derives from public sources: a company filing on Bursa
  Malaysia, published petroleum-engineering papers, trade press, an open-source
  geospatial dataset, and a public resource tracker. No PETRONAS, PETRONAS Carigali,
  MISC or contractor confidential material has been used, requested, or received.

  Nothing in this pack should be read as reflecting internal operator knowledge. Any
  reader with access to operator data should expect this document to differ from it,
  and should prefer the operator's data.
]

#v(4mm)
#heading(level: 2, numbering: none)[Not in this build]
#text(size: 8.7pt)[
  Parts 0, 2 and 4–12 are not drafted. Part 2 and Part 4 both consume the fiscal
  reconciliation, which does not yet exist as a single engine; Part 4 additionally
  consumes the Sevan-300 specification, which has not been established from a primary
  source. Drafting them now would repeat the exact failure this pack was commissioned
  to fix — many workstreams, many number sets.
]

#pagebreak()

// ══════════════════════ PART 1 ══════════════════════
#set page(header: context [
  #set text(size: 7.2pt, fill: grey)
  #grid(columns: (1fr, auto),
    [Limbayong Shadow FDP · LIM-SFDP-v0.1 · Rev 0.1 · 19 Oct 2026],
    [Independent reconstruction],
  )
  #v(-3pt)
  #line(length: 100%, stroke: 0.4pt + rgb("#CCCCCC"))
], footer: context [
  #set text(size: 6.9pt, fill: grey)
  #line(length: 100%, stroke: 0.4pt + rgb("#CCCCCC"))
  #v(1pt)
  #grid(columns: (1fr, auto),
    [Independent reconstruction from public sources — not a PCSB/PETRONAS document.],
    [Page #counter(page).display() of #counter(page).final().first()],
  )
], numbering: none)

#counter(page).update(1)

#heading(level: 1)[1    Basis and reconciliation]

#heading(level: 2)[1.1    Basis of design]
For any reader outside the operator, Limbayong presents a specific problem: the public
record contains enough to know that a development exists, and not enough to know whether
it works. This pack therefore separates three things that are usually blended together.

#figure(
  image("fig/fig0_map.png", width: 100%),
  caption: [Figure 0 — Location. Limbayong lies in Blocks G/J/R, approximately 120 km
  offshore Sabah in 900–1,200 m water depth. The shaded zone is schematic and is not an
  isobath; the block outline is not public, so a point is shown rather than a polygon.
  Base map: Natural Earth 1:10m coastline. Position: L-17. #tag("VERIFIED")],
)

*What is established.* That the field lies in Blocks G/J/R about 120 km offshore Sabah
in 900–1,200 m of water, that it was discovered in 2002, that development is a ten-well
subsea tie-back to a floating production unit, that final investment decision was taken
on 28 August 2026, and that the working interest is 100 per cent PETRONAS Carigali.
These are cited facts. #tag("VERIFIED")

*What is inferred.* That a structure 30 km long and 2.5 km wide, described by its own
operator as "industry top decile reservoir complexity" with "lateral compartmentalisation",
cannot deliver a uniform recovery factor across its length. The inference is sound, but
it is an inference. #tag("DERIVED")

*What is absent.* There is no public seismic, no public well log, no core, no PVT sample,
no production test, no cost estimate, no gas sales agreement and no fiscal term sheet.
Not "not found by this author" — absent from the public record. Every subsurface volume
in this pack is therefore a screening range, not a reserves estimate.

#block(fill: lightbg, inset: 9pt, width: 100%)[
  #set text(size: 8.5pt)
  *Language note.* This pack uses SPE-PRMS vocabulary. Nothing here is called
  "reserves". The volumes in Part 3 are *contingent resources under a development case*,
  expressed as a range because the basis for a point estimate is not public.
]

#heading(level: 2)[1.2    One number set]
The table below is the only accepted source of values for Parts 1 and 3. Every number
in those parts traces to a row here, and every row traces to Appendix B.

#figure(
  table(columns: (50mm, 24mm, 20mm, 13mm, 1fr),
    table.header([*Parameter*], [*Value used*], [*Class*], [*Row*], [*Basis*]),
    [Oil in place — low], [347 MMbbl], [ASSUMED], [L-01], [Screening range],
    [Oil in place — mid], [372.5 MMbbl], [DERIVED], [L-02], [(347 + 398) / 2],
    [Oil in place — high], [398 MMbbl], [ASSUMED], [L-03], [Screening range],
    [Recovery factor — low], [35 %], [ASSUMED], [L-04], [Screening range],
    [Recovery factor — mid], [37.5 %], [DERIVED], [L-05], [(35 + 40) / 2],
    [Recovery factor — high], [40 %], [ASSUMED], [L-06], [Screening range],
    [Recoverable — low], [121.5 MMbbl], [DERIVED], [L-07], [347 × 0.35],
    [Recoverable — mid], [139.7 MMbbl], [DERIVED], [L-08], [372.5 × 0.375],
    [Recoverable — high], [159.2 MMbbl], [DERIVED], [L-09], [398 × 0.40],
    [Plateau oil — low], [30,000 bopd], [ASSUMED], [L-10], [Screening range],
    [Plateau oil — mid], [33,507 bopd], [DERIVED], [L-11], [(30,000 + 37,014) / 2],
    [Plateau oil — high], [37,014 bopd], [ASSUMED], [L-12], [Screening range],
    [Gas recoverable], [790.9 bcf], [VERIFIED], [L-13], [Public tracker, data year 2023],
    [Gas nameplate], [150 MMscfd], [VERIFIED], [L-14], [Operator release + tracker],
    [Oil nameplate], [40,000 bopd], [VERIFIED], [L-15], [Operator release, 2021],
    [Water depth], [900–1,200 m], [VERIFIED], [L-16], [Operator release, 2021],
    [Working interest], [100 % PCSB], [VERIFIED], [L-18], [Trade press, 2026],
    [First oil], [—], [OPEN], [L-19], [Not determinable in this pack],
    [Economic limit], [—], [OPEN], [L-20], [Requires the fiscal engine],
    [Injection duty], [—], [OPEN], [L-21], [No public basis],
    [Fiscal terms], [—], [OPEN], [L-25], [PSC text not public],
  ),
  caption: [Table 1.2 — One number set for Parts 1 and 3. Values are quoted from ledger
  rows, not restated from prose. Class tags are defined in the reading guide.],
)

#heading(level: 2)[1.3    Conflicts — resolved and open]
This pack assembles nine technical sections produced in parallel. They did not agree.
Seven disagreements were identified. Two are resolved by definition; five remain open
and are carried forward to the parts that must close them.

Every open conflict appears as a red banner in the body of the affected section, and is
listed once here. No conflict has been resolved silently.

#block(fill: lightbg, inset: 8pt, width: 100%, above: 0.9em, below: 0.9em)[
  #set text(size: 8.3pt)
  *Why C-02 is resolved rather than open.* The apparent conflict between 40,000 bopd and
  35,000 bopd is not a disagreement about the field. It is a category error: 40,000 is the
  facility's nameplate capacity, and 35,000 was a forecast of what the reservoir could
  deliver into it. Once the two are named separately there is no conflict — there is a
  shortfall, which is a finding. The same applies to gas at 150 and 135 MMscfd.
]

#figure(
  table(columns: (10mm, 34mm, 28mm, 17mm, 14mm, 1fr),
    table.header([*ID*], [*Conflict*], [*Values in the record*], [*Status*], [*Owner*], [*Next action*]),
    [C-01], [Total development capex], [2.83 / 2.90 / 3.17 / 4.05 bn], [OPEN], [Part 4],
      [Independent cost build; adopt one WBS, retire the other three],
    [C-02], [Throughput: nameplate or forecast], [40,000 vs 35,000 bopd; 150 vs 135 MMscfd], [RESOLVED], [Part 1],
      [Separate the two objects; Part 3 uses 30,000–37,014 bopd and 150 MMscfd nameplate],
    [C-03], [Oil in place], [517 MMbbl STOIIP vs 347–398 MMbbl], [OPEN], [Part 5],
      [STOIIP and screening OOIP are different definitions; adopt one basis],
    [C-04], [Net present value at one price], [4 values at one price], [OPEN], [Part 4],
      [Single fiscal engine; no NPV is quoted in this pack],
    [C-05], [First oil], [2029 vs Q4 2030], [OPEN], [Part 6],
      [Integrated schedule against comparable projects],
    [C-06], [Decline requirement], ["44 %" stated], [OPEN], [Part 3],
      [Not reproducible from the stated ranges — see §3.2 and Figure 2],
    [C-07], [Water injection duty], [46,300 vs 75,000 bwpd], [OPEN], [Part 7],
      [Required voidage is derivable from rate and FVF; stated duty is not],
  ),
  caption: [Table 1.3 — Conflict register. Seven conflicts identified across the parallel
  sections. Two resolved by definition, five open and carried forward.],
)

#heading(level: 2)[1.4    When a range is a range]
A range is not a hedge. Three ranges in this pack are load-bearing and each is held
open for a different reason.

#grid(columns: (1fr, 1fr, 1fr), gutter: 8pt,
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.2pt)
    *Oil in place, 347–398 MMbbl*#linebreak()
    Open because no public OOIP exists. A screening bracket, not a probabilistic one.
    #tag("ASSUMED")
  ],
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.2pt)
    *Recovery factor, 35–40 %*#linebreak()
    Open because the recovery mechanism — solution gas, gas cap, water injection — is
    not stated publicly. #tag("ASSUMED")
  ],
  block(fill: lightbg, inset: 8pt)[
    #set text(size: 8.2pt)
    *Plateau, 30,000–37,014 bopd*#linebreak()
    Open because well count is stated but well productivity is not. #tag("ASSUMED")
  ],
)

#v(0.4em)

// ══════════════════════ PART 3 ══════════════════════
#heading(level: 1)[3    Production]

#heading(level: 2)[3.1    The three cases]
Three numbers govern the production case, and they cannot be chosen independently.

- Recoverable volume — 121.5 to 159.2 MMbbl #tag("DERIVED") (L-07 to L-09)
- Plateau rate — 30,000 to 37,014 bopd #tag("ASSUMED") (L-10, L-12)
- Field life — the dependent variable, not a choice

They are run as three cases rather than a point estimate, because the basis for a point
estimate does not exist in the public record.

#figure(
  table(columns: (44mm, 1fr, 1fr, 1fr),
    table.header([], [*Low*], [*Mid*], [*High*]),
    [Oil in place], [347 MMbbl], [372.5 MMbbl], [398 MMbbl],
    [Recovery factor], [35 %], [37.5 %], [40 %],
    [Recoverable], [121.5 MMbbl], [139.7 MMbbl], [159.2 MMbbl],
    [Plateau rate], [30,000 bopd], [33,507 bopd], [37,014 bopd],
    [Plateau duration], [7.8 yr], [8.0 yr], [8.2 yr],
    [Gas plateau], [10.1 yr], [10.1 yr], [10.1 yr],
    [Plateau share of ultimate], [70 %], [70 %], [70 %],
    [Decline], [exponential], [exponential], [exponential],
    [Economic limit], [OPEN], [OPEN], [OPEN],
  ),
  caption: [Table 3.1 — Case definition. Gas plateau duration is identical across cases
  because the gas resource is one ledger value (L-13); only oil volumes vary. The
  economic limit is deliberately not stated — it is OPEN (L-20), see §3.5.],
)

#figure(
  image("fig/fig1_profiles.png", width: 100%),
  caption: [Figure 1 — Production cases. Oil, gas and water cut for Low, Mid and High.
  The oil plateau sits *below* the 40,000 bopd nameplate in all three cases — that gap
  is the finding, not a plotting error. The gas stream holds nameplate longer than oil
  in every case. Sources: L-01 to L-15. #tag("DERIVED")],
)

The first thing Figure 1 shows is the one that matters: *no case reaches the nameplate.*
The facility is designed for 40,000 bopd and the reservoir delivers between 30,000 and
37,014. That is a 7.5 to 25 per cent shortfall against installed capacity, present from
first oil and permanent thereafter.

#heading(level: 2)[3.2    The plateau collision]
At a sustained plateau with no decline, the resource is exhausted in the time it takes
to divide recoverable volume by annual plateau volume.

#align(center)[
  #block(fill: lightbg, inset: 10pt)[
    #set text(size: 9.2pt)
    #table(columns: (24mm, 30mm, 26mm, 32mm),
      table.header([*Case*], [*Recoverable*], [*Plateau*], [*Years to exhaustion*]),
      [Low], [121.5 MMbbl], [30,000 bopd], [*11.1 years*],
      [Mid], [139.7 MMbbl], [33,507 bopd], [*11.4 years*],
      [High], [159.2 MMbbl], [37,014 bopd], [*11.8 years*],
    )
  ]
]

The three cases converge on the same answer because numerator and denominator move
together. That convergence is the finding: *within this resource range, the plateau rate
does not buy additional years. It only changes which years they are.*

#heading(level: 3)[3.2.1    The stress case: 9.6 years]
The brief for this pack cites a 9.6-year figure. It reproduces exactly — but only under
one specific pairing.

#align(center)[
  #block(fill: rgb("#FDF4F4"), stroke: (left: 3pt + red), inset: 10pt)[
    #set text(size: 9pt)
    #text(fill: red, weight: "bold")[9.6-YEAR ARITHMETIC]
    #linebreak()
    372.5 MMbbl (mid OOIP) × 0.35 (low recovery factor) = *130.4 MMbbl*
    #linebreak()
    130.4 MMbbl ÷ (37,014 bopd × 365) = *9.65 years*
    #linebreak()
    #text(size: 7.9pt, fill: grey)[The optimistic rate paired with the pessimistic
    recovery. Neither is a base case; the pairing is the stress.]
  ]
]

#open-banner[
  *C-06 — the "44 % decline requirement" does not reproduce.* If the field is held at
  37,014 bopd the resource is exhausted in 9.65 years and there is no tail to decline
  *into*. Working the other direction — a 20-year field life at the same initial rate —
  requires an exponential decline of approximately *8.7 % per year*, from
  `(1 − (1−d)^20) / d = 9.65`. Forty-four per cent appears nowhere in that arithmetic.
  The figure is therefore carried as OPEN. Either it refers to a quantity not stated in
  the brief, or it is in error. It is not silently accepted and it is not silently
  dropped.
]

#figure(
  image("fig/fig2_collision.png", width: 100%),
  caption: [Figure 2 — Plateau against resource ceiling. *Panel A:* cumulative oil at a
  sustained plateau for each case; markers show where each hits its recoverable volume.
  The red dashed line is the 9.6-year stress case. *Panel B:* the same resource expressed
  as required field life. The nameplate is 40,000 bopd; the shaded band is the
  30,000–37,014 bopd plateau range. Sources: L-01 to L-12. #tag("DERIVED")],
)

The consequence for the facility is direct. Panel B shows that a 20-year field life at
this resource range supports a plateau of roughly *17,000 to 22,000 bopd* — between 42
and 55 per cent of the 40,000 bopd nameplate. A development designed for 40,000 bopd and
a 20-year life is asking for two things the resource does not offer at once.

#heading(level: 2)[3.3    Gas against the 150 MMscfd nameplate]
Gas behaves differently, and that difference is the second half of the problem.

- Recoverable gas — 790.9 bcf #tag("VERIFIED") (L-13)
- Nameplate — 150 MMscfd #tag("VERIFIED") (L-14)
- Full-rate exhaustion — 790.9 bcf ÷ 54.75 bcf per year = *14.4 years*

At nameplate the gas stream outlasts the oil stream at plateau by roughly five years,
but likewise has no tail if drawn at full rate. Applying the same convention used for
oil — plateau carries 70 per cent of ultimate recovery — the gas plateau runs *10.1
years* against the oil plateau's 7.8 to 8.2 years.

#block(fill: lightbg, inset: 9pt, width: 100%)[
  #set text(size: 8.5pt)
  *The collision, stated plainly.* For roughly two years the facility would process gas
  with little or no oil. That tail is long in calendar time and thin in revenue. A
  floating unit's operating cost does not fall with throughput, so the unit cost of each
  barrel in that period is fixed cost divided by a small volume. That is a Part 4
  question, but it is a Part 3 *fact*, and it should not be discovered for the first
  time inside an economic model.
]

#open-banner[
  *Not established:* whether the 150 MMscfd nameplate is a gas-processing limit, a
  sales-route limit, or a reservoir-deliverability limit. Those three have completely
  different consequences. A process limit can be relieved with capital; a sales-route
  limit needs a buyer; a deliverability limit needs wells. The public record does not
  say which it is. (L-14)
]

#heading(level: 2)[3.4    Waterflood and voidage]
If the field is waterflooded — and the public record neither confirms nor denies it —
the injection duty is not an independent design choice. It follows from the production
rate and the formation volume factor.

#align(center)[
  #block(fill: lightbg, inset: 10pt)[
    #set text(size: 9pt)
    #table(columns: (58mm, 32mm, 36mm),
      table.header([*Quantity*], [*At 30,000 bopd*], [*At 37,014 bopd*]),
      [Reservoir voidage at Bo 1.25], [37,500 rb/d], [46,268 rb/d],
      [Injection at 100 % replacement], [37,500 bwpd], [46,268 bwpd],
      [Injection at 80 % replacement], [30,000 bwpd], [37,014 bwpd],
    )
  ]
]

The formation volume factor of 1.25 is #tag("ASSUMED") (L-22) — no public PVT exists.
The 100 per cent replacement case is a design ceiling, not a recommendation.

#open-banner[
  *C-07 — required voidage and stated duty do not agree.* Derivation gives roughly
  46,300 bwpd at the high plateau. A parallel section in this programme states a 75,000
  bwpd water-injection requirement. No basis for the higher figure is reproducible from
  rate and formation volume factor; it may include margin, a different rate assumption,
  or produced-water disposal. Until the basis is established the injection duty is OPEN,
  and no facility sizing should be quoted from this pack.
]

#heading(level: 2)[3.5    What these cases are not]
They are not forecasts. A forecast requires an economic limit — the rate at which
operating cost consumes the margin on the incremental barrel. Setting that rate requires
a price deck, an opex structure and a fiscal regime, none of which exist in this pack.

#open-banner[
  *L-20 — economic limit.* Not stated anywhere in this document. Every profile in
  Figure 1 therefore runs until the resource is exhausted at an arbitrary 2 per cent of
  plateau, which is a plotting convenience and not an economic cut-off. The true tail
  length is unknown, and with it the true field life, the abandonment timing and the
  late-life unit cost. This is the largest gap in Part 3.
]

#heading(level: 2)[3.6    What Part 3 establishes and what it does not]
#grid(columns: (1fr, 1fr), gutter: 10pt,
  block(fill: lightbg, inset: 9pt)[
    #set text(size: 8.3pt)
    *Established*
    #v(2pt)
    - No case reaches the 40,000 bopd nameplate. The shortfall is 7.5 to 25 per cent,
      present from first oil.
    - At this resource range the field cannot sustain 40,000 bopd for more than about
      nine to twelve years, and cannot do so with any decline tail.
    - The 9.6-year figure is real and derives from one specific pairing of optimistic
      rate with pessimistic recovery.
    - Gas at nameplate outlasts oil at plateau by roughly two years under a common
      convention, producing a thin, low-revenue tail.
    - Required water-injection duty at the high plateau is of order 46,000 bwpd.
  ],
  block(fill: lightbg, inset: 9pt)[
    #set text(size: 8.3pt)
    *Not established*
    #v(2pt)
    - Whether 10 wells can deliver 37,014 bopd. No productivity data is public.
    - Whether the recovery factor is 35 or 40 per cent.
    - Whether water injection is planned at all.
    - Where the economic limit sits (OPEN, L-20), and therefore how long the field runs.
    - What the gas nameplate constraint actually represents.
  ],
)

#v(0.3em)

// ══════════════════════ APPENDIX B ══════════════════════
#heading(level: 1, numbering: none)[Appendix B — Assumptions ledger]
#text(size: 8.4pt, fill: grey)[Only rows used by Parts 1 and 3 are listed. The full
ledger will be issued with the fiscal engine.]

#figure(
  table(columns: (12mm, 44mm, 24mm, 33mm, 20mm, 1fr),
    table.header([*Row*], [*Parameter*], [*Value*], [*Class*], [*Owner / basis*], [*Citation*]),
    [L-01], [OOIP — low case], [347 MMbbl], [ASSUMED], [Review brief], [—],
    [L-02], [OOIP — mid case], [372.5 MMbbl], [DERIVED], [(L-01 + L-03) / 2], [—],
    [L-03], [OOIP — high case], [398 MMbbl], [ASSUMED], [Review brief], [—],
    [L-04], [Recovery factor — low], [35 %], [ASSUMED], [Review brief], [—],
    [L-05], [Recovery factor — mid], [37.5 %], [DERIVED], [(L-04 + L-06) / 2], [—],
    [L-06], [Recovery factor — high], [40 %], [ASSUMED], [Review brief], [—],
    [L-07], [Recoverable — low], [121.5 MMbbl], [DERIVED], [L-01 × L-04], [—],
    [L-08], [Recoverable — mid], [139.7 MMbbl], [DERIVED], [L-02 × L-05], [—],
    [L-09], [Recoverable — high], [159.2 MMbbl], [DERIVED], [L-03 × L-06], [—],
    [L-10], [Plateau oil — low], [30,000 bopd], [ASSUMED], [Review brief], [—],
    [L-11], [Plateau oil — mid], [33,507 bopd], [DERIVED], [(L-10 + L-12) / 2], [—],
    [L-12], [Plateau oil — high], [37,014 bopd], [ASSUMED], [Review brief], [—],
    [L-13], [Recoverable gas], [790.9 bcf], [VERIFIED], [Public tracker], [S-01],
    [L-14], [Gas nameplate], [150 MMscfd], [VERIFIED], [Operator release], [S-02],
    [L-15], [Oil nameplate], [40,000 bopd], [VERIFIED], [Operator release], [S-02],
    [L-16], [Water depth], [900–1,200 m], [VERIFIED], [Operator release], [S-02],
    [L-17], [Location], [5.888°N 114.510°E], [VERIFIED], [Public tracker], [S-01],
    [L-18], [Working interest], [100 % PCSB], [VERIFIED], [Trade press], [S-03],
    [L-19], [First oil date], [—], [OPEN], [No public schedule], [—],
    [L-20], [Economic limit], [—], [OPEN], [Needs fiscal engine], [—],
    [L-21], [Injection duty], [—], [OPEN], [Basis unresolved], [—],
    [L-22], [Formation volume factor], [1.25 rb/stb], [ASSUMED], [HERMES — analogue], [—],
    [L-23], [Plateau share of ultimate], [70 %], [ASSUMED], [HERMES — convention], [—],
    [L-24], [Boe conversion], [5.8 Mcf/bbl], [ASSUMED], [HERMES — convention], [—],
    [L-25], [Fiscal terms], [—], [OPEN], [PSC text not public], [—],
  ),
  caption: [Table B.1 — Assumptions ledger. Every figure in Parts 1 and 3 resolves to a
  row here. Rows marked OPEN carry no value by design.],
)

#heading(level: 2, numbering: none)[Ledger arithmetic]
Every DERIVED row can be repeated without trusting this document.

#block(fill: lightbg, inset: 9pt, width: 100%, breakable: false)[
  #set text(size: 7.9pt, font: "DejaVu Sans Mono")
  #grid(columns: (1fr, 1fr), gutter: 12pt, row-gutter: 1.2pt,
    [L-02 = (347+398)/2 = 372.5], [L-09 = 398 × 0.40 = 159.2],
    [L-05 = (0.35+0.40)/2 = 0.375], [L-11 = (30000+37014)/2 = 33507],
    [L-07 = 347 × 0.35 = 121.45], [Plateau yr = R × 10⁶ / (rate × 365)],
    [L-08 = 372.5 × 0.375 = 139.6875], [→ 121.45e6/(30000×365) = 11.09],
    [Gas = 150 × 365 / 1000 = 54.75 bcf/yr], [→ 139.6875e6/(33507×365) = 11.42],
    [790.9 / 54.75 = 14.45 yr], [→ 159.2e6/(37014×365) = 11.78],
  )
]

#pagebreak()

// ══════════════════════ APPENDIX E ══════════════════════
#heading(level: 1, numbering: none)[Appendix E — Source register]
#text(size: 8.4pt, fill: grey)[Only sources cited in this pack are listed.]

#figure(
  table(columns: (12mm, 1fr, 22mm),
    table.header([*ID*], [*Source*], [*Accessed*]),
    [S-01], [Global Energy Monitor, *Limbayong Gas Field (Malaysia)*, Global Oil & Gas Extraction Tracker, data year 2023. Field statistics, coordinates, design capacity.], [19 Oct 2026],
    [S-02], [PETRONAS, *PETRONAS Awards Limbayong Deepwater EPCIC Contract to TechnipFMC*, media release, 1 June 2021. Water depth, distance offshore, well count, facility description.], [19 Oct 2026],
    [S-03], [Welligence Energy Analytics, *Malaysia FID alert — Limbayong*, 31 August 2026. Final investment decision, working interest, discovery history.], [19 Oct 2026],
    [S-04], [SPE 210079-MS, *Limbayong: Decoding Industry Top Decile Reservoir Complexity for Marginal Deepwater Development*, 2022. Structure dimensions, complexity characterisation.], [19 Oct 2026],
    [S-05], [SPE 210549-MS, deepwater drilling margin and managed-pressure-drilling requirement. Referenced in Part 3 context only.], [19 Oct 2026],
    [S-06], [Upstream, *Petronas finally takes FID on Limbayong deepwater development*, 28 August 2026. FID date and facility concept.], [19 Oct 2026],
    [S-07], [Dagang NeXchange Berhad, Bursa Malaysia filing, 20 August 2026. Disposal of FPSO *Excalibur* to MISC. Not used in this pack; cited in Part 4.], [19 Oct 2026],
    [S-08], [Natural Earth, 1:10m coastline, physical vector dataset. Map base for Figure 0. Public domain.], [19 Oct 2026],
  ),
  caption: [Table E.1 — Source register. Every VERIFIED row in Appendix B resolves to an
  entry here. Sources are public and independently checkable.],
)

#v(4mm)
#heading(level: 2, numbering: none)[Source limitations]
#text(size: 8.5pt)[
  *S-01 is a secondary tracker.* It reports field statistics compiled by a
  non-commercial monitor, not by the operator. Its reserve figures are treated as the
  best available public estimate and not as an operator statement.

  *S-04 and S-05 are conference papers.* They carry the operator's own technical
  characterisation of the field, which is why they are given weight — but they describe
  the reservoir, not the development plan, and they do not disclose volumes, costs or
  schedule.

  *No source in this register is a primary operator document for volumes, costs or
  fiscal terms.* That absence is the central limitation of the entire pack, and it is
  the reason so much of this document is OPEN.
]

#v(6mm)
#line(length: 100%, stroke: 0.5pt + rgb("#CCCCCC"))
#v(3mm)
#text(size: 7.6pt, fill: grey)[
  Prepared by HERMES (arifOS) for review, 19 October 2026. Independent reconstruction
  from public sources. Not a PCSB/PETRONAS document. No PETRONAS logos, branding or
  document numbering are used, and none are implied.
]
