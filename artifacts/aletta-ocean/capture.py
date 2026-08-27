"""Render sado-reference page and capture full-page screenshot."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://syedos.arif-fazil.com/sado-reference/"
OUT_DIR = Path("/root/AAA/artifacts/aletta-ocean")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_PATH = OUT_DIR / "live-preview.png"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
        )
        page = await context.new_page()

        console_msgs = []
        page.on("console", lambda msg: console_msgs.append(f"[{msg.type}] {msg.text}"))
        failed_requests = []
        page.on("requestfailed", lambda req: failed_requests.append(f"{req.url} - {req.failure}"))

        print(f"Navigating to {URL}...")
        response = await page.goto(URL, wait_until="networkidle", timeout=30000)
        print(f"Status: {response.status if response else 'no response'}")

        # Wait 5s for fonts as specified
        await page.wait_for_timeout(5000)

        # Verify presence of expected elements
        title_visible = await page.locator("text=ALETTA OCEAN").count()
        vs_count = await page.locator("text=vs").count()
        respect_section = await page.locator("text=Why Abang Sado Respect Dia").count()

        # Image checks
        imgs = page.locator("img")
        img_count = await imgs.count()
        img_details = []
        for i in range(img_count):
            img = imgs.nth(i)
            src = await img.get_attribute("src")
            alt = await img.get_attribute("alt")
            natural_w = await img.evaluate("el => el.naturalWidth")
            natural_h = await img.evaluate("el => el.naturalHeight")
            complete = await img.evaluate("el => el.complete")
            img_details.append({
                "src": src, "alt": alt,
                "naturalWidth": natural_w, "naturalHeight": natural_h,
                "loaded": complete,
            })

        # Layout probe — get bounding boxes of portraits and vs circle
        layout = await page.evaluate("""() => {
            const result = {};
            // Try to find portrait containers by alt or class
            const allImgs = Array.from(document.querySelectorAll('img'));
            result.imgCount = allImgs.length;
            result.imgs = allImgs.map(i => ({
                src: i.src,
                alt: i.alt,
                rect: i.getBoundingClientRect().toJSON(),
            }));
            // Look for 'vs' element
            const allEls = Array.from(document.querySelectorAll('*'));
            const vsEls = allEls.filter(e => e.textContent.trim() === 'vs' && e.children.length === 0);
            result.vsElements = vsEls.map(v => ({
                text: v.textContent,
                tag: v.tagName,
                rect: v.getBoundingClientRect().toJSON(),
                classes: v.className,
            }));
            // Get page dimensions
            result.pageHeight = document.documentElement.scrollHeight;
            result.pageWidth = document.documentElement.scrollWidth;
            result.viewportHeight = window.innerHeight;
            result.viewportWidth = window.innerWidth;
            result.title = document.title;
            return result;
        }""")

        print("\n=== LAYOUT PROPOSURE ===")
        print(f"Page title: {layout['title']}")
        print(f"Page dimensions: {layout['pageWidth']}x{layout['pageHeight']} (viewport {layout['viewportWidth']}x{layout['viewportHeight']})")
        print(f"Image count: {layout['imgCount']}")
        for i, img in enumerate(layout['imgs']):
            print(f"  img[{i}]: src={img['src'][-60:] if img['src'] else 'NONE'} alt={img['alt']} rect=({img['rect']['width']:.0f}x{img['rect']['height']:.0f} @ {img['rect']['x']:.0f},{img['rect']['y']:.0f})")
        print(f"vs elements: {len(layout['vsElements'])}")
        for v in layout['vsElements']:
            print(f"  '{v['text']}' <{v['tag']}> class={v['classes']} rect=({v['rect']['width']:.0f}x{v['rect']['height']:.0f} @ {v['rect']['x']:.0f},{v['rect']['y']:.0f})")

        print("\n=== TEXT PROPOSURE ===")
        print(f"'ALETTA OCEAN' matches: {title_visible}")
        print(f"'vs' matches: {vs_count}")
        print(f"'Why Abang Sado Respect Dia' matches: {respect_section}")

        print("\n=== IMAGES ===")
        for img in img_details:
            print(f"  src={img['src'][-60:] if img['src'] else 'NONE'} alt={img['alt']} {img['naturalWidth']}x{img['naturalHeight']} loaded={img['loaded']}")

        if failed_requests:
            print("\n=== FAILED REQUESTS ===")
            for f in failed_requests:
                print(f"  {f}")

        if console_msgs:
            print("\n=== CONSOLE (last 20) ===")
            for m in console_msgs[-20:]:
                print(f"  {m}")

        # Capture full-page screenshot
        print(f"\n=== CAPTURING FULL-PAGE SCREENSHOT to {SCREENSHOT_PATH} ===")
        await page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
        print(f"Screenshot saved: {SCREENSHOT_PATH}")
        print(f"File size: {SCREENSHOT_PATH.stat().st_size} bytes")

        await browser.close()

asyncio.run(main())