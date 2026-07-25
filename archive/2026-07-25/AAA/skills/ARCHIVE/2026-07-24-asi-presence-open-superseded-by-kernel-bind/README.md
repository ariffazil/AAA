# ARCHIVED 2026-07-24 — asi_presence_open

**Superseded by `kernel-bind`** (canonical, single source of truth for init).

Both `asi_presence_open` (forged 2026-07-05) and `kernel-bind` (forged
2026-07-11) targeted the same role: "single entry point that chains
constitutional skills into an auto-loading sequence before any
agent accepts work." Both replaced the same 19-skill ancestor set
(`CONSTITUTIONAL_REFLEX`, `HOST_MEMBRANE_AWARENESS`, `phase-escalation-discipline`,
`000-init-intent-classify`, etc.).

**Why kernel-bind wins:**
- Newer (2026-07-11 vs 2026-07-05)
- Three-axis schema with explicit audit_surface `['session_id', 'authority_band', 'floors_loaded', 'sovereign_id']`
- Explicit `kernel_verbs: ['arif_init', 'arif_judge']` dependency
- Cleaner trigger semantics (`session_start OR new_conversation OR resume_after_idle`)

**Path C of 2026-07-24** added `/root/scripts/federation_ritual.py` —
the canonical shell wrapper that actually calls arif_init. Both
kernel-bind and asi_presence_open documented the call; the wrapper
does the call.

Reasoning: see plan `obsidian-domino-kyle-rayner.md` in
`/root/.arifos/agents/kimi/sessions/wd_root_94a6b4475803/.../plans/`.

DITEMPA BUKAN DIBERI.
