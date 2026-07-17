/**
 * MCP Apps Host Bridge — AAA Side (G3 double-iframe)
 * ==================================================
 * Host-side implementation of SEP-1865 ext-apps protocol.
 * Manages Sandbox Proxy lifecycle, ui:// resource resolution,
 * tool input/output relay, and governance envelope parsing.
 *
 * G3 (2026-07-12): Double-iframe architecture
 *   Host → Proxy iframe (allow-scripts + allow-same-origin, srcdoc)
 *        → Guest iframe (allow-scripts only, srcdoc of app HTML)
 * Escape vector (single iframe + same-origin) closed.
 *
 * Contracts:
 *   - Resolves ui://geox/well-desk → /mcp-apps/well-desk
 *   - Sends ui/notifications/tool-input, ui/notifications/tool-result via proxy
 *   - Receives tools/call, resources/read, ui/update-model-context from guest
 *   - Parses holds[], constraints{} from structuredContent.envelope
 *
 * DITEMPA BUKAN DIBERI
 */

import {
  ALLOWED_VIEW_METHODS,
  DEFAULT_GUEST_CSP,
  SANDBOX_METHODS,
  buildSandboxProxySrcdoc,
} from "./MCPAppsSandboxProxy";

// ── Types (mirrors arifOS envelope schema) ─────────────────────────────────

export type ArifOsPolicyState =
  | "observe"
  | "review_required"
  | "hold"
  | "veto"
  | "approved"
  | "rejected";

export interface ArifOsHold {
  code: string;
  reason: string;
  severity?: "low" | "medium" | "high" | "critical";
  blocking: boolean;
  requiredWitness?: Array<"human" | "ai" | "earth">;
  expiresAt?: string | null;
}

export interface ArifOsConstraintVeto {
  active: boolean;
  reason: string | null;
  authority: string | null;
}

export interface ArifOsConstraints {
  policyState: ArifOsPolicyState;
  disabledActions: string[];
  requiredFloors: string[];
  veto: ArifOsConstraintVeto;
}

export interface ArifOsAction {
  id: string;
  label: string;
  tool: string;
  arguments?: Record<string, unknown>;
  requiresConfirmation: boolean;
  requiredFloors?: string[];
}

export interface ArifOsEnvelope {
  schemaVersion: string;
  summary: string;
  viewModel: Record<string, unknown>;
  actions: ArifOsAction[];
  holds: ArifOsHold[];
  constraints: ArifOsConstraints;
  provenance: {
    sources: string[];
    confidence: number;
    epistemicTag: string;
    timestamp?: string;
  };
  telemetry?: Record<string, unknown>;
}

// ── UI Resource mapping ────────────────────────────────────────────────────

const UI_RESOURCE_ROOTS: Record<string, string> = {
  "geox/well-desk": "/mcp-apps/well-desk",
  "geox/earth-volume": "/mcp-apps/earth-volume",
  "geox/judge-console": "/mcp-apps/judge-console",
  "aforge/preview": "/mcp-apps/aforge-preview",
  "wealth/portfolio": "/mcp-apps/wealth-portfolio",
};

/** Resolve a ui:// URI to the AAA fetch path */
export function resolveUiResource(uri: string): string | null {
  if (!uri.startsWith("ui://")) return null;
  const key = uri.slice(5);
  return UI_RESOURCE_ROOTS[key] || null;
}

// ── MCP Apps Host Bridge ──────────────────────────────────────────────────

interface PendingRequest {
  resolve: (value: unknown) => void;
  reject: (reason?: unknown) => void;
  method: string;
}

type ToolArgs = Record<string, unknown>;
type JsonRpcId = string | number;

interface MountOptions {
  displayMode?: "inline" | "fullscreen";
  initialToolInput?: ToolArgs;
  onReady?: () => void;
  guestCsp?: string;
}

interface JsonRpcMessage {
  jsonrpc: "2.0";
  id?: JsonRpcId;
  method?: string;
  params?: Record<string, unknown>;
  result?: unknown;
  error?: { message?: string; code?: number };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === "object";
}

function parseJsonRpcMessage(value: unknown): JsonRpcMessage | null {
  let parsed: unknown = value;
  if (typeof value === "string") {
    try {
      parsed = JSON.parse(value) as unknown;
    } catch {
      return null;
    }
  }
  if (!isRecord(parsed) || parsed.jsonrpc !== "2.0") return null;
  return parsed as JsonRpcMessage;
}

