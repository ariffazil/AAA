# arifOS Orientation Layer — SEALED

Status: **FROZEN** · 2026-09-03 23:49 MYT
Node: KVM8 (court-core) · 100.64.0.2
Sovereign: ARIF

## Final Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ /run/arifos/         (machine-readable, 5 + 1)              │
│   reality.json      ← reality.py (SOT, read-only)           │
│   authority.json    ← authority.py (derived from identity) │
│   inventory.json    ← inventory.py (services + ports)       │
│   attention.json    ← attention.py (top_3 only)             │
│   verdict.json      ← verdict.py (system vs governance)    │
│   reality.banner    ← banner.py (human 6-block receipt)     │
└─────────────────────────────────────────────────────────────┘

SOT HIERARCHY:
  identity.yaml   → authority.py (single derivation source)
  reality.py      → verdict.py (pass-through counts only)
  attention.py    → hand-curated top_3 (14-day rotation)
```

## SEALED Decisions

✅ `authority.py` — tolerant of KVM8/KVM4/KVM2 identity.yaml schemas
✅ `inventory.py` — pure read-only snapshot
✅ `attention.py` — top_3 + rotation_days=14, no backlog museum
✅ `verdict.py` — system vs governance split, all counts pass-through from reality.json
✅ `banner.py` — 6-block receipt with REALITY AGE + INVENTORY AGE stamps
✅ `/etc/update-motd.d/04-arifos-reality` — auto-runs arifos-stack on login
✅ `/etc/motd` archived as `.disabled-20260903`

## Frozen Numbers (snapshot at seal time)

```
services_running  : 84
unowned           : 68  (from reality.json SOT)
duplicates        : 2   (from reality.json SOT)
system_verdict    : WATCH
governance_verdict: WATCH
composite         : WATCH
identity_source   : /var/lib/arifos/111-identity/identity.yaml
identity_hash     : stable across runs (yaml untouched)
```

## Not Deployed (F13 Territory, requires Arif sign-off)

⏸ KVM4 (workshop, 100.64.0.5) — manifest at `cross-machine-orientation-manifest.md`
⏸ KVM2 (witness, 100.64.0.4) — same manifest, witness plane keeps passive

## Reversibility

All mutations backed up:

```
/usr/local/lib/arifos/reality.py.bak-20260903T233958
/etc/update-motd.d/04-arifos-reality.bak-20260903
/etc/profile.d/11-arifos-reality.sh.bak-20260903
/etc/motd.disabled-20260903          (renamed, not deleted)
```

## Adoption Metric (next 1-2 weeks)

```text
□ Do agents read /run/arifos/*.json before first token?
□ Do orientation questions reduce?
□ Is drift discovered faster?
□ Does receipt survive across sessions without re-discovery?
```

## Lower-Entropy Agent Behavior Contract

> Receipt bukan dashboard.
> Receipt ialah kontrak orientasi.
>
> Sebelum berfikir, baca reality.
> Sebelum mutate, baca inventory.
> Sebelum claim, semak authority.
> Jika reality tiada, jawab UNKNOWN.
> Jika inventory tidak lengkap, HOLD mutation.
> Jangan bina model dunia sendiri apabila reality.json sudah wujud.

DITEMPA BUKAN DIBERI ⚒️
