/**
 * Telegram WebApp SDK Wrapper
 * 
 * Handles initialization, theme, user data, and native features.
 */

import WebApp from "@twa-dev/sdk";

export const tg = WebApp;

export function initTelegram() {
  tg.ready();
  tg.expand();
  tg.setHeaderColor("#0a0a0f");
  tg.setBackgroundColor("#0a0a0f");
}

export function getUser() {
  return tg.initDataUnsafe?.user || null;
}

export function getTheme() {
  return {
    bg: tg.themeParams.bg_color || "#0a0a0f",
    text: tg.themeParams.text_color || "#e0e0e0",
    hint: tg.themeParams.hint_color || "#6b7280",
    link: tg.themeParams.link_color || "#3b82f6",
    button: tg.themeParams.button_color || "#3b82f6",
    buttonText: tg.themeParams.button_text_color || "#ffffff",
    secondaryBg: tg.themeParams.secondary_bg_color || "#1a1a2e",
  };
}

export function sendResult(data: Record<string, unknown>) {
  tg.sendData(JSON.stringify(data));
}

export function closeApp() {
  tg.close();
}

export function showPopup(title: string, message: string) {
  tg.showPopup({ title, message, buttons: [{ type: "close" }] });
}

// Check if running inside Telegram
export function isTelegram() {
  return typeof window !== "undefined" && "Telegram" in window && "WebApp" in (window as any).Telegram;
}
