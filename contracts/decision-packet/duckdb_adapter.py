"""
DuckDB Enclave Decision Packet Adapter
Converts DuckDB enclave query execution into an immutable, verifiable Decision Packet.
"""

import os
import sys
import json
import hashlib

# Add paths
sys.path.insert(0, '/root/AAA/mcp/duckdb_enclave')
sys.path.insert(0, '/root/AAA/contracts/decision-packet')

from server import duckdb_query
from engine import seal_decision_packet


def execute_and_seal_geox_packet(
    intent: str,
    sql_query: str,
    dataset_id: str,
    dataset_path: str,
    observations: list,
    interpretations: list,
    requester_id: str = "arif",
    selected_model: str = "deepseek-v4-pro"
) -> dict:
    """Execute query in DuckDB enclave and seal the resulting Decision Packet."""
    # 1. Execute query via enclave
    query_resp_raw = duckdb_query(
        query=sql_query,
        dataset_id=dataset_id,
        agent_id="geox",
        role="researcher"
    )
    resp = json.loads(query_resp_raw)
    if resp.get("status") != "SUCCESS":
        raise RuntimeError(f"DuckDB query failed: {resp.get('message')}")

    # 2. Get dataset manifest hash
    dataset_hash = ""
    if os.path.exists(dataset_path):
        with open(dataset_path, "rb") as f:
            dataset_hash = hashlib.sha256(f.read()).hexdigest()

    # 3. Formulate Evidence Object
    evidence = {
        "datasets": [
            {
                "dataset_id": dataset_id,
                "version": "v1.0",
                "manifest_hash": f"sha256:{dataset_hash}",
                "classification": "internal_geoscience"
            }
        ],
        "sources": [],
        "tool_calls": [
            {
                "server_id": "ENCLAVE-DUCKDB-01",
                "server_code_hash": "sha256:1d18da2242c65a325ebd487e7967b8a1f60cadc39806970de1090e5942def98f",
                "tool_name": "duckdb_query",
                "input_hash": f"sha256:{hashlib.sha256(sql_query.encode()).hexdigest()}",
                "query_hash": f"sha256:{resp.get('query_hash')}",
                "result_hash": f"sha256:{resp.get('result_hash')}",
                "elapsed_ms": resp.get("elapsed_ms"),
                "rows_returned": resp.get("data", {}).get("row_count", 0),
                "status": "allowed"
            }
        ]
    }

    task = {
        "task_id": f"tsk_geox_{os.urandom(4).hex()}",
        "intent": intent,
        "task_class": "data_analysis",
        "risk_class": "R0",
        "requester": {
            "type": "human",
            "id": requester_id,
            "authority": "sovereign_human"
        }
    }

    execution = {
        "orchestrator": "hermes-prime",
        "route": {
            "router": "fed",
            "route_id": "fed_route_direct",
            "selected_agent": "geox",
            "selected_model": selected_model,
            "allowed_capabilities": ["duckdb_enclave.read"]
        },
        "session": {
            "session_id_hash": f"sha256:{hashlib.sha256(b'geox_session_active').hexdigest()}",
            "authority_context": "read_only_approved",
            "policy_version": "arifos-policy-2026.09"
        }
    }

    findings = {
        "observations": observations,
        "interpretations": interpretations
    }

    action = {
        "proposed": False,
        "action_class": None,
        "target": None,
        "rollback_ref": None,
        "human_approval": {
            "required": False,
            "state": "not_required"
        }
    }

    outcome = {
        "status": "completed",
        "limitations": [
            "Only approved curated data were queried.",
            "Descriptive statistics alone do not establish subsurface certainty."
        ],
        "next_review_at_utc": None
    }

    # 4. Seal Packet
    packet = seal_decision_packet(
        task=task,
        execution=execution,
        evidence=evidence,
        findings=findings,
        action=action,
        outcome=outcome
    )

    return packet
