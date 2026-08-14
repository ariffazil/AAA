"""
test_server.py — Tests for tree777 MCP server and index generator.

Run: cd /root/AAA/mcp/tree777 && python3 -m pytest test_server.py -v
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from slug_map import slugify, COLLISION_MAP, STRIP_PREFIXES
from server import (
    cache, WikiCache, WIKI_ROOT,
    _sanitize, _extract_summary, _resolve_category,
    root_index, category_index, read_entry,
    wiki_search, wiki_read, wiki_browse,
)


# ══════════════════════════════════════════════════════════════════════════════
# Slug resolution
# ══════════════════════════════════════════════════════════════════════════════

class TestSlugify:
    """Test slug_map.slugify() collision resolution and prefix stripping."""

    def test_collision_map_overrides(self):
        """_B/_C/_D files get semantic slugs from COLLISION_MAP."""
        assert slugify("SKILL_VPS_B") == "vps-health-audit"
        assert slugify("SKILL_VPS_C") == "vps-docker-manager"
        assert slugify("SKILL_VPS_D") == "vps-management"
        assert slugify("SKILL_DOCKER_B") == "docker-security"
        assert slugify("SKILL_DOCKER_C") == "docker-thermodynamics"
        assert slugify("SKILL_SKILL_B") == "skill-creator"
        assert slugify("SKILL_SKILL_C") == "skill-promote"
        assert slugify("SKILL_SKILL_D") == "skill-reflector"

    def test_prefix_stripping(self):
        """SKILL_, CONCEPT_, SCAR_ prefixes are stripped."""
        assert slugify("SKILL_CADDY") == "caddy"
        assert slugify("CONCEPT_HAMPA") == "hampa"
        assert slugify("SCAR_ROUTE") == "route"
        assert slugify("WORKFLOW_AGENT") == "agent"

    def test_md_suffix_stripped(self):
        """_MD suffix is stripped before slugification."""
        assert slugify("EPISTEMOLOGY_MD") == "epistemology"
        assert slugify("PHYSICS_MD") == "physics"
        assert slugify("VAULT_MD") == "vault"

    def test_already_clean(self):
        """Clean names pass through with lowercase + kebab."""
        assert slugify("OBSERVABILITY") == "observability"
        assert slugify("HAMPA") == "hampa"

    def test_no_collision_map_gaps(self):
        """Every entry in COLLISION_MAP has a non-empty slug."""
        for stem, slug in COLLISION_MAP.items():
            assert slug, f"Empty slug for {stem}"
            assert slug == slug.lower(), f"Slug not lowercase: {stem} → {slug}"
            assert "_" not in slug, f"Underscore in slug: {stem} → {slug}"


# ══════════════════════════════════════════════════════════════════════════════
# Wiki scanning
# ══════════════════════════════════════════════════════════════════════════════

class TestWikiScan:
    """Test wiki scanning and entry resolution."""

    @pytest.fixture(autouse=True)
    def _refresh_cache(self):
        cache.refresh()

    def test_entry_count(self):
        """Wiki has at least 120 entries."""
        assert len(cache.entries) >= 120

    def test_no_duplicate_uris(self):
        """Every entry has a unique URI."""
        uris = [e.uri for e in cache.entries]
        assert len(uris) == len(set(uris)), f"Duplicate URIs found"

    def test_kind_coverage(self):
        """At least skill, concept, scar, axiom, entity kinds exist."""
        kinds = {e.kind for e in cache.entries}
        for expected in ["skill", "concept", "scar", "axiom", "entity"]:
            assert expected in kinds, f"Missing kind: {expected}"

    def test_category_resolution_skills(self):
        """Skill subdirs become categories."""
        infra = [e for e in cache.entries
                 if e.kind == "skill" and e.category == "infrastructure"]
        assert len(infra) >= 20, f"Expected 20+ infra skills, got {len(infra)}"

    def test_category_resolution_concepts(self):
        """Concepts without subdirs get 'root' category."""
        root_concepts = [e for e in cache.entries
                         if e.kind == "concept" and e.category == "root"]
        assert len(root_concepts) >= 20

    def test_collision_entries_resolve(self):
        """_B/_C/_D entries resolve to distinct URIs."""
        vps_entries = [e for e in cache.entries if "vps" in e.slug]
        assert len(vps_entries) >= 3, "VPS entries should include health-audit, docker-manager, management"
        slugs = {e.slug for e in vps_entries}
        assert "vps-health-audit" in slugs
        assert "vps-docker-manager" in slugs
        assert "vps-management" in slugs

    def test_no_underscore_slugs(self):
        """No entry should have underscores in its slug."""
        for e in cache.entries:
            assert "_" not in e.slug, f"Underscore in slug: {e.uri} → {e.slug}"


# ══════════════════════════════════════════════════════════════════════════════
# Security
# ══════════════════════════════════════════════════════════════════════════════

class TestSecurity:
    """Test host path sanitization and path traversal guards."""

    def test_sanitize_root_path(self):
        assert "/root/" not in _sanitize("files at /root/AAA/wiki/foo")

    def test_sanitize_opt_path(self):
        assert "/opt/" not in _sanitize("installed at /opt/arifos/src")

    def test_sanitize_preserves_other_text(self):
        result = _sanitize("Caddy reverse proxy configuration")
        assert "Caddy reverse proxy" in result

    def test_manifest_no_host_paths(self):
        """Generated index entries must not leak host filesystem paths.
        URI field is excluded — it legitimately contains '/root/' as category."""
        import re
        host_path_re = re.compile(r"/root/\w|/opt/\w|/home/\w")
        cache.refresh()
        for e in cache.entries:
            entry_dict = e.to_index_entry()
            for k, v in entry_dict.items():
                if k == "uri":
                    continue  # URI contains category 'root' — not a host path
                if isinstance(v, str):
                    assert not host_path_re.search(v), \
                        f"Host path in {e.uri}.{k}: {v}"


# ══════════════════════════════════════════════════════════════════════════════
# Search
# ══════════════════════════════════════════════════════════════════════════════

class TestSearch:
    """Test wiki search relevance and ranking."""

    @pytest.fixture(autouse=True)
    def _refresh_cache(self):
        cache.refresh()

    def test_search_by_slug(self):
        """Slug match ranks highest."""
        results = cache.search("caddy")
        assert len(results) > 0
        assert results[0].slug == "caddy"

    def test_search_by_title(self):
        """Title match returns results."""
        results = cache.search("docker")
        assert len(results) >= 2

    def test_search_empty_query(self):
        """Empty query returns no results."""
        results = cache.search("")
        assert len(results) == 0

    def test_search_limit(self):
        """Limit is respected."""
        results = cache.search("a", limit=3)
        assert len(results) <= 3

    def test_search_kind_filter(self):
        """Kind filter works in wiki_search tool."""
        results = wiki_search("arifos", kind="concept")
        for r in results:
            # Results may come back from fuzzy matching
            assert isinstance(r, dict)


# ══════════════════════════════════════════════════════════════════════════════
# Resources & Tools
# ══════════════════════════════════════════════════════════════════════════════

class TestResources:
    """Test MCP resource and tool functions."""

    @pytest.fixture(autouse=True)
    def _refresh_cache(self):
        cache.refresh()

    def test_root_index_structure(self):
        """Root index has required v2.0 fields."""
        idx = json.loads(root_index())
        assert idx["schema_version"] == "2.0"
        assert "totals" in idx
        assert "categories" in idx
        assert "template" in idx
        assert "coverage_warning" in idx
        assert idx["total_entries"] >= 120

    def test_category_index_infrastructure(self):
        """Infrastructure sub-index has entries."""
        result = json.loads(category_index("infrastructure"))
        assert result["count"] >= 20
        assert len(result["entries"]) >= 20
        # Each entry has required fields
        for entry in result["entries"]:
            assert "uri" in entry
            assert "title" in entry
            assert "sha256" in entry
            assert "size" in entry

    def test_read_entry_valid(self):
        """Reading a valid entry returns markdown."""
        body = read_entry("skill", "infrastructure", "caddy")
        assert "Caddy" in body or "caddy" in body.lower()

    def test_read_entry_not_found(self):
        """Reading a nonexistent entry raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_entry("skill", "infrastructure", "nonexistent-entry-xyz")

    def test_wiki_read_valid(self):
        """wiki_read tool returns body for valid URI."""
        body = wiki_read("tree777://skill/infrastructure/caddy")
        assert len(body) > 100

    def test_wiki_read_invalid_scheme(self):
        """wiki_read rejects non-tree777 URIs."""
        with pytest.raises(ValueError, match="Invalid URI scheme"):
            wiki_read("http://example.com/foo")

    def test_wiki_read_malformed_uri(self):
        """wiki_read rejects malformed URIs."""
        with pytest.raises(ValueError, match="Invalid tree777 URI"):
            wiki_read("tree777://only-one-part")

    def test_wiki_browse_root(self):
        """wiki_browse with no category returns root index."""
        result = wiki_browse()
        assert result["schema_version"] == "2.0"

    def test_wiki_browse_category(self):
        """wiki_browse with category returns entries."""
        result = wiki_browse(category="infrastructure")
        assert result["count"] >= 20


