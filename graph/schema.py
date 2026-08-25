#!/usr/bin/env python3
"""
schema.py — SQLite schema for codegraph.db (arifOS federation code graph).

Tables:
  repos   — registered source roots (e.g. arifOS, A-FORGE)
  files   — every indexed source file (path + language + content hash)
  symbols — definitions (function, class, method, const, interface)
  imports — file-level import statements (src_module + line)
  edges   — symbol → symbol references (calls, references, extends, implements)

Identity rules:
  - file identity = (repo_id, rel_path)
  - symbol identity = (file_id, qualified_name) — qualified_name is dotted,
    e.g. "ClassName.method_name" or "free_function" or "ClassName.NestedClass"
  - cross-file references go via name-match at query time (edges stored as
    intra-file + intra-class resolution; cross-file = lazy lookup)

DITEMPA BUKAN DIBERI ⚒️ — graph for I-ARIF and forge blast-radius.
"""
from __future__ import annotations
import sqlite3, sys
from pathlib import Path

DEFAULT_DB = Path("/root/AAA/graph/codegraph.db")
SCHEMA_VERSION = 1

DDL = """
CREATE TABLE IF NOT EXISTS meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS repos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  root_path TEXT NOT NULL,
  indexed_at TEXT,
  file_count INTEGER DEFAULT 0,
  symbol_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  repo_id INTEGER NOT NULL,
  rel_path TEXT NOT NULL,
  language TEXT,
  size_bytes INTEGER,
  mtime INTEGER,
  sha256 TEXT,
  symbol_count INTEGER DEFAULT 0,
  UNIQUE(repo_id, rel_path),
  FOREIGN KEY (repo_id) REFERENCES repos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_files_repo ON files(repo_id);
CREATE INDEX IF NOT EXISTS idx_files_lang ON files(language);

CREATE TABLE IF NOT EXISTS symbols (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  file_id INTEGER NOT NULL,
  kind TEXT NOT NULL,
  name TEXT NOT NULL,
  qualified_name TEXT NOT NULL,
  line_start INTEGER,
  line_end INTEGER,
  signature TEXT,
  docstring TEXT,
  parent_qualified TEXT,
  UNIQUE(file_id, qualified_name),
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_symbols_name ON symbols(name);
CREATE INDEX IF NOT EXISTS idx_symbols_qname ON symbols(qualified_name);
CREATE INDEX IF NOT EXISTS idx_symbols_kind ON symbols(kind);
CREATE INDEX IF NOT EXISTS idx_symbols_file ON symbols(file_id);
CREATE INDEX IF NOT EXISTS idx_symbols_parent ON symbols(parent_qualified);

CREATE TABLE IF NOT EXISTS imports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  file_id INTEGER NOT NULL,
  src_module TEXT NOT NULL,
  imported_names TEXT,
  line INTEGER,
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_imports_file ON imports(file_id);
CREATE INDEX IF NOT EXISTS idx_imports_module ON imports(src_module);

CREATE TABLE IF NOT EXISTS edges (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  src_file_id INTEGER NOT NULL,
  src_symbol_id INTEGER,
  dst_qualified_name TEXT NOT NULL,
  edge_type TEXT NOT NULL,
  line INTEGER,
  resolved_dst_symbol_id INTEGER,
  FOREIGN KEY (src_file_id) REFERENCES files(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_edges_src_file ON edges(src_file_id);
CREATE INDEX IF NOT EXISTS idx_edges_src_sym ON edges(src_symbol_id);
CREATE INDEX IF NOT EXISTS idx_edges_dst_name ON edges(dst_qualified_name);
CREATE INDEX IF NOT EXISTS idx_edges_dst_sym ON edges(resolved_dst_symbol_id);
CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(edge_type);
"""


def connect(db_path: Path = DEFAULT_DB) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), timeout=30)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(DDL)
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', ?)",
        (str(SCHEMA_VERSION),),
    )
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('created_at', "
        "strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))"
    )
    conn.commit()


if __name__ == "__main__":
    db = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DB
    conn = connect(db)
    init_schema(conn)
    print(f"schema initialised at {db}")
    for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall():
        print(f"  table: {row[0]}")
    conn.close()