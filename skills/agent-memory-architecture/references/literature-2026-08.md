# Multimodal Memory Literature — condensed (verified 2026-08-07)

Live-verified against arxiv abstract pages, project site, GitHub, and Emergent Mind.

## M3-Agent — Seeing, Listening, Remembering, and Reasoning (ByteDance Seed et al., arXiv 2508.09736)
- Multimodal agent with long-term memory: real-time visual + auditory input → episodic AND semantic memory.
- Memory organized **entity-centric, multimodal** — a shift from document memory to world-model memory.
- M3-Bench: 100 robot-perspective + 920 web long videos, open-ended QA; RL-trained agent beats Gemini-1.5-pro / GPT-4o prompting baselines by 5–8%.
- Strong: relational witness, episodic memory, entity persistence. Weak: affective witness, rasa preservation.

## AffectAgent (arXiv 2604.12735)
- Collaborative multi-agent reasoning for retrieval-augmented multimodal emotion recognition.
- Emotion understanding improves when retrieval becomes part of affective reasoning, not just model weights.
- Closest published direction to an "affective witness" — a building block for affect-aware retrieval, not yet a memory architecture.

## Awesome-Multimodal-Memory (github.com/patrick-tssn, TMLR 2025 reading list)
- Taxonomy: (A) multimodal context modeling with memory (audio/video context, long-video understanding, video QA/summarization); (B) robotics memory (navigation, planning, manipulation reasoning); (C) external memory augmentation (audio/image/video knowledge stores, retrieval-augmented MLLMs).
- Field converging on explicit memory structures rather than larger context windows.
- Links "The AI Hippocampus" (TMLR 2025): consolidation, forgetting, salience weighting, emotional significance — human memory is not a giant vector database.

## Emergent Mind — Multimodal Memory Systems (api.emergentmind.com/topics/multimodal-memory)
- Memory entry = structured tuple: raw sensory data + text annotation + metadata (timestamp, geolocation, context labels) — e.g. Memory-QA Mi=(Ii, Ci, Ti, Li).
- Structured/hierarchical arrangements: entity-centric graphs (M3-Agent), knowledge triples, dual-stream logical/visual memory banks, object-temporal dual-indexing.
- Ablations: multisignal retrieval (temporal + location + semantic) and explicit memory consolidation give the largest marginal gains.
- HippoMM (arXiv 2504.10739): mirrors hippocampal processes — pattern separation (adaptive segmentation), pattern completion (semantic replay), hierarchical retrieval.

## Synthesis — three waves
1. Remember text → RAG + vectors (solved)
2. Remember images/audio/video → multimodal embeddings + entity memory (active)
3. Remember human experience → affective persistence, emotional trajectory, dignity/suffering-aware memory (largely unsolved — the open frontier)
