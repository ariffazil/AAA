# ⚒️ INVARIANTS — Agent Architecture Rules (AAA-scope)

> **SCOPE:** Agent behavior invariants for AAA warga. For MCP-level constitutional physics, see canonical: `/root/arifOS/GENESIS/INVARIANTS.md`
> **Forged:** 2026-07-26 by FORGE (000Ω) · **Ratified:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Seal:** `INVARIANTS::AAA-AGENT::2026.07.26`
> **Doctrine:** DITEMPA BUKAN DIBERI — Interfaces are invariant. Implementations are replaceable.
> **Audience:** Semua AAA warga, semua agent baru, sesiapa yang nak ubah sistem.

---

## 0. Kenapa Dokumen Ini Wujud

Kita dah replace banyak benda — Langfuse → Kabarkan, web search API → SearXNG, OpenAI TTS → edge-tts, GPT-4 → multi-provider routing, Docker → bare-metal systemd.

Persoalan: **Apa yang kita TAK BOLEH replace?**

Dokumen ini jawab — dengan dua frame analysis yang converge kepada satu kesimpulan.

---

## 1. Dua Frame, Satu Kebenaran

### Frame A: Arif's 5-Layer Architecture (Compute → Protocol → State → Governance → AI)

```
Layer 5  AI Model      ← Observation/Action/Reward pattern
Layer 4  Governance     ← F13, F1–F13, 000→999 pipeline
Layer 3  State          ← VAULT999 chain, Postgres, Qdrant, Redis
Layer 2  Protocol       ← MCP, A2A, JSON-RPC, HTTP/SSE, Ed25519
Layer 1  Compute        ← Python, TypeScript, Rust, Linux, systemd
```

### Frame B: FORGE 3-Tier Irreplaceability (Invariant → Near-Invariant → Replaceable)

```
Tier 1  🔴 IRREPLACEABLE PROTOCOL     ← MCP, A2A, Ed25519, F1–F13, VAULT999 chain, 000→999
Tier 2  🟡 PATTERN INVARIANT          ← State stores, verifier, observation/action loop
Tier 3  ✅ REPLACEABLE                ← LLM provider, search backend, TTS, DB engine, file storage
```

### The Convergence

```
Arif Layer    FORGE Tier     Verdict
───────────   ────────────   ──────────────────────────────────────
Layer 1       ⚠️ Near-Inv     Compute substrate — replaceable in theory, practical rewrite besar
Layer 2       🔴 TIER 1       Protocol substrate — TAK BOLEH REPLACE
Layer 3       🟡 TIER 2       State substrate — pattern invariant, implementation flexible
Layer 4       🔴 TIER 1       Governance substrate — TAK BOLEH REPLACE
Layer 5       🟡 TIER 2       AI substrate — pattern invariant, format flexible
```

---

## 2. The Unifying Principle

> **Interfaces are invariant. Implementations are replaceable.**

| Interface (Invariant) | Implementation (Replaceable) |
|-----------------------|------------------------------|
| MCP `tools/list`, `tools/call` | FastMCP, custom MCP server in any language |
| F13 SOVEREIGN veto | Python `arif_judge`, Rust rewrite, TypeScript judge |
| VAULT999 append-only hash chain | Current JSONL format, any append-only store |
| Ed25519 signature verification | Current Python `cryptography` lib, any Ed25519 implementation |
| `arif_init → arif_judge → arif_forge → arif_seal` | Current Python kernel, any language that respects the sequence |

**Iron Rule:** Kalau kau tulis semula `arif_judge` dalam Rust esok, selagi dia:
1. Terima MCP JSON-RPC 2.0
2. Output SEAL/HOLD/VOID/SABAR
3. Rujuk `FLOOR_TABLE.json`
4. Tulis ke VAULT999 hash chain

...sistem masih arifOS. **Tukar behaviour salah satu dari empat tu → sistem lain.**

---

## 3. Trinity-33 Language Mapping

| Axis | Bahasa | Organ | Port | Role | Status |
|------|--------|-------|------|------|--------|
| **Δ Law** | Python | arifOS, GEOX, WEALTH, WELL | :8088, :8081, :18082, :18083 | Law, judgment, domain intelligence | ✅ Running |
| **Ω Hands** | TypeScript | A-FORGE, AAA | :7071, :3001 | Execution, control plane, cockpit | ✅ Running |
| **Ψ Nerves** | Rust | arifFlow | :7073 | Parallel execution, metabolism, FQ | ✅ Compiled |

**Rust bukan aspirational — dia dah running.** arifFlow handle apa Python dan TypeScript tak boleh buat efficiently: concurrent execution scheduling dengan guaranteed checkpoint.

```
arifFlow capabilities (Rust, zero-cost abstractions):
  BSP scheduler       — fan-out 1→N parallel execution
  Pipeline sequential  — staged execution with checkpoint between stages
  Cascade escalation   — automatic escalation on failure
  Merkle checkpoint    — cryptographic proof of execution state
  Cooling receipt      — thermodynamic cooling ledger
  Kabarkan FQ          — flow quality telemetry bridge
```

**Source:** `/root/arifFlow/` — 20 `.rs` files, `Cargo.toml` v2026.7.26, authored by Arif (F13 SOVEREIGN).