function errorMessage(error: unknown, fallback = "Unknown error"): string {
  return error instanceof Error ? error.message : fallback;
}

export interface MCPAppInstance {
  appId: string;
  /** Outer Sandbox Proxy iframe (only window host posts to) */
  iframe: HTMLIFrameElement;
  container: HTMLElement;
  state: "initializing" | "ready" | "error" | "teardown";
  pendingRequests: Map<number, PendingRequest>;
  nextId: number;
  messageHandler?: (event: MessageEvent) => void;
  /** G3: true when double-iframe proxy is active */
  g3Sandbox: boolean;
  guestLoaded: boolean;
  fetchPath: string;
}

export class MCPAppsHostBridge {
  private apps: Map<string, MCPAppInstance> = new Map();
  private toolResultHandler: ((appId: string, result: unknown) => void) | null = null;
  private toolCallHandler:
    | ((appId: string, name: string, args: ToolArgs) => Promise<unknown>)
    | null = null;

  constructor(private hostElement: HTMLElement) {}

  onToolResult(handler: (appId: string, result: unknown) => void): void {
    this.toolResultHandler = handler;
  }

  onToolCall(handler: (appId: string, name: string, args: ToolArgs) => Promise<unknown>): void {
    this.toolCallHandler = handler;
  }

  /**
   * Mount an MCP App via G3 double-iframe Sandbox Proxy.
   */
  mountApp(appId: string, options?: MountOptions): MCPAppInstance {
    const fetchPath = UI_RESOURCE_ROOTS[`geox/${appId}`] || `/mcp-apps/${appId}`;

    const container = document.createElement("div");
    container.className = "mcp-app-container mcp-app-g3";
    container.dataset.appId = appId;
    container.dataset.g3 = "true";
    container.style.cssText =
      options?.displayMode === "fullscreen"
        ? "position:fixed;inset:0;z-index:9999;background:#000;"
        : "width:100%;height:100%;min-height:400px;position:relative;";

    // Outer Sandbox Proxy — allow-scripts only. No allow-same-origin.
    // Host fetches guest HTML; proxy only relays postMessage + creates inner iframe.
    // Guest (inner) also gets allow-scripts only — see buildSandboxProxySrcdoc().
    const iframe = document.createElement("iframe");
    iframe.dataset.appId = appId;
    iframe.dataset.role = "sandbox-proxy";
    iframe.style.cssText = "width:100%;height:100%;border:none;";
    iframe.setAttribute("sandbox", "allow-scripts");
    iframe.setAttribute("referrerpolicy", "no-referrer");
    iframe.srcdoc = buildSandboxProxySrcdoc();
    container.appendChild(iframe);
    this.hostElement.appendChild(container);

    const instance: MCPAppInstance = {
      appId,
      iframe,
      container,
      state: "initializing",
      pendingRequests: new Map(),
      nextId: 1,
      g3Sandbox: true,
      guestLoaded: false,
      fetchPath,
    };
    this.apps.set(appId, instance);

    this.wireMessageListener(instance, options);

    // Load guest HTML after proxy boots (sandbox-boot) or iframe load fallback
    const loadGuest = async () => {
      try {
        const res = await fetch(fetchPath, { credentials: "same-origin" });
        if (!res.ok) throw new Error(`fetch ${fetchPath} → ${res.status}`);
        const html = await res.text();
        this.postToProxy(instance, {
          jsonrpc: "2.0",
          method: "ui/notifications/sandbox-load",
          params: {
            html,
            csp: options?.guestCsp || DEFAULT_GUEST_CSP,
            appId,
          },
        });
      } catch (err: unknown) {
        instance.state = "error";
        console.error(`[MCP App:${appId}] guest load failed`, err);
      }
    };

    iframe.addEventListener("load", () => {
      // Proxy may have already sent sandbox-boot; re-send load after load event
      void loadGuest();
    });

    return instance;
  }

