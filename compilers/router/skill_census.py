#!/usr/bin/env python3
"""skill_census.py — measured census of the AAA skill estate for hardening/distraction mapping.

Re-run any time: python3 skill_census.py [--out PATH]
Measures; never guesses. Every number in the output traces to a walk of the live tree.
"""
from __future__ import annotations
import argparse, hashlib, json, re, yaml
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

AAA = Path("/root/AAA/skills")
HERMES = Path("/root/.hermes/skills")
NOW = datetime.now(timezone.utc)

CLUSTERS = {  # family -> name regexes (from F13 P0/P1 lists + tonight's consolidation)
 "evidence":        r"claim|finding|falsif|audit|verif|recurrence|intake|review|conformance|probe-audit",
 "session":         r"session|kernel-bind|auto-init|frozen-snapshot|carry",
 "federation-rt":   r"route-dispatch|ingress|a2a|agent-card|agent-to-agent|signal-routing|lane-switch|orchestrat",
 "research-web":    r"research|web-|search|scrape|firecrawl|deep-research|youtube-eureka",
 "telegram":        r"telegram",
 "voice":           r"voice|tts|asr|speech|mimo-audio",
 "image":           r"image|photo|lora|photoreal|minimax-image|imagegen",
 "video":           r"video",
 "model-compute":   r"litellm|tokenrouter|qwencloud|model-monitor|mmx|mulerouter|model-chain|fed-model",
 "mcp-ops":         r"mcp",
 "runtime-ops":     r"drift|deploy|service|incident|infra|machine|reachab|housekeep|observ|recovery|runtime-verify",
 "delivery":        r"deliver|outbound|email|brevo|phased-delivery",
 "document":        r"pdf|document|report-layout|docforge|slide|ocr",
}


def family(name: str) -> str | None:
    n = name.lower()
    for fam, pat in CLUSTERS.items():
        if re.search(pat, n):
            return fam
    return None


