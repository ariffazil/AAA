/**
 * 🌐 Hermes-ASI — arifOS Federation Gateway Bot
 * 
 * THE main bot. Constitutional stage commands:
 * /000 → /111 → /333 → /555 → /666 → /777 → /888 → /999 → /AAA
 * 
 * DITEMPA BUKAN DIBERI
 */

import { Bot, InlineKeyboard } from "grammy";
import { config } from "dotenv";

config();

const BOT_TOKEN = process.env.BOT_TOKEN;
const MINIAPP_URL = process.env.MINIAPP_URL || "https://app.arif-fazil.com";

if (!BOT_TOKEN) {
  console.error("❌ BOT_TOKEN required");
  process.exit(1);
}

const bot = new Bot(BOT_TOKEN);

// ─── Command Definitions (stages 000-999 + AAA) ─────────────
const STAGES: Record<string, { emoji: string; name: string; desc: string; path: string }> = {
  "000": { emoji: "🧭", name: "INIT",      desc: "Intent classification — golden path entry",    path: "/init" },
  "111": { emoji: "👁️", name: "SENSE",     desc: "Evidence binding — OBSERVED, RETRIEVED",       path: "/explore" },
  "333": { emoji: "🧠", name: "MIND",      desc: "Plan generation — evidence to plan",            path: "/explore" },
  "555": { emoji: "💾", name: "MEMORY",    desc: "Memory synthesis — recall, persist, audit",     path: "/status" },
  "666": { emoji: "💔", name: "CRITIQUE",  desc: "Stress test — ethics, harm, dignity, capital",  path: "/well" },
  "777": { emoji: "⚒️", name: "FORGE",     desc: "Execution — build, deploy, verify",             path: "/forge" },
  "888": { emoji: "⚖️", name: "JUDGE",     desc: "Constitutional verdict — SEAL/HOLD/VOID",       path: "/kernel" },
  "999": { emoji: "💎", name: "SEAL",      desc: "VAULT999 — immutable audit ledger",             path: "/seal" },
  "aaa": { emoji: "🖥️", name: "COCKPIT",   desc: "Federation status — organs, health, agents",    path: "/status" },
};

let _lastConfigure = 0;
async function configure() {
  // Skip if configured recently (avoids Telegram rate limits on rapid restarts)
  if (Date.now() - _lastConfigure < 30_000) {
    console.log("⏭️ Skipping configure (ran recently)");
    return;
  }
  _lastConfigure = Date.now();
  try {
    // Set bot commands (Telegram shows these in the / menu)
    await bot.api.setMyCommands([
      ...Object.entries(STAGES).map(([cmd, meta]) => ({
        command: cmd,
        description: `${meta.name} - ${meta.desc.split("—")[0].trim()}`,
      })),
      { command: "update", description: "Self-update and redeploy" },
      { command: "restart", description: "Restart services" },
      { command: "health", description: "Quick health check" },
      { command: "help", description: "Show all commands" },
    ]);

    // Menu button
    await bot.api.setChatMenuButton({
      menu_button: {
        type: "web_app",
        text: "🌐 Federation",
        web_app: { url: `${MINIAPP_URL}/init` },
      },
    });

    await bot.api.setMyShortDescription("arifOS Federation Gateway — 000→111→333→555→666→777→888→999→AAA");
    await bot.api.setMyDescription(
      "🌐 Hermes-ASI — arifOS Federation Gateway\n\n" +
      "Constitutional stages:\n" +
      "🧭 /000 — INIT (intent)\n" +
      "👁️ /111 — SENSE (evidence)\n" +
      "🧠 /333 — MIND (plan)\n" +
      "💾 /555 — MEMORY (recall)\n" +
      "💔 /666 — CRITIQUE (stress)\n" +
      "⚒️ /777 — FORGE (execute)\n" +
      "⚖️ /888 — JUDGE (verdict)\n" +
      "💎 /999 — SEAL (vault)\n" +
      "🖥️ /AAA — COCKPIT (status)\n\n" +
      "DITEMPA BUKAN DIBERI — Forged, Not Given."
    );

    console.log("✅ Hermes-ASI configured with 9 stage commands");
  } catch (e: any) {
    console.error("⚠️ Config warning:", e.message);
  }
}

