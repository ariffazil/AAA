/**
 * 🫀 ALPHA-ZEN — WELL Human Readiness Bot
 * 
 * Telegram bot for the WELL organ.
 * Mini App: Readiness (vitality, biometrics, dignity)
 * Group: ALPHA-ZEN
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

async function configure() {
  try {
    await bot.api.setMyCommands([
      { command: "start", description: "Open Readiness Dashboard" },
      { command: "ready", description: "🫀 Quick Readiness Check" },
      { command: "vitality", description: "💚 Full Vitality Assessment" },
      { command: "help", description: "Show help" },
    ]);

    await bot.api.setChatMenuButton({
      menu_button: {
        type: "web_app",
        text: "🫀 Readiness",
        web_app: { url: `${MINIAPP_URL}/well` },
      },
    });

    await bot.api.setMyShortDescription("WELL Human Readiness — vitality, fatigue, dignity.");
    await bot.api.setMyDescription(
      "🫀 ALPHA-ZEN — Human Readiness\n\n" +
      "• 🟢 Readiness score & status\n" +
      "• 📊 Biometric signals\n" +
      "• ⏱️ Data freshness\n\n" +
      "WELL holds a mirror, not a veto.\n" +
      "DITEMPA BUKAN DIBERI"
    );

    console.log("✅ ALPHA-ZEN configured");
  } catch (e: any) {
    console.error("⚠️ Config warning:", e.message);
  }
}

bot.command("start", async (ctx) => {
  await ctx.reply(
    `🫀 *ALPHA-ZEN — Human Readiness*\n\n` +
    `WELL organ of the arifOS Federation.\n\n` +
    `Tap below to check readiness.`,
    {
      parse_mode: "Markdown",
      reply_markup: new InlineKeyboard()
        .webApp("🫀 Readiness", `${MINIAPP_URL}/well`)
        .row()
        .webApp("🏥 Federation Status", `${MINIAPP_URL}/status`),
    }
  );
});

bot.command("ready", async (ctx) => {
  await ctx.reply("🫀 *Quick Readiness Check*\n\nTap to view:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/well`),
  });
});

bot.command("vitality", async (ctx) => {
  await ctx.reply("💚 *Full Vitality Assessment*\n\nTap to view:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/well`),
  });
});

bot.command("help", async (ctx) => {
  await ctx.reply(
    `*ALPHA-ZEN — Human Readiness*\n\n` +
    `/ready — Quick readiness check\n` +
    `/vitality — Full vitality assessment\n\n` +
    `Or tap the 🫀 button at the bottom.\n\n` +
    `_WELL holds a mirror, not a veto._`,
    { parse_mode: "Markdown" }
  );
});

console.log("🫀 ALPHA-ZEN bot starting...");
await configure();
bot.start({
  onStart: (info) => console.log(`✅ ALPHA-ZEN @${info.username} live → https://t.me/${info.username}`),
});
