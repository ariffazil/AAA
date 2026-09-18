#!/usr/bin/env python3
"""Build CHRON-REALITY-MAP PDF. Light theme. OBSERVE_ONLY audit artifact."""
from pathlib import Path
from weasyprint import HTML, CSS

OUT = Path("/root/AAA/forge_work/2026-09-18-chron-reality-map")
OUT.mkdir(parents=True, exist_ok=True)

CSS_TEXT = """
@page { size: A4; margin: 14mm 13mm 16mm 13mm;
  @bottom-center { content: "CHRON REALITY MAP v1 · 2026-09-18 12:11 MYT · Lane B RECEIPT (not SEAL) · page " counter(page) " / " counter(pages);
    font-family: 'DejaVu Sans', sans-serif; font-size: 6.6pt; color: #7a8494; } }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', 'Noto Sans', sans-serif; font-size: 8.1pt; line-height: 1.42; color: #1d2430; margin: 0; }
h1 { font-size: 17pt; margin: 0 0 2px 0; letter-spacing: -0.3px; color: #0f1a2b; }
h2 { font-size: 10.6pt; margin: 15px 0 6px 0; padding: 5px 8px; background: #eef2f7;
     border-left: 3.5px solid #2f5d8a; color: #10233c; page-break-after: avoid; }
h3 { font-size: 9pt; margin: 10px 0 4px 0; color: #24405f; page-break-after: avoid; }
p { margin: 3px 0; }
.hdr { border-bottom: 2.5px solid #0f1a2b; padding-bottom: 8px; margin-bottom: 10px; }
.hdr .sub { font-size: 8.4pt; color: #46536a; }
.meta { display: table; width: 100%; margin-top: 7px; font-size: 7.4pt; }
.meta .r { display: table-row; }
.meta .c { display: table-cell; padding: 1.6px 10px 1.6px 0; }
.k { color: #6a7488; text-transform: uppercase; letter-spacing: 0.4px; font-size: 6.6pt; }
.v { color: #16202e; font-weight: 600; }
table { width: 100%; border-collapse: collapse; margin: 4px 0 8px 0; font-size: 6.9pt; }
th { background: #24405f; color: #fff; text-align: left; padding: 3.2px 4px; font-weight: 600; font-size: 6.6pt; }
td { padding: 2.8px 4px; border-bottom: 0.5px solid #dde3ec; vertical-align: top; }
tr:nth-child(even) td { background: #f7f9fc; }
.mono { font-family: 'DejaVu Sans Mono', monospace; font-size: 6.3pt; }
.tag { font-family: 'DejaVu Sans Mono', monospace; font-size: 6.2pt; padding: 0.5px 3px; border-radius: 2px; font-weight: 700; white-space: nowrap; }
.PASS { background: #dff3e4; color: #1c6b32; } .FAIL { background: #fbe0e0; color: #93211f; }
.PARTIAL { background: #fdf0d8; color: #8a5a0b; } .UNKNOWN { background: #e8eaf0; color: #4a5265; }
.DRIFT { background: #fbe0e0; color: #93211f; } .UNBUILT { background: #e8eaf0; color: #4a5265; }
.ACTIVE { background: #dff3e4; color: #1c6b32; } .DORMANT { background: #e8eaf0; color: #4a5265; }
.ARMED { background: #fdf0d8; color: #8a5a0b; } .BROKEN { background: #fbe0e0; color: #93211f; }
.box { border: 0.8px solid #ccd6e4; background: #f9fbfd; padding: 7px 9px; margin: 6px 0; page-break-inside: avoid; }
.box.warn { border-color: #e0b48a; background: #fffaf3; }
.box.law { border-color: #2f5d8a; background: #f2f7fc; }
.box h3 { margin-top: 0; }
.big { font-size: 11pt; font-weight: 700; color: #0f1a2b; }
ul { margin: 3px 0 3px 14px; padding: 0; } li { margin: 1.6px 0; }
.foot { margin-top: 12px; padding-top: 7px; border-top: 1.5px solid #0f1a2b; font-size: 7.2pt; color: #46536a; }
.two { display: table; width: 100%; } .two > div { display: table-cell; width: 50%; vertical-align: top; padding-right: 9px; }
.small { font-size: 6.8pt; color: #56627a; }
.verdict { border: 1.2px solid #0f1a2b; padding: 9px 11px; margin: 7px 0; page-break-inside: avoid; }
.verdict .n { font-size: 7pt; font-weight: 700; color: #2f5d8a; letter-spacing: 0.5px; }
.verdict h3 { margin: 2px 0 4px 0; font-size: 9.6pt; }
.chk { font-family: 'DejaVu Sans Mono', monospace; }
"""

H = []
A = H.append

A("""<!doctype html><html><head><meta charset="utf-8"><title>CHRON Reality Map v1</title></head><body>""")

# ── HEADER ───────────────────────────────────────────────────────────────
A("""
<div class="hdr">
<h1>CHRON — REALITY MAP</h1>
<div class="sub">What CHRON actually is on this machine, right now. Every line below is answerable to an artifact
that was opened, hashed, counted, or executed during this audit. Nothing is inferred from a declaration.</div>
<div class="meta">
  <div class="r"><div class="c"><span class="k">Reference</span><br><span class="v">CHRON::REALITY_MAPPER::v1</span></div>
  <div class="c"><span class="k">Authority</span><br><span class="v">ARIF (F13)</span></div>
  <div class="c"><span class="k">Mode</span><br><span class="v">OBSERVE_ONLY / AUDIT</span></div>
  <div class="c"><span class="k">Mutations</span><br><span class="v">0 — read-only</span></div></div>
  <div class="r"><div class="c"><span class="k">Render</span><br><span class="v">2026-09-18 12:11 MYT (04:11Z)</span></div>
  <div class="c"><span class="k">Seat</span><br><span class="v">HERMES (i-ARIF) on KVM8</span></div>
  <div class="c"><span class="k">Class</span><br><span class="v">Lane B RECEIPT — not a SEAL</span></div>
  <div class="c"><span class="k">Verdict model</span><br><span class="v">UNKNOWN / SABAR / HOLD / PARTIAL / SEAL</span></div></div>
</div>
<div class="box law">
<b>The constraint this document is written under.</b> DECLARATION ≠ MECHANISM. A file named <span class="mono">chron.py</span>
is not a running clock. A job marked <span class="mono">enabled</span> is not a job that fired. An empty namespace is not a
quiet subsystem. Where the evidence does not exist, this map says <span class="mono">UNBUILT</span> or
<span class="mono">UNKNOWN</span> — never PASS. The federation's own spine gate already sets that precedent: a boundary with
no artifact to test it reports <span class="tag UNBUILT">UNBUILT</span>, "honest, and NOT a pass."
</div>
""")

