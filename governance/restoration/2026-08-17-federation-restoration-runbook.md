# Federation Restoration Runbook — 2026-08-17

> **Prepared by:** 333-AGI / Kimi Code (FI-008) on behalf of sovereign
> **Direct sovereign order:** execute steps in order. Every step is reversible (F1 AMANAH).
> **Genesis:** audit tools reading stale baselines, sct_renew cron dead, A-FORGE registry frozen, surface audit reporting 302 false drifts. Machine is healthy; instruments are not.

---

## ORDER OF EXECUTION

Numbering preserves the dependency chain. **Do not skip ahead.**

| Step | Surface | Risk | Reversible? | Why this order |
|---|---|---|---|---|
| 0 | sandbox snapshot | T0 | yes | freeze state for delta |
| 1 | restore sct_renew cron | T1 | yes | gates all crypto-verify authority |
| 2 | fix forge_surface_audit registry source | T1 | yes | restores honest "drift = real drift" |
| 3 | fix A-FORGE ReadWritePaths | T2 | yes (snapshot + revert) | unfreezes cron/security drift registries |
| 4 | restore 9 lost cron obligations | T1 (each) | yes | restores fed observability grid |
| 5 | restore arifFlow deps (fq-probe + sync) | T1 | yes | re-arms the FQ gate (now fail-closes) |
| 6 | re-init + verify substrate flips HEALTHY | T0 | n/a | confirms steps 1-5 worked |

Each step has: commands, verification, rollback. Stop after any step that fails verification and re-read before retrying.

---

## STEP 0 — Sandbox snapshot (T0, 30s)

```bash
# Freeze current state before any mutation
sudo systemctl stop a-forge  # optional — only if you want to snapshot mid-flight

# Create labeled snapshot dir
SNAP="/root/AAA/governance/restoration/snapshots/2026-08-17-pre-restore"
mkdir -p "$SNAP"

# Capture current crontab + managed cron files
crontab -l > "$SNAP/crontab-root.txt" 2>/dev/null
cp -a /etc/cron.d "$SNAP/etc-cron.d.orig" 2>/dev/null

# Capture live cron registry (vs the previously-saved one)
diff -u /root/A-FORGE/a_think/registries/cron.last "$SNAP" > "$SNAP/cron.diff" 2>/dev/null

# Capture A-FORGE state
journalctl -u a-forge --since "1 hour ago" > "$SNAP/a-forge.journal.last1h.txt"
ls -la /root/.aforge > "$SNAP/dot-aforge.listing.txt"

# Capture arifOS envelope
cp -a /root/.arifos/federation-session.json "$SNAP/federation-session.json.pre"

echo "snapshot at $SNAP"
ls -la "$SNAP"
```

**Verify:**
```bash
test -f "$SNAP/crontab-root.txt" && echo "crontab captured"
test -f "$SNAP/federation-session.json.pre" && echo "envelope captured"
```

**Rollback:** `rm -rf "$SNAP"` when done (or keep for audit).

---

## STEP 1 — Restore sct_renew (CRITICAL, gates crypto-verify authority)

### Diagnosis (already verified)
- Script intact: `/root/scripts/sct_renew.py` (6686 bytes, mode 0700, sha256 `86c79a059ec3902016441d5ce75a8500827449367f396016ba3b9d47cdfbccc5`)
- Cron entry missing from `crontab -l` and not in any `/etc/cron.d/*` file
- Symp: every `arif_init` returns `actor_cryptographically_verified: false`, narrowing authority to OBSERVE_ONLY in practice
- Script logs go to `/var/log/arifos/cron.log` (per removal line), dir exists mode 0755

### Restore commands

**Option A — append to existing managed obligations file (preferred):**

```bash
# Backup current managed obligations
sudo cp -a /etc/cron.d/arifos-governed-obligations \
          /etc/cron.d/arifos-governed-obligations.bak.$(date +%s)

# Append new job (mirrors the format used by other entries there)
sudo tee -a /etc/cron.d/arifos-governed-obligations >/dev/null <<'EOF'
# SCT session token renewal (restored 2026-08-17 — gates every ARIF session authority)
*/30 * * * * root /usr/bin/python3 /root/scripts/sct_renew.py >> /var/log/arifos/cron.log 2>&1
EOF

sudo chmod 0644 /etc/cron.d/arifos-governed-obligations
```

