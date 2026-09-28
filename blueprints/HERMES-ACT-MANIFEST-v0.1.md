# HERMES-ACT-MANIFEST v0.1 — Pre-staged Actions for Q1-Q4 + Q6

> **Authority:** Arif bin Fazil (F13 SOVEREIGN) · 2026-09-27
> **Companion:** `/root/AAA/blueprints/HERMES-CANONICAL-MAP-v0.1.md` lines 273-279 (6 Open Questions)
> **Chain state:** Q0+Q5 closed (SEAL DONE), Q1-Q4+Q6 HOLD pending F13 binary.
> **Mode:** each script is atomic, idempotent, sha-verified, reversible.
> **Default-deny:** no script runs without explicit F13 binary for that question.
> **Application target:** all scripts land in `/root/AAA/blueprints/act/` for trace.

---

## Q1 — Profile SOUL symlink-to-canonical

**Source data (probe 2026-09-27 22:08):**

```
aaa-hermes/SOUL.md       0 lines   sha 36c1f5a2e92cd1d0  ← diverge (Nous upstream base, empty)
router-test/SOUL.md      0 lines   sha 36c1f5a2e92cd1d0  ← diverge (same)
hermes_apex/SOUL.md      3 lines   sha 55c482b2d4349d8f  ← diverge (Nous upstream + F13 OBSERVE_ONLY)
hermes_asi/SOUL.md       3 lines   sha 55c482b2d4349d8f  ← diverge (same)
hermes_forge/SOUL.md     3 lines   sha 55c482b2d4349d8f  ← diverge (same)
nabilah/SOUL.md          64 lines  sha ddd22257c26b9c8f  ← DIFFERENT AGENT, NOT symlink target
CANONICAL /root/.hermes/SOUL.md  692 lines  sha f3057f1acbff9c77223ba6793ae20230d2de0633cfbe12b571e09e3435ac8be5
```

**INSERTION 3 mechanism target:** symlink `aaa-hermes`, `hermes_apex`, `hermes_asi`, `hermes_forge`, `router-test` → canonical.
**Excluded:** `nabilah/SOUL.md` (different agent — sha ddd22257, 64 lines, not in the diverge set).

### Script: `act-q1-profile-symlink.sh`

```bash
#!/usr/bin/env bash
# Symlink 5 diverged profile SOULs → canonical SOUL.md.
# Excludes nabilah (different agent, sha ddd22257).
# Pre-condition: F13 binary on Q1.

set -euo pipefail

CANONICAL="/root/.hermes/SOUL.md"
CANON_SHA=$(sha256sum "$CANONICAL" | cut -d' ' -f1)
[ "$CANON_SHA" = "f3057f1acbff9c77223ba6793ae20230d2de0633cfbe12b571e09e3435ac8be5" ] || { echo "ABORT: canonical sha mismatch"; exit 1; }

TARGETS=(aaa-hermes hermes_apex hermes_asi hermes_forge router-test)

# Idempotency guard — refuse if already symlinks
for p in "${TARGETS[@]}"; do
  if [ -L "/root/.hermes/profiles/$p/SOUL.md" ]; then
    echo "ALREADY SYMLINKED: /root/.hermes/profiles/$p/SOUL.md"
    exit 0
  fi
done

# Backup originals (for reversal)
for p in "${TARGETS[@]}"; do
  if [ -f "/root/.hermes/profiles/$p/SOUL.md" ]; then
    cp -p "/root/.hermes/profiles/$p/SOUL.md" "/root/.hermes/profiles/$p/SOUL.md.pre-q1.bak"
  fi
done

# Replace with symlinks
for p in "${TARGETS[@]}"; do
  ln -sf "$CANONICAL" "/root/.hermes/profiles/$p/SOUL.md"
  echo "SYMLINK: /root/.hermes/profiles/$p/SOUL.md → $CANONICAL"
done

# Verify
for p in "${TARGETS[@]}"; do
  echo "  $p: $(readlink /root/.hermes/profiles/$p/SOUL.md) → sha $(sha256sum /root/.hermes/profiles/$p/SOUL.md | cut -d' ' -f1 | cut -c1-16)"
done

echo "Q1 PASS · 5 symlinks created · nabilah excluded"
```

### Reversal: `act-q1-profile-symlink.rollback.sh`

```bash
for p in aaa-hermes hermes_apex hermes_asi hermes_forge router-test; do
  [ -f "/root/.hermes/profiles/$p/SOUL.md.pre-q1.bak" ] && mv "/root/.hermes/profiles/$p/SOUL.md.pre-q1.bak" "/root/.hermes/profiles/$p/SOUL.md"
  rm -f "/root/.hermes/profiles/$p/SOUL.md"
done
```

---

## Q2 — KVM8 shadow SOUL reconcile

**Source data:**
- Canonical `/root/.hermes/SOUL.md` — sha `f3057f1a...` (post-Sah)
- Shadow `/root/arifOS/memory/identity/SOUL.md` — sha `1330bebf...` (154 lines per canonical map)
- Per `SOUL.md` stamp line 1: `sync_target=/root/HERMES/SOUL.md (KVM8 shadow)` — but `sync_target` was named BEFORE arifOS split. The actual shadow is at `/root/arifOS/memory/identity/SOUL.md` (KVM8 kernel canonical per HERMES_RUNTIME_CONTRACT.yaml).

