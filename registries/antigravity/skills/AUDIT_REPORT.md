# Skill Portfolio Audit Report

Generated: 2026-06-12T17:08:58.993577+00:00
Scope: /root/.agents/skills, /root/.claude/skills, /root/.codex/skills, /root/.arifos/agents/kimi/skills, /root/.hermes/skills

## Summary

- Total skills audited: **269**
- Skills with any rot flag: **153**
- Prompt bloat (>500 lines): **24**
- Stale (>30 days): **59**
- Unused candidate (>90 days): **0**
- Doc-rot (broken paths/symlinks): **52**
- High collision pairs (Jaccard ≥0.35): **8**

## Rot Matrix

| Skill | Version | Lines | Age (d) | Rot Tags | Broken Paths | Broken Symlinks |
|-------|---------|-------|---------|----------|--------------|-----------------|
| compare-models | unknown | 47 | 43.1 | stale-rot | - | - |
| find-models | unknown | 47 | 43.1 | stale-rot | - | - |
| prompt-images | unknown | 200 | 43.1 | stale-rot | - | - |
| prompt-videos | unknown | 334 | 43.1 | stale-rot, prompt-bloat | - | - |
| run-models | unknown | 69 | 43.1 | stale-rot | - | - |
| agents-sdk | unknown | 221 | 43.1 | stale-rot | - | - |
| arifos-evals | unknown | 107 | 17.5 | - | - | - |
| arifos-governance | unknown | 90 | 17.5 | - | - | - |
| arifos-mcp-federation | 1.1.0 | 108 | 0.0 | - | - | - |
| arifos-memory | 1.1.0 | 96 | 0.0 | - | - | - |
| arifos-observability | unknown | 72 | 17.5 | doc-rot | /root/.agents/telemetry/ | - |
| arifos-plan-dag | unknown | 73 | 17.5 | - | - | - |
| arifos-recursive-audit | unknown | 81 | 17.5 | - | - | - |
| arifos-untrusted-sandbox | 1.0.0 | 84 | 5.9 | - | - | - |
| cloudflare | unknown | 245 | 43.1 | stale-rot | - | - |
| cloudflare-email-service | unknown | 103 | 43.1 | stale-rot | - | - |
| durable-objects | unknown | 186 | 43.1 | stale-rot | - | - |
| frontend-design | unknown | 42 | 43.1 | stale-rot | - | - |
| geox-basin-interpreter | unknown | 89 | 17.5 | - | - | - |
| godel-humility-lock | 1.0.0 | 91 | 5.9 | - | - | - |
| replicate-models | unknown | 74 | 8.9 | - | - | - |
| replicate-prompting | unknown | 202 | 8.9 | - | - | - |
| sandbox-sdk | unknown | 177 | 43.1 | stale-rot | - | - |
| skill-creator | unknown | 66 | 17.5 | - | - | - |
| skill-trigger-linter | unknown | 81 | 17.5 | - | - | - |
| web-perf | unknown | 201 | 43.1 | stale-rot | - | - |
| workers-best-practices | unknown | 127 | 43.1 | stale-rot | - | - |
| wrangler | unknown | 922 | 43.1 | stale-rot, prompt-bloat | - | - |
| mcp-unified | "2.1.0" | 281 | 16.2 | doc-rot | /root/arifOS-pr325/, /root/docker-compose.yml | - |
| site-architecture | "2.1.0" | 208 | 26.1 | - | - | - |
| "imagegen" | unknown | 356 | 10.5 | prompt-bloat | - | - |
| "openai-docs" | unknown | 167 | 10.5 | - | - | - |
| plugin-creator | unknown | 243 | 10.5 | - | - | - |
| skill-creator | unknown | 416 | 10.5 | prompt-bloat | - | - |
| skill-installer | unknown | 58 | 10.5 | - | - | - |
| a2a-agentic-template | unknown | 64 | 17.3 | - | - | - |
| aaa-benchmark | unknown | 181 | 16.5 | - | - | - |
| aaa-speech-protocol | 1.0.0 | 161 | 17.8 | - | - | - |
| agent-email-inbound-protocol | 0.4.0 | 211 | 4.3 | doc-rot | /root/email_agent.pause, /root/email_agent.abort | - |
| agentic-autonomy-bands | 1.1.0 | 149 | 6.2 | - | - | - |
| agentic-foundations | 1.0.0 | 56 | 12.4 | - | - | - |
| arif-fazil-essays-watcher | 0.1.0 | 113 | 6.0 | doc-rot | /root/.hermes/skills/agentic/arif-fazil-essays-watcher/scripts/watch.py, /root/.hermes/skills/agentic/arif-fazil-essays-watcher/state/cron.log, /root/arif-sites/sites/arif-fazil.com/src/data/essays/99-test-essay.ts … | - |
| arif-sites-deploy | "2026.05.21" | 183 | 17.8 | - | - | - |
| arifos-mcp-humility-patch | 1.0.0 | 263 | 5.4 | doc-rot | /root/arifOS/docs/protocols/CONSTITUTIONAL_HUMILITY_PROTOCOL.md, /root/arifOS/contracts/humility.py | - |
| breaking-news-policy | 1.0.0 | 89 | 17.7 | - | - | - |
| codebase-inspection | 1.0.0 | 116 | 32.3 | stale-rot | - | - |
| docker-management | 1.0.0 | 281 | 17.3 | - | - | - |
| federation-a2a-template | 1.0 | 120 | 17.3 | - | - | - |
| github-auth | 1.1.0 | 247 | 32.3 | stale-rot | - | - |
| github-code-review | 1.1.0 | 481 | 32.3 | stale-rot, prompt-bloat | - | - |
| github-issues | 1.1.0 | 370 | 32.3 | stale-rot, prompt-bloat | - | - |
| github-pr-workflow | 1.1.0 | 367 | 32.3 | stale-rot, prompt-bloat | - | - |
| github-repo-management | 1.1.0 | 516 | 32.3 | stale-rot, prompt-bloat | - | - |
| hermes-audit-framework | unknown | 101 | 17.3 | doc-rot | /root/HERMES/skills-archive/ | - |
| kanban-orchestrator | 3.0.0 | 189 | 17.8 | - | - | - |
| kanban-worker | 2.0.0 | 184 | 17.8 | - | - | - |
| l3-feed-seal-toolkit | unknown | 88 | 9.0 | doc-rot | /root/.hermes/cron/seals/l3-feed-*.json, /root/.hermes/cron/seals/l3-feed- | - |
| malaysia-public-figure-research | 1.0.0 | 50 | 17.7 | - | - | - |
| mcp-server-forge | unknown | 185 | 6.5 | doc-rot | /root/.arifos/agents/opencode/*mcp*.json, /root/.aforge/*.json, /root/.opencode/*.json | - |
| qdrant-vector-search | 1.0.0 | 497 | 5.6 | prompt-bloat | - | - |
| node-inspect-debugger | 1.0.0 | 319 | 32.3 | stale-rot, prompt-bloat | - | - |
| peer-probe-monitor | 1.0.0 | 107 | 2.6 | doc-rot | /root/.hermes/skills/devops/peer-probe-monitor/references/openclaw-compromise-history.md | - |
| python-debugpy | 1.0.0 | 375 | 32.3 | stale-rot, prompt-bloat | - | - |
| response-rating | 0.1.0 | 143 | 6.0 | doc-rot | /root/.hermes/skills/agentic/response-rating/scripts/rate_capture.py | - |
| sovereign-ignition-protocol | 2.0 | 110 | 6.3 | - | - | - |
| sovereign-session-binding | 1.0 | 167 | 5.7 | - | - | - |
| telegram-group-contexts | unknown | 56 | 17.3 | - | - | - |
| tree777-telegram-bot-token-isolation | 1.3.0 | 390 | 17.8 | prompt-bloat | - | - |
| tree777-telegram-health-probe | 1.0.0 | 142 | 17.8 | doc-rot | /root/.hermes/scripts/telegram-health-probe.sh, /root/.hermes/logs/telegram-health.log, /root/.hermes/scripts/telegram-health-probe.sh | - |
| well-autonomous-sleep-recursive-improvement | unknown | 141 | 5.5 | doc-rot | /root/.hermes/skills/vitality-check-cron/references/well-autonomous-sleep.md | - |
| writing-plans | 1.1.0 | 297 | 32.3 | stale-rot | - | - |
| federation-engineering-prep | 1.0.0 | 224 | 0.4 | - | - | - |
| _template | 1.0.0 | 68 | 17.8 | - | - | - |
| A3 Self-Test (Awareness-Authority-Auditability) | "1.0.0" | 184 | 0.3 | doc-rot | /root/.hermes/skills/a3-selftest/scripts/a3_audit.sh, /root/.hermes/skills/a3-selftest/scripts/a3_audit_all.sh, /root/.hermes/skills/a3-selftest/scripts/a3_audit.sh … | - |
| AAA Agentic Governance (AAA-Cockpit, canonical) | "3.0.0" | 306 | 0.3 | prompt-bloat | - | - |
| memory-architecture-audit | 1.0.0 | 146 | 3.0 | - | - | - |
| recursive-improve | 0.1.0 | 231 | 1.1 | - | - | - |
| arifOS-agentic-spine | 1.0.0 | 90 | 1.5 | - | - | - |
| arifos-agentic-spine | 1.0.0 | 22 | 0.0 | - | - | - |
| budget-governor | 1.0.0 | 97 | 12.4 | - | - | - |
| constitutional-policy-engine | 2.0.0 | 292 | 0.5 | - | - | - |
| human-escalation-gate | 1.0.0 | 105 | 12.4 | - | - | - |
| output-validator | 1.0.0 | 85 | 12.4 | - | - | - |
| rag-grounding | 1.0.0 | 81 | 12.4 | - | - | - |
| replay-and-eval-harness | 1.0.0 | 97 | 12.4 | - | - | - |
| retry-replan-engine | 1.0.0 | 106 | 12.4 | - | - | - |
| semantic-cache | 1.0.0 | 92 | 12.4 | - | - | - |
| tiered-memory | 2.2.0 | 167 | 0.3 | - | - | - |
| tool-risk-classifier | 1.0.0 | 102 | 12.4 | - | - | - |
| arifos | 1.0.0 | 105 | 1.5 | - | - | - |
| arifos-constitutional-patch-authoring | 1.0.0 | 230 | 4.5 | doc-rot | /root/arifOS/docs/protocols/CONSTITUTIONAL_HUMILITY_PROTOCOL.md, /root/arifOS/contracts/humility.py | - |
| arifos-model-registry | 1.0.0 | 361 | 10.5 | prompt-bloat | - | - |
| arifos-symbolic-overheat-to-canon-recovery | unknown | 131 | 1.3 | doc-rot | /root/WELL/GENESIS/010_*.md, /root/arifOS/static/arifos/theory/000/AI_PERSONA_LOCK.md, /root/arifOS/static/arifos/theory/000/HUMAN_PERSONA_LOCK.md | - |
| autonomous-governed-execution | 1.0.0 | 304 | 3.0 | doc-rot, prompt-bloat | /root/arifOS/docs/DSG.md, /root/.hermes/skills/multimodal/{audio-ingest,multimodal-ingest,multimodal-respond}/SKILL.md, /root/.** | - |
| claim-heavy-essay-audit | 1.0.0 | 556 | 0.1 | doc-rot, prompt-bloat | /root/.hermes/cache/documents/doc_01fc6567e21d_*.md | - |
| constitutional-humility | 1.0.0 | 212 | 0.3 | - | - | - |
| evidence-envelope-pipeline | 1.0.0 | 238 | 6.6 | - | - | - |
| arifos-f13-substrate-binding | 1.0.0 | 305 | 5.0 | doc-rot, prompt-bloat | /root/AAA/skills/*/SKILL.md, /root/VAULT999/F13_, /root/000/SOVEREIGN/F13_ … | - |
| arifos-forge-vs-ask | unknown | 210 | 5.5 | doc-rot | /root/GEOX/ | - |
| arifos-recall | 1.1.0 | 808 | 16.5 | prompt-bloat | - | - |
| arif-rootkey | 1.1.0 | 288 | 5.7 | - | - | - |
| arifos-skill-self-audit-gate | 0.1.0-draft | 190 | 2.6 | - | - | - |
| sovereign-ignition | 1.0 | 120 | 5.6 | - | - | - |
| autonomous-ai-agents | 1.0.0 | 74 | 1.5 | - | - | - |
| agentic-architecture | 1.0.0 | 276 | 4.0 | - | - | - |
| claude-code | 2.2.0 | 746 | 8.5 | prompt-bloat | - | - |
| codex | 1.0.0 | 149 | 1.2 | - | - | - |
| hermes-agent | 2.2.0 | 1274 | 11.1 | doc-rot, prompt-bloat | /root/GEOX/, /root/arifOS/CONTEXT.md | - |
| kanban-codex-lane | 1.0.0 | 277 | 17.3 | - | - | - |
| opencode | 1.2.0 | 424 | 5.6 | prompt-bloat | - | - |
| creative | 1.0.0 | 153 | 1.5 | - | - | - |
| architecture-diagram | 1.0.0 | 148 | 32.3 | stale-rot | - | - |
| ascii-art | 4.0.0 | 322 | 32.3 | stale-rot, prompt-bloat | - | - |
| ascii-video | unknown | 241 | 32.3 | stale-rot | - | - |
| baoyu-article-illustrator | 1.57.0 | 207 | 17.3 | - | - | - |
| baoyu-comic | 1.56.1 | 247 | 32.3 | stale-rot | - | - |
| baoyu-infographic | 1.56.1 | 237 | 32.3 | stale-rot | - | - |
| claude-design | 1.0.0 | 661 | 5.5 | prompt-bloat | - | - |
| comfyui | 5.1.0 | 612 | 26.2 | prompt-bloat | - | - |
| ideation | 1.0.0 | 152 | 32.3 | stale-rot | - | - |
| design-md | 1.0.0 | 199 | 32.3 | stale-rot | - | - |
| excalidraw | 1.0.0 | 199 | 32.3 | stale-rot | - | - |
| humanizer | 2.5.1 | 578 | 32.3 | stale-rot, prompt-bloat | - | - |
| image-gen-recursive | 0.1.0 | 144 | 5.9 | doc-rot | /root/.hermes/memory/image-gen/YYYY-MM-DD/, /root/.hermes/memory/image-gen/templates.jsonl, /root/.hermes/memory/image-gen/templates.jsonl | - |
| manim-video | 1.0.0 | 269 | 32.3 | stale-rot | - | - |
| p5js | 1.0.0 | 556 | 32.3 | stale-rot, prompt-bloat | - | - |
| pixel-art | 2.0.0 | 218 | 32.3 | stale-rot | - | - |
| popular-web-designs | 1.0.0 | 214 | 32.3 | stale-rot | - | - |
| pretext | 1.0.0 | 220 | 32.3 | stale-rot | - | - |
| sketch | 1.0.0 | 218 | 32.3 | stale-rot | - | - |
| songwriting-and-ai-music | unknown | 287 | 32.3 | stale-rot | - | - |
| touchdesigner-mcp | 1.1.0 | 356 | 32.3 | stale-rot, prompt-bloat | - | - |
| devops | 1.0.0 | 159 | 0.4 | - | - | - |
| arif-federation-ops | 1.4.0 | 207 | 0.4 | doc-rot | /root/AAA/agents/{opencode,kimi-code}/skills/ | - |
| arif-site-content | unknown | 285 | 1.7 | doc-rot | /root/.hermes/cache/screenshots/browser_screenshot_ | - |
| arifos-agent-landscape | unknown | 177 | 5.5 | doc-rot | /root/.openclaw/workspace/agents/{hermes-asi,maxhermes}/, /root/AAA/agents/*, /root/.hermes/** … | - |
| arifos-health-probe | unknown | 540 | 7.2 | prompt-bloat | - | - |
| inference-sh-cli | 1.0.0 | 156 | 25.6 | - | - | - |
| composio-bridge-ops | 1.0.0 | 259 | 0.3 | doc-rot | /root/AAA/VAULT999/drafts/email_to_ismail_2026-06-09.md | - |
| delta-logger | 1.0.0 | 141 | 5.5 | - | - | - |
| docker-management | 1.0.0 | 408 | 21.5 | prompt-bloat | - | - |
| dynamic-state-truth | unknown | 518 | 0.3 | doc-rot, prompt-bloat | /root/.openclaw/workspace/bots/.**, /root/.hermes/audit/foo.jsonl, /root/HERMES/audit/foo.jsonl … | - |
| epistemic-conventions | 1.1.0 | 150 | 0.3 | - | - | - |
| federation-canon-reclaim | 1.0.0 | 134 | 5.5 | doc-rot | /root/AAA/agents/* | - |
| federation-engineering-prep | 1.0.0 | 224 | 0.5 | - | - | - |
| federation-entropy-audit | 1.1.0 | 290 | 1.3 | doc-rot | /root/HERMES/sessions_archive_YYYY-MM-DD, /root/HERMES/sessions/session_YYYYMMDD_old*.json, /root/HERMES/sessions_archive_YYYY-MM-DD/ … | - |
| federation-runtime-audit | 1.1.0 | 745 | 7.5 | doc-rot, prompt-bloat | /root/{arifOS,AAA,A-FORGE}/.git/hooks/pre-push, /root/arifOS/arifosmcp/runtime/rest_routes.py | - |
| hermes-cron-job-repair | unknown | 413 | 0.3 | doc-rot, prompt-bloat | /root/.hermes/cron/jobs.json.bak-$TS, /root/.hermes/cron/jobs.json.bak-{datetime.now(, /root/.hermes/cache/forge-backups/crontab.bak-$TS.txt … | - |
| kanban-playbook | 1.0.0 | 398 | 5.0 | prompt-bloat | - | - |
| mcp-boot-failure-diagnosis | 1.0.0 | 180 | 5.7 | doc-rot | /root/.cache/ms-playwright | - |
| mcp-semantic-affordance-discipline | unknown | 247 | 6.1 | doc-rot | /root/.hermes/youtube_cookies.txt, /root/.hermes/youtube_cookies.txt | - |
| memory-hygiene | 1.0.0 | 331 | 1.1 | doc-rot, prompt-bloat | /root/memory/YYYY-MM-DD.md, /root/HERMES/sessions/session_*.json, /root/HERMES/sessions_archive_YYYY-MM-DD … | - |
| openclaw-doctor-recipes | 1.1.0 | 485 | 0.3 | doc-rot, prompt-bloat | /root/arifOS/core/floors.py, /root/arifOS/core/floors.py|/root/arifOS/arifosmcp/runtime/fiqh_of_floors.py|g | - |
| python-tool-isolation | unknown | 100 | 6.5 | doc-rot | /root/.hermes/google_oauth_pending.json | - |
| supabase-db-operations | 0.1.0 | 269 | 13.1 | - | - | - |
| supabase-mcp-wiring | 1.0.0 | 255 | 5.8 | - | - | - |
| telegram-bot-security | 1.0.0 | 92 | 2.5 | - | - | - |
| vault999-repair-procedure | unknown | 190 | 7.6 | - | - | - |
| watchers | 1.1.0 | 123 | 2.5 | - | - | - |
| webhook-subscriptions | 1.1.0 | 204 | 32.3 | stale-rot | - | - |
| dogfood | 1.0.0 | 167 | 24.2 | - | - | - |
| dream-engine | 1.0.0 | 215 | 0.5 | doc-rot | /root/.hermes/cron/output/dream-engine/run_$(date | - |
| email | 1.0.0 | 66 | 1.5 | - | - | - |
| agent-email-a2a-protocol | 0.4.0 | 321 | 3.0 | doc-rot, prompt-bloat | /root/email_agent.pause, /root/email_agent.abort | - |
| agentmail | 1.0.0 | 126 | 17.3 | - | - | - |
| himalaya | 1.1.0 | 319 | 24.5 | prompt-bloat | - | - |
| fff-loop-protocol | 1.0.1 | 173 | 3.0 | - | - | - |
| github-workflow | 1.0.0 | 2099 | 5.0 | prompt-bloat | - | - |
| fitness-nutrition | 1.0.0 | 256 | 24.1 | - | - | - |
| hermes-human-life | 1.0.0 | 97 | 1.0 | - | - | - |
| briefing-system | 1.0.0 | 341 | 2.7 | doc-rot, prompt-bloat | /root/arifOS/arifosmcp/sessions/hermes-briefings/[DATE, /root/.hermes/feedback/[DATE | - |
| event-calendar-research | 2.0.0 | 233 | 0.3 | doc-rot | /root/arifOS/arifosmcp/sessions/hermes-briefings/arif-events-YYYY-MM-DD.ics, /root/arifOS/arifosmcp/sessions/hermes-briefings/arif-events-YYYY-MM-DD.ics, /root/arifOS/arifosmcp/sessions/hermes-briefings/arif-events-*.ics | - |
| wealth-site-publish | 1.0.0 | 160 | 0.9 | doc-rot | /root/arifOS/arifosmcp/sessions/hermes-briefings/[DATE | - |
| mcp | 1.0.0 | 78 | 1.5 | - | - | - |
| arif-os-mcp-tool-authoring | 0.2.0 | 501 | 5.1 | doc-rot, prompt-bloat | /root/.arifos/agents/opencode/*mcp*.json, /root/.aforge/*.json, /root/.opencode/*.json | - |
| fastmcp | unknown | 163 | 16.2 | - | - | - |
| mcporter | 1.1.0 | 262 | 16.1 | doc-rot | /root/.cache/ms-playwright, /root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome, /root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome … | - |
| native-mcp | 1.0.0 | 422 | 16.0 | prompt-bloat | - | - |
| youtube-metabolism | 2.0.0 | 374 | 5.3 | prompt-bloat | - | - |
| mlops | 1.0.0 | 139 | 1.5 | - | - | - |
| aaa-constitutional-benchmark | 2026-05-27 | 186 | 13.1 | - | - | - |
| chroma | 1.0.0 | 410 | 25.6 | prompt-bloat | - | - |
| evaluating-llms-harness | 1.0.0 | 498 | 32.3 | stale-rot, prompt-bloat | - | - |
| weights-and-biases | 1.0.0 | 594 | 32.3 | stale-rot, prompt-bloat | - | - |
| huggingface-hub | 1.0.0 | 157 | 16.5 | - | - | - |
| llama-cpp | 2.1.2 | 249 | 32.3 | stale-rot | - | - |
| obliteratus | 2.0.0 | 342 | 32.3 | stale-rot, prompt-bloat | - | - |
| serving-llms-vllm | 1.0.0 | 372 | 32.3 | stale-rot, prompt-bloat | - | - |
| audiocraft-audio-generation | 1.0.0 | 568 | 32.3 | stale-rot, prompt-bloat | - | - |
| segment-anything-model | 1.0.0 | 506 | 32.3 | stale-rot, prompt-bloat | - | - |
| ollama-runtime-health | 0.1.0 | 156 | 16.6 | - | - | - |
| qdrant-vector-search | 1.0.0 | 497 | 25.6 | prompt-bloat | - | - |
| dspy | 1.0.0 | 594 | 32.3 | stale-rot, prompt-bloat | - | - |
| huggingface-accelerate | 1.0.0 | 336 | 17.3 | prompt-bloat | - | - |
| peft-fine-tuning | 1.0.0 | 435 | 17.3 | prompt-bloat | - | - |
| whisper | 1.0.0 | 321 | 25.5 | prompt-bloat | - | - |
| multimodal | 1.0.0 | 75 | 1.5 | - | - | - |
| audio-ingest | 1.0.0 | 66 | 4.6 | doc-rot | /root/.hermes/cache/audio-ingest.log.jsonl | - |
| multimodal-ingest | 1.0.0 | 145 | 2.6 | doc-rot | /root/.hermes/cache/documents/doc_ | - |
| multimodal-respond | 1.0.0 | 68 | 4.6 | doc-rot | /root/.hermes/audio_cache/{ts( | - |
| vision-direct | 1.0.1 | 179 | 0.2 | - | - | - |
| news-analysis | 1.0.0 | 132 | 1.0 | - | - | - |
| news-analysis-protocol | 1.0.0 | 548 | 1.0 | prompt-bloat | - | - |
| news-brief-integrity | 2.0.0 | 244 | 1.0 | - | - | - |
| world-news-analysis | 1.0.0 | 373 | 1.0 | prompt-bloat | - | - |
| orthodoxy-auditor | 1.0.0 | 326 | 3.0 | doc-rot, prompt-bloat | /root/backups/AGENTS.md | - |
| paste-intent-classifier | unknown | 175 | 1.2 | doc-rot | /root/.hermes/cache/pastes/, /root/.hermes/cache/pastes/{ts}.txt, /root/.hermes/cache/pastes/20260607-042831.txt | - |
| personal | 1.0.0 | 62 | 1.0 | - | - | - |
| arif-wound-architecture | unknown | 61 | 9.0 | - | - | - |
| emotional-processing-protocol | unknown | 93 | 17.8 | doc-rot | /root/sessions/YYYY-MM-DD-execution-log.md | - |
| personal-archive-mapper | 1.0.0 | 267 | 0.2 | - | - | - |
| vitality-check-cron | unknown | 117 | 7.6 | - | - | - |
| productivity | 1.0.0 | 136 | 1.5 | - | - | - |
| airtable | 1.1.0 | 229 | 1.2 | - | - | - |
| canvas | 1.0.0 | 98 | 17.3 | - | - | - |
| composio-integration | 1.7.0 | 516 | 3.4 | doc-rot, prompt-bloat | /root/.secrets/env/*.env, /root/.secrets/tokens/telegram-*, /root/.local/share/opencode/log/*.log | - |
| flight-status | 1.1.0 | 184 | 9.2 | - | - | - |
| google-workspace | 1.1.0 | 421 | 8.2 | prompt-bloat | - | - |
| here.now | 1.15.3 | 217 | 17.3 | - | - | - |
| linear | 1.0.0 | 380 | 32.3 | stale-rot, prompt-bloat | - | - |
| maps | 1.2.0 | 195 | 32.3 | stale-rot | - | - |
| memento-flashcards | 1.0.0 | 324 | 17.3 | prompt-bloat | - | - |
| nano-pdf | 1.0.0 | 52 | 32.3 | stale-rot | - | - |
| notion | 2.0.0 | 448 | 1.2 | prompt-bloat | - | - |
| ocr-and-documents | 2.3.0 | 172 | 32.3 | stale-rot | - | - |
| pdf-handwriting-overlay | 1.0.0 | 363 | 9.1 | prompt-bloat | - | - |
| powerpoint | unknown | 237 | 32.3 | stale-rot | - | - |
| shop-app | 0.0.28 | 340 | 17.3 | prompt-bloat | - | - |
| shopify | 1.0.0 | 373 | 17.3 | prompt-bloat | - | - |
| siyuan | 1.0.0 | 298 | 17.3 | - | - | - |
| teams-meeting-pipeline | 1.1.0 | 116 | 1.2 | - | - | - |
| telephony | 1.0.0 | 418 | 17.3 | prompt-bloat | - | - |
| research | 1.0.0 | 135 | 1.5 | - | - | - |
| arxiv | 1.0.0 | 282 | 32.3 | stale-rot | - | - |
| blogwatcher | 2.0.0 | 137 | 32.3 | stale-rot | - | - |
| darwinian-evolver | 0.1.0 | 199 | 6.0 | - | - | - |
| duckduckgo-search | 1.3.1 | 238 | 11.6 | - | - | - |
| gitingest-recipe | unknown | 127 | 6.5 | - | - | - |
| llm-wiki | 2.1.0 | 578 | 26.4 | doc-rot, prompt-bloat | /root/AAA/SKILLS_INDEX.md | - |
| malaysia-political-media-research | 1.0.0 | 237 | 5.2 | - | - | - |
| malaysia-state-election-forecast | 1.1.0 | 273 | 4.4 | - | - | - |
| parallel-cli | 1.1.0 | 391 | 25.5 | prompt-bloat | - | - |
| polymarket | 1.0.0 | 77 | 32.3 | stale-rot | - | - |
| repo-eureka | unknown | 241 | 6.5 | - | - | - |
| repo-pattern-transplantation | unknown | 121 | 23.9 | - | - | - |
| research-paper-writing | 1.1.0 | 2377 | 32.3 | stale-rot, prompt-bloat | - | - |
| searxng-search | 1.0.0 | 268 | 10.5 | - | - | - |
| searxng-search | 1.0.0 | 212 | 17.3 | - | - | - |
| sherlock | 1.0.0 | 193 | 17.3 | - | - | - |
| web-pentest | unknown | 333 | 17.3 | prompt-bloat | - | - |
| session-seal-triage | unknown | 228 | 4.5 | - | - | - |
| software-development | 1.0.0 | 107 | 1.0 | - | - | - |
| agent-context-forge-loop | unknown | 274 | 4.5 | doc-rot | /root/.hermes/cache/forge-backups/{ts}/SOUL.md, /root/.hermes/X, /root/HERMES/X | - |
| constitutional-expository-forge | 1.1.0 | 366 | 5.2 | prompt-bloat | - | - |
| dual-artifact-publication | 1.1.0 | 309 | 5.2 | prompt-bloat | - | - |
| engineering-prompt-forge | 1.0.0 | 328 | 0.5 | prompt-bloat | - | - |
| fabrication-prevention | 1.2.0 | 232 | 1.3 | - | - | - |
| hermes-agent-skill-authoring | 1.0.0 | 165 | 6.0 | - | - | - |
| hermes-s6-container-supervision | 1.0.0 | 176 | 17.3 | - | - | - |
| plan | 2.0.0 | 338 | 6.0 | prompt-bloat | - | - |
| requesting-code-review | 2.0.0 | 280 | 6.0 | - | - | - |
| simplify-code | 1.0.0 | 175 | 1.2 | - | - | - |
| spike | 1.0.0 | 211 | 24.2 | - | - | - |
| subagent-driven-development | 1.1.0 | 352 | 32.3 | stale-rot, prompt-bloat | - | - |
| systematic-debugging | 1.2.0 | 482 | 3.0 | prompt-bloat | - | - |
| test-driven-development | 1.1.0 | 364 | 0.6 | prompt-bloat | - | - |
| sovereign-ai-redteam | 2.0.0 | 533 | 0.0 | prompt-bloat | - | - |
| substrate-gate-telegram | 1 | 121 | 1.7 | doc-rot | /root/.hermes/cache/substrate-gate/audit.jsonl, /root/.hermes/cache/substrate-gate/audit.jsonl | - |
| telegram-mode-guards | unknown | 312 | 2.6 | prompt-bloat | - | - |

## Collision / Trigger Overlap Risk

| Skill A | Skill B | Jaccard |
|---------|---------|---------|
| docker-management | docker-management | 1.0 |
| qdrant-vector-search | qdrant-vector-search | 1.0 |
| writing-plans | plan | 0.44 |
| federation-engineering-prep | federation-engineering-prep | 1.0 |
| claude-code | codex | 0.43 |
| claude-code | opencode | 0.43 |
| codex | opencode | 0.43 |
| searxng-search | searxng-search | 1.0 |

## Detailed Findings

### compare-models

- Path: `/root/.agents/skills/_archive/merged-2026-06-03/compare-models/SKILL.md`
- Version: unknown | Lines: 47 | Age: 43.1 days
- Rot tags: stale-rot

### find-models

- Path: `/root/.agents/skills/_archive/merged-2026-06-03/find-models/SKILL.md`
- Version: unknown | Lines: 47 | Age: 43.1 days
- Rot tags: stale-rot

### prompt-images

- Path: `/root/.agents/skills/_archive/merged-2026-06-03/prompt-images/SKILL.md`
- Version: unknown | Lines: 200 | Age: 43.1 days
- Rot tags: stale-rot

### prompt-videos

- Path: `/root/.agents/skills/_archive/merged-2026-06-03/prompt-videos/SKILL.md`
- Version: unknown | Lines: 334 | Age: 43.1 days
- Rot tags: stale-rot, prompt-bloat

### run-models

- Path: `/root/.agents/skills/_archive/merged-2026-06-03/run-models/SKILL.md`
- Version: unknown | Lines: 69 | Age: 43.1 days
- Rot tags: stale-rot

### agents-sdk

- Path: `/root/.agents/skills/agents-sdk/SKILL.md`
- Version: unknown | Lines: 221 | Age: 43.1 days
- Rot tags: stale-rot

### arifos-observability

- Path: `/root/.agents/skills/arifos-observability/SKILL.md`
- Version: unknown | Lines: 72 | Age: 17.5 days
- Rot tags: doc-rot
- Broken paths: /root/.agents/telemetry/

### cloudflare

- Path: `/root/.agents/skills/cloudflare/SKILL.md`
- Version: unknown | Lines: 245 | Age: 43.1 days
- Rot tags: stale-rot

### cloudflare-email-service

- Path: `/root/.agents/skills/cloudflare-email-service/SKILL.md`
- Version: unknown | Lines: 103 | Age: 43.1 days
- Rot tags: stale-rot

### durable-objects

- Path: `/root/.agents/skills/durable-objects/SKILL.md`
- Version: unknown | Lines: 186 | Age: 43.1 days
- Rot tags: stale-rot

### frontend-design

- Path: `/root/.agents/skills/frontend-design/SKILL.md`
- Version: unknown | Lines: 42 | Age: 43.1 days
- Rot tags: stale-rot

### sandbox-sdk

- Path: `/root/.agents/skills/sandbox-sdk/SKILL.md`
- Version: unknown | Lines: 177 | Age: 43.1 days
- Rot tags: stale-rot

### web-perf

- Path: `/root/.agents/skills/web-perf/SKILL.md`
- Version: unknown | Lines: 201 | Age: 43.1 days
- Rot tags: stale-rot

### workers-best-practices

- Path: `/root/.agents/skills/workers-best-practices/SKILL.md`
- Version: unknown | Lines: 127 | Age: 43.1 days
- Rot tags: stale-rot

### wrangler

- Path: `/root/.agents/skills/wrangler/SKILL.md`
- Version: unknown | Lines: 922 | Age: 43.1 days
- Rot tags: stale-rot, prompt-bloat

### mcp-unified

- Path: `/root/.arifos/agents/kimi/skills/mcp-unified/SKILL.md`
- Version: "2.1.0" | Lines: 281 | Age: 16.2 days
- Rot tags: doc-rot
- Broken paths: /root/arifOS-pr325/, /root/docker-compose.yml

### "imagegen"

- Path: `/root/.codex/skills/.system/imagegen/SKILL.md`
- Version: unknown | Lines: 356 | Age: 10.5 days
- Rot tags: prompt-bloat

### skill-creator

- Path: `/root/.codex/skills/.system/skill-creator/SKILL.md`
- Version: unknown | Lines: 416 | Age: 10.5 days
- Rot tags: prompt-bloat

### agent-email-inbound-protocol

- Path: `/root/HERMES/skills/.archive/agent-email-inbound-protocol/SKILL.md`
- Version: 0.4.0 | Lines: 211 | Age: 4.3 days
- Rot tags: doc-rot
- Broken paths: /root/email_agent.pause, /root/email_agent.abort

### arif-fazil-essays-watcher

- Path: `/root/HERMES/skills/.archive/arif-fazil-essays-watcher/SKILL.md`
- Version: 0.1.0 | Lines: 113 | Age: 6.0 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/skills/agentic/arif-fazil-essays-watcher/scripts/watch.py, /root/.hermes/skills/agentic/arif-fazil-essays-watcher/state/cron.log, /root/arif-sites/sites/arif-fazil.com/src/data/essays/99-test-essay.ts, /root/.hermes/skills/agentic/arif-fazil-essays-watcher/scripts/watch.py, /root/arif-sites/sites/arif-fazil.com/src/data/essays/99-test-essay.ts

### arifos-mcp-humility-patch

- Path: `/root/HERMES/skills/.archive/arifos-mcp-humility-patch/SKILL.md`
- Version: 1.0.0 | Lines: 263 | Age: 5.4 days
- Rot tags: doc-rot
- Broken paths: /root/arifOS/docs/protocols/CONSTITUTIONAL_HUMILITY_PROTOCOL.md, /root/arifOS/contracts/humility.py

### codebase-inspection

- Path: `/root/HERMES/skills/.archive/codebase-inspection/SKILL.md`
- Version: 1.0.0 | Lines: 116 | Age: 32.3 days
- Rot tags: stale-rot

### github-auth

- Path: `/root/HERMES/skills/.archive/github-auth/SKILL.md`
- Version: 1.1.0 | Lines: 247 | Age: 32.3 days
- Rot tags: stale-rot

### github-code-review

- Path: `/root/HERMES/skills/.archive/github-code-review/SKILL.md`
- Version: 1.1.0 | Lines: 481 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### github-issues

- Path: `/root/HERMES/skills/.archive/github-issues/SKILL.md`
- Version: 1.1.0 | Lines: 370 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### github-pr-workflow

- Path: `/root/HERMES/skills/.archive/github-pr-workflow/SKILL.md`
- Version: 1.1.0 | Lines: 367 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### github-repo-management

- Path: `/root/HERMES/skills/.archive/github-repo-management/SKILL.md`
- Version: 1.1.0 | Lines: 516 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### hermes-audit-framework

- Path: `/root/HERMES/skills/.archive/hermes-audit-framework/SKILL.md`
- Version: unknown | Lines: 101 | Age: 17.3 days
- Rot tags: doc-rot
- Broken paths: /root/HERMES/skills-archive/

### l3-feed-seal-toolkit

- Path: `/root/HERMES/skills/.archive/l3-feed-seal-toolkit/SKILL.md`
- Version: unknown | Lines: 88 | Age: 9.0 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/cron/seals/l3-feed-*.json, /root/.hermes/cron/seals/l3-feed-

### mcp-server-forge

- Path: `/root/HERMES/skills/.archive/mcp-server-forge/SKILL.md`
- Version: unknown | Lines: 185 | Age: 6.5 days
- Rot tags: doc-rot
- Broken paths: /root/.arifos/agents/opencode/*mcp*.json, /root/.aforge/*.json, /root/.opencode/*.json

### qdrant-vector-search

- Path: `/root/HERMES/skills/.archive/mlops-qdrant-duplicate/SKILL.md`
- Version: 1.0.0 | Lines: 497 | Age: 5.6 days
- Rot tags: prompt-bloat

### node-inspect-debugger

- Path: `/root/HERMES/skills/.archive/node-inspect-debugger/SKILL.md`
- Version: 1.0.0 | Lines: 319 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### peer-probe-monitor

- Path: `/root/HERMES/skills/.archive/peer-probe-monitor/SKILL.md`
- Version: 1.0.0 | Lines: 107 | Age: 2.6 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/skills/devops/peer-probe-monitor/references/openclaw-compromise-history.md

### python-debugpy

- Path: `/root/HERMES/skills/.archive/python-debugpy/SKILL.md`
- Version: 1.0.0 | Lines: 375 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### response-rating

- Path: `/root/HERMES/skills/.archive/response-rating/SKILL.md`
- Version: 0.1.0 | Lines: 143 | Age: 6.0 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/skills/agentic/response-rating/scripts/rate_capture.py

### tree777-telegram-bot-token-isolation

- Path: `/root/HERMES/skills/.archive/tree777-telegram-bot-token-isolation/SKILL.md`
- Version: 1.3.0 | Lines: 390 | Age: 17.8 days
- Rot tags: prompt-bloat

### tree777-telegram-health-probe

- Path: `/root/HERMES/skills/.archive/tree777-telegram-health-probe/SKILL.md`
- Version: 1.0.0 | Lines: 142 | Age: 17.8 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/scripts/telegram-health-probe.sh, /root/.hermes/logs/telegram-health.log, /root/.hermes/scripts/telegram-health-probe.sh

### well-autonomous-sleep-recursive-improvement

- Path: `/root/HERMES/skills/.archive/well-autonomous-sleep-recursive-improvement/SKILL.md`
- Version: unknown | Lines: 141 | Age: 5.5 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/skills/vitality-check-cron/references/well-autonomous-sleep.md

### writing-plans

- Path: `/root/HERMES/skills/.archive/writing-plans/SKILL.md`
- Version: 1.1.0 | Lines: 297 | Age: 32.3 days
- Rot tags: stale-rot

### A3 Self-Test (Awareness-Authority-Auditability)

- Path: `/root/HERMES/skills/a3-selftest/SKILL.md`
- Version: "1.0.0" | Lines: 184 | Age: 0.3 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/skills/a3-selftest/scripts/a3_audit.sh, /root/.hermes/skills/a3-selftest/scripts/a3_audit_all.sh, /root/.hermes/skills/a3-selftest/scripts/a3_audit.sh, /root/.hermes/skills/a3-selftest/scripts/a3_audit_all.sh, /root/.hermes/skills/a3-selftest/state/fleet_

### AAA Agentic Governance (AAA-Cockpit, canonical)

- Path: `/root/HERMES/skills/aaa-agentic-governance/SKILL.md`
- Version: "3.0.0" | Lines: 306 | Age: 0.3 days
- Rot tags: prompt-bloat

### arifos-constitutional-patch-authoring

- Path: `/root/HERMES/skills/arifos/arifos-constitutional-patch-authoring/SKILL.md`
- Version: 1.0.0 | Lines: 230 | Age: 4.5 days
- Rot tags: doc-rot
- Broken paths: /root/arifOS/docs/protocols/CONSTITUTIONAL_HUMILITY_PROTOCOL.md, /root/arifOS/contracts/humility.py

### arifos-model-registry

- Path: `/root/HERMES/skills/arifos/arifos-model-registry/SKILL.md`
- Version: 1.0.0 | Lines: 361 | Age: 10.5 days
- Rot tags: prompt-bloat

### arifos-symbolic-overheat-to-canon-recovery

- Path: `/root/HERMES/skills/arifos/arifos-symbolic-overheat-to-canon-recovery/SKILL.md`
- Version: unknown | Lines: 131 | Age: 1.3 days
- Rot tags: doc-rot
- Broken paths: /root/WELL/GENESIS/010_*.md, /root/arifOS/static/arifos/theory/000/AI_PERSONA_LOCK.md, /root/arifOS/static/arifos/theory/000/HUMAN_PERSONA_LOCK.md

### autonomous-governed-execution

- Path: `/root/HERMES/skills/arifos/autonomous-governed-execution/SKILL.md`
- Version: 1.0.0 | Lines: 304 | Age: 3.0 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/arifOS/docs/DSG.md, /root/.hermes/skills/multimodal/{audio-ingest,multimodal-ingest,multimodal-respond}/SKILL.md, /root/.**

### claim-heavy-essay-audit

- Path: `/root/HERMES/skills/arifos/claim-heavy-essay-audit/SKILL.md`
- Version: 1.0.0 | Lines: 556 | Age: 0.1 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/.hermes/cache/documents/doc_01fc6567e21d_*.md

### arifos-f13-substrate-binding

- Path: `/root/HERMES/skills/arifos/f13-substrate-binding/SKILL.md`
- Version: 1.0.0 | Lines: 305 | Age: 5.0 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/AAA/skills/*/SKILL.md, /root/VAULT999/F13_, /root/000/SOVEREIGN/F13_, /root/VAULT999/F13_, /root/000/SOVEREIGN/F13_, /root/VAULT999/*.json, /root/000/SOVEREIGN/*.json

### arifos-forge-vs-ask

- Path: `/root/HERMES/skills/arifos/forge-vs-ask/SKILL.md`
- Version: unknown | Lines: 210 | Age: 5.5 days
- Rot tags: doc-rot
- Broken paths: /root/GEOX/

### arifos-recall

- Path: `/root/HERMES/skills/arifos/recall/SKILL.md`
- Version: 1.1.0 | Lines: 808 | Age: 16.5 days
- Rot tags: prompt-bloat

### claude-code

- Path: `/root/HERMES/skills/autonomous-ai-agents/claude-code/SKILL.md`
- Version: 2.2.0 | Lines: 746 | Age: 8.5 days
- Rot tags: prompt-bloat

### hermes-agent

- Path: `/root/HERMES/skills/autonomous-ai-agents/hermes-agent/SKILL.md`
- Version: 2.2.0 | Lines: 1274 | Age: 11.1 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/GEOX/, /root/arifOS/CONTEXT.md

### opencode

- Path: `/root/HERMES/skills/autonomous-ai-agents/opencode/SKILL.md`
- Version: 1.2.0 | Lines: 424 | Age: 5.6 days
- Rot tags: prompt-bloat

### architecture-diagram

- Path: `/root/HERMES/skills/creative/architecture-diagram/SKILL.md`
- Version: 1.0.0 | Lines: 148 | Age: 32.3 days
- Rot tags: stale-rot

### ascii-art

- Path: `/root/HERMES/skills/creative/ascii-art/SKILL.md`
- Version: 4.0.0 | Lines: 322 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### ascii-video

- Path: `/root/HERMES/skills/creative/ascii-video/SKILL.md`
- Version: unknown | Lines: 241 | Age: 32.3 days
- Rot tags: stale-rot

### baoyu-comic

- Path: `/root/HERMES/skills/creative/baoyu-comic/SKILL.md`
- Version: 1.56.1 | Lines: 247 | Age: 32.3 days
- Rot tags: stale-rot

### baoyu-infographic

- Path: `/root/HERMES/skills/creative/baoyu-infographic/SKILL.md`
- Version: 1.56.1 | Lines: 237 | Age: 32.3 days
- Rot tags: stale-rot

### claude-design

- Path: `/root/HERMES/skills/creative/claude-design/SKILL.md`
- Version: 1.0.0 | Lines: 661 | Age: 5.5 days
- Rot tags: prompt-bloat

### comfyui

- Path: `/root/HERMES/skills/creative/comfyui/SKILL.md`
- Version: 5.1.0 | Lines: 612 | Age: 26.2 days
- Rot tags: prompt-bloat

### ideation

- Path: `/root/HERMES/skills/creative/creative-ideation/SKILL.md`
- Version: 1.0.0 | Lines: 152 | Age: 32.3 days
- Rot tags: stale-rot

### design-md

- Path: `/root/HERMES/skills/creative/design-md/SKILL.md`
- Version: 1.0.0 | Lines: 199 | Age: 32.3 days
- Rot tags: stale-rot

### excalidraw

- Path: `/root/HERMES/skills/creative/excalidraw/SKILL.md`
- Version: 1.0.0 | Lines: 199 | Age: 32.3 days
- Rot tags: stale-rot

### humanizer

- Path: `/root/HERMES/skills/creative/humanizer/SKILL.md`
- Version: 2.5.1 | Lines: 578 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### image-gen-recursive

- Path: `/root/HERMES/skills/creative/image-gen-recursive/SKILL.md`
- Version: 0.1.0 | Lines: 144 | Age: 5.9 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/memory/image-gen/YYYY-MM-DD/, /root/.hermes/memory/image-gen/templates.jsonl, /root/.hermes/memory/image-gen/templates.jsonl

### manim-video

- Path: `/root/HERMES/skills/creative/manim-video/SKILL.md`
- Version: 1.0.0 | Lines: 269 | Age: 32.3 days
- Rot tags: stale-rot

### p5js

- Path: `/root/HERMES/skills/creative/p5js/SKILL.md`
- Version: 1.0.0 | Lines: 556 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### pixel-art

- Path: `/root/HERMES/skills/creative/pixel-art/SKILL.md`
- Version: 2.0.0 | Lines: 218 | Age: 32.3 days
- Rot tags: stale-rot

### popular-web-designs

- Path: `/root/HERMES/skills/creative/popular-web-designs/SKILL.md`
- Version: 1.0.0 | Lines: 214 | Age: 32.3 days
- Rot tags: stale-rot

### pretext

- Path: `/root/HERMES/skills/creative/pretext/SKILL.md`
- Version: 1.0.0 | Lines: 220 | Age: 32.3 days
- Rot tags: stale-rot

### sketch

- Path: `/root/HERMES/skills/creative/sketch/SKILL.md`
- Version: 1.0.0 | Lines: 218 | Age: 32.3 days
- Rot tags: stale-rot

### songwriting-and-ai-music

- Path: `/root/HERMES/skills/creative/songwriting-and-ai-music/SKILL.md`
- Version: unknown | Lines: 287 | Age: 32.3 days
- Rot tags: stale-rot

### touchdesigner-mcp

- Path: `/root/HERMES/skills/creative/touchdesigner-mcp/SKILL.md`
- Version: 1.1.0 | Lines: 356 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### arif-federation-ops

- Path: `/root/HERMES/skills/devops/arif-federation-ops/SKILL.md`
- Version: 1.4.0 | Lines: 207 | Age: 0.4 days
- Rot tags: doc-rot
- Broken paths: /root/AAA/agents/{opencode,kimi-code}/skills/

### arif-site-content

- Path: `/root/HERMES/skills/devops/arif-site-content/SKILL.md`
- Version: unknown | Lines: 285 | Age: 1.7 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/cache/screenshots/browser_screenshot_

### arifos-agent-landscape

- Path: `/root/HERMES/skills/devops/arifos-agent-landscape/SKILL.md`
- Version: unknown | Lines: 177 | Age: 5.5 days
- Rot tags: doc-rot
- Broken paths: /root/.openclaw/workspace/agents/{hermes-asi,maxhermes}/, /root/AAA/agents/*, /root/.hermes/**, /root/.openclaw/workspace/**, /root/.openclaw/workspace/agents/*, /root/AAA/agents/*, /root/AAA/agents/*

### arifos-health-probe

- Path: `/root/HERMES/skills/devops/arifos-health-probe/SKILL.md`
- Version: unknown | Lines: 540 | Age: 7.2 days
- Rot tags: prompt-bloat

### composio-bridge-ops

- Path: `/root/HERMES/skills/devops/composio-bridge-ops/SKILL.md`
- Version: 1.0.0 | Lines: 259 | Age: 0.3 days
- Rot tags: doc-rot
- Broken paths: /root/AAA/VAULT999/drafts/email_to_ismail_2026-06-09.md

### docker-management

- Path: `/root/HERMES/skills/devops/docker-management/SKILL.md`
- Version: 1.0.0 | Lines: 408 | Age: 21.5 days
- Rot tags: prompt-bloat

### dynamic-state-truth

- Path: `/root/HERMES/skills/devops/dynamic-state-truth/SKILL.md`
- Version: unknown | Lines: 518 | Age: 0.3 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/.openclaw/workspace/bots/.**, /root/.hermes/audit/foo.jsonl, /root/HERMES/audit/foo.jsonl, /root/AAA/docs/plans/canonical/, /root/$d/AGENTS.md, /root/$d/AGENTS.md, /root/.hermes/cron/output/dream-engine/run_*.log

### federation-canon-reclaim

- Path: `/root/HERMES/skills/devops/federation-canon-reclaim/SKILL.md`
- Version: 1.0.0 | Lines: 134 | Age: 5.5 days
- Rot tags: doc-rot
- Broken paths: /root/AAA/agents/*

### federation-entropy-audit

- Path: `/root/HERMES/skills/devops/federation-entropy-audit/SKILL.md`
- Version: 1.1.0 | Lines: 290 | Age: 1.3 days
- Rot tags: doc-rot
- Broken paths: /root/HERMES/sessions_archive_YYYY-MM-DD, /root/HERMES/sessions/session_YYYYMMDD_old*.json, /root/HERMES/sessions_archive_YYYY-MM-DD/, /root/SAF/saf-data, /root/SAF, /root/HERMES/sessions/session_*.json, /root/SAF/saf-data/

### federation-runtime-audit

- Path: `/root/HERMES/skills/devops/federation-runtime-audit/SKILL.md`
- Version: 1.1.0 | Lines: 745 | Age: 7.5 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/{arifOS,AAA,A-FORGE}/.git/hooks/pre-push, /root/arifOS/arifosmcp/runtime/rest_routes.py

### hermes-cron-job-repair

- Path: `/root/HERMES/skills/devops/hermes-cron-job-repair/SKILL.md`
- Version: unknown | Lines: 413 | Age: 0.3 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/.hermes/cron/jobs.json.bak-$TS, /root/.hermes/cron/jobs.json.bak-{datetime.now(, /root/.hermes/cache/forge-backups/crontab.bak-$TS.txt, /root/.hermes/cache/forge-backups/crontab.bak-, /root/.hermes/skills/X/probe\.sh$|*/10, /root/.hermes/skills/X/probe.sh|, /root/HERMES/scripts/push_events_to_, /root/.hermes/scripts/foo.py, /root/HERMES/scripts/foo.py