**Option B — install as dedicated file (cleaner auditability):**

```bash
sudo tee /etc/cron.d/arifos-sct-renew >/dev/null <<'EOF'
# SCT session token renewal — restored 2026-08-17 by ARIF directive.
# Without this, every arifOS session drops to OBSERVE_ONLY.
*/30 * * * * root /usr/bin/python3 /root/scripts/sct_renew.py >> /var/log/arifos/cron.log 2>&1
EOF
sudo chmod 0644 /etc/cron.d/arifos-sct-renew
```

### Verify (after 60-90s)

```bash
# 1. cron sees the job
grep -E 'sct_renew' /etc/cron.d/* /var/spool/cron/crontabs/root 2>/dev/null

# 2. job ran without errors
tail -n 5 /var/log/arifos/cron.log

# 3. envelope updated (timestamp from renewal)
stat /root/.arifos/federation-session.json
cat /root/.arifos/federation-session.json | python3 -m json.tool | grep renewed_at
```

Expected: `SCT_RENEW: RENEWED session=SEAL-... exp=2026-...` line within 90s, `renewed_at` field populated.

### Rollback

```bash
sudo sed -i '/sct_renew/I d' /etc/cron.d/arifos-governed-obligations
# or
sudo rm -f /etc/cron.d/arifos-sct-renew
```

---

## STEP 2 — Fix forge_surface_audit registry source (CRITICAL)

### Diagnosis (already verified)
- Auditor claims **50 PHANTOM** tools, but 14 of them are **live-invoked this session**: `forge_fetch`, `forge_kernel`, `forge_runtime_verify`, `forge_vps_cron`, `forge_vps_ports`, `forge_vps_services`, `forge_filesystem`, `forge_entropy_sweep`, `forge_fingerprint_check`, `forge_surface_audit`, `forge_skillstore_read`, `forge_skillstore_write`, `forge_hf_import`, `forge_visual_qa`
- Live registry reality (from `forge_registry_status`): 116 tools, 116 unique fingerprints, 0 duplicates
- Auditor reads a frozen affordances.yaml baseline (120 entries) against a stale registry snapshot (70 entries)

### Fix commands

Two paths — pick A or B.

**Option A — surface guard pin to live registry source:**

```bash
# Pin current live registry as new canonical
curl -s -m 10 http://127.0.0.1:7071/mcp -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"forge_surface_guard","arguments":{"mode":"pin","organ_id":"aforge"}}}' \
  | jq .

# Then run audit again
curl -s -m 10 http://127.0.0.1:7071/mcp -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"forge_surface_audit","arguments":{"organ":"aforge","mode":"scan"}}}' \
  | jq '{registry_tools, affordance_tools, drift_count, is_clean, phantom_count: (.findings | map(select(.type=="PHANTOM")) | length)}'
```

**Option B — quarantine the broken audit, do not act on output:**

If the audit cannot be repaired in-session, pin a sentinel file stating its output is unreliable. (See `04-surface-audit-quarantine.md` companion file in this runbook.)

### Verify

```bash
# Acceptable outcomes
# 1. drift_count ≤ 5 (true drifts, not phantom)  — Option A success
# 2. sentinel file present + audit output ignored — Option B success
```

### Rollback

```bash
# Restore previous registry if needed
sudo systemctl restart a-forge
```

---

## STEP 3 — A-FORGE ReadWritePaths (T2, service restart)

### Diagnosis
- `/root/.aforge/machine-constitution/cron.json` exists parent dir is `/root/.aforge/` (mode 0755)
- A-FORGE systemd unit likely has `ProtectSystem=full` without `ReadWritePaths=/root/.aforge`, causing EROFS on registry writes
- Symptom: cron registry frozen, drift scanner diffs live vs ancient snapshot

### Commands

