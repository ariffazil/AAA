/**
 * MCP Apps Host Bridge — AAA Side
 * =================================
 * Host-side implementation of SEP-1865 ext-apps protocol.
 * Manages iframe lifecycle, ui:// resource resolution,
 * tool input/output relay, and governance envelope parsing.
 *
 * Contracts:
 *   - Resolves ui://geox/well-desk → /mcp-apps/well-desk
 *   - Sends ui/notifications/tool-input, ui/notifications/tool-result
 *   - Receives tools/call, resources/read, ui/update-model-context
 *   - Parses holds[], constraints{} from structuredContent.envelope
 *
 * DITEMPA BUKAN DIBERI
 */

// ── Types (mirrors arifOS envelope schema) ─────────────────────────────────

export type ArifOsPolicyState =
  | 'observe'
  | 'review_required'
  | 'hold'
  | 'veto'
  | 'approved'
  | 'rejected';

export interface ArifOsHold {
  code: string;
  reason: string;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  blocking: boolean;
  requiredWitness?: Array<'human' | 'ai' | 'earth'>;
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
  'geox/well-desk': '/mcp-apps/well-desk',
  'geox/earth-volume': '/mcp-apps/earth-volume',
  'geox/judge-console': '/mcp-apps/judge-console',
};

/** Resolve a ui:// URI to the AAA fetch path */
export function resolveUiResource(uri: string): string | null {
  if (!uri.startsWith('ui://')) return null;
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
  displayMode?: 'inline' | 'fullscreen';
  initialToolInput?: ToolArgs;
  onReady?: () => void;
}

interface JsonRpcMessage {
  jsonrpc: '2.0';
  id?: JsonRpcId;
  method?: string;
  params?: Record<string, unknown>;
  result?: unknown;
  error?: { message?: string };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object';
}

function parseJsonRpcMessage(value: unknown): JsonRpcMessage | null {
  let parsed: unknown = value;
  if (typeof value === 'string') {
    try {
      parsed = JSON.parse(value) as unknown;
    } catch {
      return null;
    }
  }
  if (!isRecord(parsed) || parsed.jsonrpc !== '2.0') return null;
  return parsed as JsonRpcMessage;
}

function errorMessage(error: unknown, fallback = 'Unknown error'): string {
  return error instanceof Error ? error.message : fallback;
}

export interface MCPAppInstance {
  appId: string;
  iframe: HTMLIFrameElement;
  container: HTMLElement;
  state: 'initializing' | 'ready' | 'error' | 'teardown';
  pendingRequests: Map<number, PendingRequest>;
  nextId: number;
  messageHandler?: (event: MessageEvent) => void;
}

export class MCPAppsHostBridge {
  private apps: Map<string, MCPAppInstance> = new Map();
  private toolResultHandler: ((appId: string, result: unknown) => void) | null = null;
  private toolCallHandler: ((appId: string, name: string, args: ToolArgs) => Promise<unknown>) | null = null;

  constructor(private hostElement: HTMLElement) {}

  /** Register handler for tool results coming FROM the View */
  onToolResult(handler: (appId: string, result: unknown) => void): void {
    this.toolResultHandler = handler;
  }

  /** Register handler for tool calls coming FROM the View (e.g., promote claim) */
  onToolCall(handler: (appId: string, name: string, args: ToolArgs) => Promise<unknown>): void {
    this.toolCallHandler = handler;
  }

  /**
   * Mount an MCP App in an iframe.
   * @param appId - e.g. "well-desk"
   * @param options - display mode, initial tool input, etc.
   */
  mountApp(appId: string, options?: MountOptions): MCPAppInstance {
    const fetchPath = UI_RESOURCE_ROOTS[`geox/${appId}`] || `/mcp-apps/${appId}`;

    // Create container
    const container = document.createElement('div');
    container.className = 'mcp-app-container';
    container.dataset.appId = appId;
    container.style.cssText = options?.displayMode === 'fullscreen'
      ? 'position:fixed;inset:0;z-index:9999;background:#000;'
      : 'width:100%;height:100%;min-height:400px;position:relative;';

    // Create iframe
    const iframe = document.createElement('iframe');
    iframe.src = fetchPath;
    iframe.style.cssText = 'width:100%;height:100%;border:none;';
    iframe.setAttribute('allow', 'clipboard-read; clipboard-write');
    iframe.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-forms allow-popups');
    container.appendChild(iframe);
    this.hostElement.appendChild(container);

    const instance: MCPAppInstance = {
      appId,
      iframe,
      container,
      state: 'initializing',
      pendingRequests: new Map(),
      nextId: 1,
    };
    this.apps.set(appId, instance);

    // Wire postMessage listener
    this.wireMessageListener(instance, options);
    return instance;
  }

  /**
   * Send tool input to the View (triggers the View to update)
   */
  sendToolInput(appId: string, toolName: string, args: ToolArgs, envelope: ArifOsEnvelope): void {
    const instance = this.apps.get(appId);
    if (!instance) throw new Error(`App not mounted: ${appId}`);

    // First send the tool input
    this.postToView(instance, {
      jsonrpc: '2.0',
      method: 'ui/notifications/tool-input',
      params: { arguments: args },
    });

    // Then send the result with governance envelope
    this.postToView(instance, {
      jsonrpc: '2.0',
      method: 'ui/notifications/tool-result',
      params: {
        content: [{ type: 'text', text: envelope.summary }],
        structuredContent: { envelope },
        _meta: {
          ui: {
            resourceUri: `ui://geox/${appId}`,
            visibility: ['model', 'app'],
          },
        },
      },
    });
  }

