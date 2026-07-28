#!/usr/bin/env python3
"""
mcp_ecosystem_ingest.py — External MCP server discovery & candidate catalog.
Polls public MCP directories, package registries, and GitHub for new servers.
Maintains an external candidate catalog for agent evaluation.

DITEMPA BUKAN DIBERI — Forged, Not Given.
Forged: 2026-07-28 by FORGE (000Ω) under F13 SOVEREIGN directive.
"""

import json
import hashlib
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Configuration ──────────────────────────────────────────────

CATALOG_DIR = Path("/root/AAA/registries/mcp_servers/external")
CATALOG_FILE = CATALOG_DIR / "candidates.json"
CATALOG_INDEX = CATALOG_DIR / "INDEX.json"
FORGE_WORK = Path("/root/A-FORGE/forge_work/2026-07-28/mcp-registry/external")

HEADERS = {"Accept": "application/json", "User-Agent": "arifos-mcp-ingest/1.0"}

# Known MCP directory sources
SOURCES = {
    "mcp_so": {
        "type": "directory",
        "url": "https://mcp.so",
        "api_hint": None,  # scrape-only, no public API
        "enabled": True,
    },
    "registry_mcp_io": {
        "type": "registry",
        "url": "https://registry.modelcontextprotocol.io",
        "api": "https://registry.modelcontextprotocol.io/api/servers",
        "enabled": True,
    },
    "pypi_mcp": {
        "type": "pypi",
        "url": "https://pypi.org/search/?q=mcp+server",
        "api": "https://pypi.org/simple/",
        "packages": ["mcp", "fastmcp", "modelcontextprotocol"],
        "enabled": True,
    },
    "npm_mcp": {
        "type": "npm",
        "url": "https://www.npmjs.com/search?q=mcp-server",
        "api": "https://registry.npmjs.org/-/v1/search",
        "enabled": True,
    },
    "github_topics": {
        "type": "github",
        "url": "https://github.com/topics/modelcontextprotocol",
        "api": "https://api.github.com/search/repositories",
        "topics": ["modelcontextprotocol", "mcp-server", "mcp-tool"],
        "enabled": True,
    },
}


# ── Ingestion Functions ────────────────────────────────────────