// ─── /start — Full Menu ─────────────────────────────────────
bot.command("start", async (ctx) => {
  const name = ctx.from?.first_name || "Sovereign";
  
  await ctx.reply(
    `🌐 *Hermes-ASI*\n\n` +
    `Welcome, ${name}. Federation Gateway online.\n\n` +
    `Constitutional stages:`,
    {
      parse_mode: "Markdown",
      reply_markup: new InlineKeyboard()
        .webApp("🧭 000 INIT", `${MINIAPP_URL}/init`)
        .webApp("👁️ 111 SENSE", `${MINIAPP_URL}/explore`)
        .row()
        .webApp("🧠 333 MIND", `${MINIAPP_URL}/explore`)
        .webApp("💾 555 MEMORY", `${MINIAPP_URL}/status`)
        .row()
        .webApp("💔 666 CRITIQUE", `${MINIAPP_URL}/well`)
        .webApp("⚒️ 777 FORGE", `${MINIAPP_URL}/forge`)
        .row()
        .webApp("⚖️ 888 JUDGE", `${MINIAPP_URL}/kernel`)
        .webApp("💎 999 SEAL", `${MINIAPP_URL}/seal`)
        .row()
        .webApp("🖥️ AAA COCKPIT", `${MINIAPP_URL}/status`),
    }
  );
});

// ─── Stage Commands ─────────────────────────────────────────
for (const [cmd, meta] of Object.entries(STAGES)) {
  bot.command(cmd, async (ctx) => {
    await ctx.reply(
      `${meta.emoji} *${meta.name} (${cmd})*\n\n` +
      `${meta.desc}\n\n` +
      `Tap to open:`,
      {
        parse_mode: "Markdown",
        reply_markup: new InlineKeyboard()
          .webApp(`Open ${meta.name}`, `${MINIAPP_URL}${meta.path}`)
          .row()
          .webApp("🌐 Full Menu", `${MINIAPP_URL}/init`),
      }
    );
  });
}

// ─── /update — Self-update and redeploy ─────────────────────
bot.command("update", async (ctx) => {
  const userId = ctx.from?.id;
  // Only sovereign (replace with Arif's Telegram user ID)
  // For now, allow all — tighten later with user ID check
  
  const msg = await ctx.reply("⚕ *Updating Hermes-ASI…*\n\n→ Pulling latest code…", { parse_mode: "Markdown" });

  const steps: string[] = [];
  const edit = async (text: string) => {
    try {
      await ctx.api.editMessageText(msg.chat.id, msg.message_id, text, { parse_mode: "Markdown" });
    } catch {}
  };

  try {
    // Step 1: Pull latest
    const { execSync } = await import("child_process");
    const projectDir = "/root/AAA/telegram-miniapp";
    
    try {
      execSync(`cd ${projectDir} && git pull origin main 2>&1`, { timeout: 15000 });
      steps.push("✅ Code updated");
    } catch {
      steps.push("⚠️ Git pull skipped (no remote or up to date)");
    }

    await edit(
      `⚕ *Updating Hermes-ASI…*\n\n${steps.join("\n")}\n→ Installing dependencies…`
    );

    // Step 2: Install deps
    try {
      execSync(`cd ${projectDir} && pnpm install --frozen-lockfile 2>&1`, { timeout: 30000 });
      steps.push("✅ Dependencies installed");
    } catch {
      execSync(`cd ${projectDir} && pnpm install 2>&1`, { timeout: 30000 });
      steps.push("✅ Dependencies installed");
    }

    // Step 3: Build Mini App
    await edit(
      `⚕ *Updating Hermes-ASI…*\n\n${steps.join("\n")}\n→ Building Mini App…`
    );
    execSync(`cd ${projectDir}/app && npx vite build 2>&1`, { timeout: 30000 });
    steps.push("✅ Mini App built");

    // Step 4: Deploy static files
    await edit(
      `⚕ *Updating Hermes-ASI…*\n\n${steps.join("\n")}\n→ Deploying…`
    );
    execSync(`rm -rf /var/www/html/miniapp/* && cp -r ${projectDir}/app/dist/* /var/www/html/miniapp/`, { timeout: 10000 });
    steps.push("✅ Static files deployed");

    // Step 5: Reload Caddy
    execSync(`systemctl reload caddy 2>&1`, { timeout: 5000 });
    steps.push("✅ Caddy reloaded");

    // Step 6: Restart API
    execSync(`systemctl restart miniapp-api 2>&1`, { timeout: 10000 });
    steps.push("✅ API gateway restarted");

    // Done
    await edit(
      `⚕ *Hermes-ASI Updated* ✅\n\n${steps.join("\n")}\n\n` +
      `_All organs online. DITEMPA BUKAN DIBERI._`
    );

  } catch (e: any) {
    steps.push(`✗ ${e.message?.slice(0, 100)}`);
    await edit(
      `⚕ *Hermes-ASI Update Failed* ❌\n\n${steps.join("\n")}`
    );
  }
});

