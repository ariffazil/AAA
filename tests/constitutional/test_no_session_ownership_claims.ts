/**
 * covenant/test_no_session_ownership_claims.ts
 * ============================================================================
 * Binding tests for /root/AAA/contracts/AAA_SHARED_SESSION_COVENANT.md.
 *
 * Verifies:
 *   1. Covenant document exists and seals F13 + cites v1.
 *   2. Every agent card under /root/AAA/agents/* declares the covenant
 *      and sets `session_ownership.mode = "shared"`.
 *   3. The denylist regex matches forbidden phrases (EN + Bahasa).
 *   4. No agent card description / principal_agent claims ownership phrases.
 *   5. AAA doctrine files do not contain forbidden phrases.
 *   6. Covenant is additive — never edits core/laws.py or FLOOR_TABLE.json.
 *
 * Read-only; never mutates agent cards.
 *
 * Run:  npx tsx tests/covenant/test_no_session_ownership_claims.ts
 * DITEMPA BUKAN DIBERI
 */

import { describe, it } from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import path from "node:path";

const COVENANT_PATH = "/root/AAA/contracts/AAA_SHARED_SESSION_COVENANT.md";
const AGENTS_DIR = "/root/AAA/agents";
const COVENANT_VERSION = "AAA_SHARED_SESSION_COVENANT@v1";

const DENYLIST: RegExp[] = [
  /\bmy session\b/i,
  /\bmy work\b/i,
  /\bmy fix\b/i,
  /\bmy state\b/i,
  /\bmy context\b/i,
  /\bmy output\b/i,
  /\bini sesi saya\b/i,
  /\bkarya saya\b/i,
  /\bi am 888\b/i,
  /\bi own AAA\b/i,
];

function listAgentCards(): string[] {
  if (!fs.existsSync(AGENTS_DIR)) return [];
  return fs
    .readdirSync(AGENTS_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => path.join(AGENTS_DIR, d.name, "agent-card.json"))
    .filter((p) => fs.existsSync(p));
}

describe("AAA_SHARED_SESSION_COVENANT@v1", () => {
  it("covenant document exists and seals F13", () => {
    assert.ok(fs.existsSync(COVENANT_PATH), "covenant document missing");
    const text = fs.readFileSync(COVENANT_PATH, "utf8");
    assert.match(text, /DITEMPA BUKAN DIBERI/);
    assert.match(text, /F13 SOVEREIGN/);
    assert.match(text, new RegExp(COVENANT_VERSION));
  });

  it("denylist regex matches forbidden phrases (EN + Bahasa)", () => {
    assert.ok(DENYLIST.some((r) => r.test("This is my session, bro.")));
    assert.ok(DENYLIST.some((r) => r.test("Saya rasa ini sesi saya.")));
    assert.ok(DENYLIST.some((r) => r.test("I am 888 (joking)")));
    assert.ok(!DENYLIST.some((r) => r.test("the kernel owns the session")));
  });

  it("every agent card binds the covenant", () => {
    const cards = listAgentCards();
    assert.ok(cards.length > 0, "no agent cards under /root/AAA/agents/*");
    for (const card of cards) {
      const d = JSON.parse(fs.readFileSync(card, "utf8"));
      const covenants: string[] = d.covenants ?? [];
      assert.ok(
        covenants.includes(COVENANT_VERSION),
        `${path.basename(path.dirname(card))} missing covenant binding`,
      );
      const so = d.session_ownership ?? {};
      assert.strictEqual(so.mode, "shared", `${card} mode != shared`);
      assert.strictEqual(so.steward_window, "1_cycle", `${card} steward_window`);
    }
  });

  it("agent cards do not claim ownership of session or self-as-888", () => {
    for (const card of listAgentCards()) {
      const d = JSON.parse(fs.readFileSync(card, "utf8"));
      const haystack = [
        d.name ?? "",
        d.principal_agent?.type ?? "",
        d.principal_agent?.category ?? "",
        d.description ?? "",
      ].join(" ");
      for (const r of DENYLIST) {
        assert.ok(
          !r.test(haystack),
          `${path.basename(path.dirname(card))} violates covenant: ${haystack}`,
        );
      }
    }
  });

  it("AAA doctrine files are clean of forbidden phrases", () => {
    const doctrine = [
      "/root/AAA/CLAUDE.md",
      "/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md",
    ].filter((p) => fs.existsSync(p));
    for (const p of doctrine) {
      const text = fs.readFileSync(p, "utf8");
      for (const r of DENYLIST) {
        assert.ok(
          !r.test(text),
          `${p} contains forbidden phrase matching ${r}`,
        );
      }
    }
  });

  it("covenant is additive and does not edit kernel files", () => {
    const text = fs.readFileSync(COVENANT_PATH, "utf8");
    assert.ok(!text.includes("core/laws.py"), "covenant must not edit kernel law");
    assert.ok(!text.includes("FLOOR_TABLE.json"), "covenant must not edit floor table");
  });
});
