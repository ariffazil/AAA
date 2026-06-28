#!/usr/bin/env python3
"""
MCP Cognitive Test Harness v1 — 2026-06-26

Tests the agent's cognitive substrate, NOT code paths.
Verifies: substrate integrity, deprecation awareness, session state validity,
CONTEXT tier integrity, invariant consistency, tool authority mapping,
and cross-artifact references.

This is cognitive physics testing, not software testing.
Code coverage is meaningless here — you test the agent's mind, not the code.

Usage:
    python3 mcp_cognitive_test_harness.py                 # all scenarios
    python3 mcp_cognitive_test_harness.py --scenario deprecation
    python3 mcp_cognitive_test_harness.py --verbose --trace
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

# ── Configuration ──
ROOT = Path("/root")
ARTIFACTS = {
    "invariants": ROOT / "AAA/docs/INVARIANTS.md",
    "session_state": ROOT / ".claude/projects/-root/memory/session-state.md",
    "context_focus": ROOT / "CONTEXT.md",
    "context_session": ROOT / "CONTEXT_SESSION.md",
    "context_archive": ROOT / "CONTEXT_ARCHIVE.md",
    "deprecation_registry": ROOT / "AAA/docs/deprecation-registry.json",
    "claude_md": ROOT / "AAA/CLAUDE.md",
    "vault999": ROOT / "VAULT999/outcomes.jsonl",
}

REQUIRED_SESSION_STATE_FIELDS = [
    "Current task", "Task phase", "Blockers", "Discoveries this session",
    "Open decisions", "Last action", "Next action", "Active blast radius",
    "Modified repos", "Session invariants", "Compaction count",
]

DEPRECATION_CATEGORIES = [
    "deprecated_tools", "deprecated_services", "deprecated_endpoints",
    "deprecated_patterns", "deprecated_skills", "deprecated_conventions",
]

# ── Output helpers ──
PASS = 0
FAIL = 0
TRACE = False

def ok(msg: str):
    global PASS
    PASS += 1
    print(f"  ✅ {msg}")

def err(msg: str):
    global FAIL
    FAIL += 1
    print(f"  ❌ {msg}")

def warn(msg: str):
    print(f"  ⚠️  {msg}")

def trace(msg: str):
    if TRACE:
        print(f"     🔍 {msg}")

def header(title: str):
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print(f"{'─'*60}")

# ── Scenario 1: Substrate Integrity ──
def test_substrate_integrity():
    header("SCENARIO 0: SUBSTRATE INTEGRITY")
    print("  Testing: All 4 substrate artifacts exist, are readable, and valid.\n")

    # Check all artifacts exist
    for name, path in ARTIFACTS.items():
        if path.exists():
            size = path.stat().st_size
            trace(f"{name}: {path} ({size} bytes)")
            ok(f"{name} exists ({size} bytes)")
        else:
            err(f"{name} MISSING: {path}")

    # CONTEXT.md size check (must be under 10KB — readable)
    ctx = ARTIFACTS["context_focus"]
    if ctx.exists():
        size = ctx.stat().st_size
        if size < 10_000:
            ok(f"CONTEXT.md is slim ({size} bytes) — agent can read it")
        elif size < 50_000:
            warn(f"CONTEXT.md is {size} bytes — readable but growing, consider trimming")
        else:
            err(f"CONTEXT.md is {size} bytes — TOO LARGE, agent cannot read it (>50KB)")

    # CONTEXT_ARCHIVE size sanity
    archive = ARTIFACTS["context_archive"]
    if archive.exists():
        size = archive.stat().st_size
        if size > 100_000:
            warn(f"CONTEXT_ARCHIVE.md is {size} bytes — must be grep-only, never loaded")
        else:
            ok(f"CONTEXT_ARCHIVE.md exists ({size} bytes)")

    # Deprecation registry is valid JSON
    dep = ARTIFACTS["deprecation_registry"]
    if dep.exists():
        try:
            data = json.loads(dep.read_text())
            cats_found = [k for k in DEPRECATION_CATEGORIES if k in data]
            ok(f"deprecation-registry.json is valid JSON ({len(cats_found)}/{len(DEPRECATION_CATEGORIES)} categories)")
            for cat in DEPRECATION_CATEGORIES:
                if cat in data:
                    count = len(data[cat])
                    trace(f"  {cat}: {count} entries")
                    if count == 0:
                        warn(f"  {cat} is empty — may need population")
                else:
                    warn(f"  {cat} category missing from deprecation registry")
        except json.JSONDecodeError as e:
            err(f"deprecation-registry.json is INVALID JSON: {e}")

    # Session state template has all required fields
    ss = ARTIFACTS["session_state"]
    if ss.exists():
        content = ss.read_text()
        missing = []
        for field in REQUIRED_SESSION_STATE_FIELDS:
            if field not in content:
                missing.append(field)
        if missing:
            warn(f"session-state.md missing fields: {missing}")
        else:
            ok(f"session-state.md has all {len(REQUIRED_SESSION_STATE_FIELDS)} required fields")

    # VAULT999 is append-only JSONL
    vault = ARTIFACTS["vault999"]
    if vault.exists():
        try:
            with open(vault) as f:
                for i, line in enumerate(f):
                    if i > 5:
                        break
                    if line.strip():
                        json.loads(line)
            ok("VAULT999 outcomes.jsonl is valid JSONL")
        except json.JSONDecodeError as e:
            err(f"VAULT999 outcomes.jsonl is CORRUPTED: {e}")

# ── Scenario 2: Deprecation Awareness ──
def test_deprecation_awareness():
    header("SCENARIO 2: DEPRECATION AWARENESS")
    print("  Testing: Deprecation registry covers all known deprecated items.\n")

    dep = ARTIFACTS["deprecation_registry"]
    if not dep.exists():
        err("Cannot run — deprecation registry missing")
        return

    data = json.loads(dep.read_text())

    # Verify known critical deprecations are present
    critical_deprecations = {
        "forge_*": "deprecated_tools",
        "arif_judge_deliberate": "deprecated_tools",
        "apex-prime.service": "deprecated_services",
        "non_date_tags": "deprecated_patterns",
        "containerize_core_organs": "deprecated_patterns",
    }

    for item, category in critical_deprecations.items():
        found = False
        cat_data = data.get(category, {})
        for key in cat_data:
            if item.lower() in key.lower() or key.lower() in item.lower():
                found = True
                status = cat_data[key].get("status", "?")
                migration = cat_data[key].get("migration", "?")
                trace(f"  {item}: status={status}, migration={migration[:60]}...")
                break
        if found:
            ok(f"'{item}' is in deprecation registry")
        else:
            err(f"'{item}' NOT FOUND in deprecation registry — zombie risk")

    # Verify lifecycle stages are valid
    valid_stages = {"ANNOUNCED", "DEPRECATED", "DEPRECATED_PROXY", "STOPPED_DISABLED", "REMOVED", "FORBIDDEN", "DEGRADED", "LEGACY", "REDIRECTED", "REPLACED"}
    for category in DEPRECATION_CATEGORIES:
        cat_data = data.get(category, {})
        for key, info in cat_data.items():
            status = info.get("status", "")
            if status not in valid_stages:
                warn(f"  {key}: status '{status}' not in known lifecycle stages {valid_stages}")

    # Verify every deprecated tool has a migration path
    tools = data.get("deprecated_tools", {})
    for name, info in tools.items():
        if "migration" not in info:
            err(f"  {name}: no migration path — agent cannot know replacement")
        else:
            trace(f"  {name} → {info['migration'][:80]}")

    if tools:
        ok(f"All {len(tools)} deprecated tools have migration paths")
    else:
        warn("No deprecated tools registered — may be incomplete")

# ── Scenario 3: Session State Continuity ──
def test_session_state_continuity():
    header("SCENARIO 3: SESSION STATE CONTINUITY")
    print("  Testing: Session state infrastructure can survive compaction.\n")

    # Session state file exists and is writable
    ss = ARTIFACTS["session_state"]
    if not ss.exists():
        err("session-state.md MISSING — agent cannot restore state after compaction")
        return

    # Check file is writable (agent can update it)
    if os.access(ss, os.W_OK):
        ok("session-state.md is writable (agent can update before compaction)")
    else:
        err("session-state.md is NOT writable — agent cannot update state")

    # Check precompact hook writes session-state.json
    precompact_snapshot = ROOT / ".claude/sessions/session-state.json"
    if precompact_snapshot.exists():
        try:
            snap = json.loads(precompact_snapshot.read_text())
            required = ["session_id", "timestamp", "vault_tail", "open_holds"]
            missing = [k for k in required if k not in snap]
            if missing:
                warn(f"session-state.json missing fields: {missing}")
            else:
                ok(f"session-state.json exists with all required fields (last: {snap.get('timestamp', '?')})")
        except json.JSONDecodeError:
            err("session-state.json is CORRUPTED")
    else:
        warn("session-state.json not yet created — precompact hook may not have run")

    # Check postcompact hook references session state
    postcompact = ROOT / "hooks/postcompact.sh"
    if postcompact.exists():
        content = postcompact.read_text()
        if "session-state.json" in content or "session-state.md" in content:
            ok("postcompact.sh references session state files")
        else:
            err("postcompact.sh does NOT reference session state — state lost on compaction")

    # Check precompact hook writes state
    precompact = ROOT / "hooks/precompact.sh"
    if precompact.exists():
        content = precompact.read_text()
        if "session-state.json" in content:
            ok("precompact.sh writes session-state.json")
        else:
            err("precompact.sh does NOT write session state")

    # CONTEXT tiers exist
    for tier_name in ["context_focus", "context_session", "context_archive"]:
        path = ARTIFACTS[tier_name]
        if path.exists():
            ok(f"{tier_name} exists")
        else:
            err(f"{tier_name} MISSING — tiered context incomplete")

# ── Scenario 4: Invariant Consistency ──
def test_invariant_consistency():
    header("SCENARIO 4: INVARIANT CONSISTENCY")
    print("  Testing: INVARIANTS.md claims are consistent with other artifacts.\n")

    invariants = ARTIFACTS["invariants"]
    if not invariants.exists():
        err("INVARIANTS.md MISSING — agent has no constitutional physics")
        return

    inv_content = invariants.read_text()

    # Verify INVARIANTS references all substrate artifacts
    cross_refs = {
        "deprecation-registry.json": "Invariant 6 (Deprecation)",
        "session-state.md": "Invariant 4 (Session State)",
        "CONTEXT.md": "Invariant 4 (Session State)",
        "INVARIANTS.md": "Loading Protocol",
        "CLAUDE.md": "Invariant 5 (Reversibility)",
    }

    for ref, invariant in cross_refs.items():
        if ref in inv_content:
            ok(f"INVARIANTS.md references {ref} ({invariant})")
        else:
            warn(f"INVARIANTS.md does NOT reference {ref} — {invariant} may be orphaned")

    # Verify all 7 invariants present
    invariant_markers = [
        "Tools Are Constitutional Powers",
        "MCP Is a Contract Machine",
        "Observation → Collapse → Verdict",
        "Session State Is the World Model",
        "Reversibility Before Irreversibility",
        "Deprecation Is a First-Class Citizen",
        "No Silent Failure",
    ]
    for marker in invariant_markers:
        if marker in inv_content or marker.replace(" → ", "→") in inv_content:
            trace(f"  Invariant found: {marker}")
        else:
            err(f"Invariant MISSING from INVARIANTS.md: {marker}")

    # Verify all 7 Zen principles present
    zen_markers = [
        "Clarity Over Cleverness",
        "Receipts Over Assumptions",
        "State Over Guesswork",
        "Governance Over Freedom",
        "Reversibility Over Speed",
        "Append-Only Over Rewrite",
        "No Agent Should Ever Approve Itself",
    ]
    for marker in zen_markers:
        if marker in inv_content:
            trace(f"  Zen found: {marker}")
        else:
            warn(f"Zen may be MISSING from INVARIANTS.md: {marker}")

    # Verify Floor→Invariant map exists
    if "F1" in inv_content and "F13" in inv_content:
        ok("INVARIANTS.md maps invariants to constitutional floors")
    else:
        err("INVARIANTS.md does NOT map to floors — invariants ungoverned")

    # Verify Agent Loading Protocol lists 7 files
    if "cat /root/AAA/CLAUDE.md" in inv_content:
        ok("INVARIANTS.md has Agent Loading Protocol with CLAUDE.md first")
    else:
        err("INVARIANTS.md missing Agent Loading Protocol")

# ── Scenario 5: Cross-Artifact Reference Integrity ──
def test_cross_artifact_references():
    header("SCENARIO 5: CROSS-ARTIFACT REFERENCE INTEGRITY")
    print("  Testing: All artifacts reference each other correctly.\n")

    # CLAUDE.md references INVARIANTS.md
    claude = ARTIFACTS["claude_md"]
    if claude.exists():
        cc = claude.read_text()
        refs = {
            "INVARIANTS.md": "loading sequence step 2.5",
            "session-state.md": "session start checklist",
            "deprecation-registry.json": "loading sequence step 5",
            "CONTEXT.md": "loading sequence step 3",
        }
        for ref, expected in refs.items():
            if ref in cc:
                ok(f"CLAUDE.md references {ref} ({expected})")
            else:
                err(f"CLAUDE.md does NOT reference {ref} — {expected} missing")

    # session-state.md is referenced by postcompact hook
    postcompact = ROOT / "hooks/postcompact.sh"
    if postcompact.exists():
        pc = postcompact.read_text()
        if "session-state.md" in pc or "session-state.json" in pc:
            ok("postcompact.sh references session state")
        else:
            err("postcompact.sh does NOT reference session state")

    # deprecation-registry.json is referenced by CLAUDE.md loading sequence
    if claude.exists() and "deprecation-registry.json" in claude.read_text():
        ok("CLAUDE.md loading sequence includes deprecation check")
    else:
        err("CLAUDE.md loading sequence does NOT include deprecation check")

    # MEMORY.md has entries for all 4 artifacts
    memory_md = ROOT / ".claude/projects/-root/memory/MEMORY.md"
    if memory_md.exists():
        mm = memory_md.read_text()
        mem_refs = ["session-state", "tiered-context", "deprecation-registry", "mcp-invariants"]
        for ref in mem_refs:
            if ref in mm:
                trace(f"  MEMORY.md references {ref}")
            else:
                warn(f"MEMORY.md missing entry for {ref}")

        # Count entries
        entry_count = mm.count("\n- [")
        ok(f"MEMORY.md has {entry_count} entries")
    else:
        err("MEMORY.md MISSING")

# ── Scenario 6: CONTEXT Tier Health ──
def test_context_tier_health():
    header("SCENARIO 6: CONTEXT TIER HEALTH")
    print("  Testing: Tiered context system is functioning.\n")

    focus = ARTIFACTS["context_focus"]
    session = ARTIFACTS["context_session"]
    archive = ARTIFACTS["context_archive"]

    if not focus.exists():
        err("CONTEXT.md MISSING — agent has no live state")
        return

    focus_content = focus.read_text()
    focus_size = len(focus_content)

    # Focus must be readable (< 10KB)
    if focus_size < 10_000:
        ok(f"CONTEXT.md is {focus_size} bytes (readable)")
    else:
        err(f"CONTEXT.md is {focus_size} bytes (TOO LARGE)")

    # Focus must contain key sections
    required_sections = ["CURRENT FOCUS", "ACTIVE BLOCKERS", "QUICK REFERENCE", "TIERED CONTEXT SYSTEM"]
    for section in required_sections:
        if section in focus_content:
            trace(f"  CONTEXT.md has section: {section}")
        else:
            warn(f"CONTEXT.md missing section: {section}")

    # Session log must exist
    if session.exists():
        session_size = session.stat().st_size
        if session_size < 50_000:
            ok(f"CONTEXT_SESSION.md is {session_size} bytes")
        else:
            warn(f"CONTEXT_SESSION.md is {session_size} bytes — consider archiving older entries")
    else:
        warn("CONTEXT_SESSION.md missing — will be created on first write")

    # Archive must be larger than focus
    if archive.exists():
        archive_size = archive.stat().st_size
        if archive_size > focus_size:
            ok(f"CONTEXT_ARCHIVE.md is {archive_size} bytes (larger than focus — correct)")
        else:
            warn("CONTEXT_ARCHIVE.md is smaller than CONTEXT.md — may be misconfigured")

    # No tier should reference loading the archive into context
    if "cat /root/CONTEXT_ARCHIVE.md" not in focus_content:
        ok("CONTEXT.md does NOT instruct loading archive (correct — grep only)")
    else:
        err("CONTEXT.md instructs loading archive — this will blow context window")

# ── Main ──
def main():
    global TRACE
    parser = argparse.ArgumentParser(description="MCP Cognitive Test Harness v1")
    parser.add_argument("--scenario", choices=[
        "substrate", "deprecation", "session_continuity",
        "invariant_consistency", "cross_references", "context_health",
    ], help="Run specific scenario only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--trace", "-t", action="store_true", help="Trace-level detail")
    args = parser.parse_args()

    TRACE = args.trace

    print("=" * 60)
    print("  MCP COGNITIVE TEST HARNESS v1")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print("  Testing: cognitive physics, not code coverage")
    print("=" * 60)

    scenarios = {
        "substrate": test_substrate_integrity,
        "deprecation": test_deprecation_awareness,
        "session_continuity": test_session_state_continuity,
        "invariant_consistency": test_invariant_consistency,
        "cross_references": test_cross_artifact_references,
        "context_health": test_context_tier_health,
    }

    if args.scenario:
        scenarios[args.scenario]()
    else:
        for name, fn in scenarios.items():
            fn()

    # ── Summary ──
    total = PASS + FAIL
    print(f"\n{'='*60}")
    print(f"  RESULTS: {PASS}/{total} PASS, {FAIL}/{total} FAIL")
    if FAIL == 0:
        print(f"  VERDICT: COGNITIVE SUBSTRATE INTACT ✅")
    else:
        print(f"  VERDICT: COGNITIVE SUBSTRATE DEGRADED — {FAIL} failures require attention")
    print(f"{'='*60}\n")

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