# ── PRIMARY QUESTION ─────────────────────────────────────────────────────
A("""
<div class="box warn">
<h3>Primary question</h3>
<p class="big">"Apakah task, loop, capability, dan reality-flow CHRON yang sedang hidup sekarang?"</p>
<p class="small">Answer in one sentence, from evidence only: <b>a date store (5 events), a sealed gate script (6 PASS /
3 UNBUILT), one live card lane that has produced two artifacts and delivered none, a growing receipt pile in which
100% of rows lack a trace_id, and a learning loop that inhales twice a day and has closed zero policies.</b>
Everything else that carries the name CHRON today is either a document or an empty directory.</p>
</div>
""")

# ── PHASE 1 ──────────────────────────────────────────────────────────────
A('<h2>PHASE 1 — REALITY INVENTORY</h2>')
A('<p class="small">Classes are fixed by the mission. Confidence: HIGH = opened/counted/executed this audit; MED = surface confirmed, contents not exhaustively read; LOW = name only.</p>')

def table(headers, rows):
    A('<table><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>')
    for r in rows:
        A('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>')
    A('</table>')

A('<h3>1.1 EVENT SOURCES</h3>')
table(["ID","PATH / SURFACE","LAST ACTIVITY","DECLARED","OBSERVED","CONF"], [
 ["E1","<span class='mono'>/root/.hermes/cron/jobs.json</span>","2026-09-18T12:06:12+08","job registry","39 jobs · 13 enabled · updated today","HIGH"],
 ["E2","<span class='mono'>/root/.hermes/cron/deliveries.db</span>","2026-09-18T12:06","delivery ledger","rows delivered today (12:06, 09:59, 07:02)","HIGH"],
 ["E3","<span class='mono'>systemctl list-timers --all</span>","2026-09-18T12:11","substrate health","30+ timers live; <b>none named chron</b>","HIGH"],
 ["E4","root crontab","2026-09-18 (hourly jobs firing)","infra loops","~45 lines active; <b>no CHRON entry</b>","HIGH"],
 ["E5","<span class='mono'>/etc/cron.d/aaa-rsi-loop</span>","2026-09-18T12:07:02+08","RSI exhale loop","present + firing (see L1–L4)","HIGH"],
 ["E6","<span class='mono'>/root/AAA/scripts/chron_events.json</span>","2026-09-18T10:25","canonical date store","5 events, 5/5 carry source+confidence+date+audience","HIGH"],
 ["E7","<span class='mono'>forge_work/alpha-zen/cycles.jsonl</span>","2026-09-18T10:40","render receipts","8 cycle records; 6 render_status OK; last 1 <span class='mono'>rejection_tracking=NOT_MEASURED</span>","HIGH"],
 ["E8","<span class='mono'>~/.local/share/arifos/event_bus.jsonl</span>","2026-09-17T22:15:02Z","event spine","last record <span class='mono'>sealed_events_sweep → DEFECTS_FOUND exit 1</span>","MED"],
 ["E9","<span class='mono'>~/.local/share/arifos/arifflow_receipts.jsonl</span>","2026-09-18T03:51:44Z","execution receipts","35,743 rows · <b>35,743/35,743 trace_id NULL</b>","HIGH"],
])

A('<h3>1.2 MEMORY SOURCES</h3>')
table(["ID","PATH / SURFACE","LAST ACTIVITY","DECLARED","OBSERVED","CONF"], [
 ["M1","<span class='mono'>/root/AAA/claim_ledger/claims.db</span>","2026-09-18T11:51","claim ledger","21 claims · 11 verifications · 6 artifacts · 38 chain rows · append-only triggers present. <b>Separate organ — not CHRON-owned.</b>","HIGH"],
 ["M2","<span class='mono'>A-FORGE/duties/logs/world-model-lite.jsonl</span>","2026-08-27T02:20:26Z","world model","792 rows parsed · last write <b>22 days ago</b> · writer is its only reader","HIGH"],
 ["M3","Qdrant <span class='mono'>:6333</span>","live at probe","vector memory","20 collections (arifos_memory, vault_canon, atlas333_eureka…) — presence only","MED"],
 ["M4","<span class='mono'>/root/arifOS/VAULT999/chronus/</span>","dir mtime 2026-09-09","CHRON vault namespace","<b>EMPTY — 0 entries, 0 bytes</b>","HIGH"],
 ["M5","<span class='mono'>forge_work/alpha-zen/cards/</span>","2026-09-18T10:32","episodic card store","2 records (morning/night), 1 day deep","HIGH"],
 ["M6","<span class='mono'>/root/AAA/reality-graph/</span>","(directory present)","Reality Graph","existence confirmed; contents not enumerated this pass","UNKNOWN"],
])

