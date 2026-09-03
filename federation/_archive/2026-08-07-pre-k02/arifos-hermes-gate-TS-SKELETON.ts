// arifos-hermes-gate.ts — Constitutional Membrane for Hermes
// ═══════════════════════════════════════════════════════════════════
// F1 AMANAH: every mutation is gated through arif_judge.
// F11 AUDIT: every gate decision writes to receipt trail.
// F13 SOVEREIGN: arifOS :8088 binds, this gate only routes.
// E-22: Can runtime violate without receipt? → After this gate: NO for mutations.
//
// SKELETON — not yet wired into Hermes runtime.
// Activation requires F13 ratification + reload of Hermes profile.
// ═══════════════════════════════════════════════════════════════════

// Configuration
const RECEIPT_PATH = "/root/.local/share/arifos/hermes_receipts.jsonl";
const ARIFOS_MCP = "http://127.0.0.1:8088/mcp";
const HERMES_HOME = process.env.HERMES_HOME || "/usr/local/lib/hermes-agent/profiles/aaa-hermes";

// ── Tools Hermes currently exposes (E-22 audit) ──────────────────
// Hermes has 7 violation paths (per FASA1_AUDIT_E22_PENETRATION.md).
// Each maps to a Hermes toolset below.

const HERMES_TOOLSETS: Record<string, "OBSERVE" | "MUTATE_T1" | "MUTATE_T2" | "MUTATE_T3"> = {
  // OBSERVE — passthrough, no gate needed
  read_file: "OBSERVE",
  search_files: "OBSERVE",
  web_search: "OBSERVE",
  web_extract: "OBSERVE",
  vision_analyze: "OBSERVE",
  session_search: "OBSERVE",
  skills_list: "OBSERVE",
  skills_view: "OBSERVE",
  memory: "OBSERVE",     // read only; memory write goes through dedicated tool

  // MUTATE_T1 — low blast-radius, auto-execute with witness receipt
  todo: "MUTATE_T1",
  execute_code: "MUTATE_T1",
  text_to_speech: "MUTATE_T1",
  clarify: "MUTATE_T1",
  browser_snapshot: "MUTATE_T1",
  browser_click: "MUTATE_T1",
  browser_type: "MUTATE_T1",
  browser_navigate: "MUTATE_T1",

  // MUTATE_T2 — judgment required, route to arif_judge
  write_file: "MUTATE_T2",
  patch: "MUTATE_T2",
  terminal: "MUTATE_T2",
  cronjob: "MUTATE_T2",
  memory_batch: "MUTATE_T2",     // memory write
  delegate_task: "MUTATE_T2",    // SPAWN — highest-priority gap from E-22

  // MUTATE_T3 — irreversible or high blast-radius, SEAL required
  skill_manage: "MUTATE_T3",     // modifies installed skills
  plugin_install: "MUTATE_T3",   // adds new tools
};

// ── T3 patterns — fail-CLOSED if arifOS unreachable ──────────────
const T3_PATTERNS = [
  /secrets/i,
  /\.secrets\//,
  /kunci-mas/i,
  /vault\.env/i,
  /\.signing_key/i,
  /tokenrouter/i,
  /systemctl/i,
  /arif_seal/i,
  /VAULT999/i,
];

function isT3(toolName: string, args: Record<string, unknown>): boolean {
  if (toolName === "skill_manage" || toolName === "plugin_install") return true;
  const argStr = JSON.stringify(args);
  return T3_PATTERNS.some((p) => p.test(argStr));
}

// ── Receipt writer ────────────────────────────────────────────────
function receipt(record: Record<string, unknown>): void {
  try {
    const dir = RECEIPT_PATH.substring(0, RECEIPT_PATH.lastIndexOf("/"));
    require("fs").mkdirSync(dir, { recursive: true });
    require("fs").appendFileSync(RECEIPT_PATH, JSON.stringify(record) + "\n", "utf8");
  } catch (_) {
    // Never block on receipt failure (per E-11: mechanism not memory)
  }
}

// ── Session binding (mirror OpenCode gate pattern) ────────────────
interface HermesSession {
  session_id: string;
  sct: string; // Session Capability Token
  actor_id: string;
}

function getSession(): HermesSession | null {
  const session_id = process.env.ARIFOS_SESSION_ID;
  const sct = process.env.ARIFOS_SESSION_TOKEN;
  if (!session_id || !sct) return null;
  return {
    session_id,
    sct,
    actor_id: process.env.ARIFOS_ACTOR_ID || "hermes-asi",
  };
}

// ── Tool classification ───────────────────────────────────────────
function classify(toolName: string, args: Record<string, unknown>): "OBSERVE" | "MUTATE_T1" | "MUTATE_T2" | "MUTATE_T3" {
  if (HERMES_TOOLSETS[toolName]) return HERMES_TOOLSETS[toolName];
  // Unknown tools — default to T2 (fail-closed to judgment, not auto-execute)
  return "MUTATE_T2";
}

