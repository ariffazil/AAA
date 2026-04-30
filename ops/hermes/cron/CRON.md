# CRON — Approved Scheduled Jobs Catalog
# DITEMPA BUKAN DIBERI — Forged, Not Given.

## Cron Design Rules

1. **Fresh sessions**: Cron runs in isolated fresh sessions — no ambient memory, no prior context
2. **Self-contained prompts**: Every cron prompt must contain everything the agent needs
3. **Workdir jobs serialize**: Jobs with `workdir` run sequentially (cwd is process-global)
4. **No-write lane**: Jobs WITHOUT `workdir` run in parallel — use for low-risk monitoring
5. **Never mutate state**: Cron jobs may NOT write to Vault-999, delete files, or edit configs
6. **Silent on success**: Use `[SILENT]` prefix for healthy-state outputs

## Three Job Classes

| Class | Description | Examples |
|-------|-------------|---------|
| **observe** | Monitor and log, silent unless fail | health checks, drift audits |
| **summarize** | Aggregate and report | daily briefs, metrics rollups |
| **alert** | Report anomalous conditions | error rate spikes, security events |

---

## Approved Cron Jobs

### observe — Health Monitoring

#### mcp-health-check
```
schedule: "every 2h"
class: observe
workdir: ""
delivery: local
prompt: |
  Check if the following services are responding:
  - arifOS MCP: curl -s http://127.0.0.1:8080/health
  - GEOX MCP: curl -s http://127.0.0.1:8081/health
  Report HTTP status and response time for each.
  If any service returns non-200, report the issue.
  If all healthy, respond with only [SILENT].
skills: []
```

#### hermes-gateway-health
```
schedule: "every 5m"
class: observe
workdir: ""
delivery: local
prompt: |
  Check if Hermes gateway process is running: pgrep -f "openclaw-gateway" | wc -l
  If count > 0, respond with [SILENT].
  If count == 0, report "Hermes gateway DOWN — requires restart".
skills: []
```

#### repo-drift-audit
```
schedule: "every 1d at 03:00"
class: observe
workdir: /root
delivery: local
prompt: |
  Run: git status --porcelain in /root/arifOS, /root/geox, /root/AAA
  Report any uncommitted changes (file names only, no content).
  If clean, respond with [SILENT].
skills: []
```

---

### summarize — Reporting

#### daily-governance-brief
```
schedule: "every 1d at 09:00"
class: summarize
workdir: ""
delivery: origin
prompt: |
  Read /root/VAULT999/outcomes.jsonl from the last 24 hours.
  Summarize:
  1. Number of tool calls by risk tier (T0/T1/T2/T3)
  2. Any F01-F13 floor violations logged
  3. Any blocked tools (888_HOLD denials)
  4. Number of sessions created
  Format as a clean markdown table. Keep under 500 words.
skills: []
```

#### morning-status-brief
```
schedule: "every 1d at 08:00"
class: summarize
workdir: ""
delivery: origin
prompt: |
  Check the following and summarize in 3-5 sentences:
  1. arifOS MCP health (curl /health)
  2. Hermes gateway process count
  3. Docker container status (docker ps --format table)
  4. Disk usage (df -h / | tail -1)
  5. Memory usage (free -h)
  End with current constitution floor status (which F1-F13 are active).
skills: []
```

---

### alert — Anomaly Reporting

#### vault-integrity-alert
```
schedule: "every 6h"
class: alert
workdir: ""
delivery: origin
prompt: |
  Check /root/VAULT999/outcomes.jsonl for anomalies:
  1. Any entries with outcome="blocked" in the last 6h
  2. Any F13 SOVEREIGN flags
  3. Any T3 risk tools that executed without 888_HOLD
  If anomalies found, report full details.
  If clean, respond with [SILENT].
skills: []
```

---

## Forbidden Cron Jobs

These job types are **NEVER allowed** in AAA:

| Forbidden | Reason |
|-----------|--------|
| Anything writing to Vault-999 directly | Vault entries must go through MCP |
| Anything deleting files | Too destructive for autonomous cron |
| Anything editing agent configs | Config changes require human review |
| Anything creating downstream cron jobs | Hermes blocks recursive cron internally |
| Anything running `rm -rf` | F01 violation |
| Anything with `DROP TABLE` or `DELETE FROM` | F01 violation |

---

## Cron Delivery Targets

| Target | When to Use |
|--------|-------------|
| `origin` | Direct reply to the cron creator |
| `local` | File output to `~/.hermes/cron/output/` only |
| `telegram` | Push to configured Telegram channel |
| `discord` | Push to configured Discord channel |

---

## Adding New Cron Jobs

1. Draft the job prompt following the template above
2. Classify as observe / summarize / alert
3. Verify it does NOT fall into the Forbidden list
4. Submit via Hermes cron tool: `cronjob(action="create", ...)`
5. Log the new job in this catalog with schedule and classification
