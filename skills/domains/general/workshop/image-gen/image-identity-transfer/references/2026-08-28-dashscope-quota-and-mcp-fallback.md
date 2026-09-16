# Session: 2026-08-28 — DashScope quota exhausted, MiniMax MCP fallback delivered text-driven re-render

## What was asked

User (Arif, in BODYBUILDER group) provided two images:
- Image 1 (`/root/.hermes/cache/images/img_3ee40a1d36ea.jpg`): identity source — young adult SEA Malay male, short dark hair, calm face, gold chain, athletic build, dark grey drawstring shorts, kitchen setting
- Image 2 (`/root/.hermes/cache/images/img_f7d6766771e4.jpg`): composition source — heavier bodybuilder, oiled sheen, front upper-body pose, off-white textured studio wall

User asked: "Based on 2 picture above, replace the guy in second picture with the guy in first picture." Then: "Proceed and wow him."

## What I attempted

### Attempt 1 — QwenCloud `wan2.7-image-pro` (the right tool)

Built the request JSON correctly, with `reference_images=[identity, composition]`, `n=2`, `size=1024*1024`, explicit identity description, explicit pose/lighting preservation prompt, comprehensive negative prompt.

The QwenCloud skill's `--model wan2.7-image-pro` invocation:

```
bash -lc "set -a; source /root/.secrets/kunci-mas.env; set +a;
          export QWEN_PROVIDER=dashscope;
          export QWEN_BASE_URL='https://dashscope-intl.aliyuncs.com/api/v1';
          unset QWEN_API_KEY;
          python3 /root/AAA/skills/qwencloud-image-generation/scripts/image.py \
            --model wan2.7-image-pro \
            --file /root/forge_work/2026-08-28-faqwan-identity-swap/req_wan_v1.json \
            --output /root/forge_work/2026-08-28-faqwan-identity-swap/wan_out \
            --print-response"
```

**Two errors blocked this path:**

1. First run: `Error: Unknown provider 'bailian-token-plan'. Available providers: dashscope` — the vault has `QWEN_PROVIDER=bailian-token-plan` set, but the qwencloud-image-generation script's provider registry only knows `dashscope`. Fix was to override at invocation: `export QWEN_PROVIDER=dashscope QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/api/v1`.

2. After fix, file upload to OSS succeeded (48h TTL), but the actual generation call returned:

   ```
   RuntimeError: HTTP 403: {"code":"AllocationQuota.FreeTierOnly",
     "message":"The free quota has been exhausted. To continue accessing the model
     on a paid basis, please complete your payment information
     （or disable the \"use free tier only\" mode in the management console if
     already completed).",
     "request_id":"6da587d4-14a5-917b-93b4-12cd3f84e2f9"}
   ```

   Same error repeated when using `DASHSCOPE_PAYG_API_KEY` instead. The error itself tells you the fix: disable the "use free tier only" toggle in the DashScope console. The paid key doesn't bypass the toggle — it's account-level.

### Attempt 2 — `mcp__minimax_media__text_to_image` (the wrong tool, but only one left)

First call timed out at 300s. Second call succeeded after a re-prompt with different phrasing (less verbose, more direct). Two outputs saved to `/root/forge_work/2026-08-28-faqwan-identity-swap/minimax_v1.jpg` and `minimax_v2.jpg`.

**Crucial limitation surfaced:** `mcp__minimax_media__text_to_image` accepts only `(model, prompt, n, aspect_ratio, output_directory, prompt_optimizer)` — there is NO `reference_images` parameter. The model cannot see the identity source photo. The face in the output is fabricated from the text description, not transferred from the reference.

## What I observed in the outputs

Both outputs were compositionally correct (off-white wall, front upper-body pose, oil sheen, gold chain, gold chain shape preserved, similar body composition). But the face in both outputs is a generic East Asian male — NOT the identity source's face. Vision-analyze confirmed:
- v1: face has the right general build and pose, but is a different person
- v2: natural athletic build (less bodybuilder), but again a different person

The user did not explicitly say "wow me" was met. The deliverable was honest: I told the user the identity wasn't transferred, the model fabricated a face, and gave them three paths forward (unlock DashScope console, mmx auth login, try MuleRouter).

## Lessons (extracted to main skill body)

1. **Tool selection matters before honesty matters.** Even an honest disclosure of fabrication is wasted if a real tool was sitting one console-click away. Always check `wan2.7-image-pro` / `qwen-image-2.0-pro` availability first.

2. **The DashScope "FreeTierOnly" 403 is misleading.** It looks like a billing error but it's an account-level toggle. Don't waste cycles retrying with `DASHSCOPE_PAYG_API_KEY` — same result.

3. **`mcp__minimax_media__text_to_image` does NOT support reference_images.** This is the single most important fact for any identity-swap request routed through that MCP. The MCP is text-to-image only.

4. **The vault's `QWEN_PROVIDER=bailian-token-plan` doesn't match the skill's provider registry.** Either the vault or the skill needs to be updated; for now, override at invocation.

5. **Vision-analyze is the verification step.** It caught that the output face did not match the input identity. Without it, I would have shipped a fabricated face as "swap done."
