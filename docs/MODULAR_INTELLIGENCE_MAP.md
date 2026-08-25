# arifOS MODULAR INTELLIGENCE MAP — System State
> Generated 2026-08-25 · Deep audit of all agentic layers
> This is the composition reference: what exists, how it stacks, how it modularizes.

---

## THE STACK (6 layers, bottom-up)

```
L5  DELIVERY          Telegram / PDF / PPTX / Voice / Email / Web
L4  PIPELINES         civic_briefing · trading_signal · video_gen · research_dossier
L3  CAPABILITIES      image_gen · video_gen · chart · map · flow · tts · asr · vision ...
L2  MCP SERVERS       41 tool servers (organs + substrate)
L1  MODELS            58 FED + 17 FLAME + 27 provider lanes
L0  INFRASTRUCTURE    VPS · secrets · LiteLLM :4000 · FLAME :18901 · Python stack
```

---

## LAYER 0 — INFRASTRUCTURE

| Surface | Detail |
|---|---|
| LiteLLM FED | :4000, 58 models, 4-model cascades, actor-envelope groups |
| FLAME | :18901, 17 free models (Groq/Gemini/Qwen/SEA-LION), RM0 lane |
| Python stack | numpy/pandas/polars/scipy + matplotlib/seaborn + geopandas/cartopy/folium + reportlab/weasyprint/pdfkit/pymupdf + python-pptx + opencv/pillow + playwright + librosa/pydub/soundfile + httpx/requests/aiohttp |
| Secrets | /root/.secrets/kunci-root.env (5-R protocol, mode 600) |
| CLI engines | google-chrome (headless PDF), graphviz dot, mermaid mmdc |

---

## LAYER 1 — MODELS (102 across lanes)

### FED Actor-Envelope (:4000) — 58 models
| Group | Alias | Role |
|---|---|---|
| Identity | `i-arif` | sovereign voice (default) |
| Reason | `agi-333` | reasoning |
| Verify | `asi-555` | research/verify |
| Code | `forge-777` | code (propose-only) |
| Judge | `apex-888` | constitutional |
| Vision | `fed/vision` | image understanding |
| Image | `fed/image-gen` | image synthesis |
| Audio | `fed/audio` | audio/video |

### FLAME free tier (:18901) — 17 models
Groq LPU (llama, gpt-oss, qwen3.6) · Gemini free · Qwen3.7-flash · SEA-LION BM-native

### Direct provider lanes — 27
dashscope-payg (image+video+tts+asr) · qwen-token-plan×4 seats · mimo-token-plan ·
minimax · opencode-go/zen · zai-coding-plan · gemini · groq · mulerouter ·
openrouter · perplexity · sea-lion · deepseek · anthropic · ollama (local recovery)

**Modularity rule:** FED alias = stable identity; provider lane = cost/quota knob.
Swap provider without changing caller.

---

## LAYER 2 — MCP SERVERS (41)

### Federation organs (constitutional)
`arifos` (kernel F1-F13) · `aforge` (execution actuator) · `arifflow` (FQ metabolism) ·
`geox` (Earth) · `wealth` (capital) · `well` (human readiness) · `fed` (router) ·
`mage` (image gen/edit) · `minimax-media` (image/video/music/tts)

### Substrate / tools
`playwright` (browser) · `github` · `postgres` · `sqlite` · `supabase` · `qdrant` (vector) ·
`graphiti` (knowledge graph) · `hindsight` (agent memory) · `docker` · `semgrep` (SAST) ·
`fetch` · `brave-search` · `exa` · `perplexity` · `firecrawl` (RM0 web) · `osm` (location) ·
`mapbox` · `composio` (Gmail/Reddit) · `social-mcp` · `context7` (docs) · `serena` (code) ·
`repomapper` · `sequential-thinking` · `capability-index` · `hermes` (governance) ·
`hostinger-vps` · `deep-research` (❌) · `notebooklm` (❌) · `openrouter` (❌)

**Modularity rule:** organs = domain reasoning (stateful, governed).
substrate = atomic tools (stateless). Orchestrate organs, call substrate.

---

## LAYER 3 — CAPABILITIES (atomic operations)

