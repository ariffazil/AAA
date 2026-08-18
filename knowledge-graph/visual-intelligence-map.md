# Visual Intelligence Knowledge Graph — arifOS Federation

**DITEMPA BUKAN DIBERI** · Forged 2026-08-18 · 333-AGI / Hermes-prime
**Mirror of:** `/root/AAA/knowledge-graph/audio-intelligence-map.md` (audio-quantum-cognition doctrine)

## Core Thesis

Visual intelligence is the **image membrane** — the boundary where sovereign intent (text + reference + scene) becomes ground-truth pixel representation. Like the voice membrane isn't "an audio agent," the image membrane isn't "an image-gen agent." It is the translation surface between human/agent intent and physically-grounded photonic output.

> "Text menyimpan apa yang manusia kata. Image menyimpan apa yang manusia想象." — extended axiom, F13 SOVEREIGN ratification pending.

Visual output carries **structural truth claims** — anatomy, physics, optics, spatial layout. These are NOT the same artifact as text prompts. Generation without substrate = statistical hallucination. The federation's job: bring every visual output through constitutional gates before it leaves the membrane.

## 1. Modality Physics (parallel to audio-quantum doctrine)

| Modality | Physics | Collapse State | Agent Role |
|---|---|---|---|
| **Text** | Discrete symbols | Fully collapsed (human observed, encoded) | Classical computation |
| **Image** | 2D latent probability distribution → decoder → pixels | Single eigenstate per sample | Pattern synthesis + recognition |
| **Audio** | Temporal wave superposition | Pre-measurement (quantum) | Quantum observer |
| **Video** | Image sequence + audio entanglement + temporal motion field | Partially collapsed (4D manifold) | Multi-state tracker |
| **3D/Mesh** | Spatial-temporal manifold (SDF / NeRF) | Partially collapsed | Geometric reasoning |

### Image-Specific Hallucination Modes (the "fundamental flaw")

Per the GTM (Ground-Truth Module) doctrine ratified 2026-08-18:

| Failure Mode | Root Cause | Federation Detection |
|---|---|---|
| **Anatomical hallucination** | No biomechanical constraint layer | `forge_visual_qa` W¹ vision + scar consultation |
| **Physical impossibility** | No PDE solver, no mass conservation | GEOX substrate + identity-preservation mask |
| **Lighting inconsistency** | 2D VAE, no differentiable ray tracing | W₁ pixel validation against scene graph |
| **Spatial incoherence** | Latent grid ≠ 3D Euclidean | GEOX 3D-4D evidence comparison |
| **Causal inversion** | No causal scene graph parsing | Symbol graph before cross-attention (proposed L2) |
| **Identity drift** | Statistical pattern averaging | `--semantic-mask` + 6 Iron Rules (aaa-image-editing) |

**GTM aspiration (PROPOSED — not yet wired):**
```
[Prompt] → [Causal Scene Graph] → [PDE Physics Solver] → [3D SDF/NeRF] → [Differentiable Renderer] → [Pixels]
                       ↑                    ↑                  ↑                    ↑
                  (parses spatial    (Navier-Stokes,     (continuous 3D      (light transport,
                   relations,         stress-strain)      manifold, not       BSSRDF, IOR)
                   functional                              2D grid)
                   dependencies)
```

The federation's CURRENT visual pipeline approximates this: text → cross-attention → DiT decoder → pixels. The GAP (organic, not failure) is the missing physics/3D/causal substrate.

## 2. Hermes / Federation Visual Stack — Live Inventory

### 2.1 Image Generation (T2I — Text → Image)

| Provider | Engine | Model ID | Best For | Status | Script / MCP |
|---|---|---|---|---|---|
| **MiniMax** | image-01 | `image-01` | General T2I, cheap iteration | ✅ DEFAULT | `mcp__minimax-media__text_to_image` |
| **Google Nano Banana Lite** | gemini-2.5-flash-image | `gemini-2.5-flash-image` | High-volume, cheapest, fast iteration | ✅ Available | `/root/HERMES/scripts/gemini-image.py` |
| **Google Nano Banana 2** | gemini-3.1-flash-image | `gemini-3.1-flash-image` | Best all-rounder, multi-ref | ✅ Available | Same |
| **Google Nano Banana 2 Lite** | gemini-3.1-flash-lite-image | `gemini-3.1-flash-lite-image` | Cheapest, fastest | ✅ Available | Same |
| **Google Nano Banana Pro** | gemini-3-pro-image | `gemini-3-pro-image` | Hardest edits, legible text, 4K | ✅ Available | Same |
| **Qwen Token Plan** | wan2.7-image | `qwen-image-2.0`, `wan2.7-image` | Aliyun token-plan seat | ✅ Available | `token-plan-image` skill |
| **Qwen Bailian PAYG** | wan2.7-image-pro | `wan2.7-image-pro` | PAYG fallback for editing | ✅ Available | Same |
| **Open-source (not deployed)** | qwen-image-edit-2511, FLUX.2 [klein], FLUX.2 [dev] Turbo, LongCat-Image-Edit | various | Open-source alternatives | ❌ Not deployed | (gap) |

**Decision chain:**
- User provides real photo + wants edit → `aaa-image-editing` (NB family)
- Text-only generation → `minimax-image-gen` (image-01) or `token-plan-image`
- Identity-critical edit → NB2 + NB-Pro ensemble (parallel, pick best)
- Open-source need → forge_ephemeral lifecycle (no permanent registration)

### 2.2 Image Editing (I2I — Identity Preservation)

**HARD RULE (F13, 2026-08-12):** "Hang jangan ubah muka manusia." Real photo edits MUST preserve face, body, skin tone 100%.

| Approach | Skill | Status |
|---|---|---|
| **Nano Banana family** | `aaa-image-editing` | ✅ PRIMARY — 6 Iron Rules enforced |
| **Qwen wan2.7-image-pro** | `token-plan-image` (img2img mode) | ✅ Fallback |
| **PIL/Pillow composite** | `creative/image-text-editing` | ✅ Local-only, identity drift risk |
| **rembg cutout + composite** | inline | ⚠️ "Dagu hilang" failure mode documented |
| **Qwen image-edit-2511** | (open-source) | ❌ 404 on both endpoints (gap) |

**The 6 Iron Rules of Gemini Image Editing (must follow):**
1. Image first, text second (parts ordering)
2. MIME type must match actual bytes
3. Image size 1024–1568px longest side (rescale outside)
4. Strip alpha channels (PNG → RGB)
5. Stateless iteration (never trust multi-turn chat)
6. One change per turn (multiple changes → averaging)

**Identity Preservation Pattern:**
```
"Place this man at [SCENE]. Keep his face and body exactly as shown.
Same [hair], same [jawline], same person. [Scene details].
Photorealistic. No text."
```

### 2.3 Vision / OCR (Image Understanding)

