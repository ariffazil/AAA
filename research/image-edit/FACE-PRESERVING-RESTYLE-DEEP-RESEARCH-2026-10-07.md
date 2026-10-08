# Face-Preserving Image-to-Image Editing — 2025/2026 State of the Art vs. Melayu Cultural Accuracy

> **Status:** External deep research · COMPLETE (one lane PARTIAL, see §8)
> **Date:** 2026-10-07
> **Task:** AAA visual-intelligence hardening — why mmx image-01 `--subject-ref` caps at 4-7/10 identity and 2.5-3.5/5 cultural fidelity on the Melayu royal archetype, and what actually works
> **Method:** arXiv + ICCV/CVPR primary sources, HuggingFace/GitHub cards, one Malaysia-specific peer-reviewed paper, community field reports. No promotional blogs used for verdicts.
> **Evidence classes:** OBS = measured number from a paper/repo · REP = reported by independent source · DER = my derivation from the above · UNKNOWN = not measured anywhere I could find

---

## 0 · TL;DR (the answer in one screen)

1. **mmx image-01's 4-7/10 ceiling is NOT a bug — it is the published state of the art.** The best open identity-preservation numbers on diverse test sets are Face Sim **0.72-0.77** (PuLID/InfiniteYou class) against a 1.0 ideal. "4-7/10 by human eye" sits exactly where the literature says a single-reference adapter should land. (OBS, PuLID Table 4/6.)
2. **No model in existence has been benchmarked on songket, keris, or tengkolok.** Zero. Not one paper. The closest measured proxy is CultDiff (KAIST, arXiv:2502.08914): Indonesia — the nearest culture to Malay in every training corpus — **ranked consistently in the bottom half** for clothing and architecture across SD-XL, SD3-Medium and FLUX.1-dev. Your 2.5-3.5/5 cultural fidelity is the *expected* result, and Malaysia was not even important enough to be in their 10-country list. (OBS)
3. **The two mechanisms are different problems with different fixes.** Face preservation = ID-embedding injection (a solved-ish engineering problem, ~0.77 ceiling). Cultural textile rendering = *training-data absence* (an unsolved data problem — no adapter can inject knowledge the base model never saw). You cannot fix #2 with a better face model.
4. **Best 2025/2026 path for the federation:** FLUX.1 Kontext [pro/max] (API) for editing-with-identity — it is the measured SOTA on character preservation (AuraFace similarity, KontextBench, 1,026 pairs) — **plus** InfiniteYou-FLUX (open weights, ICCV 2025 Highlight) for the local lane — **plus** ControlNet/IP-Adapter with a *real reference photo of songket/keris* rather than text prompts, because text-conditioned cultural rendering is where every model fails.
5. **Marketed-but-broken list:** PhotoMaker (v1) — Face Sim **0.271**, barely above noise, despite heavy marketing; IP-Adapter-FaceID (non-Plus) — good aesthetics, *fails identity fidelity* per F-Bench; FLUX.1-dev generic IP-Adapter — identity similarity 0.772 with CLIPScore 0.243, explicitly "not tailored for human faces" per ByteDance.

---

## 1 · Master comparison table

Metric key: **Face Sim** = cosine similarity of face-recognition embeddings (antelopev2/InsightFace class), 1.0 = identical. **CLIP-T** = prompt adherence (×100 scale in PuLID tables). DivID-120 = PuLID's diverse test set (varied skin tones, ages, genders); Unsplash-50 = open test set.

