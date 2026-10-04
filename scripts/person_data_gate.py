#!/usr/bin/env python3
"""
PERSON-DATA GATE — stop Malaysian NRIC and person-registry content reaching a remote.

Forged 2026-10-04 by FI-003 under F13 directive "bina person-data gate", after a privacy
audit of the then-public ariffazil/AAA found 5 real third-party NRICs bound to full names
(a tenant, a landlord, a 67-year-old patient, and two family-court litigants with home
addresses), a named person's GERD diagnosis, and registries/persons.yaml published despite
declaring "local-only, no GitHub push" three times in its own header.

WHY THIS GATE EXISTS
    A declaration in a file header is a comment, not a control. Nothing in the 53-check
    pre-commit chain inspected person data, so `storage: local-only` was honoured by
    nobody. This is the mechanical enforcement of that declaration.

DESIGN CONSTRAINTS (each one earned from the audit, not chosen aesthetically)

  1. Precision over recall. A naive `[0-9]{6}-[0-9]{2}-[0-9]{4}` scan of this repo returns
     26,565 matches, of which 26,560 are binary coincidences in mcp/filings/cache/*.bin
     (e.g. `320193-20-0000` x1,590). A gate that cries wolf on every commit gets
     --no-verify'd within a week. Validating the embedded date and the place-of-birth code
     reduces that to exactly the 5 real NRICs — 0 false positives, measured.

  2. Text extensions only. `-I` (skip binary) is NOT sufficient: the .bin cache files are
     mostly printable and survive it. The extension allowlist is what actually kills them.

  3. Scan the staged diff, not the working tree. The five existing NRICs are already in
     2,874 commits of history; blocking every commit that touches those files would make
     the gate an obstruction rather than a control, and the obstruction always loses.
     Only ADDED lines block. Editing an existing file without re-adding the number passes.

  4. Never print the secret. Output is masked (8509xx-xx-6217) and tokens are shown as
     bot_id + sha8. A gate that leaks what it is meant to catch is worse than no gate.

  5. Path-relative and no-op elsewhere. This hook is shared by AAA, A-FORGE, GEOX, WEALTH
     and WELL. Protected paths are repo-relative, so the gate is silent in repos that have
     no person registry.

MODES
    --staged    default; what the pre-commit hook runs. Staged diff + staged path list.
    --path F    scan one file (for investigation)
    --all       audit the whole HEAD tree. Reports; exits non-zero if anything is found.
                NOT for the hook — see constraint 3.
    --self-test run the built-in positive/negative cases
"""
import calendar
import hashlib
import re
import subprocess
import sys
from pathlib import Path

# ── detection ────────────────────────────────────────────────────────────────
NRIC_RE = re.compile(r"(?<!\d)(\d{2})(\d{2})(\d{2})-(\d{2})-(\d{4})(?!\d)")
BOT_TOKEN_RE = re.compile(r"(?<!\d)(\d{8,10}):AA[A-Za-z0-9_-]{33,}(?![A-Za-z0-9_-])")

# Malaysian place-of-birth codes actually issued: 01-59 states, 71-85 federal
# territories and non-state, 90-99 special/foreign. Anything outside is not an NRIC.
PB_VALID = set(range(1, 60)) | set(range(71, 86)) | set(range(90, 100))

TEXT_EXTENSIONS = {
    ".md", ".markdown", ".txt", ".rst", ".html", ".htm", ".css",
    ".yaml", ".yml", ".json", ".jsonl", ".toml", ".ini", ".cfg", ".conf",
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".sh", ".bash",
    ".csv", ".tsv", ".sql", ".env", ".tex", ".xml",
}

# Repo-relative paths that must never be staged to a remote. Glob-style.
PROTECTED_PATHS = [
    "registries/persons.yaml",
    "federation/person-register.json",
    "audio/voice-registry.json",
    "audio/VOICE-MAP-*",
    "knowledge-graph/identity-topology.md",
]

ALLOWLIST = Path("registries/person_data_allowlist.json")


def mask_nric(value: str) -> str:
    return f"{value[:4]}xx-xx-{value[-4:]}"