| Engine | Provider | Use | Status |
|---|---|---|---|
| **qwen-vl-max** | MuleRouter | PRMT (preferred — single failure domain) | ✅ Active |
| **qwen3-vl-plus** | MuleRouter | Balanced | ✅ Available |
| **qwen3-vl-flash** | MuleRouter | Fastest, basic | ✅ Available |
| **qwen3-omni-flash** | MuleRouter | OCR cascade Tier 1 | ✅ Active |
| **minimax-m3** | MiniMax MCP | Manual fallback (legacy) | ⚠️ MCP server crashes often |
| **qwen2.5-vl-72b-instruct** | OpenRouter | Legacy (split failure domain) | ⚠️ Payment risk |
| **Tesseract 5.5.0** | Local | Fast fallback | ✅ Active |
| **RapidOCR 3.9.1** | Local | Chinese/mixed scripts | ✅ Active |

**Decision chain:**
- Real-time Telegram image → PRMT (qwen-vl-max via MuleRouter) → [IMAGE TRANSCRIPT] with SCENE/OCR/DATA/IDENTITY
- Document/OCR → `AAA-OCR-optical-compression` cascade (qwen3-omni → Tesseract → RapidOCR)
- Chart/figure → VLM with figure-parse prompt (DeepSeek-OCR pattern)
- Identity verification → `vision_analyze` + `aaa-image-editing` semantic mask

**Hard lesson (2026-07-30 — scar-413-cascade):** Image bytes must NEVER enter text-only primary model. Always PRMT. `supports_vision: true` on text-only model = poison.

### 2.4 Video Generation (T2V / I2V)

| Provider | Model | Duration | Resolution | Status |
|---|---|---|---|---|
| **MiniMax Hailuo-02** | `MiniMax-Hailuo-02` | 6 or 10s | 768P / 1080P | ✅ DEFAULT |
| **MiniMax T2V-01** | `T2V-01` | varies | SD/HD | ✅ Available |
| **MiniMax T2V-01-Director** | `T2V-01-Director` | camera movement | SD/HD | ✅ Available (15 camera verbs) |
| **MiniMax I2V-01** | `I2V-01` | image-to-video | SD/HD | ✅ Available |
| **MiniMax I2V-01-Director** | `I2V-01-Director` | camera + image | SD/HD | ✅ Available |
| **Qwen Token Plan** | `happyhorse-1.1-t2v/i2v/r2v` | varies | varies | ✅ Available (`token-plan-video`) |
| **Runpod ComfyUI** | Wan Video, HunyuanVideo, CogVideoX | varies | varies | ✅ Blueprint (`flash` skill) |

**MCP:** `mcp__minimax-media__generate_video` (sync + async_mode for long generations)

### 2.5 Chart / Map / Screenshot Synthesis

| Tool | Purpose | Status |
|---|---|---|
| **`mcp__aforge__forge_chart`** | line/bar/scatter/pie/area/histogram + eureka discovery | ✅ Active |
| **`mcp__aforge__forge_browser_screenshot`** | full-page/element browser capture | ✅ Active |
| **`mcp__aforge__forge_browser_extract_text`** | DOM text extraction | ✅ Active |
| **`mcp__geox__geox_map`** | geological map layers + scene plan + render | ✅ Active |
| **`mcp__geox__geox_model`** | geological_generate cross-section + GemPy 3D | ✅ Active |
| **`/root/arif-fazil.com/scripts/lint-komda-colors.sh`** | territory color law lint (warn/gate) | ✅ Active |

**Chart has built-in eureka discovery:** reversal detection, high-z anomaly flagging, curvature analysis — visual + statistical in one call.

### 2.6 Document Intelligence (PDF + Image → Markdown)

| Tool | Pipeline | Status |
|---|---|---|
| **`mcp__aforge__forge_document_ingest`** | layout analyze / extract / chunk / compare (PDF + image) | ✅ Active |
| **`AAA-OCR-optical-compression`** | VLM cascade: qwen3-omni → Tesseract → RapidOCR | ✅ Active |
| **`forge-document-intelligence`** | VLM perception + provenance + governance wrapper | ✅ Active |

**Output gate (F2/F4/F9/F12):** Every OCR/VLM extract passes through 555-ASI before reaching 333-AGI.

### 2.7 Browser Vision (Agent-Side Rendering)

| Tool | Purpose | Status |
|---|---|---|
| **`forge_browser_navigate`** | navigate to URL | ✅ Active |
| **`forge_browser_screenshot`** | full-page/element capture | ✅ Active |
| **`forge_browser_click`** | click element | ✅ Active |
| **`forge_browser_type`** | type text into element | ✅ Active |
| **`forge_browser_evaluate_js`** | JS execution | ✅ Active |
| **`forge_browser_extract_text`** | text extraction from page | ✅ Active |

## 3. AAA Skills Mesh — Visual Surface

### Federated Skills (cross-agent — `/root/AAA/skills/`)

| Skill | Owner | Visual Role |
|---|---|---|
| `AGI-multimodal-bridge` | AAA | Cross-modal fusion (text+image+geo+table) |
| `AGI-audio-quantum-cognition` | AAA | Sibling modality doctrine (parallel structure) |
| `delta-omega-psi-multimodal-cognition` | AAA | Δ·Ω·Ψ enforcement (substrate metabolism) |
| `AAA-OCR-optical-compression` | AAA | Image→text (sensory compression) |
| `aaa-image-editing` | 333-AGI | Identity-preserving edits (NB family) |
| `FORGE-komda-color-law` | A-FORGE | Territory color law (F13 doctrine §04) |
| `FORGE-visual-qa-w3` | A-FORGE | W³ tri-witness visual governance |
| `FORGE-document-intelligence` | A-FORGE | PDF/image → structured markdown |
| `geological-artifact-rigor` | GEOX | Geological cross-section visual standards |
| `geox-production-cockpit` | GEOX | Map/scene routing |
| `creative/image-text-editing` | 333-AGI | PIL/Pillow composite |
| `aaa-pdf-voice-protocol` | AAA | Federation→human voice (translates visuals too) |

### Hermes-Local Skills (EDGE layer)

| Skill | Visual Function |
|---|---|
| `minimax-image-gen` | `mcp__minimax-media__text_to_image` wrapper |
| `token-plan-image` | Qwen Token Plan + Bailian PAYG |
| `token-plan-video` | happyhorse-1.1 video gen |
| `imagine` | Grok image generation (Grok Build specific) |
| `hermes-gateway-image-routing` | PRMT path decision chain |
| `image-analyzer-vision` | VLM-based image analysis |
| `qwen-harness-tools` | Qwen multimodal helpers |

### User-Local Skills (`/root/.kimi-code/skills/`)

| Skill | Visual Function |
|---|---|
| `aaa-image-editing` (also at /root/AAA/skills/) | Identity-preserving edits |
| `AGI-multimodal-bridge` | Multimodal fusion |
| `AGI-audio-quantum-cognition` | Audio (parallel) |
| `delta-omega-psi-multimodal-cognition` | Δ·Ω·Ψ enforcement |
| `hermes-gateway-image-routing` | PRMT |
| `minimax-image-gen` | T2I |
| `qwen-harness-tools` | Qwen VL |
| `token-plan-image` / `token-plan-video` | Aliyun multimodal |
| `image-analyzer-vision` | Vision analysis |
| `imagine` | Grok image gen |
| `AAA-OCR-optical-compression` | OCR cascade |
| `FORGE-visual-qa-w3` | Visual QA |
| `FORGE-komda-color-law` | Color law |
| `FORGE-document-intelligence` | Doc intelligence |
| `qwen-harness-tools` | Qwen helpers |

