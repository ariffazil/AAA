#!/usr/bin/env python3
"""asabiyyah_probe.py — AAA organ substrate reading for the federation cycle instrument.

ORGAN: AAA (doctrine, memory, governance). AAA is the primary HOME of the
ceremony-overload signature: it is the organ whose product *is* the artifact.

Emits one SubstrateReading conforming to
  /root/AAA/schemas/asabiyyah-reading.schema.json
and drops it at /var/lib/arifos/asabiyyah/AAA.json for the kernel aggregator.
The kernel functions are loaded from the shared instrument, never vendored:
  /root/arifOS/arifosmcp/runtime/asabiyyah.py

LAWS THIS FILE OBEYS
  * read-only against the repo. The only write is the drop file (rule 4).
  * every number traces to a real file/glob/DB on disk, named in `source`.
  * a signal with no honest home is NOT_APPLICABLE with a reason, value null.
    No invented numbers. A reading without a source is a STORY, not a MIRROR.
  * `evidence` carries raw ADDITIVE INTEGER counts only. The kernel re-derives
    the ratios; pre-divided ratios would not federate.

THE HEADLINE FINDING (recorded in CER's source, not hidden)
  AAA has NO per-capability invocation telemetry. Nothing on this host records
  that a AAA skill or primitive was invoked. The federation has one live
  tool-invocation table (/var/lib/arifos/apex_metrics.db `tool_calls`, 123k rows)
  but its rows are arifOS kernel verbs by 333-AGI/openclaw-anon/etc. —
  attributing those to AAA would be cross-organ telemetry theft, and would
  flatter AAA. So CER's denominator is the honest AAA-scoped substitute:
  capability units that are wired to a schedule AND corroborated by a receipt
  file written inside the window. That is a strict subset of "capabilities
  invoked", and it is labelled as such.

USAGE
  python3 /root/AAA/scripts/asabiyyah_probe.py             # emit + drop
  python3 /root/AAA/scripts/asabiyyah_probe.py --no-write  # emit only
  python3 /root/AAA/scripts/asabiyyah_probe.py --window-days 7
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import socket
import sqlite3
import sys
import time
from pathlib import Path

KERNEL_PATH = "/root/arifOS/arifosmcp/runtime/asabiyyah.py"
SCHEMA_PATH = "/root/AAA/schemas/asabiyyah-reading.schema.json"
DROP_DIR = "/var/lib/arifos/asabiyyah"
ORGAN = "AAA"

REPO = Path("/root/AAA")

# ---------------------------------------------------------------------------
# CER — ceremony artifacts: the live doctrine stock. Include globs are explicit
# and discriminating; the exclude set is what stops archive from masquerading
# as live doctrine (AAA carries 12+ archive/quarantine dirs).
# ---------------------------------------------------------------------------

DOCTRINE_GLOBS = (
    ("instructions/", REPO / "instructions", "**/*.md"),
    ("governance/", REPO / "governance", "**/*.md"),
    ("canon/", REPO / "canon", "**/*.md"),
    ("docs/", REPO / "docs", "**/*.md"),
    ("schemas/", REPO / "schemas", "**/*.json"),
    ("skills/", REPO / "skills", "**/*.md"),
    ("agents/decisions/", REPO / "agents" / "decisions", "**/*.md"),
)

EXCLUDE_PARTS = {
    "archive",
    "backups",
    "tmp",
    "node_modules",
    "dist",
    "deployments",
    "venv",
    "__pycache__",
}


def _excluded(path: Path) -> bool:
    """Live doctrine never sits in a dotted or archive/quarantine directory.

    Pruning every dot-prefixed part (plus the explicit archive/vendor parts
    below) is AAA's own census convention — /root/scripts/skills-census.py
    prunes `d not in EXCL and not d.startswith('.')` — and adopting it here is
    what makes this reading reconcilable with that live instrument.
    """
    for part in path.parts:
        low = part.lower()
        if low in EXCLUDE_PARTS or part.startswith("."):
            return True
    return False


def count_ceremony_artifacts() -> tuple[int, dict[str, int]]:
    """Live doctrine artifacts, deduped by realpath. Returns (total, per-root)."""
    per_root: dict[str, int] = {}
    seen: set[str] = set()
    total = 0
    for label, root, pattern in DOCTRINE_GLOBS:
        n = 0
        if not root.is_dir():
            per_root[label] = 0
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            here = Path(dirpath)
            dirnames[:] = [d for d in dirnames if not _excluded(here / d)]
            if _excluded(here):
                continue
            for fn in filenames:
                if not fn.endswith(".md") and not (pattern.endswith(".json") and fn.endswith(".json")):
                    continue
                p = here / fn
                try:
                    real = os.path.realpath(p)
                except OSError:
                    continue
                if real in seen:
                    continue
                seen.add(real)
                n += 1
        per_root[label] = n
        total += n
    return total, per_root


# ---------------------------------------------------------------------------
# CER — exercised capabilities. Receipts, not declarations.
# ---------------------------------------------------------------------------

CRON_SOURCES = (
    "/var/spool/cron/crontabs/root",
    "/etc/crontab",
)
CRON_D_DIR = Path("/etc/cron.d")
AAA_SCRIPT_RE = re.compile(r"(/root/AAA/scripts/[A-Za-z0-9_.\-]+)")
LOG_RE = re.compile(r"(/[\w./\-]*\.log)")

# Receipt locations probed per capability unit, beyond the cron line's own
# redirect targets. Named in `source`; nothing here is inferred.
RECEIPT_TEMPLATES = (
    "/var/log/arifos/{stem}.log",
    "/var/log/arifos/{stem_dash}.log",
    "/root/AAA/scripts/logs/{stem}.log",
    "/root/AAA/forge_work/{stem}.log",
)


def _read_cron_text() -> list[str]:
    lines: list[str] = []
    for src in CRON_SOURCES:
        try:
            lines.extend(Path(src).read_text(errors="replace").splitlines())
        except OSError:
            continue
    if CRON_D_DIR.is_dir():
        for f in sorted(CRON_D_DIR.iterdir()):
            if not f.is_file():
                continue
            try:
                lines.extend(f.read_text(errors="replace").splitlines())
            except OSError:
                continue
    return lines


def count_exercised_capabilities(window_days: int) -> tuple[int, dict[str, int], list[str]]:
    """Scheduled AAA capability units corroborated by a fresh receipt file.

    A unit counts only if BOTH hold:
      (a) it is named on a live cron line in a real cron source, and
      (b) at least one receipt file for it has mtime inside the window.
    """
    cutoff = time.time() - window_days * 86400
    lines = _read_cron_text()

    scheduled: dict[str, set[str]] = {}  # script -> candidate receipt paths
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "AAA/scripts/" not in line:
            continue
        scripts = AAA_SCRIPT_RE.findall(line)
        if not scripts:
            continue
        redirects = set(LOG_RE.findall(line))
        for s in scripts:
            # a capability unit must exist on disk; the regex also matches the
            # directory /root/AAA/scripts/logs appearing inside a redirect path
            if not os.path.isfile(s):
                continue
            scheduled.setdefault(s, set()).update(redirects)

    exercised = 0
    fresh_receipts = 0
    stale: list[str] = []
    for script, redirects in sorted(scheduled.items()):
        stem = Path(script).stem
        candidates = set(redirects)
        for t in RECEIPT_TEMPLATES:
            candidates.add(t.format(stem=stem, stem_dash=stem.replace("_", "-")))
        hit = False
        for c in sorted(candidates):
            p = Path(c)
            try:
                if p.is_file() and p.stat().st_mtime >= cutoff:
                    hit = True
                    fresh_receipts += 1
            except OSError:
                continue
        if hit:
            exercised += 1
        else:
            stale.append(Path(script).name)

    detail = {
        "scheduled_capability_units": len(scheduled),
        "fresh_receipt_files": fresh_receipts,
        "stale_capability_units": len(stale),
    }
    return exercised, detail, stale


# ---------------------------------------------------------------------------
# ASD — asabiyyah depth. doctrine_holders vs executors.
# ---------------------------------------------------------------------------


def count_doctrine_holders() -> tuple[int, int]:
    """Live skill directories in AAA's tree — each is a doctrine holder unit.

    Returns (distinct_real_homes, alias_inclusive_entries).

    distinct_real_homes: realpath-deduped. The symlinks under /root/AAA/skills
    are views onto the same doctrine, so counting them twice would overstate
    how widely the doctrine is held.
    alias_inclusive_entries: keys by relative path with followlinks=True — the
    method /root/scripts/skills-census.py uses for its `canonical_skills` field,
    so this number is reconcilable against that live AAA instrument.
    """
    root = REPO / "skills"
    seen_homes: set[str] = set()
    entries: set[str] = set()
    if not root.is_dir():
        return 0, 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        here = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not _excluded(here / d)]
        if _excluded(here):
            continue
        if "SKILL.md" in filenames and os.path.isfile(here / "SKILL.md"):
            entries.add(os.path.relpath(here, root))
            try:
                seen_homes.add(os.path.realpath(here))
            except OSError:
                continue
    return len(seen_homes), len(entries)


def count_executors(window_days: int) -> tuple[int, dict[str, int], list[str]]:
    """Distinct actor identities receipted EXECUTING something in AAA.

    Sources, each counted separately then unioned:
      S1 /root/AAA/state/a4_exceptions.jsonl  — repo=/root/AAA harness commits
      S2 /root/AAA/claim_ledger/claims.db     — claims.recorded_by,
                                                verifications.verifier
    Caveat carried into the metric notes: the A4 `actor` is
    `git config user.name`, a LABEL, not a bound identity.
    """
    cutoff = time.time() - window_days * 86400
    ident: set[str] = set()
    per_source: dict[str, int] = {}

    a4 = REPO / "state" / "a4_exceptions.jsonl"
    a4_actors: set[str] = set()
    if a4.is_file():
        for line in a4.read_text(errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = str(row.get("ts", ""))
            if not _epoch_ok(ts, cutoff):
                continue
            actor = str(row.get("actor") or "").strip()
            if actor:
                a4_actors.add(actor)
    per_source["a4_exception_actors"] = len(a4_actors)
    ident |= a4_actors

    db = REPO / "claim_ledger" / "claims.db"
    led_actors: set[str] = set()
    if db.is_file():
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            for who, ts in con.execute("SELECT recorded_by, recorded_at FROM claims"):
                if _epoch_ok(str(ts), cutoff) and who:
                    led_actors.add(str(who))
            for who, ts in con.execute("SELECT verifier, verified_at FROM verifications"):
                if _epoch_ok(str(ts), cutoff) and who:
                    led_actors.add(str(who))
            con.close()
        except sqlite3.Error:
            pass
    per_source["claim_ledger_actors"] = len(led_actors)
    ident |= led_actors

    return len(ident), per_source, sorted(ident)


def _epoch_ok(ts: str, cutoff: float) -> bool:
    """True when an ISO-8601 timestamp (with or without Z/offset) is >= cutoff."""
    if not ts:
        return False
    raw = ts.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+0000"
    m = re.match(r"^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})", raw)
    if not m:
        return False
    base = f"{m.group(1)}T{m.group(2)}"
    off = 0
    if "+" in raw or raw.count("-") > 2:
        tail = raw[len(base):]
        mo = re.search(r"([+-])(\d{2}):?(\d{2})", tail)
        if mo:
            sign = 1 if mo.group(1) == "+" else -1
            off = sign * (int(mo.group(2)) * 3600 + int(mo.group(3)) * 60)
    try:
        t = time.mktime(time.strptime(base, "%Y-%m-%dT%H:%M:%S")) - off
    except ValueError:
        return False
    return t >= cutoff


# ---------------------------------------------------------------------------
# ENC — enforcement coverage. Which enumerated mutation paths into AAA's
# protected dirs verifiably pass a validator before writing?
#
# The protected-path set is AAA's own declared protection, taken verbatim from
# /root/AAA/scripts/mutation-authority-probe.py PROTECTED (an existing AAA
# instrument — this probe does not duplicate it, it cites it).
#
# Each row: (path name, gated?, on-disk artifact that justifies the verdict).
# A row is gated only if something mechanistically precedes the write.
# ---------------------------------------------------------------------------

PROTECTED_DIRS = (
    "canon/",
    "governance/",
    "schemas/",
    "instructions/",
    "skills/",
    "agent-cards/",
    "registries/",
    "claim_ledger/",
)

ENC_PATHS: tuple[tuple[str, bool, str, str], ...] = (
    (
        "filesystem-direct-write",
        False,
        "plain write (python open()/tee/cp/editor save) by any root-capable process",
        "no interposed validator exists on this host for /root/AAA/canon|governance|schemas|instructions",
    ),
    (
        "git-commit-doctrine-files",
        False,
        "git commit of .md/.json/.yaml under the protected dirs",
        "/root/AAA/.git/hooks/pre-commit symlinks to the LSP gate whose "
        "GATED_EXTENSIONS='ts|tsx|py|js|jsx|mjs' — doctrine extensions are not covered",
    ),
    (
        "git-commit-code-files",
        True,
        "git commit of .py/.ts/.js staged under the protected dirs",
        "/root/AAA/.git/hooks/pre-commit -> /root/A-FORGE/hooks/pre-commit-lsp-gate.sh "
        "(present and executable; blocks on LSP errors)",
    ),
    (
        "git-commit-no-verify",
        False,
        "git commit --no-verify on any staged content",
        "git's own --no-verify flag; nothing records or refuses the skip",
    ),
    (
        "github-pr-to-main",
        True,
        "pull request against main",
        "/root/AAA/.github/workflows/governance-gate.yml, aaa-governance.yml, "
        "sentinel-premerge-gate.yml (but governance-gate.sh asserts file presence/README "
        "length, and sentinel Q1 CRITICAL_PATHS excludes canon/governance/schemas)",
    ),
    (
        "claim-ledger-write",
        True,
        "any UPDATE/DELETE reaching /root/AAA/claim_ledger/claims.db",
        "append-only SQL triggers trg_claims_no_update / trg_claims_no_delete RAISE(ABORT)",
    ),
)


def count_enforcement() -> tuple[int, int, list[str]]:
    gated = sum(1 for _, g, _, _ in ENC_PATHS if g)
    total = len(ENC_PATHS)
    ungated = [name for name, g, _, _ in ENC_PATHS if not g]
    return gated, total, ungated


# ---------------------------------------------------------------------------
# kernel loader — no vendored copy
# ---------------------------------------------------------------------------


def load_kernel():
    # The kernel module uses @dataclass, so it must be registered in sys.modules
    # BEFORE exec_module — dataclasses resolves cls.__module__ through sys.modules.
    spec = importlib.util.spec_from_file_location("asabiyyah", KERNEL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load kernel instrument at {KERNEL_PATH}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    try:
        spec.loader.exec_module(mod)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return mod


# ---------------------------------------------------------------------------


def build_reading(window_days: int, asb):
    observed_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")

    ceremony, per_root = count_ceremony_artifacts()
    exercised, cer_detail, stale_units = count_exercised_capabilities(window_days)
    holders, holder_entries = count_doctrine_holders()
    executors, exec_detail, exec_names = count_executors(window_days)
    gated, total_paths, ungated = count_enforcement()

    cer_source = (
        "ceremony_artifacts = live .md/.json under AAA include globs "
        "instructions/**/*.md, governance/**/*.md, canon/**/*.md, docs/**/*.md, "
        "skills/**/*.md, agents/decisions/**/*.md, schemas/**/*.json; "
        "excluded: any path part that is dot-prefixed (matches /root/scripts/skills-census.py "
        "prune rule) plus any part in " + ", ".join(sorted(EXCLUDE_PARTS)) + ". "
        "exercised_capabilities: NO per-capability invocation telemetry exists for AAA — "
        "a device-wide search for skill-usage / skill-invocation / telemetry logs returns "
        "nothing, and /var/lib/arifos/metrics/ holds no tool_invocations.jsonl (only GEOX "
        "has one). The only live federation invocation table is /var/lib/arifos/apex_metrics.db "
        "table tool_calls, whose rows are arifOS kernel verbs executed by 333-AGI / openclaw-anon / "
        "agent-zero etc. — attributing those to AAA would be cross-organ telemetry theft, so they "
        "are NOT counted here. SUBSTITUTE (labelled proxy, a strict subset not a superset): "
        "distinct /root/AAA/scripts/* capability units named on a live cron line in "
        "/var/spool/cron/crontabs/root, /etc/crontab or /etc/cron.d/* AND corroborated by at least "
        "one of that line's log redirect targets or /var/log/arifos/<stem>.log, "
        "/root/AAA/scripts/logs/<stem>.log, /root/AAA/forge_work/<stem>.log with mtime inside "
        f"the {window_days}-day window. Absence of invocation telemetry is itself the finding."
    )

    asd_source = (
        "doctrine_holders = distinct live skill directories under /root/AAA/skills containing "
        "SKILL.md, realpath-deduped so symlink views of the same doctrine are not counted twice; "
        "dot-prefixed and archive/vendor parts excluded (same filter as CER). "
        "evidence.doctrine_holder_entries is the alias-inclusive relative-path count using "
        "followlinks=True — the same method /root/scripts/skills-census.py reports as "
        "canonical_skills, recorded so this reading is reconcilable against that live instrument. "
        "executors = distinct actor identities with an execution receipt inside the window, "
        "union of S1 /root/AAA/state/a4_exceptions.jsonl rows whose ts is in window (actor field) "
        "and S2 /root/AAA/claim_ledger/claims.db claims.recorded_by + verifications.verifier whose "
        f"recorded_at/verified_at is in window. Unit caveat: numerator is actor identities, "
        "denominator is doctrine units, so ASD reads as a saturation of doctrine by executors. "
        "Caveat: the A4 actor field is git config user.name — a LABEL, not a bound identity "
        "(documented in /root/AAA/scripts/mutation-authority-probe.py)."
    )

    enc_source = (
        "Protected dirs (AAA's own declared protection, verbatim from "
        "/root/AAA/scripts/mutation-authority-probe.py PROTECTED): "
        + ", ".join(PROTECTED_DIRS)
        + ". total_paths = the enumerated mutation mechanisms into those dirs: "
        + "; ".join(f"{n}{'[GATED]' if g else '[ungated]'}" for n, g, _, _ in ENC_PATHS)
        + ". A path counts as gated only when a mechanistic check precedes the write: "
        + "; ".join(f"{n}: {ev}" for n, g, _, ev in ENC_PATHS if g)
        + ". Adversarial note: the a4 post-commit hook is a LOGGER, not a gate — its own source "
        "states 'Logging can never break the commit' — so it is not counted as coverage."
    )

    evidence = {
        # rule-6 raw additive integers
        "ceremony_artifacts": int(ceremony),
        "exercised_capabilities": int(exercised),
        "doctrine_holders": int(holders),
        "doctrine_holder_entries": int(holder_entries),
        "executors": int(executors),
        "gated_paths": int(gated),
        "total_paths": int(total_paths),
        "ungated": list(ungated),
        "window_days": int(window_days),
        # supporting additive counts so the kernel can re-derive / re-check
        "ceremony_artifacts_by_root": {k: int(v) for k, v in sorted(per_root.items())},
        "scheduled_capability_units": int(cer_detail["scheduled_capability_units"]),
        "fresh_receipt_files": int(cer_detail["fresh_receipt_files"]),
        "stale_capability_units": int(cer_detail["stale_capability_units"]),
        "stale_capability_unit_names": stale_units,
        "executor_identities": exec_names,
        "a4_exception_actors": int(exec_detail["a4_exception_actors"]),
        "claim_ledger_actors": int(exec_detail["claim_ledger_actors"]),
        "invocation_telemetry_present": 0,
    }

    metrics = {
        "cer": asb.ceremony_exercise_ratio(ceremony, exercised, source=cer_source),
        "asd": asb.asabiyyah_depth(holders, executors, source=asd_source),
        "enc": asb.enforcement_coverage(gated, total_paths, source=enc_source, ungated=ungated),
    }

    return asb.SubstrateReading(
        organ=ORGAN,
        host=socket.gethostname(),
        observed_at=observed_at,
        metrics=metrics,
        evidence=evidence,
        reading_version=1,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="asabiyyah_probe", description="AAA substrate reading")
    p.add_argument("--window-days", type=int, default=30)
    p.add_argument("--no-write", action="store_true", help="emit only, do not drop")
    args = p.parse_args(argv)

    asb = load_kernel()
    reading = build_reading(args.window_days, asb)
    payload = reading.to_json()

    if not args.no_write:
        d = Path(DROP_DIR)
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{ORGAN}.json").write_text(payload)

    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
