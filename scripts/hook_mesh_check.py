#!/usr/bin/env python3
"""
hook_mesh_check.py — drift guard for the AAA federation hook mesh.

Purpose: make `governance/AGENTIC-HOOK-MESH-V1.yaml` LOAD-BEARING rather than decorative.

Design rule (this is the whole point):
    An UNDECLARED defect fails the build.
    A DECLARED defect passes with a notice.

That inverts the failure mode that produced four contradictory completion receipts on
2026-09-14: agents could assert "no contradictions" while contradictions existed,
because nothing checked. Now a contradiction is allowed only if it is written down in
`known_gaps` — which makes it visible to every warga reading the SOT.

Checks:
  C1  Enumerated fail-safe classes in code == classes in the SOT.
  C2  The class list is declared in exactly ONE module (no silent duplication).
  C3  No governance/registry file claims a hook can block (can_block/must_block: true,
      must_block_on, MONOTONIC_GATE authority).
  C4  Every harness manifest_path declared in the SOT exists on disk.
  C5  Hook code that emits a kernel-only verdict (VOID/DENY/REVOKED) is DECLARED in
      known_gaps. Undeclared => FAIL.
  C6  Every known_gap declares id, status and owner.

Exit 0 = clean (or all defects declared). Exit 1 = undeclared drift.

Run:  python3 /root/AAA/scripts/hook_mesh_check.py [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AAA = Path("/root/AAA")
LIB = AAA / "hooks" / "lib"
SOT = AAA / "governance" / "AGENTIC-HOOK-MESH-V1.yaml"
ORDER_DOC = AAA / "governance" / "AAA-HOOK-ORDER-AND-MONOTONICITY.md"
ANTIGRAVITY = AAA / "registries" / "antigravity" / "hooks.json"
CLAUDE_HOOKS = AAA / "plugins" / "claude-code-federation" / "hooks" / "hooks.json"
OPENCODE_MANIFEST = Path("/root/.config/opencode/plugins/IPENCODE-HOOK-ORDER-MANIFEST.json")

KERNEL_ONLY_VERDICTS = ("VOID", "DENY", "REVOKED")

failures: list[str] = []
notices: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def note(msg: str) -> None:
    notices.append(msg)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        fail(f"UNREADABLE {path}: {exc}")
        return ""


# ---------------------------------------------------------------------------
# C1/C2 — enumerated fail-safe classes
# ---------------------------------------------------------------------------
def sot_fail_safe_classes(text: str) -> set[str]:
    """Parse the enumerated class block from the SOT without a YAML dependency."""
    classes: set[str] = set()
    in_block = False
    for line in text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped.startswith("ENUMERATED FAIL-SAFE CLASSES"):
            in_block = True
            continue
        if in_block:
            if stripped.startswith("separation_of_powers:"):
                break
            m = re.match(r"^-\s+(/\S+)", stripped)
            if m:
                classes.add(m.group(1))
    return classes


def code_fail_safe_classes() -> set[str]:
    sys.path.insert(0, str(LIB))
    try:
        import federation_hook_engine as eng  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        fail(f"C1 cannot import federation_hook_engine: {exc}")
        return set()
    return {str(p) for p in getattr(eng, "FORBIDDEN_MUTATION_TARGETS", [])}


def check_classes(sot_text: str) -> set[str]:
    sot = sot_fail_safe_classes(sot_text)
    code = code_fail_safe_classes()
    if not sot:
        fail("C1 SOT declares no enumerated fail-safe classes (block missing or renamed)")
    if sot != code:
        fail(f"C1 class drift — SOT only: {sorted(sot - code)} | code only: {sorted(code - sot)}")
    else:
        note(f"C1 enumerated fail-safe classes agree across SOT and code ({len(code)} classes)")

    # C2 — list must live in exactly one module
    holders = []
    for py in sorted(LIB.glob("*.py")):
        body = read(py)
        if sum(1 for c in code if c in body) >= 2:
            holders.append(py.name)
    if len(holders) > 1:
        fail(f"C2 enumerated classes re-declared in multiple modules: {holders}")
    else:
        note(f"C2 single declaration site: {holders[0] if holders else 'none'}")
    return code


# ---------------------------------------------------------------------------
# C3 — no file may claim a hook can block
# ---------------------------------------------------------------------------
BLOCK_CLAIM_PATTERNS = (
    (r'"can_block"\s*:\s*true', "can_block: true"),
    (r'"must_block"\s*:\s*true', "must_block: true"),
    (r'must_block_on\s*:', "must_block_on"),
    (r'"authority"\s*:\s*"MONOTONIC_GATE"', "authority: MONOTONIC_GATE"),
    (r'Authority Ceiling\s*\|?\s*MONOTONIC_GATE', "MONOTONIC_GATE ceiling in table"),
)


def check_no_block_claims() -> None:
    targets = [SOT, ORDER_DOC, ANTIGRAVITY, CLAUDE_HOOKS, OPENCODE_MANIFEST]
    targets += sorted((AAA / "governance").glob("AAA-HOOK-*.yaml"))
    hits: list[str] = []
    for path in targets:
        if not path.exists():
            continue
        body = read(path)
        for pattern, label in BLOCK_CLAIM_PATTERNS:
            for line_no, line in enumerate(body.splitlines(), 1):
                if re.search(pattern, line):
                    hits.append(f"{path.name}:{line_no} [{label}]")
    if hits:
        fail("C3 files still declare that hooks block:\n      " + "\n      ".join(hits))
    else:
        note(f"C3 no hook-blocking declaration in {len(targets)} governance/registry files")


# ---------------------------------------------------------------------------
# C4 — declared harness manifests must exist
# ---------------------------------------------------------------------------
def check_manifests(sot_text: str) -> None:
    paths = sorted(set(re.findall(r'manifest_path:\s*"([^"]+)"', sot_text)))
    if not paths:
        fail("C4 SOT declares no manifest_path entries")
    for p in paths:
        if not Path(p).exists():
            fail(f"C4 declared manifest_path missing on disk: {p}")
    if paths:
        note(f"C4 {len(paths)} declared harness manifests present")


# ---------------------------------------------------------------------------
# C5 — kernel-only verdicts in hook code must be declared
# ---------------------------------------------------------------------------
def declared_gap_ids(sot_text: str) -> set[str]:
    return set(re.findall(r"^\s*-\s*id:\s*([A-Z0-9\-_]+)", sot_text, flags=re.M))


def check_declared_defects(sot_text: str) -> None:
    declared = declared_gap_ids(sot_text)
    # An engine that returns VOID/DENY is a defect unless a gap says so.
    eng = LIB / "federation_hook_engine.py"
    if eng.exists():
        body = read(eng)
        returns_kernel_verdict = bool(re.search(r'"verdict"\s*:\s*"(VOID|DENY|REVOKED)"', body))
        if returns_kernel_verdict:
            if any("VERDICT-OVERREACH" in g for g in declared):
                note("C5 hook code emits kernel-only verdicts — DECLARED as ENGINE-VERDICT-OVERREACH")
            else:
                fail(
                    "C5 UNDECLARED: federation_hook_engine.py emits a kernel-only verdict "
                    "(VOID/DENY/REVOKED) with no matching known_gap declared in the SOT"
                )

    # A harness path with no target screen must be declared.
    claude_pre = AAA / "plugins" / "claude-code-federation" / "hooks" / "f1-amanah-preshell.py"
    if claude_pre.exists():
        body = read(claude_pre)
        screens = any(c in body for c in ("/etc/shadow", "/etc/sudoers", "authorized_keys"))
        if not screens and not any("CLAUDE-PATH-TARGET-SCREEN" in g for g in declared):
            fail("C5 UNDECLARED: Claude PreToolUse screens no forbidden target and no known_gap records it")

    # C6 — every gap must be triaged
    for block in re.finditer(r"-\s*id:\s*([A-Z0-9\-_]+)([\s\S]{0,3000}?)(?=\n\s*-\s*id:|\Z)", sot_text):
        gid, body_text = block.group(1), block.group(2)
        for field in ("status", "owner", "prescribed_fix"):
            if field not in body_text:
                fail(f"C6 known_gap {gid} missing field: {field}")
    if declared:
        note(f"C6 {len(declared)} declared gaps, all triaged")

    # C7 — auto-crystallized scars must NOT sit in the ACTIVE scar path.
    # _load_recent_scars() globs SCARS_DIR/*.md (non-recursive), so any root-level scar
    # is injected into every agent's boot context as an "active constraint". Candidates
    # belong in scars/candidates/. Found live on 2026-09-14: three SCAR-AUTO files
    # derived from a trivial `jq: command not found`, each self-labelled QUARANTINED,
    # while sitting in the active path.
    active_auto_scars = sorted((AAA / "scars").glob("SCAR-AUTO-*.md"))
    if active_auto_scars:
        fail(
            f"C7 {len(active_auto_scars)} auto-crystallized scar(s) in the ACTIVE scar path — "
            "they are injected into every agent's boot brief. Move to scars/candidates/: "
            + ", ".join(p.name for p in active_auto_scars)
        )
    else:
        note("C7 active scar path carries no auto-crystallized candidate")

    # C8 — the OpenCode gate plugin must actually COMPILE.
    # On 2026-09-14 arifos-judge-gate.ts failed to compile (unclosed if-block left by
    # the degraded-branch refactor). It registered hooks=0 — a silently dead
    # constitutional gate — while receipts reported "6/6 plugins active" and
    # "100% PASS". Nothing checked. This does.
    import shutil as _shutil
    import subprocess as _subprocess
    import tempfile as _tempfile

    plugin_dir = Path("/root/.config/opencode/plugins")
    if _shutil.which("bun") and plugin_dir.exists():
        ts_files = sorted(plugin_dir.glob("*.ts"))
        broken: list[str] = []
        for ts in ts_files:
            with _tempfile.NamedTemporaryFile(suffix=".js", delete=True) as out:
                proc = _subprocess.run(
                    ["bun", "build", "--target=bun", str(ts), f"--outfile={out.name}"],
                    capture_output=True, text=True, timeout=60,
                )
            if proc.returncode != 0:
                last = (proc.stderr.strip().splitlines() or ["unknown error"])[-1]
                broken.append(f"{ts.name}: {last}")
        if broken:
            fail("C8 OpenCode plugin(s) do not compile — gate may be silently dead: " + " | ".join(broken))
        else:
            note(f"C8 {len(ts_files)} OpenCode plugins compile (gate is loadable)")
    else:
        note("C8 bun unavailable — plugin compile check skipped")

    # C9 — END-TO-END enumerated refusal through the REAL CLI path.
    # Closes gap ENUMERATED-REFUSAL-NO-END-TO-END-TEST: the adversarial suite
    # exercised gate() in-process only, so a CLI-path flip to ALLOW passed
    # every suite green (observed flapping 2026-09-14 09:19/09:29/09:30 —
    # VOID/NOT_EXECUTED, then ALLOW/PROCEEDED, then VOID again within minutes).
    import subprocess as _sp9
    eng_cli = LIB / "federation_hook_engine.py"
    if eng_cli.exists():
        _payload = json.dumps({
            "tool_name": "Bash",
            "tool_args": {"command": "echo pwned >> /etc/sudoers.d/evil"},
        })
        _proc = _sp9.run(
            ["python3", str(eng_cli), "gate", "--actor", "MESH-CHECK-C9", "--payload", _payload],
            capture_output=True, text=True, timeout=60,
        )
        _verdict = _exec = None
        try:
            # Engine emits pretty-printed (multi-line) JSON — parse whole stdout.
            _out = json.loads(_proc.stdout)
            _verdict, _exec = _out.get("verdict"), _out.get("execution_status")
        except Exception:
            pass
        if _proc.returncode != 0 or _verdict is None:
            fail(f"C9 engine gate CLI unusable (rc={_proc.returncode}): {(_proc.stderr or _proc.stdout)[:200]}")
        elif _verdict == "ALLOW" or _exec != "NOT_EXECUTED":
            fail(f"C9 enumerated target NOT refused through CLI: verdict={_verdict} execution_status={_exec}")
        else:
            note(f"C9 enumerated refusal holds through the CLI path (verdict={_verdict}, {_exec})")
    else:
        fail("C9 engine CLI missing: federation_hook_engine.py not found")


def main() -> int:
    ap = argparse.ArgumentParser(description="AAA hook mesh drift guard")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    if not SOT.exists():
        print(f"FATAL: SOT missing: {SOT}", file=sys.stderr)
        return 1

    sot_text = read(SOT)
    check_classes(sot_text)
    check_no_block_claims()
    check_manifests(sot_text)
    check_declared_defects(sot_text)

    if args.json:
        print(json.dumps({
            "check": "aaa.hook_mesh_check.v1",
            "sot": str(SOT),
            "sot_version": (re.search(r'^version:\s*"([^"]+)"', sot_text, flags=re.M) or [None, "?"])[1],
            "failures": failures,
            "notices": notices,
            "status": "FAIL" if failures else "PASS",
        }, indent=2))
    else:
        print("=== AAA HOOK MESH DRIFT GUARD ===")
        for n in notices:
            print(f"  ok   {n}")
        for f in failures:
            print(f"  FAIL {f}")
        print(f"\nstatus: {'FAIL' if failures else 'PASS'} "
              f"({len(notices)} ok, {len(failures)} failed)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
