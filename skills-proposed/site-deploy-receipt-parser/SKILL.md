# Skill: site-deploy-receipt-parser

> **Status:** PROPOSED · **Created:** 2026-09-18 · **Forged by:** FI-008 (kimi-code / k3)
> **Capability, not implementation.** Govern capabilities, not implementations.

## 1. Capability contract (binding)

Bounded capability: parse the output of `make verify-pages` (the 2026-08-03 non-bypassable deploy gate) into a structured receipt that can be sealed into arifFlow and audited by F11 observers, without invoking the deploy itself.

## 2. Why this skill exists

The site deploy pipeline has a mandatory gate at `make verify-pages` (per `/root/arif-fazil.com/AGENTS.md`, after the 49-page-404 incident of 2026-08-03). Currently an agent invoking this command reads stdout text, asserts visual exit 0, and forgets. There is no persisted record of WHICH pages were verified, WHICH routes returned 200, and WHICH previous-OK routes regressed.

This skill makes the gate's output a sealed-style receipt, audit-grade.

## 3. Scope (where this skill binds)

- `make verify-pages` invocation (verify target ONLY — NOT `make deploy`)
- `scripts/verify-pages.sh` direct invocation
- `scripts/verify-surfaces.cjs` parallel verification
- Subsequent `mcp__arifFlow__flow_ingest` mint per verification round

## 4. Out-of-scope

- Running `make deploy` itself → 888_HOLD
- Reloading Caddy → 888_HOLD (T3-bound per ROOT_AGENT_CONFIG.yaml)
- rsync with `--delete` without `web_zen.py orphan` preview → HOLD

## 5. Required MCP tools

- `mcp__arifFlow__flow_ingest` — receipt mint
- `mcp__aforge__forge_shell` — to run `make verify-pages`
- `mcp__well__well_observe_evidence_backlog` — confirms audit signal coverage

## 6. Workflow (BINDING order)

```
assert_verify_pages():
    # 1. Run the gate (verify only — NEVER deploy)
    result = forge_shell(
        command="make verify-pages BASE=https://arif-fazil.com DIST=/root/arif-fazil.com/sites/arif-fazil.com/dist",
        timeout=300,
        expected_output="verify-pages-exit-0"
    )
    
    # 2. Parse the result into a structured receipt
    receipt = {
        "gate": "make verify-pages",
        "exit_code": result.exit_code,
        "pages_checked": parse_pages_checked(result.stdout),
        "pages_200": parse_200_count(result.stdout),
        "pages_404": parse_404_count(result.stdout),
        "timestamp_utc": now(),
        "actor_id": self.actor_id,
        "session_id": self.session_id
    }
    
    # 3. Mint a FlowReceipt
    arifFlow.flow_ingest(
        step_type="Verify",
        payload=receipt,
        floor_verdict="Pass" if result.exit_code == 0 else "Hold"
    )
    
    # 4. Return structured receipt, NOT raw stdout
    return receipt
```

## 7. Truth classes (F2 binding)

Receipt payloads are `OBS` from `make verify-pages` exit code and stdout. Any subsequent INTerpretation must be tagged `INT`.

## 8. Kill-switch

```yaml
kill_switch:
  kill_phrase: "STOP deploy-receipt-parser — revert to manual stdout reading"
  revert_action: "agents resume manual `make verify-pages` invocation"
  expected_recovery_time: <30s
  side_effects_on_kill: ["audit trail gap until parser resumes"]
```

## 9. Reversibility class

`REVERSIBLE`. The parser is observation-only on stdout; it never invokes the deploy.

## 10. F11 Auditability

This skill IS the F11 auditability surface for the deploy gate. Abandonment creates an audit hole for every site deploy.

## 11. F13 Sovereign veto

If any `make verify-pages` result indicates a route regressed (a previously-200 path now 404), the skill's receipt emits `floor_verdict=Hold` and stops. F13 escalation is required to choose: revert route, add to INTENTIONAL_EXCLUSIONS, or hold deploy pending sovereign review.

## 12. Operator handoff

The skill does NOT request operator input. The receipt is the operator's view. They see a structured JSON, not raw shell output.

## 13. Verification checks

- [ ] `make verify-pages` exit code captured exactly (no truncation, no rounding)
- [ ] Receipt persisted in arifFlow ledger
- [ ] No deploy mutation path enabled
- [ ] No Caddy reload triggered
- [ ] Empty output → receipt still mints (with `pages_checked=0`, `exit_code=0`)
- [ ] After regress-detection, `floor_verdict=Hold` not `Pass`

## 14. Decoration risk

A parser that writes receipts but does not surface regressions to F11 auditors is **decoration by omission**. Mitigated by always tagging regressions with `floor_verdict=Hold` AND logging to events.jsonl AND minting a separate FlowReceipt.

---

DITEMPA BUKAN DIBERI · forged, not given.