// ─── /restart — Restart bot + API services ──────────────────
let _lastRestart = 0;
bot.command("restart", async (ctx) => {
  // Rate-limit: 1 restart per 30s to prevent spam loops
  if (Date.now() - _lastRestart < 30_000) {
    await ctx.reply("⏳ Restart already in progress or recent. Wait 30s.");
    return;
  }
  _lastRestart = Date.now();
  await ctx.reply("♻️ *Restarting services…*", { parse_mode: "Markdown" });
  
  try {
    const { execSync, spawn } = await import("child_process");
    
    // Restart API first
    execSync("systemctl restart miniapp-api", { timeout: 10000 });
    await ctx.reply("✅ miniapp-api restarted");
    
    // Restart bot with detached process so systemd can hand off cleanly
    const child = spawn("systemctl", ["restart", "miniapp-bot"], {
      detached: true,
      stdio: "ignore",
    });
    child.unref();
    
    // Don't await — the process will be replaced by systemd restart
  } catch (e: any) {
    await ctx.reply(`❌ Restart failed: ${e.message?.slice(0, 200)}`);
  }
});

// ─── /health — Quick health check ───────────────────────────
bot.command("health", async (ctx) => {
  try {
    const resp = await fetch("http://localhost:3100/health", { signal: AbortSignal.timeout(3000) });
    const data = await resp.json();
    const organs = data.organs || [];
    
    await ctx.reply(
      `🏥 *Federation Health*\n\n` +
      `API Gateway: ✅\n` +
      `Organs: ${organs.join(", ")}\n` +
      `Time: ${data.timestamp || new Date().toISOString()}\n\n` +
      `_DITEMPA BUKAN DIBERI_`,
      { parse_mode: "Markdown" }
    );
  } catch {
    await ctx.reply("❌ API Gateway unreachable");
  }
});

// ─── Help ───────────────────────────────────────────────────
bot.command("help", async (ctx) => {
  const lines = Object.entries(STAGES).map(
    ([cmd, meta]) => `/${cmd} — ${meta.emoji} ${meta.name} · ${meta.desc}`
  ).join("\n");

  await ctx.reply(
    `*Hermes-ASI — Federation Gateway*\n\n` +
    `*Constitutional Stages:*\n${lines}\n\n` +
    `Tap 🌐 at the bottom for the full interface.\n\n` +
    `_DITEMPA BUKAN DIBERI_`,
    { parse_mode: "Markdown" }
  );
});

// ─── Inline Query ───────────────────────────────────────────
bot.on("inline_query", async (ctx) => {
  const query = ctx.inlineQuery.query;
  if (!query) { await ctx.answerInlineQuery([], { cache_time: 0 }); return; }

  await ctx.answerInlineQuery(Object.entries(STAGES).map(([id, meta]) => ({
    type: "article" as const,
    id,
    title: `${meta.emoji} ${meta.name} (${id})`,
    description: meta.desc,
    input_message_content: {
      message_text: `${meta.emoji} *${meta.name}*\n\n${meta.desc}`,
      parse_mode: "Markdown" as const,
    },
    reply_markup: new InlineKeyboard().webApp(`Open ${meta.name}`, `${MINIAPP_URL}${meta.path}`),
  })), { cache_time: 30 });
});

// ─── Data from Mini App ─────────────────────────────────────
bot.on("message:web_app_data", async (ctx) => {
  try {
    const data = JSON.parse(ctx.message.web_app_data.data);
    const type = data.type || "result";
    await ctx.reply(
      `📊 *${type.replace(/_/g, " ").toUpperCase()}*\n\n` +
      `\`\`\`json\n${JSON.stringify(data, null, 2).slice(0, 800)}\n\`\`\`\n\n` +
      `_Source: arifOS Federation_`,
      { parse_mode: "Markdown" }
    );
  } catch {
    await ctx.reply("📊 Result received from Mini App.");
  }
});

// ─── Start ──────────────────────────────────────────────────
async function main() {
  console.log("🌐 Hermes-ASI Federation Gateway starting...");
  console.log(`📱 Mini App URL: ${MINIAPP_URL}`);
  console.log(`📋 Stages: ${Object.keys(STAGES).join(" → ")}`);

  await configure();

  bot.start({
    onStart: (info) => {
      console.log(`✅ Hermes-ASI @${info.username} live`);
      console.log(`🔗 https://t.me/${info.username}`);
      console.log(`📋 Commands: /000 /111 /333 /555 /666 /777 /888 /999 /AAA`);
    },
  });
}

main().catch(console.error);
