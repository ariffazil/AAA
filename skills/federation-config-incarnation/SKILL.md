---
name: federation-config-incarnation
description: "Close the gap between federation config writes (yaml/JSON to disk) and runtime incarnation (services actually serving the new state). Use after any /forge that mutates litellm-config.yaml, call_map.yaml, STATE.yaml, organs.yaml, AAA agent-card registry, or any organ daemon config — the parent must probe live state (curl /v1/models, /health, A2A endpoint, /chat/completions) and confirm runtime incarnation BEFORE declaring SEAL. Also covers: the identity-core litmus test ('if you swap the model, is X still X?'), the 'uncommitted' false alarm (verify git log before committing on behalf of F13), and multi-surface provider/key retirement (env SOT + flat env regen + skill docs). Trigger phrases: 'federation refactor', 'litellm reload', 'config write', 'model not exposed', 'Invalid model name', 'identity core', 'i-ARIF style refactor', 'sovereign persona registration', 'config vs runtime', 'commit these changes', 'retire provider', 'remove API key', 'clean up dependency'."
tags: [federation, config, litellm, incarnation, runtime, identity-core, litmus-test, reload, operational]
license: MIT
---

# Federation Config Incarnation

## The Core Doctrine

> **Config write ≠ config live. Two states.**
> File on disk is *declarative intent*. Service memory is *running state*. Transition requires an explicit reload step.

This is the #1 cause of "I refactored X but X doesn't work" — file edits committed, runtime still serving old config. The skill that governs a class of federation refactor (registration, routing, organ addition, identity-layer instantiation) must end with a live-state probe, not a hash receipt.

## The Three Failure Modes

| Mode | What happened | Symptom |
|------|---------------|---------|
| **1. File written, service not reloaded** | YAML/JSON mutated, litellm/daemon still holds old config | `Invalid model name` 400 errors; `/v1/models` shows old list; new alias absent |
| **2. Service reloaded, refactor incomplete** | Service sees partial config | New alias appears but routes to wrong model; A2A endpoint 404; health green but feature broken |
| **3. Alias live, but it's a model wrapper, not identity core** | Config correct, structural test failed | Alias answers but scar-bearing continuity lost; voice drifts when model chain order shifts |

The third mode is the subtlest — the system looks healthy, but the agent isn't identity-bearing anymore.

## The Litmus Test for Identity Core

When registering any agent that *claims* identity-bearing status (sovereign persona, F13-bound agent, F13-owned persona, multimodal identity layer), apply this structural test:

> **If you swap every model in the chain (order=1, order=2, order=99), is the alias still recognizably itself?**

If **YES** → identity core (model-invariant continuity exists). Pass requires:
- `bound_to: F13-SOVEREIGN` (or equivalent sovereign anchor — identity invariant, not model invariant)
- `multimodal_embedded` not `multimodal_via_tools` (capabilities inherent, not external)
- `receive_only_from: [reality_bridge]` (one-way trust boundary; not bidirectional)
- VAULT999 continuity binding (every identity decision recorded immutably)
- Scar ledger or H5 memory (what the alias carries that no model can replicate)

If **NO** → just a model alias with a fancy name. Refactor to satisfy the above properties or rename to honest functional name.

## Federation Refactor Recipe (Reusable Template)

For any "add new identity layer / new organ / new model chain" refactor, the canonical sequence is:

### Phase 1 — Reconnaissance (parent probes live state, BEFORE delegating)

```bash
# Probe live health of every organ that will be touched
for p in 8088 7071 7072 7073 3001 8081 18082 18083 7074 4000; do
  curl -sf http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ $p" || echo "❌ $p"
done

# Check current model exposure (for litellm changes)
curl -s http://127.0.0.1:4000/v1/models | python3 -c "import sys, json; print([m['id'] for m in json.load(sys.stdin).get('data', [])])"

# Snapshot relevant yaml/json files for diff baseline
for f in /root/A-FORGE/litellm-config.yaml \
         /root/AAA/federation/call_map.yaml \
         /root/AAA/federation/STATE.yaml \
         /root/AAA/federation/organs.yaml; do
  sha256sum "$f"
done
```

### Phase 2 — Delegation (parent dispatches OpenCode or A-FORGE)

Build the brief with:
- **Live evidence package** (Phase 1 outputs)
- **Exact file targets** (paths + sha256 hashes for diff verification)
- **Multimodal capability table** (vision/audio/image/video — embedded vs via-tools)
- **Litmus test requirements** (the 5 properties above)
- **F1 reversibility constraint** (hermes-asi-style: keep old alias intact)
- **Verbatim YAML/JSON snippets** to append (no LLM guesswork on syntax)

