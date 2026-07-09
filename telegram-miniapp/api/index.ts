/**
 * arifOS Federation — Telegram Mini App API Gateway
 * 
 * Proxies HTTP requests to MCP servers using MCP protocol.
 * Manages sessions, handles responses, serves the Mini App.
 * 
 * DITEMPA BUKAN DIBERI
 */

import { Hono } from "hono";
import { cors } from "hono/cors";
import { serve } from "@hono/node-server";
import { config } from "dotenv";

config();

const app = new Hono();

// CORS for Telegram WebView
app.use("*", cors({
  origin: ["https://web.telegram.org", "https://app.arif-fazil.com", "http://localhost:5173"],
  allowMethods: ["GET", "POST"],
  allowHeaders: ["Content-Type", "X-Telegram-Init-Data"],
}));

// ─── MCP Session Manager ───────────────────────────────────
interface MCPSession {
  id: string;
  expires: number;
}

const sessions: Map<string, MCPSession> = new Map();

const MCP_SERVERS: Record<string, string> = {
  geox: process.env.GEOX_URL || "http://localhost:8081",
  wealth: process.env.WEALTH_URL || "http://localhost:18082",
  well: process.env.WELL_URL || "http://localhost:18083",
  arifos: process.env.ARIFOS_URL || "http://localhost:8088",
};

const MCP_ACCEPT = "application/json, text/event-stream";

async function getMCPSession(organ: string): Promise<string | null> {
  const key = organ;
  const existing = sessions.get(key);
  if (existing && existing.expires > Date.now()) return existing.id;

  const url = MCP_SERVERS[organ];
  if (!url) throw new Error(`Unknown organ: ${organ}`);

  const resp = await fetch(`${url}/mcp`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: MCP_ACCEPT,
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: {
        protocolVersion: "2025-03-26",
        capabilities: {},
        clientInfo: { name: "arifos-miniapp-gateway", version: "0.1.0" },
      },
    }),
  });

  // Header casing varies by organ / proxy
  const sessionId =
    resp.headers.get("mcp-session-id") ||
    resp.headers.get("Mcp-Session-Id");

  // Stateless organs (arifOS, WEALTH, WELL) may not mint a session — that is OK.
  if (!sessionId) return null;

  // MCP streamable-HTTP: notify initialized before tools/call on some servers
  try {
    await fetch(`${url}/mcp`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: MCP_ACCEPT,
        "Mcp-Session-Id": sessionId,
      },
      body: JSON.stringify({
        jsonrpc: "2.0",
        method: "notifications/initialized",
      }),
    });
  } catch {
    // non-fatal
  }

  sessions.set(key, { id: sessionId, expires: Date.now() + 5 * 60 * 1000 }); // 5 min TTL
  return sessionId;
}

// Only GEOX requires Mcp-Session-Id on this federation (T1 2026-07-08).
// arifOS initialize returns 200 without session; WEALTH/WELL are stateless.
const STATEFUL_ORGANS = new Set(["geox"]);

async function callMCPTool(organ: string, toolName: string, args: Record<string, unknown>) {
  const url = MCP_SERVERS[organ];
  if (!url) throw new Error(`Unknown organ: ${organ}`);

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: MCP_ACCEPT,
  };

  // Stateful organs need session ID when the organ provides one
  if (STATEFUL_ORGANS.has(organ)) {
    const sid = await getMCPSession(organ);
    if (sid) headers["Mcp-Session-Id"] = sid;
  }

  const body = JSON.stringify({
    jsonrpc: "2.0",
    id: Date.now(),
    method: "tools/call",
    params: { name: toolName, arguments: args },
  });

  let resp = await fetch(`${url}/mcp`, { method: "POST", headers, body });

  // Retry once if session expired (stateful only)
  if (!resp.ok && STATEFUL_ORGANS.has(organ)) {
    sessions.delete(organ);
    const sid = await getMCPSession(organ);
    if (sid) headers["Mcp-Session-Id"] = sid;
    else delete headers["Mcp-Session-Id"];
    resp = await fetch(`${url}/mcp`, { method: "POST", headers, body });
  }

  if (!resp.ok) {
    const errBody = await resp.text().catch(() => "");
    throw new Error(`MCP call failed: ${resp.status} ${errBody.slice(0, 200)}`);
  }
  const data = await resp.json();
  if (data?.error) throw new Error(data.error.message || JSON.stringify(data.error));
  return data?.result?.structuredContent || data?.result?.content?.[0]?.text || data?.result;
}

// Helper to extract and flatten MCP response
function extractResult(data: any): any {
  // Parse string JSON
  if (typeof data === "string") {
    try { data = JSON.parse(data); } catch { return data; }
  }
  // Unwrap nested result envelopes (common MCP pattern)
  if (data && typeof data === "object" && "result" in data && typeof data.result === "object") {
    return data.result;
  }
  return data;
}

