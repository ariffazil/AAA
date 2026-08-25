#!/usr/bin/env python3
"""
indexer.py — walk federation repos, parse with tree-sitter, populate codegraph.db.

Run:
    /root/.venvs/codegraph/bin/python /root/AAA/graph/indexer.py \
        --db /root/AAA/graph/codegraph.db \
        [--repo arifOS=A-FORGE=AAA=GEOX=WELL=WEALTH=arifFlow]

Filters out: node_modules, .venv, venv, dist, build, __pycache__, .git,
.mypy_cache, .pytest_cache, .cache, .tox, .claude, .opencode,
*.min.js, *.bundle.js, files >1MB, non-code extensions.

Output: /root/AAA/graph/codegraph.db populated.
"""
from __future__ import annotations
import argparse
import hashlib
import os
import sqlite3
import sys
import time
from pathlib import Path

import tree_sitter as ts
import tree_sitter_python as py_lang
import tree_sitter_javascript as js_lang

ROOT = Path("/root")
DEFAULT_DB = Path("/root/AAA/graph/codegraph.db")
DEFAULT_REPOS = ["arifOS", "A-FORGE", "AAA", "GEOX", "WELL", "WEALTH", "arifFlow"]

EXCLUDE_DIR_NAMES = {
    "node_modules", "venv", ".venv", "env", ".env",
    "dist", "build", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".git", ".cache", ".tox", ".claude", ".opencode",
    ".idea", ".vscode", ".hermes", ".kimi-code",
    "data", "fixtures", "snapshots", "_archive",
}
EXCLUDE_FILE_PATTERNS = [
    ".min.js", ".bundle.js", ".test.js", ".spec.js",
    ".test.ts", ".spec.ts", ".test.tsx",
    ".test.py", ".d.ts",
]

LANG_BY_EXT = {
    ".py": "python",
    ".pyi": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
}

MAX_FILE_BYTES = 1_000_000  # 1MB


def _hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


# ─── tree-sitter setup ────────────────────────────────────────────────

PY_LANGUAGE = ts.Language(py_lang.language())
JS_LANGUAGE = ts.Language(js_lang.language())

_PARSER_CACHE = {}
def _parser(lang: str) -> ts.Parser:
    p = _PARSER_CACHE.get(lang)
    if p is None:
        language = PY_LANGUAGE if lang == "python" else JS_LANGUAGE
        p = ts.Parser(language)
        _PARSER_CACHE[lang] = p
    return p


# ─── AST extraction ────────────────────────────────────────────────────


def _walk(node: ts.Node):
    yield node
    for c in node.children:
        yield from _walk(c)


def _node_text(node: ts.Node, src: bytes) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def _py_extract(file_id: int, src: bytes, root: ts.Node, conn: sqlite3.Connection):
    """Walk a Python tree and emit symbols + imports + edges."""
    sym_id_map: dict[int, int] = {}  # tree-sitter node.id → symbol_id
    current_qname_stack: list[str] = []
    current_class_stack: list[tuple[str, str]] = []  # (qname, kind) for parent tracking

    def get_qname_stack():
        return current_qname_stack

    def push_class(name: str):
        if current_qname_stack:
            full = ".".join(current_qname_stack) + "." + name
        else:
            full = name
        current_qname_stack.append(name)
        current_class_stack.append((full, "class"))

    def pop_class():
        if current_qname_stack:
            current_qname_stack.pop()
            current_class_stack.pop()

    def current_parent_qname():
        return current_qname_stack[-1] if current_qname_stack else None

    # First pass: definitions
    for node in _walk(root):
        if node.type == "class_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                class_name = _node_text(name_node, src)
                push_class(class_name)
                full_qname = current_parent_qname()
                body = node.child_by_field_name("body")
                # Determine line range (whole class)
                line_start = node.start_point[0] + 1
                line_end = node.end_point[0] + 1
                # Docstring (first stmt in body if ExprStmt → string)
                docstring = None
                if body and body.children:
                    first = body.children[0]
                    if first.type == "expression_statement":
                        try:
                            string_node = first.children[0]
                            if string_node.type == "string":
                                docstring = _node_text(string_node, src).strip()
                        except (IndexError, AttributeError):
                            pass
                sig = f"class {class_name}"
                cur = conn.execute(
                    "INSERT OR REPLACE INTO symbols"
                    "(file_id, kind, name, qualified_name, line_start, line_end, signature, docstring, parent_qualified)"
                    " VALUES (?,?,?,?,?,?,?,?,?)",
                    (file_id, "class", class_name, full_qname, line_start, line_end, sig, docstring, None)
                )
                sym_id_map[node.id] = cur.lastrowid
                # Process nested definitions
                if body:
                    _py_extract_nested(file_id, src, body, conn, sym_id_map, current_qname_stack, current_class_stack)
                pop_class()

        elif node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            if name_node and not _is_nested_in_class_or_method(node, src):
                # top-level function only — nested ones handled by class body walk
                func_name = _node_text(name_node, src)
                if current_qname_stack:
                    full_qname = ".".join(current_qname_stack) + "." + func_name
                else:
                    full_qname = func_name
                line_start = node.start_point[0] + 1
                line_end = node.end_point[0] + 1
                params = node.child_by_field_name("parameters")
                sig = f"def {func_name}{_node_text(params, src) if params else '()'}:"
                docstring = _py_extract_docstring(node, src)
                cur = conn.execute(
                    "INSERT OR REPLACE INTO symbols"
                    "(file_id, kind, name, qualified_name, line_start, line_end, signature, docstring, parent_qualified)"
                    " VALUES (?,?,?,?,?,?,?,?,?)",
                    (file_id, "function", func_name, full_qname, line_start, line_end, sig, docstring, current_parent_qname())
                )
                sym_id_map[node.id] = cur.lastrowid

    # Second pass: imports and calls (as edges)
    for node in _walk(root):
        if node.type in ("import_statement", "import_from_statement"):
            _py_emit_import(file_id, src, node, conn)
        elif node.type == "call":
            _py_emit_call(file_id, src, node, conn, sym_id_map)