### kanban-playbook

- Path: `/root/HERMES/skills/devops/kanban-playbook/SKILL.md`
- Version: 1.0.0 | Lines: 398 | Age: 5.0 days
- Rot tags: prompt-bloat

### mcp-boot-failure-diagnosis

- Path: `/root/HERMES/skills/devops/mcp-boot-failure-diagnosis/SKILL.md`
- Version: 1.0.0 | Lines: 180 | Age: 5.7 days
- Rot tags: doc-rot
- Broken paths: /root/.cache/ms-playwright

### mcp-semantic-affordance-discipline

- Path: `/root/HERMES/skills/devops/mcp-semantic-affordance-discipline/SKILL.md`
- Version: unknown | Lines: 247 | Age: 6.1 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/youtube_cookies.txt, /root/.hermes/youtube_cookies.txt

### memory-hygiene

- Path: `/root/HERMES/skills/devops/memory-hygiene/SKILL.md`
- Version: 1.0.0 | Lines: 331 | Age: 1.1 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/memory/YYYY-MM-DD.md, /root/HERMES/sessions/session_*.json, /root/HERMES/sessions_archive_YYYY-MM-DD, /root/HERMES/sessions/session_YYYYMMDD_*.json, /root/HERMES/sessions_archive_YYYY-MM-DD/, /root/HERMES/sessions/session_*.json, /root/arifOS/VAULT999/*.jsonl

### openclaw-doctor-recipes

- Path: `/root/HERMES/skills/devops/openclaw-doctor-recipes/SKILL.md`
- Version: 1.1.0 | Lines: 485 | Age: 0.3 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/arifOS/core/floors.py, /root/arifOS/core/floors.py|/root/arifOS/arifosmcp/runtime/fiqh_of_floors.py|g

### python-tool-isolation

- Path: `/root/HERMES/skills/devops/python-tool-isolation/SKILL.md`
- Version: unknown | Lines: 100 | Age: 6.5 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/google_oauth_pending.json

### webhook-subscriptions

- Path: `/root/HERMES/skills/devops/webhook-subscriptions/SKILL.md`
- Version: 1.1.0 | Lines: 204 | Age: 32.3 days
- Rot tags: stale-rot

### dream-engine

- Path: `/root/HERMES/skills/dream-engine/SKILL.md`
- Version: 1.0.0 | Lines: 215 | Age: 0.5 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/cron/output/dream-engine/run_$(date

### agent-email-a2a-protocol

- Path: `/root/HERMES/skills/email/agent-email-a2a-protocol/SKILL.md`
- Version: 0.4.0 | Lines: 321 | Age: 3.0 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/email_agent.pause, /root/email_agent.abort

### himalaya

- Path: `/root/HERMES/skills/email/himalaya/SKILL.md`
- Version: 1.1.0 | Lines: 319 | Age: 24.5 days
- Rot tags: prompt-bloat

### github-workflow

- Path: `/root/HERMES/skills/github/github-workflow/SKILL.md`
- Version: 1.0.0 | Lines: 2099 | Age: 5.0 days
- Rot tags: prompt-bloat

### briefing-system

- Path: `/root/HERMES/skills/hermes-human-life/briefing-system/SKILL.md`
- Version: 1.0.0 | Lines: 341 | Age: 2.7 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/arifOS/arifosmcp/sessions/hermes-briefings/[DATE, /root/.hermes/feedback/[DATE

### event-calendar-research

- Path: `/root/HERMES/skills/hermes-human-life/event-calendar-research/SKILL.md`
- Version: 2.0.0 | Lines: 233 | Age: 0.3 days
- Rot tags: doc-rot
- Broken paths: /root/arifOS/arifosmcp/sessions/hermes-briefings/arif-events-YYYY-MM-DD.ics, /root/arifOS/arifosmcp/sessions/hermes-briefings/arif-events-YYYY-MM-DD.ics, /root/arifOS/arifosmcp/sessions/hermes-briefings/arif-events-*.ics

### wealth-site-publish

- Path: `/root/HERMES/skills/hermes-human-life/wealth-site-publish/SKILL.md`
- Version: 1.0.0 | Lines: 160 | Age: 0.9 days
- Rot tags: doc-rot
- Broken paths: /root/arifOS/arifosmcp/sessions/hermes-briefings/[DATE

### arif-os-mcp-tool-authoring

- Path: `/root/HERMES/skills/mcp/arif-os-mcp-tool-authoring/SKILL.md`
- Version: 0.2.0 | Lines: 501 | Age: 5.1 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/.arifos/agents/opencode/*mcp*.json, /root/.aforge/*.json, /root/.opencode/*.json

### mcporter

- Path: `/root/HERMES/skills/mcp/mcporter/SKILL.md`
- Version: 1.1.0 | Lines: 262 | Age: 16.1 days
- Rot tags: doc-rot
- Broken paths: /root/.cache/ms-playwright, /root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome, /root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome, /root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome

### native-mcp

- Path: `/root/HERMES/skills/mcp/native-mcp/SKILL.md`
- Version: 1.0.0 | Lines: 422 | Age: 16.0 days
- Rot tags: prompt-bloat

### youtube-metabolism

- Path: `/root/HERMES/skills/media/youtube-metabolism/SKILL.md`
- Version: 2.0.0 | Lines: 374 | Age: 5.3 days
- Rot tags: prompt-bloat

### chroma

- Path: `/root/HERMES/skills/mlops/chroma/SKILL.md`
- Version: 1.0.0 | Lines: 410 | Age: 25.6 days
- Rot tags: prompt-bloat

### evaluating-llms-harness

- Path: `/root/HERMES/skills/mlops/evaluation/lm-evaluation-harness/SKILL.md`
- Version: 1.0.0 | Lines: 498 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### weights-and-biases

- Path: `/root/HERMES/skills/mlops/evaluation/weights-and-biases/SKILL.md`
- Version: 1.0.0 | Lines: 594 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### llama-cpp

- Path: `/root/HERMES/skills/mlops/inference/llama-cpp/SKILL.md`
- Version: 2.1.2 | Lines: 249 | Age: 32.3 days
- Rot tags: stale-rot

### obliteratus

- Path: `/root/HERMES/skills/mlops/inference/obliteratus/SKILL.md`
- Version: 2.0.0 | Lines: 342 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### serving-llms-vllm

- Path: `/root/HERMES/skills/mlops/inference/vllm/SKILL.md`
- Version: 1.0.0 | Lines: 372 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### audiocraft-audio-generation

- Path: `/root/HERMES/skills/mlops/models/audiocraft/SKILL.md`
- Version: 1.0.0 | Lines: 568 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### segment-anything-model

- Path: `/root/HERMES/skills/mlops/models/segment-anything/SKILL.md`
- Version: 1.0.0 | Lines: 506 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### qdrant-vector-search

- Path: `/root/HERMES/skills/mlops/qdrant/SKILL.md`
- Version: 1.0.0 | Lines: 497 | Age: 25.6 days
- Rot tags: prompt-bloat

### dspy

- Path: `/root/HERMES/skills/mlops/research/dspy/SKILL.md`
- Version: 1.0.0 | Lines: 594 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### huggingface-accelerate

- Path: `/root/HERMES/skills/mlops/training/huggingface-accelerate/SKILL.md`
- Version: 1.0.0 | Lines: 336 | Age: 17.3 days
- Rot tags: prompt-bloat

### peft-fine-tuning

- Path: `/root/HERMES/skills/mlops/training/peft-fine-tuning/SKILL.md`
- Version: 1.0.0 | Lines: 435 | Age: 17.3 days
- Rot tags: prompt-bloat

### whisper

- Path: `/root/HERMES/skills/mlops/whisper/SKILL.md`
- Version: 1.0.0 | Lines: 321 | Age: 25.5 days
- Rot tags: prompt-bloat

### audio-ingest

- Path: `/root/HERMES/skills/multimodal/audio-ingest/SKILL.md`
- Version: 1.0.0 | Lines: 66 | Age: 4.6 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/cache/audio-ingest.log.jsonl

### multimodal-ingest

- Path: `/root/HERMES/skills/multimodal/multimodal-ingest/SKILL.md`
- Version: 1.0.0 | Lines: 145 | Age: 2.6 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/cache/documents/doc_

### multimodal-respond

- Path: `/root/HERMES/skills/multimodal/multimodal-respond/SKILL.md`
- Version: 1.0.0 | Lines: 68 | Age: 4.6 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/audio_cache/{ts(

### news-analysis-protocol

- Path: `/root/HERMES/skills/news-analysis/news-analysis-protocol/SKILL.md`
- Version: 1.0.0 | Lines: 548 | Age: 1.0 days
- Rot tags: prompt-bloat

### world-news-analysis

- Path: `/root/HERMES/skills/news-analysis/world-news-analysis/SKILL.md`
- Version: 1.0.0 | Lines: 373 | Age: 1.0 days
- Rot tags: prompt-bloat

### orthodoxy-auditor

- Path: `/root/HERMES/skills/orthodoxy-auditor/SKILL.md`
- Version: 1.0.0 | Lines: 326 | Age: 3.0 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/backups/AGENTS.md

### paste-intent-classifier

- Path: `/root/HERMES/skills/paste-intent-classifier/SKILL.md`
- Version: unknown | Lines: 175 | Age: 1.2 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/cache/pastes/, /root/.hermes/cache/pastes/{ts}.txt, /root/.hermes/cache/pastes/20260607-042831.txt

### emotional-processing-protocol

- Path: `/root/HERMES/skills/personal/emotional-processing-protocol/SKILL.md`
- Version: unknown | Lines: 93 | Age: 17.8 days
- Rot tags: doc-rot
- Broken paths: /root/sessions/YYYY-MM-DD-execution-log.md

### composio-integration

- Path: `/root/HERMES/skills/productivity/composio-integration/SKILL.md`
- Version: 1.7.0 | Lines: 516 | Age: 3.4 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/.secrets/env/*.env, /root/.secrets/tokens/telegram-*, /root/.local/share/opencode/log/*.log

### google-workspace

- Path: `/root/HERMES/skills/productivity/google-workspace/SKILL.md`
- Version: 1.1.0 | Lines: 421 | Age: 8.2 days
- Rot tags: prompt-bloat

### linear

- Path: `/root/HERMES/skills/productivity/linear/SKILL.md`
- Version: 1.0.0 | Lines: 380 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### maps

- Path: `/root/HERMES/skills/productivity/maps/SKILL.md`
- Version: 1.2.0 | Lines: 195 | Age: 32.3 days
- Rot tags: stale-rot

### memento-flashcards

- Path: `/root/HERMES/skills/productivity/memento-flashcards/SKILL.md`
- Version: 1.0.0 | Lines: 324 | Age: 17.3 days
- Rot tags: prompt-bloat

### nano-pdf

- Path: `/root/HERMES/skills/productivity/nano-pdf/SKILL.md`
- Version: 1.0.0 | Lines: 52 | Age: 32.3 days
- Rot tags: stale-rot

### notion

- Path: `/root/HERMES/skills/productivity/notion/SKILL.md`
- Version: 2.0.0 | Lines: 448 | Age: 1.2 days
- Rot tags: prompt-bloat

### ocr-and-documents

- Path: `/root/HERMES/skills/productivity/ocr-and-documents/SKILL.md`
- Version: 2.3.0 | Lines: 172 | Age: 32.3 days
- Rot tags: stale-rot

### pdf-handwriting-overlay

- Path: `/root/HERMES/skills/productivity/pdf-handwriting-overlay/SKILL.md`
- Version: 1.0.0 | Lines: 363 | Age: 9.1 days
- Rot tags: prompt-bloat

### powerpoint

- Path: `/root/HERMES/skills/productivity/powerpoint/SKILL.md`
- Version: unknown | Lines: 237 | Age: 32.3 days
- Rot tags: stale-rot

### shop-app

- Path: `/root/HERMES/skills/productivity/shop-app/SKILL.md`
- Version: 0.0.28 | Lines: 340 | Age: 17.3 days
- Rot tags: prompt-bloat

### shopify

- Path: `/root/HERMES/skills/productivity/shopify/SKILL.md`
- Version: 1.0.0 | Lines: 373 | Age: 17.3 days
- Rot tags: prompt-bloat

### telephony

- Path: `/root/HERMES/skills/productivity/telephony/SKILL.md`
- Version: 1.0.0 | Lines: 418 | Age: 17.3 days
- Rot tags: prompt-bloat

### arxiv

- Path: `/root/HERMES/skills/research/arxiv/SKILL.md`
- Version: 1.0.0 | Lines: 282 | Age: 32.3 days
- Rot tags: stale-rot

### blogwatcher

- Path: `/root/HERMES/skills/research/blogwatcher/SKILL.md`
- Version: 2.0.0 | Lines: 137 | Age: 32.3 days
- Rot tags: stale-rot

### llm-wiki

- Path: `/root/HERMES/skills/research/llm-wiki/SKILL.md`
- Version: 2.1.0 | Lines: 578 | Age: 26.4 days
- Rot tags: doc-rot, prompt-bloat
- Broken paths: /root/AAA/SKILLS_INDEX.md

### parallel-cli

- Path: `/root/HERMES/skills/research/parallel-cli/SKILL.md`
- Version: 1.1.0 | Lines: 391 | Age: 25.5 days
- Rot tags: prompt-bloat

### polymarket

- Path: `/root/HERMES/skills/research/polymarket/SKILL.md`
- Version: 1.0.0 | Lines: 77 | Age: 32.3 days
- Rot tags: stale-rot

### research-paper-writing

- Path: `/root/HERMES/skills/research/research-paper-writing/SKILL.md`
- Version: 1.1.0 | Lines: 2377 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### web-pentest

- Path: `/root/HERMES/skills/security/web-pentest/SKILL.md`
- Version: unknown | Lines: 333 | Age: 17.3 days
- Rot tags: prompt-bloat

### agent-context-forge-loop

- Path: `/root/HERMES/skills/software-development/agent-context-forge-loop/SKILL.md`
- Version: unknown | Lines: 274 | Age: 4.5 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/cache/forge-backups/{ts}/SOUL.md, /root/.hermes/X, /root/HERMES/X

### constitutional-expository-forge

- Path: `/root/HERMES/skills/software-development/constitutional-expository-forge/SKILL.md`
- Version: 1.1.0 | Lines: 366 | Age: 5.2 days
- Rot tags: prompt-bloat

### dual-artifact-publication

- Path: `/root/HERMES/skills/software-development/dual-artifact-publication/SKILL.md`
- Version: 1.1.0 | Lines: 309 | Age: 5.2 days
- Rot tags: prompt-bloat

### engineering-prompt-forge

- Path: `/root/HERMES/skills/software-development/engineering-prompt-forge/SKILL.md`
- Version: 1.0.0 | Lines: 328 | Age: 0.5 days
- Rot tags: prompt-bloat

### plan

- Path: `/root/HERMES/skills/software-development/plan/SKILL.md`
- Version: 2.0.0 | Lines: 338 | Age: 6.0 days
- Rot tags: prompt-bloat

### subagent-driven-development

- Path: `/root/HERMES/skills/software-development/subagent-driven-development/SKILL.md`
- Version: 1.1.0 | Lines: 352 | Age: 32.3 days
- Rot tags: stale-rot, prompt-bloat

### systematic-debugging

- Path: `/root/HERMES/skills/software-development/systematic-debugging/SKILL.md`
- Version: 1.2.0 | Lines: 482 | Age: 3.0 days
- Rot tags: prompt-bloat

### test-driven-development

- Path: `/root/HERMES/skills/software-development/test-driven-development/SKILL.md`
- Version: 1.1.0 | Lines: 364 | Age: 0.6 days
- Rot tags: prompt-bloat

### sovereign-ai-redteam

- Path: `/root/HERMES/skills/sovereign-ai/sovereign-ai-redteam/SKILL.md`
- Version: 2.0.0 | Lines: 533 | Age: 0.0 days
- Rot tags: prompt-bloat

### substrate-gate-telegram

- Path: `/root/HERMES/skills/substrate-gate-telegram/SKILL.md`
- Version: 1 | Lines: 121 | Age: 1.7 days
- Rot tags: doc-rot
- Broken paths: /root/.hermes/cache/substrate-gate/audit.jsonl, /root/.hermes/cache/substrate-gate/audit.jsonl

### telegram-mode-guards

- Path: `/root/HERMES/skills/telegram-mode-guards/SKILL.md`
- Version: unknown | Lines: 312 | Age: 2.6 days
- Rot tags: prompt-bloat


## Recommendations

1. Refresh skills with `stale-rot` by updating `last_verified` and re-checking referenced packages/docs.
2. Split or trim skills flagged `prompt-bloat` into focused sub-skills or reference docs.
3. Resolve `doc-rot` broken paths and symlinks; update references to current canonical locations.
4. Review high collision pairs and sharpen `Use When` / `Do Not Use When` boundaries.