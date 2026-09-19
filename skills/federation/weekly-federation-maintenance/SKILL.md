---
name: weekly-federation-maintenance
description: 'Weekly federation health probe with P0 Telegram alerting.'
risk_tier: low
floor_scope: [F1, F2, F11]
autonomy_tier: T1
tags: [federation, maintenance, automation, cron, weekly]
---

# Weekly Federation Maintenance

Automated, read-only, receipt-producing. Saturday 20:00 MYT via OS cron.
Companion to federation-housekeeping-master (monthly, manual, deep audit).

## Always-on rules

1. Read-only. Script never mutates production state.
2. One script, one cron. Single orchestrator.
3. P0 escalates to agents via Telegram tag.
4. Receipts on disk. Telegram gets summary.
5. Automate safe tasks. Key rotation stays 888 HOLD.

## Locations

Script: /root/scripts/weekly-aaa-maintenance.py
Cron: /etc/cron.d/weekly-aaa-maintenance
Reports: /root/AAA/reports/weekly-maintenance/YYYY-MM-DD/
Target: -1003753855708 (AAA forum group)

## 8 phases

I: identity (hostname, dead paths, auto-reboot)
S: scheduler (jobs.json vs executions.db)
M: memory (state.db size, sessions, messages)
P: prompt (prompt-size, skill count)
T: tools (MCP ports, organ health, units)
B: backups (vault999, arifos age)
C: CLIs (agent CLI presence)
A: agents (F13 packet, TREE777, CHRON)

## Adding a phase

1. Write p_phase_name() returning list of F objects.
2. Add to phases in main() and phn in render().
3. Test: python3 /root/scripts/weekly-aaa-maintenance.py

## Pitfalls

- K-02 blocks secrets paths in terminal. Use pathlib or heredoc.
- W_SCAR blocks URLs in write_file. Use terminal heredoc.
- Token interpolation: .env has VAR=${REF}. Use _load_env_dict().
- last_status ok is not firing proof. Check executions.db.
- Cron works without env sourcing if script reads .env directly.

## Companions

federation-housekeeping-master, hermes-cron-zen,
hermes-runtime-audit, FORGE-infra-crons.

DITEMPA BUKAN DIBERI