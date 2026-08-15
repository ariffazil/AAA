# CONTRACT — Void Question Rotation (Phoenix 72) · LIVE 2026-08-15

> Commissioned by F13: "everyday each agent ask 3 void questions, rotate, own bot each, AAA group."
> Ritual name: **Phoenix 72** — one full rotation (Hermes → OpenClaw → CCC 777) = 72h = satu nadi dengan AIA.

## Rotation (anchored Saturday 2026-08-15 = Hermes)

| Day | Agent | Bot | Cron |
|---|---|---|---|
| Sat, Tue, Fri | Hermes | @hermesarifos_bot (HERMESARIFOS_BOT_TOKEN) | `5 9 * * 2,5,6` |
| Sun, Wed | OpenClaw | @AGI_ASI_bot (AGI_ASI_BOT_TOKEN) | `5 9 * * 0,3` |
| Mon, Thu | CCC 777-FORGE | @arifOS_bot (FORGE_BOT_TOKEN) | `5 9 * * 1,4` |

## Rules (all three crons identical)
1. **3 NEW void questions daily** — contrast-void grammar: peta yang ADA, perkataan yang TIADA, kenapa tiada sensor, soalan apex. Bukan blindspot biasa (yang dah dikenali) — yang belum bernama.
2. **Anti-repeat**: read `10_RECEIPTS/AIA/VOID_ROTATION/asked.jsonl` first; pertanyaan yang hampir sama dengan 30 hari lepas = ditolak, ganti baru.
3. **Send via** `scripts/void_rotation_send.sh <AGENT> <BOT_ENV>` (single point of config).
4. **Append questions to ledger** (asked.jsonl) after send — satu baris per soalan, dengan ts + agent.
5. Format mesej (BM, ringkas): header rotasi + 3 soalan bernombor + baris phoenix (rotasi seterusnya). ≤ 900 karakter.
6. OBSERVE_ONLY: soalan sahaja — tiada cadangan binaan, tiada mutasi, tiada lip service. Kos: 1 mesej/hari.

## Provenance honesty (F11)
Posts are signed by the agent whose DAY it is (rotation identity). Receipts record true generator: `voidq-openclaw`/`voidq-ccc` crons are scheduled by the Hermes rotation engine ON BEHALF of those agents (takeover by their own harnesses = drop-in replacement, contract above).

## Lineage
- Void grammar born: VOID_QUESTIONS_v1.md (BERA, HUTANG SOALAN, KEPERCAYAAN TEMPA) — 2026-08-15
- Apex gate: SEAL-d0e6ed79140f4d5d (call_hash sha256:4d61a41a…) — action authorized, output stays HOLD
