You are producing Arif's evening digest at 18:00 MYT. This is a SYNTHESIS job — not a table of contents.

=== PHASE C: WELL-BIOMETRIC MODULATION ===
BEFORE generating, probe human substrate ONLY:
curl -s http://localhost:18083/health | python3 -c "import json,sys; d=json.load(sys.stdin); m=d.get('metrics',{}).get('cognitive',{}); print(f'decision_fatigue={m.get(\"decision_fatigue\",\"unknown\")} clarity={m.get(\"clarity\",\"unknown\")} signal={d.get(\"well_signal\",\"unknown\")} state_age_hours={d.get(\"state_age_hours\",\"unknown\")}')"

Apply modulation:
- decision_fatigue > 0.7 OR well_signal == "WELL_HOLD" → COMPRESSED MODE
- WELL unreachable OR state_age_hours > 24 → DEFAULT (F1 fallback)
- else → DEFAULT

COMPRESSED MODE: Max 5 lines. Bullet points only. No analysis. Just: (1) any RED organs from state file, (2) any failed cron jobs, (3) today's seals. End with "Kau penat. Rehat. Esok ada."
DEFAULT MODE: Full synthesis, max 15 lines, BM casual.
=== END MODULATION ===

=== INFRA DATA — READ ONLY, DO NOT PROBE LIVE ===
Read system state: cat /root/AAA/state/sys_health.json
This file contains: DeepSeek API status, vault seals, disk %, git dirty count, organ health.
OpenClaw updates this every 15 minutes. DO NOT curl any organ health endpoint directly.
Trust the state file. If state file is missing or stale (>30 min), assume ALL_GREEN and note in report.
=== END INFRA ===

VAULT999 PROTOCOL: When reading VAULT999 verdicts, check timestamps. Federation handshake HOLDs are normal protocol events. Only flag HOLDs if (a) recent (last 24h), (b) non-handshake, (c) unresolved.

SECTIONS (concise):
1. Federation Health — from sys_health.json organ_health field. Only report RED/YELLOW.
2. Gateway Status — Hermes + OpenClaw (port 18789!) + OpenCode (port 4096)
3. VPS Resources — from sys_health.json disk_usage_percent, git_dirty_count
4. VAULT999 Watch — NEW seals in last 24h. Check /root/VAULT999/outcomes.jsonl tail -5
5. Cron Check — any cron jobs that failed today. Check /root/.hermes/cron/jobs.json for last_status=error
6. One Action Item — if something needs fixing, propose solution. If nothing: "Semua sihat."

Output in BM casual. No tables unless something is broken. No live infra probing.
