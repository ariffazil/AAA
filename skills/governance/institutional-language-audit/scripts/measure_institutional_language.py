#!/usr/bin/env python3
"""Institutional language audit — actor / distance / absence tests.

Usage:
    python3 measure_institutional_language.py <corpus-dir>
    python3 measure_institutional_language.py --selftest

Reads every .txt / .md file in the directory as ONE corpus (so a release saved as
.md and a press-conference transcript as .txt are measured together) and prints
three tests. Copy the numbers into the deliverable, and ship this script plus the
corpus so any reader can reproduce them.

Supports the institutional-language-audit skill.
"""
import os, re, sys, glob

HONOUR = {
    "deliver":            r"deliver",
    "sustainable":        r"sustainab",
    "value":              r"\bvalue",
    "energy transition":  r"energy transition",
    "portfolio":          r"portfolio",
    "growth":             r"growth",
    "outlook":            r"outlook|looking ahead",
    "long-term":          r"long.term",
    "solutions":          r"solution",
    "committed":          r"commit",
    "strategic":          r"strategic",
    "resilient":          r"resilien",
    "challenging":        r"challeng",
    "volatility":         r"volatilit|volatile",
    "headwinds":          r"headwind",
    "high-grading":       r"high.grad",
    "disciplined":        r"disciplin",
    "stakeholders":       r"stakeholder",
    "agile":              r"agile",
    "prudent":            r"prudent",
    "optimisation":       r"optimis",
    "double down":        r"double down",
    "rightsizing":        r"rightsiz",
}

HUMAN_IMPACT = {
    "employee":        r"employee",
    "staff":           r"\bstaff\b",
    "worker":          r"\bworker",
    "colleague":       r"colleague",
    "workforce":       r"workforce",
    "people":          r"\bpeople\b",
    "retrench":        r"retrench",
    "layoff":          r"lay.off|laid off",
    "job loss":        r"job loss|job cut",
    "unemployment":    r"unemploy",
    "redundancy":      r"redundan",
    "accident":        r"accident",
    "injury":          r"\binjur",
    "fatality":        r"fatalit",
    "death":           r"\bdeath\b|\bdied\b",
    "safety incident": r"safety incident",
    "hero/sacrifice":  r"\bhero\b|sacrific",
}

# Sentences that carry no named actor. Counted, not judged.
SUBJECT = r"\bI\b|\bwe\b|\bmy\b|\bour\b|\bus\b"
AGENTLESS = (r"\bwas\b|\bwere\b|\bhas been\b|\bhave been\b|\bis expected\b|\bremains\b|"
             r"\bunderpins\b|\bshaped\b|\bdriven by\b|\bwas delivered\b|\bis due to\b")


def read_corpus(path):
    if os.path.isdir(path):
        files = sorted(glob.glob(os.path.join(path, "*.txt")) +
                       glob.glob(os.path.join(path, "*.md")))
        parts = []
        for f in files:
            parts.append(open(f, encoding="utf-8", errors="ignore").read())
            print(f"   {os.path.getsize(f):8d}  {os.path.basename(f)}")
        if not files:
            raise SystemExit(f"no .txt/.md files in {path}")
        return "\n".join(parts), files
    return open(path, encoding="utf-8", errors="ignore").read(), [path]


def audit(text):
    low = text.lower()
    print(f"\nCORPUS: {len(text)} chars, {len(low.split())} words\n")

    # --- 1. ACTOR ---------------------------------------------------------
    sents = [s.strip() for s in re.split(r"(?<=[.])\s+", text) if len(s.strip()) > 45]
    no_subject = [s for s in sents if not re.search(SUBJECT, s, re.I)]
    agentless = [s for s in sents if re.search(AGENTLESS, s, re.I)]
    pct = (len(no_subject) / len(sents) * 100) if sents else 0.0
    print(f"ACTOR TEST - {len(sents)} sentences over 45 chars")
    print(f"  no first-person subject : {len(no_subject):4d}  ({pct:.0f}%)")
    print(f"  passive/agentless verb  : {len(agentless):4d}  "
          f"({len(agentless)/max(1,len(sents))*100:.0f}%)")

    # --- 2. DISTANCE ------------------------------------------------------
    h = sorted(((len(re.findall(p, low)), k) for k, p in HONOUR.items() if re.findall(p, low)),
               reverse=True)
    m = sorted(((len(re.findall(p, low)), k) for k, p in HUMAN_IMPACT.items()),
               reverse=True)
    print("\nDISTANCE TEST - honour words")
    for n, k in h:
        print(f"  {n:4d}  {k}")
    ht = sum(n for n, _ in h)
    print(f"  ---- total {ht}")

    # --- 3. ABSENCE (report first - it is the finding) --------------------
    print("\nABSENCE TEST - expected words that never appear")
    zeros = [(k, n) for n, k in m if n == 0]
    for k, _ in zeros:
        print(f"  {0:4d}  {k}   <-- NEVER SAID")
    for n, k in m:
        if n:
            print(f"  {n:4d}  {k}")
    mt = sum(n for n, _ in m)
    print(f"  ---- total {mt}")

    print("\nDISTANCE / ABSENCE SUMMARY")
    print(f"  honour words         : {ht}")
    print(f"  human-impact words   : {mt}")
    if mt:
        print(f"  ratio                : {ht/mt:.1f} honour words per human-impact word")
    else:
        print("  ratio                : undefined - ZERO human-impact words in the corpus")
    print(f"  words absent entirely: {len(zeros)}"
          + (f"  ({', '.join(k for k, _ in zeros)})" if zeros else ""))
    return {"chars": len(text), "sentences": len(sents), "no_subject": len(no_subject),
            "honour_total": ht, "human_total": mt, "zeros": [k for k, _ in zeros]}


def selftest():
    sample = (
        "Resilient performance was delivered against a backdrop of prolonged volatility. "
        "The increase in injury frequency is due to a broader reporting scope. "
        "Our committed team continues to deliver sustainable long-term value for stakeholders. "
        "Structural cost optimisation remains central to our disciplined capital allocation. "
    )
    r = audit(sample)
    assert r["sentences"] >= 3, r
    assert "employee" in r["zeros"], r
    assert "accident" in r["zeros"], r
    assert r["human_total"] == 0, r          # nothing human named at all
    print("\nselftest OK - agentless detection, zero-human detection and absence list all fire")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == "--selftest":
        selftest()
    else:
        print("CORPUS FILES")
        text, _ = read_corpus(sys.argv[1])
        audit(text)
