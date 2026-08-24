---
name: "qwen-harness-tools"
id: "qwen-harness-tools"
version: 1.0.0
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: "Documents Qwen Token Plan Harness tools (web search, code interpreter, web scraping, reverse image search, text-to-image search) that are built into supported models. Activates when the user asks for real-time web info, code execution in a sandbox, or image search while using a Token Plan model."
autonomy_tier: T1
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

Qwen Token Plan **Harness tools** are built into supported models. The model invokes them automatically based on the question — no extra configuration, billed per successful invocation from Token Plan Credits.

User request: $ARGUMENTS

## Applicable models (Personal + Team Edition)

| Model | Harness tools |
|---|---|
| `qwen3.8-max` | web search, code interpreter, web scraping, reverse image search, text-to-image search |
| `qwen3.7-max` | web search, code interpreter, web scraping |
| `qwen3.7-plus` | web search, code interpreter, web scraping, reverse image search, text-to-image search |

**Note:** Harness tools apply to **Token Plan**, not to **Coding Plan**.

## Tool reference

| Tool | What it does | When the model uses it |
|---|---|---|
| **Web search** | Retrieves information from the internet and generates answers based on search results. | Questions about current events, recent releases, news, prices, etc. |
| **Code interpreter** | Writes and runs Python code in a sandbox for math / data analysis. | Numerical computation, data transformation, plotting, statistical analysis. |
| **Web scraping** | Accesses a specified URL and extracts its content. | User gives a URL and asks for info from that page. |
| **Reverse image search** | Searches for visually similar images given an input image. | "Find where this image came from", "find similar products". |
| **Text-to-image search** | Searches for relevant images given a text description. | "Find me an image of X", "what does X look like". |

## Steps

1. **Verify the active model is in the supported list above.** If not, switch via the tool's model picker:
   - Claude Code: `/model qwen3.7-max`
   - OpenCode: `/models` then select
   - Qwen Code: `/model` then select
   - OpenClaw: update `~/.openclaw/openclaw.json` `agents.defaults.model.primary`

2. **Just ask.** Harness tools are automatic — the model decides when to invoke based on the question. Example: `Use the qwen3.7-max built-in web search to find the latest on <topic>.`

3. **For URL scraping specifically**, include the URL in the prompt so the model routes to the web scraping tool (not web search):
   > `Use the web scraping tool on https://example.com/page and summarize.`

4. **For code interpreter**, ask computational questions explicitly:
   > `Use code interpreter to compute the standard deviation of <list>.`

5. **Cost control**: Harness invocations are billed per successful call. Avoid invoking on trivial questions where the model could answer from context alone.

## Notes

- **Token Plan only**: these tools do NOT apply to Coding Plan, pay-as-you-go API keys (`sk-` prefix), or FLAME `RM0-TOOLS-FREELOOP` chain.
- **Vision vs Harness**: separate capability. Vision (image input) is auto-enabled for `qwen3.8-max`, `qwen3.7-plus`, `qwen3.6-plus`, `qwen3.5-plus`, `kimi-k2.5`. Harness is a tool, not vision.
- **Free alternative**: for RM0 web search outside Token Plan, use the `firecrawl-web-search` skill instead.
- **OpenCode / OpenClaw config**: see `token-plan-bailian-config` skill for the modalities / input fields that enable vision.