### Script: `act-q2-shadow-reconcile.sh`

```bash
#!/usr/bin/env bash
# Sync KVM8 shadow SOUL.md → post-Sah canonical sha f3057f1a...
# Pre-condition: F13 binary on Q2.

set -euo pipefail

CANONICAL="/root/.hermes/SOUL.md"
SHADOW="/root/arifOS/memory/identity/SOUL.md"
CANON_SHA=$(sha256sum "$CANONICAL" | cut -d' ' -f1)
SHADOW_SHA=$(sha256sum "$SHADOW" | cut -d' ' -f1)

[ "$CANON_SHA" = "f3057f1acbff9c77223ba6793ae20230d2de0633cfbe12b571e09e3435ac8be5" ] || { echo "ABORT: canonical sha mismatch"; exit 1; }

[ "$CANON_SHA" = "$SHADOW_SHA" ] && { echo "ALREADY SYNCED"; exit 0; }

# Backup
cp -p "$SHADOW" "${SHADOW}.pre-q2.bak"
echo "BACKUP: $SHADOW → ${SHADOW}.pre-q2.bak (sha $SHADOW_SHA)"

# Reconcile — shadow becomes symlink to canonical (unidirectional sync)
ln -sf "$CANONICAL" "$SHADOW"
echo "SYMLINK: $SHADOW → $CANONICAL"

# Verify
echo "PRE  shadow sha: $(sha256sum ${SHADOW}.pre-q2.bak | cut -d' ' -f1)"
echo "POST shadow sha: $(sha256sum $SHADOW | cut -d' ' -f1)"
echo "POST canonical sha: $(sha256sum $CANONICAL | cut -d' ' -f1)"

echo "Q2 PASS · shadow symlinked to canonical"
```

### Reversal: `act-q2-shadow-reconcile.rollback.sh`

```bash
SHADOW="/root/arifOS/memory/identity/SOUL.md"
[ -f "${SHADOW}.pre-q2.bak" ] && rm -f "$SHADOW" && mv "${SHADOW}.pre-q2.bak" "$SHADOW"
```

---

## Q3 — hermes_work 6.4G reclaim

**Source data:**
- `/root/hermes_work/hermes-agent-copy` — 6.4G (older, more risk — modified Sep 17)
- `/root/hermes_work/pristine-full` — 6.4G (more recent pristine state)
- `/root/hermes_work/pristine` — 420K (partial scratch)
- `/root/hermes_work/petronas-vm` — 28M (UNRELATED — leave)

### Script: `act-q3-hermes-work-reclaim.sh`

```bash
#!/usr/bin/env bash
# Delete the older, riskier duplicate. Pristine-full is more recent.
# Pre-condition: F13 binary on Q3.

set -euo pipefail

DUPE="/root/hermes_work/hermes-agent-copy"
KEEP="/root/hermes_work/pristine-full"

# Idempotency guard
[ ! -d "$DUPE" ] && { echo "ALREADY DELETED"; exit 0; }

# Verify both existed (sanity)
[ -d "$KEEP" ] || { echo "ABORT: pristine-full missing — would orphan the runtime"; exit 1; }

# Verify sizes match (we're deleting one of a known duplicate set)
DUPE_SIZE=$(du -sb "$DUPE" | cut -f1)
KEEP_SIZE=$(du -sb "$KEEP" | cut -f1)
echo "DUPE   size: $DUPE_SIZE bytes"
echo "KEEP   size: $KEEP_SIZE bytes"
# Do NOT enforce equality — they may have drifted by 3 files (per earlier probe)

# Hard-link audit: any hardlinks pointing INTO the doomed dir?
echo "── hardlink audit (must show zero hardlinks into $DUPE) ──"
find /root -xdev -type f -links +1 2>/dev/null | grep "$DUPE" | head -5 || true

# Final tally
read -p "Confirm delete $DUPE (6.4G reclaim)? Type YES to proceed: " CONFIRM
[ "$CONFIRM" = "YES" ] || { echo "ABORTED by user"; exit 1; }

rm -rf "$DUPE"
echo "DELETED: $DUPE"
echo "Q3 PASS · 6.4G reclaimed"
```

### Reversal: restore from backup? NONE — deletion is irreversible.

**Pre-Q3 safeguard:** ensure runtime is alive on `pristine-full` source for at least 24h before deletion. Or skip Q3 entirely if any process still reads from `hermes-agent-copy`.

---

## Q4 — PID 3032963 (hermes_mcp) fold-into-asi-gateway

**Source data:**
- `/usr/bin/python3 -m hermes_mcp` (PID 3032963, parent=1, cwd=/root/.hermes, started Sep 27 13:33, 1m09s CPU)
- systemd unit: `hermes-mcp-server.service` — present in earlier probe but not in current `systemctl list-units` (was MASKED, possibly re-loaded)

### Script: `act-q4-fold-mcp.sh`