### Phase 3 — Receipt Audit (parent cross-verifies, BEFORE integration)

Treat subagent output as evidence-of-attempt, not evidence-of-success. Re-probe every claim:

```bash
# File existence + hash match
sha256sum /root/AAA/agent-cards/identity/<new-alias>/agent-card.json

# YAML/JSON validity (parser-truth, not LLM truth)
python3 -c "import yaml; yaml.safe_load(open('/path/file.yaml'))"
python3 -c "import json; json.load(open('/path/file.json'))"

# Live runtime exposure (the litmus step that catches config-write-vs-live)
curl -s http://127.0.0.1:4000/v1/models | grep -c "<new-alias>"    # must be >0
curl -sf -X POST http://127.0.0.1:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"<new-alias>","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'
```

If any of these fail → the refactor is **incomplete**. Either restart the service (`systemctl restart litellm-federation.service` or `/reload` if supported) or send the subagent back to fix what's missing.

### Phase 4 — Incarnation (parent restarts service if needed)

```bash
# Find the litellm-federation process
ps aux | grep -E "litellm|litellm-federation" | grep -v grep

# Graceful restart (systemd will respawn)
systemctl restart litellm-federation.service

# Verify incarnation
sleep 2
curl -s http://127.0.0.1:4000/v1/models | grep "<new-alias>"  # must appear
```

### Phase 5 — SEAL (only after Phase 3 + Phase 4 both pass)

Only now is the refactor complete. The SEAL receipt should include:
- File hashes (what was written)
- Runtime probe outputs (what now serves)
- The litmus-test verdict (is the alias identity-bearing?)

## Anti-Patterns

