# MEMORY UPDATE — 17 September 2026
> **For:** Arif (F13) · **By:** Hermes (KVM8) · **Scope:** helix · mem0 · reality graph · canon drift
> **Status:** PARTIAL — one write blocked at a constitutional gate, correctly

---

## 1 · What was written

| Layer | Target | Action | Status |
|---|---|---|---|
| **H2-experience** | `/root/memory/H2-experience/2026-09/2026-09-17-petronas-reality-and-exit-architecture.md` | NEW — full session episode | ✅ WRITTEN |
| **H2 index** | `/root/memory/H2-experience/2026-09/` | NEW month directory created | ✅ CREATED |
| **carry-forward** | `/root/HERMES/carry_forward.json` | 7 open loops appended (114 entries, 21 open) | ✅ WRITTEN |
| **forge_work** | `2026-09-17/REALITY-CAPTURE-2026-09-17.md` | session capture, 10 sections | ✅ WRITTEN |
| **canon drift log** | `/root/AAA/canon/PETRONAS/drift_witness.jsonl` | append 5 drift checks | ⛔ **BLOCKED_AT_GATE** |

---

## 2 · BLOCKED_AT_GATE — exact blocked operation

**Target:** `/root/AAA/canon/PETRONAS/drift_witness.jsonl`

**Operation attempted:** append 5 JSON lines recording today's drift checks.

**Result:** `Operation not permitted` — the write was refused by the filesystem.

**Verified cause:** the PETRONAS canon directory and every file inside it carry
the immutable attribute:

```
----i---------e-------  /root/AAA/canon/PETRONAS/
----i---------e-------  /root/AAA/canon/PETRONAS/ATLAS.md
----i---------e-------  /root/AAA/canon/PETRONAS/KNOWLEDGE_GRAPH.json
----i---------e-------  /root/AAA/canon/PETRONAS/qdrant_backup_*.json
```

**Assessment:** this is the F13 sovereign lock functioning as designed. Canon
cannot be amended by an agent — not even to append an audit line. Lifting that
attribute is an F13 act; an agent that attempts it, or documents the exact
command to do so, is performing an unauthorised mutation attempt.

**Note:** the K-02 gate independently blocked an attempt to write the lifting
command into this document. That block was correct. The gate is doing its job.

**Consequence:** PETRONAS canon drift must be reported to Arif, never written
into canon. The five checks are therefore recorded in section 6 below and must
be applied by a human hand under F13 authority.

**F13 only — to authorise:** lift the immutable attribute on the directory and
the file, append the checks recorded in section 6, then restore the attribute.
This is an F13 decision about canon custody, not a maintenance task.

---

## 3 · Qdrant substrate — live state (probed 2026-09-17)

### Collection topology: 19 live (was 17 on 2026-09-12)

| Collection | Points | Delta | Note |
|---|---|---|---|
| `mem0` | **14,507** | **+3,403** | Hermes-private lane. Growing as designed. |
| `mem0-v4` | **5** | **NEW** | 1024d + bm25 sparse. Not in routing matrix. |
| `mcp_capabilities` | **0** | **NEW** | EMPTY. No producer found. |
| `arifos_memory` | 40 | −59 | Federation-shared. Shrank. |
| `petronas_knowledge` | 85 | **−1,375** | **EXPLAINED — section 4** |
| `arifos_precedent` | 257 | +2 | Stable |
| `atlas333_eureka` | 74 | 0 | Stable |
| `federation_memory_patterns` | 208 | +105 | Doubled |

---

## 4 · The petronas_knowledge drop is NOT a loss — probe-before-panic record

**Observed:** 1,460 points (2026-09-12) → **85 points** today. A 94% drop.

**First read (WRONG):** silent corpus loss.

**Verified read (CORRECT):** intentional refresh, F13 authorised 2026-09-12.

Evidence chain:
1. `refresh_s3.py` at `/root/AAA/canon/PETRONAS/` — its docstring states it backs
   up, re-embeds canonical content via bge-m3, then deletes and recreates the
   collection before upserting curated points.
2. Backup present and intact: `qdrant_backup_20260911T233408Z.json` declares
   `count: 1460`; parse confirms 1,460 points.
3. `drift_witness.jsonl` **line 16** (2026-09-11T23:40:04Z):
   `{"check": "qdrant_freshness", "status": "OK", "detail": "OK: 85 points, no stale revenue anchor in sample"}`

**Verdict:** 1,460 mixed and stale vectors were replaced by 85 curated canonical
ones. Collection status `green`, `optimizer_status: ok`. No fault.

**This is the second time this session that a healthy-looking system was nearly
misreported as broken.** The discipline held: probe the mechanism before
declaring loss.

---

## 5 · The real finding — petronas_knowledge is one cycle STALE

The 85 canonical vectors were embedded **2026-09-12**.

They therefore do **not** carry:

| Missing | Correct value | Found |
|---|---|---|
| Brent 1H2025 | **USD71.87** (not 76.89 — that is JCC) | 2026-09-17 |
| Upstream capital | **RM9.0b (21.7%)** — not 8.7b | 2026-09-17 |
| Downstream capital | **RM26.0b** | 2026-09-17 |
| Net cash movement | per the cash-flow statement, not the balance difference | 2026-09-17 |
| Target vs outturn | 10% announced vs 6% realised | 2026-09-17 |
| 1H2026 result set | released 28 Aug 2026 — after the refresh | — |

**RE-EMBED REQUIRED** before `petronas_knowledge` is used as a decision surface
again. The pipeline is ready; it needs a run with current anchors.

---

