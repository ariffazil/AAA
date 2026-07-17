# Reflective Agent Skills — Index

**Canonical name:** `reflective-agent-skills`
**Version:** 1.0.0
**Forged:** 2026-07-05 by FORGE (000Ω) under F13 SOVEREIGN directive
**Status:** PROPOSED → ACTIVE after OpenCode + AAA repo wire-up
**Seal:** `AAA_REFLECTIVE_SKILLS::v1.0::2026-07-05T07:50Z`

> **Purpose.** Close the constitutional gap where subagents inherit doctrine blindly from the parent. This index maps every reflective skill to the existing skill that already implements it, identifies the gaps, and provides the loading contract for any agent waking on AF-FORGE.

---

## The 13 Reflective Skills — Index

Organized by phase of an agent's life. Each row shows: (a) what it does, (b) which existing skill already does this, (c) status.

| Phase | ID | Skill | Implements via | Status |
|-------|----|-------|----------------|--------|
| META | **S00** | `reflective_self_check` | `shadow-diagnostic` (3-question shadow check) + `CONSTITUTIONAL_REFLEX` (one-shot arc) | EXISTING |
| BOOT | **S01** | `constitution_load` | `ZEN_ORGANS` (7 organs) + `AGENTS.md` heptalogy | EXISTING |
| BOOT | **S02** | `identity_bind` | `arif-agent-bootstrap` (10 cards) + `aforge-execution` | EXISTING |
| BOOT | **S03** | `session_ignite` | `000-init-intent-classify` + `FORGECODE-Autonomous-Init` + `arif_init` MCP | EXISTING |
| BOOT | **S04** | `sovereign_recognize` | **`sovereign-recognize`** (newly forged) | **NEW** |
| SENSE | **S05** | `route_least_power` | `route-least-power` (literally named) | EXISTING |
| SENSE | **S06** | `caller_trace` | **`caller-trace`** (newly forged) | **NEW** |
| SENSE | **S07** | `capability_map_read` | `tools-embodiment-application` + `mcp-mastery` | EXISTING |
| REASON | **S08** | `evidence_tag` | `111-sense-evidence-observe` + `geox-epistemic-ladder` | EXISTING |
| REASON | **S09** | `verdict_grammar` | `888-judge-verdict-render` (SEAL/HOLD/VOID etc.) | EXISTING |
| JUDGE | **S10** | `two_phase_commit` | `010-forge-execute-warrant` + `phase-escalation-discipline` | EXISTING |
| JUDGE | **S11** | `reversibility_check` | `010-forge-execute-warrant` (Reversibility table) | EXISTING |
| JUDGE | **S12** | `refusal_surface` | `shadow-diagnostic` + `zen-organ-witness` + `zen-diagnostic-probe` | EXISTING |
| SEAL | **S13** | `seal_write` | `999-vault-seal-immutable` + `vault999-integrity` | EXISTING |

**Summary:** 11 of 13 skills already exist under different names. **2 are newly forged:** S04 (sovereign-recognize) and S06 (caller-trace). The 13-skill framework is structurally complete.

---

## The Meta-Skill — S00 Reflective Self-Check

Every agent, on wake, runs an internal self-attestation before accepting work:

```
Q1: Do I know who I am?               → S02 identity_bind
Q2: Do I know what constitution I serve? → S01 constitution_load
Q3: Do I have a governed session?      → S03 session_ignite
Q4: Do I know my sovereign?            → S04 sovereign_recognize
Q5: Do I know my refusal list?         → S12 refusal_surface

If any answer is NO → refuse_task until all YES.
```

Existing implementation: **`/root/.agents/skills/CONSTITUTIONAL_REFLEX/SKILL.md`** (510 lines). It already encodes the ART → KERNEL → ACT arc that maps onto S00-S13. New agents should load it first.

---

## Two Newly Forged Skills

### SK04 → `sovereign-recognize`

**Path:** `/root/AAA/skills/reflective/sovereign-recognize/SKILL.md`

**Why new:** The existing F13 floor says "Arif holds final veto." But no skill cleanly separated "sending-as-sovereign" from "naming-the-sovereign." Without this skill, agents emit "ARIF" labels without cryptographic anchoring — which is exactly how G1 (seal actor=unknown) happened. This skill binds sovereign identity to actor_signature, not a string.

**Closes:** G1 (seal chain actor=unknown) at the structural level. Every F13-bound action must now anchor through actor_signature or REFUSE.

### SK06 → `caller-trace`

**Path:** `/root/AAA/skills/reflective/caller-trace/SKILL.md`

**Why new:** The docker-MCP scenario (5 agents, 0 tools, 30-min loop) revealed a structural gap: agents invoke tools without checking whether the call is load-bearing. `route-least-power` (S05) minimizes blast radius per call. `caller-trace` (S06) checks whether the call is needed at all.

**Closes:** the **ceremonial tool-call** failure mode — when an agent reaches for a tool because it's available, not because it's needed.

---

## Existing Skills — Where They Live

