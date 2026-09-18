#!/usr/bin/env python3
"""Build the POLIX & CIVX capability brief (light background, A4 portrait) from seed JSON."""
import html
import json

SEEDS = "/root/.hermes/workspace/polix-civx-seeds.json"
HTML_OUT = "/root/.hermes/workspace/polix-civx-brief.html"

d = json.load(open(SEEDS))
polix = d["polix_malaysia_fiscal"]
pglc = d["polix_petronas_glc"]
civx = d["civx_malaysia_2027_2040"]


def e(x):
    return html.escape(str(x))


def risk_class(v):
    v = (v or "").upper()
    if v == "HIGH":
        return "r-hi"
    if v == "MODERATE":
        return "r-md"
    if v == "LOW":
        return "r-lo"
    return ""


def score_class(s):
    if s >= 0.7:
        return "s-hi"
    if s >= 0.45:
        return "s-md"
    return "s-lo"


L_AXES = [
    ("L0", "Physical", "GEOX", "Live", "ok"),
    ("L1", "Economic", "WEALTH", "Live", "ok"),
    ("L2", "Market signals", "WEALTH", "Live + signal typing", "ok"),
    ("L3", "Institutional", "WEALTH", "Live", "ok"),
    ("L4", "Power topology", "WEALTH", "POLIX seed", "new"),
    ("L5", "Social / cultural", "—", "Vacant", "gap"),
    ("L6", "Behavioural", "WELL", "Live", "ok"),
    ("L7", "Information / entropy", "WEALTH", "Live + four-truth receipts", "ok"),
    ("L8", "Consequence topology", "WEALTH", "Partial", "part"),
    ("L9", "Constitutional", "arifOS", "Live", "ok"),
    ("L10", "Civilizational", "WEALTH", "CIVX seed", "new"),
]

STATUS_LABEL = {"ok": "●  Live", "new": "◆  New", "part": "◐  Partial", "gap": "○  Vacant"}
STATUS_CLASS = {"ok": "st-ok", "new": "st-new", "part": "st-part", "gap": "st-gap"}

parts = []
A = parts.append

