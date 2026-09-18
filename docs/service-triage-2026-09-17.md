# Service Triage — Inactive/Dead systemd Units, arifOS Federation (KVM8)

> **Date:** 2026-09-17 · **Author:** FI-008 kimi-code subagent (read-only sweep; zero unit mutations performed)
> **Method:** `systemctl list-units --state=inactive,dead` + `list-timers --all` + `list-unit-files` + `systemctl show` (Result/ExecMainStatus/TriggeredBy) + unit-file reads + consumer greps + JetStream probe.
> **Classification rule (state-transition discipline):** "inactive" is NOT "dead". A oneshot service between timer fires is HEALTHY, not a corpse. Where none of REVIVE/TOMBSTONE/DOCUMENT truthfully fits, the card says `NONE — HEALTHY`; forcing a bucket would be a transition lie.
> **Constraint noted:** F9 ANTI-HANTU hard-deny blocks agent-issued `systemctl disable|mask`. Every TOMBSTONE below therefore ends in an F13-sanctioned action, not an agent action.

## Executive summary

| Outcome | Count | Units |
|---|---|---|
| REVIVE | 2 | aforge-heartbeat, arifOS-NATS-heartbeat |
| TOMBSTONE | 1 | arifosd (retired-in-practice; formalize under F13) |
| DOCUMENT (replacement running) | 5 | arifflow-mcp, apa-telegram-bridge, minimax-media, hermes-mcp, nats |
| NONE — HEALTHY (timer oneshot, verified fired) | 33 | see sweep table |
| Ghost entries (not-found, stale references) | 6 | aforge, arifOS, frame, well-mcp, vault999-api, openclaw-gateway |

**Key anomaly:** three daemons were stopped cleanly within one window on 2026-09-16 morning (arifflow-mcp 05:42:57 exit 15, arifOS-NATS-heartbeat 06:51:34 exit 0, aforge-heartbeat 10:10:21 exit 0) — consistent with one undocumented cleanup pass. Per-unit journal entries for these units are no longer present (vacuumed), so the stop rationale is unrecoverable. Going forward: any deliberate stop should leave a receipt naming the replacing surface.

---

## TRIAGE CARDS — named services

### 1. aforge-heartbeat.service
```
Service: aforge-heartbeat.service
Status:  inactive/dead (enabled) — clean stop 2026-09-16 10:10:21 +08, exit 0
Function: organ heartbeat daemon — publishes a-forge pulse to NATS JetStream
          stream `arifos-organs` (subject arifos.organ.aforge); polls :7071/health
Replacement: none. Peer daemons geox/wealth/well-heartbeat ARE running; a-forge is
          the only dead organ pulse. surface-guard.service watches MCP drift, it does
          not publish organ pulses — not a replacement.
Consumer: /root/arifFlow/scripts/arifflow_digest.py:74 get_organ_heartbeats() reads
          all 5 organs (arifos, aforge, geox, wealth, well) from JetStream; with this
          publisher down, the digest reports aforge=UNKNOWN (Void Guard, honest but
          degraded witness coverage).
Substrate: /opt/arifos/scripts/organ_heartbeat_daemon.py present; :7071 listener up.
Classification: REVIVE
Reason: asymmetric organ pulse (4 of 5 alive), live consumer, substrate intact,
        clean stop (not a crash). Restart is reversible and low-risk.
```

### 2. arifOS-NATS-heartbeat.service
```
Service: arifOS-NATS-heartbeat.service
Status:  inactive/dead (enabled) — clean stop 2026-09-16 06:51:34 +08, exit 0
Function: publishes the arifOS kernel organ pulse to NATS (module
          arifosmcp.abi.nats_heartbeat_daemon)
Replacement: none found. nats-server.service (:4222/:8222) is UP — the transport is
          fine, its publisher is not. fq-probe/arifFlow FQ measures frequency
          quality, not the kernel organ pulse subject.
Consumer: same as above — arifflow_digest.py reads arifos.organ.arifos; currently
          UNKNOWN/stale.
Substrate: module present in /opt/arifos/current/venv (verified
          .../site-packages/arifosmcp/abi/nats_heartbeat_daemon.py). Note: restart on
          2026-09-12 (carry-forward incident receipt) proved the unit works.
Classification: REVIVE
Reason: same evidence class as aforge-heartbeat; stopped in the same 2026-09-16
        window; live consumer; substrate verified present.
```