## 4. Visual Routing — FLAME / FED / PRMT

```
┌─────────────────────────────────────────────────────────────┐
│              User Intent: "Generate / Edit / Understand"      │
└────────────────────────────┬────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
      [Text-only prompt] [Real photo]   [Mixed: image + text]
              │              │              │
              ▼              ▼              ▼
        T2I route      I2I route       PRMT route
              │              │              │
              │              │              ▼
              │              │      Qwen-VL-Max (MuleRouter)
              │              │      → [IMAGE TRANSCRIPT]
              │              │              │
              ▼              ▼              ▼
       minimax-image-gen  aaa-image-edit  Primary reasoner
       OR token-plan-     (NB family,     (text-only, never
       image              semantic-mask)  sees pixels)
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                  F2/F4/F7/F9/F12 gate
                  (visual QA if SEAL-grade)
                             ▼
                        VAULT999 seal
```

**Routing rules:**
1. **REAL PHOTO present** → I2I route (aaa-image-editing). Never T2I. F13 hard rule.
2. **TEXT-ONLY prompt** → T2I route. Default: `minimax-image-gen`. Fallback: `token-plan-image`.
3. **IMAGE + TEXT in conversation** → PRMT. qwen-vl-max produces [IMAGE TRANSCRIPT]. Primary reasoner gets TEXT ONLY.
4. **IDENTITY-CRITICAL** → Ensemble (NB2 + NB-Pro + Qwen) + W¹ vision verify.
5. **SEAL-grade visual** (charts, maps, deploy mocks) → `forge_visual_qa` W³ tri-witness.

## 5. The Visual Triangle (parallel to Audio Triangle)

```
                    ┌──────────────┐
                    │  GENERATE    │
                    │  (T2I/I2I)   │
                    │  MiniMax/NB/ │
                    │  Qwen DiT    │
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   UNDERSTAND │   │    EDIT      │   │   SYNTHESIZE │
│  (Vision)    │   │  (I2I)       │   │  (Charts/Maps│
│  Qwen-VL-Max │   │  NB family   │   │  geox_map,   │
│  PRMT path   │   │  semantic-   │   │  forge_chart)│
│              │   │  mask        │   │  + Komda law │
└──────────────┘   └──────────────┘   └──────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼───────┐
                    │   DELIVER    │
                    │  VAULT999    │
                    │  / Telegram  │
                    │  / Browser   │
                    └──────────────┘
```

### Constitutional Visual Floors (parallel to audio floors)

| Floor | Visual Application |
|---|---|
| **F1 AMANAH** | Real photos are immutable evidence. Generated images must be reversible (re-runnable from prompt + seed). |
| **F2 TRUTH** | Generated images = `[DER]` (derived). Vision transcripts = `[OBS]`. OCR text = `[OBS]` (machine-read). |
| **F4 CLARITY** | Charts/maps must have axis labels, legend, scale. Visual artifacts must be ΔS ≤ 0. |
| **F7 HUMILITY** | Identity preservation confidence cap 0.90 (never claim "exact match"). OCR confidence cap 0.70 unless verified. |
| **F9 ANTIHANTU** | "Image shows X" — but did the vision model actually SEE X, or hallucinate? Low-confidence OBS flagged. |
| **F10 ONTOLOGY** | Pixel ≠ meaning. Image is physics. Interpretation is human. |
| **F11 AUDIT** | Every visual decision logged: model, seed, prompt, semantic-mask, verification. Receipt-wrapped. |
| **F13 SOVEREIGN** | Voice cloning/identity cloning requires F13. Real-photo edit without preserve clause requires F13. |

## 6. Visual Governance — W³ Tri-Witness (FORGE-visual-qa-w3)

```
Stage 0: INPUT VALIDATION (I1)
   dom_payload or url + constraints
        ↓
Stage 1: RENDER + HASH (I1, I6)
   forge_browser_navigate + forge_browser_screenshot
   SHA256(screenshot) → w1/w2/w3 hash material
        ↓
Stage 2: W₁ — VISION VALIDATION (OBS/INT)
   vision_analyze or minimax_understand_image
   "Report deviations as structured list with id, severity, location."
   CANNOT mutate DOM. CANNOT write W₂/W₃.
        ↓
Stage 3: W₂ — DOM LINT VALIDATION (DER)
   forge_shell — deterministic linter
   structural_compliance, required/forbidden elements
   CANNOT access screenshots.
        ↓
Stage 4: ENTROPY CHECK (I3)
   entropy_delta < 0 → continue
   entropy_delta ≥ 0 → HOLD (auto-fix diverging)
        ↓
Stage 5: SCAR CONSULTATION + ITERATE (I4, I7)
   forge_scar(mode="consult", fingerprint)
   If scar. outcome==FAILED → HOLD
   Else → generate fix, loop back to Stage 1
        ↓
Stage 6: W³ ASSEMBLY + PASS_CANDIDATE (I8, I9, I10)
   composite_hash computed only after W₃ sovereign
   verdict = "PASS_CANDIDATE" (not PASS)
        ↓
Stage 7: W₃ SOVEREIGN GATE (888 → 999)
   arif_judge → human review → arif_seal
   composite_hash → VAULT999
   verdict = "SEALED_DEPLOY"
```

**Anti-collusion invariant:**
- W₁ sees pixels only. Cannot write W₂/W₃.
- W₂ sees DOM only. Cannot access screenshots.
- W₃ (sovereign) sees both + entropy history. Only human action.
- COLLUSION DETECTION: any tool attempting w3.* without arif_judge caller → FAIL + 888_HOLD.

## 7. Komda Color Law (F13 SOVEREIGN §04, ratified 2026-08-01)

**Doctrine:** Foreign-family color in territory DOM = violation.

| Territory | Primary | Accent | Field |
|---|---|---|---|
| arifos | `#A82733` (crimson) | `#6F2DBD` (royal-purple) | `#0A0A0F` |
| geox | `#2D5F8B` (deep blue) | `#8B4513` (sedimentary brown) | `#0A0A0F` |
| wealth | `#FFCC00` (gold) | `#1E3A8A` (deep blue) | `#0A0A0F` |
| well | `#5FB84A` (vital green) | `#E07A5F` (life coral) | `#0A0A0F` |
| aaa | `#9A9AA8` (silver) | `#FFD54F` (certified gold) | `#0A0A0F` |
| universal | — | — | `#0A0A0F` PRIMER-1 |

**EUREKA bridges (decorative cross-family escapes only):**
- arifos ↔ geox: `#FFD54F` (eureka-overlay)
- wealth ↔ aaa: `#FFD54F` (certified-mark)