A("""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>POLIX &amp; CIVX — WEALTH Capability Brief</title>
<style>
@page {
  size: A4 portrait;
  margin: 15mm 13mm 16mm 13mm;
  @bottom-left {
    content: "WEALTH · POLIX & CIVX capability brief · 2026-09-18";
    font-family: "DejaVu Sans"; font-size: 7pt; color: #8A98A5;
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-family: "DejaVu Sans"; font-size: 7pt; color: #8A98A5;
  }
}
* { box-sizing: border-box; }
body { font-family: "DejaVu Sans", sans-serif; font-size: 8.8pt; line-height: 1.45;
       color: #14202B; margin: 0; }
h1, h2, h3, h4 { margin: 0; font-weight: bold; }
p { margin: 0 0 6pt 0; }
.small { font-size: 7.8pt; color: #5B6B7A; }

/* ---------- cover ---------- */
.cover { border-top: 4pt solid #0F5C6B; padding-top: 10pt; margin-bottom: 12pt; }
.eyebrow { font-size: 7.6pt; letter-spacing: 1.6pt; text-transform: uppercase;
           color: #0F5C6B; font-weight: bold; margin-bottom: 6pt; }
h1 { font-size: 30pt; line-height: 1.03; letter-spacing: -0.6pt; color: #0B1B24; }
.sub { font-size: 11pt; color: #3C4C5A; margin-top: 7pt; line-height: 1.35; }
.metagrid { display: table; width: 100%; margin-top: 13pt; border-top: 0.8pt solid #D9E1E8;
            border-bottom: 0.8pt solid #D9E1E8; padding: 7pt 0; }
.metagrid .row { display: table-row; }
.metagrid .cell { display: table-cell; width: 50%; padding: 2.4pt 10pt 2.4pt 0; vertical-align: top; }
.mlabel { font-size: 7pt; letter-spacing: 0.9pt; text-transform: uppercase; color: #8A98A5; display: block; }
.mvalue { font-size: 8.8pt; color: #14202B; }
.badge { display: inline-block; font-size: 7.4pt; font-weight: bold; letter-spacing: 0.5pt;
         padding: 2pt 6pt; border-radius: 2pt; background: #FDF3DC; color: #8A5A00;
         border: 0.6pt solid #E8C97A; }

/* ---------- sections ---------- */
h2 { font-size: 12.5pt; color: #0B1B24; margin: 15pt 0 6pt 0; padding-bottom: 3pt;
     border-bottom: 1.4pt solid #0F5C6B; }
h2 .num { color: #0F5C6B; margin-right: 6pt; }
h3 { font-size: 10pt; color: #0F5C6B; margin: 11pt 0 4pt 0; }
h4 { font-size: 8.8pt; color: #14202B; margin: 8pt 0 3pt 0; }
.lede { font-size: 9.4pt; color: #33424F; margin-bottom: 8pt; }
ul { margin: 3pt 0 6pt 0; padding-left: 12pt; }
li { margin-bottom: 2.4pt; }

/* ---------- tables ---------- */
table { width: 100%; border-collapse: collapse; margin: 4pt 0 8pt 0; font-size: 7.9pt; }
th { background: #0F5C6B; color: #FFFFFF; text-align: left; font-size: 7.2pt;
     letter-spacing: 0.45pt; text-transform: uppercase; padding: 4pt 5pt; font-weight: bold; }
td { padding: 4pt 5pt; border-bottom: 0.6pt solid #E3E9EE; vertical-align: top; }
tr:nth-child(even) td { background: #F6F9FA; }
td.k { font-weight: bold; color: #0B1B24; }
caption { caption-side: top; text-align: left; font-size: 7.2pt; color: #8A98A5;
          padding-bottom: 2.5pt; letter-spacing: 0.4pt; text-transform: uppercase; }

/* ---------- chips ---------- */
.pill { display: inline-block; font-size: 6.9pt; font-weight: bold; padding: 1pt 4.5pt;
        border-radius: 2pt; letter-spacing: 0.3pt; }
.r-hi { background: #FBE7E7; color: #A32020; }
.r-md { background: #FDF3DC; color: #8A5A00; }
.r-lo { background: #E4F5EA; color: #1E7A46; }
.st-ok { color: #1E7A46; font-weight: bold; }
.st-new { color: #0F5C6B; font-weight: bold; }
.st-part { color: #8A5A00; font-weight: bold; }
.st-gap { color: #A32020; font-weight: bold; }

/* ---------- path cards ---------- */
.pcard { border: 0.7pt solid #D9E1E8; border-left: 3pt solid #0F5C6B; padding: 7pt 9pt 6pt 9pt;
         margin-bottom: 7pt; background: #FBFDFE; }
.pcard.warn { border-left-color: #B26B00; }
.pcard.bad { border-left-color: #A32020; }
.pcard h4 { margin: 0 0 3pt 0; font-size: 9.6pt; }
.pcard .pid { font-family: "DejaVu Sans Mono", monospace; font-size: 7pt; color: #8A98A5;
              letter-spacing: 0.4pt; }
.pcard .assum { font-size: 7.7pt; color: #3C4C5A; margin: 3pt 0; }

/* ---------- resilience matrix ---------- */
table.matrix td.sc { text-align: center; font-weight: bold; width: 14%; }
table.matrix th { text-align: center; }
table.matrix th.ax, table.matrix td.ax { text-align: left; }
.s-hi { background: #E4F5EA !important; color: #14663A; }
.s-md { background: #FDF3DC !important; color: #8A5A00; }
.s-lo { background: #FBE7E7 !important; color: #A32020; }

/* ---------- callouts ---------- */
.note { background: #F4F7F9; border-left: 3pt solid #0F5C6B; padding: 6pt 8pt; margin: 7pt 0;
        font-size: 8.1pt; color: #33424F; }
.note b { color: #0B1B24; }
.warnbox { background: #FDF3DC; border-left: 3pt solid #B26B00; padding: 6pt 8pt; margin: 7pt 0;
           font-size: 8.1pt; color: #5C4200; }
.two { display: table; width: 100%; }
.two > div { display: table-cell; width: 50%; vertical-align: top; padding-right: 9pt; }
.avoid { page-break-inside: avoid; }
.pb { page-break-before: always; }
</style></head><body>""")