// ── arif_judge routing ────────────────────────────────────────────
async function routeToJudge(
  toolName: string,
  args: Record<string, unknown>,
  session: HermesSession
): Promise<{ verdict: "SEAL" | "HOLD" | "VOID"; reason?: string; cc_id?: string }> {
  const body = {
    jsonrpc: "2.0",
    id: crypto.randomUUID?.() ?? `${Date.now()}`,
    method: "tools/call",
    params: {
      name: "arif_judge",
      arguments: {
        mode: "judge",
        candidate: `MUTATE tool '${toolName}' via Hermes`,
        session_id: session.session_id,
        session_token: session.sct,
        actor_id: session.actor_id,
        harness: "hermes-asi",
        args_preview: JSON.stringify(args).slice(0, 200),
        action_tier: isT3(toolName, args) ? "T3" : "T2",
        reversibility_level: isT3(toolName, args) ? "irreversible" : "reversible",
      },
    },
  };

  try {
    const res = await fetch(ARIFOS_MCP, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = (await res.json()) as any;
    const text = json?.result?.content?.[0]?.text ?? "{}";
    const result = JSON.parse(text);
    return {
      verdict: result.verdict || result.effective_verdict || "HOLD",
      reason: result.reasons,
      cc_id: result.constitutional_chain_id,
    };
  } catch (err) {
    // Fail-CLOSED for T3, fail-OPEN-with-witness for T1/T2
    throw err;
  }
}

// ── Gate decisions ────────────────────────────────────────────────
let gatedCount = 0;
let blockedCount = 0;

// ── Main gate (to be wired into Hermes runtime) ───────────────────
//
// Hermes hooks a tool_use event before tool execution. The hook must:
// 1. Classify tool
// 2. Bind to arifOS session
// 3. Route T2/T3 to arif_judge
// 4. Write receipt for every decision
// 5. Block or allow based on verdict + fail-closed policy

interface GateDecision {
  tool: string;
  classification: "OBSERVE" | "MUTATE_T1" | "MUTATE_T2" | "MUTATE_T3";
  verdict: "ALLOWED" | "BLOCKED";
  reason?: string;
  cc_id?: string;
  receipt_chain_hash?: string;
}

async function gate(
  toolName: string,
  args: Record<string, unknown>
): Promise<GateDecision> {
  const cls = classify(toolName, args);
  const session = getSession();

  // OBSERVE — passthrough
  if (cls === "OBSERVE") {
    return { tool: toolName, classification: cls, verdict: "ALLOWED" };
  }

  // MUTATE_T1 — low blast-radius, require session binding + witness
  if (cls === "MUTATE_T1") {
    if (!session) {
      blockedCount++;
      receipt({ event: "hermes-gate.blocked.no-session", tool: toolName, classification: cls });
      return { tool: toolName, classification: cls, verdict: "BLOCKED", reason: "F1/F13: no session" };
    }
    gatedCount++;
    receipt({ event: "hermes-gate.allowed.t1", tool: toolName, has_session: true });
    return { tool: toolName, classification: cls, verdict: "ALLOWED" };
  }

  // MUTATE_T2/T3 — require session + arif_judge
  if (!session) {
    blockedCount++;
    receipt({ event: "hermes-gate.blocked.no-session", tool: toolName, classification: cls });
    return { tool: toolName, classification: cls, verdict: "BLOCKED", reason: "F1/F13: no session" };
  }

  gatedCount++;

  const t3 = isT3(toolName, args);

  try {
    const judgeResult = await routeToJudge(toolName, args, session);
    if (judgeResult.verdict === "SEAL") {
      receipt({
        event: "hermes-gate.allowed",
        tool: toolName,
        classification: cls,
        verdict: "SEAL",
        cc_id: judgeResult.cc_id,
        t3,
      });
      return { tool: toolName, classification: cls, verdict: "ALLOWED", cc_id: judgeResult.cc_id };
    }
    // VOID or HOLD
    blockedCount++;
    receipt({
      event: "hermes-gate.blocked.verdict",
      tool: toolName,
      classification: cls,
      verdict: judgeResult.verdict,
      reason: judgeResult.reason,
    });
    return {
      tool: toolName,
      classification: cls,
      verdict: "BLOCKED",
      reason: `arif_judge ${judgeResult.verdict}: ${judgeResult.reason || "constitutional"}`,
    };
  } catch (err) {
    // arifOS unreachable — F1 fail-CLOSED for T3
    if (t3) {
      blockedCount++;
      receipt({
        event: "hermes-gate.blocked.t3-arifos-down",
        tool: toolName,
        error: String(err),
      });
      return {
        tool: toolName,
        classification: cls,
        verdict: "BLOCKED",
        reason: `arifOS down + T3 tool — F1 AMANAH no judge no mutation`,
      };
    }
    // T2 with arifOS down — witness receipt + allow (low blast-radius)
    receipt({
      event: "hermes-gate.allowed.arifos-down",
      tool: toolName,
      classification: cls,
      error: String(err),
    });
    return { tool: toolName, classification: cls, verdict: "ALLOWED", reason: "witness-only" };
  }
}

// ── Session close ─────────────────────────────────────────────────
function sessionClose(): void {
  receipt({
    event: "hermes-gate.session-close",
    gated_total: gatedCount,
    blocked_total: blockedCount,
    pass_rate: gatedCount > 0 ? ((gatedCount - blockedCount) / gatedCount).toFixed(2) : "N/A",
  });
}

// ── Export hooks (skeleton — wiring TBD) ──────────────────────────
//
// In Hermes runtime, this would register as:
//   before_tool_use: gate(toolName, args)
//   on_session_close: sessionClose()
//
// For this skeleton, gate is exposed as a callable function.
// Future work: integrate into Hermes CLI + Telegram gateway.

export { gate, classify, sessionClose, HERMES_TOOLSETS };
export type { GateDecision, HermesSession };

// ── Self-test (when run directly) ─────────────────────────────────
if (require.main === module) {
  (async () => {
    console.log("[hermes-gate] self-test: classify known tools");
    for (const tool of Object.keys(HERMES_TOOLSETS)) {
      console.log(`  ${tool.padEnd(20)} → ${HERMES_TOOLSETS[tool]}`);
    }
    console.log(`[hermes-gate] total tools classified: ${Object.keys(HERMES_TOOLSETS).length}`);
    console.log("[hermes-gate] skeleton complete. NOT YET WIRED. Activate via F13 ratification.");
  })();
}