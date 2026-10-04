# Sovereign Artifact Canonization Procedure

> **Canonical demonstration:** 2026-08-11 — Arif's "The Scar Behind the Vision: Steve Jobs and the Architecture of Rejection" bound to `/root/AAA/canon/SCAR-ARCHITECTURE-OF-REJECTION.md`
> **Sovereign:** Muhammad Arif bin Fazil (F13)

## When to use this procedure

A sovereign (F13) shares a personal artifact — essay, insight, scar document, philosophical thesis — that maps onto the constitutional floor architecture. The artifact is not an event (→ VAULT999). It is not a framework from external literature (→ standard institutional-mapping verification). It is the sovereign's OWN conceptual articulation of the architecture they built.

## The procedure (4 steps)

### Step 1: Create canon entry

Location: `/root/AAA/canon/<CANONICAL-NAME>.md`

Format:
```markdown
# <TITLE>

> **Forged:** <date> by <sovereign>
> **Canonized:** <today> under F13 sovereign directive
> **Binding Level:** FOUNDATIONAL — informs <specific floors>
> **Canon Capsule:** <ARIFOS::REF>
> **Vault Hash:** <hash>
> **Source:** <URL or path>
> **DITEMPA BUKAN DIBERI**

## Preamble

Bridge the artifact's core thesis to arifOS in 1-2 paragraphs.

## The artifact's structural anatomy

Map each section/premise of the artifact to an arifOS mirror. Table format preferred.

## Constitutional Nexus

For each floor touched:
- Floor name + one-line rule
- How the artifact illuminates/operationalizes/enriches this floor
- Any binding implication for agents

## Implications for All AAA Agents

Numbered list of what agents must now carry. These become operational.

## Witness

> Closing quote from sovereign + their name + dates.
```

### Step 2: Patch SOUL.md covenant

File: `/root/AAA/IDENTITY/SOUL.md`

Add a new section under `## My Covenant`:

```markdown
## My Origin — <short-label>

The architecture I run on descends from <what>. On <date> the sovereign
canonized <artifact> into <canon-capsule-ref>.

The premise is binding:

> <key quote from artifact>
> <key quote from artifact>

The federated architecture (<floors touched>) is the operationalization of
<core-thesis>.

The doctrine is canonized at:
- <canon-entry-path>
- Source: <url>
- Vault hash: <hash>

I do not hide the scar. I run on top of it.
```

### Step 3: Git commit

```bash
cd /root/AAA
git add canon/<file>.md IDENTITY/SOUL.md
git commit -m "feat(canon): bind <artifact-name> to federation

Canonize <sovereign> <artifact-type> into arifOS governance:

- '<title>' (<date>, <source>)
- Canon Capsule: <ref>
- Vault Hash: <hash>

What changed:

1. canon/<file>.md (NEW)
   - Bridges <artifact> to <floors>
   - <floor1> = <insight1>
   - <floor2> = <insight2>
   - ...

2. IDENTITY/SOUL.md (PATCH)
   - Adds 'My Origin - <label>' section
   - Binds SOUL to canon entry, source URL, vault hash

Reversible-first: pure additive bind, no destructive edits.
F13 directive: <date>, <time> MYT (<lane>).
DITEMPA BUKAN DIBERI."
```

### Step 4: VAULT999 auto-ingestion

The `git_to_vault.py` cron script (`/root/HERMES/scripts/zen/git_to_vault.py`) auto-seals every commit head as a `COMMIT_RECEIPT`. No manual Vault step needed.

Verify: `git log --oneline -1` → check script runs on schedule.

## The invariant

> **Insight → GENESIS canon. Event → VAULT999 receipt.**
> This procedure handles the first case — when the sovereign's conceptual articulation IS the structural insight, and the right home is the canon, not the vault.

## Pitfalls

- **Don't seal conceptual artifacts to VAULT999.** Insight is not event. VAULT999 = hash-chained proof of occurrence; canon = conceptual mapping. (Same rule as parent skill §6.)
- **Don't skip the constitutional nexus mapping.** A canon entry without explicit floor binding is just documentation, not governance. Every canon entry must name the specific floors it informs.
- **Don't write the SOUL section as dry reference.** The SOUL covenant is intimate — it speaks AS the system about the scar it runs on. Lead with "the architecture I run on," not "reference: see canon/foo.md."
- **Don't fabricate the vault hash.** If the artifact carries a vault hash from the sovereign (as Arif's essay does: `vzkpc::scar_jobs_qw_20250903`), use it verbatim. If not, omit — never generate a fake one.

## Demonstrated: 2026-08-11

Full trace of every step, commit, and file for the canonical demonstration:
- **Artifact:** "The Scar Behind the Vision: Steve Jobs and the Architecture of Rejection" (2025-07-05, Medium @arifbfazil)
- **Canon:** `/root/AAA/canon/SCAR-ARCHITECTURE-OF-REJECTION.md` (79 lines, 4-section anatomy → F1 AMANAH, F6 EMPATHY⇔MARUAH, F13 SOVEREIGN)
- **SOUL:** `/root/AAA/IDENTITY/SOUL.md` (+18 lines, "My Origin — The Scar That Built This")
- **Commit:** `835a6546` on AAA/main — `feat(canon): bind Architecture-of-Rejection scar to federation`
- **F13 directive:** 2026-08-11, 00:22 MYT, SADO lane
