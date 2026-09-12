/**
 * OpenClaw Orchestrator — Node.js Subprocess Adapter v0.1.0
 *
 * Narrow, allowlisted subprocess bridge from OpenClaw Node.js gateway
 * to Python orchestrator CLI. One specific tool contract. No generic spawn.
 *
 * Capability contract:
 *   - Fixed command path (allowlisted)
 *   - Fixed capability IDs (allowlisted)
 *   - JSON stdin → JSON stdout
 *   - Timeout + output size cap
 *   - No shell interpolation
 *   - No URL/network input
 *   - Path traversal rejection
 *
 * Forged: 2026-09-12 by 333-AGI under F13 directive
 * DITEMPA BUKAN DIBERI
 */

import { spawn } from "node:child_process";
import path from "node:path";

// ─── Constants ──────────────────────────────────────────────────────

const ORCHESTRATOR_CLI = "/root/AAA/agents/openclaw/runtime/orchestrator_cli.py";
const PYTHON = "python3";

const TIMEOUT_MS = 30_000;          // 30s max per call
const MAX_STDOUT_BYTES = 2_000_000; // 2MB max output
const MAX_STDERR_BYTES = 50_000;    // 50KB max stderr

/** Allowlisted capability IDs — nothing else is accepted. */
const ALLOWED_CAPABILITIES = new Set([
  "openclaw.orchestrator.classify",
  "openclaw.orchestrator.classify_multi",
  "openclaw.orchestrator.dag_define",
  "openclaw.orchestrator.dag_execute",
  "openclaw.orchestrator.dag_template",
  "openclaw.orchestrator.state_get",
  "openclaw.orchestrator.health",
]);

// ─── Types ──────────────────────────────────────────────────────────

export type OrchestratorRequest = {
  capabilityId: string;
  query?: string;
  personId?: string;
  context?: Record<string, unknown>;
  flow?: Record<string, unknown>;
  flowId?: string;
  dryRun?: boolean;
  template?: string;
  variables?: Record<string, unknown>;
};

export type OrchestratorResponse = {
  status: "success" | "failed";
  capabilityId: string;
  result?: unknown;
  intents?: unknown[];
  latencyMs?: number;
  error?: string;
  errorClass?: string;
  safeMessage?: string;
};

// ─── Validation ─────────────────────────────────────────────────────

