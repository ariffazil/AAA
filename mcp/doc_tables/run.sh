#!/usr/bin/env bash
# doc-tables-mcp launcher — always the arifOS venv (never system python).
set -euo pipefail
VENV_PY=/opt/arifos/venv/bin/python
DIR=/root/AAA/mcp/doc_tables
export DOC_TABLES_HOST="${DOC_TABLES_HOST:-127.0.0.1}"
export DOC_TABLES_PORT="${DOC_TABLES_PORT:-38500}"
export DOC_TABLES_TRANSPORT="${DOC_TABLES_TRANSPORT:-http}"
exec "$VENV_PY" "$DIR/server.py"