def census_dir(root: Path, seen: set):
    rows = []
    if not root.exists():
        return rows
    PRUNE = {".archive", ".git", "node_modules", "__pycache__", ".hermes-archived", "_archive", "archive"}
    for d in sorted(root.rglob("*")):
        if not d.is_dir() or d.name.startswith("."):
            continue
        if any(part in PRUNE for part in d.parts):
            continue
        real = d.resolve()
        if real in seen:
            continue
        seen.add(real)
        sk = d / "SKILL.md"
        if not sk.exists():
            continue
        try:
            body = sk.read_text(errors="replace")
        except Exception:
            body = ""
        h = hashlib.sha1(body.encode()).hexdigest()[:12]
        scripts = list((d / "scripts").glob("*")) if (d / "scripts").is_dir() else []
        try:
            mt = datetime.fromtimestamp(sk.stat().st_mtime, tz=timezone.utc)
            age_d = (NOW - mt).days
        except Exception:
            age_d = -1
        is_link = d.is_symlink()
        front_ok = body.startswith("---") and "description:" in body[:600]
        rows.append({
            "name": d.name, "path": str(d), "real": str(real), "symlink": is_link,
            "bytes": len(body), "hash": h, "age_days": age_d,
            "n_scripts": len(scripts), "has_exec": any(p.stat().st_mode & 0o111 for p in scripts if p.is_file()),
            "frontmatter_ok": front_ok, "family": family(d.name),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(AAA / "HARDENING_MAP.v1.yaml"))
    a = ap.parse_args()

    seen: set = set()
    rows = census_dir(AAA, seen) + census_dir(HERMES, seen)
    by_hash = defaultdict(list)
    by_name = defaultdict(list)
    for r in rows:
        by_hash[r["hash"]].append(r["path"])
        by_name[r["name"]].append(r["path"])

    twins = [{"hash": h, "members": m} for h, m in by_hash.items() if len(m) > 1 and h != hashlib.sha1(b"").hexdigest()[:12]]
    collisions = {n: m for n, m in by_name.items() if len(m) > 1}

    # live alias audit from the canonical alias table (re-measured, not trusted from prose)
    alias_stats = {"rows": 0, "live": 0, "dead": 0, "dead_targets": []}
    alias_file = AAA / "SKILL_ALIAS_TABLE.json"
    if alias_file.exists():
        try:
            at = json.loads(alias_file.read_text())
            rows_a = at.get("aliases") or []
            alias_stats["rows"] = len(rows_a)
            for row in rows_a:
                if not isinstance(row, dict):
                    continue
                if str(row.get("status", "")).lower() in ("tombstone", "retired"):
                    continue
                target = str(row.get("primary_resolved") or row.get("primary_path") or "")
                if target and Path(target).exists():
                    alias_stats["live"] += 1
                else:
                    alias_stats["dead"] += 1
                    if len(alias_stats["dead_targets"]) < 200:
                        alias_stats["dead_targets"].append({"alias": row.get("v3_name"), "target": target})
        except Exception as e:
            alias_stats["error"] = str(e)[:120]

    fams = defaultdict(list)
    for r in rows:
        if r["family"] and not r["symlink"]:
            fams[r["family"]].append(r["name"])

    stale = sorted([r for r in rows if not r["symlink"] and r["age_days"] >= 60], key=lambda r: -r["age_days"])
    doctrine_only = [r["name"] for r in rows if not r["symlink"] and r["n_scripts"] == 0]

    prov = [
        {"m": "walk", "cmd": f"iterdir {AAA} + {HERMES} (realpath-deduped)", "count": len(rows)},
        {"m": "alias audit", "cmd": f"json {alias_file} -> aliases[].primary_resolved liveness vs disk", "live": alias_stats["live"], "dead": alias_stats["dead"]},
    ]
    out = {
        "census": {
            "generated_at": NOW.isoformat(),
            "tool": "compilers/router/skill_census.py",
            "skillmd_dirs": len(rows),
            "real_dirs": sum(1 for r in rows if not r["symlink"]),
            "symlinked": sum(1 for r in rows if r["symlink"]),
            "with_scripts": sum(1 for r in rows if r["n_scripts"] > 0),
            "doctrine_only_no_scripts": len(doctrine_only),
            "provenance": prov,
        },
        "hardening": {
            "identical_twins": twins,
            "basename_collisions": {k: v for k, v in list(collisions.items())[:20]},
            "stale_60d_plus": {"count": len(stale), "oldest_first": [
                {"name": r["name"], "age_days": r["age_days"], "bytes": r["bytes"]} for r in stale[:40]]},
            "frontmatter_broken": [r["name"] for r in rows if not r["frontmatter_ok"]][:30],
        },
        "distraction": {
            "cluster_sizes": {k: len(v) for k, v in sorted(fams.items(), key=lambda x: -len(x[1]))},
            "clusters": {k: sorted(v) for k, v in fams.items()},
            "alias_liveness": alias_stats,
        },
        "action_queue": {
            "P0_identity_capability": "extend identity compiler from this census; reconcile dead alias targets",
            "P0_clusters_next": ["evidence", "session", "federation-rt", "research-web", "telegram", "runtime-ops"],
            "rule": "no cluster member may be selected while its family front door exists; per MIGRATION.md fates",
        },
    }
    Path(a.out).write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=100))
    print(f"map → {a.out}")
    print(f"skill dirs: {len(rows)} (real {out['census']['real_dirs']}, symlinked {out['census']['symlinked']})")
    print(f"identical twins: {len(twins)} groups · basename collisions: {len(collisions)}")
    print(f"stale ≥60d: {len(stale)} · doctrine-only: {len(doctrine_only)}")
    print(f"aliases: {alias_stats['rows']} rows → live {alias_stats['live']} · DEAD {alias_stats['dead']}")
    print("cluster sizes:", dict(sorted(((k, len(v)) for k, v in fams.items()), key=lambda x: -x[1])))


if __name__ == "__main__":
    main()
