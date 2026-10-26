// Server-side read proxy. Allowlist only; upstream payload never passes through.
const UPSTREAM = process.env.COCKPIT_STATUS_URL || "https://arif-fazil.com/arifos/public-truth.json";
export function pick(env) {
  const f = (env.custody && env.custody.floors && env.custody.floors.summary) || {};
  const cap = env.capability || {};
  return [
    { label: "Floors", ...f },
    { label: "Callable tools", ...(cap.callable || {}) },
    { label: "Declared tools", ...(cap.declared || {}) },
    { label: "Kernel", ...((env.custody && env.custody.kernel_status) || {}) },
    { label: "Open findings", ...((env.safety && env.safety.open_findings) || {}) },
  ];
}
export default async function handler(req, res) {
  res.setHeader("Cache-Control", "private, no-store");
  if (req.method !== "GET") return res.status(405).json({ state: "unavailable", reason: "method" });
  try {
    const r = await fetch(UPSTREAM, { signal: AbortSignal.timeout(6000) });
    if (!r.ok) throw new Error(`upstream ${r.status}`);
    const env = await r.json();
    const observed = env.generated_at || null;
    const age = observed ? (Date.now() - Date.parse(observed)) / 60000 : Infinity;
    return res.status(200).json({
      state: !observed ? "unmeasured" : age > 15 ? "stale" : "fresh",
      observed_at: observed,
      source: UPSTREAM.replace(/^https?:\/\//, ""),
      cards: pick(env),
      snapshot_hash: env.snapshot_hash || null,
    });
  } catch (e) {
    return res.status(200).json({ state: "unavailable", observed_at: null, source: "upstream",
                                  cards: [], reason: String(e.message || e) });
  }
}
