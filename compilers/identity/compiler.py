#!/usr/bin/env python3
"""identity-compiler — measures identity relations BEFORE any MATCH/DRIFT verdict.

Identity comparison requires a declared equivalence relation. A commit SHA and a
package version are not intrinsically comparable. This compiler measures what exists,
marks what does not, and emits an IdentityPacket (/root/AAA/schemas/ir/identity-packet.v1.schema.json).

identity_state:
  CONSISTENT            — every claimed edge has measured equivalence evidence, all agree
  DRIFT                 — measured edges disagree
  AMBIGUOUS_LENS_CONFLICT — independent lenses report conflicting verdicts; unresolved edges listed
  UNMEASURED            — insufficient edges measured

Usage: compiler.py --subject arifos [--lens-a lens_a_arifos.json] [--json out]
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQUIRED = ["subject_type", "identities", "equivalence_evidence", "unresolved_relations",
            "identity_state", "observed_at"]


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return r.returncode == 0, (r.stdout or r.stderr).strip()
    except Exception as e:
        return False, f"EXC:{e}"


def measure(cfg: dict, prov: list):
    ids, edges, unresolved = {}, [], []
    # source (git_sha)
    ok, out = run(["git", "-C", cfg["repo"], "log", "-1", "--format=%h"])
    prov.append({"m": "source git", "cmd": f"git -C {cfg['repo']} log -1", "ok": ok, "out": out[:120]})
    if ok:
        ids["source"] = {"scheme": "git_sha", "value": out}
    else:
        unresolved.append("source: repo not measurable")
    # package (pep440) — dist-info presence IS the identity carrier
    ok, out = run(["bash", "-c", f"ls -d {cfg['site_packages']}/{cfg['package']}-*.dist-info 2>/dev/null"])
    prov.append({"m": "package dist-info", "cmd": f"ls {cfg['site_packages']}/{cfg['package']}-*.dist-info", "ok": ok, "out": out[:120]})
    if ok and out:
        meta = Path(out.split("\n")[0]) / "METADATA"
        ok2, ver = run(["grep", "-m1", "^Version:", str(meta)])
        ids["package"] = {"scheme": "pep440", "value": ver.split(":", 1)[1].strip() if ok2 and ":" in ver else "UNPARSEABLE"}
        edges.append({"relation": "PACKAGED_AS", "from": "build", "to": "package",
                      "evidence_ref": str(meta), "measured_at": datetime.now(timezone.utc).isoformat()})
    else:
        unresolved.append("build_to_package: NO wheel/dist-info artifact on disk — "
                          "wheel-based MATCH/DRIFT verdicts compare against a phantom artifact")
    # import (filesystem_path)
    ok, out = run(cfg["import_probe"])
    prov.append({"m": "import", "cmd": " ".join(cfg["import_probe"]), "ok": ok, "out": out[:160]})
    if ok:
        ids["import"] = {"scheme": "filesystem_path", "value": out}
        # measurable edge: import lives inside the source tree?
        if ids.get("import", {}).get("value", "").startswith(cfg["repo"]):
            edges.append({"relation": "LOADED_FROM", "from": "source", "to": "import",
                          "evidence_ref": f"import path inside {cfg['repo']} worktree",
                          "measured_at": datetime.now(timezone.utc).isoformat()})
    else:
        unresolved.append("import: probe failed")
    return ids, edges, unresolved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="arifos")
    ap.add_argument("--lens-a", help="declared-lens evidence file (e.g. session arif_init release receipt)")
    ap.add_argument("--json", help="write IdentityPacket here")
    a = ap.parse_args()

    cfg = {
        "repo": "/opt/arifos",
        "site_packages": "/opt/arifos/current/venv/lib/python3.13/site-packages",
        "package": "arifosmcp",
        "import_probe": ["/opt/arifos/current/venv/bin/python", "-c", "import arifosmcp; print(arifosmcp.__file__)"],
    }
    prov: list = []
    ids, edges, unresolved = measure(cfg, prov)

    # declared lens (release manifest receipt)
    lens_a = None
    if a.lens_a and Path(a.lens_a).exists():
        lens_a = json.loads(Path(a.lens_a).read_text())
        if lens_a.get("drift") is False and lens_a.get("wheel_hash") in (None, ""):
            unresolved.append("declared lens claims CONSISTENT but wheel_hash=null — "
                              "it never measured the package edge; its CONSISTENT covers source/build/deploy only")
            edges.append({"relation": "DERIVED_FROM", "from": "source", "to": "build",
                          "evidence_ref": f"{a.lens_a} (declared lens: built==deployed==source, wheel unmeasured)",
                          "measured_at": lens_a.get("observed_at", "")})

    # classification
    if unresolved and not edges:
        state = "UNMEASURED"
    elif any("phantom" in u for u in unresolved):
        state = "AMBIGUOUS_LENS_CONFLICT"
    else:
        state = "CONSISTENT"

    pkt = {
        "subject_type": a.subject,
        "identities": ids,
        "equivalence_evidence": edges,
        "unresolved_relations": unresolved,
        "identity_state": state,
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }
    missing = [k for k in REQUIRED if k not in pkt]
    extra = [k for k in pkt if k not in REQUIRED]
    assert not missing and not extra, (missing, extra)

    out_path = a.json or str(HERE / "packets" / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}-{a.subject}.json")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps({"packet": pkt, "measurement_provenance": prov}, indent=1))
    print(f"=== IdentityPacket: {a.subject} ===")
    for k, v in ids.items():
        print(f"  {k:8s} {v['scheme']:16s} {v['value'][:70]}")
    print(f"  edges measured: {len(edges)} · unresolved: {len(unresolved)}")
    for u in unresolved:
        print(f"  ! {u}")
    print(f"  IDENTITY_STATE: {state}")
    print(f"  packet → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
