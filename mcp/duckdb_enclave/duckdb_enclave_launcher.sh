#!/usr/bin/env bash
set -euo pipefail
cd /root/AAA/mcp/duckdb_enclave
exec python3 server.py "$@"
