---
name: eureka-profile-lane-scope-2026-09-27
description: Profile-to-lane binding contract extracted from nabilah persona decomposition (F13 SEAL 2026-09-27)
metadata:
  type: eureka
---

# EUREKA — Profile = Lane Scope Contract (Nabilah decomposition 2026-09-27)

## Provenance

Source artifact: `/root/.hermes/profiles/nabilah/` (decommissioned F13 directive 2026-09-27). The nabilah profile carried a non-obvious pattern: profile → lane binding via `_profile_scope.py` lines 58-62:

```python
"nabilah": {
    "id": "nabilah",
    "lanes": ["nabilah"],
    "profile_dir": "/root/.hermes/profiles/nabilah",
}
```

This is not a config field — it is a **routing contract**: the profile declares which lanes it serves, and the gateway routes intent → profile via lane key.

## Why this is doctrine-grade (not config)

1. **Non-obvious:** A profile could trivially be a flat config blob. The lane binding makes it a **scope-routing unit**.
2. **Project-level:** Affects how every federation organ registers multi-lane agents.
3. **Survives 24-month test:** Routing keys must outlive any single profile instance.
4. **Architecture-changing:** If a profile carries lanes, then decommissioning a profile = unregistering its lane (runtime impact), not just deleting files.

## Promotion

Promote to AAA doctrine: **EVERY profile = scope contract, not config stub.** A profile MUST declare:
- `id` (canonical name)
- `lanes` (routing keys it serves)
- `profile_dir` (runtime root)
- `federation_role` (witness / builder / judge / executor)
- `sensitivity` (F1-F13 floors it binds to)

Decommissioning a profile = (a) move profile_dir to `_archive/`, (b) unregister from `_profile_scope.py`, (c) revoke lanes from any active router. Order matters: archive first, then unregister (so any in-flight routing fails-closed, not fails-open into a missing dir).

## Why:** Profile-lanes contract is non-obvious enough to recur as an anti-pattern (orphan profiles with active lanes), survives 24 months because routing is perma-layer, architecture-changing because it bridges profile-registry to gateway-router.

**How to apply:** When registering a new profile in any organ, require the 5-tuple above. When decommissioning, execute the (a)(b)(c) sequence. Never delete a profile before unregistering its lanes.

---

# EUREKA — Bundled Skills Manifest Pattern (Nabilah decomposition 2026-09-27)

## Provenance

Source artifact: `/root/.hermes/profiles/nabilah/skills/.bundled_manifest` (282 entries, gitignored at `nabilah/`). 1136 of 1144 files in nabilah's profile were *bundled shared skills* (sha256-pinned references like `AAA-asr-glm-ingest:38863c3c7fbbcc181f635d2fcfe436f6`), not nabilah-specific.

## Why this is doctrine-grade

1. **Non-obvious:** A profile's bulk content can be *other* profiles' skills. Means profile ≠ monolithic blob.
2. **Project-level:** Affects how skills registry and profile registry intersect.
3. **Survives 24-month test:** Cross-profile skill references must outlive any single profile.
4. **Architecture-changing:** Profiles become *composable* if they declare what they bundle.

## Promotion

Promote to AAA skills doctrine: **Profile = composition of bundled skills + persona-specific content.** A profile MUST separate:
- `skills/.bundled_manifest` — sha256-pinned cross-profile references (shared)
- persona files (`SOUL.md`, `MEMORY.md`) — profile-specific
- runtime state (caches, sessions) — ephemeral, gitignored

Bundled manifest is the **cross-profile skill truth table**: when a profile is decommissioned, the manifest entries remain valid (skills still served from origin profile); only the *consumer* reference is dropped.

## Why:** Manifest-as-skill-truth-table makes skill distribution auditable (every sha is content-addressed) and reversible (decommissioning a profile doesn't delete the skills it consumed, only the consumption reference).

**How to apply:** Every new profile MUST emit a `.bundled_manifest` listing sha256 of every bundled skill. AAA skills registry validates manifests on profile registration. See [[eureka-profile-lane-scope-2026-09-27]] for the profile-lanes contract that this builds on.

---

# EUREKA — Generalized RPH Generator (KSSR Curriculum Scaffold)

## Provenance

Source artifact: `/root/.hermes/profiles/nabilah/skills/nabilah-rph/SKILL.md`. Working daily-6:30-AM RPH generator for primary English teaching (Darjah 1, 3, 4 — KSSR curriculum, Malaysia MOE).

## Reusable substrate (extracted, persona-stripped)

The *generator logic* — not the persona binding — is reusable for any education-domain agent:

1. **Parallel multi-year-group generation** — single skill produces 3 lesson plans (3 age groups) in one pass.
2. **ISO week % N rotation** — deterministic topic bank cycling (`% 8` for 8 topics × 3 year groups = 24-day rotation).
3. **KSSR structure** — `Set Induksi → Langkah → Penutup + SK/SP + BBM + refleksi` is the Malaysian MOE RPH schema; reusable as `moe_rph_v1` schema.
4. **CEFR alignment check** — year-group → CEFR level mapping (Darjah 1 = Pre-A1, Darjah 3 = A1, Darjah 4 = A2).

## Promotion

Generalize to **`aaa-rph-generator`** skill (cross-organ, persona-agnostic). Strip teacher-name binding, keep schema + rotation logic. Place at `/root/AAA/skills/aaa-rph-generator/SKILL.md` so any federation agent (GEOX pedagogics, WELL education lane, etc.) can consume it.

## Why:** A working curriculum generator with KSSR schema + ISO-week rotation is a reusable substrate for any primary-education deployment, not a one-off teacher persona. The persona is consumable; the generator is portable.

**How to apply:** Extract `moe_rph_v1` schema from `nabilah-rph/SKILL.md` lines 11-44 (Darjah 1/3/4 weekly topic banks). Strip teacher binding. Publish as `aaa-rph-generator` in AAA skills catalog with `federation_role: builder`, `sensitivity: F5_PROTECTED` (children's education data).