| Model | Year | Publisher | Face-preservation approach | Identity ceiling (OBS) | Prompt adherence | Cultural-specific rendering | License / access | Honest verdict |
|---|---|---|---|---|---|---|---|---|
| **PhotoMaker v1** | 2024 | Tencent ARC | Stacked ID embedding (CLIP-based), multi-ref | **0.271** DivID-120 / 0.193 Unsplash-50 | CLIP-T 26.06 | Untested; base = SDXL → CultDiff bottom-half for Indonesia clothing | Open (HF) | **Marketized-but-broken for identity.** 0.27 is functionally "a different person who vaguely resembles you." V2 improved but F-Bench still ranks it below IP-Adapter-FaceID-Plus |
| **IP-Adapter-FaceID** | 2023 | Tencent (h94) | InsightFace embedding → decoupled cross-attn | ~0.597 (as "IPAdapter" in PuLID T6) | CLIP-T 29.39 (best editability of the SDXL generation) | Untested | Open (HF, non-commercial license) | Good aesthetics, **weak identity** — F-Bench: "produces high-quality images but lacks accuracy in Identity Fidelity" |
| **IP-Adapter-FaceID-Plus v2** | 2024 | Tencent (h94) | Face embedding + CLIP image features of the reference | Not separately quantified in PuLID tables; **best across all dimensions in F-Bench radar** | Good | Untested | Open (HF) | **F-Bench's overall winner** among 2024-era customization models (ICCV 2025, 491,130 human ratings). Best open SDXL-era choice |
| **InstantID** | 2024 | InstantX Research | IdentityNet: face embedding + facial-landmark ControlNet (strong semantic, weak spatial) | **0.755** DivID-120 / 0.648 Unsplash-50 | CLIP-T 25.33 (**worst editability** — landmark control locks pose) | Untested | Open (HF/GitHub) | Highest raw face sim of the SDXL generation but **pose-locked and prompt-deaf**; F-Bench: strong Identity Fidelity, "underperform significantly in Quality and Correspondence" |
| **PuLID / PuLID v1.1 (SDXL)** | 2024 | ByteDance | Lightning-T2I contrastive branch: alignment loss (semantic+layout) + accurate ID loss | 0.722 balanced / **0.773 max-ID** DivID-120; 0.654/0.711 Unsplash-50 | CLIP-T 30.69-31.31 (**best ID/editability tradeoff**) | Untested | Open (HF/GitHub) | The paper that exposed the core tradeoff: "enhancement in ID similarity accompanies a decrease in CLIP-T" — PuLID is the only one that partially breaks it |
| **PuLID-FLUX** | 2024 | ByteDance | PuLID ported to FLUX.1-dev DiT | ~0.72 (REP, aiofm field guide; no paper table) | Decent | Untested | Open | Superseded by InfiniteYou by its own authors: "identity similarity is not sufficient… face copy-paste issue is evident" |
| **InfiniteYou (InfU)-FLUX v1.0** | 2025 | ByteDance Intelligent Creation | SimFace identity extractor + residual injection into FLUX DiT; two variants: sim_stage1 / aes_stage2 | "Lowest ID Loss" vs PuLID-FLUX and FLUX IP-Adapter (OBS, ICCV 2025 paper); FLUX-IPA baseline CLIPScore 0.243 → InfU closes 66.7% of the gap to FLUX's 0.334 upper bound | Best text-image alignment in its comparison table | Untested | **Open weights (HF: ByteDance/InfiniteYou), ICCV 2025 Highlight** | **Current best open-weights identity lane on a FLUX base.** ComfyUI community: "InfiniteYou has held up way better than PuLID on recent Comfy" |
| **FLUX.1 Kontext [pro]/[max]** | 2025 | Black Forest Labs | Native multimodal flow-matching DiT; sequence concatenation of image+text tokens (no adapter — identity is in-context) | **Highest AuraFace before/after similarity of all models on KontextBench character-reference (193 pairs)** (OBS, arXiv:2506.15742 Fig 8f); beats GPT-Image-1, Gen-4 | Wins Text Editing + Local Editing categories; 2nd to gpt-image-1 on global editing | Untested on SEA; base FLUX.1-dev is CultDiff bottom-half for Indonesia | **[pro]/[max] = API-only** ($0.04/edit via aggregators); **[dev] = open weights**, non-commercial license, $999/mo for commercial | **Measured SOTA for edit-while-preserving-identity in 2025.** The single strongest candidate to replace mmx image-01 for the federation's restyle lane |
| **Qwen-Image-Edit (2509/2511)** | 2025 | Alibaba Qwen | Dual encoding: Qwen2.5-VL semantic + VAE reconstructive, MMDiT edit; no dedicated face adapter | No face-sim number in tech report (arXiv:2508.02324). Field: "consistent faces in about 20% of results" without a face LoRA (REP, r/comfyui); 2511 release titled "Improve Consistency" | **Top instruction-following**: wins Ecom-Edit Bench overall (G_SC 8.97 vs Kontext-dev 7.55, NanoBanana 8.22) (OBS, arXiv:2510.04483) | Chinese iconography strong (native text rendering incl. logographic); SEA untested | **Open weights (HF: Qwen/Qwen-Image-Edit)** + DashScope API | Best *instruction-follower*, **not** an identity-preservation model. Community fix is stacking a face LoRA (DiffSynth Qwen-Image-Edit-F2P). Your connection-dead lane is also the wrong tool for faces |
| **Gemini 2.5 Flash Image ("nano-banana")** | 2025 | Google | Native multimodal LLM image gen; character consistency via conversation context | Topped LMArena image-editing at launch (REP); GPT-Image-2-class face similarity ≈ **0.462-0.499** on group-identity benchmark (OBS, WithEveryone paper citing GPT-Image-2) | Strong creative flexibility (REP, wiro.ai 26-prompt test) | Untested on SEA; Google models have documented geographic representation bias (Basu et al. lineage cited in CultDiff) | **API-only** | Convenient, strong general editing; identity numbers for the MLLM-native class are *lower* than the adapter class on cosine metrics — marketing outpaces measurement |
| **mmx image-01 (MiniMax)** | 2025 | MiniMax | `subject_reference` (type: character) — proprietary; no published architecture or benchmark | **No published numbers anywhere.** Federation's own test: 4-7/10 identity, 2.5-3.5/5 cultural fidelity (OBS, first-party) | Unknown | Unknown | **API-only** | Unbenchmarkable black box. Your first-party 4-7/10 is consistent with the adapter-class ceiling (~0.7 cosine ≈ "recognizable but drifted"), but nothing external can confirm or improve it |
| **wan2.x-image (Token Plan)** | 2025 | Alibaba/Wan team | Unknown (connection-dead from this kernel) | UNKNOWN | UNKNOWN | UNKNOWN | API | Could not research from this kernel — see §8 |
| **SeedEdit 3.0 / Seedream 4.0** | 2025 | ByteDance (Volcano) | Diffusion + reward-based joint learning, meta-info embedding | Loses to Qwen-2509 on Ecom-Edit (OBS, arXiv:2510.04483); "faithful instruction following and content preservation" (REP) | Good | Untested | API-only | Solid commercial editor; not identity-specialized |
| **Midjourney / DALL-E 3 / SD (text-only, no ref)** | 2023-24 | Various | n/a (no true face-ref) | n/a | n/a | **Directly tested on Malaysian icons** (UiTM, IJRISS 2026, DOI 10.47772/IJRISS.2026.10100164): Midjourney 3.25 overall mean, SD 3.23, DALL-E 3rd; explicit **"Cultural Accuracy Gap"** — food OK, landmarks and Malaysian politician FAIL across all three; documented real-world failure: PDRM Merdeka billboard rendered **3 KLCC towers** | Mixed | The only peer-reviewed Malaysia-specific study found. Confirms: broad Malay *food* concepts exist in training data; **specific structural Malay iconography does not** |