| Skill class | Canonical location | Count |
|-------------|--------------------|-------|
| Reflexive / constitutional | `/root/.agents/skills/CONSTUTIONAL_REFLEX/` | 1 |
| Constitutional stages (000-999) | `/root/.agents/skills/000-init-intent-classify/`, `/root/.agents/skills/111-sense-evidence-observe/`, `/root/.agents/skills/333-mind-plan-generate/`, `/root/.agents/skills/666-heart-critique-stress/`, `/root/.agents/skills/888-judge-verdict-render/`, `/root/.agents/skills/999-vault-seal-immutable/` | 6 |
| Zen organs (7) | `/root/.agents/skills/zen-organ-{reality,governance,civilization,execution,memory,witness,meaning}/` | 7 |
| Tri-witness | `/root/.agents/skills/shadow-diagnostic/`, `/root/.agents/skills/zen-diagnostic-probe/` | 2 |
| Boot | `/root/.agents/skills/arif-agent-bootstrap/`, `/root/.agents/skills/FORGECODE-Autonomous-Init/` | 2 |
| Routing | `/root/.agents/skills/route-least-power/` | 1 |
| Tool assessment | `/root/.agents/skills/tools-embodiment-application/`, `/root/.agents/skills/mcp-mastery/` | 2 |
| Evidence | `/root/.agents/skills/111-sense-evidence-observe/`, `/root/.agents/skills/geox-epistemic-ladder/` | 2 |
| Verdict | `/root/.agents/skills/888-judge-verdict-render/` | 1 |
| Execution | `/root/.agents/skills/010-forge-execute-warrant/`, `/root/.agents/skills/phase-escalation-discipline/` | 2 |
| Audit | `/root/.agents/skills/700-clean-audit-immune/` (if present), `/root/.agents/skills/vault999-integrity/` | 2 |
| **Total in /root/.agents/skills/** | | **~73** |

(The AAA repo `/root/AAA/skills/` has 80+ more, organ-specific. Both surfaces must sync.)

---

## Loading Contract — What Every Agent Must Do At Wake

```python
# Forge-style boot block — paste into agent's IDENTITY.md or INIT
async def wake(actor_id):
    # S03 — session ignite
    session = await arifos_arif_init(actor_id=actor_id, mode='light')
    await bind(session_id=session['session_id'])

    # S01 — constitution load (lightweight, one-shot)
    constitution = await load_skill('CONSTITUTIONAL_REFLEX')

    # S02 — identity bind
    identity = await load_skill('arif-agent-bootstrap')

    # S04 — sovereign recognize (NEW)
    sovereign = await load_skill('sovereign-recognize')

    # S12 — refusal surface
    refusal = await load_skill('shadow-diagnostic')

    # S05 — least-power routing
    routing = await load_skill('route-least-power')

    # S13 — seal authority
    sealing = await load_skill('999-vault-seal-immutable')

    # S00 — reflective self-check
    answers = {
        'who am I?': identity,
        'what constitution?': constitution,
        'governed session?': session,
        'who is sovereign?': sovereign,
        'what do I refuse?': refusal,
        'how do I route?': routing,
        'how do I seal?': sealing,
    }
    if any(v is None for v in answers.values()):
        raise WakeRefused('Self-check failed — refuse task until ALL present.')
    return WakeToken(answers=answers, session_id=session['session_id'])
```

---

## Wiring — How This Hits OpenCode Agents

| Agent | Bind skills at boot | New skills |
|-------|--------------------|-----------|
| `forge` | CONSTITUTIONAL_REFLEX + arif-agent-bootstrap + 000-init + 999-vault-seal + 010-forge-execute-warrant | sovereign-recognize + caller-trace |
| `auditor` | CONSTITUTIONAL_REFLEX + shadow-diagnostic + 666-critique + vault999-integrity | sovereign-recognize + caller-trace |
| `ops` | CONSTITUTIONAL_REFLEX + entropy-thermo-zen + federation-observability | sovereign-recognize + caller-trace |
| `planner` | CONSTITUTIONAL_REFLEX + 333-mind-plan + phase-escalation-discipline | sovereign-recognize + caller-trace |
| `text-to-image` | CONSTITUTIONAL_REFLEX (lightweight, system-prompt only) | sovereign-recognize (cheap variant) |

Implementation detail: opencode config has `instructions` (system-prompt paths) and `references` (lookups). Skills bind via `references`. Adding skills to each agent's references is the wiring step.

---

## Sync Protocol — AAA Repo ↔ OpenCode Local

```bash
# After every git pull on AAA repo, sync skills to /root/.agents/skills/
cd /root/AAA
git pull origin main
NEW=$(git diff --name-only HEAD@{1} HEAD -- 'skills/**/SKILL.md' 'skills/**/*.md')
if [ -n "$NEW" ]; then
    rsync -av --include='*/' --include='**/SKILL.md' --exclude='*' skills/ /root/.agents/skills/
fi
# Hash-verify integrity
sha256sum /root/AAA/skills/reflective/*/SKILL.md > /tmp/remote_hash
sha256sum /root/.agents/skills/*/SKILL.md  > /tmp/local_hash
diff /tmp/remote_hash /tmp/local_hash || echo "[WARN] skill drift detected"
```

The script lives at `/root/AAA/skills/reflective/sync.sh` (auto-generated next session).

---

## Sealing — What This Artifact Becomes

This index is the canonical S00 entry point. The 13 row map is the boot contract. The 2 new SKILL.md files are the gap-fill. Together they compose into:

```
seal_id      : AAA_REFLECTIVE_SKILLS::v1.0::2026-07-05T07:50Z
witnesses    : FORGE (000Ω) proposer, AAA repo (canon), OpenCode (consumer)
cadence      : reviewed weekly, sealed monthly
next_review  : 2026-07-12 (weekly)
stable_until : 2026-08-05 (monthly seal)
supersedes   : 13-skill proposal without gap-fill analysis
```

---

*Forged: 2026-07-05 by FORGE (000Ω) under F13 SOVEREIGN directive*
*Heritage: shadow-diagnostic (LLM alignment research), CONSTITUTIONAL_REFLEX (arifOS doctrine)*
*DITEMPA BUKAN DIBERI — Reflection is forged, not inherited.*
