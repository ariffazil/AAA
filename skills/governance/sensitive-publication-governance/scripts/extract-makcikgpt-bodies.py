#!/usr/bin/env python3
"""extract-makcikgpt-bodies.py — dump arifOS article bodies to plain text.

WHY THIS EXISTS
  The canonical articles live as TypeScript modules under
  sites/arif-fazil.com/src/data/makcikgpt/*.ts. The body is an HTML template literal, and
  reading a whole corpus (~35 files, ~57k words) by hand is neither fast nor auditable. This
  dumps every body to text so the corpus can be swept, diffed, batched, or handed to
  parallel readers.

THE TWO-SHAPE PITFALL (the reason this script exists)
  The .ts files store the body in TWO different shapes:

      html: `<article ...>`            # object-property shape
      const html = `<article ...>`     # module-const shape

  A scanner anchored only on `html:` silently drops every const-shape file. In the live
  corpus that was 30 of 35 files and ~280k chars, reported as success. ALWAYS match both
  anchors, and ALWAYS print the extracted count against the source count — a partial
  extraction is otherwise invisible and produces a confidently incomplete audit.

ESCAPE-AWARE SCAN
  Walk forward from the opening delimiter honouring backslash escapes and stop at the first
  UNESCAPED backtick. Splitting on backticks naively truncates any article containing a
  literal backtick.

USAGE
  python3 extract-makcikgpt-bodies.py
  python3 extract-makcikgpt-bodies.py --src DIR --out DIR --batches 5

  --batches N spreads files round-robin into <out>/../batches/b1..bN/, the shape to hand to
  N parallel readers when auditing the whole corpus: each reader gets a small context and
  its findings stay independent of the others'.

OUTPUT
  <out>/<slug>.txt for every article, plus manifest.json ({file, slug, chars}).
"""
import argparse
import glob
import html as htmllib
import json
import os
import re
import shutil

DEFAULT_SRC = "/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt"
DEFAULT_OUT = os.path.expanduser("~/forge_work/makcikgpt-bodies/extracted")

SKIP = {"index.ts", "types.ts"}
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"[ \t]+")
BLANK = re.compile(r"\n{3,}")

# BOTH anchors. Anchoring on only the first silently drops the const-shape files.
ANCHOR = re.compile(r"\bhtml\s*:\s*|\bconst\s+html\s*=\s*")


def strip_html(s: str) -> str:
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</(p|div|h[1-6]|li|tr|td|th|blockquote)>", "\n", s, flags=re.I)
    s = TAG.sub(" ", s)
    s = htmllib.unescape(s)
    s = WS.sub(" ", s)
    s = "\n".join(line.strip() for line in s.split("\n"))
    return BLANK.sub("\n\n", s).strip()


def body_of(raw: str):
    """Return (body, None) or (None, reason). Escape-aware template-literal scan."""
    m = ANCHOR.search(raw)
    if not m:
        return None, "no html anchor"
    i = m.end()
    while i < len(raw) and raw[i] in " \t\n\r":
        i += 1
    if i >= len(raw):
        return None, "anchor at eof"
    q = raw[i]
    if q not in "`'\"":
        return None, "unexpected delimiter %r" % q
    i += 1
    out = []
    while i < len(raw):
        c = raw[i]
        if c == "\\":
            out.append(raw[i:i + 2])
            i += 2
            continue
        if c == q:
            break
        out.append(c)
        i += 1
    body = "".join(out)
    return body.replace("\\`", "`").replace("\\'", "'").replace('\\"', '"'), None


def slug_of(raw: str, fallback: str) -> str:
    m = re.search(r"slug\s*:\s*['\"`]([^'\"`]+)['\"`]", raw)
    return m.group(1) if m else fallback


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--batches", type=int, default=0)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    good, bad = [], []

    source_count = len([f for f in glob.glob(os.path.join(args.src, "*.ts"))
                        if os.path.basename(f) not in SKIP])

    for path in sorted(glob.glob(os.path.join(args.src, "*.ts"))):
        base = os.path.basename(path)
        if base in SKIP:
            continue
        raw = open(path, encoding="utf-8").read()
        body, err = body_of(raw)
        if body is None:
            bad.append((base, err))
            continue
        slug = slug_of(raw, base[:-3])
        text = strip_html(body)
        open(os.path.join(args.out, slug + ".txt"), "w", encoding="utf-8").write(text)
        good.append({"file": base, "slug": slug, "chars": len(text)})

    total_chars = sum(g["chars"] for g in good)
    words = 0
    for g in good:
        with open(os.path.join(args.out, g["slug"] + ".txt"), encoding="utf-8") as fh:
            words += len(fh.read().split())

    # Always print extracted-vs-source. A silent partial extraction looks like success.
    print("EXTRACTED %d/%d files · %d chars · ~%d words"
          % (len(good), source_count, total_chars, words))
    if bad:
        print("FAILED:")
        for base, err in bad:
            print("   %s — %s" % (base, err))
    if len(good) != source_count:
        print("WARNING: count mismatch — an anchor is missing from this script's ANCHOR regex,"
              " or a file stores the body in a third shape. Inspect the failed files above.")

    with open(os.path.join(args.out, os.pardir, "manifest.json"), "w") as fh:
        json.dump(good, fh, indent=2)

    if args.batches:
        bdir = os.path.join(args.out, os.pardir, "batches")
        if os.path.isdir(bdir):
            shutil.rmtree(bdir)
        for i in range(args.batches):
            d = os.path.join(bdir, "b%d" % (i + 1))
            os.makedirs(d, exist_ok=True)
            for g in good[i::args.batches]:
                shutil.copy2(os.path.join(args.out, g["slug"] + ".txt"), d)
        print("batched into %s/b1..b%d" % (bdir, args.batches))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
