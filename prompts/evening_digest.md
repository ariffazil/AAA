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
It is written by /root/AAA/bin/probe_sys_health.sh on a systemd timer (arifos-sys-health.timer).
Verify before use: ls -la /root/AAA/state/sys_health.json  (mtime = last write, this is reality)
DO NOT curl any organ health endpoint directly. Read the state file.

FRESHNESS IS MANDATORY — VOID GUARD APPLIES:
- The file carries `timestamp_utc`, `run_seq`, `probe_status`, `probe_failures` and `valid_for_seconds` (1800).
- If the file is MISSING, or its `timestamp_utc` is older than `valid_for_seconds`, or `probe_status` != "OK":
  report → "CANNOT_WITNESS: sys_health.json <reason>" and state which sections are unwitnessed.
  NEVER assume ALL_GREEN. Absence of data is NOT evidence of health.
  NEVER silently skip. NEVER fill a green value for something you could not read.
- If `probe_status` == "OK": report the values as observed, and say data age in minutes.
- A field that is `null` means the probe could not witness it — report it as CANNOT_WITNESS for that field,
  do not substitute a default. `vault_seals_intact: null` is NOT `true`.
- Section 1 (Federation Health) must use `organ_health`: ALL_GREEN / SYSTEM_DEGRADED / CANNOT_WITNESS.
  CANNOT_WITNESS here means at least one canonical organ unit was not active — say so explicitly.
=== END INFRA ===

VAULT999 PROTOCOL: When reading VAULT999 verdicts, check timestamps. Federation handshake HOLDs are normal protocol events. Only flag HOLDs if (a) recent (last 24h), (b) non-handshake, (c) unresolved.

SECTIONS (concise):
1. Federation Health — from sys_health.json organ_health field. Report only if not ALL_GREEN.
2. Gateway Status — Hermes + OpenClaw (port 18789!) + OpenCode (port 4096)
3. VPS Resources — from sys_health.json disk_usage_percent, git_dirty_count
4. VAULT999 Watch — NEW seals in last 24h. The AUTHORITATIVE seal store on KVM8 is the live
   writer: curl -s http://127.0.0.1:5001/vault/status  -> vault_seals_total, chain_integrity,
   chain_gaps, pending_holds. The event log is /root/VAULT999/outcomes.jsonl (tail -5).
   Do NOT use VAULT_WRITER_URL / VAULT_API_URL (:8100) — nothing listens there.
   Do NOT use /root/.local/share/arifos/vault999/outcomes.jsonl — frozen since Aug 25.
5. Cron Check — any cron jobs that failed today. Check /root/.hermes/cron/jobs.json for last_status=error
6. One Action Item — if something needs fixing, propose solution. If nothing: "Semua sihat."

Output in BM casual. No tables unless something is broken. No live infra probing.
