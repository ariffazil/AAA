#!/usr/bin/env python3
"""
token-bank-aggregate.py — Federation Token Spend Aggregation View v2
═══════════════════════════════════════════════════════════════════════
Query token_bank.db on the LOCAL node. Run this script ON each node,
then aggregate the JSON outputs externally.

Why v2: v1 used SSH recursion which broke self-referencing (FORGE→FORGE
on port 22888 didn't resolve). Simpler: run locally, output JSON, aggregate
downstream.

Usage:
  python3 token-bank-aggregate.py [--output json|table] [--days 30]

Output:
  Per-route spend breakdown + node total.
"""

import sqlite3
import sys
import json
from pathlib import Path

DEFAULT_DB_PATH = "/root/.local/share/arifos/token_bank.db"


def query_local(db_path: str = DEFAULT_DB_PATH, days: int = 30) -> dict:
    """Query token_bank.db on local node."""
    if not Path(db_path).exists():
        return {"error": f"DB not found: {db_path}", "node": "local"}

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Discover schema
    cursor.execute("PRAGMA table_info(token_bank_spend)")
    columns = [row[1] for row in cursor.fetchall()]

    if not columns:
        conn.close()
        return {"error": "token_bank_spend table empty or missing", "node": "local"}

    # Find relevant columns
    route_col = next((c for c in columns if c.lower() in ("route", "model_id", "provider_name")), "model_id")
    cost_col = next((c for c in columns if "cost" in c.lower()), None)
    in_col = next((c for c in columns if c.lower() in ("tokens_in", "input_tokens")), None)
    out_col = next((c for c in columns if c.lower() in ("tokens_out", "output_tokens")), None)
    ts_col = next((c for c in columns if "time" in c.lower() or "called" in c.lower() or "date" in c.lower()), None)

    # Build query
    select_parts = [f"{route_col} as route", "COUNT(*) as call_count"]
    if in_col:
        select_parts.append(f"SUM({in_col}) as total_input")
    if out_col:
        select_parts.append(f"SUM({out_col}) as total_output")
    if cost_col:
        select_parts.append(f"SUM({cost_col}) as total_cost")

    where = ""
    if ts_col:
        where = f"WHERE {ts_col} >= datetime('now', '-{days} days')"

    sql = f"SELECT {', '.join(select_parts)} FROM token_bank_spend {where} GROUP BY {route_col} ORDER BY total_cost DESC LIMIT 20"

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        conn.close()
        return {"error": f"Query failed: {e}", "schema": columns, "node": "local"}

    conn.close()

    routes = []
    total_cost = 0.0
    total_calls = 0

    for row in rows:
        route = row[0]
        calls = row[1]
        in_tok = row[2] if in_col else 0
        out_tok = row[3] if out_col and in_col else (row[2] if out_col and not in_col else 0)
        cost = row[4] if cost_col and in_col and out_col else (
               row[3] if cost_col and (in_col or out_col) else
               row[2] if cost_col else 0.0)

        routes.append({
            "route": route,
            "calls": calls,
            "input_tokens": in_tok or 0,
            "output_tokens": out_tok or 0,
            "cost_usd": float(cost or 0.0),
        })
        total_cost += float(cost or 0.0)
        total_calls += calls

    return {
        "node": "local",
        "db_path": db_path,
        "schema": columns,
        "days": days,
        "routes": routes,
        "total_cost": total_cost,
        "total_calls": total_calls,
    }


def render_table(data: dict):
    """Render data as human-readable table."""
    print("=" * 70)
    days = data.get('days', 30)
    print(f"FEDERATION TOKEN SPEND — Last {days} Days")
    print(f"DB: {data.get('db_path', '?')}")
    schema = data.get('schema', [])
    if schema:
        print(f"Schema columns: {', '.join(schema)}")
    print("=" * 70)

    if "error" in data:
        print(f"❌ {data['error']}")
        return

    if not data["routes"]:
        print("(no spend data)")
        print("=" * 70)
        print(f"Node total: 0 calls, $0.0000")
        return

    for route in data["routes"][:10]:
        print(f"  {route['route']:40s}  {route['calls']:5d} calls  ${route['cost_usd']:8.4f}")

    print(f"  {'─' * 60}")
    print(f"Node total: {data['total_calls']} calls, ${data['total_cost']:.4f}")
    print("=" * 70)


def main():
    output_format = "table"
    days = 30
    db_path = DEFAULT_DB_PATH

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_format = args[i + 1]
            i += 2
        elif args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1])
            i += 2
        elif args[i] == "--db-path" and i + 1 < len(args):
            db_path = args[i + 1]
            i += 2
        else:
            i += 1

    data = query_local(db_path, days)

    if output_format == "json":
        print(json.dumps(data, indent=2))
    else:
        render_table(data)


if __name__ == "__main__":
    main()
