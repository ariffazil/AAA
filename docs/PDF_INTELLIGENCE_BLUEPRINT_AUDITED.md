<!-- SOT-MANIFEST
owner: Wawa (Hermes, KVM2 flow-edge)
audit_of: "PDF Intelligence Blueprint for AAA Agents (v1, pasted by Arif 2026-10-02)"
last_verified: 2026-10-02
confidence: high
scope: node KVM2 (flow-edge, 100.64.0.4) + /root/azwaOS-workspace
-->

# PDF Intelligence Blueprint for AAA Agents — v2 (AUDITED)

> **Audit stamp:** Wawa, KVM2 `flow-edge` (100.64.0.4), 2026-10-02 08:29–08:40 MYT (+08).
> **Probe scope:** local filesystem of KVM2, `/root/.hermes/skills`, `/root/azwaOS-workspace`, `/opt/arifos`, plus the retired profile `/root/.hermes-asi.retired-20260902`.
> **Honest boundary:** anything about KVM8 / af-forge / remote organs was **not** probed from here and is marked unverified. Absence on KVM2 is not proof of fabrication elsewhere.
> **No source file for v1 exists on disk** (string-hunt for "Intelligence Blueprint" returned nothing) — v1 exists only as pasted text.

## 0. Verdict

- **Sections 1–2 (filesystem inventory, capability matrix, routing matrix) do not describe this node.** All 8 named skills, all 4 named binaries and all 4 named libraries are absent here; the tables' file counts, byte sizes, line counts, dates, versions and `abc123…` fingerprints carry no probed evidence. Treat them as **claims, not inventory**.
- **Sections 3, 4, 5, 7 survive the audit.** Evidence-surface doctrine, the provenance envelope, prompt-injection discipline, the 5s/30s/2min contract and uncertainty encoding are sound and align with existing arifOS/azwaOS doctrine. Keep them.
- **Sections 6 and 8 target things that do not exist here.** The snippets need `weasyprint`, `reportlab`, `fitz` and `matplotlib` (none installed in system Python); the plan targets `hermes_claim_validate`, `tools_sot.yaml`, a CHRON organ and a "122 tools vs 32 executors" delta — none of which were found.
- **Good news:** the core hard target of the blueprint — a **render-verify gate** — is *already executable on this node today*. It was executed during this audit and the receipts are in §4.

## 1. Claim vs reality (2026-10-02 08:35 MYT)

| Perkara | What v1 said | Reality on KVM2 at 2026-10-02 08:35 MYT |
|---|---|---|
| Skill root | `/opt/arifOS/forge/skills`, `/opt/arifOS/hermes/skills` | Both **MISSING**. Real dir is `/opt/arifos` (lowercase) and it contains **no `skills/` at all** — it holds `organs/{hermes,geox,wealth,well}`, `forge/`, `law/`, `witness/`, `receipts/`, `artifacts/`. |
| 8 PDF skills | `pdf-text-extraction`, `ppt-to-pdf`, `image-to-pdf`, `chart-generator`, `pdf-summarization`, `pdf-metadata`, `pdf-table-extract`, `pdf-signature` | **0/8 exist.** Whole-filesystem basename hunt: all eight `NOT FOUND ANYWHERE`. Three names (`ppt-to-pdf`, `image-to-pdf`, `chart-generator`) appear only as catalogue strings in a **retired** profile's hub index-cache — downloadable-catalogue entries, not installs. |
| Real PDF skills on node | (not mentioned) | `skills/productivity/pdf-author`, `skills/productivity/pdf-deliverables`, `skills/productivity/ocr-and-documents`, `skills/data-science/pdf-extraction`, `skills/creative/civic-briefing-pdf`, `skills/.archive/nano-pdf`. Node total: **230** `SKILL.md`. |
| Inventory table | 15/10/8/12/11/9/14 files, 5KB/3KB/…, 220/150/… lines, dated 2026-06-15 → 2026-08-05 | **Unprobeable.** No such paths exist, so no file count or size can be true. Row values are decoration. |
| Fingerprints | `abc123…`, `def456…`, `jkl012…` | Placeholder strings, not hashes. No file to hash. |
| Versions | PyMuPDF 1.23.4, reportlab 3.8.1, weasyprint 62.0, pandoc 3.1.1 | PyMuPDF **1.28.2** (not 1.23.4) and only inside the Hermes venv. reportlab / weasyprint / pandoc: **not installed / not found**. |
| `PROVEN: chart-generator` — "rendered a live XAUUSD chart into PDF" | Yes, page 6 | `matplotlib` and `pandas` are **not installed**. XAUUSD chart templates exist only under `/root/.hermes-asi.retired-20260902/skills/trading/…` — a profile retired **2026-09-02**. Anachronistic, not evidence of current capability. |
| Binaries | pandoc, pdftoppm, pdftotext, ghostscript | `pdftoppm` ✅ `/usr/bin/pdftoppm`, `pdftotext` ✅, `pdfinfo` ✅, `gs` ❌ NOT FOUND, `pandoc` ❌ NOT FOUND, `soffice` ❌ NOT FOUND, `xelatex` ❌ NOT FOUND. |
| CHRON organ (stage 6) | "CHRON Timestamp & Validation" | No CHRON organ on this node. 164 `chron*` matches are all **chrony** (the NTP daemon): `/etc/chrony`, `/var/lib/chrony`, dpkg files. |
| Registry | `tools_sot.yaml`; reconcile "122 tools vs 32 executors" | No `tools_sot.yaml` anywhere. The string `tools_sot` appears only inside the A-FORGE bootstrap TS source and retired state DBs. Real registries live at `/root/azwaOS-workspace/aaa_src/registries/{tools,skills,agents,hosts,servers}.yaml` — and **none contains a PDF entry**. |
| Docling / LayoutLMv3 | "modern systems treat a PDF as joint image+text+layout" | Zero traces of `docling` or `layoutlm` on disk. Fine as **literature citation**, wrong as **capability statement**. |
| Prompt injection / untrusted-data stance | OWASP "almost any source of data can be an injection vector" | **Correct and load-bearing.** Keep verbatim. |
| 5s / 30s / 2min + Mayer principles | cover → metrics+visual → evidence chain | **Sound.** No correction needed. |
| Provenance envelope fields | source_sha256, page, bbox, element_id, method, confidence, as_of, unit, supersession, tool_id, tool_version, data_hash, chart_hash | **Sound design.** Correct field list; it just had no implementation behind it. |