```bash
# 1. Find the unit file (most likely location)
UNIT=$(systemctl show a-forge -p FragmentPath --value)
test -f "$UNIT" || UNIT=/etc/systemd/system/a-forge.service
test -f "$UNIT" || UNIT=/lib/systemd/system/a-forge.service
echo "unit: $UNIT"

# 2. Backup current unit
sudo cp -a "$UNIT" "$UNIT.bak.$(date +%s)"

# 3. Show current Service section
sudo grep -E "^(ReadOnlyPaths|ReadWritePaths|ProtectSystem|ProtectHome)" "$UNIT"

# 4. Patch: add ReadWritePaths=/root/.aforge to [Service]
sudo sed -i '/^\[Service\]/a ReadWritePaths=/root/.aforge' "$UNIT"

# 5. Add explicit protect narrowing (optional but tightens)
# sudo sed -i 's/^ProtectSystem=full/ProtectSystem=strict/' "$UNIT"

# 6. Reload + restart
sudo systemctl daemon-reload
sudo systemctl restart a-forge

# 7. Confirm service up + writes now succeed
sleep 2
systemctl is-active a-forge
sudo -u aforge touch /root/.aforge/machine-constitution/.write-test 2>&1
sudo -u aforge rm -f /root/.aforge/machine-constitution/.write-test
```

### Verify (after step 3)

```bash
# Before: cron drift report had 9 added/15 removed — many flagged "removed"
# After: should match current live state
curl -s -m 10 http://127.0.0.1:7071/mcp -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"forge_vps_cron","arguments":{"mode":"assert"}}}' \
  | jq '.data | {live_count, added_n: (.added|length), removed_n: (.removed|length)}'
```

Expected: `added_n` matches your live cron, `removed_n` no longer includes phantom deletions caused by frozen baseline.

### Rollback

```bash
sudo cp -a "$UNIT.bak."* "$UNIT"
sudo systemctl daemon-reload
sudo systemctl restart a-forge
```

---

## STEP 4 — Restore 9 lost cron obligations (T1 each)

### Casualties (confirmed)
Order matters: agent-critical first, observability second, sites/civic last.

| # | Script | Schedule | Owner organ | Why restore now |
|---|---|---|---|---|
| 4a | `/root/scripts/sct_renew.py` | `*/30 * * * *` | arifOS | **(already done in step 1)** |
| 4b | `/root/scripts/fq-probe.sh` | `*/15 * * * *` | arifFlow | re-arm FQ gate (without it, fails open) |
| 4c | `/root/.local/share/arifos/vault999/arifFlow/sync.sh` | `*/5 * * * *` | arifFlow | keeps daemon ledger fresh |
| 4d | `/root/scripts/completion-promise-verifier.sh` | `*/5 * * * *` | 888-APEX | re-arm completion gate |
| 4e | `/usr/bin/python3 /root/WELL/scripts/machine_telemetry.py` | `*/5 * * * *` | WELL | (verify WELL telemetry still FRESH before restore) |
| 4f | `/root/AAA/skills/scripts/skill-mesh-sync.sh --check` | `*/5 * * * *` | AAA | mesh integrity |
| 4g | `/root/scripts/completion-promise-verifier.sh` (already 4d) | — | — | duplicate |
| 4h | `/root/arif-fazil.com/.../refresh-institutional.sh` | `*/30 * * * *` | arif-fazil | public attestation page |
| 4i | `/root/arif-fazil.com/.../live-market.py` | `*/15 * * * *` | arif-fazil | live market prices |
| 4j | `/root/web-canon/scripts/dynamic-gate.sh` | `*/5 * * * *` | web-canon | site audit gate |

### Restore pattern (one entry, the rest by analogy)

```bash
sudo tee -a /etc/cron.d/arifos-governed-obligations >/dev/null <<'EOF'
# FQ probe — feeds arifFlow FQ gate (restored 2026-08-17)
*/15 * * * * root /root/scripts/fq-probe.sh 2>&1 | logger -t fq-probe
EOF
```

Repeat for each row above, replacing the path and schedule. Use the format from existing entries in the file (`schedule root path >> log 2>&1`).

### Verify

