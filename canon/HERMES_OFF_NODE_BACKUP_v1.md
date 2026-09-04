# HERMES — Off-Node Backup Procedure (v1)

> **Status:** CANON — SEALED by F13 directive 2026-09-04 (Arif Fazil)
> **Forged:** 2026-09-04 by FI-003 (Qwen Code) under F13 directive (D6, post AMENDMENT-002)
> **Ratified:** 2026-09-04 by F13 directive (Arif Fazil) — see git commit for trace
> **Binding upstream:** `/root/AAA/canon/HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md` AMENDMENT-002 §9
> **Pair with:** MACHINE_MAP.md (canonical machine SOT)
> **DITEMPA BUKAN DIBERI** — Forged, not given.

---

## 1. Objective

This canon specifies the off-node backup + restore procedure for Hermes runtime state, satisfying audit gaps #2 (single physical concentration) + #4 (append-only ≠ immutable).

**Why:** Until this canon existed, Hermes state on KVM8 `/root/.hermes/` had only on-disk restic backups + `/root/.hermes-cold/` heritage copy on the SAME node. A disk corruption or node compromise would lose critical state (state.db, carry_forward, sessions, zen_receipts). After this canon: encrypted WORM backups to off-node object storage (B2 or S3) with quarterly restore drills, plus FRAME-OUTER independent verification on KVM2.

---

## 2. Backup Targets

| Target | Path on KVM8 | Frequency | Retention | Off-node location |
|---|---|---|---|---|
| Hermes state.db | `/root/.hermes/state.db` | 6-hourly | 30 daily + 12 monthly | B2 bucket `arifos-hermes-state` (WORM, encrypted) |
| Carry-forward | `/root/.hermes/carry_forward.json` | 1-hourly | 14 daily | B2 bucket `arifos-hermes-cf` (versioned) |
| Sessions | `/root/.hermes/sessions/` | 6-hourly | 30 daily | B2 bucket `arifos-hermes-sessions` (versioned) |
| Zen receipts | `/root/.hermes/zen_receipts/` | 6-hourly | 30 daily | B2 bucket `arifos-hermes-zen` (WORM) |
| Marrow (ledgers) | `/root/.hermes/{attestation,cooling,zen_receipts}` | 6-hourly | 30 daily + 12 monthly | B2 bucket `arifos-hermes-marrow` (WORM) |
| Heritage snapshot | `/root/.hermes-cold/HERMES-heritage-5.3G-20260904/` | weekly | 4 weekly + indefinite | B2 bucket `arifos-hermes-heritage` (cold storage) |

---

## 3. Backup Script (canonical reference)

```bash
#!/bin/bash
# /root/.hermes/scripts/backup_hermes_state.sh
# Run via systemd timer (6-hourly: */6 hours, 1-hourly for carry-forward)
set -euo pipefail

TS=$(date -u +%Y%m%dT%H%M%SZ)
B2_BUCKET="${B2_HERMES_BUCKET:-arifos-hermes-state}"
ENCRYPT_KEY_FILE="/root/.secrets/hermes-backup.age"

case "${BACKUP_TARGET:-state}" in
  state)
    sqlite3 /root/.hermes/state.db "PRAGMA quick_check"  # verify before backup
    age -e -i "$ENCRYPT_KEY_FILE" /root/.hermes/state.db \
      | rclone rcat "b2:${B2_BUCKET}/state-${TS}.db.age"
    ;;
  carry_forward)
    jq . /root/.hermes/carry_forward.json \
      | age -e -i "$ENCRYPT_KEY_FILE" \
      | rclone rcat "b2:${B2_BUCKET}/cf-${TS}.json.age"
    ;;
  marrow)
    tar -czf - -C /root/.hermes \
      attestation-ledger.jsonl cooling-ledger.jsonl zen_receipts/ \
      | age -e -i "$ENCRYPT_KEY_FILE" \
      | rclone rcat "b2:${B2_BUCKET}/marrow-${TS}.tar.gz.age"
    ;;
  heritage)
    rsync -a --delete /root/.hermes-cold/ /tmp/heritage-snapshot-${TS}/
    tar -czf - -C /tmp "heritage-snapshot-${TS}" \
      | age -e -i "$ENCRYPT_KEY_FILE" \
      | rclone rcat "b2:arifos-hermes-heritage/heritage-${TS}.tar.gz.age"
    rm -rf /tmp/heritage-snapshot-${TS}
    ;;
esac

# Emit arifFlow receipt
curl -s -X POST http://127.0.0.1:7073/ingest \
  -H 'Content-Type: application/json' \
  -d "{\"step_type\":\"Verify\",\"actor_id\":\"backup-hermes\",\"summary\":\"Hermes backup completed\",\"target\":\"${BACKUP_TARGET}\",\"ts\":\"${TS}\"}"
```

