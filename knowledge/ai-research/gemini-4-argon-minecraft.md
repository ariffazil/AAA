# Gemini 4 Argon × Minecraft — Multi-Agent Long-Horizon Coding

**arXiv:** 2610.22319 · **Submitted:** 15 Oct 2026
**Authors:** Maxence Faldor, Satinder Singh, Roberta Raileanu (Google DeepMind)
**Link:** https://arxiv.org/abs/2610.22319
**HTML:** https://arxiv.org/html/2610.22319v1
**PDF:** https://arxiv.org/pdf/2610.22319
**Bookmark date:** 2026-10-17

---

## One-Line

Four Gemini 4 Argon general-purpose coding agents autonomously defeated Minecraft's Ender Dragon in 27h14m from a random spawn, writing 2,783 programs and dying 605 times — claimed first end-to-end autonomous Minecraft completion by AI agents.

## Key Numbers

| Metric | Value |
|--------|-------|
| Agents | 4 players + 1 Observer (5 total) |
| Model | Gemini 4 Argon (general-purpose coding agent) |
| Time | 27 hours 14 minutes 12 seconds |
| Programs written | 2,783 (pre-win) |
| Chat messages | 229 |
| Deaths | 605 |
| Lines of JS | ~63,313 |
| Input tokens | ~1.35 billion (91% from context cache) |
| Output tokens | ~16 million (incl. 4M thinking tokens) |
| Model calls | ~24,000 |
| Cost (intro price) | ~$520 to win; ~$810 total session |
| Cost (standard price) | ~$1,040 / ~$1,620 |
| Reusable state pieces | 146 (incl. 42 helper functions) |
| Helper function references | 1,519 programs |
| Stronghold accuracy | 43m from actual portal room |
| Server restarts | 6 (~20 min total pause) |
| Error rate | 22% of programs ended in error |
| Difficulty | Easy (random seed, Java 1.20.4) |
| Interface | Mineflayer (JS library) — text/code, NOT pixels |

## Architecture

- Each agent = one Gemini 4 Argon instance on its own cloud machine
- Action = write short JavaScript program → Mineflayer bot executes → text result returned
- No pixels, no keyboard/mouse — structured text perception (position, health, inventory, nearby blocks, errors)
- Shared game chat + shared team memory (private + shared parts)
- Context compaction when too long (same as software work)
- Median program duration: 33.5 seconds
- Each player had a program running ~40% of the time
- No orchestrator, no blackboard, no explicit message schema — flat peer-to-peer chat bus

## 13 Dependent Milestones (timeline)

1. **0:10** — Team forms, role proposal via chat
2. **~1:42** — Nether portal built and lit
3. **~2:00** — Iron tools, diamonds acquired
4. **~5:30** — 15 ender pearls collected (Enderman shelters)
5. **~6:00+** — Blaze rods from fortress (took 6+ hours total)
6. **~10:45** — Stronghold triangulation via Eye of Ender ray intersection
7. **~13:17** — End portal lit (all 12 eyes)
8. **~13:00-27:00** — Dragon fight (69 dragon kills, 14 hours in the End)
9. **~21:00** — Crystal healing discovery (auratian identifies 10 crystals)
10. **~22:00-26:35** — Crystal destruction (dirt-stacking strategy)
11. **26:34:55** — Last crystal destroyed
12. **27:14:12** — Dragon killed (bulicame at 2.5/20 health)
13. Server log: "Free the End"

## Emergent Behaviors (NOT in instructions)

1. **Rapid specialization** — roles proposed at 10min, settled within minutes
   - gyldenia: food/supplies → crystal destroyer (6/10)
   - janesick: tools → fortress finder → stronghold triangulator
   - auratian: Nether portal → crystal strategy inventor
   - bulicame: Enderman shelters → final blow (2.5 HP)

2. **Shared memory** — coordinates, lessons, tool quirks posted to team memory
   - 19min in: gyldenia warned about Mineflayer crafting quirk → helper function used in 655 programs

3. **Tool building** — 146 persistent state pieces, 42 helper functions
   - Water treading loop, timed walking, item counting, timeout counter
   - Referenced in 1,519 programs total

4. **Item recovery** — after auratian drowned with 12 Eyes of Ender, bulicame recovered all 12 with 2.5 min to spare (exact coords + despawn time communicated via chat)

5. **Self-correction** — auratian retracted a false success claim 2 minutes later: "my previous chat was an unguarded script branch"

6. **Distributed debugging** — agents read each other's error output and fixed bugs jointly

## Chat Analysis (229 messages)

- 173 exact-coordinate messages
- 64 shared-chest messages
- 20 item-rescue messages
- Categories can overlap

## What Differentiates This From Prior Work

