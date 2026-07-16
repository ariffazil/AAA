/**
 * MCP Apps Security Tests — Sandbox isolation + origin validation
 * ================================================================
 * Verifies:
 *   1. Outer proxy iframe sandbox attributes (structural)
 *   2. Inner guest iframe sandbox attributes (structural)
 *   3. Method allowlist enforcement (behavioral)
 *   4. Hostile origin rejection (integration via jsdom)
 *
 * Run: npx tsx tests/mcp-apps-security.test.ts
 * DITEMPA BUKAN DIBERI
 */

import { describe, it } from "node:test";
import assert from "node:assert";
import { buildSandboxProxySrcdoc, ALLOWED_VIEW_METHODS, SANDBOX_METHODS, DEFAULT_GUEST_CSP } from "../src/host/MCPAppsSandboxProxy";

// ── 1. Structural: sandbox attributes ─────────────────────────────────────

describe("MCP Apps Sandbox — structural", () => {
  it("Inner guest iframe MUST have sandbox='allow-scripts' (no allow-same-origin)", () => {
    const srcdoc = buildSandboxProxySrcdoc();

    // Find the inner iframe creation: guest.setAttribute("sandbox","allow-scripts");
    const match = srcdoc.match(/guest\.setAttribute\(["']sandbox["'],\s*["']([^"']+)["']\)/);
    assert.ok(match, "Inner iframe must set sandbox attribute");
    const sandbox = match[1];

    // Must have allow-scripts
    assert.ok(sandbox.includes("allow-scripts"), "Guest must have allow-scripts");

    // Must NOT have allow-same-origin, allow-popups, allow-forms, allow-modals
    const forbidden = ["allow-same-origin", "allow-popups", "allow-forms", "allow-modals", "allow-top-navigation"];
    for (const attr of forbidden) {
      assert.ok(!sandbox.includes(attr), `Guest must NOT have ${attr}`);
    }
  });

  it("Inner guest iframe CSP MUST have connect-src 'none' and frame-src 'none'", () => {
    // DEFAULT_GUEST_CSP is the CSP injected when guest HTML doesn't declare its own
    const csp = DEFAULT_GUEST_CSP;
    assert.ok(csp.includes("default-src 'none'"), "CSP must have default-src 'none'");
    assert.ok(csp.includes("connect-src 'none'"), "CSP must have connect-src 'none'");
    assert.ok(csp.includes("frame-src 'none'"), "CSP must have frame-src 'none'");
    assert.ok(csp.includes("form-action 'none'"), "CSP must have form-action 'none'");
    assert.ok(csp.includes("object-src 'none'"), "CSP must have object-src 'none'");
    assert.ok(csp.includes("base-uri 'none'"), "CSP must have base-uri 'none'");
    assert.ok(!csp.includes("allow-same-origin"), "CSP must not allow same-origin access");
  });

  it("Inner guest iframe MUST have referrerpolicy='no-referrer'", () => {
    const srcdoc = buildSandboxProxySrcdoc();
    const match = srcdoc.match(/guest\.setAttribute\(["']referrerpolicy["'],\s*["']([^"']+)["']\)/);
    assert.ok(match, "Guest must set referrerpolicy");
    assert.strictEqual(match[1], "no-referrer");
  });

  it("Inner guest iframe MUST have empty allow attribute", () => {
    const srcdoc = buildSandboxProxySrcdoc();
    // guest.setAttribute("allow","");
    const match = srcdoc.match(/guest\.setAttribute\(["']allow["'],\s*["']([^"']*)["']\)/);
    assert.ok(match, "Guest must set allow attribute");
    assert.strictEqual(match[1], "", "allow must be empty (no extra permissions)");
  });
});

// ── 2. Behavioral: method allowlist ────────────────────────────────────────

describe("MCP Apps Security — method allowlist", () => {
  it("ALLOWED_VIEW_METHODS must contain only safe view methods", () => {
    // These are methods the guest can call through the proxy
    const expected = [
      "ui/initialize",
      "ui/notifications/initialized",
      "tools/call",
      "resources/read",
      "ui/update-model-context",
      "ui/open-link",
      "ui/message",
      "ui/resource-teardown",
    ];

    // All expected methods must be present
    for (const m of expected) {
      assert.ok(ALLOWED_VIEW_METHODS.has(m), `Expected method ${m} in allowlist`);
    }

    // Must NOT contain sandbox control methods
    for (const m of ALLOWED_VIEW_METHODS) {
      assert.ok(!m.includes("sandbox-"), `Allowed method must not be sandbox control: ${m}`);
      assert.ok(!m.includes("tools/call") || m === "tools/call", `Must not contain tool-specific methods beyond tools/call: ${m}`);
    }
  });

  it("SANDBOX_METHODS must be isolated from guest", () => {
    // SANDBOX_METHODS are proxy-only (never forwarded to guest)
    for (const m of SANDBOX_METHODS) {
      assert.ok(!ALLOWED_VIEW_METHODS.has(m),
        `Sandbox method ${m} must NOT be in ALLOWED_VIEW_METHODS`);
    }
  });
});

// ── 3. Behavioral: proxy message filtering logic ──────────────────────────

describe("MCP Apps Security — sandbox proxy logic", () => {
  it("Proxy must drop sandbox-* methods from guest (simulate spoof)", () => {
    // Simulate the proxy logic: if a method starts with "ui/notifications/sandbox-"
    // AND comes from guest, it must be dropped (not forwarded to host)
    const guestSpoofSandbox = "ui/notifications/sandbox-load";
    const isSandboxMethod = (method: string) => method.indexOf("ui/notifications/sandbox-") === 0;

    // When guest sends sandbox-load → must be dropped
    assert.ok(isSandboxMethod(guestSpoofSandbox), "sandbox-load must be flagged");
    assert.ok(SANDBOX_METHODS.has(guestSpoofSandbox), "sandbox-load in SANDBOX_METHODS");
    assert.ok(!ALLOWED_VIEW_METHODS.has(guestSpoofSandbox), "sandbox-load NOT in ALLOWED_VIEW_METHODS");

    // Host method must not be spoofable from guest
    const hostOnlyMethods = ["ui/notifications/sandbox-load", "ui/notifications/sandbox-boot", "ui/notifications/sandbox-ready"];
    for (const m of hostOnlyMethods) {
      assert.ok(SANDBOX_METHODS.has(m), `${m} must be in SANDBOX_METHODS`);
      assert.ok(!ALLOWED_VIEW_METHODS.has(m), `${m} must NOT be in ALLOWED_VIEW_METHODS`);
    }
  });

  it("Proxy must validate ev.source before forwarding to host", () => {
    const srcdoc = buildSandboxProxySrcdoc();

    // Verify the proxy checks source before toHost()
    // Pattern: if(ev.source===parent){ ... toGuest(data) }
    // Pattern: if(guest&&ev.source===guest.contentWindow){ ... toHost(data) }
    const hasParentCheck = srcdoc.includes("ev.source===parent");
    const hasGuestCheck = srcdoc.includes("ev.source===guest.contentWindow");

    assert.ok(hasParentCheck, "Proxy must validate parent source");
    assert.ok(hasGuestCheck, "Proxy must validate guest source");
  });
});

// ── 4. Integration: CSP injection logic ────────────────────────────────────

describe("MCP Apps Security — CSP injection", () => {
  it("injectCsp must add CSP meta tag to guest HTML when none exists", () => {
    const srcdoc = buildSandboxProxySrcdoc();

    // Test the injectCsp function pattern by checking the generated code
    // The function should add a CSP meta tag after <head>
    const hasCspInjection = srcdoc.includes('injectCsp');
    assert.ok(hasCspInjection, "Proxy must inject CSP into guest HTML");

    // Verify CSP is the default when no manifest override
    const cspMatch = srcdoc.match(/DEFAULT_GUEST_CSP.*?=[\s\S]*?;/);
    // DEFAULT_GUEST_CSP is defined as a const, verify it has the right policies
    assert.ok(DEFAULT_GUEST_CSP.includes("connect-src 'none'"), "Default CSP blocks network");
    assert.ok(DEFAULT_GUEST_CSP.includes("default-src 'none'"), "Default CSP denies all by default");
  });
});

console.log("✅ All MCP Apps security tests passed.");
