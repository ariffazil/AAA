#!/usr/bin/env python3
"""Conformance suite for the docforge document lane.

Run: python3 /root/AAA/scripts/test_docforge.py

THE NEGATIVES ARE THE POINT
  Every capability here is a control, and a control that cannot fail is not a
  control. So each positive assertion is paired with a case that MUST be
  rejected:

    - a 26px dark FILL must be distinguished from a 2px dark RULE
      (the exact defect that made the first dark-band test report a false alarm:
       run length is identical for both, only thickness differs)
    - the dark theme MUST fail the print-light profile
    - a text file with a .pdf extension MUST fail the real-PDF gate
    - a leaked internal filesystem path MUST fail the text gate
    - a build whose gate chain fails MUST NOT append to the seal ledger

  If any of those start passing, the lane has lost the property it exists to
  provide and this suite is what tells us.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path("/root/AAA/scripts")
sys.path.insert(0, str(SCRIPTS))

from docforge import gates as G  # noqa: E402
from docforge import seal as S  # noqa: E402

WORK = Path("/tmp/docforge-test")
PASS = FAIL = 0
FAILURES: list[str] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  [PASS] {label}" + (f" — {detail}" if detail else ""))
    else:
        FAIL += 1
        FAILURES.append(label)
        print(f"  [FAIL] {label}" + (f" — {detail}" if detail else ""))


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "docforge", *args],
                          cwd=str(SCRIPTS), capture_output=True, text=True, timeout=900)


def make_png(path: Path, spec: dict) -> Path:
    """Synthetic page: either a full dark fill, or a hairline rule, on white."""
    from PIL import Image, ImageDraw
    im = Image.new("L", (909, 1170), 255)
    d = ImageDraw.Draw(im)
    if spec.get("fill"):
        y0, y1 = spec["fill"]
        d.rectangle([20, y0, 889, y1], fill=13)
    if spec.get("rule"):
        y0, y1 = spec["rule"]
        d.rectangle([20, y0, 889, y1], fill=13)
    if spec.get("text"):
        for i in range(spec["text"]):
            y = 120 + i * 26
            d.rectangle([40, y, 40 + (600 if i % 3 else 300), y + 3], fill=60)
    im.save(path)
    return path


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)

    # ── 1. the measurement that separates a FILL from a RULE ─────────────────
    print("=" * 76)
    print("1. PAGE STATISTICS — fill vs rule (same run length, different thickness)")
    print("=" * 76)
    light = G._page_stats(make_png(WORK / "a_light.png", {"text": 30}))
    rule = G._page_stats(make_png(WORK / "b_rule.png", {"text": 30, "rule": (400, 402)}))
    fill = G._page_stats(make_png(WORK / "c_fill.png", {"text": 5, "fill": (300, 326)}))
    dark = G._page_stats(make_png(WORK / "d_dark.png", {"fill": (0, 1169)}))

    print(f"     light  dark_frac={light['dark_frac']:.3f} band={light['band_px']}px")
    print(f"     rule   dark_frac={rule['dark_frac']:.3f} band={rule['band_px']}px")
    print(f"     fill   dark_frac={fill['dark_frac']:.3f} band={fill['band_px']}px")
    print(f"     dark   dark_frac={dark['dark_frac']:.3f} band={dark['band_px']}px")

    # These assertions test the PROPERTY (separation), not a number I picked.
    # An earlier version asserted light < 0.05, which a page of 30 solid dark
    # bars legitimately exceeds at 5.7% while being 94% white. The gate's own
    # cutoff is DARK_FRAC_MAX; that is the standard the metric has to satisfy.
    check("light page sits far below the gate cutoff",
          light["dark_frac"] < G.DARK_FRAC_MAX / 4,
          f"light={light['dark_frac']:.3f} vs cutoff={G.DARK_FRAC_MAX}")
    check("26px fill IS a fill", fill["band_px"] >= 20, f"band={fill['band_px']}px")
    check("2px rule is NOT a fill (thickness, not run length, decides)",
          rule["band_px"] <= 4,
          f"band={rule['band_px']}px — a fill would be >=8px")
    check("dark_frac separates light from dark by an order of magnitude",
          dark["dark_frac"] > 10 * max(light["dark_frac"], 1e-6),
          f"dark={dark['dark_frac']:.2f} vs light={light['dark_frac']:.3f} "
          f"({dark['dark_frac']/max(light['dark_frac'],1e-6):.0f}x)")
    check("dark page exceeds the gate cutoff and light does not",
          dark["dark_frac"] > G.DARK_FRAC_MAX > light["dark_frac"] * 4)

    # ── 2. real-PDF gate, with a text file wearing a PDF extension ───────────
    print()
    print("=" * 76)
    print("2. pdf_real — an extension is not a format")
    print("=" * 76)
    fake = WORK / "fake.pdf"
    fake.write_text("this is plain text wearing a .pdf extension\n")
    f_fake = G.g_pdf_real(fake, {})
    check("text file named .pdf is REJECTED", not f_fake.ok, f_fake.detail)

    # ── 3/4/5. real builds across the theme axis ────────────────────────────
    print()
    print("=" * 76)
    print("3. THEME AXIS — light must pass print gate; dark must FAIL it")
    print("=" * 76)

    body = WORK / "content.html"
    body.write_text(
        "<h2>1 Signals</h2>"
        "<p>Body paragraph carrying a load-bearing figure: the interval is 105 days.</p>"
        "<table><thead><tr><th>Item</th><th>Reading</th></tr></thead><tbody>"
        "<tr><td>alpha</td><td>1</td></tr><tr><td>beta</td><td>2</td></tr>"
        "</tbody></table>"
        "<div class='box key'><strong>Claim class:</strong> measured.</div>"
    )

    def spec_for(theme: str, name: str, extra_gates: dict | None = None) -> Path:
        run_dir = WORK / name
        run_dir.mkdir(parents=True, exist_ok=True)
        g = {"profile": "print-light", "forbid_paths": True, "expect_pages": 2}
        if extra_gates:
            g.update(extra_gates)
        spec = {
            "edition": name.upper(), "edition_date": "2026-09-18",
            "title": "docforge conformance", "subtitle": theme,
            "template": "base-a4", "theme": theme,
            "source": "content.html", "run_dir": str(run_dir),
            "gates": g,
        }
        p = run_dir / "spec.json"
        p.write_text(json.dumps(spec, indent=2))
        shutil.copy(body, run_dir / "content.html")
        return p

    r_light = run(["build", str(spec_for("light", "light"))])
    check("light theme build exits 0", r_light.returncode == 0,
          (r_light.stdout.strip().splitlines() or ["no output"])[-1])
    light_pdf = WORK / "light" / "LIGHT.pdf"
    check("light theme produced a real PDF",
          light_pdf.exists() and light_pdf.open("rb").read(4) == b"%PDF")
    f_theme_light = G.g_theme_light(light_pdf, {"dark_frac_max": 0.25, "band_max_px": 8})
    check("light theme PASSES print-light theme gate", f_theme_light.ok, f_theme_light.detail)

    r_dark = run(["build", str(spec_for("dark", "dark"))])
    check("dark theme build REFUSES to seal (gate failure is the control)",
          r_dark.returncode != 0, f"exit={r_dark.returncode}")
    dark_pdf = WORK / "dark" / "DARK.pdf"
    check("dark build still rendered the artifact for inspection", dark_pdf.exists())
    if dark_pdf.exists():
        f_theme_dark = G.g_theme_light(dark_pdf, {"dark_frac_max": 0.25, "band_max_px": 8})
        check("dark theme FAILS print-light gate", not f_theme_dark.ok, f_theme_dark.detail)
        f_dark_ok = G.g_theme_light(dark_pdf, {"profile": "screen-dark"})
        check("dark theme PASSES screen-dark profile when declared",
              f_dark_ok.ok, f_dark_ok.detail)
    led_ws = WORK / S.LEDGER_NAME
    check("refused build appended NOTHING to the seal ledger",
          (not led_ws.exists()) or ("DARK" not in led_ws.read_text()),
          "a seal over a failed artifact would write the defect into the record")
    check("dark build surfaced the failure in its output",
          "REFUSED TO SEAL" in r_dark.stdout)

    # ── 6. text-layer gate ──────────────────────────────────────────────────
    print()
    print("=" * 76)
    print("4. text_layer — internal paths and missing strings")
    print("=" * 76)
    f_ok = G.g_text_layer(light_pdf, {"must_contain": ["105 days"], "forbid_paths": True})
    check("required string present in text layer", f_ok.ok, f_ok.detail)
    f_missing = G.g_text_layer(light_pdf, {"must_contain": ["definitely-absent-9f3a"]})
    check("absent required string is REJECTED", not f_missing.ok, f_missing.detail)

    import weasyprint  # noqa: E402
    leak_pdf = WORK / "leaked.pdf"
    leaked_html = WORK / "leaked.html"
    # a deliberately leaked local path: the gate must refuse to ship a document
    # carrying a reference to the machine that built it
    leaked_html.write_text(
        "<!DOCTYPE html><html><body>"
        "<p>see the full copy at file:///var/arif/internal-note.txt</p>"
        "</body></html>")
    weasyprint.HTML(filename=str(leaked_html)).write_pdf(str(leak_pdf))
    f_leak = G.g_text_layer(leak_pdf, {"forbid_paths": True})
    check("leaked file:/// path is REJECTED", not f_leak.ok, f_leak.detail)

    # ── 6b. blank-page detection, both directions ───────────────────────────
    print()
    print("=" * 76)
    print("4b. ink_present — a short page passes, a blank page does not")
    print("=" * 76)
    f_short = G.g_ink_present(light_pdf, {"profile": "print-light"})
    check("a SHORT page is not mistaken for a BLANK page", f_short.ok, f_short.detail)

    blank_html = WORK / "blank.html"
    blank_html.write_text(
        "<!DOCTYPE html><html><head><style>@page{size:A4;margin:20mm}"
        "</style></head><body><h1 style='font-size:11pt'>only a title</h1>"
        "<div style='page-break-after:always'></div><p>&nbsp;</p>"
        "<div style='page-break-after:always'></div><p>&nbsp;</p>"
        "<div style='page-break-after:always'></div><p>&nbsp;</p>"
        "<p>x</p></body></html>")
    blank_pdf = WORK / "blank.pdf"
    weasyprint.HTML(filename=str(blank_html)).write_pdf(str(blank_pdf))
    f_blank = G.g_ink_present(blank_pdf, {"profile": "print-light"})
    check("a genuinely BLANK page is caught", not f_blank.ok, f_blank.detail)

    # the floor is a CALIBRATED number, so pin it to the measurement that set it.
    # A floor that drifts back up starts rejecting legitimate short documents
    # (the pilot's closing page measures 3.87%; a deck slide measures 0.17%).
    check("ink floor sits below every measured real page and above measured blank",
          G.INK_FLOOR <= 0.001,
          f"floor={G.INK_FLOOR:.4f} (calibrated: blank 0.00-0.01%, heading-only "
          f"0.06%, real short page 0.17%)")

    # ── 7. seal mechanics ───────────────────────────────────────────────────
    print()
    print("=" * 76)
    print("5. SEAL — two hashes, sidecar, chain, tamper detection")
    print("=" * 76)
    led = json.loads((WORK / "light" / "LIGHT.ledger.json").read_text())
    check("content hash and artifact hash are different values",
          led["content_sha256"] != led["artifact_sha256"])
    check("all gates recorded as passing", led["gates_all_pass"] is True)
    check("signature honestly states not_signed", led["signature"] == "not_signed")
    sidecar = WORK / "light" / led["sidecar"]
    ok, msg = S.check_sidecar(sidecar)
    check("sidecar verifies with sha256sum -c", ok, msg)

    chain = WORK / S.LEDGER_NAME
    check("ledger lives one level above the run dir (one chain per workspace)",
          chain.exists(), str(chain))
    ok, lines = S.verify_chain(chain)
    check("chain verify passes on an untouched chain", ok, "; ".join(lines))

    tamper_dir = WORK / "tamper"
    tamper_dir.mkdir(exist_ok=True)
    shutil.copy(light_pdf, tamper_dir / led["artifact_file"])
    (tamper_dir / S.LEDGER_NAME).write_text(json.dumps(led) + "\n")
    with (tamper_dir / led["artifact_file"]).open("ab") as fh:
        fh.write(b"\n% tampered\n")
    ok_t, lines_t = S.verify_chain(tamper_dir / S.LEDGER_NAME)
    check("chain verify REJECTS a tampered artifact", not ok_t,
          next((l for l in lines_t if "altered" in l), "; ".join(lines_t)))

    # ── 8. the second template proves the template axis is real ─────────────
    print()
    print("=" * 76)
    print("6. TEMPLATE AXIS + chromium engine (deck template)")
    print("=" * 76)
    deck_dir = WORK / "deck"
    deck_dir.mkdir(exist_ok=True)
    (deck_dir / "slide.html").write_text(
        "<section class='slide'><h2>Slide two</h2>"
        "<p>deck content here</p></section>")
    deck_spec = {
        "edition": "DECK-001", "edition_date": "2026-09-18",
        "title": "docforge deck", "subtitle": "template axis",
        "template": "deck-16x9", "theme": "light",
        "source": "slide.html", "run_dir": str(deck_dir), "engine": "chromium",
        "gates": {"profile": "print-light", "forbid_paths": True, "expect_pages": 2},
    }
    (deck_dir / "spec.json").write_text(json.dumps(deck_spec, indent=2))
    r_deck = run(["build", str(deck_dir / "spec.json")])
    deck_pdf = deck_dir / "DECK-001.pdf"
    check("deck build succeeded via chromium", r_deck.returncode == 0,
          (r_deck.stdout.strip().splitlines() or ["no output"])[-1])
    if deck_pdf.exists():
        info = subprocess.run(["pdfinfo", str(deck_pdf)],
                              capture_output=True, text=True).stdout
        m = re.search(r"Page size:\s*([\d.]+) x ([\d.]+) pts", info)
        # compare NUMBERS, not substrings — an earlier assertion looked for the
        # literal "842" and failed against a real reading of "841.92"
        w_pt, h_pt = (float(m.group(1)), float(m.group(2))) if m else (0.0, 0.0)
        want_w, want_h = 960.0, 540.0   # 338.67mm x 190.5mm = 13.333in x 7.5in
        check("deck page is genuine 16:9 (960x540pt)", 
              abs(w_pt - want_w) <= 2 and abs(h_pt - want_h) <= 2,
              f"got {w_pt:.1f}x{h_pt:.1f}pt, want {want_w}x{want_h}pt")
        check("deck page is landscape, not A4 portrait", w_pt > h_pt,
              f"{w_pt:.0f}x{h_pt:.0f}pt")
        deck_txt = subprocess.run(["pdftotext", str(deck_pdf), "-"],
                                  capture_output=True, text=True).stdout
        check("no browser furniture leaked (no file:/// in text layer)",
              "file:///" not in deck_txt)

    # ── summary ─────────────────────────────────────────────────────────────
    print()
    print("=" * 76)
    print(f"RESULT  {PASS} passed, {FAIL} failed")
    if FAILURES:
        print("FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
    print("=" * 76)
    print("VERDICT:", "the lane holds its negatives" if not FAIL
          else "CONTROL LOST — a negative started passing")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
