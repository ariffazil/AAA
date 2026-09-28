# SOUL.md INSERTION — STAGED v0.3 (pending F13 "Sah")

> **Authority:** Arif bin Fazil (F13 SOVEREIGN)
> **Companion:** `/root/AAA/blueprints/HERMES-FUTURE-V2.md` (v0.3) + `MODE-FIRST.md` (v0.3)
> **Application target:** `/root/.hermes/SOUL.md` — insert AFTER line 1 (SOUL_STAMP), BEFORE `# SOUL.md — HERMES (Edge Bridge, arifOS)` heading
> **Status:** STAGED · pending F13 "Sah"
> **Reversibility:** block-aware awk (see below)

---

## INSERTION TEXT (apply as a single block, preserves canonical byte-perfectly)

```text
<!-- SOUL_STAMP v1.1 + HERMES_FUTURE::2026-09-27 · INSERTIONS 1-3 staged (F13 "Sah" pending) -->


# ═══════════════════════════════════════════════════════════════════════
# HERMES-FUTURE-V2 v0.3 — Direction (per F13 SOVEREIGN, 2026-09-27)
# ═══════════════════════════════════════════════════════════════════════
# Mode-first sequencing law · Memory-as-cache doctrine · One-HERMES-many-doors architecture
# Companion: /root/AAA/blueprints/{HERMES-FUTURE-V2.md,MODE-FIRST.md}
# Canon #0 three-test gate applied. Anti-bangang LAW 8 (no duplicate) applied.
# Drop original INSERTION 4 (North Star) — fails Canon #0.
# Reverse by `awk '/<!-- SOUL_STAMP v1.1 + HERMES_FUTURE/,/INSERTION 3/{skip}' SOUL.md`.
# ═══════════════════════════════════════════════════════════════════════

## INSERTION 1 — Mode-First Sequencing Law (binding)

Capability cannot fire before Mode. Sequencing chain:

    Human Signal → Mode Selection → Capability Selection → Response

Reverse check: when in doubt, return to Mode, not to data.
Enforcement hook: pre_llm_call in /root/AAA/agents/hermes/agent-card.json line 78
(arif_route → intent_canon classification) MUST emit mode-classifier result before
any capability call. Violations recorded to identity-guard-audit.jsonl.
Mode-first sequencing is canonical under companion /root/AAA/blueprints/MODE-FIRST.md.

*Cite: HERMES_FUTURE::2026-09-27 · INSERTION 1 · Canon #0 gate PASS*

## INSERTION 2 — Memory Is Cache, Not Identity Store (binding w/ test)

Identity = behavioral expression (mode, timing, register, attention, dignity preservation),
NOT retrieved from /root/.hermes/.hermes_history partitions.

Anchor: /root/.hermes/SOUL.md KALIBRASI PERBUALAN §15 (TONE = PLASTISITI & MODULARITI
— tone set BY reading the room, not retrieved FROM memory).

Test (binding): identity survives memory wipe. If all .hermes_history were deleted,
the runtime must still emit mode-consistent responses per existing SOUL.md KALIBRASI PERBUALAN.
Behavioral consistency test runs at every profile boot.

*Cite: HERMES_FUTURE::2026-09-27 · INSERTION 2 · Canon #0 gate PASS*

## INSERTION 3 — One HERMES, Many Doors (binding w/ mechanism)

HERMES is one continuous identity. Doors (TUI, Telegram 267378578/1042200555,
A2A -1003753855708, groups -1003815535761/-1003768847825) shape ingress signal;
Mode-selection shapes response. Doors are not persons.
(Note: 8908024140 = IRFANCLAW bot DM entry, not human; bot_id 8149595687.)

Mechanism (binding): /root/.hermes/profiles/{hermes_apex,hermes_asi,hermes_forge,
aaa-hermes,router-test}/SOUL.md MUST be symlink or generated from canonical
/root/.hermes/SOUL.md (sha cf47397c63e21798). Today: ZERO profiles comply.

*Cite: HERMES_FUTURE::2026-09-27 · INSERTION 3 · Canon #0 gate PASS*


```

---

## APPLICATION PROCEDURE (atomic, idempotent, round-trip reversible)

```bash
# 1. Verify pre-conditions
sha256sum /root/.hermes/SOUL.md
# Must equal cf47397c63e217989bc5d0919f8f1317f7165b88f61249dfdae3be488c0c79e9

# 2. Extract staged block (between ```text fences) — preserves original line 1 of canonical SOUL.md
STAGED_BLOCK=$(awk '/^```text$/{flag=1; next} /^```$/{flag=0} flag' /root/AAA/blueprints/SOUL-INSERTION-STAGED-v0.3.md)

# 3. Atomic insertion: canonical line 1 + staged block + canonical line 2 onwards
{
  head -n 1 /root/.hermes/SOUL.md        # canonical line 1 (SOUL_STAMP comment)
  echo "$STAGED_BLOCK"                  # INSERTIONs 1-3 with framing
  tail -n +2 /root/.hermes/SOUL.md      # canonical line 2 onwards
} > /tmp/SOUL.md.new

