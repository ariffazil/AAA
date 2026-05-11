/**
 * A2A Client — OpenClaw unified ACP client for AAA Gateway
 * Protocol: A2A v1.0.0 (JSON-RPC 2.0)
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

export interface A2APart {
  kind: "text" | "file" | "data";
  text?: string;
  data?: Record<string, unknown>;
  file?: { name?: string; mimeType: string; bytes?: string; uri?: string };
}

export interface A2AMessage {
  role: "user" | "agent";
  parts: A2APart[];
  messageId: string;
  taskId?: string;
  contextId?: string;
}

export interface A2ATaskStatus {
  state: "submitted" | "working" | "completed" | "failed" | "canceled" | "pending-human-review" | "input-required";
  message?: A2AMessage;
  timestamp?: string;
}

export interface A2ATask {
  id: string;
  contextId: string;
  status: A2ATaskStatus;
  artifacts: Array<{
    artifactId: string;
    name: string;
    parts: A2APart[];
  }>;
  history: A2AMessage[];
  metadata: Record<string, unknown>;
}

export interface JsonRpcRequest {
  jsonrpc: "2.0";
  id: string | number;
  method: string;
  params: Record<string, unknown>;
}

export interface JsonRpcSuccess<T> {
  jsonrpc: "2.0";
  id: string | number | null;
  result: T;
  error?: never;
}

export interface JsonRpcError {
  jsonrpc: "2.0";
  id: string | number | null;
  result?: never;
  error: {
    code: number;
    message: string;
    data?: Record<string, unknown>;
  };
}

export type JsonRpcResponse<T> = JsonRpcSuccess<T> | JsonRpcError;

export type Verdict = "SEAL" | "HOLD_888" | "VOID" | "pending-human-review";

export interface A2ASendOptions {
  taskId?: string;
  contextId?: string;
  a2aVersion?: string;
  authToken?: string;
  apiKey?: string;
}

export class A2AClient {
  private baseUrl: string;
  private defaultAuthToken: string;
  private defaultApiKey: string;

  constructor(baseUrl: string, authToken?: string, apiKey?: string) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.defaultAuthToken = authToken || process.env.A2A_TOKEN || "aaa-a2a-token-dev";
    this.defaultApiKey = apiKey || process.env.A2A_API_KEY || "aaa-a2a-apikey-dev";
  }

  private async rpc<T>(
    method: string,
    params: Record<string, unknown>,
    options: A2ASendOptions = {}
  ): Promise<JsonRpcResponse<T>> {
    const token = options.authToken ?? this.defaultAuthToken;
    const apiKey = options.apiKey ?? this.defaultApiKey;
    const version = options.a2aVersion ?? "1.0";

    const response = await fetch(`${this.baseUrl}/a2a/message/send`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "A2A-Version": version,
        "Authorization": `Bearer ${token}`,
        "x-a2a-key": apiKey,
      },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: `openclaw-${Date.now()}`,
        method,
        params,
      } as JsonRpcRequest),
    });

    if (!response.ok) {
      throw new Error(`A2A HTTP ${response.status}: ${await response.text()}`);
    }

    return response.json() as JsonRpcResponse<T>;
  }

  /**
   * Send a task to AAA Gateway and get 888_JUDGE verdict
   */
  async sendTask(
    text: string,
    options: A2ASendOptions = {}
  ): Promise<{ task: A2ATask; verdict: Verdict }> {
    const messageId = `openclaw-${Date.now()}`;
    const taskId = options.taskId || `openclaw-task-${messageId}`;
    const contextId = options.contextId || `openclaw-ctx-${messageId}`;

    const result = await this.rpc<{ id: string; contextId: string; status: A2ATaskStatus }>(
      "SendMessage",
      {
        message: {
          role: "user",
          parts: [{ kind: "text", text }],
          messageId,
          taskId,
          contextId,
        },
      },
      options
    );

    if ("error" in result) {
      throw new Error(`A2A Error ${result.error.code}: ${result.error.message}`);
    }

    const task: A2ATask = {
      id: result.result.id,
      contextId: result.result.contextId,
      status: result.result.status,
      artifacts: [],
      history: [],
      metadata: {},
    };

    const verdict = this.extractVerdict(task.status);
    return { task, verdict };
  }

  /**
   * Poll for task status
   */
  async getTask(
    taskId: string,
    options: A2ASendOptions = {}
  ): Promise<A2ATask> {
    const token = options.authToken ?? this.defaultAuthToken;
    const apiKey = options.apiKey ?? this.defaultApiKey;

    const response = await fetch(`${this.baseUrl}/a2a/tasks/${taskId}`, {
      headers: {
        "Authorization": `Bearer ${token}`,
        "x-a2a-key": apiKey,
      },
    });

    if (!response.ok) {
      throw new Error(`A2A HTTP ${response.status}: ${await response.text()}`);
    }

    const data = await response.json();
    return data as A2ATask;
  }

  /**
   * Cancel a pending task
   */
  async cancelTask(
    taskId: string,
    options: A2ASendOptions = {}
  ): Promise<A2ATask> {
    const result = await this.rpc<A2ATask>(
      "CancelTask",
      { id: taskId },
      options
    );

    if ("error" in result) {
      throw new Error(`A2A Error ${result.error.code}: ${result.error.message}`);
    }

    return result.result;
  }

  /**
   * Extract verdict from task status
   */
  private extractVerdict(status: A2ATaskStatus): Verdict {
    const text = status.message?.parts
      .filter((p) => p.kind === "text")
      .map((p) => p.text || "")
      .join(" ") || "";

    if (text.includes("HOLD_888") || status.state === "pending-human-review") {
      return "HOLD_888";
    }
    if (text.includes("VOID") || status.state === "failed") {
      return "VOID";
    }
    if (text.includes("SEAL") || status.state === "completed") {
      return "SEAL";
    }
    return status.state as Verdict;
  }

  /**
   * Get AAA Gateway agent card (public, no auth)
   */
  static async getAgentCard(baseUrl: string): Promise<Record<string, unknown>> {
    const response = await fetch(`${baseUrl.replace(/\/$/, "")}/.well-known/agent-card.json`);
    if (!response.ok) {
      throw new Error(`Failed to fetch agent card: ${response.status}`);
    }
    return response.json();
  }
}

// === USAGE EXAMPLE ===
// const client = new A2AClient(
//   "http://localhost:3001",
//   "aaa-a2a-token-dev",
//   "aaa-a2a-apikey-dev"
// );
//
// const { task, verdict } = await client.sendTask(
//   "openclaw task: summarize system health across arifOS federation"
// );
//
// if (verdict === "SEAL") {
//   // Execute
// } else if (verdict === "HOLD_888") {
//   // Queue for human review
// } else if (verdict === "VOID") {
//   // Block
// }