A('<h3>1.3 PREDICTION SOURCES</h3>')
table(["ID","PATH / SURFACE","LAST ACTIVITY","DECLARED","OBSERVED","CONF"], [
 ["P1","<span class='mono'>~/.local/share/arifos/state/closure-ledger.jsonl</span>","2026-09-17T23:45","prediction store","<b>4 records</b> carrying <span class='mono'>{claim, predicted, verify_cmd, verify_by, observed, verdict}</span> — the only live prediction object found","HIGH"],
 ["P2","<span class='mono'>world-model-lite.jsonl</span>","2026-08-27T02:20:26Z","prediction stream","792 predictions, 792 distinct ids, <b>5 distinct actions</b>, <span class='mono'>allow_mutate=False</span> on 734. <b>No outcome / verify_at field exists in the row schema.</b>","HIGH"],
 ["P3","calibration records","—","Brier / log-loss / ECE","<b>NOT FOUND.</b> Only a proposal: <span class='mono'>AAA/scripts/proposals/apex-zen-calibration-2026-09-13.md</span>","HIGH"],
])

A('<h3>1.4 ATTENTION SOURCES</h3>')
table(["ID","PATH / SURFACE","LAST ACTIVITY","DECLARED","OBSERVED","CONF"], [
 ["A1","<span class='mono'>/root/scripts/attention_governor.py</span> (21 KB)","2026-09-16T11:00","attention governor","present; scans carry / cron / repos / organs / pointers / seal","HIGH"],
 ["A2","<span class='mono'>state/attention-ledger.jsonl</span>","2026-09-17T23:45","attention ledger","9 rows only. 09-16: 32 loops. 09-17: 30 loops, composition changed (see D6)","HIGH"],
 ["A3","<span class='mono'>state/attention-2026-09-17.json</span>","2026-09-17T23:45","daily snapshot","16.8 KB, <span class='mono'>status: COMPLETE</span>","HIGH"],
 ["A4","Hermes job <span class='mono'>attention-closure</span> (23:45)","2026-09-17T23:46 ok","daily closure pass","enabled · <span class='mono'>--no-agent</span> · empty stdout delivers nothing","HIGH"],
 ["A5","ALPHA-ZEN cards + <span class='mono'>docforge</span> editions","2026-09-18T10:32 / 09:57","human-facing cards","2 card artifacts today; EDITION-001.pdf + EDITION-002 built with light-theme + ink gates","HIGH"],
])

A('<h3>1.5 LEARNING SOURCES</h3>')
table(["ID","PATH / SURFACE","LAST ACTIVITY","DECLARED","OBSERVED","CONF"], [
 ["L1","<span class='mono'>AAA/rsi/state/atoms.jsonl</span>","2026-09-18T12:07","RSI atoms","346 atoms · 318 verified · 28 rejected","HIGH"],
 ["L2","<span class='mono'>AAA/rsi/state/loop-ledger.jsonl</span>","2026-09-18T12:07","loop receipts","14 cycles · <b>5 EXHALED · 8 INHALE_ONLY</b> · 1 note. Latest 4 cycles all INHALE_ONLY","HIGH"],
 ["L3","<span class='mono'>AAA/rsi/state/consequence.jsonl</span>","2026-09-18T12:07","consequence ledger","33 rows · <b>7 PENDING</b> (consequence not yet observable)","HIGH"],
 ["L4","<span class='mono'>AAA/rsi/state/baselines.json</span>","2026-09-18T12:07","capability baselines","7 baselines, <b>all status PENDING</b>, 7-day windows","HIGH"],
 ["L5","<span class='mono'>AAA/governance/UNRATIFIED-LESSONS-LEDGER.jsonl</span>","(12 rows)","lesson ledger","10 <span class='mono'>UNRATIFIED_LESSON</span> + 2 <span class='mono'>PENDING_V12_FOLD</span> → <b>0 ratified</b>","HIGH"],
 ["L6","<span class='mono'>AAA/scars/</span>","last new scar 2026-09-15","scar store","13 scars + 4 auto-candidates (latest 2026-09-15)","HIGH"],
 ["L7","POLICY CHANGES","—","lesson → policy promotion","<b>0 OBSERVED.</b> No policy-candidate object exists; nothing can be promoted from one episode","HIGH"],
])

A("""
<div class="box"><h3>Phase 1 finding — the inventory's shape</h3>
<p>CHRON's <b>evidence</b> is real and countable on every surface above. What is not present is CHRON <b>as a
running thing</b>: there is no service, no timer, no cron line, and no job whose name or target is CHRON. The
nearest live neighbours each own a different organ — the RSI loop belongs to capability evolution, the attention
governor belongs to the attention lane, <span class="mono">docforge-edition-daily</span> belongs to the briefing
lane. CHRON's own code exists and runs on demand; nothing schedules it.</p></div>
""")

# ── PHASE 2 ──────────────────────────────────────────────────────────────
A('<h2>PHASE 2 — SPINE EXTRACTION</h2>')
A("""<p class="small">The spine below is the one CHRON itself declares and tests: <span class="mono">WORLD → OBSERVE → ENCODE →
SELECT → DELIVER → RESPONSE → OUTCOME → COMPARE → EXPERIENCE → MEMORY → LEARNING → SHADOW → VALIDATION →
PROMOTION → NEW VERSION</span>. It was <b>executed</b> this audit — <span class="mono">python3 /root/AAA/scripts/chron_spine_gate.py</span>
— not read. Raw verdict: <b>6 PASS · 0 FAIL · 3 UNBUILT</b>, self-test PASS (every check can reject).</p>""")

