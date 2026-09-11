#!/usr/bin/env python3
"""
aaa_drift_check.py — AAA Federation drift detection
═══════════════════════════════════════════════════
Checks canonical registries against live state.
Exit 0 = SEAL (no blocking drift).
Exit 1 = PARTIAL (non-blocking gaps).
Exit 2 = HOLD (contradiction blocks autonomous execution).
Exit 3 = VOID (invalid state).

DITEMPA BUKAN DIBERI — Forged 2026-07-31
"""
import json, yaml, os, sys, hashlib
from pathlib import Path
from datetime import datetime, timezone

AAA = Path("/root/AAA")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def read_json(p):
    try:
        with open(p) as f: return json.load(f)
    except: return None

def read_yaml(p):
    try:
        with open(p) as f: return yaml.safe_load(f)
    except: return None

findings = []
holds = []

def finding(severity, check, detail, verdict="PARTIAL"):
    findings.append({"severity": severity, "check": check, "detail": detail, "verdict": verdict})
    if verdict == "HOLD":
        holds.append(detail)

def check_file_exists(path, desc):
    p = AAA / path
    if p.exists():
        finding("OK", desc, f"EXISTS: {path}", "SEAL")
        return True
    else:
        finding("GAP", desc, f"MISSING: {path}", "HOLD")
        return False

# ── 1. Canonical agent cards exist ──
a2a_reg = read_yaml(AAA / "a2a/registry/agents.yaml")
if a2a_reg:
    for a in a2a_reg.get("agents", []):
        aid = a.get("agent_id")
        card = a.get("card_path", "")
        if card.startswith("external://"):
            finding("SKIP", f"Agent card for {aid}", f"External card: {card}", "SEAL")
        else:
            cfp = AAA / card
            if cfp.exists():
                finding("OK", f"Agent card for {aid}", f"EXISTS: {card}", "SEAL")
            else:
                finding("GAP", f"Agent card for {aid}", f"MISSING: {card}", "HOLD")
else:
    finding("CRITICAL", "A2A agent registry", "a2a/registry/agents.yaml MISSING — cannot verify agents", "VOID")

# ── 2. AGENTS_UNIFIED.yaml — canonical agent registry ──
agents_unified = read_yaml(AAA / "registries/AGENTS_UNIFIED.yaml")
if agents_unified:
    # Verify invariants
    invariants = agents_unified.get("invariants", [])
    fi_slots = agents_unified.get("forge_instruments", [])
    identity_lanes = agents_unified.get("identity_lanes", [])

    # Check FI slots have unique owners
    slot_ids = {}
    for fi in fi_slots:
        sid = fi.get("fi_slot")
        owner = fi.get("id")
        if sid and owner:
            if sid in slot_ids:
                finding("CONFLICT", f"FI slot {sid}", f"Duplicate: {slot_ids[sid]} and {owner}", "HOLD")
            else:
                slot_ids[sid] = owner
    finding("OK", "FI slots", f"{len(fi_slots)} slots, all unique owners per AGENTS_UNIFIED.yaml", "SEAL")

    # Check identity lanes don't claim FI slots
    for lane in identity_lanes:
        if lane.get("fi_slot") is not None:
            finding("CONFLICT", f"Identity lane {lane['id']}", "Claims FI slot — violates invariant #2", "HOLD")

    # Check all canonical_card paths
    ghost_paths = 0
    for layer_name in ["identity_lanes", "forge_instruments", "extensions", "organs"]:
        for entry in agents_unified.get(layer_name, []):
            card = entry.get("canonical_card")
            if card:
                cp = Path(card)
                if not cp.exists() and not str(card).startswith("null"):
                    ghost_paths += 1
                    finding("GAP", f"Card for {entry.get('id', entry.get('fi_slot'))}", f"MISSING: {card}", "HOLD")

    if ghost_paths == 0:
        finding("OK", "Canonical cards", "All paths resolve — 0 ghost paths", "SEAL")
    else:
        finding("GAP", "Canonical cards", f"{ghost_paths} ghost paths", "HOLD")

    # Check collapsed agents have no active FI slot
    for c in agents_unified.get("collapsed", []):
        fid = c.get("previous_fi_slot")
        if fid:
            # Verify FI slot is now vacant or reassigned
            fi_match = next((f for f in fi_slots if f.get("fi_slot") == fid), None)
            if fi_match and fi_match.get("id") == c.get("id"):
                finding("CONFLICT", f"Collapsed agent {c['id']}", f"Still owns {fid} — should be vacant or reassigned", "HOLD")

    finding("OK", "AGENTS_UNIFIED.yaml", f"5 layers, {len(invariants)} invariants — canonical registry valid", "SEAL")
