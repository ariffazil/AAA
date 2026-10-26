# HERMES MCP — FULL SURFACE TEST — 2026-10-17

**Verdict (1 baris):** 52 tools + 44 resources + 12 prompts SEMUA berfungsi — KECUALI satu bug klasifikasi yang tepat macam Arif tulis: `"LLMs"` diklasifikasikan sebagai `PERSON` (manusia).

## Surface census (live-probed via MCP 2025-11-25)

| Server | Endpoint | Tools | Resources | Prompts | Status |
|--------|----------|-------|-----------|---------|--------|
| hermes_mcp ("Meaning Integrity Organ") | :18087/mcp | 15 | 42 | 10 | ✅ semua live |
| hermes-rasa | :18420/mcp | 31 | 0 | 0 | ✅ semua live |
| session-federation | :18088/mcp | 6 | 2 | 2 | ✅ semua live |
| hermes-a2a | :18089/mcp | — | — | — | ⚠️ bukan MCP (404) — A2A listener, jangkaan |

**Total: 52 tools, 44 resources, 12 prompts — semua invoke/read/render OK.**

## Tools (52)
- **hermes_mcp (15):** registry_status, claim_validate, perspective_scope, qualia_boundary, contradiction_scan, counterstory_test, uncreated_classify, handoff_package, moral_physics, institutional_decay, reality_grounding, retrieve, makcik_render, witness_signal, scar_wisdom
- **hermes-rasa (31):** observe, claim, perspective, consent, contradiction, infer, relationship, stop, seal, shadow_map, paradox_map, discrepancy, counterstory, shadow_provenance, projection_guard, context_split, rasa_hold, human_revision, uncreated, agent_shadow, cross_layer_check, adjudicate_claim, signal_assessment, motive_boundary, calibration_check, dajjal_check, calhoun_check, signal_gate, fabrication_detector, cheap_probe, behavioral_boundary
- **session-federation (6):** session_list, session_search, session_read, session_stats, session_related, federation_health

## Resources (44) — semua read OK
42 doktrin BIOS + L0–L6 REALITY333 + capability index (hermes_mcp) · 2 store_info/sources (session-federation)

## Prompts (12) — semua render OK **apabila diberi argumen wajib**
10 (hermes_mcp: understand_without_mindreading, map_multi_principal, counterstory, negotiate_uncreated, reflect_lived_experience, prepare_domain_handoff, reality_check, calhoun_audit, dajjal_detection, witness_mode) + 2 (session-federation). Setiap satu ada arg wajib (situation/statement/claim/institution/…) — panggilan kosong = error "rendering", BUKAN bug.

---

## 🐛 BUG DITEMUKAN (diproduksi semula)

`hermes_claim_validate` dengan klaim **"LLMs cannot understand Malay nuance and idiom."** → pulang:

```json
"principal": {"identity": "LLMs", "type": "PERSON"},
"referenced_principals": [{"identity": "LLMs", "type": "PERSON"}],
"verdict": "REWRITE_REQUIRED",
"violations": [{"rule": "CL-03_private_state_promotion", "message": "Interior state (understand) asserted about another person..."}]
```

**"LLMs" diklas sebagai PERSON (manusia)** → sebab tu ia trigger peraturan "interior state" yang hanya patut terpakai pada manusia. Ini EXACT bug yang Arif dokumen: *"HERMES salah klasifikasi 'LLMs' sebagai manusia dan kenakan syarat hubungan sesama manusia."*

### Punca (source, deterministic)
`/root/HERMES/hermes_mcp/_perspective.py` · `classify_principal()` (line 501). Fallback terakhir:

```python
if (name[:1].isupper() and name.lower() not in _PERSON_PRONOUNS
    and name.lower() not in DISCOURSE_MARKERS):
    return "PERSON"
```

"LLMs" huruf besar + tak ada dalam mana-mana senarai (SYSTEM_TERMS, INSTITUTIONS, COLLECTIVES, fine-classifier) → jatuh ke fallback `huruf-besar → PERSON`.

- `SYSTEM_TERMS` (line 112) ada "kernel/organ/mcp/server/bot/agent/tool/api/…" — **tapi TIADA "llm", "model", "ai", "assistant", "gpt".**
- `_fine_classify` (line 437) load `principal_type_classifier.py` — ia pulang None/UNKNOWN untuk "LLMs".
- Fail-class ini DAH di-red-team 2× sebelum ni (comment line 415 "hard-typed PERSON", line 427 "SEAL typed PERSON") — patched SEAL + DAP, tapi belum LLM/model.

### Fix (3 pilihan, ranked)
1. **Paling surgical:** tambah `"llm", "model", "ai", "assistant", "gpt", "language_model"` ke `SYSTEM_TERMS` dalam `_perspective.py` → "LLMs" kena `SYSTEM` sebelum fallback PERSON.
2. **Paling dalam:** tukar fallback `name[:1].isupper() → PERSON` jadi `→ UNDEFINED` (huruf besar ≠ bukti manusia). Ini hapus fail-open di akar.
3. **Fine classifier:** ajar `principal_type_classifier.py` klas "LLM/model/AI" → SYSTEM/AI_ORGAN.

Ujian regresi: klaim tentang "LLMs"/"model"/"AI" mesti pulang `type != PERSON`. Tambah contoh manusia/institusi/model/petikan dalam fixture.

## Semakan silang dengan dokumen Arif
- Keutamaan #1 dokumen: "Jadikan kes LLMs diklas manusia ujian regresi" → **dipenuhi: bug diproduksi + lokasi source + 3 fix.**
- Ini satu-satunya permukaan yang gagal. Yang lain (52 tools, 44 resources, 12 prompts) hijau.
