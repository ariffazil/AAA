# .archive/2026-06-27-stub-batch

> **Provenance:** Quarantined 2026-06-27 by FORGE (000Ω) per F13 directive *"audit model registry in AAA github repo. please organize the model registry accordingly"*.

## Why these files are quarantined

28 stub files moved here from the working tree. They:

1. **Claimed false provenance** — every file's frontmatter asserted `forged_by: FORGE (000Ω) via asal.py`. Verified: `/root/AAA/registries/asal.py:main()` does NOT write yaml files. It only supports `--json` or stdout text. The `forged_by` field is therefore inaccurate.

2. **Lack canonical schema fields** — none of the 28 files contain any of:
   - `sources:` — evidence source list
   - `substrate_evidence:` — API key path, endpoint, plan
   - `promotion_evidence:` — live API receipt IDs
   - `cooling_ledger_ref:` — VAULT999 chain reference
   - `f11_audit_status:` — ACTIVE / PARTIAL / etc
   - `live_evidence_*:` — actual test results

3. **Duplicate already-canonical providers**:
   - `openai_soul.yaml` + `openai_shadow.yaml` — collides with the tracked canonical `gpt/GPT-FAMILY-REGISTRY.md` (3.4 KB, ratified 2026-06-22).
   - `groq_soul.yaml` + `groq_shadow.yaml` and `ollama_soul.yaml` + `ollama_shadow.yaml` — already wired with API keys + rate limit documentation in `/root/AAA/registries/FEDERATION_MODEL.json`.

4. **Generated in a single batch at 23:02 today** — all 28 files have identical mtime and forged_at `'2026-06-27T00:00:00Z'`. They were not forged across multiple forge cycles; they were generated as a single batch.

5. **Cover providers that are not yet substrate-evidenced** — google_gemini, xai_grok, zhipu_glm, nvidia_nemotron, stepfun, tencent_hunyuan, sakana_fugu, bytedance_seed, kuaishou_kling, microsoft_mai, miromind, tokenrouter. None have live API keys at `/root/.secrets/tokens/`.

## What was preserved

Each file's original content is intact. Use `git diff HEAD -- registries/models/<name>` after restoring to verify bytewise identity.

## Restoration

To restore any file to the working tree:
```bash
mv /root/AAA/registries/models/.archive/2026-06-27-stub-batch/<name>.yaml \
   /root/AAA/registries/models/<name>.yaml
```

To delete (after F13 ratification):
```bash
rm /root/AAA/registries/models/.archive/2026-06-27-stub-batch/<name>.yaml
```

## F13 ratification needed

F13 SOVEREIGN must decide for each of the 14 providers whether to:

| Option | Meaning | Effort |
|--------|---------|--------|
| **Enrich** | Add substrate_evidence, live_evidence, sources, cooling_ledger_ref, f11_audit_status — match canonical schema | High (real API keys + probes) |
| **Adopt canonical pattern** | Promote `gpt/GPT-FAMILY-REGISTRY.md` pattern (separate .md per provider family, not soul/shadow split) | Medium |
| **Delete** | F13 confirms false provenance, files are removed permanently | Low |
| **Hold** | Leave quarantined pending future enrichment | None |

The 7 canonical tracked providers (anthropic, deepseek, ilmu, kimi, minimax, qwen, xiaomi_mimo) remain untouched in the working tree.

## Files in this archive

12 provider pairs (24 files) — held pending F13 enrichment ratification:
- `bytedance_seed_{soul,shadow}.yaml`
- `google_gemini_{soul,shadow}.yaml`
- `kuaishou_kling_{soul,shadow}.yaml`
- `microsoft_mai_{soul,shadow}.yaml`
- `miromind_{soul,shadow}.yaml`
- `nvidia_nemotron_{soul,shadow}.yaml`
- `sakana_fugu_{soul,shadow}.yaml`
- `stepfun_{soul,shadow}.yaml`
- `tencent_hunyuan_{soul,shadow}.yaml`
- `tokenrouter_{soul,shadow}.yaml`
- `xai_grok_{soul,shadow}.yaml`
- `zhipu_glm_{soul,shadow}.yaml`

## Files deleted from this archive (F13 ratification 2026-06-27)

3 provider pairs (6 files) — deleted as unambiguous duplicates:
- `openai_{soul,shadow}.yaml` — info canonical at `gpt/GPT-FAMILY-REGISTRY.md` (3.4 KB, ratified 2026-06-22)
- `groq_{soul,shadow}.yaml` — info canonical at `FEDERATION_MODEL.json` with API key + rate-limit docs
- `ollama_{soul,shadow}.yaml` — info canonical at `FEDERATION_MODEL.json` with API key + rate-limit docs

---

*Quarantined 2026-06-27 by FORGE (000Ω) — MiniMax-M3*
*Per F13 SOVEREIGN directive: "audit model registry in AAA github repo. please organize the model registry accordingly"*
*DITEMPA BUKAN DIBERI*