def fetch_json(url: str, timeout: int = 15) -> dict | None:
    """Fetch and parse JSON from a URL."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  ⚠️ {url}: {e}")
        return None


def ingest_registry_mcp_io() -> list[dict]:
    """Fetch official MCP registry server list."""
    print("🔍 Polling registry.modelcontextprotocol.io...")
    data = fetch_json(SOURCES["registry_mcp_io"]["api"])
    if not data:
        return []

    servers = data.get("servers", data.get("results", []))
    candidates = []
    for s in servers:
        candidates.append(
            {
                "source": "registry.modelcontextprotocol.io",
                "source_type": "official_registry",
                "name": s.get("name", "?"),
                "description": s.get("description", ""),
                "url": s.get("url", s.get("repository", "")),
                "author": s.get("author", s.get("owner", "")),
                "tags": s.get("tags", []),
                "transport": s.get("transport", "unknown"),
                "discovered_at": datetime.now(timezone.utc).isoformat(),
            }
        )
    print(f"  ✅ {len(candidates)} servers from official registry")
    return candidates


def ingest_npm() -> list[dict]:
    """Search npm registry for MCP server packages."""
    print("🔍 Searching npm registry...")
    candidates = []
    for query in ["mcp-server", "modelcontextprotocol", "@modelcontextprotocol"]:
        params = urllib.parse.urlencode({"text": query, "size": 50})
        data = fetch_json(f"{SOURCES['npm_mcp']['api']}?{params}")
        if not data:
            continue
        for obj in data.get("objects", []):
            pkg = obj.get("package", {})
            candidates.append(
                {
                    "source": "npm",
                    "source_type": "package_registry",
                    "name": pkg.get("name", "?"),
                    "description": pkg.get("description", ""),
                    "url": pkg.get("links", {}).get("npm", ""),
                    "repository": pkg.get("links", {}).get("repository", ""),
                    "author": pkg.get("publisher", {}).get("username", ""),
                    "tags": pkg.get("keywords", []),
                    "version": pkg.get("version", ""),
                    "discovered_at": datetime.now(timezone.utc).isoformat(),
                }
            )
    # Deduplicate
    seen = set()
    unique = []
    for c in candidates:
        if c["name"] not in seen:
            seen.add(c["name"])
            unique.append(c)
    print(f"  ✅ {len(unique)} unique packages from npm")
    return unique


def ingest_pypi() -> list[dict]:
    """Search PyPI for MCP-related packages."""
    print("🔍 Searching PyPI...")
    candidates = []
    for pkg_name in SOURCES["pypi_mcp"]["packages"]:
        data = fetch_json(f"{SOURCES['pypi_mcp']['api']}{pkg_name}/json")
        if not data:
            continue
        info = data.get("info", {})
        candidates.append(
            {
                "source": "pypi",
                "source_type": "package_registry",
                "name": info.get("name", pkg_name),
                "description": info.get("summary", ""),
                "url": info.get("package_url", ""),
                "author": info.get("author", ""),
                "tags": info.get("keywords", "").split(",") if info.get("keywords") else [],
                "version": info.get("version", ""),
                "discovered_at": datetime.now(timezone.utc).isoformat(),
            }
        )
    print(f"  ✅ {len(candidates)} packages from PyPI")
    return candidates


def ingest_github() -> list[dict]:
    """Search GitHub for MCP server repos."""
    print("🔍 Searching GitHub topics...")
    candidates = []
    for topic in SOURCES["github_topics"]["topics"]:
        params = urllib.parse.urlencode(
            {
                "q": f"topic:{topic}",
                "sort": "updated",
                "order": "desc",
                "per_page": 30,
            }
        )
        api_url = f"{SOURCES['github_topics']['api']}?{params}"
        data = fetch_json(api_url)
        if not data:
            continue
        for item in data.get("items", []):
            candidates.append(
                {
                    "source": "github",
                    "source_type": "repository",
                    "name": item.get("full_name", "?"),
                    "description": item.get("description", ""),
                    "url": item.get("html_url", ""),
                    "author": item.get("owner", {}).get("login", ""),
                    "tags": item.get("topics", []),
                    "stars": item.get("stargazers_count", 0),
                    "language": item.get("language", ""),
                    "updated_at": item.get("updated_at", ""),
                    "discovered_at": datetime.now(timezone.utc).isoformat(),
                }
            )
    # Deduplicate
    seen = set()
    unique = []
    for c in candidates:
        if c["name"] not in seen:
            seen.add(c["name"])
            unique.append(c)
    print(f"  ✅ {len(unique)} repos from GitHub")
    return unique


# ── Scoring ────────────────────────────────────────────────────


def score_candidate(candidate: dict) -> float:
    """Score candidate for federation compatibility (0-1)."""
    score = 0.0

    # Source quality
    source_scores = {
        "official_registry": 0.3,
        "package_registry": 0.2,
        "repository": 0.15,
        "directory": 0.1,
    }
    score += source_scores.get(candidate.get("source_type", ""), 0.05)

    # Has description
    desc = candidate.get("description", "")
    if len(desc) > 50:
        score += 0.1
    if len(desc) > 200:
        score += 0.05

    # Has repository/url
    if candidate.get("url") or candidate.get("repository"):
        score += 0.1

    # Has tags
    tags = candidate.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    if len(tags) > 0:
        score += 0.05
    if len(tags) > 3:
        score += 0.05

    # Transport info
    transport = candidate.get("transport", "unknown")
    if transport != "unknown":
        score += 0.1

    # Stars/popularity (GitHub)
    stars = candidate.get("stars", 0)
    if stars > 100:
        score += 0.05
    if stars > 1000:
        score += 0.05

    # Language (prefer Python, TypeScript)
    lang = candidate.get("language", "")
    if lang in ("Python", "TypeScript", "JavaScript"):
        score += 0.05

    return min(score, 1.0)


# ── Catalog Management ─────────────────────────────────────────


def load_existing() -> dict[str, dict]:
    """Load existing candidate catalog."""
    if CATALOG_FILE.exists():
        try:
            data = json.loads(CATALOG_FILE.read_text())
            return {c["name"]: c for c in data.get("candidates", [])}
        except (json.JSONDecodeError, KeyError):
            pass
    return {}


def merge_candidates(existing: dict[str, dict], new: list[dict]) -> tuple[list[dict], int, int]:
    """Merge new candidates into existing, tracking new/updated counts."""
    new_count = 0
    updated_count = 0

    for c in new:
        name = c["name"]
        if name not in existing:
            existing[name] = c
            new_count += 1
        else:
            # Update if newer or richer description
            old = existing[name]
            if len(c.get("description", "")) > len(old.get("description", "")):
                old["description"] = c["description"]
            if c.get("tags") and len(c.get("tags", [])) > len(old.get("tags", [])):
                old["tags"] = c["tags"]
            if c.get("stars", 0) > old.get("stars", 0):
                old["stars"] = c["stars"]
            old["last_seen_at"] = datetime.now(timezone.utc).isoformat()
            if not old.get("first_seen_at"):
                old["first_seen_at"] = c["discovered_at"]
            updated_count += 1

    # Score all
    result = list(existing.values())
    for c in result:
        c["federation_score"] = score_candidate(c)

    # Sort by score desc
    result.sort(key=lambda x: x.get("federation_score", 0), reverse=True)

    return result, new_count, updated_count


def write_catalog(candidates: list[dict], stats: dict):
    """Write candidate catalog and index."""
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    FORGE_WORK.mkdir(parents=True, exist_ok=True)

    catalog = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_candidates": len(candidates),
        "new_this_cycle": stats.get("new", 0),
        "updated_this_cycle": stats.get("updated", 0),
        "sources_polled": list(SOURCES.keys()),
        "top_scored": [
            {
                "name": c["name"],
                "score": c.get("federation_score", 0),
                "source": c.get("source", "?"),
                "description": c.get("description", "")[:120],
            }
            for c in candidates[:20]
            if c.get("federation_score", 0) > 0.3
        ],
        "candidates": candidates,
    }

    CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    print(f"\n📦 Catalog: {CATALOG_FILE} ({len(candidates)} candidates)")

    # Dated copy
    dated_path = FORGE_WORK / "candidates.json"
    dated_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))

    # Index
    index = {
        "name": "External MCP Server Candidates",
        "purpose": "Discovered external MCP servers evaluated for federation compatibility",
        "total_candidates": len(candidates),
        "high_confidence": len([c for c in candidates if c.get("federation_score", 0) > 0.5]),
        "medium_confidence": len([c for c in candidates if 0.25 < c.get("federation_score", 0) <= 0.5]),
        "low_confidence": len([c for c in candidates if c.get("federation_score", 0) <= 0.25]),
        "sources": list(SOURCES.keys()),
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "top_picks": [
            {"name": c["name"], "score": c.get("federation_score", 0), "source": c.get("source", "?")}
            for c in candidates[:10]
            if c.get("federation_score", 0) > 0.4
        ],
    }
    (CATALOG_DIR / "INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"📋 Index: {CATALOG_DIR / 'INDEX.json'}")


# ── Main ───────────────────────────────────────────────────────


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  mcp_ecosystem_ingest.py — External MCP Discovery       ║")
    print("║  DITEMPA BUKAN DIBERI  ·  2026-07-28                     ║")
    print("╚══════════════════════════════════════════════════════════╝")

    existing = load_existing()
    print(f"📚 Existing catalog: {len(existing)} candidates\n")

    all_new = []

    # Poll each source
    if SOURCES["registry_mcp_io"]["enabled"]:
        all_new.extend(ingest_registry_mcp_io())

    if SOURCES["npm_mcp"]["enabled"]:
        all_new.extend(ingest_npm())

    if SOURCES["pypi_mcp"]["enabled"]:
        all_new.extend(ingest_pypi())

    if SOURCES["github_topics"]["enabled"]:
        all_new.extend(ingest_github())

    # Merge and score
    candidates, new_count, updated_count = merge_candidates(existing, all_new)

    stats = {
        "new": new_count,
        "updated": updated_count,
        "total": len(candidates),
    }

    print(f"\n{'=' * 60}")
    print(f"📊 INGESTION SUMMARY")
    print(f"  New candidates:       {new_count}")
    print(f"  Updated candidates:   {updated_count}")
    print(f"  Total in catalog:     {len(candidates)}")
    print(f"  High confidence (>0.5): {len([c for c in candidates if c.get('federation_score', 0) > 0.5])}")

    write_catalog(candidates, stats)

    # Hash
    catalog_hash = hashlib.sha256(CATALOG_FILE.read_bytes()).hexdigest()
    print(f"\n🔐 SHA256: {catalog_hash}")

    return candidates


if __name__ == "__main__":
    main()