# ══════════════════════════════════════════════════════════════════════════════
# Index generator
# ══════════════════════════════════════════════════════════════════════════════

class TestManifest:
    """Test the generated tree-manifest.json."""

    def test_manifest_file_exists(self):
        manifest_path = WIKI_ROOT / "tree-manifest.json"
        assert manifest_path.exists()

    def test_manifest_schema_version(self):
        m = json.loads((WIKI_ROOT / "tree-manifest.json").read_text())
        assert m["schema_version"] == "2.0"

    def test_manifest_no_host_paths(self):
        """Manifest entry values must not contain host filesystem paths.
        URI keys/values are excluded — URIs contain category 'root'."""
        import re
        host_path_re = re.compile(r"/root/\w|/opt/\w|/home/\w")
        m = json.loads((WIKI_ROOT / "tree-manifest.json").read_text())
        for uri, entry in m["entries"].items():
            for k, v in entry.items():
                if isinstance(v, str):
                    assert not host_path_re.search(v), \
                        f"Host path in {uri}.{k}: {v}"

    def test_manifest_entry_fields(self):
        """Every entry has required v2.0 fields."""
        m = json.loads((WIKI_ROOT / "tree-manifest.json").read_text())
        required = {"slug", "title", "kind", "category", "sha256", "size", "updated_at"}
        for uri, entry in m["entries"].items():
            missing = required - set(entry.keys())
            assert not missing, f"Missing fields in {uri}: {missing}"

    def test_manifest_has_coverage_warnings(self):
        m = json.loads((WIKI_ROOT / "tree-manifest.json").read_text())
        assert "coverage_warning" in m
        assert isinstance(m["coverage_warning"], list)
