# HERMES — Kill / Isolate / Restart Procedure Spec (v1)

> **Status:** CANON — Pending F13 ratification (drafted by FI-003 per F13 directive, D5 P0 hardening)
> **Forged:** 2026-09-04 by FI-003 (Qwen Code) under F13 directive (D5, post AMENDMENT-002)
> **Binding upstream:** `/root/AAA/canon/HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md` AMENDMENT-002 §8
> **Pair with:** HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md §8, MACHINE_MAP.md
> **DITEMPA BUKAN DIBERI** — Forged, not given.

---

## 1. Objective

This canon specifies the operational runbook for invoking the four procedures inherited from AMENDMENT-002 §8: **KILL_EXECUTION**, **KILL_EGRESS**, **ISOLATE_NODE**, **ISOLATE_KVM4**, and **RESTART_HERMES**. Each procedure is reversible (K-1 invariant) but logged irreversibly.

**Why:** Until AMENDMENT-002 §8, the contract defined the procedures but not the operational steps to invoke them. After this canon: every procedure has a named trigger, a sequence of commands, a recovery plan, and an audit trail.

---

## 2. Procedure Catalogue (per AMENDMENT-002 §8, operational expansion)

### 2.1 KILL_EXECUTION

**Trigger:** SEV-0/1 — Hermes output observed to mutate production unexpectedly, repeated F2/F9 violations, suspected prompt-injection escape.

**Sequence (Hermes on KVM8):**
```bash
# 1. Drop the gateway
sudo systemctl stop hermes-asi-gateway.service

# 2. Freeze the queue (Telegram + A2A pending)
sudo systemctl stop hermes-asi-gateway-queue-watcher.service  # if exists
sudo iptables -I OUTPUT -p tcp --dport 443 -m owner --uid-owner hermes -j DROP

# 3. Log to VAULT999 with class=incident
cat >> /root/VAULT999/incidents/$(date -u +%Y-%m-%d).jsonl << JSON
{"ts":"$(date -u +%FT%TZ)","actor":"F13/AAA","class":"KILL_EXECUTION","reason":"<free-text>","sessions_killed":<n>,"evidence":<sha256>}
JSON

# 4. Notify A-FORGE + arifFlow
curl -s -X POST http://127.0.0.1:7073/ingest \
  -H 'Content-Type: application/json' \
  -d '{"step_type":"Seal","actor_id":"hermes-asi","summary":"KILL_EXECUTION","reason":"<free-text>"}'
```

**Recovery:**
1. F13 signs restart token (out-of-band, e.g. signed message in another channel)
2. AAA verifies token against ledger
3. A-FORGE re-arms `hermes-asi-gateway.service` with new lease
4. Verify `curl http://127.0.0.1:8088/health` returns 200 (kernel sees gateway)
5. F13 confirms production parity before live use

**Owner:** F13 + A-FORGE
**Asymmetric degradation:** Hermes-Read is preserved via heritage cold copy if KVM8 fails; this procedure blocks Draft + Broker only.

---

### 2.2 KILL_EGRESS

**Trigger:** SEV-0/1 — Data egress anomaly, prompt-injection at scale, suspected credential leak.

**Sequence (Hermes on KVM8):**
```bash
# 1. Block outbound at Caddy layer
sudo caddy reload --config /etc/caddy/Caddyfile.killed-egress

# 2. Quarantine outbound queue
sudo mv /var/spool/hermes/outbound /var/spool/hermes/quarantine-$(date -u +%Y%m%dT%H%M%SZ)

# 3. Freeze Telegram webhook
sudo systemctl stop hermes-asi-gateway-telegram.service  # if exists

# 4. Log + notify (same pattern as KILL_EXECUTION §2.1)
```

**Recovery:**
1. F13 + A-FORGE restore
2. AAA verifies model route has not exfiltrated (compare recent egress log vs receipts)
3. If model route compromised, KILL_EXECUTION on the route too

**Owner:** F13 + A-FORGE + AAA

---

### 2.3 ISOLATE_NODE (KVM8 / Hermes runtime)

**Trigger:** SEV-0 — KVM8 (Hermes runtime, court) compromise suspected.

**Sequence:**
```bash
# 1. Remove KVM8 from headscale ACL (cross-node traffic blocked)
# Edit /etc/headscale/acl.yaml on KVM8 control plane, remove tag:arifos rules
# Or on KVM8: sudo headscale policy check -f /etc/headscale/acl.yaml

# 2. Freeze all cross-node calls
sudo ufw deny out to 100.64.0.0/16  # KVM4 + KVM2 tailnet range

# 3. Route Hermes fallback to KVM4 dormant backup (read-only)
# AAA reactivates /root/HERMES/ on KVM4 as fallback Hermes (manual, not auto)
# NOTE: requires AAA identity plane re-binding + F13 sign-off

# 4. FRAME-OUTER signs the isolation event (witness record)
curl -s -X POST http://kvm2:7074/frame/attest -d '{"event":"ISOLATE_NODE","kvm":"kvm8","ts":"<iso>"}'
```

**Recovery:**
1. F13 signs KVM8 rejoin token
2. AAA re-verifies identity plane (all hermes-asi signatures valid)
3. FRAME-OUTER confirms clean state (no rogue processes)
4. Restore headscale ACL + UFW rules
5. Restart hermes-asi-gateway.service

**Owner:** F13 + A-FORGE + AAA + FRAME

---

### 2.4 ISOLATE_KVM4 (workshop: OpenClaw + LiteLLM :4000)

**Trigger:** SEV-0 — KVM4 (workshop, OpenClaw edge + LiteLLM :4000 brain) compromise suspected.