## 2. Corrected inventory — what PDF capability actually exists here

Verified 2026-10-02 by import/execute, not by reading a manifest.

| Capability | Handle (absolute path) | Version | State | Evidence |
|---|---|---|---|---|
| PyMuPDF (text, render, split/merge, pixmap) | `/usr/local/lib/hermes-agent/venv/bin/python3` (Py 3.11.15) | **1.28.2** | **EXECUTED** | extracted 18-page PDF, page-0 text returned |
| fpdf2 (authoring) | same venv | **2.8.8** | **EXECUTED** | created `/tmp/rv-created.pdf`, 1 page, A4, sha256 `eb5ff619…6b11` |
| pdfplumber (text + tables) | `/usr/bin/python3` (3.14.4) | **0.11.10** | **EXECUTED** | read 18 pages, page-0 text 120 chars, 0 tables on p0 |
| pdfminer.six | `/usr/bin/python3` | **20260107** | LOADABLE | import OK |
| pypdfium2 (render alt) | `/usr/bin/python3` | **5.12.1** | LOADABLE | import OK |
| Pillow | both interpreters | 12.3.0 | LOADABLE | import OK |
| Poppler CLI | `/usr/bin/pdftoppm`, `/usr/bin/pdftotext`, `/usr/bin/pdfinfo` | — | **EXECUTED** | rendered 2 PNGs + read metadata |
| Tesseract (OCR) | `/usr/bin/tesseract` | — | PRESENT | on PATH; `pytesseract` binding **not** installed |
| Disk headroom for marker-pdf (~5 GB) | `/` | — | — | 61 GB free (38% used) — marker-pdf is *installable* if OCR-grade extraction is ever needed |

**Absent on this node** (do not write snippets that assume them): `reportlab`, `weasyprint`, `matplotlib`, `pandas`, `pypdf`/`PyPDF2`, `panflute`, `docling`, `tabula-py`, `camelot`, `ocrmypdf`; binaries `pandoc`, `ghostscript`/`gs`, `soffice`, `xelatex`.

> Consequence: the **Markdown→PDF (pandoc/xelatex)** and **HTML→PDF (weasyprint)** routes in v1 §6 do not exist here. The real authoring route is **fpdf2**. The real verification route is **poppler + PyMuPDF**.

## 3. Two stacks, one node — the split that must be stated

There is one trap worth writing down permanently: **the PDF libraries are split across two interpreters.**

- **Hermes venv** (`/usr/local/lib/hermes-agent/venv/bin/python3`, 3.11.15): `pymupdf`, `fpdf2`.
- **System python3** (3.14.4): `pdfplumber`, `pdfminer.six`, `pypdfium2`, `fpdf`.

Running the documented `python scripts/extract_pymupdf.py file.pdf` as written **fails** with `ModuleNotFoundError: No module named 'pymupdf'` — reproduced during this audit. The `ocr-and-documents` skill was patched with the venv path as a result. Any pipeline must name its interpreter explicitly.

## 4. The render-verify gate — executed, with real receipts

This is the v1 §8 item 2 gate. It is not a proposal; it ran today.

