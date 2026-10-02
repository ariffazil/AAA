#!/usr/bin/env python3
"""route_capability.py — AAA capability compiler router.

JOB → FAMILY MANIFEST → canonical owner → adapter/tool → receipt

Usage:
  route_capability.py "<job text>"            # resolve best family+job
  route_capability.py "<text>" --prove        # also append receipt to PROOFS.jsonl
  route_capability.py --list                  # list families + jobs
Exit codes: 0 resolved · 1 unresolved (candidates listed, never guessed)
"""
from __future__ import annotations
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FAMILIES = ROOT / "families"
ALIASES = ROOT / "references" / "ALIASES.yaml"
PROOFS = ROOT / "references" / "PROOFS.jsonl"


def load_families() -> list[dict]:
    fams = []
    for f in sorted(FAMILIES.glob("*.yaml")):
        fams.append(yaml.safe_load(f.read_text()) | {"_file": f.name})
    return fams


def load_aliases() -> dict:
    if ALIASES.exists():
        return yaml.safe_load(ALIASES.read_text()) or {}
    return {}


def resolve(query: str, fams: list[dict]) -> tuple[dict | None, list[dict]]:
    q = query.lower()
    scored: list[tuple[int, dict, dict]] = []
    for fam in fams:
        for job_name, job in (fam.get("jobs") or {}).items():
            triggers = [str(t).lower() for t in (job.get("triggers") or [])]
            score = sum(1 for t in triggers if t in q)
            if job_name.lower().replace("_", " ") in q:
                score += 3
            if score:
                scored.append((score, fam, {"job": job_name, **job}))
    if not scored:
        return None, []
    scored.sort(key=lambda x: -x[0])
    top = scored[0]
    ties = [s for s in scored if s[0] == top[0]]
    return (top[1], top[2]), ties


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="*", help="job text")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--prove", action="store_true")
    args = ap.parse_args()

    fams = load_families()
    aliases = load_aliases()

    if args.list:
        for fam in fams:
            print(f"family: {fam['family']}  door: {fam.get('canonical_owner')}  state: {fam.get('status')}")
            for job_name, job in (fam.get("jobs") or {}).items():
                print(f"  - {job_name}: {job.get('executor')}  [{job.get('maturity', '?')}]")
        return 0

    query = " ".join(args.query).strip()
    if not query:
        ap.error("give a job description or --list")

    # alias short-circuit: query names a known alias
    alias_hit = next((a for a, v in aliases.items() if a.lower() in query.lower()), None)
    hit, ties = resolve(query, fams)
    now = datetime.now(timezone.utc).isoformat()

    if hit is None and not alias_hit:
        # fabric fallback: consult the compiler-level universal table
        jt = Path("/root/AAA/compilers/router/job-types.yaml")
        if jt.exists():
            import yaml as _y
            jobs = (_y.safe_load(jt.read_text()) or {}).get("jobs") or {}
            q = query.lower()
            scored = []
            for jname, j in jobs.items():
                score = sum(1 for w in jname.split("_") if len(w) > 4 and w in q)
                for t in (j.get("triggers") or []):
                    score += 2 if str(t).lower() in q else 0
                if score:
                    scored.append((score, jname, j))
            if scored:
                scored.sort(key=lambda x: -x[0])
                _, jname, j = scored[0]
                print(f"FABRIC ROUTE: {jname} -> compiler '{j.get('compiler')}'  [{j.get('status')}]")
                print(f"output: {j.get('output')}   producers: {j.get('producers')}")
                if j.get("door"):
                    print(f"door:   {j['door']}")
                if j.get("note"):
                    print(f"note:   {j['note']}")
                receipt = {"ts": now, "query": query, "fabric_job": jname,
                           "compiler": j.get("compiler"), "status": j.get("status")}
                if args.prove:
                    PROOFS.parent.mkdir(parents=True, exist_ok=True)
                    with PROOFS.open("a") as f:
                        f.write(json.dumps(receipt, ensure_ascii=False) + "\n")
                return 0
        print(f"UNRESOLVED: no family job matches '{query}'.")
        print("Nearest families:", ", ".join(f["family"] for f in fams))
        print("Add the job to its family manifest — do NOT create a new skill name.")
        return 1

    if hit is None and alias_hit:
        v = aliases[alias_hit]
        print(f"ALIAS RESOLVED: {alias_hit} → {v.get('canonical')}  [{v.get('action')}]")
        print(f"door: {v.get('canonical')}")
        receipt = {"ts": now, "query": query, "alias": alias_hit,
                   "resolved_to": v.get("canonical"), "via": "aliases"}
    else:
        fam, job = hit
        door = fam.get("canonical_owner")
        note = ""
        if alias_hit and aliases[alias_hit].get("canonical") and alias_hit.lower() in query.lower():
            note = f" (alias {alias_hit} → {aliases[alias_hit]['canonical']})"
        print(f"FAMILY:   {fam['family']}{note}")
        print(f"JOB:      {job['job']}")
        print(f"DOOR:     {door}   [{fam.get('status')}]")
        print(f"EXECUTOR: {job.get('executor')}")
        print(f"MATURITY: {job.get('maturity', '?')}   AUTHORITY: {job.get('authority', 'per-door')}")
        if job.get("verify"):
            print(f"VERIFY:   {job.get('verify')}")
        if len(ties) > 1:
            print(f"NOTE: {len(ties)} jobs tie on triggers — refine wording. Ties: " +
                  ", ".join(t[2]["job"] + "@" + t[1]["family"] for t in ties[:5]))
        receipt = {"ts": now, "query": query, "family": fam["family"], "job": job["job"],
                   "door": door, "executor": job.get("executor"),
                   "maturity": job.get("maturity"), "alias_resolved": alias_hit}

    if args.prove:
        PROOFS.parent.mkdir(parents=True, exist_ok=True)
        with PROOFS.open("a") as f:
            f.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        print(f"receipt → {PROOFS.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