def _py_extract_nested(file_id: int, src: bytes, body: ts.Node,
                       conn: sqlite3.Connection, sym_id_map,
                       qname_stack: list[str], class_stack: list):
    """Walk inside a class body for methods + nested classes."""
    for node in _walk(body):
        if node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                method_name = _node_text(name_node, src)
                if qname_stack:
                    full_qname = ".".join(qname_stack) + "." + method_name
                else:
                    full_qname = method_name
                line_start = node.start_point[0] + 1
                line_end = node.end_point[0] + 1
                params = node.child_by_field_name("parameters")
                sig = f"def {method_name}{_node_text(params, src) if params else '()'}:"
                docstring = _py_extract_docstring(node, src)
                cur = conn.execute(
                    "INSERT OR REPLACE INTO symbols"
                    "(file_id, kind, name, qualified_name, line_start, line_end, signature, docstring, parent_qualified)"
                    " VALUES (?,?,?,?,?,?,?,?,?)",
                    (file_id, "method", method_name, full_qname, line_start, line_end, sig, docstring, class_stack[-1][0])
                )
                sym_id_map[node.id] = cur.lastrowid

        elif node.type == "class_definition":
            # nested class
            name_node = node.child_by_field_name("name")
            if name_node:
                name = _node_text(name_node, src)
                qname_stack.append(name)
                class_stack.append((".".join(qname_stack), "class"))
                _py_extract_nested(file_id, src, node.child_by_field_name("body"),
                                   conn, sym_id_map, qname_stack, class_stack)
                qname_stack.pop()
                class_stack.pop()


def _is_nested_in_class_or_method(node: ts.Node, src: bytes) -> bool:
    """Returns True if this function_definition is nested inside a class body
    (we already handle those via _py_extract_nested)."""
    parent = node.parent
    while parent:
        if parent.type == "class_definition":
            return True
        if parent.type in ("function_definition", "decorated_definition"):
            return True
        parent = parent.parent
    return False


def _py_extract_docstring(fn_node: ts.Node, src: bytes) -> str | None:
    body = fn_node.child_by_field_name("body")
    if body and body.children:
        first = body.children[0]
        if first.type == "expression_statement":
            try:
                s = first.children[0]
                if s.type == "string":
                    raw = _node_text(s, src).strip()
                    # strip triple quotes
                    return raw[3:-3] if raw.startswith('"""') or raw.startswith("'''") else raw[1:-1]
            except (IndexError, AttributeError):
                pass
    return None


def _py_emit_import(file_id: int, src: bytes, node: ts.Node, conn: sqlite3.Connection):
    if node.type == "import_statement":
        # `import os, sys`
        names = []
        for c in node.children:
            if c.type == "dotted_name" or c.type == "aliased_import":
                names.append(_node_text(c, src).split(" as ")[0])
        for n in names:
            conn.execute(
                "INSERT INTO imports(file_id, src_module, imported_names, line) VALUES (?,?,?,?)",
                (file_id, n, None, node.start_point[0] + 1),
            )
    elif node.type == "import_from_statement":
        # `from foo.bar import Baz`
        module_name_node = node.child_by_field_name("module_name")
        module = _node_text(module_name_node, src) if module_name_node else ""
        imported_names = []
        for c in node.children:
            if c.type == "dotted_name" and c is not module_name_node:
                imported_names.append(_node_text(c, src).split(" as ")[0])
            elif c.type == "aliased_import":
                imported_names.append(_node_text(c, src).split(" as ")[0])
        conn.execute(
            "INSERT INTO imports(file_id, src_module, imported_names, line) VALUES (?,?,?,?)",
            (file_id, module, ",".join(imported_names) if imported_names else None,
             node.start_point[0] + 1),
        )


