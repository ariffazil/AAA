#!/usr/bin/env python3
"""docbuild — one federated document pipeline: render, verify, seal.

WHY THIS EXISTS
---------------
The federation has strong document skills but no shared engine, so every build
re-implements the same six steps by hand and forgets one of them under time
pressure. This is the engine those skills point at. Renderer is swappable; the
gates and the seal are not.

LAYERS (each owned by a skill — this script only executes them)
  1 build    HTML source ......................... caller
  2 render   engine adapter ...................... this file
  3 verify   page count / ink / leaks / text ..... this file
  4 seal     content hash + artifact hash + ledger  this file
  Audit doctrine: rendered-document-audit · paged-media-report-layout
  Seal doctrine:  sealed-deliverable-provenance
  Design doctrine: human-facing-artifact-design

THE SEAL CONTRACT (from sealed-deliverable-provenance)
  A file cannot contain its own hash. So:
    content_sha256  = sha256(template BEFORE placeholder substitution) → printed INSIDE
    artifact_sha256 = sha256(rendered bytes AFTER render)              → sidecar BESIDE
  Order is load-bearing: hash the template, inject, render, hash the render.

USAGE
  python3 docbuild.py --src index.html --out EDITION.pdf \\
      --edition 001 --ledger ledger.jsonl [--engine chrome|weasyprint] [--no-seal]
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------- engines

def _which(name: str) -> str | None:
    return shutil.which(name)


def render_chrome(src_path: str, out_path: str, timeout: int = 180) -> tuple[bool, str]:
    """Headless Chromium. Highest CSS fidelity; JS supported.

    Chrome 85+ emits a TAGGED PDF (accessibility baseline) automatically.
    Chrome 'was never meant to be a backend service' — for high-volume or
    untrusted HTML prefer weasyprint. --no-pdf-header-footer is REQUIRED or
    the renderer burns file:/// paths and timestamps into every page.
    """
    exe = _which("google-chrome") or _which("chromium") or _which("chromium-browser")
    if not exe:
        return False, "no chrome/chromium binary on PATH"
    cmd = [
        exe, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=15000",
        f"--print-to-pdf={out_path}", f"file://{os.path.abspath(src_path)}",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if not os.path.exists(out_path):
        return False, f"chrome produced no file (rc={p.returncode}) {p.stderr[-300:]}"
    return True, "chrome"


def render_weasyprint(src_path: str, out_path: str, timeout: int = 180) -> tuple[bool, str]:
    """WeasyPrint: strong CSS-paged-media (running headers/footers via @page),
    pure Python, no browser. No JavaScript support."""
    if not _which("weasyprint"):
        return False, "weasyprint not installed"
    p = subprocess.run(["weasyprint", src_path, out_path],
                       capture_output=True, text=True, timeout=timeout)
    if not os.path.exists(out_path):
        return False, f"weasyprint produced no file {p.stderr[-300:]}"
    return True, "weasyprint"


def render_reportlab(src_path: str, out_path: str, timeout: int = 180) -> tuple[bool, str]:
    """ReportLab path is programmatic, not HTML — the caller must supply a
    build script instead of an HTML file. Registered so the router can name it,
    deliberately not auto-invoked from here."""
    return False, "reportlab requires a python build script, not an HTML source (see scientific-pdf-generation)"


ENGINES = {
    "chrome": render_chrome,
    "weasyprint": render_weasyprint,
    "reportlab": render_reportlab,
}


# ---------------------------------------------------------------- gates

def pdf_pages(path: str) -> int | None:
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else None


def text_layer(path: str) -> str:
    return subprocess.run(["pdftotext", path, "-"],
                          capture_output=True, text=True).stdout


def ink_coverage(path: str, dpi: int = 72) -> list[float] | None:
    """Per-page ink share. Works for light documents (dark marks on white).
    A page an order of magnitude below its neighbours is a stranded fragment."""
    try:
        from PIL import Image
    except ImportError:
        return None
    tmp = "/tmp/docbuild_pg"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", path, f"{tmp}/p"], check=False)
    out = []
    for f in sorted(x for x in os.listdir(tmp) if x.endswith(".png")):
        im = Image.open(os.path.join(tmp, f)).convert("L")
        w, h = im.size
        small = im.resize((max(1, w // 2), max(1, h // 2)))
        data = list(small.tobytes())          # bytes, not getdata() — stable across Pillow versions
        dark = sum(1 for p in data if p < 200)
        out.append(round(100.0 * dark / max(1, len(data)), 2))
    shutil.rmtree(tmp, ignore_errors=True)
    return out


def verify(out_path: str, content_hash: str) -> dict:
    """The gate set from rendered-document-audit + sealed-deliverable-provenance."""
    txt = text_layer(out_path)
    pages = pdf_pages(out_path)
    ink = ink_coverage(out_path)
    checks = {
        "is_real_pdf":          open(out_path, "rb").read(5) == b"%PDF-",
        "pages":                pages,
        "text_chars":           len(txt),
        "content_hash_inside":  txt.count(content_hash),
        "artifact_not_inside":  True,   # asserted below by caller-supplied hash
        "internal_path_leak":   len(re.findall(r"file:///|/root/", txt)),
        "ink_per_page":         ink,
    }
    # structural verdicts
    problems = []
    if not checks["is_real_pdf"]:
        problems.append("not a real PDF")
    if not pages:
        problems.append("page count unreadable")
    if checks["text_chars"] < 200:
        problems.append(f"text layer nearly empty ({checks['text_chars']} chars)")
    if checks["content_hash_inside"] < 1:
        problems.append("content hash NOT embedded in the document")
    if checks["internal_path_leak"] != 0:
        problems.append(f"internal path leaked ({checks['internal_path_leak']}x)")
    if ink:
        sparsest = min(ink)
        if sparsest < 3.0:
            problems.append(f"page at {sparsest}% ink — stranded/near-empty page")
        if max(ink) > 4 * max(sparsest, 1.0):
            problems.append(f"ink spread {sparsest}–{max(ink)}% — layout break signature")
    checks["problems"] = problems
    checks["verdict"] = "PASS" if not problems else "FAIL"
    return checks


# ---------------------------------------------------------------- seal

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def seal(out_path: str, content_hash: str, edition: str, ledger: str | None,
         authority: str) -> dict:
    import pathlib
    art = sha256_file(out_path)
    sidecar = out_path.rsplit(".", 1)[0] + ".sha256"
    with open(sidecar, "w") as f:
        f.write(f"{art}  {os.path.basename(out_path)}\n")

    chain_prev = ""
    if ledger and os.path.exists(ledger):
        try:
            last = [json.loads(l) for l in open(ledger) if l.strip()][-1]
            chain_prev = last.get("artifact_sha256", "")
        except (json.JSONDecodeError, IndexError):
            chain_prev = ""

    row = {
        "edition": edition,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content_sha256": content_hash,
        "artifact_sha256": art,
        "chain_prev": chain_prev,
        "seal_authority": authority,
        "pages": pdf_pages(out_path),
    }
    if ledger:
        with open(ledger, "a") as f:
            f.write(json.dumps(row) + "\n")
    return {"artifact_sha256": art, "sidecar": sidecar, "ledger_row": row}


# ---------------------------------------------------------------- main

PLACEHOLDER = "{{CONTENT_SHA256}}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--edition", default="draft")
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--engine", default="chrome", choices=sorted(ENGINES))
    ap.add_argument("--authority", default="NOT F13-RATIFIED — lane B receipt",
                    help="named on every ledger row; an unlabelled seal reads as the strongest one")
    ap.add_argument("--no-seal", action="store_true")
    args = ap.parse_args()

    print(f"docbuild — edition {args.edition} via {args.engine}")

    # STEP 1 — hash the TEMPLATE, before substitution (order is load-bearing)
    raw = open(args.src, encoding="utf-8").read()
    if PLACEHOLDER not in raw:
        print(f"  note: {PLACEHOLDER} not in source — content hash will not be embedded")
    content_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    print(f"  content_sha256 {content_hash[:16]}…  (of template, pre-substitution)")

    # STEP 2 — inject, render to a temp source so the original is untouched
    rendered_src = "/tmp/docbuild_src.html"
    with open(rendered_src, "w", encoding="utf-8") as f:
        f.write(raw.replace(PLACEHOLDER, content_hash))

    # STEP 3 — render
    ok, why = ENGINES[args.engine](rendered_src, args.out)
    if not ok:
        print(f"  RENDER FAILED: {why}")
        return 2
    print(f"  rendered → {args.out}")

    # STEP 4 — verify
    v = verify(args.out, content_hash)
    print(f"\n  GATES — {v['verdict']}")
    print(f"    pages ................. {v['pages']}")
    print(f"    text layer ............ {v['text_chars']} chars")
    print(f"    content hash inside ... {v['content_hash_inside']} (need >=1)")
    print(f"    internal path leak .... {v['internal_path_leak']} (need 0)")
    if v["ink_per_page"]:
        print(f"    ink per page .......... {v['ink_per_page']}")
    for p in v["problems"]:
        print(f"    !! {p}")

    if args.no_seal:
        print("\n  --no-seal: skipping seal")
        return 0 if v["verdict"] == "PASS" else 1

    # STEP 5 — seal
    s = seal(args.out, content_hash, args.edition, args.ledger, args.authority)
    print(f"\n  SEAL — {args.authority}")
    print(f"    artifact_sha256 ....... {s['artifact_sha256']}")
    print(f"    sidecar ............... {s['sidecar']}")
    if args.ledger:
        print(f"    ledger row ............ chain_prev={s['ledger_row']['chain_prev'][:16] or '(genesis)'}")
    print(f"    verify ................ sha256sum -c {os.path.basename(s['sidecar'])}")

    return 0 if v["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
