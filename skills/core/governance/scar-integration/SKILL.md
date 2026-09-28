---
name: scar-integration
id: scar-integration
version: 2.0.0-wave2-merged
description: "Capture session failure patterns as constitutional scars — reusable diagnostics that prevent repeat mistakes."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F7, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - wisdom-scar-session-audit (sha256: f168d9ddf0418241b1afabc9393573ba9ea4de65e2e438be4efb81766763586d)
wave: 2
ts: 2026-09-16T22:46:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/scar-integration/TOMBSTONE-wisdom-scar-session-audit.json
triggers:
  - "capture wisdom scar"
  - "session failure audit"
  - "scar ledger"
  - "constitutional scar"
attention:
  load_class: medium
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "scar"
    - "failure pattern"
    - "wisdom"
  output_contract:
    - "scar_receipt"
    - "scar_severity"
    - "scar_remediation"
tags: [governance, scar, wisdom, session, F2, F7, F11]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
owned_by: AAA
authority_of: AAA
---

# core/governance/scar-integration

Session failure pattern → constitutional scar promotion. Merged from wisdom-scar-session-audit per Wave 2 APEX verdict.

A scar is a reusable diagnostic that prevents repeat mistakes. Severity: P0-P4 per AGY/SCAR doctrine.

## Sc — — ar centralisation (canonical procedure)

Scars scattered across 8+ filesystem locations (`.hermes/scars/drafts/`,
`arifOS/VAULT999/scar/`, `arifOS/vault/scars/`, `AAA/scars/`, `AAA/canon/`,
`AAA/federation/...`, `forge_work/...`, `HAMPA/`) is the failure mode. The fix is
SOT centralisation by symlink, never by move:

1. **Pick one SOT.** Default: `/root/AAA/scars/` for scars, `/root/AAA/eurekas/`
   for eurekas. Anything already there wins — never overwrite an existing
   canonical entry with a symlink.
2. **Symlink, never copy.** `ln -s <satellite> <SOT>/<basename>`. Copies fork
   the truth; symlinks preserve the satellite as fossil AND make the SOT the
   single lookup surface.
3. **Idempotent + collision-skip.** If `<SOT>/<basename>` already exists (file or
   symlink), skip — the SOT already covers it. Log every decision.
4. **Verify zero dangling.** `find /root/AAA/scars /root/AAA/eurekas -maxdepth 1
   -type l ! -exec test -e {} \;` must return empty. A symlink to a missing
   file is a broken scar.
5. **Reversible by design.** Deleting a symlink leaves the satellite file
   untouched. The SOT can shrink without losing data.

Reference implementation: `/root/.hermes/scripts/sot-consolidate-scars-eurekas.sh`
+ log at `/root/.hermes/workspace/SOT_CONSOLIDATION_<date>.log`. Run once after a
new satellite-tree spawn, audit quarterly.

## Sc — — skill mapping (the integration step that closes the loop)

A scar file alone is archive, not constraint. The integration step is mapping each
scar to the skill it should harden — by trigger clause, by description line, by
runtime guard, or by skill behaviour patch. Without this step, scars accumulate
but never change behaviour; the ledger grows, the agent stays the same.

Four hardening targets, in order of cost:

1. **Static citation** — append the scar ID + one-line reason to the target
   skill's description. Cheapest. Loads when the skill loads. Catches when the
   matching skill fires.