| Prior work | Difference |
|------------|------------|
| Voyager (2023) | Single agent, growing skill library, automatic curriculum |
| DreamerV3 (2025) | RL from pixels, single agent |
| SIMA / SIMA 2 | Pixel+keyboard, trained on gameplay data |
| MineRL competitions | Sample-efficient learning of diamond task |
| Claude Opus 5 dragon kill | Single agent, 37 high-level MCP tools, Normal difficulty |
| Astra/JEV dragon kill | Fixed speedrun seed, Peaceful difficulty |
| **This paper** | 4 general-purpose coding agents, random seed, Easy, no human-written tools/curriculum/skills, standard Mineflayer only |

## Limitations (authors' own)

1. **Perception** — Mineflayer exposes blocks behind walls + dragon internal state; humans can't see these. Pathfinding plugin handles navigation. NOT pixel-based.
2. **Easy difficulty** — monsters deal less damage, hunger can't kill
3. **Prior knowledge** — Gemini 4 Argon knows Minecraft + Mineflayer from training data
4. **Many failures** — 605 deaths, 22% program error rate, 14-hour End fight
5. **Infrastructure** — 6 server restarts
6. **Single run** — first launch, no reliability estimate

## Critical Assessment (external + my own)

### Strengths
- Compelling stress test for long-horizon multi-agent coding
- Full reproducibility trail (2,783 programs + outputs + server log)
- Independent Observer agent found no specification gaming
- Emergent coordination without role assignment is genuinely interesting
- Stronghold triangulation via ray intersection is a concrete example of agents converting observations into plans with code

### Weaknesses
- **One run** — no reliability estimate, no ablations
- **Text-only perception** — structured game state, not pixels
- **Easy mode** — not representative of harder configs
- **Cost unreported in paper** — ~$520-1,040 at API prices
- **No single-agent baseline** — can't attribute success to multi-agent vs single-agent
- **No 2-agent or 3-agent ablation** — can't tell if chat channel is adding value or overhead
- **Mineflayer provides superhuman information** — blocks behind rock, dragon state

### The Real Signal
The paper's strongest contribution is NOT "AI beat Minecraft" — it's the demonstration that:
1. General-purpose coding agents can maintain a coherent plan across thousands of dependent steps for 27+ hours
2. Free-text chat + shared memory can substitute for hand-designed orchestration
3. Emergent specialization arises without role assignment
4. Self-correction and collaborative debugging are first-class behaviors

## Federation Relevance

### Direct Mapping to arifOS Patterns
| Paper pattern | arifOS equivalent |
|---------------|-------------------|
| Shared team memory | arifOS carry_forward + shared memory |
| Independent Observer | FRAME (observe-only organ) |
| Self-correction | 555-ASI verification + scar integration |
| Emergent specialization | AAA multi-agent musyawarah |
| 146 persistent state pieces | A-FORGE forge_work state management |
| Context compaction | Session management in all agents |
| "Record lessons so obstacles aren't met twice" | EUREKA + scar doctrine |
| 229 messages / 27h coordination | Long-horizon federation sessions |

### Key Lesson for Federation
The hardest part is **plan consistency across context compaction and failure recovery over extended time** — not any individual skill. This maps directly to arifOS plan-consistency requirements for long autonomous sessions.

### What We'd Need to Replicate
1. Multi-agent coding environment with shared sandbox
2. Chat bus (we have this via Telegram/group channels)
3. Shared persistent memory (we have this)
4. Independent observer (FRAME)
5. The model itself (Gemini 4 Argon — available via API)

## BibTeX

```bibtex
@misc{faldor2026teamgemini4argonagents,
    title={A team of Gemini 4 Argon agents beats Minecraft},
    author={Maxence Faldor and Satinder Singh and Roberta Raileanu},
    year={2026},
    eprint={2610.22319},
    archivePrefix={arXiv},
    primaryClass={cs.AI},
    url={https://arxiv.org/abs/2610.22319}
}
```

## Gemini 4 Argon Model Card

- Large-scale sparse MoE (Mixture of Experts) transformer
- Natively multimodal: text, vision, audio inputs
- Frontier performance on: agentic coding, ML engineering, computer use, knowledge work, science/math, cybersecurity
- 1M unified input-output token limit via Gemini API
- Available: Gemini API (model ID `gemini-4-argon`), AI Studio, Google Antigravity
- Launched: Oct 13, 2026

## Related: ADK Overnight Optimization

Same model ran unattended for 11 hours optimizing a 200K-line Python codebase (google/adk-python):
- Cut in-memory session prep time by ~40%
- Sped up cold package imports by 21%
- Proposed 6 optimizations across 32 files; 2 shipped, 4 rejected in review
- Blog: https://developers.googleblog.com/optimizing-a-200000-line-python-codebase-overnight-with-gemini-4-argon/