function validateRequest(req: OrchestratorRequest): string | null {
  // 1. Capability allowlist
  if (!ALLOWED_CAPABILITIES.has(req.capabilityId)) {
    return `CAPABILITY_DENIED: ${req.capabilityId}`;
  }

  // 2. Query validation for classify capabilities
  if (
    req.capabilityId === "openclaw.orchestrator.classify" ||
    req.capabilityId === "openclaw.orchestrator.classify_multi"
  ) {
    if (!req.query) return "MISSING_FIELD: query";
    if (req.query.length > 10000) return "QUERY_TOO_LONG";
    // Reject shell metacharacters (semicolon, pipe, ampersand, dollar, backtick)
    if (/[;|&$`]/.test(req.query)) return "DANGEROUS_CHARACTERS";
  }

  // 3. Flow validation for dag_define
  if (req.capabilityId === "openclaw.orchestrator.dag_define") {
    if (!req.flow) return "MISSING_FIELD: flow";
    if (!req.flow.tasks || !Array.isArray(req.flow.tasks)) return "MISSING_FIELD: flow.tasks";
    if (req.flow.tasks.length > 20) return "TOO_MANY_TASKS";
    for (let i = 0; i < req.flow.tasks.length; i++) {
      const task = req.flow.tasks[i] as Record<string, unknown>;
      if (!task.id) return `MISSING_FIELD: flow.tasks[${i}].id`;
      if (!task.agent) return `MISSING_FIELD: flow.tasks[${i}].agent`;
    }
  }

  // 4. Flow ID validation for dag_execute
  if (req.capabilityId === "openclaw.orchestrator.dag_execute") {
    if (!req.flowId) return "MISSING_FIELD: flowId";
    if (req.flowId.includes("..") || req.flowId.includes("/")) return "INVALID_FIELD: flowId traversal";
  }

  // 5. No URLs anywhere in the request
  const jsonStr = JSON.stringify(req);
  if (/https?:\/\//.test(jsonStr)) return "URL_NOT_ALLOWED";

  return null; // valid
}

// ─── Subprocess Execution ───────────────────────────────────────────

function spawnBoundedJson(
  command: string,
  args: string[],
  input: string,
  options: {
    timeoutMs: number;
    maxStdoutBytes: number;
    maxStderrBytes: number;
  }
): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      stdio: ["pipe", "pipe", "pipe"],
      timeout: options.timeoutMs,
      env: {
        PATH: "/usr/bin:/bin:/usr/local/bin",
        HOME: "/root",
        PYTHONUNBUFFERED: "1",
        NO_PROXY: "*",
      },
      cwd: "/root/AAA",
    });

    let stdout = "";
    let stderr = "";
    let stdoutBytes = 0;
    let stderrBytes = 0;
    let killed = false;

    child.stdout.on("data", (chunk: Buffer) => {
      stdoutBytes += chunk.length;
      if (stdoutBytes > options.maxStdoutBytes) {
        if (!killed) {
          killed = true;
          child.kill("SIGKILL");
          reject(new Error("STDOUT_LIMIT_EXCEEDED"));
        }
        return;
      }
      stdout += chunk.toString();
    });

    child.stderr.on("data", (chunk: Buffer) => {
      stderrBytes += chunk.length;
      if (stderrBytes > options.maxStderrBytes) {
        // Don't kill for stderr overflow, just truncate
        return;
      }
      stderr += chunk.toString();
    });

    child.on("error", (err) => {
      reject(new Error(`SPAWN_ERROR: ${err.message}`));
    });

    child.on("close", (code) => {
      if (killed) return; // already rejected
      resolve({ stdout, stderr, exitCode: code ?? 1 });
    });

    // Write input and close stdin
    child.stdin.write(input);
    child.stdin.end();
  });
}

// ─── Public API ─────────────────────────────────────────────────────

/**
 * Run the orchestrator via allowlisted subprocess.
 * This is the ONE entry point the Node.js gateway should call.
 */
export async function runOrchestrator(
  req: OrchestratorRequest
): Promise<OrchestratorResponse> {
  // 1. Validate request
  const validationError = validateRequest(req);
  if (validationError) {
    return {
      status: "failed",
      capabilityId: req.capabilityId,
      error: validationError,
      errorClass: "VALIDATION_ERROR",
      safeMessage: "Request validation failed. Check capability ID and input fields.",
    };
  }

  // 2. Build stdin payload (canonicalize — no extra fields)
  const stdinPayload: Record<string, unknown> = {
    capability_id: req.capabilityId,
  };
  if (req.query !== undefined) stdinPayload.query = req.query;
  if (req.personId !== undefined) stdinPayload.person_id = req.personId;
  if (req.context !== undefined) stdinPayload.context = req.context;
  if (req.flow !== undefined) stdinPayload.flow = req.flow;
  if (req.flowId !== undefined) stdinPayload.flow_id = req.flowId;
  if (req.dryRun !== undefined) stdinPayload.dry_run = req.dryRun;
  if (req.template !== undefined) stdinPayload.template = req.template;
  if (req.variables !== undefined) stdinPayload.variables = req.variables;

  const inputJson = JSON.stringify(stdinPayload);

  // 3. Spawn subprocess
  try {
    const { stdout, stderr, exitCode } = await spawnBoundedJson(
      PYTHON,
      [ORCHESTRATOR_CLI],
      inputJson,
      {
        timeoutMs: TIMEOUT_MS,
        maxStdoutBytes: MAX_STDOUT_BYTES,
        maxStderrBytes: MAX_STDERR_BYTES,
      }
    );

    // 4. Parse output
    if (exitCode === 2) {
      // Validation failure
      try {
        const parsed = JSON.parse(stdout);
        return {
          status: "failed",
          capabilityId: req.capabilityId,
          error: parsed.error || "Validation failure",
          errorClass: "VALIDATION_ERROR",
          safeMessage: "Input validation failed.",
        };
      } catch {
        return {
          status: "failed",
          capabilityId: req.capabilityId,
          error: "Validation failure (unparseable output)",
          errorClass: "VALIDATION_ERROR",
          safeMessage: "Input validation failed.",
        };
      }
    }

    if (exitCode !== 0) {
      return {
        status: "failed",
        capabilityId: req.capabilityId,
        error: `Process exited with code ${exitCode}`,
        errorClass: "PROCESS_ERROR",
        safeMessage: "Orchestrator process failed.",
      };
    }

    // 5. Parse successful output
    try {
      const parsed = JSON.parse(stdout) as OrchestratorResponse;
      return parsed;
    } catch {
      return {
        status: "failed",
        capabilityId: req.capabilityId,
        error: "Invalid JSON output from orchestrator",
        errorClass: "OUTPUT_ERROR",
        safeMessage: "Orchestrator returned invalid response.",
      };
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return {
      status: "failed",
      capabilityId: req.capabilityId,
      error: message,
      errorClass: "ADAPTER_ERROR",
      safeMessage: "Subprocess execution failed.",
    };
  }
}

// ─── Convenience Functions ──────────────────────────────────────────

/** Classify a single query intent. */
export async function classifyIntent(
  query: string,
  personId?: string
): Promise<OrchestratorResponse> {
  return runOrchestrator({
    capabilityId: "openclaw.orchestrator.classify",
    query,
    personId,
  });
}

/** Classify multi-intent query. */
export async function classifyMultiIntents(
  query: string,
  personId?: string
): Promise<OrchestratorResponse> {
  return runOrchestrator({
    capabilityId: "openclaw.orchestrator.classify_multi",
    query,
    personId,
  });
}

/** Define a DAG workflow. */
export async function defineWorkflow(
  flow: Record<string, unknown>
): Promise<OrchestratorResponse> {
  return runOrchestrator({
    capabilityId: "openclaw.orchestrator.dag_define",
    flow,
  });
}

/** Execute a DAG workflow (dry run or live). */
export async function executeWorkflow(
  flowId: string,
  dryRun?: boolean
): Promise<OrchestratorResponse> {
  return runOrchestrator({
    capabilityId: "openclaw.orchestrator.dag_execute",
    flowId,
    dryRun,
  });
}

/** Create workflow from template. */
export async function createFromTemplate(
  template: string,
  variables?: Record<string, unknown>
): Promise<OrchestratorResponse> {
  return runOrchestrator({
    capabilityId: "openclaw.orchestrator.dag_template",
    template,
    variables,
  });
}

/** Get orchestrator health. */
export async function getHealth(): Promise<OrchestratorResponse> {
  return runOrchestrator({
    capabilityId: "openclaw.orchestrator.health",
  });
}
