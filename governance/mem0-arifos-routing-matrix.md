# mem0 ↔ arifOS Routing Matrix — S3 Semantic Recall Canon

> **Status:** CANONICAL_COMMIT (Loop #2 of 9-loop triage 2026-09-12) · canonicalized by FI-008 from 333-AGI §A design
> **Evidence class:** OBS — every number below re-probed live 2026-09-12 00:1x MYT (2026-09-11 16:1x UTC) by FI-008, not copied from the triage doc.
> **Parents:** `institutional-memory-strata` (WHERE memory lives) · `memory-promotion-gate` (WHEN writes are allowed)
> **Probe discipline:** every row carries its falsifiable command. A claim without its probe is intent wearing witness clothes.

---

## 1. Substrate observed (Qdrant `127.0.0.1:6333`, live 2026-09-12 00:1x MYT)

17 collections alive. Point counts + dense-vector config via `/collections/<name>`:

| Collection | Points | Dense config | Owner / role |
|---|---|---|---|
| `mem0` | **11,104** | 1024-dim Cosine | Hermes S3 (per `~/.hermes/config.yaml:34 provider: mem0`) — live writes ongoing (11,097 @ triage 00:14, 11,277 @ 2026-09-11 audit; count drifts with traffic) |
| `arifos_memory` | 99 | 1024-dim Cosine | Federation S3 default (arif_memory L1–L6 / forge_memory) |
| `petronas_knowledge` | 1,460 | 1024-dim Cosine | Domain corpus (GEOS) |
| `arifos_precedent` | 255 | 1024-dim Cosine | JUDGE-anchored floor precedents |
| `arifOS_skill_mesh` | 191 | **384-dim** | Live tool affordance mirror |
| `federation_memory_patterns` | 103 | **384-dim** | Cross-organ patterns |
| `atlas333_eureka` | 74 | 1024-dim | Eureka/paradox entries |
| `arifos_session_memory` | 56 | 1024-dim | session_id-keyed chat memory |
| `federation_shared` | 30 | 1024-dim | Cross-organ shared |
| `arif_evidence` | 16 | **768-dim** | Evidence payloads (different embedder) |
| `arifos_constitution` | 14 | 1024-dim | Constitution fragments |
| `arifos_vault_canon` | 13 | 1024-dim | Sealed canon |
| `arifos_vault_working` | 7 | 1024-dim | Mutable working surface |
| `openclaw_memory` | 9 | 1024-dim | OpenClaw edge memory — **NOT in triage §A list; observed live** |
| `identity_vault` | 2 | **512-dim** | Sovereign identity bindings |
| `arifos_audio_memory` | 2 | no dense vectors (sparse/BM25 only) | Audio EMD packets |
| `mem0migrations` | 0 | 1024-dim | Bookkeeping |

**Corrections vs triage doc §A (F2 drift caught by re-probe):**
1. `arifos_evidence` — listed in triage §A; **ABSENT live**. The evidence collection that exists is `arif_evidence` (768-dim). Routing rule below uses the witnessed name.
2. `openclaw_memory` — not in triage §A; **exists live** (9 pts). Added to matrix.

Falsify: `curl -s 127.0.0.1:6333/collections | python3 -m json.tool | grep name`

## 2. Routing rules (canonical)

| Intent | Route to | Reason | Falsifiable check |
|---|---|---|---|
| Hermes private memory (per-user, per-group) | `mem0` | Wired via config.yaml:34; live 11k pts; multi-tenant isolation native | `grep -A2 '^memory:' /root/.hermes/config.yaml` |
| Federation canonical doctrine / SKILL canon | `arifos_vault_canon` | Immutable canon lives in governed substrate (F11) | points_count > 0 |
| Federation working / scratch reasoning | `arifos_vault_working` | Mutable, kernel-bound | points_count > 0 |
| Constitutional floor precedents | `arifos_precedent` | JUDGE-anchored | 255 pts |
| Atlas333 / eureka entries | `atlas333_eureka` | Existing collection | 74 pts |
| Per-session memory (chat) | `arifos_session_memory` | session_id keyed | 56 pts |
| Audio reflex packets (EMD pipeline) | `arifos_audio_memory` | media-typed, sparse-only | 2 pts |
| Skill mesh (live tool affordances) | `arifOS_skill_mesh` | live-mirrored, 384-dim | 191 pts |
| Cross-organ shared patterns | `federation_shared` + `federation_memory_patterns` | cross-organ lanes | 30 / 103 pts |
| Identity bindings | `identity_vault` | sovereign-bound, 512-dim | 2 pts |
| Petronas / GEOS domain corpora | `petronas_knowledge` | domain corpus | 1,460 pts |
| OpenClaw edge memory | `openclaw_memory` | edge-agent private lane (new row, live-observed) | 9 pts |
| Generic federation recall (default) | `arifos_memory` | ONLY when intent is explicitly "recall federation canon" — near-empty (99 pts) is expected, not a bug | 99 pts |

**Anti-rule (from institutional-memory-strata):** Hermes recall ≠ arifos_memory. Never route Hermes user memory into federation collections; never claim "Hermes remembers" while pointing at `arifos_memory`.

## 3. Embedding-dimension boundary (observed)

Five different dense configs coexist (1024 / 768 / 512 / 384 / sparse-only). Cross-collection ANN joins are **invalid** across dimension boundaries — any reconciliation tooling must embed per-target-collection, not reuse vectors. Witnessed pairs:
- 1024: mem0, arifos_memory, petronas_knowledge, most arifos_* lanes
- 768: arif_evidence · 512: identity_vault · 384: arifOS_skill_mesh, federation_memory_patterns · sparse-only: arifos_audio_memory

## 4. Open Loop — carried forward (F13 decision pending)

Two parallel S3 stores without automatic reconciliation: `mem0` (Hermes-private, 11k pts) and `arifos_memory` (federation-shared, 99 pts). Options on the table: (a) converge to one backend, or (b) declare mem0 Hermes-private permanently and stop calling arifos_memory canonical for Hermes. Until F13 decides, every agent reading the strata fragment gets a wrong picture of where Hermes memory lives. This matrix is the interim routing truth: **option (b) behavior** — explicit split, no cross-writes, no convergence claims.

## 5. Maintenance law

- Point counts here are a snapshot, not a registry. Any agent citing a count must re-probe (`/collections/<name>`) — mem0 drifts by the hour.
- New collection appears → this matrix gets a row or the anomaly gets flagged (openclaw_memory was invisible to the 2026-09-11 audit because no one listed collections that day).
- A listed collection missing live → correct the matrix, don't narrate around it (arifos_evidence).

DITEMPA BUKAN DIBERI ⚒️
