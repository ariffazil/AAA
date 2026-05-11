# LLM Engineering — Core Topics Map
*Source: Towards Data Science | Aliaksei Mikhailiuk | May 9, 2026*

## 13 Must-Know Topics for LLM Engineering

| # | Topic | Key Points |
|---|-------|-----------|
| 1 | Tokenisation | BPE (Byte-Pair Encoding), subword units, vocabulary building |
| 2 | Embeddings | dense vector spaces, semantic relationships, word2vec/GloVe/BERT |
| 3 | Positional Encoding | absolute (sine/cosine), RoPE (relative/rotary), learned positional |
| 4 | Transformer Architecture | Multi-Head Attention, FFN, Residual Connections, LayerNorm |
| 5 | Attention Types | self-attention, masked self-attention, cross-attention; O(n²) complexity bottleneck |
| 6 | Architecture Types | Encoder-only (BERT), Decoder-only (GPT), Encoder-Decoder (T5/BART) |
| 7 | Decoding Strategies | greedy, beam search, top-k, top-p (nucleus), temperature |
| 8 | Pre-training | scaling laws, data sources (web/books/code), data quality & filtering challenges |
| 9 | Fine-tuning | SFT, LoRA (Low-Rank Adaptation), parameter-efficient methods |
| 10 | RLHF / Alignment | preference learning, safety constraints (capability → alignment) |
| 11 | Prompt Engineering | techniques to guide model behaviour |
| 12 | Evaluation | pitfalls, benchmarks, metrics |
| 13 | Inference Optimization & Hallucination Reduction | practical deployment concerns |

## Summary
Written for engineers moving from other ML backgrounds into LLMs. Structured as a map, not a deep-dive — bridges the gap between theory and practical reality.

## arifOS Notes
- Relevant for: arifOS MCP engineering, OpenClaw tool design, AI agent architecture
- Gap assessment: where is current arifOS stack relative to these layers?
- Action: review which topics directly apply to current build vs. future scaling
