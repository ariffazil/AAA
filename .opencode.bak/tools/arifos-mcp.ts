import { tool } from "@opencode-ai/plugin"
import { z } from "zod"

export default tool({
  description: "Call the arifOS MCP public endpoint for constitutional evaluation and tool execution. Use this to list tools, check health, and call arifOS governance tools (arif_judge_deliberate, arif_vault_seal, etc.)",
  schema: z.object({
    path: z.string().default("/tools").describe("MCP endpoint path"),
    method: z.enum(["GET", "POST"]).default("GET").describe("HTTP method"),
    body: z.record(z.any()).optional().describe("Request body for POST"),
  }),
  async execute({ path, method, body }, ctx) {
    const base = "https://mcp.arif-fazil.com"
    const url = `${base}${path}`

    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: method === "POST" ? JSON.stringify(body ?? {}) : undefined,
    })

    const text = await res.text()
    let json: any = null
    try { json = JSON.parse(text) } catch { /* plain text */ }

    return {
      url,
      status: res.status,
      ok: res.ok,
      json,
      raw: text,
    }
  }
})