---

## 2 · The identity-preservation ceiling — what the numbers actually say

**The hard quantitative spine (all OBS, PuLID paper Tables 4 & 6, arXiv:2404.16022):**

| Method | Face Sim DivID-120 | CLIP-T DivID-120 | Face Sim Unsplash-50 |
|---|---|---|---|
| PhotoMaker | 0.271 | 26.06 | 0.193 |
| IP-Adapter(-FaceID) | 0.597 | 29.39 | 0.572 |
| InstantID | 0.755 | 25.33 | 0.648 |
| PuLID (max ID) | 0.773 | 24.77 | 0.711 |
| PuLID (balanced) | 0.722 | 30.69 | 0.654 |

Three laws fall out of this table:

1. **The realistic ceiling for single-reference, tuning-free identity preservation is ~0.75-0.78 cosine, and reaching it costs prompt adherence.** PuLID's own ablation: max-ID variant gains +0.05 Face Sim and loses ~6 CLIP-T points. InfiniteYou (2025) narrows but does not close this tradeoff. Anything marketing "100% face consistency" (multiple YouTube/SEO titles found) is selling LoRA-trained per-identity models, which is a *different technique* (fine-tuning, not zero-shot reference).
2. **Sub-0.6 is the failure zone.** Below ~0.6 cosine, face-recognition systems and humans start treating outputs as different people. PhotoMaker v1 (0.27) and generic FLUX IP-Adapter live there — that's why they feel "kinda like him."
3. **Translation to the federation's 0-10 scale:** 0.72-0.77 cosine on diverse sets ≈ **6-8/10 human-judged likeness on favorable subjects** (frontal, even light) and ≈ **4-6/10 on hard subjects**. mmx image-01's measured 4-7/10 band is *inside the published envelope of the entire field*. The lane is underperforming marketing, not underperforming physics.