  sendToolInput(appId: string, toolName: string, args: ToolArgs, envelope: ArifOsEnvelope): void {
    const instance = this.apps.get(appId);
    if (!instance) throw new Error(`App not mounted: ${appId}`);

    this.postToView(instance, {
      jsonrpc: "2.0",
      method: "ui/notifications/tool-input",
      params: { arguments: args, tool: toolName },
    });

    this.postToView(instance, {
      jsonrpc: "2.0",
      method: "ui/notifications/tool-result",
      params: {
        content: [{ type: "text", text: envelope.summary }],
        structuredContent: { envelope },
        _meta: {
          ui: {
            resourceUri: `ui://geox/${appId}`,
            visibility: ["model", "app"],
          },
        },
      },
    });
  }

  sendHostContext(context: Record<string, unknown>): void {
    for (const [_appId, instance] of this.apps) {
      this.postToView(instance, {
        jsonrpc: "2.0",
        method: "ui/notifications/host-context-changed",
        params: context,
      });
    }
  }

  teardownApp(appId: string, reason?: string): void {
    const instance = this.apps.get(appId);
    if (!instance) return;

    this.postToView(instance, {
      jsonrpc: "2.0",
      method: "ui/resource-teardown",
      params: { reason: reason || "host teardown" },
    });

    if (instance.messageHandler) {
      window.removeEventListener("message", instance.messageHandler);
    }
    instance.container.remove();
    this.apps.delete(appId);
  }

  getGovernanceState(_appId: string): ArifOsEnvelope | null {
    return null;
  }

  // ── Private ────────────────────────────────────────────────────────────

  private wireMessageListener(instance: MCPAppInstance, options?: MountOptions): void {
    // EXPECTED_HOST_ORIGIN: secondary check after event.source.
    // Proxy iframe now has sandbox="allow-scripts" (no allow-same-origin),
    // so event.origin will be "null". Accept either host origin or "null".
    const expectedHostOrigin: string = window.location.origin;

    const handler = (event: MessageEvent) => {
      // PRIMARY check: window identity (strong — cannot be spoofed)
      if (event.source !== instance.iframe.contentWindow) return;

      // SECONDARY check: origin validation (defense-in-depth)
      // Proxy has null origin (sandboxed, no allow-same-origin).
      // Accept "null" or the actual host origin.
      if (event.origin !== "null" && event.origin !== expectedHostOrigin) {
        console.warn(`[MCP App:${instance.appId}] dropped message from unexpected origin:`, event.origin);
        return;
      }

      const data = parseJsonRpcMessage(event.data);
      if (!data) return;

      const method = data.method || "";

      // G3 sandbox control plane
      if (SANDBOX_METHODS.has(method)) {
        if (method === "ui/notifications/sandbox-ready") {
          instance.guestLoaded = true;
        }
        // sandbox-boot: guest not loaded yet; load is triggered by iframe load event
        return;
      }

      // Response correlation
      if (typeof data.id === "number" && (data.result !== undefined || data.error !== undefined)) {
        const pending = instance.pendingRequests.get(data.id);
        if (pending) {
          instance.pendingRequests.delete(data.id);
          if (data.error) {
            pending.reject(new Error(data.error.message ?? "RPC error"));
          } else {
            pending.resolve(data.result);
          }
        }
        return;
      }

      // Allowlist View methods only
      if (method && !ALLOWED_VIEW_METHODS.has(method)) {
        console.warn(`[MCP App:${instance.appId}] dropped method (not allowlisted):`, method);
        return;
      }

      void this.handleViewMethod(instance, data, options);
    };

    window.addEventListener("message", handler);
    instance.messageHandler = handler;
  }