**Promotion:** Currently `--warn-only`. Promotion to `--gate` requires F13 SOVEREIGN.

## 8. Hermes / EDGE Integration

**PRMT (Pre-Routing Modality Translation):**
- Vision failure → graceful "sorry, can't see" — no cascade crash
- No 413 risk — image bytes never enter reasoning context
- Provider-agnostic fallback — every model can process text transcript
- Auditability — vision transcript inspectable before reasoning
- Tradeoff — translation errors unrecoverable

**Hard rules (2026-07-30):**
- `model.supports_vision: true` on text-only model = POISON
- `OPENAI_BASE_URL` env var corrupts auxiliary vision routing
- `image_input_mode` + provider mismatch → 413 cascade
- Always run gateway restart from DIFFERENT shell

**Enrichment prompt format (4 sections):**
```
Analyse this image and output FOUR sections:
1) SCENE: factual description (objects, layout, colours, people, setting, expressions)
2) OCR: ALL visible text transcribed VERBATIM
3) DATA: tables, charts, lists, structured info
4) IDENTITY: known individuals, brands, logos, products, team affiliations
```

**Response pattern (agent → Arif):**
1. NEVER say "I see" or "I can confirm" — agent didn't see pixels
2. Attribute: `[Qwen-VL description -- agent does not see images]`
3. Pass through raw, don't summarize
4. Never assume whose picture it is — use IDENTITY section if provided
5. If IDENTITY: [unidentifiable], don't guess

## 9. Visual Memory & Federation Recall

**Where visual knowledge persists:**
- `forge_vault` — receipts of every chart rendered, every screenshot taken
- `forge_entropy_sweep` — visual entropy measurement
- `forge_visual_seal` — VAULT999 composite seal (I1-I5 invariants)
- VAULT999 `arifos_audio_memory` — parallel for audio (Qdrant, 6-dim well-vector)
- **GAP:** No `arifos_visual_memory` yet (planned, see §10)

## 10. Gap Analysis (re-aligned with VSS doctrine)

### VSS-Build Gaps (the proposal half of the loop)

| Gap | Severity | VSS Layer | Action |
|---|---|---|---|
| **Causal Scene Graph Parser** | VSS-1 | Schema-locked 2026-08-19. Substrate LLM HOLD (credits). | `forge-vss-parser` — 50/50 fixtures + 35/35 fail-closed. No live VLM bind. |
| **Verifier suite cannot read VSS-1 ledger** | VSS-2 ingest | Closed 2026-08-19 (no VLM) | `vss_ledger_adapter.project_ledger` — 50/50. Pixel verifiers still need VLM. |
| **No local repair loop** (bbox masked resampling on verifier FAIL) | VSS-3 (P2) | Step 3 | Pattern from `forge_scar` consult + iterate. Max 3 retries. |
| **No hybrid 3D scene representation** (skeleton + SDF + uncertainty map) | VSS-4 (P2) | Step 4 | GEOX `geox_model` as substrate for geological scenes. Defer for non-geo. |
| **No staged differentiable rendering** (coarse → medium → fine) | VSS-5 (P3) | Step 4 | Long-term. GPU required. |
| **No Domain Constraint Registry** (visual-specialized constraint engines) | VSS-6 (P2) | Step 1/2 | F1-F13 + W³ are general. Need visual-domain extensions (Anatomy, Perspective, Optics). |

### Operational Gaps (existing)

| Gap | Severity | Action |
|---|---|---|
| **No identity-preserving open-source** (qwen-image-edit-2511, FLUX.2, LongCat) | P2 | 404 on endpoints. Deploy when stable. `forge_ephemeral` lifecycle. |
| **No `arifos_visual_memory`** (Qdrant vector persistence for generated images) | P2 | Mirror audio memory. Cosmetic/identity embeddings, 6-dim vector. |
| **Komda lint not at `--gate`** (warn-only) | P3 | F13 ratification required for promotion. |
| **No visual-AI fork differentiation** (DiT vs A2I vs SSM) | P3 | Architecture research. Hermes still calls external APIs. |
| **Real-photo edit ensemble not always run** (NB2+NB-Pro+NB+Qwen) | P3 | Default in `aaa-image-editing`. Enforce when identity-critical. |
| **OCR cascade not yet federated to GEOX** (only AAA + Hermes) | P3 | Cross-organ bridge needed. |
| **`forge_visual_qa` only on SEAL-grade** (could extend to all charts/maps) | P3 | Selective application. Don't over-process low-stakes visuals. |
| **Visual section missing in i-ARIF identity card** | P3 | Mirror audio section. Voice preferences for visual = same scope. |
| **Verifier suite not yet wired** into `aaa-image-editing` post-edit check | P2 | Quick win. Add depth/shadow/count verifiers after NB family edit. |

## 11. The Zen Path (How to Zen the Visual Stack)

Per the Zen doctrine (`/root/AAA/instructions/zen.md`):

### Machine peace: no visual mutation without rollback

- **Snapshot FIRST** before any visual artifact mutation (rsync, deploy, image-to-image cascade)
- **Dry-run** before destructive visual sync (`.env`, `/tmp/`, `node_modules/`, generated asset dirs)
- **Canary**: 1 visual asset → health check → 60s → next

### Agent peace: no visual write without schema

- Generated images: store with `{prompt, seed, model, semantic_mask, w1_hash}` envelope
- Charts: `forge_chart` output schema + eureka discoveries logged
- Visual seals: composite_hash only via `arif_judge` → `arif_seal` chain
- VAULT999 writes: `git_to_vault.py` auto-ingests commit heads. Idempotent.

### Human peace: no ping without consequence

- Quiet hours 23:00–07:00 MYT (no visual SEALS except VOID/breach/data-loss)
- Budget: ≤3 immediate visual SEALS/day; overflow → evening-zen-brief
- Goal: most days end with `Required sovereign decision: NONE`
- Visual SEAL requests via Telegram → tell Hermes, do not SSH

### Forge → Vault ingestion (anti-forget)

- Every visual SEAls in forge_work/ → auto-sealed into VAULT999 as VISUAL_RECEIPT
- Idempotent: re-running on same composite_hash produces no duplicate

### Zen practice for visual work (VSS-aligned)

The zen path now mirrors the VSS loop: **Proposal → Verify → Repair → Seal**. Each phase has its own gate.

1. **Before any image gen/edit (Proposal phase):**
   - Run `forge_entropy_sweep` on target dir. If ΔS > 0, find the source.
   - If prompt is ambiguous → Causal Scene Graph parser (when built) or manual disambiguation. Don't generate without resolving core ambiguities.
   - Pick smallest capable model: text-only generation → MiniMax; identity edit → NB family; document → OCR cascade; chart → `forge_chart`.

2. **Before SEAL-grade visual (Verify phase):**
   - Run `forge_visual_qa` W³ tri-witness. Don't seal without composite_hash.
   - Run lightweight verifiers (depth/shadow/count/containment/occlusion) when available.
   - Check Domain Constraint Registry (F1-F13 floors + visual-domain extensions).

