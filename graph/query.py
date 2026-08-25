#!/usr/bin/env python3
"""
query.py — read-side API over codegraph.db.

Public surface (all return plain dicts, never raw rows):
  blast_radius(file_path)               -> {"files": [...], "symbols": [...], "summary": ...}
  dependents(symbol_qualified_name)     -> {"callers": [...], "files": [...], "count": N}
  symbols_in(file_path)                 -> list of symbol dicts
  search(name, kind=None, limit=50)     -> list of matching symbols
  file_summary(file_path)               -> summary dict with counts
  impact(file_path, depth=2)            -> transitive blast radius
  cross_repo_callers(symbol_qualified_name)  -> external callers across repo boundaries

Resolve semantics:
  - edges.dst_qualified_name is matched against symbols.qualified_name within
    the same file or same repo. Cross-repo resolution is best-effort by
    qualified_name match across all repos.

DITEMPA BUKAN DIBERI ⚒️ — graph for I-ARIF and forge blast-radius.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Optional

DEFAULT_DB = Path("/root/AAA/graph/codegraph.db")


def connect(db_path: Path = DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


# ─── resolution helpers ────────────────────────────────────────────────


def _resolve_file(conn, repo: str | None, rel_path: str) -> Optional[int]:
    """Find files.id for a given (repo?, rel_path?). repo=None means
    match any repo with that rel_path (rare; prefer repo)."""
    if repo:
        r = conn.execute(
            "SELECT f.id FROM files f JOIN repos r ON f.repo_id=r.id"
            " WHERE r.name=? AND f.rel_path=?",
            (repo, rel_path),
        ).fetchone()
        if r:
            return r["id"]
    # fallback: match on rel_path only
    r = conn.execute("SELECT id FROM files WHERE rel_path=? LIMIT 1", (rel_path,)).fetchone()
    return r["id"] if r else None


def _resolve_symbols_by_qname(conn, qname: str) -> list[dict]:
    rows = conn.execute(
        "SELECT s.*, f.rel_path, f.repo_id, r.name AS repo_name, f.language"
        " FROM symbols s"
        " JOIN files f ON s.file_id=f.id"
        " JOIN repos r ON f.repo_id=r.id"
        " WHERE s.qualified_name=? OR s.qualified_name LIKE ?",
        (qname, f"%{qname}"),
    ).fetchall()
    return [dict(r) for r in rows]


# ─── public queries ────────────────────────────────────────────────────


def blast_radius(repo_or_path: str, *, depth: int = 1,
                 db_path: Path = DEFAULT_DB) -> dict:
    """What breaks if I change this file or symbol?

    Inputs accepted:
      "arifOS/path/to/file.py"  → blast radius of that file
      "path/to/file.py"         → match any repo
      "Symbol.qualified_name"    → blast radius of that symbol
    """
    conn = connect(db_path)
    file_id = None
    if "/" in repo_or_path:
        repo, rel = repo_or_path.split("/", 1) if repo_or_path.split("/", 1)[0] in _known_repos(conn) \
            else (None, repo_or_path)
        file_id = _resolve_file(conn, repo, rel)
    if not file_id:
        # treat as symbol qualified name
        return blast_radius_symbol(repo_or_path, depth=depth, db_path=db_path)

    # 1. Direct dependents: edges whose dst matches symbols in this file
    rows = conn.execute(
        "SELECT s.qualified_name, s.file_id, f.rel_path, r.name AS repo_name, "
        "       s.kind, e.edge_type, e.line"
        " FROM edges e"
        " JOIN symbols s ON e.resolved_dst_symbol_id = s.id"
        " JOIN files f ON s.file_id=f.id"
        " JOIN repos r ON f.repo_id=r.id"
        " WHERE e.src_file_id != ? AND s.file_id = ?",
        (file_id, file_id),
    ).fetchall()
    # Fallback: also include edges where dst_qualified_name appears in this file
    fallback_rows = []
    if not rows:
        file_qnames = [r["qualified_name"] for r in conn.execute(
            "SELECT qualified_name FROM symbols WHERE file_id=?", (file_id,)
        ).fetchall()]
        if file_qnames:
            placeholders = ",".join("?" * len(file_qnames))
            fallback_rows = conn.execute(
                "SELECT DISTINCT e.src_file_id, e.src_symbol_id, e.dst_qualified_name,"
                "       e.edge_type, e.line, f.rel_path, r.name AS repo_name"
                " FROM edges e"
                " JOIN files f ON e.src_file_id=f.id"
                " JOIN repos r ON f.repo_id=r.id"
                " WHERE e.dst_qualified_name IN (" + placeholders + ")"
                "   AND e.src_file_id != ?",
                (*file_qnames, file_id),
            ).fetchall()

    # Also: files that import this file's module path
    file_rel = conn.execute(
        "SELECT f.rel_path, r.name AS repo_name FROM files f"
        " JOIN repos r ON f.repo_id=r.id WHERE f.id=?",
        (file_id,),
    ).fetchone()
    module_imports = []
    if file_rel:
        # Naive: any file that imports this rel_path's dotted form
        dotted = file_rel["rel_path"].replace("/", ".").removesuffix(".py").removesuffix(".__init__")
        for r in conn.execute(
            "SELECT DISTINCT f.rel_path, r.name AS repo_name, f.id AS file_id"
            " FROM imports i"
            " JOIN files f ON i.file_id=f.id"
            " JOIN repos r ON f.repo_id=r.id"
            " WHERE i.src_module=? OR i.src_module LIKE ? OR i.src_module LIKE ?",
            (dotted, f"%{dotted}%", f"%{file_rel['rel_path']}%"),
        ).fetchall():
            module_imports.append({"file_id": r["file_id"], "rel_path": r["rel_path"],
                                    "repo": r["repo_name"], "via": "import"})

    conn.close()
    affected_files = list({(r["rel_path"], r["repo_name"]) for r in rows + fallback_rows})
    if module_imports:
        affected_files.extend((m["rel_path"], m["repo"]) for m in module_imports)

    return {
        "target_file": file_rel["rel_path"] if file_rel else None,
        "target_repo": file_rel["repo_name"] if file_rel else None,
        "affected_files_count": len({r[0] for r in affected_files}),
        "affected_files": sorted({r[0] for r in affected_files}),
        "affected_repos": sorted({r[1] for r in affected_files}),
        "edges": [dict(r) for r in rows],
        "import_dependents": module_imports,
        "summary": f"{len({r[0] for r in affected_files})} files in "
                   f"{len({r[1] for r in affected_files})} repos may break",
    }


def blast_radius_symbol(qname: str, *, depth: int = 1,
                          db_path: Path = DEFAULT_DB) -> dict:
    """Blast radius centered on a symbol's qualified name."""
    conn = connect(db_path)
    syms = _resolve_symbols_by_qname(conn, qname)
    if not syms:
        conn.close()
        return {"target_symbol": qname, "found": False,
                "summary": "no symbols match that qualified name"}

    # Direct callers — edges whose dst is one of these symbols
    sym_ids = [s["id"] for s in syms]
    placeholders = ",".join("?" * len(sym_ids))
    rows = conn.execute(
        "SELECT DISTINCT e.src_file_id, e.src_symbol_id, e.dst_qualified_name,"
        "       e.edge_type, e.line, f.rel_path, r.name AS repo_name"
        " FROM edges e"
        " JOIN files f ON e.src_file_id=f.id"
        " JOIN repos r ON f.repo_id=r.id"
        " WHERE e.resolved_dst_symbol_id IN (" + placeholders + ")",
        sym_ids,
    ).fetchall()
    # Fallback: by name
    fb_rows = []
    if not rows:
        qnames = [s["qualified_name"] for s in syms]
        name_ph = ",".join("?" * len(qnames))
        fb_rows = conn.execute(
            "SELECT DISTINCT e.src_file_id, e.src_symbol_id, e.dst_qualified_name,"
            "       e.edge_type, e.line, f.rel_path, r.name AS repo_name"
            " FROM edges e"
            " JOIN files f ON e.src_file_id=f.id"
            " JOIN repos r ON f.repo_id=r.id"
            " WHERE e.dst_qualified_name IN (" + name_ph + ")",
            qnames,
        ).fetchall()

    affected_files = sorted({(r["rel_path"], r["repo_name"]) for r in rows + fb_rows})
    conn.close()
    return {
        "target_symbol": qname,
        "found": True,
        "matched_symbols": [s["qualified_name"] for s in syms],
        "matched_files": sorted({s["rel_path"] for s in syms}),
        "matched_repos": sorted({s["repo_name"] for s in syms}),
        "callers_count": len({r["src_file_id"] for r in rows + fb_rows}),
        "affected_files": affected_files,
        "edges": [dict(r) for r in rows],
        "summary": f"{len({r['src_file_id'] for r in rows + fb_rows})} caller file(s)",
    }