| Capability | Primary tool/script | Models | Fallback |
|---|---|---|---|
| image_gen | `dashscope_media.py image` | wan2.7-image, qwen-image-3.0-pro | MiniMax MCP → Gemini |
| image_edit | `dashscope_media.py edit` | wan2.7-image-pro | mage MCP |
| video_t2v | `dashscope_media.py video t2v` | wan3.0-video, happyhorse-1.1-t2v | minimax-media |
| video_i2v | `dashscope_media.py video i2v` | happyhorse-1.1-i2v | minimax-media |
| chart | `civic_analytics.py chart` | matplotlib/seaborn | reportlab |
| map | `civic_analytics.py map` | geopandas/cartopy | folium (interactive) |
| flow | `civic_analytics.py flow` | graphviz dot | mermaid mmdc |
| mermaid | `civic_analytics.py mermaid` | mmdc | — |
| pdf_render | weasyprint / chrome headless | — | pdfkit |
| pptx | python-pptx / pptxgenjs | — | — |
| tts | i-arif-sovereign pipeline | minimax speech-2.8-hd | edge-tts Yasmin |
| asr | Groq whisper-turbo | — | faster-whisper local |
| vision | fed/vision | qwen-vl-max | MiMo |
| web_search | firecrawl / searxng | — | brave/exa/perplexity |
| browser | playwright MCP | — | chrome headless |

**Modularity rule:** each capability has a PRIMARY (free quota first) + ordered fallback.
`dashscope_media.py` + `civic_analytics.py` are the unified wrappers.

---

## LAYER 4 — PIPELINES (reusable composition)

| Pipeline | Composition | Output |
|---|---|---|
| `civic_briefing` | content → analytics(chart/map/flow) → HTML render → PDF | briefing.pdf + assets |
| `video_gen` | prompt → image(frame) → i2v → poll → download | .mp4 |
| `trading_signal` | OHLC → indicator → chart → PDF → Telegram | signal.png/pdf |
| `research_dossier` | search → extract → synthesize → pdf | dossier.pdf |
| `voice_note` | text → i-arif TTS → ogg | voice bubble |

---

## LAYER 5 — DELIVERY
Telegram (ASI_arifOS_bot, one bot, free-response groups) · PDF/PPTX file ·
Voice bubble · Email (Brevo) · Web deploy

---

## SKILL CLUSTERS (347 skills, grouped by domain)

| Cluster | Count | Anchor skills |
|---|---|---|
| FORGE (infra/ops/code) | ~90 | github-ops, vps-docker, fastmcp, cicd, secret-hygiene |
| ASI/APEX (governance) | ~20 | agent-invariants, drift-watch, fabrication-prevention |
| AAA (audio/media/voice) | ~15 | tts-engine-catalog, voice-cloning, audio-emd |
| Media (gen/edit) | ~20 | minimax-image-gen, token-plan-image, happyhorse-video |
| Research | ~20 | deep-research, dossier, intelligence-briefing |
| Creative | ~15 | civic-intelligence-pdf, scientific-pdf, open-slide |
| Productivity | ~10 | xlsx, powerpoint, pdf, ocr |
| Legal/counseling | ~8 | family-law, tenancy, decision-advisory |
| Trading | ~6 | XAUUSD-stack, agentic-trading, mt5 |
| GEOX/Wellness | ~8 | geox-grounding, well-operations |
| Runtime/substrate | ~30 | kernel-bind, observe-ground, route-dispatch, memory-manage |

---

## MODULARITY PRINCIPLES (the system contract)

1. **Registry is SOT.** `/root/.config/capability_registry.json` maps intent→capability→tool→model.
   Hermes config / picker configs are CONSUMERS, not authority.
2. **Free quota first.** DashScope/Token Plan before Gemini/MiniMax. Enforced in capability order.
3. **Alias over endpoint.** Call FED alias or wrapper script, never raw curl per-task.
4. **Compose, don't duplicate.** Pipelines call capabilities; capabilities call tools; tools call models.
5. **Governed vs atomic.** Organs reason (stateful), substrate executes (stateless).
6. **Every act receipts.** F11 audit — image/video/seal all leave a receipt.
7. **ΔS ≤ 0.** Reversible-first. Constitutional changes need F13.

---

## GAPS → ACTIVE WORK (delegated to Qwen Code)

1. `capability_registry.json` — full 347-skill audit → capability map (IN PROGRESS)
2. `capability_router.py` — intent→execution-plan query interface
3. `pipeline_civic_briefing.py` — auto-compose civic PDF + analytics
4. `civic-intelligence-pdf` skill → wire to pipeline

**Done in this session (by Hermes):**
- `dashscope_media.py` — unified DashScope image+video wrapper (tested ✅)
- `civic_analytics.py` — chart/map/flow/mermaid analytics layer (written)
- `ACTION_LADDER.yaml` — capability_map flipped DashScope-primary
- `forge-multimodal-router` skill — hard routing doctrine added

*DITEMPA BUKAN DIBERI — 2026-08-25*