### 3. arifflow-mcp.service
```
Service: arifflow-mcp.service
Status:  inactive/dead (enabled) — SIGTERM stop 2026-09-16 05:42:57 +08, exit 15
Function: arifFlow FastMCP server — HTTP MCP transport for the arifFlow organ
Replacement: YES, three layers: (1) mcp.json "arifFlow" = stdio launcher
          (/root/.arifos/agents/kimi/mcp-launchers/arifflow.sh) wrapping the Rust
          daemon REST :7073 (arifflow.service, RUNNING, pid alive on 127.0.0.1:7073);
          (2) fed-router.service :7074 (RUNNING) federation MCP router;
          (3) mcp-media-ingest etc. cover specific flows. No listener missing.
Classification: DOCUMENT
Reason: HTTP FastMCP transport superseded by stdio launcher + fed-router. Unit can
        stay disabled; formal disable/mask (and removing the enabled-state mismatch)
        is an F13-sanctioned cleanup item.
```

### 4. apa-telegram-bridge.service
```
Service: apa-telegram-bridge.service
Status:  inactive/dead (enabled) — SIGTERM stop 2026-09-02 20:57:56 +08, exit 15;
         no :18096 listener
Function: APA Telegram Bridge — F13 veto surface for A-FORGE (forge_telegram)
Replacement: YES — forge-bot.service "FORGE Bot — Gateway 3 (@arifOS_bot Telegram →
          A-FORGE)" RUNNING since 2026-09-13 13:17:46, same bot token family, plus
          ack-consumer.service (human acceptance callbacks). The bridge (earlier
          gateway generation) was stopped 11 days BEFORE Gateway 3 started; same
          token cannot have two pollers anyway (Telegram getUpdates conflict).
Classification: DOCUMENT
Reason: superseded by forge-bot Gateway 3. Residual doc debt (cleanup list):
        APA_CUSTODY_LAYER.md:75 still names apa-telegram-bridge :18096 as the veto
        lane (stale), and the forge-drift-scanner port SOT still lists 18096.
        F2 hygiene note: the unit override carries a plaintext bot token in
        /etc/systemd/system/apa-telegram-bridge.service.d/override.conf — should not
        remain on disk if the unit is formally retired (F13).
```

### 5. arif-dream.service + arif-dream-distill.service
```
Service: arif-dream.service / arif-dream-distill.service
Status:  inactive/dead — HEALTHY: timer-driven oneshots, 72h cadence
         (OnUnitActiveSec=72h, Persistent=true), last ran Tue 2026-09-15
         22:49:29 / 22:52:49 exit 0; next fires Fri 2026-09-18 ~22:51 / ~22:54
Function: nightly(→72h) memory consolidation + reasoning distillation with
          Telegram delivery
Replacement: none needed
Classification: NONE — HEALTHY (no action)
Reason: inactive-between-fires is the designed state. Nit: unit descriptions still
        say "Nightly"/"72h ... " — the consolidation unit's Description says
        "Nightly Memory Consolidation" while the cadence is 72h; stale wording only.
```

### 6. aaa-drift-check.service
```
Service: aaa-drift-check.service
Status:  inactive/dead — HEALTHY: timer-driven oneshot; fired 2026-09-17 00:00:23
Function: AAA Federation daily drift check
Classification: NONE — HEALTHY (with a watch flag)
Reason: timer armed (next Sat 00:05). Watch flag: last run exited 1
        (ExecMainStatus=1, Result=success). Exit 1 appears to be the
        drift-found convention, but the journal for the unit is gone (vacuumed) so
        semantics are unverified. Verify on next fire; if exit 1 = finding, fine;
        if it is an error, treat as soft-REVIVE of the script fix.
```

