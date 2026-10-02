# RECEIPT — HUD Substrate Panel (P1 Fresh-Agent Gap Closure)
**Date:** 2026-10-01T21:48:34Z
**Lane:** B (autonomous, additive, reversible)
**Prior:** [receipt: /root/AAA/cockpit/receipts/RECEIPT_HUD_FRESH_AGENT_2026-10-02.md]

## P1 gaps closed
1. **canonical_paths** vs **sealed_paths** — fresh agent can now see which are mutate-with-authority vs read-only-append-only
2. **runtime vs source SHA drift** — scar-bound; arifOS=match (800eb0ae0), geox/a-forge=no-comparable (one not git-tracked)

## Live values (verified)
| Field | Value | Source |
|---|---|---|
| substrate.drift_count | 0 | arifOS match; geox/a-forge no-comparable |
| substrate.canonical_paths | 10 paths | organs.yaml + path_class map |
| substrate.sealed_paths | 2 (VAULT999, BACKUPS) | organs.yaml + path_class map |
| arifOS source_sha | 800eb0ae0 | git -C /root/arifOS |
| arifOS runtime_sha | 800eb0ae0 | git -C /opt/arifos/app (finds parent /opt/arifos/.git) |
| geox source | no-git | /root/GEOX not git repo |
| geox runtime | 7027ff64 | /opt/geox git-tracked |
| a-forge both | no-git | /opt/a-forge/app no .git found |

## Path classification (the authority surface)
- canonical: /root/AAA{,/cockpit,/federation,/data,/governance,/audits}
- source-only: /root/arifOS
- live-binary: /opt/{arifos/app, a-forge/app, geox}
- sealed: /root/VAULT999 (symlink → /root/arifOS/VAULT999 — chmod 777 ⚠️ held)
- backup: /root/BACKUPS
- scratch: /root/forge_work (NOT yet surfaced; held)
- quarantine: /root/._litter-archive (active; lease=true)

## Discovery (scar-bound)
- arifOS runtime IS git-tracked at /opt/arifos/.git (parent of /opt/arifos/app)
- SHA coincidentally matches /root/arifOS — both at 800eb0ae0 today
- Future drift possible: only verified today, not assumed persistent

## F1 / F7 compliance
- All values from live probes, no narrative smoothing
- Hash: a397aa78a5ff98e0654eab6edeb173f92871fe415b9d5c456e6697acd30a2ec7
- Reversibility: additive — remove `substrate` key from HDR panels [3]

## Held (sovereign lane, F13)
- Why VAULT999 perm=777 (sealed but world-writable ⚠️)
- Why geox source is not git-tracked (or is there a /root/GEOX/.git somewhere?)
- Surface scratch_paths (forge_work) in next iteration

[receipt: /root/AAA/cockpit/hud-state.json]
[receipt: /root/AAA/cockpit/receipts/RECEIPT_HUD_SUBSTRATE_2026-10-02.md]
