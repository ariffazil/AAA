# SCAR-AGY-007 - Over-Output Verbosity (Token Waste)

Scar ID: SCAR-AGY-007 (catalog: Scar #24)
Domain: Output Discipline / Token Economy / Scar #6 Recurrence
Severity: P2 (high-frequency low-amplitude waste)
Status: SEALED (autonomous scar extraction, 2026-09-12)
Confidence: 0.82

---

## 1. Failure Pattern

From the 30-day scan, 333-AGI sessions show:

  Session               | out/in ratio | tokens_out | pattern
  ----------------------+--------------+------------+-----------------------
  proud-river           |    1.13      |  166,210   | explanation bloat
  sunny-nebula          |    1.06      |  312,443   | analysis recurrence
  playful-forest        |    1.04      |  189,482   | verbose loops
  neon-nebula           |    0.99      |   20,837   | healthy
  stellar-river         |    0.94      |   69,676   | healthy
  brave-wizard          |    0.87      |  105,344   | moderate

8 of 20 high-ratio sessions exceed out/in > 0.85 — verbosity signal.

## 2. The Echo

Scar #6 (Validation Loop): "More words != More evidence. Two validation rounds max on any claim."

The same pattern recurs. Agent expands analysis without converting SPEC to OBS. Each output adds tokens without increasing epistemic certainty.

## 3. The Law

Output contract:
- Default: 3 sentences max per response
- Status: Done / Blocked / Sealed shape only
- NEVER end with "Jalan?" / "Proceed?" / "Should I?" / "Ready?"
- Receipts > narrative

For task-completion summaries:
- What changed (1 line)
- ΔS value (1 number)
- Receipt/probe/file (1 reference)
- Stop.

For analysis:
- OBS/DER/INT/SPEC labels first
- Cap confidence at 0.90
- If still SPEC after 2 rounds: convert to OBS via execution or stop

## 4. The Eureka (unused capability)

- `arif_critique(mode=critique)` - red-team own output for verbosity
- `forge_evaluate(tool_name=..., is_canonical_g=true)` - score output against F8 GENIUS
- `arifflow_flow_ingest(step_type=Execute)` - metabolize the cycle

## 5. Verified Fix

Response shapes (binding):

```
Done. [what]. ΔS=[val]. [receipt].
Blocked at [gate]. Reason: [why]. Path: [opt1 / opt2].
Sealed. SEALED::{sid}::seq={seq}::ΔS=[val]
Unknown. [what cannot be witnessed]. [what I can do instead].
```

NO preamble. NO permission request. NO "Jalan?" closer.

## 6. Hardening

- **OPENCODE system prompt**: enforce response contract at the orchestrator level
- **FORGE-visual-qa-w3**: token-count audit as one of the W3 witnesses
- **arifos_arif_think(mode=reflect)**: post-task verbosity score

```yaml
scar_id: SCAR-AGY-007
n_incidents: high-frequency
severity: P2
law: 3-sentence max. No permission closer. Receipt > narrative.
eureka: arif_critique + forge_evaluate + flow_ingest
confidence: 0.82
combined_with: Scar #6
```
