# arifOS Orientation Layer — Cross-Machine Deployment Manifest

Status: **REVIEW ONLY** — No deployment executed. Awaiting Arif sign-off.

## Goal

Every KVM machine (KVM8 court, KVM4 workshop, KVM2 witness) should expose the same
5-file orientation layer at `/run/arifos/`:

```
reality.json      (already exists on all 3 — from reality.py)
authority.json    (NEW — derive from identity.yaml)
inventory.json    (NEW — services + ports + containers)
attention.json    (NEW — top_3 hand-curated)
verdict.json      (NEW — system vs governance split, no magic numbers)
```

Plus:

```
reality.banner    (already exists on KVM8 — human-readable 6-block receipt)
```

## Files to Deploy (3-node identical)

Source: KVM8 `/usr/local/lib/arifos/` (the implementation is node-agnostic).

```
/usr/local/lib/arifos/authority.py
/usr/local/lib/arifos/inventory.py
/usr/local/lib/arifos/attention.py
/usr/local/lib/arifos/verdict.py
/usr/local/lib/arifos/banner.py

/usr/local/bin/arifos-authority
/usr/local/bin/arifos-inventory
/usr/local/bin/arifos-attention
/usr/local/bin/arifos-verdict
/usr/local/bin/arifos-receipt
/usr/local/bin/arifos-stack
```

Total: 11 files. ~14 KB code.

## Per-Node Identity.yaml (current state — read-only, do not modify)

| Field | KVM8 | KVM4 | KVM2 |
|---|---|---|---|
| `node_id` | KVM8 | forge-core | KVM2 |
| `ARIFOS_NODE_NAME` | (missing) | forge-core | (missing) |
| `role` | institutional_substrate | execution-core | witness_plane |
| `authority_class` | canonical | worker | projection |
| `canonical_owner` | KVM8 | court-core | KVM8 |
| `mesh_ip` | 100.64.0.2 | 100.64.0.5 | 100.64.0.4 |

authority.py is **already tolerant** of all 3 schemas (KVM4 dual-key handled).

## MOTD Patches (already applied on KVM8)

```
/etc/update-motd.d/04-arifos-reality    → call arifos-stack
/etc/profile.d/11-arifos-reality.sh     → cat reality.banner
/etc/motd                              → archived as .disabled-20260903
```

These need equivalent application on KVM4 and KVM2 if Arif wants login banner
on those nodes. **NOT recommended** for KVM2 (witness plane — keep passive).
**Recommended** for KVM4 (workshop — agents work there).

## Risks

1. **Cross-machine SSH deploy** — F13 territory. Arif must authorize.
2. **MOTD scripts on KVM2** — witness plane philosophy: don't render banners.
   Receipt may exist as JSON but no MOTD layer.
3. **Authority.json drift** — if KVM4 modifies identity.yaml, authority.json
   follows. This is intentional (yaml is SOT). But agents must trust yaml, not
   authority.json, for canonical naming.

## Reversibility

Every file has timestamped backup (KVM8 pattern):
```
/usr/local/lib/arifos/reality.py.bak-YYYYMMDDTHHMMSS
/etc/update-motd.d/04-arifos-reality.bak-YYYYMMDD
/etc/profile.d/11-arifos-reality.sh.bak-YYYYMMDD
```

## ZEN Audit

```
New daemons      : 0
New databases    : 0
New frameworks   : 0
New agents       : 0
New code total   : ~14 KB across 5 generators
Compatibility    : KVM8 ✓, KVM4 (yaml schema) ✓, KVM2 (yaml schema) ✓
Adoption metric  : do agents read /run/arifos/*.json after first token
```

DITEMPA BUKAN DIBERI ⚒️
