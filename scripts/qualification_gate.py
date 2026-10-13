#!/usr/bin/env python3
"""
qualification_gate.py — CI constitutional conformance gate for the AAA agent/plugin surface.

Implements BIJAKSANA WAJIB #57 (CI constitutional tests) + #58 (adversarial canaries)
for the qualification surface (audit FL-5, F13 order 2026-09-25).

Honest by design: tests that FAIL report FAIL. A green gate over a red mesh is theatre.
Exit 0 only when every test passes.

Run:  python3 /root/AAA/scripts/qualification_gate.py
"""
from __future__ import annotations
import glob, json, os, re, sys

AAA = "/root/AAA"
CANON = f"{AAA}/canon/APEX-MATH-CANON-2026-09-23.md"
VALID_LAYERS = {"L0","L0.5","L1","L1.5","L2","L3","L4","L4.5","L5","L6",
                "L7","L7.5","L8","L8.5","L9","L10","L11","L12","meta-L9"}
VALID_CS = {"CANON_DERIVED","UNVERIFIED","MEASURED","HUMAN_PRINCIPAL"}
FED_ORGANS = re.compile(r"arifos|well|wealth|geox|forge|arif-?irfan|chron", re.I)

results: list[tuple[str, bool, str]] = []

def record(name, ok, detail):
    results.append((name, ok, detail))

def load_cards():
    paths = sorted(set(
        glob.glob(f"{AAA}/agent-cards/**/agent-card*.json", recursive=True)
        + glob.glob(f"{AAA}/agents/_external/*/agent-card.json")))
    cards = []
    for p in paths:
        if os.path.getsize(p) < 1024:
            continue
        try:
            cards.append((p, json.load(open(p))))
        except Exception:
            pass
    return paths, cards

# ── T1 structure ─────────────────────────────────────────────────────
def t1_structure(paths, cards):
    missing = [p for p, d in cards
               if not isinstance(d.get("qualification"), dict)
               or d["qualification"].get("schema") != "arifOS/qualification/v1"]
    record("T1 qualification block on every card", not missing,
           f"{len(cards)-len(missing)}/{len(cards)} carry arifOS/qualification/v1"
           + (f" · MISSING: {missing}" if missing else ""))

# ── T2 vocabulary ────────────────────────────────────────────────────
def t2_vocabulary(cards):
    bad = []
    for p, d in cards:
        q = d.get("qualification", {})
        mc = q.get("math_competency", {})
        layers, cs = mc.get("layers"), mc.get("claim_state")
        if cs not in VALID_CS:
            bad.append((p, f"claim_state {cs!r}")); continue
        if layers is not None:
            if not isinstance(layers, list) or not set(layers) <= VALID_LAYERS or not layers:
                bad.append((p, f"bad layers {layers}"))
        for sub in (q.get("irfan", {}).get("least_power", {}),
                    q.get("irfan", {}).get("abstention", {}),
                    q.get("epistemic_typing", {})):
            if sub and sub.get("claim_state") not in VALID_CS:
                bad.append((p, f"sub-state {sub.get('claim_state')!r}"))
    record("T2 layer vocabulary + claim-state enum", not bad, f"{len(cards)} checked" + (f" · BAD: {bad[:4]}" if bad else ""))

# ── T3 no unbacked MEASURED + adversarial self-test ─────────────────
def unbacked(d):
    q = d.get("qualification", {})
    out = []
    def walk(node, path):
        if isinstance(node, dict):
            if node.get("claim_state") == "MEASURED" and not node.get("evidence"):
                out.append(path)
            for k, v in node.items():
                walk(v, f"{path}.{k}")
    walk(q, "qualification")
    return out

def t3_measured_backing(cards):
    bad = []
    for p, d in cards:
        bad += [(p, path) for path in unbacked(d)]
    # adversarial canary: validator must reject a fabricated MEASURED-without-evidence card
    forged = {"qualification": {"math_competency": {"layers": ["L0"], "source": "air", "claim_state": "MEASURED"}}}
    canary_ok = bool(unbacked(forged))   # must DETECT the forgery
    record("T3 MEASURED claims carry evidence", not bad and canary_ok,
           f"{len(cards)} checked · forgery-detection canary {'OK' if canary_ok else 'BLIND'}"
           + (f" · UNBACKED: {bad[:4]}" if bad else ""))