**Sequence:**
```bash
# 1. Remove KVM4 from headscale ACL
# Edit /etc/headscale/acl.yaml, remove tag:forge rules

# 2. Freeze FED lane (KVM8 HAProxy → KVM4 litellm)
sudo systemctl stop haproxy-kvm8.service  # stops 4000 → KVM4 backend
# Or: sudo iptables -I INPUT -p tcp --dport 4000 -s 100.64.0.5 -j DROP

# 3. Freeze OpenClaw edge (independent)
sudo -u kvm4-admin ssh kvm4-admin@100.64.0.5 'sudo systemctl stop openclaw-gateway.service'

# 4. Hermes on KVM8 falls back to direct external-model route or local Ollama
# Update FED config to skip KVM4 backend
# Or: Hermes uses KVM8 local Ollama directly

# 5. FRAME-OUTER signs the isolation event
```

**Recovery:**
1. F13 signs KVM4 rejoin token
2. AAA re-verifies identity plane
3. FRAME-OUTER confirms clean state
4. Restore headscale ACL + FED :4000 backend
5. Restart openclaw-gateway.service on KVM4

**Owner:** F13 + A-FORGE + AAA + FRAME

---

### 2.5 RESTART_HERMES

**Trigger:** Routine maintenance, model upgrade, gateway service update.

**Sequence (auto if lease valid):**
```bash
# 1. Verify state.db + carry_forward integrity
sqlite3 /root/.hermes/state.db "PRAGMA quick_check"
test -f /root/.hermes/carry_forward.json && echo "carry_forward OK"

# 2. Restart gateway
sudo systemctl restart hermes-asi-gateway.service

# 3. Verify boot
sleep 5
curl -s http://127.0.0.1:8088/health | jq .status  # kernel sees gateway
systemctl is-active hermes-asi-gateway
```

**Recovery:** Auto-restart on failure (systemd Restart=on-failure); manual investigation if repeated failures.

**Owner:** A-FORGE (auto)
**Approval:** None required (routine)

---

## 3. SEV Taxonomy (per AMENDMENT-002 §8)

| Level | Definition | Examples |
|---|---|---|
| SEV-0 | Federational impact (cross-organ, cross-node) | ISOLATE_NODE, ISOLATE_KVM4, mass injection event |
| SEV-1 | Hermes output integrity violated | KILL_EXECUTION, single-organ mutation |
| SEV-2 | Single-tool or single-chat anomaly | KILL_EGRESS for one session |
| SEV-3 | User-affecting degradation (latency, quality) | Restart + monitor |
| SEV-4 | Informational (logged only) | Audit-event log |

---

## 4. Mandatory Audit Fields

Every procedure invocation MUST emit a FlowReceipt with:

```yaml
actor: "F13 / AAA / FRAME / A-FORGE"
timestamp: "ISO-8601 UTC"
trigger_evidence: "<sha256 or pointer>"
procedure_class: "KILL_EXECUTION / KILL_EGRESS / ISOLATE_NODE / ISOLATE_KVM4 / RESTART_HERMES"
parameters: { ... procedure-specific ... }
recovery_plan: "<free-text>"
f13_signoff: "<required for KILL_*, ISOLATE_*; not for RESTART_HERMES>"
vault999_receipt_hash: "<auto-generated>"
```

**Invariant:** No procedure invokes without a vault999_receipt_hash. Hermes Output Receipts (§3 membrane §6) MUST cite this hash.

---

## 5. Pre-flight Checklist (BEFORE invoking any KILL/ISOLATE)

1. ☐ Confirm trigger evidence is concrete (not "I think...")
2. ☐ Check that a less-severe option is not available
3. ☐ F13 (or F13-signed proxy) is the invoker
4. ☐ All 3 of: A-FORGE, arifFlow, FRAME-OUTER are accepting FlowReceipts
5. ☐ Recovery plan is documented in this canon (above)
6. ☐ VAULT999 path is writable
7. ☐ Telegram bots are notified (if Hermes is the affected surface)

If any ☐ fails → HOLD. Do not invoke.

---

## 6. Post-incident Procedure (every KILL/ISOLATE)

1. **T+0**: Procedure invoked. Receipt emitted.
2. **T+15min**: First stability check (curl /health on affected organ).
3. **T+1h**: FRAME-OUTER independent verification of isolation.
4. **T+24h**: AAA identity plane re-verification.
5. **T+7d**: F13 ratifies the incident as canonical scar OR voids the invocation as false alarm.

If ratification as scar: write to `/root/AAA/canon/SCAR_RECORDS/scar-NNN-<short-name>.md` with full trace.

---

## 7. Cross-References

- `/root/AAA/canon/HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md` AMENDMENT-002 §8 (canonical upstream)
- `/root/AAA/canon/HERMES_PROMPT_INJECTION_MEMBRANE_v1.md` §11 (failure modes + 888_HOLD)
- `/root/AAA/docs/MACHINE_MAP.md` (canonical machine SOT)
- `/root/AAA/docs/HEADSCALE_ACL.md` (when exists — referenced for ACL operations)

---

## 8. Open Questions (PENDING F13)

- **Q1**: F13-signed proxy — can AAA issue a F13-signed kill token under emergency? Or must F13 sign out-of-band every time? (Default: F13 out-of-band, AAA cannot proxy)
- **Q2**: KILL_EXECUTION auto-restore timeout — if F13 doesn't sign restart within X hours, should gateway auto-rearm in degraded mode? (Default: NO, stay down until F13)
- **Q3**: ISOLATE_KVM4 auto-fallback — should Hermes auto-switch to local Ollama on KVM8, or 888_HOLD until F13? (Default: auto-switch, log loudly)

---

DITEMPA BUKAN DIBERI — v1 DRAFT SEALED FOR REVIEW
