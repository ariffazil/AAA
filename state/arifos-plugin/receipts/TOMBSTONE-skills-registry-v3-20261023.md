# TOMBSTONE (POINTER) — FEDERATED_SKILLS_REGISTRY_V3.yaml · 2026-10-23

> Kaedah POINTER dipilih F13 ("sah semuanya go" item 2, 02:17:41Z). Fail asal dalam pokok beku
> `/root/AAA/skills/` TIDAK disentuh. `/root/AAA/docs/deprecation-registry.json` juga beku
> (EPERM OBS) — penanda ini di `state/` adalah inventori tombstone sehingga registry boleh menerima.

- **Sasaran:** `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` (declare 255 skills vs 778 live, refresh 2026-09-19)
- **Consumer hidup (kedua-duanya selamat):** `skills-declaration-gate.py:40` (graceful-skip bila fail tiada) · `zen-reconcile.sh:33` (tombstone-guard dipasang 2026-10-23, backup .bak-arifcore-20261023)
- **Pengganti:** census `federation_build.py` → `state/arifos-plugin/capabilities/skill-index.generated.json` + `receipts/drift.generated.json`
- **Rollback:** buang fail ini sahaja (fail asal tak pernah berubah)
- **Fizikal retire fail asal:** menunggu ruling beku fail-tunggal (sama dengan item F13 lama)

Dicatat: 333-AGI · jejak: decision_ledger.jsonl 02:17:41Z · resit: plugin-alignment-2026-10-23.md