def _py_emit_call(file_id: int, src: bytes, node: ts.Node,
                  conn: sqlite3.Connection, sym_id_map: dict):
    """Emit edges for call expressions.

    We resolve the *containing* function (best-effort: nearest enclosing
    function_definition) as src_symbol_id. The dst is the qualified_name
    of the called thing (e.g. 'os.path.join' or 'requests.get' or 'MyClass.foo').
    """
    func_node = node.child_by_field_name("function")
    if not func_node:
        return
    func_text = _node_text(func_node, src).strip()

    src_sym_id = _py_enclosing_symbol(node, sym_id_map)

    conn.execute(
        "INSERT INTO edges(src_file_id, src_symbol_id, dst_qualified_name, edge_type, line)"
        " VALUES (?,?,?,?,?)",
        (file_id, src_sym_id, func_text, "calls", node.start_point[0] + 1),
    )


def _py_enclosing_symbol(node: ts.Node, sym_id_map: dict) -> int | None:
    """Walk ancestors to find the nearest function/class containing this node."""
    parent = node.parent
    while parent:
        if parent.id in sym_id_map:
            return sym_id_map[parent.id]
        # also check via class body
        if parent.type in ("class_definition", "function_definition"):
            # Look for the parent node-id in sym_id_map (top-level only)
            pass
        parent = parent.parent
    return None


# ─── TS/JS extraction (lighter) ────────────────────────────────────────


def _ts_extract(file_id: int, src: bytes, root: ts.Node, conn: sqlite3.Connection):
    """Extract functions, classes, imports, calls from TS/JS.

    Qualified-name heuristic: dot-path of enclosing scope + name.
    For class methods, the qname is "ClassName.methodName".
    """
    sym_id_map: dict[int, int] = {}

    for node in _walk(root):
        if node.type == "class_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                class_name = _node_text(name_node, src)
                line_start = node.start_point[0] + 1
                line_end = node.end_point[0] + 1
                body = node.child_by_field_name("body")
                cur = conn.execute(
                    "INSERT OR REPLACE INTO symbols"
                    "(file_id, kind, name, qualified_name, line_start, line_end, signature, parent_qualified)"
                    " VALUES (?,?,?,?,?,?,?,?)",
                    (file_id, "class", class_name, class_name, line_start, line_end,
                     f"class {class_name}", None)
                )
                sym_id_map[node.id] = cur.lastrowid
                # methods
                if body:
                    for member in body.children:
                        if member.type == "method_definition":
                            mn = member.child_by_field_name("name")
                            if mn:
                                mname = _node_text(mn, src)
                                qname = f"{class_name}.{mname}"
                                ms = member.start_point[0] + 1
                                me = member.end_point[0] + 1
                                mp = member.child_by_field_name("parameters")
                                sig = f"{mname}({_node_text(mp, src) if mp else ''})"
                                cur2 = conn.execute(
                                    "INSERT OR REPLACE INTO symbols"
                                    "(file_id, kind, name, qualified_name, line_start, line_end, signature, parent_qualified)"
                                    " VALUES (?,?,?,?,?,?,?,?)",
                                    (file_id, "method", mname, qname, ms, me, sig, class_name)
                                )
                                sym_id_map[member.id] = cur2.lastrowid

        elif node.type == "function_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                fname = _node_text(name_node, src)
                line_start = node.start_point[0] + 1
                line_end = node.end_point[0] + 1
                params = node.child_by_field_name("parameters")
                sig = f"function {fname}({_node_text(params, src) if params else ''})"
                cur = conn.execute(
                    "INSERT OR REPLACE INTO symbols"
                    "(file_id, kind, name, qualified_name, line_start, line_end, signature, parent_qualified)"
                    " VALUES (?,?,?,?,?,?,?,?)",
                    (file_id, "function", fname, fname, line_start, line_end, sig, None)
                )
                sym_id_map[node.id] = cur.lastrowid

        elif node.type == "lexical_declaration":
            # `const x = () => {}` — capture the name
            for child in node.children:
                if child.type == "variable_declarator":
                    name_n = child.child_by_field_name("name")
                    if name_n:
                        nname = _node_text(name_n, src)
                        cur = conn.execute(
                            "INSERT OR REPLACE INTO symbols"
                            "(file_id, kind, name, qualified_name, line_start, line_end, signature, parent_qualified)"
                            " VALUES (?,?,?,?,?,?,?,?)",
                            (file_id, "const", nname, nname,
                             child.start_point[0] + 1, child.end_point[0] + 1,
                             f"const {nname}", None)
                        )
                        sym_id_map[child.id] = cur.lastrowid

        elif node.type == "import_statement":
            # `import { x, y } from "./foo"`
            src_text = None
            for child in node.children:
                if child.type == "string":
                    src_text = _node_text(child, src).strip("'\"")
                elif child.type == "import_clause":
                    for c2 in child.children:
                        if c2.type == "named_imports":
                            names = []
                            for spec in c2.children:
                                if spec.type == "import_specifier":
                                    nm = spec.child_by_field_name("name")
                                    if nm:
                                        names.append(_node_text(nm, src))
                            if src_text:
                                conn.execute(
                                    "INSERT INTO imports(file_id, src_module, imported_names, line) VALUES (?,?,?,?)",
                                    (file_id, src_text, ",".join(names),
                                     node.start_point[0] + 1),
                                )

    # Pass 2: call expressions
    for node in _walk(root):
        if node.type == "call_expression":
            func_node = node.child_by_field_name("function")
            if not func_node:
                continue
            func_text = _node_text(func_node, src).strip()
            src_sym_id = _ts_enclosing_symbol(node, sym_id_map)
            conn.execute(
                "INSERT INTO edges(src_file_id, src_symbol_id, dst_qualified_name, edge_type, line)"
                " VALUES (?,?,?,?,?)",
                (file_id, src_sym_id, func_text, "calls", node.start_point[0] + 1),
            )


