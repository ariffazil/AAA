/**
 * 🖥️ AAA — Control Plane Cockpit Bot
 * 
 * Telegram bot for the AAA organ.
 * Mini App: Federation status, agent registry, health
 * Group: AAA
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
      { command: "start", description: "Open AAA Cockpit" },
      { command: "status", description: "🏥 Federation Status" },
      { command: "organs", description: "🫀 Organ Health" },
      { command: "help", description: "Show help" },
    ]);

    await bot.api.setChatMenuButton({
      menu_button: {
        type: "web_app",
        text: "🖥️ Cockpit",
        web_app: { url: `${MINIAPP_URL}/status` },
      },
    });

    await bot.api.setMyShortDescription("AAA Control Plane — federation status, agent registry, governance.");
    await bot.api.setMyDescription(
      "🖥️ AAA — Control Plane Cockpit\n\n" +
      "• 🏥 Federation organ health\n" +
      "• 📊 Agent registry\n" +
      "• ⚖️ Constitutional governance\n\n" +
      "DITEMPA BUKAN DIBERI"
    );

    console.log("✅ AAA configured");
  } catch (e: any) {
    console.error("⚠️ Config warning:", e.message);
  }
}

bot.command("start", async (ctx) => {
  await ctx.reply(
    `🖥️ *AAA — Control Plane*\n\n` +
    `Cockpit of the arifOS Federation.\n\n` +
    `Tap below to open the dashboard.`,
    {
      parse_mode: "Markdown",
      reply_markup: new InlineKeyboard()
        .webApp("🖥️ Cockpit", `${MINIAPP_URL}/status`)
        .row()
        .webApp("🌍 Earth Explorer", `${MINIAPP_URL}/explore`)
        .row()
        .webApp("💰 Capital Intel", `${MINIAPP_URL}/wealth`)
        .row()
        .webApp("🫀 Readiness", `${MINIAPP_URL}/well`),
    }
  );
});

bot.command("status", async (ctx) => {
  await ctx.reply("🏥 *Federation Status*\n\nTap to view:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open Cockpit", `${MINIAPP_URL}/status`),
  });
});

bot.command("organs", async (ctx) => {
  await ctx.reply("🫀 *Organ Health*\n\nTap to view:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open Cockpit", `${MINIAPP_URL}/status`),
  });
});

bot.command("help", async (ctx) => {
  await ctx.reply(
    `*AAA — Control Plane*\n\n` +
    `/status — Federation status\n` +
    `/organs — Organ health grid\n\n` +
    `Or tap the 🖥️ button at the bottom.\n\n` +
    `_DITEMPA BUKAN DIBERI_`,
    { parse_mode: "Markdown" }
  );
});

console.log("🖥️ AAA bot starting...");
await configure();
bot.start({
  onStart: (info) => console.log(`✅ AAA @${info.username} live → https://t.me/${info.username}`),
});
