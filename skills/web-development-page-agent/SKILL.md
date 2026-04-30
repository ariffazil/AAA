---
name: web-development-page-agent
description: Embed alibaba/page-agent AI copilot into web applications. Use when you need to add natural language voice/copilot control to a web app (click "login", fill "username as John"), modernize legacy apps without rewriting frontend, or add accessibility via natural language. NOT for server-side browser automation — use Hermes built-in browser tool instead.
tags: [web, javascript, agent, browser, gui, alibaba, embed, copilot, saas]
version: 1.0.0
author: Hermes / arifOS AAA
license: MIT
requirements:
  - Node 22.13+ or 24+, npm 10+
  - OpenAI-compatible LLM endpoint
---

# page-agent — In-Page AI Copilot Widget

## What it is

alibaba/page-agent (MIT, 17k+ stars) is a TypeScript widget that drops into any web app and lets users drive the UI with natural language ("click login, fill username as John"). It reads the DOM as text — no screenshots, no multimodal LLM needed.

## When to use this skill

Load this skill when:
- Adding an AI copilot layer to arif-sites (arif-fazil.com, apex.arif-fazil.com)
- Making legacy web apps accessible via voice/text commands
- Building interactive demos or training flows
- Adding "copilot in your app" feature to SaaS/admin/ERP/CRM

## When NOT to use this

- **Hermes drives a browser** → use Hermes built-in browser tool instead
- **Cross-tab automation** → use Playwright or browser-use
- **Visual grounding** → page-agent is text-DOM only; use browser_vision instead

## Three Deployment Paths

### Path 1 — 30-second CDN demo (evaluation only)
```html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.8.0/dist/iife/page-agent.demo.js" crossorigin="anonymous"></script>
```
For quick eval only — rate-limited, not for production.

### Path 2 — npm install (production)
```bash
npm install page-agent
```
```javascript
import { PageAgent } from 'page-agent'

const agent = new PageAgent({
  model: 'qwen3.5-plus',
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: process.env.LLM_API_KEY,
  language: 'en-US',
})

// Show the panel for end users
agent.panel.show()

// Or drive programmatically
await agent.execute('Click submit button, then fill username as John')
```

Provider examples:

| Provider | baseURL | model |
|---------|---------|-------|
| Qwen/DashScope | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen3.5-plus` |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| Ollama (local) | `http://localhost:11434/v1` | `qwen3:14b` |
| OpenRouter | `https://openrouter.ai/api/v1` | `anthropic/claude-sonnet-4.6` |

### Path 3 — Clone source (development/contributing)
```bash
git clone https://github.com/alibaba/page-agent.git
cd page-agent
npm ci
# Create .env with LLM_API_KEY and LLM_BASE_URL
npm run dev:demo
# Bookmarklet: javascript:(function(){var s=document.createElement('script');s.src='http://localhost:5174/page-agent.demo.js';document.head.appendChild(s);})();
```

## Deploying to arif-sites

1. `cd /root/arif-sites`
2. `npm install page-agent`
3. Add to your app:
```javascript
import { PageAgent } from 'page-agent'
// Initialize with desired LLM
const agent = new PageAgent({ ... })
agent.panel.show()
```
4. Build and deploy

## Security Notes

- Never ship demo CDN to production (rate-limited, not your API key)
- Never hardcode `apiKey` in client-side JS — proxy through your backend
- Demo CDN API keys are alibaba's — don't use in production

## Constitutional Notes

- F05 PEACE: No harmful or abusive UI interactions
- F12 INJECTION: Sanitize all natural language inputs to page-agent
