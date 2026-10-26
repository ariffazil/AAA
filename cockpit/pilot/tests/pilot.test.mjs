import test from "node:test";
import assert from "node:assert/strict";
import { stateOf, nextInterval, shouldPoll, card, STALE_AFTER_MS } from "../app.js";
import { pick } from "../api/status.js";
import { relevant } from "../ignore-build.mjs";
import cfg from "../vercel.json" with { type: "json" };

const NOW = Date.parse("2026-10-26T06:00:00Z");
const at = (iso) => iso;

test("fresh vs stale vs unmeasured", () => {
  assert.equal(stateOf(at("2026-10-26T05:59:30Z"), NOW), "fresh");
  assert.equal(stateOf(at("2026-10-26T05:50:00Z"), NOW), "stale");
  assert.equal(stateOf(null, NOW), "unmeasured");
  assert.equal(stateOf("bukan-tarikh", NOW), "unmeasured");
  assert.ok(Date.parse("2026-10-26T05:50:00Z") < NOW - STALE_AFTER_MS);
});

test("a field without a timestamp is never shown fresh", () => {
  const c = card("X", { value: 1, source: "s" }, NOW);
  assert.equal(c.state, "unmeasured");
  assert.equal(c.observedAt, null);
});

test("hidden tab stops polling; offline stops polling", () => {
  assert.equal(shouldPoll({ hidden: true }), false);
  assert.equal(shouldPoll({ online: false }), false);
  assert.equal(shouldPoll({}), true);
});

test("backoff grows and is capped", () => {
  assert.equal(nextInterval(0), 30_000);
  assert.equal(nextInterval(1), 60_000);
  assert.equal(nextInterval(3), 240_000);
  assert.equal(nextInterval(9), 240_000);
});

test("allowlist proxy exposes only named fields", () => {
  const cards = pick({
    custody: { floors: { summary: { value: { measured: 11 }, source: "kernel", observed_at: "t" } }, kernel_status: { value: "degraded" } },
    capability: { callable: { value: 9 }, declared: { value: 49 } },
    safety: { open_findings: { value: 5 } },
    orgs: { secret_token: "LEAK" },
  });
  const flat = JSON.stringify(cards);
  assert.ok(!flat.includes("secret_token"));
  assert.ok(!flat.includes("LEAK"));
  assert.ok(flat.includes("Callable tools"));
});

test("api routes are not swallowed by the SPA fallback", () => {
  const catchAll = cfg.rewrites.find((r) => r.destination === "/index.html");
  assert.ok(catchAll.source.includes("(?!api/)"), "catch-all must exclude /api");
});

test("unrelated changes do not trigger a build; cockpit changes do", () => {
  assert.equal(relevant(["docs/readme.md", "src/Cockpit.tsx"]), false);
  assert.equal(relevant(["cockpit-pilot/app.js"]), true);
  assert.equal(relevant(["package.json"]), true);
});

test("ignore-build: no evidence never skips (Vercel no-argv trap fixed)", async () => {
  const { decide } = await import("../ignore-build.mjs");
  assert.equal(decide({ argvPaths: [], env: {} }).action, "build");
  assert.equal(decide({ argvPaths: [], env: {} }).reason, "no-change-evidence");
});

test("ignore-build: real repo path cockpit/pilot/ is relevant", async () => {
  const { relevant } = await import("../ignore-build.mjs");
  assert.equal(relevant(["cockpit/pilot/app.js"]), true);
  assert.equal(relevant(["cockpit-pilot/app.js"]), true); // legacy prefix kept
  assert.equal(relevant(["docs/readme.md"]), false);
});

test("ignore-build: git-diff lane fails safe when git is unavailable", async () => {
  const { decide } = await import("../ignore-build.mjs");
  const d = decide({
    argvPaths: [],
    env: { VERCEL_GIT_PREVIOUS_SHA: "no-such-sha", VERCEL_GIT_COMMIT_SHA: "also-no-such" },
  });
  assert.equal(d.action, "build");
  assert.equal(d.reason, "git-diff-unavailable");
});

test("ignore-build: argv lane still skips provably irrelevant changes", async () => {
  const { decide } = await import("../ignore-build.mjs");
  assert.equal(decide({ argvPaths: ["docs/x.md"] }).action, "skip");
  assert.equal(decide({ argvPaths: ["cockpit/pilot/app.js"] }).action, "build");
});
