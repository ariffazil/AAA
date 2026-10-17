#!/usr/bin/env python3
"""
arifOS Audit Probe Suite — reproducible snapshot tooling
========================================================
PURPOSE:  Produce repeatable snapshots of federation memory state so that
          future audits NEVER hallucinate numbers. Witness before interpretation.
          (F1 reversible · F2 truth · F11 auditable · F4 delta-S reduced)

OUTPUT:   /root/AAA/audit/probes/probe_<ts>.json  (machine) + console (human)

USAGE:
  probe_audit.py qdrant     -> Qdrant vector collections census
  probe_audit.py falkordb   -> FalkorDB graph census
  probe_audit.py scheduler  -> cron + systemd timer manifest
  probe_audit.py all        -> all three (default)

METHOD (reproducible — anyone can rerun to reach the same numbers):
  Qdrant:    GET  localhost:6333/collections/{name}  (points_count, dim, distance)
  FalkorDB:  redis-cli -p 6380 GRAPH.QUERY <g> "MATCH (n) RETURN count(n)"
  Scheduler: crontab -l  +  /etc/cron.d/*  +  systemctl list-timers

DITEMPA BUKAN DIBERI ⚒️
"""
import json, subprocess, sys, urllib.request, datetime, collections

TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT_DIR = "/root/AAA/audit/probes"
import os
os.makedirs(OUT_DIR, exist_ok=True)

def _http_json(url, timeout=6):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"_error": str(e)}

def probe_qdrant():
    """Witness: exact points per collection. Must never report '0' on a 2019 store."""
    data = _http_json("http://localhost:6333/collections")
    cols = data.get("result", {}).get("collections", [])
    rows = []
    total = 0; populated = 0; empty = 0
    for c in sorted(cols, key=lambda x: x["name"]):
        d = _http_json(f"http://localhost:6333/collections/{c['name']}")
        r = d.get("result", {})
        if not isinstance(r, dict):
            rows.append({"collection": c["name"], "points": -1, "dim": "?", "distance": "?", "error": str(r)})
            continue
        pts = r.get("points_count", -1)
        vec = r.get("config", {}).get("params", {}).get("vectors", {})
        dim = vec.get("size", "?") if isinstance(vec, dict) else "?"
        dist = vec.get("distance", "?") if isinstance(vec, dict) else "?"
        total += max(pts, 0)
        populated += 1 if pts > 0 else 0
        empty += 1 if pts == 0 else 0
        rows.append({"collection": c["name"], "points": pts, "dim": dim, "distance": dist})
    return {
        "layer": "SEMANTIC",
        "engine": "qdrant :6333",
        "collections": rows,
        "summary": {"total_points": total, "populated": populated, "empty": empty, "collections_total": len(rows)},
        "method": "GET localhost:6333/collections/{name}",
    }

def probe_falkordb():
    """Witness: which graphs hold nodes, which are ghosts (0 nodes)."""
    p = subprocess.run(["redis-cli", "-p", "6380", "GRAPH.LIST"], capture_output=True, text=True, timeout=10)
    graphs = [line for line in p.stdout.splitlines() if line.strip() and not line.startswith("-")]
    rows = []
    for g in graphs:
        q = subprocess.run(["redis-cli", "-p", "6380", "GRAPH.QUERY", g, "MATCH (n) RETURN count(n)"],
                           capture_output=True, text=True, timeout=10)
        # result: header line, then count value line
        val = 0
        lines = [l.strip() for l in q.stdout.splitlines() if l.strip()]
        # find the integer count (second data line)
        for l in lines[1:]:
            if l.isdigit():
                val = int(l); break
        rows.append({"graph": g, "nodes": val, "status": "LIVE" if val > 0 else "GHOST"})
    return {
        "layer": "RELATIONSHIP",
        "engine": "falkordb :6380",
        "graphs": rows,
        "summary": {"graphs_total": len(rows), "live": sum(1 for r in rows if r["nodes"] > 0), "ghost": sum(1 for r in rows if r["nodes"] == 0)},
        "method": "redis-cli -p 6380 GRAPH.QUERY <g> 'MATCH (n) RETURN count(n)'",
    }

def probe_scheduler():
    """Witness: all scheduling mechanisms, one manifest. Anti-fragmentation."""
    mech = {}
    p = subprocess.run(["bash", "-lc", "crontab -l 2>/dev/null | grep -v '^\\s*#' | grep -v '^\\s*$'"], capture_output=True, text=True, timeout=10)
    mech["root_crontab"] = len([l for l in p.stdout.splitlines() if l.strip()])
    import glob
    cron_d = []
    for f in glob.glob("/etc/cron.d/*"):
        try:
            with open(f) as fh:
                cron_d += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
        except: pass
    mech["cron_d_lines"] = len(cron_d)
    t = subprocess.run(["systemctl", "list-timers", "--all", "--no-pager"], capture_output=True, text=True, timeout=10)
    mech["systemd_timers"] = len([l for l in t.stdout.splitlines() if l.strip() and not l.startswith("NEXT") and "timer" in l])
    return {
        "layer": "EXECUTION",
        "engine": "crontab + /etc/cron.d + systemd timers",
        "mechanisms": mech,
        "summary": {"scheduled_entries": sum(mech.values())},
        "method": "crontab -l; ls /etc/cron.d/*; systemctl list-timers",
    }

def run_all(which):
    probes = {"qdrant": probe_qdrant, "falkordb": probe_falkordb, "scheduler": probe_scheduler}
    if which == "all":
        selected = list(probes.keys())
    else:
        selected = [which]
    out = {"probe_id": f"probe-{TS}", "generated_utc": TS, "witness": []}
    for name in selected:
        out["witness"].append(probes[name]())
    path = f"{OUT_DIR}/probe_{TS}.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    return out, path

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    out, path = run_all(which)
    # human-readable console
    for w in out["witness"]:
        print(f"\n=== {w['layer']} — {w['engine']} ===")
        if "summary" in w:
            print("  SUMMARY:", json.dumps(w["summary"]))
        rows = w.get("collections") or w.get("graphs") or []
        for r in rows[:15]:
            print(f"  {r}")
    print(f"\nSNAPSHOT WRITTEN: {path}")