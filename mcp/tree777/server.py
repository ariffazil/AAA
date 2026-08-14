#!/usr/bin/env python3
"""
tree777 — AAA Wiki MCP Resource Server (v2.0)

Progressive-disclosure knowledge server for the arifOS federation wiki.
Exposes a thin root index → per-category sub-indexes → full markdown bodies,
plus wiki_search / wiki_read tools for model-accessible retrieval.

URI scheme:  tree777://{kind}/{category}/{slug}
Kinds:       skill, concept, scar, axiom, arifos, entity, infrastructure,
             nine-signal, playbook, raw

Spec alignment (MCP 2026-07-28):
  - annotations (audience, priority)
  - _meta (sha256, updated_at, size, tags, related)
  - text/markdown MIME for wiki bodies
  - -32602 for not-found

DITEMPA BUKAN DIBERI — Forged, not given.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from fastmcp import FastMCP

from slug_map import slugify, COLLISION_MAP

logger = logging.getLogger("tree777")

# ── Configuration ─────────────────────────────────────────────────────────────

WIKI_ROOT = Path("/root/AAA/wiki")
CACHE_TTL_SECONDS = 300  # 5 minutes
SERVER_PORT = 18077

SKIP_DIRS = {".git", "_runtime", "backups", ".arifos", "node_modules"}
SKIP_FILES = {"INDEX.md", "INDEX_MD.md", "LOG.md", "LOG_MD.md", "SCHEMA.md",
              "SCHEMA.md.docs-version-archived"}

FRONT_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

# ── Kind mapping: top-level directory → kind ──────────────────────────────────

DIR_TO_KIND = {
    "skills":          "skill",
    "concepts":        "concept",
    "scars":           "scar",
    "axioms":          "axiom",
    "arifos":          "arifos",
    "entities":        "entity",
    "infrastructure":  "infrastructure",
    "nine-signal":     "nine-signal",
    "playbook":        "playbook",
    "raw":             "raw",
    "workflows":       "workflow",
}

# Maturity thresholds
MATURITY_HIGH = 10
MATURITY_MEDIUM = 3

# ── FastMCP server ────────────────────────────────────────────────────────────

mcp = FastMCP(
    name="tree777",
    instructions=(
        "AAA Federation Wiki — progressive-disclosure knowledge server. "
        "Use tree777://index for the root catalog, tree777://index/{category} "
        "for per-category browsing, and tree777://{kind}/{category}/{slug} "
        "for full entry bodies. Or use wiki_search / wiki_read tools."
    ),
)

# ── Wiki entry data class ─────────────────────────────────────────────────────

class WikiEntry:
    __slots__ = (
        "path", "rel_path", "kind", "category", "stem", "slug",
        "title", "summary", "tags", "confidence", "updated_at",
        "sha256", "size", "word_count", "frontmatter",
    )

    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def uri(self) -> str:
        return f"tree777://{self.kind}/{self.category}/{self.slug}"

    def to_index_entry(self) -> dict:
        """Compact representation for sub-index listing."""
        d: dict[str, Any] = {
            "kind": self.kind,
            "slug": self.slug,
            "uri": self.uri,
            "title": self.title,
            "summary": self.summary,
            "tags": self.tags,
            "updated_at": self.updated_at,
            "sha256": self.sha256,
            "size": self.size,
            "confidence": self.confidence,
        }
        return d

    def read_body(self) -> str:
        return self.path.read_text(errors="ignore")


# ── Cache layer ───────────────────────────────────────────────────────────────

class WikiCache:
    """In-memory cache with TTL for wiki scan results."""

    def __init__(self, ttl: int = CACHE_TTL_SECONDS):
        self._ttl = ttl
        self._entries: list[WikiEntry] | None = None
        self._by_uri: dict[str, WikiEntry] = {}
        self._by_kind: dict[str, list[WikiEntry]] = {}
        self._by_category: dict[str, list[WikiEntry]] = {}
        self._generated_at: str = ""
        self._last_scan: float = 0

    @property
    def stale(self) -> bool:
        return (time.time() - self._last_scan) > self._ttl

    def refresh(self) -> None:
        if not self.stale and self._entries is not None:
            return
        self._entries = _scan_wiki(WIKI_ROOT)
        self._by_uri = {e.uri: e for e in self._entries}
        self._by_kind = {}
        self._by_category = {}
        for e in self._entries:
            self._by_kind.setdefault(e.kind, []).append(e)
            self._by_category.setdefault(e.category, []).append(e)
        self._generated_at = datetime.now(timezone.utc).isoformat()
        self._last_scan = time.time()
        logger.info("Wiki cache refreshed: %d entries", len(self._entries))

    @property
    def entries(self) -> list[WikiEntry]:
        self.refresh()
        return self._entries or []

    def by_uri(self, uri: str) -> WikiEntry | None:
        self.refresh()
        return self._by_uri.get(uri)

    def by_category(self, category: str) -> list[WikiEntry]:
        self.refresh()
        return sorted(self._by_category.get(category, []), key=lambda e: e.slug)

    def by_kind(self, kind: str) -> list[WikiEntry]:
        self.refresh()
        return sorted(self._by_kind.get(kind, []), key=lambda e: (e.category, e.slug))

    @property
    def categories(self) -> dict[str, dict]:
        self.refresh()
        cats: dict[str, dict] = {}
        for cat, entries in self._by_category.items():
            count = len(entries)
            if count >= MATURITY_HIGH:
                maturity = "high"
            elif count >= MATURITY_MEDIUM:
                maturity = "medium"
            else:
                maturity = "stub"
            cats[cat] = {
                "count": count,
                "maturity": maturity,
                "index": f"tree777://index/{cat}",
            }
        return dict(sorted(cats.items(), key=lambda x: -x[1]["count"]))

    @property
    def coverage_warnings(self) -> list[str]:
        return [cat for cat, info in self.categories.items()
                if info["maturity"] == "stub"]

    @property
    def totals(self) -> dict[str, int]:
        self.refresh()
        return {kind: len(entries) for kind, entries in
                sorted(self._by_kind.items(), key=lambda x: -len(x[1]))}

    @property
    def generated_at(self) -> str:
        self.refresh()
        return self._generated_at

    def search(self, query: str, limit: int = 15) -> list[WikiEntry]:
        self.refresh()
        q = query.strip().lower()
        if not q:
            return []
        scored: list[tuple[float, WikiEntry]] = []
        for e in self.entries:
            score = 0.0
            if q in e.slug:
                score += 3.0
            if q in e.title.lower():
                score += 2.0
            if q in e.summary.lower():
                score += 1.0
            if any(q in str(t).lower() for t in e.tags):
                score += 1.5
            # Full-text search (more expensive but thorough)
            if score == 0:
                try:
                    body = e.read_body()
                    if q in body.lower():
                        score += 0.5
                except Exception:
                    pass
            if score > 0:
                scored.append((score, e))
        scored.sort(key=lambda x: -x[0])
        return [e for _, e in scored[:limit]]


cache = WikiCache()


# ── Wiki scanner ──────────────────────────────────────────────────────────────

def _parse_frontmatter(text: str) -> dict:
    m = FRONT_RE.match(text)
    if not m:
        return {}
    try:
        fm = yaml.safe_load(m.group(1))
        return fm if isinstance(fm, dict) else {}
    except yaml.YAMLError:
        return {}


_HOST_PATH_RE = re.compile(r"/root/[\w\-./]*|/opt/[\w\-./]*|/home/[\w\-./]*")


def _sanitize(text: str) -> str:
    """Strip host filesystem paths from text (security: no path leakage)."""
    return _HOST_PATH_RE.sub("<path>", text)


def _extract_summary(text: str, fm: dict) -> str:
    """First meaningful paragraph after frontmatter, max 200 chars."""
    body = FRONT_RE.split(text)
    content = body[-1] if len(body) > 1 else text
    h2_lines = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("## "):
            h2_lines.append(line[3:].strip())
            continue
        if line.startswith("#"):
            continue
        if line.startswith(">"):
            continue
        if re.match(r"^[\w\-]+(\s*\([^)]*\))?\s*:", line):
            continue
        if len(line) > 20:
            return _sanitize(line[:200])
    if h2_lines:
        return _sanitize(h2_lines[0][:200])
    return ""


def _meta_for(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "sha256": hashlib.sha256(data).hexdigest()[:16],
        "size": len(data),
        "updated_at": datetime.fromtimestamp(
            path.stat().st_mtime, tz=timezone.utc
        ).isoformat(),
    }


def _resolve_category(rel: Path, kind: str) -> str:
    """Determine category from path structure.

    URI pattern: tree777://{kind}/{category}/{slug}
    - Root-level files → "root"
    - Files directly in kind dir (concepts/X.md) → "root"
    - Files in subdirs (skills/infrastructure/X.md) → subdir name
    - Deeply nested (raw/repos/notes/X.md) → immediate subdir
    """
    parts = rel.parts
    if len(parts) == 1:
        return "root"

    top_dir = parts[0]

    # Skills have organized subdirs: skills/infrastructure/X.md
    if kind == "skill":
        if len(parts) == 2:
            # skills/SKILL_ANTI.md → category "root"
            return "root"
        # skills/infrastructure/SKILL_CADDY.md → "infrastructure"
        return parts[1]

    # Raw has subdirs: raw/repos/X.md, raw/notes/X.md
    if kind == "raw":
        if len(parts) == 2:
            return "root"
        return parts[1]

    # Workflows: workflows/WORKFLOW_AGENT.md or workflows/sub-workflow/...
    if kind == "workflow":
        if len(parts) == 2:
            # workflows/WORKFLOW_AGENT.md → use filename-based category
            stem = Path(parts[1]).stem.lower().replace("workflow_", "").replace("-", "-")
            return stem if stem else "root"
        # workflows/workflow-agent-onboarding/reasoning/X.md → "agent-onboarding"
        sub = parts[1].lower().replace("workflow-", "")
        return sub if sub else "root"

    # For kind dirs with files directly inside (concepts/X.md, scars/X.md)
    # → "root" since the kind already provides the classification
    if len(parts) == 2:
        return "root"

    # Deeper nesting (unlikely but handle)
    return parts[1]


def _scan_wiki(root: Path) -> list[WikiEntry]:
    """Scan wiki directory tree and return list of WikiEntry objects."""
    entries = []
    for md in sorted(root.rglob("*.md")):
        # Skip excluded dirs
        if any(s in md.parts for s in SKIP_DIRS):
            continue
        # Skip excluded files
        if md.name in SKIP_FILES:
            continue

        rel = md.relative_to(root)
        parts = rel.parts
        if not parts:
            continue

        # Determine kind from top-level directory
        top_dir = parts[0]
        kind = DIR_TO_KIND.get(top_dir)

        # Root-level files (not in any subdirectory)
        if len(parts) == 1:
            kind = _infer_root_kind(md.stem)

        if kind is None:
            continue

        category = _resolve_category(rel, kind)
        fm_text = md.read_text(errors="ignore")
        fm = _parse_frontmatter(fm_text)
        meta = _meta_for(md)

        # Title from frontmatter or first H1 (sanitized for host paths)
        title = str(fm.get("title", "")) if fm.get("title") else ""
        if not title:
            h1 = re.search(r"^#\s+(.+)$", fm_text, re.MULTILINE)
            title = h1.group(1).strip() if h1 else md.stem.replace("_", " ").title()
        title = _sanitize(title)

        # Tags (normalize to strings — YAML may parse integers)
        raw_tags = fm.get("tags", [])
        if isinstance(raw_tags, str):
            tags = [t.strip().strip('"').strip("'") for t in raw_tags.split(",")]
        elif isinstance(raw_tags, list):
            tags = [str(t).strip() for t in raw_tags]
        else:
            tags = []

        # Confidence
        confidence = str(fm.get("confidence", "medium"))

        # Summary
        summary = _extract_summary(fm_text, fm)

        # Updated from frontmatter or mtime
        updated_raw = fm.get("updated")
        updated_at = str(updated_raw) if updated_raw else meta["updated_at"]

        slug = slugify(md.stem)

        entries.append(WikiEntry(
            path=md,
            rel_path=str(rel),
            kind=kind,
            category=category,
            stem=md.stem,
            slug=slug,
            title=title,
            summary=summary,
            tags=tags,
            confidence=confidence,
            updated_at=updated_at,
            sha256=meta["sha256"],
            size=meta["size"],
            word_count=len(fm_text.split()),
            frontmatter=fm,
        ))

    return entries


def _infer_root_kind(stem: str) -> str:
    """Infer kind for root-level wiki files."""
    upper = stem.upper()
    if upper.startswith("SCAR_"):
        return "scar"
    if upper.startswith("ARIF_FAZIL"):
        return "entity"
    if upper.startswith("HERMES"):
        return "entity"
    if upper.startswith("MEMORY"):
        return "concept"
    if upper.startswith("POST_TASK"):
        return "skill"
    if upper.startswith("AGENT_IDENTITY"):
        return "entity"
    return "concept"


# ── Path traversal guard ─────────────────────────────────────────────────────

def _safe_resolve(entry: WikiEntry) -> Path:
    """Verify entry path stays within wiki root."""
    resolved = entry.path.resolve()
    if WIKI_ROOT.resolve() not in [resolved.parent.resolve(), *resolved.parents]:
        raise ValueError("path escapes wiki root")
    return resolved


# ══════════════════════════════════════════════════════════════════════════════
# RESOURCES
# ══════════════════════════════════════════════════════════════════════════════

# ── Root index (thin, progressive disclosure) ────────────────────────────────

@mcp.resource(
    "tree777://index",
    name="wiki-root-index",
    title="📚 AAA Wiki — Root Index",
    description=(
        "Thin root index of the AAA federation wiki. "
        "Category counts, maturity, and pointers to sub-indexes. "
        "Use tree777://index/{category} for per-category entries."
    ),
    mime_type="application/json",
    annotations={"audience": ["user", "assistant"], "priority": 1.0},
)
def root_index() -> str:
    """Root index — category counts, maturity, pointers."""
    return json.dumps({
        "schema_version": "2.0",
        "generated_at": cache.generated_at,
        "totals": cache.totals,
        "total_entries": len(cache.entries),
        "categories": cache.categories,
        "coverage_warning": cache.coverage_warnings,
        "template": "tree777://{kind}/{category}/{slug}",
        "search": "tree777://search?q={query}",
    }, indent=2)


# ── Per-category sub-index (template) ────────────────────────────────────────

@mcp.resource(
    "tree777://index/{category}",
    name="wiki-category-index",
    title="📂 Category Index",
    description="Per-category sub-index with self-describing entries.",
    mime_type="application/json",
    annotations={"audience": ["user", "assistant"], "priority": 0.8},
)
def category_index(category: str) -> str:
    """Per-category index of self-describing entries."""
    entries = cache.by_category(category)
    if not entries:
        # Try kind-based lookup (user might pass "skills" instead of "skill")
        for e in cache.entries:
            if e.kind == category or e.category == category:
                entries = cache.by_category(e.category)
                break

    return json.dumps({
        "category": category,
        "generated_at": cache.generated_at,
        "count": len(entries),
        "entries": [e.to_index_entry() for e in entries],
    }, indent=2)


# ── Full entry body (template) ───────────────────────────────────────────────

@mcp.resource(
    "tree777://{kind}/{category}/{slug}",
    name="wiki-entry-body",
    title="📄 Wiki Entry",
    description="Full markdown body of a wiki entry.",
    mime_type="text/markdown",
    annotations={"audience": ["user", "assistant"], "priority": 0.5},
)
def read_entry(kind: str, category: str, slug: str) -> str:
    """Full markdown body of a wiki entry."""
    uri = f"tree777://{kind}/{category}/{slug}"
    entry = cache.by_uri(uri)

    if entry is None:
        # Fuzzy match: try to find by slug across all entries
        for e in cache.entries:
            if e.slug == slug and (e.kind == kind or e.category == category):
                entry = e
                break

    if entry is None:
        raise FileNotFoundError(f"tree777 entry not found: {uri}")

    _safe_resolve(entry)
    return entry.read_body()


# ── Search affordance as resource template ───────────────────────────────────

@mcp.resource(
    "tree777://search",
    name="wiki-search-resource",
    title="🔍 Wiki Search",
    description=(
        "Search the AAA wiki. Use the wiki_search tool for parameterized "
        "queries, or this resource for a usage guide."
    ),
    mime_type="text/markdown",
    annotations={"audience": ["assistant"], "priority": 0.3},
)
def search_guide() -> str:
    """Usage guide for wiki search."""
    return (
        "# Wiki Search\n\n"
        "Use the `wiki_search` tool with a `query` parameter to search the wiki.\n\n"
        "Example: call `wiki_search(query='caddy')` to find entries about Caddy.\n\n"
        "Results are ranked by relevance (slug match > title > tags > body).\n"
        "Each result includes a `resource_link` with URI, title, and summary.\n\n"
        "Then use `wiki_read(uri='tree777://...')` to read the full body."
    )


# ══════════════════════════════════════════════════════════════════════════════
# TOOLS — for model-accessible retrieval regardless of client resource support
# ══════════════════════════════════════════════════════════════════════════════

@mcp.tool(
    annotations={
        "title": "Wiki Search",
        "readOnlyHint": True,
        "idempotentHint": True,
    },
)
def wiki_search(query: str, limit: int = 15, kind: str = "") -> list[dict]:
    """Search the AAA federation wiki. Returns ranked resource links
    (uri + title + summary + score). Use wiki_read to get full bodies.

    Args:
        query: Search query (matches against slug, title, tags, summary, body).
        limit: Maximum results (default 15).
        kind: Filter by kind (skill, concept, scar, etc.). Empty = all kinds.
    """
    results = cache.search(query, limit=limit * 2)
    if kind:
        results = [e for e in results if e.kind == kind]
    results = results[:limit]

    output = []
    for e in results:
        output.append({
            "type": "resource_link",
            "uri": e.uri,
            "name": e.slug,
            "title": e.title,
            "mimeType": "text/markdown",
            "summary": e.summary,
            "tags": e.tags,
            "confidence": e.confidence,
            "size": e.size,
        })
    return output


@mcp.tool(
    annotations={
        "title": "Wiki Read",
        "readOnlyHint": True,
        "idempotentHint": True,
    },
)
def wiki_read(uri: str) -> str:
    """Read a tree777 wiki entry body by URI.

    Args:
        uri: Full tree777 URI, e.g. tree777://skill/infrastructure/caddy
    """
    if not uri.startswith("tree777://"):
        raise ValueError(f"Invalid URI scheme (expected tree777://): {uri}")

    rest = uri[len("tree777://"):]
    parts = rest.split("/", 2)
    if len(parts) != 3:
        raise ValueError(
            f"Invalid tree777 URI (expected kind/category/slug): {uri}"
        )

    kind, category, slug = parts
    entry = cache.by_uri(uri)

    if entry is None:
        # Fuzzy match
        for e in cache.entries:
            if e.slug == slug and (e.kind == kind or e.category == category):
                entry = e
                break

    if entry is None:
        raise FileNotFoundError(f"Entry not found: {uri}")

    _safe_resolve(entry)
    return entry.read_body()


@mcp.tool(
    annotations={
        "title": "Wiki Browse",
        "readOnlyHint": True,
        "idempotentHint": True,
    },
)
def wiki_browse(category: str = "", kind: str = "") -> dict:
    """Browse the wiki index. Returns category overview or sub-index.

    Args:
        category: Category name (e.g. 'infrastructure', 'arifos'). Empty = root index.
        kind: Filter by kind (skill, concept, scar). Optional.
    """
    if not category:
        return json.loads(root_index())

    entries = cache.by_category(category)
    if kind:
        entries = [e for e in entries if e.kind == kind]

    return {
        "category": category,
        "count": len(entries),
        "entries": [e.to_index_entry() for e in entries],
    }


# ══════════════════════════════════════════════════════════════════════════════
# SERVER ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else SERVER_PORT
    logger.info("Starting tree777 on port %d", port)
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
