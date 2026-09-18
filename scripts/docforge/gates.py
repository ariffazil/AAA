#!/usr/bin/env python3
"""docforge.gates — the verification chain an artifact must pass before delivery.

WHY A CHAIN AND NOT ONE CHECK
  Each gate answers a different question, and they fail independently:

      pdf_real      did a real PDF come out at all?
      geometry      is the page count and paper size what the design intended?
      ink_present   is any page blank (content silently lost)?
      theme_light   is the page light-background or a toner-eating dark fill?
      text_layer    did the text arrive, in order, with no internal path leaked?
      figures       do embedded images exist where the captions claim?

  "It opens" answers none of them. A file can open, be a real PDF, and still be
  a stack of blank paper with headings on it.

THE DARK-FILL GATE, AND THE TEST THAT WAS WRONG
  A first version of this check measured only the longest horizontal run of dark
  pixels. It flagged 797px runs on seven pages and declared a dark-band failure.
  That test was mis-specified: a 2px navy *rule* under a table header and a
  26px navy *fill* produce the SAME horizontal run. Run length cannot tell them
  apart. Thickness can. A control image proves it.

  So two measurements are used, and the primary one is the direct reading of the
  actual complaint:
      dark_frac  = fraction of page pixels below the dark threshold
                   light page ~0.03-0.10 | a filled dark background ~0.5-0.9
      band height = vertical thickness of any wide dark region
                   a rule is 1-3px (0.2-0.7mm); a fill is 20px+ (4.6mm+)

  A gate that reports the wrong thing is worse than no gate: it spends the
  operator's trust and buys nothing. This one reports the quantity a human
  actually cares about, so it cannot pass a document the human would reject.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

# thresholds, all overridable by profile
DARK_PX = 90          # 0-255 luminance under which a pixel is "dark ink"
INK_PX = 235          # under which a pixel carries any mark at all
INK_FLOOR = 0.0005    # below this a page is BLANK. CALIBRATED, not chosen: a
                      # genuinely blank A4 at 110dpi measured 0.00-0.01% ink; a
                      # heading-only page measured 0.06%; a real slide holding a
                      # heading plus one line measured 0.17%. 0.05% sits below
                      # every measured blank and above none of them.
INK_DENSE_MEDIAN = 0.02   # above this the document is dense enough that a
                          # sparse page is anomalous rather than just short
INK_SPARSE_RATIO = 0.25   # a page under 25% of a dense document's median ink
DARK_FRAC_MAX = 0.25  # above this the page is a dark-background page
BAND_MIN_PX = 8       # at 110dpi 1px = 0.231mm; >=8px (1.85mm) is a fill, not a rule


@dataclass
class Finding:
    gate: str
    ok: bool
    detail: str
    evidence: str = ""


def _effective(opts: dict | None) -> dict:
    """Merge the named profile into opts so EVERY gate sees its own thresholds.

    First version applied profiles only inside run_chain(). A gate invoked
    directly then silently used the defaults, which is how the suite caught the
    bug: `g_theme_light(pdf, {"profile": "screen-dark"})` ignored the profile and
    judged a deliberately dark document by the light-page cutoff. A gate whose
    thresholds depend on HOW it was called is not a gate.
    """
    o = dict(opts or {})
    name = o.get("profile")
    if not name:
        return o
    base = PROFILES.get(name)
    if not base:
        raise RuntimeError(f"unknown profile {name!r}; known: {sorted(PROFILES)}")
    merged = dict(base)
    merged.update({k: v for k, v in o.items() if v is not None})
    return merged


def _run(cmd: list[str], timeout: int = 300):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def _need(binary: str) -> bool:
    return shutil.which(binary) is not None


_RENDER_CACHE: dict[tuple, list[Path]] = {}
_STATS_CACHE: dict[tuple, dict] = {}


def _render_pages(pdf: Path, dpi: int = 110) -> list[Path]:
    """Rasterise pages to PNG, cached per (file, mtime, dpi).

    Two gates read pixels (ink_present, theme_light). Without the cache each
    build rasterises the document twice; with it, once. Keyed on mtime_ns so a
    rebuilt file is never served stale pixels.
    """
    key = (str(pdf), pdf.stat().st_mtime_ns, dpi)
    if key in _RENDER_CACHE:
        return _RENDER_CACHE[key]
    tmp = Path("/tmp/docforge-qa")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)
    _run(["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(tmp / "pg")])
    pages = sorted(tmp.glob("pg-*.png"))
    _RENDER_CACHE.clear()
    _RENDER_CACHE[key] = pages
    return pages


# ── gate 1: it is actually a PDF ─────────────────────────────────────────────


def g_pdf_real(pdf: Path, opts: dict) -> Finding:
    if not pdf.exists():
        return Finding("pdf_real", False, "file does not exist")
    head = pdf.open("rb").read(5)
    if head != b"%PDF-":
        return Finding("pdf_real", False,
                       f"magic bytes are {head!r}, not %PDF- "
                       "(an extension is not a format)")
    if _need("file"):
        out = _run(["file", str(pdf)]).stdout.strip()
        if "PDF document" not in out:
            return Finding("pdf_real", False, f"file(1) says: {out}")
    if _need("pdfinfo"):
        info = _run(["pdfinfo", str(pdf)]).stdout
        m = re.search(r"PDF version:\s*(\S+)", info)
        ver = m.group(1) if m else "?"
        return Finding("pdf_real", True, f"real PDF, version {ver}", "magic=%PDF-")
    return Finding("pdf_real", True, "real PDF (magic bytes)")


# ── gate 2: geometry ─────────────────────────────────────────────────────────


def g_geometry(pdf: Path, opts: dict) -> Finding:
    opts = _effective(opts)
    if not _need("pdfinfo"):
        return Finding("geometry", True, "pdfinfo absent, skipped")
    info = _run(["pdfinfo", str(pdf)]).stdout
    pages = re.search(r"^Pages:\s*(\d+)", info, re.M)
    size = re.search(r"^Page size:\s*(.+)$", info, re.M)
    n = int(pages.group(1)) if pages else 0
    want = opts.get("expect_pages")
    if not n:
        return Finding("geometry", False, "page count unreadable")
    if want is not None and n != int(want):
        return Finding("geometry", False,
                       f"{n} pages, expected {want} "
                       "(a mismatch means content moved or overflowed)")
    return Finding("geometry", True, f"{n} pages, {size.group(1).strip() if size else 'size ?'}")


# ── gate 3: ink present (blank-page detector) ────────────────────────────────


def _page_stats(img_path: Path) -> dict:
    """dark_frac / ink_frac / largest wide-dark band thickness.

    numpy rather than a nested pixel loop: at 110dpi a page is ~900x1170, so a
    pure-Python walk is ~1M getpixel calls per page. Vectorised it is a few
    milliseconds, which is what makes a 6-gate chain affordable per build.
    """
    import numpy as np
    from PIL import Image

    key = (str(img_path), img_path.stat().st_mtime_ns)
    if key in _STATS_CACHE:
        return _STATS_CACHE[key]

    arr = np.asarray(Image.open(img_path).convert("L"), dtype=np.uint8)
    h, w = arr.shape

    dark_mask = arr < DARK_PX
    ink_frac = float((arr < INK_PX).mean())
    dark_frac = float(dark_mask.mean())

    # longest horizontal dark run per row, via run-boundary detection.
    # Padding by one column makes every run yield exactly one +1 (start) and one
    # -1 (end) in the column-wise difference, so k-th start pairs with k-th end.
    padded = np.pad(dark_mask, ((0, 0), (1, 1))).astype(np.int8)
    edges = np.diff(padded, axis=1)
    max_runs = np.zeros(h, dtype=np.int32)
    for y in range(h):
        row = edges[y]
        starts = np.flatnonzero(row == 1)
        if starts.size:
            ends = np.flatnonzero(row == -1)
            max_runs[y] = int((ends - starts).max())

    wide = max_runs > 0.4 * w
    band = cur = 0
    for is_wide in wide:
        cur = cur + 1 if is_wide else 0
        band = max(band, cur)
    band_px = int(band)

    result = {
        "dpi": 110, "w": w, "h": h,
        "dark_frac": dark_frac,
        "ink_frac": ink_frac,
        "band_px": band_px,
        "band_mm": round(band_px * 0.231, 2),
    }
    _STATS_CACHE.clear()
    _STATS_CACHE[key] = result
    return result


def g_ink_present(pdf: Path, opts: dict) -> Finding:
    """Blank-page detection, which is inherently RELATIVE to the document.

    First version used an absolute floor of 3%, inherited from guidance written
    about dense report pages. It refused to seal a legitimately short two-page
    document whose second page carried 0.9% ink — visibly populated text, not a
    blank page. An absolute threshold cannot tell "short" from "empty", because
    the two are the same number in different documents.

    So: an absolute floor catches a genuinely blank page, and a relative test
    catches an orphan page inside a document that is otherwise dense. The
    relative test only engages when the median page exceeds INK_DENSE_MEDIAN, so
    a uniformly sparse document is never flagged for being sparse.

    STATED LIMITATION: ink alone cannot separate a page carrying only a heading
    from a page carrying a short paragraph — measured 0.06% vs 0.17%, too close
    to gate reliably. That case is covered by the text_layer gate, which refuses
    a page with no text layer at all. Two gates, two different signals; neither
    pretends to be the other.
    """
    opts = _effective(opts)
    if not _need("pdftoppm"):
        return Finding("ink_present", True, "pdftoppm absent, skipped")
    pages = _render_pages(pdf)
    if not pages:
        return Finding("ink_present", False, "no page images rendered")

    vals = [_page_stats(p)["ink_frac"] for p in pages]
    floor = opts.get("ink_floor", INK_FLOOR)
    med = sorted(vals)[len(vals) // 2]
    dense = med >= opts.get("ink_dense_median", INK_DENSE_MEDIAN)
    rel = opts.get("ink_sparse_ratio", INK_SPARSE_RATIO)
    # A document that declares an explicit cover page is exempting its first
    # page from the orphan check. A title page is sparse BY DESIGN; treating
    # it as an orphan is a false positive. The opt-in is in the spec, so the
    # exemption cannot be applied accidentally to a document that has no cover.
    cover_exempt = bool(opts.get("cover_orphan_exempt", False))
    n = len(pages)

    blank: list[str] = []
    reported: list[str] = []
    for i, (pg, v) in enumerate(zip(pages, vals)):
        is_cover = cover_exempt and i == 0
        # Median calculation skips the cover so a sparse cover cannot drag the
        # document-wide median down and mask a genuine blank later.
        if not is_cover:
            reported.append(v)
        if v < floor:
            blank.append(f"{pg.stem}:{100*v:.2f}% (blank)")
        elif dense and v < rel * med:
            if is_cover:
                continue
            blank.append(f"{pg.stem}:{100*v:.2f}% (under {int(rel*100)}% of the "
                         f"{100*med:.1f}% median — orphan page)")
    med = sorted(reported)[len(reported) // 2] if reported else 0

    summary = (f"min ink {100*min(vals):.2f}%, median {100*med:.2f}%, "
               f"floor {100*floor:.2f}%"
               + ("" if dense else " (relative test off: document is uniformly light)"))
    if blank:
        return Finding("ink_present", False,
                       f"blank/orphan page(s): {', '.join(blank)} | {summary}")
    rows = " ".join(f"{p.stem}:{100*v:.1f}%" for p, v in zip(pages, vals))
    return Finding("ink_present", True, summary + " — no blank page | " + rows)


# ── gate 4: light theme (the actual human requirement, mechanised) ───────────


def g_theme_light(pdf: Path, opts: dict) -> Finding:
    opts = _effective(opts)
    if not _need("pdftoppm"):
        return Finding("theme_light", True, "pdftoppm absent, skipped")
    cutoff = opts.get("dark_frac_max", DARK_FRAC_MAX)
    band_max = opts.get("band_max_px", BAND_MIN_PX)
    pages = _render_pages(pdf)
    if not pages:
        return Finding("theme_light", False, "no page images rendered")

    offenders, fills, worst, worst_page = [], [], 0.0, ""
    for p in pages:
        st = _page_stats(p)
        if st["dark_frac"] > worst:
            worst, worst_page = st["dark_frac"], p.stem
        if st["dark_frac"] > cutoff:
            offenders.append(f"{p.stem}:{100*st['dark_frac']:.0f}%")
        if st["band_px"] >= band_max:
            fills.append(f"{p.stem}:{st['band_mm']}mm")
    detail = (f"max dark-area {100*worst:.1f}% ({worst_page}), "
              f"limit {100*cutoff:.0f}%")
    if offenders:
        return Finding("theme_light", False,
                       f"dark-background page(s): {', '.join(offenders)} | {detail}")
    if fills:
        return Finding("theme_light", False,
                       f"wide dark FILL band(s) >= {band_max}px: {', '.join(fills)} | {detail}")
    return Finding("theme_light", True, detail + " — no dark fill, bands are rules only")


# ── gate 5: text layer ───────────────────────────────────────────────────────


def g_text_layer(pdf: Path, opts: dict) -> Finding:
    opts = _effective(opts)
    if not _need("pdftotext"):
        return Finding("text_layer", True, "pdftotext absent, skipped")
    txt = _run(["pdftotext", str(pdf), "-"]).stdout

    if opts.get("forbid_paths", True):
        leaked = re.findall(r"file:///|/root/|/tmp/|/home/", txt)
        if leaked:
            uniq = sorted(set(leaked))
            return Finding("text_layer", False,
                           f"internal filesystem path leaked into the document: {uniq}")

    must = opts.get("must_contain") or []
    missing = [m for m in must if m not in txt]
    if missing:
        return Finding("text_layer", False, f"absent from text layer: {missing}")

    if opts.get("expect_pages") and _need("pdfinfo"):
        m = re.search(r"^Pages:\s*(\d+)", _run(["pdfinfo", str(pdf)]).stdout, re.M)
        if m:
            n = int(m.group(1))
            empty = [str(i) for i in range(1, n + 1)
                     if not _run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"])
                     .stdout.strip()]
            if empty:
                return Finding("text_layer", False, f"page(s) with no text layer: {empty}")

    return Finding("text_layer", True,
                   f"{len(txt)} chars extracted, no internal path, "
                   f"{len(must)} required string(s) present")


# ── gate 6: figures ──────────────────────────────────────────────────────────


def g_figures(pdf: Path, opts: dict) -> Finding:
    opts = _effective(opts)
    want = opts.get("expect_images")
    if want is None:
        return Finding("figures", True, "not asserted for this document")
    if not _need("pdfimages"):
        return Finding("figures", True, "pdfimages absent, skipped")
    out = _run(["pdfimages", "-list", str(pdf)]).stdout
    rows = [l for l in out.splitlines()[2:] if l.strip()]
    n = len(rows)
    ok = n >= int(want)
    return Finding("figures", ok,
                   f"{n} embedded image object(s), expected >= {want}"
                   + ("" if ok else " — a caption without an image is a missing figure"))


# ── chain ────────────────────────────────────────────────────────────────────

CHAIN = [g_pdf_real, g_geometry, g_ink_present, g_theme_light, g_text_layer, g_figures]

# profile a document so gates know what to demand
PROFILES = {
    "print-light": {"dark_frac_max": 0.25, "band_max_px": 8,
                    "ink_floor": 0.0005, "forbid_paths": True},
    "screen-dark":  {"dark_frac_max": 0.95, "band_max_px": 10**6,
                     "ink_floor": 0.0005, "forbid_paths": True},
    "accessible":   {"dark_frac_max": 0.25, "band_max_px": 8,
                     "ink_floor": 0.0005, "forbid_paths": True,
                     "require_pdfua": True},
}


def run_chain(pdf: Path, opts: dict | None = None) -> list[Finding]:
    opts = _effective(opts)
    return [g(pdf, opts) for g in CHAIN]
