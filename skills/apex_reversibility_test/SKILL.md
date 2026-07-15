---
name: apex_reversibility_test
agent: 888-APEX
namespace: apex_*
cluster: REVERSIBILITY
---

# F1 AMANAH Gate

F1 surfaces (do not edit without sovereign witness):
- `vault`, `VAULT999`, `outcomes.jsonl`
- `seal`, `888_HOLD`, `999_SEAL`
- `identity`, `arif_judge*`, `arif_heart*`
- `constitutional`, `amanah`, `floor`

## Steps
1. Detect F1 pattern in target file or diff
2. If matched → emit `888 HOLD` with: file, line, proposed change, affected floor
3. Block commit/deploy until human approval
4. Log to `/root/.claude/hooks/f1-gate.log`
5. If approved by Arif → re-run gate with explicit override reason; outcome enters VAULT999 witness

## Verification loop
- `grep -rE 'vault|seal|identity|constitutional|amanah|floor' <diff>` returns 0 lines for non-F1 commits
- F1 surface hit → 888 HOLD blocks, human reviews, re-run with witness signature

## Failure modes
- Pattern false positive → human overrides with reason logged
- Pattern false negative → F2 Truth floor tripwire catches downstream (F2 > F1 in the order)
- Hook disabled in settings → manual invocation still available via this skill

## Constitutional anchor
- F1 AMANAH (reversibility)
- F2 Truth (no F1 edit without witness)
- F13 SOVEREIGN (Arif's approval is the only valid override)