def dependents(qname: str, *, db_path: Path = DEFAULT_DB) -> dict:
    """Who calls / references this symbol? (alias of blast_radius_symbol)."""
    return blast_radius_symbol(qname, depth=1, db_path=db_path)


def symbols_in(repo_or_path: str, *, db_path: Path = DEFAULT_DB) -> list[dict]:
    """List all symbols defined in a file."""
    conn = connect(db_path)
    repo, rel = (None, repo_or_path)
    if "/" in repo_or_path:
        first = repo_or_path.split("/", 1)[0]
        if first in _known_repos(conn):
            repo, rel = first, repo_or_path.split("/", 1)[1]
    file_id = _resolve_file(conn, repo, rel)
    if not file_id:
        conn.close()
        return []
    rows = conn.execute(
        "SELECT s.*, f.rel_path, r.name AS repo_name"
        " FROM symbols s JOIN files f ON s.file_id=f.id JOIN repos r ON f.repo_id=r.id"
        " WHERE s.file_id=? ORDER BY s.line_start",
        (file_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search(name: str, *, kind: Optional[str] = None, limit: int = 50,
           db_path: Path = DEFAULT_DB) -> list[dict]:
    """Substring search by symbol name (LIKE %name%)."""
    conn = connect(db_path)
    if kind:
        rows = conn.execute(
            "SELECT s.qualified_name, s.kind, s.line_start, s.line_end,"
            "       s.signature, f.rel_path, r.name AS repo_name, f.language"
            " FROM symbols s JOIN files f ON s.file_id=f.id"
            " JOIN repos r ON f.repo_id=r.id"
            " WHERE s.name LIKE ? AND s.kind=? LIMIT ?",
            (f"%{name}%", kind, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT s.qualified_name, s.kind, s.line_start, s.line_end,"
            "       s.signature, f.rel_path, r.name AS repo_name, f.language"
            " FROM symbols s JOIN files f ON s.file_id=f.id"
            " JOIN repos r ON f.repo_id=r.id"
            " WHERE s.name LIKE ? LIMIT ?",
            (f"%{name}%", limit),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def file_summary(repo_or_path: str, *, db_path: Path = DEFAULT_DB) -> dict:
    conn = connect(db_path)
    repo, rel = (None, repo_or_path)
    if "/" in repo_or_path:
        first = repo_or_path.split("/", 1)[0]
        if first in _known_repos(conn):
            repo, rel = first, repo_or_path.split("/", 1)[1]
    file_id = _resolve_file(conn, repo, rel)
    if not file_id:
        conn.close()
        return {"found": False, "path": repo_or_path}
    meta = dict(conn.execute(
        "SELECT f.*, r.name AS repo_name FROM files f"
        " JOIN repos r ON f.repo_id=r.id WHERE f.id=?", (file_id,)
    ).fetchone())
    sym_count = conn.execute("SELECT COUNT(*) FROM symbols WHERE file_id=?",
                             (file_id,)).fetchone()[0]
    imp_count = conn.execute("SELECT COUNT(*) FROM imports WHERE file_id=?",
                             (file_id,)).fetchone()[0]
    out_edge = conn.execute("SELECT COUNT(*) FROM edges WHERE src_file_id=?",
                            (file_id,)).fetchone()[0]
    in_edge = conn.execute("SELECT COUNT(*) FROM edges e JOIN symbols s"
                           " ON e.resolved_dst_symbol_id=s.id WHERE s.file_id=?",
                           (file_id,)).fetchone()[0]
    conn.close()
    return {
        "found": True,
        "repo": meta["repo_name"],
        "rel_path": meta["rel_path"],
        "language": meta["language"],
        "size_bytes": meta["size_bytes"],
        "symbols": sym_count,
        "imports": imp_count,
        "edges_out": out_edge,
        "edges_in": in_edge,
    }


def impact(repo_or_path: str, *, depth: int = 2,
           db_path: Path = DEFAULT_DB) -> dict:
    """Transitive blast radius (BFS up to `depth` levels)."""
    seen_files = set()
    seen_symbols = set()
    frontier_files = {repo_or_path}
    frontier_symbols = set()
    layers = []

    for lvl in range(depth):
        layer_files = set()
        layer_symbols = set()
        for f in frontier_files:
            if f in seen_files:
                continue
            seen_files.add(f)
            br = blast_radius(f, depth=1, db_path=db_path)
            layer_files.update(br.get("affected_files", []))
        for s in frontier_symbols:
            if s in seen_symbols:
                continue
            seen_symbols.add(s)
            d = dependents(s, db_path=db_path)
            layer_files.update(p[0] for p in d.get("affected_files", []))
        if not layer_files:
            break
        layers.append({"level": lvl + 1, "files": sorted(layer_files)})
        frontier_files = layer_files

    return {
        "target": repo_or_path,
        "depth": depth,
        "layers": layers,
        "total_files": len(seen_files),
        "summary": f"{len(seen_files)} files reachable within {depth} hops",
    }


def cross_repo_callers(qname: str, *, db_path: Path = DEFAULT_DB) -> dict:
    """For a symbol defined in repo X, who calls it from OTHER repos?

    v1.1: name-match against dst_qualified_name (not just resolved IDs),
    so we can surface even calls that aren't fully resolved cross-file.
    Cross-repo callers must have an `import` statement pointing into the
    defining repo's package — pure HTTP/MCP calls don't show up here.
    """
    conn = connect(db_path)
    target_syms = _resolve_symbols_by_qname(conn, qname)
    if not target_syms:
        conn.close()
        return {"target_symbol": qname, "found": False}

    # Split exact vs. fuzzy matches — defining set is EXACT qualified_name only.
    target_syms_exact = [s for s in target_syms if s["qualified_name"] == qname]
    target_syms_similar = [s for s in target_syms if s["qualified_name"] != qname]
    if not target_syms_exact:
        # Nothing defines this exact name — caller probably meant a similar symbol.
        conn.close()
        return {"target_symbol": qname, "found": False,
                "similar_symbols": sorted({s["qualified_name"] for s in target_syms_similar}),
                "summary": f"no symbol defines '{qname}' exactly; "
                           f"{len(target_syms_similar)} similar names exist"}
    target_repos = {s["repo_name"] for s in target_syms_exact}
    target_qnames = sorted({s["qualified_name"] for s in target_syms_exact})
    similar_qnames = sorted({s["qualified_name"] for s in target_syms_similar})

    # Step 1: imports — find files (any repo) that import any of the
    # defining repo's top-level modules containing target_qnames.
    # Heuristic: dotted = repo_name + "." + part of file rel_path
    # e.g. arifOS.symbols.arif_judge → import "arifOS.arifosmcp.tools.judge"
    # Better: build a map of file rel_path → module dotted-name candidates
    # per repo, then check imports.src_module against those.
    import_candidates = set()
    for s in target_syms:
        rel = s["rel_path"]
        # strip extension
        if rel.endswith(".py"):
            mod = rel[:-3].replace("/", ".")
            if mod.endswith(".__init__"):
                mod = mod[:-9]
            import_candidates.add(mod)
            # Also: parent packages
            parts = mod.split(".")
            for i in range(1, len(parts)):
                import_candidates.add(".".join(parts[:i]))

    # Step 2: same-repo callers — symbols/edges that reference target_qnames
    # by name match (regardless of resolution)
    placeholders = ",".join("?" * len(target_qnames))
    same_repo_rows = conn.execute(
        "SELECT DISTINCT e.src_file_id, e.dst_qualified_name,"
        "       f.rel_path, r.name AS caller_repo"
        " FROM edges e"
        " JOIN files f ON e.src_file_id=f.id"
        " JOIN repos r ON f.repo_id=r.id"
        " WHERE e.dst_qualified_name IN (" + placeholders + ")",
        target_qnames,
    ).fetchall()
    same = [dict(r) for r in same_repo_rows if r["caller_repo"] in target_repos]
    cross = [dict(r) for r in same_repo_rows if r["caller_repo"] not in target_repos]

    # Step 3: cross-repo callers via imports — files in other repos that
    # import a module of the defining repo's package.
    cross_import_rows = []
    if import_candidates:
        ic_ph = ",".join("?" * len(import_candidates))
        cross_import_rows = conn.execute(
            "SELECT DISTINCT f.rel_path AS importer, r.name AS importer_repo,"
            "       i.src_module AS imported_module"
            " FROM imports i"
            " JOIN files f ON i.file_id=f.id"
            " JOIN repos r ON f.repo_id=r.id"
            " WHERE i.src_module IN (" + ic_ph + ")"
            "   AND r.name NOT IN (" + ",".join("?" * len(target_repos)) + ")",
            (*import_candidates, *target_repos),
        ).fetchall()

    conn.close()
    return {
        "target_symbol": qname,
        "found": True,
        "defined_in_repos": sorted(target_repos),
        "similar_symbols": similar_qnames,
        "cross_repo_caller_count": len(cross),
        "cross_repo_caller_files": sorted({r["rel_path"] for r in cross}),
        "cross_repo_via_import": [
            {"importer": r["importer"], "importer_repo": r["importer_repo"],
             "imported_module": r["imported_module"]}
            for r in cross_import_rows
        ],
        "same_repo_caller_count": len(same),
        "summary": (
            f"{len(cross)} cross-repo caller file(s) + "
            f"{len(cross_import_rows)} cross-repo importer file(s) via module imports"
        ),
    }


# ─── internal ───────────────────────────────────────────────────────────


def _known_repos(conn) -> set[str]:
    return {r["name"] for r in conn.execute("SELECT name FROM repos").fetchall()}


# ─── CLI ────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) < 2:
        print("usage: query.py <command> [args]\n"
              "  commands:\n"
              "    blast <repo/path> | <symbol>\n"
              "    dependents <symbol>\n"
              "    symbols <repo/path>\n"
              "    search <name> [--kind class|function|method]\n"
              "    file <repo/path>\n"
              "    impact <repo/path> [--depth N]\n"
              "    cross <symbol>")
        sys.exit(0)

    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else ""

    fn = {
        "blast": blast_radius,
        "dependents": dependents,
        "symbols": symbols_in,
        "search": search,
        "file": file_summary,
        "impact": impact,
        "cross": cross_repo_callers,
    }.get(cmd)
    if not fn:
        print(f"unknown command: {cmd}")
        sys.exit(1)

    depth = 2
    kind = None
    if "--depth" in sys.argv:
        i = sys.argv.index("--depth")
        depth = int(sys.argv[i+1])
    if "--kind" in sys.argv:
        i = sys.argv.index("--kind")
        kind = sys.argv[i+1]

    kwargs = {}
    if depth and cmd == "impact":
        kwargs["depth"] = depth
    if kind and cmd == "search":
        kwargs["kind"] = kind

    result = fn(arg, **kwargs)
    print(json.dumps(result, indent=2, default=str))