A('<h3>2.1 Edges with an artifact behind them</h3>')
table(["EDGE","SOURCE → TARGET","DECLARED","OBSERVED","PROOF","LAST SEEN","STATUS"], [
 ["E-01","WORLD → OBSERVE","events carry provenance","5/5 events carry source, confidence, date, audience","<span class='mono'>chron_events.json</span> + gate check 1","2026-09-18T10:25",'<span class="tag PASS">PASS</span>'],
 ["E-02","OBSERVE → CLAIM","every cell classed","9 rows, every cell tagged (OBS/DER/INT/CONTESTED)","gate check 2 + <span class='mono'>cards/2026-09-18-*.json</span>","2026-09-18T10:32",'<span class="tag PASS">PASS</span>'],
 ["E-03","CLAIM → ATTENTION","truth ≠ urgency","truth and urgency exposed separately; provably diverge on a collision pair","gate check 3","2026-09-18T11:02",'<span class="tag PASS">PASS</span>'],
 ["E-04","ATTENTION → DELIVERY","newest row resolves","newest row resolves; 4 older rows stale, all predating the content-addressing fix","gate check 4","2026-09-18T11:02",'<span class="tag PASS">PASS</span>'],
 ["E-05","DELIVERY → HUMAN","one reader contract","12 patterns (10 word-bounded prose, 2 literal); inner-state rule present","gate check 5","2026-09-18T11:02",'<span class="tag PASS">PASS</span>'],
 ["E-06","LEARNING → PRODUCTION","learner behind a ladder","engine defaults to SHADOW and cannot send; a separate production renderer exists — the ladder holds","gate check 8","2026-09-18T11:02",'<span class="tag PASS">PASS</span>'],
 ["E-07","EXPERIENCE → MEMORY","episodes persist","collection has no payload schema","gate check 6",'<span class="mono">—</span>','<span class="tag UNBUILT">UNBUILT</span>'],
 ["E-08","MEMORY → POLICY","lesson promotion","no policy-candidate object exists","gate check 7",'<span class="mono">—</span>','<span class="tag UNBUILT">UNBUILT</span>'],
 ["E-09","OUTCOME → LEARNING","verified prediction retained","no prediction object exists in that lane, so no failed prediction can be retained","gate check 9",'<span class="mono">—</span>','<span class="tag UNBUILT">UNBUILT</span>'],
])

A('<h3>2.2 Edges the declaration implies but no artifact carries</h3>')
table(["EDGE","DECLARED","OBSERVED","PROOF","STATUS"], [
 ["ENCODE (format contract)","canonical encode step","<span class='mono'>alpha_zen_card.schema.json</span> exists and gates a card; no CHRON-owned encode contract","schema file present, not referenced by any CHRON trigger",'<span class="tag PARTIAL">PARTIAL</span>'],
 ["RESPONSE (did the human reply?)","human response is an event","delivery receipts exist; <b>no response-capture edge</b> from the reader back into CHRON","<span class='mono'>deliveries.db</span> shows DELIVERED, never REPLIED",'<span class="tag UNKNOWN">UNKNOWN</span>'],
 ["COMPARE (predicted vs observed)","outcome comparison","<b>2 of 4</b> closure-ledger records reached a verdict; the rest open or contradicted","<span class='mono'>closure-ledger.jsonl</span>",'<span class="tag PARTIAL">PARTIAL</span>'],
 ["SHADOW / VALIDATION / PROMOTION","maturity chain before promotion","RSI verifier marks itself <span class='mono'>independence_class: NOMINAL · independent: false · provisional: true</span>","<span class='mono'>rsl/state/receipts/loop-2026-09-18T120702+0800.json</span>",'<span class="tag PARTIAL">PARTIAL</span>'],
 ["NEW VERSION","promotion produces a new version","<b>0 policies promoted</b>, so no new version has been produced","UNRATIFIED-LESSONS-LEDGER (12 rows, 0 ratified)",'<span class="tag FAIL">FAIL</span>'],
])

# ── PHASE 3 ──────────────────────────────────────────────────────────────
A('<h2>PHASE 3 — DECLARATION vs REALITY (REALITY_DRIFT_LEDGER)</h2>')
table(["#","CAPABILITY","DECLARED_MECHANISM","OBSERVED_MECHANISM","CONTRADICTION","SEV"], [
 ["D1","ALPHA-ZEN three-pulse lane","3 jobs enabled, delivering cards to the two-person room <span class='mono'>-1003815535761</span> at 07:15 / 14:00 / 21:15",
  "All 3 created <b>2026-09-18T10:02</b>; <span class='mono'>last_run_at = null</span> on all 3; <span class='mono'>repeat.completed = 0</span>",
  "Jobs were born 2h47m <b>after</b> their own 07:15 slot. A card pipeline that pass all its gates has <b>zero executions and zero delivery receipts</b>. SCHEDULED ≠ RAN.","HIGH"],
 ["D2","Daily sovereign brief","<span class='mono'>docforge-edition-daily · 0 6 * * *</span> → PDF to Arif's DM",
  "Created 09:34 today; first run <b>09:59</b> (EDITION-001.pdf, real PDF, gates passed) — nearly 4 h after the declared window",
  "The 06:00 brief has never run at 06:00. For 2026-09-18 no 06:00 artifact exists at all; what exists is a 09:59 artifact under a 06:00 label.","MED"],
 ["D3","World model / prediction substrate","a maintained prediction layer","792 predictions, 792 distinct ids, <b>only 5 distinct actions</b>; last write 2026-08-27T02:20Z; row schema has <b>no outcome field</b>; the writer is the only reader",
  "Artifacts look healthy (valid JSONL, growing to 600 KB) while the producer silently ceased <b>22 days ago</b>. Exactly the failure shape the federation already named: a subsystem whose artifacts look fine while it has stopped.","HIGH"],
 ["D4","VAULT999 CHRON namespace","<span class='mono'>VAULT999/chronus/</span> exists as a namespace","directory present, <b>0 entries</b>","A named namespace with zero records reads as 'nothing to seal' when it actually means 'nothing was ever sealed'. Empty ≠ quiet.","MED"],
 ["D5","Execution receipts as causal ledger","receipts bind action to objective","35,743 rows; <b>35,743 rows with <span class='mono'>trace_id = NULL</span></b> (100%); last row verdict <span class='mono'>UNKNOWN · signal FQ_SIGNAL_DRIFT</span>",
  "A receipt without a trace_id is an event-pile entry, not a causal-ledger entry. The doctrine that named this defect is being violated by the running system, measurably, at 100%.","HIGH"],
 ["D6","Attention closure (silent jobs)","CRON_SILENT is tracked and surfaced","2026-09-16 ledger: 32 loops — CRON_DISABLED 15, CRON_SILENT 6. 2026-09-17: 30 loops — CRON_DISABLED 22, <b>CRON_SILENT absent</b>",
  "The silent-job category did not get fixed; it disappeared while the disabled count rose 15 → 22. A reclassification, not a resolution — and the closure ledger's own record (<span class='mono'>REALITY_DISAGREED</span>) proves reality refused the prediction.","MED"],
 ["D7","KVM4 cron reachability","cron API not exposed on KVM4","<span class='mono'>GET /cron/jobs</span> → <b>HTTP error <span class='mono'>proxy_attribution_required</span></b> (not empty, not 404)",
  "The recorded finding said the endpoint 'returns empty'. It does not — it refuses with a proxy-attribution error. 'No data' was read as 'all clear'. <span class='mono'>/health</span> answers <span class='mono'>{ok:true,status:live}</span> on the same port.","MED"],
 ["D8","Audit artifact currency","blockers B1–B4 describe live code","<span class='mono'>alpha_zen_engine.py</span> was <b>repaired at 11:18 today</b> — the year-wrong budget date and the frozen <span class='mono'>od1_days</span> literal are gone from the code; <span class='mono'>AUDIT-ALPHA-ZEN-2026-09-18.json</span> records <b>no supersession</b>",
  "The blockers are fixed in the code and still stand in the audit. A reader picking up that artifact tomorrow inherits four defects that no longer exist — Stale Claim Propagation, in the artifact whose job was to prevent exactly this.","MED"],
])

