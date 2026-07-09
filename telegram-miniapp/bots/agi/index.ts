/**
 * 🦞 AGI — OpenClaw Legacy Bot
 * 
 * Legacy bot from OpenClaw era. Now serves the same
 * Federation Mini App as Hermes, but with its own identity.
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
      { command: "start", description: "🦞 Open Federation Gateway" },
      { command: "explore", description: "🌍 Earth Explorer" },
      { command: "wealth", description: "💰 Capital Intel" },
      { command: "well", description: "🫀 Readiness" },
      { command: "status", description: "🏥 Federation Status" },
      { command: "help", description: "Show help" },
    ]);

    await bot.api.setChatMenuButton({
      menu_button: {
        type: "web_app",
        text: "🦞 Federation",
        web_app: { url: `${MINIAPP_URL}/explore` },
      },
    });

    await bot.api.setMyShortDescription("AGI — arifOS Federation Gateway (OpenClaw legacy).");
    await bot.api.setMyDescription(
      "🦞 AGI — Federation Gateway\n\n" +
      "Legacy OpenClaw bot, now serving the arifOS Federation.\n\n" +
      "🌍 /explore — Earth intelligence\n" +
      "💰 /wealth — Capital intelligence\n" +
      "🫀 /well — Human readiness\n" +
      "🏥 /status — Federation health\n\n" +
      "DITEMPA BUKAN DIBERI"
    );

    console.log("✅ AGI configured");
  } catch (e: any) {
    console.error("⚠️ Config warning:", e.message);
  }
}

bot.command("start", async (ctx) => {
  await ctx.reply(
    `🦞 *AGI — Federation Gateway*\n\nOpenClaw legacy bot. Same federation, different door.`,
    {
      parse_mode: "Markdown",
      reply_markup: new InlineKeyboard()
        .webApp("🌍 Earth", `${MINIAPP_URL}/explore`)
        .webApp("💰 Capital", `${MINIAPP_URL}/wealth`)
        .row()
        .webApp("🫀 Readiness", `${MINIAPP_URL}/well`)
        .webApp("🏥 Status", `${MINIAPP_URL}/status`),
    }
  );
});

bot.command("explore", async (ctx) => {
  await ctx.reply("🌍 *Earth Explorer*\n\nTap to open:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/explore`),
  });
});

bot.command("wealth", async (ctx) => {
  await ctx.reply("💰 *Capital Intel*\n\nTap to open:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/wealth`),
  });
});

bot.command("well", async (ctx) => {
  await ctx.reply("🫀 *Readiness*\n\nTap to open:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/well`),
  });
});

bot.command("status", async (ctx) => {
  await ctx.reply("🏥 *Federation Status*\n\nTap to open:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/status`),
  });
});

bot.command("help", async (ctx) => {
  await ctx.reply(
    `*AGI — Federation Gateway*\n\n` +
    `/explore — 🌍 Earth intelligence\n` +
    `/wealth — 💰 Capital intelligence\n` +
    `/well — 🫀 Human readiness\n` +
    `/status — 🏥 Federation health\n\n` +
    `_DITEMPA BUKAN DIBERI_`,
    { parse_mode: "Markdown" }
  );
});

console.log("🦞 AGI bot starting...");
await configure();
bot.start({
  onStart: (info) => console.log(`✅ AGI @${info.username} live → https://t.me/${info.username}`),
});