```bash
F=/root/The-Craft-of-Readable-PDFs.pdf
pdftoppm -png -r 60 -f 1 -l 2 "$F" /tmp/rv-page     # render
pdfinfo "$F"                                        # page count / metadata
pdftotext -layout "$F" -                            # text channel
sha256sum "$F" /tmp/rv-page-*.png                   # hashes
```

**Observed output (verbatim):**

```
source   /root/The-Craft-of-Readable-PDFs.pdf   87,938 B
         sha256 8a51fb5002202dfc1d8c2bebac05c05afe1a3e8cb4b6a8c7da4e8a655cd9e479
         pages 18 | A4 595.28x841.89pt | Tagged: no | JavaScript: no
render   /tmp/rv-page-01.png  sha256 6736c25b6f64ba53e76c0290c07a58f1a932872d7d79b77a50fa2ea0cdc0b76b
         /tmp/rv-page-02.png  sha256 9a767e86d56cda6e55ee64d33019a2cbed9cee33c27077ad057fb4da18e7657d
create   /tmp/rv-created.pdf  sha256 eb5ff6190b7806854495df76a5e363fd148ebec6cac5003ade69936ac14e6b11
         pdfinfo Pages: 1 | pdftotext round-trip matched the input string
```

Two verification channels stay separate, per the existing `pdf-deliverables` doctrine: **`pdftotext` for TEXT**, **vision pass on the rendered PNG for LAYOUT** (overlap, clipping, off-page slivers, missing glyphs). `pdfinfo` catches page-count pathology — historically the one silent failure that produced a 331-page document instead of a 6-page guide.

## 5. Corrected implementation plan (hardening that actually exists)

1. **Make the render-verify gate mandatory, today.** It already works (§4). Wire it into `skills/productivity/pdf-deliverables` + `pdf-author` as a non-skippable pre-delivery step: render → `pdfinfo` page count → `pdftotext` sanity → vision pass → record `source_sha256` + page hashes in the delivered message. **Cost: ~1 day. Risk removed: shipping a broken/invisible artifact.**
2. **Fix the interpreter split, not the fiction.** Every PDF snippet in any doctrine file must name `/usr/local/lib/hermes-agent/venv/bin/python3` or `/usr/bin/python3` explicitly (§3). `ocr-and-documents` patched 2026-10-02.
3. **Provenance fields — attach them to the artifact that exists.** The envelope in v1 §4 is a good schema; its real home is the **fpdf2 authoring path in `pdf-author`/`pdf-deliverables`**, not a non-existent `hermes_claim_validate`. Minimum viable: `source_sha256`, `page`, `bbox`, `extraction_method`, `tool_id`, `exec_timestamp`, `data_hash` on any claim sourced from a PDF.
4. **Registry truth.** If PDF tools should be discoverable by agents, the file to edit is `/root/azwaOS-workspace/aaa_src/registries/tools.yaml` (verified: currently **no PDF entry**). `tools_sot.yaml` does not exist — drop the reference rather than "auditing" it.
5. **Delete, don't repair, the fabricated rows.** §1's tables cannot be fixed by editing numbers; they must be re-derived from a real probe (this document) or removed. A document that stakes its credibility on provenance while carrying unprovenanced inventories is self-refuting.
6. **OCR is available but unbound.** `tesseract` is on PATH and 61 GB is free, so scanned PDFs are *solvable* — but there is no Python binding installed, and marker-pdf is not installed. Decide: bind `pytesseract` (cheap) or keep OCR out of scope honestly.

## 6. Gaps this document still carries

- No Markdown/HTML → PDF route on this node (needs `pandoc` or `weasyprint` — neither installed). Authoring is fpdf2-only.
- No PDF signature verification (`pdf-signature` never existed; `pdfsig` from poppler was not checked).
- Bbox provenance requires a layout extractor. PyMuPDF `get_text("dict")` gives per-span bboxes and is available; no Docling-class layout model is installed.
- Nothing here was validated against KVM8/af-forge or any remote organ. If the blueprint was authored *for the federation*, its inventory must be re-probed on the node that owns those paths.

## 7. Decision boundary (Arif only)

1. Is this blueprint meant to be **KVM2-node-specific** or a **federation-wide spec**? If federation-wide, the inventory must be re-probed where the paths are claimed to live.
2. Do PDF capabilities get **registered** in `aaa_src/registries/tools.yaml` (making them agent-discoverable), or stay as Hermes skills?
3. Ship the corrected version to whoever authored v1 — **with the probe boundary stated**, so "not found on KVM2" is not read as "fabricated by the author".

---

*Audited by Wawa, KVM2 flow-edge. Receipts-not-stories: every state above comes from an executed command, not from a manifest. DITEMPA BUKAN DIBERI.*