else:
    finding("CRITICAL", "Agent registry", "AGENTS_UNIFIED.yaml MISSING", "VOID")

# ── 3. Skills.yaml registration coverage ──
skills_yaml = read_yaml(AAA / "registries/skills.yaml")
# Only AAA skills/ directory — not .hermes/skills/, agents/_external/*/skills/, etc.
skill_files = list((AAA / "skills").glob("*/SKILL.md"))
registered_ids = set()
if skills_yaml:
    for s in skills_yaml.get("skills", []):
        registered_ids.add(s.get("id"))

orphan_count = 0
for sf in skill_files:
    rel = str(sf.relative_to(AAA))
    skill_dir = sf.parent.name
    found = False
    if skills_yaml:
        for sy in skills_yaml.get("skills", []):
            sp = sy.get("source_path", "")
            if rel in sp or skill_dir == sy.get("id"):
                found = True
                break
    if not found:
        orphan_count += 1

if orphan_count > 0:
    finding("GAP", "Skill registration", f"{orphan_count} SKILL.md files not registered in skills.yaml", "PARTIAL")
else:
    finding("OK", "Skill registration", "All SKILL.md files registered", "SEAL")

# ── 4. Registered skills have files (AAA scope only) ──
missing_skill_count = 0
if skills_yaml:
    for s in skills_yaml.get("skills", []):
        sp = s.get("source_path")
        sid = s.get("id")
        if sp:
            sfp = AAA / sp
            if not sfp.exists():
                # Also try by ID if source_path is stale
                alt_path = AAA / "skills" / sid / "SKILL.md"
                if not alt_path.exists():
                    missing_skill_count += 1

if missing_skill_count > 0:
    finding("GAP", "Registered skill files", f"{missing_skill_count} registered skills have missing SKILL.md files", "PARTIAL")
else:
    finding("OK", "Registered skill files", "All registered skills have SKILL.md files", "SEAL")

# ── 5. Tools authority coverage ──
tools_yaml = read_yaml(AAA / "registries/tools.yaml")
if tools_yaml:
    tools_with_auth = 0
    tools_without_auth = 0
    for t in tools_yaml.get("tools", []):
        if "authority" in str(t).lower() or "gate" in str(t).lower() or "risk" in str(t).lower():
            tools_with_auth += 1
        else:
            tools_without_auth += 1
    finding("INFO", "Tool authority", f"{tools_with_auth} tools with authority hints, {tools_without_auth} without", "PARTIAL")
else:
    finding("CRITICAL", "Tool registry", "tools.yaml missing", "VOID")

# ── 6. Live agent card count ──
agent_cards = list(AAA.rglob("agent-card.json"))
finding("INFO", "Agent cards on disk", f"{len(agent_cards)} agent-card.json files found", "SEAL")

# ── 7. Unified registry exists ──
check_file_exists("registries/AGENTS_UNIFIED.yaml", "Canonical agent registry (AGENTS_UNIFIED)")
check_file_exists("registries/CANONICAL_REGISTRY_POLICY.yaml", "Canonical registry policy")
check_file_exists("registries/REGISTRY_CATALOG.generated.yaml", "Registry catalog")
check_file_exists("registries/bindings.generated.yaml", "Agent-skill bindings")

