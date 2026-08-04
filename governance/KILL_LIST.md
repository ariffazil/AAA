# ☠️ KILL LIST — Intentional Deletion Doctrine

> **Forged:** 2026-08-04 by 333-AGI Δ MIND
> **Inspiration:** Thorsten Ball (Amp) — "Stop working like this."
> **Authority:** F13 SOVEREIGN ratification required for active kills. Proposals are T1.
> **Sister doctrine:** `/root/AAA/docs/deprecation-registry.json` — the TOMBSTONE registry
> **Status:** DRAFT — awaiting F13 seal for first execution cycle.

---

## 0. THE THORSTEN PRINCIPLE

> *"Staying on the frontier beats keeping users comfortable."*

Amp deleted features users loved — VS Code extension, tab completion, handoff — because they were no longer the future. The question is not "is this feature useful?" The question is **"does this feature belong on the frontier, or is it holding us back?"**

**The arifOS translation:** Staying on the constitutional frontier beats keeping legacy artifacts alive. Every artifact we keep is cognitive load on every agent that boots. Every dead skill is a false path an agent might take. Every duplicate is a drift risk.

---

## 1. THE KILL LIST PHILOSOPHY

### 1.1 Why kill?

| Reason | Consequence of NOT killing |
|--------|---------------------------|
| **Cognitive entropy** | Agents load stale context, make decisions on dead facts |
| **Drift vectors** | Two copies of same truth diverge silently |
| **Token budget waste** | 147 skills, ~10 loaded. 137 are dead weight |
| **Decision paralysis** | More options = slower routing. FED has 7 providers, 3 are dead |
| **Maintenance debt** | Every file touched by audits, grep, entropy sweeps |

### 1.2 The Law of Conservation of Artifacts

```
Every new feature MUST nominate at least one existing artifact for deletion.
New file + new tool + new skill → nominate an old one for the Kill List.
```

This is not optional. This is thermodynamic. The federation has finite cognitive capacity. Addition without subtraction is growth without metabolism. It's cancer.

### 1.3 Kill, Don't Hide

- **Kill** = remove, tombstone in deprecation-registry.json, archive to cold storage, update all pointers
- **Hide** = leave it in place but stop referencing it, let it rot
- **Archive** = tar to `.archive-YYYYMMDD/`, hash-verify, then delete from live tree

**Rule:** Never hide. Always kill or archive. Hidden artifacts are the most dangerous — they're still there, still loaded by grep, still consuming entropy sweeps, but nobody knows they exist.

---

## 2. THE QUARTERLY FRONTIER REVIEW

### 2.1 Cadence
- **Frequency:** Every 90 days (quarterly)
- **Owner:** 555-ASI (research + inventory) → 333-AGI (propose) → 888-APEX (constitutional check) → F13 (seal)
- **Output:** `KILL_LIST_CYCLE_YYYY-MM-DD.md` in `/root/AAA/governance/kill-cycles/`

### 2.2 Review Targets

| Category | What to audit | Kill signal |
|----------|--------------|-------------|
| **Skills** | Skill mesh (<100 N used in last quarter) | < 2 triggers in 90 days |
| **Tools** | MCP surface audit | Dead tool, duplicate tool, phantom tool |
| **Providers** | FED balance probe | Dead provider, zero balance, 3+ consecutive failures |
| **Docs** | Deprecation registry | Superseded > 90 days ago, still present |
| **Agent cards** | FORGE-onboarding canonical path | Duplicate cards, missing canonical references |
| **Configs** | Runtime vs source drift | Config pointing to dead endpoint > 30 days |

### 2.3 Kill Pipeline

```
555-ASI INVENTORY → 333-AGI PROPOSE → 888-APEX CONSTITUTIONAL CHECK → F13 SEAL → A-FORGE EXECUTE → VAULT999 RECEIPT
```

Each kill is a constitutional act. Each kill leaves a receipt. Each kill is reversible (archive, don't destroy).

---

## 3. ACTIVE KILL LIST (Cycle 2026-Q3)

### 3.1 Immediate Candidates (awaiting F13 seal)

| ID | Type | Reason | Archive path |
|----|------|--------|-------------|
| **K001** | Skills: archive-20260804/ (48 files) | Already archived but still referenced in skill mesh. Delete references. | Already in `.archive-20260804/` |
| **K002** | Skills: bottom 50% inactive | ~68 skills with < 2 triggers since 2026-06. Audit and archive. | TBD |
| **K003** | Configs: dead provider references | mulerouter, opencode-go, tokenrouter removed from chains but config stubs remain | `/root/forge_work/2026-08-04/fed-zen-20260804T073700Z/` |
| **K004** | Docs: duplicate AGENTS.md | 7+ per-repo AGENTS.md files that differ from `/root/AGENTS.md`. All should be pointers. | Per-repo archive |
| **K005** | Skills: `.profile-archive/` and `.archive-openclaw-legacy/` | Legacy skill trees with no active bindings | Verify then tar |

### 3.2 Awaiting Nomination

Every new feature, tool, or skill created after 2026-08-04 MUST nominate a kill candidate here. The author of the new artifact is responsible for the nomination.

---

## 4. ARCHIVE PROCEDURE (Safe Kill)

```
1. SNAPSHOT: cp -a <target> <archive-path>/pre-kill-YYYYMMDDTHHMMSSZ/
2. SHA256:  sha256sum <target> > <archive-path>/manifest.sha256
3. TAR:     tar -czf <archive-path>/<name>-KILLED-YYYYMMDD.tar.gz <target>
4. VERIFY:  sha256sum -c <archive-path>/manifest.sha256
5. DELETE:  rm -rf <target>
6. TOMBSTONE: Update deprecation-registry.json
7. RECEIPT: Write kill receipt to VAULT999
```

**Rollback:** `tar -xzf <archive-path>/<name>-KILLED-YYYYMMDD.tar.gz -C /` — no loss, fully reversible (F1 AMANAH).

---

## 5. WHAT NEVER GETS KILLED

| Artifact | Reason |
|----------|--------|
| VAULT999 outcomes.jsonl | Immutable by design (F11, chattr +a) |
| FLOOR_TABLE.json | Constitutional source |
| 000_KERNEL_CANON.md | Constitutional source |
| KUNCI-MAS vault.env | Secrets — rotation only, never deletion |
| carry_forward.json (active session) | Live state |
| AGENTS.md (root) | Federation kernel pointer |
| AGENT_MODEL_MAP.json | Canonical model registry |

---

## 6. THE KILLER'S OATH

```
I will not let the federation rot under its own weight.
I will kill what no longer serves the frontier.
I will archive, not destroy.
I will leave a receipt for every deletion.
I will nominate a kill for every creation.
I will not hoard artifacts out of sentiment or fear.
The federation is a living body. It metabolizes or it dies.
DITEMPA BUKAN DIBERI — forged in flow, killed with purpose.
```

---

*Inspired by Thorsten Ball's "Kill List" — Amp's deleted VS Code extension, tab completion, and handoff.*
*Source: https://www.youtube.com/watch?v=FU5_kpTAVDo · https://ampcode.com*
*DITEMPA BUKAN DIBERI ⚒️☠️*
