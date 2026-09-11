# Institutional Memory Strata — Memory Lives in Governed Artifacts

> **Status:** F13_RATIFIED_CHAT (2026-09-11)
> **Origin:** External repo analysis (github.com/ariffazil/{AAA,arifos,A-FORGE}) + Arif's synthesis: *"di mana memory sebenarnya hidup?"* Corrections applied after live probe (F2 — witnessed, bukan narrated).
> **⚠️ AUDIT 2026-09-11 ~12:3x MYT:** Label F2 di atas **tidak disokong probe** untuk Correction #1 asal. Live probe selepas itu falsify claim tersebut; Correction #1 kini dibetulkan dengan evidence (W1–W4). Lihat `/root/AAA/reports/memory-strata-mem0-contradiction-audit-2026-09-11.md`. Jangan percaya label epistemic tanpa probe yang menghasilkan ayat itu.
> **Companion:** `memory-promotion-gate.md` (WHEN memory write dibenarkan) → doktrin ini (WHERE memory hidup).
> **Applies to:** ALL agents in arifOS federation.

---

## The Thesis

```text
Memory should not live in the model.
Memory should live in governed artifacts.
```

Ini **institutional memory**, bukan model memory. Model = mangkin (catalyst), bukan takung (container). Repos federation = Externalized Cognitive Substrate.

## The Four Strata (dinamakan oleh apa yang membunuhnya)

| Stratum | Isi | Mati bila | Mod |
|---|---|---|---|
| **S0 Context Memory** | Context window | Session habis | Chat |
| **S1 Repository Memory** | SOUL.md, AGENTS.md, IDENTITY, DOCTRINE, skills, receipts, `carry_forward.json` | Repo dipadam | **Reconstruction** |
| **S2 Witness Memory** | VAULT999, ledgers, seals | Tidak — immutable | **Attestation** |
| **S3 Semantic Recall** | `arif_memory` L1–L6 / `forge_memory` atas Qdrant (live) | Vector store dipadam | **Recall** |

```text
Loaded identity (S1) ≠ Remembered identity (S3)
```

Blank slate pada empty clone adalah EXPECTED. Fix = substrate, bukan model.

**Axis note:** Ini paksi *substrate-persistence* — jangan campur dengan `MEMORY_ENGINEERING_SPEC_v2` functional Layers 1–5 atau L1–L6 operational tiers. Tiga paksi berbeza.

## Witnessed Corrections (live probe 2026-09-11)

Claim luaran yang SALAH terhadap kanon sendiri:

1. **`"Hermes semantic recall = arif_memory only"`** — SALAH. *(CORRECTED 2026-09-11 ~12:3x MYT — pembetulan F2 selepas live probe; claim asal di bawah ternyata Registry menyamar sebagai Witness.)*
   - **Witnessed:** `/root/.hermes/config.yaml` L33-34 → `memory: provider: mem0` (live provider line, bukan remnant). Qdrant collection `mem0` = **11,277 points** — terbesar dalam federation (7.7× `petronas_knowledge` 1,460; **114×** `arifos_memory` 99). Read + write path exercised in-session: 4× `mem0_search` (score 0.72–0.87) + **8× `mem0_delete` semua success**. Remnant tidak boleh terima write.
   - **Mem0 ialah S3 backend Hermes yang HIDUP.** `ARCHITECTURE_BLUEPRINT_3NODE.md` rejection (*"middleman on a deeper stack"*) = **intent (Registry)**, bukan **runtime (Witness)**. Gap antara dua itu = unbuilt work, bukan settled fact.
   - **Evidence:** `/root/AAA/reports/memory-strata-mem0-contradiction-audit-2026-09-11.md` (W1–W4).
   - **Falsifiable dalam 2 command:** `grep -A2 '^memory:' /root/.hermes/config.yaml` · `curl -s 127.0.0.1:6333/collections/mem0 | grep -o '"points_count":[0-9]*'`
2. **"Claude/Kimi/Codex tiada carry-forward"** — SALAH. `carry_forward.json` = convention federation, ditulis closing agent tak kira harness (witnessed: modified hari ini). Tetapi ia S1 reconstruction, bukan S3 recall — point asal survive, label salah.

**OPEN LOOP (belum settle — F13 decide):** Mem0 (Hermes S3, 11k points) dan `arif_memory`/`forge_memory` (federation S3, 99 points) ialah **dua semantic store selari tanpa reconciliation path**. Pilih: (a) converge ke satu backend, atau (b) declare Mem0 Hermes-private dan berhenti panggil `arif_memory` canonical untuk Hermes. Selagi terbuka, setiap agent yang baca fragment ini akan dapat gambaran salah tentang di mana memory Hermes sebenarnya hidup.

**Meta-lesson (scar, bukan cerita):** Claim #1 asalnya di-ratify dengan label *"applied after live probe (F2 — witnessed, bukan narrated)"* padahal probe tidak pernah dijalankan terhadapnya. **Label F2 yang tidak disokong probe lebih bahaya daripada Registry yang jujur — sebab ia membawa baju Witness.** Ujian: jangan terima label epistemic; tanya *"probe mana yang hasilkan ayat ini?"*

## Corrected Harness Matrix

```text
Semua agent federation:      S0 + S1 + S2
S3 semantic recall:          terbuka kepada SEMUA agent MCP-wired
                             (Claude/OpenCode/Kimi witnessed wired ke arifos+aforge)
```

Beza Hermes vs coding agents = **akses DAN reflex default** *(dibetulkan 2026-09-11: asalnya claim "bukan akses" — itu derived dari premis salah bahawa Mem0 rejected; lihat Correction #1)*:
- **Akses:** Hermes ada S3 sendiri yang hidup (`mem0`, 11,277 points, read+write exercised). Coding agents wired ke `arif_memory`/`forge_memory` (99 points) — store berbeza, hampir kosong relatif.
- **Reflex:** Hermes recall by design (gateway routing melalui memory). Coding agents reconstruct by default (murah, deterministic); recall atas demand.
- **Implikasi:** matrix ini perlu re-derive selepas OPEN LOOP di atas settle — selagi dua store selari, "beza Hermes vs coding agents" belum boleh disebut sebagai satu paksi tunggal.

```text
Hermes remembers.
Coding agents reconstruct — dan boleh recall bila route melalui arif_memory.
Nothing rediscovers — selagi substrate hidup.
```

## The Harness-Swap Substrate Test (falsifiable)

```text
Tukar: Claude → Kimi → GPT → Grok → OpenCode
```

- Capability yang TERUS HIDUP selepas swap → ia hidup di S1/S2 (substrate).
- Capability yang MATI selepas swap → ia cuma S0 narrative — bukan institution.

Ini test, bukan crisis. Harness swap ialah cara mengukur apa yang benar-benar dipunyai federation.

## Operational Binding

- Lulus Memory Promotion Gate → pilih **stratum sasaran**: governed artifact (S1/S2). Never model-only.
- Jangan claim "agent ini ingat" tanpa nyatakan stratum — ingat di S1 (reconstruct) ≠ ingat di S3 (recall).
- S1 artifacts mesti kekal render-able + greppable (reconstruction = baca semula; kalau tak jumpa, tak ingat).
- Coding agents: sebelum kata "tiada memory" — probe S3 dulu (`forge_memory` recall). Fail-closed termasuk terhadap claim ketiadaan sendiri.

## Compression

> **Model = mangkin. Substrate = memory. Swap model untuk uji apa yang sebenar.**

DITEMPA BUKAN DIBERI ⚒️