A("""
<div class="box warn"><h3>Phase 3 note on the one contradiction that went the other way</h3>
<p>Not every discrepancy is decay. <span class="mono">chron.py</span> and <span class="mono">alpha_zen_engine.py</span> now
<b>read one canonical store</b> (<span class="mono">chron_events.json</span>) and compute every day-count at render; the
engine returns <b>no countdown at all</b> rather than inventing one when the store is unreadable. That is the correct
repair of the exact defect class this phase hunts — two clocks drifting silently because both numbers look plausible.
Recorded here so the ledger is not one-sided.</p></div>
""")

# ── PHASE 4 ──────────────────────────────────────────────────────────────
A('<h2>PHASE 4 — TASK EXTRACTION (only tasks with evidence)</h2>')
A('<p class="small">No task below is proposed. Each is either a registered trigger observed in the scheduler, or a coded pipeline observed on disk and clearly wired to one.</p>')
table(["TASK_ID","PURPOSE","TRIGGER","OUTPUT","SCHEDULE","LAST_RUN","LAST_SUCCESS","DEPENDENCIES","RECEIPT_PATH","STATUS"], [
 ["CH-T01","Morning dual-lens card → two-person room","Hermes cron <span class='mono'>8313453a73a7</span>","1 message + ALPHA-ZEN-MORNING.png","15 7 * * *","<b>null</b>","—","skills/apex-cognitive-reflex/alpha-zen-lanes · chron.py · alpha_zen_card.py","<span class='mono'>cards/2026-09-18-morning.json</span>",'<span class="tag ARMED">ARMED</span>'],
 ["CH-T02","Afternoon body check → same room","Hermes cron <span class='mono'>3e40c50f0ca2</span>","1 message","0 14 * * *","<b>null</b>","—","WELL organ tools · chron.py","cycles.jsonl (manual runs only)",'<span class="tag ARMED">ARMED</span>'],
 ["CH-T03","Night card → same room","Hermes cron <span class='mono'>161c0d5e0d0c</span>","1 message + ALPHA-ZEN-NIGHT.png","15 21 * * *","<b>null</b>","—","GEOX · WEALTH · chron.py · alpha_zen_card.py","<span class='mono'>cards/2026-09-18-night.json</span>",'<span class="tag ARMED">ARMED</span>'],
 ["CH-T04","Sovereign daily brief PDF → Arif DM","Hermes cron <span class='mono'>a77681618199</span>","EDITION-00N.pdf + ledger + receipt","0 6 * * *","2026-09-18T09:59:06","ok (3h59m late)","weasyprint 69.0 · base-a4 template · brief-rules-context.py","<span class='mono'>forge_work/docforge-ledger.jsonl</span>",'<span class="tag ACTIVE">ACTIVE</span>'],
 ["CH-T05","Daily attention closure + quiet scan","Hermes cron <span class='mono'>attention-closure</span>","ledger row + snapshot (silence if clean)","45 23 * * *","2026-09-17T23:46","ok","attention_governor.py · closure_probe.py","<span class='mono'>state/attention-ledger.jsonl</span>",'<span class="tag ACTIVE">ACTIVE</span>'],
 ["CH-T06","Capability evolution (inhale→exhale)","<span class='mono'>/etc/cron.d/aaa-rsi-loop</span>","atoms, loop receipt, baselines","every 6 h @ :07","2026-09-18T12:07","<span class='mono'>INHALE_ONLY</span> (no exhale)","promote.py (FORBIDDEN_PATHS self-test) · rsi verifier","<span class='mono'>rsi/state/receipts/loop-*.json</span>",'<span class="tag ACTIVE">ACTIVE</span>'],
 ["CH-T07","FI mesh health sentinel","<span class='mono'>/etc/cron.d/aaa-mesh-health</span>","mesh-health.json + holds","17 3 * * *","(daily)","—","mesh-health-probe.sh","<span class='mono'>forge_work/mesh-health.log</span>",'<span class="tag ACTIVE">ACTIVE</span>'],
 ["CH-T08","Prediction stream for federation state","A-FORGE duties loop","world-model-lite.jsonl rows","declared continuous","2026-08-27T02:20Z","stale 22 d","world_model_lite.py — <b>no consumer</b>","<span class='mono'>duties/logs/world-model-lite.jsonl</span>",'<span class="tag BROKEN">BROKEN</span>'],
 ["CH-T09","Gate + self-test over the spine","manual / audit only","6 PASS · 0 FAIL · 3 UNBUILT","<b>no trigger</b>","2026-09-18T12:10 (by this audit)","PASS","chron_events.json · cards/ · cycles.jsonl","stdout only — no receipt path",'<span class="tag DORMANT">DORMANT</span>'],
 ["CH-T10","Render the CHRON clock","manual / called from job prompts","ranked temporal list to stdout","<b>no trigger</b>","invoked inside CH-T01..03 prompts","PASS","chron_events.json","none",'<span class="tag DORMANT">DORMANT</span>'],
])