3. **Before territory color claim:**
   - Run `lint-komda-colors.sh --gate` (or --warn-only at deploy).

4. **Before real-photo edit (Verify + Repair phase):**
   - Verify semantic-mask, 6 Iron Rules, identity preservation clause.
   - On verifier FAIL → consult `forge_scar(mode="consult")` before resampling. Prevent repeating known failures.
   - Bounded retries (max 3 per region). Escalate to W₃ sovereign if loop diverges.

5. **Before visual memory write:**
   - Check Qdrant collection exists. If not, `forge_ephemeral`.

6. **Before any new visual capability:**
   - Q1-Q7 from agentic-architecture doctrine. If ephemeral candidate, `forge_ephemeral` first.
   - Promotion only after 5+ missions, success_rate ≥ 0.90, zero sandbox violations, multi-model consensus, F13 ratification.

7. **After every visual work cycle:**
   - Composite seal or HOLD. No silent failures.
   - `git_to_vault.py` auto-ingests visual SEAls to VAULT999 as VISUAL_RECEIPT.
   - Audit `AUDIT-skill-atlas` for new visual skill overlap. Metabolize duplicates.

### ΔS ≤ 0 on visual stack

**Current entropy hotspots (audit):**
- 13+ visual skills across 3 directories → potential fragmentation
- Multiple competing image-gen providers (MiniMax, NB, Qwen) → consolidation needed
- PDF/image/document tools overlap (forge_document_ingest + AAA-OCR + FORGE-document-intelligence)

**Proposed metabolism:**
- Consolidate `aaa-image-editing` + `creative/image-text-editing` + `image-analyzer-vision` into single visual-editing skill family
- Keep `minimax-image-gen` (T2I) + `token-plan-image` (Qwen T2I/I2I) as distinct — they serve different providers
- Merge OCR cascade skills under one `AAA-OCR-optical-compression` owner
- Keep `forge_visual_qa-w3` separate — it's governance, not generation

**Ephemeral tools (per Meta-Mesa doctrine, /root/AAA/instructions/agentic-architecture.md):**
- New visual capabilities → `forge_ephemeral` lifecycle FIRST
- Promote to permanent only after 5+ missions, success_rate ≥ 0.90, zero sandbox violations, multi-model consensus, F13 ratification
- Until then: ephemeral. Lives. Works. Dissolves.

## 12. Link Map — Knowledge Graph Connections

| Visual Element | Connects To | Via |
|---|---|---|
| `aaa-image-editing` | `AGI-multimodal-bridge` | Both register visual modality |
| `aaa-image-editing` | `AGI-audio-quantum-cognition` | Parallel membrane doctrine |
| `aaa-image-editing` | `delta-omega-psi-multimodal-cognition` | Δ·Ω·Ψ rules apply to image |
| `AAA-OCR-optical-compression` | `forge-document-intelligence` | Same VLM cascade substrate |
| `AAA-OCR-optical-compression` | `hermes-gateway-image-routing` | PRMT can use OCR cascade |
| `minimax-image-gen` | `mcp__minimax-media__text_to_image` | Direct MCP call |
| `token-plan-image` | `token-plan-video` | Same Aliyun endpoint family |
| `token-plan-image` | `mcp__minimax-media__text_to_image` | Fallback for Throttling.AllocationQuota |
| `hermes-gateway-image-routing` | `hermes-init` / `hermes-forge` | Gateway routing layer |
| `hermes-gateway-image-routing` | `forge_browser_*` | Both touch image bytes |
| `FORGE-visual-qa-w3` | `forge_visual_qa` MCP | Direct skill-to-MCP |
| `FORGE-visual-qa-w3` | `forge_visual_seal` MCP | Composite seal |
| `FORGE-visual-qa-w3` | `forge_scar` MCP | Scar consultation before fix |
| `FORGE-visual-qa-w3` | `forge_entropy_sweep` | ΔS ≤ 0 enforcement |
| `FORGE-komda-color-law` | `FORGE-agentic-web-builder` | Both audit web surfaces |
| `FORGE-komda-color-law` | `lint-komda-colors.sh` | Direct script call |
| `geological-artifact-rigor` | `geox_prospect`, `geox_map` | GEOX 3D/2D outputs |
| `forge_chart` | `forge_entropy_sweep` | Chart eureka discovery |
| `mcp__aforge__forge_browser_screenshot` | `FORGE-visual-qa-w3` | W₁ evidence source |
| `mcp__geox__geox_map` | `geox-production-cockpit` | Map rendering |
| `mcp__geox__geox_model` | `geological-artifact-rigor` | Cross-section standards |
| All visual skills | `arif_init` → `arif_judge` → `arif_seal` | Constitutional pipeline |

## 13. Identity: i-ARIF Visual Preferences

**Arif's observed visual preferences (session-confirmed):**

| Preference | Evidence | Date |
|---|---|---|
| **Identity preservation on real photos** ("Hang jangan ubah muka manusia") | F13 directive | 2026-08-12 |
| **T2I for diagrams/illustrations, not real-photo fake** | inferred from session patterns | 2026-08 |
| **Komda color compliance** (federation territory respect) | F13 §04 ratification | 2026-08-01 |
| **No over-smoothing** (preserve skin texture) | session feedback | 2026-08-12 |
| **Photorealistic > illustrated** for hero assets | session feedback | 2026-08 |

**i-ARIF identity card:** `/root/AAA/agent-cards/identity/i-ARIF/identity-card.json` (audio section present, visual section TBD — gap).

## 14. The Verified Scene Synthesis Aspiration (Hybrid Proposal-Verification-Repair)

> **Ratified:** 2026-08-18 by F13 SOVEREIGN via refinement of prior over-constrained framing.
> **Convergent with:** NVIDIA Edify, Luma Genie, World Labs Marble, Google Genie 3 — the post-DiT consensus direction.
> **DITEMPA BUKAN DIBERI** ⚒️

### 14.1 The Core Correction

**Original framing (REJECTED):** Pure deterministic physics engine — "Ground-Truth Module" that simulates everything.

**Why it fails:**
1. Prompts are **underspecified** — natural language leaves most physical detail undefined
2. Compute is **finite** — full path tracing every denoising step is impossible
3. Many visual decisions are **aesthetic not physical** — pure determinism kills creativity
4. "Deterministic Absolute Truth" is **unrealistic** when input is ambiguous

**Refined framing (RATIFIED):** Hybrid Proposal-Verification-Repair Architecture
> *Probabilistic generators propose structured worlds. Domain-specific verifiers and differentiable renderers test, constrain, and repair them.*

The federation moves from "deterministic simulator" to **executable, hybrid AI framework** — the generator does what it does best (rich textures, creative proposals), and external geometric/physical verifiers enforce boundary conditions.

### 14.2 The Architecture