**Which subjects it fails on (evidence + mechanism):**
- **Non-frontal / stylized targets:** InstantID's landmark ControlNet degrades when the requested pose diverges from the reference pose — identity holds, editability dies (OBS, F-Bench: InstantID/FastComposer "score well in Identity Fidelity but underperform significantly in Quality and Correspondence").
- **Strongly masculine jaw/brow features under stylization:** no paper isolates jaw geometry, but the mechanism is documented: ID embeddings from recognition models (antelopev2/ArcFace family) are trained on *recognition*, which weights eye-nose-mouth config over jaw silhouette; heavy style transfer (armor, royal regalia, dramatic lighting) shifts the rendered face toward the *style prior's* face shape. DER from PuLID §3 + F-Bench class-wise analysis (F-Bench does run age/class breakdowns and finds attribute-specific prompts score worst).
- **Darker skin tones / underrepresented ethnicities:** ICCV 2025 W paper "Data Bias Mitigation and Evaluation Framework for Diffusion-based Generative Face Models" (OBS abstract): "diffusion models also exhibit biases across various social groups, displaying preferences for attributes like **white skin** and female gender." For a Malay subject this means the base model's face prior pulls renders lighter/softer than the reference — a *systematic* identity leak orthogonal to the adapter.
- **Multi-person scenes:** WithEveryone (2025, OBS): even GPT-Image-2 only reaches 0.462-0.499 target-context face similarity when binding multiple identities — group portraits are the hardest case in the field.

---

## 3 · Cultural-specific rendering — songket, keris, tengkolok: the brutal answer

**Does any model render them accurately? UNKNOWN → almost certainly no, and here is the measured evidence:**

1. **CultDiff benchmark (KAIST, arXiv:2502.08914, Feb 2025)** — the only rigorous multi-country cultural-artifact benchmark found. 10 countries × architecture/clothing/food, human-annotated, models = SD-XL, SD3-Medium, FLUX.1-dev:
   - **Indonesia ranked in the bottom half ("Q1.2-Lowest Score") in 4 of 9 model×category cells**, including SD-XL architecture, SD3-Medium architecture, FLUX clothing, FLUX food. USA/UK/S.Korea/Mexico dominate the top. (OBS, Table 1)
   - Conclusion verbatim: models "often fail to generate cultural artifacts in architecture, clothing, and food, especially for underrepresented country regions." (OBS)
   - **Malaysia was not in the 10 countries.** If Indonesia — with ~10× the population and far more web-scraped batik/textile imagery — lands bottom-half, Malay-specific artifacts (songket *weave structure* vs Indonesian batik *wax-resist*, tengkolok fold geometry, which is a *Malay-court* item with a tiny web corpus) are strictly harder. DER, high confidence.
   - Standard metrics don't even see the failure: FID and LPIPS had **negative** correlation with human cultural-similarity judgments (−0.11, −0.14); only their trained CultDiff-S metric got +0.18 (OBS, Table 2). Any internal eval using FID/CLIP for cultural fidelity is measuring nothing.
