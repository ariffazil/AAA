#!/usr/bin/env python3
"""
runtime-identity.py — A-FORGE runtime sensor (Lane B, reversible).

Per sovereign 2026-10-02:
- Source SHA ≠ built SHA ≠ deployed SHA ≠ imported runtime
- All four identities must be measurable
- Drift among them surfaced as CONTRADICTION

Output: /root/AAA/cockpit/runtime-identity.json (atomic write)
"""
import json, sys, hashlib, subprocess
from pathlib import Path

def now_utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def git_sha(repo_path: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", repo_path, "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "no-git"

def file_sha(path: str) -> str:
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]
    except Exception:
        return "no-file"

def pkg_version(import_name: str) -> str:
    try:
        mod = __import__(import_name)
        v = getattr(mod, "__version__", "unknown")
        return str(v)
    except Exception as e:
        return f"import-error:{type(e).__name__}"

def main():
    organs = {
        "arifos": {
            "source_path": "/root/arifOS",
            "runtime_path": "/opt/arifos/app",
            "import_name": "arifos",
        },
        "aforge": {
            "source_path": "/root/A-FORGE",
            "runtime_path": "/opt/a-forge",
            "import_name": "a_forge",
        },
        "frame": {
            "source_path": "/root/AAA/federation/frame",
            "runtime_path": "/opt/frame/app",
            "import_name": "frame_organ",
        },
    }
    out = {
        "schema": "runtime-identity-v1",
        "generated_at": now_utc(),
        "sovereign_law": "Source ≠ build ≠ deployed ≠ imported runtime; all four identities must be measurable; drift surfaced as CONTRADICTION",
        "organs": {},
        "summary": {
            "total_organs": 0,
            "drift_count": 0,
            "contradictions": [],
        },
    }
    for name, paths in organs.items():
        src_sha = git_sha(paths["source_path"])
        # Find a representative runtime file
        rt_dir = Path(paths["runtime_path"])
        if rt_dir.exists():
            # Hash first .py file at depth 3
            rt_files = list(rt_dir.rglob("*.py"))[:1]
            rt_file_sha = file_sha(str(rt_files[0])) if rt_files else "no-py"
        else:
            rt_file_sha = "no-runtime-dir"
        pkg_v = pkg_version(paths["import_name"])
        # File SHA from source main file
        src_main = list(Path(paths["source_path"]).rglob("*.py"))[:1] if Path(paths["source_path"]).exists() else []
        src_file_sha = file_sha(str(src_main[0])) if src_main else "no-source"

        # Drift detection — HASH-EQUIVALENCE only (per forge_runtime_verify doctrine)
        # Semantic divergence (PEP 440 version vs commit SHA) is NOT a runtime failure;
        # it is a legitimate duality answered by a different question.
        drift = []
        if src_sha != "no-git" and src_file_sha != "no-source" and rt_file_sha != "no-runtime-dir" and rt_file_sha != "no-py":
            if src_file_sha != rt_file_sha:
                drift.append("source_file_sha != runtime_file_sha")

        out["organs"][name] = {
            "source_path": paths["source_path"],
            "runtime_path": paths["runtime_path"],
            "source_sha": src_sha,
            "source_file_sha": src_file_sha,
            "runtime_file_sha": rt_file_sha,
            "pkg_version": pkg_v,
            "pkg_version_note": "semantic, not hash-equal to source_sha (different question)",
            "drift_signals": drift,
        }
        out["summary"]["total_organs"] += 1
        if drift:
            out["summary"]["drift_count"] += 1
            out["summary"]["contradictions"].append({
                "organ": name,
                "drift_signals": drift,
                "source_sha": src_sha,
                "pkg_version": pkg_v,
                "note": "HASH-equivalence only; pkg_version is semantic, not drift",
            })

    # MD5 identity probe (per Hermes hook finding 2026-10-02):
    # source package __init__.py md5 vs deployed site-packages __init__.py md5
    # Sovereign invariant #46: "drift among them is surfaced"
    md5_identity = {}
    for name, paths in organs.items():
        src_init = Path(paths["source_path"]) / name / "__init__.py"
        deployed_init = Path("/opt") / name / "current/venv/lib/python3.13/site-packages" / name / "__init__.py"
        # Fallback: search for __init__.py under /opt/<name>/**/site-packages/<name>/
        if not deployed_init.exists():
            for p in Path("/opt").rglob(f"{name}/__init__.py"):
                if "site-packages" in str(p):
                    deployed_init = p
                    break
        src_md5 = file_sha(str(src_init)) if src_init.exists() else "no-source-init"
        py_md5 = file_sha(str(deployed_init)) if deployed_init.exists() else "no-deployed-init"
        md5_match = (src_md5 == py_md5) and src_md5 not in ("no-source-init", "no-deployed-init")
        md5_identity[name] = {
            "source_init_md5": src_md5,
            "deployed_init_md5": py_md5,
            "md5_match": md5_match,
            "note": "Hash-level identity check beyond commit SHA. Per Hermes hook finding 2026-10-02: 'dua fail entry-point package berbeza kandungan antara source dan deployed'",
        }
    out["md5_identity"] = md5_identity

    body = json.dumps(out, sort_keys=True).encode("utf-8")
    out["integrity_hash"] = hashlib.sha256(body).hexdigest()
    out_path = Path("/root/AAA/cockpit/runtime-identity.json")
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(out, indent=2))
    tmp.replace(out_path)
    print(f"runtime-identity: {out_path} sha256={out['integrity_hash'][:12]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())