#!/usr/bin/env python3
"""Structural pre-send check for an HTML artifact, without a browser.

    python3 verify-html-artifact.py ARTIFACT.html [options]

Options
    --min-words N      fail if the visible word count is below N (default 0 = no floor)
    --max-words N      fail if the visible word count is above N (default 0 = no ceiling)
    --expect TEXT      fail unless TEXT appears in the visible text (repeatable)
    --forbid TEXT      fail if TEXT appears in the visible text (repeatable)
    --allow-internal   disable the built-in house-furniture forbidden list
    --class NAME       report the element count for class="NAME" (repeatable, informational)
    --quiet            print only the failure lines

Exit 0 when every check passes, 1 otherwise, so it composes into a build gate.

Why this exists: a real browser render is the strongest check, but it is not always available
in the session building the artifact. This runs on the source file with the standard library
only and catches what page counts and eyeballing miss: tags left unclosed by a hand-edited
layout, a block that silently failed to render, and internal vocabulary that leaked into text
a human will read. It is a complement to a render, not a replacement -- when a browser is
reachable, render and look at the pages as well.
"""

import argparse
import re
import sys
from html.parser import HTMLParser

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr",
    "path", "rect", "circle", "line", "ellipse", "polygon", "polyline", "stop", "use",
}

# Vocabulary that is payload for an internal reader and a leak for an outside one.
HOUSE_FURNITURE = [
    "DITEMPA", "arifOS", "federation", "Federation", "VAULT999", "vault999",
    "APEX-ZEN", "MCP", "organ bridge",
]


class Structure(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.classes = {}
        self.skip = 0
        self.text = []
        self.headings = []
        self._in_heading = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag not in VOID:
            self.stack.append(tag)
        for token in (dict(attrs).get("class") or "").split():
            self.classes[token] = self.classes.get(token, 0) + 1
        if tag in ("h1", "h2", "h3"):
            self._in_heading = True

    def handle_startendtag(self, tag, attrs):
        for token in (dict(attrs).get("class") or "").split():
            self.classes[token] = self.classes.get(token, 0) + 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in ("h1", "h2", "h3"):
            self._in_heading = False
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            self.errors.append(
                "</%s> closes while <%s> is still open" % (tag, self.stack[-1])
            )
            while self.stack and self.stack.pop() != tag:
                pass
        else:
            self.errors.append("stray </%s> with nothing open" % tag)

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        if self._in_heading and data.strip():
            self.headings.append(data.strip())


class Report:
    def __init__(self):
        self.failures = []
        self.notes = []

    def check(self, ok, message):
        (self.notes if ok else self.failures).append(message)
        return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description="Browser-free structural check for an HTML artifact.")
    ap.add_argument("path")
    ap.add_argument("--min-words", type=int, default=0)
    ap.add_argument("--max-words", type=int, default=0)
    ap.add_argument("--expect", action="append", default=[])
    ap.add_argument("--forbid", action="append", default=[])
    ap.add_argument("--allow-internal", action="store_true")
    ap.add_argument("--class", dest="classes", action="append", default=[])
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    try:
        src = open(args.path, encoding="utf-8").read()
    except OSError as exc:
        print("FAIL: cannot read %s: %s" % (args.path, exc))
        return 1

    parser = Structure()
    parser.feed(src)
    parser.close()

    visible = re.sub(r"\s+", " ", " ".join(parser.text)).strip()
    words = len(visible.split())

    rep = Report()

    rep.check(not parser.stack, "unclosed at EOF: %s" % (parser.stack or "none"))
    rep.check(not parser.errors, "tag nesting: %s" % (parser.errors[:5] or "clean"))
    rep.notes.append("visible words: %d" % words)
    rep.notes.append("headings: %d" % len(parser.headings))

    if args.min_words:
        rep.check(words >= args.min_words, "word floor %d (got %d)" % (args.min_words, words))
    if args.max_words:
        rep.check(words <= args.max_words, "word ceiling %d (got %d)" % (args.max_words, words))

    for name in args.classes:
        rep.notes.append('class="%s": %d' % (name, parser.classes.get(name, 0)))

    for needle in args.expect:
        rep.check(needle in visible, "expected text present: %r" % needle)

    forbidden = list(args.forbid)
    if not args.allow_internal:
        forbidden += HOUSE_FURNITURE
    for needle in forbidden:
        rep.check(needle not in visible, "forbidden text absent: %r" % needle)

    if not args.quiet:
        for note in rep.notes:
            print("ok   %s" % note)
    for failure in rep.failures:
        print("FAIL %s" % failure)

    if rep.failures:
        print("\n%d check(s) failed: %s" % (len(rep.failures), args.path))
        return 1
    print("\nall checks passed: %s" % args.path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