A("""
<div class="box"><h3>Phase 4 finding — armed is not fired</h3>
<p>Three tasks (CH-T01..03) carry a full contract, a named audience, a gate that can refuse, and a rendered artifact
already sitting on disk from manual runs. None has ever executed. The difference between that and a working lane is
not code — it is <b>one receipt</b>. The next scheduled opportunity is <b>14:00 MYT today</b> (CH-T02).</p></div>
""")

# ── PHASE 5 ──────────────────────────────────────────────────────────────
A('<h2>PHASE 5 — LOOP CLOSURE AUDIT (9 loops)</h2>')
table(["#","LOOP","EXISTS","PROOF","LAST EVIDENCE","STATUS"], [
 ["L1","Observation → Witness","Yes","5/5 events carry provenance; spine gate check 1","2026-09-18T10:25",'<span class="tag PASS">PASS</span>'],
 ["L2","Witness → Claim","Yes","21 claims with source_ref + locator + sha256 binding; append-only triggers; spine check 2","2026-09-18T11:51",'<span class="tag PASS">PASS</span>'],
 ["L3","Claim → Prediction","Partly","Only closure-ledger carries a prediction object — <b>4 records total</b>; none derived from the claim ledger automatically","2026-09-17T23:45",'<span class="tag PARTIAL">PARTIAL</span>'],
 ["L4","Prediction → Verification","Yes, small","<span class='mono'>verify_cmd</span> + <span class='mono'>verify_by</span> present on every closure row; appointment honoured at 23:45","2026-09-17T23:45",'<span class="tag PASS">PASS</span>'],
 ["L5","Verification → Outcome","Yes","Observed values recorded: 2 × <span class='mono'>PREDICTION_MATCHED</span>, 1 × <span class='mono'>REALITY_DISAGREED</span>, 1 <span class='mono'>OPEN</span> due 2026-09-21","2026-09-17T23:45",'<span class="tag PARTIAL">PARTIAL</span>'],
 ["L6","Outcome → Calibration","<b>No</b>","No Brier / log-loss / ECE artifact anywhere; scoring never computed; only a 2026-09-13 proposal","—",'<span class="tag FAIL">FAIL</span>'],
 ["L7","Error → Lesson / Scar","Yes","12 unratified lessons + 13 scars + 4 auto-candidates; 28 RSI atoms rejected rather than absorbed","2026-09-18T12:07",'<span class="tag PASS">PASS</span>'],
 ["L8","Lesson → Policy","<b>No</b>","12 lessons, <b>0 ratified</b>, 0 policy-candidate objects; RSI <span class='mono'>organs</span> outcome reads <span class='mono'>applied: false, reason: deferred</span>","—",'<span class="tag FAIL">FAIL</span>'],
 ["L9","Policy → Attention","<b>No</b>","Attention is generated from <i>gaps</i> (stale pointers, silent cron, dirty repos), not from policy; no policy→attention edge observed","2026-09-17T23:45",'<span class="tag FAIL">FAIL</span>'],
])

A("""
<div class="box warn"><h3>Phase 5 finding — the loop closes at verification and dies there</h3>
<p>Six of nine loops have real artifacts. Three do not, and they are the three that would make CHRON <i>learn</i>:
calibration, promotion, and attention feedback. The system today can <b>observe, claim, predict, and verify</b>.
It cannot <b>score itself, promote a lesson, or let a promoted policy change what it looks at next</b>. That is the
learning-closure problem, and it is measured here rather than asserted: one failed prediction
(<span class="mono">REALITY_DISAGREED</span>, silent-job count = 6) exists on disk and has produced no calibration
entry, no lesson row, and no policy.</p></div>
""")

# ── PHASE 6 ──────────────────────────────────────────────────────────────
A('<h2>PHASE 6 — CHRON MATURITY SCORE (counts only, no subjective scoring)</h2>')
A('<h3>6.1 Observed totals — each figure bound to the artifact that produced it</h3>')
table(["METRIC","COUNT","SOURCE ARTIFACT","STATE OF THAT ARTIFACT"], [
 ["TOTAL_EVENTS_OBSERVED","14 named events (5 CHRON store + 8 render cycles + 1 event-bus record)","<span class='mono'>chron_events.json</span> · <span class='mono'>cycles.jsonl</span> · <span class='mono'>event_bus.jsonl</span>","last event-bus record ends <span class='mono'>DEFECTS_FOUND exit 1</span>"],
 ["TOTAL_RECEIPTS_OBSERVED","35,743 (arifflow) + 38 (claim chain) + 9 (attention)","<span class='mono'>arifflow_receipts.jsonl</span> · <span class='mono'>claims.db::ledger_chain</span> · <span class='mono'>attention-ledger.jsonl</span>","<b>100% of the 35,743 carry trace_id = NULL</b>"],
 ["TOTAL_PREDICTIONS_OBSERVED","796 (792 world-model + 4 closure-ledger)","<span class='mono'>world-model-lite.jsonl</span> · <span class='mono'>closure-ledger.jsonl</span>","792 are dead &amp; outcome-less (22 d stale); 4 are live"],
 ["TOTAL_VERIFICATIONS_OBSERVED","14 (11 claim verifications + 3 closure verdicts)","<span class='mono'>claims.db::verifications</span> · <span class='mono'>closure-ledger.jsonl</span>","1 of the 11 is <span class='mono'>PARTIAL</span> (evidence hash moved under the claim)"],
 ["TOTAL_LESSONS_OBSERVED","29 (12 unratified + 13 scars) + 4 scar candidates + 346 RSI atoms","<span class='mono'>UNRATIFIED-LESSONS-LEDGER.jsonl</span> · <span class='mono'>scars/</span> · <span class='mono'>atoms.jsonl</span>","atoms: 318 verified / 28 rejected; every verification <span class='mono'>provisional</span>"],
 ["TOTAL_POLICY_CHANGES_OBSERVED","<b>0</b>","no artifact exists","nothing to bind — the object class is absent"],
])

