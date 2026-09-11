"""
DuckDB Analytical Enclave Security Policy Engine
Governs queries, path containment, and audit logging per P1-A specification.
"""

import os
import re
import json
import time
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

# Approved directory roots for query access
APPROVED_ROOTS = [
    "/data/aaa/audit",
    "/data/aaa/ledgers",
    "/data/geox/derived",
    "/data/aaa/log-exports",
]

# Strictly denied roots
DENIED_ROOTS = [
    "/root",
    "/home",
    "/etc",
    "/proc",
    "/sys",
    "/var/run/docker.sock",
    "/run/secrets",
    "/var",
    "/opt",
]

# Query limitations
MAX_ROWS = 500
MAX_BYTES = 1048576  # 1 MB
QUERY_TIMEOUT_SECONDS = 30
AUDIT_LOG_FILE = "/data/aaa/audit/duckdb_enclave_audit.jsonl"

# Allowed statement prefixes (case-insensitive)
ALLOWED_PREFIXES = ("SELECT", "DESCRIBE", "EXPLAIN", "SHOW", "PRAGMA", "WITH")

# Explicitly forbidden SQL tokens/statements
FORBIDDEN_KEYWORDS = {
    "ATTACH", "DETACH", "IMPORT", "EXPORT", "COPY", "INSTALL", "LOAD",
    "CREATE", "DROP", "ALTER", "INSERT", "UPDATE", "DELETE", "CALL",
    "CHECKPOINT", "VACUUM", "SET", "RESET", "CREATE_SECRET", "USE"
}

FORBIDDEN_SCHEMES = ("http://", "https://", "s3://", "hf://", "gcs://", "ftp://")


class EnclaveSecurityViolation(Exception):
    """Raised when a query violates security or sandbox policy."""
    pass


def validate_sql(query: str) -> None:
    """Validate that SQL query contains only allowed read-only operations."""
    cleaned = query.strip()
    if not cleaned:
        raise EnclaveSecurityViolation("Empty query is not allowed.")

    # Remove comments
    cleaned = re.sub(r"^/\*.*?\*/\s*", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"^--.*?\n\s*", "", cleaned)
    cleaned = cleaned.strip()

    first_word = cleaned.split()[0].upper()
    if first_word not in ALLOWED_PREFIXES:
        raise EnclaveSecurityViolation(
            f"Command '{first_word}' is forbidden. Only {ALLOWED_PREFIXES} queries are permitted."
        )

    # Check for forbidden keywords anywhere as distinct words
    tokens = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", cleaned.upper())
    for token in tokens:
        if token in FORBIDDEN_KEYWORDS:
            if token in {"ATTACH", "DETACH", "INSTALL", "LOAD", "COPY", "CREATE", "DROP", "ALTER", "INSERT", "UPDATE", "DELETE", "CREATE_SECRET"}:
                raise EnclaveSecurityViolation(f"Operation '{token}' is forbidden in read-only analytical enclave.")

    # Check for network URLs
    for scheme in FORBIDDEN_SCHEMES:
        if scheme in cleaned.lower():
            raise EnclaveSecurityViolation(f"Network scheme '{scheme}' is forbidden in local analytical enclave.")


def validate_paths(query: str) -> List[str]:
    """Extract and validate all file paths referenced in the query."""
    literals = re.findall(r"['\"]([^'\"]+)['\"]", query)
    validated_paths = []

    for lit in literals:
        if "/" in lit or lit.endswith((".parquet", ".csv", ".json", ".jsonl", ".las", ".tsv", ".txt")):
            abs_path = os.path.realpath(os.path.abspath(lit))

            # Check denied roots
            for denied in DENIED_ROOTS:
                if abs_path == denied or abs_path.startswith(denied + "/"):
                    raise EnclaveSecurityViolation(
                        f"Access Denied: Path '{lit}' resolves inside forbidden root '{denied}'."
                    )

            # Check approved roots
            is_approved = any(
                abs_path == app or abs_path.startswith(app + "/")
                for app in APPROVED_ROOTS
            )

            if not is_approved:
                raise EnclaveSecurityViolation(
                    f"Access Denied: Path '{lit}' is outside approved enclave roots {APPROVED_ROOTS}."
                )

            validated_paths.append(abs_path)

    return validated_paths


def record_audit(
    agent_id: str,
    role: str,
    dataset_id: str,
    query: str,
    rows_returned: int,
    elapsed_ms: float,
    status: str,
    error: str = None,
    result_data: Any = None
) -> Dict[str, Any]:
    """Record an immutable audit event for every query invocation."""
    query_hash = hashlib.sha256(query.strip().encode()).hexdigest()
    
    result_hash = None
    if result_data is not None:
        result_bytes = json.dumps(result_data, sort_keys=True).encode()
        result_hash = hashlib.sha256(result_bytes).hexdigest()

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_id,
        "role": role,
        "dataset_id": dataset_id or "adhoc",
        "query_hash": query_hash,
        "result_hash": result_hash,
        "rows_returned": rows_returned,
        "elapsed_ms": round(elapsed_ms, 2),
        "status": status,
        "error": error
    }

    try:
        os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
    except Exception as e:
        import sys
        print(f"[AUDIT FAILURE] Failed to write audit event: {e}", file=sys.stderr)

    return event