def mask_token(value: str) -> str:
    bot_id = value.split(":")[0]
    return f"bot_id={bot_id} sha8={hashlib.sha256(value.encode()).hexdigest()[:8]}"


def plausible_nric(groups) -> bool:
    """Validate the embedded birth date and place-of-birth code.

    This is what separates 5 real NRICs from 26,560 binary coincidences.
    """
    yy, mm, dd, pb, ssss = (int(g) for g in groups)
    if not 1 <= mm <= 12:
        return False
    if dd < 1:
        return False
    # A 2-digit year is ambiguous between centuries; accept either, so 29 Feb is valid
    # for a leap year in one of them.
    if not any(dd <= calendar.monthrange(c + yy, mm)[1] for c in (1900, 2000)):
        return False
    if pb not in PB_VALID:
        return False
    return 1 <= ssss <= 9999


def load_allowlist() -> set:
    """Documented synthetic values permitted as fixtures. Empty by default.

    An entry needs a reason and an approver. A real person's NRIC is never
    allowlisted — the fixture must be replaced with a synthetic number instead.
    """
    if not ALLOWLIST.is_file():
        return set()
    try:
        import json
        data = json.loads(ALLOWLIST.read_text())
        entries = data.get("allow", [])
        out = set()
        for e in entries:
            if e.get("synthetic") is True and e.get("reason") and e.get("approved_by"):
                out.add(e["value"])
        return out
    except Exception:
        return set()  # fail toward scanning everything, never toward skipping


def scan_text(text: str, allow: set):
    """Return (nrics, tokens) found in a blob of text."""
    nrics, tokens = [], []
    for m in NRIC_RE.finditer(text):
        val = m.group(0)
        if val in allow:
            continue
        if plausible_nric(m.groups()):
            nrics.append((val, m.start()))
    for m in BOT_TOKEN_RE.finditer(text):
        if m.group(0) not in allow:
            tokens.append(m.group(0))
    return nrics, tokens


def is_text_path(path: str) -> bool:
    p = Path(path)
    if p.suffix.lower() in TEXT_EXTENSIONS:
        return True
    # extensionless but conventionally text
    return p.name in {"Makefile", "Dockerfile", "LICENSE", "README", "AGENTS", "SOUL"}


def run(args, timeout=240):
    """Run a git command. Returns (stdout, returncode).

    Fail-closed contract: a non-zero exit is NOT the same as an empty result. The first
    version of this gate returned "" on any git error, so a bogus rev made the audit mode
    print nothing and exit 0 — a guard reporting clean because it could not observe its
    own failure. Callers must check the returncode.
    """
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return p.stdout, p.returncode
    except subprocess.TimeoutExpired:
        return "", 124


def run_or_die(args, what, timeout=240):
    out, rc = run(args, timeout)
    if rc != 0:
        print(f"PERSON-DATA GATE [FAIL-CLOSED]: {what} failed (rc={rc}). "
              f"Refusing to report clean on an unreadable input.", file=sys.stderr)
        sys.exit(1)
    return out


def repo_root() -> str:
    out, rc = run(["git", "rev-parse", "--show-toplevel"])
    if rc != 0 or not out.strip():
        print("PERSON-DATA GATE [FAIL-CLOSED]: not inside a git repository.", file=sys.stderr)
        sys.exit(1)
    return out.strip()


def match_protected(path: str) -> bool:
    from fnmatch import fnmatch
    return any(fnmatch(path, pat) for pat in PROTECTED_PATHS)


# ── modes ────────────────────────────────────────────────────────────────────
def check_staged():
    """Scan the staged diff. Only ADDED lines and newly-staged protected paths block."""
    allow = load_allowlist()
    violations = []

    names = run_or_die(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                       "reading the staged file list").splitlines()
    for path in [n.strip() for n in names if n.strip()]:
        if match_protected(path):
            violations.append(("PROTECTED-PATH", path, "",
                               "person registry must never be staged to a remote"))

    diff = run_or_die(["git", "diff", "--cached", "-U0", "--diff-filter=ACM"],
                      "reading the staged diff")
    current = None
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
            continue
        if line.startswith("+++") or not line.startswith("+"):
            continue
        if not current or not is_text_path(current):
            continue
        content = line[1:]
        nrics, tokens = scan_text(content, allow)
        for val, _ in nrics:
            violations.append(("NRIC", current, mask_nric(val),
                               "plausible Malaysian NRIC in added content"))
        for val in tokens:
            violations.append(("BOT-TOKEN", current, mask_token(val),
                              "Telegram bot token in added content"))
    return violations