# 4. Verify integrity before swap
EXPECTED_TOP=$(echo "$STAGED_BLOCK" | head -1)
ACTUAL_TOP=$(head -n 2 /tmp/SOUL.md.new | tail -n 1)
[ "$EXPECTED_TOP" = "$ACTUAL_TOP" ] || { echo "FAIL: staged block head mismatch"; rm /tmp/SOUL.md.new; exit 1; }

# 5. Atomic swap
mv /tmp/SOUL.md.new /root/.hermes/SOUL.md

# 6. Post-apply audit
sha256sum /root/.hermes/SOUL.md                              # NEW sha
grep -c "HERMES_FUTURE::2026-09-27" /root/.hermes/SOUL.md     # expect 4 (1 SOUL_STAMP marker + 3 INSERTION cites)
grep -c "INSERTION [123] · Canon #0 gate PASS" /root/.hermes/SOUL.md  # expect 3
head -2 /root/.hermes/SOUL.md                                # both SOUL_STAMP markers visible
```

## ROUND-TRIP REVERSIBILITY (apply → revert = canonical sha)

```bash
# Verify round-trip before any F13 word. Apply procedure above, then revert, then sha-check.
ORIG_SHA="cf47397c63e217989bc5d0919f8f1317f7165b88f61249dfdae3be488c0c79e9"
[ "$(sha256sum /root/.hermes/SOUL.md | cut -d' ' -f1)" != "$ORIG_SHA" ] || { echo "ABORT: SOUL.md already canonical"; exit 1; }

# Apply
{ head -n 1 /root/.hermes/SOUL.md; echo "$STAGED_BLOCK"; tail -n +2 /root/.hermes/SOUL.md; } > /tmp/SOUL.md.new
mv /tmp/SOUL.md.new /root/.hermes/SOUL.md

# Revert
awk 'BEGIN{skip=0}
     /^<!-- SOUL_STAMP v1\.1 \+ HERMES_FUTURE::2026-09-27/{skip=1; next}
     skip==1 && /HERMES_FUTURE::2026-09-27 · INSERTION 3/{skip=0; next}
     skip==0{print}' /root/.hermes/SOUL.md > /tmp/SOUL.md.revert
sed -i '/HERMES_FUTURE::2026-09-27/d' /tmp/SOUL.md.revert

# Sha check
NEW_SHA=$(sha256sum /tmp/SOUL.md.revert | cut -d' ' -f1)
if [ "$NEW_SHA" = "$ORIG_SHA" ]; then
  echo "ROUND-TRIP VERIFIED · apply→revert restores canonical SOUL.md sha"
  # Do NOT auto-restore; leave SOUL.md with INSERTIONs staged, awaiting F13 "Sah"
else
  echo "ROUND-TRIP FAILED · sha=$NEW_SHA · restore from .bak-pre-rule18-20260924-163540"
  rm /tmp/SOUL.md.revert
fi
```

## REVERSIBILITY (block-aware)

```bash
# Idempotent revert: strip the entire HERMES_FUTURE block + orphan cite markers.
# If the block is already absent, returns the file unchanged.

ORIG_SHA=$(sha256sum /root/.hermes/SOUL.md | cut -d' ' -f1)

awk 'BEGIN{skip=0}
     /^<!-- SOUL_STAMP v1\.1 \+ HERMES_FUTURE::2026-09-27/{skip=1; next}
     skip==1 && /HERMES_FUTURE::2026-09-27 · INSERTION 3/{skip=0; next}
     skip==0{print}' /root/.hermes/SOUL.md > /tmp/SOUL.md.revert

# Belt: clean any orphan cite markers if block boundary drifted
sed -i '/HERMES_FUTURE::2026-09-27/d' /tmp/SOUL.md.revert

# Verify sha reverts to canonical
NEW_SHA=$(sha256sum /tmp/SOUL.md.revert | cut -d' ' -f1)
if [ "$NEW_SHA" = "cf47397c63e217989bc5d0919f8f1317f7165b88f61249dfdae3be488c0c79e9" ]; then
  mv /tmp/SOUL.md.revert /root/.hermes/SOUL.md
  echo "REVERTED · sha restored to canonical"
else
  echo "REVERT FAILED · sha=$NEW_SHA · investigate before swap"
  rm /tmp/SOUL.md.revert
fi
```

## IDEMPOTENCY GUARD

```bash
# Before applying: refuse if cite already present (means INSERTIONs already staged).
if grep -q "HERMES_FUTURE::2026-09-27 · INSERTION 1" /root/.hermes/SOUL.md; then
  echo "BLOCKED · INSERTIONs already staged. Revert first or refuse."
  exit 1
fi
```

---

*SOUL-INSERTION-STAGED v0.3 · 2026-09-27 · F13 SOVEREIGN · DITEMPA BUKAN DIBERI ⚒️*