A('<h3>6.2 Which of these is CHRON</h3>')
A("""
<table>
<tr><th style="width:30%">Candidate identity</th><th style="width:10%">Mark</th><th>Evidence, or the absence of it</th></tr>
<tr><td><b>Scheduler</b></td><td class="chk">[x]</td><td>39-job registry + delivery ledger + 30 systemd timers + ~45 crontab lines, all live today. <b>But none of them is CHRON's</b> — CHRON owns no trigger. Scheduler capability exists in the substrate; CHRON is a client of it, not the owner.</td></tr>
<tr><td><b>Relevance Engine</b></td><td class="chk">[x]</td><td><span class="mono">chron.py</span> ranks by urgency × consequence × actionability × confidence with a non-linear urgency curve and drops expired events; the card gate selects 9 of 18 signals and <b>refuses</b> a bad card. Scoring is real and executable. Its trigger is not.</td></tr>
<tr><td><b>Claim-State Engine</b></td><td class="chk">[ ]</td><td>A real claim-state store exists — <span class="mono">claims.db</span>, 21 claims, 11 verifications, append-only triggers, <span class="mono">supersedes_claim_id</span>. It is <b>a separate organ</b>; no CHRON-owned claim-state object was observed, and nothing in CHRON reads it automatically.</td></tr>
<tr><td><b>Temporal Reconciliation Layer</b></td><td class="chk">[ ]</td><td>This is the declared identity. Observed: a gate script that reconciles <i>declared boundaries against artifacts</i> (6 PASS / 3 UNBUILT) and runs only when a human types its name. Declared-vs-observed reconciliation as a <b>daily job</b> does not exist — which is why D1–D8 were still open today.</td></tr>
<tr><td><b>Learning System</b></td><td class="chk">[ ]</td><td>The loop runs (14 cycles, 346 atoms) and does not close: 8 of 14 cycles inhaled without exhaling, latest 4 consecutive cycles <span class="mono">INHALE_ONLY</span>, all 7 baselines <span class="mono">PENDING</span>, 7 consequences <span class="mono">PENDING</span>, 12 lessons unratified, 0 policies. A verifier that grades its own author's work is not a learning system yet.</td></tr>
</table>
<div class="box"><p class="small"><b>CURRENT CHRON IS:</b> Scheduler &#9744; <i>(substrate, not owned)</i> · Relevance Engine &#9746; ·
Claim-State Engine &#9744; · Temporal Reconciliation Layer &#9744; · Learning System &#9744;.
<b>Two of five, and both of the two are the parts that do not require the loop to close.</b></p></div>
""")

# ── FINAL VERDICT ────────────────────────────────────────────────────────
A('<h2>FINAL VERDICT — five items only</h2>')

A("""
<div class="verdict">
<div class="n">1 · CURRENT REALITY</div>
<h3>A date store, a gate, and a card lane that has never fired.</h3>
<p>What is alive on this machine under the name CHRON: <b>5 canonically-sourced events</b> in one store; a
<b>spine gate</b> that executes clean and self-tests its own ability to reject (6 PASS · 0 FAIL · 3 UNBUILT); a
<b>relevance engine</b> (<span class="mono">chron.py</span>) that computes every countdown at render and expires what has passed;
and a <b>two-per-day card lane</b> with two rendered artifacts and <b>zero executions</b>.</p>
<p>What is alive around it and often mistaken for it: a 39-job scheduler (13 enabled), an RSI learning loop firing
every 6 hours, a daily attention closure at 23:45, a claim ledger holding 21 claims and 11 verifications, and a
briefing lane that produced a real PDF this morning. CHRON wrote the contract for the card; CHRON does not own the
scheduler that would run it, and nothing schedules CHRON's own scripts.</p>
<p><b>And one thing is definitively dead:</b> the world-model prediction stream — 792 rows, 5 distinct actions,
no outcome field, last write 22 days ago, no reader.</p>
</div>
""")

A("""
<div class="verdict">
<div class="n">2 · ACTIVE TASKS</div>
<h3>Seven carry a live trigger. Three are armed but never fired. Two are dormant code.</h3>
<p><b>Live and evidenced:</b> <span class="mono">docforge-edition-daily</span> (06:00 → ran 09:59 today) ·
<span class="mono">attention-closure</span> (23:45 → last 09-17) · <span class="mono">aaa-rsi-loop</span>
(every 6 h → 12:07 today) · <span class="mono">aaa-mesh-health</span> (03:17) · the root crontab loops
(metabolism 30 min, reality-pulse 15 min, cockpit probe 15 min, well intake 30 min, arifFlow digest 22:00) ·
systemd timers including <span class="mono">vault999-backup</span>, <span class="mono">triadic-snapshot</span>,
<span class="mono">arifos-reality</span>.</p>
<p><b>Armed, never executed:</b> the three ALPHA-ZEN jobs — 07:15 (missed by construction: created 10:02), 14:00
(next, in ~2 h), 21:15.</p>
<p><b>Dormant code with no trigger:</b> <span class="mono">chron.py</span> and <span class="mono">chron_spine_gate.py</span>
— both run correctly, both invoked only by hand or from inside another job's prompt text.</p>
</div>
""")

A("""
<div class="verdict">
<div class="n">3 · MISSING LOOPS</div>
<h3>Three, and they are the three that would let CHRON learn.</h3>
<p><b>L6 Outcome → Calibration</b> — nothing scores anything. No Brier, log-loss, or ECE artifact exists. The single
recorded failure (<span class="mono">REALITY_DISAGREED</span>, silent-count predicted 7, observed 6) produced no
calibration entry. <b>L8 Lesson → Policy</b> — 12 lessons sit unratified; no policy-candidate object exists, so there
is nothing a lesson could be promoted into. <b>L9 Policy → Attention</b> — attention is generated from
infrastructure gaps, never from an adopted policy; a change in what matters does not change what is looked at.</p>
<p>Two further arrow-level gaps sit behind these, both reported <span class="mono">UNBUILT</span> by CHRON's own gate:
<b>EXPERIENCE → MEMORY</b> (a collection exists with no payload schema) and <b>MEMORY → POLICY</b>.</p>
</div>
""")