```
                       [Prompt]
                          │
                          ▼
        ┌─────────────────────────────────┐
        │ Causal Scene Graph Parser       │
        │ (Disambiguation & Entities)     │
        └────────────────┬────────────────┘
                         │
                         ▼
                ┌────────────────┐         ┌────────────────────────┐
                │ Domain Router  │────────>│ Domain Constraint       │
                │ (routes only   │         │ Registry                │
                │  relevant      │         │ (Geometry, Optics,      │
                │  verifiers)    │         │  Fluid, Kinematics)     │
                └────────┬───────┘         └────────────┬───────────┘
                         │ <──(Constraint Guidance)──────┘
                         ▼
        ┌─────────────────────────────────┐
        │ Probabilistic World Latent       │
        │ Generator                       │
        │ (3D/4D Bounding Boxes, SDFs,     │
        │  Materials, Uncertainty Maps)    │
        └────────────────┬────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │ Staged Differentiable Rendering  │
        │ (Coarse → Fine)                  │
        └────────────────┬────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │ Independent Specialist Verifiers │ <── Domain Registry
        │ (Geometry, Optics, Biomechanics, │
        │  Linguistics, Fluid Mechanics)   │
        └────────────────┬────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
        ┌──────────┐         ┌──────────────────┐
        │   PASS   │         │      FAIL        │
        │ pixels + │         │ (violations >    │
        │ provenance│        │  threshold ε)    │
        └──────────┘         └────────┬─────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │ Targeted Local       │
                          │ Repair / Resampling  │
                          │ Loop (only failing   │
                          │ sub-region)          │
                          └──────────┬───────────┘
                                     │
                                     └────> back to Staged Rendering
```

### 14.3 The Four Architectural Shifts (Precision Fixes)

**Shift 1 — Language Disambiguation & Domain Routing**
- Causal Scene Graph extracts structural tuples: Entities, Spatial Relations (`inside`, `supported_by`), Optical Properties (`translucent`, `point_light_source`), Causal Dependencies.
- Domain Router maps scene graph to specific constraint engines:
  - Static portrait → Anatomy + Differentiable Optics verifiers only
  - Breaking wave → Fluid Mechanics (Navier-Stokes) verifiers only
  - Architecture → Geometric Perspective + Optical verifiers only
- Unrelated modules remain dormant. **No global solver waste.**

**Shift 2 — Hybrid 3D Scene Representation (not pure neural implicit)**
- Structural Skeleton: bounding boxes, object identities, contact manifolds, explicit depth ordering
- Surface Geometry & Appearance: implicit SDFs OR lightweight meshes coupled with material reflectance fields (BSDF parameters)
- **Uncertainty Maps:** explicit voxels/regions tagged with high uncertainty where the prompt leaves geometry or occluded surfaces undefined — gives the probabilistic generator room to sample valid variants

**Shift 3 — Staged Differentiable Rendering (coarse → fine)**
- Path tracing during every denoising step = impossible compute bottleneck
- Render by spatial abstraction level: coarse geometry pass → medium material pass → fine detail pass
- Differentiable only at the levels needed for the verifier feedback loop

**Shift 4 — Independent Verifier & Local Repair Loop**
- Soft physics loss functions drift into local minima → soft loss is wrong tool
- Hard assertions by external verifiers = deterministic boundaries

| Verifier | Validation Target | Failure Action |
|---|---|---|
| **Linguistic & Causal** | entity containment, count, occlusion relations | Mask object bbox → resample latent vector |
| **Geometric & Perspective** | multi-view camera matrices, vanishing points, horizon alignment | Adjust camera projection in rasterizer |
| **Biomechanical** | joint limits, skeletal proportions, volumetric mass | Apply pose deformation to surface mesh |
| **Optical & Photometric** | light trajectory, shadow alignment, IOR refraction | Re-project shadow rays via differentiable path tracer |

If verifier flags violation above threshold ε → **Localized Inpainting/Resampling Loop** on only the failing sub-region, preserving valid surrounding generation.

### 14.4 Epistemic Comparison

| Dimension | Standard Latent Diffusion (DiT/U-Net) | Pure Deterministic Engine (REJECTED) | Verified Scene Synthesis (RATIFIED) |
|---|---|---|---|
| **Core Nature** | Statistical pattern distribution matcher | Over-constrained physical simulator | Probabilistic Proposal Engine + Deterministic Verifier |
| **Prompt Handling** | Soft text embeddings (CLIP/T5) | Strict physical specification | Causal Scene Graph with Disambiguation Engine |
| **Physics Application** | Implicit visual co-occurrence | Constant global solver evaluation | Targeted Domain-Routed Verification |
| **Failure Mode** | Visual hallucination + physical nonsense | Cannot handle underspecified prompts | Targeted Local Repair on Constraint Violations |
| **Output Guarantee** | Visual plausibility only | Unrealistic "Deterministic Absolute Truth" | Constraint-Consistent Rendering + Provenance Confidence |

### 14.5 Federation Alignment with Verified Scene Synthesis

**Key insight:** The federation already has the **governance primitives** for the verifier layer. We are missing the parser and the world latent.

| VSS Module | Federation Substrate | Status |
|---|---|---|
| **Domain Constraint Registry** | arifOS F1-F13 floors (constitutional assertions) + W³ tri-witness | ✅ Exists (governance layer) |
| **Independent Specialist Verifiers** | `forge-vss-verifier-suite` + W³ | Ingests VSS-1 ledger. Pixel VLM still HOLD. |
| **Local Repair Loop** | `forge_scar` (consult before fix) + iterate loop in W³ | ✅ Exists (governance layer) |
| **Composite Seal + Provenance** | `forge_visual_seal` → VAULT999 | ✅ Exists |
| **Causal Scene Graph Parser** | `forge-vss-parser` (schema + contract, no live substrate) | Schema-locked 2026-08-19 |
| **Domain Router** | `arif_route` (intent→organ dispatch) | ✅ Exists (general router, needs visual-specialization) |
| **Probabilistic World Latent Generator** | MiniMax `image-01`, NB family, Qwen DiT | ✅ Exists (external API) |
| **Staged Differentiable Rendering** | (not implemented) | Gap — long-term |
| **Hybrid 3D Scene Representation** | GEOX `geox_model` (GemPy 3D) | Partial — subsurface only |
| **Uncertainty Maps** | (not implemented) | Gap — research needed |
| **Physics Constraint Engines** (per domain) | GEOX `geox_geomechanics` (rock), `geox_petrophysics` (porosity/perm) | Partial — geoscience only |
| **Biomechanical Kinematics** | (not implemented) | Gap — research needed |
| **Optical/Photometric Verifier** | (not implemented) | Gap — long-term |

**Honest reframe:** The federation's current visual stack is **probabilistic proposal engine + constitutional verifier + local repair loop + composite seal**. We have the GOVERNANCE half of VSS. The PROPOSAL half (causal scene graph + world latent + staged rendering) is the build.

This is a far better starting position than I claimed in v1 — the federation is not "statistical correlation engine only." It is **half-built Verified Scene Synthesis.**

### 14.6 Practical Execution Path (Federation-Mapped)

Per Arif's ratified 4-step build sequence:

