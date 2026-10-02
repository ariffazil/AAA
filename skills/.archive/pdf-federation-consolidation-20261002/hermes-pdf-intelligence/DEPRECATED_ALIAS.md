---
name: DEPRECATED-ALIAS
description: Deprecated alias. Do not select. Routed to canonical owner. This file is a redirect only — no executable content.
canonical_owner: pdf-federation
canonical_path: /root/.hermes/skills/pdf-federation/
do_not_select: true
deprecation_reason: "13 PDF skill names collapsed to 1 canonical front door per F13 directive (2026-10-02). This folder remains for backward compatibility; no agent should select it directly."
hash_of_original: "87208163af121d1f2c2a0540a6d76f4a4cc241fbaf561f366335c8fcdd7d140a"
redirect_to: pdf-federation
---

# DEPRECATED ALIAS

This skill name has been collapsed into **pdf-federation**, the single canonical front door for all PDF capabilities in the AAA federation.

## If you reached this file via discovery

You were looking for a PDF skill. The correct destination is:

```
/root/.hermes/skills/pdf-federation/SKILL.md
```

It contains:
- A single routing matrix (`references/ROUTING.yaml`)
- One operational reference (`references/PDF_OPERATIONS.md`)
- One absorbed doctrine (`references/HERMES_PDF_INTELLIGENCE.md`)
- Three scripts: `compose_artifact.py`, `verify_artifact.sh`, `probe.py`
- One manifest schema (`references/build-manifest.v1.yaml`)
- Live capability state (`references/CAPABILITY_STATE.json`)

## What this folder contains

This folder is **deprecated**. Its scripts and references have been **copied** into `pdf-federation/` for active use. The copies here are preserved for backward compatibility but should not be edited.

**Do not select this skill directly.** If a future agent discovers this folder and selects it, the discovery rule is:

> discovery_rule: "If an agent selects any deprecated PDF skill name, route to pdf-federation"

(See `pdf-federation/references/ROUTING.yaml`.)

## Migration lineage (kept for audit)

This file was created on **2026-10-02** during the F13-mandated `0013 → 3 → 1` PDF skill federation collapse. Sequence:

1. PROBE both `/root/.hermes/skills/hermes-pdf-intelligence/` and `/root/.hermes/skills/pdf-federation/`
2. HASH their contents (this file's source: sha256 = `87208163…2911d04a`, 117 lines)
3. DIFF them — both coherent; hermes-pdf-intelligence focuses on doctrine, pdf-federation on routing
4. choose pdf-federation as canonical
5. merge unique content only
6. move doctrine → `references/HERMES_PDF_INTELLIGENCE.md`
7. preserve scripts under `scripts/`
8. create `ROUTING.yaml` + `CAPABILITY_STATE.json`
9. turn legacy paths into aliases (this file is step 9)
10. run selection test (agent picks pdf-federation, not the legacy names)
11. run compiler proof (manifest-driven build → verifier PASS)
12. only later archive old folders (after confidence)

## See also

- `pdf-federation/SKILL.md` — the canonical door
- `pdf-federation/references/CAPABILITY_STATE.json` — the migration map
- `pdf-federation/references/ROUTING.yaml` — the routing rule

---

DITEMPA BUKAN DIBERI — forged, not given. The forge was the probe; the proof is the verifier.