---

## 4. The Federation as a World Model

Cameron Wolfe's *Agentic World Models* (Jul 2026) describes the exact loop our federation runs:

| Wolfe Concept | Federation Equivalent |
|---------------|----------------------|
| **Observation tokens** | Tool output, organ health, receipt state, FQ delta |
| **Action tokens** | Tool call, forge execution, seal |
| **Consequence** | FFF gate scores, FQ delta, new receipt |
| **World model** | Kernel's understanding of federation state |
| **Reward/Verifier** | FFF gates, FQ, receipt verification |

Maksudnya: **The federation IS the observation → action → consequence loop.** Wolfe proves that training agents to predict observation tokens (not just optimize for reward) improves learning efficiency, capability, and generalization. Federation dah ada semua komponen ni — FFF sebagai verifier, VAULT999 sebagai ground truth, FQ sebagai reward signal.

---

## 5. Path A Implications (Agent Training)

Kalau kita train model pada 127 trajectories — training loop KENA:

| Wajib | Jangan |
|-------|--------|
| BBB prompt→response → FFF gates → reward | Ubah MCP interface |
| Output ke GGG trajectory dataset | Ubah VAULT999 seal format |
| D4 receipt guna format sedia ada | Ubah authority chain |
| CPU training, RM0 | Gantungkan pada GPU |

**Training loop adalah plugin ke federation — bukan rewrite federation.**

---

## 6. Invariants Map (Quick Reference)

```
┌─────────────────────────────────────────────────────────────────┐
│                     🔴 TAK BOLEH REPLACE                        │
│                                                                 │
│  MCP + A2A          ← Protocol standard — ecosystem依赖         │
│  Ed25519            ← Root of trust — semua signature           │
│  F13 + F1–F13       ← Perlembagaan — bukan kod                  │
│  000→999 pipeline   ← Metabolic cycle — identity sistem         │
│  VAULT999 chain     ← Immutable truth — foundation              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                     🟡 PATTERN INVARIANT                        │
│                                                                 │
│  Postgres/Qdrant    ← Specific engine → replace. Pattern → wajib│
│  Observation/Action ← Wajib ada. Format flexible                │
│  FFF verifier       ← Verifier atau learned model — pilihan     │
│  LOCALHOST_IS_PASS  ← Prinsip: internal trusted, external block │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                     ⚠️  NEAR-INVARIANT                          │
│                                                                 │
│  Python/TS/Rust     ← Boleh rewrite. Praktikal tak.             │
│  Linux + systemd    ← Boleh ganti OS. Kenapa?                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                     ✅  REPLACEABLE                              │
│                                                                 │
│  LLM provider       ← DeepSeek → Qwen → Groq → Ollama          │
│  Search backend     ← Google API → SearXNG (self-hosted)        │
│  TTS engine         ← OpenAI TTS → edge-tts                     │
│  Observability      ← Langfuse → Kabarkan                       │
│  DB engine          ← Postgres → SQLite (if needed)             │
│  File storage       ← Local → MinIO → R2                        │
│  Reverse proxy      ← Caddy → Nginx                             │
│  Container runtime  ← Docker → bare-metal systemd               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Testable Invariants

Setiap invariant ni ada live probe untuk sahkan:

```bash
# F13 SOVEREIGN — human at /000
curl -sf https://arifos.arif-fazil.com/health | jq '.identity_hash'

# VAULT999 — immutable chain
curl -sf https://arif-fazil.com/999/verify | jq '.verified'

# MCP — protocol contract
curl -sf http://localhost:8088/mcp -X POST \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | jq '.result.tools | length'

# arifFlow — Ψ Nerves
curl -sf http://localhost:7073/health | jq '{organ, receipt_count, cooling}'

# Trinity-33 — all three languages running
curl -sf http://localhost:8088/health | jq '.software_release.language'  # Python
curl -sf http://localhost:7071/health | jq '.runtime'                     # TypeScript
curl -sf http://localhost:7073/health | jq '.organ'                       # Rust
```

---

## 8. Constitutional Alignment

| Floor | Invariant Binding |
|-------|-------------------|
| **F1 AMANAH** | Reversible-first. Setiap replace mesti boleh rollback. |
| **F2 TRUTH** | Setiap claim invariant mesti ada live probe evidence. |
| **F4 CLARITY** | Dokumen ini ΔS ≤ 0 — reduce ambiguity, bukan tambah. |
| **F11 AUDIT** | Setiap change pada invariant mesti sealed ke VAULT999. |
| **F13 SOVEREIGN** | Semua di atas — subject to Arif's absolute veto. |

---

## 9. Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-07-26 | Initial forge — two-frame analysis consolidated | FORGE (000Ω) |
| 2026-07-26 | Rust/arifFlow verified — 20 .rs files, compiled binary | FORGE (000Ω) |
| 2026-07-26 | Ratified by Arif (F13 SOVEREIGN) | Arif |

---

*DITEMPA BUKAN DIBERI ⚒️*
*Yang kita forge sendiri — itu bukti implementation replaceable.*
*Yang tak boleh forge — protocol standards, perlembagaan, truth substrate.*
*Interfaces are invariant. Implementations are replaceable.*
