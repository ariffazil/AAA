#!/usr/bin/env python3
"""Sweep a TypeScript-content corpus for paragraphs carrying publication risk.

Extracts every `html: `...`` template literal from .ts modules, strips HTML to
plain paragraphs, and scores each paragraph against risk classes. Ranks; does not
judge. Read the top hits before writing anything.

Usage:
    python3 sweep-corpus.py <corpus_dir> <out_dir> [--top N]

Outputs (in <out_dir>):
    corpus.jsonl   every paragraph, per file
    flagged.jsonl  scored candidates, with the class tags that fired
"""
import argparse
import glob
import json
import os
import re
from collections import Counter

# Skip list: registry / schema modules, not article bodies.
SKIP = {"index.ts", "types.ts"}

# Broad pass: finds candidates, over-weights well-cited material.
BROAD = [
    ("EMPLOYER", 3, r"\b(company|employer|corp|group|holdings|sdn bhd)\b"),
    ("SECRET_VERB", 4, r"(leak|confidential|internal|proprietary|undisclosed|"
                       r"bocor|rahsia|sulit|dalaman|belum diumum)"),
    ("LEGAL_MATTER", 3, r"(court|litigation|lawsuit|charge|trial|writ|"
                          r"mahkamah|saman|tuduhan|undang-undang)"),
    ("NAMED_SENIOR", 2, r"(CEO|CFO|CTO|Chairman|President|Managing Director|"
                          r"General Manager|Minister|Pengerusi|Menteri|Tan Sri|Datuk|Dato)"),
    ("PROJECT_NAME", 3, r"\b[A-Z]{3,}\b"),
    ("PERSONAL_ATTR", 3, r"(salary|bonus|promotion|appraisal|redundancy|retrench|"
                           r"gaji|naik pangkat|penilaian prestasi|dibuang)"),
    ("FIGURE", 3, r"(\bRM\s?\d[\d,.]*|\d[\d,.]*\s?(%|billion|million|bilion|juta|bn))"),
]

# Narrow pass: the classes that actually carry exposure.
NARROW = [
    ("A_ATTRIBUTED_SPEECH", 5, r"(someone in the room|a source said|an insider said|"
                                 r"seseorang dalam|orang dalam cakap|kata seorang sumber|"
                                 r"menurut seorang sumber|sumber dalaman)"),
    ("B_CAUSAL_INSINUATION", 5, r"(not a coincidence|no accident|deliberate|engineered|"
                                  r"bukan kebetulan|bukan coincidence|sengaja|dirancang|"
                                  r"itu signal|tepat masa|hari yang sama)"),
    ("D_INNUENDO_PERSON", 5, r"(his hand was in|something there|incompetent|corrupt|"
                               r"tangan dia masuk|ada sesuatu|lingkup|gagal|rasuah|sakap)"),
    ("E_INSIDER_STANDING", 4, r"(\bI work\b|I have worked|people inside|we inside|"
                                r"\baku kerja\b|orang dalam|anak buah|staff.*\b(kata|cakap))"),
    ("F_INTERNAL_ARTIFACT", 4, r"(internal dossier|internal report|internal memo|board minutes|"
                                 r"dossier dalaman|laporan dalaman|minit mesyuarat|nota dalaman)"),
]

# Self-attribution: the sentence that converts anonymous voice to named source.
SELF_ATTR = re.compile(
    r"(proprietary intelligence|my employer|anak [A-Z]|oleh [A-Z][a-z]+ [A-Z][a-z]+|"
    r"perisikan proprietari|saya bekerja di|kerja kat|employee of)", re.I)


def extract_literals(path):
    """Pull every `html: `...`` template literal, honouring backslash escapes."""
    src = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(r"html:\s*`", src):
        i, buf = m.end(), []
        while i < len(src):
            c = src[i]
            if c == "\\":
                buf.append(src[i:i + 2])
                i += 2
                continue
            if c == "`":
                break
            buf.append(c)
            i += 1
        out.append("".join(buf))
    return out


def unescape(h):
    for a, b in (("\\`", "`"), ("\\$", "$"), ("\\n", "\n"),
                 ("\\\\", "\\"), ('\\"', '"'), ("\\'", "'")):
        h = h.replace(a, b)
    return h


def strip_html(h):
    h = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", h, flags=re.I)
    h = re.sub(r"<br\s*/?>", "\n", h, flags=re.I)
    h = re.sub(r"</(p|div|h[1-6]|li|tr|section|blockquote)>", "\n", h, flags=re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&quot;", '"'),
                 ("&#39;", "'"), ("&mdash;", "\u2014"), ("&ndash;", "\u2013"),
                 ("&hellip;", "\u2026")):
        h = h.replace(a, b)
    h = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), h)
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--top", type=int, default=60)
    ap.add_argument("--min-len", type=int, default=60)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(args.corpus_dir, "*.ts")))

    corpus, flagged = [], []
    for path in files:
        name = os.path.basename(path)
        if name in SKIP:
            continue
        text = strip_html(unescape("\n\n".join(extract_literals(path))))
        text = re.sub(r"[ \t]+", " ", text)
        paras = [p.strip() for p in text.split("\n") if len(p.strip()) >= args.min_len]
        corpus.append({"file": name, "n": len(paras), "paras": paras})

        for i, p in enumerate(paras):
            broad = [n for n, _, rx in BROAD if re.search(rx, p, re.I)]
            narrow = [n for n, _, rx in NARROW if re.search(rx, p)]
            w = sum(wt for n, wt, rx in BROAD if re.search(rx, p, re.I))
            w += sum(wt for n, wt, rx in NARROW if re.search(rx, p))
            sa = bool(SELF_ATTR.search(p))
            w += 6 if sa else 0
            if narrow or sa:
                flagged.append({"file": name, "i": i, "w": w,
                                "narrow": narrow, "broad": broad,
                                "self_attr": sa, "text": p})

    with open(os.path.join(args.out_dir, "corpus.jsonl"), "w", encoding="utf-8") as f:
        for r in corpus:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    flagged.sort(key=lambda h: (-h["w"], h["file"], h["i"]))
    with open(os.path.join(args.out_dir, "flagged.jsonl"), "w", encoding="utf-8") as f:
        for r in flagged:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"articles: {len(corpus)}")
    print(f"paragraphs: {sum(r['n'] for r in corpus)}")
    print(f"flagged: {len(flagged)}")
    print("\nnarrow-class counts:")
    for k, v in Counter(t for h in flagged for t in h["narrow"]).most_common():
        print(f"  {k:24s} {v}")
    selfattr = [h for h in flagged if h["self_attr"]]
    print(f"\nSELF-ATTRIBUTION hits: {len(selfattr)}  <-- read these first")
    for h in selfattr:
        print(f"  {h['file']} #{h['i']}: {h['text'][:200]}")
    print(f"\ntop {args.top} by weight - read before writing anything:\n")
    for h in flagged[:args.top]:
        print(f"[{h['w']:2d}] {h['file']} #{h['i']}  {'/'.join(h['narrow'])}")
        print(f"     {h['text'][:300]}\n")
    print(f"written: {os.path.join(args.out_dir, 'corpus.jsonl')}")
    print(f"written: {os.path.join(args.out_dir, 'flagged.jsonl')}")


if __name__ == "__main__":
    main()
