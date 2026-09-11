#!/usr/bin/env python3
"""
DuckDB Analytical Enclave MCP Server (Canary P1-A)
Provides governed, in-process columnar SQL queries over approved datasets
without dumping raw telemetry into agent context.
"""

import sys
import os
import time
import json
import duckdb
from datetime import date, datetime, timezone
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP

from policy import (
    APPROVED_ROOTS,
    DENIED_ROOTS,
    MAX_ROWS,
    MAX_BYTES,
    QUERY_TIMEOUT_SECONDS,
    EnclaveSecurityViolation,
    validate_sql,
    validate_paths,
    record_audit
)

# Initialize FastMCP
mcp = FastMCP("duckdb-enclave")


def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return str(obj)


def get_db_connection():
    """Create isolated in-memory duckdb connection with external extensions locked down."""
    return duckdb.connect(
        database=":memory:",
        config={
            "autoload_known_extensions": False,
            "autoinstall_known_extensions": False,
            "max_memory": "512MB",
            "threads": 4
        }
    )


@mcp.tool()
def duckdb_query(
    query: str,
    dataset_id: str = "adhoc",
    agent_id: str = "geox",
    role: str = "researcher"
) -> str:
    """
    Execute a bounded, read-only SQL query over approved datasets (.parquet, .csv)
    in /data/geox/derived, /data/aaa/audit, /data/aaa/ledgers, /data/aaa/log-exports.
    
    Only SELECT, DESCRIBE, EXPLAIN, SHOW queries are allowed.
    All operations outside approved roots are strictly blocked.
    Results are capped at 500 rows and 1MB.
    """
    start_time = time.perf_counter()

    try:
        # Step 1: SQL Keyword & Structure Validation
        validate_sql(query)

        # Step 2: Path Containment Validation
        validate_paths(query)

        # Step 3: Execution in sandboxed memory DuckDB
        con = get_db_connection()
        rel = con.sql(query)
        
        # Extract columns
        columns = rel.columns

        # Fetch up to MAX_ROWS + 1 to detect truncation
        raw_rows = rel.fetchmany(MAX_ROWS + 1)
        truncated = len(raw_rows) > MAX_ROWS
        rows = raw_rows[:MAX_ROWS]

        # Convert row tuples to JSON serializable objects
        formatted_rows = []
        for r in rows:
            formatted_rows.append([_json_serial(val) if val is not None else None for val in r])

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        result_payload = {
            "columns": columns,
            "row_count": len(formatted_rows),
            "truncated": truncated,
            "max_rows_limit": MAX_ROWS,
            "rows": formatted_rows
        }

        # Check byte limit
        json_output = json.dumps(result_payload, default=_json_serial)
        if len(json_output.encode("utf-8")) > MAX_BYTES:
            raise EnclaveSecurityViolation(
                f"Result payload size ({len(json_output)} bytes) exceeded enclave limit ({MAX_BYTES} bytes)."
            )

        # Record audit log
        audit_event = record_audit(
            agent_id=agent_id,
            role=role,
            dataset_id=dataset_id,
            query=query,
            rows_returned=len(formatted_rows),
            elapsed_ms=elapsed_ms,
            status="SUCCESS",
            result_data=result_payload
        )

        response = {
            "status": "SUCCESS",
            "enclave": "duckdb_analytical_canary_v1",
            "query_hash": audit_event["query_hash"],
            "result_hash": audit_event["result_hash"],
            "elapsed_ms": audit_event["elapsed_ms"],
            "data": result_payload
        }

        return json.dumps(response, indent=2)

    except EnclaveSecurityViolation as esv:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        record_audit(
            agent_id=agent_id,
            role=role,
            dataset_id=dataset_id,
            query=query,
            rows_returned=0,
            elapsed_ms=elapsed_ms,
            status="SECURITY_DENIED",
            error=str(esv)
        )
        return json.dumps({
            "status": "DENIED",
            "error_class": "ENCLAVE_SECURITY_VIOLATION",
            "message": str(esv)
        }, indent=2)

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        record_audit(
            agent_id=agent_id,
            role=role,
            dataset_id=dataset_id,
            query=query,
            rows_returned=0,
            elapsed_ms=elapsed_ms,
            status="QUERY_ERROR",
            error=str(exc)
        )
        return json.dumps({
            "status": "ERROR",
            "error_class": "DUCKDB_EXECUTION_ERROR",
            "message": str(exc)
        }, indent=2)


@mcp.tool()
def duckdb_describe(file_path: str, agent_id: str = "geox") -> str:
    """
    Inspect schema, data types, and column metadata of a dataset within approved roots.
    """
    start_time = time.perf_counter()
    try:
        # Validate path
        abs_path = os.path.realpath(os.path.abspath(file_path))
        for denied in DENIED_ROOTS:
            if abs_path == denied or abs_path.startswith(denied + "/"):
                raise EnclaveSecurityViolation(f"Access Denied: Path '{file_path}' resolves inside forbidden root '{denied}'.")

        is_approved = any(abs_path == app or abs_path.startswith(app + "/") for app in APPROVED_ROOTS)
        if not is_approved:
            raise EnclaveSecurityViolation(f"Access Denied: Path '{file_path}' outside approved roots.")

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Dataset file '{file_path}' does not exist.")

        con = get_db_connection()
        if abs_path.endswith(".parquet"):
            rel = con.sql(f"DESCRIBE SELECT * FROM read_parquet('{abs_path}');")
        elif abs_path.endswith(".csv"):
            rel = con.sql(f"DESCRIBE SELECT * FROM read_csv('{abs_path}');")
        else:
            rel = con.sql(f"DESCRIBE SELECT * FROM '{abs_path}';")

        columns = rel.columns
        rows = rel.fetchall()

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        schema_info = [dict(zip(columns, r)) for r in rows]

        record_audit(
            agent_id=agent_id,
            role="researcher",
            dataset_id=file_path,
            query=f"DESCRIBE {file_path}",
            rows_returned=len(schema_info),
            elapsed_ms=elapsed_ms,
            status="SUCCESS",
            result_data=schema_info
        )

        return json.dumps({
            "status": "SUCCESS",
            "dataset": file_path,
            "schema": schema_info
        }, indent=2, default=_json_serial)

    except Exception as exc:
        return json.dumps({
            "status": "ERROR",
            "error_class": "DESCRIBE_FAILED",
            "message": str(exc)
        }, indent=2)


@mcp.tool()
def duckdb_list_approved_datasets() -> str:
    """
    List all datasets currently available across approved analytical enclave directories.
    """
    datasets = []
    for root in APPROVED_ROOTS:
        if os.path.exists(root):
            for dirpath, _, filenames in os.walk(root):
                for f in filenames:
                    if f.endswith((".parquet", ".csv", ".json", ".jsonl", ".las")):
                        full_path = os.path.join(dirpath, f)
                        try:
                            stat = os.stat(full_path)
                            datasets.append({
                                "file_path": full_path,
                                "size_bytes": stat.st_size,
                                "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                                "format": f.split(".")[-1].lower()
                            })
                        except Exception:
                            pass

    return json.dumps({
        "status": "SUCCESS",
        "approved_roots": APPROVED_ROOTS,
        "dataset_count": len(datasets),
        "datasets": datasets
    }, indent=2)


if __name__ == "__main__":
    # Support stdio (default) or http flag
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 18086
        mcp.run(transport="http", host="127.0.0.1", port=port)
    else:
        mcp.run(transport="stdio")