A("""
<div class="verdict">
<div class="n">4 · HIGHEST DRIFT</div>
<h3>Three enabled jobs, a full pipeline, a named room — and zero receipts.</h3>
<p><b>D1, highest.</b> The ALPHA-ZEN contract is complete: gate that refuses, canonical clock, schema, audience rule,
memory boundary, delivery target, and two artifacts rendered by hand this morning. All three jobs read
<span class="mono">enabled: true · state: scheduled · last_run_at: null · completed: 0</span>, and all three were created
at 10:02 today — <b>after the 07:15 slot they were built for</b>. Nothing here is broken; nothing here has run.
The gap is a missing receipt, and the window to close it is today at 14:00.</p>
<p><b>D5, structural.</b> 35,743 execution receipts, <b>100 % without a trace_id</b>. The federation already named this
defect in doctrine; today it is measurable in the running system. Not a missing log — a missing causal join.</p>
<p><b>D3, silent.</b> A 792-row prediction stream that looks healthy by every surface check (valid JSONL, growing file,
distinct ids) and stopped writing 22 days ago, with no reader and no outcome field. Its shape is the warning:
artifacts that look fine while the thing behind them has ceased.</p>
<p class="small">Also open: D8 — the ALPHA-ZEN audit still lists four blockers that were repaired in code this morning
with no supersession recorded. The artifact that taught this lesson is now an example of it.</p>
</div>
""")

A("""
<div class="verdict">
<div class="n">5 · NEXT LOWEST-RISK WITNESS ACTION</div>
<h3>Witness the 14:00 fire — capture the receipt, not the intent.</h3>
<p><b>Action:</b> at 14:00 MYT today, read-only, record for the ALPHA-ZEN body-check job: (a)
<span class="mono">last_run_at</span> and <span class="mono">last_status</span> from
<span class="mono">jobs.json</span>; (b) the delivery row from <span class="mono">deliveries.db</span>; (c) any
artifact mtime/hash produced; (d) the Telegram <span class="mono">message_id</span> if the receipt carries one.
Then file the result as <b>DELIVERED / OBSERVED / ACKNOWLEDGED</b>, separately — never as one word.</p>
<p><b>Why this one:</b> zero mutation, zero new architecture, no F13 decision required, and it is the only step that
converts the single largest drift from <i>armed but unproven</i> into either a receipt or a named fault. It also closes
loop L1 with real evidence instead of a scheduled promise — and it directly answers the question Arif was asking this
morning about a PDF he could not find: <b>whether a scheduled lane produced anything at all, or only a schedule.</b></p>
<p class="small"><b>Named hazard for that run:</b> the two prior card renders happened by hand. If 14:00 produces a
message without a <span class="mono">message_id</span>, that is the same D5/D6 class already recorded against the
digest lane — channel proven, event unbound. Report it that way; do not read a delivery row as proof the room saw it.</p>
</div>
""")

A("""
<div class="box law"><h3>Standing constraints observed while writing this</h3>
<p><b>OBSERVE_ONLY:</b> no file outside this artifact's own directory was created or modified. <b>DECLARATION ≠ MECHANISM:</b>
every capability claim above is bound to a path that was opened or a command that was executed during this pass.
<b>WITNESS BEFORE MUTATION:</b> the eight drifts are recorded, not repaired — repair is a separate, authorised action.</p>
<p><b>Naming honesty:</b> this is a <b>Lane B RECEIPT</b>, not a SEAL. <span class="mono">seal_allowed=false</span> is
reported here from the day's own prior artifact, not re-probed by this seat; no judge hash, no witness, no
cryptographic actor binding is claimed. The word SEAL does not appear as a verdict anywhere in this document.</p></div>
""")

A("""
<div class="foot">
<b>CHRON::REALITY_MAPPER::v1</b> · Authority: ARIF (F13) · Mode: OBSERVE_ONLY / AUDIT · Render: 2026-09-18 12:11 MYT ·
Seat: HERMES (i-ARIF), KVM8 · Class: Lane B RECEIPT · Mutations: 0<br>
Probe set executed this pass: <span class="mono">jobs.json</span> (39 jobs) · <span class="mono">deliveries.db</span> ·
<span class="mono">systemctl list-timers</span> · <span class="mono">crontab -l</span> + <span class="mono">/etc/cron.d</span> ·
<span class="mono">claims.db</span> (4 tables) · <span class="mono">closure-ledger.jsonl</span> ·
<span class="mono">attention-ledger.jsonl</span> + snapshot · <span class="mono">rsi/state/*</span> (atoms, loop-ledger,
consequence, baselines) · <span class="mono">UNRATIFIED-LESSONS-LEDGER.jsonl</span> · <span class="mono">scars/</span> ·
<span class="mono">chron_events.json</span> · <span class="mono">cycles.jsonl</span> · <span class="mono">cards/</span> ·
<span class="mono">world-model-lite.jsonl</span> (792 rows parsed) · <span class="mono">arifflow_receipts.jsonl</span>
(35,743 rows parsed) · <span class="mono">chron_spine_gate.py</span> <b>executed</b> · Qdrant collection list ·
KVM4 <span class="mono">/health</span> + cron API.<br>
DITEMPA BUKAN DIBERI ⚒️
</div>
""")

A("</body></html>")

html = "\n".join(H)
(OUT / "chron-reality-map.html").write_text(html, encoding="utf-8")
HTML(string=html, base_url=str(OUT)).write_pdf(OUT / "CHRON-REALITY-MAP-2026-09-18.pdf",
                                               stylesheets=[CSS(string=CSS_TEXT)])
print("built:", OUT / "CHRON-REALITY-MAP-2026-09-18.pdf")