**Step 1 — Parser Layer (L2 skill, medium-term)**
Build the **Causal Scene Graph Parser** as a new L2 skill:
- Input: raw prompt (text + optional reference image)
- Output: typed JSON with Entities, Spatial Relations, Optical Properties, Causal Dependencies
- Tools: `mcp__arifos__arif_route` (intent classification) + VLM extraction (qwen3-omni-flash)
- F2/F4 gates: every entity tagged with epistemic label, every relation schema-validated
- Federation integration: feeds `aaa-image-editing` semantic-mask builder + `geox_*` scene grounding

**Step 2 — Verifier Suite (short-term, low cost)**
Implement **lightweight post-generation verifiers** as independent check gates. This is where the federation has prior art:
- **Depth consistency check** — run shadow direction analysis via Qwen-VL
- **Shadow direction consistency** — single light source per scene (unless explicit multiple)
- **Spatial containment** — entities inside containers stay inside (use segmentation + bbox)
- **Count assertion** — "five birds" → verify 5 segmented regions
- **Occclusion ordering** — foreground objects correctly occlude background
- Each verifier returns PASS/HOLD/FAIL + deviation list
- These can wrap existing `vision_analyze` calls — no GPU needed

**Step 3 — Local Repair Mechanism (medium-term)**
Wire **bounding-box masked resampling** driven by verifier failure flags:
- Verifier FAIL on sub-region → mask that region's bbox → call generator again with same prompt + bbox mask
- Limit retries (max 3 per region) — escalate to human (W₃ sovereign) if loop diverges
- Pattern matches `forge_visual_qa-w3` Stage 5 scar consultation + iterate
- Use `forge_scar(mode="consult")` BEFORE resampling — prevent repeating known failures

**Step 4 — World Latent Integration (long-term, GPU required)**
Bridge the **2D latent space with 3D explicit bounding proxies** + staged differentiable rendering:
- GEOX `geox_model` (GemPy 3D) as world latent substrate for geological scenes
- For non-geo scenes: deferred until GPU available or via Runpod serverless (Wan Video, HunyuanVideo)
- Staged rendering: coarse bbox layout → medium material pass → fine detail pass
- Differentiable at coarse level only — fine detail is generator's job

### 14.7 What Changes for Federation Visual Work (Immediate)

**No new tools needed for short-term gains.** Apply VSS pattern to existing stack:

| Current Practice | VSS Pattern | Implementation |
|---|---|---|
| Single-shot MiniMax generation | Proposal + multi-verifier + targeted repair | `forge_visual_qa-w3` after each generation |
| aaa-image-editing single-pass | Proposal (NB family) + 6 Iron Rules as verifiers + repair on failure | Already in skill; tighten via Stage 5 scar loop |
| `forge_chart` output | Chart eureka discovery IS verifier signal | Already exists — surface deviations explicitly |
| Hermes PRMT path | PRMT is the verifier on input (image → [IMAGE TRANSCRIPT] constraints) | Already exists |
| Vision-SEAL grade charts | W³ tri-witness IS multi-verifier pattern | Already exists — `forge_visual_qa-w3` |

**The federation has been doing VSS in governance form for months.** The proposal is to extend the same pattern to content generation — making the GEN half as governed as the SEAL half.

### 14.8 The Asymptote

Verified Scene Synthesis is not a destination — it's an asymptote. Each iteration:
- Parser gets better at disambiguation
- Verifier suite expands to cover more domains
- Repair loop becomes more targeted
- World latent bridges more domains to 3D substrate

The federation's current state: **half the VSS loop built (governance), half aspirational (parser + world latent + staged rendering).** Continue along the asymptote.

---

### 14.9 VSS-1 Honest Status (F13 Correction, 2026-08-19)

> **Correction note:** Prior synthesis (this map, v1) claimed VSS-1 "schema + engine contract is ROBUST" and "falsification gate status: Schema + engine contract is ROBUST." F13 SOVEREIGN (2026-08-19) corrected: this was **overclaim**. Schema conformance ≠ semantic anti-overclaim proven.

**VSS-1 CURRENT STATE — HONEST:**

| Layer | Status | Evidence |
|---|---|---|
| VSS-1 schema (`vss_assertion_ledger.schema.json`) | **PASS** | Strict Draft-07 schema, `additionalProperties: false`, closed enums, regex patterns |
| VSS-1 fixture conformance | **PASS** | All 50 hand-crafted expected ledgers validate against schema (35 boundary + 15 complex) |
| VSS-1 parser engine self-test | **PASS** | Built-in `mock_valid_payload` validates as VALID_SCHEMA |
| VSS-1 semantic anti-overclaim (NEAR stays NEAR) | **NOT PROVEN** | Only stub-based; no real LLM substrate tested |
| VSS-1 relation→verifier mapping correctness | **NOT PROVEN** | Mapping rules in system prompt; never executed by LLM |
| VSS-1 entity/assertion reference semantics | **NOT PROVEN** | Schema validates structure; semantic validity unverified |
| VSS-1 real substrate (qwen3-omni-flash) | **BLOCKED** | MuleRouter -0.7476 credits, OpenRouter 0 credits, Gemini 429 depleted |
| VSS-1 LLM produces valid ledgers consistently | **NOT PROVEN** | No substrate call has succeeded |
| VSS-1 extracts real scene correctly | **NOT PROVEN** | Same blocker |
| VSS-1 0.98 semantic + ambiguity result (target) | **NOT ACHIEVED** | Acceptance threshold not reached |
| VSS-2 implementation | **HOLD** | Blocked on VSS-1 real substrate validation |
| VSS-2 read-only contract compatibility audit | **ALLOWED** | Interface inspection only — no execution |

**What the 35 boundary cases proved:**
- Schema accepts the migrated expected ledgers
- Parser passes a valid stub payload through the schema gate
- Schema migration did not break the declared fixture set (categories A/B/D only)

**What the 35 boundary cases did NOT prove (correction note):**
- 35 = 10 (A_simple_grounding) + 15 (B_ambiguity_underspecification) + 10 (D_adversarial_non_visual). The C_complex_multi_entity_lighting category (15 cases) was **absent from the report** despite being part of the 50-case fixture set. So "35 boundary cases pass" is valid only for those listed categories — not a full four-category suite.
- Category C (compound scenes with multiple entities + lighting + containers + optical relations) has not been validated through the parser engine self-test.

**Substrate blockage detail:**
- MuleRouter (PRIMARY per F9): `-0.7476 credits` — insufficient balance (HTTP 402)
- OpenRouter (FALLBACK): `0 credits` — insufficient balance (HTTP 402)
- Gemini (Tertiary fallback): HTTP 429 — prepayment credits depleted
- **DO NOT** top up credits automatically
- **DO NOT** retry Gemini blindly
- **DO NOT** bind unverified parser to visual pipeline

**Honest label:**
> "VSS-1 schema and fixture-conformance gate passed; real-substrate and semantic anti-overclaim validation remain pending."