# ── Cover ────────────────────────────────────────────────────────────────
A(f"""
<div class="cover">
  <div class="eyebrow">WEALTH Organ · arifOS Federation · Knowledge Axis L4 &amp; L10</div>
  <h1>POLIX &amp; CIVX</h1>
  <div class="sub">Power topology and civilizational horizon for the Malaysian fiscal regime —
  who holds power, who captures the rent, who pays, and what becomes irreversible between
  2027 and 2040.</div>
  <div class="metagrid">
    <div class="row">
      <div class="cell"><span class="mlabel">Domain</span><span class="mvalue">{e(polix['domain'])}</span></div>
      <div class="cell"><span class="mlabel">Horizon</span><span class="mvalue">14 years — 2027 to 2040</span></div>
    </div>
    <div class="row">
      <div class="cell"><span class="mlabel">Schemas</span><span class="mvalue">POLIX-v1.0.0 &nbsp;·&nbsp; CIVX-v1.0.0</span></div>
      <div class="cell"><span class="mlabel">Tools</span><span class="mvalue">capital_polix &nbsp;·&nbsp; capital_civx</span></div>
    </div>
    <div class="row">
      <div class="cell"><span class="mlabel">Evidence basis</span><span class="mvalue">Public sources only · no insider knowledge</span></div>
      <div class="cell"><span class="mlabel">Epistemic tag</span><span class="mvalue">INTERPRETED · DYNAMIC, not observed</span></div>
    </div>
    <div class="row">
      <div class="cell"><span class="mlabel">Governance status</span>
        <span class="mvalue"><span class="badge">SAFE_TO_STUDY — NOT DECISION AUTHORITY</span></span></div>
      <div class="cell"><span class="mlabel">Produced</span><span class="mvalue">18 September 2026 · WEALTH / POLIX · CIVX</span></div>
    </div>
  </div>
</div>""")

# ── 1. The void ──────────────────────────────────────────────────────────
rows = "".join(
    f'<tr><td class="k">{a}</td><td>{b}</td><td>{c}</td>'
    f'<td class="{"warn" if d2 == "gap" else ""}">{e(d2)}</td>'
    f'<td class="{STATUS_CLASS[s]}">{STATUS_LABEL[s]}</td></tr>'
    for a, b, c, d2, s in L_AXES)

A(f"""
<h2><span class="num">1</span>The void this fills</h2>
<p class="lede">Before POLIX and CIVX, WEALTH could do the arithmetic of capital — NPV, IRR,
entry plans, entropy — but had no political economy, no distribution of consequence, and no
horizon long enough to see what cannot be undone. A number that is correct and unplaced is
still a blind spot.</p>
<p>The gap was structural, not cosmetic. Four questions could not be answered at all:</p>
<ul>
  <li><b>Who captured the regulator?</b> — POLIX now maps incentive, opacity and capture risk
      per institution.</li>
  <li><b>Who benefits, and who pays?</b> — POLIX now traces rent flows from source to
      beneficiary to cost-bearer.</li>
  <li><b>What becomes irreversible in fourteen years?</b> — CIVX now names the lock-ins
      per path.</li>
  <li><b>How resilient is the system under different oil and reform paths?</b> — CIVX now
      scores six resilience axes across three explicit paths.</li>
</ul>
<table>
  <caption>Knowledge axis coverage after this build</caption>
  <tr><th>Axis</th><th>Domain</th><th>Owner</th><th>Status</th><th>Availability</th></tr>
  {rows}
</table>
<p class="small">Two axes remain open. <b>L5 — social and cultural</b> is vacant. <b>L8 —
consequence topology</b> is partial. Both are the next voids.</p>""")

