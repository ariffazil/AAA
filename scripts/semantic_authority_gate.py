#!/usr/bin/env python3
"""semantic_authority_gate.py — DECLARATION != ENFORCEMENT, made machine-testable.

THE DEFECT FAMILY THIS KILLS
  A thing named `gate`, `health`, `sandbox`, `verify`, `seal`, `drift`, `shadow`
  or `authority` reads as a control. The NAME grants semantic authority that the
  RUNTIME may not enforce. Agents (and humans) believe the name faster than they
  read the mechanism, so the gap propagates across the whole federation.

  Observed in one session, every one of them a different file:
    a gate module imported by nobody      -> gate as ARTIFACT, not boundary
    a /health endpoint returning a literal -> health-shaped output, no measurement
    a rejection funnel of constants        -> measurement-shaped, no measurement
    a privacy flag contradicted by its own artifact
    a receipt naming a file that never existed
    a ratification record written by its own beneficiary

  They are not six bugs. They are one bug wearing six names.

THE INVARIANT
  NAME_REQUIRES_MECHANISM. A control-like name must present runtime causal
  evidence, not architectural intent.

  SEMANTIC_AUTHORITY = NAME
                     ∩ CALL_PATH        (something actually calls it)
                     ∩ MEASURED_EFFECT  (bad input changes the output)
                     ∩ BYPASS_RESISTANCE(a path that skips it exists or not)
                     ∩ EVIDENCE         (the claim is checkable on disk)

  Any empty term -> AUTHORITY_CLAIM = VOID. Not FAIL: VOID. The claim was never
  valid, so there is nothing to be wrong about.

VERDICTS
  BOUND     all four terms present; the name is earned
  VOID      a term is empty; the name asserts control the runtime does not show
  UNTESTED  no mechanical check exists yet for this surface (honest, not a pass)
  ARTIFACT  exists and is coherent but nothing calls it — a document, not a wall

WHY RENAME COMES BEFORE FIX
  A `/health` that returns a literal is not a broken health check; it is a
  correctly working status banner with a dishonest name. Renaming it to
  `status_banner` costs nothing and removes the false assurance immediately.
  Fixing the measurement is real work. Naming honesty is a security control that
  ships in seconds.

Run:  python3 semantic_authority_gate.py [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path

ROOTS = [Path("/root/AAA/scripts"), Path("/root/A-FORGE/scripts"),
         Path("/root/arifOS/arifosmcp/runtime"), Path("/root/scripts")]
GIT_ROOTS = [Path("/root/AAA"), Path("/root/scripts"), Path("/root/arifOS"),
             Path("/root/A-FORGE")]

# A name that promises enforcement. If a file or symbol carries one of these,
# the burden of proof is on it.
CONTROL_WORDS = ("gate", "guard", "fence", "verify", "seal", "health", "drift",
                 "sandbox", "secure", "shadow", "authority", "boundary",
                 "enforce", "tripwire", "sentinel", "watchdog", "membrane")

BOUND, VOID, UNTESTED, ARTIFACT = "BOUND", "VOID", "UNTESTED", "ARTIFACT"


@dataclass
class Finding:
    surface: str
    path: str
    control_word: str
    caller_proof: str = VOID
    effect_proof: str = UNTESTED
    bypass_proof: str = UNTESTED
    evidence: list[str] = field(default_factory=list)
    note: str = ""

    @property
    def verdict(self) -> str:
        terms = (self.caller_proof, self.effect_proof, self.bypass_proof)
        if all(t == "EVIDENCED" for t in terms):
            return BOUND
        if self.caller_proof == "VOID":
            return ARTIFACT
        if VOID in terms:
            return VOID
        return UNTESTED


# ── proof 1: CALL_PATH ───────────────────────────────────────────────────────

def _all_py() -> list[Path]:
    out = []
    for r in ROOTS:
        if r.exists():
            out += [p for p in r.rglob("*.py") if "__pycache__" not in str(p)]
    return out


def _invocation_modes() -> str:
    """Concatenated text of every scheduler registration on the host.

    A control can be reached without an import: cron runs a script by path,
    systemd runs a unit, and a cron prompt can shell out to a tool. Checking
    only for imports flagged every CLI entry point as an orphan — a false-alarm
    storm of exactly the kind this file exists to prevent, produced by this file
    on its first run (40+ ARTIFACT verdicts, including this gate itself, which is
    invoked by path and never imported).
    """
    blobs = []
    for cmd in (["crontab", "-l"], ["bash", "-lc", "cat /etc/cron.d/* 2>/dev/null"]):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            blobs.append(r.stdout)
        except Exception:
            pass
    for d in (Path("/etc/systemd/system"), Path("/root/.hermes/cron")):
        try:
            for p in d.rglob("*"):
                if p.is_file() and (p.suffix in (".service", ".timer", ".json") or "cron" in str(p)):
                    blobs.append(p.read_text(errors="replace"))
        except Exception:
            pass
    return "\n".join(blobs)


def caller_proof(module: Path, corpus: list[Path], sched_text: str) -> tuple[str, list[str]]:
    """Is this control actually reached — by import, by path, or by scheduler?

    A control's proof depends on its INVOCATION MODE:
      library (no __main__)  -> must be imported
      CLI (has __main__)     -> must be invoked by path, from cron, systemd, or
                                a subprocess call
    Checking only for imports produced a false-alarm storm on first run: every
    CLI tool whose name contained a control word was reported as an orphan.

    A docstring mention still satisfies NOTHING. The federation's own reality
    gate was named in two companion docstrings (`GATE: reality_object_gate.py`),
    which made its call graph LOOK connected while zero invocations existed.
    """
    stem = module.stem
    try:
        src = module.read_text(errors="replace")
    except Exception:
        return VOID, ["unreadable"]
    is_cli = "__main__" in src

    # 1. import, including dotted package paths (from a.b.mod import ...)
    pat_imp = re.compile(
        rf"^\s*(?:from\s+[\w.]*\b{re.escape(stem)}\b\s+import|"
        rf"import\s+[\w.]*\b{re.escape(stem)}\b)", re.M)

    found: list[str] = []
    prose: list[str] = []
    for p in corpus:
        if p == module:
            continue
        try:
            t = p.read_text(errors="replace")
        except Exception:
            continue
        if pat_imp.search(t):
            found.append(f"import: {p.name}")
        elif re.search(rf"subprocess[^\n]{{0,200}}{re.escape(stem)}", t) or \
                re.search(rf"argv[^\n]{{0,80}}{re.escape(stem)}", t):
            found.append(f"subprocess: {p.name}")
        elif stem in t:
            prose.append(p.name)

    # 2. scheduler / by-path invocation
    if module.name in sched_text or str(module) in sched_text or stem in sched_text:
        found.append("scheduler registration")

    if found:
        return "EVIDENCED", found[:3]
    if prose:
        mode = "CLI invoked by path" if is_cli else "library"
        return VOID, [f"{mode}; named only in {', '.join(prose[:2])} — no import, "
                      f"no subprocess, no scheduler entry"]
    mode = "CLI invoked by path" if is_cli else "library"
    return VOID, [f"{mode}; no reference of any kind"]


# ── proof 2: MEASURED_EFFECT ─────────────────────────────────────────────────

# A BARE CONSTANT status — the literal is the whole value, e.g. {"status": "ok"}
# The trailing [,}] distinguishes a constant from an EXPRESSION:
#   {"status": "healthy"}                  -> banner (matches)
#   {"status": "healthy" if up else "bad"} -> computed (does not match)
LITERAL_HEALTH = re.compile(
    r'["\']status["\']\s*:\s*["\'](healthy|ok|up|good)["\']\s*[,}]')

# A file only HAS a health surface if it declares one. Without this, the scanner
# flagged any module containing an ordinary `{"status": "ok"}` dict — including
# l5_graphiti_bridge.py, which has NO health endpoint at all (line 414 is a
# plain status field). That produced 14 invented surfaces: findings shaped like
# measurements with no measurement behind them — precisely the disease this gate
# exists to catch, committed by the gate itself on its first two runs.
HEALTH_SURFACE = re.compile(
    r'(/health\b|/healthz\b|def\s+health|health_check\s*\(|["\']health["\']\s*:)')


def effect_proof_health(path: Path) -> tuple[str, list[str]]:
    """Does a declared health surface report live state, or a bare constant?

    Requires an ACTUAL health surface to exist in the file first. A module with
    no health route cannot have a broken health route, and reporting one is a
    fabricated finding.
    """
    try:
        t = path.read_text(errors="replace")
    except Exception:
        return UNTESTED, ["unreadable"]
    if not HEALTH_SURFACE.search(t):
        return UNTESTED, ["no health surface declared in this file"]
    if not LITERAL_HEALTH.search(t):
        return "EVIDENCED", ["health surface present; status is computed, not constant"]
    state_reads = re.findall(
        r"(urlopen|requests\.(?:get|post)|socket\.|subprocess\.|check_output|"
        r"\.exists\(\)|urllib)", t)
    if len(state_reads) < 2:
        return VOID, [f"declared health surface returns a bare constant with "
                      f"{len(state_reads)} live-state read(s) — the bytes cannot "
                      f"change when a dependency dies"]
    return "EVIDENCED", [f"health surface with a constant present but {len(state_reads)} live-state reads nearby"]


# ── proof 3: BYPASS_RESISTANCE ───────────────────────────────────────────────

def bypass_proof_module(module: Path, corpus: list[Path]) -> tuple[str, list[str]]:
    """If nothing calls it, bypass is total — but that is CALL_PATH's verdict.

    When a module IS called, bypass resistance is about alternate routes. That
    needs per-surface analysis, so it is reported UNTESTED rather than assumed.
    Claiming bypass resistance without an attempted bypass would be exactly the
    declaration-over-enforcement defect this file exists to catch.
    """
    return UNTESTED, ["no bypass attempt encoded for this surface yet"]


# ── the scan ─────────────────────────────────────────────────────────────────

def scan() -> list[Finding]:
    corpus = _all_py()
    sched = _invocation_modes()
    findings: list[Finding] = []

    for module in corpus:
        if module == Path(__file__).resolve() or module.name == Path(__file__).name:
            continue          # this scanner's own prose must not count as a referrer
        words = [w for w in CONTROL_WORDS if w in module.stem.lower()]
        if not words:
            continue
        cp, cev = caller_proof(module, corpus, sched)
        ep, eev = (effect_proof_health(module) if "health" in module.stem.lower()
                   else (UNTESTED, ["no effect check encoded for this surface"]))
        bp, bev = bypass_proof_module(module, corpus)
        findings.append(Finding(
            surface=module.stem, path=str(module), control_word=words[0],
            caller_proof=cp, effect_proof=ep, bypass_proof=bp,
            evidence=cev + eev + bev,
            note="named in prose but never imported" if cp == VOID and cev and "named only" in cev[0] else ""))

    # health surfaces living inside larger files — but ONLY where a health
    # surface actually exists. The first version flagged every module that
    # happened to contain a `{"status": "ok"}` dict, inventing 14 endpoints.
    for p in corpus:
        try:
            t = p.read_text(errors="replace")
        except Exception:
            continue
        if p == Path(__file__):
            continue                      # the scanner's own prose is not evidence
        if HEALTH_SURFACE.search(t) and "health" not in p.stem.lower():
            ep, eev = effect_proof_health(p)
            findings.append(Finding(
                surface=f"{p.stem}:/health", path=str(p), control_word="health",
                caller_proof="EVIDENCED", effect_proof=ep, bypass_proof=UNTESTED,
                evidence=eev,
                note="health-shaped handler inside a larger module"))

    return findings


# ── self-test: every proof must be able to FAIL ──────────────────────────────

def selftest() -> tuple[bool, list[str]]:
    problems = []
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        gate = d / "widget_gate.py"
        gate.write_text("def gate(x):\n    return x\n")
        companion = d / "companion.py"
        companion.write_text("GATE: widget_gate.py\n")   # prose only
        corpus = [gate, companion]

        # CALL_PATH must NOT accept a prose mention
        v, ev = caller_proof(gate, corpus, sched_text="")
        if v != VOID:
            problems.append("caller_proof accepted a docstring mention as a call")

        # and MUST accept a real import
        caller = d / "caller.py"
        caller.write_text("from widget_gate import gate\ngate(1)\n")
        v, ev = caller_proof(gate, [gate, companion, caller], sched_text="")
        if v != "EVIDENCED":
            problems.append("caller_proof rejected a real import")

        # a CLI tool must be reachable by PATH, not only by import. This was the
        # first run's false-alarm storm: every CLI whose name held a control word
        # was called an orphan.
        cli = d / "tool_gate.py"
        cli.write_text('import argparse\nif __name__ == "__main__":\n    argparse.ArgumentParser().parse_args()\n')
        v, ev = caller_proof(cli, [cli], sched_text="*/5 * * * * root python3 /tmp/tool_gate.py")
        if v != "EVIDENCED":
            problems.append("caller_proof rejected a CLI registered in a scheduler")
        v, ev = caller_proof(cli, [cli], sched_text="")
        if v != VOID:
            problems.append("caller_proof accepted a CLI with no invocation anywhere")

        # EFFECT_PROOF must reject a bare-constant status on a DECLARED surface
        banner = d / "banner.py"
        banner.write_text('def health():\n    return {"status": "healthy"}\n')
        v, ev = effect_proof_health(banner)
        if v != VOID:
            problems.append("effect_proof accepted a bare-constant status as measurement")

        # and MUST NOT invent a surface that does not exist. A module holding a
        # plain status dict is not a health endpoint — flagging it was this
        # scanner's own false-alarm storm (14 invented surfaces on run two).
        plain = d / "plain.py"
        plain.write_text('def result():\n    return {"status": "ok", "n": 1}\n')
        v, ev = effect_proof_health(plain)
        if v == VOID:
            problems.append("effect_proof invented a health surface in a file with none")

        # and MUST accept a status backed by live reads
        real = d / "real.py"
        real.write_text(
            'import urllib.request\n'
            'def health():\n'
            '    up = 0\n'
            '    for u in ("a", "b"):\n'
            '        try:\n'
            '            urllib.request.urlopen(u).read(1024)\n'
            '            up += 1\n'
            '        except Exception:\n'
            '            pass\n'
            '    return {"status": "healthy" if up == 2 else "degraded"}\n')
        v, ev = effect_proof_health(real)
        if v != "EVIDENCED":
            problems.append("effect_proof rejected a health surface backed by live reads")

    return (not problems), problems


def main() -> int:
    ap = argparse.ArgumentParser(description="NAME_REQUIRES_MECHANISM auditor")
    ap.add_argument("--json", action="store_true", dest="as_json")
    a = ap.parse_args()

    findings = scan()
    ok_self, problems = selftest()

    counts: dict[str, int] = {}
    for f in findings:
        counts[f.verdict] = counts.get(f.verdict, 0) + 1

    if a.as_json:
        print(json.dumps({
            "invariant": "NAME_REQUIRES_MECHANISM",
            "formula": "SEMANTIC_AUTHORITY = NAME ∩ CALL_PATH ∩ MEASURED_EFFECT ∩ BYPASS_RESISTANCE ∩ EVIDENCE",
            "rule": "any empty term -> AUTHORITY_CLAIM = VOID",
            "counts": counts,
            "self_test": "PASS" if ok_self else "FAIL",
            "findings": [asdict(f) | {"verdict": f.verdict} for f in findings],
        }, indent=2, ensure_ascii=False))
        return 0

    print("SEMANTIC AUTHORITY GATE — NAME_REQUIRES_MECHANISM")
    print("=" * 70)
    for f in sorted(findings, key=lambda x: (x.verdict != ARTIFACT, x.surface)):
        if f.verdict == BOUND and f.effect_proof == UNTESTED and f.bypass_proof == UNTESTED:
            label = UNTESTED
        else:
            label = f.verdict
        print(f"  [{label:<8}] {f.surface[:34]:<34} {f.control_word:<10} {f.evidence[0][:52] if f.evidence else ''}")
    print("=" * 70)
    print(f"  self-test (every proof must be able to REJECT): "
          f"{'PASS' if ok_self else 'FAIL'}")
    for p in problems:
        print(f"      {p}")
    print(f"  total surfaces scanned: {len(findings)}")
    print(f"  verdicts: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print()
    print("  VOID is not FAIL — it means the claim was never valid, so there is")
    print("  nothing to be wrong about. Rename BEFORE fixing: a banner called")
    print("  'health' is not a broken check, it is a working banner with a")
    print("  dishonest name, and the name is the hazard.")
    return 0 if ok_self else 1


if __name__ == "__main__":
    sys.exit(main())