**Path forward (strict):**
1. ✅ Document this honest state (this section) — DONE 2026-08-19
2. ⏸ Read-only contract compatibility audit on VSS-2 (interface inspection only)
3. ❌ DO NOT proceed to VSS-2 execution or implementation
4. ❌ DO NOT claim parser is production-ready until real substrate achieves ≥0.98 semantic + ambiguity result

---

### 14.10 VSS-2 Read-Only Contract Compatibility Audit (Interface Inspection Only)

> Per F13 SOVEREIGN directive (2026-08-19): this audit is **interface inspection, not VSS-2 execution**. No visual verifier runs, no new LLM call justified. Audit performed via source code inspection of `/root/AAA/skills/forge-vss-verifier-suite/`.

**Files audited (read-only):**
- `forge_vss_verifier_suite.py` (execution script)
- `vss_ledger_adapter.py` (VSS-1 → VSS-2 projection)
- `SKILL.md` (skill spec)

---

**Audit Question 1: Can VSS-2 load the VSS-1 schema?**

**RESULT: YES (with caveat).** `vss_ledger_adapter.py` lines 16-20 import `VSSParserEngine` from `/root/AAA/skills/forge-vss-parser/` and call `engine.validate(ledger)` (line 49). This validates against `vss_assertion_ledger.schema.json` via jsonschema. Schema validation failures return `{"ok": False, "error_code": "E_SCHEMA_INVALID", "validation_message": <jsonschema msg>}`.

**Caveat:** Loading is via `import` path hardcoded to `/root/AAA/skills/forge-vss-parser/`. If VSS-1 schema path moves, the import breaks silently (will fall through to E_CONTRACT_INVALID).

---

**Audit Question 2: Can VSS-2 iterate through assertions?**

**RESULT: YES.** `vss_ledger_adapter.py` lines 70-101 iterate `for assertion in ledger.get("assertions", [])`. Each assertion is routed to a verifier suite via `VERIFIER_DISPATCH` dict (lines 23-29):
- `containment_v1` → `count_containment` suite
- `count_v1` → `count_containment` suite
- `perspective_v1` → `perspective_depth` suite
- `shadow_v1` → `shadow_light` suite
- `none` → unrouted (no pixel check)

Subject/target entities are looked up via `_entity_index()` (lines 32-33). Subject/target labels are extracted for the work order. Containments are filtered to `inside`/`on`/`supported_by` relations.

---

**Audit Question 3: Does VSS-2 ignore `UNVERIFIED` status (not treat as PASSED)?**

**RESULT: NO — CONTRACT GAP.**

The adapter does NOT check `assertion.get("status")`. It iterates ALL assertions in the ledger regardless of whether status is `UNVERIFIED`, `PASSED`, or `FAILED`. There is no filter for `status != "UNVERIFIED"` or `status == "UNVERIFIED"` before projection to the work order.

**Implication:** VSS-2 work order will include assertions that the VSS-1 parser already marked as PASSED or FAILED. If those are then re-validated by VSS-2 pixel verifiers, the result is incoherent — a PASSED assertion may produce a new verifier report, contradicting the prior verdict.

**Required for production (NOT implemented in this audit):** Filter assertions where `status == "UNVERIFIED"` before projection. PASSED and FAILED assertions should not be re-verified by VSS-2 pixel check.

---

**Audit Question 4: Does VSS-2 fail-closed on malformed/dangling references?**

**RESULT: PARTIAL — CONTRACT GAP on dangling references.**

**Fail-closed on:**
- Non-dict input → `E_LEDGER_NOT_OBJECT` (line 42-46)
- Schema violations → `E_SCHEMA_INVALID` via `engine.validate()` (line 49-52)
- Contract violations → `E_CONTRACT_INVALID` (line 51)

**NOT fail-closed on:**
- Dangling subject reference: `subject = entities.get(assertion["subject"], {})` (line 73). Returns empty dict for missing subject, then `subject_label = subject.get("label", assertion["subject"])` falls back to raw ID. **No error raised.**
- Dangling target reference: same pattern, line 74-80. Falls back silently to raw ID.

**Implication:** A ledger with `assertion.subject = "ghost_id"` (referencing a non-existent entity) will be silently processed with `subject_label = "ghost_id"`, propagated to the work order. The VSS-2 pixel verifier will then fail with a confusing "subject not found in image" error rather than a clear "ledger schema invalid: dangling reference."

**Required for production (NOT implemented in this audit):** Explicit check `if not subject: return {ok: False, error_code: "E_DANGLING_REFERENCE", ...}` before constructing the work_order item.

---

**Audit Question 5: Does VSS-2 preserve distinction between HARD_GEOMETRIC / HARD_COUNT / OPTICAL_LIGHTING / SOFT_STYLE?**

**RESULT: PARTIAL — class is preserved as data but not used for routing.**

**Preserved:** `item["class"] = assertion["class"]` (line 81) puts the class into each work_order item. Class field travels with the item through to verifier suites.

**Used:** Only `HARD_COUNT` triggers count aggregation (line 98-100). Other classes are data-only — they don't affect which verifier suite handles the assertion.

**Implication:** VSS-2 routing is by **verifier** (containment_v1/count_v1/perspective_v1/shadow_v1), NOT by **class**. The class field is metadata for downstream reasoning but not enforced in the work order construction.

**Required for production (NOT implemented in this audit):** Decide whether class should drive routing (e.g., `OPTICAL_LIGHTING` always goes to `shadow_light`), or remain pure metadata. Currently class is metadata-only.

---

**Audit Summary (interface inspection only):**

| Question | Result | Contract Gap? |
|---|---|---|
| 1. Schema load | YES | No (caveat: hardcoded import path) |
| 2. Iterate assertions | YES | No |
| 3. Ignore UNVERIFIED | **NO** | **YES — critical gap** |
| 4. Fail-closed on dangling refs | PARTIAL | **YES — silent fallback** |
| 5. Preserve HARD_GEOMETRIC/HARD_COUNT/OPTICAL_LIGHTING/SOFT_STYLE | PARTIAL | YES — class preserved as data, not used for routing |

**Two contract gaps identified (NOT fixed in this audit):**
1. **UNVERIFIED status not filtered** — VSS-2 will re-verify already-passed assertions. Incoherent ledger state.
2. **Dangling references not fail-closed** — Silently produces work order items with raw IDs as labels. Confusing downstream errors.

**Status:** Audit complete (read-only). No code modified. No execution run. No LLM call.

**Next action:** HOLD. Awaiting F13 directive on whether to fix the two contract gaps, or move to VSS-1 real-substrate validation, or both.

---

*Forged 2026-08-18 by 333-AGI / Hermes-prime under F13 SOVEREIGN directive "map all visual intelligence in AAA state."*
*Refined 2026-08-18 by F13 SOVEREIGN ratification of Verified Scene Synthesis doctrine (Hybrid Proposal-Verification-Repair).*
*Mirror of `/root/AAA/knowledge-graph/audio-intelligence-map.md`.*
*DITEMPA BUKAN DIBERI — Probabilistic proposals + deterministic verifiers + local repair = executable hybrid AI framework. Visual output carries truth claims. Govern them accordingly.* ⚒️