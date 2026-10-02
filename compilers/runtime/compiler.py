#!/usr/bin/env python3
"""runtime-compiler — DeclaredRuntime → ObservedRuntime → Difference → Consequence.

Compiles a live subject into a RuntimePacket (runtime-packet.schema.json).
Every field is MEASURED or explicitly UNKNOWN. Drift is classified only from
comparable identity pairs vs baselines.json. Never guesses.

Usage:
  compiler.py --subject arifos                 # human summary + JSON
  compiler.py --subject aforge --json out.json
  compiler.py --subject aforge --update-baseline   # stamp today's packet as drift baseline
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA_KEYS = ["subject", "observed_at", "source_identity", "build_identity", "deployed_identity",
               "process_identity", "import_origin", "service_state", "callable_surface", "behavior",
               "drift", "measurement_identity", "unknowns"]


def run(cmd, timeout=15):
    """Run a measurement command. Returns (ok, output). Every call is logged as provenance."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, (r.stdout or r.stderr).strip()
    except Exception as e:
        return False, f"EXC:{e}"


def sh(s):
    return s.split() if isinstance(s, str) else s


def compile_subject(name: str, cfg: dict) -> dict:
    unknowns, prov = [], []
    pkt = {k: None for k in SCHEMA_KEYS if k not in ("drift", "measurement_identity", "unknowns")}
    pkt.update({"drift": {"classification": "UNMEASURED", "pairs_compared": [], "details": []},
                "measurement_identity": prov, "unknowns": unknowns, "subject": name,
                "observed_at": datetime.now(timezone.utc).isoformat()})
    meas = lambda stage, cmd, ok, out: prov.append({"stage": stage, "cmd": cmd if isinstance(cmd, str) else " ".join(cmd), "ok": ok, "out": out[:200]})

    # IDENTITY — git HEAD for each candidate repo
    heads = {}
    for repo in cfg.get("repos") or []:
        ok, out = run(["git", "-C", repo, "log", "-1", "--format=%h %ci"])
        meas("identity", f"git -C {repo} log -1", ok, out)
        if ok:
            heads[repo] = out.split()[0]
        else:
            unknowns.append(f"source_identity: {repo} not a git repo")
    pkt["source_identity"] = ";".join(f"{k.split('/')[-1]}={v}" for k, v in heads.items()) or None
    if not cfg.get("repos"):
        unknowns.append("source_identity: no repos configured for subject")

    # BUILD/DEPLOY identity — marker files if the subject ships them, else UNKNOWN
    rel = Path("/opt/arifos/canon-release.json")
    if name == "arifos":
        ok, out = run(["cat", str(rel)])
        meas("deploy", f"cat {rel}", ok, out)
        if ok and out.strip():
            try:
                j = json.loads(out)
                pkt["build_identity"] = str(j.get("built_commit") or j.get("build") or "")[:64] or None
                pkt["deployed_identity"] = str(j.get("deployed_commit") or j.get("deploy") or "")[:64] or None
            except Exception:
                unknowns.append("deployed_identity: release marker unparseable")
        else:
            unknowns.append("deployed_identity: no release marker file content")
    else:
        unknowns.append(f"build/deploy_identity: no marker convention defined for {name}")

    # PROCESS — systemd
    svc = None
    ok, out = run(sh("systemctl list-units --type=service --no-legend --plain"))
    meas("process", "systemctl list-units", ok, out)
    if ok:
        import re
        pat = cfg["service_regex"].strip("^$")
        m = re.search(rf"({pat}.*?)\s+loaded\s+(\S+)", out)
        if m:
            svc = m.group(1).strip()
            ok2, out2 = run(["systemctl", "show", svc, "-p", "MainPID,ActiveState"])
            meas("process", f"systemctl show {svc}", ok2, out2)
            pkt["process_identity"] = f"{svc} pid=" + (out2.split("MainPID=")[1].split("\n")[0] if "MainPID=" in out2 else "?")
            pkt["service_state"] = (out2.split("ActiveState=")[1].split("\n")[0] if "ActiveState=" in out2 else None)
        else:
            unknowns.append(f"process_identity: no unit matches /{cfg['service_regex']}/")

    # IMPORT origin
    if cfg.get("import_probe"):
        ok, out = run(cfg["import_probe"])
        meas("import", " ".join(cfg["import_probe"]), ok, out)
        pkt["import_origin"] = out if ok else None
        if not ok:
            unknowns.append("import_origin: probe failed")
    else:
        unknowns.append("import_origin: no import probe configured")

    # SURFACE — health endpoint
    if cfg.get("port"):
        ok, out = run(["curl", "-s", "-m", "5", "-o", "/dev/null", "-w", "%{http_code}", f"http://127.0.0.1:{cfg['port']}/health"])
        meas("surface", f"curl :{cfg['port']}/health", ok, out)
        pkt["callable_surface"] = f"http://127.0.0.1:{cfg['port']}/health -> {out if ok else 'no-resp'}"
    else:
        unknowns.append("callable_surface: no port configured")

    pkt["behavior"] = None
    unknowns.append("behavior: not probed tonight (stage reserved)")

    # DRIFT — compare vs baselines.json (only pairs where both sides measured)
    bl_path = HERE / "baselines.json"
    baselines = {}
    if bl_path.exists():
        try:
            baselines = json.loads(bl_path.read_text()).get(name, {})
        except Exception:
            unknowns.append("drift: baselines.json unparseable")
    comparisons = []
    for key, live in [("source", pkt["source_identity"]), ("import", pkt["import_origin"]),
                      ("surface", pkt["callable_surface"]), ("process", pkt["process_identity"])]:
        base = baselines.get(key)
        if base and live:
            same = base == live
            comparisons.append({"pair": key, "baseline": base[:60], "live": live[:60], "same": same})
            if not same:
                pkt["drift"]["details"].append(f"{key} moved since baseline: {str(base)[:40]} -> {str(live)[:40]}")
    pkt["drift"]["pairs_compared"] = comparisons
    if not comparisons:
        pkt["drift"]["classification"] = "UNMEASURED"
        unknowns.append("drift: no baseline to compare — run --update-baseline to stamp today")
    elif any("moved" in d for d in pkt["drift"]["details"]):
        pkt["drift"]["classification"] = "DRIFT"
    else:
        pkt["drift"]["classification"] = "CONVERGED"

    # schema conformance (required keys present, no extra)
    missing = [k for k in SCHEMA_KEYS if k not in pkt]
    extra = [k for k in pkt if k not in SCHEMA_KEYS]
    if missing or extra:
        pkt["drift"]["details"].append(f"SCHEMA VIOLATION missing={missing} extra={extra}")
    return pkt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--json", help="write packet JSON here")
    ap.add_argument("--update-baseline", action="store_true")
    a = ap.parse_args()

    import yaml
    subjects = yaml.safe_load((HERE / "subjects.yaml").read_text())
    if a.subject not in subjects:
        print(f"UNKNOWN subject '{a.subject}'. Known: {', '.join(subjects)}")
        return 2
    pkt = compile_subject(a.subject, subjects[a.subject])

    if a.update_baseline:
        bl = json.loads((HERE / "baselines.json").read_text() or "{}")
        bl[a.subject] = {"source": pkt["source_identity"], "import": pkt["import_origin"],
                         "surface": pkt["callable_surface"], "process": pkt["process_identity"],
                         "stamped_at": pkt["observed_at"]}
        (HERE / "baselines.json").write_text(json.dumps(bl, indent=2))
        print(f"baseline stamped for {a.subject} @ {pkt['observed_at']}")

    out = json.dumps(pkt, indent=2)
    if a.json:
        Path(a.json).write_text(out)
    print(f"=== RuntimePacket: {a.subject} ===")
    print(f"service:    {pkt['service_state']}  process: {pkt['process_identity']}")
    print(f"source:     {pkt['source_identity']}")
    print(f"import:     {pkt['import_origin']}")
    print(f"surface:    {pkt['callable_surface']}")
    print(f"DRIFT:      {pkt['drift']['classification']}  ({len(pkt['drift']['pairs_compared'])} pairs compared)")
    for d in pkt["drift"]["details"]:
        print(f"  ! {d}")
    print(f"unknowns:   {len(pkt['unknowns'])} (honest) -> " + "; ".join(pkt["unknowns"][:4]))
    if a.json:
        print(f"packet → {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