### 7. arifos-backup.service
```
Service: arifos-backup.service
Status:  inactive/dead — HEALTHY: timer-driven (arifos-backup.timer 04:30 daily);
         last ran 2026-09-17 04:31:09 exit 0
Function: Tier-A direct backup (VAULT999 + state)
Classification: NONE — HEALTHY (no action)
Reason: ran this morning. Known SCOPE gap (not liveness): deprecation registry
        DIV-HERMES-BACKUP-GAP — script does not cover /root/.hermes sovereign state.
```

### 8. arifos-morning-briefing.service
```
Service: arifos-morning-briefing.service
Status:  inactive/dead — HEALTHY: timer-driven; last ran 2026-09-17 06:30:52 exit 0
Function: autonomous human-benefit loop #1 (F13 directive 2026-09-16)
Classification: NONE — HEALTHY (no action)
Reason: distinct from the tombstoned root-crontab "morning briefing" (removed
        2026-09-09, deprecation registry). Do not confuse the two.
```

### 9. arifflow-cooling-watchdog.service
```
Service: arifflow-cooling-watchdog.service
Status:  inactive/dead — HEALTHY: timer-driven, ~1-minute cadence; last ran
         2026-09-17 14:32:07 exit 0
Function: auto-resume daemon after arifFlow cooldown
Classification: NONE — HEALTHY (no action)
```

### 10. arifos-capability-probe.service / arifos-deploy-reconciler.service / hermes-liveness.service
```
Service: arifos-capability-probe.service   — timer-driven, last 2026-09-17 06:15:39 exit 0
Service: arifos-deploy-reconciler.service  — timer-driven, last 2026-09-17 14:32:11 exit 0
Service: hermes-liveness.service           — timer-driven (5 min), last 2026-09-17 14:31:13 exit 0
Classification (all three): NONE — HEALTHY (no action)
Reason: all fired today with exit 0, timers armed. Inactive state is the normal
        between-runs state for Type=oneshot.
```

### 11. hermes-mcp.service (masked)
```
Service: hermes-mcp.service
Status:  masked (deliberate; unmask is agent-blocked, F9)
Function: legacy HERMES MCP surface
Replacement: hermes-mcp-server.service RUNNING (streamable-http :18087)
Classification: DOCUMENT
Reason: textbook replacement case. Mask already marks the tombstone; keep the
        registry entry, no further action.
```

### 12. minimax-media.service (+ minimax-media MCP)
```
Service: minimax-media.service
Status:  inactive/dead (enabled) — clean stop 2026-09-02 08:11:04 exit 0; :18100 has
         NO listener (verified via ss). MCP entry disabled in mcp.json since
         2026-09-04 (PATCH-M1b, reason recorded: ":18100 listener absent").
Function: MiniMax media organ — image/video/TTS/music generation
Replacement: YES — FED image-generation cascade (federation-models.json capability
          fed-image-generation: bailian/wan2.7-image-pro → pollinations keyless →
          hf-flux) + dashscope_media.py for video t2v/i2v (MODULAR_INTELLIGENCE_MAP).
Classification: DOCUMENT
Reason: deliberate, documented disable with replacement cascade; final
        tombstone-vs-revive decision is explicitly parked "per M2" in mcp.json —
        that M2 decision needs F13. Until then: documented, no action.
```

### 13. arifosd.service
```
Service: arifosd.service
Status:  inactive/dead, unit DISABLED, never activated (no ExecMainExitTimestamp);
         /run/arifos/arifosd.sock and compat symlink both absent; no consumers found
Function: Constitutional Control Plane Daemon (kernel companion socket server)
Replacement: de-facto yes — arifos.service (arifOS Agent, RUNNING) is the kernel
          runtime; vault999-writer.service (:5001) is the only seal writer;
          aaa-signing.service handles F13 challenge signing. ORGAN.md:168 still
          lists arifosd as "control-plane daemon" (stale doc).
Classification: TOMBSTONE (retired-in-practice)
Reason: disabled + never runs + no socket + no consumer = dead with no one looking.
        Formalize: F13-sanctioned mask/unit removal + ORGAN.md correction. Not
        agent-executable (F9 ANTI-HANTU hard-deny on disable/mask).
```