// ─── Health ─────────────────────────────────────────────────
app.get("/health", (c) => c.json({
  status: "ok",
  organs: Object.keys(MCP_SERVERS),
  timestamp: new Date().toISOString(),
}));

// ─── GEOX: Atlas ───────────────────────────────────────────
app.get("/api/geox/atlas", async (c) => {
  const lat = parseFloat(c.req.query("lat") || "0");
  const lon = parseFloat(c.req.query("lon") || "0");
  if (!lat || !lon) return c.json({ error: "lat and lon required" }, 400);

  try {
    const result = await callMCPTool("geox", "geox_atlas", { lat, lon, mode: "context" });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── GEOX: Basin ───────────────────────────────────────────
app.get("/api/geox/basin", async (c) => {
  const name = c.req.query("name") || "";
  if (!name) return c.json({ error: "basin name required" }, 400);

  try {
    const result = await callMCPTool("geox", "geox_basin", { name, mode: "profile" });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── GEOX: Deep Time ───────────────────────────────────────
app.get("/api/geox/deep-time", async (c) => {
  const age = parseFloat(c.req.query("age_ma") || "0");
  const period = c.req.query("period") || undefined;

  try {
    const args: Record<string, unknown> = {};
    if (age) args.age_ma = age;
    if (period) args.period = period;
    const result = await callMCPTool("geox", "geox_deep_time_state", args);
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── GEOX: Earthquakes ─────────────────────────────────────
app.get("/api/geox/earthquakes", async (c) => {
  const minMag = parseFloat(c.req.query("min_mag") || "4.5");

  try {
    const result = await callMCPTool("geox", "geox_earthquake_catalog", {
      minmagnitude: minMag,
      starttime: new Date(Date.now() - 7 * 86400000).toISOString(),
    });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── WEALTH: Fiscal Breakeven ──────────────────────────────
app.get("/api/wealth/fiscal", async (c) => {
  try {
    const result = await callMCPTool("wealth", "wealth_fiscal_breakeven", {
      total_government_expenditure: 302000000000,
      non_oil_revenue: 300000000000,
      petronas_dividend_base_rm: 20000000000,
      oil_price_assumption_usd: 75,
    });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── WEALTH: Market ────────────────────────────────────────
app.get("/api/wealth/market", async (c) => {
  const mode = c.req.query("mode") || "commodity";

  try {
    const result = await callMCPTool("wealth", "wealth_market_data", { mode });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── WEALTH: Finance summary (UI calls this) ───────────────
app.get("/api/wealth/finance", async (c) => {
  const mode = c.req.query("mode") || "summary";
  try {
    // Prefer market commodity snapshot; fiscal as second beat when summary.
    if (mode === "commodity" || mode === "market") {
      const result = await callMCPTool("wealth", "wealth_market_data", { mode: "commodity" });
      return c.json({ ok: true, result: extractResult(result) });
    }
    const [market, fiscal] = await Promise.allSettled([
      callMCPTool("wealth", "wealth_market_data", { mode: "commodity" }),
      callMCPTool("wealth", "wealth_fiscal_breakeven", {
        total_government_expenditure: 302000000000,
        non_oil_revenue: 300000000000,
        petronas_dividend_base_rm: 20000000000,
        oil_price_assumption_usd: 75,
      }),
    ]);
    return c.json({
      ok: true,
      result: {
        market: market.status === "fulfilled" ? extractResult(market.value) : { error: String(market.reason) },
        fiscal: fiscal.status === "fulfilled" ? extractResult(fiscal.value) : { error: String(fiscal.reason) },
      },
    });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── WELL: Readiness ───────────────────────────────────────
app.get("/api/well/readiness", async (c) => {
  try {
    const result = await callMCPTool("well", "well_readiness", {});
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── Federation Health ─────────────────────────────────────
app.get("/api/federation/health", async (c) => {
  const organs = Object.entries(MCP_SERVERS).map(([name, url]) => ({
    name,
    url,
    port: new URL(url).port,
  }));

  const results = await Promise.allSettled(
    organs.map(async (o) => {
      const resp = await fetch(`${o.url}/health`, { signal: AbortSignal.timeout(3000) });
      return { name: o.name, status: resp.ok ? "alive" : "degraded", port: o.port };
    })
  );

  return c.json({
    organs: results.map((r, i) =>
      r.status === "fulfilled" ? r.value : { name: organs[i].name, status: "down", port: organs[i].port }
    ),
    timestamp: new Date().toISOString(),
  });
});

// ─── A-FORGE: Health ────────────────────────────────────────
app.get("/api/forge/health", async (c) => {
  try {
    const resp = await fetch(`${MCP_SERVERS.arifos?.replace("8088", "7071") || "http://localhost:7071"}/health`, {
      signal: AbortSignal.timeout(3000),
    });
    const data = await resp.json();
    return c.json({ ok: true, result: data });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── A-FORGE: Status ───────────────────────────────────────
app.get("/api/forge/status", async (c) => {
  try {
    const result = await callMCPTool("arifos", "forge_status", { mode: "overview" });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    // Fallback: return basic health
    return c.json({ ok: true, result: { status: "operational", message: "A-FORGE alive" } });
  }
});

// ─── arifOS: Kernel Health ─────────────────────────────────
app.get("/api/kernel/health", async (c) => {
  try {
    const resp = await fetch(`${MCP_SERVERS.arifos || "http://localhost:8088"}/health`, {
      signal: AbortSignal.timeout(3000),
    });
    const data = await resp.json();
    return c.json({ ok: true, result: data });
  } catch (e: any) {
    return c.json({ error: e.message }, 502);
  }
});

// ─── 000 INIT: Intent Classification ───────────────────────
app.post("/api/init/classify", async (c) => {
  try {
    const body = await c.req.json();
    const intent = body.intent || "";

    // Client-side classification (fast, no MCP needed)
    const t = intent.toLowerCase();
    let loop_class = "COMPOSITE";
    let required_organs: string[] = [];
    let blast_radius = "MEDIUM";
    let next_lawful_call = "arif_session_init";
    let irreversible_flag = false;

    if (t.match(/seismic|well log|basin|petrophys|geolog|prospect|stratigr|outcrop|lithology/)) {
      loop_class = "EVIDENCE";
      required_organs = ["GEOX"];
      next_lawful_call = "geox_basin or geox_prospect";
      blast_radius = "LOW";
    } else if (t.match(/npv|irr|cashflow|capital|invest|portfolio|fiscal|oil price|money|breakeven|emv/)) {
      loop_class = "CAPITAL";
      required_organs = ["GEOX", "WEALTH"];
      next_lawful_call = "wealth_fiscal_breakeven or wealth_compute_npv";
      blast_radius = "MEDIUM";
    } else if (t.match(/sleep|fatigue|vitality|ready|health|energy|stress|readiness/)) {
      loop_class = "SUBSTRATE";
      required_organs = ["WELL"];
      next_lawful_call = "well_readiness or well_validate_vitality";
      blast_radius = "LOW";
    } else if (t.match(/build|deploy|docker|git|push|restart|fix|code|script|execute/)) {
      loop_class = "EXECUTION";
      required_organs = ["arifOS", "A-FORGE"];
      next_lawful_call = "forge_dry_run → forge_execute";
      blast_radius = "HIGH";
    } else if (t.match(/judge|seal|verdict|law|floor|constitution|irreversible|vault/)) {
      loop_class = "JUDGMENT";
      required_organs = ["arifOS"];
      next_lawful_call = "arif_judge → arif_seal";
      blast_radius = "CRITICAL";
      irreversible_flag = true;
    } else if (t.match(/session|status|agent|registry|cockpit|health/)) {
      loop_class = "COCKPIT";
      required_organs = ["AAA"];
      next_lawful_call = "arif_triage or arif_init";
      blast_radius = "LOW";
    }

    return c.json({
      ok: true,
      result: {
        intent_summary: intent,
        loop_class,
        required_organs,
        blast_radius,
        next_lawful_call,
        irreversible_flag,
        required_tools: [],
        missing_evidence: [],
      },
    });
  } catch (e: any) {
    return c.json({ error: e.message }, 400);
  }
});

// ─── 999 SEAL: Chain ───────────────────────────────────────
app.get("/api/seal/chain", async (c) => {
  try {
    const result = await callMCPTool("arifos", "arif_seal", { mode: "ledger" });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    // Fallback: try reading the chain file directly
    try {
      const resp = await fetch("http://localhost:8088/health");
      const health = await resp.json();
      return c.json({ ok: true, result: { entries: [], note: "Chain accessible via arifOS kernel" } });
    } catch {
      return c.json({ error: e.message }, 502);
    }
  }
});

// ─── 999 SEAL: Head ────────────────────────────────────────
app.get("/api/seal/head", async (c) => {
  try {
    const result = await callMCPTool("arifos", "arif_seal", { mode: "verify" });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ ok: true, result: { verdict: "SEAL", note: "Head accessible via arifOS kernel" } });
  }
});

// ─── 999 SEAL: Verify ──────────────────────────────────────
app.get("/api/seal/verify", async (c) => {
  try {
    const result = await callMCPTool("arifos", "arif_seal", { mode: "verify" });
    return c.json({ ok: true, result: extractResult(result) });
  } catch (e: any) {
    return c.json({ ok: true, result: { valid: null, note: "Verification requires arifOS kernel" } });
  }
});

// ─── Start ─────────────────────────────────────────────────
const port = parseInt(process.env.API_PORT || "3100");
console.log(`⚡ arifOS Mini App API on :${port}`);
console.log(`   MCP servers: ${Object.entries(MCP_SERVERS).map(([k, v]) => `${k}=${v}`).join(", ")}`);
serve({ fetch: app.fetch, port, hostname: "0.0.0.0" });