## 6 · DRIFT CHECKS PENDING CANON (F13 to apply)

```json
{"ts": "2026-09-17T16:40:00Z", "check": "qdrant_collection_topology", "status": "DRIFT", "detail": "19 collections live (was 17 on 2026-09-12). NEW: mem0-v4 (5 pts, 1024d plus bm25 sparse), mcp_capabilities (0 pts, EMPTY). Routing matrix needs 2 new rows."}
{"ts": "2026-09-17T16:40:00Z", "check": "petronas_knowledge_count", "status": "OK-EXPLAINED", "detail": "85 pts vs backup 1460 pts. NOT a loss: refresh_s3.py (F13 authorised 2026-09-12) deleted and recreated the collection. Drift log line 16 confirms OK 85 points. Backup intact."}
{"ts": "2026-09-17T16:40:00Z", "check": "petronas_knowledge_freshness", "status": "STALE", "detail": "Canonical vectors embedded 2026-09-12, BEFORE the 1H2026 full result set and BEFORE the 2026-09-17 numeric audit. Missing: corrected Brent, corrected upstream, corrected downstream, target-vs-outturn gap. RE-EMBED REQUIRED."}
{"ts": "2026-09-17T16:40:00Z", "check": "atlas_label_conflict", "status": "DRIFT", "detail": "00_QUANTITATIVE.md line 14 gives one PAT-ex-PRefChem figure; the same file's reconciliation at lines 78-80 implies a materially different one. Both cannot hold. ATLAS presents the lower figure as REALITY opposing a PROPAGANDA headline. Possible sign inversion. Mark CONTESTED; do not cite."}
{"ts": "2026-09-17T16:40:00Z", "check": "mem0_growth", "status": "OK", "detail": "mem0 14507 pts, up 3403 since 2026-09-12. Hermes-private lane growing as designed. arifos_memory 40 pts, down from 99."}
```

---

## 7 · DRIFT — label conflict inside our own records

Two mutually exclusive figures both live in `00_QUANTITATIVE.md`:

```
line 14    : PAT excluding the JV item        one figure (-73.3% YoY)
line 78-80 : operating 42.0
             less recognition 15.2
             tax and minorities 0.4
             = reported 27.2
             => excluding the item would be ~42, not the line-14 figure
```

Both cannot be true. ATLAS presents the line-14 figure as **REALITY**, opposing a
**PROPAGANDA** headline — i.e. as evidence of concealment.

**Hypothesis:** the sign may be inverted. The report states that figure in the
sentence that *excludes* the one-off item — which would make it the **cleaner**
number, not the worse one. If so, an explanation has been read as a concealment,
and the finding has been pointed the wrong way.

**Status: CONTESTED.** Do not cite. Do not promote. Verify against the primary
1H2026 financial report before any external use.

This matters because it already sits in ATLAS, in the public vitals surface, and
potentially in published articles.

---

## 8 · Helix state after this update

| Axis | Layer | Status |
|---|---|---|
| **H** | H1 capture | active — but **only a 2026-08 directory exists (2026-09 gap)** |
| **H** | **H2 experience** | **✅ 2026-09 created, 1 episode** |
| **H** | H3 knowledge | unchanged |
| **H** | H4 identity | unchanged |
| **H** | H5 scars | 24 SEAL — **candidate new scar (section 9)** |
| **H** | H6 constitution | unchanged |
| **P** | ARIF person-card | exists, last touched 2026-09-16 |
| **L** | L3 Qdrant | 19 collections, 2 new, 1 stale |
| **L** | L6 VAULT999 | unchanged — nothing sealed (correct: nothing was decided) |

### H1 gap flagged
`/root/memory/H1-capture/` holds only a `2026-08/` directory. Two weeks of
September passed with no fast-inbox capture. Either capture stopped, or it is
routing elsewhere. Worth a look.

---

## 9 · Scar candidate — The Void Pattern

**Definition:** a system that reports itself healthy while its capacity to
correct has been removed. The failure is never the visible error — it is the
removal of the channel that would have caught it.

Evidence instances observed in one session:

1. **HERMES MCP** — dead for hours; the surfaced error named a missing Python
   module; the true cause was a broken interpreter symlink. Five sibling
   services answered health checks from deleted file handles and would have died
   on any restart.
2. **petronas_knowledge** — a 94% point drop that looked like loss and was a
   refresh. A near-miss in the opposite direction: healthy read as broken.
3. **Desired Behaviours** — two self-correction mechanisms removed from the
   cultural rubric; the replacement presumes the frame is correct.
4. **WELL** — reports human state but cannot measure it; the number is
   self-reported and the organ says so honestly. The channel exists and is
   labelled.

**Proposed:** register under H5, floors F2 · F7 · F11 · F13.
Awaiting F13.

---

## 10 · Actions for next session

1. **Re-embed `petronas_knowledge`** with current anchors (pipeline ready).
2. **Resolve the PAT label conflict** against the primary 1H2026 report. Mark
   ATLAS CONTESTED until resolved.
3. **Add two rows to the routing matrix**: `mem0-v4`, `mcp_capabilities`.
4. **Investigate `mcp_capabilities`** — zero points, no producer identified.
5. **Investigate the `arifos_memory` shrink** (99 → 40).
6. **Apply the five drift checks to canon** — requires F13 authority (section 2).
7. **Check the H1 capture gap** (nothing for 2026-09).
8. **Decide the scar** — The Void Pattern (section 9).

---

*ΔS ≤ 0. Nothing was decided this session. Nothing should have been sealed.*
*DITEMPA BUKAN DIBERI*
