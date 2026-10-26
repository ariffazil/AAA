# BOOKMARK — RAW-RAG is the null hypothesis for agent memory

> **Status:** REFERENCE_ANCHOR · 2026-10-24 · Ditempatkan oleh HERMES atas arahan F13 ("bookmark it")
> **Paper:** Zhengye Bao, Shengtao Zhang, Haokai Zhang, Shiqi Lou, Muning Wen, Minnan Luo.
> *Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought.*
> arXiv:2610.30755v1 · 22 Oct 2026 · https://arxiv.org/abs/2610.30755
> **Verification:** title, authors, four benchmarks, "six of seven", "0.13-5.53 points" and the
> evidence-coverage explanation all read from the arXiv API record on 2026-10-24T05:35Z.
> The abstract's own closing line: naive RAG is "an essential baseline."

## The claim, in the paper's own terms

Raw-RAG = dense retrieval + reranking over RAW conversation history, then a reader LLM.
No extraction, no mutation, no graph, no learned retrieval policy.

It ranked **first in 6 of 7 benchmark-model settings** across LoCoMo, LongMemEval, MEME and
MemoryAgentBench, beating the strongest agentic-memory system by **0.13-5.53 points**.

Mechanism the authors name: **evidence coverage**. Useful evidence is not only the answer value
but *the relations and dependency paths needed to derive it*. Transforming conversations into
extracted memory entries discards those connections — and **even complete access to the
transformed store leaves an accuracy gap relative to raw evidence.**

## Why this binds arifOS

This is the same failure class this federation produced five times in one week, in five
different registers — not because memory is bad, but because compression dropped the path:

| Compression | What vanished | Where it bit |
|---|---|---|
| callsign `333-AGI` | harness · model · boot time · PID · custody window | attribution became UNKNOWN |
| verdict `PASS` | the empty input that produced it | `{}` → PASS class of defect |
| state `3 holds` | source · observed_at · generation time · write-path status | three incompatible realities |
| metric `FQ` | scope · denominator · timestamp | unlike measurements made to look equal |
| dashboard `valid state` | why the producer stopped | stale truth re-rendered as fresh |

**The invariant, stated as a hierarchy:**

    RAW EVIDENCE > DERIVED MEMORY > SUMMARY > NARRATIVE

Raw evidence preserves what happened. RAG locates what may matter. Memory preserves reusable
interpretation. Skills preserve reusable procedure. Governance determines admissible action.
Receipts bind action back to reality.

Derived memory may guide attention. **It may never silently overwrite the raw record.**

## Layer placement in arifOS (does not replace existing doctrine — it names the floor beneath it)

- **L0 raw evidence** — transcripts, command output, diffs, API responses, timestamps, source
  hashes, process/harness identity, receipts, test results, live probes, deploy observations.
- **L1 retrieval** — dense + rerank. **Mandatory baseline** for any memory claim.
- **L2 derived memory** — lessons, task state, ownership maps, failure modes, scars, skills,
  open contradictions. Every promoted entry must carry: provenance · scope · status ·
  observed_at · falsifier · link to raw evidence.
- **L3 governance** — 333 proposes, 555 verifies, 888 judges, A-FORGE executes, VAULT999
  witnesses, F13 accepts consequence. Retrieval supplies evidence; it confers no authority.

## The test any memory layer must now pass

Before AAA / HERMES / Mem0-like layer claims improvement, run it against Raw-RAG on the same
workload. Measure: answer accuracy · necessary-evidence coverage · dependency-path preservation ·
temporal-relation preservation · attribution accuracy · contradiction retention · ingestion time ·
retrieval latency · storage cost · recovery from incorrect memory mutation.

Ablate: **A** raw only · **B** derived only · **C** raw + derived · **D** raw + derived + governance.

The memory layer earns its existence only if it improves a load-bearing measure without
destroying evidence needed for later re-examination.

## Scope limit (F2)

The paper evaluates *conversation tasks* (LoCoMo, LongMemEval, MEME, MemoryAgentBench). It does
not claim complex memory is useless everywhere — it claims naive RAG is an essential baseline
that beat the compared agentic systems on those benchmarks. Extrapolating past that is ours to
prove, not theirs to assert. That is why this is filed as a reference anchor, not a doctrine seal.

## Note for AAA (open, not acted on)

Current AAA memory architecture was not built against this baseline. Whether it beats Raw-RAG is
**UNMEASURED** — which is itself the honest state, and the same state F6 sits in. Do not claim
memory improves recall until ablated against raw retrieval on the federation's own workload.
