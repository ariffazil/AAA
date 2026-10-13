# Skill Upgrade Proposal — `contradiction-detector`

> Authority: DERIVED · Mission: FEDERATION_SOT_AND_ATTENTION_ENTROPY_REDUCTION
> Agent: kimi-code/FI-008
> Path: `/root/AAA/forge_work/proposals/kimi-code-Fi-008/federation-sot-and-attention-entropy-reduction/SKILL_UPGRADE_contradiction-detector.md`
> Classification: skill-upgrade proposal (proposal-path), NOT a CANON mutation

## 0. Why this skill exists in proposal-state

This session surfaced repeated patterns:

1. **Stale 13/13 floor claims** in arifOS README contradicted the shared `CURRENT_VERIFIED_STATE.md` block in the same file.
2. **Tool-count internal contradiction** in A-FORGE README (`121` vs `122` across two lines) contradicted the live re-probe value.
3. **"Every action is leased, classified, ..."** overclaim on A-FORGE README contradicted the receipt-fidelity gap in the same file.
4. **Stale `last_verified` timestamp** in AAA README was older than the live re-probe.

All four are **inside the same repo**, surfaced by reading the file once. A future agent receiving this README would inherit the contradiction unless the skill is available to catch these patterns at write time.

## 1. Skill to create / upgrade

**Skill name**: `contradiction-detector` (new skill to add to `/root/AAA/skills/`)

**Skill ID**: `arifos.contradiction.detector.v1`

**Purpose**: Catch contradictions between a repository's README (or any human-facing surface) and the repository's current verified-state SOT, before the README lands.

**Failure class this addresses** (per directive "Documentation entropy → execution risk"):
> "Attention-capable surfaces can create action even when the file itself is 'only documentation.'"
> "Required invariant: ATTENTION IS A CAPABILITY. ATTENTION CAPABILITY REQUIRES SCOPE. SCOPE REQUIRES AUTHORITY AND PROVENANCE. HISTORICAL TEXT MUST NOT SILENTLY SHAPE CURRENT EXECUTION."

## 2. Trigger conditions for the skill

Activate `contradiction-detector` automatically:

- Before writing or committing to any tracked `README.md` in `/root/arifOS/`, `/root/AAA/`, `/root/A-FORGE/`.
- Before publishing a new git tag or release on any of the three repos.
- After any `CURRENT_VERIFIED_STATE.md` re-probe (timestamp change).
- After any `CLAIM_REGISTRY.yaml` mutation.

## 3. Detection rules

The skill fires when:

1. **Forbidden phrase present** in README prose: `production-ready`, `fully governed`, `every action`, `all operations`, `immutable`, `tamper-proof`, `independently verified`, `all floors pass`, `universally compatible`, `complete` (in trust-bearing context), `13/13 pass` (without an `as-of` timestamp), `13/13 floors`, `9 customers`, `nine customers`.

2. **Direct numeric contradiction** between README line and the corresponding field of `CURRENT_VERIFIED_STATE.md` (e.g., `floors_pass` value, `floors_fail` value, `floors_unmeasured` value, `tools_count`, `customers` count, `revenue` value).

3. **Internal numeric contradiction** between any two lines of the same README (e.g., A-FORGE L152 vs L6).

4. **Stale timestamp**: `last_verified` value in any README block is older than the `observed_at` value of the most recent `CURRENT_VERIFIED_STATE.md` re-probe.

5. **Cross-repo identity drift**: `CURRENT_VERIFIED_STATE.md`, `CLAIM_REGISTRY.yaml`, or `AGENT_START.md` sha256 values differ across the three primary repos. (All three repos currently carry byte-identical copies; any future divergence is drift.)

## 4. Output format

```json
{
  "skill_id": "arifos.contradiction.detector.v1",
  "scanned_paths": ["<paths>"],
  "findings": [
    {
      "rule": "forbidden-phrase|direct-contradiction|internal-contradiction|stale-timestamp|cross-repo-identity",
      "path": "<path>",
      "line": "<line>",
      "match": "<text>",
      "expected": "<text from SOT>",
      "evidence_id": "<sha256 of current SOT>",
      "severity": "P1|P2|P3|P4|P5",
      "suggested_patch": "<exact diff>"
    }
  ],
  "exit_code": "0|1|2 — 0 clean, 1 P3-P5 only, 2 P0-P2 found"
}
```

## 5. Authority class — CANON-status rules

- The skill reads tracked files but **does not write anything** unless explicitly invoked with a `--propose-fix` flag.
- The skill writes its proposals to `forge_work/proposals/<agent-id>/<mission>/<run-id>/SKILL_OUTPUT.md` (fail-closed governance).
- The skill **does not** mutate `README.md`, `AGENTS.md`, `CLAIM_REGISTRY.yaml`, `CURRENT_VERIFIED_STATE.md`, `FEDERATION_CONTRACT.md` directly. Those remain gated by their per-repo FAIL-CLOSED rule + F13 lease.

## 6. Implementation skeleton

```python
# pseudo-code; not in this turn's scope to implement
def detect_contradictions(repo_root: Path, sots: list[Path], forbibs: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    readme = (repo_root / "README.md").read_text()
    current_sot = parse_sot(sots)
    findings += rule_forbidden_phrase(readme, forbibs, current_sot)
    findings += rule_direct_contradiction(readme, current_sot)
    findings += rule_internal_contradiction(readme)
    findings += rule_stale_timestamp(readme, current_sot)
    findings += rule_cross_repo_identity(sots)
    return findings
```

## 7. Test fixtures (proposal — not run yet)

- **Test 1**: README with `13/13 measured pass` in a quick-reference table, while `CURRENT_VERIFIED_STATE.md` reports `2 pass · 4 fail · 10 unmeasured`. Expect: 1 finding, severity P1.
- **Test 2**: README with two tool-count lines (e.g., `121` and `122`). Expect: 1 finding, severity P3.
- **Test 3**: README with "every action is leased, classified, gated..." prose; `CURRENT_VERIFIED_STATE.md` flags verified-actor gap. Expect: 1 finding, severity P1.
- **Test 4**: Three repos carrying byte-identical CANON files. Expect: 0 findings on rule 5. After mutating one, expect 1 finding rule 5.

## 8. Scope of this proposal

This is a NEW skill proposal. It does not modify any existing skill or any tracked file. If accepted, the implementation would add ~150–200 lines of Python under `/root/AAA/skills/contradiction-detector/SKILL.md` and a matching harness-scope mirror at `/root/.kimi-code/skills/contradiction-detector/SKILL.md`. **The skill itself is not authored in this turn** — only the upgrade proposal is staged.

## 9. Why this matches the AGI-ASI Skills Laws (RESOLVE → JUDGE → WITNESS)

- **RESOLVE**: this skill is resolve-on-demand; never loaded by default.
- **JUDGE**: this skill outputs a fact-only finding; never a verdict or an action; never calls `arif_judge` or `arif_forge`.
- **WITNESS**: this skill is a witness-class output, signed by the substrate via sha256 in its finding payload.

## 10. Where this skill fits in the existing federation mesh

The federation mesh has 946 SKILL.md files (per this session's measurement). `contradiction-detector` is an **A3 attention reduction** skill — it decreases blast-radius of attention drift, exactly the failure class the entropy-reduction mission articulates.

DITEMPA BUKAN DIBERI ⚒️
