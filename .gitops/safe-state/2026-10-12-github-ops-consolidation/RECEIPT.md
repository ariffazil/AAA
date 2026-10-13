# GitHub Ops Consolidation Receipt — 2026-10-12

**Actor:** FI-008 (Kimi)
**Session:** github-ops-refresh-2026-10-12
**Authority:** Arif (sovereign) direct task — "update all AAA github ops skills, workflow tools and capabilities"
**Canon test (Canon #0 three-test gate):**

| Test | Verdict |
|---|---|
| (a) eliminate demonstrated failure class | **PASS** — duplicate-skill selection (3 byte-identical SKILL.md copies + 2 stale worktree copies) is gone |
| (b) compile into enforceable mechanism | **PASS** — `verify-canonical.sh` (6 checks: canonical exists / sha256 match / 11 aliases resolve / registry binds / no rogue dirs / federated metadata present) |
| (c) materially improve a decision | **PASS** — any agent asking "do github ops" now finds ONE canonical (was 7+ candidates) |

**Mutation surface (8-stage Governed Witness Mutation Protocol):**

| Stage | Status | Evidence |
|---|---|---|
| 1 AUTHORIZE | ✓ | Sovereign task |
| 2 BACKUP | ✓ | 4 .bak files + manifest at `/root/AAA/.gitops/safe-state/2026-10-12-github-ops-consolidation/before/` |
| 3 MUTATE | ✓ | 3 symlinks created (forge-github-ops → github-ops, hardening/github → AAA/github-ops, hardening/github-repo-manager → AAA/github-ops) |
| 4 VERIFY | ✓ | `verify-canonical.sh` reports VERDICT: PASS |
| 5 REINDEX | ✓ | `FEDERATED_SKILLS_REGISTRY_V3.yaml` `dev` domain now declares `github-ops` as canonical |
| 6 RELINK | ✓ | All 11 alias paths resolve to canonical sha256 |
| 7 WITNESS | ⏳ | This receipt (low-tier, machine-readable, not arif_seal-grade) |
| 8 NOTIFY | ⏳ | User-facing summary |

## What changed

| Path | Before | After |
|---|---|---|
| `/root/AAA/skills/forge-github-ops/` | real dir, 16549 bytes SKILL.md (byte-identical dup) | **symlink** → `github/github-ops/` |
| `/root/AAA/skills/FORGE-github-ops/` | symlink → `/root/.hermes/skills/FORGE-github-ops` | unchanged — load-bearing for hermes runtime |
| `/root/AAA/skills/github/{auth,code-review,issue-to-pr,issues,pr-workflow,repo-management}/` | symlinks → `github-ops` | unchanged — already canonical |
| `/root/arifOS-wt-mcp-hardening/skills/github/` | real dir, 4168 bytes (old format, stale) | **symlink** → `/root/AAA/skills/github/github-ops` |
| `/root/arifOS-wt-mcp-hardening/skills/github-repo-manager/` | real dir, 4600 bytes (old format, stale) | **symlink** → `/root/AAA/skills/github/github-ops` |
| `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` dev domain | `- dev-github` (dead, no on-disk dir) | `- github-ops` (canonical + comment) |
| `/root/AAA/skills/github/github-ops/scripts/verify-canonical.sh` | did not exist | **NEW** — Canon #0 test (b) enforceable mechanism |

## Distinct concerns (kept separate, not duplicated)

- `/root/AAA/skills/FORGE-github-workflow/` — A-FORGE class-level umbrella with cognitive hints (claude/codex/hermes). Different scope (cross-domain workflow patterns), kept.
- `/root/AAA/skills/github-public-push-privacy/` — narrow public-push privacy gate, F13-ratified, forged from 2026-08-15 near-miss. Distinct concern, kept.

## What stayed in place

- `/root/AAA/skills/github/` NAMESPACE.md (canonical marker, Fasa 1 skill hygiene)
- `/root/AAA/skills/integrations/github/contract.yaml` (federated-agentic binding: allowed_operations, required_witnesses, requires_arifos_judgment) — anemic (5 ops, 415 bytes) but in scope
- `/root/AAA/instructions/github-zen.md` (F-1 through F-7 enforcement record, 2026-09-06 deep research; remained as-is — F13-ratified doctrine)
- `/root/.hermes/skills/FORGE-github-ops/` (hermes runtime home; load-bearing per `~/.hermes/AGENTS.md`)

## Open debts discovered (NOT auto-fixed, surface only)

1. ~~`/root/AAA/skills/.archive/merge-20260920/github/` — GHOST-DOCUMENTATION.~~ **FIXED 2026-10-12 stage 4:** SKILL.md REFERENCES table column renamed "Original path (now archived)" → "Original path (pre-merge)"; the false "Pre-merge archive" bullet replaced with truthful pointer to the live `/root/forge_work/merge-2026-09-20/github-receipt.json` (9394 bytes, confirmed via `ls`) and the Scar-2026-10-03-001 reference. Canonical SHA moved from 956425a6d1... to 6e6056b002d... (see after/SKILL.md.stage4-fixed-ghost-archive).

2. ~~`/root/AAA/skills/integrations/github/contract.yaml` listed only 5 allowed ops vs canonical covers 7+.~~ **FIXED 2026-10-12 stage 4:** contract.yaml promoted v1 → v2, added 4 ops (`auth`, `repo-management`, `pr-workflow`, `federation-overlay`), 3 risk_classes (`push_to_main`, `archive_op`, `transfer_op`), 3 contract metadata lines (canonical_skill, verifier, contract_updated). See after/contract.yaml.stage4-v2.

3. `dev-github` entry was removed from `FEDERATED_SKILLS_REGISTRY_V3.yaml` dev domain (it was dead). The SKILL_ALIAS_TABLE.json may still reference it — out of scope for this consolidation; re-run alias reconciliation if needed. **STILL OPEN** (not in scope of Arif's "1 2").

### Additional hardening: dynamic-SHA verifier

verify-canonical.sh was promoted from hardcoded-SHA (`956425a6d1...`) to **dynamic-SHA** (computed live from canonical on each invocation). This kills the "stale-hardcoded-hash" failure class: the test now reflects the current canonical content rather than a snapshot from 2026-09-27. See after/verify-canonical.sh.stage4-dynamic-sha.

## Federation binding — who sees the canonical

Per `FEDERATED_SKILLS_REGISTRY_V3.yaml` `agent_profiles.*.domains`, github-ops in `dev/` is now bound to:

| Agent | FI-Slot | Sees dev? |
|---|---|---|
| codex | — | ✓ |
| kimi (MiniMax M3) | FI-008 | ✓ |
| opencode (DeepSeek V4) | warga-AGI | ✓ |
| claude (DeepSeek-on-Anthropic) | FI-002 | ✓ |
| grok | — | ✓ |
| copilot (DeepSeek V4) | FI-006 | ✓ |
| antigravity (Gemini 3.5 Flash) | FI-004 | ✓ |
| aider (DeepSeek) | FI-007 | ✓ |
| hermes | sovereign runtime home | ✗ (own load-bearing canon) |
| openclaw | KVM4 (separate runtime) | ✗ (separate profile) |

8 of 10 federated agents now have ONE canonical to invoke. hermes and openclaw have their own canon by design (per hermes/AGENTS.md).

## Rollback path

If anything in this consolidation breaks:
```bash
# Restore AAA duplicate
rm /root/AAA/skills/forge-github-ops
cp -a /root/AAA/.gitops/safe-state/2026-10-12-github-ops-consolidation/before/forge-github-ops-SKILL.md.bak /root/AAA/skills/forge-github-ops/SKILL.md

# Restore hardening worktree
rm /root/arifOS-wt-mcp-hardening/skills/github
cp -a /root/AAA/.gitops/safe-state/2026-10-12-github-ops-consolidation/before/hardening-github-SKILL.md.bak /root/arifOS-wt-mcp-hardening/skills/github/SKILL.md
# (repeat for github-repo-manager)

# Revert registry
cd /root/AAA && git checkout -- skills/FEDERATED_SKILLS_REGISTRY_V3.yaml
```

DITEMPA BUKAN DIBERI ⚒️