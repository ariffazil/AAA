/**
 * 🏦 AIA — WEALTH Capital Intelligence Bot
 * 
 * Telegram bot for the WEALTH organ.
 * Mini App: Capital Intel (fiscal, market, finance)
 * Group: AIA
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
      { command: "start", description: "Open Capital Intelligence" },
      { command: "fiscal", description: "⛽ Malaysia Fiscal Breakeven" },
      { command: "market", description: "📊 Market Data" },
      { command: "finance", description: "💰 Personal Finance" },
      { command: "help", description: "Show help" },
    ]);

    await bot.api.setChatMenuButton({
      menu_button: {
        type: "web_app",
        text: "💰 Capital Intel",
        web_app: { url: `${MINIAPP_URL}/wealth` },
      },
    });

    await bot.api.setMyShortDescription("WEALTH Capital Intelligence — fiscal breakeven, market data, capital flows.");
    await bot.api.setMyDescription(
      "🏦 AIA — Capital Intelligence\n\n" +
      "• ⛽ Malaysia fiscal breakeven analysis\n" +
      "• 📊 Brent crude & market data\n" +
      "• 💰 Personal finance tracking\n\n" +
      "WEALTH computes. arifOS judges. Arif decides.\n" +
      "DITEMPA BUKAN DIBERI"
    );

    console.log("✅ AIA configured");
  } catch (e: any) {
    console.error("⚠️ Config warning:", e.message);
  }
}

bot.command("start", async (ctx) => {
  await ctx.reply(
    `🏦 *AIA — Capital Intelligence*\n\n` +
    `WEALTH organ of the arifOS Federation.\n\n` +
    `Tap below to explore capital intelligence.`,
    {
      parse_mode: "Markdown",
      reply_markup: new InlineKeyboard()
        .webApp("💰 Capital Intel", `${MINIAPP_URL}/wealth`)
        .row()
        .webApp("🏥 Federation Status", `${MINIAPP_URL}/status`),
    }
  );
});

bot.command("fiscal", async (ctx) => {
  await ctx.reply("⛽ *Malaysia Fiscal Breakeven*\n\nTap to view:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/wealth`),
  });
});

bot.command("market", async (ctx) => {
  await ctx.reply("📊 *Market Data*\n\nTap to view:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/wealth`),
  });
});

bot.command("finance", async (ctx) => {
  await ctx.reply("💰 *Personal Finance*\n\nTap to view:", {
    parse_mode: "Markdown",
    reply_markup: new InlineKeyboard().webApp("Open", `${MINIAPP_URL}/wealth`),
  });
});

bot.command("help", async (ctx) => {
  await ctx.reply(
    `*AIA — Capital Intelligence*\n\n` +
    `/fiscal — Malaysia fiscal breakeven\n` +
    `/market — Market data (Brent, FX)\n` +
    `/finance — Personal finance\n\n` +
    `Or tap the 💰 button at the bottom.\n\n` +
    `_WEALTH computes. arifOS judges. Arif decides._`,
    { parse_mode: "Markdown" }
  );
});

console.log("🏦 AIA bot starting...");
await configure();
bot.start({
  onStart: (info) => console.log(`✅ AIA @${info.username} live → https://t.me/${info.username}`),
});