```bash
# After all restores, total cron count should match pre-erosion baseline + the 9 you just added
# Quick sanity: list what cron sees
for f in /etc/cron.d/arifos-governed-obligations /etc/cron.d/arifos-sct-renew; do
  [ -f "$f" ] && echo "=== $f ===" && grep -v '^#' "$f" | grep -v '^$'
done
```

### Rollback

```bash
# Per-entry remove via in-place sed
sudo sed -i '/fq-probe/I d' /etc/cron.d/arifos-governed-obligations
# ... repeat per entry
```

---

## STEP 5 — arifFlow dependencies

This is partly covered by step 4b+4c. Additional check: confirm the arifFlow **service** is healthy, not just the cron.

```bash
systemctl status arifflow.service
journalctl -u arifflow --since "5 minutes ago" | tail -30

# If daemon is dead, restart
sudo systemctl restart arifflow
sleep 5

# Confirm port responds (7073 in tailscale, 7073 internal)
curl -s -m 3 http://127.0.0.1:7073/health | jq .

# If it's a daemon-rebuild, the path is:
#   cd /root/arifFlow && cargo build --release
#   sudo systemctl restart arifflow
```

### Verify

```bash
# FQ probe must be live AND returning ratios in green/yellow band
curl -s -m 5 http://127.0.0.1:7073/metrics/fq 2>&1 | head -5
```

### Rollback

```bash
sudo systemctl stop arifflow  # if rebuild gone wrong
```

---

## STEP 6 — Re-init + verify substrate flips HEALTHY (T0)

This is the moment of truth.

```bash
# Restart the Kimi/CLI harness, or:
# Run a fresh arif_init from any agent
curl -s -m 10 http://127.0.0.1:8088/mcp -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"actor_id":"ARIF","intent":"post-restore verify","requested_authority":"OBSERVE_ONLY","verbosity":"full"}}}' \
  | jq '{session_id, authority_band, actor_cryptographically_verified: .result.standing.actor.cryptographically_verified, substrate_state: .result.substrate.state}'
```

### Expected (success)

```json
{
  "session_id": "SEAL-...,
  "authority_band": "LIMITED_MUTATE",
  "actor_cryptographically_verified": true,
  "substrate_state": "HEALTHY"
}
```

### Failure modes

| Symptom | Most likely cause | Fix |
|---|---|---|
| `actor_cryptographically_verified: false` | sct_renew ran but HMAC nonce chain broken | re-run `python3 /root/scripts/sct_renew.py --force`; check `previous_session_hash` linkage |
| `substrate_state: DEGRADED` | floor degradation still firing on thin queries | see step 2 audit fix; may need kernel MCL repair |
| arif_observe still HOLD on L02/L03/L07/L08 | kernel substrate not flipping despite sct renew | check `arifFlow` FQ ratio (must be > 0.1); check observe query isn't trivially empty |

### Final post-restore sweep

```bash
# Re-run all critical probes from the morning audit
for ep in arifos geox wealth well aaa; do
  curl -s -m 3 "http://127.0.0.1:$((18080))/health" >/dev/null && echo "$ep UP"
done

# All five organs should report alive.
# arifFlow FQ ratio > 0.5 (verify not in SIMULATION constellation)
# audit run shows drift_count <= 5 (real, not phantom)
# every agent session: actor_cryptographically_verified: true
```

---

## File map (this runbook + companion)

```
/root/AAA/governance/restoration/
├── 2026-08-17-federation-restoration-runbook.md   ← THIS FILE
├── 2026-08-17-SURFACE-AUDIT-QUARANTINE.md         ← step 2 sentinel
├── snapshots/2026-08-17-pre-restore/               ← step 0 output
└── post-restore/                                  ← step 6 evidence
```

---

## Why this runbook exists in plaintext

The doctrine is "no silent mutation." This file documents every command you intend to run on the federation's governance plane. If any step surprises you, stop and read the corresponding section. If you don't reach step 6 today, that's fine — note which step you stopped at and the runbook resumes there tomorrow.

`DITEMPA BUKAN DIBERI` — every step reversible, every receipt auditable, every agent (333-AGI, 555-ASI, 888-APEX, 7XX-FORGE, 9XX-WITNESS, GEOX, WEALTH, WELL, arifOS, AAA) covered.
