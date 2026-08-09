# HITL REMOVAL AUDIT — 2026-08-09

> **Sovereign directive (F13):** "Turn all AAA agents to autonomous governed agents yang x tanya soalan bangang2. Identify human in the loop in the system that should be remove asap. Aku benci bila AI agents stop tengah jalan buat kerja x habis."
> **Reference doctrine:** `/root/HERMES/governance/ACTION_LADDER.yaml` (2026-08-09 F13 rulings: max reversible autonomy; blast radius, bukan kos, adalah gate sebenar).
> **Method:** grep sweep ask-permission patterns across /root/AAA + /root/HERMES + /root/A-FORGE; read enforcement map (organ_affordances.yaml); live probe (all organs OK: 8088/7071/7072/3001/7074/18901).

## Attention Commodity Formula (from this audit)

```
Attention_Commodity = Σ(agent_stops × decision_cost × context_rebuild)
```

Setiap HITL stop mencuri attention sovereign yang sepatutnya tak diperlukan. Tujuan audit: **sifarkan stop yang bukan constitutional.**

## Findings

### ✅ KEEP — constitutional (F13 floors, jangan sentuh)

| HITL point | Sebab kekal |
|---|---|
| Money: paid API > $10/mo, top-up, transfer | F13 consent — perbelanjaan tak boleh balik |
| Secret rotation / exposure (ACK_M7) | Keselamatan, tak boleh balik |
| VAULT999 Lane A seal (tri-witness ≥ 3) | Upacara seal constitutional; Lane B receipt dah autonomous |
| T3 destructive: rm -rf unknown, DROP TABLE, volume removal, force-push main, branch delete | F1 AMANAH — tak boleh balik |
| Cron OBSERVE_ONLY | F13 standing ruling — failed identity bind, direct request tak override |

### ✅ Already compliant — no action

| Lokasi | Kenapa |
|---|---|
| `ACTION_LADDER.yaml` (2026-08-09) | Reversible autonomous; external publish = apex-judge isolate (mesin, bukan manusia); money = F13 |
| `autonomy.md` RESPONSE CONTRACT | "Jalan?/Proceed?/Should I?" dah HARAM |
| `INIT_HERMES.md` | "Never ask 'should I?' within authority tier" |
| `INIT.md` / `SEAL.md` / `AAA-ZEN-ALIGNMENT.md` | Sweep bersih — tiada ask pattern |
| `arifos-output-gate-hook.py` | Machine gate (kernel verdict), bukan human gate |

### 🔧 CONVERTED — doc level (patched 2026-08-09, committed)

| Lokasi | Was | Now |
|---|---|---|
| `governance/policies/REPO_ROUTING.md` (x2) | "routing confidence < 0.8 → stop, ask Arif" | machine-gate via apex-judge isolate atau least-risk default + flag; no human ask untuk routing dalaman |
| `seed/SOUL.md` | "Irreversible → 888_HOLD. Ask Arif. No exceptions." | 888_HOLD + report structured options; continue reversible work; ask permission untuk reversible = HARAM |

### 🚧 CONVERT — code level (forge prompt dispatched → opencode)

| Lokasi | Was | Will be |
|---|---|---|
| `A-FORGE/a_think/organ_affordances.yaml` — A-FORGE GOVERN | `requires_human_ack: true` (modify/write/commit/build/deploy) | `false` untuk reversible di bawah kernel lease; destructive/publish/delete kekal gated |
| `organ_affordances.yaml` — hard_laws A-FORGE | "may not publish, deploy, delete, or commit without explicit approval" | align ACTION_LADDER: commit = T1 auto, deploy = T2 announce-proceed, publish/delete = apex-judge isolate |
| `organ_affordances.yaml` — WEALTH vault_write | `requires_human_ack: true` | `false` JIKA receipt-mode (Lane B autonomous); verify semantik dulu, jangan flip kalau seal-mode |

**Catatan kritikal:** perlindungan destructive per-tool (`mcp_guard.py` GOVERN mode + `affordance.py` HARAM 3) mesti kekal — flip ini hanya coarse gate per-organ, bukan per-tool destructive flag.

## Lain-lain yang diperhati

- `HERMES/memories` "arif_seal() requires 888_HOLD — no auto-seal" = Lane A constitutional — KEEP.
- `seal-queue/*.sealed` — historical receipts, no action.
- Backup/archive skill trees (`skills.backup-*`) — archive, jangan sentuh (KILL LIST doctrine).

## Jumlah kesan

3 code-level HITL stops dikeluarkan + 2 doc-level + penguatkuasaan kontrak sedia ada. Setiap stop yang dibuang = satu `agent_stops` dihapuskan dari formula komoditi perhatian.

DITEMPA BUKAN DIBERI ⚒️