# ── 2. POLIX ─────────────────────────────────────────────────────────────
actor_rows = "".join(
    f'<tr><td class="k">{e(a["name"])}</td><td>{e(a["actor_type"])}</td>'
    f'<td style="text-align:center">{a["opacity_score"]:.1f}</td>'
    f'<td><span class="pill {risk_class(a["capture_risk"])}">{e(a["capture_risk"])}</span></td>'
    f'<td>{e(a["notes"])}</td></tr>'
    for a in polix["actors"])

rent_rows = "".join(
    f'<tr><td class="k">{e(r["rent_type"].replace("_", " ").title())}</td>'
    f'<td>{e(r["source"])}</td><td>{e(r["beneficiary"])}</td><td>{e(r["cost_bearer"])}</td>'
    f'<td>{e(r["estimated_annual_value"])}</td><td>{e(r["reversibility"].split(" — ")[0])}</td></tr>'
    for r in polix["rent_flows"])

asym_rows = "".join(
    f'<tr><td>{e(a["description"])}</td><td>{e(a["who_benefits"])}</td>'
    f'<td>{e(a["who_bears_cost"])}</td><td><span class="pill r-md">{e(a["reform_difficulty"])}</span></td>'
    f'<td>{e(a["notes"])}</td></tr>'
    for a in polix["rule_asymmetries"])

coercion = "".join(f"<li>{e(c)}</li>" for c in polix["coercion_signals"])
geo = "".join(f"<li>{e(g)}</li>" for g in polix["geopolitical_exposure"])

A(f"""
<div class="pb"></div>
<h2><span class="num">2</span>POLIX — power topology of the Malaysian fiscal regime</h2>
<p class="lede">Scope: federal petroleum revenue, taxation, subsidies, GLC governance and
federal–state fiscal relations. Six actors, four rent flows, three rule asymmetries.</p>

<div class="note"><b>Capture score: {e(polix["capture_score"])}.</b> Not uniform. State governments
carry the highest capture risk (opacity 0.7); Bank Negara Malaysia the lowest (0.3) — operational
independence holds even though the Governor is politically appointed. The concentration that
matters most is not in a regulator but at the centre: the Prime Minister also holds the Finance
portfolio.</div>

<h3>2.1 Actors: mandate, opacity, capture risk</h3>
<table>
  <caption>Opacity 0–1: how much of the decision process is publicly legible</caption>
  <tr><th>Actor</th><th>Type</th><th>Opacity</th><th>Capture</th><th>Structural note</th></tr>
  {actor_rows}
</table>

<h3>2.2 Rent flows: source, beneficiary, cost-bearer</h3>
<table>
  <caption>Where value is extracted, who receives it, and who absorbs the cost</caption>
  <tr><th>Rent type</th><th>Source</th><th>Beneficiary</th><th>Cost bearer</th>
      <th>Est. annual</th><th>Reversibility</th></tr>
  {rent_rows}
</table>
<p class="small">The resource rent is the one that compounds. States bear extraction costs and
receive a fixed fraction — the rule is capped at 5%, and it takes an Act of Parliament
(Petroleum Development Act 1974) to move it.</p>

<h3>2.3 Rule asymmetries</h3>
<table>
  <caption>Rules that distribute advantage without distributing accountability</caption>
  <tr><th>Asymmetry</th><th>Who benefits</th><th>Who carries the cost</th>
      <th>Reform difficulty</th><th>Note</th></tr>
  {asym_rows}
</table>

<div class="two avoid">
  <div>
    <h4>Coercion signals — pressure points</h4>
    <ul>{coercion}</ul>
  </div>
  <div>
    <h4>Geopolitical exposure</h4>
    <ul>{geo}</ul>
  </div>
</div>""")

# ── 3. PETRONAS / GLC ────────────────────────────────────────────────────
glc_rows = "".join(
    f'<tr><td class="k">{e(a["name"])}</td><td>{e(a["actor_type"])}</td>'
    f'<td style="text-align:center">{a["opacity_score"]:.1f}</td>'
    f'<td><span class="pill {risk_class(a["capture_risk"])}">{e(a["capture_risk"])}</span></td>'
    f'<td>{e(a["notes"])}</td></tr>'
    for a in pglc["actors"])