def _ts_enclosing_symbol(node: ts.Node, sym_id_map: dict) -> int | None:
    parent = node.parent
    while parent:
        if parent.id in sym_id_map:
            return sym_id_map[parent.id]
        parent = parent.parent
    return None


# ─── file walking + main loop ──────────────────────────────────────────


def _walk_repo(repo_path: Path):
    """Yield (rel_path, abs_path) for indexable files, excluding noise dirs."""
    for dirpath, dirnames, filenames in os.walk(repo_path):
        # in-place prune
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIR_NAMES and not d.startswith(".")]
        for fn in filenames:
            if any(p in fn for p in EXCLUDE_FILE_PATTERNS):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext not in LANG_BY_EXT:
                continue
            ap = Path(dirpath) / fn
            try:
                if ap.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            rel = ap.relative_to(repo_path).as_posix()
            yield rel, ap


def index_repo(repo_name: str, repo_path: Path, db: Path, verbose: bool = True) -> dict:
    """Walk a single repo, index files. Returns {file_count, symbol_count}."""
    conn = sqlite3.connect(str(db), timeout=60)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    conn.execute(
        "INSERT OR IGNORE INTO repos(name, root_path) VALUES (?,?)",
        (repo_name, str(repo_path)),
    )
    repo_id = conn.execute(
        "SELECT id FROM repos WHERE name=?", (repo_name,)
    ).fetchone()[0]

    if not repo_path.exists():
        if verbose:
            print(f"  [{repo_name}] MISSING at {repo_path}")
        conn.execute("UPDATE repos SET indexed_at=? WHERE id=?",
                     (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), repo_id))
        conn.commit(); conn.close()
        return {"file_count": 0, "symbol_count": 0}

    # Existing sha256 cache (for incremental re-runs)
    existing = {}
    for row in conn.execute("SELECT rel_path, sha256 FROM files WHERE repo_id=?", (repo_id,)):
        existing[row[0]] = row[1]

    files_added = 0
    files_updated = 0
    files_skipped = 0
    symbols_added = 0
    edges_added = 0
    imports_added = 0
    started = time.time()

    for rel_path, abs_path in _walk_repo(repo_path):
        try:
            content = abs_path.read_bytes()
        except (OSError, PermissionError):
            continue
        if not content:
            continue
        sha = _hash(content)
        if existing.get(rel_path) == sha:
            files_skipped += 1
            continue

        ext = abs_path.suffix.lower()
        language = LANG_BY_EXT[ext]
        st = abs_path.stat()
        # Upsert file row
        if rel_path in existing:
            cur = conn.execute(
                "UPDATE files SET language=?, size_bytes=?, mtime=?, sha256=?, symbol_count=0"
                " WHERE repo_id=? AND rel_path=?",
                (language, st.st_size, int(st.st_mtime), sha, repo_id, rel_path),
            )
            file_id = conn.execute(
                "SELECT id FROM files WHERE repo_id=? AND rel_path=?",
                (repo_id, rel_path),
            ).fetchone()[0]
            # Wipe stale symbols/edges/imports
            conn.execute("DELETE FROM symbols WHERE file_id=?", (file_id,))
            conn.execute("DELETE FROM edges WHERE src_file_id=?", (file_id,))
            conn.execute("DELETE FROM imports WHERE file_id=?", (file_id,))
            files_updated += 1
        else:
            cur = conn.execute(
                "INSERT INTO files(repo_id, rel_path, language, size_bytes, mtime, sha256)"
                " VALUES (?,?,?,?,?,?)",
                (repo_id, rel_path, language, st.st_size, int(st.st_mtime), sha),
            )
            file_id = cur.lastrowid
            files_added += 1

        # Parse + extract
        try:
            parser = _parser(language)
            tree = parser.parse(content)
            root = tree.root_node
            before_sym = conn.execute("SELECT COUNT(*) FROM symbols").fetchone()[0]
            before_edge = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
            before_imp = conn.execute("SELECT COUNT(*) FROM imports").fetchone()[0]
            if language == "python":
                _py_extract(file_id, content, root, conn)
            else:
                _ts_extract(file_id, content, root, conn)
            after_sym = conn.execute("SELECT COUNT(*) FROM symbols").fetchone()[0]
            after_edge = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
            after_imp = conn.execute("SELECT COUNT(*) FROM imports").fetchone()[0]
            symbols_added += after_sym - before_sym
            edges_added += after_edge - before_edge
            imports_added += after_imp - before_imp
            sym_count = conn.execute(
                "SELECT COUNT(*) FROM symbols WHERE file_id=?", (file_id,)
            ).fetchone()[0]
            conn.execute("UPDATE files SET symbol_count=? WHERE id=?", (sym_count, file_id))
        except Exception as e:
            if verbose:
                print(f"  parse err {rel_path}: {e!r}")
            continue

        # batched commit
        if (files_added + files_updated) % 200 == 0:
            conn.commit()
            if verbose:
                elapsed = time.time() - started
                rate = (files_added + files_updated) / max(elapsed, 0.001)
                print(f"  [{repo_name}] {files_added+files_updated} files "
                      f"({rate:.1f}/s) — {symbols_added} sym, {edges_added} edges, {imports_added} imports")

    conn.execute("UPDATE repos SET indexed_at=?, file_count=?, symbol_count=? WHERE id=?",
                 (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  files_added + files_updated + files_skipped, symbols_added, repo_id))
    conn.commit()
    conn.close()
    elapsed = time.time() - started
    return {
        "added": files_added, "updated": files_updated, "skipped": files_skipped,
        "symbols": symbols_added, "edges": edges_added, "imports": imports_added,
        "elapsed_s": round(elapsed, 1),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--repo", action="append",
                        help="repo name(s) to index (repeatable); default = all 7")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    repo_names = args.repo or DEFAULT_REPOS

    # ensure schema
    from schema import init_schema, connect as schema_connect
    sc = schema_connect(Path(args.db))
    init_schema(sc)
    sc.close()

    print(f"# codegraph indexer — db={args.db}")
    print(f"# repos: {', '.join(repo_names)}")
    print(f"# exclusions: {sorted(EXCLUDE_DIR_NAMES)}")
    print()

    grand = {"files": 0, "symbols": 0, "edges": 0, "imports": 0, "t": 0.0}
    for rn in repo_names:
        rp = ROOT / rn
        print(f"[{rn}]  root={rp}")
        r = index_repo(rn, rp, Path(args.db), verbose=not args.quiet)
        msg = (f"  +{r.get('added',0)} new / ~{r.get('updated',0)} upd / "
               f"={r.get('skipped',0)} cached   "
               f"sym={r.get('symbols',0)}  edges={r.get('edges',0)}  "
               f"imports={r.get('imports',0)}   {r.get('elapsed_s','?')}s")
        print(msg)
        grand["files"] += r.get("added", 0) + r.get("updated", 0)
        grand["symbols"] += r.get("symbols", 0)
        grand["edges"] += r.get("edges", 0)
        grand["imports"] += r.get("imports", 0)
        grand["t"] += r.get("elapsed_s", 0.0)

    print()
    print(f"# total  files_touched={grand['files']}  symbols={grand['symbols']}  "
          f"edges={grand['edges']}  imports={grand['imports']}  time={grand['t']:.1f}s")


if __name__ == "__main__":
    main()