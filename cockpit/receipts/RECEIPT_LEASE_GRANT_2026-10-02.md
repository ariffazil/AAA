# RECEIPT — Cockpit Lease Grant (F13-class, 2026-10-02)

**Lease file:** `/root/AAA/cockpit/.lease`
**F1 hash:** `be5631b057ad7432d144549ccd7557f9de0a5ae2223426b50ccf04fc01115e35`
**Schema:** `cockpit-lease-v1`

## Sovereign signal pathway (audit trail)

| Turn | Word | Meaning |
|---|---|---|
| T1 | "lease" | chose `full` mode (5 fields, one per turn) |
| T2 | "full" | explicit ratification request — default fields disclosed |
| T3 | "sah" | ratification (Malay: ratify/affirm) |
| T4 | "forge" | execution command |

## Lease terms

| Field | Value |
|---|---|
| holder | arif (sovereign) |
| path_scope | /root/AAA/cockpit/ |
| excludes | /root/AAA/VAULT999/, /root/AAA/cockpit/receipts/ |
| duration | this session |
| revoke | arif (one word: "revoke lease") |
| rule | exclusive (only holder may write) |
| authority_band_at_grant | OBSERVE_ONLY (unchanged — lease does not promote authority) |

## Reversibility

Full. Single command: `rm /root/AAA/cockpit/.lease`. No data touched outside cockpit/.

## What this lease does NOT do

- Does not promote me from OBSERVE_ONLY to ACT.
- Does not fix actor_crypto=NO (that requires sovereign signal on a different F13 binary).
- Does not authorize writes outside /root/AAA/cockpit/.
- Does not authorize writes to receipts/ subdir (that's pinned/operational).

## What this lease DOES do

- Declares machine-verifiable that the sovereign is the only legal writer to /root/AAA/cockpit/.
- Blocks concurrent writes from other agents until revoke.
- Makes HUD `active_lease` field display `arif (exclusive)` instead of `unknown`.

## F1 integrity verified

Body SHA256: `be5631b057ad7432d144549ccd7557f9de0a5ae2223426b50ccf04fc01115e35`
Integrity hash: same. Pass.

## Backups

- `/root/AAA/cockpit/hud-state.json.bak-lease-20261002T002142Z`
- `/root/AAA/cockpit/execution-path-next.json.bak-lease-20261002T002142Z`
- `/root/AAA/cockpit/display-hud.sh.bak-lease-20261002T002142Z`
