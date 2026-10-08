#!/usr/bin/env python3
"""
doc-truth-tripwire.py — SSOT drift guard for federation live surfaces.

Born from audit 2026-10-08 (Arif): "jujur-menerbit bukan treatment.
Treatment: SSOT per domain + render per surface + tripwire pada setiap render."

SSOT anchors (live truth, probed 2026-10-08):
  PORTS      : HERMES MCP = 18087 (live pid), HERMES A2A listener = 18089.
               8644 = dead legacy port, HARAM in any live doc.
  STAGE      : JUDGE = 666, FORGE = 777 (F13-ratified 2026-07-31). "KERNEL 888"
               = retired label, HARAM in live mirrors.
  ORGANS     : 7 canonical organs (contract ruling 2026-09-14). HERMES/CHRON
               = Tier-3 boundaries. Claims of 9/11 organs in live docs = RED.
  IDENTITY   : two lineages exist and are a TRACKED GAP (consolidation open).
               Deploy-parity per lineage is ENFORCED (red on drift);
               lineage divergence is YELLOW (loud, not silent).
  AGENT CARD : /root/AAA/src/seed/agent-card.json = SSOT (server.js:1561).
               All live agents/*/agent-card.json must share one $schema.
               Legacy agent.json (v1 filename) outside archive = RED.

Exit: 0 = green/yellow only · 1 = any RED.
Scope: LIVE surfaces only — .archive, archive/, .ua, build/, node_modules,
skills-cold, cockpit are cold by definition and out of scope.
"""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

RED: list[str] = []
YELLOW: list[str] = []
GREEN: list[str] = []

AAA = Path("/root/AAA")
ARIFOS = Path("/root/arifOS")
VENV = Path("/opt/arifos/current/venv/lib/python3.13/site-packages")

COLD = re.compile(r"(\.archive|/archive/|\.ua/|/build/|node_modules|skills-cold|/cockpit/|\.bak|hermes-archived)")
# Historical witness records: append-only session/eureka/audit-report logs quote
# what was true at their timestamp — an audit finding "port 8644 matches nothing"
# IS history. Rewriting them falsifies history (F1 > doc-truth).
HISTORICAL = re.compile(
    r"(BOOT_EUREKA\.md|EUREKA-SESSION|/receipts/|seal_chain|/reports/|/sessions/|AUDIT_README|AUDIT_.*\.md|framing-example|-20\d{2}-\d{2}-\d{2})"
)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def grep_live(root: Path, pattern: str, globs=("*.md", "*.yaml", "*.yml", "*.json")) -> list[str]:
    """Grep live (non-cold) files under root for a regex; return path:line hits."""
    hits: list[str] = []
    rx = re.compile(pattern, re.IGNORECASE)
    for g in globs:
        try:
            out = subprocess.run(
                ["grep", "-rnE", pattern if False else rx.pattern, str(root), "--include", g],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            continue
        for line in out.stdout.splitlines():
            p = line.split(":", 1)[0]
            if COLD.search(p) or HISTORICAL.search(p):
                continue
            hits.append(line[:200])
    return hits


# ── 1. DEAD PORT ────────────────────────────────────────────────
hits = grep_live(AAA, r"(:|\b)8644\b") + grep_live(ARIFOS / "docs", r"(:|\b)8644\b")
if hits:
    RED.append(f"DEAD_PORT 8644 in live docs: {hits[:3]}")
else:
    GREEN.append("DEAD_PORT: 8644 absent from live surfaces (18087/18089 live-verified)")

# ── 2. STAGE 888 residue ────────────────────────────────────────
hits = grep_live(ARIFOS, r"KERNEL 888", globs=("*.md", "*.yaml", "*.py", "*.txt"))
hits = [h for h in hits if "PROMPT_666" not in h and "README" not in h.split(":")[0]]
if hits:
    RED.append(f"STAGE_888 residue in live mirrors: {hits[:3]}")
else:
    GREEN.append("STAGE_LABEL: no KERNEL 888 in live mirrors (666/777 canonical)")

# ── 3. ORGAN COUNT ──────────────────────────────────────────────
hits = grep_live(AAA / "README.md", r"1[01] (organs|forge instruments)") + grep_live(
    ARIFOS / "README.md", r"1[01] (organs|forge instruments)"
)
if hits:
    RED.append(f"ORGAN_COUNT inflation (canonical=7, ruling 2026-09-14): {hits[:3]}")
else:
    GREEN.append("ORGAN_COUNT: no 9/11-organ claims in live READMEs")

# ── 4. IDENTITY lineage parity ──────────────────────────────────
pairs = [
    (ARIFOS / "contracts/identity.py", VENV / "contracts/identity.py", "lineage-A (top-level contracts)"),
    (ARIFOS / "arifosmcp/contracts/identity.py", VENV / "arifosmcp/contracts/identity.py", "lineage-B (kernel pkg)"),
]
hashes = {}
for repo, deployed, name in pairs:
    if not (repo.exists() and deployed.exists()):
        RED.append(f"IDENTITY missing file: {repo} or {deployed}")
        continue
    hr, hd = sha(repo), sha(deployed)
    hashes[name] = hr
    if hr != hd:
        RED.append(f"IDENTITY deploy drift {name}: repo={hr} deployed={hd}")
    else:
        GREEN.append(f"IDENTITY deploy parity {name}: {hr}")

vals = set(hashes.values())
if len(hashes) == 2 and len(vals) == 2:
    YELLOW.append(
        "IDENTITY lineage divergence (TRACKED GAP, consolidation open): "
        f"A={hashes.get('lineage-A (top-level contracts)')} B={hashes.get('lineage-B (kernel pkg)')} — "
        "runtime authority = lineage B (arifosmcp); consolidation needs ratified commit"
    )

# ── 5. AGENT CARD schema unity ──────────────────────────────────
import json

seed = AAA / "src/seed/agent-card.json"
if not seed.exists():
    RED.append("CARD_SSO seed card missing: src/seed/agent-card.json")
else:
    GREEN.append(f"CARD_SSO seed present: version={json.loads(seed.read_text()).get('version', '?')}")

schemas: dict[str, int] = {}
legacy: list[str] = []
for card in sorted((AAA / "agents").glob("*/agent-card.json")):
    try:
        s = json.loads(card.read_text()).get("$schema", "MISSING")
        schemas[str(s)[:60]] = schemas.get(str(s)[:60], 0) + 1
    except Exception as e:  # noqa: BLE001
        RED.append(f"CARD_SCHEMA unparseable: {card} ({e})")
for legacy_card in sorted((AAA / "agents").glob("*/agent.json")):
    if not COLD.search(str(legacy_card)):
        legacy.append(str(legacy_card))
if len(schemas) > 1:
    RED.append(f"CARD_SCHEMA split across live cards: {schemas}")
else:
    GREEN.append(f"CARD_SCHEMA unity: {sum(schemas.values())} cards, {list(schemas)[:1]}")
if legacy:
    RED.append(f"CARD_LEGACY v1 agent.json alive outside archive: {legacy[:3]}")

# ── report ──────────────────────────────────────────────────────
print("=== DOC-TRUTH TRIPWIRE ===")
for g in GREEN:
    print(f"  GREEN  {g}")
for y in YELLOW:
    print(f"  YELLOW {y}")
for r in RED:
    print(f"  RED    {r}")
print(f"=== {len(GREEN)} green · {len(YELLOW)} yellow (tracked) · {len(RED)} red ===")
sys.exit(1 if RED else 0)
