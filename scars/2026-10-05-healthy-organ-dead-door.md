---
scar_id: SCAR-SYS-2026-10-05-001
title: "Healthy organ, dead door — process liveness is not door liveness"
filed_by: FI-008 (kimi-code/FI-008, session SEAL-8ae3ddee596e4f87)
acquired_at: 2026-10-05T23:30+08:00
domain: federation-transport / public-door reliability
cost: "frame.arif-fazil.com public door 502 for unknown duration (≥1 day, bound unknown) — discovered only by external-bound audit, not by any internal monitor"
trigger_pattern: "Any claim of 'organ alive' derived from `systemctl is-active` or a local port bind, while the PUBLIC path (DNS → CF edge → tunnel ingress SNI → caddy vhost → upstream) is unverified. Also: tunnel ingress entries whose originServerName points at another hostname (apex) — caddy answers the TLS alert 'internal_error' and CF renders 502 while every local probe stays green."
rule_extracted: "A door is alive only when a synthetic request traverses the FULL public path from outside (or loopback-with-SNI + --resolve); process/port checks prove nothing about the door."
responsibility_today: "P0 fixed frame (vhost + correct SNI in /etc/cloudflared/config.yml, verified 200 via CF). Owed: sentinel/doctor probes must include per-door synthetic initialize (loopback --resolve minimum, external worker ideal) so a dead door alerts within one probe cycle — fold into P1 MINT generator's verify pass. Until then, any 'all organs healthy' claim MUST carry the door-probe asterisk."
elevation: "candidate-if-recurring (1 occurrence; watch for second distinct door failure)"
salience: 0.8
last_reaffirmed: 2026-10-05
sealed_to_vault999: false
w_scar: 0.7
kin:
  - scar-2026-10-03-probe-without-fetch-stale-map (address on stale map — same shape: verified the wrong object)
  - capability-truth rule (AGENTS.md:146): declare down/up only after alternate-lane test
evidence:
  - "/etc/cloudflared/config.yml:104-107 — frame entry originServerName: arif-fazil.com (wrong SNI), journal: 'remote error: tls: internal error' originService=https://127.0.0.1:443"
  - "frame-mcp.service active + 127.0.0.1:18086 LISTEN throughout the outage"
  - "fix verified: HTTP 200 via Cloudflare, serverInfo frame-mcp 2026.09.14 (23:40 MYT)"
  - "receipt: /root/AAA/research/P0-EXECUTION-RECEIPT-2026-10-05.md"
---