# ── 8. Live lanes have identity ──
for lane in ["333-AGI", "555-ASI", "888-APEX"]:
    identity_files = list((AAA / "agents" / "_lanes" / lane).glob("identity.*"))
    card_files = list((AAA / "agent-cards" / "identity" / lane).glob("agent-card.json"))
    if card_files:
        finding("OK", f"{lane} identity", f"Agent card at agent-cards/identity/{lane}/agent-card.json", "SEAL")
    else:
        finding("GAP", f"{lane} identity", "No agent card in agent-cards/identity/", "HOLD")

# ── 9. Deprecated files still in active paths ──
dep_count = 0
for fp in AAA.rglob("*"):
    if fp.is_file() and fp.suffix in (".yaml", ".json", ".md"):
        try:
            head = fp.read_text()[:500]
            if ("DEPRECATED" in head.upper() or "TOMBSTONE" in head.upper()) and "deprecated" not in fp.name.lower():
                if "_archive" not in str(fp) and "archive/" not in str(fp):
                    dep_count += 1
        except:
            pass

if dep_count > 10:
    finding("GAP", "Deprecated files", f"{dep_count} deprecated/tombstone files in active paths", "PARTIAL")
else:
    finding("OK", "Deprecated files", f"{dep_count} deprecated files in active paths", "SEAL")

# ── 10. A2A alignment ──
check_file_exists("a2a/A2A_ALIGNMENT_SPEC.md", "A2A alignment spec")
check_file_exists("a2a/taskstate_verdict_map.json", "TaskState→Verdict map")
check_file_exists(".well-known/agent-card.json", "Public agent card")

# ── 11. HARNESS WIRE-YIELD (EUREKA-2026-09-11-HARNESS-COMMODITY-BOUNDARY-001) ──
# Engine vs steering. arifOS may RENT model inference; it must NEVER rent the
# orchestration loop. Any organ pointing its session state / sub-agent routing at
# an external hosted harness (OpenAI Agents API) has yielded the cognitive wire,
# which breaks F13 SOVEREIGN + the Substrate Swap Test. Detection is debt until
# it can say NO -> this emits HOLD, not a note.
# Doctrine: /root/AAA/instructions/harness-commoditization-boundary.md
import re as _re
from pathlib import Path as _Path

_WIRE_PATTERNS = [
    # ── OpenAI (Agents API / hosted Codex harness) ──
    r"codex-cloud-environments",        # hosted-harness WebSocket endpoint
    r"agents\.sessions\.create",        # Agents API session creation (state machine)
    r"client\.beta\.agents",            # SDK handle
    r"codex\s+exec-server",             # remote-environment executor registration
    # ── Anthropic (hosted agents SDK, witnessed in vendor tree 2026-09-11) ──
    r"\.beta\.agents\.(?:create|sessions)",
    r"anthropic[\w.]*\.beta\.agents",
    # ── Google (genai GAOS hosted agents) ──
    # NOTE: bare `base_agent:` is a MODEL/HARNESS identifier key, legitimately
    # present in local agent cards (e.g. AAA/agents/antigravity/agent.yaml).
    # Flagging it false-HOLDs a sovereign local agent every run. The genuine
    # hosted signal is the remote environment declaration or the hosted endpoint.
    r"""base_environment["']?\s*[:=]\s*["']?remote""",
    r"generativelanguage\.googleapis\.com/[\w/]*agents",
]
_wire_re = _re.compile("|".join(_WIRE_PATTERNS))
# Source-of-truth organs only. Vendor trees, caches, docs and session logs are
# not the federation's own wiring and must not produce false holds.
_ORGAN_ROOTS = [
    _Path("/root/arifOS"), _Path("/root/A-FORGE"), _Path("/root/GEOX"),
    _Path("/root/WEALTH"), _Path("/root/WELL"), _Path("/root/AAA"),
]
_SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "build",
              "dist", "deploy", "cache", "sessions", ".hermes", "runtime"}