2. **Description patch** — extend the skill's `## When to use` or `## Failure
   modes` section with the scar's constraint. Same cost, deeper coverage.
4. **Runtime guard** — write a pre-tool hook or wrapper that rejects the scar's
   failure mode (path-hallucination-guard, echo-loop-detector). Heavier; only
   when the failure mode is concrete and machine-checkable.
5. **Join table** — produce `scar-eureka-skill-join-<date>.json` with per-scar
   target_skill, severity, action_status. Audit trail for the mapping, not a
   runtime surface.

Pitfalls:

- **Cite by scar ID, not by incident narrative.** "Always validate path before
  read_file" reads as a generic reminder; "Scar SCAR-AGY-005 — reject paths with
  ≥3 consecutive repeated segments" carries the exact rule.
- **Don't cite scars the skill already covers in its body.** Search the skill
  first; strengthening an existing line beats appending a second copy.
- **Pitfall attached to step, not appended.** The scar's WHY lives with the
  step that prevents the failure, not in a separate "scar references" section.
- **Hardening a skill is never self-authorising.** The mapping is a proposal;
  ratification (when scar → skill promotion is structural) needs the same F13
  ceremony as a constitution mutation.

### Caller-chain enforcement gap (the missing third leg)

A boundary rule has **three legs** that all must be intact, or the rule is theatre:

1. **The rule** — the regex / policy / mode-cap table that says "no menus in light mode".
2. **The enforcer** — the module that strips, rejects, or caps based on the rule.
3. **The wire** — the call site that actually passes the metadata the enforcer needs.

If all three legs read green in a static audit, the rule can still fail at runtime. The
failure shape is: rule INTACT, enforcer INTACT, but the call site never populates the
metadata the enforcer reads. The enforcer then falls back to a default that is correct
only if the call site is correct — and there is no verification the call site is correct
from the static audit. Diagnose by:

1. **Grep every call site** for the metadata key the enforcer reads. `grep -rn
   'metadata\["hermes_mode"\]' /path/to/runtime/` — zero hits means wire is open.
2. **Read the function that builds metadata** at the entry point. If it composes
   `thread_id`, `hermes_profile`, and similar but never sets the mode key, the
   enforcer will silently see `None` regardless of inbound classification.
3. **Trace the mode classifier** if one exists. If `classify_mode()` returns a label
   but no caller assigns it to the source/metadata, the classifier output is dead.

The fix is **at the call site**, not the enforcer. Patching the enforcer to be stricter
when metadata is missing ("fail-safe default = strictest mode") is a useful safety net but
**NOT a root cause fix** — it over-trims legitimate messages in the modes that rely on
metadata being present. The three-leg rule:

> Static audit: rule ✓ + enforcer ✓ ≠ enforcement ✓.
> Always probe the wire, never infer it from the enforcer.

This pattern generalises: any boundary enforcement that depends on caller-supplied
metadata has the same failure mode (rate limiters without caller-supplied identity,
scope checks without caller-supplied actor, etc.). When you find it once, audit all
caller-supplied-metadata boundaries for the same gap.

### Runtime patch is not loaded patch

A patch that writes to disk is **not** the patch that runs. Two consequences:

1. **Python modules are loaded into the process heap at boot.** Editing a `.py` file
   does not change what already-loaded processes execute. Patch lands → restart
   required. Detect: `ls -la <file>.py` mtime newer than process `start_time` from
   `ps -o pid,start`.
2. **There are TWO copies of runtime source** — the live install at
   `/usr/local/lib/hermes-agent/...` and a working/upstream clone at `/tmp/...` or
   similar. Patching the clone does not patch the live install. Detect: compare mtime
   of the two copies, and `grep -n <unique_marker> /usr/local/lib/hermes-agent/...`
   vs `/tmp/.../...` to verify which one the live install actually carries.

When proposing a patch, identify which copy is the live install (whichever process is
running) and patch that copy. Patching the clone produces a green static audit and a
broken runtime — the leak then survives the audit that should have caught it.

## Sc — — retrieval discipline (opt-in only)

Retrieving a scar in real time is constitutional anchor, not auto-prepend. See
`arifos-evidence-policy` → "Scar / eureka context is opt-in" for the binding rule.
Quick reference for the scar-integration steward:

- Retrieval path: `/root/AAA/scars/<SCAR-ID>.md` (or symlink-resolved path).
- Never wire retrieval into `pre_llm_call` or any per-turn LLM hook without F13
  ceremony; the discipline section above is the law.
- Shadow observation (record what WOULD have been retrieved) is the audit
  surface; opt-in tool calls are the invocation surface.
- Hard-ban lanes (`light`, `witness`, `sado`, `homie`, `banter`) must remain
  unaffected. Recording the block is allowed; injecting wisdom is not.

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- skills/wisdom-scar-session-audit/
rm -rf skills/core/governance/scar-integration/
```

## Provenance
- **Wave:** 2, item 10
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-wisdom-scar-session-audit.md` — content absorbed from the retired `wisdom-scar-session-audit` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17). Living scar catalog: #1–#19. Latest additions are Scar #18 (Cross-Agent Artifact Verification, 2026-09-22) and Scar #19 (Person-Binding vs Pattern-Binding in Scar Records, 2026-09-22). Always read this file when the user says "capture wisdom scar", "what did we learn", "session failure audit", or when an institutional scar is being created.
