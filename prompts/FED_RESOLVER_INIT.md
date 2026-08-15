# FED-RESOLVER INIT — Next Qwen Code Session (FI-003)

> **Forged:** 2026-08-15, output of the GLM-5.3 session (SEAL-d186bb9c9f934225)
> **Doctrine binding:** `/root/AAA/canon/ACTOR_SURFACE_DOCTRINE.md` (RATIFIED, resit 09db16ec)
> **DITEMPA BUKAN DIBERI**

---

## Boot (30 saat)

1. `source /root/.secrets/kunci-mas.env`
2. Baca `/root/AAA/canon/ACTOR_SURFACE_DOCTRINE.md` — ini undang-undang sesi ini
3. Probe live: `curl :7074/health` (FED) · `curl :8088/health` (kernel) · `fed_status`
4. Ingat dosa lama: satu release GLM = lima commit. Itu penyakit geometri, bukan kerja.

## Misi

**LiteLLM/FED bukan model registry. FED ialah runtime resolver.**

Salah (hari ini): `agents.333.model: glm-5.3` — actor ↘ model, model berubah → actor rosak.
Betul: `333 → contract(reasoning) → FED.resolve() → glm-5.3 → zai` — model berubah → satu edit runtime binding.

Kunci kanun:
```
Actors know contracts.
Contracts know requirements.
FED knows models.
Models never know actors.
```

## Geometri sasaran (4 registry LOGIKAL — bukan semestinya 4 fail baharu)

1. **Actor** (invariant) — sudah wujud: `agent-cards/identity/`, kad 43-medan
2. **Surface** (semi-statik) — sudah wujud: `agents/_external/`, `registries/forge_instruments.yaml`
3. **Capability/CCC** (statik-ish) — sudah wujud: `governance/CCC_DOCTRINE.md`, `capability_signatures` dalam SOT
4. **Runtime binding** (dinamik) — sebahagian wujud: `~/.config/federation-models.json` (`agents[].fallback_chain`, `model_routes`), lane litellm (`dynamic-registry.yaml`: `agi-333`, `apex-888`, `fed-reasoning-heavy`)

## ZEN RULE —连接 arrows, bukan tambah komponen

F13 freeze berkuat kuasa: **jangan cipta fail registry baharu** selagi boleh dibentuk semula dari sedia ada. Sebelum tulis fail baru, jawab: "adakah ini seksyen/namespace dalam SOT sedia ada?" federation-models.json sudah pun mengandungi B+D+catalog — pemisahan 4-registry mungkin *logical keys*, bukan *physical files*. Yang layak mati: pertindihan `AGENT_MODEL_MAP.json` vs `UNIFIED_PROVIDER_REGISTRY.yaml` vs SOT — cadangkan konsolidasi, jangan laksanakan tanpa T2 announce.

## Langkah dicadangkan

1. **Probe** `~/.config/opencode/dynamic-registry.yaml` + lane litellm — kenalpasti lane bernama yang hidup
2. **Peta** permintaan lane → binding runtime hari ini (siapa panggil lane, siapa panggil model mentah)
3. **Tukar satu consumer** (qwen-code atau opencode) dari model mentah → lane; biar direct jadi escape hatch
4. **Echo reflex** untuk kerusi konstitusi: setiap panggilan 888/999 banding `requested_model` vs `returned_model`; mismatch = drift event (arifFlow resit). Silent redirect Z.ai mesti tertangkap hari pertama
5. **RCR metric** masuk resit: `files_changed / model_release`. GLM-6 mesti = 1. Kalau 5 lagi, geometri gagal — bawa ke mahkamah 888

## Kerusi konstitusi — tiada kompromi

888/999: `inhabitant_policy: ratify` (F13 + 888 sahaja bertukar penghuni) + echo attestation.
Route zai coding plan DILARANG untuk kerusi judge — redirect senyap = hakim bertukar tanpa kebenaran.
Sokongan: SHADOW-GLM-004 (`registries/models/zhipu_glm_shadow.yaml` v1.1.0).

## Deliverable sesi

- Minimal diff (connect arrows), resit `sessions.jsonl`, T2 announce untuk sebarang restart
- Cadangan konsolidasi registry (T1.5 propose, jangan auto-laksana)
- Seal Lane B di akhir; laporkan RCR baseline

**Structure remembers; runtime rotates.**