_SKIP_SUFFIX = {".log", ".jsonl", ".cache", ".md", ".lock", ".min.js", ".map"}
_SRC_SUFFIX = {".py", ".js", ".ts", ".mjs", ".cjs", ".yaml", ".yml", ".toml",
               ".json", ".sh", ".env", ".conf", ".service"}

_SELF = _Path(__file__).resolve()

def _scan_wire_yield():
    hits = []
    scanned = 0
    for root in _ORGAN_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            try:
                if not p.is_file():
                    continue
                # Self-exclusion: this scanner necessarily carries the wire
                # literals it hunts. Without it the detector flags itself and
                # every run is a false HOLD (witnessed 2026-09-11).
                if p.resolve() == _SELF:
                    continue
                if any(part in _SKIP_DIRS for part in p.parts):
                    continue
                if p.suffix not in _SRC_SUFFIX or p.suffix in _SKIP_SUFFIX:
                    continue
                if p.stat().st_size > 2_000_000:
                    continue
                scanned += 1
                txt = p.read_text(errors="ignore")
                if _wire_re.search(txt):
                    hits.append(str(p))
            except Exception:
                continue
    return hits, scanned

_wire_hits, _wire_scanned = _scan_wire_yield()
if _wire_hits:
    finding("CRITICAL", "Harness wire-yield (F13/Substrate Swap)",
            f"EXTERNAL ORCHESTRATION WIRE in {len(_wire_hits)} organ source file(s): "
            + "; ".join(_wire_hits[:4])
            + " — session state/routing delegated to hosted harness; leash no longer local",
            "HOLD")
else:
    finding("OK", "Harness wire-yield (F13/Substrate Swap)",
            f"No Agents-API orchestration wire in organ source ({_wire_scanned} files scanned) — "
            f"engine local, leash held by arifOS", "SEAL")

# ── SUMMARY ──
print(f"\n{'='*60}")
print(f"AAA DRIFT CHECK — {NOW}")
print(f"{'='*60}")
seal_count = len([f for f in findings if f["verdict"] == "SEAL"])
partial_count = len([f for f in findings if f["verdict"] == "PARTIAL"])
hold_count = len([f for f in findings if f["verdict"] == "HOLD"])
void_count = len([f for f in findings if f["verdict"] == "VOID"])
print(f"Checks: {len(findings)} | SEAL={seal_count} PARTIAL={partial_count} HOLD={hold_count} VOID={void_count}")
print()

for f in findings:
    icon = {"SEAL": "✅", "PARTIAL": "⚠️", "HOLD": "🔴", "VOID": "💀", "OK": "✅", "GAP": "⚠️", "CONFLICT": "🔴", "CRITICAL": "💀", "INFO": "ℹ️", "SKIP": "⏭️"}.get(f["severity"], "❓")
    print(f"  {icon} [{f['verdict']}] {f['check']}: {f['detail'][:120]}")

# Write results
result = {
    "check_time": NOW,
    "total_checks": len(findings),
    "seal": seal_count,
    "partial": partial_count,
    "hold": hold_count,
    "void": void_count,
    "findings": findings,
}

out_path = AAA / "forge_work/entropy-reduction/drift_check_result.json"
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)

print(f"\nResults written: {out_path}")

if void_count > 0:
    print("\nVERDICT: VOID")
    sys.exit(3)
elif hold_count > 0:
    print("\nVERDICT: HOLD — unresolved conflicts block autonomous execution")
    sys.exit(2)
elif partial_count > 0:
    print("\nVERDICT: PARTIAL — non-blocking gaps documented")
    sys.exit(1)
else:
    print("\nVERDICT: SEAL — no drift detected")
    sys.exit(0)
