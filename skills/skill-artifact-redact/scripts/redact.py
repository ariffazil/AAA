#!/usr/bin/env python3
"""redact.py — one redaction boundary for captured text.

Contract:
  * never prints a matched secret (class + length only)
  * --check exits 1 when any class matches (the write gate)
  * default mode writes redacted text to stdout

Usage:
  redact.py [FILE ...]          # redacted copy to stdout (stdin if no FILE)
  redact.py --check [FILE ...]  # gate: exit 1 if a secret class is present
  redact.py --in-place FILE ... # rewrite files with redaction (creates .bak)
"""
import re
import sys
from pathlib import Path

PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
    re.S,
)

PATTERNS = [
    ("private_key", PRIVATE_KEY),
    ("aws_session_token", re.compile(r"(X-Amz-Security-Token=)(?!<REDACTED>)[^&\s\"']+")),
    ("presigned_sig", re.compile(r"(X-Amz-(?:Credential|Signature)=)(?!<REDACTED>)[^&\s\"']+")),
    ("google_sig", re.compile(r"(X-Goog-Signature=)(?!<REDACTED>)[^&\s\"']+")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}")),
    ("github_token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("aws_access_key_id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("telegram_bot_token", re.compile(r"\b\d{8,10}:[A-Za-z0-9_\-]{35}\b")),
    ("bearer", re.compile(r"(Bearer\s+)(?!<REDACTED>)[A-Za-z0-9._\-]{16,}")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("assigned_secret", re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password|passwd|pwd)(\s*[:=]\s*)(?!<REDACTED>)\S{8,}")),
    ("cookie", re.compile(r"(?i)\b(set-cookie|cookie|sessionid|sid)(\s*:\s*)\S{12,}")),
]


def redact(text):
    hits = []
    for name, rx in PATTERNS:
        def _sub(m, _name=name):
            kept = "".join(g for g in m.groups() if g) if m.groups() else ""
            hits.append((_name, len(m.group(0))))
            return f"{kept}<REDACTED>" if kept else "<REDACTED>"
        text = rx.sub(_sub, text)
    return text, hits


def main(argv):
    check = "--check" in argv
    inplace = "--in-place" in argv
    paths = [a for a in argv if not a.startswith("--")]
    sources = [Path(p) for p in paths]
    rc = 0

    if not sources:
        data = sys.stdin.read()
        out, hits = redact(data)
        for name, ln in hits:
            print(f"REDACTED[{name}] len={ln}", file=sys.stderr)
        if check:
            return 1 if hits else 0
        sys.stdout.write(out)
        return 0

    for p in sources:
        data = p.read_text(errors="replace")
        out, hits = redact(data)
        for name, ln in hits:
            print(f"{p}: REDACTED[{name}] len={ln}", file=sys.stderr)
        if check:
            if hits:
                rc = 1
            continue
        if inplace:
            if hits:
                bak = p.with_suffix(p.suffix + ".bak")
                if not bak.exists():
                    bak.write_text(data)
                p.write_text(out)
        else:
            sys.stdout.write(out)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
