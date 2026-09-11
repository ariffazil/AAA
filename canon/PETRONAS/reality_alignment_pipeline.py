#!/usr/bin/env python3
"""
reality_alignment — autonomous pipeline (forged 2026-09-12, F13 ceiling ratified).
Capability: diff S1 truth vs S3 recall vs live surface → emit FRESH/STALE/DRIFT/CONFLICT.

AUTONOMY CEILING (Arif 2026-09-12):
    AUTO:  DETECT drift → WITNESS (jsonl) → COMMIT (reversible git, atlas only) → RECEIPT
    F13:   SEAL (never — no VAULT999 write from this loop)

SCOPE:
    PETRONAS atlas (AAA/canon/PETRONAS) ↔ WEALTH engine (petronas_vitals.py)
    ↔ live /vitals ↔ arifOS entities ↔ evidence corpus ↔ Qdrant petronas_knowledge

AUTO-FIX is NARROW and one-directional:
    ONLY the ATLAS.md Brent-sensitivity anchor line, and ONLY when it drifts from the
    WEALTH engine (compute = source of truth). Everything else = WITNESS-ONLY (report).

    Never mutates: arifOS entities, WEALTH engine, public surface, Qdrant, VAULT999.

Output: drift report on stdout + append-only witness at drift_witness.jsonl.
Exit 0 = no auto-fixable drift (or fix applied). Exit 1 = witness-only drift found.
"""
import json, os, sys, subprocess, urllib.request, datetime, re

ROOT = "/root"
ATLAS = f"{ROOT}/AAA/canon/PETRONAS/ATLAS.md"
KG = f"{ROOT}/AAA/canon/PETRONAS/KNOWLEDGE_GRAPH.json"
WITNESS = f"{ROOT}/AAA/canon/PETRONAS/drift_witness.jsonl"
BASE = "https://arif-fazil.com"
QDRANT = "http://localhost:6333"

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

def http_get(url, timeout=6):
    try:
        return urllib.request.urlopen(url, timeout=timeout).read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"

def http_post(url, payload, timeout=6):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))