glc_asym = "".join(
    f'<li><b>{e(a["who_benefits"])}</b> benefit; <b>{e(a["who_bears_cost"])}</b> carry the cost. '
    f'{e(a["description"])} <span class="small">({e(a["notes"])})</span></li>'
    for a in pglc["rule_asymmetries"])

A(f"""
<h3>2.4 Second seed case — PETRONAS and the GLC layer</h3>
<p>Three actors control the country's largest pools of institutional capital. The structural
tension is the same in each: a commercial mandate and a national mandate held by the same board,
with the appointment power sitting outside the balance sheet.</p>
<table>
  <caption>GLC layer — opacity and capture risk</caption>
  <tr><th>Actor</th><th>Type</th><th>Opacity</th><th>Capture</th><th>Structural note</th></tr>
  {glc_rows}
</table>
<ul>{glc_asym}</ul>
<div class="note">Khazanah carries RM100B+ and PNB RM300B+ — between them, a large share of listed
Malaysian equity. When appointment is political and the mandate is dual, the performance drag is
real but diffuse. That diffuseness is exactly why it survives scrutiny.</div>""")

# ── 4. CIVX ──────────────────────────────────────────────────────────────
axis_rows = "".join(
    f'<tr><td class="k">{e(ax["name"])}</td>'
    f'<td>{e(" · ".join(ax["values"]))}</td>'
    f'<td>{e(ax["basis"])}</td>'
    f'<td><span class="pill {risk_class(ax["uncertainty"])}">{e(ax["uncertainty"])}</span></td></tr>'
    for ax in civx["assumption_axes"])

paths = civx["paths"]
axes6 = ["FISCAL", "ENERGY", "INSTITUTIONAL", "SOCIAL_COHESION", "SOVEREIGNTY", "INTERGENERATIONAL"]
header = "".join(f'<th>{e(p["path_id"].replace("MY-FISCAL-", ""))}<br>'
                 f'<span style="font-weight:normal;font-size:6.6pt">{e(p["name"].split(" — ")[0])}</span></th>'
                 for p in paths)
matrix_rows = "".join(
    f'<tr><td class="ax k">{e(ax.replace("_", " ").title())}</td>' +
    "".join(f'<td class="sc {score_class(p["resilience_scores"][ax])}">'
            f'{p["resilience_scores"][ax]:.1f}</td>' for p in paths) + "</tr>"
    for ax in axes6)

cards = []
for p in paths:
    cls = "pcard"
    if p["path_id"].endswith("BASE"):
        cls += " warn"
    if p["path_id"].endswith("WORST"):
        cls += " bad"
    assum = " · ".join(v for v in p["assumptions"].values())
    risks = "".join(f"<li>{e(r)}</li>" for r in p["key_risks"])
    irrev = "".join(f"<li>{e(i)}</li>" for i in p["irreversibility"])
    cards.append(f"""<div class="{cls} avoid">
  <span class="pid">{e(p["path_id"])} · {p["horizon_years"]}y</span>
  <h4>{e(p["name"])}</h4>
  <div class="assum"><b>Assumptions:</b> {e(assum)}</div>
  <div class="two"><div><b>Key risks</b><ul>{risks}</ul></div>
  <div><b>Irreversible if taken</b><ul>{irrev}</ul></div></div>
  <div class="small"><b>Option space:</b> {e(p["option_space"])} &nbsp;|&nbsp; {e(p["notes"])}</div>
</div>""")

lims = "".join(f"<li>{e(x)}</li>" for x in civx["limitations"])
calib = "".join(f"<li>{e(x)}</li>" for x in civx["calibration_data"])

