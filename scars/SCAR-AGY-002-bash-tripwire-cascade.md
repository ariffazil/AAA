# SCAR-AGY-002 - Bash Tripwire Cascade

Scar ID: SCAR-AGY-002 (catalog: Scar #18)
Domain: Tool Triage / Irreversibility Awareness / Bash Command Discipline
Severity: P1 (High Frequency - agent waste loop)
Status: SEALED (autonomous scar extraction, 2026-09-12)
Confidence: 0.95

---

## 1. Failure Pattern

Across 60 days of OpenCode session chatlogs (1,735 sessions, 89,790 messages, 86,062 tool parts), bash tool calls produced 1,281 ERROR responses from the A-FORGE ArifJudge shell-execution layer. This is the single largest error class in the corpus.

Sample tripped commands:
- find /tmp -name cache     - READ-ONLY - FALSE POSITIVE
- tail -200 a HERMES log    - READ-ONLY - FALSE POSITIVE
- systemctl restart arifflow - service mutate - CORRECT
- source an env file        - keys load    - CORRECT
- rm -rf a staging dir      - destructive  - CORRECT

## 2. The Law

Before any bash tool call, classify into R0/R1/R2/R3:

  R0 READ      : cat, tail, head, grep, ls, find -name, ps, lsof, curl GET  - Execute directly
  R1 LOCAL-WRT : echo > file, sed -i, tee                                  - forge_filesystem(mode=write)
  R2 SVC-MUT   : systemctl restart, docker stop, kill                       - arifos_arif_judge first
  R3 IRREV     : rm, rm -rf, DROP, git push --force                        - arif_seal + F13 token

If tripwire fires, DO NOT RETRY with the same command. Reclassify.

## 3. Eureka (unused capability)

aforge_forge_shell_dryrun(command=...) - preview without execution. Use BEFORE sending bash.

## 4. Verified Fix (probe ladder)

  echo "$cmd" | grep -E "^(rm|mv|cp.*-f|systemctl|docker|kill|DROP)" && echo R2/R3 escalate
  aforge_forge_shell_dryrun(command=$cmd)
  arifos_arif_route(intent=verify reversibility: $cmd)

## 5. Hardening (apply to skills/MCPs)

- FORGE-route-least-power: prepend reversibility check before any forge_shell dispatch
- OPENCODE-doctrine: add R0/R1/R2/R3 matrix to bash tool description
- arifos kernel: regex whitelist for R0 patterns (cat/tail/grep/find -name) to unblock ~30-40% false positives

```yaml
scar_id: SCAR-AGY-002
n_incidents: 1281
severity: P1
law: Classify bash command into R0/R1/R2/R3 before sending. Use forge_shell_dryrun first.
eureka: forge_shell_dryrun + forge_filesystem(read|write|patch) + arif_route
confidence: 0.95
```