### 14. nats.service
```
Service: nats.service
Status:  inactive/dead, disabled, never activated in current journal horizon
Function: legacy NATS unit
Replacement: nats-server.service RUNNING (:4222 client, :8222 monitor)
Classification: DOCUMENT (tombstone already executed)
Reason: officially DEPRECATED 2026-09-09 in /root/AAA/docs/deprecation-registry.json
        ("Superseded by distro unit nats-server.service during NATS migration").
        Nothing to do; entry exists for completeness. Companion tombstone:
        nats-prometheus-exporter.service → kabarkan-collector.service (same registry).
```

---

## SWEEP — remaining federation inactive units (all verified healthy oneshots)

| Unit | Last run (+08) | Exit | Timer next fire | Note |
|---|---|---|---|---|
| arifos-drift-check | 09-17 14:30 | 0 | 14:45 today | healthy |
| arifos-sys-health | 09-17 14:30 | 0 | 14:45 today | healthy |
| arifos-reality | 09-17 14:32 | 0 | 14:32 today | healthy |
| arifos-deploy-reconciler | 09-17 14:32 | 0 | 14:32 today | healthy (see card 10) |
| federation-state | 09-17 14:32 | 0 | 14:32 today | healthy |
| triadic-snapshot | 09-17 14:32 | 0 | 14:32 today | healthy |
| arifflow-cooling-watchdog | 09-17 14:32 | 0 | every ~1 min | healthy (card 9) |
| well-machine-telemetry | 09-17 14:31 | 0 | 14:36 today | healthy |
| hermes-liveness | 09-17 14:31 | 0 | 14:36 today | healthy (card 10) |
| sct-renew | 09-17 14:06 | 0 | 14:36 today | healthy |
| fq-probe | 09-17 14:07 | 0 | 14:37 today | healthy |
| frame-reader | 09-17 14:11 | 0 | 14:42 today | healthy |
| frame-probe | 09-17 14:28 | 0 | 14:44 today | healthy |
| fed-sync | 09-17 14:30 | 0 | 14:45 today | healthy |
| gov-a008-arifflow-sync | 09-17 14:00 | 0 | 15:00 today | healthy |
| gov-a009-git-to-vault | 09-17 14:00 | 0 | 15:00 today | healthy |
| stabilization-check | 09-17 14:01 | **2** | 15:00 today | exit 2 = intentional RED findings (L1 RED disk 78% > 60%, swap 87% > 50%; L2 arifOS degraded drift=true). Unit healthy; SUBSTRATE findings are real — disk/swap cleanup is a separate watch item. |
| vps-receipt | 09-17 14:00 | 0 | 15:00 today | healthy |
| fed-provider-probe | 09-17 14:00 | 0 | 20:00 today | healthy |
| security-disclosure-watch | 09-17 12:24 | 0 | 16:23 today | healthy |
| frame-witness-reader | 09-17 12:41 | 0 | 16:41 today | healthy |
| auditor-drift-check | 09-17 08:03 | 0 | 00:03 tomorrow | healthy |
| drift-detector | 09-17 07:15 | 0 | 07:15 tomorrow | healthy |
| arifos-capability-probe | 09-17 06:15 | 0 | 06:15 tomorrow | healthy (card 10) |
| arifos-morning-briefing | 09-17 06:30 | 0 | 06:30 tomorrow | healthy (card 8) |
| arifos-backup | 09-17 04:31 | 0 | 04:30 tomorrow | healthy (card 7) |
| vault999-backup | 09-17 03:50 | 0 | 03:51 tomorrow | healthy |
| wealth-market-daily | 09-17 00:01 | 0 | 00:01 tomorrow | healthy |
| aaa-drift-check | 09-17 00:00 | **1** | 00:05 tomorrow | healthy; exit-1 semantics unverified — watch flag (card 6) |
| arif-dream / arif-dream-distill | 09-15 22:49 / 22:52 | 0 | Fri ~22:51 / ~22:54 | healthy, 72h cadence (card 5) |

## Ghost entries — not-found inactive units (stale references, no unit file)

`aforge.service` (typo of a-forge.service, which IS running) · `arifOS.service` ·
`frame.service` · `well-mcp.service` (→ well.service, running) ·
`vault999-api.service` (→ vault999-writer.service, running) · `openclaw-gateway.service`