A(f"""
<div class="pb"></div>
<h2><span class="num">3</span>CIVX — civilizational horizon, 2027 to 2040</h2>
<p class="lede">Five assumption axes, three explicit paths, six resilience axes per path. Every
number below is an interpretation held open for calibration — not a forecast.</p>

<h3>3.1 Assumption axes</h3>
<table>
  <caption>Each axis is stated with its range and its uncertainty class</caption>
  <tr><th>Axis</th><th>Values</th><th>Basis</th><th>Uncertainty</th></tr>
  {axis_rows}
</table>
<p class="small">Four of the five axes are political or behavioural. That is the honest shape of
this problem: the geology and the price are the easier half.</p>

<h3>3.2 Resilience matrix</h3>
<table class="matrix">
  <caption>Ordinal scores 0–1 · green ≥ 0.70 · amber 0.45–0.69 · red &lt; 0.45</caption>
  <tr><th class="ax">Resilience axis</th>{header}</tr>
  {matrix_rows}
</table>

<h3>3.3 The three paths</h3>
{"".join(cards)}

<div class="warnbox"><b>The gap that matters:</b> the distance between BEST (0.8 fiscal) and WORST
(0.2 fiscal) is not oil. Both extreme paths assume the same geology; they differ on political
choices — tax base, subsidy design, and how early the transition is funded. Oil sets the
weather. Reform decides the outcome.</div>""")

# ── 5. Limits & governance ───────────────────────────────────────────────
A(f"""
<div class="pb"></div>
<h2><span class="num">4</span>Limits, calibration debt and governance status</h2>
<div class="warnbox"><b>Status: SAFE_TO_STUDY.</b> CIVX is not decision authority. No path becomes
decision-eligible until it is calibrated against realised history and promoted by a sovereign
decision.</div>

<div class="two avoid">
  <div>
    <h4>Stated limitations</h4>
    <ul>{lims}</ul>
  </div>
  <div>
    <h4>Calibration backlog — the path to trust</h4>
    <ul>{calib}</ul>
    <p class="small">Until these five lines are measured, the resilience scores stay ordinal and
    the paths stay scenarios.</p>
  </div>
</div>

<h3>4.1 How to read this document</h3>
<ul>
  <li><b>POLIX is structural, not personal.</b> It maps roles, rules and flows — it does not
      allege motive in any individual. Capture risk is a property of a position, not a verdict
      on a person.</li>
  <li><b>CIVX is a study, not a prediction.</b> Three discrete paths, no Monte Carlo, no
      external shocks modelled. It is a reasoning scaffold.</li>
  <li><b>Epistemic tags are load-bearing.</b> Every rent flow and rule asymmetry carries its
      basis — OBSERVED, DERIVED or INTERPRETED. The distinction is the value.</li>
  <li><b>Nothing here is sourced from inside.</b> Public sources only. No insider knowledge.</li>
</ul>

<div class="note"><b>Provenance of this document.</b> The POLIX-v1.0.0 and CIVX-v1.0.0 seed
constructors were executed on 18 September 2026 for both cases, and the values printed here are
their own output, reproduced verbatim. The analysis layer is therefore sound.</div>

<div class="warnbox"><b>Status of the endpoint layer — declared, not hidden.</b> The tool wrappers
<code>capital_polix</code> and <code>capital_civx</code> failed on every live call at the MCP
boundary (a schema-name mismatch in the response envelope). The repair is written and staged;
the service reload is withheld pending a governed approval decision. Until that reload lands, the
intelligence in this brief is reproducible but not yet served through the tool interface. Read
this as a study produced correctly, from an interface not yet declared live.</div>

<div class="note"><b>What would make this decision-grade:</b> PETRONAS dividend against budget
assumption accuracy over ten years; realised GST-versus-SST revenue; DOSM projection error
against actual; and the state-versus-federal petroleum take resolved as a number rather than a
negotiation. Four measurements, and the whole structure tightens.</div>

<p class="small" style="margin-top:10pt;color:#8A98A5">
WEALTH — capital intelligence for arifOS · POLIX-v1.0.0 · CIVX-v1.0.0 · seed case
<code>{e(civx["domain"])}</code> · generated {e(civx["computed_at"][:19].replace("T", " "))} UTC ·
DITEMPA BUKAN DIBERI.</p>
</body></html>""")

open(HTML_OUT, "w").write("\n".join(parts))
print("HTML written:", HTML_OUT, len("\n".join(parts)), "chars")
