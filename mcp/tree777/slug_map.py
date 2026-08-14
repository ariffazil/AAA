"""
slug_map.py — Semantic slug resolution for tree777 wiki entries.

Resolves _B/_C/_D suffix collisions and strips redundant prefixes
(SKILL_, CONCEPT_, SCAR_, WORKFLOW_, AXIOM_) to produce clean kebab-case slugs.

DITEMPA BUKAN DIBERI
"""
from __future__ import annotations

# ── Collision map: filename stem → semantic slug ─────────────────────────────
# Every _B/_C/_D file gets a meaningful name derived from its frontmatter title.
# Keys are UPPERCASE stems (matching disk filenames without .md).

COLLISION_MAP: dict[str, str] = {
    # ── Infrastructure skills ────────────────────────────────────────────
    "SKILL_CLOUDFLARE_B": "cloudflare-email",
    "SKILL_CLOUDFLARE_C": "cloudflare-platform",
    "SKILL_DOCKER_B":     "docker-security",
    "SKILL_DOCKER_C":     "docker-thermodynamics",
    "SKILL_MCP_B":        "mcp-server-builder",
    "SKILL_MCP_C":        "mcp-unified",
    "SKILL_SECRET_B":     "secret-hygiene",
    "SKILL_SECRET_C":     "secret-rotation",
    "SKILL_VPS_B":        "vps-health-audit",
    "SKILL_VPS_C":        "vps-docker-manager",
    "SKILL_VPS_D":        "vps-management",

    # ── arifOS skills ────────────────────────────────────────────────────
    "SKILL_ARIFOS_B":          "arifos-atlas",
    "SKILL_ARIFOS_C":          "arifos-memory",
    "SKILL_ARIFOS_D":          "arifos-operator",
    "SKILL_CONSTITUTIONAL_B":  "constitutional-advisor",
    "SKILL_CONSTITUTIONAL_C":  "constitutional-reasoning",
    "SKILL_SKILL_B":           "skill-creator",
    "SKILL_SKILL_C":           "skill-promote",
    "SKILL_SKILL_D":           "skill-reflector",

    # ── Federation skills ────────────────────────────────────────────────
    "SKILL_AGENT_B": "agent-onboarding",
    "SKILL_AGENT_C": "agent-zero",

    # ── Scars ────────────────────────────────────────────────────────────
    "SCAR_OPENCLAW_B": "openclaw-diagnostic-cascade",
    "SCAR_OPENCLAW_C": "openclaw-telegram-conflict",

    # ── Concepts ─────────────────────────────────────────────────────────
    "CONCEPT_ARIFOS_B":  "arifos-self-certification",
    "CONCEPT_ARIFOS_C":  "arifos-heart-verdict-split",
    "CONCEPT_ARIFOS_D":  "arifos-not-llm",
    "CONCEPT_ARIFOS_E":  "arifos-loops",
    "CONCEPT_MEMORY_B":  "memory-knowledge-loop",
    "CONCEPT_MEMORY_C":  "memory-knowledge-paradox",
    "CONCEPT_MEMORY_D":  "memory-layers",
    "CONCEPT_SKILLS_B":  "skills-mcp-tool-map",
    "CONCEPT_SKILLS_C":  "skills-vs-workflows",

    # ── Root-level _B/_C collisions ──────────────────────────────────────
    "ARIF_FAZIL_B": "arif-fazil-complete-map",
    "ARIF_FAZIL_C": "arif-fazil-scar-terrain",
}

# ── Aliases: old URI → new URI (backward compat for one deprecation window) ──

ALIASES: dict[str, str] = {
    old_uri: new_uri
    for stem, slug in COLLISION_MAP.items()
    for old_uri, new_uri in [
        (f"tree777://skills/*/{stem}", f"tree777://skill/*/{slug}"),
    ]
}

# ── Prefixes to strip for default slug generation ────────────────────────────

STRIP_PREFIXES = (
    "SKILL_", "CONCEPT_", "SCAR_", "WORKFLOW_", "AXIOM_",
    "ENTITY_", "HUMAN_", "AGENT_",
)

STRIP_SUFFIXES = ("_MD",)


def slugify(stem: str) -> str:
    """Convert a filename stem to a clean kebab-case slug.

    1. Check COLLISION_MAP for explicit override.
    2. Strip known prefixes (SKILL_, CONCEPT_, etc.).
    3. Strip _MD suffix.
    4. Lowercase + underscores → hyphens.
    """
    upper = stem.upper()

    if upper in COLLISION_MAP:
        return COLLISION_MAP[upper]

    s = stem
    for prefix in STRIP_PREFIXES:
        if s.upper().startswith(prefix):
            s = s[len(prefix):]
            break

    for suffix in STRIP_SUFFIXES:
        if s.upper().endswith(suffix):
            s = s[:-len(suffix)]
            break

    return s.lower().replace("_", "-")


def old_uri_for(kind: str, category: str, stem: str) -> str:
    """Reconstruct the legacy tree777:// URI for backward compat."""
    kind_plural = {"skill": "skills", "concept": "concepts", "scar": "scars"}.get(kind, kind + "s")
    return f"tree777://{kind_plural}/{category}/{stem}"


def alias_for(kind: str, category: str, stem: str, new_slug: str) -> str | None:
    """Return legacy URI if stem differs from slug (i.e., an alias exists)."""
    old_slug = slugify(stem)
    if old_slug != new_slug or stem.lower().replace("_", "-") != new_slug:
        return old_uri_for(kind, category, stem)
    return None