def witness(ts, check, status, detail):
    rec = {"ts": ts, "check": check, "status": status, "detail": detail}
    with open(WITNESS, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[{status}] {check}: {detail}")
    return rec

def engine_anchors():
    sys.path.insert(0, f"{ROOT}/WEALTH/wealth_core")
    import petronas_vitals as pv
    out = {}
    for b in (100.60, 84.10, 67.34, 50.00):
        r = pv.compute_brent_sensitivity(b)
        out[b] = (round(r["projected_full_year_pat_usd_b"], 1), r["projected_extraction_ratio"])
    out["pulse"] = pv.compute_petronas_vitals().get("pulse")
    out["threshold"] = pv.compute_brent_sensitivity(84.10)["brent_threshold_for_exit_usd"]
    return out

def check_atlas_brent(eng):
    """Does ATLAS.md Brent line match engine? Auto-fix if drifted."""
    txt = open(ATLAS).read()
    m = re.search(r"- \*\*Brent sensitivity \(WEALTH[^\n]*\n?", txt)
    line = m.group(0) if m else ""
    want = (
        f"- **Brent sensitivity (WEALTH `compute_brent_sensitivity()`, engine-calibrated):** "
        f"${100.60:.2f} → PAT RM{eng[100.60][0]:.1f}B, extraction {eng[100.60][1]}% (exit {'✅' if eng[100.60][1] < 55 else '❌'}) · "
        f"${84.10:.2f} → RM{eng[84.10][0]:.1f}B, {eng[84.10][1]}% ({'✅' if eng[84.10][1] < 55 else '❌'}) · "
        f"**${eng['threshold']:.2f} → RM36.4B, 55.0% (⚠️ threshold)** · "
        f"${50.00:.2f} → RM{eng[50.00][0]:.1f}B, {eng[50.00][1]}% (❌). "
        f"Exit threshold: **Brent > ${eng['threshold']:.2f} sustained.** War-driven, not structural.\n"
    )
    if line and line.strip() == want.strip():
        return ("OK", "atlas Brent line matches engine", False)
    return ("DRIFT", f"atlas Brent line drifted from engine (auto-fixable)", True)

def auto_fix_brent(eng):
    txt = open(ATLAS).read()
    new_line = (
        f"- **Brent sensitivity (WEALTH `compute_brent_sensitivity()`, engine-calibrated):** "
        f"$100.60 → PAT RM{eng[100.60][0]:.1f}B, extraction {eng[100.60][1]}% (exit {'✅' if eng[100.60][1] < 55 else '❌'}) · "
        f"$84.10 → RM{eng[84.10][0]:.1f}B, {eng[84.10][1]}% ({'✅' if eng[84.10][1] < 55 else '❌'}) · "
        f"**${eng['threshold']:.2f} → RM36.4B, 55.0% (⚠️ threshold)** · "
        f"$50.00 → RM{eng[50.00][0]:.1f}B, {eng[50.00][1]}% (❌). "
        f"Exit threshold: **Brent > ${eng['threshold']:.2f} sustained.** War-driven, not structural."
    )
    txt, n = re.subn(r"- \*\*Brent sensitivity \(WEALTH[^\n]*", new_line, txt, count=1)
    if n == 1:
        open(ATLAS, "w").write(txt)
        return True
    return False

def check_paths():
    nodes = json.load(open(KG))
    missing = [n["path"] for n in nodes["nodes"] if not os.path.exists(n["path"])]
    return missing

def check_entities():
    ents = [
        f"{ROOT}/arifOS/memory/entities/PETRONAS_INTERNAL_ANALYTICAL_GRAPH_2026.md",
        f"{ROOT}/arifOS/memory/entities/petronas/00-EPISTEMIC-HEADER.md",
        f"{ROOT}/arifOS/memory/entities/PETRONAS_Collapse_Trajectory_v3_2026.json",
        f"{ROOT}/arifOS/memory/entities/PETRONASThirdAxisCollapse2026.json",
    ]
    return [p for p in ents if not os.path.exists(p)]

def check_live():
    html = http_get(f"{BASE}/vitals/")
    missing = []
    for s in ("70.5%", "sealed:\"2026-08-03\"", "20.29", "100.60"):
        if s not in html:
            missing.append(s)
    return missing

def check_qdrant():
    try:
        c = http_post(f"{QDRANT}/collections/petronas_knowledge/points/count", {"exact": True})
        n = c.get("result", {}).get("count", -1)
    except Exception as e:
        return f"qdrant unreachable: {e}"
    if n <= 0:
        return f"petronas_knowledge EMPTY (count={n})"
    # sample one point for staleness (revenue anchor)
    try:
        pts = http_post(f"{QDRANT}/collections/petronas_knowledge/points/scroll", {"limit": 5, "with_payload": True})
        revenue_hits = []
        for p in pts.get("result", {}).get("points", []):
            t = (p.get("payload") or {}).get("text", "")
            mm = re.search(r"revenue FY2025:\s*RM([\d\.]+)\s*billion", t)
            if mm and abs(float(mm.group(1)) - 266.1) > 1.0:
                revenue_hits.append(mm.group(1))
        if revenue_hits:
            return f"STALE: {len(revenue_hits)} sampled vectors claim revenue RM{set(revenue_hits)} != RM266.1B"
        return f"OK: {n} points, no stale revenue anchor in sample"
    except Exception as e:
        return f"sample err: {e}"

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    print(f"=== PETRONAS knowledge loop {ts} ===")
    auto_fixable = []

    # Engine (source of truth)
    eng = engine_anchors()
    print(f"engine: {json.dumps(eng)}")

    # Atlas Brent line vs engine (auto-fixable)
    st, det, fixable = check_atlas_brent(eng)
    witness(ts, "atlas_brent_vs_engine", st, det)
    if fixable:
        auto_fixable.append("atlas_brent")

    # Node paths
    miss = check_paths()
    witness(ts, "atlas_node_paths", "OK" if not miss else "DRIFT",
            f"{len(miss)} orphan paths" if miss else "all resolve")
    if miss:
        print("  orphan:", miss)

    # Entities
    me = check_entities()
    witness(ts, "entities", "OK" if not me else "DRIFT", f"{me}" if me else "all resolve")

    # Live surface
    ml = check_live()
    witness(ts, "live_vitals_anchors", "OK" if not ml else "DRIFT",
            f"missing {ml}" if ml else "anchors present")

    # Qdrant freshness
    q = check_qdrant()
    witness(ts, "qdrant_freshness", "OK" if q.startswith("OK") else "DRIFT", q)

    # AUTO-FIX (narrow: atlas Brent line only)
    if auto_fixable:
        for item in auto_fixable:
            if item == "atlas_brent":
                if auto_fix_brent(eng):
                    r = sh(f"cd {ROOT}/AAA && git add canon/PETRONAS/ATLAS.md && git commit -q -m 'loop: auto-fix atlas Brent anchors to engine' && echo committed")
                    witness(ts, "auto_fix_atlas_brent", "COMMIT", r or "committed")
                else:
                    witness(ts, "auto_fix_atlas_brent", "FAIL", "regex replace failed — manual review needed")

    print(f"=== witness appended to {WITNESS} ===")
    return 1 if (miss or me or ml or (not q.startswith('OK'))) else 0

if __name__ == "__main__":
    sys.exit(main())
