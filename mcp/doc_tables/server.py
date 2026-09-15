#!/opt/arifos/venv/bin/python
"""
doc-tables-mcp — TABLES-AS-STRUCTURE extractor + total reconciler for the arifOS federation.

WHY THIS EXISTS
---------------
Linear text extraction (pdftotext -layout, naive page.extract_text()) destroys table
geometry: cells get flattened, columns interleave, and numbers are re-associated with
the wrong row labels. That failure already put a wrong number into a published brief.

This organ NEVER returns a table as prose. A table is returned as a 2-D cell matrix
with page + bbox provenance, and every extracted total can be reconcilied against the
total that is actually printed in the source.

DOCTRINE
--------
- Structure over text: cells, not sentences.
- Witness over projection: bbox + page + strategy are recorded, so any number is traceable.
- Void Guard: a table with no printed total returns verdict UNRECONCILED — never "pass".
- Capability != Authority: READ_ONLY. This organ parses documents; it never mutates them.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import io
import os
import re
import tempfile
import urllib.request
from typing import Any

from fastmcp import FastMCP

SERVER_NAME = "doc-tables-mcp"
SERVER_VERSION = "2026.09.15"
DEFAULT_PORT = 38500
CACHE_DIR = "/tmp/doc_tables_cache"

mcp = FastMCP(
    name=SERVER_NAME,
    version=SERVER_VERSION,
    instructions=(
        "doc-tables-mcp — extract TABLES from PDF/HTML as structured JSON (cell matrices), "
        "never mangled text, and reconcile an extracted total against the printed total. "
        "Authority: READ_ONLY. Use this instead of pdftotext/page.extract_text() whenever a "
        "number must be read out of a table."
    ),
)

# --------------------------------------------------------------------------------------
# Source resolution
# --------------------------------------------------------------------------------------

_UA = {"User-Agent": "doc-tables-mcp/2026.09.15 (+arifOS federation)"}


def _resolve_source(source: str) -> tuple[str, bool]:
    """Return (local_path, is_temp). Downloads http(s) sources into CACHE_DIR."""
    if source.startswith(("http://", "https://")):
        os.makedirs(CACHE_DIR, exist_ok=True)
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", source.rsplit("/", 1)[-1])[:120] or "download.bin"
        dest = os.path.join(CACHE_DIR, name)
        if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
            req = urllib.request.Request(source, headers=_UA)
            with urllib.request.urlopen(req, timeout=90) as resp, open(dest, "wb") as fh:
                fh.write(resp.read())
        return dest, True
    path = os.path.abspath(os.path.expanduser(source))
    if not os.path.exists(path):
        raise FileNotFoundError(f"source not found: {path}")
    return path, False


def _as_range(page_range: Any) -> tuple[int, int] | None:
    """Coerce an MCP list[int] into a (start, end) inclusive tuple."""
    if not page_range:
        return None
    if len(page_range) == 1:
        return (int(page_range[0]), int(page_range[0]))
    return (int(page_range[0]), int(page_range[1]))


def _is_html(path: str) -> bool:
    if path.lower().endswith((".html", ".htm", ".xhtml")):
        return True
    try:
        with open(path, "rb") as fh:
            head = fh.read(2048).lstrip().lower()
        return head.startswith(b"<!doctype html") or head.startswith(b"<html")
    except OSError:
        return False


# --------------------------------------------------------------------------------------
# Numeric parsing — the numbers a table actually asserts
# --------------------------------------------------------------------------------------

_NUM_RE = re.compile(r"\(?\s*-?\d[\d,]*(?:\.\d+)?\s*%?\s*\)?")
_PURE_RE = re.compile(r"^\s*\(?\s*(-?\d[\d,]*(?:\.\d+)?)\s*(%?)\s*\)?\s*$")


def parse_cell_number(cell: Any, mode: str = "last") -> float | None:
    """Pull a numeric value out of a cell.

    mode='last'  -> the LAST numeric literal (== the computed result of a worked example
                    like '440,000 x 50% = 220,000' -> 220000). Default and safest.
    mode='first' -> the FIRST numeric literal.
    mode='only'  -> only if the cell is purely a number (no surrounding prose).

    Accounting negatives in parentheses are honoured. Thousands separators removed.
    Percent signs are stripped but the value is NOT divided by 100 (tables state 70% = 70).
    """
    if cell is None:
        return None
    s = str(cell).replace("\u00a0", " ").replace("\u2212", "-").strip()
    if not s:
        return None
    if mode == "only":
        m = _PURE_RE.match(s)
        if not m:
            return None
        v = float(m.group(1).replace(",", ""))
        return -v if s.strip().startswith("(") and s.strip().endswith(")") else v
    hits = _NUM_RE.findall(s)
    if not hits:
        return None
    raw = hits[0] if mode == "first" else hits[-1]
    m = re.search(r"-?\d[\d,]*(?:\.\d+)?", raw)
    if not m:
        return None
    v = float(m.group(0).replace(",", ""))
    # Accounting negative ONLY when the entire cell is wrapped in parens, e.g. "(1,234)".
    # A label like "Capital requirement (8%)" is NOT a negative eight.
    whole_paren = s.startswith("(") and s.endswith(")")
    neg = whole_paren and raw.strip().startswith("(") and raw.strip().endswith(")")
    if neg or raw.strip().startswith("-"):
        v = -abs(v)
    return v


def all_cell_numbers(cell: Any) -> list[float]:
    if cell is None:
        return []
    out = []
    for raw in _NUM_RE.findall(str(cell)):
        m = re.search(r"-?\d[\d,]*(?:\.\d+)?", raw)
        if m:
            out.append(float(m.group(0).replace(",", "")))
    return out


def _is_numeric_cell(cell: Any) -> bool:
    return parse_cell_number(cell, "only") is not None


def _digit_density(cell: str) -> float:
    """Fraction of a cell's characters that are digits.

    Separates a LABEL column (prose, ~0.00-0.05) from a VALUE column, including worked
    examples whose cells are expressions rather than pure numbers (~0.45-0.60).
    """
    if not cell:
        return 0.0
    return sum(ch.isdigit() for ch in cell) / max(1, len(cell))


# --------------------------------------------------------------------------------------
# Table object model
# --------------------------------------------------------------------------------------


def _rows_to_matrix(rows: list[list[Any]]) -> list[list[str]]:
    """Normalise a raw extracted table into a rectangular string matrix."""
    width = max((len(r) for r in rows), default=0)
    mat: list[list[str]] = []
    for r in rows:
        cells = []
        for c in r:
            if c is None:
                cells.append("")
            else:
                # collapse internal newlines: a cell is one logical value
                cells.append(re.sub(r"\s*\n\s*", " ", str(c).replace("\u00a0", " ")).strip())
        cells += [""] * (width - len(cells))
        mat.append(cells)
    return mat


def _grid_widths(mat: list[list[str]]) -> tuple[int, int]:
    if not mat:
        return 0, 0
    return len(mat), max((len(r) for r in mat), default=0)


def score_matrix(mat: list[list[str]]) -> float:
    """Score how likely a candidate table is a REAL table.

    Real tables: many non-empty cells, several numeric cells, consistent grid.
    False positives: page headers/footers (1 row), prose blobs (1 huge ragged row).
    """
    rows, cols = _grid_widths(mat)
    if rows < 2 or cols < 2:
        return float("-inf")
    nonempty = sum(1 for r in mat for c in r if c)
    if nonempty < 4:
        return float("-inf")
    numeric = sum(1 for r in mat for c in r if _is_numeric_cell(c))
    prose = sum(1 for r in mat for c in r if len(c) > 140 or len(c.split()) > 22)
    # A candidate whose cells are mostly prose paragraphs is flowing text, not a table.
    if prose / max(1, nonempty) > 0.40:
        return float("-inf")
    # Ragged rows are a WEAK signal: real tables with merged/spanned cells are legitimately
    # ragged, so this must not bury them. Fully-empty rows are noise and are penalised.
    ragged = sum(1 for r in mat if 0 < sum(1 for c in r if c) < max(1, cols // 2))
    empty_rows = sum(1 for r in mat if not any(c for c in r))
    return (
        nonempty * 1.0
        + numeric * 2.0
        + rows * 0.35
        + cols * 0.4
        - prose * 6.0
        - ragged * 0.8
        - empty_rows * 1.2
    )


def _caption_above(page, bbox: tuple[float, float, float, float], max_lines: int = 3) -> str:
    """Nearest non-empty text line above the table bbox — the usual table caption."""
    try:
        x0, top, x1, _bottom = bbox
        crop = page.crop((max(0, x0 - 40), max(0, top - 60), min(page.width, x1 + 40), top))
        txt = (crop.extract_text() or "").strip()
    except Exception:
        return ""
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    if not lines:
        return ""
    # strip the recurring BNM running header
    lines = [
        ln
        for ln in lines
        if not re.search(r"(UNIFIED|Islamic Banking and|Capital Adequacy Framework|Page\s*\d+|\d+\s*/\s*\d+)", ln)
    ]
    return " ".join(lines[-max_lines:])[:200]


def _header_rows(mat: list[list[str]], limit: int = 3) -> int:
    """Leading rows that contain no pure numbers => header block."""
    n = 0
    for r in mat[:limit]:
        filled = [c for c in r if c]
        if filled and not any(_is_numeric_cell(c) for c in filled):
            n += 1
        else:
            break
    return n


def table_to_markdown(mat: list[list[str]], header_rows: int | None = None) -> str:
    """Render a cell matrix as GitHub markdown. Pipes escaped, newlines as <br>."""
    rows, cols = _grid_widths(mat)
    if not rows or not cols:
        return ""
    if header_rows is None:
        header_rows = _header_rows(mat)
    header_rows = max(1, min(header_rows, rows))

    def esc(c: str) -> str:
        return c.replace("|", "\\|")

    out: list[str] = []
    for idx in range(header_rows):
        out.append("| " + " | ".join(esc(c) for c in mat[idx]) + " |")
    out.append("| " + " | ".join(["---"] * cols) + " |")
    for r in mat[header_rows:]:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


def _contains_ratio(a, b) -> float:
    """Intersection area divided by the SMALLER box area (0.0-1.0).

    Unlike IoU this is stable when one candidate is a wide page-spanning blob and the
    other is a small genuine table nested inside it.
    """
    if not a or not b:
        return 0.0
    ix0, iy0 = max(a[0], b[0]), max(a[1], b[1])
    ix1, iy1 = min(a[2], b[2]), min(a[3], b[3])
    if ix1 <= ix0 or iy1 <= iy0:
        return 0.0
    inter = (ix1 - ix0) * (iy1 - iy0)
    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    smaller = min(area_a, area_b)
    return inter / smaller if smaller > 0 else 0.0


def _pack(mat: list[list[str]], page_no: int | None, bbox, strategy: str, score: float,
          caption: str = "", source: str = "") -> dict[str, Any]:
    rows, cols = _grid_widths(mat)
    numeric_cells = sum(1 for r in mat for c in r if _is_numeric_cell(c))
    return {
        "page": page_no,
        "shape": {"rows": rows, "columns": cols, "numeric_cells": numeric_cells},
        "bbox": [round(v, 2) for v in bbox] if bbox else None,
        "strategy": strategy,
        "score": round(score, 2) if score != float("-inf") else None,
        "caption": caption or None,
        "header_rows": _header_rows(mat),
        "cells": mat,
        "markdown": table_to_markdown(mat),
        "source": source,
    }


# --------------------------------------------------------------------------------------
# PDF extraction
# --------------------------------------------------------------------------------------

# Lines-strategy (ruled tables) is authoritative when it fires; text-strategy is a
# fallback that splits words mid-token, so its candidates are down-weighted.
STRATEGY_WEIGHT: dict[str, float] = {
    "lines": 1.0,
    "lines_text": 0.78,
    "text_lines": 0.55,
    "text": 0.32,
    "html_dom": 1.0,
}

STRATEGIES: list[tuple[str, dict[str, Any]]] = [
    ("lines", {"vertical_strategy": "lines", "horizontal_strategy": "lines"}),
    ("lines_text", {"vertical_strategy": "lines", "horizontal_strategy": "text"}),
    ("text_lines", {"vertical_strategy": "text", "horizontal_strategy": "lines"}),
    ("text", {
        "vertical_strategy": "text",
        "horizontal_strategy": "text",
        "min_words_vertical": 3,
        "min_words_horizontal": 1,
    }),
]


def _extract_pdf_page(page, page_no: int, source: str, min_rows: int, min_cols: int,
                      strategies: list[tuple[str, dict[str, Any]]]) -> list[dict[str, Any]]:
    """Collect every candidate table on a page from every strategy, then arbitrate.

    Arbitration order matters and is the core of this organ's accuracy:
      1. RULED DOMINANCE - candidates found by the `lines` strategy are direct geometric
         evidence (visible rules). Any borderless `text` candidate overlapping one yields.
      2. REGION DEDUPE     - same physical region found twice: keep the higher score.
      3. SCORE RANK        - table_index 0 is the most table-like object on the page.

    NOTE: no candidate may be discarded before step 1. An early coarse dedupe here once
    evicted the true ruled table in favour of a higher-scoring prose blob, which is
    exactly the class of error this organ exists to prevent.
    """
    cands: list[dict[str, Any]] = []
    seen_exact: set[tuple] = set()
    for sname, settings in strategies:
        try:
            found = page.find_tables(table_settings=settings)
        except Exception:
            continue
        for t in found:
            try:
                bbox = tuple(t.bbox)
                raw = t.extract()
            except Exception:
                continue
            mat = _rows_to_matrix(raw)
            rows, cols = _grid_widths(mat)
            if rows < min_rows or cols < min_cols:
                continue
            sc = score_matrix(mat)
            if sc == float("-inf"):
                continue
            # NUMERIC-BACKBONE GUARD (borderless strategies only).
            # A page of narrative prose split on word gaps yields a candidate with dozens
            # of rows and almost no numbers ("This policy do | c | ument set | s out").
            # No real tabular data has that shape. Returning such a blob as a "table" is
            # precisely the mangling this organ exists to prevent, so it is refused
            # outright rather than ranked low. Small all-text tables (<15 rows) are kept.
            if sname != "lines":
                nonempty_cells = sum(1 for r in mat for c in r if c)
                numeric_cells = sum(1 for r in mat for c in r if _is_numeric_cell(c))
                density = numeric_cells / max(1, nonempty_cells)
                if rows >= 15 and density < 0.12:
                    continue
            sc *= STRATEGY_WEIGHT.get(sname, 0.5)
            exact = (sname, round(bbox[0], 1), round(bbox[1], 1), round(bbox[2], 1), round(bbox[3], 1))
            if exact in seen_exact:
                continue
            seen_exact.add(exact)
            cap = _caption_above(page, bbox)
            packed = _pack(mat, page_no, bbox, sname, sc, cap, source)
            packed["_score"] = sc
            cands.append(packed)

    if not cands:
        return []

    # 1. RULED DOMINANCE
    ruled = [c for c in cands if c["strategy"] == "lines"]
    if ruled:
        kept = []
        for c in cands:
            if c["strategy"] == "lines":
                kept.append(c)
            elif not any(_contains_ratio(c["bbox"], r["bbox"]) > 0.45 for r in ruled):
                kept.append(c)
        cands = kept

    # 2. REGION DEDUPE (highest score wins a physical region)
    kept = []
    for c in sorted(cands, key=lambda d: -d["_score"]):
        if any(_contains_ratio(c["bbox"], k["bbox"]) > 0.70 for k in kept):
            continue
        kept.append(c)

    # 3. SCORE RANK
    out = sorted(kept, key=lambda d: -d["_score"])
    for d in out:
        d.pop("_score", None)
    return out


def extract_from_pdf(path: str, page: int | None = None, page_range: tuple[int, int] | None = None,
                     min_rows: int = 2, min_cols: int = 2, limit: int = 50,
                     strategies: list[tuple[str, dict[str, Any]]] | None = None,
                     source_label: str = "") -> dict[str, Any]:
    import pdfplumber

    strategies = strategies or STRATEGIES
    tables: list[dict[str, Any]] = []
    with pdfplumber.open(path) as pdf:
        total_pages = len(pdf.pages)
        if page is not None:
            idxs = [page] if page >= 0 else [total_pages + page]
        elif page_range is not None:
            a, b = page_range
            idxs = list(range(max(0, a), min(total_pages - 1, b) + 1))
        else:
            idxs = list(range(total_pages))
        pages_scanned = 0
        for i in idxs:
            if not (0 <= i < total_pages):
                continue
            if len(tables) >= limit:
                break
            pages_scanned += 1
            got = _extract_pdf_page(pdf.pages[i], i, source_label or path, min_rows, min_cols, strategies)
            for g in got:
                if len(tables) >= limit:
                    break
                tables.append(g)
    return {
        "source": source_label or path,
        "format": "pdf",
        "total_pages": total_pages,
        "pages_scanned": pages_scanned,
        "table_count": len(tables),
        "truncated": len(tables) >= limit,
        "tables": tables,
    }


# --------------------------------------------------------------------------------------
# HTML extraction
# --------------------------------------------------------------------------------------


def extract_from_html(path: str, min_rows: int = 2, min_cols: int = 2, limit: int = 50,
                      source_label: str = "") -> dict[str, Any]:
    from lxml import html as LH

    with open(path, "rb") as fh:
        doc = LH.fromstring(fh.read())
    tables: list[dict[str, Any]] = []
    for ti, node in enumerate(doc.iter("table")):
        if len(tables) >= limit:
            break
        raw: list[list[str]] = []
        for tr in node.iter("tr"):
            cells = tr.xpath("./th|./td")
            if not cells:
                continue
            raw.append([
                re.sub(r"\s+", " ", " ".join(c.itertext())).strip() for c in cells
            ])
        if not raw:
            continue
        # fill-down rowspans so every row keeps its label (a classic silent-data-loss bug)
        mat = _rows_to_matrix(raw)
        rows, cols = _grid_widths(mat)
        if rows < min_rows or cols < min_cols:
            continue
        cap = ""
        for xp in ("preceding::caption[1]", "preceding::h1[1]", "preceding::h2[1]", "preceding::h3[1]"):
            got = node.xpath(xp)
            if got:
                cap = re.sub(r"\s+", " ", " ".join(got[0].itertext())).strip()[:200]
                break
        sc = score_matrix(mat)
        if sc == float("-inf"):
            continue
        tables.append(_pack(mat, None, None, "html_dom", sc, cap, source_label or path))
    return {
        "source": source_label or path,
        "format": "html",
        "total_pages": None,
        "pages_scanned": 1,
        "table_count": len(tables),
        "truncated": len(tables) >= limit,
        "tables": tables,
    }


def extract_any(source: str, page: int | None = None, page_range: tuple[int, int] | None = None,
                min_rows: int = 2, min_cols: int = 2, limit: int = 50) -> dict[str, Any]:
    path, _ = _resolve_source(source)
    if _is_html(path):
        return extract_from_html(path, min_rows, min_cols, limit, source)
    return extract_from_pdf(path, page, page_range, min_rows, min_cols, limit, None, source)


# --------------------------------------------------------------------------------------
# Reconciliation — extracted total vs printed total
# --------------------------------------------------------------------------------------


def _find_index(cells: list[str], pattern: str) -> int | None:
    rx = re.compile(pattern, re.I)
    for i, c in enumerate(cells):
        if c and rx.search(c):
            return i
    return None


def _tolerance_ok(delta: float, printed: float, abs_tol: float, rel_tol: float) -> bool:
    if abs(delta) <= abs_tol:
        return True
    if printed != 0 and abs(delta) / abs(printed) <= rel_tol:
        return True
    return printed == 0 and abs(delta) <= abs_tol


def reconcile_table(mat: list[list[str]], total_col_label: str = r"^total$",
                    total_row_label: str = r"\btotal\b", value_mode: str = "last",
                    abs_tolerance: float = 0.5, rel_tolerance: float = 0.005,
                    skip_row_label: str | None = r"\btotal\b") -> dict[str, Any]:
    """Reconcile a printed total against the components that should produce it.

    Two orientations are supported and auto-detected:

    A) TOTAL-COLUMN  — a column whose header matches total_col_label.
       For each data row: sum the other numeric cells in that row, compare to the
       total-column cell of that row.  (e.g. CCPRS + IPRS = Total)

    B) TOTAL-ROW     — the first cell of some row matches total_row_label.
       For each numeric column: sum the cells above the total row, compare to the
       total row's cell.  (e.g. 'Total exposures' at the foot of a column)
    """
    rows, cols = _grid_widths(mat)
    if rows < 2 or cols < 2:
        return {"verdict": "UNRECONCILED", "reason": "table too small to reconcile",
                "checks": [], "orientation": None}

    header_idx_end = max(1, _header_rows(mat))

    # --- Orientation A: total as a COLUMN -------------------------------------------
    tcol = None
    for h in range(header_idx_end):
        idx = _find_index(mat[h], total_col_label)
        if idx is not None:
            tcol = idx
            break
    if tcol is not None and cols >= 3:
        # A LABEL column holds no pure numbers at all across the data rows. Its text can
        # still contain digits (e.g. "Capital requirement (8%)") — summing those would
        # fabricate a delta, so label columns are excluded from the component set.
        data_rows = range(header_idx_end, rows)
        label_cols: set[int] = set()
        for c in range(cols):
            if c == tcol:
                continue
            cells = [mat[r][c] for r in data_rows if mat[r][c]]
            if not cells:
                continue
            mean_density = sum(_digit_density(x) for x in cells) / len(cells)
            if mean_density < 0.15:
                label_cols.add(c)
        checks = []
        for r in range(header_idx_end, rows):
            printed = parse_cell_number(mat[r][tcol], value_mode)
            if printed is None:
                continue
            comps = []
            for c in range(cols):
                if c == tcol or c in label_cols:
                    continue
                v = parse_cell_number(mat[r][c], value_mode)
                if v is not None:
                    comps.append({"column": c, "cell": mat[r][c][:120], "value": v})
            if not comps:
                continue
            computed = sum(x["value"] for x in comps)
            delta = computed - printed
            checks.append({
                "row": r,
                "row_label": mat[r][0][:150],
                "components": comps,
                "computed_total": round(computed, 6),
                "printed_total": printed,
                "delta": round(delta, 6),
                "rel_delta": round(abs(delta) / abs(printed), 8) if printed else None,
                "result": "PASS" if _tolerance_ok(delta, printed, abs_tolerance, rel_tolerance) else "FAIL",
            })
        if checks:
            fails = [c for c in checks if c["result"] == "FAIL"]
            return {
                "orientation": "total_column",
                "total_column_index": tcol,
                "label_columns_excluded": sorted(label_cols),
                "total_column_header": mat[0][tcol] or (mat[header_idx_end - 1][tcol] if header_idx_end else ""),
                "value_mode": value_mode,
                "abs_tolerance": abs_tolerance,
                "rel_tolerance": rel_tolerance,
                "checks": checks,
                "checks_run": len(checks),
                "checks_failed": len(fails),
                "verdict": "RECONCILED" if not fails else "MISMATCH",
            }

    # --- Orientation B: total as a ROW ----------------------------------------------
    trow = None
    for r in range(rows - 1, -1, -1):
        if mat[r] and mat[r][0] and re.search(total_row_label, mat[r][0], re.I):
            trow = r
            break
    if trow is not None and trow > 0:
        checks = []
        for c in range(cols):
            printed = parse_cell_number(mat[trow][c], value_mode)
            if printed is None:
                continue
            comps = []
            for r in range(header_idx_end, trow):
                if skip_row_label and mat[r][0] and re.search(skip_row_label, mat[r][0], re.I) and r != trow:
                    continue
                v = parse_cell_number(mat[r][c], value_mode)
                if v is not None:
                    comps.append({"row": r, "label": mat[r][0][:120], "value": v})
            if len(comps) < 2:
                continue
            computed = sum(x["value"] for x in comps)
            delta = computed - printed
            checks.append({
                "column": c,
                "column_header": mat[0][c][:80] if mat[0] and c < len(mat[0]) else "",
                "components": comps,
                "computed_total": round(computed, 6),
                "printed_total": printed,
                "delta": round(delta, 6),
                "rel_delta": round(abs(delta) / abs(printed), 8) if printed else None,
                "result": "PASS" if _tolerance_ok(delta, printed, abs_tolerance, rel_tolerance) else "FAIL",
            })
        if checks:
            fails = [c for c in checks if c["result"] == "FAIL"]
            return {
                "orientation": "total_row",
                "total_row_index": trow,
                "total_row_label": mat[trow][0],
                "value_mode": value_mode,
                "abs_tolerance": abs_tolerance,
                "rel_tolerance": rel_tolerance,
                "checks": checks,
                "checks_run": len(checks),
                "checks_failed": len(fails),
                "verdict": "RECONCILED" if not fails else "MISMATCH",
            }

    return {
        "orientation": None,
        "checks": [],
        "checks_run": 0,
        "checks_failed": 0,
        "verdict": "UNRECONCILED",
        "reason": (
            f"no total found (looked for total column header ~ /{total_col_label}/ "
            f"and total row label ~ /{total_row_label}/). "
            "UNRECONCILED is NOT a pass — a number from this table is not yet verified."
        ),
    }


# --------------------------------------------------------------------------------------
# Text-mangling guard — proves why prose extraction is banned for tables
# --------------------------------------------------------------------------------------


def text_mangle_report(page, source: str, page_no: int) -> dict[str, Any]:
    """Render the SAME page region two ways and diff the numbers.

    Left:  structured cells (this organ).
    Right: the pdftotext -layout style prose rendering of that table's OWN bbox.

    Both sides are scoped to the identical geometric region, so the comparison is
    apples-to-apples and falsifiable: same ink, two renderings. Reports numbers the prose
    path loses, re-orders, or invents. This is the anti-regression witness for the known
    failure in which a collapsed risk-weight table put a wrong number into a brief.
    """
    prose = page.extract_text(layout=True) or ""
    prose_nums = [round(v, 4) for v in all_cell_numbers(prose)]

    cand = _extract_pdf_page(page, page_no, source, 2, 2, STRATEGIES)
    struct_nums: list[float] = []
    for t in cand:
        struct_nums.extend(all_cell_numbers("\n".join(" ".join(r) for r in t["cells"])))

    out: dict[str, Any] = {
        "page": page_no,
        "source": source,
        "structured_cells": {
            "tables_found": len(cand),
            "numbers": len(struct_nums),
            "sequence_head": struct_nums[:25],
        },
        "prose_layout_text": {
            "numbers": len(prose_nums),
            "sequence_head": prose_nums[:25],
        },
        "whole_page_reading_order_preserved": struct_nums[:25] == prose_nums[:25],
    }

    # Region-scoped comparison: the best table's own bbox, rendered as cells vs as text.
    if cand:
        best = cand[0]
        region = {"table_shape": best["shape"], "strategy": best["strategy"], "bbox": best["bbox"]}
        cell_nums: list[float] = []
        for r in best["cells"]:
            for c in r:
                cell_nums.extend(all_cell_numbers(c))
        cell_nums = [round(v, 4) for v in cell_nums]
        try:
            crop = page.crop(tuple(best["bbox"]))
            region_prose = crop.extract_text(layout=True) or ""
        except Exception:
            region_prose = ""
        region_nums = [round(v, 4) for v in all_cell_numbers(region_prose)]

        def near(a: float, pool: list[float]) -> bool:
            return any(abs(a - b) <= max(0.005, abs(a) * 1e-6) for b in pool)

        lost = sorted({v for v in cell_nums if not near(v, region_nums)})
        invented = sorted({v for v in region_nums if not near(v, cell_nums)})
        region.update({
            "cells_numbers": len(cell_nums),
            "layout_text_numbers": len(region_nums),
            "cells_sequence": cell_nums[:25],
            "layout_text_sequence": region_nums[:25],
            "numbers_lost_by_prose": lost[:30],
            "numbers_lost_by_prose_count": len(lost),
            "numbers_invented_by_prose": invented[:30],
            "numbers_invented_by_prose_count": len(invented),
            "reading_order_preserved": cell_nums[:25] == region_nums[:25],
            "layout_text_excerpt": region_prose[:600],
        })
        unsafe = bool(lost or invented) or (cell_nums[:25] != region_nums[:25])
        out["region_scope"] = region
        out["verdict"] = "TEXT_PATH_UNSAFE" if unsafe else "TEXT_PATH_AGREES"
    else:
        out["region_scope"] = None
        out["verdict"] = "TEXT_PATH_UNSAFE" if struct_nums != prose_nums else "TEXT_PATH_AGREES"

    out["note"] = (
        "TEXT_PATH_UNSAFE means the layout-text rendering of this region loses, re-orders or "
        "invents numbers relative to the cell matrix. Any number read from that text is "
        "unverified — read it from doc_tables_extract cells and confirm it with "
        "doc_tables_reconcile before publishing."
    )
    return out


# ======================================================================================
# MCP TOOLS
# ======================================================================================


@mcp.tool()
def doc_tables_health() -> dict[str, Any]:
    """Health + capability self-report for doc-tables-mcp.

    Use first when another organ reports a parsing failure, or to confirm the
    pdfplumber/bs4/lxml stack is importable in this server's interpreter.
    """
    caps: dict[str, Any] = {"server": SERVER_NAME, "version": SERVER_VERSION,
                            "authority": "READ_ONLY", "interpreter": None}
    try:
        import sys
        caps["interpreter"] = sys.executable
    except Exception:
        pass
    for mod in ("pdfplumber", "lxml", "bs4", "pandas"):
        try:
            m = __import__(mod)
            caps[mod] = getattr(m, "__version__", "present")
        except Exception as e:  # pragma: no cover
            caps[mod] = f"MISSING: {type(e).__name__}"
    caps["tools"] = [
        "doc_tables_health",
        "doc_tables_list",
        "doc_tables_extract",
        "doc_tables_reconcile",
        "doc_tables_text_mangle_check",
    ]
    caps["status"] = "UP"
    return caps


@mcp.tool()
def doc_tables_list(source: str, page: int | None = None, page_range: list[int] | None = None,
                    min_rows: int = 2, min_cols: int = 2, limit: int = 50) -> dict[str, Any]:
    """INVENTORY tables in a PDF or HTML document WITHOUT returning their cells.

    Use this to find which page holds the table you need, before extracting it.
    `source` = local path or http(s) URL. `page` is 0-based. `page_range` = [start, end]
    inclusive. Scanning a whole large PDF with no page bound can take minutes — pass a
    page or page_range when you know roughly where the table is.
    """
    rng = _as_range(page_range)
    res = extract_any(source, page=page, page_range=rng,
                      min_rows=min_rows, min_cols=min_cols, limit=limit)
    return {
        "source": res["source"],
        "format": res["format"],
        "total_pages": res["total_pages"],
        "pages_scanned": res["pages_scanned"],
        "table_count": res["table_count"],
        "truncated": res["truncated"],
        "inventory": [
            {
                "page": t["page"],
                "shape": t["shape"],
                "strategy": t["strategy"],
                "score": t["score"],
                "caption": t["caption"],
                "bbox": t["bbox"],
                "header_preview": [c for c in (t["cells"][0] if t["cells"] else []) if c][:8],
            }
            for t in res["tables"]
        ],
    }


@mcp.tool()
def doc_tables_extract(source: str, page: int | None = None, page_range: list[int] | None = None,
                       min_rows: int = 2, min_cols: int = 2, limit: int = 50,
                       include_cells: bool = True, include_markdown: bool = True) -> dict[str, Any]:
    """EXTRACT tables as structured cell matrices (JSON) — never as mangled text.

    THIS is the tool to use whenever a number must be read out of a table. Linear text
    extraction (pdftotext -layout) collapses columns and re-associates numbers with the
    wrong labels; that failure has already put a wrong number into a published brief.

    Each table returns: 2-D `cells` matrix, `markdown`, page, bbox, extraction strategy,
    header_rows, and shape {rows, columns, numeric_cells}. Every number is therefore
    traceable to a page and a geometric position.

    `source` = local path or http(s) URL (.pdf or .html). `page` is 0-based.
    """
    rng = _as_range(page_range)
    res = extract_any(source, page=page, page_range=rng,
                      min_rows=min_rows, min_cols=min_cols, limit=limit)
    tables = []
    for i, t in enumerate(res["tables"]):
        item = {k: v for k, v in t.items() if k not in ("cells", "markdown")}
        item["table_index"] = i
        if include_cells:
            item["cells"] = t["cells"]
        if include_markdown:
            item["markdown"] = t["markdown"]
        tables.append(item)
    return {
        "source": res["source"],
        "format": res["format"],
        "total_pages": res["total_pages"],
        "pages_scanned": res["pages_scanned"],
        "table_count": res["table_count"],
        "truncated": res["truncated"],
        "tables": tables,
    }


@mcp.tool()
def doc_tables_reconcile(source: str, page: int | None = None, table_index: int | None = None,
                         total_col_label: str = r"^total$", total_row_label: str = r"\btotal\b",
                         value_mode: str = "last", abs_tolerance: float = 0.5,
                         rel_tolerance: float = 0.005, page_range: list[int] | None = None,
                         min_rows: int = 2) -> dict[str, Any]:
    """RECONCILE an extracted total against the total actually PRINTED in the source.

    The anti-fabrication gate: it re-derives the printed total from the component cells
    and reports PASS/FAIL per row or column, with the raw cell text that produced each
    number. Auto-detects two orientations:
      * total_column — a column headed 'Total'; each row's other numbers must sum to it.
      * total_row    — a row labelled 'Total'; the numbers above must sum to it.

    verdict RECONCILED  = the printed total equals the sum of its stated components.
    verdict MISMATCH    = at least one derived-vs-printed check failed. Do not publish.
    verdict UNRECONCILED= no total was located. This is NOT a pass (Void Guard: absence
                          of evidence is not evidence of correctness).

    `value_mode`: 'last' takes the last numeric literal in a cell — correct for worked
    examples like '440,000 x 50% = 220,000' -> 220000. Use 'first' or 'only' otherwise.
    """
    rng = _as_range(page_range)
    res = extract_any(source, page=page, page_range=rng, min_rows=min_rows, min_cols=2, limit=50)
    if not res["tables"]:
        return {"verdict": "UNRECONCILED", "reason": "no tables found at the given scope",
                "source": res["source"], "table_count": 0}
    idxs = range(len(res["tables"])) if table_index is None else [table_index]
    results = []
    for i in idxs:
        if not (0 <= i < len(res["tables"])):
            continue
        t = res["tables"][i]
        rec = reconcile_table(t["cells"], total_col_label, total_row_label, value_mode,
                              abs_tolerance, rel_tolerance)
        results.append({
            "table_index": i,
            "page": t["page"],
            "shape": t["shape"],
            "caption": t["caption"],
            "bbox": t["bbox"],
            "strategy": t["strategy"],
            "markdown": t["markdown"],
            **rec,
        })
    if not results:
        return {"verdict": "UNRECONCILED", "reason": "no table in scope", "source": res["source"]}
    reconc = [r for r in results if r["verdict"] == "RECONCILED"]
    mism = [r for r in results if r["verdict"] == "MISMATCH"]
    overall = "MISMATCH" if mism else ("RECONCILED" if reconc else "UNRECONCILED")
    return {
        "source": res["source"],
        "verdict": overall,
        "published_safe": overall == "RECONCILED",
        "tables_evaluated": len(results),
        "tables_reconciled": len(reconc),
        "tables_mismatched": len(mism),
        "results": results,
    }


@mcp.tool()
def doc_tables_text_mangle_check(source: str, page: int, page_range: list[int] | None = None) -> dict[str, Any]:
    """WITNESS the failure mode: compare structured cells vs layout-prose text on one page.

    Reports which numbers are LOST or re-ordered when the same page is flattened to
    pdftotext -layout style text. Use as evidence when someone proposes reading a number
    from linear text, or to prove a past extraction was unsafe.

    verdict TEXT_PATH_UNSAFE = the prose path loses or reorders numbers on this page.
    """
    import pdfplumber

    path, _ = _resolve_source(source)
    if _is_html(path):
        return {"verdict": "NOT_APPLICABLE", "reason": "HTML has no layout-text failure mode"}
    with pdfplumber.open(path) as pdf:
        if not (0 <= page < len(pdf.pages)):
            return {"verdict": "ERROR", "reason": f"page {page} out of range (0..{len(pdf.pages)-1})"}
        return text_mangle_report(pdf.pages[page], source, page)


def main() -> None:
    port = int(os.environ.get("DOC_TABLES_PORT", DEFAULT_PORT))
    host = os.environ.get("DOC_TABLES_HOST", "127.0.0.1")
    transport = os.environ.get("DOC_TABLES_TRANSPORT", "http")
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host=host, port=port)


if __name__ == "__main__":
    main()