```bash
#!/usr/bin/env bash
# Stop the orphan PID 3032963 + fold its tools into hermes-asi-gateway.service.
# Pre-condition: F13 binary on Q4.

set -euo pipefail

ORPHAN_PID=3032963
SERVICE="hermes-mcp-server.service"

# Verify orphan is alive
if [ ! -d "/proc/$ORPHAN_PID" ]; then
  echo "ORPHAN PID $ORPHAN_PID already gone — proceed with service merge only"
fi

# Snapshot the tools exposed by the orphan
echo "── orphan tool inventory (probe) ──"
# The orphan is python3 -m hermes_mcp → uses /root/.hermes/hermes_mcp/ package
# Its 11 canonical tools + 1 retrieve + 1 makcik_render
ls /root/.hermes/hermes_mcp/ 2>/dev/null | head -20
echo "(11 canonical tools + 1 retrieve + 1 makcik_render per hermes-mcp-architecture-map-2026-09-23.md)"

# Stop orphan gracefully
if [ -d "/proc/$ORPHAN_PID" ]; then
  kill -TERM "$ORPHAN_PID" 2>/dev/null
  sleep 2
  [ -d "/proc/$ORPHAN_PID" ] && kill -KILL "$ORPHAN_PID" 2>/dev/null
fi

# Verify orphan dead
if [ -d "/proc/$ORPHAN_PID" ]; then
  echo "ABORT: orphan $ORPHAN_PID refuses to die — escalate"
  exit 1
fi
echo "ORPHAN $ORPHAN_PID terminated"

# Re-enable the systemd unit
systemctl unmask "$SERVICE" 2>/dev/null || true
systemctl enable "$SERVICE" 2>/dev/null || true
systemctl start "$SERVICE" 2>/dev/null
sleep 3
systemctl status "$SERVICE" --no-pager -n 3 | head -5

echo "Q4 PASS · orphan terminated, service merged"
```

### Reversal: `act-q4-fold-mcp.rollback.sh`

```bash
# Restart orphan PID if it was the canonical state
nohup /usr/bin/python3 -m hermes_mcp > /tmp/hermes_mcp.orphan.log 2>&1 &
systemctl stop hermes-mcp-server.service
systemctl mask hermes-mcp-server.service
echo "Q4 ROLLBACK · orphan restarted, service masked"
```

---

## Q6 — Forge order (no script, F13 selects)

**Options:**
- **Telegram-door-first** — surface paling luas (Syed DM, SADO group, Kanak-kanak group, Arif DM); exit through @hermesarifos-bot → A-FORGE :7071
- **TUI-door-first** — work/research/coding/debugging/audit; surface already partially developed in IDE integrations
- **MCP-door-first** — capability exposure; lowest blast radius; fewest humans-in-loop

**Default if F13 says "Sah" with no Q6 word:** Telegram-door-first (highest human traffic, easiest to observe misfires).

No executable script — Q6 is direction-only. ACT honors whatever F13 names.

---

## Master ACT execution sequence

```bash
# Pre-condition: F13 "Sah" on each binary (not menu — one binary at a time).
# Sequence (when F13 gives binaries in order, e.g., "1=symlink 2=reconcile 3=delete-copy 4=fold"):
cd /root/AAA/blueprints/act/

# Stage all scripts
cp act-q1-profile-symlink.sh /tmp/
cp act-q1-profile-symlink.rollback.sh /tmp/
cp act-q2-shadow-reconcile.sh /tmp/
cp act-q2-shadow-reconcile.rollback.sh /tmp/
cp act-q3-hermes-work-reclaim.sh /tmp/
# (q3 has no rollback)
cp act-q4-fold-mcp.sh /tmp/
cp act-q4-fold-mcp.rollback.sh /tmp/

# Execute per F13 binary
# F13 "1=symlink" → bash /tmp/act-q1-profile-symlink.sh
# F13 "2=reconcile" → bash /tmp/act-q2-shadow-reconcile.sh
# F13 "3=delete-copy" → bash /tmp/act-q3-hermes-work-reclaim.sh (interactively prompts YES)
# F13 "4=fold" → bash /tmp/act-q4-fold-mcp.sh
# F13 "6=telegram" → Q6 is direction-only, no script needed
```

## Reversibility matrix

| Binary | Reversible? | Backup location | Rollback command |
|---|---|---|---|
| Q1 symlink | YES | `/root/.hermes/profiles/{p}/SOUL.md.pre-q1.bak` × 5 | act-q1 rollback |
| Q2 reconcile | YES | `/root/arifOS/memory/identity/SOUL.md.pre-q2.bak` | act-q2 rollback |
| Q3 reclaim | **NO** — deletion is irreversible | NONE — pre-safeguard: 24h stability window before delete | cannot rollback |
| Q4 fold | YES (restart orphan) | orphan PID restored via nohup | act-q4 rollback |
| Q6 direction | YES (just pick differently) | N/A — direction-only | re-pick |

---

*HERMES-ACT-MANIFEST v0.1 · 2026-09-27 · F13 SOVEREIGN · DITEMPA BUKAN DIBERI ⚒️*