def check_path(target: str):
    allow = load_allowlist()
    p = Path(target)
    if not p.is_file():
        print(f"PERSON-DATA GATE [FAIL-CLOSED]: not a file: {target}", file=sys.stderr)
        sys.exit(1)
    try:
        text = p.read_text(errors="replace")
    except OSError as exc:
        print(f"PERSON-DATA GATE [FAIL-CLOSED]: unreadable: {exc}", file=sys.stderr)
        sys.exit(1)
    nrics, tokens = scan_text(text, allow)
    out = []
    if match_protected(str(target)):
        out.append(("PROTECTED-PATH", str(target), "", "person registry"))
    for val, _ in nrics:
        out.append(("NRIC", str(target), mask_nric(val), "plausible Malaysian NRIC"))
    for val in tokens:
        out.append(("BOT-TOKEN", str(target), mask_token(val), "Telegram bot token"))
    return out


def check_all(rev="HEAD"):
    """Audit mode over a whole tree. Reports; not intended for the hook (see constraint 3)."""
    allow = load_allowlist()
    # git grep exits 1 when it finds NO match — that is a clean result, not an error.
    # Only rc > 1 is a real failure, and that must fail closed rather than report clean.
    out, rc = run(["git", "grep", "-I", "-n", "-E",
                   r"[0-9]{6}-[0-9]{2}-[0-9]{4}|[0-9]{8,10}:AA[A-Za-z0-9_-]{33,}", rev, "--"] +
                  [f"*{e}" for e in sorted(TEXT_EXTENSIONS)])
    if rc > 1:
        print(f"PERSON-DATA GATE [FAIL-CLOSED]: git grep over {rev} failed (rc={rc}).",
              file=sys.stderr)
        sys.exit(1)
    found = []
    for line in out.splitlines():
        parts = line.split(":", 3)
        if len(parts) < 4:
            continue
        _, path, lineno, content = parts
        nrics, tokens = scan_text(content, allow)
        for val, _ in nrics:
            found.append(("NRIC", f"{path}:{lineno}", mask_nric(val),
                          "plausible Malaysian NRIC"))
        for val in tokens:
            found.append(("BOT-TOKEN", f"{path}:{lineno}", mask_token(val),
                          "Telegram bot token"))
    return found


def report(violations, label):
    seen = set()
    for kind, where, value, why in violations:
        key = (kind, where, value)
        if key in seen:
            continue
        seen.add(key)
        if kind == "PROTECTED-PATH":
            print(f"PERSON-DATA GATE [BLOCK]: {where} — {why}. "
                  f"This file declares itself local-only; it must not reach a remote.",
                  file=sys.stderr)
        else:
            print(f"PERSON-DATA GATE [BLOCK]: {kind} {value} in {where} — {why}. "
                  f"Redact it, or replace a test fixture with a synthetic number.",
                  file=sys.stderr)
    return len(seen)


