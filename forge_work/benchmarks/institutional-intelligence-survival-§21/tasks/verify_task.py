#!/usr/bin/env python3
"""S21 independent verifier runner (spec: verifier-independence per scar-2026-10-01-002).
Records verifier_actor_id / verifier_model_lane / verifier_process_tree_hash. GUARDS:
refuses if verifier lane == executor lane (costume verification forbidden). Usage:
  verify_task.py --task-set task-set.json --task T1-1 --workspace ./ws \
      --verifier-actor codex/FI-005 --verifier-lane codex --executor-lane forge-777 [--selftest]"""
import argparse, hashlib, json, os, subprocess, sys, time, datetime

def tree_hash():
    try:
        out = subprocess.run(["ps", "-o", "pid,ppid,args", "-e"], capture_output=True, text=True).stdout
        return hashlib.sha256(out.encode()).hexdigest()[:16]
    except Exception:
        return "unmeasured"

def materialize(task, ws):
    os.makedirs(ws, exist_ok=True)
    for rel, content in task.get("workspace", {}).items():
        p = os.path.join(ws, rel)
        os.makedirs(os.path.dirname(p) or ws, exist_ok=True)
        open(p, "w").write(content)

def verify(args):
    ts = json.load(open(args.task_set))
    task = next((t for t in ts["tasks"] if t["id"] == args.task), None)
    if not task:
        print(json.dumps({"verdict": "UNKNOWN_TASK"})); return 2
    if args.verifier_lane == args.executor_lane:
        print(json.dumps({"verdict": "REFUSED", "reason": "scar-002: verifier lane == executor lane"})); return 2
    ws = args.workspace
    if os.path.isdir(ws) and os.listdir(ws):
        mat = "skipped (existing workspace preserved)"
    else:
        materialize(task, ws)
        mat = "materialized"
    results = []
    for acc in task.get("acceptance", []):
        t0 = time.time()
        r = subprocess.run(acc["cmd"], shell=True, cwd=ws, capture_output=True, text=True, timeout=600)
        results.append({"cmd": acc["cmd"], "expect": acc["expect"],
                        "exit": r.returncode, "ok": r.returncode == 0,
                        "wall_s": round(time.time() - t0, 2)})
    out = {"task_id": task["id"], "verdict": "PASS" if all(r["ok"] for r in results) else "FAIL",
           "acceptance": results,
           "verifier": {"actor_id": args.verifier_actor, "model_lane": args.verifier_lane,
                        "process_tree_hash": tree_hash(),
                        "executor_lane": args.executor_lane, "independence": "lane!=executor", "materialize": mat},
           "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    print(json.dumps(out, indent=1))
    return 0 if out["verdict"] == "PASS" else 1

def selftest():
    tmp = "/tmp/s21-verify-selftest"
    ts = {"tasks": [{"id": "SELF-1", "class": "T1", "workspace": {"check.py": "print('ok')"},
                     "acceptance": [{"cmd": "python3 check.py", "expect": "exit 0"}]}]}
    open(f"{tmp}-ts.json", "w").write(json.dumps(ts))
    a = argparse.Namespace(task_set=f"{tmp}-ts.json", task="SELF-1", workspace=tmp,
                           verifier_actor="selftest", verifier_lane="codex",
                           executor_lane="forge-777")
    rc = verify(a)
    a2 = argparse.Namespace(task_set=f"{tmp}-ts.json", task="SELF-1", workspace=tmp,
                            verifier_actor="selftest", verifier_lane="forge-777",
                            executor_lane="forge-777")
    rc2 = verify(a2)
    print("selftest: accept=", rc == 0, " refuse_costume=", rc2 == 2)
    return 0 if (rc == 0 and rc2 == 2) else 1

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--task-set"); ap.add_argument("--task"); ap.add_argument("--workspace", default="./ws")
    ap.add_argument("--verifier-actor", default="unassigned"); ap.add_argument("--verifier-lane", default="unassigned")
    ap.add_argument("--executor-lane", default="unassigned"); ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    sys.exit(selftest() if args.selftest else verify(args))
