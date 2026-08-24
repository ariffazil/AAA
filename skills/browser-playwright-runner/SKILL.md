---
name: browser-playwright-runner
description: Automated headless browser testing, end-to-end UI verification, full-page screenshot capture, visual regression checks, and client-side DOM assertions via Playwright.
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Browser Playwright UI & E2E Testing Skill (`browser-playwright-runner`)

Enables AI agents to perform end-to-end web application testing, visual UI verification, interactive DOM testing, and client-side error auditing.

## Execution Patterns

### 1. Visual Verification & Full-Page Screenshot
```bash
npx playwright screenshot --full-page --url https://arif-fazil.com/earth/ screenshot_earth.png
```

### 2. Console Error & Network Health Audit
```python
from playwright.sync_api import sync_playwright

def test_web_page(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url)
        page.wait_for_load_state("networkidle")
        browser.close()
        return {"url": url, "errors": errors}
```

### 3. DOM & Interactive Assertions
- Verify button clicks, dynamic modal popups, and tab view switches.
- Assert element visibility (`#main-content`, `.site-frame`, `table`, `svg`).

---

## Best Practices for Federation Agents

1. **Pre-Deploy UI Verification**: Run headless visual and console checks before deploying web applications to production.
2. **Visual Diff Testing**: Compare full-page screenshots before and after UI changes.