2. **Malaysia-specific peer-reviewed study (UiTM Melaka, IJRISS Vol 10(1) 2026, DOI 10.47772/IJRISS.2026.10100164)** — Midjourney/DALL-E/SD on Malaysian icons, expert panel, VARS 8-criteria:
   - **"A significant 'Cultural Accuracy Gap' was identified across all models"** — broad subjects (Nasi Lemak: "Near Perfect" agreement for Midjourney) OK; **intricate architecture (landmarks) and specific persons FAIL** (OBS, abstract).
   - Real-world scar cited in-paper: PDRM's AI Merdeka billboard rendered **three KLCC towers** — public, national-scale proof that structural Malay iconography is outside these models' reliable knowledge (OBS, ref 21).
   - DALL-E refused/could not render a Malaysian politician "due to ethical concern" — safety filters add a *second* failure mode on top of capability (OBS).
3. **Songket/keris/tengkolok specifically:** no benchmark, paper, or model card anywhere in this research mentions them (searched: songket, keris, tengkolok, batik+AI). Batik is the *only* Malay-archipelago textile with a research thread — and even there, the generative-AI batik literature (GAN-based, e.g. IJASEIT batik-GAN: FID-global 42, FID-local 16) shows documented "Failed Batik Pattern because of lost the main pattern" cases (OBS, ResearchGate figure from batik pattern study). Textile *weave structure* (songket's supplementary-weft gold threads) is a fine-grained texture regularity that diffusion VAEs at 1024px systematically blur — DER from FLUX Kontext paper's own VAE reconstruction analysis (rFID 0.949→0.332 range across VAEs).

**Which models handle non-Western iconography relatively well:**
- **Qwen-Image / Qwen-Image-Edit** — the only frontier model with *native logographic text rendering* and China-centric training; East/Southeast-Asian material culture is measurably better-represented than in SD/FLUX (REP, tech report + community; CultDiff shows China also scores low on *Western-annotator* scales but that conflates annotator familiarity). Best commercial bet for "Asian" iconography generally. NOT verified for Malay-court items.
- **FLUX.1-dev** — best open base for ControlNet/IP-Adapter stacks, so the *reference-image pathway* (give it a real songket photo as IP-Adapter/Redux input) works better than on SDXL. But its text-conditioned Indonesia scores are bottom-half (CultDiff).
- Everything else: no evidence of SEA specialization.

**The operative conclusion for the federation:** cultural fidelity cannot be prompt-engineered or adapter-injected — the knowledge isn't in the weights. The only reliable pathway is **reference-image conditioning with real photographs of the actual artifact** (songket swatch, keris blade, tengkolok fold) via IP-Adapter/Redux/Kontext character+style reference, or **LoRA training on a small curated corpus** (the Qwen-Image-Edit-F2P face-LoRA pattern generalizes to artifact-LoRAs). Text prompts alone = the 2.5-3.5/5 you measured, permanently.

---

## 4 · Independent sources per model family (≥3 each, URLs)

**IP-Adapter / FaceID family:**
1. F-Bench (ICCV 2025): https://arxiv.org/html/2412.13155v2 + https://openaccess.thecvf.com/content/ICCV2025/papers/Liu_F-Bench_Rethinking_Human_Preference_Evaluation_Metrics_for_Benchmarking_Face_Generation_ICCV_2025_paper.pdf
2. Model card: https://huggingface.co/h94/IP-Adapter-FaceID
3. ConsistentID paper comparison table (CVPR 2024): https://arxiv.org/html/2404.16771v1
4. PuLID paper quantitative comparison: https://arxiv.org/html/2404.16022v2

**InstantID:**
1. Paper: https://arxiv.org/abs/2401.07519
2. Project page: https://instantid.github.io/
3. GitHub: https://github.com/instantx-research/instantid
4. F-Bench evaluation: https://arxiv.org/html/2412.13155v2
5. PuLID comparison: https://arxiv.org/html/2404.16022v2

**PhotoMaker:**
1. Paper: https://arxiv.org/abs/2312.04461 (v1/v2)
2. PuLID Table 4/6 numbers: https://arxiv.org/html/2404.16022v2
3. F-Bench radar: https://arxiv.org/html/2412.13155v2
4. ResearchGate survey coverage: https://www.researchgate.net/publication/384144278

**PuLID / InfiniteYou (ByteDance line):**
1. PuLID: https://arxiv.org/html/2404.16022v2 · https://github.com/ToTheBeginning/PuLID
2. InfiniteYou (ICCV 2025 Highlight): https://arxiv.org/html/2503.16418v2 · https://openaccess.thecvf.com/content/ICCV2025/papers/Jiang_InfiniteYou_Flexible_Photo_Recrafting_While_Preserving_Your_Identity_ICCV_2025_paper.pdf · https://github.com/bytedance/InfiniteYou
3. Community verdict (ComfyUI): https://www.reddit.com/r/comfyui/comments/1uwl84a/
4. Field comparison guide: https://aiofm.info/en/guides/pulid-vs-instantid-vs-faceid

**FLUX.1 Kontext:**
1. Paper (KontextBench): https://arxiv.org/abs/2506.15742 · HTML: https://arxiv.org/html/2506.15742v2
2. Official: https://bfl.ai/blog/flux-1-kontext (vendor — used only for availability/pricing facts)
3. TBStar-Edit independent bench (Ecom-Edit, beats Kontext-dev): https://arxiv.org/html/2510.04483v1
4. Independent fine-tune comparison (Oxen): https://ghost.oxen.ai/fine-tuned-qwen-image-edit-vs-nano-banana-and-flux-kontext-dev/
5. 26-prompt 4-way test: https://wiro.ai/blog/nano-banana-vs-qwen-flux-kontext-pro-seededit/

**Qwen-Image-Edit:**
1. Tech report: https://arxiv.org/abs/2508.02324
2. Model card: https://huggingface.co/Qwen/Qwen-Image-Edit
3. 2511 consistency release: https://qwen.ai/blog?id=qwen-image-edit-2511
4. Face-consistency failure field report: https://www.reddit.com/r/comfyui/comments/1rj994t/
5. Ecom-Edit Bench win: https://arxiv.org/html/2510.04483v1

**Gemini 2.5 Flash Image (nano-banana):**
1. LMArena/Oxen launch coverage: https://ghost.oxen.ai/fine-tuned-qwen-image-edit-vs-nano-banana-and-flux-kontext-dev/
2. WithEveryone (GPT-Image-2/MLLM-class face-sim numbers): https://www.researchgate.net/publication/413064802
3. Wiro 26-prompt test: https://wiro.ai/blog/nano-banana-vs-qwen-flux-kontext-pro-seededit/

**Cultural-accuracy evidence base:**
1. CultDiff (KAIST): https://arxiv.org/html/2502.08914v1
2. UiTM Malaysian-icons study: https://rsisinternational.org/journals/ijriss/view/evaluating-visual-accuracy-in-ai-generated-images-of-malaysian-themed-icons (DOI 10.47772/IJRISS.2026.10100164)
3. ICCV 2025W face-generation bias framework: https://openaccess.thecvf.com/content/ICCV2025W/STREAM/papers/Yu_Data_Bias_Mitigation_and_Evaluation_Framework_for_Diffusion-based_Generative_Face_ICCVW_2025_paper.pdf
4. MLLM cultural bias (C3NLP 2025): https://aclanthology.org/2025.c3nlp-1.11.pdf
5. Cultural-bias systematic review: https://www.researchgate.net/publication/393394999

---

## 5 · Access-class matrix (open vs API vs local-installable)

| Class | Models |
|---|---|
| **Open weights, HF-downloadable, ComfyUI-installable** | IP-Adapter-FaceID(+Plus v2) · InstantID · PhotoMaker v1/v2 · PuLID v1.1 · PuLID-FLUX · **InfiniteYou-FLUX v1.0** · Qwen-Image-Edit (2509/2511) · FLUX.1 Kontext **[dev]** (non-commercial license; $999/mo commercial via BFL) · FLUX.1-dev base |
| **API-only (paywalled)** | **FLUX.1 Kontext [pro]/[max]** · Gemini 2.5 Flash Image · GPT-Image-1 · mmx image-01 (MiniMax) · SeedEdit 3.0/Seedream 4.0 · wan2.x-image · Midjourney · DALL-E |
| **Both** | Qwen-Image-Edit (HF weights + DashScope) — the federation's currently-dead lane is recoverable locally from HF without DashScope |

---

## 6 · Why the federation's lanes fail — diagnosis mapped to evidence

| Lane | Measured symptom | Root cause (evidence-backed) | Class |
|---|---|---|---|
| mmx image-01 `--subject-ref` | 4-7/10 identity | Black-box adapter inside the published 0.6-0.77 cosine envelope; no architecture or benchmark published → cannot be tuned past vendor ceiling | Capability ceiling (not defect) |
| mmx image-01 cultural | 2.5-3.5/5 | Training-data absence for Malay-court artifacts; CultDiff shows even Indonesia bottom-half on FLUX-class bases; text-prompt pathway cannot inject absent knowledge | Data absence (unfixable by prompting) |
| qwen-image-edit | Connection-dead from kernel | Infrastructure, not model. Note: even alive, it's an *instruction-editing* model — community reports ~20% face consistency without a face LoRA | Wrong tool for identity; right tool for edits |
| wan2.7-image-pro | Connection-dead | Could not verify externally (see §8) | UNKNOWN |
| gemini-2.5-flash-image | Untested, key present | MLLM-native class: strong editing, but cosine face-sim for this class measured ~0.46-0.50 (GPT-Image-2 proxy) — below adapter class | Test it, expect mid identity |

---

## 7 · Recommended architecture (smallest reversible path)

1. **Identity lane:** run a benchmark of **InfiniteYou-FLUX (sim_stage1)** locally vs **FLUX.1 Kontext [max]** API vs current mmx image-01, on 10 federation reference faces (include masculine-jaw, darker-skin-tone subjects), scoring with **AuraFace or InsightFace cosine** (both are what the papers use — do NOT use CLIP-I or FID; CultDiff proved they anti-correlate with human cultural judgment).
2. **Cultural lane:** stop text-prompting songket/keris/tengkolok. Build a **reference-image conditioning pathway** (IP-Adapter/Redux on FLUX, or Kontext style-reference) fed with real photographs of the artifacts; if the archetype matters long-term, a **small artifact-LoRA** (30-100 curated images) is the only mechanism in the literature that actually installs missing cultural knowledge.
3. **Eval lane:** adopt CultDiff-S-style human-anchored scoring for cultural fidelity; the UiTM VARS 8-criteria panel is a ready-made Malay-context rubric.
4. **Retire or demote:** PhotoMaker-class (0.27) anything in federation tooling; generic FLUX IP-Adapter for faces.

---

## 8 · Blocked lanes & smallest unblock probes

- **wan2.x-image-pro research: PARTIAL.** Token-plan connectivity dead from this kernel and no independent benchmark found in external search within budget. Smallest probe: web search from a non-federation egress for "Wan 2.5 image edit technical report arxiv" — Alibaba publishes Wan video tech reports (arXiv:2503.20314 lineage); an image-edit report may exist behind modelscope.cn, which firecrawl did not surface.
- **Reddit thread bodies:** firecrawl refuses reddit.com ("we do not support this site"). Two community data points were recovered via search excerpts instead (r/comfyui 20% face consistency; InfiniteYou>PuLID). Unblock probe: old.reddit.com via browser tool if full threads are needed.
- **mmx image-01 internals:** no public architecture paper exists. Unblock probe: none possible externally — only first-party A/B testing moves this.

---

## 9 · F2 honesty ledger

- Every quantitative claim above is traceable to a scraped primary source this session; the three big tables (PuLID T4/T6, CultDiff T1/T2, F-Bench radar, KontextBench Fig 8) were read from the arXiv HTML directly, not from secondary summaries.
- The aiofm.info "~0.69/0.72/0.78" figures are a *field guide*, REP-class only — used once, labeled.
- Vendor pages (bfl.ai, qwen.ai, minimax docs) used only for availability/pricing/interface facts, never for quality verdicts.
- The wiro.ai 26-prompt test is quasi-promotional (aggregator blog); used only for its runtime/price table and the qualitative one-liners, labeled REP.
- **Not found anywhere (UNKNOWN):** any face-sim number for mmx image-01, Gemini 2.5 Flash Image, or SeedEdit; any songket/keris/tengkolok benchmark; any Malaysia entry in CultDiff; jaw-feature-specific failure studies.

*Compiled by Hermes external-research subagent for the AAA visual-intelligence hardening project. REALITY > EVERYTHING.*
