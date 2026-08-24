---
name: duckdb-analytics-engine
description: In-process columnar SQL analytics engine over Parquet, CSV, JSONL, and well log (.las) files using DuckDB and Polars.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# DuckDB & Polars High-Performance Analytics Skill (`duckdb-analytics-engine`)

Enables AI agents to execute sub-second columnar SQL queries over large local datasets (well logs, financial ledgers, web access logs, Parquet files) directly in memory with zero database server overhead.

## Execution Patterns

### 1. Querying Local Parquet / CSV / JSONL via DuckDB
```python
import duckdb

# Query multiple Parquet/CSV files directly using SQL
query = """
SELECT 
    formation_name,
    AVG(gamma_ray) AS avg_gr,
    MAX(resistivity) AS max_res,
    COUNT(*) AS sample_count
FROM read_parquet('data/well_logs/*.parquet')
WHERE depth_m BETWEEN 2000 AND 3500
GROUP BY formation_name
ORDER BY avg_gr ASC;
"""

df = duckdb.query(query).to_df()
print(df)
```

### 2. High-Speed LAS / Well Log Batch Summaries
```python
import duckdb

# Execute direct SQL aggregations over exported CSV/JSON log data
res = duckdb.sql("""
    SELECT 
        COUNT(*) as total_samples,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gr) as median_gr,
        SUM(CASE WHEN gr < 45 AND res > 20 THEN 0.15 ELSE 0 END) as estimated_pay_m
    FROM 'well_log_export.csv'
""")
res.show()
```

---

## Best Practices for Federation Agents

1. **Sub-second Performance**: Use `duckdb-analytics-engine` instead of raw Python `for` loops when parsing tabular files > 5MB.
2. **Zero Setup Overhead**: DuckDB runs in-process without requiring external database services or network ports.
