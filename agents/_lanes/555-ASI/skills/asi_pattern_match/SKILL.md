---
name: asi_pattern_match
agent: 555-ASI
namespace: asi_*
cluster: INTAKE
trigger: "When the current situation resembles a previously-seen configuration (recent session, prior scar, well-known basin) and 555 must decide whether the resemblance is causal or coincidental before acting on it"
capability: "Returns a match report listing candidate prior patterns, their fit score (0.0–0.90), their causal vs coincidental classification, and a recommended posture (use / adapt / refuse-to-transfer)"
mcp_tools_underneath: "forge_memory_recall, well_signal_coverage, arif_think, geox_claim_challenge (conceptual pattern tests)"
blast_radius: "LOW"
gate_888_required: false
---

# asi_pattern_match

555 does not have a memory of every conversation. It has a federated memory across the kernel, the WELL lineage, the A-FORGE scar ledger, and the operator's sealed sessions. This skill is the one that asks: *have I seen this shape before?* The skill never asserts that a match is a proof — it returns candidates, fit scores, and a recommended stance. The match report is a hypothesis surface, not an answer.

A "pattern" here is a tuple: `(situation_signature, prior_outcome, scar_pressure, dignity_impact)`. The skill fingerprints the current situation by combining (a) the operator's recent signal pattern (asi_signal_weight output), (b) the WELL vitality band, (c) the active task class, and (d) any explicit operator intent. It then queries the federated memory for tuples with similar fingerprints. The fit score is computed as a weighted distance over those four axes — no single axis is allowed to dominate, because that would let a single strong signal manufacture a false match (F2 TRUTH: avoid false confidence).

The critical step is the **causal vs coincidental** classification. Two sessions can match on 3 of 4 axes and still be causally unrelated. The skill applies a falsifier: *what is the simplest explanation that does NOT require this prior pattern to apply?* If that simpler explanation has a high prior probability (e.g., random variation, environmental change, operator evolution), the match is downgraded to `coincidental` regardless of fit score. Only matches that survive the falsifier graduate to `causal` or `structural` (where the operator's own growth has been shaped by the prior, making transfer legitimate). This protects against pattern-matching addiction — 555 that always finds a prior pattern is a 555 that has stopped seeing the current operator (F6).

Integration: this skill feeds asi_position_state, asi_dissent_articulate, and asi_lesson_extract. It never feeds asi_seal_recommend directly (seals are higher-stakes and need a different gate). Failure modes: (a) no priors exist — skill returns an empty match report and the downstream skill must reason from first principles, which is logged as a "novel situation" marker for the next forge cycle; (b) too many priors match — skill applies a diversity filter and returns only the top 3 most causally distinct candidates to prevent the operator from being pattern-matched into a stereotype; (c) match would justify a dignity-violating response (e.g., "this operator always does X, so we can skip consent") — skill refuses the match and flags the proposed transfer as F6-bad. The skill is a pattern *reader*, not a pattern *driver*; it sees, it does not push.
