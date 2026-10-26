import { stateOf, nextInterval, shouldPoll, card, STALE_AFTER_MS } from "./app.js";
import { pick } from "./api/status.js";
import { relevant } from "./ignore-build.mjs";
import cfg from "./vercel.json" with { type: "json" };
const NOW = Date.parse("2026-10-26T06:00:00Z");
let pass = 0, fail = 0;
const t = (name, fn) => { try { fn(); console.log("PASS", name); pass++; }
  catch (e) { console.log("FAIL", name, "—", e.message); fail++; } };
const eq = (a, b, m) => { if (a !== b) throw new Error(`${m || ""} got ${JSON.stringify(a)} want ${JSON.stringify(b)}`); };
t("fresh", () => eq(stateOf("2026-10-26T05:59:30Z", NOW), "fresh"));
t("stale", () => eq(stateOf("2026-10-26T05:50:00Z", NOW), "stale"));
t("unmeasured null", () => eq(stateOf(null, NOW), "unmeasured"));
t("unmeasured garbage", () => eq(stateOf("bukan-tarikh", NOW), "unmeasured"));
t("staleness boundary is 120s", () => eq(STALE_AFTER_MS, 120000));
t("no timestamp => unmeasured card", () => { const c = card("X", { value: 1, source: "s" }, NOW); eq(c.state, "unmeasured"); eq(c.observedAt, null); });
t("hidden tab stops polling", () => eq(shouldPoll({ hidden: true }), false));
t("offline stops polling", () => eq(shouldPoll({ online: false }), false));
t("backoff 30->60->120->240 cap", () => { eq(nextInterval(0),30000); eq(nextInterval(1),60000); eq(nextInterval(2),120000); eq(nextInterval(3),240000); eq(nextInterval(9),240000); });
t("allowlist strips unknown keys", () => {
  const flat = JSON.stringify(pick({ custody:{ floors:{summary:{value:{measured:11},source:"k",observed_at:"t"}}, kernel_status:{value:"degraded"} },
    capability:{ callable:{value:9}, declared:{value:49} }, safety:{ open_findings:{value:5} }, orgs:{ secret_token:"LEAK" } }));
  if (flat.includes("LEAK") || flat.includes("secret_token")) throw new Error("leaked");
  if (!flat.includes("Callable tools")) throw new Error("missing card");
});
t("api not swallowed by SPA fallback", () => {
  const c = cfg.rewrites.find((r) => r.destination === "/index.html");
  if (!c.source.includes("(?!api/)")) throw new Error("catch-all swallows /api");
});
t("unrelated diff skips build", () => eq(relevant(["docs/readme.md","src/Cockpit.tsx"]), false));
t("cockpit diff builds", () => eq(relevant(["cockpit-pilot/app.js"]), true));
console.log(`\n${pass} passed, ${fail} failed`);
process.exitCode = fail ? 1 : 0;