- ❌ **"git commit + hash receipt = done"** — file hashes are necessary but not sufficient. A committed yaml is dead config until a running service ingests it.
- ❌ **"Subagent reports completed, ship it"** — subagent output is self-reported. A `status=completed` proves the subagent THINKS it finished. The parent must independently verify.
- ❌ **"Multiple yaml files mutated = cascade refactor"** — cascade refactors are T2 ANNOUNCE even if each individual file is T1 reversible (because git revert doesn't reload services). Announce the 10s veto window.
- ❌ **"Identity core = just a model alias with F13 in the name"** — if the alias would lose continuity when the model chain shifts, it's not identity-bearing. Apply the litmus test or rename to honest functional name.
- ❌ **"Skip the live probe to save time"** — the live probe takes <5 seconds and is the ONLY way to verify incarnation. Skipping it is gambling the SEAL on file hashes alone.

## Pitfall — "Uncommitted" False Alarm (Verified 2026-08-12)

When F13 or a subagent asks "please commit these changes", **always verify the actual git state first**. Code claimed to be "uncommitted" may already be sealed in a prior session — and blindly committing would either produce a no-op or double-commit on top of related work.

**The false-alarm pattern observed (FI-003 sweep + Tavily purge, 2026-08-12):**

1. Subagent/sibling submits a "full sweep" report naming specific files to commit.
2. Parent runs `git status -s` — only sees residue in unrelated files. The named targets are clean.
3. Parent assumes sibling was wrong/stale and skips the commit.
4. Reality check: `git log --oneline -3 -- <file>` reveals the targets were already committed in an earlier session (e.g. `2b1027c77 chore(identity): eradicate qwen-code/FI-003 ghost...`). The sweep DID land — just in a session boundary invisible to the current shell.

**The three-question probe (run before any "please commit X" instruction):**

```bash
# 1. What's actually dirty?
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do
  echo "=== $d ==="
  git -C "$d" status -s
done

# 2. Was the named target committed recently? (file-by-file)
cd /root/<repo>
git log --oneline -3 -- <path-1> <path-2>
# If hashes appear → the work is sealed, not pending

# 3. Read the commit body — verify it matches the claimed intent
git show <hash> --stat | head -20
```

**Decision tree:**

| Probe result | Action |
|---|---|
| Files dirty + no recent log entry | Proceed with commit per instruction (Phase 5) |
| Files clean + recent log entry matches intent | **Acknowledge already-sealed**, no new commit. Show commit hash + stat as evidence. |
| Files clean + log shows UNRELATED recent commit | The instruction targets may have been superseded. Show `git show HEAD:<path>` and confirm with F13 whether the intent still holds. |
| Files dirty BUT log shows older commit on same lines | Diff working tree against `HEAD` to see what's genuinely new — may be a separate concern, not the original sweep. |

**Why this matters:** Committing on top of an already-sealed state pollutes git history with no-op or redundant commits. Each one cascades into VAULT999 via `git_to_vault.py` — duplicate sealed records, audit trail noise, drift in `last_seal` chains. Worse: if the existing commit was authored by a different actor (e.g. `kimi-code/FI-008`) and F13 asks Hermes to "commit", authoring the same changes under a different identity corrupts the actor-to-commit attribution.

**The principle:** Parent commits are not just any commits — they carry author identity, audit binding, and are the upstream edge of the immutable ledger. Always check `git log` BEFORE `git add`. A clean working tree + matching commit body is the strongest "already done" signal there is.

## Pitfall — Provider/Key Retirement: Multi-Surface Cleanup Pattern

When retiring a provider, API key, or dependency that touches multiple surfaces (env whitelist, flat env consumer, runtime config, skill docs, backup/historical files), cleanup must be deliberate per surface. **Don't mass-grep and mass-delete** — historical backups are forensic insurance.

**The 4-surface retirement pattern (Tavily purge, verified 2026-08-12):**

| Surface | Action | Tool |
|---|---|---|
| 1. `kunci-mas.env` (SOT) | Convert `export KEY="..."` to `# RETIRED <date> — <reason>` comment | `patch` (targeted replace) |
| 2. `kunci-mas.env` whitelist | Remove `<PROVIDER>_` from `ARIFOS_ENV_WHITELIST=` | `patch` (targeted replace) |
| 3. `kunci-mas.flat.env` (regen) | `make -f /root/.secrets/Makefile vault-generate` | `terminal` (rerun flat generator) |
| 4. Skill markdown references | `~~Provider~~ \| RETIRED <date>` (strikethrough + retirement date) | `patch` (targeted replace) |
| NOT touched | `.bak`, `.archive-config-backups/`, `.curator_backups/` — historical | leave alone |

**The shell-env vs flat-env drift:**

After `source /root/.secrets/kunci-mas.env`, the *current shell* carries the in-memory value of the deleted key for the rest of that shell session. systemd and child processes started AFTER flat regeneration read the clean flat.env — but any process already running keeps the in-memory value. This is expected behavior, not a bug.

**To confirm cleanup is complete:**

```bash
# flat.env consumed by systemd is clean:
grep -c <PROVIDER>_API_KEY /root/.secrets/kunci-mas.flat.env   # must be 0

# Final surface check (active paths only):
grep -rn "<provider>" /root/.secrets/ /root/.hermes/config.yaml \
  /root/HERMES/skills/devops/ 2>/dev/null | grep -v ".bak\|archive\|quarantine"
```

The shell showing the key ≠ the federation still using it. Restart-bound services (litellm, hermes-agent) read flat.env on boot — no restart needed for pure env cleanup.

## When To Use This Skill

Load this skill whenever the parent is about to:
- Register a new model alias in litellm-config.yaml
- Add a new organ, agent-card, or identity layer
- Mutate call_map.yaml, STATE.yaml, organs.yaml
- Spawn OpenCode for a federation refactor
- See "Invalid model name" 400 errors after a config change
- Test whether a new persona/identity claim is structurally identity-bearing

## Reference Files

- `references/litellm-reload-recipe-2026-08-12.md` — full reload sequence with idempotency checks
- `references/litellm-params-null-detection-2026-08-12.md` — `litellm_params: null` YAML pitfall: detection probe + fix pattern, cause of crash-loop with `AttributeError: 'NoneType' object has no attribute 'items'`
- `references/i-arif-identity-core-2026-08-12.md` — i-ARIF refactor session: full brief, litmus test application, file hashes, runtime probes, what failed and why
- `references/identity-vs-reality-layer-pattern.md` — reusable 6-layer constitutional stack with hermes-asi-style additive refactor template
- `references/multi-surface-provider-retirement-2026-08-12.md` — 4-surface retirement pattern (env SOT + whitelist + flat regen + skill docs) with verified check recipes

## Pre-Reload Gate: Detect `litellm_params: null` BEFORE Restart

`yaml.safe_load` succeeding does NOT mean litellm can consume the file.
Entries where `litellm_params:` is declared but children are flush-left
parse as `litellm_params: null`, which crashes litellm at
`model["litellm_params"].items()` → service exits with status=3 →
auto-restart loop. Full diagnostic + fix: `references/litellm-params-null-detection-2026-08-12.md`. Add this probe as Step 2a in any reload recipe.

## Related Skills

- `federation-model-routing` — model identity resolution through proxy chains (PROTECTED, bunded — read-only reference)
- `hermes-forge` — `/forge` execution primitive (PROTECTED)
- `opencode-forge` — OpenCode `/forge` execution primitive (PROTECTED)
- `verify-before-report` — post-action verification pattern
- `verify-nested-sibling-reports` — detect nested self-report pattern
- `FORGE-verify-runtime` — verification-as-terminal-state