# Federated Plugin Architecture — ONE SOT, N Views

> **Status:** BUILT_NOT_INSTALLED · trace receipts in `dist/build_receipt.json`
> **Date:** 2026-09-25 · **Builder:** FI-003 (333-AGI BUILD lane)
> **Resolves:** "federated plugins for all AAA agents" — F13 directive relayed through Codex plugin-doctrine research (2026-09-24/25).

## The Law

A plugin is a **packaging layer, not a runtime**. All capability lives in the
substrate (arifOS kernel, A-FORGE, CHRON, arifFlow, WELL). Therefore the
federation must never hand-build N per-harness plugins — it maintains **one
canonical SOT compiled to N harness views**, with the shared hook mesh and
the kernel doing the actual work.

```
                    ┌─────────────────────────────────┐
                    │  /root/AAA/plugins/arif-core/   │  ← SOT (manifest.yaml)
                    │  organs: AAA/federation/organs.yaml (endpoint SOT)
                    │  hooks:  AAA/hooks/lib contract │
                    └───────────────┬─────────────────┘
                        build.sh → adapters/compile.py
        ┌───────────────────┬───────┴────────┬──────────────────┐
        ▼                   ▼                ▼                  ▼
  dist/codex/          dist/qwen/      claude (existing)   future: kimi/
  plugin.json          QWEN.md         claude-code-        grok/ gemini/
  hooks.json           snippets        federation          (adapters as FI
  .mcp.json                            remains surface     lanes mature)
```

## Federation invariants (FP-01..FP-07) — additive to Codex I-01..I-41

| # | Invariant |
|---|---|
| FP-01 | ONE SOT, N views. Views are build artifacts — never hand-edit a view. |
| FP-02 | **Hooks are sensors, not judges.** Advisory collection only; verdict authority stays with the kernel (`forge_shell`/ArifJudge/`mcp_guard`). A hook that adjudicates is an authority violation. |
| FP-03 | Skills referenced, never copied. `/root/AAA/skills` stays canonical; views carry pointer skills only (no regrowth of the 518-mirror defect). |
| FP-04 | Coverage per harness is declared (FULL / DEGRADED / ABSENT / UNVERIFIED), never assumed. See `dist/coverage-matrix.md`. |
| FP-05 | Install/sync per harness = explicit forge step only. AAA writes SOT; F13 holds the picker pen; no auto-sync ever. |
| FP-06 | Every build emits a receipt: `sot_sha256`, `trace_id`, view list, next gates. |
| FP-07 | Organ endpoints resolve from `organs.yaml` at build time — no hardcoded ports in views. |

## Substrate truth (what a plugin can and cannot do)

- **CAN:** bundle skills pointer, wire lifecycle sensors, mount organ MCP servers, schedule automations, pin install integrity (sha).
- **CANNOT:** mint ephemeral tools (A-FORGE does), persist memory (CHRON/VAULT999 do), judge (arif_judge does), witness (W³/FRAME do), authorize (kernel mints envelopes; issuer ≠ executor).

The "AGI-coder" delta is therefore: the plugin converts declared substrate
capability into **default harness behavior** — sensors on every mutation,
organs mounted at load, receipts on every action — while enforcement and
authority remain kernel-side.

## Division of labor (APEX-ZEN)

| Lane | Actor | Work |
|---|---|---|
| BUILD | FI-003 (Qwen) | SOT, codex adapter, compiler, views, this doctrine |
| VERIFY | Codex FI / 555 | validate emitted codex view vs `validate_plugin.py` + I-01..I-41; cross-check decision-wire schema |
| JUDGE | 888-APEX | any question of authority or scope |
| SEAL | F13 | install per harness (picker pen), marketplace opening, author.email confirm |

## Provenance

- Hook contract pre-existed: AAA-HOOK-FORGE-V1.0 (`/root/AAA/hooks/lib/`), 8 adapters, evidence ledger, policy engine.
- Codex event names: `codex-rs/protocol/src/protocol.rs` HookEventName (12) — via Codex FI research 2026-09-25.
- This SOT adds: codex adapter (12-event map, DEGRADED declared), arif-core manifest, compiler, coverage matrix.
