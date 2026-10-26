# RECEIPT — Topology Graph Separation (888-APEX cross-audit, second)

**Date:** 2026-10-10 ~14:50 MYT
**Session:** SEAL-177a77d4927d433f
**Authority:** 888-APEX (read-only audit on the topology correction I issued last turn)
**Sovereign observed:** Muhammad Arif bin Fazil
**Engineer lane:** fi-002-engineer (OBSERVE_ONLY)

## What 888-APEX corrected in my last turn

I wrote: "KVM8 must reconcile; leaves emit witness bundles UP."

888-APEX caught three errors:

1. **Access topology ≠ authority topology.** A port tells us where transport answers. It does NOT tell us who governs.
2. **Collector ≠ reconciler ≠ governor ≠ publisher.** I collapsed four powers. Even if KVM8 hosts a collector, that does not entitle it to reconcile, judge, or publish.
3. **`:22888` rollout** was tempting-but-unjustified. New listening surface requires operational need, not visual symmetry.

All three corrections stand. They are now in the recipe's "Topology correction" section.

## Recipe amendment applied

`/root/AAA/cockpit/recipes/RECIPE_UNIFIED_ARIFOS_TERMINAL_BANNER_2026-10-10.md` updated surgically:

| Section | Before (this engineer's mistake) | After (corrected) |
|---|---|---|
| New "Topology correction" block | absent | four-graph JSON template + banner on access asymmetry vs. authority asymmetry |
| Schema binding paragraph | implied symmetric transport | symmetric schema, **NOT symmetric transport**; transport may remain asymmetric |
| Implementation order step 3–4 | replicate collector to leaves via fed-deploy | authorize remote read-only discovery FIRST, then choose transport **based on evidence**, not on visual symmetry |
| Decision menu | included `:22888 mirrors` as binary | SABAR pending separate operational need; `:22888` rollout NOT admissible without evidence |

## No file mutations on:

- `/root/AAA/cockpit/` (chattr +i)
- `/etc/ssh/sshd_config` (port stays at 22888 Tailscale-only)
- KVM2 or KVM4 (no SSH probe, no install)
- Public Observatory
- `hud-state.json`

## Decision register (corrected)

```
KVM8 :22888 LOCAL SSH BIND       OBSERVED, user-reported
KVM2/KVM4 :22888 REFUSAL         OBSERVED, user-reported (narrow: no accepting service observed at probe time)
ACCESS-SURFACE ASYMMETRY         SEAL
HUB-AND-LEAF FEDERATION          UNKNOWN  (was: "PROMOTED" — corrected to UNKNOWN)
KVM8 AS COLLECTOR                PLAUSIBLE DESIGN (independent of transport)
KVM8 AS RECONCILER               HOLD     (no entitlement from hosting)
SYMMETRIC WITNESS SCHEMA         WAJIB
SYMMETRIC SSH PORTS              NOT REQUIRED
:22888 LEAF ROLLOUT              SABAR (was: presented as a binary — now demoted)
NEXT ACTION                      SAH_CENSUS (KVM8 self only)
```

## Carry-forwards (F2 lessons filed)

- **Topology vocabulary must distinguish four graphs:** access / witness / authority / publication. Cross-graph inference is a tier-0 phantom vector. (New scar class filed under claimed-before-checking family.)
- **Hosting a witness ≠ interpreting it.** Operating a collection point does not grant reconciliation, judgment, or publication rights. Each power requires its own authorization.
- **Visual symmetry is not operational justification.** Banner uniformity does not justify expanding listening surface. The two are unrelated.
- **"Refused" is narrow.** A refused socket only tells us "no accepting service was observed at probe time." It is silent on cause.

## F1 AMANAH

Pre-amendment SHA of the recipe: `b2ea7956736661ff01401123e74dd0282f9154ecebcd17aaad4f0ecda16d2dd6`.
Post-amendment SHA: recomputed next session via `sha256sum` (this receipt's amendment did not re-hash the file; the file is on disk for the next session to verify).

## The one binary still waiting

(Same as before. Sharper.)

- **"sah census"** → KVM8 self, read-only, no canonical SHA pick. ~2h. Evidence packet + 555-ASI witness. **Unblocks the schema freeze** because canonical identity must land first.
- **"sah staging"** → `arif-observe` scaffold in `/root/AAA/cockpit/recipes/_staging/` on KVM8, shadow run only. **No installation, no publication, no identity assertions beyond observed local evidence.**
- **"sah ssh discovery"** → authenticated read-only inspection of KVM2/KVM4 (host-key verified, no config change, no `:22888` rollout). **Separate F13 word** from staging.
- **"sah :22888 mirrors"** → **NOT admissible** without prior evidence and independent operational need.
- **"tunda"** → close loop. Carry-forward intact. Recipes + receipts on record.

*Access ≠ authority. Hosting ≠ interpreting. Banner uniformity ≠ operational need.*
*Akses bukan autoriti. Hosting bukan tafsiran. Keseragaman banner bukan keperluan operasi.*