  /**
   * Send a host context change notification to all apps
   */
  sendHostContext(context: Record<string, unknown>): void {
    for (const [_appId, instance] of this.apps) {
      this.postToView(instance, {
        jsonrpc: '2.0',
        method: 'ui/notifications/host-context-changed',
        params: context,
      });
    }
  }

  /**
   * Teardown an app
   */
  teardownApp(appId: string, reason?: string): void {
    const instance = this.apps.get(appId);
    if (!instance) return;

    this.postToView(instance, {
      jsonrpc: '2.0',
      method: 'ui/resource-teardown',
      params: { reason: reason || 'host teardown' },
    });

    if (instance.messageHandler) {
      window.removeEventListener('message', instance.messageHandler);
    }
    instance.container.remove();
    this.apps.delete(appId);
  }

  /**
   * Get the governance state of a specific app (last known)
   */
  getGovernanceState(_appId: string): ArifOsEnvelope | null {
    // This would ideally be stored per-app. For now returns null.
    return null;
  }

  // ── Private helpers ────────────────────────────────────────────────────

  private wireMessageListener(instance: MCPAppInstance, options?: MountOptions): void {
    const handler = (event: MessageEvent) => {
      if (event.source !== instance.iframe.contentWindow) return;

      // Must be JSON-RPC 2.0
      const data = parseJsonRpcMessage(event.data);
      if (!data) return;

      // Response correlation
      if (typeof data.id === 'number' && (data.result !== undefined || data.error !== undefined)) {
        const pending = instance.pendingRequests.get(data.id);
        if (pending) {
          instance.pendingRequests.delete(data.id);
          if (data.error) {
            pending.reject(new Error(data.error.message ?? 'RPC error'));
          } else {
            pending.resolve(data.result);
          }
        }
        return;
      }

      // Handle View-initiated methods
      this.handleViewMethod(instance, data, options);
    };

    window.addEventListener('message', handler);
    // Store reference for cleanup
    instance.messageHandler = handler;
  }

  private async handleViewMethod(instance: MCPAppInstance, msg: JsonRpcMessage, options?: MountOptions): Promise<void> {
    switch (msg.method) {
      case 'ui/initialize': {
        // Reply with host capabilities
        this.postToView(instance, {
          jsonrpc: '2.0',
          id: msg.id,
          result: {
            protocolVersion: '2026-01-26',
            hostCapabilities: {
              serverTools: {},
              serverResources: {},
              logging: {},
              sandbox: {},
            },
            hostInfo: { name: 'aaa-host', version: '1.0.0' },
            hostContext: {
              theme: document.documentElement.getAttribute('data-theme') || 'dark',
              displayMode: options?.displayMode || 'inline',
              platform: 'desktop',
            },
          },
        });
        break;
      }

      case 'ui/notifications/initialized': {
        instance.state = 'ready';
        options?.onReady?.();
        break;
      }

      case 'tools/call': {
        // View wants to call a server tool (e.g., geox_claim_create)
        const toolName = typeof msg.params?.name === 'string' ? msg.params.name : undefined;
        const toolArgs = isRecord(msg.params?.arguments) ? msg.params.arguments : {};
        if (this.toolCallHandler && toolName) {
          try {
            const result = await this.toolCallHandler(instance.appId, toolName, toolArgs);
            this.postToView(instance, {
              jsonrpc: '2.0',
              id: msg.id,
              result,
            });
          } catch (err: unknown) {
            this.postToView(instance, {
              jsonrpc: '2.0',
              id: msg.id,
              error: { code: -32603, message: errorMessage(err, 'Tool call failed') },
            });
          }
        }
        break;
      }

      case 'resources/read': {
        // View requests a resource read
        this.postToView(instance, {
          jsonrpc: '2.0',
          id: msg.id,
          error: { code: -32601, message: 'resources/read not implemented in host bridge' },
        });
        break;
      }

      case 'ui/update-model-context': {
        // View shares updated model context
        const sc = msg.params?.structuredContent;
        const envelope = isRecord(sc) ? sc.envelope : null;
        if (envelope) {
          this.toolResultHandler?.(instance.appId, envelope);
        }
        this.postToView(instance, {
          jsonrpc: '2.0',
          id: msg.id,
          result: { ok: true },
        });
        break;
      }

      case 'ui/open-link': {
        // View wants to open a link
        const url = msg.params?.url;
        if (typeof url === 'string') window.open(url, '_blank');
        break;
      }

      case 'ui/message': {
        // View sends a log message
        console.log(`[MCP App:${instance.appId}]`, msg.params?.level || 'info',
          msg.params?.message || '');
        break;
      }
    }
  }

  private postToView(instance: MCPAppInstance, payload: Record<string, unknown>): void {
    if (instance.iframe?.contentWindow) {
      instance.iframe.contentWindow.postMessage(payload, window.location.origin);
    }
  }
}

// ── Governance envelope parser ─────────────────────────────────────────────

/**
 * Parse an arifOS envelope and return the rendering hints.
 * Used by the AAA React cockpit to render F13 veto / 888 HOLD states.
 */
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
      policyState: 'observe',
      isVetoed: false,
      isHeld: false,
      blockingHolds: [],
      disabledActions: [],
      requiredFloors: [],
    };
  }

  const constraints = envelope.constraints || { policyState: 'observe', disabledActions: [], requiredFloors: [], veto: { active: false } };
  const holds = Array.isArray(envelope.holds) ? envelope.holds : [];
  const blockingHolds = holds.filter(h => h.blocking !== false);
  const isVetoed = constraints.veto?.active === true;
  const isHeld = blockingHolds.length > 0;

  return {
    policyState: constraints.policyState || 'observe',
    isVetoed,
    isHeld,
    blockingHolds,
    disabledActions: constraints.disabledActions || [],
    requiredFloors: constraints.requiredFloors || [],
  };
}