def self_test():
    """Positive and negative arms. The negative arm is the one that matters:
    a gate that blocks everything is not a control, it is an obstruction.

    Every fixture below is SYNTHETIC and registered in registries/person_data_allowlist.json.
    The audit that motivated this gate found a real third-party NRIC used as the test
    fixture for a PII-redaction control — the control meant to stop leaks was demonstrated
    with leaked data. This file does not repeat that mistake.
    """
    allow = set()
    cases = [
        # (text, expect_nric_count, label)
        ("| Tenant | Someone bin Example (NRIC 990101-14-5001) |", 1, "synthetic NRIC in a tenancy-shaped table"),
        ("No. K/P: 880229-10-5002<br>", 1, "synthetic NRIC in a legal-notice shape (leap day)"),
        ("IC 700315-02-5003, age 67", 1, "synthetic NRIC beside an age"),
        ("binary coincidence 320193-20-0000", 0, "day 93 is not a date"),
        ("binary coincidence 193125-13-4165", 0, "month 31 is not a month"),
        ("binary coincidence 628280-16-0203", 0, "month 82 is not a month"),
        ("binary coincidence 140361-26-0353", 0, "day 61 is not a date"),
        ("version 202601-15-1234", 0, "month 15 is not a month"),
        ("metric G=0.2811 P=0.8409", 0, "metric decimals, no dashes"),
        ("latitude=5.4141&longitude=100.3288", 0, "coordinates are not NRICs"),
        ("bot 1234567890:AASyntheticSelfTestValueNotARealToken00 here", 0, "bot token, not an NRIC"),
        ("order id 250905-14-5009", 1, "shape-valid: the gate is deliberately shape-based"),
    ]
    fails = 0
    print("PERSON-DATA GATE self-test (all fixtures synthetic)")
    for text, expect, label in cases:
        nrics, tokens = scan_text(text, allow)
        got = len(nrics)
        ok = got == expect
        if not ok:
            fails += 1
        print(f"  {'PASS' if ok else 'FAIL'}  nric={got} expect={expect}  {label}")
    # token arm
    SYN_TOKEN = "1234567890:AASyntheticSelfTestValueNotARealToken00"
    _, toks = scan_text(f"curl https://api.telegram.org/bot{SYN_TOKEN}/getUpdates", allow)
    tok_ok = len(toks) == 1
    if not tok_ok:
        fails += 1
    print(f"  {'PASS' if tok_ok else 'FAIL'}  bot-token detected={len(toks)} expect=1")
    _, toks2 = scan_text("bot 123:notavalidtoken", allow)
    tok2_ok = len(toks2) == 0
    if not tok2_ok:
        fails += 1
    print(f"  {'PASS' if tok2_ok else 'FAIL'}  malformed token ignored={len(toks2)} expect=0")
    # allowlist arm — a registered synthetic fixture must be skipped
    _, toks3 = scan_text(f"bot {SYN_TOKEN}", {SYN_TOKEN})
    allow_ok = len(toks3) == 0
    if not allow_ok:
        fails += 1
    print(f"  {'PASS' if allow_ok else 'FAIL'}  allowlisted value skipped={len(toks3)} expect=0")
    # protected-path arm
    prot_ok = match_protected("registries/persons.yaml") and not match_protected("registries/skills.yaml")
    if not prot_ok:
        fails += 1
    print(f"  {'PASS' if prot_ok else 'FAIL'}  protected-path match is specific, not greedy")
    # masking arm — the gate must never emit the value it caught
    masked = mask_nric("990101-14-5001")
    mask_ok = "990101-14-5001" not in masked and masked == "9901xx-xx-5001"
    if not mask_ok:
        fails += 1
    print(f"  {'PASS' if mask_ok else 'FAIL'}  output is masked ({masked})")
    print(f"\n  {fails} failure(s)")
    sys.exit(1 if fails else 0)


def main(argv):
    if "--self-test" in argv:
        self_test()
        return
    root = repo_root()
    import os
    os.chdir(root)

    if "--path" in argv:
        target = argv[argv.index("--path") + 1]
        violations = check_path(target)
        label = f"path {target}"
    elif "--all" in argv:
        i = argv.index("--all")
        rev = argv[i + 1] if len(argv) > i + 1 and not argv[i + 1].startswith("-") else "HEAD"
        violations = check_all(rev)
        label = f"full tree at {rev}"
    else:
        violations = check_staged()
        label = "staged diff"

    if violations:
        n = report(violations, label)
        kinds = sorted({v[0] for v in violations})
        print(f"PERSON-DATA GATE [BLOCK]: {n} finding(s) ({', '.join(kinds)}) in {label}.",
              file=sys.stderr)
        sys.exit(1)

    if "--all" not in argv:
        print("PERSON-DATA GATE [PASS]: no NRIC, bot token, or person-registry path in "
              f"{label} ({len(PROTECTED_PATHS)} protected paths watched)")


if __name__ == "__main__":
    main(sys.argv[1:])