  private async handleViewMethod(
    instance: MCPAppInstance,
    msg: JsonRpcMessage,
    options?: MountOptions,
  ): Promise<void> {
    switch (msg.method) {
      case "ui/initialize": {
        this.postToView(instance, {
          jsonrpc: "2.0",
          id: msg.id,
          result: {
            protocolVersion: "2026-01-26",
            hostCapabilities: {
              serverTools: {},
              serverResources: {},
              logging: {},
              sandbox: { g3: true, doubleIframe: true },
            },
            hostInfo: { name: "aaa-host", version: "1.1.0-g3" },
            hostContext: {
              theme: document.documentElement.getAttribute("data-theme") || "dark",
              displayMode: options?.displayMode || "inline",
              platform: "desktop",
            },
          },
        });
        break;
      }

      case "ui/notifications/initialized": {
        instance.state = "ready";
        options?.onReady?.();
        break;
      }

      case "tools/call": {
        const toolName = typeof msg.params?.name === "string" ? msg.params.name : undefined;
        const toolArgs = isRecord(msg.params?.arguments) ? msg.params.arguments : {};
        if (this.toolCallHandler && toolName) {
          try {
            const result = await this.toolCallHandler(instance.appId, toolName, toolArgs);
            this.postToView(instance, {
              jsonrpc: "2.0",
              id: msg.id,
              result,
            });
          } catch (err: unknown) {
            this.postToView(instance, {
              jsonrpc: "2.0",
              id: msg.id,
              error: { code: -32603, message: errorMessage(err, "Tool call failed") },
            });
          }
        } else {
          this.postToView(instance, {
            jsonrpc: "2.0",
            id: msg.id,
            error: {
              code: -32601,
              message: "tools/call handler not registered — wire arifOS path",
            },
          });
        }
        break;
      }

      case "resources/read": {
        this.postToView(instance, {
          jsonrpc: "2.0",
          id: msg.id,
          error: { code: -32601, message: "resources/read not implemented in host bridge" },
        });
        break;
      }

      case "ui/update-model-context": {
        const sc = msg.params?.structuredContent;
        const envelope = isRecord(sc) ? sc.envelope : null;
        if (envelope) {
          this.toolResultHandler?.(instance.appId, envelope);
        }
        this.postToView(instance, {
          jsonrpc: "2.0",
          id: msg.id,
          result: { ok: true },
        });
        break;
      }

      case "ui/open-link": {
        // Host-mediated open only (never guest navigation)
        const url = msg.params?.url;
        if (typeof url === "string" && /^https?:\/\//i.test(url)) {
          window.open(url, "_blank", "noopener,noreferrer");
        }
        break;
      }

      case "ui/message": {
        console.log(
          `[MCP App:${instance.appId}]`,
          msg.params?.level || "info",
          msg.params?.message || "",
        );
        break;
      }
    }
  }

  /**
   * Post to Sandbox Proxy (forwards to guest except sandbox-* control).
   *
   * Uses "*" targetOrigin because the proxy iframe has sandbox="allow-scripts"
   * (no allow-same-origin), giving it a null/unique origin. A specific
   * targetOrigin would silent-drop the message.
   *
   * Safe because:
   *   1. instance.iframe.contentWindow is a reference WE created — we know
   *      exactly which window receives the message
   *   2. The proxy validates ev.source === parent before acting (identity check)
   *   3. The guest has connect-src 'none' — cannot exfiltrate even if it
   *      receives data through other channels
   */
  private postToProxy(instance: MCPAppInstance, payload: Record<string, unknown>): void {
    if (instance.iframe?.contentWindow) {
      instance.iframe.contentWindow.postMessage(payload, "*");
    }
  }

  /** Post to View via proxy (alias for host→guest traffic). */
  private postToView(instance: MCPAppInstance, payload: Record<string, unknown>): void {
    this.postToProxy(instance, payload);
  }
}

// ── Governance envelope parser ─────────────────────────────────────────────

export function parseGovernanceEnvelope(envelope: ArifOsEnvelope | null): {
  policyState: ArifOsPolicyState;
  isVetoed: boolean;
  isHeld: boolean;
  blockingHolds: ArifOsHold[];
  disabledActions: string[];
  requiredFloors: string[];
} {
  if (!envelope) {
    return {
      policyState: "observe",
      isVetoed: false,
      isHeld: false,
      blockingHolds: [],
      disabledActions: [],
      requiredFloors: [],
    };
  }

  const constraints = envelope.constraints || {
    policyState: "observe",
    disabledActions: [],
    requiredFloors: [],
    veto: { active: false, reason: null, authority: null },
  };
  const holds = Array.isArray(envelope.holds) ? envelope.holds : [];
  const blockingHolds = holds.filter((h) => h.blocking !== false);
  const isVetoed = constraints.veto?.active === true;
  const isHeld = blockingHolds.length > 0;

  return {
    policyState: constraints.policyState || "observe",
    isVetoed,
    isHeld,
    blockingHolds,
    disabledActions: constraints.disabledActions || [],
    requiredFloors: constraints.requiredFloors || [],
  };
}