Classification: DOCUMENT. These are failed unit-name references left in systemd's
state (someone issued start/stop against wrong names). Cleanup is one reversible
command (`systemctl reset-failed` for the six names); no F13 needed since no unit
file is touched.

## Other masked units verified (all deliberate, all have live replacements)

arif-agent-worker · forge-gateway (→ a-forge.service RUNNING) ·
hermes-agent-mcp (→ hermes-mcp-server.service RUNNING) ·
wealth.service (→ wealth-organ.service RUNNING) · opencode-bot (opencode lane known
dead per DIV-VERIFICATION-LANE-OUTAGE; FI-003 surface = qwen-serve.service RUNNING) ·
audit-rules (stock OS unit, masked deliberately; auditd.service RUNNING).
Classification: DOCUMENT, no action.

## Action list (ordered)

1. **REVIVE (agent-executable, reversible):** `systemctl start aforge-heartbeat.service arifOS-NATS-heartbeat.service` (both enabled, Restart=on-failure). Verify with one JetStream read per organ and next arifflow digest (aforge/arifos should leave UNKNOWN).
2. **Watch:** stabilization-check RED findings — disk 78%, swap 87%; aaa-drift-check exit-1 semantics on next fire.
3. **F13 queue (document, do not execute):** mask/remove arifosd + fix ORGAN.md:168; decide minimax-media M2 (tombstone vs revive); formalize arifflow-mcp disable; retire apa-telegram-bridge unit + scrub its plaintext-token override + update APA_CUSTODY_LAYER.md:75 and the forge-drift-scanner port SOT (18096).
4. **Cheap cleanup (agent-executable):** `systemctl reset-failed` for the six ghost names.
5. **Discipline receipt:** the 2026-09-16 stop cluster (05:42 / 06:51 / 10:10) left no receipt; stop rationale was unrecoverable because per-unit journals were vacuumed. Future deliberate stops must record replacing-surface + evidence in deprecation-registry.json at stop time.

## Evidence receipts

- `systemctl list-units --state=inactive,dead` — 172 units; `--state=active,running` — 136 units (2026-09-17 ~14:32 +08)
- `systemctl list-timers --all` — 43 federation/OS timers armed, all with past LAST and future NEXT
- `systemctl show <unit> -p Result,ExecMainStatus,ExecMainExitTimestamp,TriggeredBy` for 38 units (table above)
- Unit files read: apa-telegram-bridge (+override), aforge-heartbeat (+privilege-inversion override), arifflow-mcp, arifOS-NATS-heartbeat, minimax-media, arifosd (+override), surface-guard, forge-bot, arif-dream.timer, arif-dream-distill.timer, aaa-drift-check
- Consumers: /root/arifFlow/scripts/arifflow_digest.py:74 (JetStream arifos-organs, 5 organs); /root/A-FORGE/duties/forge-drift-scanner.sh:66 (port SOT incl. 18096); /root/AAA/docs/APA_CUSTODY_LAYER.md:75
- mcp.json: minimax-media disabled_at 2026-09-04 PATCH-M1b with reason + revive-or-tombstone-per-M2 note; arifFlow via stdio launcher wrapping REST :7073
- deprecation-registry.json (2026.09.16): nats.service + nats-prometheus-exporter tombstones; DIV-HERMES-BACKUP-GAP; DIV-SYSTEMD-ORPHAN-UNITS; DIV-VERIFICATION-LANE-OUTAGE (opencode dead)
- Listeners (ss): :7071 node (a-forge), :7072 node (a-forge-mcp), :7073 arifflow (Rust), :7074 python (fed-router), :4222/:8222 nats-server; NO :18096, NO minimax :18100
- JetStream `nats stream info arifos-organs`: 33,183 messages, 5 subjects (stream alive; publishers for arifos+aforge stopped 09-16)
- Substrate presence: /opt/arifos/scripts/organ_heartbeat_daemon.py, /opt/arifos/current/venv/.../nats_heartbeat_daemon.py, /root/arifOS/arifosd.py, /root/A-FORGE/bridges/telegram_bridge.py

DITEMPA BUKAN DIBERI ⚒️
