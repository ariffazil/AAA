#!/usr/bin/env python3
"""
registry_score.py — Supply-chain risk scorer for MCP registry entries.

Computes 0-100 risk score (lower = better) for a given MCP server name.
Hits https://registry.modelcontextprotocol.io/v0.1/servers/{name}/versions
and applies heuristics calibrated 2026-09-25.

API structure:
    GET /v0.1/servers/{name}/versions -> {"servers": [{server: {...}, _meta: {...}}, ...]}
    GET /v0.1/servers?search=<query>&limit=N -> {"servers": [...], "metadata": {...}}

Usage:
    python3 registry_score.py <server-name>
    python3 registry_score.py <server-name> --json
    python3 registry_score.py --batch < names.txt

Output: tab-separated or JSON to stdout. HTTP probes for remote reachability
are opt-in (--probe) since they add latency.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone


REGISTRY_BASE = "https://registry.modelcontextprotocol.io/v0.1"


def fetch_versions(name):
    """Fetch all versions for one server. Returns list of {server: {...}, _meta: {...}}."""
    encoded = urllib.parse.quote(name, safe='')
    url = f"{REGISTRY_BASE}/servers/{encoded}/versions"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                return []
            data = json.loads(resp.read().decode())
            return data.get("servers", [])
    except Exception as e:
        print(f"[ERR] fetch failed for {name}: {e}", file=sys.stderr)
        return []


def probe_remote(url):
    """HEAD probe of a remote MCP endpoint. Opt-in."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return 200 <= resp.status < 500
    except Exception:
        return False


def compute_score(name, versions, remote_reachable=None):
    """Apply heuristics. Returns dict with score, breakdown, risk_band."""
    score = 0
    breakdown = []

    if not versions:
        return {
            "name": name,
            "score": None,
            "risk_band": "UNKNOWN",
            "error": "not found in registry",
            "breakdown": [],
            "remote_reachable": remote_reachable,
            "version_count": 0,
        }

    # Latest version is the first entry (API returns ordered)
    latest_wrapper = versions[0]
    latest = latest_wrapper.get("server", {})
    latest_meta = latest_wrapper.get("_meta", {}).get(
        "io.modelcontextprotocol.registry/official", {}
    )
    version_count = len(versions)

    # Namespace depth signal
    if name.startswith("com."):
        score -= 15
        breakdown.append(("domain-anchored namespace (com.*)", -15))
    elif name.startswith("ac."):
        score -= 10
        breakdown.append(("academic namespace (ac.*)", -10))
    elif name.startswith("io.github."):
        score += 0
        breakdown.append(("github-anchored namespace (io.github.*)", 0))
    elif name.startswith("ai."):
        score += 10
        breakdown.append(("bulk-generic ai.* namespace", +10))

    # Version count signal — single-server spam pattern (925+ versions = abuse)
    if version_count == 1:
        score -= 5
        breakdown.append(("single-version server", -5))
    elif 2 <= version_count <= 20:
        score += 0
        breakdown.append((f"normal version history ({version_count} versions)", 0))
    elif 21 <= version_count <= 100:
        score += 5
        breakdown.append((f"high version count ({version_count}) - review churn", +5))
    elif 101 <= version_count <= 500:
        score += 15
        breakdown.append((f"very high version count ({version_count}) - spam signal", +15))
    else:  # >500
        score += 25
        breakdown.append((f"extreme version count ({version_count}) - likely spam/abuse", +25))

    # Version freshness
    published_at = latest_meta.get("publishedAt") or latest.get("publishedAt")
    if published_at:
        try:
            pub_dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - pub_dt).days
            if age_days > 180:
                score += 10
                breakdown.append((f"latest version is {age_days}d old (>180d)", +10))
            elif age_days > 90:
                score += 5
                breakdown.append((f"latest version is {age_days}d old (>90d)", +5))
            else:
                breakdown.append((f"latest version is {age_days}d old (fresh)", 0))
        except Exception:
            pass

    # Status signals
    status = latest_meta.get("status", "active")
    if status == "deleted":
        score += 30
        breakdown.append(("latest version status=deleted", +30))
    elif status == "deprecated":
        score += 10
        breakdown.append(("latest version status=deprecated", +10))

    # Remote reachability
    if remote_reachable is False:
        score += 25
        breakdown.append(("remote endpoint unreachable (listed but broken)", +25))
    elif remote_reachable is True:
        breakdown.append(("remote endpoint reachable", 0))

    # Schema era
    schema_url = latest.get("$schema", "") or ""
    if "2025-12-11" in schema_url:
        breakdown.append(("schema current (2025-12-11)", 0))
    elif schema_url:
        score += 5
        breakdown.append((f"schema older than 2025-12-11: {schema_url}", +5))

    # Clamp to 0-100
    score = max(0, min(100, score))

    # Risk band
    if score <= 20:
        band = "LOW"
    elif score <= 40:
        band = "MEDIUM"
    elif score <= 60:
        band = "HIGH"
    else:
        band = "AVOID"

    return {
        "name": name,
        "score": score,
        "risk_band": band,
        "breakdown": breakdown,
        "remote_reachable": remote_reachable,
        "latest_version": latest.get("version"),
        "latest_status": status,
        "version_count": version_count,
        "is_latest": latest_meta.get("isLatest"),
    }


def score_one(name, probe=False):
    versions = fetch_versions(name)

    # Optional remote probe - only for the latest version's remotes
    remote_reachable = None
    if probe and versions:
        latest = versions[0].get("server", {})
        remotes = latest.get("remotes", []) or []
        if remotes:
            remote_url = remotes[0].get("url", "")
            if remote_url:
                remote_reachable = probe_remote(remote_url)

    return compute_score(name, versions, remote_reachable)


def main():
    ap = argparse.ArgumentParser(description="Score MCP registry entries for supply-chain risk.")
    ap.add_argument("name", nargs="?", help="Server name (e.g. ai.example/foo)")
    ap.add_argument("--json", action="store_true", help="Emit JSON output")
    ap.add_argument("--probe", action="store_true", help="HEAD-probe remote endpoint (adds latency)")
    ap.add_argument("--batch", action="store_true", help="Read names from stdin")
    args = ap.parse_args()

    names = []
    if args.batch:
        names = [line.strip() for line in sys.stdin if line.strip()]
    elif args.name:
        names = [args.name]
    else:
        ap.print_help()
        sys.exit(2)

    results = [score_one(n, probe=args.probe) for n in names]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            if r.get("error"):
                print(f"{r['name']}\t{r['error']}\t{r['risk_band']}")
            else:
                print(f"{r['name']}\tscore={r['score']}\tband={r['risk_band']}\t"
                      f"latest={r['latest_version']}\tversions={r['version_count']}\t"
                      f"status={r['latest_status']}")
                for label, pts in r["breakdown"]:
                    print(f"    {pts:+3d}  {label}")


if __name__ == "__main__":
    main()