---

## 4. Restore Procedure

**Quarterly restore drill (per AMENDMENT-002 §9):**

1. Pick a random backup from B2 (use `rclone lsf` with most-recent filter).
2. Decrypt: `age -d -i /root/.secrets/hermes-backup.age backup.age > restored`
3. Verify integrity:
   - state.db: `sqlite3 restored "PRAGMA quick_check"` + check `PRAGMA integrity_check`
   - JSON files: `jq . file | sha256sum` vs known-good
   - tar.gz: `tar tzf file` + spot-check contents
4. FRAME-OUTER signs: `curl -s -X POST http://kvm2:7074/frame/attest -d '{"event":"RESTORE_DRILL","target":"<state|cf|marrow|heritage>","sha256":"<hex>","ts":"<iso>"}'`
5. Compare sha256 vs original (if known) or vs last-known-good.
6. Log to VAULT999.

**Catastrophic restore (KVM8 total loss):**

1. Boot KVM8 fresh (or use KVM4 dormant backup `/root/HERMES/`).
2. Restore from B2: state.db + carry_forward + marrow.
3. Restart `hermes-asi-gateway.service`.
4. FRAME-OUTER attest.
5. AAA identity-plane re-bind (out-of-band F13 sign-off).
6. Restore certificates + Ed25519 keys from offline vault.

---

## 5. Independent Verification (FRAME-OUTER on KVM2)

Per audit gap #3 (witness independence):

```bash
# FRAME-OUTER daily job (KVM2):
rclone lsf "b2:arifos-hermes-state/" --format "tp" | head -7 > /tmp/state-listings.txt
sha256sum /tmp/state-listings.txt > /tmp/state-listings.sha
# Send to F13 inbox as daily digest
mail -s "Hermes backup daily digest" arif@arif-fazil.com < /tmp/state-listings.sha
```

**Invariant:** KVM8 may not be sole signer of backup verification. KVM4 may not be sole signer. KVM2 (FRAME-OUTER) MUST produce a daily digest independently.

---

## 6. Encryption + Key Management

- **Algorithm:** `age` (https://age-encryption.org) — simple, modern, post-quantum-safe trajectory.
- **Key location:** `/root/.secrets/hermes-backup.age` (mode 600, root only).
- **Key rotation:** Annual (every Jan 1). Old keys retained for 1 year to decrypt historical backups.
- **Key backup:** Offline (printed paper in sealed envelope, stored in physical safe separate from VPS).
- **Per F1 AMANAH:** Loss of key = loss of all backups. The physical paper key is the lifeline.

---

## 7. Retention Policy

| Class | Retention | Rationale |
|---|---|---|
| Daily snapshots | 30 days | Recent debugging + accident recovery |
| Monthly snapshots | 12 months | Year-over-year trends + audit |
| Heritage snapshots | 4 weekly + indefinite | Major version transitions |
| Tombstones (deleted intents) | 7 years | Compliance + audit (if applicable) |

---

## 8. Failure Modes + 888_HOLD Triggers

| Trigger | Verdict | Owner |
|---|---|---|
| Backup script fails (non-zero exit) | 888_HOLD + alert F13 | A-FORGE |
| B2 connection failure | Log warning, retry hourly | A-FORGE |
| Backup file size anomaly (>2x or <0.5x previous) | 888_HOLD + manual review | A-FORGE |
| Decryption fails on restore drill | 888_HOLD + key review | F13 |
| FRAME-OUTER digest missing for >24h | 888_HOLD + manual FRAME restart | F13 + FRAME |

---

## 9. Cross-References

- `/root/AAA/canon/HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md` AMENDMENT-002 §9 (binding upstream)
- `/root/AAA/docs/MACHINE_MAP.md` §1 (heritage cold backup row)
- `/root/AAA/docs/HEADSCALE_ACL.md` (when exists)
- `/root/.hermes/state.db` recovery procedure (existing skill)

---

## 10. Open Questions (PENDING F13)

- **Q1**: B2 bucket vs S3 vs Wasabi — which provider? (Default: B2 already wired)
- **Q2**: Quarterly drill cadence — is it quarterly sufficient? (Default: yes per AMENDMENT-002 §9)
- **Q3**: Should heritage snapshots be decrypted-only-on-demand, or decrypted+stored warm on KVM2? (Default: cold, decrypt on drill)

---

DITEMPA BUKAN DIBERI — v1 SEALED 2026-09-04 by F13 directive (Arif Fazil)