# ── T4 organ cards declare authority bound (least-power) ────────────
def t4_organ_authority(cards):
    bad = [p for p, d in cards
           if "/organs/" in p
           and d.get("qualification", {}).get("irfan", {}).get("least_power", {}).get("claim_state") != "MEASURED"]
    record("T4 organ cards declare authority bound", not bad,
           f"organ cards least-power MEASURED" + (f" · MISSING: {bad}" if bad else ""))

# ── T5 canon referential integrity ──────────────────────────────────
def t5_canon_ref(cards):
    bad = [(p, d["qualification"]["math_competency"].get("source"))
           for p, d in cards
           if d.get("qualification", {}).get("math_competency", {}).get("claim_state") == "CANON_DERIVED"
           and "APEX-MATH-CANON-2026-09-23" not in str(d["qualification"]["math_competency"].get("source"))]
    record("T5 CANON_DERIVED sources cite existing canon", (not bad) and os.path.exists(CANON),
           f"canon {'present' if os.path.exists(CANON) else 'MISSING'}" + (f" · BAD: {bad[:3]}" if bad else ""))

# ── T6 phantom-plugin canary ────────────────────────────────────────
def t6_phantom_plugins():
    manifests = []
    for dirpath, dirnames, filenames in os.walk("/root/.codex/plugins/cache"):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        manifests += [os.path.join(dirpath, f) for f in filenames if f == "plugin.json"]
    stubs = []
    for m in manifests:
        try:
            d = json.load(open(m))
        except Exception:
            continue
        label = json.dumps(d)
        wired = bool(d.get("mcpServers") or d.get("hooks") or d.get("skills")
                     or (d.get("interface") or {}).get("capabilities"))
        if FED_ORGANS.search(label) and not wired:
            stubs.append(m)
    record("T6 no phantom federation plugins in cache", not stubs,
           f"{len(manifests)} manifests · {len(stubs)} phantom stubs wearing organ names with zero wiring"
           + (f" · purge queue: {sorted(set(stubs))[:3]}…" if stubs else ""))

# ── T7 mesh hygiene ─────────────────────────────────────────────────
def t7_mesh(paths, cards):
    broken = []
    for root in (f"{AAA}/skills",):
        for dirpath, _, files in os.walk(root):
            for f in files:
                fp = os.path.join(dirpath, f)
                if os.path.islink(fp) and not os.path.exists(fp):
                    broken.append(fp)
    ids = [str(d.get("id") or d.get("agentId") or d.get("name")) for _, d in cards]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    record("T7a no broken skill symlinks", not broken, f"{len(broken)} broken" + (f": {broken[:4]}" if broken else ""))
    record("T7b unique card identity", not dupes, f"duplicate ids: {dupes}" if dupes else "all unique")

# ── T8 card-directory debris ────────────────────────────────────────
def t8_debris(paths):
    dirs = {os.path.dirname(p) for p in paths}
    debris = []
    for d in dirs:
        for f in glob.glob(f"{d}/*.json"):
            if os.path.basename(f) != "agent-card.json" and os.path.getsize(f) < 1024:
                debris.append(f)
    record("T8 no sub-1KB json debris in card dirs", not debris,
           f"{len(debris)} debris files" + (f": {debris[:4]}" if debris else ""))

def main():
    paths, cards = load_cards()
    t1_structure(paths, cards)
    t2_vocabulary(cards)
    t3_measured_backing(cards)
    t4_organ_authority(cards)
    t5_canon_ref(cards)
    t6_phantom_plugins()
    t7_mesh(paths, cards)
    t8_debris(paths)

    print(f"QUALIFICATION GATE · {len(cards)} cards · {len(results)} tests")
    print("─" * 72)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name:<44} {detail}")
    fails = sum(1 for _, ok, _ in results if not ok)
    print("─" * 72)
    print(f"VERDICT: {'GATE_GREEN' if fails == 0 else f'GATE_RED ({fails} failing — queue, not theatre)'}")
    return 0 if fails == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
